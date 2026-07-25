# -*- coding: utf-8 -*-
"""Recoverable-error notifications for catalog issues (constitution VIII)."""
import xbmcgui

DEFAULT_HEADING = "La Gramola de Videos"


def notify_catalog_errors(errors, heading=DEFAULT_HEADING):
    """Show a friendly notice when ``errors`` is non-empty; no-op if empty."""
    if not errors:
        return
    count = len(errors)
    if count == 1:
        message = "Hay un problema en el catálogo; se muestra lo usable."
    else:
        message = (
            "Hay {0} problemas en el catálogo; se muestra lo usable.".format(count)
        )
    xbmcgui.Dialog().notification(heading, message, time=5000)
