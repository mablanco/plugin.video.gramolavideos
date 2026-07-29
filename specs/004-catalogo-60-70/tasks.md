# Tasks: Base de catálogo 60s/70s

**Input**: Design documents from `/specs/004-catalogo-60-70/`

**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/, quickstart.md

**Tests**: Validación mecánica vía pytest de catálogo existente + script de conteos del quickstart. Smoke de reproducción manual/oEmbed (FR-010). No suite TDD nueva salvo actualizar expectativas de N años.

**Organization**: Feature de **contenido + proceso offline**. US2 documenta/ejecuta semilla; US3 revisa; US1 entrega CSV navegables; US4 docs de crecimiento. Sin cambios de navegación UI (003).

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- Artefactos: `specs/004-catalogo-60-70/`
- Catálogo: `resources/csv/YYYY.csv`
- Docs producto: `README.md`, `addon.xml`, `changelog.txt`
- Validación: `resources/lib/catalog.py`, `tests/unit/test_catalog_*.py`
- Runbook: `specs/004-catalogo-60-70/contracts/seed-process.md`, `docs/seed-60-70.md` (crear si se elige doc dedicado)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Preparar registro de semilla y workspace de candidatos

- [X] T001 Verificar que existen `specs/004-catalogo-60-70/plan.md`, `spec.md`, `research.md`, `data-model.md`, `quickstart.md` y `contracts/` según `plan.md`
- [X] T002 [P] Crear `specs/004-catalogo-60-70/validation-log.md` con secciones Pipeline / Conteos / Smoke 5+5 / Docs y columnas Resultado / Notas / Fecha
- [X] T003 [P] Crear directorio de trabajo de candidatos `specs/004-catalogo-60-70/seed-work/` (gitkeep) y plantilla `specs/004-catalogo-60-70/seed-work/candidates.md` con columnas year_id / title / video_id / editorial_ok / format_ok / notes
- [X] T004 Confirmar baseline: cero CSV 1960–1979 en `resources/csv/` y anotar conteo actual de años 1980–1999 en `specs/004-catalogo-60-70/validation-log.md`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Congelar runbook, criterios editoriales y herramientas de validación en host

**⚠️ CRITICAL**: No publicar CSV finales hasta completar checklist y validadores

- [X] T005 Redactar runbook operativo enlazando `specs/004-catalogo-60-70/contracts/seed-process.md` en `docs/seed-60-70.md` (pasos 1–6, invariante “no runtime Kodi”)
- [X] T006 [P] Copiar/adaptar checklist imprimible desde `specs/004-catalogo-60-70/contracts/editorial-review.md` hacia `specs/004-catalogo-60-70/seed-work/editorial-checklist.md` con casillas E1–E6
- [X] T007 [P] Añadir helper de conteo documentado (snippet del `quickstart.md`) en `docs/seed-60-70.md` o script host `scripts/count_seed_60_70.py` que imprima years/rows en 1960–1979 **sin** importarse desde `addon.py`
- [X] T008 Documentar en `docs/seed-60-70.md` el uso de validación existente (`catalog.load_year` / pytest) y sonda oEmbed si se usa `resources/lib/youtube_probe.py` solo en host

**Checkpoint**: Proceso reproducible antes de generar masa de candidatos

---

## Phase 3: User Story 2 - Generar la base de forma asistida (Priority: P1)

**Goal**: Obtener candidatos multi-año 60s y 70s en formato catálogo (FR-003)

**Independent Test**: `seed-work/candidates.md` tiene filas para ambas décadas listas para revisión

### Implementation for User Story 2

- [X] T009 [US2] Generar lista asistida de candidatos (≥50 brutos recomendados) de pop/rock/canción española 60s/70s en `specs/004-catalogo-60-70/seed-work/candidates.md` con `year_id` + `title`
- [X] T010 [US2] Resolver `video_id` públicos para el máximo posible de candidatos en `specs/004-catalogo-60-70/seed-work/candidates.md` (desechar sin id usable)
- [X] T011 [US2] Marcar `format_ok` ejecutando validación mecánica (patrón título + `VIDEO_ID_RE`) y registrar fallos en `specs/004-catalogo-60-70/seed-work/candidates.md`
- [X] T012 [US2] Anotar en `specs/004-catalogo-60-70/validation-log.md` que el pipeline de generación se ejecutó offline (no vía `kodi_plugin.run`)

**Checkpoint**: Candidatos generados y formateables; aún no en `resources/csv/`

---

## Phase 4: User Story 3 - Revisar y quedarse solo con publicables (Priority: P1)

**Goal**: Filtrar por checklist editorial y preparar conjunto publicable (FR-004)

**Independent Test**: Ningún candidato `editorial_ok=false` o `format_ok=false` entra al conjunto “publish”

### Implementation for User Story 3

- [X] T013 [US3] Aplicar E1–E6 de `specs/004-catalogo-60-70/seed-work/editorial-checklist.md` fila a fila sobre `candidates.md` y marcar `editorial_ok`
- [X] T014 [US3] Eliminar duplicados de `video_id` intra-año en el conjunto aceptado (anotar en `candidates.md` notes)
- [X] T015 [US3] Congelar lista “publish” (subset aceptado) en `specs/004-catalogo-60-70/seed-work/publish-list.md` con conteo previo years/rows
- [X] T016 [US3] Verificar umbrales previos FR-005/006 sobre `publish-list.md` (≥40 filas, ≥8 años, ambas décadas) o volver a T009–T010 si faltan

**Checkpoint**: Lista publish lista para escribir CSV

---

## Phase 5: User Story 1 - Disponer de una base navegable 60s/70s (Priority: P1) 🎯 MVP producto

**Goal**: CSV en `resources/csv/` navegables y reproducibles (SC-001, SC-002)

