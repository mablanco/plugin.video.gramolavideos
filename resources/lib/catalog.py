# -*- coding: utf-8 -*-
"""Catalog CSV load — literal extract from addon.py (no semantic change)."""
from __future__ import print_function

import csv
import io
import os
import sys


class CatalogLoadResult(object):
    """Minimal result shape (full validation arrives in US2)."""

    def __init__(self, years=None, videos=None, errors=None, ok=True):
        self.years = years if years is not None else []
        self.videos = videos if videos is not None else []
        self.errors = errors if errors is not None else []
        self.ok = ok


def load_all_videos(csv_dir):
    """Discover ``*.csv`` under ``csv_dir`` and parse rows with ``;`` delimiter.

    Mirrors the legacy ``addon.py`` loop: binary open on Py2, text wrapper on
    Py3 so host pytest can characterize the same row shapes.
    """
    videoslists = {}
    if not os.path.isdir(csv_dir):
        return videoslists
    for filename in os.listdir(csv_dir):
        if filename.endswith(".csv"):
            path = os.path.join(csv_dir, filename)
            with open(path, "rb") as raw:
                if sys.version_info[0] >= 3:
                    csvfile = io.TextIOWrapper(raw, encoding="utf-8", newline="")
                else:
                    csvfile = raw
                videosreader = csv.reader(csvfile, delimiter=";")
                tempvideotuple = tuple(videosreader)
                videoslists[os.path.splitext(filename)[0]] = tempvideotuple
    return videoslists


def list_years(csv_dir):
    """Return years discovered under ``csv_dir`` (legacy: may read all CSVs)."""
    data = load_all_videos(csv_dir)
    years = sorted(data.keys())
    return CatalogLoadResult(years=years, ok=True)


def load_year(csv_dir, year_id):
    """Return rows for ``year_id`` (legacy: may load the whole catalog first)."""
    data = load_all_videos(csv_dir)
    rows = list(data.get(year_id, ()))
    return CatalogLoadResult(videos=rows, ok=True)
