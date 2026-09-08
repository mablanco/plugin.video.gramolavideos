# Contrato de navegación del plugin: búsqueda

**Versión**: propuesta para `007-busqueda-catalogo`  
**Base**: contrato de décadas de `003-navegacion-videos`.

## Raíz

Sin `mode`, el plugin abre el directorio raíz con:

1. la carpeta **Buscar**, con URL `?mode=search`;
2. las carpetas de décadas derivadas del catálogo, con
   `?mode=decade&foldername=<decade_id>`;
3. la carpeta Favoritos si y solo si su capacidad ya está instalada.

Buscar es un acceso adicional: no sustituye décadas → años → canciones.

## Modos

| Modo | Parámetros | Acción | Salida |
|------|------------|--------|--------|
| *(ausente)* | — | Construye la raíz. | Buscar + décadas + Favoritos opcional. |
| `search` | — | Solicita texto con el teclado de Kodi. | Sin query: finaliza sin listar catálogo; query válida: abre `search_results`. |
| `search_results` | `q` obligatorio | Consulta catálogo local para `q`. | Directorio de hasta 100 canciones o vacío comprensible. |
| `decade` | `foldername=<YYYY>` | Lista años de la década. | Carpetas de años. |
| `year` | `foldername=<YYYY>` | Carga el CSV del año. | Canciones reproducibles. |
| `song` | `foldername=<video_id>` | Resuelve mediante YouTube. | URL reproducible o aviso recuperable. |

## Parámetro `q`

- `q` codifica la consulta original mediante `urlencode`; el parser de plugin
  la recupera con `parse_qs`.
- `q` se recorta antes de llamar a `catalog.search`.
- Falta, vacío, solo espacios o cancelación son entradas no ejecutables: no
  invocan una búsqueda global ni presentan filas.
- La URL de resultados puede contener caracteres Unicode y espacios
  codificados; no contiene IDs de vídeo ni estado de favoritos.

## Ítems de resultados

Cada fila de `search_results`:

- usa `isFolder=False` e `IsPlayable=true`;
- enlaza a `?mode=song&foldername=<video_id>`;
- etiqueta el título editorial y puede añadir `year_id` como contexto;
- usa la misma construcción de `ListItem` y el mismo resolver que una canción
  listada desde un año.

La UI muestra una notificación amigable por errores recuperables de carga y un
estado vacío comprensible si no hay coincidencias.
