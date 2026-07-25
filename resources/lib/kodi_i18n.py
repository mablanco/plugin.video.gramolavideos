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
