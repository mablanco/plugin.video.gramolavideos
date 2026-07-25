# -*- coding: utf-8 -*-
"""SC-006: zero known-invalid YouTube ids in versioned catalog (T045)."""
import csv
import os

import catalog


def test_all_catalog_video_ids_match_contract(csv_dir):
    bad = []
    for filename in os.listdir(csv_dir):
        if not filename.endswith(".csv"):
            continue
        year_id = os.path.splitext(filename)[0]
        path = os.path.join(csv_dir, filename)
        with open(path, "r", encoding="utf-8", newline="") as fh:
            for lineno, fields in enumerate(csv.reader(fh, delimiter=";"), 1):
                if not fields or (len(fields) == 1 and not fields[0].strip()):
                    continue
                video, err = catalog._parse_row(fields, year_id)
                if err is not None:
                    bad.append((filename, lineno, err.code, fields))
                assert video is not None or err is not None
    assert bad == [], "invalid catalog rows: {0}".format(bad)
