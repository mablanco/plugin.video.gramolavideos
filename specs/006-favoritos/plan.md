# Plan de implementación: Favoritos de usuario

**Branch**: `006-favoritos` | **Date**: 2026-07-29 | **Spec**:
[spec.md](./spec.md)

**Input**: Feature specification from `/specs/006-favoritos/spec.md`.

**Note**: Planificación de favoritos solamente; no genera `tasks.md` ni
incluye búsqueda, sync, multi-listas o cambios al catálogo editorial.

## Summary

Incorporar favoritos locales por perfil de Kodi: una carpeta **Favoritos** en
la raíz, acciones de contexto para añadir/quitar canciones y un listado
reproducible usando el mismo flujo YouTube. `favorites.py` persistirá una
colección JSON independiente del CSV, identificada por `year_id + video_id`,
y `kodi_plugin.py` conservará el routing y la UI. Los favoritos que dejen de
resolver se ocultan por defecto y se notifican si llegan a reproducirse.

Las decisiones y sus alternativas quedan en [research.md](./research.md); los
contratos de interfaz y persistencia están en
[plugin-navigation.md](./contracts/plugin-navigation.md) y
[favorites-store.md](./contracts/favorites-store.md).

## Technical Context

**Language/Version**: Python 3 del runtime de Kodi (Matrix, Nexus, Omega y
posteriores); documentación en español.

**Primary Dependencies**: APIs Kodi `xbmcaddon`, `xbmcgui` y `xbmcplugin`;
`plugin.video.youtube` ya declarado para reproducción; biblioteca estándar
`json`, `datetime` y filesystem. Sin dependencias nuevas ni binarias.

**Storage**: `favorites.json` bajo el perfil/addon_data de Kodi, por
instalación/perfil. Los CSV `resources/csv/YYYY.csv` siguen siendo solo
catálogo editorial.

**Testing**: pytest para `favorites.py`, resolución/deduplicación y wiring de
modos; smoke manual de Kodi descrito en [quickstart.md](./quickstart.md).

**Target Platform**: addon `plugin.video.gramolavideos` en Kodi Matrix/Nexus/
Omega+.

**Project Type**: plugin de vídeo Kodi con navegación de directorios.

**Performance Goals**: raíz y listado de favoritos responden sin red adicional;
resolver una lista lineal abre únicamente los CSV referenciados, adecuado para
decenas o cientos de favoritos del MVP.

**Constraints**: mantener décadas → años → canciones → reproducción; no tocar
el formato CSV ni rehostear vídeo; JSON local tolerante a errores; acciones
usables con mando; cadenas de UI extraíbles a idiomas Kodi.

**Scale/Scope**: una lista por perfil, operaciones add/list/remove, orden
reciente primero y política `hide_or_notify`; fuera de alcance búsqueda,
carpetas, orden manual, nube, cuentas y multi-dispositivo.

## Constitution Check

*GATE: comprobado antes de investigación y de nuevo después del diseño.*

From `.specify/memory/constitution.md` (La Gramola de Videos v1.3.0):

| Principle | Pre-design | Post-design |
|---|---|---|
| **I. Catálogo como datos** | PASS — no se modifican CSV | PASS — JSON es preferencia; CSV continúa como fuente editorial |
| **II. Reproducción vía YouTube** | PASS | PASS — se reutiliza el resolved URL vigente |
| **III. Alcance editorial** | PASS — sin entradas nuevas | PASS |
| **IV. Simplicidad / flujo** | PASS condicional — raíz extra requiere justificación | PASS — acceso adicional documentado en Complexity Tracking; no sustituye décadas |
| **V. Metadatos y versionado** | PASS — implementación evaluará bump/changelog | PASS — el plan preserva id y no añade dependencias |
| **VI. Kodi moderna** | PASS — Python 3 y sin binarios | PASS |
| **VII. Desacoplamiento y APIs Kodi** | PASS — separar datos de UI | PASS — `favorites.py` puro; `kodi_plugin.py` encapsula `xbmc*` |
| **VIII. Tolerancia a fallos** | PASS — I/O local recuperable | PASS — errores/huérfanos notifican sin abortar |
| **IX. IA / secretos** | PASS | PASS — no se versiona el perfil ni datos locales |
| **X. Idioma / i18n** | PASS — docs en español | PASS — etiquetas/avisos mediante strings es/en |

**Gate result**: PASS. La única ampliación de navegación es una entrada raíz
adicional, justificada abajo y sin taxonomía editorial paralela.

## Project Structure

### Documentation (this feature)

```text
specs/006-favoritos/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
└── contracts/
    ├── favorites-store.md
    └── plugin-navigation.md
```

`tasks.md` no se crea en esta fase.

### Source Code (previsto al implementar)

```text
addon.py
resources/
├── csv/                              # catálogo editorial sin cambios
├── lib/
│   ├── catalog.py                    # resolución de MusicVideo existente
│   ├── favorites.py                  # modelo y store JSON sin xbmc*
│   ├── kodi_i18n.py                  # fallback de nuevos IDs
│   └── kodi_plugin.py                # raíz, modos y contexto Kodi
└── language/
    ├── resource.language.es_es/strings.xml
    └── resource.language.en_gb/strings.xml
tests/
└── unit/
    ├── test_favorites.py
    └── test_plugin_favorites.py
```

**Structure Decision**: Extender el layout existente. `favorites.py` contiene
solo lógica de preferencias y resolución basada en `catalog`; la UI, URLs,
notificaciones y objetos `xbmc*` permanecen en módulos Kodi ya establecidos.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|---|---|---|
| Entrada raíz adicional **Favoritos** frente al flujo constitucional décadas → años → canciones → reproducción | Da acceso rápido a preferencias personales sin alterar los CSV ni añadir un nivel al browse cronológico. | Ocultar favoritos dentro de cada año obliga a recordar el año; reemplazar décadas elimina la navegación editorial; una nueva taxonomía/carpeta jerárquica excede el MVP. |
