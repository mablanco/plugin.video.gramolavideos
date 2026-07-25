# Research: Auditoría y remediación incremental

**Feature**: `001-auditoria-codigo`  
**Date**: 2026-07-25

## R-001: Estrategia de remediación en 3 fases

**Decision**: Ejecutar la remediación en tres fases consecutivas e irreversibles en orden: (1) tests de caracterización, (2) bugs críticos / compatibilidad, (3) refactor y deuda técnica. No se avanza de fase hasta que la anterior tenga criterios de salida verificables.

**Rationale**: La constitution (IX) exige evolución sobre el addon existente, no reescritura. El código actual es un monolito Python 2 en `addon.py` sin tests; tocar bugs o arquitectura sin red de seguridad viola el espíritu de VII y aumenta el riesgo de regresiones silenciosas en el flujo años → canciones → YouTube (IV).

**Alternatives considered**:
- Refactor primero y tests después — rechazado: no hay baseline de comportamiento.
- Big-bang rewrite bajo otro addon id / scaffold `plugin.video.gramola` — rechazado por FR-012a / SC-009 y veredicto de andamiaje.
- Corregir bugs P1 sin caracterización — rechazado: mezcla corrección con cambio de contrato implícito.

## R-002: Cómo caracterizar código acoplado a `xbmc*`

**Decision**: En Fase 1, introducir un harness de tests con stubs mínimos de `xbmc`, `xbmcgui`, `xbmcplugin` (y `xbmcaddon` si hace falta) más una extracción *literal* (move, sin cambio de semántica) de la lectura/parseo CSV a un módulo puro bajo `resources/lib/` (p. ej. `catalog.py`). Los tests de caracterización fijan: años descubiertos, ordenación, forma de filas actuales (incluye filas inválidas *tal cual* se cargan hoy), y el contrato de query `mode`/`foldername`.

**Rationale**: `addon.py` ejecuta I/O y UI al import/nivel de módulo; no es importable sin Kodi. La extracción mínima de datos es el único camino pragmático para “congelar comportamiento” sin lanzar Kodi, alineado con constitution VII y FR-004/FR-005. No es el refactor completo (eso es Fase 3): es el mínimo para poder observar.

**Alternatives considered**:
- Solo mocks sin extracción — rechazado: el side-effect al import hace frágil el harness.
- Tests solo manuales en Kodi — rechazado: no cumple SC-003 ni habilita remediación segura.
- Copiar lógica de parseo al test (duplicar) — rechazado: drift inmediato.

## R-003: Stack de testing

**Decision**: `pytest` sobre el host (Python 3.x del mantenedor), con fixtures de CSV temporales. Sin dependencias binarias. Tests de reproducción end-to-end siguen siendo manuales en Kodi + `plugin.video.youtube` (asumido en la spec).

**Rationale**: Estándar de facto en Python; no requiere runtime de Kodi para lógica de catálogo; compatible con “MUST NOT introducir libs binarias ajenas” (VI) porque pytest es tooling de desarrollo, no dependencia del addon en `addon.xml`.

**Alternatives considered**:
- `unittest` solo — viable pero menos ergonómico para fixtures CSV.
- Framework de tests de Kodi (xbmcswift-style) — overkill / YAGNI (IV, FR-012).

## R-004: Migración Python 2 → Python 3 / Kodi Matrix+

**Decision**: En Fase 2, actualizar `addon.xml` (`xbmc.python` a versión Matrix+, p. ej. `3.0.0`), reemplazar `urllib`/`urlparse` por `urllib.parse`, abrir CSV en texto con encoding UTF-8, eliminar `.decode('utf-8')` sobre paths, usar APIs de `ListItem` modernas (sin `iconImage`/`thumbnailImage` deprecados), y resolver rutas vía `xbmcaddon.Addon().getAddonInfo('path')` (o equivalente encapsulado) en lugar de hardcodear `special://home/addons/<id>/...`.

**Rationale**: Hallazgo P1 de auditoría; constitution VI marca destino Matrix/Nexus/Omega+; el código actual declara `xbmc.python` `2.25.0` y usa APIs Py2.

**Alternatives considered**:
- Mantener dual Py2/Py3 — rechazado: coste sin beneficio; Kodi moderno es Py3.
- Esperar a Fase 3 — rechazado: sin esto el addon puede no arrancar (P1).

## R-005: Reproducción e historial de directorio

**Decision**: En Fase 2, alinear la acción `mode=song` con el patrón de pluginsource de Kodi: construir el item reproducible y usar `xbmcplugin.setResolvedUrl` (o el equivalente encapsulado en la fachada Kodi) en lugar de `xbmc.Player().play(...)` directo cuando se llega desde un listado de directorio. Mantener la URI `plugin://plugin.video.youtube/play/?video_id=...`.

**Rationale**: Spec (flujo reproducción / historial); `Player().play` desde un pluginsource desacopla el item del handle del plugin y degrada historial/contexto.

