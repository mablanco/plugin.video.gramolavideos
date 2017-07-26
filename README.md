# La Gramola de Videos (Addon para Kodi)

## Introducción

Addon para Kodi que muestra una colección de vídeos musicales encontrados en YouTube de artistas y bandas españolas desde los 60 a los 90.

## Instalación

Descarga el fichero ZIP más reciente e instala el addon. Consulta [http://kodi.wiki/view/HOW-TO:Install_an_Add-on_from_a_zip_file][1] para obtener más detalles acerca de la instalación de addons en Kodi mediante paquetes ZIP.

Este addon depende del plugin de YouTube, que debería instalarse automáticamente si no está ya instalado en Kodi.

## Uso

"La Gramola de Vídeos" es accesible desde el menú de addons de vídeo de Kodi. Una vez abierto, muestra en pantalla una lista de años que contienen a su vez enlaces a los vídeos en YouTube.

## FAQ

**¿Está disponible este addon en un repositorio de Kodi?** No, pero puede que en el futuro. Si alguien quiere echar una mano en el proceso, estaré encantado de recibir su ayuda.

**¿Puedo añadir más vídeos? ¿Cómo?** Sí, es completamente posible. Basta con editar los ficheros CSV incluidos en el código del addon en la ruta `resources/csv`. En cada fila hay dos campos, el nombre del vídeo (formato: artista - canción) y el código de YouTube del mismo. Cada campo debe estar separado por un punto y coma (;).

## TODO

- Añadir más vídeos musicales (¿alguien se anima?)
- Las listas de vídeos se leen desde ficheros CSV cada vez que se accede al listado de años, lo cual dista de ser óptimo.
- Estas listas se guardan en un diccionario de listas, que hay que ordenar cada vez que se accede al listado de años, lo cual tampoco es lo más adecuado.

## Licencia

Este software se distribuye libremente bajo la [licencia GPL 3.0][2].

[1]: http://kodi.wiki/view/HOW-TO:Install_an_Add-on_from_a_zip_file
[2]: http://www.gnu.org/licenses/gpl-3.0.html
