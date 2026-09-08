# Feature Specification: Favoritos de usuario

**Feature Branch**: `[006-favoritos]`

**Created**: 2026-07-29

**Updated**: 2026-07-29

**Status**: Draft

**Input**: User description: handoff `specs/005-busqueda-favoritos/handoff-favoritos.md`
(“Favoritos de usuario… solo favoritos; MVP add/list/remove + persistencia
local + huérfanos hide_or_notify; exclusiones multi-listas/nube/búsqueda/…”);
adaptación de la spec ya existente en `specs/006-favoritos/`.

## Contexto y problema

Hoy el oyente solo llega a una canción recorriendo la jerarquía del catálogo
(décadas → años → canciones). No hay forma de **marcar / desmarcar** temas
habituales ni de **reabrirlos** desde un acceso rápido sin volver a buscar el
año.

El estudio `005-busqueda-favoritos` decidió **separar favoritos y búsqueda**,
con **favoritos primero**. Esta feature implementa **solo favoritos**:
preferencias del usuario por instalación/perfil, conviviendo con la navegación
de `003` como **entrada adicional en la raíz**, sin sustituir el browse
cronológico, sin búsqueda por texto y sin alterar el catálogo editorial.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Añadir (y reconocer) un favorito (Priority: P1)

Como oyente con mando de TV, quiero marcar una canción del catálogo como
favorita cuando la veo, para recuperarla después sin recordar el año.

**Why this priority**: Sin “añadir”, no hay lista útil (`FavoritesCapability.actions`:
add).

**Independent Test**: Desde el listado de canciones de un año, añadir un
favorito y comprobar que aparece en Favoritos y no se duplica si se vuelve a
marcar.

**Acceptance Scenarios**:

1. **Given** el usuario en el listado de canciones de un año del catálogo, **When** elige añadir a favoritos, **Then** esa canción queda guardada y puede abrirse desde el acceso Favoritos.
2. **Given** una canción ya favorita, **When** el usuario la vuelve a ver en el catálogo, **Then** puede reconocer el estado (indicación o acción de quitar/desmarcar) y **MUST NOT** duplicarse en la lista.
3. **Given** el marcado completado, **When** cierra y reabre el addon en la misma instalación/perfil, **Then** el favorito sigue disponible (persistencia local).

---

### User Story 2 - Listar y reproducir desde la raíz (Priority: P1)

Como oyente, quiero un ítem **Favoritos** en la raíz del addon para listar mi
conjunto personal y reproducir una entrada resoluble igual que desde su año.

**Why this priority**: Acceso rápido y reproducción (`actions`: list + play vía
catálogo).

**Independent Test**: Abrir Favoritos desde la raíz, reproducir un favorito
válido; comprobar que décadas/años siguen disponibles en paralelo.

**Acceptance Scenarios**:

1. **Given** el addon con favoritos, **When** el usuario abre la gramola, **Then** ve Favoritos en la raíz junto al recorrido del catálogo (no en sustitución).
2. **Given** la lista no vacía, **When** entra en Favoritos, **Then** ve títulos comprensibles (artista / canción) y puede seleccionar una para reproducir.
3. **Given** un favorito aún presente en el catálogo editorial, **When** lo reproduce desde Favoritos, **Then** la experiencia de reproducción es la misma que desde su año (mismo proveedor YouTube; sin rehosteo ni fuente distinta).

---

### User Story 3 - Quitar / desmarcar un favorito (Priority: P1)

Como oyente, quiero quitar canciones de Favoritos (desde la lista o
desmarcando en el catálogo) para mantener la lista útil.

**Why this priority**: Sin remove, la lista se ensucia (`actions`: remove).

**Independent Test**: Quitar un favorito y comprobar que desaparece de la lista
sin borrar la entrada del catálogo editorial.

**Acceptance Scenarios**:

