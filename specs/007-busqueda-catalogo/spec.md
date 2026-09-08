# Feature Specification: Búsqueda en catálogo

**Feature Branch**: `[007-busqueda-catalogo]`

**Created**: 2026-07-29

**Updated**: 2026-07-29

**Status**: Draft

**Input**: User description: handoff
`specs/005-busqueda-favoritos/handoff-busqueda.md` (“Búsqueda local…
ítem Buscar; query título/artista local; resultados reproducibles o enlace
al año; vacío claro; exclusiones remota/filtros/favoritos/…”); adaptación
de la spec ya existente en `specs/007-busqueda-catalogo/`.

## Contexto y problema

Hoy el oyente solo localiza una canción recorriendo la jerarquía del catálogo
(décadas → años → canciones). Si no recuerda el año, el recorrido es lento,
sobre todo cuando el catálogo crece (p. ej. tras `004-catalogo-60-70`).

El estudio `005-busqueda-favoritos` decidió **separar búsqueda y favoritos**,
con **búsqueda en segundo lugar**. Esta feature implementa **solo búsqueda
local** sobre el catálogo editorial del addon: ítem **Buscar** en la raíz,
query de texto sobre título/artista, resultados usables y vacío claro. No
incluye marcar/listar favoritos, no busca en YouTube web y no sustituye el
browse cronológico de `003`.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Buscar por texto en el catálogo local (Priority: P1)

Como oyente con mando de TV, quiero escribir un trozo del artista o de la
canción y ver coincidencias **solo del catálogo del addon**, sin adivinar el
año.

**Why this priority**: Valor principal; `SearchCapability.query_scope` =
`local_catalog`.

**Independent Test**: Abrir Buscar, introducir texto que coincida con una
entrada conocida y verla en resultados; repetir sin coincidencias y ver vacío
claro.

**Acceptance Scenarios**:

1. **Given** el addon con catálogo cargado, **When** el usuario abre **Buscar**
   en la raíz e introduce un texto que coincide con parte del artista o del
   título de una entrada del catálogo, **Then** ve al menos esa coincidencia
   en resultados.
2. **Given** una consulta sin coincidencias en el catálogo local, **When** se
   muestran resultados, **Then** ve un estado vacío comprensible
   (`empty_behavior`), no un fallo opaco ni resultados de fuera del catálogo.
3. **Given** varias coincidencias, **When** se listan, **Then** cada ítem
   muestra título comprensible (artista / canción) y permite **reproducir** o
   un **enlace/camino al año** de esa entrada, de forma consistente con el
   resto del addon.

---

### User Story 2 - Usar un resultado hasta oír la canción (Priority: P1)

Como oyente, quiero que un resultado me lleve a reproducir la canción (o al
año desde el que puedo reproducirla) con la misma experiencia que el browse.

**Why this priority**: Sin cierre hasta reproducción, la búsqueda no aporta.

**Independent Test**: Desde un resultado válido, reproducir (o abrir el año y
reproducir) y comparar con el flujo desde el listado del año.

**Acceptance Scenarios**:

1. **Given** un resultado resoluble en el catálogo, **When** el usuario lo
   selecciona para reproducir (o sigue el enlace al año y reproduce), **Then**
   la reproducción se comporta como al reproducir esa misma canción desde su
   año.
2. **Given** un fallo recuperable al reproducir, **When** ocurre desde
   búsqueda, **Then** hay aviso amigable y no hay aborto catastrófico.

---

### User Story 3 - Resultados manejables (orden y límite) (Priority: P1)

Como oyente, quiero que con muchas coincidencias la lista siga siendo usable
con mando: orden predecible y límite de resultados acotado en el MVP.

**Why this priority**: El handoff exige acotar ordenación/límite; tras ampliar
catálogo es crítico en TV.

**Independent Test**: Buscar un término genérico con muchas coincidencias;
comprobar orden documentado y que el tope (si aplica) es comprensible.

**Acceptance Scenarios**:

1. **Given** muchas coincidencias, **When** se muestran resultados, **Then**
   el listado sigue un **orden predecible documentado** (p. ej. alfabético por
   título mostrado).
2. **Given** un volumen de coincidencias por encima del tope de producto del
   MVP, **When** se listan, **Then** solo se muestran hasta ese límite de forma
   comprensible (sin filtros avanzados ni paginación compleja obligatoria).
3. **Given** texto con distinta capitalización que el catálogo, **When** se
   busca, **Then** las coincidencias no exigen acertar mayúsculas/minúsculas.

---

### User Story 4 - Independencia de favoritos y simplicidad (Priority: P2)

Como oyente y mantenedor, quiero Buscar como ítem extra en la raíz, usable
sin favoritos, sin cuenta online y sin hinchar el producto.

**Why this priority**: Veredicto 005 + invariantes del handoff (simplicidad;
teclado TV = fricción a cuidar).

**Independent Test**: Usar solo búsqueda sin favoritos; browse cronológico
intact; exclusiones revisables en la spec.

**Acceptance Scenarios**:

1. **Given** el addon con búsqueda, **When** el usuario no usa Buscar, **Then**
   puede recorrer décadas → años → canciones → reproducir como hasta ahora.
2. **Given** favoritos presentes o no (`006`), **When** usa la búsqueda,
   **Then** consultar y listar resultados **no exige** favoritos.
3. **Given** el alcance de esta feature, **When** se revisan exclusiones,
   **Then** quedan fuera: búsqueda remota / YouTube global; filtros
   avanzados, fuzzy online, sinónimos; recomendaciones; marcar/listar
   favoritos; cambiar el CSV como fuente editorial o el proveedor de
   reproducción; cuenta online obligatoria.

