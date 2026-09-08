# Plan de implementación: Búsqueda en catálogo

**Branch**: `007-busqueda-catalogo` | **Date**: 2026-07-29 | **Spec**:
[spec.md](./spec.md)

**Input**: Especificación de
`/specs/007-busqueda-catalogo/spec.md` y handoff de búsqueda de 005.

**Note**: Plan de diseño; no genera `tasks.md`.

## Summary

Añadir **Buscar** como acceso adicional en la raíz del addon. La UI abre el
teclado Kodi y navega a un directorio de hasta 100 canciones reproducibles que
coinciden por subcadena, sin distinguir capitalización, con el título editorial
`Artista - Canción` de todos los CSV locales. La búsqueda vive en `catalog`;
`kodi_plugin` solo solicita la query, construye URLs/listados y reutiliza el
resolver YouTube ya existente.

La función es independiente de Favoritos y se recomienda implementarla tras
`004-catalogo-60-70` (o con una semilla amplia), sobre la navegación por
décadas de `003`.

## Technical Context

**Language/Version**: Python 3 en runtime Kodi Matrix, Nexus, Omega y
posteriores; documentación y UI priorizan español.

**Primary Dependencies**: APIs Kodi existentes encapsuladas en
`kodi_plugin` (`xbmcgui`, `xbmcplugin`, `xbmcaddon`); reproducción existente
con `plugin.video.youtube`; sin dependencias nuevas.

**Storage**: CSV editorial existente en `resources/csv/YYYY.csv`; formato y
contenido sin cambios. No hay índice, base de datos ni caché persistente.

**Testing**: pytest para búsqueda pura, límite/orden/errores y modos/URLs del
plugin; smoke manual Kodi según [quickstart.md](./quickstart.md).

**Target Platform**: addon `plugin.video.gramolavideos` para Kodi moderno.

**Project Type**: plugin de vídeo Kodi con navegación por directorios.

**Performance Goals**: una búsqueda recorre como máximo aproximadamente 40 CSV
pequeños bajo demanda; los resultados se ordenan y limitan a 100 antes de
pintar la UI. La raíz y el browse cronológico no cargan todo el catálogo.

**Constraints**: ámbito exclusivamente `local_catalog`; subcadena
case-insensitive en título; query vacía/cancelada no lista el catálogo; sin
fuzzy, filtros, ranking, remoto ni dependencia de Favoritos; errores de CSV o
reproducción son recuperables y notificables.

**Scale/Scope**: ~40 años de catálogo 1960–1999; una carpeta raíz adicional,
dos modos (`search`, `search_results`), una función de datos, pruebas unitarias
y textos de UI extraíbles a i18n.

## Constitution Check

*GATE: aprobado antes de investigación y revalidado tras el diseño.*

From `.specify/memory/constitution.md` (La Gramola de Videos v1.3.0):

| Principio | Pre-diseño | Post-diseño |
|-----------|------------|-------------|
| **I. Catálogo como datos** | PASS | PASS — se leen CSV existentes; no se hardcodean canciones ni se escribe contenido. |
| **II. Reproducción vía YouTube** | PASS | PASS — cada resultado enlaza al mismo `mode=song` y resolver de YouTube. |
| **III. Alcance editorial** | PASS | PASS — no añade ni altera entradas. |
| **IV. Simplicidad del plugin** | PASS condicional | PASS — carpeta Buscar y exploración total justificadas en Complexity Tracking; el browse décadas→años→canciones se conserva. |
| **V. Metadatos y versionado** | PASS | PASS — al implementar, actualizar versión/changelog si el cambio de UX se publica. |
| **VI. Kodi moderna** | PASS | PASS — Python 3 y APIs Kodi existentes; no hay binarios ni librerías nuevas. |
| **VII. Desacoplamiento y APIs Kodi** | PASS | PASS — `catalog.search` no importa Kodi; teclado/listados viven en `kodi_plugin`. |
| **VIII. Tolerancia a fallos** | PASS | PASS — se acumulan fallos de carga y se muestran avisos sin abortar el directorio. |
| **IX. IA y secretos** | PASS | PASS — artefactos de planificación sin secretos ni tooling regenerable. |
| **X. Idioma e i18n** | PASS | PASS — documentación española; cadenas visibles centralizables y sin impedir futura localización. |

