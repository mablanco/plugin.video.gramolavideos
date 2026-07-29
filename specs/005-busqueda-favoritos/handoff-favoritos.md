# Handoff: `/speckit-specify` — Favoritos de usuario

**Origen**: `005-busqueda-favoritos` (veredicto: dos features; favoritos **1º**)  
**Nombre sugerido**: `favoritos-usuario` (o `006-favoritos`)  
**Fecha**: 2026-07-29

## Prompt borrador para `/speckit-specify`

```text
Favoritos de usuario en la gramola Kodi: marcar/desmarcar canciones del
catálogo editorial, listarlas desde un ítem en la raíz del addon y
persistir la preferencia por instalación/perfil, sin sincronización en la
nube ni multi-listas.

Contexto: el estudio 005-busqueda-favoritos decidió separar favoritos y
búsqueda. Esta feature implementa SOLO favoritos. No incluye búsqueda por
texto. Convive con la navegación por años/décadas (003) como entrada
adicional en la raíz; no sustituye el browse cronológico.

MVP:
- Añadir favorito desde una canción del catálogo.
- Listar favoritos desde la raíz.
- Quitar favorito.
- Persistencia local (perfil/instalación).
- Huérfanos (entrada borrada del CSV): ocultar o avisar (hide_or_notify).

Exclusiones:
- Multi-listas / carpetas de favoritos.
- Sync nube / multi-dispositivo.
- Playlists colaborativas.
- Recomendaciones.
- Fusionar favoritos en el CSV editorial.
- Cambiar proveedor YouTube o formato de filas del catálogo.
- Búsqueda por texto (feature aparte: busqueda-catalogo).

Invariantes: CSV = fuente editorial; favoritos = preferencias; sin cuenta
online obligatoria.
```

## Referencias

- [decision.md](./decision.md) — veredicto y flujo MVP favoritos
- [contracts/packaging-verdict.md](./contracts/packaging-verdict.md)
- [data-model.md](./data-model.md) — `FavoritesCapability`
- [research.md](./research.md) R-003, R-005
