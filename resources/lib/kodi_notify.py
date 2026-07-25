# -*- coding: utf-8 -*-
"""Recoverable-error notifications for catalog issues (constitution VIII)."""
from __future__ import annotations

from typing import Iterable, Optional

import xbmcgui

import kodi_i18n
from catalog import CatalogError

STRING_HEADING = 30000
STRING_CATALOG_ONE = 30001
STRING_CATALOG_MANY = 30002


def notify_catalog_errors(
    errors: Iterable[CatalogError], heading: Optional[str] = None
) -> None:
    """Show a friendly notice when ``errors`` is non-empty; no-op if empty."""
    error_list = list(errors)
    if not error_list:
        return
    if heading is None:
        heading = kodi_i18n.localize(STRING_HEADING)
    count = len(error_list)
    if count == 1:
        message = kodi_i18n.localize(STRING_CATALOG_ONE)
    else:
        message = kodi_i18n.localize(STRING_CATALOG_MANY, count)
    xbmcgui.Dialog().notification(heading, message, time=5000)
