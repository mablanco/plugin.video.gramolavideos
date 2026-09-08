# -*- coding: utf-8 -*-
"""Minimal xbmcaddon stub with configurable addon root."""

_addon_root = None
_addon_info = {
    "id": "plugin.video.gramolavideos",
    "name": "La Gramola de Videos",
    "version": "0.0.0",
}
_STRINGS = {
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


def reset():
    global _addon_root
    _addon_root = None


def set_addon_root(path):
    global _addon_root
    _addon_root = path


class Addon(object):
    def __init__(self, id=None):
        self._id = id or _addon_info["id"]

    def getAddonInfo(self, key):
        if key == "path":
            if _addon_root is not None:
                return _addon_root
            return ""
        return _addon_info.get(key, "")

    def getSetting(self, key):
        return ""

    def getLocalizedString(self, string_id):
        return _STRINGS.get(int(string_id), "")
