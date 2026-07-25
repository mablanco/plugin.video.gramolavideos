# Feature Specification: Auditoría y remediación de calidad del código

**Feature Branch**: `[001-auditoria-codigo]`

**Created**: 2026-07-25

**Status**: Draft

**Input**: User description: "Analizar la base de código actual para identificar bugs, deuda técnica, código acoplado, áreas de mejora, code smells, problemas de rendimiento y violaciones de mantenibilidad, respetando las reglas definidas en constitution.md. Documentar el comportamiento actual versus el comportamiento deseado." Ampliación: migrar la rama por defecto del repositorio de `master` a `main`.

## Comportamiento actual frente al deseado

Esta sección resume el resultado de la auditoría del addon publicado
`plugin.video.gramolavideos` frente a la constitution del proyecto. El alcance
de remediación es este addon; un andamiaje paralelo con otro id de addon queda
fuera de alcance.

### Decisión: andamiaje `plugin.video.gramola` (veredicto)

Tras revisar el repositorio hermano `plugin.video.gramola` (plantilla/scaffold
sin catálogo CSV ni reproducción YouTube, id distinto, un solo commit de
estructura inicial), se decide:

**No fusionar ni portar ese repositorio** como base de la remediación. El
producto y los datos viven en `plugin.video.gramolavideos`.

En el plan e implementación de esta feature **SÍ** se pueden adoptar, como
ideas de diseño (no como copia literal de código legacy Python 2), solo:

1. **Layout**: entry point fino + módulos bajo `resources/lib/`, con prefijo
   `kodi` para lo que toque APIs de Kodi y módulos sin ese prefijo para la
   lógica de catálogo verificable sin UI (alineado con constitution VII).
2. **Avisos al usuario**: un helper acotado de notificación ante fallos
   recuperables de catálogo (constitution VIII / FR-006).
3. **Esqueleto i18n**: carpeta `resources/language/` con ficheros de idioma
   estándar de Kodi cuando se toquen cadenas de UI, con al menos vía clara
   hacia `es` y `en` (constitution X / FR-015); no hace falta i18n completa
   en el primer incremento si las cadenas quedan preparadas para extracción.

**Explícitamente fuera de alcance** respecto a ese andamiaje:

- Dependencia `script.module.routing` (YAGNI para el flujo años → canciones).
- Settings de debug, logging elaborado tipo plantilla, o `.travis.yml` orientado a Python 2.
- Sustituir el id del addon, metadatos o README por los del scaffold.
- Traer código de plantilla sin modernizar al destino Kodi/Python 3 del proyecto.

### Flujo de usuario (años → canciones → reproducción)

| Aspecto | Comportamiento actual | Comportamiento deseado |
|---------|----------------------|------------------------|
| Navegación | Lista de años desde CSV → lista de canciones del año → reproducción vía YouTube | Mismo flujo de producto (constitution IV); no se añade navegación compleja |
| Contenido listado | Solo años 1980–1999 (falta 1994); no hay entradas de los 60/70 pese a la promesa del addon | Catálogo coherente con la descripción editorial (60s–90s) o descripción/metadatos alineados con lo que realmente hay; entradas inválidas corregidas o excluidas |
| Fallos de catálogo | Un CSV corrupto, fila incompleta o ruta inexistente puede abortar el listado sin aviso útil | Fallos recuperables no congelan ni abortan de forma catastrófica; el usuario recibe un aviso comprensible (constitution VIII) |
| Miniaturas | Dependen de una URL externa insegura; un fallo de miniatura puede degradar la experiencia | El listado sigue siendo usable si falla la imagen; se evita depender de transporte inseguro para lo esencial |
| Reproducción | Se lanza el reproductor con la URI del addon de YouTube | Sigue delegando en YouTube (constitution II); la acción de reproducir se integra de forma coherente con el listado del plugin (historial/contexto de directorio) |

### Calidad, mantenibilidad y gobernanza

