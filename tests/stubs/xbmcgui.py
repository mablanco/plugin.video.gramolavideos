# -*- coding: utf-8 -*-
"""Minimal xbmcgui stub for host pytest."""

_notifications = []


def reset():
    global _notifications, _next_input
    _notifications = []
    _next_input = None


class ListItem(object):
    def __init__(self, label="", label2="", path="", offscreen=False, **kwargs):
        # Accept legacy iconImage / thumbnailImage and modern kwargs
        self.label = label
        self.label2 = label2
        self.path = path
        self.offscreen = offscreen
        self.iconImage = kwargs.get("iconImage")
        self.thumbnailImage = kwargs.get("thumbnailImage")
        self._art = {}
        self._info = {}
        self._properties = {}
        self._context_menu = []
        self._context_replace = False

    def getLabel(self):
        return self.label

    def setArt(self, art):
        self._art.update(art or {})

    def setInfo(self, type_, infoLabels):
        self._info[type_] = infoLabels

    def setProperty(self, key, value):
        self._properties[key] = value

    def addContextMenuItems(self, items, replaceItems=False):
        self._context_menu = list(items or [])
        self._context_replace = bool(replaceItems)


_next_input = None


class Dialog(object):
    def notification(self, heading, message, icon="", time=5000, sound=True):
        _notifications.append(
            {
                "heading": heading,
                "message": message,
                "icon": icon,
                "time": time,
                "sound": sound,
            }
        )

    def input(self, heading, defaultt="", type=0, **kwargs):
        global _next_input
        value = _next_input
        _next_input = None
        if value is None:
            return ""
        return value


def set_next_input(value):
    global _next_input
    _next_input = value


def get_notifications():
    return list(_notifications)
