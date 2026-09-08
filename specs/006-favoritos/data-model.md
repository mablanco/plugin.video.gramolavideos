# Modelo de datos: Favoritos de usuario

## Referencia al catálogo

`CatalogEntry` es la referencia lógica a `catalog.MusicVideo`:

| Campo | Origen | Uso |
|---|---|---|
| `year_id` | `MusicVideo.year_id` | Identifica el CSV editorial que debe resolverse. |
| `video_id` | `MusicVideo.video_id` | Identificador YouTube y segunda parte de la identidad. |
| `title` | `MusicVideo.title` | Texto visible; se copia al añadir. |

El catálogo CSV sigue siendo la autoridad para resolver y reproducir una
entrada. No se añade ningún campo ni fila al CSV.

## Favorite

Preferencia persistida del usuario para una `CatalogEntry`.

| Campo | Tipo | Reglas |
|---|---|---|
| `year_id` | `str` | Obligatorio; exactamente cuatro dígitos; coincide con la clave de la entrada. |
| `video_id` | `str` | Obligatorio; debe cumplir la validación vigente de ID YouTube del catálogo. |
| `title` | `str` | Obligatorio y no vacío al añadir; instantánea para presentación, no clave. |
| `added_at` | `str` | Obligatorio; marca temporal UTC ISO-8601 para ordenar descendentemente. |

**Clave de identidad**: `(year_id, video_id)`. Dos favoritos con la misma
clave representan la misma preferencia aunque difieran en título o fecha.

## FavoritesStore

Servicio de datos puro responsable de cargar, validar, deduplicar y persistir
una colección de `Favorite` en JSON dentro del perfil Kodi.

- No importa `xbmc`, `xbmcgui`, `xbmcplugin` ni construye `ListItem`.
- Expone operaciones equivalentes a `list()`, `contains(year_id, video_id)`,
  `add(catalog_entry)` y `remove(year_id, video_id)`.
- La escritura conserva solo entradas válidas y únicas; los errores de I/O se
  devuelven o elevan para que la capa UI los comunique con una notificación
  amigable.
- El listado se entrega por `added_at` descendente: reciente primero.

## Resolución y estado de un favorito

Para listar o reproducir, la capa de datos intenta cargar `year_id` y busca el
`video_id` exacto entre los vídeos válidos de ese año.

| Estado | Condición | Comportamiento |
|---|---|---|
| `active` | Existe el año y contiene la pareja `(year_id, video_id)`. | Se lista y reproduce mediante el flujo YouTube existente. |
| `orphan` | Falta el CSV, no puede leerse, o ya no contiene el `video_id`. | Se oculta por defecto; no se borra del almacenamiento. Si se solicita reproducción, se avisa y se ofrece/quedará disponible la acción de quitar. |
| `removed` | El usuario ejecuta quitar. | Se elimina del store; no modifica el catálogo. |

Un error de fila ajena al favorito no lo convierte automáticamente en huérfano;
solo importa que no pueda resolverse la referencia solicitada.

## Transiciones

```text
entrada de catálogo no favorita --add--> active
active --add de la misma clave--> active (idempotente, sin duplicado)
active --catalog deja de resolver--> orphan
orphan --catálogo vuelve a resolver--> active
active/orphan --remove--> removed
removed --add desde catálogo--> active
```

`add` solo acepta una `CatalogEntry` válida del catálogo; `remove` acepta la
clave persistida para que también pueda limpiar un huérfano. La resolución no
actualiza ni elimina entradas automáticamente.
