# -*- coding: utf-8 -*-
"""Minimal xbmcaddon stub with configurable addon root."""

_addon_root = None
_addon_info = {
    "id": "plugin.video.gramolavideos",
    "name": "La Gramola de Videos",
    "version": "0.0.0",
}


def reset():
    global _addon_root
    _addon_root = None


def set_addon_root(path):
    global _addon_root
    _addon_root = path


class Addon(object):
    def __init__(self, id=None):
        self._id = id or _addon_info["id"]

    def getAddonInfo(self, key):
        if key == "path":
            if _addon_root is not None:
                return _addon_root
            return ""
        return _addon_info.get(key, "")

    def getSetting(self, key):
        return ""
