# Contrato de almacenamiento: `FavoritesStore`

## Ubicación y alcance

El store se ubica conceptualmente en:

```text
<Kodi profile>/addon_data/plugin.video.gramolavideos/favorites.json
```

La implementación obtiene el perfil mediante la API de Kodi del addon y crea
el directorio si falta. El fichero pertenece a la instalación y perfil activos;
no se guarda en `resources/csv/`, no viaja con el addon y no se sincroniza.

## Esquema JSON

La raíz es un objeto versionable:

```json
{
  "version": 1,
  "favorites": [
    {
      "year_id": "1986",
      "video_id": "AbCdEfGhI_j",
      "title": "Artista - Canción",
      "added_at": "2026-07-29T19:54:00Z"
    }
  ]
}
```

Campos obligatorios de cada entrada:

| Campo | Validación |
|---|---|
| `year_id` | Cadena de cuatro dígitos. |
| `video_id` | ID válido conforme a la regla del catálogo. |
| `title` | Cadena no vacía tras recortar espacios. |
| `added_at` | Fecha ISO-8601 UTC válida. |

Los campos desconocidos pueden ignorarse al leer para permitir evolución
compatible. JSON malformado, raíz o tipos inesperados, y entradas inválidas son
errores recuperables: no se propagan a `kodi_plugin` sin traducción a un aviso
amigable.

## Operaciones

### `add(entry)`

1. Valida una referencia de catálogo resoluble.
2. Busca por clave `(year_id, video_id)`.
3. Si ya existe, no añade otra entrada ni altera su fecha: resultado idempotente.
4. Si no existe, captura título y fecha UTC, persiste y deja la nueva entrada
   primera al ordenar por `added_at` descendente.

### `remove(year_id, video_id)`

Elimina la entrada de esa clave si existe y persiste la colección resultante.
Si no existe, no modifica nada y se considera una operación idempotente. No
abre, edita ni borra un CSV.

### `list_resolved(catalog_dir)`

Lee favoritos válidos, los ordena de más reciente a más antiguo y para cada
uno carga su año y busca el ID de vídeo. Devuelve los activos y separa los
huérfanos para que la UI los oculte por defecto o pueda avisar ante una ruta
directa.

## Reglas de deduplicación y huérfanos

- La clave compuesta es la única regla de deduplicación; no se deduplica por
  título.
- La primera inserción válida conserva su `added_at`; un segundo añadir no
  cambia el orden.
- Es huérfano si el año no existe/no es legible o si el ID no aparece entre las
  filas válidas del año.
- El store conserva huérfanos hasta que el usuario los quite. No hay limpieza
  automática ni modificación del catálogo.
