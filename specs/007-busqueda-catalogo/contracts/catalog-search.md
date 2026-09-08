# Contrato de datos: `catalog.search`

## Firma propuesta

```python
def search(csv_dir: str, query: str, limit: int = 100) -> CatalogLoadResult:
    ...
```

El resultado usa `CatalogLoadResult.videos` para devolver coincidencias
reproducibles `MusicVideo` y `CatalogLoadResult.errors` para fallos
recuperables al descubrir o cargar años. No necesita APIs Kodi.

## Precondiciones y normalización

1. Convertir `query` a texto, aplicar `strip()` y después `casefold()`.
2. Si el valor normalizado queda vacío, devolver
   `CatalogLoadResult(videos=[], errors=[], ok=True)` sin abrir CSV.
3. El límite efectivo del MVP es 100. La UI llama con el valor por defecto; no
   se admite que una llamada aumente la exposición por encima de 100.

## Algoritmo observable

1. Llamar una vez a `list_years(csv_dir)`.
2. Para cada año listado, llamar a `load_year(csv_dir, year.id)`.
3. Acumular errores de descubrimiento y carga; continuar con los demás años.
4. Incluir cada vídeo válido cuando el texto normalizado es una subcadena de
   `video.title.casefold()`.
5. Ordenar las coincidencias por
   `(video.title.casefold(), video.year_id, video.video_id)`.
6. Devolver como máximo los primeros 100 resultados.

La búsqueda solo inspecciona los títulos locales `Artista - Canción`; no usa
metadatos remotos, ranking, fuzzy matching, sinónimos ni datos de favoritos.

## Comportamiento vacío y de error

| Situación | `videos` | `errors` | Responsabilidad UI |
|-----------|----------|----------|--------------------|
| Query vacía/cancelada | `[]` | `[]` | No presentar el catálogo completo. |
| Sin coincidencias | `[]` | Puede contener errores recuperables | Mostrar vacío comprensible y notificar errores. |
| Catálogo vacío o directorio ausente | `[]` | Errores de catálogo cuando correspondan | Mostrar vacío/aviso, sin abortar. |
| CSV corrupto | Coincidencias de filas/años válidos | Errores de filas o años afectados | Notificar sin ocultar resultados válidos. |

## Invariantes

- No se escribe, modifica ni reordena ningún CSV.
- `video_id` y `year_id` de cada resultado conservan los valores producidos por
  `load_year`.
- El límite se aplica después de ordenar, por lo que el listado es predecible.
