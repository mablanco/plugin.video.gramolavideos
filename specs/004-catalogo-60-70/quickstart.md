# Quickstart: Validar semilla 60/70

**Feature**: `004-catalogo-60-70`

## Prerrequisitos

- Checkout con CSV nuevos (o en PR)
- `pip install -r requirements-dev.txt`

## Comprobaciones automáticas

```bash
# Años descubiertos (debe incluir <1980 tras semilla)
python -c "from pathlib import Path; print(sorted(p.stem for p in Path('resources/csv').glob('*.csv')))"

python -m pytest -q tests/unit/test_catalog_load.py tests/unit/test_catalog_video_ids.py tests/unit/test_catalog_years.py
```

Ajustar expectativas de `test_catalog_years.py` / wiring si aún asumen 19 años.

## Conteos de aceptación (SC-002)

```bash
python - <<'PY'
from pathlib import Path
rows=years=0
for p in sorted(Path('resources/csv').glob('*.csv')):
    y=p.stem
    if not (y.isdigit() and 1960 <= int(y) <= 1979):
        continue
    n=sum(1 for line in p.read_text(encoding='utf-8').splitlines() if line.strip())
    if n:
        years += 1
        rows += n
        print(y, n)
print('years', years, 'rows', rows)
PY
```

Esperado: `years >= 8`, `rows >= 40`, al menos un año en 1960–69 y uno en 1970–79.

## Smoke reproducción (SC-004)

1. Elegir 5 ids de CSV 60s y 5 de 70s.
2. Reproducir en Kodi (o sondear oEmbed como en tooling existente).
3. Anotar fallos; sustituir ids o listar deuda en el PR.

## Docs

- README describe 60/70 y enlace al proceso ([contracts/seed-process.md](./contracts/seed-process.md)).
- Checklist editorial aplicada ([contracts/editorial-review.md](./contracts/editorial-review.md)).
