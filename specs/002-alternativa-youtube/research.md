# Research: Alternativa al addon de YouTube

**Feature**: `002-alternativa-youtube`  
**Date**: 2026-07-25  
**Updated**: 2026-07-28 (reframe tras smoke Kodi M1–M3)

## R-001: Naturaleza del problema (reframe post-smoke)

**Decision**: Separar dos fricciones distintas:

| Fricción | Estado tras smoke 2026-07-28 | Impacto en veredicto |
|----------|------------------------------|----------------------|
| API key / consola de desarrollador Google | **Mitigada** en la práctica con `plugin.video.youtube` **7.4.x** (Kodi 20.5 Nexus): el recorrido feliz mayoritario reproduce **sin** API key | Ya **no** justifica por sí sola sustituir YouTube |
| Login de cuenta YouTube en **ciertos** vídeos | **Confirmada** (p. ej. catálogo 1984 *La Unión - Eclipse total*); restricción del lado YouTube/addon, no bug de Gramola | **Problema vigente** a resolver con alternativa/fallback |

Fuente: `specs/001-auditoria-codigo/validation-log.md` (nota del smoke M1–M3).

**Rationale**: El input original de la feature asumía API key como bloqueo principal
(evidencia de issues/wiki 2025). El smoke del mantenedor en 7.4.x invalida ese
diagnóstico como único motor de decisión. Seguir recomendando “sustituir YouTube
por API key” sería resolver un problema que ya no duele, ignorando el que sí.

**Alternatives considered**:
- Ignorar el smoke y mantener el diagnóstico API-key — rechazado (FR-012).
- Tratar el login-wall como fuera de alcance — rechazado: es el dolor residual
  explícito del mantenedor (“saltar la restricción en ciertos vídeos”).

## R-002: Criterios de evaluación (actualizados)

**Decision**: Puntuar con C1–C8:

| Id | Criterio | Qué “bien” significa |
|----|----------|----------------------|
| C1 | Sin API key de desarrollador | Recorrido mayoritario sin consola Google |
| C2 | Sin rehost / sin descarga-solución | Solo stream; no almacenar vídeo en el addon |
| C3 | Catálogo intacto | Ids de YouTube en CSV |
| C4 | Flujo años → canciones → play | Sin rediseño de navegación |
| C5 | Compatibilidad Kodi Matrix+ | Destino moderno del proyecto |
| C6 | Sostenibilidad / ToS | Riesgos explícitos; dependencia sustituible |
| C7 | Instalabilidad | Preferible repo oficial; ZIP = fricción media |
| C8 | Cobertura login-wall | Puede intentar reproducir títulos que YouTube bloquea tras login, **sin** forzar login de cuenta en el addon oficial |

**Rationale**: C1 ya lo cumple YouTube 7.4.x; **C8** es el diferencial que motiva
seguir con una alternativa.

## R-003: Opciones evaluadas (rescoring)

### Opción A — Solo `plugin.video.youtube` + mitigaciones

| Criterio | Valoración |
|----------|------------|
| C1 | **Bien** — smoke 7.4.x sin API key en recorrido mayoritario |
| C2–C5, C7 | Bien |
| C6 | Media — frágil ante cambios Google |
| C8 | **Mal** — los títulos con login-wall siguen pidiendo cuenta |

**Mitigaciones**: mensaje claro (“este vídeo pide cuenta YouTube”); guía de
login opcional; listar en README títulos conocidos problemáticos.

**Conclusión parcial**: Válida como **proveedor por defecto**, insuficiente
sola si el objetivo es C8.

### Opción B — `plugin.video.tubed`

Sin cambio material: no aporta C8 de forma fiable; historial de cuotas. **No
recomendada** como primaria ni como fallback.

### Opción C — `plugin.video.sendtokodi` (yt-dlp) como **fallback / complemento**

| Criterio | Valoración |
|----------|------------|
| C1 | Bien — sin API key |
| C2–C5 | Bien |
| C6 | Media-baja — yt-dlp + ToS/scraping; cobertura login-wall **no garantizada al 100%** |
| C7 | Media — ZIP/repo tercero |
| C8 | **Bien (parcial)** — candidato a reproducir *parte* de los títulos con login-wall sin login en el addon YouTube |

