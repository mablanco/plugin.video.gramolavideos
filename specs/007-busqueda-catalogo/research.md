# Investigación: búsqueda local en el catálogo

**Fecha**: 2026-07-29  
**Ámbito**: MVP local y offline de `007-busqueda-catalogo`.

## R-001 — Alcance y regla de coincidencia

**Decisión**: Buscar una subcadena sin distinguir mayúsculas/minúsculas en
`MusicVideo.title`. Ese título editorial ya contiene `Artista - Canción`, por
lo que cubre ambos campos sin modificar el CSV ni duplicar su análisis.

**Razonamiento**: `catalog.py` valida y entrega títulos completos desde los CSV
por año; una comparación `casefold()` de la consulta normalizada contra
`title.casefold()` es suficiente para el MVP y funciona con artistas y
canciones. Se elimina el espacio exterior de la consulta antes de buscar.

**Alternativas consideradas**:

- Separar artista y canción en el CSV o en un modelo nuevo: no aporta valor al
  caso de uso y cambia innecesariamente la fuente editorial.
- Búsqueda remota de YouTube: queda fuera de alcance y cambiaría el ámbito de
  `local_catalog`.
- Fuzzy matching, sinónimos o ranking: aumentan complejidad y son innecesarios
  para localizar un fragmento conocido.

## R-002 — Carga y coste de exploración

**Decisión**: Añadir la lógica de búsqueda a `catalog`, iterando
`list_years(csv_dir)` y llamando a `load_year(csv_dir, year.id)` para cada
año. Acumular los vídeos válidos que coincidan y también los errores de lectura
o de filas.

**Razonamiento**: reutiliza las rutas de validación existentes, conserva CSV
como fuente única y mantiene `xbmc*` fuera de la lógica de datos. Abrir hasta
unas 40 hojas CSV pequeñas al iniciar una búsqueda es aceptable para la escala
del addon y sucede solo bajo una acción explícita del usuario. No se introduce
índice persistente ni caché en el MVP.

**Alternativas consideradas**:

- Índice precargado o SQLite: requiere invalidación al editar CSV y añade
  estado sin una necesidad de rendimiento demostrada.
- Lógica inline en `kodi_plugin`: viola el desacoplamiento de datos y UI de la
  constitution.
- API separada que no reutilice `load_year`: duplicaría parsing y manejo de
  errores.

## R-003 — Forma y orden de los resultados

**Decisión**: El resultado primario será un ítem de canción reproducible,
usando el mismo `mode=song` y `video_id` que el listado anual. El año se
mostrará como contexto en la etiqueta o información del ítem (por ejemplo,
`Artista - Canción (1984)`), sin convertir el resultado en una carpeta.

Los resultados se ordenan alfabéticamente, sin distinguir mayúsculas/minúsculas,
por el título editorial y, ante empate, por `year_id` y `video_id`. El MVP
expone como máximo **100 resultados** después de ordenar.

**Razonamiento**: la reproducción directa cierra el recorrido del usuario con
una pulsación y conserva exactamente el resolver de YouTube existente. El
contexto del año evita ambigüedad entre títulos repetidos. El tope mantiene el
directorio navegable con mando sin paginación.

**Alternativas consideradas**:

- Enlazar solo a la carpeta del año: añade pasos al flujo principal de la
  búsqueda.
- Ordenar por año o mantener el orden de archivos: resulta menos predecible
  para quien busca por nombre.
- Sin límite: puede crear listados poco manejables; paginación queda fuera del
  MVP.

## R-004 — Flujo Kodi y consultas vacías

**Decisión**: La raíz incorporará la carpeta **Buscar** junto a las décadas y,
si la feature 006 está disponible, Favoritos. `mode=search` abrirá el teclado
de Kodi; una consulta válida navega a `mode=search_results&q=<consulta>`.
`mode=search_results` muestra el directorio de canciones o un estado vacío
comprensible.

Una consulta cancelada, vacía o formada solo por espacios termina el flujo sin
mostrar el catálogo completo ni crear resultados artificiales.

**Razonamiento**: separa la interacción con `xbmcgui.Dialog().input` de la
consulta pura, conserva URLs reproducibles y evita que pulsar Buscar se
convierta accidentalmente en un listado total.

**Alternativas consideradas**:

- Ejecutar la búsqueda ya en `mode=search` sin URL de resultado: dificulta
  navegación, pruebas y contratos.
- Tratar vacío como `match all`: contradice los edge cases y produce una lista
  extensa sin intención del usuario.

## R-005 — Secuenciación de producto

**Decisión**: La búsqueda es independiente de Favoritos y se recomienda
implementarla después de `004-catalogo-60-70` (o cuando exista una semilla
amplia) y sobre la navegación de `003`.

**Razonamiento**: una base de catálogo más amplia hace visible el valor de
buscar; no obstante, la ruta, los datos y las pruebas no requieren que exista
Favoritos.
