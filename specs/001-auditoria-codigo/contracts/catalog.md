# Contract: Catálogo (lógica de datos)

**Feature**: `001-auditoria-codigo`  
**Audience**: mantenedores / tests sin Kodi  
**Module target**: `resources/lib/catalog.py` (nombre orientativo)

## Purpose

Contrato estable de lectura y validación del catálogo CSV, independiente de `xbmc*`.

## Functions

### `list_years(csv_dir: str | Path) -> CatalogLoadResult`

- **Input**: directorio que contiene `*.csv`.
- **Behavior**:
  - Incluye solo ficheros cuyo stem es un año de 4 dígitos.
  - No MUST materializar el contenido de las canciones (FR-008; obligatorio tras Fase 3; en Fases 1–2 puede aún leer ficheros si la implementación legacy lo hace, pero el contrato de *retorno* no expone vídeos).
  - Ordena `years` ascendente por `id`.
  - Si `csv_dir` no existe: `errors` con `csv_dir_missing`, `years=[]`.
- **Output**: `CatalogLoadResult` con `years` y `errors`.

### `load_year(csv_dir: str | Path, year_id: str) -> CatalogLoadResult`

- **Input**: directorio CSV + `year_id`.
- **Behavior**:
  - Lee únicamente `{year_id}.csv` (FR-009 tras Fase 3; en caracterización puede documentarse el comportamiento legacy si aún carga todo).
  - Parsea filas `title;video_id`.
  - Omite filas inválidas; añade `CatalogError` por cada una (o agregadas por tipo — documentar en implementación).
  - No lanza hacia el caller por filas malas; solo por bugs de programación.
- **Output**: `CatalogLoadResult` con `videos` válidos y `errors`.

### Validación de fila

| Condición | Resultado |
|-----------|-----------|
| ≠ 2 campos | inválida → error `row_invalid` |
| title vacío | inválida → error `row_invalid` |
| video_id no `^[A-Za-z0-9_-]{11}$` | inválida → error `row_bad_video_id` |
| OK | `MusicVideo` |

## Characterization vs post-fix

| Aspecto | Fase 1 (freeze) | Fase 2+ (deseado) |
|---------|-----------------|-------------------|
| Filas con id corto | Se cargan si el parser legacy no valida | Se omiten + error |
| Carga de todos los CSV al listar años | Puede coincidir con legacy | Prohibido materializar vídeos |
| Encoding | Documentar comportamiento actual del extract | UTF-8 texto |

Los tests de caracterización MUST etiquetarse claramente; al cambiar a comportamiento deseado en Fase 2, se actualizan assertions de validación *después* de tener la suite verde en el freeze.
