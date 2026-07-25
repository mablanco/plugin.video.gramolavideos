# Implementation Plan: Auditoría y remediación incremental

**Branch**: `001-auditoria-codigo` | **Date**: 2026-07-25 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/001-auditoria-codigo/spec.md` + input de planificación: estrategia en 3 fases consecutivas (caracterización → bugs críticos → refactor/deuda), basándose en la auditoría y `.specify/memory/constitution.md`.

**Note**: Este plan es la salida de `/speckit-plan`. Las tareas ejecutables se generarán con `/speckit-tasks` (no en este comando).

## Summary

Remediar de forma evolutiva el addon publicado `plugin.video.gramolavideos` (monolito Python 2 en `addon.py`, sin tests) para alinearlo con la constitution (Kodi/Python 3, desacoplamiento datos/UI, tolerancia a fallos, catálogo como CSV, YouTube) **sin** fusionar el scaffold `plugin.video.gramola`.

Enfoque técnico: tres fases consecutivas con criterios de salida — (1) red de seguridad con pytest + extract literal de catálogo, (2) corrección P1 de compatibilidad/robustez/reproducción + migración `main`, (3) layout `resources/lib/`, carga selectiva, typing/higiene e i18n-ready. YAGNI: sin routing externo ni reescritura total.

## Technical Context

**Language/Version**: Python 3 (destino Kodi Matrix / Nexus / Omega+); código actual legacy Python 2 en `addon.py`

**Primary Dependencies**: Runtime Kodi (`xbmc`, `xbmcgui`, `xbmcplugin`, `xbmcaddon`); `plugin.video.youtube` (declarado en `addon.xml`). Tooling de desarrollo: `pytest` (no va en `requires` del addon)

**Storage**: Ficheros CSV por año en `resources/csv/` (`Artista - Canción;youtube_video_id`, delimitador `;`)

**Testing**: pytest + stubs `xbmc*` para harness; caracterización y unitarios de catálogo sin UI; reproducción end-to-end manual en Kodi

**Target Platform**: Addon Kodi `xbmc.python.pluginsource`, plataforma `all`

**Project Type**: Kodi video plugin (índice/navegador de vídeos musicales)

**Performance Goals**: Listar años / un año sin materializar todo el catálogo (SC-004); recorrido feliz &lt; 30 s en red normal (SC-001)

**Constraints**: GPL-3.0; id fijo `plugin.video.gramolavideos`; sin libs binarias ajenas al runtime Kodi; sin rehostear vídeo; sin frameworks no justificados; comunicación/docs de producto en español; UI i18n-ready al tocar cadenas

**Scale/Scope**: ~20 CSV de año (1980–1999 sin 1994), ~140 filas; un entry point; remediación incremental en 3 fases (este plan)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

From `.specify/memory/constitution.md` (La Gramola de Videos v1.2.1):

| Principle | Pre-design | Post-design (Phase 1) |
|-----------|------------|------------------------|
| **I. Catálogo como datos** | PASS — remediación mantiene CSV; no hardcodea listas | PASS — contratos/data-model preservan formato `;` |
| **II. Reproducción vía YouTube** | PASS — se mantiene URI/dependencia | PASS — contract de navegación lo fija |
| **III. Alcance editorial** | PASS — alinear mensaje/datos; fix id inválido; ampliar 60–70 MAY ser contenido aparte | PASS |
| **IV. Simplicidad** | PASS — flujo años→canciones→play; capas nuevas solo en Complexity Tracking | PASS — sin routing; layout mínimo justificado |
| **V. Metadatos / versionado** | PASS — id preservado; versión/changelog en cambios de comportamiento | PASS |
| **VI. Compatibilidad Kodi moderna** | PASS — Fase 2 migra Py3/APIs | PASS — research R-004 |
| **VII. Desacoplamiento** | PASS — extract + `resources/lib/` | PASS — contracts catalog vs kodi |
| **VIII. Tolerancia a fallos** | PASS — `CatalogLoadResult` + notificación | PASS |
| **IX. IA / secretos** | PASS — no secretos; evolución no rewrite | PASS |
| **X. Idioma / i18n** | PASS — plan en español; esqueleto language al tocar UI | PASS |

**Gate result**: PASS (sin violaciones injustificadas). Complejidad añadida justificada abajo.

## Project Structure

### Documentation (this feature)

```text
specs/001-auditoria-codigo/
├── plan.md              # This file
├── research.md          # Phase 0
├── data-model.md        # Phase 1
├── quickstart.md        # Phase 1
├── contracts/           # Phase 1
│   ├── catalog.md
│   ├── plugin-navigation.md
│   └── repo-default-branch.md
├── checklists/
└── tasks.md             # Phase 2 output (/speckit-tasks — NOT created here)
```

### Source Code (target layout after Fase 3; Fase 1 introduce lo mínimo)

```text
addon.py                 # entry point fino (pluginsource)
addon.xml                # id, version, requires (xbmc.python 3.x), metadata
changelog.txt
README.md
resources/
├── csv/                 # YYYY.csv
├── lib/
│   ├── catalog.py       # datos puros (sin xbmc)
│   ├── kodi_plugin.py   # listados / resolve / handle
│   └── kodi_notify.py   # avisos recuperables
├── language/            # esqueleto i18n cuando se toquen cadenas
│   ├── resource.language.es_es/
│   └── resource.language.en_gb/   # o en_us según convención elegida en tasks
├── icon.png
└── fanart.jpg
tests/
├── unit/
│   └── test_catalog_*.py
├── fixtures/            # CSV válidos/inválidos
└── stubs/               # xbmc* mínimos si hacen falta
```

**Structure Decision**: Addon Kodi existente en la raíz del repo. Se adopta layout entry + `resources/lib/` (ideas del andamiaje, no fusión). Tests en `tests/` solo como tooling de desarrollo. No se cambia el addon id ni se importa `script.module.routing`.

## Complexity Tracking

| Violation / added surface | Why Needed | Simpler Alternative Rejected Because |
|---------------------------|------------|--------------------------------------|
| Paquete `resources/lib/` + módulos kodi/datos | Constitution VII, FR-004/005/012b; habilita tests sin Kodi | Seguir en un solo `addon.py` — impide SC-003 y remediación segura |
| `tests/` + stubs `xbmc*` + pytest | Fase 1 safety net; SC-003 | Solo QA manual en Kodi — no congela comportamiento |
| Helper de notificación | Constitution VIII, FR-006 | Traceback/silencio — falla robustez auditada |
| Esqueleto `resources/language/` | Constitution X, FR-015 | Literales dispersos — bloquean i18n futura |
| API `list_years` / `load_year` | Preparar FR-008/009 sin segundo quiebre | Optimizar ad hoc dentro de UI — acopla de nuevo datos y pantalla |

Explicitly **not** added: `script.module.routing`, fusión `plugin.video.gramola`, settings/debug stack del scaffold.

---

## Implementation Strategy — 3 fases consecutivas (obligatorias)

> Estas fases son el eje del trabajo de remediación. **No** se solapan: cada una tiene criterio de salida. Mapean el inventario P1–P3 de la spec.

### Fase 1 — Tests de caracterización (Safety Net)

**Objetivo**: Congelar el comportamiento *actual* antes de correcciones funcionales.

**Incluye**:
1. Harness pytest + fixtures CSV (válido, fila corta, fila incompleta, dir vacío).
2. Extracción *literal* de lectura/parseo CSV a `resources/lib/catalog.py` (move sin cambio de semántica) para poder importar sin Kodi.
3. Stubs mínimos `xbmc*` solo si se necesita ejercitar el cableado de query sin runtime real.
4. Tests que fijan: conjunto de años del repo (incl. ausencia de 1994), forma de filas cargadas hoy (incl. id inválido de Chiquilla *aún presente* en datos), contrato `mode`/`foldername`.
5. Documentar en comentarios/tests qué assertions son “legacy freeze” vs las que se sustituirán en Fase 2.

**No incluye**: validación estricta de video_id, migración Py3 en `addon.xml`, `setResolvedUrl`, carga lazy, i18n completa, cambio editorial de descripción.

**Criterio de salida**: `pytest` verde; SC-003 baseline; cero cambios de producto observables en Kodi respecto al legacy (salvo path de import del extract).

**Hallazgos cubiertos**: base para P1 acoplamiento (preparación); no cierra bugs todavía.

### Fase 2 — Corrección de bugs críticos

**Objetivo**: Priorizar roturas, excepciones y compatibilidad (inventario P1 + gobernanza `main`).

**Incluye** (orden sugerido):
1. **Compatibilidad Kodi/Python 3**: `addon.xml` (`xbmc.python` 3.x), `urllib.parse`, I/O texto UTF-8, ListItem APIs modernas, resolución de path del addon sin hardcode frágil, content type adecuado.
2. **Robustez de catálogo**: validación de filas / video_id; `CatalogLoadResult` + errores recuperables; notificación amigable; omitir inválidas sin tumbar listado.
3. **Datos**: corregir o eliminar `Seguridad Social - Chiquilla;d3mZmP_me4`.
4. **Reproducción**: integrar play con handle del plugin (`setResolvedUrl` / fachada); HTTPS en thumbnails; fallo de imagen no bloquea.
5. **Rama por defecto**: migrar `master` → `main`; actualizar changelog/README/referencias (FR-018–020).
6. Actualizar tests: de “freeze legacy” a comportamiento deseado en validación/errores; mantener verdes.
7. Versión + changelog si el comportamiento de usuario cambia (FR-011).

**Criterio de salida**: P1 del inventario cerrados o con decisión documentada (SC-005); SC-001/SC-002 en prueba manual; default branch `main` (SC-008); pytest verde.

**Hallazgos cubiertos**: P1 plataforma, P1 robustez, P1 id inválido; P2 rama `main`; parte de P2 clasificación/miniaturas si se toca la capa Kodi.

### Fase 3 — Refactorización y deuda técnica

**Objetivo**: Arquitectura, desacoplamiento completo, typing y limpieza (P2/P3 restantes).

**Incluye**:
1. Entry point fino: `addon.py` delega en `resources/lib/kodi_*.py`; catálogo solo en módulo de datos.
2. Implementar carga selectiva real: `list_years` sin materializar canciones; `load_year` solo un CSV (FR-008/009, SC-004); cerrar TODOs del README.
3. Type hints graduales en `resources/lib/`; limpieza de smells (ordenaciones redundantes, rutas rígidas residuales).
4. Esqueleto i18n + centralizar cadenas tocadas (FR-015); no hace falta UI bilingüe completa en este incremento.
5. Alineación editorial: ajustar description/summary **o** plan de contenido; 0 ids inválidos conocidos (SC-006).
6. Higiene de producto: metadatos incompletos, changelog útil, deuda README.
7. Verificar mapa FR-001–FR-020 → evidencia (SC-007).

**Criterio de salida**: layout objetivo; SC-004; SC-006; sin hallazgos P1 abiertos; Complexity Tracking sin sorpresas nuevas no justificadas.

**Hallazgos cubiertos**: P1 acoplamiento (cierre), P2 rendimiento, P2 producto–datos, P3 higiene.

---

## Phase 0 / Phase 1 Speckit design outputs

- [research.md](./research.md) — decisiones R-001…R-012 (fases, pytest, Py3, validación, layout, lazy load, thumbnails, `main`, typing)
- [data-model.md](./data-model.md) — Year, MusicVideo, CatalogLoadResult, CatalogError, AuditFinding, DefaultBranch
- [contracts/](./contracts/) — catálogo, navegación plugin, default branch
- [quickstart.md](./quickstart.md) — validación por fase

## Next command

`/speckit-tasks` para desglosar estas 3 fases en tareas dependency-ordered en `tasks.md`.
