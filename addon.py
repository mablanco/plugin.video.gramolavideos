# -*- coding: utf-8 -*-
import os
import sys
import csv
import urllib
import urlparse
import xbmc,xbmcgui,xbmcplugin

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])
addonID = 'plugin.video.gramolavideos'
csvdir = xbmc.translatePath('special://home/addons/' + addonID + '/resources/csv/').decode('utf-8')
xbmcplugin.setContent(addon_handle, 'movies')
mode = args.get('mode', None)

def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

videoslists = {}
for filename in os.listdir(csvdir):
    if filename.endswith(".csv"):
        with open(os.path.join(csvdir, filename), 'rb') as csvfile:
            videosreader = csv.reader(csvfile, delimiter=';')
            tempvideotuple = tuple(videosreader)
            videoslists[os.path.splitext(filename)[0]] = tempvideotuple
yearslist = videoslists.keys()
if mode is None:
    for year in sorted(yearslist):
        url = build_url({'mode': 'year', 'foldername': year})
        li = xbmcgui.ListItem(year, iconImage='DefaultFolder.png')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)
elif mode[0] == 'year':
    foldername = args['foldername'][0]
    for musicvideo in sorted(videoslists[foldername]):
        video_id = musicvideo[1]
        url = build_url({'mode': 'song', 'foldername': video_id})
        img = "http://img.youtube.com/vi/"+video_id+"/0.jpg"
        li = xbmcgui.ListItem(musicvideo[0], iconImage=img, thumbnailImage=img)
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
    xbmcplugin.endOfDirectory(addon_handle)
elif mode[0] == 'song':
    foldername = args['foldername'][0]
    xbmc.Player().play('plugin://plugin.video.youtube/play/?video_id='+foldername)
