# INDEX — FRD F-WH-PACK Packing

## Pack Contents

| File | Primary reader | Purpose |
|---|---|---|
| 00_OVERVIEW | all | scope/dependency/coverage |
| 01_UI | FE/QA | screen behavior and UI/API anchors |
| 02_API | BE/FE | HTTP contracts |
| 03_LOGIC | BE/Architect | functions/engines/transactions |
| 04_DB | DBA/BE | schema/RLS/integrity |
| 05_RULES | BE/QA | authoritative rules/errors/security |
| 06_TESTS | QA | acceptance/DoD/cross-module tests |
| 07_LOCKED_DECISIONS | all | immutable decisions and OQ guards |

## Statistics

| Item | Count |
|---|---:|
| UI pages/tabs/overlays | 4 pages + 3 overlays |
| APIs | 17 + Picking internal intake port |
| Functions | 14 |
| Engines | 2 DRAFT |
| Tables | 7 |
| Business rules | 16 |
| Acceptance cases | 20 |
| Cross-module cases | 5 |

## Critical Reading Paths

- FE: `01_UI` → `02_API` read models/errors → HTML source → UI brief
- BE: `02_API` → `03_LOGIC` trace → `05_RULES` → `04_DB`
- QA: `06_TESTS` → `05_RULES` → `01_UI` visible anchors
- Architect: `07_LOCKED_DECISIONS` → engines → DN/Transfer OQs

## R8 Verification

Every API-05..15 and API-17 mutation has a function in `03_LOGIC §3.3`; both engines are called; all functions appear in trace/read/intake paths. No HTTP business logic is authoritative outside the logic/rules files.

## Source Precedence

Locked decisions > Picking final cross-feature contract > Central Plan global flow > PREBRIEF business intent > approved HTML behavior > checklist inventory. UX waiver does not override central CI/quality requirements for production implementation.
