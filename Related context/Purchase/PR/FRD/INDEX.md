# INDEX — FRD F-PR-001 ใบขอซื้อ (Purchase Requisition)

> **Variant:** FULL · **Audience:** All roles (entry point)
> **Purpose:** Cross-reference + Function Trace + Quick Nav

---

## 📂 Pack Contents

| # | File | Audience | Size hint |
|---|---|---|---|
| 00 | OVERVIEW.md | All | Meta + Scope + Roles + Open Questions |
| 01 | UI.md | FE dev | 3 pages (List / Create drawer / View drawer-tabbed) |
| 02 | API.md | BE dev (HTTP) | 10 API contracts |
| 03 | LOGIC.md | BE dev (logic) | 10 Functions + 3 Engines + Trace |
| 04 | DB.md | DBA / BE | 3 tables + Data Classification |
| 05 | RULES.md | BE + QA | 14 BR + State Machine + 9 Edge Cases + Errors |
| 06 | TESTS.md | QA | 17 AC + 20 TC + DoD |
| 07 | LOCKED_DECISIONS.md | All | 6 LD + Convention deviations |

---

## 🔍 Quick Nav by Question

- **FE dev เริ่มที่ไหน?** → 01_UI §1.2 (per-page actions → API ID) + 02_API response schemas
- **BE dev สร้าง endpoint?** → 02_API §2.2 (contract) → 03_LOGIC §3.3 (Functions/Engines) → 04_DB (tables) → 05_RULES (BR/validation)
- **DBA?** → 04_DB §4.2 (schema + RLS + indexes) + §4.6 (classification)
- **QA?** → 06_TESTS §6.1 (AC) + 05_RULES §5.5 (edge) + §6.4 (DoD)
- **PM (risk/open)?** → 00_OVERVIEW §0.8 (OQ-01..05)
- **Architect (engines)?** → 03_LOGIC §3.2 (ENG-DOC-AMT DRAFT) + 07_LD-05

---

## 🔗 Cross-Reference: Page → API

| Page | Actions | Calls |
|---|---|---|
| P-01 List | row click / ดู | F-PR-API-03 |
| P-01 List | filter/search | F-PR-API-01 |
| P-02 Create | บันทึกร่าง | F-PR-API-02 / F-PR-API-04 |
| P-02 Create | ส่งอนุมัติ | F-PR-API-05 |
| P-03 View | อนุมัติ | F-PR-API-06 |
| P-03 View | ตีกลับ | F-PR-API-07 |
| P-03 View | ยกเลิก | F-PR-API-08 |
| P-03 View | เลือกเส้นทาง | F-PR-API-09 |
| P-03 View | PDF | F-PR-API-10 |

---

## 🔗 Cross-Reference: API → Function/Engine (R8)

| API | Functions | Engines |
|---|---|---|
| API-01 GET list | FN-04 | — |
| API-02 POST create | FN-01, FN-03 | ENG-DOC-AMT |
| API-03 GET detail | FN-04 | — |
| API-04 PUT update | FN-02, FN-03 | ENG-DOC-AMT |
| API-05 POST submit | FN-06, FN-03 | ENG-BUDGET, ENG-DOA |
| API-06 POST approve | FN-07 | ENG-BUDGET |
| API-07 POST reject | FN-08 | — |
| API-08 POST cancel | FN-09 | ENG-BUDGET |
| API-09 POST route | FN-10 | — |
| API-10 GET pdf | FN-11 | — |

---

## 🔗 Cross-Reference: Function → Table

| Function | Writes/Reads |
|---|---|
| FN-01 create | INSERT T_pr_header, T_pr_line |
| FN-02 update | UPDATE T_pr_header, replace T_pr_line |
| FN-04 list/hydrate | READ T_pr_header (+join branch/budget/line) |
| FN-06 submit | UPDATE status/chain; READ budget |
| FN-07 approve | UPDATE chain/status; commit budget |
| FN-09 cancel | UPDATE status; reverse budget |
| FN-11 pdf | READ header+line+branch+org |

---

## 🔗 Engines Summary

| Engine | Status | Owner | Used by |
|---|---|---|---|
| `doc-amount-engine` (ENG-DOC-AMT) | DRAFT (register at hand-off) | shared | F-PR-001 + F-PO/CP/QT planned |
| `doa-resolver` (ENG-DOA) | EXISTING | DOA module (F-PC-DOA-01) | ทุก approval feature |
| `budget-availability-engine` (ENG-BUDGET) | EXISTING | Budget module (F-BGT-REQ-001) | F-BGT, F-PR, F-PO |

---

## ⚠️ Open Questions (blocking marked)

| OQ | Question | Blocking | Owner |
|---|---|:---:|---|
| OQ-01 | Atomic budget commit strategy (EC-05) | YES | Bird/Strike |
| OQ-02 | event `pr_linked` ↔ budget 3-stage contract | YES | ทีม Budget |
| OQ-03 | DOA chain by_department vs by_amount | NO | Admin (Phase 3) |
| OQ-04 | VAT-included rounding (ROUND_HALF_UP?) | NO | Finance |
| OQ-05 | Restricted fields wire Restricted Resources | NO | Policy Center |

---

## 📦 Dev Handover Map
- 01_UI → FE · 02_API → BE (HTTP) · 03_LOGIC → BE (logic) · 04_DB → DBA · 05_RULES → BE+QA · 06_TESTS → QA · 07_LD → all
- **Parallel:** html-generator-v3 (อ่าน 01_UI) · frd-qa-generator (อ่าน 02/03/05/06)
