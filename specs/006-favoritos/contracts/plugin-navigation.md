# Contrato de navegación del plugin: Favoritos

## Invariantes

- La raíz mantiene el browse `décadas → años → canciones → reproducción`.
  **Favoritos** es una carpeta adicional, no una categoría editorial ni un
  reemplazo de las décadas.
- Las URLs se construyen con `build_url()` y parámetros codificados; no se
  interpolan títulos ni datos CSV sin codificar.
- Los modos existentes `decade`, `year` y `song` mantienen sus parámetros y
  comportamiento actuales.
- Los textos visibles y las acciones de contexto usan IDs de idioma Kodi.

## Raíz

Sin `mode`, el plugin añade primero una carpeta:

| Etiqueta | URL | Tipo |
|---|---|---|
| `Favoritos` (localizada) | `?mode=favorites` | carpeta |

Después añade exactamente las carpetas de décadas que devuelve el catálogo.
Una lista vacía de favoritos no elimina ni deshabilita la carpeta.

## Modos nuevos

| Mode | Parámetros requeridos | Resultado |
|---|---|---|
| `favorites` | ninguno | Lista favoritos resolubles, en orden de alta descendente; muestra estado vacío localizado si no hay activos. |
| `favorite_add` | `year_id`, `video_id`, `title` | Añade idempotentemente la entrada de catálogo; persiste y notifica éxito/error. |
| `favorite_remove` | `year_id`, `video_id` | Quita idempotentemente la preferencia; persiste y notifica éxito/error. |

`favorite_add` valida que la referencia siga resolviendo en el catálogo antes
de escribir. `favorite_remove` no exige resolución, por lo que puede eliminar
un favorito huérfano.

## Canciones y acciones de contexto

Al generar una canción desde `mode=year`, la UI conoce `year_id`, `video_id` y
`title` y añade una acción de contexto:

- si la clave no está guardada: **Añadir a favoritos** →
  `mode=favorite_add`;
- si ya está guardada: **Quitar de favoritos** →
  `mode=favorite_remove`.

Cada acción conserva como mínimo `year_id` y `video_id`; la acción de añadir
incluye el título codificado como instantánea. La canción conserva su URL de
reproducción vigente, `mode=song&foldername=<video_id>`.

En `mode=favorites`, cada favorito `active` se presenta como una canción
reproducible con el mismo resolved URL de YouTube que el listado de su año y
lleva la acción **Quitar de favoritos**. La ruta de reproducción debe
revalidar `(year_id, video_id)` antes de delegar en YouTube.

## Huérfanos y errores recuperables

- `favorites` no lista por defecto favoritos que no se resuelvan.
- Si una URL de favorito ya emitida intenta reproducir un huérfano, el plugin
  muestra una notificación localizada, no resuelve URL y mantiene disponible
  `favorite_remove`.
- Fallos al cargar o guardar el store producen notificación localizada y
  cierran la vista/directorio de forma segura; nunca abortan el addon.
