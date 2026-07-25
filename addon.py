# -*- coding: utf-8 -*-
import os
import sys

try:
    from urllib.parse import parse_qs, urlencode
except ImportError:
    from urllib import urlencode
    from urlparse import parse_qs

import xbmc
import xbmcgui
import xbmcplugin

# Bootstrap resources/lib for catalog (Kodi + host tests)
_lib_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources", "lib")
if _lib_dir not in sys.path:
    sys.path.insert(0, _lib_dir)
import catalog  # noqa: E402

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = parse_qs(sys.argv[2][1:])
addonID = "plugin.video.gramolavideos"
_csvdir = xbmc.translatePath("special://home/addons/" + addonID + "/resources/csv/")
csvdir = _csvdir.decode("utf-8") if isinstance(_csvdir, bytes) else _csvdir
xbmcplugin.setContent(addon_handle, "movies")
mode = args.get("mode", None)


def build_url(query):
    return base_url + "?" + urlencode(query)


videoslists = catalog.load_all_videos(csvdir)
yearslist = videoslists.keys()
if mode is None:
    for year in sorted(yearslist):
        url = build_url({"mode": "year", "foldername": year})
        li = xbmcgui.ListItem(year, iconImage="DefaultFolder.png")
        xbmcplugin.addDirectoryItem(
            handle=addon_handle, url=url, listitem=li, isFolder=True
        )
    xbmcplugin.endOfDirectory(addon_handle)
elif mode[0] == "year":
    foldername = args["foldername"][0]
    for musicvideo in sorted(videoslists[foldername]):
        video_id = musicvideo[1]
        url = build_url({"mode": "song", "foldername": video_id})
        img = "http://img.youtube.com/vi/" + video_id + "/0.jpg"
        li = xbmcgui.ListItem(musicvideo[0], iconImage=img, thumbnailImage=img)
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
    xbmcplugin.endOfDirectory(addon_handle)
elif mode[0] == "song":
    foldername = args["foldername"][0]
    xbmc.Player().play(
        "plugin://plugin.video.youtube/play/?video_id=" + foldername
    )
