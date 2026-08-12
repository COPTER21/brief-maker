# UAT Lite Audit — F-BOM-001

- Source MD: 44 cases / 98 steps
- Kept in UAT: 23 cases; source 59 steps → rendered 47 human-readable steps
- Dropped: 21 cases / 39 steps
- Mode: Lite-first; retained TC IDs exactly

## Drop ledger

- `TC-A01`, `TC-A02`, `TC-A03` — provisional boundary/master policies require controlled backend/master seed; ordinary user cannot reliably trigger them.
- `TC-B01` — selection/cancel permutation is already exercised inside `TC-S03`, `TC-B02`, `TC-B03`.
- `TC-D02` — immutable MO snapshot needs downstream module and baseline comparison; kept in AI suite.
- `TC-P01`, `TC-P02`, `TC-P03`, `TC-P04` — role injection, cost masking, denied mutation and cross-tenant isolation require real authorization environment; prototype has one fixed Planner identity.
- `TC-R01`..`TC-R06` — concurrency, idempotency, missing ID design, dependency outage and audit rollback require technical injection.
- `TC-V07`, `TC-V08` — UI deliberately prevents choosing forged FG/UoM; server-negative tests remain in AI suite.
- `TC-X01`..`TC-X04` — Production/MO and Costing screens/services are declared-unbuilt and require simulation.

## Merge notes

- 12 atomic navigation/typing/verification rows were merged into adjacent human actions: 59 source steps → 47 rendered steps.
- No validation message, acceptance outcome, destructive confirmation, status transition, or Scope Lock assertion was removed from retained cases.
- Prototype-specific record counts were replaced by “เท่ากับข้อมูลจริง” phrasing; master-derived UoM/cost expectations refer to their source rather than fixed mock values.

