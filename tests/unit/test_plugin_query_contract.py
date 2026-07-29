# -*- coding: utf-8 -*-
"""Query contract mode / foldername (plugin-navigation v2 — decades)."""
import pytest

pytestmark = pytest.mark.legacy_freeze

# Contract snapshot — keep in sync with specs/003-navegacion-videos/contracts/plugin-navigation.md
MODES = {None, "decade", "year", "song"}
FOLDERNAME_FOR = {
    None: None,  # unused when listing decades
    "decade": "D",  # decade start year e.g. 1980
    "year": "YYYY",
    "song": "video_id",
}


def test_mode_values_documented():
    assert MODES == {None, "decade", "year", "song"}


def test_parse_qs_mode_none_for_root():
    from urllib.parse import parse_qs

    args = parse_qs("")  # argv[2][1:] when argv[2] == '?'
    assert args.get("mode", None) is None


def test_parse_qs_decade_year_and_song():
    from urllib.parse import parse_qs

    decade_args = parse_qs("mode=decade&foldername=1980")
    assert decade_args["mode"] == ["decade"]
    assert decade_args["foldername"] == ["1980"]

    year_args = parse_qs("mode=year&foldername=1991")
    assert year_args["mode"] == ["year"]
    assert year_args["foldername"] == ["1991"]

    song_args = parse_qs("mode=song&foldername=dQw4w9WgXcQ")
    assert song_args["mode"] == ["song"]
    assert song_args["foldername"] == ["dQw4w9WgXcQ"]


def test_foldername_roles():
    assert FOLDERNAME_FOR["decade"] == "D"
    assert FOLDERNAME_FOR["year"] == "YYYY"
    assert FOLDERNAME_FOR["song"] == "video_id"
