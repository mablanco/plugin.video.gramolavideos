# -*- coding: utf-8 -*-
"""Kodi pluginsource UI: listings, resolve, and plugin entry routing."""
from __future__ import annotations

import os
import sys
from typing import Dict, List, Mapping, Optional, Sequence
from urllib.parse import parse_qs, urlencode

import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin

import catalog
import favorites
import kodi_i18n
import kodi_notify
import youtube_probe

CONTENT_MUSICVIDEOS = "musicvideos"
YOUTUBE_PLAY_URI = "plugin://plugin.video.youtube/play/?video_id={video_id}"
YOUTUBE_THUMB_URI = "https://img.youtube.com/vi/{video_id}/0.jpg"

# Decade folder labels (keep in sync with resources/language/*/strings.xml).
_DECADE_STRING_IDS = {
    "1960": 30010,
    "1970": 30011,
    "1980": 30012,
    "1990": 30013,
}

STRING_FAVORITES = 30020
STRING_FAV_ADD = 30021
STRING_FAV_REMOVE = 30022
STRING_FAV_EMPTY = 30023
STRING_FAV_ADDED = 30024
STRING_FAV_REMOVED = 30025
STRING_FAV_SAVE_ERROR = 30026
STRING_FAV_ORPHAN = 30027


def addon_root() -> str:
    return xbmcaddon.Addon().getAddonInfo("path")


def csv_dir() -> str:
    return os.path.join(addon_root(), "resources", "csv")


def favorites_path() -> str:
    """Per-profile favorites.json under Kodi addon_data."""
    profile = xbmc.translatePath(
        "special://profile/addon_data/plugin.video.gramolavideos"
    )
    return os.path.join(profile, "favorites.json")


def set_musicvideos_content(handle: int) -> None:
    xbmcplugin.setContent(handle, CONTENT_MUSICVIDEOS)


def decade_label(decade_id: str) -> str:
    """Localized decade folder label (e.g. ``Años 80``); no scattered literals."""
    string_id = _DECADE_STRING_IDS.get(decade_id)
    if string_id is not None:
        return kodi_i18n.localize(string_id)
    if len(decade_id) == 4 and decade_id.isdigit():
        return "Años {0}".format(decade_id[2:])
    return decade_id


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


def _attach_favorite_context(
    li: xbmcgui.ListItem,
    base_url: str,
    year_id: str,
    video_id: str,
    title: str,
    store_path: str,
) -> None:
    if favorites.contains(store_path, year_id, video_id):
        label = kodi_i18n.localize(STRING_FAV_REMOVE)
        url = build_url(
            base_url,
            {
                "mode": "favorite_remove",
                "year_id": year_id,
                "video_id": video_id,
            },
        )
    else:
        label = kodi_i18n.localize(STRING_FAV_ADD)
        url = build_url(
            base_url,
            {
                "mode": "favorite_add",
                "year_id": year_id,
                "video_id": video_id,
                "title": title,
            },
        )
    try:
        li.addContextMenuItems([(label, "RunPlugin({0})".format(url))])
    except Exception:
        pass


def _notify(message_id: int) -> None:
    kodi_notify.notify_message(kodi_i18n.localize(message_id))


def run(argv: Optional[Sequence[str]] = None) -> None:
    """Plugin entry: decades, favorites, years, songs, playback."""
    argv_list: Sequence[str] = sys.argv if argv is None else argv
    base_url = argv_list[0]
    handle = int(argv_list[1])
    args: Dict[str, List[str]] = parse_qs(argv_list[2][1:])
    mode = args.get("mode", None)
    catalog_dir = csv_dir()
    store_path = favorites_path()
    set_musicvideos_content(handle)

    if mode is None:
        fav_url = build_url(base_url, {"mode": "favorites"})
        xbmcplugin.addDirectoryItem(
            handle=handle,
            url=fav_url,
            listitem=folder_listitem(kodi_i18n.localize(STRING_FAVORITES)),
            isFolder=True,
        )
        result = catalog.list_decades(catalog_dir)
        kodi_notify.notify_catalog_errors(result.errors)
        for decade in result.decades:
            url = build_url(
                base_url, {"mode": "decade", "foldername": decade.id}
            )
            li = folder_listitem(decade_label(decade.id))
            xbmcplugin.addDirectoryItem(
                handle=handle, url=url, listitem=li, isFolder=True
            )
        xbmcplugin.endOfDirectory(handle)
        return

    if mode[0] == "favorites":
        try:
            active, _orphans = favorites.list_resolved(store_path, catalog_dir)
        except Exception:
            _notify(STRING_FAV_SAVE_ERROR)
            xbmcplugin.endOfDirectory(handle, succeeded=True)
            return
        if not active:
            _notify(STRING_FAV_EMPTY)
        for item in active:
            video = item["video"]
            url = build_url(
                base_url, {"mode": "song", "foldername": video.video_id}
            )
            li = song_listitem(video.title, video.video_id)
            _attach_favorite_context(
                li,
                base_url,
                video.year_id,
                video.video_id,
                video.title,
                store_path,
            )
            xbmcplugin.addDirectoryItem(handle=handle, url=url, listitem=li)
        xbmcplugin.endOfDirectory(handle)
        return

    if mode[0] == "favorite_add":
        year_id = args.get("year_id", [""])[0]
        video_id = args.get("video_id", [""])[0]
        title = args.get("title", [""])[0]
        ok, err = favorites.add(
            store_path, catalog_dir, year_id, video_id, title
        )
        if ok:
            _notify(STRING_FAV_ADDED)
        elif err == "not_in_catalog":
            _notify(STRING_FAV_ORPHAN)
        else:
            _notify(STRING_FAV_SAVE_ERROR)
        return

    if mode[0] == "favorite_remove":
        year_id = args.get("year_id", [""])[0]
        video_id = args.get("video_id", [""])[0]
        if favorites.remove(store_path, year_id, video_id):
            _notify(STRING_FAV_REMOVED)
        else:
            _notify(STRING_FAV_SAVE_ERROR)
        return

    if mode[0] == "decade":
        decade_id = args["foldername"][0]
        result = catalog.years_in_decade(catalog_dir, decade_id)
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
        xbmcplugin.setPluginCategory(handle, year_id)
        result = catalog.load_year(catalog_dir, year_id)
        kodi_notify.notify_catalog_errors(result.errors)
        for video in result.videos:
            url = build_url(
                base_url, {"mode": "song", "foldername": video.video_id}
            )
            li = song_listitem(video.title, video.video_id)
            _attach_favorite_context(
                li,
                base_url,
                year_id,
                video.video_id,
                video.title,
                store_path,
            )
            xbmcplugin.addDirectoryItem(handle=handle, url=url, listitem=li)
        xbmcplugin.endOfDirectory(handle)
        return

    if mode[0] == "song":
        video_id = args["foldername"][0]
        year_id = args.get("year_id", [None])[0]
        if year_id:
            result = catalog.load_year(catalog_dir, year_id)
            if not any(v.video_id == video_id for v in result.videos):
                _notify(STRING_FAV_ORPHAN)
                xbmcplugin.setResolvedUrl(handle, False, xbmcgui.ListItem())
                return
        resolve_youtube_playback(handle, video_id)
