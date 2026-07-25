# -*- coding: utf-8 -*-
"""SC-009 / FR-012a / FR-013: scope guards."""
import os
import xml.etree.ElementTree as ET


def test_addon_id_unchanged_and_no_routing(repo_root):
    tree = ET.parse(os.path.join(repo_root, "addon.xml"))
    root = tree.getroot()
    assert root.attrib.get("id") == "plugin.video.gramolavideos"
    requires = [
        node.attrib.get("addon")
        for node in root.findall("./requires/import")
    ]
    assert "script.module.routing" not in requires
    assert "xbmc.python" in requires
    assert "plugin.video.youtube" in requires
    text = open(os.path.join(repo_root, "addon.xml"), encoding="utf-8").read()
    assert "plugin.video.gramola" not in text or "plugin.video.gramolavideos" in text
    assert "plugin.video.gramola<" not in text
    assert "plugin.video.gramola\"" not in text


def test_language_skeleton_present(repo_root):
    for lang in ("resource.language.es_es", "resource.language.en_gb"):
        path = os.path.join(repo_root, "resources", "language", lang, "strings.xml")
        assert os.path.isfile(path)
        body = open(path, encoding="utf-8").read()
        assert 'id="30000"' in body
        assert 'id="30001"' in body
        assert 'id="30002"' in body
