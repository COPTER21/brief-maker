# INDEX — FRD F-PRODUCT-MASTER-001 Product Master (v2.0 · FULL)

> Entry point ทุก role · **Reverse Mode:** HTML `product-master.html` v6 = Source of Truth (ไม่มี BRD)

---

## 📂 Pack Contents

| # | File | Audience | เนื้อหา |
|---|---|---|---|
| 00 | OVERVIEW.md | All | Scope (no-approval) · Deps · OQ-01..07 · Coverage Manifest H-01..14 |
| 01 | UI.md | FE | Layout Decision Log (observed) · P-01..P-06 · routing/Esc/context |
| 02 | API.md | BE (HTTP) | API-01..07 · Cross-Module `PRODUCT_STOCK_THRESHOLD v1` |
| 03 | LOGIC.md | BE (logic) | FN-01..12 · no owned engine (ENG-STOCK-ALERT = downstream) · R8 trace |
| 04 | DB.md | DBA/BE | T_product + 4 children · Classification (Confidential = pricing) · migration v3.5→2.0 |
| 05 | RULES.md | BE+QA | BR-PDM-01..10 · state machine 5 · EC-01..08 · error catalog · D-CLASS |
| 06 | TESTS.md | QA | AC-01..20 · XT-01..03 · microcopy verbatim |
| 07 | LOCKED_DECISIONS.md | All | Scope Lock N/A · LD-01..06 · CD-01..02 |

---

## 🔍 Quick Nav

- **FE เริ่มที่:** 01_UI (route + pattern ต่อหน้า → action ชี้ API ID) · microcopy 06 §6.10
- **BE endpoint:** 02_API §2.2 → 03_LOGIC §3.3 (FN ที่ต้องเรียก) → 04_DB → 05_RULES
- **DBA:** 04_DB §4.2 (CHECK VR-MM, indexes, RLS) + §4.4 migration (pending→draft, drop 4CODE)
- **QA:** 06_TESTS + 05 §5.5 · baseline = Playwright 46/46 บน prototype
- **PM/Strike:** 00 §0.8 OQ (DOA phase, lot/serial UI, regulated) · 07 LD-01
- **Architect:** 02 §2.X + 07 LD-03 — register `ENG-STOCK-ALERT` (owner Inventory Monitoring)

---

## 🔗 Cross-Reference

### Page → API
| Page | APIs |
|---|---|
| P-01 list | API-01, API-02 (row click) |
| P-02/03 wizard | API-03 (create±activate), API-04 (amend), API-06 GET /uoms |
| P-04 view | API-02, API-05 (เปิดใช้งาน), API-06 (transitions) |
| P-05 modals | API-06 |
| P-06 bulk | API-07 |

### API → Function (R8)
API-01→FN-01 · API-03→FN-02(+09,10,07,08,06) · API-04→FN-03(+07,08,06) · API-05→FN-04(→06,07) · API-06→FN-05(+06) · API-07→FN-12(→11,02,09)

### Rule → Test
BR-PDM-01→AC-03/16 · 02→AC-07 · 03→AC-08 · 04→AC-09 · 05→AC-05/13 · 06→AC-10+XT-01 · 07→AC-06 · 08→AC-15+XT-03 · 10→AC-11 · §5.2→AC-12..15

### สิ่งที่ถูกถอดจาก v3.5 (อ่านก่อน review)
- ชั้นอนุมัติ/DOA ทั้งหมด (LD-01) — placeholder fields คงไว้ (LD-02)
- ENH-4CODE (LD-04)
- เพิ่มใหม่: ENH-MINMAX (BR-PDM-06) · state transitions ครบ (§5.2) · bulk import (API-07)

**Chain ถัดไป (SOW3.5):** ai-testcase-md-generator + qa-friendly-html-generator → "Product Master HTML Testcase.html" → uba-taxonomy-register / output-checker / dev-brief-generator
