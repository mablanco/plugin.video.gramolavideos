# Implementation Plan: Alcance de búsqueda y favoritos

**Branch**: `005-busqueda-favoritos` | **Date**: 2026-07-29 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/005-busqueda-favoritos/spec.md`

**Note**: Feature de **análisis y empaquetado** (FR-010). **No** implementa
búsqueda ni favoritos en el addon. Veredicto: **dos features separadas**.

## Summary

Evaluar si búsqueda y favoritos van juntas o separadas. Decisión documentada:
**separar** en dos features futuras, con favoritos primero y búsqueda después
(tras o en paralelo a 003/004 según prioridad). Entregable = `decision.md` +
contratos; 0 cambios de runtime aquí.

## Technical Context

**Language/Version**: Documentación en español.

**Primary Dependencies**: N/A runtime. Contexto: `catalog` + `kodi_plugin`
actuales (browse-only); sin settings/favoritos hoy.

**Storage**: N/A en esta feature. (Futuro: favoritos = preferencias usuario;
búsqueda = índice/lectura catálogo — solo esbozado en data-model.)

**Testing**: Revisión documental del veredicto (quickstart). Sin pytest nuevo.

**Target Platform**: Decisión de producto para `plugin.video.gramolavideos`.

**Project Type**: Estudio de alcance / packaging Speckit.

**Performance Goals**: N/A.

**Constraints**: No implementar UI; no cambiar CSV ni YouTube; respetar
simplicidad (IV); catálogo editorial ≠ favoritos (FR-007).

**Scale/Scope**: 1 veredicto; 2 perfiles de capacidad; orden + nombres sugeridos
para siguientes `/speckit-specify`; 0 LOC addon.

## Constitution Check

| Principle | Pre-design | Post-design |
|-----------|------------|-------------|
| **I–III, V–X** | PASS | PASS — sin runtime |
| **IV. Simplicidad** | PASS | PASS — separar reduce monolito; implementación futura justificará capas |

**Gate result**: PASS (solo análisis).

## Project Structure

```text
specs/005-busqueda-favoritos/
├── plan.md
├── research.md
├── decision.md
├── data-model.md
├── quickstart.md
├── contracts/
│   ├── decision-criteria.md
│   └── packaging-verdict.md
├── checklists/
└── tasks.md
```

**Structure Decision**: Solo artefactos bajo `specs/005-busqueda-favoritos/`.

## Complexity Tracking

Ninguna violación en esta fase. Futuras features de implementación MUST
rellenar Complexity Tracking si añaden settings, teclado virtual o índices.
