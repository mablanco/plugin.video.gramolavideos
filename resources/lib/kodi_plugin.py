# -*- coding: utf-8 -*-
"""Kodi pluginsource UI: listings, resolve, and plugin entry routing."""
from __future__ import annotations

import os
import sys
from typing import Dict, List, Mapping, Optional, Sequence
from urllib.parse import parse_qs, urlencode

import xbmcaddon
import xbmcgui
import xbmcplugin

import catalog
import kodi_notify
import youtube_probe

CONTENT_MUSICVIDEOS = "musicvideos"
YOUTUBE_PLAY_URI = "plugin://plugin.video.youtube/play/?video_id={video_id}"
YOUTUBE_THUMB_URI = "https://img.youtube.com/vi/{video_id}/0.jpg"


def addon_root() -> str:
    return xbmcaddon.Addon().getAddonInfo("path")


def csv_dir() -> str:
    return os.path.join(addon_root(), "resources", "csv")


def set_musicvideos_content(handle: int) -> None:
    xbmcplugin.setContent(handle, CONTENT_MUSICVIDEOS)


def folder_listitem(label: str) -> xbmcgui.ListItem:
    li = xbmcgui.ListItem(label=label)
    li.setArt({"icon": "DefaultFolder.png", "thumb": "DefaultFolder.png"})
    return li


def song_listitem(title: str, video_id: str) -> xbmcgui.ListItem:
    """Build a playable song item; thumbnail failures must not block the row."""
    li = xbmcgui.ListItem(label=title)
    thumb = YOUTUBE_THUMB_URI.format(video_id=video_id)
    try:
        li.setArt({"icon": thumb, "thumb": thumb})
    except Exception:
        pass
    li.setProperty("IsPlayable", "true")
    return li


def resolve_youtube_playback(handle: int, video_id: str) -> str:
    """Resolve play via YouTube addon; block early on private/unavailable ids."""
    status = youtube_probe.probe_youtube_video(video_id)
    if status in (
        youtube_probe.STATUS_PRIVATE,
        youtube_probe.STATUS_UNAVAILABLE,
    ):
        kodi_notify.notify_playback_blocked(status)
        xbmcplugin.setResolvedUrl(handle, False, xbmcgui.ListItem())
        return ""
    play_url = YOUTUBE_PLAY_URI.format(video_id=video_id)
    li = xbmcgui.ListItem(path=play_url)
    xbmcplugin.setResolvedUrl(handle, True, li)
    return play_url


def build_url(base_url: str, query: Mapping[str, str]) -> str:
    return base_url + "?" + urlencode(dict(query))


def run(argv: Optional[Sequence[str]] = None) -> None:
    """Plugin entry: list years, list a year, or resolve a song."""
    argv_list: Sequence[str] = sys.argv if argv is None else argv
    base_url = argv_list[0]
    handle = int(argv_list[1])
    args: Dict[str, List[str]] = parse_qs(argv_list[2][1:])
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
