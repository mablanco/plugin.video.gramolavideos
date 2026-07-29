# Data Model: Navegación por décadas

**Feature**: `003-navegacion-videos`  
**Date**: 2026-07-29

Sin nuevo almacenamiento. Entidades de presentación derivadas del catálogo.

## Entities

### Year (existente)

| Campo | Descripción | Validación |
|-------|-------------|------------|
| id | Stem `YYYY` del CSV | `^\d{4}$`; fichero presente en `resources/csv/` |

### MusicVideo (existente)

Sin cambio. Pertenece a un Year.

### Decade (nuevo, derivado)

| Campo | Descripción | Validación |
|-------|-------------|------------|
| id | Año de inicio de década (p. ej. `1980`) | `id % 10 == 0`; `id == (year_id // 10) * 10` |
| label_key | Clave i18n / etiqueta ES por defecto (`Años 80`) | Derivada de `id` (década = id/10 % 10 para 1900–1999; regla documentada en contrato) |
| years | Lista de Year.id en `[id, id+9]` presentes en catálogo | No vacía al listar la década |

Relación: Decade 1—* Year 1—* MusicVideo.

### NavigationLevel

| Valor | Significado |
|-------|-------------|
| `root` | Listado de Decade |
| `decade` | Listado de Year de una Decade |
| `year` | Listado de MusicVideo |
| `song` | Resolve reproducción |

## Validation rules

- No crear Decade sin al menos un Year real.
- No crear Year vacío en UI (sigue FR catálogo: sin CSV → no aparece).
- Todo Year del catálogo MUST ser alcanzable vía exactamente una Decade (SC-004).

## State / transitions (UI)

`root` → `decade` → `year` → (play). Atrás invierte la pila.
