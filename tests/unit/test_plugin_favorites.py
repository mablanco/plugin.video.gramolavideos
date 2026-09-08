# -*- coding: utf-8 -*-
"""Plugin wiring for favorites (feature 006)."""
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


def test_favorite_add_and_list(csv_dir):
    _run_addon(
        "mode=favorite_add&year_id=1985&video_id=i7cEs-1qK5k"
        "&title=Hombres+G+-+Venezia"
    )
    notes = xbmcgui.get_notifications()
    assert notes
    assert "favorito" in notes[0]["message"].lower()

    _run_addon("mode=favorites")
    adds = xbmcplugin.calls_named("addDirectoryItem")
    assert len(adds) >= 1
    labels = [c["kwargs"]["listitem"].getLabel() for c in adds]
    assert any("Venezia" in label or "Hombres" in label for label in labels)
    qs = parse_qs(urlparse(adds[0]["kwargs"]["url"]).query)
    assert qs["mode"] == ["song"]


def test_year_songs_have_favorite_context():
    _run_addon("mode=year&foldername=1985")
    adds = xbmcplugin.calls_named("addDirectoryItem")
    assert adds
    li = adds[0]["kwargs"]["listitem"]
    assert getattr(li, "_context_menu", None)
    assert li._context_menu
    assert "favoritos" in li._context_menu[0][0].lower()
    assert "RunPlugin(" in li._context_menu[0][1]


def test_favorite_remove(csv_dir):
    _run_addon(
        "mode=favorite_add&year_id=1985&video_id=i7cEs-1qK5k&title=X"
    )
    _run_addon(
        "mode=favorite_remove&year_id=1985&video_id=i7cEs-1qK5k"
    )
    _run_addon("mode=favorites")
    adds = xbmcplugin.calls_named("addDirectoryItem")
    assert adds == []
