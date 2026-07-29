# Implementation Plan: Mejorar la navegación del catálogo de vídeos

**Branch**: `003-navegacion-videos` (artefactos; implementar en rama dedicada) | **Date**: 2026-07-29 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/003-navegacion-videos/spec.md`

**Note**: Estudio + implementación. Veredicto en [research.md](./research.md) /
[decision.md](./decision.md): **década → año → canciones → reproducir**.

## Summary

Sustituir el listado plano de años en la raíz por un primer nivel de **décadas**
(solo las que tengan CSV), luego años de esa década, luego canciones. El
catálogo CSV por año y YouTube no cambian. Hay que **enmendar constitution IV**
(flujo documentado) antes o junto al cambio de UI.

## Technical Context

**Language/Version**: Python 3 (runtime Kodi Matrix+); docs en español.

**Primary Dependencies**: APIs plugin Kodi existentes (`xbmcplugin` vía
`kodi_plugin`); `catalog.list_years` / `load_year`; sin nuevas deps de addon.

**Storage**: `resources/csv/YYYY.csv` sin cambio de formato. Agrupación de
década derivada del stem del año (cálculo, no ficheros nuevos).

**Testing**: pytest unit (modes, agrupación, wiring); smoke manual Kodi
(quickstart).

**Target Platform**: `plugin.video.gramolavideos` en Kodi Matrix/Nexus/Omega+.

**Project Type**: Kodi video plugin (navegación de directorios).

**Performance Goals**: `list_years` sin abrir CSV; raíz ≤12 entradas (SC-003);
recorrido feliz &lt; 30 s (SC-005).

**Constraints**: No hardcodear canciones; no rehost; i18n-ready en cadenas
nuevas; enmendar constitution IV; YAGNI (sin routing framework).

**Scale/Scope**: Catálogo actual ~19 años; diseño para ~40 años (1960–1999);
1 nivel nuevo (`mode=decade`); enmienda gobernanza + README.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

From `.specify/memory/constitution.md` (v1.2.1):

| Principle | Pre-design | Post-design |
|-----------|------------|-------------|
| **I. Catálogo como datos** | PASS | PASS — CSV intacto |
| **II. Reproducción YouTube** | PASS | PASS |
| **III. Alcance editorial** | PASS | PASS — sin contenido nuevo aquí |
| **IV. Simplicidad / flujo años→canciones** | FAIL previsto | PASS condicional — flujo pasa a décadas→años→canciones; **enmienda IV** + Complexity Tracking |
| **V. Metadatos** | PASS | PASS — bump versión al implementar |
| **VI. Kodi moderna** | PASS | PASS |
| **VII. Desacoplamiento** | PASS | PASS — helper de décadas en `catalog` o módulo datos; UI en `kodi_plugin` |
| **VIII. Tolerancia fallos** | PASS | PASS |
| **IX. IA / secretos** | PASS | PASS |
| **X. Idioma / i18n** | PASS | PASS — etiquetas vía language strings |

**Gate result**: PASS con Complexity Tracking (IV).

## Project Structure

### Documentation (this feature)

```text
specs/003-navegacion-videos/
├── plan.md
├── research.md
├── decision.md
├── data-model.md
├── quickstart.md
├── contracts/
│   ├── decision-criteria.md
│   ├── plugin-navigation.md
│   └── constitution-amendment-draft-iv.md
├── checklists/
└── tasks.md                 # /speckit-tasks (no este comando)
```

### Source Code (previsto al implementar)

```text
addon.py
addon.xml                    # versión + descripción si cambia UX
resources/lib/catalog.py     # group_years_by_decade / list_decades
resources/lib/kodi_plugin.py # mode=decade; raíz = décadas
resources/language/...       # "Años 80", etc.
tests/unit/test_catalog_*.py
tests/unit/test_plugin_*.py
```

**Structure Decision**: Extender layout addon existente; sin apps nuevas.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Ampliar flujo IV (nivel década) | Listado plano no escala a 60s–90s (SC-003 ≤12 en raíz) | Seguir con años planos — falla SC-003 con ~40 años; “recientes+archivo” — UX inconsistente (research R-003) |
