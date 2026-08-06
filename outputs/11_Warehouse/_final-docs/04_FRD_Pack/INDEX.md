# INDEX — FRD F-LOCATION-MASTER-001 · Warehouse & Bin (คลังและตำแหน่ง)

> FULL Pack (9 files + INDEX) · WF-01 SOW3.3 · `frd-generator-v6` v6.1 HTML-first · v1.0 · 2026-08-07

## Files
| File | Audience | Contents |
|---|---|---|
| 00_OVERVIEW.md | all | Doc control, variant, scope, roles, deps, Scope Lock, Coverage Manifest, Open Questions, probe log |
| 01_UI.md | FE | §1.0 Layout Decision Log (observed), 8 pages/views, components, RBAC UI, journey |
| 02_API.md | BE | 18 endpoints (HTTP layer) + §2.9 Cross-Module Contract |
| 03_LOGIC.md | BE | 18 Functions + 2 Engines + §3.3 API↔Logic trace |
| 04_DB.md | DBA | 7 owned tables + 2 external, indexes/constraints, classification |
| 05_RULES.md | BE/QA | BR-001..018, status machine, 18 edge cases, error catalog, D-CLASS |
| 06_TESTS.md | QA | AT-01..10, edge, permission, status, XT cross-module, DoD |
| 07_LOCKED_DECISIONS.md | all | Scope Lock §7.0 + LD-01..13 + convention deviations |

## Quick Nav
- **Pages ↔ APIs:** P-01→API-01/02, P-03→API-03/04, P-04→API-08/09, P-05→API-13/14, P-06→API-06, P-07→API-10/11/12, P-08→API-05/11/12.
- **Function Trace:** see 03_LOGIC §3.3 (every mutation API → Function/Engine, R8 verified).
- **Engines:** ENG-HIER-PATH (full-path builder, reusable/CUBIC candidate), ENG-BULK-PLAN (bulk template expansion + collision).

## Counts
- Pages/views: **8** · API endpoints: **18** · Functions: **18** (17 active + 1 deferred WHB-FN-18) · Engines: **2** · Business rules: **18** (BR-001..018) · Edge cases: **18** (EC-01..13 ☑ + EC-14..18 ☐) · Errors: **17** · LDs: **13** (+ 7 Scope Lock) · Stories covered: **10** (S-01..10) · Cross-module tests: **4** (XT-01..04).

## Chain
Upstream: BRD_Warehouse_Bin.md (APPROVED) + WarehouseBin.html. Downstream: html-ui-brief (05_UI_BRIEF) → ai-testcase-md-generator + qa-friendly-html-generator (06/07).

## Traceability (3-way)
BRD §7 story ↔ 00_OVERVIEW §0.12 Coverage Manifest ↔ 06_TESTS AT. BRD §9 rule ↔ 05_RULES §5.1 ↔ 02_API errors ↔ 03_LOGIC FN. HTML view/fn ↔ 01_UI §1.0 (evidence: selector·fn·line).