1. **Given** un favorito en la lista, **When** el usuario lo quita, **Then** deja de aparecer en Favoritos.
2. **Given** un favorito quitado, **When** vuelve al año de esa canción, **Then** la canción sigue en el catálogo editorial (quitar ≠ borrar CSV / fila).
3. **Given** Favoritos vacío tras quitar el último, **When** abre Favoritos, **Then** ve un estado vacío comprensible, no un fallo opaco.

---

### User Story 4 - Huérfanos y tolerancia (Priority: P1)

Como oyente, quiero que si una canción favorita desaparece del catálogo
editorial (p. ej. fila o año eliminado), el addon no se rompa y yo pueda
entenderlo y limpiar la preferencia.

**Why this priority**: El handoff exige política `hide_or_notify` en el MVP.

**Independent Test**: Simular un favorito cuya entrada ya no está en el
catálogo; abrir Favoritos y/o intentar reproducir; comprobar aviso u ocultación
comprensible y posibilidad de quitar si sigue visible.

**Acceptance Scenarios**:

1. **Given** un favorito huérfano, **When** el usuario abre Favoritos, **Then** la entrada o bien no se lista (ocultar) o se muestra de forma que se entiende que no está disponible (avisar / marcar), sin cierre catastrófico.
2. **Given** un favorito huérfano aún visible, **When** intenta reproducirlo, **Then** recibe un aviso amigable y puede quitarlo de Favoritos.
3. **Given** errores recuperables al abrir o persistir favoritos, **When** ocurren, **Then** hay aviso amigable y el addon no aborta de forma catastrófica.

---

### User Story 5 - Convivir con la gramola simple (Priority: P2)

Como mantenedor y oyente, quiero que Favoritos sea solo preferencias de
usuario: no fusionar con el CSV, no cuenta online, no búsqueda, y sin hinchar
el producto con multi-listas o sync.

**Why this priority**: Invariantes del handoff y veredicto 005.

**Independent Test**: Revisar exclusiones e invariantes en la spec y en el
comportamiento documentado; browse cronológico intacto sin usar Favoritos.

**Acceptance Scenarios**:

1. **Given** el addon con favoritos, **When** el usuario no usa Favoritos, **Then** puede recorrer décadas → años → canciones → reproducir como hasta ahora.
2. **Given** favoritos guardados, **When** se inspecciona el modelo de producto, **Then** CSV = fuente editorial y favoritos = preferencias (no filas nuevas del catálogo maestro).
3. **Given** el alcance de esta feature, **When** se revisan exclusiones, **Then** quedan fuera: multi-listas/carpetas, sync nube / multi-dispositivo, playlists colaborativas, recomendaciones, búsqueda por texto, cuenta online obligatoria, y cambiar el proveedor de reproducción o el formato de filas del catálogo.

---

### Edge Cases

- **Lista vacía al primer uso**: Favoritos accesible; estado vacío claro.
- **Favorito huérfano**: política `hide_or_notify` (US4); nunca tumbar el addon.
- **Doble marcado**: una sola entrada en la lista.
- **Muchos favoritos**: listado lineal usable con mando; sin paginación avanzada
  ni carpetas en el MVP.
- **Perfil / instalación distinta**: no hay sync; cada perfil/instalación tiene
  su lista.
- **Reproducción fallida del proveedor**: mismo tipo de tolerancia que desde el
  catálogo.
- **Convivencia con `003`**: Favoritos es ítem extra en la raíz junto a décadas
  (o el primer nivel vigente); no depende de `004` para entregarse.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El addon MUST permitir **añadir** una canción del catálogo como
  favorita desde el contexto del listado de canciones (acción explícita).
- **FR-002**: El addon MUST exponer en la raíz una entrada **Favoritos** que
  conviva con el browse del catálogo (años/décadas), sin sustituirlo.
- **FR-003**: El addon MUST **listar** las canciones favoritas con título
  comprensible (equivalente al del catálogo).
- **FR-004**: El usuario MUST poder **reproducir** desde Favoritos una entrada
  aún resoluble en el catálogo, con el mismo mecanismo YouTube que el resto del
  addon.
