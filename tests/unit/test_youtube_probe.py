# -*- coding: utf-8 -*-
"""Unit tests for YouTube oEmbed availability probe."""
import youtube_probe


def test_classify_oembed_http_status():
    assert youtube_probe.classify_oembed_http_status(200) == youtube_probe.STATUS_OK
    assert (
        youtube_probe.classify_oembed_http_status(403)
        == youtube_probe.STATUS_PRIVATE
    )
    assert (
        youtube_probe.classify_oembed_http_status(404)
        == youtube_probe.STATUS_UNAVAILABLE
    )
    assert (
        youtube_probe.classify_oembed_http_status(500)
        == youtube_probe.STATUS_UNKNOWN
    )
    assert (
        youtube_probe.classify_oembed_http_status(None)
        == youtube_probe.STATUS_UNKNOWN
    )


def test_probe_maps_http_error(monkeypatch):
    from urllib.error import HTTPError
    from io import BytesIO

    def fake_urlopen(request, timeout=0):
        raise HTTPError(request.full_url, 403, "Forbidden", hdrs=None, fp=BytesIO())

    monkeypatch.setattr(youtube_probe, "urlopen", fake_urlopen)
    assert (
        youtube_probe.probe_youtube_video("abcdefghijk")
        == youtube_probe.STATUS_PRIVATE
    )


def test_probe_unknown_on_network_error(monkeypatch):
    from urllib.error import URLError

    def fake_urlopen(request, timeout=0):
        raise URLError("down")

    monkeypatch.setattr(youtube_probe, "urlopen", fake_urlopen)
    assert (
        youtube_probe.probe_youtube_video("abcdefghijk")
        == youtube_probe.STATUS_UNKNOWN
    )
