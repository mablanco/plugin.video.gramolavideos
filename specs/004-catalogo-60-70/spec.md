# Feature Specification: Base de catálogo 60s/70s

**Feature Branch**: `[004-catalogo-60-70]`

**Created**: 2026-07-29

**Status**: Draft

**Input**: User description: "añadir automaticamente contenido de los 60/70 para crear una base de canciones sobre la que crecer"

## Contexto y problema

La Gramola promete editorialmente vídeos musicales de artistas y bandas
españolas en un arco que incluye los **60 y 70**, pero el catálogo publicado
cubre sobre todo **1980–1999** (sin 1994). El README ya trata la ampliación a
60/70 como trabajo de contenido pendiente. Rellenar esas décadas a mano, fila a
fila, es lento y frena tener una **base inicial** sobre la que el mantenedor y
colaboradores puedan crecer.

El problema de producto es: **obtener de forma asistida/automática un conjunto
inicial de entradas 1960–1979** (título + identificador de reproducción) en el
mismo formato de catálogo que el resto del addon, con calidad suficiente para
navegar y reproducir, sin convertir el addon en un rastreador en vivo ni romper
el modelo “catálogo como datos”.

Esta feature es **de contenido y de proceso de contribución**, no de rediseño
de navegación (eso es `003-navegacion-videos`) ni de cambio de proveedor de
reproducción.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Disponer de una base navegable 60s/70s (Priority: P1)

Como oyente, quiero abrir la gramola y encontrar años de los 60 y/o 70 con
canciones reproducibles, de modo que el arco editorial deje de estar vacío en
esas décadas.

**Why this priority**: Sin entradas reales no hay producto en 60/70; es el
resultado visible de la feature.

**Independent Test**: Abrir el addon (o inspeccionar el catálogo instalado),
listar años &lt; 1980 presentes, entrar en varios y reproducir al menos una
entrada válida por década.

**Acceptance Scenarios**:

1. **Given** el addon con esta feature entregada, **When** el usuario abre el listado de años, **Then** aparecen años de los 60 y de los 70 que antes no existían en el catálogo publicado.
2. **Given** un año de los 60 con entradas, **When** el usuario entra y elige una canción válida, **Then** se inicia la reproducción como con el resto del catálogo.
3. **Given** un año de los 70 con entradas, **When** el usuario hace lo mismo, **Then** obtiene el mismo comportamiento de reproducción que en los 80/90.

---

### User Story 2 - Generar la base de forma asistida (Priority: P1)

Como mantenedor, quiero un proceso **asistido o automático** (fuera de la
pantalla del oyente) que proponga o genere filas de catálogo para 1960–1979 en
el formato ya usado, de modo que no tenga que inventar y teclear cada entrada
desde cero.

**Why this priority**: El valor “automático” es reducir el coste de crear la
semilla; sin proceso asistido la feature degenera en curación manual pura.

**Independent Test**: Ejecutar el proceso documentado de generación/asistencia
y comprobar que produce (o actualiza) ficheros de año con filas en el formato
`Artista - Canción;identificador`, listos para revisión.

**Acceptance Scenarios**:

1. **Given** el repositorio sin (o con poca) cobertura 1960–1979, **When** se ejecuta el proceso asistido documentado, **Then** se obtienen candidatos o filas para múltiples años de ambas décadas.
2. **Given** la salida del proceso, **When** se revisa el formato, **Then** cada fila usable respeta el delimitador y el patrón de título ya usados en el catálogo.
3. **Given** el proceso, **When** se describe en la documentación de contribución, **Then** un colaborador entiende cómo regenerar o ampliar la semilla sin adivinar pasos ocultos.

---

### User Story 3 - Revisar y quedarse solo con entradas publicables (Priority: P1)

Como mantenedor, quiero revisar la semilla generada y **aceptar solo** entradas
alineadas con el criterio editorial (música española de la época) y con
identificadores de reproducción utilizables, descartando basura automática.

