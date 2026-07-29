# Validation log: 003-navegacion-videos

**Feature**: Mejorar la navegación del catálogo de vídeos  
**Date opened**: 2026-07-29

## Baseline (antes de implementar)

| Aspecto | Estado | Notas | Fecha |
|---------|--------|-------|-------|
| Raíz del addon | Años planos | `mode` ausente → `catalog.list_years` (~19 carpetas 1980–1999 sin 1994) | 2026-07-29 |
| Contrato legacy | Vigente en runtime | `specs/001-auditoria-codigo/contracts/plugin-navigation.md` (años → canciones → play) | 2026-07-29 |
| Contrato objetivo | Documentado | `specs/003-navegacion-videos/contracts/plugin-navigation.md` (décadas → años → …) | 2026-07-29 |

## Pasos quickstart

| Paso | Resultado | Notas | Fecha |
|------|-----------|-------|-------|
| Parte documental: `decision.md` veredicto década→año | PASS | Opción B; matriz C1–C5 × A–C; fuera de alcance 004/005 | 2026-07-29 |
| Parte documental: criterios C1–C5 en `research.md` | PASS | R-001–R-003 | 2026-07-29 |
| Parte documental: revisar `contracts/plugin-navigation.md` | PASS | v2 + nota supersesión 001 | 2026-07-29 |
| pytest `test_catalog_decades` + query + wiring | PASS | 17 passed | 2026-07-29 |
| Smoke Kodi: raíz ≤12 décadas | PASS | Confirmado por mantenedor en Kodi | 2026-07-29 |
| Smoke Kodi: Años 80 → años → canción → play | PASS | Confirmado por mantenedor en Kodi | 2026-07-29 |
| Smoke Kodi: atrás hasta raíz | PASS | Confirmado por mantenedor en Kodi | 2026-07-29 |
| Invariante: sin cambios de formato en `resources/csv/` | PASS | `git status`/`diff` vacío bajo `resources/csv/` | 2026-07-29 |
| pytest completo `python -m pytest -q` | PASS | 40 passed | 2026-07-29 |

## Notas adicionales

- Constitution IV enmendada a 1.3.0 (décadas → años → canciones → play).
- Addon bump `0.3.1` → `0.3.2`; URI YouTube e import `plugin.video.youtube` intactos.
- `.gitignore` sigue bloqueando `.env*`, secretos y `.specify/feature.json` (constitution IX).
- Recorrido atrás (US3): confirmado en smoke Kodi (pila nativa con carpetas década/año).
- Smoke Kodi completo (SC-003, SC-005): PASS según mantenedor.
