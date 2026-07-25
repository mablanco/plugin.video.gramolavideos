# -*- coding: utf-8 -*-
"""Query contract mode / foldername (quickstart C5, plugin-navigation.md)."""
import pytest

pytestmark = pytest.mark.legacy_freeze

# Contract snapshot — keep in sync with contracts/plugin-navigation.md
MODES = {None, "year", "song"}
FOLDERNAME_FOR = {
    None: None,  # unused when listing years
    "year": "YYYY",
    "song": "video_id",
}


def test_mode_values_documented():
    assert MODES == {None, "year", "song"}


def test_parse_qs_mode_none_for_root():
    from urllib.parse import parse_qs

    args = parse_qs("")  # argv[2][1:] when argv[2] == '?'
    assert args.get("mode", None) is None


def test_parse_qs_year_and_song():
    from urllib.parse import parse_qs

    year_args = parse_qs("mode=year&foldername=1991")
    assert year_args["mode"] == ["year"]
    assert year_args["foldername"] == ["1991"]

    song_args = parse_qs("mode=song&foldername=dQw4w9WgXcQ")
    assert song_args["mode"] == ["song"]
    assert song_args["foldername"] == ["dQw4w9WgXcQ"]


def test_foldername_roles():
    assert FOLDERNAME_FOR["year"] == "YYYY"
    assert FOLDERNAME_FOR["song"] == "video_id"
