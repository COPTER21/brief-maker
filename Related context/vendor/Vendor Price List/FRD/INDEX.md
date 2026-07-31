# INDEX — F-VENDOR-PRICELIST-001 Vendor Price List (FRD Pack v5.1 FULL)

## Files
| File | Audience | Content |
|---|---|---|
| 00_OVERVIEW.md | All | Control, Scope, Roles, Engines summary, Open Questions, Data Classification summary |
| 01_UI.md | FE | 9 pages + Layout Template IDs + UI→API map |
| 02_API.md | BE | 13 endpoints (HTTP) + Calls(Logic) |
| 03_LOGIC.md | BE | 12 Functions + 4 Engines + Trace Table (R8) |
| 04_DB.md | DBA/BE | 3 tables + classification + indexes |
| 05_RULES.md | BE/QA | R01–R18 + VR01–11 + E01–16 + §5.7 D-CLASS |
| 06_TESTS.md | QA | TC-01–24 + ENG-T1–6 + DoD |
| 07_LOCKED_DECISIONS.md | All | LD-01–09 + deviations + ID registry |

## Quick Nav by Question
- "ราคาคำนวณยังไง" → 03_LOGIC ENG-VPL-02 landed-price · R09
- "get-price ทำงานยังไง (PR/PO ดึง)" → 03_LOGIC ENG-VPL-01 · 02_API API-13
- "approval/SoD" → 03_LOGIC FN-08 · 02_API API-10 · R12
- "DOA threshold" → ENG-VPL-04 (placeholder) · LD-04 · OQ1/OQ6
- "ราคา mask/Confidential" → 03_LOGIC FN-12 · 04_DB §4.6 · 05_RULES §5.7
- "compare ข้ามคู่ค้า" → API-12 · ENG-VPL-01/-02/-03
- "schema/classification" → 04_DB

## Function Trace (R8 summary)
- Mutation APIs 05–11 → ทุกตัวมี Function (FN-01,02,05,06,07,08,09) ✅
- Engines ENG-01..04 ถูกเรียกผ่าน Function/API ✅ · ไม่มี orphan ✅

## Downstream Chain
- 🎨 html-generator-v3 ← 01_UI.md (มี HTML prototype แล้ว: `vendor-pricelist.html`)
- 📋 frd-qa-generator-v2 ← 02_API + 03_LOGIC + 05_RULES + 06_TESTS (→ SCN/TC/DATA/CSV)
- 📦 Dev handover: 02_API→BE(HTTP), 03_LOGIC→BE(logic), 04_DB→DBA, 05_RULES→BE+QA, 06_TESTS→QA
- 🔗 Governance (Phase 2): DOA pairing + Data Classification/Restricted ที่ Policy Center (OQ4/OQ6)
