# -*- coding: utf-8 -*-
"""Catalog CSV load — pure data, no xbmc*."""
import csv
import os
import re

YEAR_STEM_RE = re.compile(r"^\d{4}$")
VIDEO_ID_RE = re.compile(r"^[A-Za-z0-9_-]{11}$")


class Year(object):
    def __init__(self, id_, csv_path=None):
        self.id = id_
        self.csv_path = csv_path

    def __repr__(self):
        return "Year({0!r})".format(self.id)


class MusicVideo(object):
    def __init__(self, title, video_id, year_id):
        self.title = title
        self.video_id = video_id
        self.year_id = year_id

    def __repr__(self):
        return "MusicVideo({0!r}, {1!r})".format(self.title, self.video_id)


class CatalogError(object):
    def __init__(self, code, message, year_id=None, row=None):
        self.code = code
        self.message = message
        self.year_id = year_id
        self.row = row

    def __repr__(self):
        return "CatalogError({0!r}, {1!r})".format(self.code, self.message)


class CatalogLoadResult(object):
    def __init__(self, years=None, videos=None, errors=None, ok=True):
        self.years = years if years is not None else []
        self.videos = videos if videos is not None else []
        self.errors = errors if errors is not None else []
        self.ok = ok


def _row_raw(fields):
    return ";".join(fields)


def _parse_row(fields, year_id):
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


def _read_year_file(path, year_id):
    """Return (videos, errors). Raises OSError if the file cannot be read."""
    videos = []
    errors = []
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


def load_all_videos(csv_dir):
    """Legacy-shaped dict year_id -> tuple of raw field lists (unvalidated).

    Prefer ``list_years`` / ``load_year`` for validated results.
    """
    videoslists = {}
    if not os.path.isdir(csv_dir):
        return videoslists
    for filename in os.listdir(csv_dir):
        if not filename.endswith(".csv"):
            continue
        year_id = os.path.splitext(filename)[0]
        path = os.path.join(csv_dir, filename)
        with open(path, "r", encoding="utf-8", newline="") as csvfile:
            videoslists[year_id] = tuple(csv.reader(csvfile, delimiter=";"))
    return videoslists


def list_years(csv_dir):
    """List year stems under ``csv_dir`` without requiring song materialization API.

    Still may scan directory entries; returns ``Year`` objects and recoverable errors.
    """
    errors = []
    if not os.path.isdir(csv_dir):
        errors.append(
            CatalogError(
                "csv_dir_missing",
                "catalog directory missing: {0}".format(csv_dir),
            )
        )
        return CatalogLoadResult(years=[], errors=errors, ok=True)

    years = []
    for filename in os.listdir(csv_dir):
        if not filename.endswith(".csv"):
            continue
        stem = os.path.splitext(filename)[0]
        if not YEAR_STEM_RE.match(stem):
            continue
        years.append(Year(stem, csv_path=os.path.join(csv_dir, filename)))
    years.sort(key=lambda y: y.id)
    return CatalogLoadResult(years=years, errors=errors, ok=True)


def load_year(csv_dir, year_id):
    """Load and validate a single year CSV; omit bad rows into ``errors``."""
    errors = []
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
