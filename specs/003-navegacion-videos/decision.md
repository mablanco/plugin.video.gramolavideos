# Decisión: Modelo de navegación

**Feature**: `003-navegacion-videos`  
**Date**: 2026-07-29  
**Status**: Recomendado (pendiente validación mantenedor en implementación)

## Veredicto

Adoptar **década → año → canciones → reproducir** (opción B en
[research.md](./research.md)).

## Criterios y puntuación (resumen)

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

## Gobernanza

- Enmendar constitution IV: flujo **décadas → años → canciones → play**.
- Actualizar README / contrato `plugin-navigation`.
- Bump de versión del addon al implementar.

## Siguiente paso

`/speckit-tasks` sobre esta feature, o implementar según `tasks.md` cuando exista.
