# -*- coding: utf-8 -*-
"""Plugin-URL parameter validation and atomic favorites writes."""
from __future__ import annotations

import json
import os

import pytest
import xbmcplugin

import catalog
import favorites


def _run(query):
    import kodi_plugin

    kodi_plugin.run(["plugin://plugin.video.gramolavideos/", "1", "?" + query])


def _outside_csv(tmp_path):
    """A well-formed catalog CSV that lives outside the catalog directory."""
    secret = tmp_path / "secret.csv"
    secret.write_text("Secret - Title;dQw4w9WgXcQ\n", encoding="utf-8")
    return str(secret)


@pytest.mark.parametrize("year_id", ["../x", "/etc/passwd", "19850", "", None])
def test_load_year_rejects_invalid_ids_without_touching_disk(csv_dir, year_id):
    result = catalog.load_year(csv_dir, year_id)
    assert result.videos == []
    assert [e.code for e in result.errors] == ["invalid_year_id"]


def test_load_year_blocks_traversal_to_outside_csv(csv_dir, tmp_path):
    secret = _outside_csv(tmp_path)
    relative = os.path.relpath(secret[: -len(".csv")], csv_dir)
    absolute = secret[: -len(".csv")]
    for year_id in (relative, absolute):
        result = catalog.load_year(csv_dir, year_id)
        assert result.videos == []


@pytest.mark.parametrize("decade_id", ["abc", "1985", "../1980", ""])
def test_years_in_decade_rejects_invalid_ids(csv_dir, decade_id):
    result = catalog.years_in_decade(csv_dir, decade_id)
    assert result.years == []
    assert [e.code for e in result.errors] == ["invalid_decade_id"]


@pytest.mark.parametrize(
    "query",
    [
        "mode=year&foldername=..%2F..%2Fsecret",
        "mode=year&foldername=%2Fetc%2Fpasswd",
        "mode=year",
        "mode=decade&foldername=abc",
        "mode=decade",
    ],
)
def test_invalid_folder_routes_end_directory_unsuccessfully(query):
    _run(query)
    assert xbmcplugin.calls_named("addDirectoryItem") == []
    ends = xbmcplugin.calls_named("endOfDirectory")
    assert len(ends) == 1
    assert ends[0]["kwargs"]["succeeded"] is False


@pytest.mark.parametrize(
    "query",
    [
        "mode=song&foldername=dQw4w9WgXcQ%26audio_only%3Dtrue",
        "mode=song&foldername=short",
        "mode=song",
        "mode=song&foldername=dQw4w9WgXcQ&year_id=..%2Fx",
    ],
)
def test_invalid_song_ids_never_probe_or_play(monkeypatch, query):
    import kodi_plugin

    probed = []
    monkeypatch.setattr(
        kodi_plugin.youtube_probe,
        "probe_youtube_video",
        lambda vid, *_a, **_k: probed.append(vid) or "ok",
    )
    _run(query)
    assert probed == []
    resolved = xbmcplugin.calls_named("setResolvedUrl")
    assert len(resolved) == 1
    assert resolved[0]["kwargs"]["succeeded"] is False


def test_save_store_leaves_no_temp_files(tmp_path):
    path = str(tmp_path / "favorites.json")
    entry = {
        "year_id": "1985",
        "video_id": "i7cEs-1qK5k",
        "title": "Hombres G - Venezia",
        "added_at": "2026-01-01T00:00:00Z",
    }
    favorites.save_store(path, [entry])
    assert os.listdir(str(tmp_path)) == ["favorites.json"]
    assert favorites.load_store(path) == [entry]


def test_save_store_failure_keeps_previous_file(tmp_path, monkeypatch):
    path = str(tmp_path / "favorites.json")
    entry = {
        "year_id": "1985",
        "video_id": "i7cEs-1qK5k",
        "title": "Hombres G - Venezia",
        "added_at": "2026-01-01T00:00:00Z",
    }
    favorites.save_store(path, [entry])

    def boom(*_a, **_k):
        raise OSError("disk full")

    monkeypatch.setattr(favorites.json, "dump", boom)
    with pytest.raises(OSError):
        favorites.save_store(path, [])
    assert os.listdir(str(tmp_path)) == ["favorites.json"]
    with open(path, encoding="utf-8") as handle:
        assert json.load(handle)["favorites"] == [entry]
