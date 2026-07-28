# -*- coding: utf-8 -*-
"""Lightweight YouTube availability probe via oEmbed (no API key)."""
from __future__ import annotations

from typing import Optional
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

OEMBED_URL = (
    "https://www.youtube.com/oembed?url="
    "https://www.youtube.com/watch?v={video_id}&format=json"
)
DEFAULT_TIMEOUT_SECONDS = 5.0

STATUS_OK = "ok"
STATUS_PRIVATE = "private"
STATUS_UNAVAILABLE = "unavailable"
STATUS_UNKNOWN = "unknown"


def classify_oembed_http_status(http_status: Optional[int]) -> str:
    """Map an oEmbed HTTP status to a coarse playback availability class."""
    if http_status == 200:
        return STATUS_OK
    if http_status == 403:
        return STATUS_PRIVATE
    if http_status == 404:
        return STATUS_UNAVAILABLE
    return STATUS_UNKNOWN


def probe_youtube_video(
    video_id: str, timeout: float = DEFAULT_TIMEOUT_SECONDS
) -> str:
    """Return availability class for ``video_id`` using YouTube oEmbed.

    On network/timeout errors returns ``unknown`` so callers may still attempt
    playback via the YouTube addon.
    """
    url = OEMBED_URL.format(video_id=video_id)
    request = Request(url, headers={"User-Agent": "plugin.video.gramolavideos"})
    try:
        with urlopen(request, timeout=timeout) as response:
            return classify_oembed_http_status(getattr(response, "status", 200))
    except HTTPError as exc:
        return classify_oembed_http_status(exc.code)
    except (URLError, TimeoutError, OSError, ValueError):
        return STATUS_UNKNOWN
