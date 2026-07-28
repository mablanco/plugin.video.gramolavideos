# Decision: Alternativa al addon de YouTube

**Feature**: `002-alternativa-youtube`  
**Date**: 2026-07-28  
**Status**: Cerrada (veredicto operativo)

## Resumen ejecutivo

Tras smoke en Kodi 20.5 + `plugin.video.youtube` 7.4.x y pruebas con
SendToKodi: **se descarta** sustituir o complementar YouTube con un híbrido
yt-dlp. Se mantiene YouTube como único proveedor. El trabajo útil es **higiene
de catálogo** (todos los ids) y **mensajes más claros** cuando un vídeo no sea
reproducible (privado / no disponible / pide cuenta).

## Hallazgos

| Hallazgo | Evidencia |
|----------|-----------|
| API key no es el bloqueo principal | Smoke 001, YouTube 7.4.x |
| Fallos observados = restricciones reales del vídeo | *Eclipse total* privado; YouTube “Please sign in” |
| SendToKodi no salta privados | yt-dlp: `Private video` |
| Integración SendToKodi poco fiable para Gramola | Resolve OK a veces; `Player.Open` / carpeta vacía |

## Veredicto

- **choice**: `keep_youtube_mitigate`
- **api_key_required_happy_path**: `no` (7.4.x+)
- **login_wall_bypass_attempt**: `no` (descartado a propósito)
- **constitution_amendment_required**: `false` (no se añade segundo proveedor)
- **hybrid SendToKodi**: **DESCARTADO**

## Plan de acción acordado

1. Auditar y arreglar **todo** el catálogo CSV (ids privados/no disponibles).
2. Mejorar mensajes cuando la reproducción no sea posible (sign-in / no disponible).
3. No implementar fallback SendToKodi ni enmienda de constitution II por este motivo.

Detalle de smoke: [validation-log.md](./validation-log.md).
