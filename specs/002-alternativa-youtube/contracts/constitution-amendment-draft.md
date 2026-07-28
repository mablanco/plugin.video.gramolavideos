# Contract: Borrador de enmienda a la constitution (principio II)

**Feature**: `002-alternativa-youtube`  
**Updated**: 2026-07-28  
**Applies when**: Se confirme el veredicto híbrido (YouTube + fallback) o
cualquier proveedor adicional.  
**Must be merged before**: PR que añada segundo proveedor o cambie la URI de play.

## Current text (v1.2.1) — extracto

> ### II. Reproducción vía YouTube  
> La reproducción MUST delegarse a `plugin.video.youtube` …

## Proposed replacement (draft)

### II. Reproducción de vídeos de YouTube (sin rehost)

La reproducción MUST delegarse a uno o más **proveedores externos de Kodi**
capaces de reproducir el vídeo de YouTube identificado por el
`youtube_video_id` del catálogo. El addon MUST NOT descargar, almacenar ni
rehostear ficheros de vídeo.

MUST haber un **proveedor por defecto** declarado en `addon.xml` / README.
MAY existir un **proveedor de respaldo** (fallback) para mejorar usabilidad
cuando el proveedor por defecto exija login de cuenta u falle la resolución
en títulos concretos del catálogo. El fallback MUST documentarse (instalación
incluida si no está en el repo oficial) y MUST NOT usarse para rehostear.

Históricamente el único proveedor fue `plugin.video.youtube`. En instalaciones
modernas (p. ej. 7.4.x+) ese addon suele funcionar **sin API key** en el
recorrido mayoritario; el dolor residual conocido es el **login selectivo**.
Un fallback basado en resolución yt-dlp MAY adoptarse para intentar esos casos,
con riesgos ToS/roturas documentados y **sin** garantizar cobertura total.

Las miniaturas MAY seguir obteniéndose de URLs públicas de YouTube.

## Accompanying edits (checklist for the amendment PR)

- [ ] Actualizar **Restricciones técnicas** (permitir default + optional fallback).
- [ ] Bump constitution **MINOR** (p. ej. 1.2.x → 1.3.0).
- [ ] `Last Amended` = fecha ISO.
- [ ] Revisar plantillas Speckit que citen II de forma rígida.
- [ ] No introducir secretos ni claves de ejemplo reales.

## Non-amendment path

Si el smoke del fallback no aporta C8: **no** aplicar este borrador; solo
mejorar mensajes bajo II vigente.
