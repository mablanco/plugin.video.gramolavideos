# Validation log (T054 / quickstart)

**Date**: 2026-07-25 (smoke Kodi M1–M3: 2026-07-28)  
**Branch**: `001-auditoria-polish`  
**Runtime smoke**: Kodi 20.5 Nexus (KDE neon), `plugin.video.youtube` 7.4.x + `inputstream.adaptive` (paquete Debian)

| Check | Result |
|-------|--------|
| `.venv/bin/python -m pytest -q` | Ver green en PR (stubs, sin Kodi) |
| `gh repo view --json defaultBranchRef` | `main` |
| `rg commits/master README.md changelog.txt` | sin matches |
| Smoke Kodi M1–M3 / YouTube real | **PASS** (T027/T035). M1 play OK tras actualizar YouTube (6.8.x daba HTTP 400 + segfault). M2 Back/historial OK. M3 aviso + listado residual OK. Nota: algunos vídeos exigen login en el addon YouTube (p. ej. 1984 *La Unión - Eclipse total*); es restricción del lado YouTube, no de Gramola. |

Primary gate: terminal pytest + governance checks above.
