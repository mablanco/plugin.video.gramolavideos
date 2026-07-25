# -*- coding: utf-8 -*-
"""Characterization: repo year inventory (quickstart C4)."""
import os

import catalog


def test_repo_years_1980_1999_without_1994(csv_dir):
    result = catalog.list_years(csv_dir)
    years = [y.id for y in result.years]
    expected = [str(y) for y in range(1980, 2000) if y != 1994]
    assert years == expected
    assert "1994" not in years
    assert len(years) == 19


def test_repo_csv_files_match_list_years(csv_dir):
    on_disk = sorted(
        os.path.splitext(f)[0]
        for f in os.listdir(csv_dir)
        if f.endswith(".csv")
    )
    assert [y.id for y in catalog.list_years(csv_dir).years] == on_disk
