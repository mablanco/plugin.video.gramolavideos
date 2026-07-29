# Contract: Revisión editorial de semilla

**Feature**: `004-catalogo-60-70`

Cada candidato MUST pasar antes de publicar:

| # | Comprobación | Rechazar si |
|---|--------------|-------------|
| E1 | Artista/banda española (o justificación explícita en nota de cambio) | Acto claramente extranjero sin vínculo editorial |
| E2 | Vídeo musical / actuación de la época (60s o 70s según año asignado) | Contenido ajeno (sketch, unrelated) |
| E3 | Título `Artista - Canción` | Formato distinto o basura |
| E4 | `video_id` forma válida | No cumple patrón de 11 chars |
| E5 | No duplicar mismo `video_id` en el mismo año | Duplicado intra-año |
| E6 | Año coherente con la canción (aprox.) | Año inventado sin criterio |

**Firma**: el mantenedor confirma el batch en el mensaje de commit / PR.

**Fuera de esta checklist**: exhaustividad discográfica; calidad audiovisual
perfecta; ausencia total de login-wall (se gestiona en smoke / deuda).
