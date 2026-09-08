# Feature Specification: Año visible al entrar en un año

**Feature Branch**: `[008-ano-visible]`

**Created**: 2026-07-29

**Status**: Draft

**Input**: User description: "me gustaria que se viese en pantalla el año en el
que se está cuanto se entra en uno"

## Contexto y problema

Tras elegir un año en la gramola, el oyente ve el listado de canciones de ese
año. En pantalla no queda claro de forma persistente **en qué año se está**:
solo aparecen títulos de canciones, y al desplazarse o volver de un nivel es
fácil perder la orientación (sobre todo con mando/TV y catálogo amplio).

El recorrido del catálogo (décadas → años → canciones → reproducir) no cambia;
falta **contexto visual del año activo** mientras se está dentro de ese año.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Ver el año al listar sus canciones (Priority: P1)

Como oyente con mando de TV, quiero ver claramente el año en el que estoy
cuando abro el listado de canciones de ese año, para no confundirme con otro
año al desplazarme por la lista.

**Why this priority**: Es el problema planteado; sin este contexto la feature
no aporta valor.

**Independent Test**: Entrar en un año conocido (p. ej. 1985), mirar la
pantalla del listado de canciones y comprobar que el año aparece de forma
visible y comprensible sin abrir menús extra.

**Acceptance Scenarios**:

1. **Given** el usuario en el listado de años de una década (o el camino
   vigente hasta elegir año), **When** selecciona un año concreto, **Then** en
   la pantalla del listado de canciones de ese año se muestra el año de forma
   visible (p. ej. como título/categoría de la vista o equivalente claro en
   pantalla).
2. **Given** el listado de canciones de un año, **When** el usuario se
   desplaza por varias entradas, **Then** el indicador del año sigue siendo
   identificable sin tener que salir del listado.
3. **Given** dos años distintos visitados en secuencia, **When** el usuario
   entra en el segundo, **Then** el contexto mostrado corresponde al año
   actual, no al anterior.

---

### User Story 2 - No alterar el recorrido ni la reproducción (Priority: P1)

Como oyente, quiero que mostrar el año no añada pasos de navegación ni cambie
cómo se reproducen las canciones.

**Why this priority**: La mejora es de orientación, no de un flujo nuevo.

**Independent Test**: Desde un año con el indicador visible, reproducir una
canción válida y usar “atrás” hasta la década/años; el número de pasos del
recorrido documentado no aumenta.

**Acceptance Scenarios**:

1. **Given** el listado de canciones con el año visible, **When** el usuario
   selecciona una canción válida, **Then** la reproducción se comporta como
   hasta ahora (mismo mecanismo de reproducción del addon).
2. **Given** el usuario dentro de un año, **When** usa la navegación atrás
   habitual, **Then** vuelve al nivel anterior del catálogo (años de la
   década o equivalente) sin pantallas intermedias nuevas solo por el
   indicador.
3. **Given** el alcance de esta feature, **When** se revisa el producto,
   **Then** no se exige renombrar canciones en el catálogo editorial ni
   cambiar el formato de los datos por año.

---

### User Story 3 - Contexto coherente y legible (Priority: P2)

Como oyente, quiero que el año se muestre de forma legible y coherente con el
resto de etiquetas de la gramola (mismo idioma/estilo de presentación que el
usuario espera en el addon).

**Why this priority**: Un indicador confuso o inconsistente empeora la
orientación en lugar de mejorarla.

**Independent Test**: Comparar la forma en que se presenta el año en el
listado de canciones con cómo se etiquetan los años en el nivel anterior;
debe ser reconocible como el mismo año.

**Acceptance Scenarios**:

1. **Given** un año etiquetado en el nivel de años (p. ej. `1980`), **When**
   el usuario entra en ese año, **Then** el contexto en pantalla identifica el
   mismo año de forma inequívoca.
2. **Given** el addon con textos en el idioma activo del usuario, **When** se
   muestra el contexto del año, **Then** no introduce literales de otro
   idioma de forma inconsistente con el resto de la UI del addon.
