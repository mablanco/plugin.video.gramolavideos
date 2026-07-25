# Tasks: Auditoría y remediación incremental

**Input**: Design documents from `/specs/001-auditoria-codigo/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md

**Tests**: Incluidos — SC-003 / plan Fase 1 (caracterización) y actualización a comportamiento deseado en Fase 2 (quickstart B1–B3, R1–R2). pytest es tooling de desarrollo, no dependencia del addon.

**Harness Kodi (obligatorio en Fase 1/Foundational)**: Stubs/mocks de `xbmc`, `xbmcgui`, `xbmcplugin` y `xbmcaddon` bajo `tests/stubs/`, cargados vía `tests/conftest.py`, para que **toda** la remediación y el refactor se verifiquen con `python -m pytest -q` en terminal **sin abrir Kodi**. La reproducción real YouTube end-to-end sigue siendo el único smoke manual residual (SC-001).

**Organization**: Tareas agrupadas por user story (prioridad P1→P3). El orden respeta las 3 fases consecutivas del plan: safety net (US3) → bugs/compat (US1, US2, US5) → refactor/deuda (US4, US6) → polish.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Puede ejecutarse en paralelo (ficheros distintos, sin dependencia de tareas incompletas)
- **[Story]**: User story (US1…US6)
- Incluir rutas exactas en cada descripción

## Path Conventions

- Addon: `addon.py`, `addon.xml`, `changelog.txt`, `README.md`
- Catálogo: `resources/csv/YYYY.csv`
- Lógica: `resources/lib/catalog.py`, `resources/lib/kodi_plugin.py`, `resources/lib/kodi_notify.py`
- i18n: `resources/language/resource.language.es_es/`, `resources/language/resource.language.en_gb/`
- Tests: `tests/unit/`, `tests/fixtures/`, `tests/stubs/` (`xbmc*.py`), `tests/conftest.py`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Harness de desarrollo y estructura mínima para caracterización **sin abrir Kodi**

- [X] T001 Create directory layout `tests/unit/`, `tests/fixtures/`, `tests/stubs/`, and `resources/lib/` per plan.md project structure
- [X] T002 [P] Document or add a minimal `requirements-dev.txt` (or README section) with `pytest` for host Python 3; do not add pytest to `addon.xml` requires; state that `python -m pytest -q` is the primary refactor verification path
- [X] T003 [P] Add CSV fixtures under `tests/fixtures/` covering valid year file, short/incomplete row, extra fields, and empty directory case (quickstart C1–C3)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: (1) Extracción literal del parseo CSV y (2) **mocks obligatorios de la API Kodi** para importar y ejercitar el plugin en terminal — MUST completarse antes de cualquier user story

**⚠️ CRITICAL**: No empezar remediación de bugs ni refactor hasta el checkpoint de esta fase. Los stubs `xbmc*` **no** son opcionales: sin ellos no se puede verificar el cableado UI/plugin en CI/terminal.

- [X] T004 Add `resources/lib/__init__.py` so `resources/lib` is an importable package
- [X] T005 Extract *literal* CSV discovery/read/parse from `addon.py` into `resources/lib/catalog.py` with no semantic change (move only; research R-002)
- [X] T006 Wire `addon.py` to call `resources/lib/catalog.py` (sys.path / package bootstrap) so Kodi behavior is unchanged aside from import path
- [X] T007 Implement stub module `tests/stubs/xbmc.py` covering at least `translatePath`, `log`, and `Player` (with recordable `play` calls) sufficient to import and run plugin modes without real Kodi
- [X] T008 [P] Implement stub module `tests/stubs/xbmcgui.py` covering `ListItem` (modern and legacy kwargs as needed) plus a notification/dialog surface usable by recoverable-error helpers
- [X] T009 [P] Implement stub module `tests/stubs/xbmcplugin.py` that **records** calls to `addDirectoryItem`, `endOfDirectory`, `setResolvedUrl`, and `setContent` for assertions in unit tests
- [X] T010 [P] Implement stub module `tests/stubs/xbmcaddon.py` with `Addon().getAddonInfo('path')` (and related getters) returning a configurable fake addon root for path-resolution tests
- [X] T011 Add `tests/conftest.py` that prepends `tests/stubs/` to `sys.path` before imports, resets stub call history per test, and documents how to run the suite with `python -m pytest -q` without launching Kodi

**Checkpoint**: `import xbmc, xbmcgui, xbmcplugin, xbmcaddon` and `resources/lib/catalog` succeed on host Python; stub call recorders work; addon still opens in real Kodi with legacy behavior

---

## Phase 3: User Story 3 - Mantener y verificar el catálogo con seguridad (Priority: P1) 🎯 MVP safety net

**Goal**: Congelar comportamiento de catálogo **y** cableado `mode`/`foldername` con pytest + stubs (plan Fase 1 / SC-003 / research R-002)

**Independent Test**: `python -m pytest -q` verde (catálogo + wiring contra stubs) sin lanzar Kodi

### Tests for User Story 3

> Escribir tests que fallen o fijar el comportamiento *legacy* real antes de “mejorar” validación (Fase 2 del plan)

- [X] T012 [P] [US3] Add characterization tests for repo year inventory (1980–1999 without 1994) in `tests/unit/test_catalog_years.py` (quickstart C4)
- [X] T013 [P] [US3] Add characterization tests for current row-loading shape (including invalid Chiquilla id still present) in `tests/unit/test_catalog_load.py` (quickstart C1–C2)
- [X] T014 [P] [US3] Add characterization tests for missing year / empty / unreadable fixtures in `tests/unit/test_catalog_edge.py` (quickstart C3)
- [X] T015 [US3] Document and assert query contract `mode` / `foldername` per `contracts/plugin-navigation.md` in `tests/unit/test_plugin_query_contract.py` (quickstart C5)
- [X] T016 [US3] Add plugin-wiring characterization tests in `tests/unit/test_plugin_wiring.py` that invoke list-years / list-year / play entry paths against `tests/stubs/` and assert recorded `xbmcplugin` / `xbmc.Player` calls (so later refactors are verified in terminal only)

### Implementation for User Story 3

- [X] T017 [US3] Label “legacy freeze” vs future assertions in `tests/unit/` (comments or markers) so Fase 2 can swap validation/playback expectations safely
- [X] T018 [US3] Ensure `list_years` / `load_year` function signatures exist on `resources/lib/catalog.py` matching `contracts/catalog.md` even if implementation still mirrors legacy load (research R-008)

**Checkpoint**: Suite verde vía stubs; SC-003 baseline; cero cambios de producto observables en Kodi real (salvo path de import)

---

## Phase 4: User Story 1 - Usar la gramola en Kodi moderno sin roturas (Priority: P1)

**Goal**: Compatibilidad Python 3 / APIs Kodi modernas y reproducción integrada con el handle del plugin (plan Fase 2 / FR-003, FR-010)

**Independent Test**: (1) `pytest` verde actualizando `tests/unit/test_plugin_wiring.py` para `setResolvedUrl`, HTTPS thumbs y content type; (2) smoke manual opcional M1–M2 en Kodi solo para YouTube real (SC-001)

### Implementation for User Story 1

- [X] T019 [US1] Update `addon.xml` `xbmc.python` requirement to Matrix+ (`3.0.0` or agreed) while keeping addon id `plugin.video.gramolavideos` (FR-013)
- [X] T020 [US1] Replace `urllib` / `urlparse` with `urllib.parse` in `addon.py` (and any extracted kodi module) for Py3
- [X] T021 [US1] Switch catalog file I/O in `resources/lib/catalog.py` to text mode with UTF-8 encoding; remove Py2 `.decode` path hacks
- [X] T022 [US1] Modernize ListItem construction and set content type to music videos (not `movies`) in `addon.py` or `resources/lib/kodi_plugin.py` (research R-011); extend `tests/stubs/xbmcgui.py` / `xbmcplugin.py` if new APIs are used
- [X] T023 [US1] Resolve addon resource paths via `xbmcaddon.Addon().getAddonInfo('path')` (or encapsulated helper) instead of hardcoding `special://home/addons/...`; cover with stub path in `tests/unit/`
- [X] T024 [US1] Implement `mode=song` with `xbmcplugin.setResolvedUrl` (or facade) and YouTube URI `plugin://plugin.video.youtube/play/?video_id=...` in `addon.py` / `resources/lib/kodi_plugin.py` (research R-005)
- [X] T025 [US1] Use HTTPS YouTube thumbnail URLs and ensure thumbnail failure does not block list items in `resources/lib/kodi_plugin.py` (or `addon.py`) (research R-009)
- [X] T026 [US1] Update `tests/unit/test_plugin_wiring.py` (and stubs if needed) so terminal `pytest` asserts `setResolvedUrl`, HTTPS thumbnail URLs, and music-video content type — primary gate before any Kodi smoke
- [X] T027 [US1] Optionally smoke-check quickstart M1–M2 on reference Kodi for real YouTube playback (SC-001); do not block refactor completion on this if T026 is green

