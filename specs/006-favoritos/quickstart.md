# Quickstart de validación: Favoritos

Esta guía valida el contrato de navegación y el modelo de datos; no sustituye
las pruebas unitarias previstas.

## Prerrequisitos

- Entorno Python con `pytest` disponible.
- Checkout del addon con `resources/csv/` y el directorio de pruebas.
- Kodi Matrix, Nexus u Omega con `plugin.video.gramolavideos` y
  `plugin.video.youtube` instalados para el smoke manual.
- Un perfil Kodi de prueba, para no mezclar preferencias personales.

## Pruebas automatizadas

Desde la raíz del repositorio:

```bash
pytest -q
```

Añadir o ejecutar específicamente las pruebas de `favorites.py` y del wiring
de `kodi_plugin` debe comprobar:

1. añadir una `CatalogEntry` válida crea el JSON y una segunda adición de la
   misma pareja `(year_id, video_id)` no duplica la entrada;
2. cargar una nueva instancia del store conserva el favorito y su orden;
3. `remove` quita solo la preferencia y no toca el CSV;
4. un favorito cuyo año o vídeo ya no resuelve se clasifica como huérfano y no
   aparece entre los activos;
5. las URLs y acciones de contexto usan los parámetros de
   [plugin-navigation.md](contracts/plugin-navigation.md).

## Smoke manual Kodi

1. Iniciar el addon y confirmar que la raíz contiene **Favoritos** además de
   las décadas; abrir una década, un año y una canción para confirmar que el
   browse habitual sigue funcionando.
2. Abrir un año, mostrar el menú contextual de una canción y elegir **Añadir a
   favoritos**. Confirmar la notificación de éxito y la acción posterior de
   quitar.
3. Volver a la raíz, abrir **Favoritos** y comprobar que aparece la canción
   con título comprensible. Seleccionarla y confirmar que reproduce mediante
   el mismo addon YouTube que desde su año.
4. Cerrar y abrir de nuevo el addon en el mismo perfil. Confirmar que el
   favorito continúa listado.
5. Desde Favoritos (o desde el año), elegir **Quitar de favoritos**. Confirmar
   que desaparece de Favoritos, el estado vacío es claro si era el último, y
   la canción permanece en su CSV/año.
6. Con una copia del perfil de prueba, conservar un favorito y retirar
   temporalmente su fila o CSV. Abrir Favoritos: no debe aparecer ni cerrar el
   addon. Si se intenta seguir una URL de favorito previamente emitida, debe
   mostrarse un aviso amigable y poder quitarse la preferencia.

Restaurar cualquier CSV modificado durante el smoke. No se debe confirmar ni
distribuir el `favorites.json` del perfil de prueba.
