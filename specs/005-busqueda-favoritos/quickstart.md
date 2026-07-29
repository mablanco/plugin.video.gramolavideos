# Quickstart: Validar veredicto 005

**Feature**: `005-busqueda-favoritos`

## Objetivo

Comprobar en &lt;10 minutos (SC-003) que el empaquetado está decidido y es accionable.

## Pasos

1. Abrir [decision.md](./decision.md).
2. Verificar respuesta inequívoca: **dos features**.
3. Verificar orden: **favoritos → búsqueda**.
4. Abrir [research.md](./research.md): perfiles separados + tabla P1–P5.
5. Abrir [contracts/packaging-verdict.md](./contracts/packaging-verdict.md):
   `implements_runtime_in_005: false`.
6. Confirmar que no hay cambios de código exigidos por este quickstart.

## Resultado esperado

| Check | OK si |
|-------|-------|
| SC-001 | Una frase de veredicto clara |
| SC-002 | Ambas capacidades descritas + criterios |
| SC-004 | Entrega parcial posible (features o MVP partido) |
| SC-005 | Catálogo ≠ favoritos; YouTube intacto |

## Siguiente acción

`/speckit-specify` de favoritos cuando se priorice implementación (no
re-planificar búsqueda+favoritos como un solo bloque).