| Aspecto | Comportamiento actual | Comportamiento deseado |
|---------|----------------------|------------------------|
| Compatibilidad | En instalaciones modernas de Kodi el addon puede fallar o comportarse de forma obsoleta por depender de un runtime y APIs antiguas | El addon funciona de forma usable en el destino Kodi moderno del proyecto, sin dependencias ajenas no soportadas (constitution VI) |
| Separación de responsabilidades | Lectura de catálogo, navegación y reproducción están mezcladas en un solo bloque difícil de verificar | El catálogo se puede cargar y validar aparte de la pantalla; la interfaz usa una capa acotada de Kodi (constitution VII) |
| Carga de catálogo | Cada uso vuelve a leer y preparar todo el catálogo, incluso cuando solo hace falta un año o reproducir | Solo se prepara lo necesario para la pantalla o acción actual; el coste no crece de más con el tamaño del catálogo (deuda ya anotada en el README) |
| Validación de datos | No se validan filas; existe al menos una entrada con id de reproducción de formato inválido | Filas inválidas se detectan y se omiten o se reportan sin tumbar el listado; ids de reproducción comprobables |
| Idioma de UI | La experiencia está en español sin preparación clara para multiidioma; los metadatos del addon ya tienen textos es/en | Los textos tocados no bloquean la futura UI en inglés vía el mecanismo estándar de Kodi (constitution X) |
| Trazabilidad de cambios | El historial de cambios aporta poca información útil al usuario/instalador; el changelog apunta a commits en `master` | Cambios de comportamiento relevantes suben versión y quedan reflejados en el historial (constitution V); las referencias públicas usan la rama por defecto `main` |
| Rama por defecto del repositorio | La rama por defecto remota y local es `master` | La rama por defecto es `main`; clones, PRs y documentación apuntan a `main`; `master` deja de ser la rama canónica (redirigida o retirada tras la migración) |
| Catálogo como datos | Cumple: canciones en CSV por año, formato `Artista - Canción;id` | Se mantiene; el código no hardcodea listas de canciones (constitution I) |

### Hallazgos de auditoría (inventario)

Prioridad orientativa para planificación posterior (`/speckit-plan` / `/speckit-tasks`):

1. **P1 – Bugs / roturas de plataforma**: dependencia de runtime y APIs antiguas; rutas de recursos frágiles; listados y reproducción no alineados con el comportamiento esperado en Kodi actual.
2. **P1 – Robustez**: errores de lectura de catálogo sin aviso útil; filas mal formadas pueden tumbar el flujo; entrada de catálogo con id de reproducción inválido (`Seguridad Social - Chiquilla` en 1991).
3. **P1 – Acoplamiento**: un solo bloque mezcla datos, navegación y reproducción; el catálogo no se puede verificar sin la UI completa.
4. **P2 – Rendimiento / smells**: carga completa del catálogo en cada uso; trabajo repetido de ordenación; clasificación de contenido poco adecuada para vídeos musicales; ubicación del addon asumida de forma rígida.
5. **P2 – Alineación producto–datos**: descripción “60s a 90s” frente a cobertura real ~1980–1999 (sin 1994 ni décadas 60–70).
6. **P2 – Rama por defecto**: el repositorio usa `master` como rama canónica; conviene migrar a `main` y actualizar enlaces/documentación (p. ej. historial de cambios que cita `commits/master`).
7. **P3 – Higiene de producto**: metadatos incompletos; historial de cambios poco útil; sin base de idioma para UI; deuda del README sin plan cerrado.
8. **Fuera de alcance**: reescritura total bajo otro id de addon; fusión/porte del andamiaje `plugin.video.gramola`; capas o frameworks no justificados (p. ej. routing externo) salvo Complexity Tracking (constitution IV, IX).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Usar la gramola en Kodi moderno sin roturas (Priority: P1)

Como oyente, abro el addon en una instalación actual de Kodi, recorro años y
canciones y reproduzco un vídeo musical vía YouTube igual que espera el
producto.

**Why this priority**: Sin compatibilidad real, el resto de mejoras no aporta
valor al usuario final.

**Independent Test**: Instalar el addon en un Kodi con runtime Python 3
soportado, abrir el addon, entrar en un año con entradas válidas y reproducir
una canción hasta que empiece el vídeo.

**Acceptance Scenarios**:

1. **Given** el addon instalado en Kodi moderno con el addon de YouTube disponible, **When** el usuario abre la gramola, **Then** ve la lista de años disponibles ordenada.
2. **Given** un año con canciones válidas, **When** el usuario entra en ese año, **Then** ve títulos en formato artista–canción y puede iniciar la reproducción.
3. **Given** una canción seleccionada, **When** el usuario la reproduce, **Then** la reproducción se delega en YouTube y no se descarga ni rehostea el vídeo.

---

### User Story 2 - Fallos de catálogo visibles y no catastróficos (Priority: P1)

