# Quickstart: Validar el veredicto (híbrido / login-wall)

**Feature**: `002-alternativa-youtube`  
**Updated**: 2026-07-28

## Prerequisites

- Kodi Matrix / Nexus / Omega.
- `plugin.video.youtube` **7.4.x+** (o la versión smokeada sin API key).
- Posibilidad de instalar ZIP (SendToKodi) para la Parte 3.
- Referencia de smoke previo: `specs/001-auditoria-codigo/validation-log.md`.

## Parte 1 — Revisar el entregable (≤ 15 min)

1. Leer [research.md](./research.md) **R-001** y **R-004**.
2. Comprobar reframe: API key ya no es el motor; login-wall sí.
3. Comprobar veredicto **híbrido** y SC-003 (a)+(b).
4. Comprobar que rehost/descarga = incompatible.

## Parte 2 — Baseline YouTube (sin cuenta / sin API key)

1. Sin API key personal configurada (o instalación limpia del addon YouTube).
2. Reproducir desde Gramola un título del catálogo que **no** pida login → OK.
3. Reproducir (o intentar) un título con login-wall conocido, p. ej. 1984
   *La Unión - Eclipse total* → confirmar que pide login / no reproduce sin cuenta.

**Esperado**: C1 OK en (2); C8 fallido en (3) solo con YouTube.

## Parte 3 — Fallback yt-dlp (C8)

1. Instalar `plugin.video.sendtokodi` (ZIP/repo) **sin** iniciar sesión en el
   addon YouTube.
2. Resolver el **mismo** `video_id` del título con login-wall vía URI SendToKodi
   (watch URL). Ver [playback-provider.md](./contracts/playback-provider.md).
3. Anotar en [validation-log.md](./validation-log.md): reproduce / no reproduce /
   otro error.

### Criterio de salida hacia implementación híbrida

| Resultado Parte 3 | Acción |
|-------------------|--------|
| Reproduce sin login YouTube | Confirmar veredicto híbrido → enmienda II + feature implementación |
| No aporta | Plan B: solo YouTube + mensajes; diferir fallback |

## Parte 4 — Checklist mínima (≥ 3 pasos, SC-006)

- [ ] Título OK sin login vía YouTube 7.4.x+
- [ ] Título login-wall confirmado en YouTube
- [ ] Mismo título contrastado con fallback (o fallo documentado)

## References

- [decision-criteria.md](./contracts/decision-criteria.md)
- [data-model.md](./data-model.md)
- Código actual: `resources/lib/kodi_plugin.py`
