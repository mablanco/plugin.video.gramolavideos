# Tasks: Alcance de búsqueda y favoritos

**Input**: Design documents from `/specs/005-busqueda-favoritos/`

**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/, decision.md, quickstart.md

**Tests**: No suite automatizada. Validación = revisión documental del `quickstart.md` (SC-001–SC-005). **Prohibido** cambiar código del addon en estas tareas (FR-010).

**Organization**: Feature de **análisis y empaquetado**. El veredicto preliminar ya está en `decision.md` / `research.md`; estas tareas lo cierran, auditan y dejan el handoff a futuros `/speckit-specify`.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- Artefactos: `specs/005-busqueda-favoritos/`
- Código del addon (**no modificar**): `addon.py`, `addon.xml`, `resources/lib/`, `resources/csv/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Dejar el directorio listo para el cierre documental

- [ ] T001 Verificar que existen `specs/005-busqueda-favoritos/plan.md`, `spec.md`, `research.md`, `decision.md`, `data-model.md`, `quickstart.md` y `contracts/` según `plan.md`
- [ ] T002 [P] Crear `specs/005-busqueda-favoritos/validation-log.md` con tabla del `quickstart.md` (pasos 1–6) y columnas Resultado / Notas / Fecha
- [ ] T003 [P] Anotar en `specs/005-busqueda-favoritos/validation-log.md` el invariante FR-010: cero cambios runtime en esta feature

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Alinear criterios, contratos y status del veredicto antes de las historias

**⚠️ CRITICAL**: No marcar US1 completa hasta congelar criterios P1–P5 y contrato de packaging

- [ ] T004 Alinear la tabla de criterios P1–P5 en `specs/005-busqueda-favoritos/decision.md` con `specs/005-busqueda-favoritos/contracts/decision-criteria.md` y `research.md` R-001
- [ ] T005 [P] Confirmar en `specs/005-busqueda-favoritos/contracts/packaging-verdict.md` los campos `strategy: two_features`, `order: favorites -> search`, `implements_runtime_in_005: false`
- [ ] T006 [P] Inventariar en `specs/005-busqueda-favoritos/decision.md` las estrategias A (una feature) y B (dos features) con enlace a `research.md` R-004
- [ ] T007 Actualizar `Status` en `specs/005-busqueda-favoritos/decision.md` a texto explícito “Aprobado para cierre documental” o “Pendiente validación mantenedor” según revisión actual
- [ ] T008 Confirmar en `specs/005-busqueda-favoritos/decision.md` que no se modifican `addon.py` / `resources/lib/kodi_plugin.py` / `resources/csv/` en el alcance de 005

**Checkpoint**: Foundation ready — se pueden cerrar las historias en paralelo documental

---

## Phase 3: User Story 1 - Decidir una vs dos features (Priority: P1) 🎯 MVP

**Goal**: Veredicto inequívoco una vs dos features, con orden y exclusiones (SC-001, SC-003)

**Independent Test**: Leer solo `specs/005-busqueda-favoritos/decision.md` y extraer decisión, orden, exclusiones y siguiente Speckit en &lt;10 minutos

### Implementation for User Story 1

- [ ] T009 [US1] Completar o verificar matriz P1–P5 × estrategias A/B en `specs/005-busqueda-favoritos/decision.md` (o tabla resumen que cite `research.md` R-004)
- [ ] T010 [US1] Redactar el veredicto único en una frase destacada al inicio de `specs/005-busqueda-favoritos/decision.md` (“Dos features distintas…”)
- [ ] T011 [US1] Documentar orden favoritos → búsqueda y nombres sugeridos (`favoritos-usuario`, `busqueda-catalogo`) en `specs/005-busqueda-favoritos/decision.md` alineados con `contracts/packaging-verdict.md`
- [ ] T012 [US1] Listar fuera de alcance de 005 (implementación UI, pytest nuevo, cambio de CSV/YouTube) en `specs/005-busqueda-favoritos/decision.md`
- [ ] T013 [US1] Marcar pasos 1–3 del `quickstart.md` como PASS en `specs/005-busqueda-favoritos/validation-log.md` tras auto-revisión SC-001/SC-003

**Checkpoint**: MVP documental — empaquetado decidido sin Kodi

---

## Phase 4: User Story 2 - Describir el valor de búsqueda (Priority: P1)

**Goal**: Perfil de búsqueda independiente y testeable sin favoritos (FR-003)

**Independent Test**: Sección de búsqueda en `decision.md`/`research.md` describe flujo, vacío y exclusiones sin mencionar favoritos como dependencia

### Implementation for User Story 2

- [ ] T014 [P] [US2] Completar sección “Búsqueda — flujo MVP” en `specs/005-busqueda-favoritos/decision.md` (entrada raíz, query local título/artista, resultados, vacío) citando `research.md` R-002
- [ ] T015 [P] [US2] Listar exclusiones de búsqueda (YouTube global, filtros avanzados, recomendaciones) en `specs/005-busqueda-favoritos/decision.md`
- [ ] T016 [US2] Añadir nota de priorización: búsqueda gana valor tras `004-catalogo-60-70` en `specs/005-busqueda-favoritos/decision.md`
- [ ] T017 [US2] Verificar que `SearchCapability` en `specs/005-busqueda-favoritos/data-model.md` coincide con el texto de `decision.md` y corregir divergencias

**Checkpoint**: Búsqueda definida como feature futura aislable

---

## Phase 5: User Story 3 - Describir el valor de favoritos (Priority: P1)

**Goal**: Perfil de favoritos independiente (marcar / listar / quitar)

**Independent Test**: Flujo de favoritos usable como historia sola, sin búsqueda

### Implementation for User Story 3

- [ ] T018 [P] [US3] Completar sección “Favoritos — flujo MVP” en `specs/005-busqueda-favoritos/decision.md` (añadir, listar desde raíz, quitar, persistencia local) citando `research.md` R-003
- [ ] T019 [P] [US3] Listar exclusiones de favoritos (multi-listas, nube, playlists colaborativas) en `specs/005-busqueda-favoritos/decision.md`
- [ ] T020 [US3] Documentar política de huérfanos a alto nivel (`hide_or_notify`) en `specs/005-busqueda-favoritos/decision.md` enlazando `data-model.md` (`orphan_policy`)
- [ ] T021 [US3] Verificar que `FavoritesCapability` en `specs/005-busqueda-favoritos/data-model.md` coincide con `decision.md` y corregir divergencias

**Checkpoint**: Favoritos definidos como 1ª feature de implementación futura

---

## Phase 6: User Story 4 - Encajar con la gramola simple (Priority: P2)

**Goal**: Invariantes de producto y convivencia con navegación/catálogo (SC-005)

**Independent Test**: `decision.md` afirma CSV editorial intacto, YouTube intacto, favoritos ≠ catálogo, entrada adicional en raíz

### Implementation for User Story 4

- [ ] T022 [P] [US4] Añadir sección “Invariantes de producto” en `specs/005-busqueda-favoritos/decision.md` (catálogo CSV, no rehost, reproducción YouTube, favoritos como preferencias)
- [ ] T023 [P] [US4] Documentar convivencia con raíz de `003-navegacion-videos` (ítems Buscar/Favoritos junto a décadas) en `specs/005-busqueda-favoritos/decision.md` citando `research.md` R-006
- [ ] T024 [US4] Confirmar en `specs/005-busqueda-favoritos/decision.md` que opciones con cuenta online obligatoria o reescritura masiva de CSV quedan rechazadas
- [ ] T025 [US4] Anotar prioridad relativa vs 003/004 en `specs/005-busqueda-favoritos/decision.md` (favoritos paralelizable; búsqueda preferible tras 004)

**Checkpoint**: Encaje con identidad del producto explícito

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Handoff Speckit y cierre de validación

- [ ] T026 [P] Escribir borrador de prompt para `/speckit-specify` de favoritos en `specs/005-busqueda-favoritos/handoff-favoritos.md` (alcance MVP + exclusiones de `decision.md`)
- [ ] T027 [P] Escribir borrador de prompt para `/speckit-specify` de búsqueda en `specs/005-busqueda-favoritos/handoff-busqueda.md` (alcance MVP + exclusiones + dependencia recomendada de 004)
- [ ] T028 Actualizar sección “Siguiente comando Speckit” en `specs/005-busqueda-favoritos/decision.md` enlazando `handoff-favoritos.md` y `handoff-busqueda.md`
- [ ] T029 Ejecutar checklist del `specs/005-busqueda-favoritos/quickstart.md` completo y marcar PASS en `specs/005-busqueda-favoritos/validation-log.md` (SC-001–SC-005)
- [ ] T030 [P] Actualizar `specs/005-busqueda-favoritos/checklists/requirements.md` Notes con enlace a `validation-log.md` y estado de cierre
- [ ] T031 [P] Verificar con `git status` / diff que no hay cambios bajo `resources/` ni `addon.py` atribuibles a 005; anotar en `validation-log.md`
- [ ] T032 Marcar `Status` final en `specs/005-busqueda-favoritos/spec.md` como “Decision complete” (o equivalente) tras PASS del quickstart

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: inmediato
- **Foundational (Phase 2)**: tras Setup — bloquea cierre formal de US1
- **US1–US4 (Phases 3–6)**: tras Foundational; US2/US3/US4 documentales pueden ir en paralelo tras T009–T011
- **Polish**: tras US1–US4 deseadas

### User Story Dependencies

- **US1**: Tras foundational — MVP
- **US2**: Independiente de US3 (puede paralelizar)
- **US3**: Independiente de US2
- **US4**: Ideal tras US1 (usa el veredicto); puede solaparse con US2/US3

### Parallel Opportunities

- T002/T003; T005/T006; T014/T015; T018/T019; T022/T023; T026/T027; T030/T031

---

## Parallel Example: User Story 2 + 3

```bash
Task: "Completar sección Búsqueda en specs/005-busqueda-favoritos/decision.md"
Task: "Completar sección Favoritos en specs/005-busqueda-favoritos/decision.md"
Task: "Listar exclusiones de búsqueda en decision.md"
Task: "Listar exclusiones de favoritos en decision.md"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Phase 1–2
2. Phase 3 (US1) → veredicto auditable
3. **STOP**: quickstart pasos 1–3
4. Continuar US2–US4 + handoffs

### Incremental Delivery

1. US1 → decisión publicada
2. US2 + US3 → perfiles listos para specify futuros
3. US4 + Polish → handoff y cierre formal de 005

### Suggested next after this feature

1. `/speckit-specify` usando `handoff-favoritos.md`
2. Más tarde `/speckit-specify` usando `handoff-busqueda.md`
3. No reabrir 005 como implementación de UI

---

## Notes

- [P] = distintos ficheros o secciones sin dependencia
- Cero LOC de addon
- No generar pytest
- El “MVP” de 005 es el veredicto, no favoritos usables en Kodi
