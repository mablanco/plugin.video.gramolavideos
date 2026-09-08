# Contrato: navegación del plugin — categoría del año

**Feature**: `008-ano-visible`  
**Complementa**: `specs/003-navegacion-videos/contracts/plugin-navigation.md`

## Regla para `mode=year`

Para cada invocación con `mode=year` y `foldername=<YYYY>`, antes de finalizar
el directorio el addon MUST invocar:

```python
xbmcplugin.setPluginCategory(handle, year_id)
```

`year_id` MUST ser exactamente el identificador recibido en `foldername`. Por
ejemplo, `mode=year&foldername=1985` establece la categoría `1985`.

La llamada debe aplicarse aunque `catalog.load_year` devuelva cero canciones o
errores recuperables; la notificación y el listado residual conservan su
comportamiento vigente.

## Query string

No hay cambios en los parámetros ni en la forma de las URL:

| Parámetro | Valor para canciones de año |
|-----------|------------------------------|
| `mode` | `year` |
| `foldername` | `YYYY` |

No se añade un parámetro de categoría ni se modifica la URL de las canciones
(`mode=song&foldername=<video_id>`).

## Límites

- No se modifica la categoría en la vista `mode=decade` como parte de este
  contrato.
- Las etiquetas de las canciones no se prefijan con el año.
- La reproducción por YouTube y el flujo décadas → años → canciones →
  reproducción permanecen sin cambios.
