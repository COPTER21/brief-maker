# INDEX — FRD F-HR-EXPENSE · Expense Claim (เบิกค่าใช้จ่าย)

> **Variant:** FULL (9 files + INDEX) · **Archetype:** Q-document (Pattern Q)
> **Source of truth:** expense.html (7 จอ · list + wizard 5 steps + view 4 tabs + 3 modal) — FRD 1:1 กับจอ (R14 HTML Fidelity)

---

## 📂 Pack Contents

| # | File | Audience | Content |
|---|---|---|---|
| 00 | OVERVIEW.md | All | Meta + Scope + Roles + Dependencies + OQ + **Coverage Manifest §0.12** |
| 01 | UI.md | FE dev | **Layout Decision Log §1.0** + 7 Pages + Journey + NTF |
| 02 | API.md | BE dev (HTTP) | 19 API contracts + Cross-Module §2.X |
| 03 | LOGIC.md | BE dev (logic) | 23 Functions + 2 Engines + Trace §3.3 |
| 04 | DB.md | DBA / BE | 4 Tables + Classification §4.6 |
| 05 | RULES.md | BE + QA | 16 BR + State Machines (8 state) + Edge (EC-01..08) + Errors + Security |
| 06 | TESTS.md | QA | 18 AC + 22 TC + DoD + XT cross-module |
| 07 | LOCKED_DECISIONS.md | All | Scope Lock §7.0 (LOCK-01..10) + LD-01..06 |

---

## 🔍 Quick Nav by Question
- **FE dev เริ่มไหน?** → 01_UI (§1.0 Decision Log + §1.2 per-page action → API)
- **BE dev endpoint ใหม่?** → 02_API §2.2 → 03_LOGIC §3.3 → 04_DB → 05_RULES
- **DBA?** → 04_DB (§4.2 schema + §4.6 classification)
- **QA?** → 06_TESTS §6.1 AC + 05_RULES §5.5 Edge
- **PM/SEC risk/OQ?** → 00_OVERVIEW §0.8 (OQ-01..06 + OQ-EXP-04) + 07_LOCKED §7.5
- **Architect engines?** → 03_LOGIC §3.2 (ENG-EXP-01/02 DRAFT) + 07_LD-02

---

## 🔗 Cross-Reference Tables

### Page → API
| Page | Action | Calls |
|---|---|---|
| P-01 รายการใบเบิก | คลิกแถว / filter / สร้าง | API-03 / API-01 / API-02 |
| P-02 wizard (5 ขั้น) | เลือกผู้เบิก / เพิ่มรายการ / ส่งอนุมัติ | API-14+15 / API-02 / API-05 |
| P-03 view (detail) | เลือกจ่าย / สถานะจ่าย / หักลบทดรอง | API-10 / API-11 / API-16 |
| P-03 (footer) | อนุมัติ / ไม่อนุมัติ / ยกเลิก / ยื่นใหม่ | API-06 / API-07 / API-08 / API-09 |
| P-04 DOA slot picker | ส่งอนุมัติ (resolve) | API-05 / API-12 |
| P-07 PDF | พิมพ์/ดาวน์โหลด | API-20 |

### API → Logic (R8)
ดู 03_LOGIC §3.3 (ครบทุก mutation → ≥1 Function; FN-21 audit ทุกตัว)

### API → DB
| API | Reads | Writes |
|---|---|---|
| API-02 | HR Config, Movement, Employee | T_expense_claim, T_expense_line, audit |
| API-05 | (DOA resolve) | T_expense_approval_step, claim, audit |
| API-06 | T_expense_approval_step | approval_step, claim(doc_no), audit + (7C/PDF ext) |
| API-07 | T_expense_claim | claim(rejected), audit |
| API-08 | T_expense_claim | claim(cancelled), audit |
| API-10 | T_expense_claim, F103 | claim(pay,sent_to_pay,advance_offset), audit |
| API-01/03 | claim, lines, steps, audit | — (scope + mask) |

### Engine ↔ Feature
| Engine | Used by | Status |
|---|---|---|
| ENG-EXP-01 expense-vat-calculator | F-HR-EXPENSE (list/wizard/view/PDF) · เอกสาร line VAT (planned) | DRAFT |
| ENG-EXP-02 advance-offset-calculator | F-HR-EXPENSE (FN-18) · F103 reconcile (planned) | DRAFT |
| (ext) DOA / ENG-NOTIFY / ENG-DOC-NUM/STORE / F103 / F117 / F102 | F-DLG-001 / F-NOTIFY / DOCCFG / F103 / F117(W7) / F102 | EXTERNAL |

---

## 🚨 R8 Verification Matrix

**Rule:** ทุก mutation API มี ≥1 Function/Engine

| API (mutation) | Functions | Engines | ✅ |
|---|---|---|---|
| API-02 create | FN-01/15/13 + FN-21 | ENG-EXP-01 | ✅ |
| API-04 update | FN-02/13 + FN-21 | ENG-EXP-01 | ✅ |
| API-05 submit | FN-05/06/13/14 + FN-21 | 0 | ✅ |
| API-06 approve | FN-07/11/22/23 + FN-21 | 0 | ✅ |
| API-07 reject | FN-08 + FN-21 | 0 | ✅ |
| API-08 cancel | FN-09 + FN-21 | 0 | ✅ |
| API-09 reopen | FN-10 + FN-21 | 0 | ✅ |
| API-10 pay-channel | FN-12/16 + FN-21 | ENG-EXP-02 | ✅ |

**No orphan Function/Engine:** FN-01..23 + ENG-EXP-01/02 traced ใน 03_LOGIC §3.3 ✅

---

## 📊 Pack Statistics
| Metric | Count |
|---|---|
| Pages (จอ) | 7 (list + wizard 5-step + view 4-tab + 3 modal + PDF) |
| Routes | 1 feature menu (#/expense · overlay = drawer/modal) |
| APIs | 19 (8 mutation + read/ref/hook · DOA/Movement/HRConfig/F103/F117/F102) |
| Functions | 23 (FN-01..23) |
| Engines | 2 (DRAFT) + 5 external |
| DB Tables | 4 (claim/line/approval_step/audit) |
| Business Rules | 16 (BR-01..15 + BR-18) |
| Edge Cases | 8 (EC-01..08 · Phase 2.5) |
| Error codes | 19 |
| FN coverage | **25/25** (FN-01..17 + FN-90..94 + **FN-18/19/20**) |
| Locked Decisions | 6 (LD-01..06) + Scope Lock LOCK-01..10 |
| Open Questions | 6 (OQ-01..06) + OQ-EXP-04 + OQ-UX |
| Lifecycle states | 8 (draft/pending_approval/approved/sent_to_pay/paid/closed/rejected/cancelled) |

---

## 🎯 Reading Order
1. 00_OVERVIEW (scope + coverage) → 2. INDEX (this) → 3. 01_UI (FE) / 02_API+03_LOGIC (BE) / 04_DB (DBA) → 4. 05_RULES → 5. 06_TESTS

## Coverage Manifest Pointer
- ทุก BRD requirement + 25 FN → ที่อยู่ใน pack: **00_OVERVIEW §0.12** · Scope Lock: **07_LOCKED §7.0**
