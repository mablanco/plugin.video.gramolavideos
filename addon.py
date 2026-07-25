# -*- coding: utf-8 -*-
import os
import sys
from urllib.parse import parse_qs, urlencode

import xbmcplugin

# Bootstrap resources/lib (Kodi + host tests)
_lib_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources", "lib")
if _lib_dir not in sys.path:
    sys.path.insert(0, _lib_dir)
import catalog  # noqa: E402
import kodi_plugin  # noqa: E402

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = parse_qs(sys.argv[2][1:])
csvdir = kodi_plugin.csv_dir()
kodi_plugin.set_musicvideos_content(addon_handle)
mode = args.get("mode", None)


def build_url(query):
    return base_url + "?" + urlencode(query)


videoslists = catalog.load_all_videos(csvdir)
yearslist = videoslists.keys()
if mode is None:
    for year in sorted(yearslist):
        url = build_url({"mode": "year", "foldername": year})
        li = kodi_plugin.folder_listitem(year)
        xbmcplugin.addDirectoryItem(
            handle=addon_handle, url=url, listitem=li, isFolder=True
        )
    xbmcplugin.endOfDirectory(addon_handle)
elif mode[0] == "year":
    foldername = args["foldername"][0]
    for musicvideo in sorted(videoslists[foldername]):
        # Short / incomplete rows may IndexError — unchanged until US2 validation
        video_id = musicvideo[1]
        url = build_url({"mode": "song", "foldername": video_id})
        li = kodi_plugin.song_listitem(musicvideo[0], video_id)
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
    xbmcplugin.endOfDirectory(addon_handle)
elif mode[0] == "song":
    foldername = args["foldername"][0]
    kodi_plugin.resolve_youtube_playback(addon_handle, foldername)
