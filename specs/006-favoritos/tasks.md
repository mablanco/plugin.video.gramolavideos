# Tasks: Favoritos de usuario

**Input**: Design documents from `/specs/006-favoritos/`

**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/, quickstart.md

**Tests**: El plan exige pytest de `favorites.py` y wiring de modos; se incluyen tests unitarios. Smoke Kodi en polish.

**Organization**: Capas datos → UI por historias P1 (add / list-play / remove / orphans) y P2 (convivencia); polish con README/versión.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- Artefactos: `specs/006-favoritos/`
- Runtime: `resources/lib/favorites.py`, `resources/lib/kodi_plugin.py`, `resources/lib/catalog.py`, `resources/lib/kodi_i18n.py`, `resources/lib/kodi_notify.py`
- i18n: `resources/language/resource.language.es_es/strings.xml`, `resources/language/resource.language.en_gb/strings.xml`
- Tests: `tests/unit/test_favorites.py`, `tests/unit/test_plugin_favorites.py`
- Docs/release: `README.md`, `addon.xml`, `changelog.txt`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Confirmar artefactos y registro de validación

- [X] T001 Verificar que existen `specs/006-favoritos/plan.md`, `spec.md`, `research.md`, `data-model.md`, `quickstart.md` y `contracts/` según `plan.md`
- [X] T002 [P] Crear `specs/006-favoritos/validation-log.md` con tabla de pasos del `quickstart.md` (pytest + smoke Kodi) y columnas Resultado / Notas / Fecha
- [X] T003 [P] Anotar en `specs/006-favoritos/validation-log.md` el baseline actual (raíz = décadas sin Favoritos; sin `favorites.json`)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Store JSON puro + strings i18n + contrato de modos documentado, sin UI aún

**⚠️ CRITICAL**: No empezar wiring de raíz/contexto hasta completar esta fase

- [X] T004 Crear `resources/lib/favorites.py` con tipos/entradas alineados a `specs/006-favoritos/data-model.md` y esquema de `contracts/favorites-store.md` (sin imports `xbmc*`)
- [X] T005 Implementar en `resources/lib/favorites.py` carga/guardado tolerante de `favorites.json` (versión 1, errores recuperables, dedupe por `(year_id, video_id)`)
- [X] T006 [P] Añadir strings de Favoritos / añadir / quitar / vacío / huérfano / errores de store en `resources/language/resource.language.es_es/strings.xml`
- [X] T007 [P] Añadir las mismas claves en `resources/language/resource.language.en_gb/strings.xml`
- [X] T008 Registrar IDs nuevos en `resources/lib/kodi_i18n.py` (o mapa equivalente) sin literales dispersos nuevos en UI
- [X] T009 [P] Crear `tests/unit/test_favorites.py` cubriendo add idempotente, persistencia en disco temporal, remove y clasificación de huérfanos según `contracts/favorites-store.md`

**Checkpoint**: Store testeable sin Kodi; i18n listo

---

## Phase 3: User Story 1 - Añadir (y reconocer) un favorito (Priority: P1) 🎯 MVP

**Goal**: Marcar una canción desde el listado de año y persistirla (SC-001, SC-003 parcial)

**Independent Test**: Menú contextual «Añadir» en un año → favorito en store; segundo add no duplica

### Implementation for User Story 1

- [X] T010 [US1] Exponer `add` / `contains` en `resources/lib/favorites.py` validando resolución vía `catalog` antes de escribir
- [X] T011 [US1] Implementar modo `favorite_add` en `resources/lib/kodi_plugin.py` con params `year_id`, `video_id`, `title` según `contracts/plugin-navigation.md`
- [X] T012 [US1] En `mode=year` de `resources/lib/kodi_plugin.py`, añadir acción de contexto «Añadir a favoritos» (o «Quitar» si ya está) en cada canción
- [X] T013 [US1] Notificar éxito/error recuperable de add vía `resources/lib/kodi_notify.py` (o helper existente)
- [X] T014 [P] [US1] Ampliar `tests/unit/test_plugin_favorites.py` (o crearlo) para assert de URL `favorite_add` y no-duplicado tras segundo add

**Checkpoint**: Se puede añadir favorito desde un año y verlo en el JSON del perfil de prueba

---

## Phase 4: User Story 2 - Listar y reproducir desde la raíz (Priority: P1)

**Goal**: Carpeta Favoritos en raíz + listado reproducible (SC-002)

**Independent Test**: Raíz muestra Favoritos; entrar, ver título, reproducir como desde el año

### Implementation for User Story 2

- [X] T015 [US2] Implementar `list_resolved` en `resources/lib/favorites.py` (orden `added_at` desc; activos vs huérfanos)
- [X] T016 [US2] En raíz sin `mode` de `resources/lib/kodi_plugin.py`, añadir carpeta localizada Favoritos (`mode=favorites`) **antes** de las décadas, sin quitar el browse
- [X] T017 [US2] Implementar modo `favorites` en `resources/lib/kodi_plugin.py`: listar activos con `song_listitem` + URL `mode=song`; estado vacío localizado si no hay activos
- [X] T018 [US2] Revalidar `(year_id, video_id)` antes de resolver play desde Favoritos en `resources/lib/kodi_plugin.py` (mismo YouTube que `mode=song`)
- [X] T019 [P] [US2] Actualizar `tests/unit/test_plugin_favorites.py` / wiring para raíz con Favoritos + décadas y listado reproducible

**Checkpoint**: Acceso raíz + play desde Favoritos en tests/smoke

