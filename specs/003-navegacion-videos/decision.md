# Decisión: Modelo de navegación

**Feature**: `003-navegacion-videos`  
**Date**: 2026-07-29  
**Status**: Aprobado para implementación (opción B)

## Veredicto

Adoptar **década → año → canciones → reproducir** (opción B en
[research.md](./research.md) R-003), alineado con
[contracts/decision-criteria.md](./contracts/decision-criteria.md) (C1–C5).

## Matriz C1–C5 × opciones A–C

Detalle y valoraciones: [research.md](./research.md) R-002. Resumen auditable:

| Opción | C1 TV | C2 pasos | C3 escala | C4 simple | C5 identidad | Resultado |
|--------|-------|----------|-----------|-----------|--------------|-----------|
| A Plano años | Mal | Bien | Mal | Bien | Bien | Rechazada como objetivo |
| B Década→año | Bien | Bien | Bien | Bien | Bien | **Elegida** |
| C Recientes+archivo | Medio | Variable | Bien | Mal | Medio | Rechazada |

## Recorrido de usuario

1. Abrir addon → décadas con datos (p. ej. `Años 80`, `Años 90`).
2. Elegir década → años CSV de ese rango.
3. Elegir año → canciones.
4. Elegir canción → reproducción YouTube (sin cambio).

## Edge cases (fijados)

- Década incompleta: solo años con CSV.
- Una sola década en catálogo: igual se muestra el nivel década (estructura fija).
- Años 1960–1999 proyectados: ≤4 ítems en raíz (cumple SC-003).

## Fuera de alcance

- Contenido editorial de los **60/70** (feature `004-catalogo-60-70`).
- **Búsqueda** y **favoritos** (feature `005-busqueda-favoritos`).
- Frameworks de routing (`script.module.routing`) y colapso del nivel década.

## Gobernanza

- Enmendar constitution IV: flujo **décadas → años → canciones → play**.
- Actualizar README / contrato `plugin-navigation`.
- Bump de versión del addon al implementar.

## Siguiente paso

Implementar según [tasks.md](./tasks.md) / [plan.md](./plan.md).
