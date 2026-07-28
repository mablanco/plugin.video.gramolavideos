# Contract: Criterios de decisión

**Feature**: `002-alternativa-youtube`  
**Updated**: 2026-07-28  
**Consumers**: Mantenedor, revisores, `/speckit-tasks` / implementación futura

## Purpose

Congelar cómo se evalúan las opciones tras el reframe post-smoke (FR-002, FR-012).

## Criteria (MUST)

| Id | Name | Pass condition |
|----|------|----------------|
| C1 | Sin API key desarrollador | Recorrido mayoritario sin consola Google |
| C2 | No rehost / no descarga-solución | No almacena el vídeo como solución |
| C3 | Catálogo intacto | CSV con ids de YouTube |
| C4 | Flujo de producto | años → canciones → reproducir |
| C5 | Kodi moderno | Matrix+ / destino del proyecto |
| C6 | Sostenibilidad | Riesgos ToS/mantenimiento documentados |
| C7 | Instalabilidad | Preferible repo oficial; ZIP permitido si C8 lo exige |
| C8 | Cobertura login-wall | Puede intentar títulos que YouTube bloquea tras login sin forzar ese login |

## Scoring vocabulary (MUST)

- `bien` | `medio` | `mal` | `incompatible` | `n/a` | `parcial`

## Options minimum set (MUST)

1. Solo `plugin.video.youtube` (+ mitigaciones ante login).
2. Al menos un fallback/alternativa orientado a C8 (p. ej. SendToKodi).
3. Modo híbrido (YouTube por defecto + fallback) **o** mitigaciones no triviales.

Estado actual (research): veredicto **híbrido**.

## Verdict fields (MUST)

- `choice` (p. ej. `hybrid_youtube_plus_ytdlp_fallback`)
- `api_key_required_happy_path` (`no` tras smoke 7.4.x+)
- `login_wall_bypass_attempt` (`yes` / `no` / `partial`)
- `constitution_amendment_required` (bool)
- `implementation_in_this_feature` = `false`
- `next_steps`
- Riesgos residuales (cobertura parcial C8, ToS)

## Non-goals

- No garantiza reproducir el 100% de títulos con login-wall.
- No prescribe la UX exacta del fallback (auto vs menú) — eso es feature de implementación.