---

### Edge Cases

- **Catálogo vacío**: Buscar accesible; vacío o aviso comprensible.
- **Consulta vacía / solo espacios / cancelada**: no listar “todo el
  catálogo” como si fueran resultados.
- **Consulta muy corta o muy larga**: usable (mínimo de caracteres o truncado
  simple permitido) sin bloquear “parte del nombre”.
- **Entradas corruptas/incompletas**: no tumbar toda la búsqueda; omitir o
  avisar.
- **Teclado en TV**: fricción aceptada en el MVP; sin voz ni sugerencias
  predictivas obligatorias; el plan debe cuidar el flujo de entrada.
- **Favoritos**: no son parte de esta feature; acciones de contexto sobre un
  resultado MAY existir si `006` ya está, pero no son requisito.
- **Momento de implementación**: **recomendado** tras `004` (o semilla mínima
  amplia) y con navegación `003`; se puede planificar antes si hay catálogo
  suficiente para probar.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El addon MUST exponer en la raíz un ítem **Buscar** junto al
  recorrido del catálogo (décadas/años) y a Favoritos si existe, sin sustituir
  el browse cronológico.
- **FR-002**: El usuario MUST poder introducir una query de texto y obtener
  coincidencias solo sobre el **catálogo editorial local** (campos de
  título/artista de las entradas del addon), no sobre YouTube web ni otras
  fuentes remotas (`query_scope`: `local_catalog`).
- **FR-003**: La coincidencia MUST ser usable sin capitalización exacta.
- **FR-004**: Los resultados MUST ser usables con mando; cada resultado
  resoluble MUST permitir **reproducción** con el mismo mecanismo YouTube que
  el resto del addon **o** un **enlace/camino al año** de esa entrada desde el
  que se pueda reproducir.
- **FR-005**: Una consulta sin coincidencias MUST mostrar vacío comprensible
  (`empty_behavior`).
- **FR-006**: El producto MUST definir y aplicar **ordenación predecible** y
  un **límite** de resultados mostrados en el MVP cuando el volumen sea alto,
  de forma comprensible para el oyente.
- **FR-007**: Ante errores recuperables al buscar o al usar un resultado, el
  addon MUST avisar de forma amigable y MUST NOT abortar de forma catastrófica.
- **FR-008**: Esta feature MUST NOT exigir: búsqueda remota / YouTube global;
  filtros avanzados, fuzzy online o sinónimos; recomendaciones; favoritos;
  cuenta online; cambiar el CSV editorial como fuente ni el proveedor de
  reproducción.
- **FR-009**: La búsqueda MUST poder usarse y demostrarse **sin depender** de
  favoritos.
- **FR-010**: La búsqueda MUST NOT alterar ni sustituir el catálogo editorial
  (CSV por año) como fuente de canciones publicadas.
- **FR-011**: La documentación de uso orientada a humanos (p. ej. README) MUST
  describir Buscar como acceso adicional al flujo de navegación cuando la
  capacidad esté disponible.

### Key Entities

- **Year**: unidad de datos/navegación del catálogo.
- **MusicVideo** / **CatalogEntry**: artista/canción + id de reproducción;
  pertenece a un Year; ámbito de la query.
- **Search query**: texto del usuario sobre el catálogo local.
- **Search result**: coincidencia de una CatalogEntry; puede llevar a
  reproducción o al Year.
- **SearchCapability** (perfil de producto heredado de 005):
  `query_scope` = `local_catalog`; `match_fields` = título (artista + canción);
  `empty_behavior` = listado vacío + mensaje claro; `out_of_scope` = remoto,
  filtros avanzados, favoritos.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Un oyente que conoce parte del título o artista puede
  localizarla vía Buscar y lanzar reproducción (directa o vía año) en menos de
  2 minutos (mando/TV, sin cuenta ni configuración extra).
- **SC-002**: En ≥95 % de las pruebas con entrada en catálogo y query con
  fragmento claro de artista/título, la entrada aparece entre los resultados
  **mostrados** (respetando el límite MVP).
- **SC-003**: El 100 % de las pruebas sin coincidencias muestran vacío
  comprensible y ninguna salida catastrófica.
- **SC-004**: Usar un resultado válido ofrece la misma clase de experiencia de
  reproducción que desde el año de esa canción en ≥95 % de intentos con
  entradas válidas.
- **SC-005**: Un revisor confirma que Buscar es independiente de Favoritos,
  que el browse cronológico sigue como camino principal, y que remota /
  filtros / recomendaciones quedan fuera; y que orden + límite de resultados
  están definidos para el MVP.

## Assumptions

- Alcance = prompt de
  [handoff-busqueda.md](../005-busqueda-favoritos/handoff-busqueda.md) y
  veredicto 005 (búsqueda **2º** tras favoritos `006`).
- **Dependencia recomendada de implementación**: tras `004-catalogo-60-70` (o
  semilla mínima amplia); no bloquea planificar la feature ahora.
- Coincidencia MVP: subcadena sobre artista y/o título; sin ranking
  “inteligente” ni stemming.
- Orden por defecto: alfabético por título mostrado; el plan fija el número
  concreto del tope de resultados.
- Consulta vacía/cancelada: no listar todo el catálogo como resultados.
- Entrada raíz etiquetada de forma clara (p. ej. “Buscar”).
- Teclado TV: fricción conocida; el plan cuida el flujo de entrada sin ampliar
  a voz/autocompletado avanzado.
- Textos según idioma del proyecto (español prioritario; no bloquear i18n).
