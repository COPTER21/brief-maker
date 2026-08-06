# INDEX — FRD_F-LOCATION-MASTER-001_v2_Pack (FULL)

> v2.0 · Enhancement of v1 (single-entity → full 5-level hierarchy). Source: BRD-F-LOCATION-MASTER-001 v2.0.

| File | Audience | Content |
|---|---|---|
| 00_OVERVIEW.md | all | control, scope, roles, deps, classification, 5 open questions |
| 01_UI.md | FE / html-generator-v3 | 8 pages, dual-view, layouts, journeys, action→API |
| 02_API.md | BE | 18 endpoints (node CRUD ×4 levels + location 6 + geo 3) |
| 03_LOGIC.md | BE | 24 functions + 2 engines + trace |
| 04_DB.md | DBA/BE | 5 owned tables + geo refs + CHECK + indexes + classification |
| 05_RULES.md | BE/QA | 19 rules + state machine + 17 edge + errors + D-CLASS |
| 06_TESTS.md | QA | 27 acceptance + DoD |
| 07_LOCKED_DECISIONS.md | all | 12 LDs (LD-09..12 ใหม่) |

## Function Trace Summary
- **GET** → FN-01/02/03/22/24 (+ENG-HIER-PATH)
- **POST/PUT/PATCH/DELETE** → FN-04/05/06/07/08/09/10/13/14/15/16/17/18/19/20/21/23 (+ENG-LOC-GEN)
- No orphan functions/engines. R8 satisfied (ทุก mutation API trace ≥1 function).

## Cross-refs
UI actions (01) → APIs (02) → Functions/Engines (03) → Tables (04). Rules (05) enforced in FN-04/07/09/10/13/14/17. Tests (06) cover all FR + edge (EC-01..17).

## What changed v1 → v2
| Area | v1 | v2 |
|---|---|---|
| Entities CRUD | locations only | + warehouses/zones/areas/racks (full) |
| Pages | 6 | 8 (+ dual-view) |
| APIs | 8 | 18 (node CRUD ×4 + geo ×3) |
| Functions | 14 | 24 |
| Location types | 9 | 10 (+PACK) |
| Address | free-text | geo cascade (Geo Master) |
| New LDs | — | LD-09..12 |

## Quick Nav
- Flexible parent → 03 FN-13/14, 04 CHECK, 05 BR-001/002
- 5-level CRUD → 02 API-01..05, 03 FN-01..10, 05 BR-003/005
- Geo address → 02 API-20/21/22, 03 FN-24, 04 §4.2 warehouses, 05 BR-008
- PACK / type defaults → 04 type enum, 03 FN-23, 05 BR-004/015 (OQ-3)
- Dual-view / Tree → 01 §1.3/§1.4, 07 LD-10 (OQ-2)
- Bulk-gen → 03 ENG-LOC-GEN, 01 §1.8, 05 BR-011

## Downstream
→ html-generator-25/v3 (01_UI + Layout IDs) · → frd-qa-generator (05_RULES + 06_TESTS + 02_API + 03_LOGIC)
