# Audit findings status (SC-005 / T046)

**Feature**: `001-auditoria-codigo`  
**Updated**: 2026-07-25

Estado de los hallazgos del inventario de la spec tras la remediación incremental.

| Id | Severidad | Hallazgo | Status | Evidencia |
|----|-----------|----------|--------|-----------|
| P1-compat | P1 | Runtime/APIs Python 2 / Kodi antiguo | **fixed** | US1: `xbmc.python` 3.0.0, urllib.parse, ListItem moderno, `setResolvedUrl` |
| P1-paths | P1 | Rutas `special://home/addons/...` frágiles | **fixed** | US1: `Addon.getAddonInfo('path')` en `kodi_plugin.csv_dir` |
| P1-robustez | P1 | Filas/CSV malos sin aviso / aborto | **fixed** | US2: validación + `CatalogError` + `kodi_notify` |
| P1-chiquilla | P1 | Id YouTube inválido en 1991 | **fixed** | US2: `-d3mZmP_me4` en `resources/csv/1991.csv` |
| P2-carga | P2 | Carga completa del catálogo al listar años | **fixed** | US4: `list_years` stems-only; `load_year` un fichero |
| P2-monolito | P2 | Datos y UI acoplados en `addon.py` | **fixed** | US3 extract + US4 `addon.py` fino / `kodi_plugin.run` |
| P2-editorial | P2 | Promesa 60s–90s vs cobertura ~1980–1999 | **fixed** | US6: description/README alineados a 80s–90s; 60–70 como TODO de contenido |
| P2-main | P2 | Rama canónica `master` | **fixed** | US5: default `main` + protección de rama |
| P3-i18n | P3 | Cadenas UI sin esqueleto i18n | **fixed** | Polish: `resources/language/` + `kodi_i18n` |
| P3-typing | P3 | Sin type hints en lib | **fixed** | Polish: hints graduales en `resources/lib/` |
| P3-changelog | P3 | Historial poco útil / enlaces a master | **fixed** | US1–US5 changelog + commits/main |

**P1 abiertos**: ninguno.  
**SC-006**: 0 ids inválidos conocidos en `resources/csv/` (suite `test_catalog_video_ids.py`).
