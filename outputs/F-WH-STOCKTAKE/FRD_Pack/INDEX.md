# INDEX — FRD F084 Stocktake

| File | Audience | Purpose |
|---|---|---|
| 00_OVERVIEW | all | scope, locks, manifest, OQ |
| 01_UI | FE/QA | routes, overlays, states, microcopy |
| 02_API | BE/integration | HTTP and cross-module contracts |
| 03_LOGIC | BE/architect | functions, engines, trace |
| 04_DB | DBA/BE | schema/classification/RLS |
| 05_RULES | BE/QA | declarative rules, permissions, errors |
| 06_TESTS | QA | acceptance, data, XT |
| 07_LOCKED_DECISIONS | all | immutable decisions |

## Cross-reference

| Page | API |
|---|---|
| P-01 | API-01/02 |
| P-02 | API-03/04/05 |
| P-03 | API-06/07/08/09 |
| P-04 | API-10 |

| Mutation API | Function/Engine | DB writes |
|---|---|---|
| API-02 | FN-02 | round,event |
| API-03 | FN-03/04 | lock,snapshot,event,round |
| API-04 | FN-05 | sheet,event,round |
| API-05 | FN-06/07, ENG-01 | line,sheet,event,round |
| API-07 | FN-09, ENG-01 | approval,event,round |
| API-08 | FN-10 | approval,event,round,lock |
| API-09 | FN-11, ENG-02 | handoff,event,round,lock |

## Pack Statistics

Pages/routes 5 · overlays 5 · APIs 10 · functions 12 · engines 2 · tables 8 · rules 10 · acceptance 20 · cross-module tests 5 · locks 5

## Phase 3.5 Verification

- A completeness 9/9 files ✅
- B/C API↔Logic mutation 7/7; no orphan ✅
- D API↔DB linkage complete ✅
- E UI↔API actions complete ✅
- F/G engine purity and placement complete ✅
- H security triggers applied ✅
- I naming conventions complete ✅
- J classification/PII columns complete ✅
- K manifest stories 8/8, rules 10/10, edges 10/10 ✅
- L scope/value-stream contracts complete ✅
- M routes 5/5, patterns 5/5, microcopy sample 10/10 match HTML ✅

Verdict: **PASS**
