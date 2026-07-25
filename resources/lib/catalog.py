# -*- coding: utf-8 -*-
"""Catalog CSV load — pure data, no xbmc*."""
from __future__ import annotations

import csv
import os
import re
from typing import List, Optional, Sequence, Tuple

YEAR_STEM_RE = re.compile(r"^\d{4}$")
VIDEO_ID_RE = re.compile(r"^[A-Za-z0-9_-]{11}$")


class Year(object):
    def __init__(self, id_: str, csv_path: Optional[str] = None) -> None:
        self.id = id_
        self.csv_path = csv_path

    def __repr__(self) -> str:
        return "Year({0!r})".format(self.id)


class MusicVideo(object):
    def __init__(self, title: str, video_id: str, year_id: str) -> None:
        self.title = title
        self.video_id = video_id
        self.year_id = year_id

    def __repr__(self) -> str:
        return "MusicVideo({0!r}, {1!r})".format(self.title, self.video_id)


class CatalogError(object):
    def __init__(
        self,
        code: str,
        message: str,
        year_id: Optional[str] = None,
        row: Optional[str] = None,
    ) -> None:
        self.code = code
        self.message = message
        self.year_id = year_id
        self.row = row

    def __repr__(self) -> str:
        return "CatalogError({0!r}, {1!r})".format(self.code, self.message)


class CatalogLoadResult(object):
    def __init__(
        self,
        years: Optional[List[Year]] = None,
        videos: Optional[List[MusicVideo]] = None,
        errors: Optional[List[CatalogError]] = None,
        ok: bool = True,
    ) -> None:
        self.years = years if years is not None else []
        self.videos = videos if videos is not None else []
        self.errors = errors if errors is not None else []
        self.ok = ok


def _row_raw(fields: Sequence[str]) -> str:
    return ";".join(fields)


def _parse_row(
    fields: Sequence[str], year_id: str
) -> Tuple[Optional[MusicVideo], Optional[CatalogError]]:
    """Return (MusicVideo|None, CatalogError|None)."""
    if len(fields) != 2:
        return None, CatalogError(
            "row_invalid",
            "expected exactly 2 fields, got {0}".format(len(fields)),
            year_id=year_id,
            row=_row_raw(fields),
        )
    title = (fields[0] or "").strip()
    video_id = (fields[1] or "").strip()
    if not title:
        return None, CatalogError(
            "row_invalid",
            "empty title",
            year_id=year_id,
            row=_row_raw(fields),
        )
    if not VIDEO_ID_RE.match(video_id):
        return None, CatalogError(
            "row_bad_video_id",
            "invalid video_id {0!r}".format(video_id),
            year_id=year_id,
            row=_row_raw(fields),
        )
    return MusicVideo(title, video_id, year_id), None


def _read_year_file(
    path: str, year_id: str
) -> Tuple[List[MusicVideo], List[CatalogError]]:
    """Return (videos, errors). Raises OSError if the file cannot be read."""
    videos: List[MusicVideo] = []
    errors: List[CatalogError] = []
    with open(path, "r", encoding="utf-8", newline="") as csvfile:
        for fields in csv.reader(csvfile, delimiter=";"):
            if not fields or (len(fields) == 1 and not fields[0].strip()):
                continue
            video, err = _parse_row(fields, year_id)
            if err is not None:
                errors.append(err)
            if video is not None:
                videos.append(video)
    videos.sort(key=lambda v: v.title)
    return videos, errors


def list_years(csv_dir: str) -> CatalogLoadResult:
    """List year stems under ``csv_dir`` without opening CSV contents (FR-008)."""
    errors: List[CatalogError] = []
    if not os.path.isdir(csv_dir):
        errors.append(
            CatalogError(
                "csv_dir_missing",
                "catalog directory missing: {0}".format(csv_dir),
            )
        )
        return CatalogLoadResult(years=[], errors=errors, ok=True)

    years: List[Year] = []
    for filename in os.listdir(csv_dir):
        if not filename.endswith(".csv"):
            continue
        stem = os.path.splitext(filename)[0]
        if not YEAR_STEM_RE.match(stem):
            continue
        years.append(Year(stem, csv_path=os.path.join(csv_dir, filename)))
    years.sort(key=lambda y: y.id)
    return CatalogLoadResult(years=years, errors=errors, ok=True)


def load_year(csv_dir: str, year_id: str) -> CatalogLoadResult:
    """Load and validate only ``{year_id}.csv`` (FR-009); omit bad rows into ``errors``."""
    errors: List[CatalogError] = []
    if not os.path.isdir(csv_dir):
        errors.append(
            CatalogError(
                "csv_dir_missing",
                "catalog directory missing: {0}".format(csv_dir),
                year_id=year_id,
            )
        )
        return CatalogLoadResult(videos=[], errors=errors, ok=True)

    path = os.path.join(csv_dir, "{0}.csv".format(year_id))
    if not os.path.isfile(path):
        errors.append(
            CatalogError(
                "year_missing",
                "year file not found: {0}".format(path),
                year_id=year_id,
            )
        )
        return CatalogLoadResult(videos=[], errors=errors, ok=True)

    try:
        videos, row_errors = _read_year_file(path, year_id)
    except OSError as exc:
        errors.append(
            CatalogError(
                "year_unreadable",
                "cannot read year file: {0}".format(exc),
                year_id=year_id,
            )
        )
        return CatalogLoadResult(videos=[], errors=errors, ok=True)

    errors.extend(row_errors)
    return CatalogLoadResult(videos=videos, errors=errors, ok=True)
