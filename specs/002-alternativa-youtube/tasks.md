# Tasks: Alternativa al addon de YouTube

**Input**: Design documents from `/specs/002-alternativa-youtube/`

**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/, quickstart.md

**Tests**: No suite automatizada pedida en la spec. La validación es documental + smoke manual en Kodi (quickstart). No se generan tareas pytest.

**Organization**: Feature de **análisis y decisión** (FR-010): no cambiar código de reproducción ni `addon.xml` en estas tareas. La implementación del sustituto es una feature posterior.

**Reframe 2026-07-28**: El veredicto vigente es **híbrido** (YouTube por defecto + fallback yt-dlp para login-wall), no sustitución total. Al ejecutar estas tareas, alinear `decision.md` con `research.md` R-001/R-004 actualizados (C8, SC-003). Priorizar smoke T015 sobre un título con login-wall (p. ej. *Eclipse total*).

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- Artefactos de esta feature: `specs/002-alternativa-youtube/`
- Código del addon (**no modificar** en esta feature): `addon.py`, `addon.xml`, `resources/lib/kodi_plugin.py`
- Catálogo (**no modificar** como solución): `resources/csv/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Dejar el directorio de la feature listo para el paquete de decisión

- [ ] T001 Verificar que existen `specs/002-alternativa-youtube/plan.md`, `spec.md`, `research.md`, `data-model.md`, `quickstart.md` y `contracts/` según `plan.md`
- [ ] T002 [P] Crear esqueleto vacío `specs/002-alternativa-youtube/decision.md` con secciones Título, Resumen ejecutivo, Opciones, Veredicto, Fricción usuario, Gobernanza, Riesgos, Siguientes pasos
- [ ] T003 [P] Crear esqueleto `specs/002-alternativa-youtube/validation-log.md` con tabla de pasos del quickstart (Parte 1 documental / Parte 2 smoke) y columnas Resultado / Notas / Fecha

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Congelar criterios y baseline de opciones antes de redactar el veredicto final

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T004 Alinear la tabla de criterios C1–C7 en `specs/002-alternativa-youtube/decision.md` con `specs/002-alternativa-youtube/contracts/decision-criteria.md` y `research.md` R-002 (sin cambiar el vocabulario de scoring)
- [ ] T005 [P] Inventariar en `specs/002-alternativa-youtube/decision.md` el set mínimo de opciones A (YouTube+mitigaciones), B (Tubed), C (SendToKodi) citando `research.md` R-003
- [ ] T006 [P] Registrar en `specs/002-alternativa-youtube/decision.md` las opciones D–F como rechazadas/incompatibles con una línea de motivo cada una (research R-003)
- [ ] T007 Confirmar en `specs/002-alternativa-youtube/decision.md` el invariante “sin cambio de código en esta feature” (FR-010) y enlace a URI actual en `resources/lib/kodi_plugin.py` solo como referencia

**Checkpoint**: Foundation ready — se puede completar el veredicto y las historias en paralelo documental

---

## Phase 3: User Story 1 - Decidir con criterios claros (Priority: P1) 🎯 MVP

**Goal**: Publicar un entregable de decisión accionable (adoptar SendToKodi / plan B / diferir) auditable en ≤ 15 minutos

**Independent Test**: Leer solo `specs/002-alternativa-youtube/decision.md` y comprobar opciones ≥ 3, veredicto único, y si hace falta enmendar gobernanza

### Implementation for User Story 1

- [ ] T008 [US1] Completar matriz de scoring (C1–C7 × opciones A–C como mínimo) en `specs/002-alternativa-youtube/decision.md` según `contracts/decision-criteria.md`
- [ ] T009 [US1] Redactar el veredicto único en `specs/002-alternativa-youtube/decision.md` (choice, `api_key_free_happy_path`, justificación) alineado con `research.md` R-004
- [ ] T010 [US1] Añadir sección “Impacto en gobernanza” en `specs/002-alternativa-youtube/decision.md` enlazando `contracts/constitution-amendment-draft.md` y dejando explícito `constitution_amendment_required`
- [ ] T011 [US1] Listar fuera de alcance en `specs/002-alternativa-youtube/decision.md` (embeber yt-dlp, rehost, cambio de CSV, implementación en esta feature)
- [ ] T012 [US1] Marcar Parte 1 del quickstart como hecha en `specs/002-alternativa-youtube/validation-log.md` tras auto-revisión de SC-001–SC-005 sobre `decision.md`

**Checkpoint**: US1 entregable — MVP documental listo sin necesitar Kodi

---

## Phase 4: User Story 2 - Validar experiencia del oyente inexperto (Priority: P1)

**Goal**: Documentar el recorrido feliz sin API key (y el contraste con YouTube) y registrar smoke del candidato

**Independent Test**: `decision.md` describe pasos no automáticos; `validation-log.md` tiene resultado de smoke o Plan B explícito

### Implementation for User Story 2

- [ ] T013 [P] [US2] Escribir el `FrictionProfile` del camino recomendado (pasos, `requires_developer_console=false`, fallos esperados) en `specs/002-alternativa-youtube/decision.md`
- [ ] T014 [P] [US2] Escribir el `FrictionProfile` de mantener YouTube (API key/OAuth) en `specs/002-alternativa-youtube/decision.md` para contraste honesto (spec US2 escenario 3)
- [ ] T015 [US2] Ejecutar Parte 2 del `specs/002-alternativa-youtube/quickstart.md` en Kodi (instalar SendToKodi, resolver URI de prueba con un `video_id` de `resources/csv/`) y anotar resultados en `specs/002-alternativa-youtube/validation-log.md`
- [ ] T016 [US2] Si el smoke falla, actualizar el veredicto operativo a Plan B en `specs/002-alternativa-youtube/decision.md` y `validation-log.md` según `contracts/playback-provider.md` (backup path)
- [ ] T017 [US2] Documentar mensajes de error esperados (proveedor ausente / resolución fallida / vídeo no disponible) en `specs/002-alternativa-youtube/decision.md` alineados con `contracts/playback-provider.md`

**Checkpoint**: US2 — queda claro si el usuario inexperto evita API key en el recorrido recomendado (SC-003)

---

## Phase 5: User Story 3 - Preservar el producto como índice (Priority: P2)

**Goal**: Dejar explícito que catálogo, flujo y política anti-rehost se preservan

**Independent Test**: Revisar `decision.md` + contracts y confirmar que no se propone rehost ni cambio de modelo CSV

### Implementation for User Story 3

- [ ] T018 [P] [US3] Añadir sección “Invariantes de producto” en `specs/002-alternativa-youtube/decision.md` (CSV/`video_id` YouTube, años→canciones→play, no descarga) citando `data-model.md`
- [ ] T019 [P] [US3] Verificar que opciones con descarga/rehost quedan `incompatible` al 100% en `specs/002-alternativa-youtube/decision.md` (SC-004) y en la tabla de `research.md` si hace falta un apunte cruzado
- [ ] T020 [US3] Confirmar en `specs/002-alternativa-youtube/decision.md` que miniaturas HTTPS de YouTube pueden permanecer sin depender del addon YouTube (`contracts/playback-provider.md`)
- [ ] T021 [US3] Anotar en `specs/002-alternativa-youtube/decision.md` que `addon.xml` / `resources/lib/kodi_plugin.py` **no** se modifican hasta la feature de implementación posterior

**Checkpoint**: US3 — límites de producto cerrados sin ambigüedad

---

## Phase 6: User Story 4 - Dejar listo el siguiente paso de planificación (Priority: P2)

**Goal**: Paquete de handoff para enmendar constitution + feature de implementación (o cierre limpio Plan B)

**Independent Test**: Un mantenedor puede abrir `/speckit-specify` o un plan de implementación solo con `decision.md` + contracts + validation-log

### Implementation for User Story 4

- [ ] T022 [US4] Redactar “Siguientes pasos” ordenados en `specs/002-alternativa-youtube/decision.md` (enmienda II → smoke OK → feature implementación URI/`requires`/README)
- [ ] T023 [P] [US4] Revisar y, si hace falta, ajustar redacción del borrador en `specs/002-alternativa-youtube/contracts/constitution-amendment-draft.md` para que sea pegable en `.specify/memory/constitution.md` en un PR futuro
- [ ] T024 [P] [US4] Completar checklist de impacto futuro (addon.xml, README, mensajes de error, version bump) en `specs/002-alternativa-youtube/decision.md` según `contracts/playback-provider.md`
- [ ] T025 [US4] Si Plan B: listar mitigaciones priorizadas (guía README, aviso al fallar resolve) en `specs/002-alternativa-youtube/decision.md` sin proponer cambio de dependencia
- [ ] T026 [US4] Enumerar lagunas residuales no bloqueantes en `specs/002-alternativa-youtube/decision.md` (research R-007) sin reabrir el veredicto principal

**Checkpoint**: US4 — handoff listo; esta feature puede cerrarse sin código

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Cierre de calidad del paquete de análisis

- [ ] T027 [P] Actualizar `specs/002-alternativa-youtube/checklists/requirements.md` notes confirmando que el paquete cumple SC-001–SC-006 o listando gaps residuales
- [ ] T028 [P] Releer `specs/002-alternativa-youtube/decision.md` y eliminar detalles de implementación innecesarios (mantener WHAT/WHY; URIs de contrato sí permitidas)
- [ ] T029 Verificar que ningún artefacto de `specs/002-alternativa-youtube/` contiene API keys, client secrets ni credenciales de ejemplo reales (constitution IX)
- [ ] T030 Confirmar que esta feature **no** alteró `addon.xml`, `resources/lib/kodi_plugin.py` ni el principio II en `.specify/memory/constitution.md` (FR-010)
- [ ] T031 Ejecutar revisión final de `specs/002-alternativa-youtube/quickstart.md` Parte 1+estado Parte 2 y cerrar filas pendientes en `specs/002-alternativa-youtube/validation-log.md`
- [ ] T032 [P] Añadir al inicio de `specs/002-alternativa-youtube/decision.md` un resumen de 5–10 líneas usable como abstract del veredicto (SC-001)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Sin dependencias
- **Foundational (Phase 2)**: Depende de Setup — BLOQUEA historias
- **US1 (Phase 3)**: Tras Phase 2 — MVP documental
- **US2 (Phase 4)**: Tras Phase 2; idealmente tras borrador de veredicto US1 (T009) antes de T016
- **US3 (Phase 5)**: Tras Phase 2; puede ir en paralelo a US1/US2 en lo documental
- **US4 (Phase 6)**: Tras US1 (veredicto) y preferiblemente tras US2 (smoke o Plan B)
- **Polish (Phase 7)**: Tras las historias deseadas

### User Story Dependencies

- **US1 (P1)**: Independiente tras foundation — MVP
- **US2 (P1)**: Usa el veredicto de US1; el smoke puede confirmar o forzar Plan B
- **US3 (P2)**: Independiente documentalmente; refuerza invariantes del veredicto
- **US4 (P2)**: Depende del veredicto estable (US1 + resultado US2)

### Within Each User Story

- Redacción antes de marcar validation-log
- Smoke (T015) antes de decidir Plan B (T016)
- Handoff (US4) después del veredicto operativo final

### Parallel Opportunities

- T002/T003 en Setup
- T005/T006 en Foundational
- T013/T014 en US2
- T018/T019 en US3
- T023/T024 en US4
- T027/T028/T032 en Polish
- US3 puede avanzar en paralelo mientras se prepara el smoke de US2

---

## Parallel Example: User Story 1

```bash
# Tras T008 (matriz), el veredicto y gobernanza pueden repartirse:
Task: "T009 [US1] Redactar veredicto en specs/002-alternativa-youtube/decision.md"
Task: "T011 [US1] Listar fuera de alcance en specs/002-alternativa-youtube/decision.md"
# T010 (gobernanza) tras T009; T012 al cerrar la auto-revisión
```

## Parallel Example: User Story 2

```bash
Task: "T013 [US2] FrictionProfile recomendado en specs/002-alternativa-youtube/decision.md"
Task: "T014 [US2] FrictionProfile YouTube en specs/002-alternativa-youtube/decision.md"
# Luego secuencial: T015 smoke → T016 Plan B si falla → T017 mensajes
```

## Parallel Example: User Story 3

```bash
Task: "T018 [US3] Invariantes de producto en specs/002-alternativa-youtube/decision.md"
Task: "T019 [US3] Marcar rehost/descarga incompatible en specs/002-alternativa-youtube/decision.md"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Completar Phase 1–2
2. Completar Phase 3 (US1) → `decision.md` usable
3. **STOP y validar** SC-001/SC-002/SC-005 en lectura de 15 minutos
4. Demo al mantenedor sin Kodi

### Incremental Delivery

1. Setup + Foundational
2. US1 → veredicto documental (MVP)
3. US2 → smoke / fricción real → confirma o Plan B
4. US3 → candados de producto
5. US4 → handoff a enmienda + feature de implementación
6. Polish → cierre

### Parallel Team Strategy

1. Una persona cierra US1 (`decision.md`)
2. Otra prepara entorno Kodi y US2 smoke
3. US3 en paralelo sobre invariantes
4. US4 cuando el veredicto operativo esté estable

---

## Notes

- [P] = distintos ficheros o secciones sin dependencia dura
- **No** implementar el cambio de proveedor en `resources/lib/kodi_plugin.py` ni tocar `addon.xml` aquí
- **No** enmendar `.specify/memory/constitution.md` en esta feature (solo pulir el borrador en `contracts/`)
- El smoke T015 puede quedar “pendiente de entorno” temporalmente, pero entonces el veredicto debe quedar **condicionado** y US4 no debe lanzar implementación
- Commit por grupo lógico de tareas si el mantenedor lo pide
