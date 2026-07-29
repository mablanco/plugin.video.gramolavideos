# La Gramola de Videos (Addon para Kodi)

## Introducción

Addon para Kodi que muestra una colección de vídeos musicales encontrados en YouTube de artistas y bandas españolas de los años **80 y 90** (años de catálogo 1980–1999; sin 1994). La ampliación a los 60 y 70 queda como trabajo de contenido futuro, no como promesa del listado actual.

Este es un proyecto **ya existente** (desarrollado y publicado históricamente de forma manual). En esta etapa se está **integrando el uso de IA** en el flujo de desarrollo (asistencia de código, Speckit/constitution, etc.) para modernizar y mantener el addon sin reescribir su propósito. La gobernanza para ese trabajo vive en `.specify/memory/constitution.md`. El `.gitignore` del repositorio está preparado para evitar filtrar secretos, credenciales y artefactos locales de herramientas de IA.

El trabajo del proyecto (documentación y comunicación con el mantenedor) es en **español**. A futuro, la interfaz del addon debe poder mostrarse también en **inglés** (soporte multiidioma).

## Instalación

Descarga el fichero ZIP más reciente e instala el addon. Consulta [http://kodi.wiki/view/HOW-TO:Install_an_Add-on_from_a_zip_file][1] para obtener más detalles acerca de la instalación de addons en Kodi mediante paquetes ZIP.

Este addon depende del plugin de YouTube, que debería instalarse automáticamente si no está ya instalado en Kodi.

## Uso

"La Gramola de Vídeos" es accesible desde el menú de addons de vídeo de Kodi. Una vez abierto, muestra **décadas** con catálogo (p. ej. Años 80, Años 90); al entrar en una década aparecen los **años** con CSV; cada año lista las **canciones** que se reproducen vía YouTube.

## Desarrollo y tests

En el host (Python 3), instala las dependencias de desarrollo y ejecuta la suite. **No** declares `pytest` en `addon.xml` (solo tooling de mantenedor).

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

`python -m pytest -q` es la vía principal de verificación del refactor (stubs Kodi, sin abrir Kodi). La reproducción real vía YouTube en Kodi sigue siendo smoke manual residual. En GitHub Actions, el workflow **Tests** ejecuta la misma suite en cada push/PR a `main`.

La rama por defecto del repositorio es **`main`**. El trabajo se hace en ramas feature y se integra mediante pull request (sin push directo a `main`).

## FAQ

**¿Está disponible este addon en un repositorio de Kodi?** No, pero puede que en el futuro. Si alguien quiere echar una mano en el proceso, estaré encantado de recibir su ayuda.

**¿Puedo añadir más vídeos? ¿Cómo?** Sí, es completamente posible. Basta con editar los ficheros CSV incluidos en el código del addon en la ruta `resources/csv`. En cada fila hay dos campos, el nombre del vídeo (formato: artista - canción) y el código de YouTube del mismo. Cada campo debe estar separado por un punto y coma (;).

**¿Por qué un vídeo no se reproduce?** Suele ser porque el id de YouTube es privado, se retiró o YouTube exige iniciar sesión. La gramola muestra un aviso en esos casos; conviene sustituir el id en el CSV por uno público del mismo tema.

## TODO

- Añadir más vídeos musicales (¿alguien se anima?), en particular de los 60 y 70 si se quiere ampliar el arco editorial.
- Opcional: rellenar el hueco de 1994 si aparece material adecuado.

El listado de décadas/años solo descubre los ficheros `YYYY.csv` (sin leer su contenido); al abrir un año se carga únicamente ese CSV.

## Licencia

Este software se distribuye libremente bajo la [licencia GPL 3.0][2].

[1]: http://kodi.wiki/view/HOW-TO:Install_an_Add-on_from_a_zip_file
[2]: http://www.gnu.org/licenses/gpl-3.0.html
