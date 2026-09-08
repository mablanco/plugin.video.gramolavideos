# -*- coding: utf-8 -*-
"""Unit tests for catalog.search (feature 007)."""
from __future__ import annotations

import os

import catalog


def test_search_empty_query_opens_no_needless_match(csv_dir):
    result = catalog.search(csv_dir, "   ")
    assert result.videos == []
    assert result.ok


def test_search_casefold_match(csv_dir):
    years = catalog.list_years(csv_dir).years
    video = None
    for year in years:
        loaded = catalog.load_year(csv_dir, year.id)
        if loaded.videos:
            video = loaded.videos[0]
            break
    assert video is not None
    fragment = video.title[2:8]
    result = catalog.search(csv_dir, fragment.upper())
    ids = {v.video_id for v in result.videos}
    assert video.video_id in ids


def test_search_no_matches(csv_dir):
    result = catalog.search(csv_dir, "zzzxxyyzz-no-match-099")
    assert result.videos == []


def test_search_limit_and_sort(tmp_path):
    csv_dir = str(tmp_path / "csv")
    os.makedirs(csv_dir)
    # Many matching rows across two years
    rows_a = [
        "Artist {0:03d} - Song;aaaaaaaaaa{0:01d}".format(i)
        for i in range(10)
    ]
    # Fix video ids to 11 chars
    rows = []
    for i in range(60):
        vid = "a{0:010d}".format(i)[-11:]
        rows.append("Zebra Band - Track {0:03d};{1}".format(i, vid))
    with open(os.path.join(csv_dir, "1980.csv"), "w", encoding="utf-8") as f:
        f.write("\n".join(rows[:40]) + "\n")
    with open(os.path.join(csv_dir, "1981.csv"), "w", encoding="utf-8") as f:
        f.write("\n".join(rows[40:]) + "\n")
    result = catalog.search(csv_dir, "Zebra", limit=100)
    assert len(result.videos) == 60
    titles = [v.title for v in result.videos]
    assert titles == sorted(titles, key=lambda t: t.casefold())
    capped = catalog.search(csv_dir, "Zebra", limit=1000)
    assert len(capped.videos) == 60  # only 60 exist
    # Pad to >100
    extra = []
    for i in range(60, 120):
        vid = "b{0:010d}".format(i)[-11:]
        extra.append("Zebra Band - Track {0:03d};{1}".format(i, vid))
    with open(os.path.join(csv_dir, "1982.csv"), "w", encoding="utf-8") as f:
        f.write("\n".join(extra) + "\n")
    limited = catalog.search(csv_dir, "Zebra", limit=100)
    assert len(limited.videos) == 100
