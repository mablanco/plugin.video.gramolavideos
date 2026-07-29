# Checklist editorial imprimible (E1–E6)

Fuente: `specs/004-catalogo-60-70/contracts/editorial-review.md`

Aplicar fila a fila sobre `candidates.md` antes de pasar a `publish-list.md`.

## Por candidato

Aplicado al batch de 60 candidatos en `candidates.md` (2026-07-29):

- [x] **E1** Artista/banda española (o justificación explícita en notes)
- [x] **E2** Vídeo musical / actuación de la época (60s o 70s según año)
- [x] **E3** Título en formato `Artista - Canción`
- [x] **E4** `video_id` válido (11 chars `[A-Za-z0-9_-]`)
- [x] **E5** Sin duplicar el mismo `video_id` en el mismo año
- [x] **E6** Año coherente con la canción (aprox.)

## Batch

- [x] Ningún candidato con `editorial_ok=false` o `format_ok=false` entra en publish
- [x] Umbrales previos: ≥40 filas, ≥8 años, ≥1 año en 1960–69 y ≥1 en 1970–79
- [x] Firma mantenedor (commit / PR)
