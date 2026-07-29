# -*- coding: utf-8 -*-
"""Plugin wiring against xbmc* stubs — decade navigation (feature 003).

Former LEGACY_FREEZE play/content/thumb assertions replaced after Matrix+ work.
Root lists decades (not flat years); decade/year folders keep isFolder=True for
Kodi native back stack.
"""
import importlib
import os
import sys
from urllib.parse import parse_qs, urlparse

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
    for name in (
        "addon",
        "kodi_plugin",
        "kodi_notify",
        "kodi_i18n",
        "catalog",
        "youtube_probe",
    ):
        if name in sys.modules:
            del sys.modules[name]
    return importlib.import_module("addon")


def test_root_lists_decades_not_flat_years(csv_dir):
    _run_addon("")
    contents = xbmcplugin.calls_named("setContent")
    assert contents and contents[0]["kwargs"]["content"] == "musicvideos"
    adds = xbmcplugin.calls_named("addDirectoryItem")
    # Seed 60/70 + legacy 80/90 → four decades (not flat year list)
    assert len(adds) == 4
    assert len(adds) <= 12
    assert all(c["kwargs"]["isFolder"] is True for c in adds)
    labels = [c["kwargs"]["listitem"].getLabel() for c in adds]
    assert labels == ["Años 60", "Años 70", "Años 80", "Años 90"]
    for call in adds:
        qs = parse_qs(urlparse(call["kwargs"]["url"]).query)
        assert qs["mode"] == ["decade"]
        assert qs["foldername"][0] in ("1960", "1970", "1980", "1990")


def test_decade_drill_down_to_years():
    _run_addon("mode=decade&foldername=1980")
    adds = xbmcplugin.calls_named("addDirectoryItem")
    assert len(adds) == 10
    assert all(c["kwargs"]["isFolder"] is True for c in adds)
    years = [c["kwargs"]["listitem"].getLabel() for c in adds]
    assert years == [str(y) for y in range(1980, 1990)]
    for call in adds:
        qs = parse_qs(urlparse(call["kwargs"]["url"]).query)
        assert qs["mode"] == ["year"]


def test_list_year_songs_use_https_thumbs():
    _run_addon("mode=year&foldername=1991")
    adds = xbmcplugin.calls_named("addDirectoryItem")
    assert len(adds) >= 1
    assert all(not c["kwargs"].get("isFolder") for c in adds)
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