**Gate result**: PASS. No requiere enmienda de constitution.

## Project Structure

### Documentation (esta feature)

```text
specs/007-busqueda-catalogo/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   ├── catalog-search.md
│   └── plugin-navigation.md
└── checklists/
    └── requirements.md
```

`tasks.md` no se crea en esta fase.

### Source Code (previsto al implementar)

```text
addon.py
addon.xml
changelog.txt
resources/
├── csv/                         # fuente editorial sin cambios
├── language/                    # cadenas de Buscar/vacío, si se añaden
└── lib/
    ├── catalog.py               # search: recorrido, match, orden, límite
    ├── kodi_plugin.py           # raíz, teclado y modos de búsqueda
    ├── kodi_i18n.py
    └── kodi_notify.py
tests/
├── unit/
│   ├── test_catalog_search.py
│   ├── test_plugin_search.py
│   └── test_plugin_query_contract.py
└── stubs/                       # xbmc* para pruebas sin Kodi
```

**Structure Decision**: Extender el layout existente. La búsqueda de datos se
integra en `resources/lib/catalog.py`, que ya encapsula discovery y carga de
años; la navegación y la interacción Kodi permanecen en
`resources/lib/kodi_plugin.py`. No se crea módulo, servicio o almacenamiento
adicional.

## Diseño de implementación

1. Exponer `catalog.search(csv_dir, query, limit=100)` según
   [catalog-search.md](./contracts/catalog-search.md). Normalizar consulta,
   salir pronto si es vacía, iterar `list_years`/`load_year`, acumular errores,
   filtrar título con `casefold`, ordenar y limitar.
2. Añadir una factoría de etiqueta para resultados que preserve el título y
   muestre el año solo como contexto, y reutilice `song_listitem`/resolver
   para `video_id`.
3. En raíz, añadir la carpeta Buscar con `mode=search` sin quitar décadas ni
   acoplarla a Favoritos.
4. Implementar `mode=search`: abrir `xbmcgui.Dialog().input`, cancelar de
   forma silenciosa si no hay texto y navegar a `search_results` solo con
   query válida.
5. Implementar `mode=search_results`: validar `q`, llamar a `catalog.search`,
   notificar errores, crear canciones reproducibles y finalizar un directorio
   vacío con mensaje claro cuando no haya coincidencias.
6. Añadir localización o una ruta explícita de extracción para textos
   “Buscar”, vacío y límite si se muestran.
7. Actualizar README, versión y changelog al publicar la capacidad, como exige
   FR-011 y el principio V.

## Complexity Tracking

| Adición / decisión | Por qué se necesita | Alternativa más simple descartada |
|--------------------|---------------------|-----------------------------------|
| Carpeta raíz **Buscar** y modos `search` / `search_results` | Proporciona acceso directo desde mando a una canción cuando no se conoce el año, sin alterar el browse cronológico. | Dejar solo décadas/años obliga a recorrer el catálogo y no cumple FR-001/SC-001. |
| Escaneo completo bajo demanda con `list_years` + `load_year` | Las coincidencias pueden existir en cualquier CSV; ~40 archivos pequeños es un coste aceptable para una acción explícita. | Abrir un único año no satisface búsqueda de catálogo; índice/SQLite/caché añade estado, invalidación y complejidad sin necesidad demostrada. |
| Límite de 100 resultados ordenados | Mantiene un directorio manejable con mando y un orden determinista. | Sin límite puede saturar la UI; paginación, ranking o filtros aumentan alcance sin requerimiento MVP. |
