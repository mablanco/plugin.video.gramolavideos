# Modelo de datos: contexto de vista anual

## YearContext

Entidad efímera que representa el contexto de una vista de canciones abierta
desde un año del catálogo. No se persiste ni se añade al CSV.

| Campo | Tipo | Origen | Reglas |
|-------|------|--------|--------|
| `year_id` | `str` | `foldername` de la query `mode=year` | Identificador del año seleccionado; se entrega sin transformación a la categoría de Kodi (p. ej. `1985`). |
| `view_mode` | literal `year` | parámetro `mode` | Debe ser `year` para aplicar este contexto. |
| `category_label` | `str` | `year_id` | Debe ser exactamente igual a `year_id`; no se prefija ni se traduce en este MVP. |

## Relaciones y ciclo de vida

- Un `YearContext` se crea al procesar `mode=year&foldername=<YYYY>`.
- El mismo `year_id` se usa para cargar `MusicVideo` mediante
  `catalog.load_year(...)` y para `xbmcplugin.setPluginCategory(...)`.
- Un contexto aplica a cero o más `MusicVideo`: incluso si el catálogo queda
  vacío o contiene errores recuperables, no requiere almacenamiento adicional.
- Termina cuando Kodi finaliza el listado actual; no se comparte con otra
  navegación ni con reproducción, favoritos o búsqueda.

## Datos que no cambian

- Los CSV siguen siendo un fichero por año y mantienen sus filas
  `Artista - Canción;youtube_video_id`.
- `MusicVideo`, `Decade` y las URL del plugin no incorporan campos nuevos.
