# Plan de implementación: Año visible al entrar en un año

**Branch**: `008-ano-visible` | **Date**: 2026-07-29 | **Spec**:
[spec.md](./spec.md)

**Input**: Especificación de feature de
`/specs/008-ano-visible/spec.md`.

## Summary

Mostrar de forma persistente el año activo en el listado de sus canciones
mediante `xbmcplugin.setPluginCategory(handle, year_id)`. El cambio queda
acotado a la rama `mode=year` de `resources/lib/kodi_plugin.py` y a una prueba
unitaria de wiring. No cambia el catálogo CSV, las query strings, las etiquetas
editoriales ni el flujo décadas → años → canciones → reproducción.

## Technical Context

**Language/Version**: Python 3, runtime Kodi Matrix/Nexus/Omega y posteriores;
documentación en español.

**Primary Dependencies**: APIs de plugin Kodi existentes (`xbmcplugin`, en
concreto `setPluginCategory`) encapsuladas en `kodi_plugin`; sin dependencias
nuevas.

**Storage**: CSV `resources/csv/YYYY.csv`, sin cambios de formato ni datos
persistidos.

**Testing**: pytest unitario con stubs `xbmcplugin`; smoke manual en Kodi según
[quickstart.md](./quickstart.md).

**Target Platform**: addon `plugin.video.gramolavideos` en Kodi Matrix, Nexus,
Omega y posteriores.

**Project Type**: plugin de vídeo Kodi (navegación de directorios).

**Performance Goals**: Una llamada adicional a la API de Kodi por entrada en un
año; sin I/O, consultas ni latencia adicional perceptible.

**Constraints**: La categoría para `mode=year` debe ser exactamente `year_id`;
no cambiar URL, reproducción, contenido CSV, títulos de canciones ni niveles de
navegación.

**Scale/Scope**: Una rama de routing existente, una llamada a API Kodi y una
prueba de wiring; cero entidades persistidas.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

From `.specify/memory/constitution.md` (La Gramola de Videos v1.3.0):

| Principio | Pre-diseño | Post-diseño |
|-----------|------------|-------------|
| **I. Catálogo como datos** | PASS | PASS — CSV intacto; no hay contenido nuevo. |
| **II. Reproducción vía YouTube** | PASS | PASS — no se toca resolución ni dependencia. |
| **III. Alcance editorial** | PASS | PASS — no se modifica catálogo. |
| **IV. Simplicidad del plugin** | PASS | PASS — conserva décadas → años → canciones → reproducción; usa una API existente. |
| **V. Metadatos y versionado** | PASS | PASS — sin cambio de id ni assets; decidir versión/changelog al implementar conforme al impacto de release. |
| **VI. Kodi moderna** | PASS | PASS — `setPluginCategory` es API estándar de plugin Kodi y no incorpora binarios. |
| **VII. Desacoplamiento y APIs Kodi** | PASS | PASS — la llamada permanece en `kodi_plugin`, capa de UI ya existente; datos no cambian. |
| **VIII. Tolerancia a fallos** | PASS | PASS — se conservan notificaciones y listado residual de catálogo. |
| **IX. IA / secretos** | PASS | PASS — artefactos de planificación sin secretos ni tooling regenerable. |
| **X. Idioma / i18n** | PASS | PASS — la categoría es el identificador numérico del año, sin literal nuevo. |

**Resultado del gate**: PASS antes de investigación y tras el diseño.

## Project Structure

### Documentation (this feature)

```text
specs/008-ano-visible/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── plugin-navigation.md
└── checklists/
```

### Source Code (previsto al implementar)

```text
addon.py                           # entry pluginsource
resources/lib/kodi_plugin.py       # rama mode=year; categoría Kodi
tests/unit/test_plugin_wiring.py   # stub y aserción de setPluginCategory
```

**Structure Decision**: Extender el adaptador de UI existente y su prueba de
wiring. No crear módulos, capas, persistencia, cadenas ni directorios de
navegación.

## Complexity Tracking

No aplica. El diseño usa una API Kodi ya disponible dentro de la capa de UI
existente y no introduce una nueva capa ni una excepción a la constitution.
