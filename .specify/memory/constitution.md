<!--
Sync Impact Report
- Version change: 1.2.1 → 1.3.0
- Modified principles:
  - IV. Simplicidad del plugin: flujo años→canciones→play → décadas→años→canciones→play
    (décadas derivadas del catálogo CSV por año; año sigue siendo unidad de datos)
- Added / clarified:
  - Restricciones técnicas: listados coherentes con flujo décadas→años→canciones
- Removed sections: none
- Templates requiring updates:
  - README.md (flujo de uso) — con feature 003
  - specs/003 contracts/plugin-navigation.md — contrato v2
- Follow-up TODOs: none
- Prior (1.2.0 → 1.2.1): Speckit project state vs regenerable tooling; ignore feature.json
-->

# La Gramola de Videos Constitution

## Core Principles

### I. Catálogo como datos
El catálogo de vídeos MUST residir en `resources/csv/` como un fichero CSV por año
(nombre de fichero = año, p. ej. `1980.csv`). Cada fila MUST usar el formato
`Artista - Canción;youtube_video_id` con delimitador `;`. Añadir, corregir o
eliminar entradas MUST hacerse editando CSV; el código Python MUST NOT hardcodear
listas de canciones. Rationale: el README documenta este flujo de contribución y
mantiene el plugin separado del contenido.

### II. Reproducción vía YouTube
La reproducción MUST delegarse a `plugin.video.youtube` (p. ej. URI
`plugin://plugin.video.youtube/play/?video_id=...`). El addon MUST NOT descargar,
almacenar ni rehostear ficheros de vídeo. La dependencia MUST declararse en
`addon.xml`. Rationale: el producto es un índice/navegador, no un cliente de
streaming propio.

### III. Alcance editorial
El catálogo MUST centrarse en vídeos musicales de artistas y bandas españolas,
cubriendo aproximadamente las décadas de los 60 a los 90 según la descripción del
addon. Nuevas entradas MUST seguir ese criterio editorial. Entradas fuera de
alcance REQUIRE justificación explícita en la especificación o en el mensaje de
cambio. Rationale: la identidad del producto es esa colección, no un jukebox
genérico.

### IV. Simplicidad del plugin
El addon MUST preservar el flujo de usuario **décadas → años → canciones →
reproducción**, donde las décadas se derivan de los años presentes en el
catálogo (CSV por año) y no sustituyen al año como unidad de datos. Nuevas
capas, frameworks o abstracciones MUST justificarse en Complexity Tracking del
plan. La evolución del código MAY introducir módulos, pero MUST NOT complicar
el producto más allá de lo necesario (YAGNI). Rationale: el listado plano de
años no escala al arco editorial 60s–90s; un único nivel de agrupación por
década mantiene la identidad cronológica sin añadir búsqueda ni taxonomías
paralelas.

### V. Metadatos y versionado del addon
El id del addon MUST permanecer `plugin.video.gramolavideos`. Cambios de
comportamiento, dependencia o catálogo relevantes MUST actualizar la versión en
`addon.xml` y quedar reflejados en el historial de cambios (changelog y/o
commits). Assets referenciados en metadatos (`resources/icon.png`,
`resources/fanart.jpg`) MUST existir. Rationale: convenciones de addons Kodi y
trazabilidad para instaladores.

### VI. Compatibilidad Kodi moderna
El destino técnico MUST ser código compatible con la API de Kodi en Python 3
(Matrix, Nexus, Omega y posteriores). MUST NOT introducirse librerías Python con
módulos binarios en C ajenos al runtime de Kodi o a dependencias declaradas en
`addon.xml`. El código legacy (Python 2 / APIs antiguas) MAY permanecer hasta
que un plan de migración lo reemplace; ese plan MUST documentar riesgos,
compatibilidad y pruebas en Kodi. Rationale: el boceto de constitución del
mantenedor y la viabilidad a largo plazo del addon.

### VII. Desacoplamiento y APIs Kodi
La lógica de datos (lectura de CSV, validación de catálogo, y cualquier acceso
de red futuro) MUST estar separada de la construcción de la interfaz
(`xbmcgui` / listados). El uso de `xbmc`, `xbmcgui`, `xbmcplugin` y
`xbmcaddon` MUST estar encapsulado (módulos dedicados o fachadas), de modo que
la lógica de datos pueda probarse sin lanzar Kodi cuando se añadan tests.
Rationale: desacoplamiento del boceto previo; habilita calidad y refactor
seguro.

### VIII. Tolerancia a fallos
Si el addon realiza I/O de ficheros o red, MUST usar timeouts explícitos donde
aplique y MUST capturar fallos de forma que la UI no se congele ni aborte de
forma catastrófica. Ante errores recuperables, MUST mostrarse una notificación
amigable al usuario (p. ej. diálogo de Kodi). Rationale: robustez ante CSV
corruptos, rutas inexistentes o fuentes externas no disponibles.

### IX. Adopción de IA en un proyecto existente
Este repositorio es un addon ya desarrollado y publicado históricamente sin
flujo de IA. La integración de asistentes de IA (Speckit, agentes de código,
etc.) está adoptándose ahora. Por tanto:

- Documentación orientada a humanos (como mínimo `README.md`) MUST dejar claro
  que el proyecto acepta desarrollo asistido por IA a partir de esta etapa.
