# -*- coding: utf-8 -*-
"""Minimal xbmcplugin stub that records calls for assertions."""

_calls = []


def reset():
    global _calls
    _calls = []


def _record(name, **kwargs):
    _calls.append({"name": name, "kwargs": kwargs})


def addDirectoryItem(handle, url, listitem, isFolder=False, totalItems=0):
    _record(
        "addDirectoryItem",
        handle=handle,
        url=url,
        listitem=listitem,
        isFolder=isFolder,
        totalItems=totalItems,
    )
    return True


def endOfDirectory(handle, succeeded=True, updateListing=False, cacheToDisc=True):
    _record(
        "endOfDirectory",
        handle=handle,
        succeeded=succeeded,
        updateListing=updateListing,
        cacheToDisc=cacheToDisc,
    )


def setResolvedUrl(handle, succeeded, listitem):
    _record(
        "setResolvedUrl",
        handle=handle,
        succeeded=succeeded,
        listitem=listitem,
    )


def setContent(handle, content):
    _record("setContent", handle=handle, content=content)


def get_calls():
    return list(_calls)


def calls_named(name):
    return [c for c in _calls if c["name"] == name]
