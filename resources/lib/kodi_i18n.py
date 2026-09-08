# -*- coding: utf-8 -*-
"""Minimal i18n helper for UI strings (Kodi getLocalizedString + fallbacks)."""
from __future__ import annotations

from typing import Any

import xbmcaddon

# Fallback when language packs are missing (host tests / incomplete installs).
# Keep in sync with resources/language/*/strings.po or strings.xml ids.
_FALLBACK = {
    30000: "La Gramola de Videos",
    30001: "Hay un problema en el catálogo; se muestra lo usable.",
    30002: "Hay %d problemas en el catálogo; se muestra lo usable.",
    30003: "Este vídeo ya no está disponible en YouTube.",
    30004: (
        "Este vídeo es privado o requiere iniciar sesión en YouTube."
    ),
    30010: "Años 60",
    30011: "Años 70",
    30012: "Años 80",
    30013: "Años 90",
    30020: "Favoritos",
    30021: "Añadir a favoritos",
    30022: "Quitar de favoritos",
    30023: "No hay favoritos todavía.",
    30024: "Añadido a favoritos.",
    30025: "Quitado de favoritos.",
    30026: "No se pudo guardar el favorito.",
    30027: "Este favorito ya no está en el catálogo.",
    30030: "Buscar",
    30031: "Buscar en el catálogo",
    30032: "Sin coincidencias.",
}


def localize(string_id: int, *args: Any) -> str:
    """Return localized string ``string_id``, optionally %-formatted with ``args``."""
    text = ""
    try:
        text = xbmcaddon.Addon().getLocalizedString(string_id) or ""
    except Exception:
        text = ""
    if not text:
        text = _FALLBACK.get(string_id, str(string_id))
    if args:
        try:
            text = text % args
        except (TypeError, ValueError):
            pass
    return text
