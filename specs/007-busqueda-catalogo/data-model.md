# Modelo de datos: búsqueda en catálogo

## `SearchQuery`

Representa la intención introducida por el oyente antes de consultar el
catálogo editorial local.

| Campo | Tipo | Regla |
|-------|------|-------|
| `text` | `str` | Texto recibido desde la UI. Se normaliza con `strip()`. |
| `normalized_text` | `str` | `text.casefold()` tras el recorte; se usa solo para comparar. |

**Validación**:

- Una consulta cancelada, vacía o formada por espacios no es ejecutable.
- No existe longitud mínima en el MVP: incluso un fragmento de un carácter es
  válido, aunque puede alcanzar el límite de resultados.
- La consulta no modifica el CSV ni se persiste.

## `SearchResult`

Representa una coincidencia local reproducible. Puede ser una clase ligera o
un `MusicVideo` enriquecido en la capa de presentación; no duplica contenido
editorial.

| Campo | Tipo | Origen / uso |
|-------|------|--------------|
| `title` | `str` | `MusicVideo.title`: `Artista - Canción`. |
| `video_id` | `str` | `MusicVideo.video_id`; identifica la reproducción. |
| `year_id` | `str` | `MusicVideo.year_id`; contexto para etiqueta/info. |

**Relaciones y reglas**:

- Un `SearchResult` corresponde a una fila válida de un CSV de `Year`.
- El resultado principal es reproducible mediante la ruta de canción existente;
  no cambia el proveedor `plugin.video.youtube`.
- La colección se ordena por `title.casefold()`, después `year_id` y
  `video_id`, y se recorta a 100 elementos.
- Errores de una hoja o fila no invalidan resultados válidos de otros años;
  vuelven como errores de catálogo para que la UI los notifique.

## `SearchCapability`

Perfil de producto que restringe la funcionalidad de búsqueda.

| Propiedad | Valor MVP |
|-----------|-----------|
| `query_scope` | `local_catalog` |
| `match_fields` | título editorial completo (`artista + canción`) |
| `match_rule` | subcadena, sin distinguir capitalización |
| `result_kind` | canción reproducible; año como contexto opcional |
| `sort` | alfabético por título, con desempates estables |
| `result_limit` | 100 |
| `empty_behavior` | directorio vacío + mensaje claro; nunca catálogo completo |
| `out_of_scope` | YouTube/remoto, fuzzy, sinónimos, filtros, recomendaciones y favoritos |

`SearchCapability` se alinea con `SearchQuery` porque solo admite texto local
normalizado, y con `SearchResult` porque todo resultado procede de un
`MusicVideo` validado por el catálogo.
