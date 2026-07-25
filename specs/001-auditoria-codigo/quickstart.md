# Quickstart: Validación de la remediación incremental

**Feature**: `001-auditoria-codigo`  
**Date**: 2026-07-25

Guía de validación end-to-end por fase. Detalles de entidades: [data-model.md](./data-model.md). Contratos: [contracts/](./contracts/).

## Prerequisites

- Python 3.x en el host del mantenedor.
- `pytest` instalado en el entorno de desarrollo (no se declara en `addon.xml`).
- Kodi Matrix+ (o el target moderno acordado) + `plugin.video.youtube` para pruebas manuales de reproducción.
- Checkout del repo con catálogo en `resources/csv/`.

## Setup (tests)

```bash
cd /path/to/plugin.video.gramolavideos
python -m pip install pytest
# Tras existir tests/ (Fase 1):
python -m pytest -q
```

## Fase 1 — Caracterización (safety net)

### Escenarios automatizados

| # | Escenario | Esperado |
|---|-----------|----------|
| C1 | CSV de ejemplo válido | Se obtienen años / entradas según comportamiento *actual* documentado |
| C2 | Fila incompleta / campos de más | Comportamiento legacy fijado (hoy: puede tumbar o producir filas raras — capturar el real) |
| C3 | Año ausente / dir vacío | Resultado no catastrófico según extract actual |
| C4 | Inventario de años del repo | Lista de stems `1980`…`1999` sin `1994` coincide con ficheros presentes |
| C5 | Query contract | Documentado: `mode` / `foldername` como en [plugin-navigation.md](./contracts/plugin-navigation.md) |

### Criterio de salida Fase 1

- Suite verde sobre lógica de catálogo **sin** UI Kodi (SC-003 baseline).
- Ningún cambio funcional de producto todavía (salvo extract literal necesario para testear).

## Fase 2 — Bugs críticos

### Automatizado

| # | Escenario | Esperado |
|---|-----------|----------|
| B1 | Fila con `video_id` ≠ 11 chars (p. ej. Chiquilla) | Omitida + error `row_bad_video_id` |
| B2 | CSV ilegible inyectado | `errors` no vacío; resto de años listables |
| B3 | Mezcla válidas/inválidas en un año | Solo válidas en `videos` |

### Manual (Kodi)

| # | Escenario | Esperado |
|---|-----------|----------|
| M1 | Abrir addon → año → play | Recorrido &lt; 30 s en red normal (SC-001) |
| M2 | Reproducir canción válida | Delega en YouTube; historial/contexto de directorio coherente |
| M3 | CSV corrupto de prueba | Aviso comprensible; no freeze (SC-002) |

### Gobernanza

```bash
gh repo view mablanco/plugin.video.gramolavideos --json defaultBranchRef --jq .defaultBranchRef.name
# Esperado: main
rg -n 'commits/master|\bmaster\b' README.md changelog.txt || true
```

### Criterio de salida Fase 2

- Hallazgos P1 del inventario cerrados o con decisión explícita (SC-005).
- Default branch `main` (SC-008).
- pytest verde con assertions de validación *deseada*.

## Fase 3 — Refactor y deuda

### Automatizado / diseño

| # | Escenario | Esperado |
|---|-----------|----------|
| R1 | `list_years` | No materializa todas las canciones (SC-004) |
| R2 | `load_year` | Solo lee el CSV de ese año |
| R3 | Cambio de etiqueta UI | No modifica reglas de parseo CSV (US3) |

### Manual / producto

| # | Escenario | Esperado |
|---|-----------|----------|
| R4 | Descripción vs años | Sin contradicción editorial grave (SC-006) |
| R5 | Catálogo versionado | 0 ids YouTube inválidos conocidos |

### Criterio de salida Fase 3

- Layout `addon.py` fino + `resources/lib/` (kodi vs datos).
- Deuda README de carga completa abordada.
- Versión/`changelog` actualizados si hubo cambio de comportamiento (FR-011).

## Out of scope checks

- No debe aparecer dependencia de `script.module.routing` ni fusión del scaffold `plugin.video.gramola` (SC-009).
- Id del addon sigue siendo `plugin.video.gramolavideos` (FR-013).
