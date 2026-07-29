# Handoff: `/speckit-specify` — Búsqueda en catálogo

**Origen**: `005-busqueda-favoritos` (veredicto: dos features; búsqueda **2º**)  
**Nombre sugerido**: `busqueda-catalogo` (o `007-busqueda-catalogo`)  
**Fecha**: 2026-07-29  
**Dependencia recomendada**: tras `004-catalogo-60-70` (o semilla mínima amplia)

## Prompt borrador para `/speckit-specify`

```text
Búsqueda local en el catálogo de la gramola Kodi: entrada “Buscar” en la
raíz, query de texto sobre título/artista de las entradas del addon
(no YouTube web), resultados reproducibles o enlace al año, y vacío claro
si no hay coincidencias.

Contexto: 005-busqueda-favoritos decidió separar búsqueda de favoritos.
Esta feature implementa SOLO búsqueda. No incluye marcar/listar favoritos.
Ideal después de ampliar el catálogo (004); convive con navegación 003
como ítem adicional en la raíz.

MVP:
- Ítem Buscar en la raíz junto a décadas/años.
- Coincidencia local en título/artista del catálogo.
- Resultados usables con mando; acotar ordenación/límite de resultados.
- Comportamiento vacío comprensible.

Exclusiones:
- Búsqueda remota / YouTube global.
- Filtros avanzados, fuzzy online, sinónimos.
- Recomendaciones.
- Favoritos (feature aparte: favoritos-usuario).
- Cambiar CSV editorial como fuente ni proveedor de reproducción.

Invariantes: catálogo local = ámbito de la query; sin cuenta online;
simplicidad de la gramola (teclado TV = fricción a diseñar con cuidado).
```

## Referencias

- [decision.md](./decision.md) — veredicto y flujo MVP búsqueda
- [contracts/packaging-verdict.md](./contracts/packaging-verdict.md)
- [data-model.md](./data-model.md) — `SearchCapability`
- [research.md](./research.md) R-002, R-005
