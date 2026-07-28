# Data Model: Decisión de proveedor de reproducción

**Feature**: `002-alternativa-youtube`  
**Date**: 2026-07-25

Este modelo describe las entidades del **análisis/decisión**, no un esquema de
persistencia nuevo. El catálogo de canciones no cambia.

## Entities

### Year / MusicVideo (catálogo existente — sin cambio)

| Campo | Descripción | Validación |
|-------|-------------|------------|
| Year.id | Año como clave de listado (nombre CSV) | Existente |
| MusicVideo.title | `Artista - Canción` | Existente |
| MusicVideo.video_id | Id de vídeo de YouTube (11 chars) | Existente; fuente de verdad del contenido |

Relación: Year 1—* MusicVideo.

### PlaybackProvider

Representa un componente externo de Kodi que convierte `video_id` en reproducción.

| Campo | Descripción |
|-------|-------------|
| id | Identificador estable (p. ej. `plugin.video.youtube`, `plugin.video.sendtokodi`, `plugin.video.tubed`) |
| display_name | Nombre legible |
| requires_api_key | bool — si el usuario final necesita claves de desarrollador |
| install_channel | `official_repo` \| `third_party_repo` \| `zip` |
| play_uri_template | Plantilla para construir la URI de resolve a partir de `video_id` |
| rehosts_or_downloads | bool — si la opción implica almacenar vídeo (incompatible si true como solución) |
| maturity | `stable` \| `mixed` \| `early` |
| notes | Riesgos ToS, cuotas, mantenimiento |

### EvaluatedOption

Una fila de la comparativa (FR-001 / SC-002).

| Campo | Descripción |
|-------|-------------|
| option_id | `A`…`F` (ver research) |
| provider | PlaybackProvider o `n/a` (mitigaciones / rechazadas) |
| scores | Mapa criterio → `bien` \| `medio` \| `mal` \| `incompatible` |
| result | `recommended` \| `backup` \| `rejected` \| `incompatible` |
| rationale | Texto corto |

### FrictionProfile

Describe el recorrido del usuario inexperto hasta la primera reproducción.

| Campo | Descripción |
|-------|-------------|
| non_automatic_steps | Lista ordenada de pasos manuales |
| requires_developer_console | bool |
| estimated_step_count | Entero (≥ 0) |
| failure_hints | Mensajes esperados si falta proveedor / vídeo |

### Verdict

Decisión final (FR-003).

| Campo | Descripción |
|-------|-------------|
| choice | `hybrid_youtube_plus_ytdlp_fallback` (recomendado) \| `keep_youtube_mitigate` (plan B) \| `replace_with_ytdlp` (no preferido post-smoke) \| `defer` |
| api_key_required_happy_path | **`no`** tras smoke YouTube 7.4.x+ |
| login_wall_bypass_attempt | `yes` \| `no` \| `partial` — **`partial`** vía fallback yt-dlp |
| constitution_amendment_required | bool — **true** si se añade fallback o se cambia II |
| implementation_in_this_feature | **false** (FR-010) |
| next_steps | Lista (smoke C8 → enmendar II → feature implementación híbrida) |
| residual_risks | Cobertura parcial login-wall, ToS, ZIP |

### DecisionCriteria

Criterios congelados C1–C8 (research R-002). No son mutables sin actualizar
research + contracts.

### LoginWall

Evento de reproducción en el que el proveedor por defecto exige autenticación
de cuenta para un `MusicVideo` concreto.

## State transitions (análisis)

```text
[Draft analysis]
      │
      ▼
[Options scored] ──► [Verdict draft]
      │                     │
      │                     ▼
      │              [Smoke pending / done]
      │                     │
      └─────────────────────► [Verdict published]
                                │
                    ┌───────────┴───────────┐
                    ▼                       ▼
        [Amend constitution II]    [Plan B: mitigate YouTube]
                    │
                    ▼
        [Future hybrid implementation]
```

## Invariants

1. Ningún Verdict recomendado puede tener `rehosts_or_downloads = true`.
2. Todo Verdict que añada fallback o deje de ser “solo YouTube” debe marcar
   `constitution_amendment_required = true` mientras II cite solo
   `plugin.video.youtube`.
3. `MusicVideo.video_id` permanece como id de YouTube aunque haya fallback.
4. Esta feature no altera entidades de runtime del addon.
5. No se promete cobertura 100% de LoginWall vía fallback.
