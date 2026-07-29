# Feature Specification: Mejorar la navegación del catálogo de vídeos

**Feature Branch**: `[003-navegacion-videos]`

**Created**: 2026-07-29

**Status**: Draft

**Input**: User description: "quiero mejorar el sistema de navegacion por los videos. actualmente tenemos un listado enorme ordenado por años que puede crecer aun mas si se incluyen los 60 y los 70. una opcin podria ser meter un primer nivel por decada y un segundo por año. quiero por tanto realizar un estudio de la mejor opcion de nevagacion por los videos e impoementarla"

## Contexto y problema

La Gramola de Vídeos es un índice/navegador: el oyente abre el addon, elige un
año y luego una canción para reproducir. Hoy el **primer nivel** es un listado
plano de todos los años disponibles (aprox. 1980–1999, sin 1994). Ese listado
ya es largo y **crecerá** si se incorporan las décadas de los 60 y los 70 que el
producto promete editorialmente.

El problema de producto es: **¿cómo organizar la navegación del catálogo para
que siga siendo fácil de recorrer en mando/TV cuando haya muchas más carpetas de
año?** Una opción candidata es **década → año → canciones → reproducir**; otras
pueden ser mejores según criterios de simplicidad, familiaridad y escalabilidad.

Esta feature tiene **dos fases de valor**: (1) **estudiar y decidir** el modelo
de navegación, y (2) **implementarlo** en el addon según el veredicto, sin
cambiar el modelo de datos del catálogo ni la reproducción por YouTube.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Decidir el modelo de navegación (Priority: P1)

Como mantenedor, necesito un veredicto documentado que compare opciones de
navegación del catálogo (incluida la propuesta década → año y al menos otras
alternativas razonables), con criterios claros y una recomendación accionable.

**Why this priority**: Sin decisión fundamentada se arriesga complicar el
producto o elegir una jerarquía que no escale ni encaje con el mando de TV.

**Independent Test**: Leer el documento de decisión y comprobar que evalúa ≥3
opciones bajo los mismos criterios, declara un ganador (o “mantener status quo
con mitigaciones”) y lista el impacto en la experiencia del usuario y en la
gobernanza del proyecto.

**Acceptance Scenarios**:

1. **Given** el listado plano actual de años y la expectativa de ampliar a 60s/70s, **When** se completa el estudio, **Then** existe un documento de decisión con al menos tres opciones evaluadas (p. ej. listado plano, década→año, y otra alternativa) bajo criterios comunes.
2. **Given** ese documento, **When** un revisor lo lee, **Then** entiende por qué se elige una opción, qué queda fuera de alcance y si hace falta actualizar el flujo de producto documentado (años → canciones → reproducir).
3. **Given** la opción ganadora, **When** se publica el veredicto, **Then** describe el recorrido de usuario completo hasta reproducir una canción y cómo se comportan años sueltos o décadas incompletas.

---

### User Story 2 - Recorrer el catálogo con la navegación elegida (Priority: P1)

Como oyente con mando de TV, quiero llegar a una canción de un año concreto
sin desplazarme por un listado inmanejable de décadas enteras de años, usando
solo la jerarquía decidida en el estudio.

**Why this priority**: Es el valor tangible para el usuario final; justifica la
implementación tras la decisión.

**Independent Test**: En Kodi, abrir el addon, seguir el recorrido documentado
hasta un año conocido y reproducir una canción válida; medir que el número de
pasos y el tamaño de cada listado encajan con lo prometido en el veredicto.

**Acceptance Scenarios**:

1. **Given** el addon con la navegación implementada y el catálogo actual, **When** el usuario abre la gramola, **Then** ve el primer nivel definido por el veredicto (no un listado plano de todos los años si ese modelo fue descartado).
2. **Given** un año que existe en el catálogo, **When** el usuario lo selecciona tras el recorrido previsto, **Then** ve las canciones de ese año y puede reproducir una entrada válida.
3. **Given** el catálogo ampliado hipotéticamente a años de los 60 y 70, **When** se aplica la misma jerarquía, **Then** el primer nivel sigue siendo manejable (pocas entradas agrupadoras o un criterio equivalente documentado) sin exigir un listado único de ~40 años.

---

### User Story 3 - Volver atrás y orientarse sin perder el contexto (Priority: P2)

