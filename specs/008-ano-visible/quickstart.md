# Guía de validación: año visible

## Prerrequisitos

- Entorno de pruebas Python del repositorio con los stubs de `xbmcplugin`.
- Kodi Matrix, Nexus u Omega con el addon instalado para el smoke manual.
- Un año del catálogo con al menos una canción, por ejemplo `1985`.

## Prueba unitaria de wiring

1. Añadir una prueba en `tests/unit/test_plugin_wiring.py` (o el módulo de
   wiring equivalente) que ejecute:

   ```python
   _run_addon("mode=year&foldername=1985")
   ```

2. Obtener las llamadas del stub:

   ```python
   categories = xbmcplugin.calls_named("setPluginCategory")
   assert len(categories) == 1
   assert categories[0]["kwargs"]["handle"] == 1
   assert categories[0]["kwargs"]["category"] == "1985"
   ```

3. Ejecutar la prueba junto con la suite:

   ```bash
   pytest tests/unit/test_plugin_wiring.py
   ```

**Resultado esperado**: la categoría se establece una vez con el año solicitado,
sin cambiar las URL ni las propiedades reproducibles de las canciones. Véase el
[contrato de navegación](./contracts/plugin-navigation.md).

## Smoke manual en Kodi

1. Abrir la Gramola de Videos.
2. Entrar en una década y seleccionar un año conocido.
3. Confirmar que el listado de canciones muestra `1985` (o el año elegido) como
   categoría/cabecera visible de la vista.
4. Desplazarse por varias canciones y comprobar que el año sigue siendo
   identificable.
5. Volver atrás y abrir otro año; comprobar que la categoría cambia al nuevo
   año.
6. Reproducir una canción y volver atrás; el flujo no debe añadir pantallas ni
   modificar la reproducción.

**Resultado esperado**: el año seleccionado se percibe en pantalla sin prefijar
los títulos de canciones ni crear niveles de navegación nuevos.
