#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Host-only: count seed rows/years in 1960–1979. Not imported by addon.py."""
from __future__ import annotations

from pathlib import Path


def main() -> None:
    csv_dir = Path(__file__).resolve().parents[1] / "resources" / "csv"
    rows = years = 0
    decades = {"60s": False, "70s": False}
    for path in sorted(csv_dir.glob("*.csv")):
        year = path.stem
        if not (year.isdigit() and 1960 <= int(year) <= 1979):
            continue
        n = sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip())
        if not n:
            continue
        years += 1
        rows += n
        decades["60s" if int(year) < 1970 else "70s"] = True
        print(year, n)
    print("years", years, "rows", rows)
    print("decade_60s", decades["60s"], "decade_70s", decades["70s"])


if __name__ == "__main__":
    main()
