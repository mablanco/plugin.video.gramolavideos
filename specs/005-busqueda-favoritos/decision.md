# Decisión: Empaquetado búsqueda / favoritos

**Feature**: `005-busqueda-favoritos`  
**Date**: 2026-07-29  
**Status**: Recomendado

## Veredicto (SC-001)

**Dos features distintas**, no una combinada.

| Capacidad | Feature futura sugerida | Orden |
|-----------|-------------------------|-------|
| Favoritos | `/speckit-specify` → favoritos de usuario | **1º** |
| Búsqueda local | `/speckit-specify` → búsqueda en catálogo | **2º** |

## Criterios (resumen)

Independencia de historias alta; solapamiento de diseño bajo; una feature
única hincharía riesgo/tamaño; favoritos no necesitan teclado ni catálogo
masivo.

## MVP / exclusiones por capacidad

### Favoritos (1º)
- Incluye: marcar, listar, quitar; persistencia local; acceso desde raíz.
- Excluye: multi-listas, sync nube, playlists colaborativas.

### Búsqueda (2º)
- Incluye: query texto sobre catálogo local; resultados; vacío claro.
- Excluye: YouTube global, filtros avanzados, recomendaciones.

## Relación con 003 / 004

- No bloqueadas por este veredicto.
- Ideal: 003 + 004 (o semilla parcial) antes de **implementar** búsqueda.
- Favoritos pueden planificarse en cuanto exista capacidad de mantenimiento.

## Qué no cambia

- CSV editorial = fuente de canciones.
- Reproducción YouTube.
- Esta feature **no** entrega código de ninguna de las dos capacidades (FR-010).

## Siguiente comando Speckit

1. (Opcional) `/speckit-tasks` solo si se quieren tareas de cierre documental de 005.
2. Preferible: `/speckit-specify` de **favoritos** cuando toque implementar.
3. Luego `/speckit-specify` de **búsqueda**.

Detalle: [contracts/packaging-verdict.md](./contracts/packaging-verdict.md).
