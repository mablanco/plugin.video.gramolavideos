# -*- coding: utf-8 -*-
"""Characterization: repo year inventory (quickstart C4 + seed 60/70)."""
import os

import catalog

# Seed 004: continuous years 1964–1979; legacy 1980–1999 without 1994.
EXPECTED_YEARS = [str(y) for y in range(1964, 1980)] + [
    str(y) for y in range(1980, 2000) if y != 1994
]


def test_repo_years_60_70_seed_and_1980_1999_without_1994(csv_dir):
    result = catalog.list_years(csv_dir)
    years = [y.id for y in result.years]
    assert years == EXPECTED_YEARS
    assert "1994" not in years
    assert len(years) == 35
    seed = [y for y in years if 1960 <= int(y) <= 1979]
    assert len(seed) >= 8
    assert any(int(y) < 1970 for y in seed)
    assert any(int(y) >= 1970 for y in seed)


def test_repo_csv_files_match_list_years(csv_dir):
    on_disk = sorted(
        os.path.splitext(f)[0]
        for f in os.listdir(csv_dir)
        if f.endswith(".csv")
    )
    assert [y.id for y in catalog.list_years(csv_dir).years] == on_disk
