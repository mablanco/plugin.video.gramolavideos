# Tasks: Mejorar la navegación del catálogo de vídeos

**Input**: Design documents from `/specs/003-navegacion-videos/`

**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/, decision.md, quickstart.md

**Tests**: El plan exige pytest de agrupación/modes/wiring. Se incluyen tareas de tests unitarios (la suite actual romperá si la raíz deja de listar años planos). Smoke Kodi en polish.

**Organization**: US1 = cerrar/validar veredicto (artefactos); US2–US4 = implementación runtime. Enmienda constitution IV en foundational antes de merge de UI.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- Artefactos: `specs/003-navegacion-videos/`
- Runtime: `resources/lib/catalog.py`, `resources/lib/kodi_plugin.py`
- i18n: `resources/language/resource.language.es_es/strings.xml`, `resources/language/resource.language.en_gb/strings.xml`
- Tests: `tests/unit/test_catalog_*.py`, `tests/unit/test_plugin_*.py`
- Gobernanza: `.specify/memory/constitution.md`, `README.md`, `addon.xml`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Confirmar artefactos de plan y registro de validación

- [X] T001 Verificar que existen `specs/003-navegacion-videos/plan.md`, `spec.md`, `research.md`, `decision.md`, `data-model.md`, `quickstart.md` y `contracts/` según `plan.md`
- [X] T002 [P] Crear `specs/003-navegacion-videos/validation-log.md` con tabla de pasos del `quickstart.md` (documental + pytest + smoke Kodi) y columnas Resultado / Notas / Fecha
- [X] T003 [P] Anotar en `specs/003-navegacion-videos/validation-log.md` el baseline actual (raíz = años planos; contrato `specs/001-auditoria-codigo/contracts/plugin-navigation.md`)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Congelar veredicto, enmienda IV y API de décadas en capa datos (sin UI aún)

**⚠️ CRITICAL**: No user story de implementación UI hasta completar esta fase (US1 documental puede solaparse con T004–T007)

- [X] T004 Confirmar veredicto opción B en `specs/003-navegacion-videos/decision.md` alineado con `research.md` R-003 y `contracts/decision-criteria.md` (C1–C5)
- [X] T005 Aplicar enmienda de flujo en `.specify/memory/constitution.md` según `specs/003-navegacion-videos/contracts/constitution-amendment-draft-iv.md` (bump 1.2.1 → 1.3.0, Sync Impact Report)
- [X] T006 [P] Implementar helpers puros `decade_id_for_year`, `list_decades` y `years_in_decade` en `resources/lib/catalog.py` según `specs/003-navegacion-videos/data-model.md` (sin `xbmc*`)
- [X] T007 [P] Añadir tests de agrupación de décadas en `tests/unit/test_catalog_decades.py` cubriendo décadas incompletas y proyección 1960–1999 sin inventar años vacíos
- [X] T008 Actualizar o añadir nota de supersesión en `specs/003-navegacion-videos/contracts/plugin-navigation.md` enlazando el contrato legacy 001 como histórico tras el cambio

**Checkpoint**: Constitution IV actualizada; API de décadas testeable sin Kodi

---

## Phase 3: User Story 1 - Decidir el modelo de navegación (Priority: P1) 🎯 MVP documental

**Goal**: Dejar el veredicto auditable y el validation-log de Parte documental cerrado (SC-001)

**Independent Test**: Leer solo `decision.md` + `research.md` y comprobar ≥3 opciones, ganador B, edge cases y gobernanza

### Implementation for User Story 1

- [X] T009 [US1] Completar matriz C1–C5 × opciones A–C en `specs/003-navegacion-videos/decision.md` (o confirmar que `research.md` R-002/R-003 ya la cubre con enlace explícito)
- [X] T010 [P] [US1] Documentar fuera de alcance (contenido 60/70, búsqueda/favoritos) en `specs/003-navegacion-videos/decision.md`
- [X] T011 [P] [US1] Registrar en `specs/003-navegacion-videos/validation-log.md` la Parte documental del `quickstart.md` (SC-001) como PASS tras auto-revisión

**Checkpoint**: MVP documental — se puede demo el “qué vamos a construir” sin código UI

---

## Phase 4: User Story 2 - Recorrer el catálogo con la navegación elegida (Priority: P1)

**Goal**: Raíz = décadas; entrar a año y reproducir (SC-002–SC-005)

**Independent Test**: pytest wiring + abrir addon: décadas → año → canción → play

### Implementation for User Story 2

- [X] T012 [US2] Cambiar la raíz sin `mode` en `resources/lib/kodi_plugin.py` para listar décadas vía `catalog.list_decades` y URLs `mode=decade` según `contracts/plugin-navigation.md`
- [X] T013 [US2] Implementar rama `mode=decade` en `resources/lib/kodi_plugin.py` listando años con `years_in_decade` y URLs `mode=year` existentes
- [X] T014 [P] [US2] Preservar ramas `mode=year` y `mode=song` en `resources/lib/kodi_plugin.py` sin cambiar URI YouTube ni formato CSV
- [X] T015 [US2] Actualizar contrato de query en `tests/unit/test_plugin_query_contract.py` para incluir `mode=decade`
- [X] T016 [US2] Actualizar `tests/unit/test_plugin_wiring.py` para esperar décadas en raíz (no 19 años planos) y un drill-down década→año
- [X] T017 [US2] Ejecutar `python -m pytest -q tests/unit/test_catalog_decades.py tests/unit/test_plugin_query_contract.py tests/unit/test_plugin_wiring.py` y anotar resultado en `specs/003-navegacion-videos/validation-log.md`

