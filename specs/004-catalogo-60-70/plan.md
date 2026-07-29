# Implementation Plan: Base de catálogo 60s/70s

**Branch**: `004-catalogo-60-70` | **Date**: 2026-07-29 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/004-catalogo-60-70/spec.md`

**Note**: Contenido + proceso de semilla **offline**. No cambia navegación UI
(003) ni reproducción. El addon solo gana CSV nuevos bajo `resources/csv/`.

## Summary

Generar de forma asistida una **semilla** ≥40 entradas en ≥8 años de
1960–1979 (ambas décadas), revisar editorialmente, validar formato/ids,
publicar CSV y actualizar README/metadatos. Proceso de mantenedor documentado;
sin rastreo en vivo en el plugin.

## Technical Context

**Language/Version**: Datos CSV + docs ES; tooling de semilla en host Python 3
(dev only, no `addon.xml`).

**Primary Dependencies (runtime)**: sin cambio (`plugin.video.youtube`).  
**Dev**: pytest/validadores existentes (`catalog`, opcional `youtube_probe` /
oEmbed); asistencia IA o listas curadas para candidatos.

**Storage**: nuevos `resources/csv/1960.csv`…`1979.csv` (solo años con ≥1 fila
publicable). No tocar masivamente 1980–1999.

**Testing**: validación de formato (suite catalog); muestreo smoke Kodi 5+5
(quickstart); checklist editorial.

**Target Platform**: mismo addon; catálogo ampliado.

**Project Type**: ampliación de datos + runbook de contribución.

**Performance Goals**: N/A UI; `list_years` sigue O(n ficheros) sin abrir CSV.

**Constraints**: constitution I–III; no rehost; no scrapear dentro del addon;
revisión humana obligatoria; umbrales FR-005/006.

**Scale/Scope**: ≥40 filas, ≥8 años, 2 décadas; README + versión addon;
runbook de semilla; tests de conteo de años a actualizar.

## Constitution Check

| Principle | Pre-design | Post-design |
|-----------|------------|-------------|
| **I. Catálogo como datos** | PASS | PASS — semilla = CSV |
| **II. YouTube** | PASS | PASS — solo video_id |
| **III. Alcance editorial** | PASS | PASS — ES 60/70; checklist |
| **IV. Simplicidad** | PASS | PASS — sin UI nueva; aviso: listado plano crece (mitiga 003) |
| **V. Metadatos** | PASS | PASS — bump + descripción 60–90 |
| **VI–X** | PASS | PASS |

**Gate result**: PASS. Dependencia blanda de 003 para UX con muchos años (no
bloquea esta feature).

## Project Structure

### Documentation

```text
specs/004-catalogo-60-70/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   ├── seed-process.md
│   └── editorial-review.md
├── checklists/
└── tasks.md
```

### Source / data

```text
resources/csv/19xx.csv          # nuevos años 60/70
README.md                       # alcance + cómo sembrar
addon.xml                       # versión / summary
# Opcional dev-only (si se añade en tasks):
# scripts/ o docs/seed-60-70.md — fuera del runtime Kodi
tests/unit/test_catalog_years.py  # actualizar expectativas de N años
```

**Structure Decision**: Datos en CSV; proceso en docs/scripts de mantenedor,
nunca en el path caliente del oyente.

## Complexity Tracking

Ninguna violación. (Crecimiento del listado plano es deuda de UX cubierta por
003, no una violación de esta feature.)
