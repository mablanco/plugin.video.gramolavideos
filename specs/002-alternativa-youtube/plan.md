# Implementation Plan: Alternativa al addon de YouTube

**Branch**: `002-alternativa-youtube` (artefactos; trabajo actual puede estar en otras ramas) | **Date**: 2026-07-25 | **Updated**: 2026-07-28 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/002-alternativa-youtube/spec.md` +
hallazgo de smoke en `specs/001-auditoria-codigo/validation-log.md`.

**Note**: Feature de **análisis y decisión** (FR-010). No cambia el código de
reproducción aquí.

## Summary

Tras smoke y acuerdo del mantenedor (2026-07-28): **mantener solo**
`plugin.video.youtube`; **descartar** híbrido SendToKodi. Acciones
ejecutadas/derivadas: auditoría oEmbed de todo el catálogo, sustitución de ids
privados/no disponibles, y mensajes claros ante bloqueo de reproducción.


## Technical Context

**Language/Version**: Documentación en español; sin cambio de código en esta
feature. Validación: Kodi Nexus/Matrix+/Omega, YouTube 7.4.x+.

**Primary Dependencies** (producto actual): `plugin.video.youtube`.  
**Candidato fallback**: `plugin.video.sendtokodi` (yt-dlp).  
**Descartada como primaria**: sustitución total; Tubed.

**Storage**: CSV sin cambio.

**Testing**: Revisión documental + smoke híbrido (quickstart). Sin pytest nuevo.

**Target Platform**: `plugin.video.gramolavideos` (cadena de reproducción).

**Project Type**: Estudio de viabilidad / decisión de producto.

**Performance Goals**: N/A análisis.

**Constraints**: No rehost; no implementar aquí; enmendar constitution II antes
de añadir segundo proveedor; ToS del fallback = riesgo explícito.

**Scale/Scope**: 1 veredicto híbrido; ≥3 opciones; borrador de enmienda;
checklist con título OK + título login-wall; 0 cambios de runtime aquí.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

From `.specify/memory/constitution.md` (La Gramola de Videos v1.2.1):

| Principle | Pre-design | Post-design (Phase 1 / reframe) |
|-----------|------------|----------------------------------|
| **I. Catálogo como datos** | PASS | PASS |
| **II. Reproducción vía YouTube** | PASS para esta feature (sin código); veredicto híbrido **planea** ampliar II | PASS condicional — enmienda obligatoria antes de implementar fallback; Complexity Tracking |
| **III–I, IV–X** | PASS (sin cambio de producto runtime) | PASS |

**Gate result**: PASS para análisis. Violación futura de II (segundo proveedor)
justificada abajo.

## Project Structure

### Documentation (this feature)

```text
specs/002-alternativa-youtube/
├── plan.md
├── research.md             # R-001 reframe + veredicto híbrido
├── data-model.md
├── quickstart.md           # smoke YouTube OK + login-wall + fallback
├── validation-log.md       # registro del reframe / smokes 002
├── contracts/
│   ├── decision-criteria.md
│   ├── playback-provider.md
│   └── constitution-amendment-draft.md
├── checklists/
└── tasks.md
```

**Structure Decision**: Solo artefactos bajo `specs/002-alternativa-youtube/`.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Ampliar principio II (segundo proveedor / fallback) | Login-wall en ciertos vídeos del catálogo tras smoke; YouTube solo no cubre C8 | Sustituir YouTube por completo — innecesario: 7.4.x ya va bien sin API key. Solo mensajes — no intenta reproducir esos títulos |
| Dependencia ZIP yt-dlp | Única vía práctica evaluada para C8 parcial | Embeber yt-dlp en Gramola — viola IV / identidad índice |
