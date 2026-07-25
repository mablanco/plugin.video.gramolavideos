# -*- coding: utf-8 -*-
"""Kodi pluginsource UI: listings, resolve, and plugin entry routing."""
import os
import sys
from urllib.parse import parse_qs, urlencode

import xbmcaddon
import xbmcgui
import xbmcplugin

import catalog
import kodi_notify

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


def build_url(base_url, query):
    return base_url + "?" + urlencode(query)


def run(argv=None):
    """Plugin entry: list years, list a year, or resolve a song."""
    argv = sys.argv if argv is None else argv
    base_url = argv[0]
    handle = int(argv[1])
    args = parse_qs(argv[2][1:])
    mode = args.get("mode", None)
    catalog_dir = csv_dir()
    set_musicvideos_content(handle)

    if mode is None:
        result = catalog.list_years(catalog_dir)
        kodi_notify.notify_catalog_errors(result.errors)
        for year in result.years:
            url = build_url(base_url, {"mode": "year", "foldername": year.id})
            li = folder_listitem(year.id)
            xbmcplugin.addDirectoryItem(
                handle=handle, url=url, listitem=li, isFolder=True
            )
        xbmcplugin.endOfDirectory(handle)
        return

    if mode[0] == "year":
        year_id = args["foldername"][0]
        result = catalog.load_year(catalog_dir, year_id)
        kodi_notify.notify_catalog_errors(result.errors)
        for video in result.videos:
            url = build_url(
                base_url, {"mode": "song", "foldername": video.video_id}
            )
            li = song_listitem(video.title, video.video_id)
            xbmcplugin.addDirectoryItem(handle=handle, url=url, listitem=li)
        xbmcplugin.endOfDirectory(handle)
        return

    if mode[0] == "song":
        resolve_youtube_playback(handle, args["foldername"][0])
