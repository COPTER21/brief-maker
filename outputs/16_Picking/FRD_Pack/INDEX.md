# INDEX — FRD F-WH-PICK Picking

## Pack contents

| File | Audience | Purpose |
|---|---|---|
| 00_OVERVIEW | all | scope, roles, manifest, OQs |
| 01_UI | FE | routes/pages/components/microcopy |
| 02_API | BE | HTTP and cross-module contracts |
| 03_LOGIC | BE/Architect | functions, allocation engine, transactions |
| 04_DB | BE/DBA | tables, classification, indexes/RLS |
| 05_RULES | BE/QA | rules, states, permissions, errors |
| 06_TESTS | QA | acceptance, negative and cross-module tests |
| 07_LOCKED_DECISIONS | all | immutable scope and decisions |

## Quick trace

| UI | APIs | Logic |
|---|---|---|
| P-01 queue/list | 01,02 | FN-01,02 |
| P-02 create | 03,04,08,09 | FN-03..05,09,10, ENG-01 |
| P-03 operate | 05..16 | FN-06..17, ENG-01 |

## API → DB

- API-01/02/16 read Pick plus upstream contract/snapshot
- API-03..15 write `T_pick_header`, `T_pick_line`, `T_pick_audit`; cross-module writes use service contracts/outbox

## R8 verification

16 APIs, 17 functions, 1 engine; every mutation has ≥1 function, every function/engine is traced, no business calculation lives in API.

## Pack statistics

3 routes, 16 endpoints, 17 functions, 1 engine candidate, 3 owned tables, 17 business rules, 12 edge cases, 12 immutable locks.

## Recommended reading

All: 00 → this INDEX. FE: 01. BE: 02→03→05→04. QA: 06 + 05. Architect: 03 + 07.
