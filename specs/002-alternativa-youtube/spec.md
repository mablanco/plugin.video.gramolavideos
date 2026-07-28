# Feature Specification: Alternativa al addon de YouTube para reproducción

**Feature Branch**: `[002-alternativa-youtube]`

**Created**: 2026-07-25

**Updated**: 2026-07-28 (reframe tras smoke Kodi)

**Status**: Draft

**Input**: User description: "analiza la posibilidad de usar un sustituto del addon de youtube ya que éste pide una API key y no es tan sencillo de usar para usuarios inexpertos como lo era antiguamente". Ampliación tras smoke (2026-07-28): en versiones recientes el addon de YouTube ya no exige API key para funcionar, pero aún pide login en una cuenta de YouTube para acceder a ciertos vídeos; interesa que una alternativa pueda reproducir esos casos sin forzar el login.

## Contexto y problema

La Gramola de Vídeos es un índice/navegador de vídeos musicales: el usuario elige
año → canción y espera que el vídeo se reproduzca. Hoy la reproducción se
delega en el addon oficial de YouTube para Kodi.

**Evidencia de smoke (2026-07-28)**: en Kodi 20.5 Nexus con
`plugin.video.youtube` 7.4.x el recorrido feliz funciona **sin API key** (como
antiguamente) para la mayoría de entradas. Persiste otra fricción: **algunos
vídeos del catálogo exigen iniciar sesión en una cuenta de YouTube** dentro del
addon (p. ej. 1984 *La Unión - Eclipse total*). Eso sigue siendo un obstáculo
para usuarios inexpertos o que no quieren vincular una cuenta.

El problema de producto a resolver ya **no** es “obligar a crear una API key de
desarrollador”, sino: **¿cómo reproducir también las entradas que el addon de
YouTube bloquea tras login, sin convertir la gramola en un cliente de streaming
propio ni rehostear vídeo?**

El motivo histórico de esta feature (API key) queda como contexto; el criterio
de éxito se actualiza al dolor observado en smoke. Una vía alternativa (p. ej.
resolución yt-dlp) se evalúa sobre todo como **complemento o fallback para
ciertos vídeos**, no necesariamente como sustitución total del addon de YouTube.

Esta feature **no implementa aún** el cambio de proveedor. Su propósito es
**analizar, comparar y decidir**. Cualquier cambio de dependencia o de política
de reproducción implica **revisar y, si procede, enmendar** la gobernanza del
proyecto.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Decidir con criterios claros (Priority: P1)

Como mantenedor, necesito un veredicto documentado sobre si conviene una
alternativa o un fallback al addon de YouTube para cubrir los vídeos que
exigen login de cuenta, con criterios explícitos de aceptación o rechazo
(incluyendo el hallazgo de que la API key ya no es el bloqueo principal).

**Why this priority**: Sin decisión fundamentada no se puede planificar
migración, documentación ni cambios de gobernanza; el problema de usabilidad
sigue abierto (ahora centrado en login selectivo).

**Independent Test**: Leer el entregable de decisión y comprobar que incluye
opciones evaluadas, criterios, riesgos, impacto en usuarios y un veredicto
accionable (fallback/complemento / sustitución total / solo mitigar).

**Acceptance Scenarios**:

1. **Given** el smoke que muestra YouTube usable sin API key pero con login en ciertos vídeos, **When** se completa el análisis, **Then** existe un documento de decisión con al menos las opciones relevantes evaluadas bajo los mismos criterios.
2. **Given** ese documento, **When** un revisor lo lee, **Then** entiende por qué se recomienda una vía concreta (p. ej. fallback solo para títulos bloqueados) y qué queda fuera de alcance.
3. **Given** una recomendación que cambia o amplía la dependencia de reproducción, **When** se publica el veredicto, **Then** indica explícitamente si hace falta enmendar la gobernanza del proyecto y qué debe cambiar en la experiencia del usuario.

---

### User Story 2 - Validar la experiencia del oyente inexperto (Priority: P1)

Como oyente sin conocimientos técnicos, quiero poder usar la gramola tras
instalarla (y, como mucho, instalar dependencias simples) **sin crear API keys
ni verse obligado a iniciar sesión en YouTube** para oír entradas del catálogo
que el addon oficial bloquea tras login.

**Why this priority**: El smoke confirma que el dolor residual es el login
selectivo; la API key ya no es el bloqueo principal en versiones recientes.

**Independent Test**: Recorrer el flujo descrito para la opción recomendada con
(a) un vídeo que YouTube reproduce sin login y (b) un vídeo conocido que exige
login en el addon YouTube, y comprobar el comportamiento documentado.

**Acceptance Scenarios**:

1. **Given** un usuario nuevo sin API key ni cuenta de YouTube vinculada en Kodi, **When** reproduce una canción que el addon YouTube 7.4.x permite sin login, **Then** el recorrido feliz documentado funciona (vía YouTube u otra vía recomendada).
2. **Given** una canción del catálogo que el addon YouTube bloquea pidiendo login, **When** se usa la vía alternativa/fallback recomendada (si el veredicto la adopta), **Then** el análisis documenta si puede reproducirse sin ese login o por qué no.
3. **Given** que falta o falla el proveedor de fallback, **When** el usuario intenta reproducir un título bloqueado, **Then** recibe un aviso comprensible (p. ej. “este vídeo pide cuenta YouTube” / “instala el proveedor alternativo”) sin fallo silencioso.

