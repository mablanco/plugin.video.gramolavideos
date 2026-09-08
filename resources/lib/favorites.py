# -*- coding: utf-8 -*-
"""User favorites store — pure data, no xbmc*."""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

import catalog

STORE_VERSION = 1


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace(
        "+00:00", "Z"
    )


def _valid_year_id(year_id: str) -> bool:
    return bool(catalog.YEAR_STEM_RE.match(year_id or ""))


def _valid_video_id(video_id: str) -> bool:
    return bool(catalog.VIDEO_ID_RE.match(video_id or ""))


def _normalize_entry(raw: Any) -> Optional[Dict[str, str]]:
    if not isinstance(raw, dict):
        return None
    year_id = str(raw.get("year_id", "")).strip()
    video_id = str(raw.get("video_id", "")).strip()
    title = str(raw.get("title", "")).strip()
    added_at = str(raw.get("added_at", "")).strip()
    if not (
        _valid_year_id(year_id)
        and _valid_video_id(video_id)
        and title
        and added_at
    ):
        return None
    return {
        "year_id": year_id,
        "video_id": video_id,
        "title": title,
        "added_at": added_at,
    }


def load_store(path: str) -> List[Dict[str, str]]:
    """Load favorites from ``path``; missing/corrupt → empty list."""
    if not path or not os.path.isfile(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, ValueError, TypeError):
        return []
    if not isinstance(data, dict):
        return []
    raw_list = data.get("favorites")
    if not isinstance(raw_list, list):
        return []
    entries: List[Dict[str, str]] = []
    seen = set()
    for raw in raw_list:
        entry = _normalize_entry(raw)
        if entry is None:
            continue
        key = (entry["year_id"], entry["video_id"])
        if key in seen:
            continue
        seen.add(key)
        entries.append(entry)
    return entries


def save_store(path: str, favorites: List[Dict[str, str]]) -> None:
    """Persist favorites; creates parent directories as needed."""
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    payload = {"version": STORE_VERSION, "favorites": list(favorites)}
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def contains(path: str, year_id: str, video_id: str) -> bool:
    key = (str(year_id).strip(), str(video_id).strip())
    return any(
        (e["year_id"], e["video_id"]) == key for e in load_store(path)
    )


def add(
    path: str,
    catalog_dir: str,
    year_id: str,
    video_id: str,
    title: str,
) -> Tuple[bool, Optional[str]]:
    """Add favorite if catalog entry resolves. Idempotent on duplicate key."""
    year_id = (year_id or "").strip()
    video_id = (video_id or "").strip()
    title = (title or "").strip()
    if not _valid_year_id(year_id) or not _valid_video_id(video_id):
        return False, "invalid_ids"
    if not title:
        return False, "empty_title"
    if contains(path, year_id, video_id):
        return True, None
    result = catalog.load_year(catalog_dir, year_id)
    if not any(v.video_id == video_id for v in result.videos):
        return False, "not_in_catalog"
    # Prefer live catalog title when available.
    for video in result.videos:
        if video.video_id == video_id:
            title = video.title
            break
    favorites = load_store(path)
    favorites.append(
        {
            "year_id": year_id,
            "video_id": video_id,
            "title": title,
            "added_at": _utc_now_iso(),
        }
    )
    try:
        save_store(path, favorites)
    except OSError:
        return False, "io_error"
    return True, None


def remove(path: str, year_id: str, video_id: str) -> bool:
    """Remove favorite by key; idempotent. Does not touch CSV."""
    year_id = (year_id or "").strip()
    video_id = (video_id or "").strip()
    favorites = load_store(path)
    kept = [
        e
        for e in favorites
        if not (e["year_id"] == year_id and e["video_id"] == video_id)
    ]
    if len(kept) == len(favorites):
        return True
    try:
        save_store(path, kept)
    except OSError:
        return False
    return True


def list_resolved(
    path: str, catalog_dir: str
) -> Tuple[List[Dict[str, Any]], List[Dict[str, str]]]:
    """Return (active, orphans) ordered by added_at descending among actives."""
    favorites = load_store(path)
    favorites_sorted = sorted(
        favorites, key=lambda e: e.get("added_at", ""), reverse=True
    )
    active: List[Dict[str, Any]] = []
    orphans: List[Dict[str, str]] = []
    year_cache: Dict[str, catalog.CatalogLoadResult] = {}
    for entry in favorites_sorted:
        year_id = entry["year_id"]
        if year_id not in year_cache:
            year_cache[year_id] = catalog.load_year(catalog_dir, year_id)
        result = year_cache[year_id]
        match = None
        for video in result.videos:
            if video.video_id == entry["video_id"]:
                match = video
                break
        if match is None:
            orphans.append(entry)
            continue
        active.append(
            {
                "year_id": match.year_id,
                "video_id": match.video_id,
                "title": match.title,
                "added_at": entry["added_at"],
                "video": match,
            }
        )
    return active, orphans