URI: `plugin://plugin.video.sendtokodi/?url=` + watch URL del `video_id`.

**Conclusión parcial**: Mejor papel = **fallback para ciertos vídeos**, no
sustitución ciega de YouTube (que ya funciona bien en el caso general).

### Opción G — **Híbrido** (YouTube por defecto + fallback yt-dlp)

| Criterio | Valoración |
|----------|------------|
| C1 | Bien (vía YouTube 7.4.x+) |
| C8 | Bien (parcial) vía fallback |
| C4 | Bien si el fallback es transparente o con un reintento/menú mínimo |
| C7 | Media — hace falta instalar el fallback además de YouTube |
| Complejidad | Media — justificada en Complexity Tracking |

**Conclusión parcial**: **Mejor alineación** con el smoke + el deseo de cubrir
login-wall en ciertos vídeos.

### Opciones D–F

Sin cambio: D (forks inmaduros / descarga) rechazadas como primaria; E (yt-dlp
dentro de Gramola) rechazada; F (rehost) incompatible.

## R-004: Veredicto accionable (actualizado 2026-07-28)

**Decision**: **Mantener solo `plugin.video.youtube`** como proveedor.
**Descartar** el modo híbrido y cualquier dependencia de SendToKodi / yt-dlp
como fallback de Gramola.

Motivo: el smoke muestra que los fallos “sign in” observados corresponden a
vídeos **privados o no disponibles**; un fallback no los salva y añade fricción
(ZIP, Deno, reproducción poco fiable vía JSON-RPC). La API key ya no es el
problema principal en 7.4.x+.

Acciones de producto acordadas:

1. Auditar y corregir **todos** los ids del catálogo.
2. Mejorar mensajes de usuario ante no reproducible / sign-in.
3. No enmendar constitution II por un segundo proveedor.

**Alternatives considered**: híbrido (R-003 G) — rechazado tras smoke C8 y
pruebas de integración; sustitución total por SendToKodi — rechazada.

## R-005: Impacto en gobernanza (borrador)

**Decision**: Enmienda MINOR del principio II para permitir **proveedor
principal + proveedor de respaldo** declarados, ambos sin rehost, tipicamente
YouTube + resolución yt-dlp. Ver
`contracts/constitution-amendment-draft.md`.

## R-006: Contrato de integración futuro (híbrido)

**Decision** (feature de implementación posterior):

1. Mantener resolve a YouTube como camino por defecto.
2. Añadir estrategia de fallback (reintento automático ante fallo/login, o
   acción/contexto “Reproducir con proveedor alternativo”) vía URI SendToKodi.
3. Declarar dependencias: YouTube required; fallback recommended/optional o
   required según decisión de UX en la feature de implementación.
4. Mensajes: distinguir “pide cuenta YouTube” vs “instala fallback” vs “vídeo
   no disponible”.
5. Encapsular en `kodi_plugin` (constitution VII).
6. Miniaturas HTTPS sin cambio.

**Rationale**: Diff acotado; maximiza C8 sin romper el happy path.

## R-007: Riesgos residuales

| Riesgo | Severidad | Mitigación |
|--------|-----------|------------|
| Fallback no salta todos los login-wall | Alta | Smoke con título conocido; documentar “parcial”; no prometer 100% |
| ToS / políticas de la plataforma | Media-alta | Solo stream; README de riesgos; no promocionar descarga |
| YouTube 7.4.x vuelve a exigir API key | Media | Reabrir veredicto; el híbrido ya tiene plan B extractor |
| Complejidad de dos proveedores | Media | YAGNI: un solo fallback; sin UI elaborada al inicio |
| ZIP / repo tercero | Media | Documentar instalación; mensaje si falta |
| yt-dlp se rompe | Alta | Auto-update en el addon fallback; reevaluar |

## R-008: Pruebas manuales

Ver `quickstart.md` actualizado: (1) vídeo OK sin login en YouTube 7.4.x;
(2) vídeo con login-wall (p. ej. *Eclipse total*); (3) mismo id vía SendToKodi
sin cuenta YouTube en el addon oficial.