---

### User Story 3 - Preservar el producto como índice, no como cliente de streaming (Priority: P2)

Como mantenedor, quiero que cualquier alternativa siga siendo un navegador del
catálogo editorial (vídeos musicales españoles referenciados por identificadores
de YouTube en los CSV), sin convertir el addon en un descargador ni en un
almacén de ficheros de vídeo.

**Why this priority**: Protege la identidad del producto y los límites legales /
éticos ya asumidos; evita un alcance incontrolado.

**Independent Test**: Revisar la recomendación y comprobar que el catálogo
sigue siendo la fuente de verdad, que no se propone rehosteo, y que la
reproducción sigue siendo delegada a un proveedor externo adecuado.

**Acceptance Scenarios**:

1. **Given** el catálogo actual por años con títulos e ids de vídeo, **When** se recomienda una alternativa, **Then** no exige reescribir el catálogo a otro tipo de medio ni alojar los vídeos en el addon.
2. **Given** la recomendación, **When** se describe el flujo de usuario, **Then** se mantiene el recorrido años → canciones → reproducir (salvo justificación explícita de un cambio mínimo de UX).
3. **Given** restricciones de no descargar/rehostear, **When** una opción candidata las incumple, **Then** se descarta o se marca como incompatible con los principios del proyecto.

---

### User Story 4 - Dejar listo el siguiente paso de planificación (Priority: P2)

Como mantenedor, tras el veredicto quiero un paquete de hallazgos suficiente
para `/speckit-plan` (o para cerrar el tema sin más trabajo): impacto en
dependencias, documentación de usuario, pruebas manuales y gobernanza.

**Why this priority**: Evita un análisis que no se pueda ejecutar; reduce
retrabajo al planificar.

**Independent Test**: Comprobar que el entregable incluye riesgos, supuestos,
criterios de salida y una lista de cambios de producto/documentación si hay
adopción (o un cierre limpio si no).

**Acceptance Scenarios**:

1. **Given** un veredicto “adoptar alternativa X”, **When** se inicia la planificación, **Then** están listados los cambios de producto visibles (dependencia, mensajes, README) y los riesgos principales.
2. **Given** un veredicto “no sustituir”, **When** se cierra la feature, **Then** quedan documentadas mitigaciones opcionales (p. ej. mejor guía) y por qué no se cambia el proveedor.
3. **Given** incertidumbre residual no bloqueante, **When** se publica el análisis, **Then** las lagunas se enumeran sin impedir el veredicto principal.

---

### Edge Cases

- El addon de YouTube está instalado y actualizado (7.4.x+) pero un vídeo pide login: ¿la gramola ofrece fallback, mensaje claro, o parece un fallo de la gramola?
- El usuario tiene fallback yt-dlp instalado pero no el addon de YouTube (o al revés): ¿qué dependencias se declaran y cuál es el orden de intento?
- Un id del catálogo es válido en formato pero el vídeo ya no está disponible en la fuente.
- La alternativa funciona en unas versiones de Kodi y no en otras del destino del proyecto.
- La alternativa exige otra configuración compleja (cuenta, cookies, repositorio de terceros): ¿sigue siendo “más simple” que un login de YouTube en el addon?
- El fallback reproduce algunos títulos con login-wall y otros no (geo, edad, retirada): documentar límites honestos.
- Cambiar o duplicar proveedor rompe miniaturas, historial o el comportamiento al volver atrás.
- Adoptar un complemento entra en conflicto con la gobernanza actual: tratar la enmienda como requisito.
- Opciones que descarguen o almacenen vídeo localmente: fuera de política del producto.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El sistema de trabajo de esta feature MUST producir un análisis comparativo de opciones para la reproducción de entradas del catálogo, incluyendo al menos: (a) mantener solo el addon de YouTube (+ mitigaciones/mensajes ante login), (b) una o más alternativas o fallbacks en el ecosistema Kodi orientadas a reproducir sin login de cuenta los títulos que YouTube bloquea, y (c) un modo híbrido (YouTube por defecto + fallback para ciertos vídeos) si es viable.
- **FR-002**: Cada opción MUST evaluarse con criterios explícitos y compartidos: simplicidad para usuario inexperto (sin API key de desarrollador **y** sin login de cuenta YouTube cuando sea posible), cobertura de títulos con login-wall, viabilidad legal/ToS a alto nivel, compatibilidad con el destino Kodi moderno, impacto en el flujo años → canciones → reproducir, mantenimiento a medio plazo, y alineación con no rehostear ni descargar vídeo.
- **FR-003**: El análisis MUST concluir con un veredicto único accionable: fallback/complemento yt-dlp, sustitución total, mantener YouTube con mitigaciones, o diferir con condiciones claras.
- **FR-004**: Si el veredicto cambia o amplía la dependencia de reproducción respecto al solo-addon de YouTube, el entregable MUST incluir una propuesta de enmienda a la gobernanza del proyecto antes de cualquier implementación posterior.
- **FR-005**: El análisis MUST asumir que el catálogo sigue siendo CSV por año con título e identificador de vídeo de YouTube; MUST NOT proponer rehosteo ni un catálogo de ficheros locales como solución.
- **FR-006**: La opción recomendada MUST describir el recorrido del usuario inexperto desde la instalación hasta (a) reproducir un vídeo sin login-wall y (b) intentar un vídeo con login-wall, contando pasos no automáticos.
- **FR-007**: La opción recomendada MUST describir el comportamiento ante fallo del proveedor (ausente, mal configurado, vídeo no disponible, login requerido sin fallback).
- **FR-008**: El entregable MUST listar riesgos residuales (roturas del proveedor, ToS/scraping, repositorios de terceros, cambios de políticas, soporte desigual por versión de Kodi) y el hecho de que **no todos** los vídeos con login-wall tienen por qué ser reproducibles por un fallback.
- **FR-009**: El entregable MUST indicar pruebas manuales mínimas: al menos un vídeo OK sin login en YouTube 7.4.x+ y, si se conoce, un vídeo del catálogo que exija login (p. ej. el citado en el smoke de 001), contrastando con el fallback candidato.
- **FR-010**: Esta feature MUST NOT implementar el cambio de proveedor en el código del addon; la implementación, si procede, será una feature o plan posterior.
- **FR-011**: La comunicación y el entregable de esta feature MUST estar en español.
- **FR-012**: El análisis MUST registrar el hallazgo de smoke de que la API key ya no es requisito práctico en `plugin.video.youtube` 7.4.x+ para el recorrido feliz mayoritario, y MUST NOT basar el veredicto solo en el problema histórico de la API key.

