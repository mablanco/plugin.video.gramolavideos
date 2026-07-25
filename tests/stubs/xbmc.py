# -*- coding: utf-8 -*-
"""Minimal xbmc stub for host pytest (no real Kodi)."""

_log_calls = []
_translate_root = None


def reset():
    global _log_calls, _translate_root
    _log_calls = []
    _translate_root = None
    Player.reset_plays()


def set_translate_root(path):
    """Configure base path returned by translatePath for special://home/addons/..."""
    global _translate_root
    _translate_root = path


def translatePath(path):
    """Map special://home/addons/<id>/... to a configurable fake root."""
    import os

    prefix = "special://home/addons/"
    if _translate_root and path.startswith(prefix):
        rest = path[len(prefix) :]
        # rest like "plugin.video.gramolavideos/resources/csv/"
        parts = rest.split("/", 1)
        addon_rest = parts[1] if len(parts) > 1 else ""
        return os.path.join(_translate_root, addon_rest.replace("/", os.sep))
    return path


def log(msg, level=0):
    _log_calls.append((msg, level))


class Player(object):
    _plays = []

    def __init__(self):
        pass

    @classmethod
    def reset_plays(cls):
        cls._plays = []

    def play(self, item=None, listitem=None, windowed=False, startpos=-1):
        Player._plays.append(
            {
                "item": item,
                "listitem": listitem,
                "windowed": windowed,
                "startpos": startpos,
            }
        )