- **FR-005**: El usuario MUST poder **quitar / desmarcar** un favorito; eso
  MUST NOT eliminar ni alterar filas del catálogo editorial.
- **FR-006**: Los favoritos MUST **persistir** entre sesiones en la misma
  instalación/perfil (`storage_scope`: per_install_or_profile).
- **FR-007**: Añadir de nuevo una canción ya favorita MUST NOT crear
  duplicados.
- **FR-008**: Ante favoritos huérfanos, el addon MUST aplicar la política
  **`hide_or_notify`**: ocultarlos del listado y/o mostrarlos como no
  disponibles con aviso comprensible; al intentar reproducir uno visible MUST
  avisar de forma amigable; MUST NOT abortar de forma catastrófica.
- **FR-009**: Favoritos vacíos MUST presentarse de forma comprensible.
- **FR-010**: Esta feature MUST NOT exigir: multi-listas o carpetas de
  favoritos; sincronización en la nube o multi-dispositivo; playlists
  colaborativas; recomendaciones; cuenta online; búsqueda por texto; fusionar
  favoritos en el CSV editorial; cambiar el proveedor YouTube o el formato de
  las filas del catálogo.
- **FR-011**: El catálogo CSV por año MUST seguir siendo la única fuente
  editorial de canciones publicadas; favoritos MUST modelarse solo como
  preferencias de usuario.
- **FR-012**: La documentación de uso orientada a humanos (p. ej. README) MUST
  describir Favoritos como acceso adicional al flujo de navegación cuando la
  capacidad esté disponible.

### Key Entities

- **Year**: unidad de datos/navegación del catálogo; sin cambio de rol.
- **MusicVideo** / **CatalogEntry**: artista/canción + id de reproducción;
  pertenece a un Year; es lo referenciado por un favorito.
- **Favorite**: preferencia del usuario que apunta a una CatalogEntry (o su
  identidad estable); pertenece a la instalación/perfil, no al CSV.
- **Favorites list**: conjunto de Favorite bajo la entrada Favoritos; puede
  estar vacío.
- **FavoritesCapability** (perfil de producto heredado de 005):
  `actions` = add / list / remove; `orphan_policy` = `hide_or_notify`;
  `storage_scope` = per_install_or_profile.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Un oyente puede añadir una canción a Favoritos y verla listada en
  menos de 1 minuto desde el listado de canciones (mando/TV, sin cuenta ni
  configuración extra).
- **SC-002**: En ≥95 % de los intentos con favoritos aún en el catálogo,
  reproducir desde Favoritos equivale a reproducir desde el año de esa canción.
- **SC-003**: Tras reiniciar el addon (misma instalación/perfil), el 100 % de
  los favoritos válidos de la sesión anterior siguen listados hasta que el
  usuario los quite.
- **SC-004**: Con lista vacía o favorito huérfano, el 100 % de las pruebas
  manuales muestran estado/aviso comprensible (`hide_or_notify`) y ninguna
  salida catastrófica.
- **SC-005**: Un revisor confirma en documentación de producto que Favoritos es
  acceso adicional, que el browse cronológico sigue siendo el camino principal,
  y que búsqueda / multi-listas / sync nube quedan fuera de este alcance.

## Assumptions

- Alcance = prompt de [handoff-favoritos.md](../005-busqueda-favoritos/handoff-favoritos.md)
  y veredicto de 005 (favoritos 1º; búsqueda = `007-busqueda-catalogo` u
  equivalente).
- Orden por defecto de la lista: más recientemente añadidos primero, salvo
  justificación simple en el plan.
- Marcar/quitar usable con mando (acción de contexto o equivalente); detalle
  de UI en planificación.
- `hide_or_notify`: el plan puede elegir ocultar, avisar, o ambos, siempre que
  cumpla FR-008 y SC-004; no se exige sync de limpieza automática del
  almacenamiento más allá de no romper la UI.
- No requiere semilla `004` ni cuenta online.
- Textos según idioma del proyecto (español prioritario; no bloquear i18n).
