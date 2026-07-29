# Validation log: Base de catálogo 60s/70s

**Feature**: `004-catalogo-60-70`  
**Date**: 2026-07-29

## Pipeline

| Paso | Resultado | Notas | Fecha |
|------|-----------|-------|-------|
| Baseline (cero CSV 1960–1979) | PASS | 0 ficheros en rango; 19 años 1980–1999 (sin 1994) | 2026-07-29 |
| Artefactos plan/spec/research/data-model/quickstart/contracts | PASS | T001 | 2026-07-29 |
| Generación candidatos offline | PASS | 60/60 vía yt-dlp en host; no `kodi_plugin.run` | 2026-07-29 |
| Validación mecánica / editorial | PASS | E1–E6; 0 dups intra-año; oEmbed ok=60/60 | 2026-07-29 |
| Publicación CSV | PASS | 16 ficheros nuevos 1964–1979; 1980–1999 sin cambios | 2026-07-29 |

## Conteos

| Métrica | Resultado | Notas | Fecha |
|---------|-----------|-------|-------|
| Años 1980–1999 (baseline) | 19 | 1980–1993, 1995–1999 | 2026-07-29 |
| years 1960–1979 | 16 | `scripts/count_seed_60_70.py` | 2026-07-29 |
| rows 1960–1979 | 60 | | 2026-07-29 |
| Umbrales FR-005/006 (≥8 años, ≥40 filas, ambas décadas) | PASS | 16 / 60 / 60s+70s | 2026-07-29 |
| pytest catalog load/ids/years | PASS | 9 passed | 2026-07-29 |
| CSV 1980–1999 reescritos | PASS (ninguno) | `git diff` vacío en esos paths | 2026-07-29 |

## Smoke 5+5

Muestreo oEmbed host (`youtube_probe.probe_youtube_video`); ≥80 % OK.

| video_id | década | Resultado | Notas | Fecha |
|----------|--------|-----------|-------|-------|
| 6CsvB8lT_Jo | 60s | ok | Los Sírex - La escoba (1964) | 2026-07-29 |
| Xj4nU5dOkn8 | 60s | ok | Los Bravos - Black Is Black (1966) | 2026-07-29 |
| JhPAZOwEY0I | 60s | ok | Massiel - La, la, la (1968) | 2026-07-29 |
| 2wQ5o9uHo-s | 60s | ok | Fórmula V - Cuéntame (1969) | 2026-07-29 |
| QeuJKgOskMw | 60s | ok | Juan y Junior - Anduriña (1967) | 2026-07-29 |
| E5MM8ccNRZA | 70s | ok | Miguel Ríos - Himno a la alegría (1970) | 2026-07-29 |
| 1qfh-BhVKZc | 70s | ok | Joan Manuel Serrat - Mediterráneo (1971) | 2026-07-29 |
| A5vaIjBQnmk | 70s | ok | Mocedades - Eres tú (1973) | 2026-07-29 |
| p5iqf86qLZA | 70s | ok | Triana - Abre la puerta (1975) | 2026-07-29 |
| 6ssGfaPrORE | 70s | ok | Burning - Qué hace una chica… (1978) | 2026-07-29 |

**Smoke batch**: 10/10 ok (100 %). Sin deuda de ids fallidos.

## Docs

| Entregable | Resultado | Notas | Fecha |
|------------|-----------|-------|-------|
| `docs/seed-60-70.md` | PASS | Pasos 1–6 + conteo + pytest/oEmbed host | 2026-07-29 |
| `scripts/count_seed_60_70.py` | PASS | Host-only; no importado por addon | 2026-07-29 |
| README / addon.xml / changelog | PASS | v0.4.0; alcance 60–90 | 2026-07-29 |
| Flujo «añadir una fila» (SC-005) | PASS | Documentado en README FAQ; &lt;5 min en seco | 2026-07-29 |
| pytest completo | PASS | 32 passed | 2026-07-29 |
| Nota UX listado plano (003) | PASS | Listado plano crece ~+16 años; UX mitigada por feature `003-navegacion-videos` | 2026-07-29 |
| CSV vacíos 1960–1979 | PASS | Ninguno | 2026-07-29 |
| Secretos en seed-work | PASS | Sin API keys; solo ids públicos | 2026-07-29 |
