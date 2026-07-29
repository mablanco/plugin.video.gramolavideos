# Contract: Navegación del plugin (v2 — décadas)

**Feature**: `003-navegacion-videos`  
**Supersedes (runtime)**: `specs/001-auditoria-codigo/contracts/plugin-navigation.md`
para el nivel raíz y el parámetro `mode=decade`. El contrato 001 permanece como
**histórico** de la navegación plana años→canciones; no borrarlo.

## Flujo

1. Sin `mode`: listar **décadas** (directorios) derivadas de años con CSV.
2. `mode=decade` + `foldername=<D>` donde `D` es año inicio de década (`1960`, `1970`, …): listar años de esa década.
3. `mode=year` + `foldername=<YYYY>`: listar canciones (sin cambio).
4. `mode=song` + `foldername=<video_id>`: reproducción YouTube (sin cambio).

## Query string

| Param | Values | Notes |
|-------|--------|-------|
| `mode` | omitido \| `decade` \| `year` \| `song` | |
| `foldername` | década \| año \| `video_id` | Legacy name; no renombrar |

## Etiquetas

- ES por defecto: `Años 60`, `Años 70`, `Años 80`, `Años 90` para `D` en 1960…1990.
- MUST pasar por mecanismo de idioma del addon (no literales dispersos nuevos sin ruta i18n).

## Reglas de agrupación

- `decade_id = (int(year) // 10) * 10`
- Solo décadas con ≥1 año presente
- Orden: décadas y años ascendentes

## Reproducción / errores

Igual que contrato 001: YouTube URI; notificar errores de catálogo sin tumbar listado residual.
