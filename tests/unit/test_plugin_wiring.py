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
    """Import/reload thin addon.py (and kodi_plugin) with plugin argv."""
    sys.argv = [
        "plugin://plugin.video.gramolavideos/",
        "1",
        "?" + query if query is not None else "?",
    ]
    for name in ("addon", "kodi_plugin", "kodi_notify", "kodi_i18n", "catalog", "youtube_probe"):
        if name in sys.modules:
            del sys.modules[name]
    return importlib.import_module("addon")


def test_list_years_musicvideos_content(csv_dir):
    _run_addon("")
    contents = xbmcplugin.calls_named("setContent")
    assert contents and contents[0]["kwargs"]["content"] == "musicvideos"
    adds = xbmcplugin.calls_named("addDirectoryItem")
    expected = len([f for f in os.listdir(csv_dir) if f.endswith(".csv")])
    assert len(adds) == expected
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


def test_play_song_uses_set_resolved_url(monkeypatch):
    import kodi_plugin
    import youtube_probe

    monkeypatch.setattr(
        kodi_plugin.youtube_probe,
        "probe_youtube_video",
        lambda *_a, **_k: youtube_probe.STATUS_OK,
    )
    vid = "dQw4w9WgXcQ"
    sys.argv = [
        "plugin://plugin.video.gramolavideos/",
        "1",
        "?mode=song&foldername=" + vid,
    ]
    kodi_plugin.run(sys.argv)
    resolved = xbmcplugin.calls_named("setResolvedUrl")
    assert len(resolved) == 1
    assert resolved[0]["kwargs"]["succeeded"] is True
    assert resolved[0]["kwargs"]["listitem"].path == (
        "plugin://plugin.video.youtube/play/?video_id=" + vid
    )
    assert xbmc.Player._plays == []


def test_play_song_blocks_private_with_notification(monkeypatch):
    import kodi_plugin
    import youtube_probe
    import xbmcgui

    monkeypatch.setattr(
        kodi_plugin.youtube_probe,
        "probe_youtube_video",
        lambda *_a, **_k: youtube_probe.STATUS_PRIVATE,
    )
    vid = "privateVideo1"
    sys.argv = [
        "plugin://plugin.video.gramolavideos/",
        "1",
        "?mode=song&foldername=" + vid,
    ]
    kodi_plugin.run(sys.argv)
    resolved = xbmcplugin.calls_named("setResolvedUrl")
    assert len(resolved) == 1
    assert resolved[0]["kwargs"]["succeeded"] is False
    notes = xbmcgui.get_notifications()
    assert notes
    msg = notes[0]["message"].lower()
    assert "privado" in msg or "sesión" in msg


def test_csv_dir_comes_from_addon_path(repo_root):
    import kodi_plugin

    assert kodi_plugin.csv_dir() == os.path.join(repo_root, "resources", "csv")
    assert xbmcaddon.Addon().getAddonInfo("path") == repo_root
