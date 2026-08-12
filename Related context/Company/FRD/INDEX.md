# INDEX — FRD_F-ORG-001_Pack (FULL)

## Files
| File | Audience | เนื้อหา |
|---|---|---|
| 00_OVERVIEW.md | All | Control + Scope + Roles + Dependencies + Data Classification summary + Open Questions |
| 01_UI.md | FE | 9 screens + components + Layout Template IDs + UI→API |
| 02_API.md | BE (HTTP) | 14 APIs + contracts + Calls(Logic) |
| 03_LOGIC.md | BE (logic) | 14 Functions + 3 Engines + Trace Table (R8) |
| 04_DB.md | DBA/BE | 5 tables + Data Classification 4-level (§4.6) |
| 05_RULES.md | BE/QA | 13 BR + validation + 10 edge + error catalog + §5.7 D-CLASS |
| 06_TESTS.md | QA | 15 acceptance + DoD |
| 07_LOCKED_DECISIONS.md | All | 8 LD + layout reference |

## Function Trace (Quick — เต็มใน 03_LOGIC §3.3)
mutation APIs: API-03(create)→FN-01/05/06/07 · API-04(update)→FN-02/05/07 · API-05(status)→FN-03 · API-06(delete)→FN-04+ENG-03 · API-08(import)→FN-11+ENG-02+FN-07 · API-09(chart)→ENG-01 · API-13(logo)→FN-13 · API-14(del logo)→FN-14. **No orphan, all mutation traced (R8 ✅)**

## Engines (CUBIC candidates)
F-ORG-ENG-01 org-tree-builder · F-ORG-ENG-02 csv-import-validator · F-ORG-ENG-03 cascade-resolver (register ตอน CUBIC Registry)

## Cross-refs verified (Phase 3.5)
UI→API ✅ · API→Function/Engine ✅ · API→DB ✅ · no orphan ✅ · Data Classification ทุก column ✅ · Security P3 ✅

## Next Chain
🎨 html-generator-v3 (อ่าน 01_UI — prototype มีแล้ว) · 📋 frd-qa-generator-v2 (อ่าน 02/03/05/06) · 📦 Dev handover per file
