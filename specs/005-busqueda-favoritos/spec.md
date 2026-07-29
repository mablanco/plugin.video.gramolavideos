# Feature Specification: Alcance de búsqueda y favoritos

**Feature Branch**: `[005-busqueda-favoritos]`

**Created**: 2026-07-29

**Status**: Decision complete

**Input**: User description: "búsqueda/favoritos, decidiendo si deben ser una o dos features diferentes"

## Contexto y problema

Hoy la gramola se recorre por jerarquía de catálogo (años y, en el futuro
posible, agrupaciones como décadas) hasta llegar a una canción. No hay forma de
**buscar** por texto ni de **guardar favoritos** para volver rápido a temas
habituales. Ambas ideas suelen mencionarse juntas como “mejoras de
descubrimiento”, pero **no son el mismo problema de usuario**:

- **Búsqueda**: encontrar una canción o artista sin recorrer carpetas.
- **Favoritos**: marcar y reabrir un conjunto personal de entradas ya conocidas.

Implementarlas a la vez puede hinchar el alcance; separarlas puede duplicar
trabajo de diseño si comparten pantallas o reglas. El objetivo de **esta**
feature es **decidir con criterios explícitos si búsqueda y favoritos deben
planificarse e implementarse como una sola feature o como dos features
distintas** (y en qué orden), dejando listo el siguiente paso de planificación
sin comprometer aún una implementación completa de ambas capacidades.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Decidir una vs dos features (Priority: P1)

Como mantenedor, necesito un veredicto documentado que compare tratar
**búsqueda y favoritos juntos** frente a **separarlos en dos features**, con
criterios claros (alcance, dependencias, valor incremental, riesgo de
complejidad) y una recomendación accionable.

**Why this priority**: Sin esta decisión, `/speckit-plan` y el trabajo posterior
arriesgan un alcance ambiguo o un monolitismo innecesario.

**Independent Test**: Leer el documento de decisión y comprobar que evalúa al
menos las dos estrategias (una feature vs dos), declara un ganador, el orden
sugerido si hay secuencia, y qué queda fuera de cada paquete.

**Acceptance Scenarios**:

1. **Given** la necesidad de mejorar descubrimiento/acceso rápido al catálogo, **When** se completa el estudio, **Then** existe un veredicto que elige explícitamente “una feature combinada” o “dos features separadas”.
2. **Given** ese veredicto, **When** un revisor lo lee, **Then** entiende los criterios usados, los pros/contras de cada opción y el impacto en el tamaño del siguiente plan.
3. **Given** una recomendación de dos features, **When** se publica, **Then** indica orden (cuál primero), dependencias entre ellas y si comparten supuestos de producto; **Given** una recomendación de una sola, **Then** indica límites internos (MVP vs diferido) para no mezclar todo sin control.

---

### User Story 2 - Describir el valor de búsqueda para el oyente (Priority: P1)

Como oyente con mando, quiero poder localizar una canción o artista del
catálogo por un criterio de texto simple, sin depender solo de recordar el año.

**Why this priority**: Define el problema de búsqueda de forma independiente,
necesario para juzgar si puede vivir sola como feature.

**Independent Test**: Revisar en el entregable la descripción de búsqueda
(entradas, resultados esperados, qué no incluye) y comprobar que es testeable
sin asumir favoritos.

**Acceptance Scenarios**:

1. **Given** el catálogo con muchas entradas, **When** se describe el flujo de búsqueda en el estudio, **Then** queda claro qué puede buscar el usuario (p. ej. parte del título / artista) y qué ve como resultado.
2. **Given** una búsqueda sin coincidencias, **When** se describe el comportamiento, **Then** el usuario recibe un resultado vacío comprensible, no un fallo opaco.
3. **Given** el alcance de búsqueda del estudio, **When** se listan exclusiones, **Then** queda fuera lo no esencial (p. ej. búsqueda en internet fuera del catálogo local, filtros avanzados) salvo justificación.

---

### User Story 3 - Describir el valor de favoritos para el oyente (Priority: P1)

Como oyente, quiero marcar canciones que me gustan y volver a esa lista
después, sin volver a buscar el año.

**Why this priority**: Define favoritos de forma independiente para poder
separar o unir features con criterio.

**Independent Test**: Revisar en el entregable el flujo de marcar / listar /
quitar favorito y comprobar que es usable como historia aislada.

**Acceptance Scenarios**:

1. **Given** el usuario en una canción del catálogo, **When** se describe “añadir a favoritos”, **Then** esa entrada puede reabrirse desde un acceso de favoritos en una sesión posterior.
2. **Given** un favorito guardado, **When** el usuario lo quita, **Then** deja de aparecer en la lista de favoritos.
3. **Given** el alcance de favoritos del estudio, **When** se listan exclusiones, **Then** no se exige por defecto listas múltiples, carpetas de favoritos ni sincronización en la nube, salvo que el veredicto lo justifique como parte del mismo paquete.

---

### User Story 4 - Encajar con la gramola simple (Priority: P2)

Como mantenedor, quiero que la decisión respete la identidad del producto
(índice editorial por catálogo, reproducción delegada, sin hinchar el addon) y
deje claro qué habría que actualizar en el flujo de usuario documentado si se
añaden estas capacidades.

**Why this priority**: Evita que el veredicto proponga un mini-Netflix o un
alcance incompatible con la simplicidad del plugin.

**Independent Test**: Comprobar que el veredicto menciona impacto en el flujo
actual, en el catálogo como fuente de verdad y qué no se cambia (reproducción /
formato de datos de canciones).

**Acceptance Scenarios**:

