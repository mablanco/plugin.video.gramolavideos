# -*- coding: utf-8 -*-
"""Pytest harness: inject Kodi API stubs before addon imports.

Run the suite on host Python 3 without launching Kodi:

    python -m pip install -r requirements-dev.txt
    python -m pytest -q
"""
from __future__ import print_function

import os
import sys

import pytest

_REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_STUBS_DIR = os.path.join(os.path.dirname(__file__), "stubs")
_LIB_DIR = os.path.join(_REPO_ROOT, "resources", "lib")


def pytest_configure(config):
    # Stubs first so `import xbmc*` resolves to tests/stubs
    if _STUBS_DIR not in sys.path:
        sys.path.insert(0, _STUBS_DIR)
    if _LIB_DIR not in sys.path:
        sys.path.insert(0, _LIB_DIR)
    if _REPO_ROOT not in sys.path:
        sys.path.insert(0, _REPO_ROOT)


@pytest.fixture(autouse=True)
def _reset_kodi_stubs():
    import xbmc
    import xbmcaddon
    import xbmcgui
    import xbmcplugin

    xbmc.reset()
    xbmcgui.reset()
    xbmcplugin.reset()
    xbmcaddon.reset()
    # Fake Kodi addon install root = repo root (contains resources/csv)
    xbmc.set_translate_root(_REPO_ROOT)
    xbmcaddon.set_addon_root(_REPO_ROOT)
    yield
    xbmc.reset()
    xbmcgui.reset()
    xbmcplugin.reset()
    xbmcaddon.reset()


@pytest.fixture
def repo_root():
    return _REPO_ROOT


@pytest.fixture
def csv_dir(repo_root):
    return os.path.join(repo_root, "resources", "csv")


@pytest.fixture
def fixtures_dir():
    return os.path.join(os.path.dirname(__file__), "fixtures")
