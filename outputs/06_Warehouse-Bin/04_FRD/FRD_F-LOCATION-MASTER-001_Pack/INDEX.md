# INDEX — FRD F-LOCATION-MASTER-001 Warehouse & Bin

> **Variant:** FULL · **Entry point:** `00_OVERVIEW.md`

## Pack Contents

| # | File | Audience | Core content |
|---|---|---|---|
| 00 | `00_OVERVIEW.md` | all | scope, context, assumptions, coverage manifest |
| 01 | `01_UI.md` | FE/QA | real state routes, overlays, exact microcopy |
| 02 | `02_API.md` | BE/integration | 24 endpoint contracts |
| 03 | `03_LOGIC.md` | BE/architect | 25 functions, 2 engines, R8 trace |
| 04 | `04_DB.md` | DBA/BE | 7 owned tables, constraints, classification |
| 05 | `05_RULES.md` | BE/QA | 17 BRs, state, validation, errors |
| 06 | `06_TESTS.md` | QA | 12 ACs, 21 TCs, 6 cross-module tests |
| 07 | `07_LOCKED_DECISIONS.md` | all | immutable locks, LDs, pending decisions |

## Quick Navigation

- FE: `01_UI.md` → API IDs in §1.8 → schemas in `02_API.md`
- BE: `02_API.md` → R8 in `03_LOGIC.md §3.3` → rules/errors in `05_RULES.md`
- DBA: `04_DB.md`, especially parent XOR, unique indexes, RLS and WORM audit
- QA: `06_TESTS.md` plus edge cases in `05_RULES §5.5`
- PM/BA: open questions and HTML gaps in `00_OVERVIEW §0.8/§0.9`
- Architect: engines in `03_LOGIC §3.2`, tradeoffs in `07_LOCKED_DECISIONS.md`

## Page → API

| Surface | APIs |
|---|---|
| P-01 root/drill | 01, 04, 05..13 |
| P-02 all Locations | 03, 04, 18, 19 |
| P-03 hierarchy | 02, 04 |
| D-01 parent form | 05..12 |
| D-02 Location wizard | 14, 15 |
| D-03 bulk generation | 17 |
| D-04 detail/audit | 04, 21 |
| M-01 status reason | 16, 18 |
| M-02 delete/decommission | 13, 20 |

## Mutation R8 Verification

| API range/action | Function/engine coverage | Result |
|---|---|---:|
| 05/06 Warehouse | FN-04/05/22/23 | ✅ |
| 07/08 Zone | FN-06/07/23 | ✅ |
| 09/10 Area | FN-08/09/23 | ✅ |
| 11/12 Rack | FN-10/11/23 | ✅ |
| 13 parent delete | FN-12/23 | ✅ |
| 14/15 Location create/update | FN-13/14/15/23 | ✅ |
| 16 status | FN-16/17/23 | ✅ |
| 17 generation | FN-14/18/23 + ENG-LOC-GEN | ✅ |
| 18 bulk status | FN-16/19/23 | ✅ |
| 19 bulk UOM | FN-20/23 | ✅ |
| 20 decommission | FN-21/23 | ✅ |
| 24 capacity signal | FN-16/25/23 | ✅ |

No orphan: read FN-01/02/03/22/24 and `ENG-HIER-PATH` are traced by API-01..04/22/23; all mutation functions are listed above.

## API → DB Summary

| APIs | Main reads | Main writes |
|---|---|---|
| 01..04 | hierarchy tables | — |
| 05..13 | hierarchy parents/children, Company ref | corresponding parent + audit |
| 14..16 | Location/parent/type/Inventory guard | Location + audit |
| 17..19 | batch inputs/Locations/Inventory | Rack/Location + audit |
| 20 | Location/Inventory | Location decommission + audit |
| 21..23 | audit/external refs | — |
| 24 | Location | Location derived state + audit |

## Engine ↔ Feature

| Engine | Current use | Status |
|---|---|---|
| `ENG-LOC-GEN` / `location-generation` | atomic template preview/plan | DRAFT; global ID OQ-LOC-07 |
| `ENG-HIER-PATH` / `hierarchy-path-builder` | tree/path/counts, Inventory/report projections | DRAFT; global ID OQ-LOC-07 |

## Pack Statistics

| Metric | Count |
|---|---:|
| page states | 3 |
| drawer/modal states | 6 |
| APIs | 24 |
| functions | 25 |
| engines | 2 |
| owned DB tables | 7 |
| business rules | 17 |
| acceptance criteria | 12 |
| test cases | 21 |
| immutable scope locks | 6 |

## Coverage Pointers

- complete BRD mapping: `00_OVERVIEW §0.12`
- Scope Lock: `07_LOCKED_DECISIONS §7.0`
- Company/Inventory/Geo/Audit/Reporting tests: `06_TESTS §6.9`
- verified prototype behavior gaps: `00_OVERVIEW §0.9`
