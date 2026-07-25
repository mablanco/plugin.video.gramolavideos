# -*- coding: utf-8 -*-
"""Characterization: missing year / empty / unreadable (quickstart C3).

LEGACY_FREEZE: document non-catastrophic outcomes of the current extract.
"""
import os
import stat

import catalog
import pytest

pytestmark = pytest.mark.legacy_freeze


def test_empty_directory_yields_no_years(fixtures_dir):
    empty = os.path.join(fixtures_dir, "empty_dir")
    result = catalog.list_years(empty)
    assert result.years == []
    assert result.ok is True


def test_missing_year_returns_empty_videos(csv_dir):
    result = catalog.load_year(csv_dir, "1994")
    assert result.videos == []
    assert result.ok is True


def test_missing_csv_dir_returns_empty(tmp_path):
    missing = str(tmp_path / "no-such-csv-dir")
    assert catalog.load_all_videos(missing) == {}
    assert catalog.list_years(missing).years == []


def test_unreadable_year_file_surfaces_error(tmp_path):
    """Legacy open raises OSError; load_all_videos does not catch it today."""
    year_path = tmp_path / "1988.csv"
    year_path.write_text("A - B;dQw4w9WgXcQ\n", encoding="utf-8")
    year_path.chmod(0)
    try:
        with pytest.raises(OSError):
            catalog.load_all_videos(str(tmp_path))
    finally:
        year_path.chmod(stat.S_IRUSR | stat.S_IWUSR)
