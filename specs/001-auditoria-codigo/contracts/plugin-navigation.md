# Contract: Navegación del plugin (UI / query)

**Feature**: `001-auditoria-codigo`  
**Audience**: capa `resources/lib/kodi_*.py` + `addon.py`  
**Status**: **Histórico** — superseded by
`specs/003-navegacion-videos/contracts/plugin-navigation.md` (raíz = décadas,
`mode=decade`). Conservar este documento como baseline de la navegación plana.

## Flujo

Preservar constitution IV / FR-001 *(texto de 001; el runtime actual sigue el
contrato 003)*:

1. Sin `mode` (o `mode` ausente): listar años (directorios).
2. `mode=year` + `foldername=<YYYY>`: listar canciones del año (items reproducibles).
3. `mode=song` + `foldername=<video_id>`: resolver reproducción vía YouTube.

## Query string

| Param | Values | Notes |
|-------|--------|-------|
| `mode` | omitido \| `year` \| `song` | Caracterización: el código actual usa `args.get('mode', None)` y compara `mode[0]`. |
| `foldername` | año o `video_id` | Nombre legacy; no renombrar en Fase 1–2 salvo necesidad fuerte (YAGNI). |

## Reproducción

- URI: `plugin://plugin.video.youtube/play/?video_id=<id>`
- MUST NOT descargar/rehostear (constitution II).
- Integración con handle del plugin: `setResolvedUrl` (o fachada) tras Fase 2.

## Errores recuperables (UI)

- Si `CatalogLoadResult.errors` no vacío: mostrar notificación amigable (helper acotado).
- MUST NOT abortar el listado residual usable (FR-006).

## Content / ListItem

- Content type: preferir vídeos musicales (no `movies`) tras Fase 2.
- Thumbnails: HTTPS; fallo de imagen no bloquea el item.
- Cadenas nuevas: centralizadas / preparadas para `resources/language/` (FR-015).
