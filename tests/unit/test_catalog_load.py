# -*- coding: utf-8 -*-
"""Characterization: current row-loading shape (quickstart C1–C2).

LEGACY_FREEZE: invalid video ids (e.g. Chiquilla) are still loaded as rows.
Desired validation (omit + error) lands in US2 / T028.
"""
import os

import catalog
import pytest

pytestmark = pytest.mark.legacy_freeze

CHIQUILLA_ID = "d3mZmP_me4"  # known invalid length; still present in freeze


def test_valid_fixture_loads_two_field_rows(fixtures_dir):
    # Point load at a temp dir containing only valid_year.csv as YYYY.csv
    import shutil
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        shutil.copy(
            os.path.join(fixtures_dir, "valid_year.csv"),
            os.path.join(tmp, "1985.csv"),
        )
        result = catalog.load_year(tmp, "1985")
        assert len(result.videos) == 2
        assert result.videos[0] == ["Artista Uno - Cancion A", "dQw4w9WgXcQ"]
        assert result.videos[1][1] == "jNQXAC9IVRw"


def test_1991_includes_chiquilla_invalid_id(csv_dir):
    result = catalog.load_year(csv_dir, "1991")
    chiquilla = [row for row in result.videos if row and row[0].endswith("Chiquilla")]
    assert len(chiquilla) == 1
    assert chiquilla[0][1] == CHIQUILLA_ID
    assert len(CHIQUILLA_ID) != 11


def test_incomplete_row_fixture_keeps_short_tuples(fixtures_dir):
    import shutil
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        shutil.copy(
            os.path.join(fixtures_dir, "incomplete_row.csv"),
            os.path.join(tmp, "1980.csv"),
        )
        rows = catalog.load_year(tmp, "1980").videos
        assert any(len(r) < 2 for r in rows)
        assert any(len(r) == 2 and len(r[1]) != 11 for r in rows)


def test_extra_fields_fixture_keeps_leading_title_and_id(fixtures_dir):
    import shutil
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        shutil.copy(
            os.path.join(fixtures_dir, "extra_fields.csv"),
            os.path.join(tmp, "1980.csv"),
        )
        rows = catalog.load_year(tmp, "1980").videos
        assert rows[0][0] == "Artista - Tema"
        assert rows[0][1] == "dQw4w9WgXcQ"
        assert len(rows[0]) > 2
