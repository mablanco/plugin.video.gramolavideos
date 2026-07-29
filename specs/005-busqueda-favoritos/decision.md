# Decisión: Empaquetado búsqueda / favoritos

**Feature**: `005-busqueda-favoritos`  
**Date**: 2026-07-29  
**Status**: Aprobado para cierre documental

> **Veredicto (SC-001):** Dos features distintas — favoritos primero
> (`favoritos-usuario`), búsqueda después (`busqueda-catalogo`); 005 no
> implementa runtime de ninguna de las dos.

| Capacidad | Feature futura sugerida | Orden |
|-----------|-------------------------|-------|
| Favoritos | `/speckit-specify` → `favoritos-usuario` (o `006-favoritos`) | **1º** |
| Búsqueda local | `/speckit-specify` → `busqueda-catalogo` (o `007-busqueda-catalogo`) | **2º** |

Contrato normativo: [contracts/packaging-verdict.md](./contracts/packaging-verdict.md)  
(`strategy: two_features`, `order: favorites -> search`,
`implements_runtime_in_005: false`).

---

## Criterios P1–P5 (FR-002)

Alineados con [contracts/decision-criteria.md](./contracts/decision-criteria.md)
y [research.md](./research.md) R-001:

| Id | Criterio | Pregunta |
|----|----------|----------|
| P1 | Valor oyente | ¿Duele ya con el catálogo actual/ampliado? |
| P2 | Independencia historias | ¿Se puede demo/testear sola? |
| P3 | Tamaño / riesgo | ¿Cuánto UX + persistencia + pruebas? |
| P4 | Solapamiento diseño | ¿Comparten pantallas/datos obligatorios? |
| P5 | Simplicidad producto | ¿Unir hincha el primer PR? |

---

## Estrategias evaluadas (FR-001)

Inventario con detalle en [research.md](./research.md) R-004:

### Estrategia A — Una feature combinada

Una sola feature Speckit cubre búsqueda y favoritos (posible MVP interno
favoritos-primero, pero el paquete sigue acoplado).

### Estrategia B — Dos features separadas *(elegida)*

Dos `/speckit-specify` independientes, con contratos de navegación raíz
compartidos si hace falta.

### Matriz P1–P5 × estrategias A/B

| Criterio | A (una feature) | B (dos features) |
|----------|-----------------|------------------|
| P1 Valor | Medio — “descubrimiento” amplio | Bien — priorización explícita |
| P2 Independencia | Mal — bloquea demo parcial limpia | Bien |
| P3 Tamaño/riesgo | Mal — teclado + persistencia + 2 entradas raíz | Bien — PRs acotados |
| P4 Solapamiento | Bajo real (casi solo raíz) | Mínimo (ítem raíz); OK |
| P5 Simplicidad | Mal — primer plan hinchado | Bien |

**Conclusión:** Estrategia B gana en P2, P3 y P5; P4 no justifica unir; P1 se
atiende mejor priorizando favoritos ya y búsqueda tras catálogo amplio.

---

## Orden, nombres y exclusiones de 005 (US1)

- **Orden:** favoritos → búsqueda (valor inmediato + menos fricción TV primero;
  búsqueda gana valor tras catálogo grande).
- **Nombres sugeridos:** `favoritos-usuario`, `busqueda-catalogo` (ver
  packaging-verdict).
- **Fuera de alcance de 005:**
  - Implementación UI en Kodi (buscar, marcar, listar).
  - Suite pytest nueva para estas capacidades.
  - Cambios en CSV editorial o en el proveedor YouTube.
  - Cualquier LOC en `addon.py`, `resources/lib/kodi_plugin.py`,
    `resources/csv/`.

---

## Búsqueda — flujo MVP (US2)

Cita: [research.md](./research.md) R-002. Independiente de favoritos (FR-003).

