# La Gramola de Videos (Addon para Kodi)

## Introducción

Addon para Kodi que muestra una colección de vídeos musicales encontrados en YouTube de artistas y bandas españolas de los años **60, 70, 80 y 90** (años de catálogo con semilla 1964–1979 más 1980–1999; sin 1994). El proceso para ampliar la semilla 60/70 está en [docs/seed-60-70.md](docs/seed-60-70.md).

Este es un proyecto **ya existente** (desarrollado y publicado históricamente de forma manual). En esta etapa se está **integrando el uso de IA** en el flujo de desarrollo (asistencia de código, Speckit/constitution, etc.) para modernizar y mantener el addon sin reescribir su propósito. La gobernanza para ese trabajo vive en `.specify/memory/constitution.md`. El `.gitignore` del repositorio está preparado para evitar filtrar secretos, credenciales y artefactos locales de herramientas de IA.

El trabajo del proyecto (documentación y comunicación con el mantenedor) es en **español**. A futuro, la interfaz del addon debe poder mostrarse también en **inglés** (soporte multiidioma).

## Instalación

Descarga el fichero ZIP más reciente e instala el addon. Consulta [http://kodi.wiki/view/HOW-TO:Install_an_Add-on_from_a_zip_file][1] para obtener más detalles acerca de la instalación de addons en Kodi mediante paquetes ZIP.

Este addon depende del plugin de YouTube, que debería instalarse automáticamente si no está ya instalado en Kodi.

## Uso

"La Gramola de Vídeos" es accesible desde el menú de addons de vídeo de Kodi. Una vez abierto, muestra en pantalla una lista de años que contienen a su vez enlaces a los vídeos en YouTube.

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

**¿Puedo añadir más vídeos? ¿Cómo?** Sí. Edita (o crea) un fichero `resources/csv/YYYY.csv`. Cada fila tiene dos campos separados por `;`: título (`Artista - Canción`) e id de YouTube. Cronometrado en seco: añadir una fila válida suele llevar menos de 5 minutos. Para regenerar o ampliar la **semilla 60/70** de forma asistida, sigue [docs/seed-60-70.md](docs/seed-60-70.md) y el contrato [specs/004-catalogo-60-70/contracts/seed-process.md](specs/004-catalogo-60-70/contracts/seed-process.md) (solo en el host; nunca en runtime Kodi).

**¿Por qué un vídeo no se reproduce?** Suele ser porque el id de YouTube es privado, se retiró o YouTube exige iniciar sesión. La gramola muestra un aviso en esos casos; conviene sustituir el id en el CSV por uno público del mismo tema.

## TODO

- Seguir ampliando el catálogo (más filas 60–90) siguiendo el FAQ / runbook de semilla.
- Opcional: rellenar el hueco de 1994 si aparece material adecuado.

El listado de años solo descubre los ficheros `YYYY.csv` (sin leer su contenido); al abrir un año se carga únicamente ese CSV.

## Licencia

Este software se distribuye libremente bajo la [licencia GPL 3.0][2].

[1]: http://kodi.wiki/view/HOW-TO:Install_an_Add-on_from_a_zip_file
[2]: http://www.gnu.org/licenses/gpl-3.0.html
