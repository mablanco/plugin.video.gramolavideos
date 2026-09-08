# Investigación: Favoritos de usuario

## R-001 — Persistencia de preferencias

**Decision**: Guardar los favoritos en un fichero JSON dentro del directorio de
perfil (`addon_data`) que Kodi asigna al addon y al perfil activo.

**Rationale**: Los CSV en `resources/csv/` son la fuente editorial versionada.
El perfil de Kodi da persistencia por instalación/perfil sin requerir cuenta,
red ni cambiar los datos distribuidos con el addon. Un JSON es suficiente para
una colección pequeña, legible y sin dependencias adicionales.

**Alternatives considered**:

- Añadir una columna o filas al CSV: descartado porque mezclaría preferencias
  personales con catálogo editorial y alteraría el formato contractual.
- SQLite: descartado para el MVP; aporta consultas y esquema innecesarios para
  una lista lineal pequeña.
- Servicio remoto o sincronización: descartado por estar fuera de alcance.

## R-002 — Identidad y deduplicación

**Decision**: La identidad estable de un favorito es la pareja
`year_id + video_id`; se conserva `title` como instantánea para presentar y
diagnosticar la entrada.

**Rationale**: Un mismo vídeo de YouTube puede figurar en más de un año y el
año identifica la fila editorial concreta. El título puede corregirse en el
CSV, por lo que no sirve como clave; la instantánea conserva un texto útil si
la fila se convierte en huérfana.

**Alternatives considered**:

- Solo `video_id`: descartado porque colapsaría entradas editoriales distintas.
- Título + vídeo: descartado porque las correcciones de título generarían
  duplicados.
- Índice de fila CSV: descartado porque cambia al editar el catálogo.

## R-003 — Entrada y acciones de interfaz

**Decision**: Añadir la carpeta raíz localizada **Favoritos** y acciones de
contexto localizadas para añadir o quitar sobre las canciones.

**Rationale**: La carpeta ofrece recuperación rápida desde el mando sin
sustituir el recorrido décadas → años → canciones. El menú de contexto permite
actuar sobre una canción concreta y cambiar la acción según su estado, sin
añadir pantallas ni controles persistentes.

**Alternatives considered**:

- Reemplazar las décadas por favoritos: descartado; viola el flujo cronológico.
- Botones o diálogo propio: descartado; añade complejidad a la navegación Kodi.
- Solo un indicador visual: descartado; no satisface la acción explícita de
  añadir/quitar.

## R-004 — Resolución de huérfanos

**Decision**: Aplicar `hide_or_notify`: al listar, resolver cada favorito
contra `catalog.load_year()` y ocultar por defecto los no resolubles; si una
URL conservada o una selección llega a reproducción, avisar amigablemente y
permitir quitarlo.

**Rationale**: La lista normal no se ensucia con entradas que el catálogo ya no
publica, pero la preferencia no se elimina silenciosamente. La notificación
evita un fallo catastrófico en rutas directas o estados intermedios.

**Alternatives considered**:

- Borrar automáticamente el huérfano: descartado porque es una mutación
  irreversible sin confirmación.
- Mostrar siempre todos los huérfanos: descartado; degrada el acceso rápido.
- Fallar al abrir la lista: descartado por FR-008.

## R-005 — Orden de la lista

**Decision**: Mostrar primero los favoritos añadidos más recientemente.

**Rationale**: Es el orden esperado para recuperar descubrimientos recientes y
se obtiene con un campo `added_at` sin introducir orden manual ni carpetas.

**Alternatives considered**:

- Orden alfabético: descartado porque no conserva la intención reciente.
- Orden por año: descartado porque replica el browse y no el uso personal.
- Orden manual: descartado por estar fuera del MVP.

## R-006 — Separación técnica e i18n

**Decision**: Crear `resources/lib/favorites.py` para modelo, validación,
lectura/escritura JSON y resolución contra el catálogo; mantener las rutas,
listados, acciones de contexto y notificaciones en `kodi_plugin.py`. Las
etiquetas y avisos nuevos usarán IDs de cadenas Kodi con equivalentes español e
inglés.

**Rationale**: Mantiene la lógica de datos comprobable con pytest sin importar
`xbmc*`, respeta el desacoplamiento constitucional y evita literales de UI
dispersos. JSON y biblioteca estándar no añaden dependencias binarias.

**Alternatives considered**:

- Concentrar la lógica en `kodi_plugin.py`: descartado por acoplar I/O y UI.
- Introducir una dependencia de persistencia: descartado por YAGNI y la
  restricción de Kodi.
- Textos literales solo en español: descartado; bloquearía la i18n prevista.