**Alternatives considered**:
- Dejar `Player().play` — rechazado: incompatibilidad de UX con listados modernos.
- Rehostear/stream propio — rechazado por constitution II.

## R-006: Validación de filas e id de YouTube

**Decision**: Validar filas como `title;video_id` con título no vacío e id que cumpla el formato canónico de YouTube video id (11 caracteres `[A-Za-z0-9_-]`). Filas inválidas se omiten del listado y se acumulan en un resultado de carga (`CatalogLoadResult`) para aviso. Corregir o eliminar la entrada conocida `Seguridad Social - Chiquilla;d3mZmP_me4` (10 caracteres) en Fase 2 (datos) o como fix de catálogo acoplado a la validación.

**Rationale**: FR-007, SC-006, hallazgo P1; el id actual es obviamente inválido.

**Alternatives considered**:
- Solo longitud sin charset — más débil, acepta basura.
- Fallar todo el año si hay una fila mala — rechazado por constitution VIII / FR-006.

## R-007: Layout objetivo (ideas del andamiaje, sin fusionar)

**Decision**: Adoptar solo las tres ideas aprobadas en la spec: (1) entry point fino `addon.py` + `resources/lib/` con módulos `kodi*` vs lógica de catálogo sin prefijo kodi; (2) helper de notificación ante errores recuperables; (3) esqueleto `resources/language/` cuando se toquen cadenas. **No** adoptar `script.module.routing`, settings de debug de plantilla, ni el id/metadatos del scaffold.

**Rationale**: FR-012a/b, SC-009, constitution IV/VII/VIII/X.

**Alternatives considered**:
- Fusionar `plugin.video.gramola` — rechazado explícitamente.
- Routing externo — YAGNI para años → canciones.

## R-008: Carga selectiva de catálogo

**Decision**: Diferir la optimización de carga lazy (listar años sin leer todos los CSV; cargar un año solo) a Fase 3, pero diseñar la API de catálogo en Fase 1/2 (`list_years(csv_dir)`, `load_year(csv_dir, year)`) para que Fase 3 solo cambie la implementación, no el contrato.

**Rationale**: FR-008/009 y deuda del README son P2; primero seguridad y bugs. Diseñar la API evita un segundo quiebre de interfaz.

**Alternatives considered**:
- Optimizar en Fase 2 junto a bugs — aumenta superficie de cambio en la fase de estabilidad.
- Caché en disco/JSON — overkill (IV).

## R-009: Miniaturas y transporte

**Decision**: Usar HTTPS para thumbnails de YouTube (`https://img.youtube.com/vi/<id>/...`). Un fallo de imagen no debe impedir el listado (ListItem usable sin thumb).

**Rationale**: Hallazgo de auditoría (URL insegura); constitution VIII.

**Alternatives considered**:
- Eliminar miniaturas — peor UX sin ganancia suficiente.
- Descargar y cachear localmente — complejidad injustificada.

## R-010: Rama por defecto `master` → `main`

**Decision**: Migrar en Fase 2 (higiene P2 pero acoplada a remediación): crear/renombrar a `main`, cambiar default branch en GitHub, actualizar changelog/README/enlaces `commits/master` → `main`, documentar forks. No bloquea tests de caracterización.

**Rationale**: FR-018–020, SC-008; no hay CI/protección que dependa de `master` según assumptions de la spec.

**Alternatives considered**:
- Dejar `master` — rechazado por requisitos de la feature.
- Hacerlo en Fase 3 — posible, pero conviene cerrarlo antes de PRs de refactor largos.

## R-011: Content type y metadatos de listado

**Decision**: Usar un content type adecuado a vídeos musicales (p. ej. `musicvideos` o el valor soportado por el target Kodi documentado en implementación) en lugar de `movies`. Ajustar en Fase 2 junto a APIs de ListItem.

**Rationale**: Hallazgo P2 de clasificación; bajo coste si se toca la capa Kodi.

**Alternatives considered**:
- Dejar `movies` — aceptable temporalmente pero incorrecto semánticamente.

## R-012: Typing y limpieza

**Decision**: En Fase 3, añadir type hints graduales en módulos de `resources/lib/` (Python 3), sin `mypy` estricto como puerta de CI en este incremento salvo que el mantenedor lo pida después. Eliminar código muerto y literales de UI sin ruta i18n cuando se toquen.

**Rationale**: Mejora mantenibilidad sin hinchar el alcance de Fase 2; constitution IV.

**Alternatives considered**:
- Typing estricto + CI mypy ahora — prematuro para un addon pequeño en remediación.

## Resolución de NEEDS CLARIFICATION

No quedan ítems NEEDS CLARIFICATION abiertos: el destino Kodi/Python 3, el rechazo del scaffold, el formato CSV, y el orden de fases vienen fijados por spec + constitution + input del usuario.
