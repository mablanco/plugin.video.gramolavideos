# -*- coding: utf-8 -*-
"""Plugin wiring for catalog search (feature 007)."""
from __future__ import annotations

import importlib
import sys
from urllib.parse import parse_qs, urlparse

import xbmcgui
import xbmcplugin


def _run_addon(query):
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
        "favorites",
        "youtube_probe",
    ):
        if name in sys.modules:
            del sys.modules[name]
    return importlib.import_module("addon")


def test_search_results_playable_urls():
    _run_addon("mode=search_results&q=Mecano")
    adds = xbmcplugin.calls_named("addDirectoryItem")
    assert len(adds) >= 1
    for call in adds:
        assert not call["kwargs"].get("isFolder")
        qs = parse_qs(urlparse(call["kwargs"]["url"]).query)
        assert qs["mode"] == ["song"]
        assert call["kwargs"]["listitem"]._properties.get("IsPlayable") == "true"


def test_search_empty_notifies():
    _run_addon("mode=search_results&q=zzznomatch999")
    adds = xbmcplugin.calls_named("addDirectoryItem")
    assert adds == []
    notes = xbmcgui.get_notifications()
    assert notes
    assert "coincidencias" in notes[0]["message"].lower() or "matches" in notes[0]["message"].lower()


def test_search_mode_cancel_lists_nothing():
    xbmcgui.set_next_input("")
    _run_addon("mode=search")
    adds = xbmcplugin.calls_named("addDirectoryItem")
    assert adds == []


def test_search_mode_with_input_lists_results():
    xbmcgui.set_next_input("Mecano")
    _run_addon("mode=search")
    adds = xbmcplugin.calls_named("addDirectoryItem")
    assert len(adds) >= 1