3. **Given** un año sin canciones o con error recuperable de catálogo,
   **When** se muestra esa vista, **Then** el indicador del año (si la vista
   se muestra) no provoca un fallo catastrófico; los avisos de error siguen
   siendo amigables.

---

### Edge Cases

- **Año con una sola canción**: el año sigue visible; no se omite el contexto
  por lista corta.
- **Año vacío o catálogo con error parcial**: orientación del año si hay
  pantalla de listado; errores recuperables con aviso amigable.
- **Navegación rápida entre años**: el contexto debe actualizarse al año
  visitado, sin residual del anterior.
- **Niveles distintos**: esta feature se centra en la vista **dentro de un
  año** (listado de canciones). Mostrar también la década en la vista de años
  de una década queda **fuera del MVP**, salvo que se decida ampliar en plan
  sin hinchar alcance.
- **Favoritos / búsqueda** (features futuras o paralelas): al abrir canciones
  desde esos accesos no se exige el mismo indicador de “año de carpeta”; si
  aplica, el plan puede aclararlo, pero el requisito P1 es al entrar por el
  browse de catálogo en un año.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Cuando el usuario entra en un año del catálogo y ve su listado
  de canciones, el addon MUST mostrar en pantalla de forma visible e inequívoca
  el año en el que se encuentra.
- **FR-002**: El indicador del año MUST corresponder al año seleccionado en la
  navegación (no a otro año visitado antes).
- **FR-003**: Mostrar el año MUST NOT añadir niveles de navegación obligatorios
  ni cambiar el flujo décadas → años → canciones → reproducir.
- **FR-004**: Mostrar el año MUST NOT alterar el catálogo editorial ni el
  mecanismo de reproducción de canciones.
- **FR-005**: El indicador MUST permanecer comprensible mientras el usuario
  recorre el listado de canciones de ese año (no desaparecer solo por hacer
  scroll de ítems, dentro de lo razonable en la UI del cliente).
- **FR-006**: Ante errores recuperables al cargar el año, el addon MUST seguir
  las reglas de tolerancia a fallos del producto (aviso amigable, sin aborto
  catastrófico).
- **FR-007**: Esta feature MUST NOT exigir cambios de contenido en los datos
  por año ni nuevas taxonomías (géneros, carpetas extra, etc.).

### Key Entities

- **Year**: unidad de navegación y de datos del catálogo; es lo que debe
  identificarse en pantalla al listar sus canciones.
- **MusicVideo**: entrada de canción dentro de un Year; su listado es la vista
  donde debe verse el contexto del año.
- **Decade** (si aplica en la navegación vigente): agrupación superior; no es
  el foco del indicador de esta feature.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: En el 100 % de las pruebas manuales al entrar en un año con
  canciones, un observador identifica el año activo en pantalla en menos de
  3 segundos sin salir del listado.
- **SC-002**: Tras visitar dos años distintos seguidos, el 100 % de las
  comprobaciones muestran el contexto del segundo año (no el del primero).
- **SC-003**: El número de pasos de navegación desde la raíz hasta reproducir
  una canción de un año no aumenta respecto al flujo vigente (mismo recorrido
  de niveles).
- **SC-004**: Al menos 9 de 10 oyentes de prueba (o revisores del mantenedor
  en su defecto) confirman que, dentro de un año, ya no dudan “en qué año
  estoy” solo mirando la pantalla del listado.

## Assumptions

- El problema es de **orientación en la vista de canciones de un año**, no de
  renombrar ítems del catálogo ni de añadir el año a cada título de canción
  (evitar listas tipo “1980 — Artista - Canción” por defecto, salvo que el
  plan demuestre que es la única forma viable en el cliente).
- La forma concreta de “verse en pantalla” se elige en planificación según lo
  que permita la UI del cliente de forma estándar (título de categoría /
  cabecera de listado / equivalente), sin inventar una capa de UI paralela.
- Ampliar el mismo patrón a la vista de “años dentro de una década” (mostrar
  la década) queda fuera del MVP de esta feature.
- No depende de favoritos ni de búsqueda.
- Idioma y presentación coherentes con las reglas de i18n del proyecto.