Como oyente, si un fichero de año está dañado o una fila es inválida, el addon
no “muere” en silencio ni congela la interfaz: recibo un aviso claro y, si es
posible, sigo viendo el resto del catálogo usable.

**Why this priority**: La constitution exige tolerancia a fallos en I/O; hoy no
hay red de seguridad.

**Independent Test**: Provocar un CSV ilegible o una fila incompleta en un
entorno de prueba y comprobar notificación + listado residual usable.

**Acceptance Scenarios**:

1. **Given** un año cuyo fichero no se puede leer, **When** el usuario abre la gramola o ese año, **Then** recibe un aviso comprensible y el resto de años válidos sigue listándose cuando aplique.
2. **Given** un año con algunas filas inválidas y otras válidas, **When** el usuario abre ese año, **Then** las válidas se muestran y las inválidas no provocan un cierre abrupto del addon.

---

### User Story 3 - Mantener y verificar el catálogo con seguridad (Priority: P1)

Como mantenedor, puedo razonar sobre la lectura y validación del catálogo CSV
sin depender de lanzar la UI completa de Kodi, y el código de listado no
mezcla esa lógica de forma inseparable.

**Why this priority**: Habilita remediación segura y cumple el desacoplamiento
exigido por la constitution.

**Independent Test**: Ejecutar comprobaciones automatizadas (o un harness
mínimo) sobre carga/validación de CSV de ejemplo sin instancia de Kodi.

**Acceptance Scenarios**:

1. **Given** un conjunto de CSV de ejemplo (válidos e inválidos), **When** se ejecuta la lógica de datos del catálogo, **Then** se obtienen años y entradas válidas y se identifican las inválidas sin APIs de UI.
2. **Given** un cambio solo en la presentación del listado, **When** se revisa el diseño, **Then** no es necesario alterar las reglas de parseo del CSV para cambiar etiquetas o iconos.

---

### User Story 4 - Apertura ágil al crecer el catálogo (Priority: P2)

Como oyente, al abrir la lista de años o un año concreto no pago el coste de
releer y reordenar todo el catálogo si solo necesito una parte.

**Why this priority**: Deuda explícita en el README; impacto crece con más
CSV/entradas.

**Independent Test**: Comparar que listar años no exige materializar todas las
canciones de todos los años, y que listar un año no exige cargar los demás.

**Acceptance Scenarios**:

1. **Given** un catálogo con varios años, **When** el usuario solo pide la lista de años, **Then** el sistema no necesita cargar el detalle de todas las canciones para mostrar esos años.
2. **Given** el usuario entra en un año, **When** se construye el listado de canciones, **Then** solo se usa el contenido de ese año.

---

### User Story 5 - Colaborar sobre la rama por defecto `main` (Priority: P2)

Como mantenedor o colaborador, clono o abro un PR contra la rama por defecto
del repositorio y esa rama es `main`, no `master`. La documentación del
proyecto no empuja a trabajar sobre `master`.

**Why this priority**: Alinea el repo con la convención actual de GitHub y
evita fricción en contribución y automatización; es independiente del código
del addon pero forma parte de la higiene de esta remediación.

**Independent Test**: Comprobar en el remoto que la rama por defecto es `main`
y que la documentación/enlaces del historial ya no presentan `master` como
rama canónica.

**Acceptance Scenarios**:

1. **Given** el repositorio en el hosting remoto, **When** un colaborador consulta la rama por defecto, **Then** esa rama es `main`.
2. **Given** la documentación o el historial de cambios del proyecto que citaba commits de la rama antigua, **When** se revisan tras la migración, **Then** apuntan a `main` (o a una URL de historial que no dependa de `master`).
3. **Given** un clon fresco del repositorio, **When** se comprueba la rama de seguimiento por defecto, **Then** se obtiene `main` sin pasos manuales extra para “renombrar master”.

---

### User Story 6 - Coherencia editorial entre promesa y catálogo (Priority: P3)

Como oyente o colaborador de contenido, la descripción del addon y los años
disponibles no se contradicen de forma grave; las entradas rotas del catálogo
se corrigen o se eliminan.

**Why this priority**: Afecta confianza y alcance editorial (constitution III),
pero no bloquea la modernización técnica.

**Independent Test**: Revisar años presentes frente a summary/description y
comprobar que no quedan ids de reproducción obviamente inválidos.

**Acceptance Scenarios**:

