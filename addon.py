# -*- coding: utf-8 -*-
"""Thin Kodi pluginsource entry — delegates to resources.lib.kodi_plugin."""
import os
import sys

_lib_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources", "lib")
if _lib_dir not in sys.path:
    sys.path.insert(0, _lib_dir)

import kodi_plugin  # noqa: E402

kodi_plugin.run()
