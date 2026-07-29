# Data Model: Semilla 60s/70s

**Feature**: `004-catalogo-60-70`  
**Date**: 2026-07-29

Reutiliza el modelo de catálogo existente; añade entidades de proceso.

## Entities

### Year / MusicVideo (existente)

| Campo | Descripción | Validación |
|-------|-------------|------------|
| Year.id | `YYYY` 1960–1979 para esta feature | CSV presente solo si hay filas |
| MusicVideo.title | `Artista - Canción` | No vacío; patrón editorial |
| MusicVideo.video_id | Id YouTube 11 chars | `VIDEO_ID_RE`; único por año |

### SeedCandidate

Propuesta pre-publicación.

| Campo | Descripción |
|-------|-------------|
| year_id | Año objetivo |
| title | Título propuesto |
| video_id | Id propuesto o vacío si pendiente |
| editorial_ok | bool tras revisión |
| format_ok | bool tras validación mecánica |
| notes | Motivo de rechazo / deuda smoke |

### SeedBatch

| Campo | Descripción |
|-------|-------------|
| decade_coverage | flags 60s / 70s |
| entry_count | filas publicables |
| year_count | años distintos con ≥1 fila |
| smoke_sample | lista de ids muestreados + resultado |

### PublishedSeed

Estado “listo” cuando:

- `entry_count >= 40`
- `year_count >= 8`
- ambas décadas con ≥1 año
- 0 filas con `format_ok=false` en lo publicado
- checklist editorial firmada (mantenedor)

## Relationships

SeedCandidate → (aceptado) → MusicVideo en Year CSV.  
SeedBatch agrega candidatos; PublishedSeed es el umbral de aceptación del batch.