**Why this priority**: “Automático” sin filtro rompe la identidad del producto
y puede meter ids rotos o temas fuera de alcance.

**Independent Test**: Partir de una salida cruda con al menos un candidato
inválido o fuera de alcance y comprobar que el flujo de revisión lo excluye
antes de considerar el catálogo listo.

**Acceptance Scenarios**:

1. **Given** candidatos generados automáticamente, **When** termina la revisión de publicación, **Then** no quedan en el catálogo entregado filas con identificador de formato inválido.
2. **Given** un candidato claramente fuera del alcance editorial (no artista/banda española / no vídeo musical de la época), **When** se aplica el criterio de revisión, **Then** no se incluye en la base publicada.
3. **Given** la base publicada, **When** se hace smoke de un muestreo de entradas (varias de 60s y varias de 70s), **Then** la mayoría del muestreo reproduce o, si falla por bloqueo del proveedor, queda documentado para sustituir el id (mismo criterio que el catálogo actual).

---

### User Story 4 - Dejar el catálogo listo para crecer a mano (Priority: P2)

Como colaborador, después de la semilla quiero poder **añadir más canciones**
editando los CSV de año como hasta ahora, sin depender del proceso automático
para cada nueva fila.

**Why this priority**: La feature pide una base “sobre la que crecer”, no un
sistema cerrado de auto-relleno continuo en producción.

**Independent Test**: Añadir manualmente una fila a un CSV de un año 60/70 y
verificar que aparece en el listado del addon como cualquier otra.

**Acceptance Scenarios**:

1. **Given** la semilla publicada, **When** un colaborador añade una fila válida a un CSV de 1960–1979, **Then** esa canción aparece al abrir ese año sin pasos extra.
2. **Given** la documentación de contribución, **When** se actualiza tras esta feature, **Then** describe tanto el flujo manual clásico como el proceso asistido de semilla (si se mantiene para ampliaciones futuras).
3. **Given** metadatos/README que hablaban solo de 80/90, **When** la base 60/70 está publicada, **Then** la descripción de producto refleja que el catálogo incluye también esas décadas (o el alcance real resultante).

---

### Edge Cases

- Año sin candidatos buenos tras la revisión: no crear un año vacío engañoso; omitir ese año hasta tener al menos una entrada publicable.
- Identificador que parece válido pero el vídeo es privado, eliminado o exige login: mismo tratamiento que el catálogo actual (omitir, sustituir o documentar); no bloquear toda la semilla.
- Duplicados (misma canción/id en el mismo año o entre años): la revisión MUST evitar duplicar el mismo id en el mismo año; el estudio de proceso puede definir política entre años.
- Colisión con años 80/90 existentes: esta feature MUST NOT degradar ni reescribir de forma masiva el catálogo ya publicado de 1980–1999 salvo corrección puntual justificada.
- Generación que proponga artistas no españoles o covers ajenos al criterio: rechazar en revisión.
- Proceso automático no disponible (falla de red/herramienta en el entorno del mantenedor): debe quedar documentada una vía de semilla mínima o reintento; el addon del oyente no debe depender de ese proceso en tiempo de ejecución.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El proyecto MUST incorporar al catálogo publicado una **base inicial** de vídeos musicales de artistas/bandas españolas para las décadas 1960–1969 y 1970–1979.
- **FR-002**: Cada entrada publicada MUST usar el formato de catálogo existente: título `Artista - Canción` e identificador de reproducción, delimitados como el resto de CSV por año.
- **FR-003**: MUST existir un proceso **asistido o automático de generación de semilla** ejecutable por el mantenedor (o documentado paso a paso) que produzca candidatos o filas para múltiples años de 1960–1979. Ese proceso MUST NOT ejecutarse como rastreo en vivo dentro de la experiencia normal del oyente al navegar el addon.
- **FR-004**: Antes de publicar la base, MUST aplicarse una **revisión editorial**: alcance español / vídeo musical de la época, formato de fila correcto e identificador con forma válida.
- **FR-005**: La base publicada MUST cubrir **ambas** décadas (60s y 70s) con al menos un año navegable en cada una.
- **FR-006**: La base publicada MUST incluir al menos **40 entradas** en total entre 1960 y 1979, repartidas de forma que no concentre todo en un único año (mínimo **8 años distintos** con al menos una entrada).
- **FR-007**: El catálogo 1980–1999 existente MUST permanecer usable; esta feature MUST NOT exigir borrar o migrar masivamente esas entradas para entregar la semilla.
- **FR-008**: Las entradas publicadas MUST ser ampliables después con el flujo manual de edición de CSV ya conocido.
- **FR-009**: La documentación orientada a humanos (como mínimo README / guía de contribución tocada por el cambio) MUST actualizar el alcance de décadas para reflejar la presencia de 60/70 y MUST explicar cómo se generó o se puede regenerar la semilla.
- **FR-010**: Un muestreo de verificación (al menos 5 entradas de 60s y 5 de 70s) MUST realizarse antes de dar la base por cerrada; los fallos de reproducción detectados MUST corregirse (sustitución de id) o documentarse explícitamente como deuda conocida.
- **FR-011**: El proceso automático/asistido MUST privilegiar fuentes y criterios compatibles con no rehostear vídeo y con identificadores del proveedor de reproducción ya usado por el producto.
- **FR-012**: Años sin ninguna entrada publicable tras revisión MUST NOT aparecer como carpetas vacías en el catálogo entregado.

