# Data Model: Auditoría y remediación

**Feature**: `001-auditoria-codigo`  
**Date**: 2026-07-25

## Entities

### Year

Clave de navegación del plugin.

| Field | Type | Rules |
|-------|------|--------|
| `id` | `str` | Nombre base del fichero CSV sin extensión; MUST ser exactamente 4 dígitos (`^\d{4}$`) para listarse. Ficheros que no cumplan se ignoran (no tumbar el listado). |
| `csv_path` | path | `resources/csv/{id}.csv` relativo al addon (o path absoluto resuelto en runtime). |

**Relationships**: Un `Year` tiene 0..N `MusicVideo` válidos tras la carga.

**State**: No hay máquina de estados; existe o no como fichero legible.

### MusicVideo

Entrada de catálogo reproducible.

| Field | Type | Rules |
|-------|------|--------|
| `title` | `str` | Campo 1 de la fila CSV; MUST no estar vacío tras strip. Formato editorial esperado: `Artista - Canción` (no se valida el guion de forma estricta en v1 de validación). |
| `video_id` | `str` | Campo 2; MUST coincidir con `^[A-Za-z0-9_-]{11}$`. |
| `year_id` | `str` | FK lógica al `Year.id` del que procede. |

**Relationships**: Pertenece a un `Year`.

### CatalogLoadResult

Resultado de una operación de carga (años o un año concreto).

| Field | Type | Rules |
|-------|------|--------|
| `years` | `list[Year]` | Solo presente en listado de años; ordenado ascendente por `id`. |
| `videos` | `list[MusicVideo]` | Solo presente en carga de un año; orden estable (caracterización: orden lexicográfico de tuplas como hoy, o documentar el orden post-fix). |
| `errors` | `list[CatalogError]` | Errores recuperables (I/O, parseo, validación). |
| `ok` | `bool` | `True` si hay al menos datos usables *o* la operación terminó sin aborto catastrófico; la UI decide notificación si `errors` no está vacío. |

### CatalogError

| Field | Type | Rules |
|-------|------|--------|
| `code` | enum-like `str` | p. ej. `year_unreadable`, `year_missing`, `row_invalid`, `row_bad_video_id`, `csv_dir_missing`. |
| `message` | `str` | Mensaje técnico interno (log); la UI mapea a texto amigable / i18n-ready. |
| `year_id` | `str \| None` | Año afectado si aplica. |
| `row` | `str \| None` | Contenido crudo de fila si aplica. |

### AuditFinding

Trazabilidad de la auditoría (documento de planificación; no es runtime del addon).

| Field | Type | Rules |
|-------|------|--------|
| `id` | `str` | Identificador estable (p. ej. `P1-compat`, `P1-chiquilla`). |
| `severity` | `P1` \| `P2` \| `P3` | Del inventario de la spec. |
| `current` | `str` | Comportamiento actual. |
| `desired` | `str` | Comportamiento deseado. |
| `remediation_phase` | `1` \| `2` \| `3` | Fase de este plan. |
| `status` | `open` \| `fixed` \| `deferred` \| `accepted` | SC-005. |

### DefaultBranch

Gobernanza del repositorio (no runtime).

| Field | Type | Rules |
|-------|------|--------|
| `name` | `str` | MUST ser `main` tras migración (FR-018). |
| `legacy_name` | `str` | `master`; no canónica (FR-020). |

## Validation rules (catalog)

1. Delimitador de fila: `;`.
2. Número de campos tras split: exactamente 2 (campos vacíos → inválido).
3. `video_id` válido: 11 caracteres `[A-Za-z0-9_-]`.
4. Entrada conocida inválida a eliminar/corregir: `1991.csv` → `Seguridad Social - Chiquilla;d3mZmP_me4`.
5. Directorio CSV ausente o vacío: `CatalogLoadResult` con error + lista de años vacía; notificación amigable; sin traceback no capturado hacia la UI.

## State transitions (plugin navigation)

```text
[plugin open] --mode=None--> list Years
     |
     +--mode=year&foldername=YYYY--> list MusicVideos for YYYY
            |
            +--mode=song&foldername=VIDEO_ID--> resolve play via YouTube URI
```

Caracterización (Fase 1) MUST fijar los nombres de query actuales (`mode`, `foldername`) salvo que Fase 2 documente un cambio de contrato UI y lo cubra con tests actualizados *después* de tener la red de seguridad.

## Mapping hallazgos → entidades / fases

| Finding | Entity / área | Phase |
|---------|---------------|-------|
| Runtime/APIs antiguas | Plugin runtime, `addon.xml` | 2 |
| Rutas frágiles | Year path resolution | 2 |
| CSV/filas sin aviso | `CatalogLoadResult`, `CatalogError` | 2 (tras 1) |
| Id inválido Chiquilla | `MusicVideo` + CSV | 2 |
| Monolito datos/UI | Year/MusicVideo vs kodi UI | 1 (extract mínima) + 3 (refactor) |
| Carga completa siempre | API Year list vs load year | 3 |
| Promesa 60s–90s | Editorial / metadata | 3 (o contenido; alinear mensaje) |
| `master` → `main` | `DefaultBranch` | 2 |
| Changelog/i18n/hygiene | Metadatos | 2–3 |