**Checkpoint**: Wiring and compat verified in terminal via stubs; optional Kodi smoke for real YouTube only

---

## Phase 5: User Story 2 - Fallos de catálogo visibles y no catastróficos (Priority: P1)

**Goal**: Validación de filas, `CatalogLoadResult` / errores recuperables y notificación amigable (FR-006, FR-007 / SC-002)

**Independent Test**: (1) pytest B1–B3 + stub assertion de notificación; (2) smoke manual M3 solo si se desea confirmar diálogo real en Kodi

### Tests for User Story 2

- [ ] T028 [P] [US2] Replace legacy-freeze assertions with desired validation in `tests/unit/test_catalog_load.py` and `tests/unit/test_catalog_edge.py` (omit bad `video_id`, `row_invalid`, unreadable year → errors; quickstart B1–B3)

### Implementation for User Story 2

- [ ] T029 [US2] Implement `Year`, `MusicVideo`, `CatalogError`, and `CatalogLoadResult` in `resources/lib/catalog.py` per `data-model.md` and `contracts/catalog.md`
- [ ] T030 [US2] Enforce row validation (exactly 2 fields, non-empty title, `video_id` `^[A-Za-z0-9_-]{11}$`); omit invalids into `errors` without aborting in `resources/lib/catalog.py`
- [ ] T031 [P] [US2] Fix or remove invalid entry `Seguridad Social - Chiquilla;d3mZmP_me4` in `resources/csv/1991.csv`
- [ ] T032 [US2] Add recoverable-error notification helper in `resources/lib/kodi_notify.py` (constitution VIII / FR-012b) using APIs mirrored by `tests/stubs/xbmcgui.py` (or `xbmc`)
- [ ] T033 [US2] Wire UI to show friendly notice when `CatalogLoadResult.errors` is non-empty and still list residual usable data in `resources/lib/kodi_plugin.py` / `addon.py`
- [ ] T034 [US2] Add `tests/unit/test_kodi_notify.py` (and extend wiring tests) asserting that recoverable catalog errors trigger the stub notification API and still produce directory items — verify in terminal without Kodi
- [ ] T035 [US2] Optionally smoke-check quickstart M3 on real Kodi for SC-002 UX; terminal suite (T028+T034) is the required gate

