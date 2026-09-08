# Tasks: Búsqueda en catálogo

**Input**: Design documents from `/specs/007-busqueda-catalogo/`

**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/, quickstart.md

**Tests**: El plan exige pytest de `catalog.search` y modos/URLs; se incluyen tests unitarios. Smoke Kodi en polish.

**Organization**: Datos de búsqueda primero; luego UI Buscar/resultados/play; orden-límite; independencia de favoritos; polish.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- Artefactos: `specs/007-busqueda-catalogo/`
- Runtime: `resources/lib/catalog.py`, `resources/lib/kodi_plugin.py`, `resources/lib/kodi_i18n.py`, `resources/lib/kodi_notify.py`
- i18n: `resources/language/resource.language.es_es/strings.xml`, `resources/language/resource.language.en_gb/strings.xml`
- Tests: `tests/unit/test_catalog_search.py`, `tests/unit/test_plugin_search.py`, `tests/unit/test_plugin_query_contract.py`
- Docs/release: `README.md`, `addon.xml`, `changelog.txt`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Confirmar artefactos y registro de validación

- [X] T001 Verificar que existen `specs/007-busqueda-catalogo/plan.md`, `spec.md`, `research.md`, `data-model.md`, `quickstart.md` y `contracts/` según `plan.md`
- [X] T002 [P] Crear `specs/007-busqueda-catalogo/validation-log.md` con tabla del `quickstart.md` (pytest + smoke) y columnas Resultado / Notas / Fecha
- [X] T003 [P] Anotar en `specs/007-busqueda-catalogo/validation-log.md` dependencia recomendada de `004` y baseline (raíz sin Buscar)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: API pura `catalog.search` + i18n de Buscar/vacío, sin teclado UI aún

**⚠️ CRITICAL**: No cablear modos `search`/`search_results` hasta completar esta fase

- [X] T004 Implementar `search(csv_dir, query, limit=100)` en `resources/lib/catalog.py` según `contracts/catalog-search.md` (strip/casefold, subcadena en título, acumular errores, sin `xbmc*`)
- [X] T005 En `resources/lib/catalog.py`, aplicar orden `(title.casefold(), year_id, video_id)` y tope 100 **después** de ordenar; query vacía → videos=[] sin abrir CSV
- [X] T006 [P] Crear `tests/unit/test_catalog_search.py` con fixtures temporales CSV: match, casefold, vacío, sin coincidencias, límite 100, CSV corrupto parcial
- [X] T007 [P] Añadir strings Buscar / vacío / (opcional límite) en `resources/language/resource.language.es_es/strings.xml`
- [X] T008 [P] Añadir las mismas claves en `resources/language/resource.language.en_gb/strings.xml`
- [X] T009 Registrar IDs en `resources/lib/kodi_i18n.py` sin literales dispersos nuevos

**Checkpoint**: Búsqueda de datos testeable sin Kodi

---

## Phase 3: User Story 1 - Buscar por texto en el catálogo local (Priority: P1) 🎯 MVP

**Goal**: Ítem Buscar + teclado + resultados locales (SC-001/SC-002/SC-003 parcial)

**Independent Test**: Abrir Buscar, query conocida → aparece; query sin match → vacío claro

### Implementation for User Story 1

- [X] T010 [US1] En raíz sin `mode` de `resources/lib/kodi_plugin.py`, añadir carpeta localizada Buscar (`mode=search`) junto a décadas (y Favoritos solo si ya existe), sin sustituir browse
- [X] T011 [US1] Implementar modo `search` en `resources/lib/kodi_plugin.py` con `xbmcgui.Dialog().input`; cancel/vacío finaliza sin listar catálogo
- [X] T012 [US1] Implementar modo `search_results` en `resources/lib/kodi_plugin.py` leyendo `q`, llamando `catalog.search` y listando hasta 100 canciones o vacío localizado
- [X] T013 [US1] Notificar errores recuperables de carga vía `resources/lib/kodi_notify.py` sin abortar el directorio
- [X] T014 [P] [US1] Actualizar `tests/unit/test_plugin_query_contract.py` para modos `search` / `search_results` y param `q`
- [X] T015 [P] [US1] Crear/ampliar `tests/unit/test_plugin_search.py` para raíz con Buscar, cancelación y vacío sin coincidencias

**Checkpoint**: Flujo Buscar → resultados/vacío en tests

---

## Phase 4: User Story 2 - Usar un resultado hasta oír la canción (Priority: P1)

**Goal**: Resultados reproducibles con el mismo resolver YouTube (SC-004)

