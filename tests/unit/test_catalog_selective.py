# -*- coding: utf-8 -*-
"""Prove selective catalog I/O (SC-004 / quickstart R1–R2)."""
import os

import catalog


def test_list_years_does_not_open_csv_contents(csv_dir, monkeypatch):
    opened = []
    real_open = open

    def tracking_open(path, *args, **kwargs):
        opened.append(os.path.abspath(str(path)))
        return real_open(path, *args, **kwargs)

    monkeypatch.setattr("builtins.open", tracking_open)
    result = catalog.list_years(csv_dir)
    assert len(result.years) >= 19
    assert len(result.years) == len(
        [f for f in os.listdir(csv_dir) if f.endswith(".csv")]
    )
    assert result.videos == []
    assert not any(p.endswith(".csv") for p in opened)


def test_load_year_opens_only_requested_csv(csv_dir, monkeypatch):
    opened = []
    real_open = open

    def tracking_open(path, *args, **kwargs):
        opened.append(os.path.abspath(str(path)))
        return real_open(path, *args, **kwargs)

    monkeypatch.setattr("builtins.open", tracking_open)
    result = catalog.load_year(csv_dir, "1991")
    assert result.videos
    csv_opens = [p for p in opened if p.endswith(".csv")]
    assert csv_opens == [os.path.abspath(os.path.join(csv_dir, "1991.csv"))]
    assert not any(p.endswith("1990.csv") for p in csv_opens)
