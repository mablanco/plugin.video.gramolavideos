# Validation log — 002 alternativa YouTube

**Feature**: `002-alternativa-youtube`  
**Updated**: 2026-07-28

## Reframe (evidencia externa a esta feature)

| Fuente | Hallazgo |
|--------|----------|
| `specs/001-auditoria-codigo/validation-log.md` (smoke 2026-07-28) | Kodi 20.5 Nexus, `plugin.video.youtube` **7.4.x**: M1–M3 PASS **sin** API key en caso general. Algunos vídeos exigen **login** (p. ej. 1984 *La Unión - Eclipse total*). |

## Parte 1 — Documental (reframe)

| Check | Resultado | Fecha | Notas |
|-------|-----------|-------|-------|
| R-001 actualizado (API key vs login-wall) | PASS (docs) | 2026-07-28 | Veredicto documental → híbrido |
| Spec/plan/contracts alineados al smoke | PASS (docs) | 2026-07-28 | FR-012, C8, SC-003 |

## Parte 2 — Baseline YouTube

| Check | Resultado | Fecha | Notas |
|-------|-----------|-------|-------|
| Título OK sin login / sin API key | PASS (vía 001) | 2026-07-28 | Smoke M1 en 001 |
| Título login-wall observado | PASS | 2026-07-28 | Gramola → YouTube: `Please sign in` para `-owGOAjMjKk` (*Eclipse total*) |

## Parte 3 — Fallback SendToKodi (C8)

| Check | Resultado | Fecha | Notas |
|-------|-----------|-------|-------|
| Instalar SendToKodi sin cuenta YouTube | PASS | 2026-07-28 | `plugin.video.sendtokodi` **0.9.1094** (+ repo); yt-dlp 2026.07.04 y Deno v2.9.4 gestionados por el addon |
| Mismo `video_id` login-wall vía SendToKodi | **FAIL** | 2026-07-28 | `could not resolve url`. Log: yt-dlp `Private video. Sign in if you've been granted access` para `-owGOAjMjKk`. **No es un fallo de instalación**: el id del catálogo apunta a un vídeo privado; ni YouTube ni SendToKodi lo reproducen sin autenticación/cookies. |
| SendToKodi con un vídeo **público** del catálogo | **MIXED** | 2026-07-28 | *Lobo-hombre* `9qbxiPLVHNE`: (1) intento mal formado resolvió `-9qbxiPLVHN` → `Video unavailable`; (2) URI correcta: yt-dlp **sí resolvió** (DASH 720p + audio en `127.0.0.1:40215`) pero `Player.Open` falló con `OpenInputStream - error opening [plugin://plugin.video.sendtokodi/...]`. SendToKodi arranca; la integración vía `Player.Open`/plugin path no completa playback de forma fiable en esta prueba. |

## Veredicto operativo

- **choice**: `keep_youtube_mitigate` — ver [decision.md](./decision.md).
- **Híbrido SendToKodi**: **DESCARTADO** (2026-07-28, acuerdo mantenedor).
- **Siguiente**: (1) auditar/arreglar **todo** el catálogo; (2) mensajes claros
  ante privado / no disponible / sign-in; (3) sin segundo proveedor.