**Checkpoint**: Invalid rows/files handled; pytest+stubs prove notify + residual listing; known bad id fixed in data

---

## Phase 6: User Story 5 - Colaborar sobre la rama por defecto `main` (Priority: P2)

**Goal**: Default branch remota `main`; docs sin `master` canónico (FR-018–020 / SC-008)

**Independent Test**: `gh repo view mablanco/plugin.video.gramolavideos --json defaultBranchRef` → `main`; README/changelog sin enlaces canónicos a `master`

### Implementation for User Story 5

- [ ] T036 [US5] Migrate repository default branch from `master` to `main` on remote `mablanco/plugin.video.gramolavideos` per `contracts/repo-default-branch.md` (rename + set default)
- [ ] T037 [P] [US5] Update canonical branch references in `README.md` and `changelog.txt` (`commits/master` → `main` or history URL not tied to `master`)
- [ ] T038 [US5] Verify default branch and remaining `master` mentions with `gh repo view` and `rg` per quickstart governance; document legacy `master` if kept temporarily (FR-020)

**Checkpoint**: SC-008 satisfied; collaborators clone/PR against `main`

---

## Phase 7: User Story 4 - Apertura ágil al crecer el catálogo (Priority: P2)

**Goal**: Carga selectiva real + entry point fino (FR-008/009 / SC-004 / plan Fase 3)

**Independent Test**: `list_years` no materializa canciones; `load_year` solo lee ese CSV (quickstart R1–R2); wiring tests contra stubs siguen verdes tras mover UI a `kodi_plugin.py`

### Tests for User Story 4

- [ ] T039 [P] [US4] Add unit tests proving `list_years` does not materialize all songs and `load_year` only reads one file in `tests/unit/test_catalog_selective.py` (SC-004)

### Implementation for User Story 4

- [ ] T040 [US4] Implement selective `list_years` in `resources/lib/catalog.py` (stems only; no full song materialization)
- [ ] T041 [US4] Implement selective `load_year` in `resources/lib/catalog.py` reading only `{year_id}.csv`
- [ ] T042 [US4] Move listing/resolve UI from monolithic `addon.py` into `resources/lib/kodi_plugin.py`; leave `addon.py` as thin entry that delegates (FR-012b / constitution VII); keep `tests/unit/test_plugin_wiring.py` green via stubs after the move
- [ ] T043 [US4] Update `README.md` to close TODOs about loading the entire catalog on every use

**Checkpoint**: Layout target for data/UI split; SC-004 met; full suite green without Kodi