- Cambios generados o guiados por IA MUST respetar esta constitution y el
  historial/intención del mantenedor; no reescribir el producto “desde cero”
  sin plan aprobado.
- Artefactos de IA locales, credenciales, prompts con secretos y salidas
  sensibles MUST NOT commitearse (ver sección de seguridad del repositorio).
- El fichero de constitución Speckit (`.specify/memory/constitution.md`) es la
  fuente de gobernanza para trabajo con agentes; borradores externos MAY
  enriquecerla pero no la sustituyen hasta fusionarse aquí.

Rationale: transparencia con colaboradores y preparación segura del repo para
herramientas de IA.

### X. Idioma del proyecto e internacionalización
- La comunicación con el mantenedor (chat, agentes, revisiones) MUST ser en
  **español**.
- Documentación del repositorio orientada a humanos (`README.md`, specs
  escritas para este proyecto, comentarios de producto) MUST priorizar el
  **español** mientras el proyecto sea el idioma principal de trabajo.
- Objetivo futuro: la UI del addon MUST poder mostrarse también en **inglés**
  (soporte multiidioma). Cuando se implemente i18n, MUST usarse el mecanismo
  estándar de Kodi (`resources/language/` / strings `.po` o el formato vigente
  del target Kodi), con al menos `es` e `en` (o `en_gb` según convención del
  addon).
- Hasta que exista i18n, los textos de UI MAY permanecer solo en español; los
  planes que añadan cadenas visibles MUST no bloquear la futura extracción a
  ficheros de idioma (evitar literales dispersos sin ruta clara de migración
  cuando se toque esa zona).

Rationale: el mantenedor y el producto trabajan en español; el alcance
internacional (inglés en pantalla) es un objetivo explícito, no un
requerimiento inmediato de cada cambio.

## Restricciones técnicas

- Entry point: `addon.py` (o el `library` declarado en `addon.xml`) vía
  `xbmc.python.pluginsource`.
- Licencia: GPL-3.0 (MUST preservarse).
- Dependencia de reproducción: `plugin.video.youtube` (versión mínima según
  `addon.xml`).
- Plataforma declarada: `all`.
- Stack permitido: runtime Python de Kodi + addons/módulos declarados en
  `requires`; MUST NOT añadir dependencias binarias no soportadas por Kodi.
- Listados de directorio MUST usar las APIs de plugin de Kodi de forma
  coherente con el flujo décadas → años → canciones.

## Flujo de contribución de contenido

1. Editar o crear el CSV del año en `resources/csv/`.
2. Verificar que el `youtube_video_id` reproduce el vídeo correcto.
3. Mantener el título en formato `Artista - Canción`.
4. Si el cambio es significativo para usuarios, subir versión en `addon.xml` y
   anotar el cambio.
5. No commitear secretos ni URLs de tracking ajenas al id de YouTube.

## Seguridad del repositorio e higiene de secretos

- El repositorio MUST mantener un `.gitignore` que excluya secretos y material
  local sensible: ficheros `.env`, claves API, tokens, credenciales de
  proveedores de IA, certificados privados, y cachés/artefactos locales de
  agentes que puedan contener datos privados.
- MUST NOT commitear contraseñas, tokens, cookies de sesión, ni dumps de
  conversaciones que incluyan secretos.
- Antes de añadir tooling de IA o CI, revisar que no se filtren paths de
  configuración local del mantenedor.
- Los CSV del catálogo son datos públicos del addon; no son secretos. Los
  secretos son credenciales y configuración privada del entorno de desarrollo.
- Speckit: MUST versionar el **estado del proyecto** (p. ej. `memory/`,
  `templates/`, `extensions.yml`, `init-options.json`, `integration.json`,
  `.cursor/rules/`) y MUST NOT versionar **tooling regenerable** (p. ej.
  `.cursor/skills/`, `.specify/scripts/`, `workflows/`, `integrations/`,
  `extensions/`) ni el puntero de sesión `.specify/feature.json`. Ese tooling
  se restaura con `specify init` / instalación de extensiones.

## Governance

Esta constitution prevalece sobre hábitos ad hoc del repositorio y sobre
borradores externos no fusionados. Las enmiendas MUST:

1. Actualizar `.specify/memory/constitution.md` con principios claros y
   comprobables (MUST/SHOULD).
2. Incrementar la versión (MAJOR: redefinición incompatible; MINOR: nuevo
   principio/sección; PATCH: aclaraciones).
3. Poner `Last Amended` en fecha ISO `YYYY-MM-DD` y propagar impacto a
   plantillas Speckit, README y `.gitignore` cuando aplique.
4. Verificar cumplimiento en el Constitution Check de cada plan de feature
   antes de Phase 0 y de nuevo tras Phase 1.

PRs y revisiones MUST comprobar: formato CSV, dependencia YouTube, alcance
editorial, dirección de compatibilidad Kodi/Python 3, desacoplamiento cuando
se toque arquitectura, ausencia de secretos en el diff, idioma/i18n cuando
aplique, y complejidad justificada. Guidance operativa: `README.md` y esta
constitution.

**Version**: 1.3.0 | **Ratified**: 2026-07-25 | **Last Amended**: 2026-07-29
