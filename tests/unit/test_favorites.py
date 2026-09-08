# -*- coding: utf-8 -*-
"""Unit tests for favorites store (feature 006)."""
from __future__ import annotations

import json
import os

import favorites


def _first_video(csv_dir):
    import catalog

    years = catalog.list_years(csv_dir).years
    assert years
    result = catalog.load_year(csv_dir, years[0].id)
    assert result.videos
    return result.videos[0]


def test_add_idempotent_and_persist(tmp_path, csv_dir):
    path = str(tmp_path / "favorites.json")
    video = _first_video(csv_dir)
    ok, err = favorites.add(
        path, csv_dir, video.year_id, video.video_id, video.title
    )
    assert ok and err is None
    ok2, err2 = favorites.add(
        path, csv_dir, video.year_id, video.video_id, "Other Title"
    )
    assert ok2 and err2 is None
    stored = favorites.load_store(path)
    assert len(stored) == 1
    assert stored[0]["video_id"] == video.video_id
    assert favorites.contains(path, video.year_id, video.video_id)


def test_remove_does_not_touch_csv(tmp_path, csv_dir):
    path = str(tmp_path / "favorites.json")
    video = _first_video(csv_dir)
    favorites.add(path, csv_dir, video.year_id, video.video_id, video.title)
    csv_path = os.path.join(csv_dir, "{0}.csv".format(video.year_id))
    before = open(csv_path, encoding="utf-8").read()
    assert favorites.remove(path, video.year_id, video.video_id)
    after = open(csv_path, encoding="utf-8").read()
    assert before == after
    assert favorites.load_store(path) == []


def test_orphan_classification(tmp_path, csv_dir):
    path = str(tmp_path / "favorites.json")
    favorites.save_store(
        path,
        [
            {
                "year_id": "1985",
                "video_id": "AAAAAAAAAAA",  # valid shape, not in catalog
                "title": "Ghost - Track",
                "added_at": "2026-01-01T00:00:00Z",
            }
        ],
    )
    active, orphans = favorites.list_resolved(path, csv_dir)
    assert active == []
    assert len(orphans) == 1


def test_corrupt_json_loads_empty(tmp_path):
    path = str(tmp_path / "favorites.json")
    path.write_text("{not-json", encoding="utf-8") if False else None
    with open(path, "w", encoding="utf-8") as handle:
        handle.write("{not-json")
    assert favorites.load_store(path) == []


def test_add_rejects_missing_catalog_entry(tmp_path, csv_dir):
    path = str(tmp_path / "favorites.json")
    ok, err = favorites.add(
        path, csv_dir, "1985", "BBBBBBBBBBB", "Missing - Song"
    )
    assert not ok
    assert err == "not_in_catalog"