Como oyente, quiero poder subir de nivel (p. ej. de canciones a año, de año a
década o al raíz) con el comportamiento habitual de “atrás” en Kodi y entender
en qué punto del catálogo estoy.

**Why this priority**: En TV, perderse en la jerarquía anula la mejora de
navegación.

**Independent Test**: Entrar dos o tres niveles, usar atrás hasta la raíz y
comprobar que los títulos/etiquetas de carpeta coinciden con el modelo
decidido.

**Acceptance Scenarios**:

1. **Given** el usuario dentro de la lista de canciones de un año, **When** usa atrás, **Then** vuelve al listado del nivel padre inmediato (año o agrupación superior según el modelo).
2. **Given** el usuario en un nivel intermedio (si existe), **When** usa atrás de nuevo, **Then** llega a la raíz del addon sin pantallas vacías ni bucles.
3. **Given** cada nivel del recorrido, **When** el usuario mira el listado, **Then** las etiquetas son comprensibles en español (p. ej. “Años 80”, “1985”) y coherentes con el veredicto.

---

### User Story 4 - Preservar catálogo y reproducción (Priority: P2)

Como mantenedor, quiero que la nueva navegación sea solo una forma de
presentar el catálogo existente: los CSV por año siguen siendo la fuente de
verdad y la reproducción sigue delegada en YouTube, sin rehostear vídeo ni
hardcodear listas de canciones.

**Why this priority**: Protege la identidad del producto y los límites ya
asumidos; evita que “mejorar el menú” se convierta en un rediseño de datos o
de streaming.

**Independent Test**: Revisar el veredicto y la implementación: mismos CSV por
año, mismas filas, misma delegación de reproducción; ningún cambio de formato
de catálogo exigido solo por la UI.

**Acceptance Scenarios**:

1. **Given** los CSV actuales por año, **When** se implementa la navegación, **Then** no hace falta renombrar ni fusionar ficheros de catálogo para que el menú funcione.
2. **Given** una canción listada, **When** el usuario la reproduce, **Then** el comportamiento de reproducción permanece el ya establecido (proveedor YouTube / flujo actual del addon).
3. **Given** una opción de navegación que exigiría otro almacenamiento o rehosteo, **When** se evalúa en el estudio, **Then** se descarta o se marca incompatible con los principios del proyecto.

---

### Edge Cases

- Año presente en el catálogo pero década “incompleta” (faltan otros años de esa década): la agrupación debe mostrar solo lo disponible, sin inventar años vacíos salvo que el veredicto lo justifique explícitamente.
- Catálogo con un solo año o una sola década: la jerarquía no debe obligar a pasos inútiles; el estudio debe indicar si se colapsa o se mantiene la estructura fija.
- Años fuera de una década “redonda” o etiquetado ambiguo (p. ej. límites 1960–1969 vs “años 60”): el veredicto fija la regla de agrupación.
- Listado vacío en un nivel (carpeta sin hijos tras filtrar errores): el usuario recibe un listado vacío usable o un aviso comprensible, sin abortar el addon.
- Ampliación futura del catálogo a 60s/70s: la navegación elegida debe seguir siendo usable sin un rediseño inmediato.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El proyecto MUST documentar un estudio de navegación que compare al menos tres opciones, una de ellas siendo **década → año → canciones → reproducir**, otra el **listado plano de años** (status quo), y al menos una tercera alternativa razonable (p. ej. agrupación por rangos distintos, acceso directo a años recientes + archivo, u otra justificada en el estudio).
- **FR-002**: El estudio MUST usar criterios explícitos y comunes (como mínimo: facilidad con mando/TV, número de pasos hasta una canción, escalabilidad al añadir 60s/70s, simplicidad del producto, y coherencia con la identidad de la gramola).
- **FR-003**: El estudio MUST producir un veredicto accionable (opción elegida o mantenimiento del status quo con mitigaciones) y MUST indicar si el flujo de producto documentado necesita actualizarse.
- **FR-004**: Tras el veredicto, el addon MUST implementar la navegación elegida de forma que el usuario pueda llegar desde la raíz del addon hasta reproducir una canción del catálogo.
- **FR-005**: Los listados de cada nivel MUST derivarse del catálogo existente (años presentes como datos), sin hardcodear la lista de canciones en el código.
- **FR-006**: La implementación MUST NOT exigir cambiar el formato ni la ubicación de los CSV por año como condición para navegar.
- **FR-007**: La reproducción MUST seguir el modelo de producto ya vigente (delegación externa; sin descargar ni rehostear vídeo).
- **FR-008**: La navegación MUST comportarse de forma predecible con “atrás” en Kodi: cada nivel tiene un padre claro hasta la raíz.
- **FR-009**: Las etiquetas visibles de los niveles de navegación MUST estar en español y ser comprensibles para un oyente no técnico (p. ej. década y año recognoscibles).
- **FR-010**: Si un nivel no tiene entradas utilizables, el addon MUST mostrar un resultado vacío o un aviso comprensible sin fallo catastrófico.
- **FR-011**: El diseño elegido MUST seguir siendo usable si el catálogo pasa a incluir años de los 60 y 70 (escala objetivo del estudio), aunque **añadir esas entradas al catálogo** queda fuera del alcance de esta feature.
- **FR-012**: Cualquier cambio del flujo de usuario respecto al modelo “años → canciones → reproducir” MUST quedar reflejado en la documentación de producto / gobernanza que el veredicto indique como necesaria antes o junto a la implementación.