**Independent Test**: `list_years` incluye años &lt;1980; abrir un año 60 y uno 70 muestra canciones

### Implementation for User Story 1

- [X] T017 [US1] Escribir ficheros `resources/csv/YYYY.csv` solo para años con ≥1 fila de `publish-list.md` (formato `Artista - Canción;video_id`)
- [X] T018 [P] [US1] Confirmar que no se han reescrito masivamente CSV 1980–1999 en el diff (FR-007); anotar en `validation-log.md`
- [X] T019 [US1] Actualizar expectativas de inventario en `tests/unit/test_catalog_years.py` (y wiring si cuenta años en raíz) al nuevo N de stems
- [X] T020 [US1] Ejecutar `python -m pytest -q tests/unit/test_catalog_load.py tests/unit/test_catalog_video_ids.py tests/unit/test_catalog_years.py` y registrar PASS en `specs/004-catalogo-60-70/validation-log.md`
- [X] T021 [US1] Ejecutar conteo del `quickstart.md` / `scripts/count_seed_60_70.py` y registrar years/rows ≥ umbrales en `validation-log.md`

**Checkpoint**: Catálogo instalable ya muestra 60/70

---

## Phase 6: User Story 3 (continuación) - Muestreo smoke (Priority: P1)

**Goal**: SC-004 / FR-010 — muestreo 5+5 reproducciones

**Independent Test**: Log con 10 ids y ≥80 % OK o deuda listada

### Implementation

- [X] T022 [US3] Seleccionar 5 `video_id` de CSV 1960–1969 y 5 de 1970–1979 y listarlos en `specs/004-catalogo-60-70/validation-log.md`
- [X] T023 [US3] Ejecutar smoke Kodi u oEmbed host sobre esos 10 ids; anotar pass/fail en `validation-log.md`
- [X] T024 [US3] Sustituir ids fallidos en `resources/csv/YYYY.csv` correspondientes o documentar deuda explícita en `specs/004-catalogo-60-70/validation-log.md` y `README.md` si aplica

**Checkpoint**: Semilla “cerrada” a nivel calidad de reproducción

---

## Phase 7: User Story 4 - Dejar el catálogo listo para crecer (Priority: P2)

**Goal**: Docs de contribución + alcance de producto actualizado (SC-005, SC-006)

**Independent Test**: Colaborador añade una fila siguiendo solo README/runbook

### Implementation for User Story 4

- [X] T025 [P] [US4] Actualizar introducción y TODO en `README.md` para reflejar cobertura 60/70 y enlace a `docs/seed-60-70.md`
- [X] T026 [P] [US4] Actualizar `addon.xml` (summary/description es/en) para no afirmar catálogo solo 80/90
- [X] T027 [US4] Bump de versión en `addon.xml` y entrada en `changelog.txt` por ampliación de catálogo
- [X] T028 [US4] Documentar flujo manual clásico + regeneración de semilla en `README.md` FAQ o sección desarrollo citando `contracts/seed-process.md`
- [X] T029 [US4] Probar en seco el flujo “añadir una fila” editando un CSV 60/70 de prueba o documentando el procedimiento cronometrado (&lt;5 min) en `validation-log.md` (SC-005)

**Checkpoint**: Base publicada y crecible a mano

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Cierre de calidad y no regresiones

- [X] T030 Ejecutar `python -m pytest -q` completo y anotar en `specs/004-catalogo-60-70/validation-log.md`
- [X] T031 [P] Revisar que no hay CSV vacíos 1960–1979 en `resources/csv/` (FR-012)
- [X] T032 [P] Confirmar ausencia de secretos/API keys en `specs/004-catalogo-60-70/seed-work/` y que candidatos crudos no-publicables no se requieren en el repo final (limpiar o `.gitignore` selectivo si hace falta)
- [X] T033 [P] Nota cruzada en `specs/004-catalogo-60-70/validation-log.md`: listado plano crece — UX mitigada por feature `003-navegacion-videos`
- [X] T034 Marcar checklist `specs/004-catalogo-60-70/checklists/requirements.md` Notes con enlace a `validation-log.md` PASS final

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup → Foundational → US2 → US3 (filtro) → US1 (CSV) → US3 smoke → US4 → Polish**
- US1 de producto **después** de tener `publish-list.md` (no al revés)
- Smoke (T022–T024) después de CSV escritos

### User Story Dependencies

- **US2**: Tras foundational
- **US3 (review)**: Tras US2
- **US1**: Tras publish-list (US3)
- **US3 (smoke)**: Tras US1
- **US4**: Tras US1 (idealmente tras smoke)

### Parallel Opportunities

- T002/T003; T006/T007; T018 con preparación de T019; T025/T026; T031/T032/T033

---

## Parallel Example: User Story 4

```bash
Task: "Actualizar README.md alcance 60/70"
Task: "Actualizar addon.xml descriptions"
# Luego bump versión + changelog (secuencial)
```

---

## Implementation Strategy

### MVP First

1. Setup + Foundational + US2 + US3 review → publish-list
2. US1 → CSV + pytest años → **MVP navegable**
3. Smoke T022–T024
4. US4 docs + versión

### Incremental Delivery

- Se puede abrir PR con CSV parcial si cumple umbrales; no mergear por debajo de FR-005/006
- 003 puede ir en paralelo; si 003 no está, aceptar listado largo temporalmente (T033)

---

## Notes

- MUST NOT scrapear catálogo dentro del addon en runtime
- MUST NOT crear `YYYY.csv` vacío
- Preferir asistencia IA/listas en host; revisión humana obligatoria antes de `resources/csv/`
- Limpiar `seed-work/` de ruido no publicable antes del merge final si no aporta trazabilidad
