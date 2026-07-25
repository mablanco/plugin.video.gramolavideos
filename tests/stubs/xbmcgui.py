# -*- coding: utf-8 -*-
"""Minimal xbmcgui stub for host pytest."""

_notifications = []


def reset():
    global _notifications
    _notifications = []


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

    def setArt(self, art):
        self._art.update(art or {})

    def setInfo(self, type_, infoLabels):
        self._info[type_] = infoLabels

    def setProperty(self, key, value):
        self._properties[key] = value


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


def get_notifications():
    return list(_notifications)
