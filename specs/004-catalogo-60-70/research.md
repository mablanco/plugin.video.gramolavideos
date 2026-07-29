# Research: Semilla de catálogo 60s/70s

**Feature**: `004-catalogo-60-70`  
**Date**: 2026-07-29

## R-001: Qué significa “automático”

**Decision**: Automatización **offline de contribución** (generar candidatos +
validar formato/ids), con **revisión humana** antes de merge. El addon **no**
descubre catálogo en runtime.

**Rationale**: Constitution I (catálogo como datos) y FR-003; evita red/ToS en
el path del oyente.

**Alternatives considered**:
- Scrape continuo al abrir el addon — rechazado (I, II, VIII, identidad).
- Solo curación 100 % manual — no cumple el espíritu “asistido” aunque válido
  como fallback si falla la herramienta.

## R-002: Pipeline de semilla

**Decision**: Pipeline en 5 pasos (contrato `seed-process.md`):

1. **Candidatos**: lista de `Artista - Canción` + año editorial (60/70 ES),
   generada con asistencia (IA/listas históricas) en el entorno del mantenedor.
2. **Resolución de video_id**: buscar id público YouTube del tema (manual o
   asistido); rechazar si no hay id usable.
3. **Validación mecánica**: formato fila, `VIDEO_ID_RE`, sin duplicar id en el
   mismo año; reutilizar lógica de `catalog` en host.
4. **Revisión editorial**: checklist (contrato `editorial-review.md`).
5. **Muestreo smoke**: ≥5 ids 60s + ≥5 70s (oEmbed/Kodi); sustituir o
   documentar fallos (FR-010 / SC-004).

**Output**: CSV solo para años con ≥1 fila aceptada; commit + README.

## R-003: Volumen y distribución

**Decision**: Cumplir mínimos de spec sin rellenar los 20 años obligatoriamente:

- ≥40 entradas en 1960–1979
- ≥8 años distintos
- ≥1 año en 1960–1969 y ≥1 en 1970–1979
- Preferir repartir (~2–8 temas/año sembrado) frente a un único año masivo

## R-004: Fuentes y riesgos

**Decision**: Priorizar temas reconocibles del pop/rock/canción española de la
época; ids de vídeos **públicamente listados**. No embeber descargas. No
commitear claves API. Fallos de login-wall: mismo criterio que catálogo actual
(sustituir id o deuda documentada; ver 002).

## R-005: Relación con 003 / tests

**Decision**: 004 puede aterrizar **antes o en paralelo** a 003. Si 003 no está,
el listado plano crecerá (~+8…20 carpetas): aceptable temporalmente; priorizar
003 si el mantenedor percibe dolor inmediato.

Actualizar tests que fijan `19` años / rango 1980–1999.

## Alternatives considered

| Alternativa | Por qué no |
|-------------|------------|
| Un solo `60s.csv` agregando años | Rompe convención CSV-por-año / `list_years` |
| Base &lt;40 “para empezar” | Incumple FR-006 acordado en spec |
| Publicar sin smoke | Incumple FR-010 |
