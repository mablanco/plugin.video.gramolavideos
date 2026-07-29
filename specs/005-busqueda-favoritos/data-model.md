# Data Model: Empaquetado (conceptual)

**Feature**: `005-busqueda-favoritos`  
**Date**: 2026-07-29

Modelo para el **análisis**; no implica schema implementado en esta feature.

## Entities

### CatalogEntry (existente, vista lógica)

| Campo | Descripción |
|-------|-------------|
| year_id | Año del CSV |
| title | `Artista - Canción` |
| video_id | Id reproducción |

### SearchCapability (perfil de producto)

| Campo | Descripción |
|-------|-------------|
| query_scope | `local_catalog` |
| match_fields | título (artista + canción) |
| empty_behavior | listado vacío + mensaje claro |
| out_of_scope | remoto, filtros avanzados |

### FavoritesCapability (perfil de producto)

| Campo | Descripción |
|-------|-------------|
| storage_scope | `per_install_or_profile` |
| actions | add / list / remove |
| orphan_policy | `hide_or_notify` (a fijar en spec futura) |
| out_of_scope | multi-listas, nube |

### PackagingVerdict

| Campo | Descripción |
|-------|-------------|
| strategy | `single_feature` \| `two_features` |
| chosen | `two_features` |
| order | `[favorites, search]` |
| next_specify | nombres sugeridos |

## Relationships

FavoritesCapability referencia CatalogEntry (no la sustituye).  
SearchCapability consulta el conjunto de CatalogEntry.  
No hay relación de datos obligatoria entre Favorites y Search.