---

## Phase 5: User Story 3 - Quitar / desmarcar un favorito (Priority: P1)

**Goal**: Remove desde Favoritos o desde el año; CSV intacto; vacío claro (FR-005, FR-009)

**Independent Test**: Quitar → desaparece de Favoritos; canción sigue en su año/CSV

### Implementation for User Story 3

- [X] T020 [US3] Completar `remove` idempotente en `resources/lib/favorites.py` sin tocar CSV
- [X] T021 [US3] Implementar modo `favorite_remove` en `resources/lib/kodi_plugin.py` (`year_id`, `video_id`) según contrato
- [X] T022 [US3] Añadir acción de contexto «Quitar de favoritos» en `mode=favorites` y mantener toggle en `mode=year` en `resources/lib/kodi_plugin.py`
- [X] T023 [US3] Mostrar estado vacío localizado tras quitar el último favorito en modo `favorites` de `resources/lib/kodi_plugin.py`
- [X] T024 [P] [US3] Extender `tests/unit/test_favorites.py` y `tests/unit/test_plugin_favorites.py` para remove + CSV no modificado

**Checkpoint**: Ciclo add → list → remove completo

---

## Phase 6: User Story 4 - Huérfanos y tolerancia (Priority: P1)

**Goal**: Política `hide_or_notify` sin abortos (SC-004, FR-008)

**Independent Test**: Favorito con CSV/fila ausente no aparece en lista; play huérfano avisa; se puede remove

### Implementation for User Story 4

- [X] T025 [US4] Asegurar en `resources/lib/favorites.py` que `list_resolved` excluye huérfanos del listado activo y los conserva en store hasta remove
- [X] T026 [US4] En ruta de play de favorito huérfano en `resources/lib/kodi_plugin.py`, notificar amigable, no resolver URL y permitir `favorite_remove`
- [X] T027 [US4] Manejar fallos de I/O del store en `resources/lib/favorites.py` / `kodi_plugin.py` con notificación y cierre seguro de directorio
- [X] T028 [P] [US4] Añadir casos huérfano + I/O corrupto en `tests/unit/test_favorites.py` y wiring en `tests/unit/test_plugin_favorites.py`

**Checkpoint**: Huérfanos y errores no tumban el addon

---

## Phase 7: User Story 5 - Convivir con la gramola simple (Priority: P2)

**Goal**: Browse cronológico intacto; exclusiones documentadas (SC-005)

**Independent Test**: Sin usar Favoritos, décadas→años→canciones→play igual; docs describen acceso extra

### Implementation for User Story 5

- [X] T029 [US5] Verificar en `tests/unit/test_plugin_wiring.py` (o favoritos) que raíz sigue listando décadas y que modes `decade`/`year`/`song` no cambian de contrato
- [X] T030 [P] [US5] Actualizar `README.md` describiendo Favoritos como acceso adicional (FR-012)
- [X] T031 [P] [US5] Confirmar en `specs/006-favoritos/validation-log.md` exclusiones (sin búsqueda, multi-listas, sync, cuenta online)

**Checkpoint**: Producto documentado; browse principal preservado

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Release hygiene y cierre quickstart

- [X] T032 Bump de versión en `addon.xml` y entrada en `changelog.txt` al publicar favoritos
- [X] T033 [P] Confirmar dependencia YouTube intacta en `addon.xml` (constitution II)
- [X] T034 [P] Confirmar `.gitignore` no versiona `favorites.json` / addon_data / secretos (IX)
- [X] T035 Ejecutar `pytest -q tests/unit/test_favorites.py tests/unit/test_plugin_favorites.py` y anotar PASS en `specs/006-favoritos/validation-log.md`
- [X] T036 Completar smoke Kodi del `quickstart.md` (pasos 1–6) en `specs/006-favoritos/validation-log.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: inmediato
- **Foundational (Phase 2)**: tras Setup — **bloquea** todas las US
- **US1 → US2 → US3 → US4**: secuencial recomendado (mismo `kodi_plugin.py` / store)
- **US5**: tras US2 como mínimo (raíz con Favoritos)
- **Polish**: tras US deseadas

### User Story Dependencies

- **US1**: tras Phase 2
- **US2**: tras US1 (necesita entradas para listar/play útiles; carpeta raíz puede stubs vacío antes)
- **US3**: tras US1/US2
- **US4**: tras US2 (list_resolved) y US3 (remove)
- **US5**: tras US2

### Parallel Opportunities

- T002/T003; T006/T007; T014 con docs; T030/T031; T033/T034
- Tests de store (`test_favorites.py`) vs i18n strings en Phase 2

---

## Parallel Example: User Story 1

```bash
Task: "Implementar modo favorite_add en resources/lib/kodi_plugin.py"
Task: "Ampliar tests/unit/test_plugin_favorites.py para favorite_add"
```

---

## Implementation Strategy

### MVP First (US1 + store)

1. Phase 1–2 → store + i18n
2. US1 add desde año → validar JSON
3. Luego US2 list/play (demo usable)
4. US3 remove → US4 orphans → US5 docs → polish

### Incremental Delivery

1. Foundation → add → list/play (MVP demo)
2. Remove + empty state
3. Orphans + tolerancia
4. README / versión / smoke completo

---

## Notes

- No fusionar favoritos en CSV; no modos de búsqueda en esta feature
- `tasks.md` es la fuente de ejecución para `/speckit-implement`
- Commit por tarea o grupo lógico tras validar checkpoint