1. **Given** el flujo actual de navegación por catálogo, **When** se recomienda búsqueda y/o favoritos, **Then** se indica si son entradas adicionales en la raíz (u otro punto) y cómo conviven con el recorrido por años.
2. **Given** el catálogo basado en datos por año, **When** se evalúan favoritos, **Then** no se propone sustituir los CSV del catálogo como fuente editorial; los favoritos son preferencias del usuario, no el catálogo maestro.
3. **Given** una opción que exija rehosteo, cuenta online obligatoria o reescritura masiva del catálogo, **When** se evalúa, **Then** se descarta o se marca incompatible.

---

### Edge Cases

- Catálogo ampliado (p. ej. tras semilla 60/70): la decisión MUST considerar que búsqueda gana valor con más entradas; favoritos también, pero con distinto umbral de urgencia.
- Navegación por décadas u otra jerarquía (`003`): el estudio MUST decir si búsqueda/favoritos dependen de esa feature o pueden ir en paralelo.
- Favorito cuyo año o id desaparece del catálogo: el veredicto MUST indicar el comportamiento deseado a alto nivel (ocultar, avisar, enlace roto comprensible).
- Búsqueda con muchas coincidencias: el estudio MUST acotar si hay límite de resultados mostrado o criterio de ordenación a nivel de producto (sin detallar implementación).
- Usuario que solo quiere una de las dos capacidades: argumento a favor de features separadas o de un MVP partido dentro de una sola feature.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El proyecto MUST producir un **veredicto de alcance** que elija entre: (A) una única feature que cubra búsqueda y favoritos, o (B) dos features distintas (búsqueda y favoritos), con justificación explícita.
- **FR-002**: El veredicto MUST usar criterios documentados comunes, incluyendo al menos: valor para el oyente, independencia de historias de usuario, tamaño/riesgo de implementación, solapamiento de diseño, y encaje con la simplicidad del producto.
- **FR-003**: El estudio MUST describir por separado el problema de **búsqueda** y el de **favoritos** (flujos de usuario, inclusiones y exclusiones de MVP), aunque la decisión final sea unificarlos.
- **FR-004**: Si la recomendación es **dos features**, el veredicto MUST indicar orden de entrega, dependencias y qué puede diferirse sin bloquear la otra.
- **FR-005**: Si la recomendación es **una feature**, el veredicto MUST definir un MVP interno (qué se entrega primero dentro del mismo paquete) y qué queda explícitamente fuera de la primera entrega.
- **FR-006**: El veredicto MUST pronunciarse sobre prioridad relativa frente a otras líneas abiertas de producto (navegación del catálogo, ampliación 60/70), sin exigir completarlas antes salvo dependencia real.
- **FR-007**: El estudio MUST asumir que el catálogo editorial sigue siendo la fuente de las canciones disponibles; favoritos MUST modelarse como preferencias de usuario, no como sustituto del catálogo.
- **FR-008**: El estudio MUST NOT exigir, para esta decisión, cambiar el proveedor de reproducción ni el formato de filas del catálogo.
- **FR-009**: El entregable MUST dejar listo el enganche al siguiente paso: nombres/alcance sugeridos para `/speckit-plan` o para nuevos `/speckit-specify` si se parten en dos.
- **FR-010**: Esta feature de decisión MUST NOT implementarse como desarrollo completo de búsqueda y favoritos en el addon; la implementación concreta queda para el/los planes posteriores según el veredicto. (Se admite solo documentación de decisión y, si hiciera falta, esbozos de producto no enlazados a código.)

### Key Entities

- **Búsqueda de catálogo**: capacidad de localizar entradas del catálogo por criterio de texto u otro filtro simple definido en el estudio.
- **Favorito**: marca de preferencia del usuario sobre una entrada del catálogo, consultable después.
- **Veredicto de empaquetado**: decisión “una feature” vs “dos features” con criterios, orden y límites de MVP.
- **Entrada de catálogo**: canción ya existente en los datos del addon (título + año + identificador de reproducción).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Existe un único documento de decisión que responde de forma inequívoca si búsqueda y favoritos van en **una** o en **dos** features.
- **SC-002**: El documento evalúa ambas estrategias con los mismos criterios (≥4 criterios de FR-002) y dedica al menos un apartado a cada capacidad (búsqueda y favoritos).
- **SC-003**: Un revisor puede, en menos de 10 minutos, extraer del veredicto: decisión, orden/MVP, exclusiones y siguiente comando Speckit recomendado.
- **SC-004**: El veredicto no deja la implementación de ambas capacidades como “obligatoria e indivisible” sin opción de entrega parcial (ya sea vía dos features o MVP interno).
- **SC-005**: Queda explícito que el catálogo editorial no se sustituye por favoritos y que la reproducción no cambia de modelo por esta decisión.

## Assumptions

- El disparador de esta feature es **decidir el empaquetado** (una vs dos), no entregar aún búsqueda y favoritos usables en Kodi.
- Búsqueda se limita al **catálogo local** del addon, no a YouTube global ni a la web.
- Favoritos son **por instalación/perfil de usuario** en el dispositivo, sin sincronización multi-dispositivo en el MVP conceptual.
- No se requieren listas múltiples de favoritos, playlists colaborativas ni recomendaciones automáticas en el alcance de decisión.
- La entrada desde la raíz del addon (ítems “Buscar” / “Favoritos” o equivalente) es la hipótesis de UX por defecto a contrastar en el estudio; el veredicto puede ajustar el punto de acceso.
- Features `003-navegacion-videos` y `004-catalogo-60-70` son contexto de priorización; esta decisión puede recomendar paralelismo o espera, pero no las implementa.
- Un solo mantenedor valida el veredicto.
