# -*- coding: utf-8 -*-
"""Plugin wiring characterization against xbmc* stubs (T016).

LEGACY_FREEZE: play uses xbmc.Player().play (not setResolvedUrl yet — US1).
"""
import importlib
import sys

import pytest
import xbmc
import xbmcplugin

pytestmark = pytest.mark.legacy_freeze


def _run_addon(query):
    """Import/reload addon.py with plugin argv. ``query`` is the part after ``?``."""
    sys.argv = [
        "plugin://plugin.video.gramolavideos/",
        "1",
        "?" + query if query is not None else "?",
    ]
    if "addon" in sys.modules:
        del sys.modules["addon"]
    return importlib.import_module("addon")


def test_list_years_adds_directory_items_and_ends(csv_dir):
    _run_addon("")
    adds = xbmcplugin.calls_named("addDirectoryItem")
    ends = xbmcplugin.calls_named("endOfDirectory")
    contents = xbmcplugin.calls_named("setContent")
    assert contents and contents[0]["kwargs"]["content"] == "movies"
    assert len(adds) == 19
    assert all(c["kwargs"]["isFolder"] for c in adds)
    assert ends and ends[0]["kwargs"]["handle"] == 1
    urls = [c["kwargs"]["url"] for c in adds]
    assert any("mode=year" in u and "foldername=1991" in u for u in urls)


def test_list_year_songs_for_1991():
    _run_addon("mode=year&foldername=1991")
    adds = xbmcplugin.calls_named("addDirectoryItem")
    assert len(adds) >= 1
    assert all(not c["kwargs"]["isFolder"] for c in adds)
    assert any("mode=song" in c["kwargs"]["url"] for c in adds)
    assert xbmcplugin.calls_named("endOfDirectory")


def test_play_song_uses_player_not_set_resolved():
    vid = "dQw4w9WgXcQ"
    _run_addon("mode=song&foldername=" + vid)
    assert xbmc.Player._plays
    played = xbmc.Player._plays[0]["item"]
    assert played == "plugin://plugin.video.youtube/play/?video_id=" + vid
    assert xbmcplugin.calls_named("setResolvedUrl") == []