**Checkpoint**: Navegación usable en tests; listo para smoke Kodi

---

## Phase 5: User Story 3 - Volver atrás y orientarse (Priority: P2)

**Goal**: Etiquetas claras ES/EN y pila atrás predecible (SC-006)

**Independent Test**: Entrar 2–3 niveles, atrás hasta raíz; leer etiquetas sin ayuda

### Implementation for User Story 3

- [X] T018 [P] [US3] Añadir strings de décadas (`Años 60`… / equivalentes EN) en `resources/language/resource.language.es_es/strings.xml`
- [X] T019 [P] [US3] Añadir las mismas claves en `resources/language/resource.language.en_gb/strings.xml`
- [X] T020 [US3] Usar `xbmcaddon`/helper de localize existente en `resources/lib/kodi_plugin.py` para etiquetas de carpeta década (sin literales nuevos dispersos)
- [X] T021 [US3] Verificar en comentario de prueba o assert de wiring que `folder_listitem` de década/año mantiene `isFolder=True` para pila atrás nativa de Kodi en `tests/unit/test_plugin_wiring.py`
- [X] T022 [US3] Documentar recorrido atrás en `specs/003-navegacion-videos/validation-log.md` (smoke o checklist manual)

**Checkpoint**: Orientación y atrás validados

---

## Phase 6: User Story 4 - Preservar catálogo y reproducción (Priority: P2)

**Goal**: CSV y YouTube intactos; 100 % años alcanzables (SC-004, FR-006/007)

**Independent Test**: Diff de `resources/csv/` vacío de cambios de formato; play de una canción conocida

### Implementation for User Story 4

- [X] T023 [P] [US4] Confirmar que ningún task ha modificado filas en `resources/csv/` por esta feature; anotar en `specs/003-navegacion-videos/validation-log.md`
- [X] T024 [P] [US4] Añadir test de cobertura SC-004 en `tests/unit/test_catalog_decades.py`: todo stem de `list_years` pertenece a exactamente una década listada
- [X] T025 [US4] Confirmar URI `plugin://plugin.video.youtube/play/?video_id=` intacta en `resources/lib/kodi_plugin.py` y dependencia en `addon.xml`

**Checkpoint**: Invariantes de producto preservados

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Docs de producto, versión y smoke final

- [X] T026 [P] Actualizar flujo de usuario en `README.md` (décadas → años → canciones)
- [X] T027 [P] Actualizar descripción/summary en `addon.xml` si menciona solo listado de años planos
- [X] T028 Bump de versión en `addon.xml` y entrada en `changelog.txt` por cambio de navegación
- [X] T029 [P] Actualizar referencia legacy en `specs/001-auditoria-codigo/contracts/plugin-navigation.md` con nota “superseded by 003” (sin borrar historia)
- [X] T030 Ejecutar smoke Kodi del `specs/003-navegacion-videos/quickstart.md` y completar `validation-log.md` (SC-003, SC-005)
- [X] T031 [P] Confirmar que `.gitignore` sigue bloqueando secretos/artefactos IA y que el diff de esta feature no los introduce (constitution IX)
- [X] T032 Ejecutar `python -m pytest -q` completo y anotar PASS en `specs/003-navegacion-videos/validation-log.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: inmediato
- **Foundational (Phase 2)**: tras Setup — bloquea UI (Phase 4+)
- **US1 (Phase 3)**: puede ir en paralelo a T006–T007 tras T004
- **US2 (Phase 4)**: requiere T006–T007 (y preferible T005)
- **US3 (Phase 5)**: tras T012–T013 (necesita carpetas década)
- **US4 (Phase 6)**: tras US2 estable
- **Polish**: tras US2–US4 deseadas

### User Story Dependencies

- **US1**: Independiente (documental)
- **US2**: Depende de foundational (helpers décadas)
- **US3**: Depende de US2 (UI décadas)
- **US4**: Depende de US2 (verificar no regresión)

### Parallel Opportunities

- T002/T003; T006/T007; T010/T011; T018/T019; T023/T024; T026/T027/T029/T031

---

## Parallel Example: User Story 2

```bash
# Tras T012–T013, en paralelo:
Task: "Preservar year/song en resources/lib/kodi_plugin.py"
Task: "Actualizar tests/unit/test_plugin_query_contract.py"
# Luego secuencial wiring + pytest
```

---

## Implementation Strategy

### MVP First

1. Phase 1–2 + US1 → veredicto y API datos
2. US2 → navegación funcional (MVP de producto)
3. STOP: pytest + smoke corto
4. US3 → etiquetas i18n
5. US4 + Polish → release

### Incremental Delivery

- Merge posible tras US2+tests si constitution IV ya está enmendada
- US3/US4 pueden ir en el mismo PR o follow-up corto

---

## Notes

- No añadir `script.module.routing`
- No colapsar el nivel década aunque solo exista una
- Contenido 60/70 es feature 004 (fuera de estas tareas salvo CSV de prueba opcional en smoke)