### Key Entities

- **Proveedor de reproducción**: Componente externo (addon u otro mecanismo de Kodi) que convierte un identificador de vídeo del catálogo en una reproducción real. Hoy: addon de YouTube.
- **Opción evaluada**: Candidato de decisión con pros, contras, criterios puntuados o valorados cualitativamente, y resultado (viable / no viable / viable con matices).
- **Veredicto**: Decisión final documentada con justificación, impacto en usuario, impacto en gobernanza y siguientes pasos.
- **Fricción de configuración**: Pasos no triviales (API key histórica, **login de cuenta YouTube**, repos ZIP, cookies) antes de reproducir.
- **Login-wall**: Situación en la que el addon de YouTube exige autenticación de cuenta para un `video_id` concreto del catálogo.
- **MusicVideo / Year**: Sin cambio de modelo de contenido: año de catálogo y entrada `Artista - Canción` + id de vídeo de YouTube.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Existe un entregable de decisión revisable (en el directorio de esta feature) que un mantenedor puede usar para sí/no en menos de 15 minutos de lectura.
- **SC-002**: Al menos 3 opciones distintas quedan evaluadas con la misma tabla o lista de criterios (incluido “solo YouTube”, al menos un fallback/alternativa, y el modo híbrido o mitigaciones).
- **SC-003**: El veredicto declara de forma inequívoca: (a) si el recorrido feliz mayoritario exige API key (**no**, según smoke 7.4.x+), y (b) si el camino recomendado permite intentar títulos con login-wall sin login de cuenta (**sí / no / parcialmente**).
- **SC-004**: El 100% de las opciones que impliquen descargar o rehostear vídeo quedan marcadas como incompatibles con la política del producto.
- **SC-005**: Si se recomienda fallback o cambio de proveedor, el entregable incluye impacto en gobernanza y documentación; si no, incluye mitigaciones concretas ante login-wall.
- **SC-006**: Queda definida una checklist mínima de verificación manual en Kodi (≥ 3 pasos) que incluye al menos un título OK sin login y, si está identificado, un título con login-wall del catálogo.

## Assumptions

- El problema **vigente** (tras smoke 2026-07-28) es el **login selectivo** en ciertos vídeos, no la API key de desarrollador en `plugin.video.youtube` 7.4.x+.
- Los identificadores del CSV siguen siendo ids de YouTube; se busca otro **camino de reproducción** para casos bloqueados, no otro catálogo.
- El alcance de esta feature sigue siendo **análisis y decisión**; la implementación es posterior.
- “Saltar la restricción en ciertos vídeos” se interpreta como: ofrecer un proveedor alternativo/fallback que, en la práctica, pueda reproducir parte de los títulos con login-wall **sin** pedir al usuario que inicie sesión en el addon YouTube; no se garantiza cobertura del 100% de esos títulos.
- Aspectos legales/ToS del uso de extractores frente a políticas de la plataforma se tratan como riesgo de mantenedor, no como dictamen jurídico.
- Un modo **híbrido** (YouTube por defecto + fallback yt-dlp) es preferible a sustituir YouTube por completo si el smoke mayoritario ya funciona sin API key.
- Compatibilidad objetivo: Kodi moderno (Matrix+ / Nexus / Omega).
- Enmendar la constitución es prerrequisito de cualquier adopción de proveedor adicional o distinto.
