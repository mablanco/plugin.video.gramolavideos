# -*- coding: utf-8 -*-
"""Catalog edge cases — desired recoverable errors (quickstart B2 / T028)."""
import os
import stat

import catalog


def test_empty_directory_yields_no_years(fixtures_dir):
    empty = os.path.join(fixtures_dir, "empty_dir")
    result = catalog.list_years(empty)
    assert result.years == []
    assert result.errors == []
    assert result.ok is True


def test_missing_year_returns_year_missing_error(csv_dir):
    result = catalog.load_year(csv_dir, "1994")
    assert result.videos == []
    assert any(e.code == "year_missing" for e in result.errors)
    assert result.ok is True


def test_missing_csv_dir_error(tmp_path):
    missing = str(tmp_path / "no-such-csv-dir")
    assert catalog.load_all_videos(missing) == {}
    listed = catalog.list_years(missing)
    assert listed.years == []
    assert any(e.code == "csv_dir_missing" for e in listed.errors)


def test_unreadable_year_file_becomes_error(tmp_path):
    """B2: unreadable CSV → errors, no crash."""
    year_path = tmp_path / "1988.csv"
    year_path.write_text("A - B;dQw4w9WgXcQ\n", encoding="utf-8")
    year_path.chmod(0)
    try:
        result = catalog.load_year(str(tmp_path), "1988")
        assert result.videos == []
        assert any(e.code == "year_unreadable" for e in result.errors)
        assert result.ok is True
    finally:
        year_path.chmod(stat.S_IRUSR | stat.S_IWUSR)
