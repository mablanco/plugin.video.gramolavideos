#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Host-only: resolve YouTube ids for seed candidates via yt-dlp search."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

VIDEO_ID_RE = re.compile(r"^[A-Za-z0-9_-]{11}$")
TITLE_RE = re.compile(r".+\s-\s.+")

# year, title (Artista - Canción)
SEED = [
    (1965, "Los Brincos - Mejor"),
    (1966, "Los Bravos - Black Is Black"),
    (1966, "Los Brincos - Un sorbito de champagne"),
    (1967, "Los Brincos - Lola"),
    (1967, "Juan y Junior - Anduriña"),
    (1967, "Los Ángeles - Mañana, mañana"),
    (1968, "Massiel - La, la, la"),
    (1968, "Joan Manuel Serrat - La tieta"),
    (1968, "Raphael - Digan lo que digan"),
    (1969, "Fórmula V - Cuéntame"),
    (1969, "Los Canarios - Get On Your Knees"),
    (1969, "Karina - El baúl de los recuerdos"),
    (1969, "Miguel Ríos - El río"),
    (1970, "Miguel Ríos - Himno a la alegría"),
    (1970, "Fórmula V - Vacaciones de verano"),
    (1970, "Nino Bravo - Te quiero, te quiero"),
    (1970, "Pop Tops - Oh Lord, Why Lord"),
    (1971, "Pop Tops - Mamy Blue"),
    (1971, "Joan Manuel Serrat - Mediterráneo"),
    (1971, "Nino Bravo - Mi gran amor"),
    (1971, "Los Diablos - Un rayo de sol"),
    (1971, "Fórmula V - Eva María"),
    (1972, "Nino Bravo - Un beso y una flor"),
    (1972, "Julio Iglesias - Un canto a Galicia"),
    (1972, "Camilo Sesto - Algo de mí"),
    (1972, "Mari Trini - Yo no soy esa"),
    (1972, "Juan Pardo - La balada del hombre del sur"),
    (1973, "Mocedades - Eres tú"),
    (1973, "Camilo Sesto - Algo más"),
    (1973, "Nino Bravo - América, América"),
    (1973, "Joan Manuel Serrat - Penélope"),
    (1973, "Las Grecas - Te estoy amando locamente"),
    (1974, "Camilo Sesto - ¿Quieres ser mi amante?"),
    (1974, "Mocedades - Tómame o déjame"),
    (1974, "Juan Bau - La estrella de David"),
    (1974, "Danny Daniel - Por el amor de una mujer"),
    (1975, "Cecilia - Un ramito de violetas"),
    (1975, "Triana - Abre la puerta"),
    (1975, "Camilo Sesto - Melina"),
    (1975, "Braulio - Contigo"),
    (1975, "Víctor Manuel - Soy un corazón tendido al sol"),
    (1976, "Triana - En el lago"),
    (1976, "Camilo Sesto - Vivir así es morir de amor"),
    (1976, "Miguel Bosé - Linda"),
    (1976, "Baccara - Yes Sir, I Can Boogie"),
    (1977, "Triana - Tu frialdad"),
    (1977, "Camilo Sesto - El amor de mi vida"),
    (1977, "Miguel Bosé - Amelia"),
    (1977, "Alameda - Aires de la Alameda"),
    (1978, "Burning - Qué hace una chica como tú en un sitio como éste"),
    (1978, "Tequila - Salta"),
    (1978, "Miguel Bosé - Super Superman"),
    (1978, "Triana - Una historia"),
    (1979, "Leño - Este Madrid"),
    (1979, "Tequila - Rock and Roll en la plaza del pueblo"),
    (1979, "Asfalto - Capitan Trueno"),
    (1964, "Los Sírex - La escoba"),
    (1965, "Los Relámpagos - Noches de blanco satén"),
    (1966, "Lone Star - La caza"),
    (1968, "Joan Manuel Serrat - Cançó de matinada"),
]


def resolve_id(title: str) -> str:
    query = f"ytsearch1:{title} oficial OR live OR vídeo musical"
    try:
        out = subprocess.check_output(
            [
                "yt-dlp",
                "--flat-playlist",
                "--print",
                "%(id)s",
                "--no-warnings",
                "-q",
                query,
            ],
            text=True,
            timeout=60,
            stderr=subprocess.DEVNULL,
        ).strip()
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
        return ""
    line = out.splitlines()[0].strip() if out else ""
    return line if VIDEO_ID_RE.match(line) else ""


def main() -> None:
    rows = []
    seen_ids: set[str] = set()
    for year, title in SEED:
        vid = resolve_id(title)
        format_ok = bool(TITLE_RE.match(title) and VIDEO_ID_RE.match(vid))
        notes = []
        if not vid:
            notes.append("no_id")
            format_ok = False
        elif vid in seen_ids:
            notes.append("dup_global")
        if vid:
            seen_ids.add(vid)
        rows.append(
            {
                "year_id": year,
                "title": title,
                "video_id": vid,
                "editorial_ok": "",
                "format_ok": format_ok,
                "notes": ";".join(notes),
            }
        )
        print(f"{year}\t{format_ok}\t{vid or '-'}\t{title}", flush=True)

    out_path = Path(__file__).resolve().parents[1] / "specs/004-catalogo-60-70/seed-work/resolved.json"
    out_path.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    ok = sum(1 for r in rows if r["format_ok"])
    print(f"resolved_ok={ok}/{len(rows)} -> {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
