# -*- coding: utf-8 -*-
"""Desired catalog validation (quickstart B1–B3 / T028)."""
import os
import shutil
import tempfile

import catalog


def test_valid_fixture_loads_music_videos(fixtures_dir):
    with tempfile.TemporaryDirectory() as tmp:
        shutil.copy(
            os.path.join(fixtures_dir, "valid_year.csv"),
            os.path.join(tmp, "1985.csv"),
        )
        result = catalog.load_year(tmp, "1985")
        assert result.errors == []
        assert len(result.videos) == 2
        assert result.videos[0].title == "Artista Dos - Cancion B"
        assert result.videos[0].video_id == "jNQXAC9IVRw"
        assert result.videos[1].title == "Artista Uno - Cancion A"
        assert result.videos[1].video_id == "dQw4w9WgXcQ"


def test_bad_video_id_omitted_with_error(fixtures_dir):
    """B1: video_id ≠ 11 valid chars → omit + row_bad_video_id."""
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "1991.csv")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write("Ok - Tema;dQw4w9WgXcQ\n")
            fh.write("Seguridad Social - Chiquilla;d3mZmP_me4\n")
        result = catalog.load_year(tmp, "1991")
        assert len(result.videos) == 1
        assert result.videos[0].video_id == "dQw4w9WgXcQ"
        assert any(e.code == "row_bad_video_id" for e in result.errors)


def test_1991_chiquilla_fixed_in_repo(csv_dir):
    result = catalog.load_year(csv_dir, "1991")
    chiquilla = [v for v in result.videos if v.title.endswith("Chiquilla")]
    assert len(chiquilla) == 1
    assert chiquilla[0].video_id == "-d3mZmP_me4"
    assert catalog.VIDEO_ID_RE.match(chiquilla[0].video_id)
    assert not any(
        e.row and "d3mZmP_me4" in e.row and "-d3mZmP_me4" not in e.row
        for e in result.errors
    )


def test_incomplete_and_short_id_rows_omitted(fixtures_dir):
    with tempfile.TemporaryDirectory() as tmp:
        shutil.copy(
            os.path.join(fixtures_dir, "incomplete_row.csv"),
            os.path.join(tmp, "1980.csv"),
        )
        result = catalog.load_year(tmp, "1980")
        assert len(result.videos) == 1
        assert result.videos[0].video_id == "dQw4w9WgXcQ"
        codes = {e.code for e in result.errors}
        assert "row_invalid" in codes
        assert "row_bad_video_id" in codes


def test_extra_fields_row_invalid(fixtures_dir):
    with tempfile.TemporaryDirectory() as tmp:
        shutil.copy(
            os.path.join(fixtures_dir, "extra_fields.csv"),
            os.path.join(tmp, "1980.csv"),
        )
        result = catalog.load_year(tmp, "1980")
        assert len(result.videos) == 1
        assert result.videos[0].title == "Solo dos campos"
        assert any(e.code == "row_invalid" for e in result.errors)


def test_mixed_valid_invalid_keeps_only_valid(tmp_path):
    """B3: mix → only valid in videos."""
    path = tmp_path / "1982.csv"
    path.write_text(
        "Good - One;dQw4w9WgXcQ\n"
        "Bad;;\n"
        "Good - Two;jNQXAC9IVRw\n"
        "Short;abc\n",
        encoding="utf-8",
    )
    result = catalog.load_year(str(tmp_path), "1982")
    assert [v.title for v in result.videos] == ["Good - One", "Good - Two"]
    assert len(result.errors) >= 2
