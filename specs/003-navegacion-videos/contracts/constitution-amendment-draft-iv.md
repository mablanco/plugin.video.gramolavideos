# Borrador de enmienda: Constitution principio IV

**Feature**: `003-navegacion-videos`  
**Target**: `.specify/memory/constitution.md`  
**Proposed version bump**: 1.2.1 → 1.3.0 (cambio de flujo de producto)

## Texto actual (resumen)

IV exige preservar el flujo **años → canciones → reproducción**.

## Texto propuesto

### IV. Simplicidad del plugin

El addon MUST preservar el flujo de usuario **décadas → años → canciones →
reproducción**, donde las décadas se derivan de los años presentes en el
catálogo (CSV por año) y no sustituyen al año como unidad de datos. Nuevas
capas, frameworks o abstracciones MUST justificarse en Complexity Tracking del
plan. La evolución del código MAY introducir módulos, pero MUST NOT complicar
el producto más allá de lo necesario (YAGNI).

Rationale: el listado plano de años no escala al arco editorial 60s–90s; un
único nivel de agrupación por década mantiene la identidad cronológica sin
añadir búsqueda ni taxonomías paralelas.

## Restricciones técnicas (ajuste)

- Listados de directorio MUST usar las APIs de plugin de Kodi de forma coherente
  con el flujo **décadas → años → canciones**.

## Cuándo aplicar

Antes o en el mismo PR que active `mode=decade` en runtime. No aplicar solo por
existir este borrador.