| Paso | Comportamiento |
|------|----------------|
| Entrada | Ítem en raíz del addon (p. ej. “Buscar”), junto a décadas/años. |
| Query | Texto local; coincidencia en **título / artista** del catálogo del addon. |
| Resultados | Ítems reproducibles (o enlace al año); ordenación/límite a fijar en su spec. |
| Vacío | Listado vacío + mensaje claro (`empty_behavior` en data-model). |

**Exclusiones de búsqueda:** YouTube global / web remota; filtros avanzados;
fuzzy online; sinónimos; recomendaciones.

**Priorización:** la búsqueda gana valor tras `004-catalogo-60-70` (más filas);
ideal implementar después de 003/004 o tras semilla mínima. No depende de
favoritos.

**Alineación data-model:** `SearchCapability` —
`query_scope: local_catalog`, `match_fields: título (artista + canción)`,
`empty_behavior: listado vacío + mensaje claro`,
`out_of_scope: remoto, filtros avanzados` — coincide con este apartado.

---

## Favoritos — flujo MVP (US3)

Cita: [research.md](./research.md) R-003. Historia aislable sin búsqueda.

| Paso | Comportamiento |
|------|----------------|
| Añadir | Marcar desde una canción del catálogo (contexto / acción). |
| Listar | Entrada raíz “Favoritos”; lista persistente por instalación/perfil. |
| Quitar | Desmarcar; deja de aparecer en la lista. |
| Persistencia | Local (`storage_scope: per_install_or_profile`); sin sync multi-dispositivo en MVP. |

**Exclusiones de favoritos:** multi-listas; carpetas de favoritos; sync en la
nube; playlists colaborativas; recomendaciones automáticas.

**Huérfanos:** si el año o `video_id` desaparece del catálogo, política a alto
nivel `hide_or_notify` (ocultar o avisar con enlace comprensible) — a fijar en
la spec futura; ver `orphan_policy` en
[data-model.md](./data-model.md) (`FavoritesCapability`).

**Alineación data-model:** `FavoritesCapability` —
`actions: add / list / remove`, `orphan_policy: hide_or_notify`,
`out_of_scope: multi-listas, nube` — coincide con este apartado.

---

## Invariantes de producto (US4 / SC-005)

- **CSV editorial** = fuente de canciones disponibles; no se reescribe masivamente
  ni se fusionan favoritos dentro del CSV maestro (FR-007).
- **No rehost** de medios; reproducción sigue delegada a **YouTube** (FR-008).
- **Favoritos = preferencias de usuario**, no catálogo.
- **Entradas adicionales en la raíz** (“Buscar” / “Favoritos”) junto a décadas
  (si 003) o años — no sustituyen el browse cronológico
  ([research.md](./research.md) R-006).

**Opciones rechazadas:** cuenta online obligatoria; reescritura masiva del CSV;
sustituir el proveedor de reproducción.

**Prioridad relativa vs 003 / 004:**

| Línea | Relación |
|-------|----------|
| `003-navegacion-videos` | Convive; favoritos/búsqueda no la bloquean ni la exigen. |
| `004-catalogo-60-70` | Favoritos paralelizable ya; búsqueda **preferible tras 004**. |
| Este veredicto | No bloquea 003/004; condiciona el *momento* de implementar búsqueda. |

---

## Qué no cambia en el addon (FR-010)

En el alcance de **005** no se modifican:

- `addon.py`
- `resources/lib/kodi_plugin.py` (ni el resto de `resources/lib/`)
- `resources/csv/`

Entregable = documentación de decisión + handoffs; 0 LOC de addon.

---

## Siguiente comando Speckit

1. **`/speckit-specify` de favoritos** usando el borrador
   [handoff-favoritos.md](./handoff-favoritos.md).
2. Más tarde **`/speckit-specify` de búsqueda** usando
   [handoff-busqueda.md](./handoff-busqueda.md) (ideal tras 004).
3. No reabrir 005 como implementación de UI.

Validación del cierre: [validation-log.md](./validation-log.md) /
[quickstart.md](./quickstart.md).
