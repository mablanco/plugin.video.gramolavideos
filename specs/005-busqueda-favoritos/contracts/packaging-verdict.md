# Contract: Veredicto de empaquetado

**Feature**: `005-busqueda-favoritos`

## Resultado normativo de este estudio

```text
strategy: two_features
order: favorites -> search
implements_runtime_in_005: false
```

## Feature futura — Favoritos

| Campo | Valor |
|-------|-------|
| suggested_short_name | `favoritos-usuario` |
| depends_on_003 | no (convive con raíz años o décadas) |
| depends_on_004 | no |
| catalog_role | preferencias usuario |

## Feature futura — Búsqueda

| Campo | Valor |
|-------|-------|
| suggested_short_name | `busqueda-catalogo` |
| depends_on_003 | no estricta |
| depends_on_004 | recomendada (más valor) |
| catalog_role | consulta del catálogo editorial |

## Prohibiciones

- MUST NOT tratar esta feature 005 como implementación de UI.
- MUST NOT fusionar favoritos dentro del CSV editorial.
- MUST NOT requerir cuenta online para el MVP conceptual de favoritos.