1. **Given** la descripción pública del addon, **When** un usuario explora los años, **Then** o bien existen entradas representativas del arco editorial declarado, o bien la descripción se ha ajustado a la cobertura real.
2. **Given** el catálogo versionado, **When** se valida el formato de entradas, **Then** no permanecen ids de YouTube con formato inválido conocidos.

---

### Edge Cases

- ¿Qué ocurre si la carpeta de CSV no existe o está vacía?
- ¿Qué ocurre si un nombre de fichero no es un año de cuatro dígitos?
- ¿Qué ocurre si falta el addon de YouTube en el sistema?
- ¿Qué ocurre si una fila tiene más o menos de dos campos, campos vacíos o caracteres especiales en el título?
- ¿Qué ocurre si falla la obtención de la miniatura pero el id de vídeo es válido?
- ¿Qué ocurre al reproducir tras navegar atrás/adelante en el historial del plugin?
- ¿Qué ocurre con clones locales, forks o PRs abiertos que aún siguen `master` tras renombrar la rama por defecto?
- ¿Qué ocurre con enlaces externos (changelog, README, issues) que apuntaban a `commits/master`?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El sistema MUST preservar el flujo de usuario años → canciones → reproducción vía YouTube, sin rehostear ni descargar vídeo.
- **FR-002**: El catálogo MUST seguir siendo editable como CSV por año en el formato `Artista - Canción;youtube_video_id` con delimitador `;`, sin hardcodear listas de canciones en el código.
- **FR-003**: El addon MUST ejecutarse de forma usable en las versiones de Kodi modernas que la constitution del proyecto declara como destino técnico.
- **FR-004**: La lectura y validación del catálogo MUST estar separada de la construcción de la interfaz de listados.
- **FR-005**: El uso de APIs de Kodi para UI/plugin MUST estar encapsulado de modo que la lógica de datos pueda ejercitarse sin lanzar Kodi.
- **FR-006**: Ante errores recuperables de fichero o datos de catálogo, el sistema MUST mostrar un aviso comprensible al usuario y MUST NOT abortar de forma catastrófica el resto del flujo cuando aún haya datos usables.
- **FR-007**: El sistema MUST validar entradas de catálogo lo suficiente como para omitir o señalar filas inválidas (campos ausentes, id de reproducción con formato inválido) sin tumbar el listado completo.
- **FR-008**: Al mostrar solo la lista de años, el sistema MUST NOT requerir cargar el detalle completo de canciones de todos los años.
- **FR-009**: Al mostrar las canciones de un año, el sistema MUST cargar únicamente los datos necesarios de ese año.
- **FR-010**: La reproducción MUST seguir delegándose en el addon de YouTube declarado como dependencia.
- **FR-011**: Los cambios de comportamiento relevantes MUST actualizar la versión del addon y quedar reflejados en el historial de cambios del proyecto.
- **FR-012**: La remediación MUST NOT introducir frameworks o capas que compliquen el producto más allá de lo necesario; toda complejidad extra MUST justificarse en el plan.
- **FR-012a**: La remediación MUST NOT basarse en fusionar o copiar el repositorio andamiaje `plugin.video.gramola`; MUST limitarse a las ideas de diseño aprobadas en la sección «Decisión: andamiaje plugin.video.gramola».
- **FR-012b**: Al desacoplar (FR-004/FR-005), el plan MUST preferir entry point fino + `resources/lib/` con separación kodi/datos, helper de notificación ante errores de catálogo, y preparación i18n según esa misma decisión.
- **FR-013**: El id del addon MUST permanecer `plugin.video.gramolavideos`.
- **FR-014**: Assets referenciados en metadatos (icono y fanart) MUST seguir existiendo y siendo válidos.
- **FR-015**: Cualquier cadena nueva de UI tocada en esta remediación MUST quedar en una forma que no impida la futura extracción a ficheros de idioma estándar de Kodi (es + en).
- **FR-016**: El mantenedor MUST disponer de un inventario trazable (esta especificación y el plan/tareas derivados) que relacione hallazgos de auditoría con el comportamiento deseado y su remediación.
- **FR-017**: La cobertura editorial o la descripción pública del addon MUST quedar alineadas (ampliar catálogo hacia el arco declarado, o ajustar el mensaje a la cobertura real), incluyendo la corrección o eliminación de entradas de reproducción inválidas ya identificadas.
- **FR-018**: La rama por defecto del repositorio MUST ser `main` (no `master`) en el remoto canónico.
- **FR-019**: La documentación y referencias del propio proyecto que presentaban `master` como rama canónica (incluido el historial de cambios) MUST actualizarse para reflejar `main`.
- **FR-020**: Tras la migración, `master` MUST NOT permanecer como rama por defecto; si se conserva temporalmente, MUST quedar claro que no es la rama de trabajo canónica (redirección o retirada planificada).

