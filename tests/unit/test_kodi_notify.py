# -*- coding: utf-8 -*-
"""Notify + residual listing when catalog has recoverable errors (T034)."""
import importlib
import os
import sys

import xbmcgui
import xbmcplugin


def _run_addon(query):
    sys.argv = [
        "plugin://plugin.video.gramolavideos/",
        "1",
        "?" + query if query is not None else "?",
    ]
    for name in ("addon", "kodi_plugin", "kodi_notify", "catalog"):
        if name in sys.modules:
            del sys.modules[name]
    return importlib.import_module("addon")


def test_notify_catalog_errors_no_op_when_empty():
    import kodi_notify

    kodi_notify.notify_catalog_errors([])
    assert xbmcgui.get_notifications() == []


def test_notify_catalog_errors_records_dialog():
    import catalog
    import kodi_notify

    err = catalog.CatalogError("row_invalid", "bad", year_id="1980", row="x")
    kodi_notify.notify_catalog_errors([err])
    notes = xbmcgui.get_notifications()
    assert len(notes) == 1
    assert "catálogo" in notes[0]["message"].lower()


def test_year_with_bad_rows_notifies_and_lists_residual(tmp_path, repo_root):
    csv_root = tmp_path / "resources" / "csv"
    csv_root.mkdir(parents=True)
    (csv_root / "1980.csv").write_text(
        "Good - Song;dQw4w9WgXcQ\nBadShort;abc\n",
        encoding="utf-8",
    )
    import xbmcaddon

    xbmcaddon.set_addon_root(str(tmp_path))
    _run_addon("mode=year&foldername=1980")
    notes = xbmcgui.get_notifications()
    assert notes
    adds = xbmcplugin.calls_named("addDirectoryItem")
    assert len(adds) == 1
    assert adds[0]["kwargs"]["listitem"].label == "Good - Song"
