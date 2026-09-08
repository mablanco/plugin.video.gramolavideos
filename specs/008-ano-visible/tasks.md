# Tasks: Año visible al entrar en un año

**Input**: Design documents from `/specs/008-ano-visible/`

**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/, quickstart.md

**Tests**: El plan exige assert de `setPluginCategory` en wiring; se incluye test unitario. Smoke Kodi en polish.

**Organization**: Cambio mínimo en `mode=year`; US2/US3 son validación de no-regresión y coherencia.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- Artefactos: `specs/008-ano-visible/`
- Runtime: `resources/lib/kodi_plugin.py`
- Tests: `tests/unit/test_plugin_wiring.py`
- Docs/release: `README.md` (solo si hace falta), `addon.xml`, `changelog.txt`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Confirmar artefactos y registro de validación

- [X] T001 Verificar que existen `specs/008-ano-visible/plan.md`, `spec.md`, `research.md`, `data-model.md`, `quickstart.md` y `contracts/plugin-navigation.md`
- [X] T002 [P] Crear `specs/008-ano-visible/validation-log.md` con pasos del `quickstart.md` (pytest wiring + smoke Kodi) y columnas Resultado / Notas / Fecha
- [X] T003 [P] Anotar en `specs/008-ano-visible/validation-log.md` el baseline: `mode=year` sin `setPluginCategory` en `resources/lib/kodi_plugin.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Congelar contrato de categoría; sin cambio de query string

**⚠️ CRITICAL**: No implementar UI hasta confirmar el contrato

- [X] T004 Confirmar regla `xbmcplugin.setPluginCategory(handle, year_id)` con `year_id == foldername` en `specs/008-ano-visible/contracts/plugin-navigation.md`
- [X] T005 [P] Confirmar en `specs/008-ano-visible/research.md` el rechazo a prefijar títulos de canciones y que década-en-vista-años queda fuera de MVP
- [X] T006 [P] Revisar stubs de `xbmcplugin` en `tests/` (o `tests/stubs/`) para poder capturar `setPluginCategory` en wiring

**Checkpoint**: Contrato y stubs listos

---

## Phase 3: User Story 1 - Ver el año al listar sus canciones (Priority: P1) 🎯 MVP

**Goal**: Categoría visible = año activo al entrar en un año (SC-001, SC-002)

**Independent Test**: `_run_addon("mode=year&foldername=1985")` → una llamada `setPluginCategory(..., "1985")`

### Implementation for User Story 1

- [X] T007 [US1] En la rama `mode=year` de `resources/lib/kodi_plugin.py`, invocar `xbmcplugin.setPluginCategory(handle, year_id)` antes de `endOfDirectory`, también con 0 canciones o errores recuperables
- [X] T008 [US1] Añadir assert de categoría en `tests/unit/test_plugin_wiring.py` según `specs/008-ano-visible/quickstart.md` (handle + category == year_id)
- [X] T009 [US1] Ejecutar `pytest tests/unit/test_plugin_wiring.py` y registrar PASS en `specs/008-ano-visible/validation-log.md`

**Checkpoint**: Año visible vía categoría Kodi en tests

---

## Phase 4: User Story 2 - No alterar el recorrido ni la reproducción (Priority: P1)

**Goal**: Mismos pasos decades→años→canciones→play; URLs intactas (SC-003)

**Independent Test**: Contrato query sin cambios; play y atrás sin pantallas nuevas

### Implementation for User Story 2

- [X] T010 [US2] Verificar en `tests/unit/test_plugin_query_contract.py` (o wiring) que `mode=year&foldername=YYYY` y `mode=song` no ganan parámetros nuevos
- [X] T011 [US2] Confirmar en `resources/lib/kodi_plugin.py` que títulos de canciones no se prefijan con el año y que `resolve_youtube_playback` no cambia
- [X] T012 [P] [US2] Anotar en `specs/008-ano-visible/validation-log.md` checklist: atrás sin niveles extra; reproducción igual

**Checkpoint**: Sin regresiones de navegación/play

---

## Phase 5: User Story 3 - Contexto coherente y legible (Priority: P2)

**Goal**: Categoría = mismo year_id que la carpeta del nivel anterior (SC-004)

**Independent Test**: Entrar 1980 luego 1985 → categoría cambia; errores de catálogo no abortan

### Implementation for User Story 3

- [X] T013 [US3] Extender `tests/unit/test_plugin_wiring.py` con dos invocaciones de año distintas y categorías correspondientes
- [X] T014 [US3] Confirmar que con `load_year` vacío/errores la categoría sigue fijándose y `kodi_notify.notify_catalog_errors` se conserva en `resources/lib/kodi_plugin.py`
- [X] T015 [P] [US3] Documentar en `specs/008-ano-visible/validation-log.md` que MVP no exige categoría en `mode=decade`

**Checkpoint**: Coherencia multi-año y tolerancia

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Smoke y release hygiene

- [X] T016 Completar smoke Kodi del `quickstart.md` (entrar año, scroll, cambiar de año, play) en `specs/008-ano-visible/validation-log.md`
- [X] T017 Decidir y aplicar bump en `addon.xml` / `changelog.txt` si el release incluye el cambio de UX
- [X] T018 [P] Confirmar que no hay literales i18n nuevos ni cambios CSV en el diff (constitution I/X)
- [X] T019 [P] Ejecutar suite unitaria relevante `pytest -q tests/unit/test_plugin_wiring.py` y cerrar validation-log

---

## Dependencies & Execution Order

### Phase Dependencies

- Setup → Foundational → US1 (MVP) → US2 → US3 → Polish
- US2/US3 son mayormente validación tras T007

### User Story Dependencies

- **US1**: tras Phase 2 — entrega el valor
- **US2**: tras US1
- **US3**: tras US1

### Parallel Opportunities

- T002/T003; T005/T006; T012 con docs; T015; T018/T019

---

## Parallel Example: User Story 1

```bash
Task: "Invocar setPluginCategory en resources/lib/kodi_plugin.py mode=year"
Task: "Añadir assert setPluginCategory en tests/unit/test_plugin_wiring.py"
```

---

## Implementation Strategy

### MVP First

1. Setup + contrato
2. US1 `setPluginCategory` + test → **STOP y validar**
3. US2/US3 checks → smoke → versión si aplica

### Incremental Delivery

Cambio pequeño: se puede mergear tras US1+test+smoke mínimo.

---

## Notes

- Fuera de alcance: categoría en vista de década
- No crear módulos nuevos ni persistencia
