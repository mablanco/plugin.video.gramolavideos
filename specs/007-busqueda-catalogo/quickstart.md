# Quickstart de validación: búsqueda en catálogo

## Prerrequisitos

- Estar en una copia del addon con el catálogo CSV disponible en
  `resources/csv/`.
- Tener Python 3 y `pytest` para las pruebas unitarias.
- Para el smoke, instalar el addon en Kodi Matrix, Nexus u Omega con
  `plugin.video.youtube` disponible.

## Pruebas unitarias

Añadir casos centrados en `catalog.search` y en el cableado de
`kodi_plugin.run`:

1. Buscar un fragmento de artista y otro de canción de una fila conocida:
   ambos devuelven el mismo `MusicVideo`.
2. Repetir con capitalización distinta y comprobar que la coincidencia es
   idéntica.
3. Probar `""`, espacios y una cancelación simulada: devuelven cero resultados
   y no llaman a cargas de todos los años.
4. Crear coincidencias repartidas entre años y verificar orden por título,
   desempate por año/ID y máximo de 100 filas.
5. Incluir una fila o CSV inválido: conserva coincidencias válidas y expone
   el error recuperable.
6. Comprobar que la raíz incluye `mode=search`; una query válida genera
   `mode=search_results&q=...`; cada resultado usa `mode=song` y es
   reproducible, no carpeta.

Ejecutar:

```bash
python3 -m pytest tests/unit -q
```

Resultado esperado: todas las pruebas existentes y las nuevas pasan, sin
importar módulos `xbmc*` desde `catalog.py`.

## Smoke manual Kodi

1. Abrir el addon y confirmar que la raíz conserva las décadas y muestra
   **Buscar**; si existe, Favoritos también permanece disponible.
2. Abrir Buscar, introducir parte de un artista o canción conocido y confirmar
   que aparece una fila con título claro y año opcional.
3. Seleccionar la fila y comprobar que reproduce mediante el mismo flujo
   YouTube que desde su año.
4. Buscar el mismo término con otra combinación de mayúsculas/minúsculas y
   confirmar el mismo conjunto ordenado alfabéticamente.
5. Buscar un texto inexistente y comprobar un estado vacío comprensible, sin
   error opaco.
6. Cancelar el teclado y probar una query formada solo por espacios; en ambos
   casos no debe abrirse un listado de todo el catálogo.
7. Usar un término amplio y verificar que hay como máximo 100 filas y que la
   navegación con mando sigue siendo fluida.

Registrar cualquier error recuperable de CSV o reproducción como notificación
amigable; no debe cerrar ni bloquear el addon.
