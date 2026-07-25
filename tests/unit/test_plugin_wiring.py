# -*- coding: utf-8 -*-
"""Plugin wiring against xbmc* stubs — desired US1 behavior (T026).

Former LEGACY_FREEZE play/content/thumb assertions replaced after Matrix+ work.
"""
import importlib
import os
import sys

import xbmc
import xbmcaddon
import xbmcplugin


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


def test_list_years_musicvideos_content(csv_dir):
    _run_addon("")
    contents = xbmcplugin.calls_named("setContent")
    assert contents and contents[0]["kwargs"]["content"] == "musicvideos"
    adds = xbmcplugin.calls_named("addDirectoryItem")
    assert len(adds) == 19
    assert all(c["kwargs"]["isFolder"] for c in adds)


def test_list_year_songs_use_https_thumbs():
    _run_addon("mode=year&foldername=1991")
    adds = xbmcplugin.calls_named("addDirectoryItem")
    assert len(adds) >= 1
    assert all(not c["kwargs"]["isFolder"] for c in adds)
    for call in adds:
        li = call["kwargs"]["listitem"]
        thumb = (li._art or {}).get("thumb", "")
        assert thumb.startswith("https://img.youtube.com/vi/")
        assert li._properties.get("IsPlayable") == "true"


def test_play_song_uses_set_resolved_url():
    vid = "dQw4w9WgXcQ"
    _run_addon("mode=song&foldername=" + vid)
    resolved = xbmcplugin.calls_named("setResolvedUrl")
    assert len(resolved) == 1
    assert resolved[0]["kwargs"]["succeeded"] is True
    assert resolved[0]["kwargs"]["listitem"].path == (
        "plugin://plugin.video.youtube/play/?video_id=" + vid
    )
    assert xbmc.Player._plays == []


def test_csv_dir_comes_from_addon_path(repo_root):
    import kodi_plugin

    assert kodi_plugin.csv_dir() == os.path.join(repo_root, "resources", "csv")
    assert xbmcaddon.Addon().getAddonInfo("path") == repo_root
