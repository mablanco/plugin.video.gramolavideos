# Research: Empaquetado búsqueda vs favoritos

**Feature**: `005-busqueda-favoritos`  
**Date**: 2026-07-29

## R-001: Criterios (FR-002)

| Id | Criterio | Pregunta |
|----|----------|----------|
| P1 | Valor oyente | ¿Duele ya con el catálogo actual/ampliado? |
| P2 | Independencia historias | ¿Se puede demo/testear sola? |
| P3 | Tamaño / riesgo | ¿Cuánto UX+persistencia+pruebas? |
| P4 | Solapamiento diseño | ¿Comparten pantallas/datos obligatorios? |
| P5 | Simplicidad producto | ¿Unir hincha el primer PR? |

## R-002: Perfil — Búsqueda (catálogo local)

**MVP conceptual**:
- Entrada desde raíz (p. ej. “Buscar”).
- Input de texto (teclado Kodi); coincidencia en título/artista del catálogo
  local (no YouTube web).
- Resultados = ítems reproducibles o enlace al año; vacío comprensible.
- Exclusiones: filtros avanzados, fuzzy online, sinónimos, búsqueda remota.

**Notas**: Valor sube mucho tras 004 (más filas). En TV el teclado es fricción
(P3 alto). Puede requerir escanear varios CSV (tensión con carga selectiva →
diseño cuidadoso en su propia feature).

## R-003: Perfil — Favoritos

**MVP conceptual**:
- Marcar/desmarcar desde una canción (contexto o acción).
- Entrada raíz “Favoritos” con lista persistente por perfil/instalación.
- Quitar favorito; favorito huérfano → ocultar o avisar (definir en su spec).
- Exclusiones: multi-listas, nube, recomendaciones.

**Notas**: Valor inmediato aunque el catálogo sea pequeño. Persistencia local
(nueva), pero historias independientes de búsqueda (P2 alto). Sin teclado.

## R-004: Estrategias de empaquetado

### Estrategia A — Una feature combinada

| Criterio | Valoración |
|----------|------------|
| P1 | Medio — entrega “descubrimiento” amplio |
| P2 | Mal — bloquea demo parcial limpia |
| P3 | Mal — teclado + persistencia + 2 entradas raíz en un PR |
| P4 | Bajo solapamiento real (casi solo raíz compartida) |
| P5 | Mal — primer plan hinchado |

MVP interno posible (favoritos primero dentro del mismo número) pero confunde
trazabilidad Speckit.

### Estrategia B — Dos features separadas

| Criterio | Valoración |
|----------|------------|
| P1 | Bien — priorización explícita |
| P2 | Bien |
| P3 | Bien — PRs acotados |
| P4 | Solapamiento mínimo (ítem raíz); contratos de navegación compartidos OK |
| P5 | Bien |

## R-005: Veredicto de empaquetado

**Decision**: **Estrategia B — dos features distintas.**

**Orden recomendado**:
1. **Favoritos** primero (menor fricción TV, valor inmediato, no depende de 004).
2. **Búsqueda** después (más valor con catálogo grande; mejor tras 003/004).

**Prioridad relativa vs 003/004**:
- 003 (navegación) y 004 (contenido) **antes o en paralelo** a favoritos;
  búsqueda **después** de 004 idealmente (o tras semilla mínima).
- Ninguna de 003/004 bloquea el *estudio* actual; sí condicionan el *momento*
  de implementar búsqueda.

**Nombres sugeridos** para `/speckit-specify` futuros:
- `favoritos-usuario` (o `006-favoritos`)
- `busqueda-catalogo` (o `007-busqueda-catalogo`)

## R-006: Convivencia con navegación

Ambas capacidades futuras = **entradas adicionales en la raíz** junto a
décadas (si 003) o años (si no). No sustituyen el browse cronológico. Favoritos
referencian entradas del catálogo (año + video_id + título), no copian CSV
maestro.

## Alternatives considered

| Alternativa | Por qué no |
|-------------|------------|
| Una feature con MVP solo favoritos | Posible, pero el nombre “búsqueda/favoritos” sigue acoplando alcance |
| Búsqueda primero | Peor UX mando y menos urgente antes de semilla grande |
| Esperar a “plataforma de descubrimiento” única | Viola YAGNI / IV |