### Key Entities

- **Año (CSV)**: fichero de catálogo nombrado por año civil; unidad de almacenamiento existente.
- **Entrada de vídeo musical**: título + identificador de reproducción; pertenece a un Año.
- **Semilla 60/70**: conjunto inicial de entradas 1960–1979 publicado para crecer después.
- **Candidato generado**: propuesta del proceso asistido aún no aceptada editorialmente.
- **Revisión editorial**: paso humano (o lista de comprobación explícita) que filtra candidatos antes de publicar.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Tras la entrega, un oyente puede abrir al menos un año de los 60 y uno de los 70 y ver canciones en cada uno.
- **SC-002**: El catálogo publicado incluye ≥40 entradas nuevas o recuperadas en el rango 1960–1979, en ≥8 años distintos.
- **SC-003**: El 100 % de las filas publicadas de la semilla cumplen el formato de título e identificador del catálogo (comprobable por inspección o validación existente).
- **SC-004**: En un muestreo de 10 reproducciones (5×60s + 5×70s), al menos el 80 % inicia reproducción con éxito en condiciones normales, o los fallos quedan listados con id a sustituir.
- **SC-005**: Un colaborador nuevo puede añadir una canción más a un año 60/70 en menos de 5 minutos siguiendo solo la documentación de contribución actualizada.
- **SC-006**: La descripción pública del addon deja de afirmar que el catálogo es solo 80/90 si la semilla 60/70 ya está incluida.

## Assumptions

- “Automáticamente” significa **automatización del trabajo de curación/semilla** (herramientas, scripts o asistencia en el entorno de desarrollo), **no** que el addon descargue o descubra catálogo nuevo cada vez que el oyente abre un menú.
- La semilla es **representativa y crecible**, no una discografía exhaustiva de dos décadas; el crecimiento posterior es manual o por nuevas corridas opcionales del mismo proceso.
- Se reutiliza el proveedor de reproducción y el formato CSV actuales; no se inventa un almacén paralelo.
- El criterio editorial sigue siendo artistas/bandas españolas y vídeos musicales de la época (constitution de alcance).
- La feature de navegación (`003-navegacion-videos`) puede desarrollarse en paralelo; esta feature **no** depende de décadas en UI, pero se beneficia de ella cuando el listado de años crezca.
- Un mantenedor hace la revisión final de lo publicado; no se exige un panel de moderación multi-usuario.
- No se requiere relleno obligatorio de **todos** los años 1960–1979 en esta entrega (solo el mínimo de cobertura de FR-005/FR-006).