**Independent Test**: Desde un resultado, play = misma experiencia que desde el año

### Implementation for User Story 2

- [X] T016 [US2] En `search_results` de `resources/lib/kodi_plugin.py`, crear ítems con `song_listitem`, `IsPlayable=true` y URL `mode=song&foldername=<video_id>`
- [X] T017 [US2] Añadir año como contexto en etiqueta o info del `ListItem` en `resources/lib/kodi_plugin.py` sin alterar el título editorial del CSV
- [X] T018 [US2] Confirmar que fallos de play reutilizan `resolve_youtube_playback` / notificaciones existentes en `resources/lib/kodi_plugin.py`
- [X] T019 [P] [US2] Extender `tests/unit/test_plugin_search.py` assert URL `mode=song` en resultados

**Checkpoint**: Play desde búsqueda cableado

---

## Phase 5: User Story 3 - Resultados manejables (orden y límite) (Priority: P1)

**Goal**: Orden predecible + límite 100 comprensible (FR-006, SC-005 parcial)

**Independent Test**: Query genérica → orden alfa estable; no más de 100 filas

### Implementation for User Story 3

- [X] T020 [US3] Verificar/ajustar en `resources/lib/catalog.py` que el límite efectivo no supera 100 aunque la UI pase otro valor
- [X] T021 [US3] Asegurar en `mode=search_results` de `resources/lib/kodi_plugin.py` que se usa el límite por defecto del contrato
- [X] T022 [P] [US3] Ampliar `tests/unit/test_catalog_search.py` con >100 matches sintéticos y orden determinista
- [X] T023 [P] [US3] Documentar en `specs/007-busqueda-catalogo/validation-log.md` el tope 100 y el criterio de orden

**Checkpoint**: Orden/límite verificados por tests

---

## Phase 6: User Story 4 - Independencia de favoritos y simplicidad (Priority: P2)

**Goal**: Buscar sin depender de Favoritos; exclusiones claras (SC-005)

**Independent Test**: Suite/search funciona sin módulo favorites; docs sin acoplar

### Implementation for User Story 4

- [X] T024 [US4] Revisar `resources/lib/kodi_plugin.py` y `resources/lib/catalog.py` para que search no importe ni exija `favorites`
- [X] T025 [P] [US4] Actualizar `README.md` describiendo Buscar como acceso adicional (FR-011)
- [X] T026 [P] [US4] Registrar en `specs/007-busqueda-catalogo/validation-log.md` exclusiones (remoto, filtros, fuzzy, favoritos como requisito)

**Checkpoint**: Feature autónoma documentada

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Release y cierre quickstart

- [X] T027 Bump de versión en `addon.xml` y entrada en `changelog.txt` al publicar búsqueda
- [X] T028 [P] Confirmar YouTube dependency intacta en `addon.xml` (constitution II)
- [X] T029 [P] Confirmar CSV no modificados por search (constitution I) en revisión de diff
- [X] T030 Ejecutar `pytest -q tests/unit/test_catalog_search.py tests/unit/test_plugin_search.py tests/unit/test_plugin_query_contract.py` y anotar en `specs/007-busqueda-catalogo/validation-log.md`
- [X] T031 Completar smoke Kodi del `quickstart.md` en `specs/007-busqueda-catalogo/validation-log.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup → Foundational** bloquea US
- **US1** habilita UI; **US2** sobre resultados; **US3** endurece orden/límite (puede solaparse con T004–T005)
- **US4** tras US1
- **Polish** al final

### User Story Dependencies

- **US1**: tras Phase 2
- **US2**: tras US1 (`search_results`)
- **US3**: lógica ya en Phase 2; tareas UI/docs tras US1
- **US4**: tras US1

### Parallel Opportunities

- T002/T003; T006–T008; T014/T015; T022/T023; T025/T026; T028/T029

---

## Parallel Example: User Story 1

```bash
Task: "Actualizar tests/unit/test_plugin_query_contract.py para search/search_results"
Task: "Crear tests/unit/test_plugin_search.py para raíz Buscar y vacío"
```

---

## Implementation Strategy

### MVP First

1. Phase 1–2 → `catalog.search` + tests
2. US1 Buscar + results/vacío
3. US2 play → demo
4. US3 asserts límite → US4 docs → polish

### Incremental Delivery

1. Datos search
2. UI teclado/resultados
3. Play
4. Límite/orden evidenciado
5. README/versión/smoke

---

## Notes

- Implementación ideal tras catálogo amplio (`004`); no bloquea estas tareas
- No añadir favoritos ni índices persistentes en este feature
