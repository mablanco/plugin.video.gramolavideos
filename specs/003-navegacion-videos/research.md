# Research: Navegación del catálogo

**Feature**: `003-navegacion-videos`  
**Date**: 2026-07-29

## R-001: Criterios de evaluación

**Decision**: Puntuar opciones con C1–C5 (alineados a FR-002):

| Id | Criterio | “Bien” significa |
|----|----------|------------------|
| C1 | Mando / TV | Pocos ítems por pantalla; etiquetas claras |
| C2 | Pasos hasta canciones | ≤3 carpetas antes de ver canciones (SC-002) |
| C3 | Escalabilidad 60s–90s | Raíz ≤12 con escenario 1960–1999 (SC-003) |
| C4 | Simplicidad producto | Sin frameworks; reglas fáciles de explicar |
| C5 | Identidad gramola | Sigue siendo índice por época, no buscador |

## R-002: Opciones evaluadas (≥3)

### Opción A — Listado plano de años (status quo)

| Criterio | Valoración |
|----------|------------|
| C1 | Mal con ≥20–40 años |
| C2 | Bien (1 paso a canciones del año) |
| C3 | Mal (~40 ítems en raíz) |
| C4–C5 | Bien |

**Conclusión**: Insuficiente como diseño objetivo; válido solo como baseline.

### Opción B — Década → año → canciones → play

| Criterio | Valoración |
|----------|------------|
| C1 | Bien — 2–4 décadas en raíz hoy/proyectado |
| C2 | Bien — 2 pasos de carpeta hasta canciones |
| C3 | Bien — máximo ~4 décadas (1960–1999) |
| C4 | Bien — regla `year // 10` |
| C5 | Bien — sigue anclado en años |

**Reglas**:
- Década `D` = años `D0`–`D9` (p. ej. 1980–1989 → “Años 80”).
- Solo mostrar décadas con ≥1 CSV real; no inventar años vacíos.
- Estructura fija (no colapsar si hay una sola década): predecible al crecer el catálogo.
- Etiquetas ES: `Años 60`, `Años 70`, … (strings i18n-ready).

### Opción C — “Recientes” planos + “Archivo” por década

| Criterio | Valoración |
|----------|------------|
| C1 | Medio — mezcla dos modelos |
| C2 | Bien/variable |
| C3 | Bien |
| C4 | Mal — regla de “reciente” arbitraria |
| C5 | Medio |

**Conclusión**: Rechazada por inconsistencia y YAGNI.

### Opción D (descartada rápido) — Raíz por artista

Exige índice nuevo o escanear todos los CSV en raíz → choca con carga selectiva
y con identidad “por años”. Fuera de alcance (búsqueda = 005).

## R-003: Veredicto

**Decision**: **Opción B — década → año → canciones → reproducir**.

**Rationale**: Única opción que cumple C3 sin complicar C4/C5; añade un solo
`mode` y deriva agrupación de `list_years` sin tocar CSV.

**Gobernanza**: Actualizar constitution IV y contratos de navegación
(`contracts/constitution-amendment-draft-iv.md`).

**Fuera de alcance**: contenido 60/70 (004); búsqueda/favoritos (005).

## R-004: Contrato de query

**Decision**:

| mode | foldername | UI |
|------|------------|-----|
| (ausente) | — | listar décadas presentes |
| `decade` | `1960` \| `1970` \| … (año inicio de década) | listar años de esa década |
| `year` | `YYYY` | canciones (sin cambio) |
| `song` | `video_id` | play (sin cambio) |

Atrás de Kodi: pila natural de directorios plugin.

## R-005: Dónde vive la lógica de décadas

**Decision**: Función pura en capa catálogo (p. ej. `list_decades` /
`years_in_decade`) sin `xbmc*`; `kodi_plugin` solo pinta.

**Alternatives**: Agrupar solo en UI — acopla y dificulta tests; ficheros por
década — viola “CSV por año” / FR-006.

## Alternatives considered (global)

| Alternativa | Por qué no |
|-------------|------------|
| Mantener plano + scroll | Falla SC-003 con 004 |
| Colapsar nivel si 1 década | Ahorra un clic hoy; confunde cuando aparezca la 2ª |
| `script.module.routing` | YAGNI (constitution / 001) |
