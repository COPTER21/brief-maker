# INDEX — FRD F-VENDOR-PRICELIST-001 Vendor Price List

> **Variant:** FULL · **Version:** 1.0 · **Status:** IN-REVIEW

## Pack Contents

| File | Start here when… |
|---|---|
| [00_OVERVIEW.md](00_OVERVIEW.md) | ต้องการรู้ scope, roles, dependencies, manifest |
| [01_UI.md](01_UI.md) | implement routes, drawers, modals, states and UI behavior |
| [02_API.md](02_API.md) | implement HTTP contracts/integrations |
| [03_LOGIC.md](03_LOGIC.md) | implement orchestration/calculation/resolution |
| [04_DB.md](04_DB.md) | create schema, constraints, RLS, WORM controls |
| [05_RULES.md](05_RULES.md) | validate business rules, state, permissions, edge cases |
| [06_TESTS.md](06_TESTS.md) | determine acceptance/DoD/cross-module tests |
| [07_LOCKED_DECISIONS.md](07_LOCKED_DECISIONS.md) | resolve conflicts and prevent design drift |

## Quick Nav

- FE: `01_UI` → relevant API in `02_API` → UI expected tests in `06_TESTS`.
- BE: `02_API` → trace row in `03_LOGIC §3.3` → table in `04_DB` → rules/errors in `05_RULES`.
- QA: `06_TESTS` → edge cases in `05_RULES §5.5` → visible anchors in `01_UI`.
- Architect: Engines in `03_LOGIC §3.2`, ownership in `00_OVERVIEW §0.5`, decisions in `07_LOCKED_DECISIONS`.
- PM/BA: scope/manifest in `00_OVERVIEW`, immutable decisions/drift in `07_LOCKED_DECISIONS`.

## Page → API

| Surface | Main calls |
|---|---|
| P-01 list | API-01, API-02, API-03, API-08 |
| P-02 vendor drill-in | API-01 with vendor filter, API-03 |
| P-03 Batch Entry | API-09, API-10 |
| P-04 Create/Edit/New Version | API-03,04,05,07,16 |
| P-05 View/Approval | API-02,06,08 |
| P-06 Compare | API-13 |
| P-07 Confirm | API-06 or API-08 |
| P-08 Import | API-11,12,17 |

## API → Logic → DB

| API group | Functions / Engines | Reads/Writes |
|---|---|---|
| 01,02,15,16,17 | FN-01,02,14,15,16 | owned tables + ref/config reads |
| 03,04 | FN-03,04,17; ENG-01 | Header/Version/Tier/History |
| 05,06,07 | FN-05,06,07,12; ENG-01 | Version/Header/History + DOA/outbox |
| 08 | FN-13 | Header/History/outbox |
| 09..12 | FN-08..11,04,05; ENG-01 | preview store + owned tables |
| 13,14 | FN-18,19; ENG-02→ENG-01 | candidate read; no price mutation |

## Cross-Module Ownership

```text
F-VENDOR ──active UUID/currency──► Vendor Price List ◄──active+purchasable UUID/UOM── Product Master
                                         │
                 Policy/DOA ◄── approval │ calculation/resolve ──► PR / RFQ / PO
                                         │
F-VENDOR API-20 ◄── read-only summary façade owned by VPL
```

## R8 Verification

- Mutation APIs: 10
- Mutation APIs with Function trace: 10/10
- Functions declared/traced: 19/19
- Engines declared/traced: 2/2
- Hidden HTTP-layer business logic: none specified

## Pack Statistics

| Metric | Count |
|---|---:|
| Routes | 4 (list, vendor drill-in, batch, compare) |
| Overlay surfaces | 4 (form drawer, view drawer, confirm modal, import modal) |
| APIs | 17 |
| Functions | 19 |
| Engines | 2 |
| Owned tables | 4 |
| Business rules | 21 |
| Edge cases | 16 |
| Locked decisions | 12 + 17 imported locks |
| Test cases in FRD inventory | 31 |

## Coverage & Authority

- Coverage Manifest: `00_OVERVIEW §0.12` — Stories 5/5, Rules 21/21, Edges 16/16.
- Scope Lock: `07_LOCKED_DECISIONS §7.0`.
- UI source: `../vendor-price-list-v6.html`.
- BRD source: `../BRD_VendorPriceList_v2.4.md`.
- Vendor source: `../../F-VENDOR/_final-docs`.
- Product source: `../../../Related context/Item Master`.

## Recommended Reading Order

1. `00_OVERVIEW`
2. `07_LOCKED_DECISIONS` (especially LD-02/03/04/05)
3. Role-specific file from Pack Contents
4. `05_RULES`
5. `06_TESTS`
