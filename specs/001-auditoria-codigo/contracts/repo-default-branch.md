# Contract: Gobernanza del repositorio (`main`)

**Feature**: `001-auditoria-codigo`

## Default branch

| Antes | Después |
|-------|---------|
| `master` (canónica) | `main` (canónica) |

## Requisitos comprobables

1. En el remoto `mablanco/plugin.video.gramolavideos`, la default branch es `main` (FR-018).
2. README / changelog / docs del repo no presentan `master` como rama canónica (FR-019, SC-008).
3. Si `master` existe aún, no es default y está documentado como legacy o se retira (FR-020).

## Fuera de contrato

- Actualizar forks de terceros (aviso puntual, no bloqueante).
