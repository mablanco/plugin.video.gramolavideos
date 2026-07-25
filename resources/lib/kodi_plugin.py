# -*- coding: utf-8 -*-
"""Kodi UI helpers for the gramola pluginsource (no catalog I/O)."""
import os

import xbmcaddon
import xbmcgui
import xbmcplugin

CONTENT_MUSICVIDEOS = "musicvideos"
YOUTUBE_PLAY_URI = "plugin://plugin.video.youtube/play/?video_id={video_id}"
YOUTUBE_THUMB_URI = "https://img.youtube.com/vi/{video_id}/0.jpg"


def addon_root():
    return xbmcaddon.Addon().getAddonInfo("path")


def csv_dir():
    return os.path.join(addon_root(), "resources", "csv")


def set_musicvideos_content(handle):
    xbmcplugin.setContent(handle, CONTENT_MUSICVIDEOS)


def folder_listitem(label):
    li = xbmcgui.ListItem(label=label)
    li.setArt({"icon": "DefaultFolder.png", "thumb": "DefaultFolder.png"})
    return li


def song_listitem(title, video_id):
    """Build a playable song item; thumbnail failures must not block the row."""
    li = xbmcgui.ListItem(label=title)
    thumb = YOUTUBE_THUMB_URI.format(video_id=video_id)
    try:
        li.setArt({"icon": thumb, "thumb": thumb})
    except Exception:
        pass
    li.setProperty("IsPlayable", "true")
    return li


def resolve_youtube_playback(handle, video_id):
    play_url = YOUTUBE_PLAY_URI.format(video_id=video_id)
    li = xbmcgui.ListItem(path=play_url)
    xbmcplugin.setResolvedUrl(handle, True, li)
    return play_url
