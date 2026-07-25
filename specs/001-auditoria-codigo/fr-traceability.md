# FR-001–FR-020 evidence map (SC-007 / T052)

**Feature**: `001-auditoria-codigo`  
**Updated**: 2026-07-25

| FR | Evidencia | Notas |
|----|-----------|-------|
| FR-001 | `kodi_plugin.run` años→canciones→YouTube | Flujo preservado |
| FR-002 | `resources/csv/*.csv` + `catalog._parse_row` | Formato `;` |
| FR-003 | `addon.xml` `xbmc.python` 3.0.0; US1 | Matrix+ |
| FR-004 | `catalog.py` vs `kodi_plugin.py` | Datos ≠ UI |
| FR-005 | `tests/stubs/` + `conftest.py` | Suite sin Kodi |
| FR-006 | `kodi_notify.notify_catalog_errors` | Aviso + residual |
| FR-007 | Validación + `CatalogError` (US2) | Omitir inválidos |
| FR-008 | `list_years` stems-only + `test_catalog_selective` | SC-004 |
| FR-009 | `load_year` un fichero + selective tests | SC-004 |
| FR-010 | URI `plugin://plugin.video.youtube/...` | Sin rehost |
| FR-011 | `addon.xml` version + `changelog.txt` | Por US |
| FR-012 | Complexity Tracking en `plan.md` | Sin routing |
| FR-012a | Sin fusión scaffold; `test_scope_guards` | SC-009 |
| FR-012b | Entry fino + lib + notify + i18n | Polish T048–T049 |
| FR-013 | id `plugin.video.gramolavideos` | `test_scope_guards` |
| FR-014 | `resources/icon.png`, `fanart.jpg` en assets | Sin cambio destructivo |
| FR-015 | `resources/language/.../strings.xml` + `kodi_i18n` | es_es + en_gb |
| FR-016 | `spec.md` + `audit-findings.md` + este mapa | Inventario trazable |
| FR-017 | US6 description/README + Chiquilla fix | SC-006 |
| FR-018 | Default branch `main` (US5) | `gh repo view` |
| FR-019 | README/changelog sin `commits/master` | US5 |
| FR-020 | `master` retirada tras rename | US5 |

**Exclusiones justificadas (Complexity Tracking / plan)**: no `script.module.routing`; no fusión `plugin.video.gramola`; no mypy estricto en CI (R-012).
