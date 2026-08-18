# INDEX — FRD F-SALES-PROMO Promotion

| Audience | Start here | Then |
|---|---|---|
| FE dev | `01_UI.md` | `02_API.md`, Promotion.html |
| BE dev | `02_API.md` | `03_LOGIC.md`, `05_RULES.md` |
| DBA | `04_DB.md` | `05_RULES.md` |
| QA | `06_TESTS.md` | `05_RULES.md`, testcases MD |
| Architect | `03_LOGIC.md` ENG-01 | `07_LOCKED_DECISIONS.md` |
| BA/PM | `00_OVERVIEW.md` | BRD + Feature TLDR |

## File Map

- `00_OVERVIEW.md` — scope, roles, dependencies, locks, coverage manifest
- `01_UI.md` — five AS-BUILT surfaces on `#/promotions`
- `02_API.md` — 15 endpoint contracts and cross-module interfaces
- `03_LOGIC.md` — 12 functions + one engine + trace
- `04_DB.md` — five tables, classification, indexes, retention
- `05_RULES.md` — calculation, authoring, lifecycle, DOA, errors, permissions
- `06_TESTS.md` — 24 acceptance, 6 XT, negative/boundary/lock coverage
- `07_LOCKED_DECISIONS.md` — immutable business and architecture decisions

## Function Trace Quick View

`UI → API-01..15 → FN-01..12 → ENG-01 where evaluation is required`. No orphan mutation or function.

## Final Mechanical Verification

| Check | Result |
|---|:---:|
| FULL expected files present | PASS |
| mutation APIs have logic calls | PASS 14/14 |
| functions have callers | PASS 12/12 |
| UI actions map to APIs | PASS |
| API tables exist | PASS |
| data classification every DB column | PASS |
| Scope Locks imported | PASS 7/7 |
| Cross-module downstream tests | PASS 6/6 |
| HTML route/surface alignment | PASS 1 route / 5 surfaces |
| Coverage Manifest complete | PASS |

Verdict: **PASS — ready for declaration/UI brief/test generation**.