### Key Entities

- **Año**: unidad de catálogo ya existente; corresponde a un conjunto de vídeos de un año civil presente en los datos.
- **Agrupación de navegación**: nivel opcional por encima del año (p. ej. década) definido por el veredicto; no sustituye al Año como fuente de datos.
- **Vídeo musical**: entrada del catálogo (título + identificador de reproducción) perteneciente a un Año.
- **Nivel de listado**: pantalla de directorio en el addon (raíz, agrupación, año o canciones) según el modelo elegido.
- **Veredicto de navegación**: documento de decisión con opciones, criterios, ganador e implicaciones de gobernanza/UX.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: El estudio entrega un veredicto en el que ≥3 opciones se evalúan con los mismos criterios y una recomendación clara en un único documento revisable.
- **SC-002**: Con la navegación implementada, un oyente llega desde la apertura del addon hasta la lista de canciones de un año conocido en **como máximo el número de pasos de directorio** definido en el veredicto (y en ningún caso más de 3 pasos de carpeta antes de ver canciones).
- **SC-003**: En el primer nivel visible tras abrir el addon, el número de entradas es **≤ 12** con el catálogo actual y **sigue ≤ 12** en el escenario proyectado 1960–1999 (o el techo equivalente que fije el veredicto si el modelo no es por décadas).
- **SC-004**: El 100 % de los años presentes en el catálogo siguen siendo alcanzables (ningún año existente queda oculto o inaccesible tras el cambio).
- **SC-005**: En una prueba manual en Kodi, el recorrido feliz (raíz → … → año → canción → reproducción iniciada) se completa en **menos de 30 segundos** en condiciones de red normales, igual que la expectativa previa del producto.
- **SC-006**: Un revisor no técnico puede explicar, tras leer etiquetas en pantalla, en qué agrupación y año se encuentra, en una comprobación informal sin ayuda del mantenedor.

## Assumptions

- El dolor principal es la **escala del listado de años**, no la búsqueda por artista/título ni favoritos; esas capacidades quedan **fuera de alcance** salvo que el estudio las mencione solo como “no elegidas”.
- **Incorporar contenido** de los 60 y 70 (nuevos CSV/filas) **no** forma parte de esta feature; sí forma parte del criterio de diseño el que la navegación **escale** cuando ese contenido exista.
- La opción “década → año” es **candidata**, no decisión previa; el veredicto puede elegir otra si los criterios lo justifican.
- Se mantiene el catálogo como CSV por año y la reproducción delegada; esta feature no reabre el debate de proveedor de streaming salvo para afirmar que no cambia.
- Si el modelo ganador introduce un nivel por encima de “año”, se asume que habrá que **actualizar** el flujo de producto documentado (hoy “años → canciones → reproducir”) como parte del trabajo de esta feature, no como un proyecto aparte bloqueante indefinido.
- El público objetivo sigue siendo oyente en TV/salón con mando; la simplicidad prima sobre filtros avanzados.
- Un único mantenedor valida el veredicto antes de implementar; no se requiere estudio de usuarios externo formal (basta smoke manual y revisión del documento).
