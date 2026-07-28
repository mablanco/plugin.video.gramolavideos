# Contract: Proveedor de reproducción (actual vs híbrido recomendado)

**Feature**: `002-alternativa-youtube`  
**Updated**: 2026-07-28  
**Status**: Contrato de **intención**; el código vigente aún solo usa YouTube.

## Current (shipped)

| Aspect | Value |
|--------|-------|
| Provider id | `plugin.video.youtube` |
| Declared in | `addon.xml` `<requires>` |
| Resolve URI | `plugin://plugin.video.youtube/play/?video_id={video_id}` |
| Code locus | `resources/lib/kodi_plugin.py` |
| Thumbnails | `https://img.youtube.com/vi/{video_id}/0.jpg` |
| User friction (7.4.x+, smoke 2026-07-28) | **Sin API key** en recorrido mayoritario; **login de cuenta** en *ciertos* vídeos |

### Error UX (mitigación si no hay fallback)

- Aviso comprensible si un título pide cuenta YouTube.
- No presentar el fallo como “bug de Gramola” cuando es restricción del proveedor.

## Recommended future — híbrido

| Role | Provider | Notes |
|------|----------|-------|
| Default | `plugin.video.youtube` ≥ 7.4.x | Caso general validado en smoke |
| Fallback (C8) | `plugin.video.sendtokodi` | URI con watch URL del mismo `video_id` |
| Catalog | Sin cambio CSV | |
| Thumbnails | Sin cambio | |

### Resolve behavior (intención)

1. Intentar YouTube (comportamiento actual).
2. Ante login-wall / fallo de resolución elegible: usar fallback yt-dlp **o**
   ofrecer acción explícita “reproducir con proveedor alternativo”
   (detalle UX en feature de implementación).
3. Si falta el fallback: mensaje con pista de instalación + mención de login.

### Error UX (híbrido)

| Situación | Comportamiento esperado |
|-----------|-------------------------|
| Vídeo OK en YouTube sin login | Reproduce por defecto |
| Login-wall + fallback instalado | Intenta / ofrece fallback; sin pedir API key |
| Login-wall + fallback ausente | Aviso: cuenta YouTube **o** instalar fallback |
| Fallback no puede el título | Aviso honesto: no disponible por esta vía |
| Rehost/descarga | **Fuera de contrato** |

### Explicitly out of contract

- Descargar vídeo a disco desde la gramola.
- Prometer cobertura 100% de login-wall.
- Embebido de yt-dlp dentro de Gramola.

## Backup path

Si el smoke del fallback **no** mejora C8: permanecer en **Current** +
mensajes; no añadir dependencia ZIP.