---

## Phase 8: User Story 6 - Coherencia editorial entre promesa y catálogo (Priority: P3)

**Goal**: Descripción alineada con cobertura real (o plan de contenido) y 0 ids YouTube inválidos conocidos (FR-017 / SC-006)

**Independent Test**: Revisar `addon.xml` summary/description vs years in `resources/csv/`; validate no known bad video ids remain

### Implementation for User Story 6

- [ ] T044 [US6] Align public description/summary in `addon.xml` with actual catalog coverage **or** document an explicit follow-up content plan for 60s–70s in `README.md` / spec notes (constitution III)
- [ ] T045 [US6] Scan `resources/csv/*.csv` and ensure zero known invalid YouTube ids remain (SC-006 / R5)
- [ ] T046 [P] [US6] Record AuditFinding status updates (fixed/deferred/accepted) for P1–P3 inventory items in `specs/001-auditoria-codigo/` checklist or plan notes for SC-005

**Checkpoint**: No grave editorial contradiction; SC-006; P1 findings closed or explicitly decided

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Typing, i18n-ready, versionado, trazabilidad FR, validación final

- [ ] T047 [P] Add gradual type hints in `resources/lib/catalog.py`, `resources/lib/kodi_plugin.py`, and `resources/lib/kodi_notify.py` (research R-012; no strict mypy CI gate unless requested)
- [ ] T048 [P] Create i18n skeleton `resources/language/resource.language.es_es/` and `resources/language/resource.language.en_gb/` (or `en_us` if chosen) with strings.xml placeholders (FR-015)
- [ ] T049 Centralize UI strings touched during remediación into the language files / a single gettext-style helper used by `resources/lib/kodi_plugin.py` and `resources/lib/kodi_notify.py`
- [ ] T050 Remove residual smells (redundant sorts, rigid path leftovers) in `resources/lib/` and `addon.py` justified under constitution IV
- [ ] T051 Bump version in `addon.xml` and write useful entries in `changelog.txt` for user-visible behavior changes (FR-011)
- [ ] T052 [P] Produce FR-001–FR-020 → evidence map (tasks/commits/exclusions) for SC-007 in `specs/001-auditoria-codigo/` (checklist or short traceability note)
- [ ] T053 [P] Confirm out-of-scope: no `script.module.routing`, no scaffold merge, id remains `plugin.video.gramolavideos` (SC-009 / FR-012a / FR-013) in `addon.xml` and deps
- [ ] T054 Run full `specs/001-auditoria-codigo/quickstart.md` validation prioritizing `python -m pytest -q` (stubs); add manual Kodi only for YouTube smoke + `gh` default-branch check

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Sin dependencias — empezar ya
- **Foundational (Phase 2)**: Depende de Setup — **bloquea** todas las user stories; incluye mocks `xbmc*` **obligatorios** (T007–T011)
- **US3 (Phase 3)**: Depende de Foundational — **debe** cerrarse antes de cambiar semántica (plan R-001); incluye wiring tests contra stubs (T016)
- **US1 (Phase 4)**: Depende de US3 (safety net verde); gate principal = pytest/stubs (T026)
- **US2 (Phase 5)**: Depende de US3; idealmente tras o en paralelo cuidadoso con US1; gate = pytest/stubs (T028+T034)
- **US5 (Phase 6)**: Independiente del código del addon tras Foundational; puede ir en paralelo con US1/US2 si no choca con docs
- **US4 (Phase 7)**: Depende de US1+US2; wiring stubs deben seguir verdes tras thin entry
- **US6 (Phase 8)**: Depende de US2; puede solaparse parcialmente con US4
- **Polish (Phase 9)**: Tras las stories deseadas; i18n tras tocar cadenas (US1/US2)

### User Story Dependencies

- **US3 (P1)**: Tras Foundational — sin dependencia de otras stories — **MVP técnico / safety net + harness stubs**
- **US1 (P1)**: Tras US3 — MVP de producto (verificado en terminal; smoke Kodi opcional)
- **US2 (P1)**: Tras US3 — robustez; comparte `catalog.py` / stubs con US1
- **US5 (P2)**: Tras Foundational — independiente del runtime del addon
- **US4 (P2)**: Tras US1+US2 — carga selectiva + thin entry
- **US6 (P3)**: Tras US2 (datos válidos) — alineación editorial

### Within Each User Story

- Tests (si hay) antes o al cambiar contrato; etiquetar freeze vs deseado
- Modelos/resultados de catálogo antes de UI
- UI/notificación después de `CatalogLoadResult`
- Extender stubs cuando aparezcan APIs Kodi nuevas usadas por el código
- Story completa y verificable con `pytest` antes de subir de fase del plan

