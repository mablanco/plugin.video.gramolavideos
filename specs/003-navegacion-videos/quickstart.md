# Quickstart: Validar navegación por décadas

**Feature**: `003-navegacion-videos`

## Prerrequisitos

- Repo con catálogo en `resources/csv/`
- `pip install -r requirements-dev.txt`
- Kodi Matrix+ con el addon + `plugin.video.youtube` (smoke manual)

## Validación automatizada (tras implementar)

```bash
python -m pytest -q tests/unit/test_catalog_*.py tests/unit/test_plugin_*.py
```

Esperado: tests de `list_decades` / `mode=decade`; raíz ya no asume N años planos
como único primer nivel.

## Smoke documental (antes de código)

1. Leer [decision.md](./decision.md): veredicto = década→año.
2. Comprobar criterios C1–C5 en [research.md](./research.md).
3. Revisar [contracts/plugin-navigation.md](./contracts/plugin-navigation.md).

## Smoke Kodi (después de código)

1. Abrir addon → ver ≤12 carpetas de década (hoy tipicamente 2: 80 y 90).
2. Entrar `Años 80` → ver años 1980–1989 presentes.
3. Abrir un año → canción → play.
4. Atrás hasta raíz sin bucles.
5. (Opcional) Con CSV 1960/1970 de prueba: raíz muestra esas décadas; SC-003.

## Criterios de éxito rápidos

| SC | Comprobación |
|----|----------------|
| SC-001 | `decision.md` existe con ≥3 opciones |
| SC-003 | Conteo visual raíz ≤12 |
| SC-004 | Todo año del repo alcanzable |
| SC-005 | Recorrido &lt; 30 s |