### Key Entities

- **Year**: Clave de navegación derivada del nombre del fichero CSV (p. ej. `1980`); representa un listado de vídeos de ese año.
- **MusicVideo**: Entrada de catálogo con título (`Artista - Canción`) e id de YouTube; pertenece a un Year.
- **CatalogLoadResult**: Resultado de intentar cargar catálogo o un año (entradas válidas, errores recuperables, avisos).
- **AuditFinding**: Hallazgo de calidad (bug, deuda, smell, violación de constitution) con severidad y comportamiento actual/deseado asociado.
- **DefaultBranch**: Rama canónica del repositorio remoto (`main` tras la migración); punto de entrada para clones y PRs.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: En un Kodi moderno de referencia del mantenedor, un usuario completa el recorrido abrir addon → elegir año → reproducir canción válida en menos de 30 segundos en condiciones normales de red.
- **SC-002**: Con al menos un CSV ilegible o una fila inválida inyectada en prueba, el addon muestra un aviso comprensible y no impide listar el resto de años o canciones válidas en el 100 % de esos casos de prueba definidos.
- **SC-003**: La lógica de carga/validación del catálogo puede verificarse con un conjunto de pruebas automatizadas o harness sin abrir la UI de Kodi, cubriendo al menos CSV válido, fila inválida y año ausente.
- **SC-004**: Listar años con un catálogo de prueba de tamaño ≥ 2× el actual no requiere materializar todas las canciones de todos los años (verificable por diseño/prueba de carga selectiva).
- **SC-005**: Tras la remediación, no quedan hallazgos P1 abiertos del inventario de esta especificación sin decisión explícita documentada (corregido, diferido con justificación, o aceptado como riesgo).
- **SC-006**: Descripción pública y años/entradas disponibles no presentan contradicción editorial grave; 0 ids de YouTube con formato inválido conocidos en el catálogo versionado.
- **SC-007**: Un revisor puede mapear cada requisito FR-001–FR-020 (incl. FR-012a/FR-012b) a evidencia en plan/tareas o a una exclusión justificada en Complexity Tracking.
- **SC-009**: El plan de remediación no propone adoptar el scaffold `plugin.video.gramola` como base; si menciona ese repo, solo como referencia de las tres ideas aprobadas (layout, notificación, esqueleto i18n).
- **SC-008**: Tras la migración, la rama por defecto del remoto canónico es `main` y un clon fresco sigue esa rama sin configuración manual adicional; las referencias internas del proyecto a la rama canónica usan `main` (0 enlaces canónicos restantes a `master` en README/changelog del repo).

## Assumptions

- El sujeto de la auditoría y remediación es `plugin.video.gramolavideos` (este repositorio), no un andamiaje con otro addon id.
- El veredicto sobre `plugin.video.gramola` (no fusionar; solo layout, notificación e i18n como ideas) es vinculante para `/speckit-plan` e implementación.
- No se cambia el propósito del producto: índice/navegador de vídeos musicales españoles vía YouTube.
- La modernización se hace de forma evolutiva sobre el addon existente (constitution IX), no como reescritura total sin plan.
- El soporte multiidioma completo (ficheros de idioma es/en) puede quedar como seguimiento si esta feature solo deja el código listo para extracción; la UI puede permanecer en español hasta una feature de i18n dedicada.
- Ampliar el catálogo con décadas 60–70 puede ser trabajo de contenido separado; esta feature exige al menos alinear mensaje y datos y corregir entradas inválidas conocidas.
- Las pruebas sin Kodi se limitan a lógica de datos; la verificación de reproducción real sigue requiriendo Kodi + YouTube.
- Los problemas de rendimiento relevantes son los de carga de catálogo en el dispositivo del usuario, no de servidor propio (no hay backend).
- La migración `master` → `main` se hace en el remoto GitHub del mantenedor (`mablanco/plugin.video.gramolavideos`); forks ajenos pueden requerir un aviso puntual pero no bloquean el cambio de rama por defecto.
- No hay reglas de protección de rama ni CI activos que dependan de `master` en el momento de la auditoría; si aparecen antes de ejecutar la migración, el plan debe actualizarlas a `main`.
