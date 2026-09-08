# Investigación: año visible en el listado de canciones

## R-001 — Contexto visible del año

**Decision**: En la rama `mode=year` de `resources/lib/kodi_plugin.py`, llamar a
`xbmcplugin.setPluginCategory(handle, year_id)` antes de añadir las canciones.

**Rationale**: `setPluginCategory` es la API estándar de Kodi para declarar la
categoría o cabecera contextual del listado activo. El valor ya está disponible
como `year_id`, no exige datos nuevos y Kodi puede presentarlo como parte de la
navegación de la vista. Al ejecutarse para cada entrada en un año, el contexto se
actualiza y no conserva el año visitado previamente.

**Alternatives considered**:

- Prefijar cada título con el año, por ejemplo `1985 — Artista - Canción`:
  rechazado. Contradice la asunción de la especificación, duplica información en
  todas las filas y modifica la presentación editorial de cada canción.
- Crear un `ListItem` o directorio intermedio solo para el año: rechazado.
  Añadiría navegación y vulneraría el flujo vigente décadas → años → canciones →
  reproducción.
- Añadir una capa propia de UI: rechazado. No es necesaria cuando Kodi ofrece la
  API de categoría y aumentaría complejidad.

## R-002 — Contexto de década

**Decision**: No establecer la categoría con la etiqueta de década en
`mode=decade` en esta feature.

**Rationale**: El requisito P1 se limita al listado de canciones dentro de un
año. Aunque `setPluginCategory(handle, decade_label(decade_id))` sería
compatible con el patrón, ampliar el contexto a la vista de años queda fuera de
alcance.

**Alternatives considered**:

- Mostrar también la década como categoría al listar sus años: diferido. Puede
  evaluarse como mejora opcional en una feature posterior, sin condicionarla a
  este MVP.

## R-003 — Alcance de implementación y pruebas

**Decision**: Limitar el cambio de runtime a la rama `mode=year` de
`resources/lib/kodi_plugin.py` y añadir o ajustar una prueba unitaria de wiring.

**Rationale**: La categoría recibe el identificador de año ya extraído de
`foldername`; no se modifica el catálogo, las URL, la reproducción ni la
estructura de navegación. Un stub de `xbmcplugin` permite comprobar la llamada
sin ejecutar Kodi.

**Alternatives considered**:

- Crear un modelo persistido para recordar la última categoría: rechazado. El
  contexto pertenece a la invocación actual y Kodi administra la presentación.
- Cambiar la query string o añadir un parámetro de categoría: rechazado. El
  contrato vigente `mode=year&foldername=<YYYY>` ya contiene el valor necesario.