### Parallel Opportunities

- T002 ∥ T003 en Setup
- T007–T010 stubs en paralelo tras T001 (antes o junto a T005–T006)
- T012 ∥ T013 ∥ T014 en US3
- T028 ∥ T031 en US2 (tests vs fix CSV) tras API de validación
- T037 ∥ trabajo de código US1/US2 (docs vs código)
- T039 ∥ preparación de layout US4 tras API estable
- T046 ∥ T044/T045 en US6
- T047 ∥ T048 ∥ T052 ∥ T053 en Polish
- US5 puede ejecutarse en paralelo con US1/US2 (staff distinto)

---

## Parallel Example: Foundational stubs (Phase 2)

```bash
# Tras T001, crear mocks Kodi en paralelo:
Task: "Implement stub module tests/stubs/xbmc.py"
Task: "Implement stub module tests/stubs/xbmcgui.py"
Task: "Implement stub module tests/stubs/xbmcplugin.py"
Task: "Implement stub module tests/stubs/xbmcaddon.py"
# Luego T011 conftest.py que los inyecta en sys.path
```

## Parallel Example: User Story 3

```bash
# Tras Foundational (stubs + conftest), lanzar tests de caracterización en paralelo:
Task: "Characterization tests for repo year inventory in tests/unit/test_catalog_years.py"
Task: "Characterization tests for current row-loading shape in tests/unit/test_catalog_load.py"
Task: "Characterization tests for missing year / empty fixtures in tests/unit/test_catalog_edge.py"
# Luego wiring contra stubs:
Task: "Plugin-wiring characterization tests in tests/unit/test_plugin_wiring.py"
```

## Parallel Example: User Story 2

```bash
# Tras implementar validación en catalog.py:
Task: "Update unit tests to desired validation in tests/unit/test_catalog_load.py"
Task: "Fix or remove Chiquilla invalid id in resources/csv/1991.csv"
```

## Parallel Example: Polish

```bash
Task: "Add gradual type hints in resources/lib/*.py"
Task: "Create i18n skeleton under resources/language/"
Task: "Produce FR-001–FR-020 evidence map for SC-007"
Task: "Confirm no routing/scaffold merge (SC-009) in addon.xml"
```

---

## Implementation Strategy

### MVP First (Safety net + terminal harness + usable modern plugin)

1. Completar Phase 1: Setup
2. Completar Phase 2: Foundational (**extract + mocks `xbmc*` + `conftest.py`**)
3. Completar Phase 3: **US3** — `pytest` verde / SC-003 (catálogo + wiring)
4. Completar Phase 4: **US1** — compat/play verificados con stubs (T026); smoke Kodi opcional
5. **STOP and VALIDATE** con `python -m pytest -q`
6. Seguir con US2 (robustez vía stubs), luego US5 / US4 / US6 y polish

### Suggested MVP scope

- **MVP técnico**: Setup + Foundational (incl. stubs) + **US3**
- **MVP de producto**: + **US1** (gate terminal T026)
- **Cierre P1 inventario**: + **US2** (gate terminal T034)

### Incremental Delivery

1. Setup + Foundational → catálogo importable + API Kodi mockeada en terminal
2. US3 → caracterización congelada (datos + wiring)
3. US1 → compat/play assertados en pytest; smoke YouTube real opcional
4. US2 → fallos recuperables assertados en stubs
5. US5 → gobernanza `main` (puede adelantarse en paralelo)
6. US4 → rendimiento/layout con suite stubs verde
7. US6 → coherencia editorial
8. Polish → i18n-ready, versión, SC-007/SC-009

### Parallel Team Strategy

1. Equipo cierra Setup + Foundational (stubs) + US3 juntos
2. Después:
   - Dev A: US1 (compat / play + actualizar stubs/tests)
   - Dev B: US2 (validación / notify + `test_kodi_notify.py`)
   - Dev C: US5 (rama `main` + docs)
3. Luego US4 → US6 → Polish

---

## Notes

- Respetar fases consecutivas del plan: no “arreglar” validación antes de tener freeze verde (US3)
- **Mocks `xbmc*` son obligatorios** desde Foundational; ampliar stubs cuando el código use APIs nuevas
- Verificar refactor con `python -m pytest -q` — no hace falta abrir Kodi salvo smoke YouTube real
- No fusionar `plugin.video.gramola`; no añadir `script.module.routing`
- Commits lógicos tras cada checkpoint de fase / story
- Cada tarea incluye ruta de fichero para ejecución directa por un agente/LLM
