# Contract: Proceso de semilla 60/70

**Feature**: `004-catalogo-60-70`  
**Audience**: mantenedor / colaboradores (host), no runtime Kodi

## Invariantes

1. Salida = ficheros `resources/csv/YYYY.csv` con filas `título;video_id`.
2. MUST NOT ejecutarse como parte de `kodi_plugin.run` / navegación del oyente.
3. MUST NOT rehostear ni descargar ficheros de vídeo al repo.
4. Años sin filas aceptadas → no crear CSV vacío.

## Pasos mínimos (orden)

| Paso | Entrada | Salida | Hecho cuando |
|------|---------|--------|--------------|
| 1 Candidatos | Criterio editorial 60/70 ES | Lista año+título[+id] | ≥50 candidatos brutos recomendable (margena de rechazo) |
| 2 Ids | Candidatos | Filas con video_id | Id 11 chars o descarte |
| 3 Validación | Filas | Informe OK/KO | 100 % publicados pasan validador de catálogo |
| 4 Editorial | Filas OK formato | Subconjunto publicable | Checklist `editorial-review.md` |
| 5 Smoke | Muestra 5+5 | Log pass/fail | SC-004 (≥80 % o deuda listada) |
| 6 Publicar | Filas finales | CSV + README + versión | Umbrales FR-005/006 |

## Regeneración

El runbook (README o doc enlazado) MUST permitir repetir el proceso para ampliar
la base sin borrar 1980–1999.
