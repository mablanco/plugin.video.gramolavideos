# -*- coding: utf-8 -*-
"""Decade grouping helpers (feature 003)."""
import os

import catalog


def test_decade_id_for_year():
    assert catalog.decade_id_for_year("1980") == "1980"
    assert catalog.decade_id_for_year("1987") == "1980"
    assert catalog.decade_id_for_year("1999") == "1990"
    assert catalog.decade_id_for_year("1960") == "1960"


def test_list_decades_repo_has_1960_through_1990(csv_dir):
    result = catalog.list_decades(csv_dir)
    ids = [d.id for d in result.decades]
    assert ids == ["1960", "1970", "1980", "1990"]
    assert len(ids) <= 12


def test_years_in_decade_incomplete_no_invented_years(csv_dir):
    result = catalog.years_in_decade(csv_dir, "1990")
    years = [y.id for y in result.years]
    assert "1994" not in years
    assert years == [
        "1990",
        "1991",
        "1992",
        "1993",
        "1995",
        "1996",
        "1997",
        "1998",
        "1999",
    ]


def test_years_in_decade_1980s_complete(csv_dir):
    result = catalog.years_in_decade(csv_dir, "1980")
    assert [y.id for y in result.years] == [str(y) for y in range(1980, 1990)]


def test_projection_1960_1999_no_empty_decades(tmp_path):
    """Only decades with real CSV appear; empty decades are not invented."""
    for year in (1965, 1972, 1981, 1999):
        (tmp_path / "{0}.csv".format(year)).write_text(
            "Artista - Tema;dQw4w9WgXcQ\n", encoding="utf-8"
        )
    result = catalog.list_decades(str(tmp_path))
    assert [d.id for d in result.decades] == ["1960", "1970", "1980", "1990"]
    assert len(result.decades) <= 12
    assert [y.id for y in catalog.years_in_decade(str(tmp_path), "1960").years] == [
        "1965"
    ]
    assert catalog.years_in_decade(str(tmp_path), "1950").years == []


def test_every_year_belongs_to_exactly_one_listed_decade(csv_dir):
    """SC-004: every list_years stem maps to exactly one listed decade."""
    years = [y.id for y in catalog.list_years(csv_dir).years]
    decade_ids = {d.id for d in catalog.list_decades(csv_dir).decades}
    for year_id in years:
        decade_id = catalog.decade_id_for_year(year_id)
        assert decade_id in decade_ids
        in_decade = [
            y.id for y in catalog.years_in_decade(csv_dir, decade_id).years
        ]
        assert year_id in in_decade
    # No year appears in two decades
    seen = {}
    for decade_id in decade_ids:
        for year_id in [
            y.id for y in catalog.years_in_decade(csv_dir, decade_id).years
        ]:
            assert year_id not in seen
            seen[year_id] = decade_id
    assert set(seen) == set(years)


def test_list_decades_missing_dir():
    result = catalog.list_decades(os.path.join("no", "such", "csv"))
    assert result.decades == []
    assert result.errors
    assert result.errors[0].code == "csv_dir_missing"
