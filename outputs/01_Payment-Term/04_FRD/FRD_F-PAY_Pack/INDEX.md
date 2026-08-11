# INDEX — FRD F-PAY Payment Term (เงื่อนไขการชำระเงิน)

> **Variant:** FULL (9 files + INDEX) · **Audience:** All roles (entry point)
> **Purpose:** Cross-reference + Function Trace + Quick Nav
> **Source of Truth:** HTML `01_HTML/f-payterm.html` (gate-passed) · BRD APPROVED · Conflict Priority: LOCK > BRD > HTML

---

## 📂 Pack Contents

| # | File | Audience | Content |
|---|---|---|---|
| 00 | OVERVIEW.md | All | Meta + Scope + Roles + Dependencies + OQ + **Coverage Manifest §0.12** |
| 01 | UI.md | FE dev | **Layout Decision Log §1.0** + Pages P-01..05 + Journey |
| 02 | API.md | BE (HTTP) | 8 APIs + **Cross-Module Contract §2.X** |
| 03 | LOGIC.md | BE (logic) | 11 Functions + **ENG-PT-01/02** + Trace §3.3 |
| 04 | DB.md | DBA / BE | 2 Tables + Data Classification (Internal) |
| 05 | RULES.md | BE + QA | BR-01..13 + 7 validations + Edge Cases + Errors + Security |
| 06 | TESTS.md | QA | AT-01..19 + DoD + Cross-Module + Microcopy verbatim |
| 07 | LOCKED_DECISIONS.md | All | **Scope Lock §7.0** + LD-F-01..06 |
| — | INDEX.md | All | This file |

---

## 🔍 Quick Nav by Question

- **FE dev เริ่มที่ไหน?** → 01_UI §1.0 (Layout Decision Log) → §1.2 (page actions + API)
- **BE dev สร้าง endpoint?** → 02_API §2.2 → 03_LOGIC §3.3 (Functions/Engines) → 04_DB → 05_RULES
- **DBA?** → 04_DB (2 tables + RLS + partial-unique default index)
- **QA?** → 06_TESTS §6.1 (AT) + 05_RULES §5.5 (Edges) + §6.10 (microcopy verbatim)
- **PM — OQ/risk?** → 00_OVERVIEW §0.8 (OQ-PAY-01..07, ENG-REG, blocking flags)
- **Architect — CUBIC engines?** → 03_LOGIC §3.2 (ENG-PT-01/02 DRAFT) + 07 LD-F-03

---

## 🔗 Cross-Reference Tables

### Page → API (from 01_UI §1.2)
| Page | Actions | Calls |
|---|---|---|
| P-01 List | row click / filter / stat / bulk-status | API-03 / API-01 / API-01 / API-06 |
| P-02 Create | save | API-02 |
| P-03 Edit | save | API-04 |
| P-04 View | change status | API-05 |
| P-05 Bulk delete | confirm | API-07 |
| (downstream) | picker | API-08 |

### API → Logic (from 03_LOGIC §3.3)
| API | Functions | Engines |
|---|---|---|
| API-01 GET /payment-terms | FN-04, FN-10 | — |
| API-02 POST /payment-terms | FN-01, FN-03, FN-08, FN-09 | ENG-PT-01* |
| API-03 GET /:id | FN-10 | — |
| API-04 PUT /:id | FN-02, FN-03, FN-08, FN-09 | ENG-PT-01* |
| API-05 PATCH /:id/status | FN-05 | — |
| API-06 POST /bulk-status | FN-06 | — |
| API-07 POST /bulk-delete | FN-07 | — |
| API-08 GET /active | FN-11 | ENG-PT-02 |

*ENG-PT-01 = if type=installment

### API → DB (from 02_API side effects)
| API | Reads | Writes |
|---|---|---|
| API-01/03/08 | T_payment_term (+installment) | — |
| API-02 | (dup check) | T_payment_term, T_payment_term_installment, T_audit_log |
| API-04 | T_payment_term | T_payment_term, installment (replace), T_audit_log |
| API-05/06 | T_payment_term | status, T_audit_log |
| API-07 | T_payment_term (used check) | DELETE (used=0) + CASCADE, T_audit_log |

### Engine ↔ Feature (from 03_LOGIC §3.2)
| Engine | Used by | Status |
|---|---|---|
| ENG-PT-01 installment-validator | F-PAY (validate) + AP/AR Invoice (split) | DRAFT → register |
| ENG-PT-02 payment-trigger-resolver | F-PAY (trigger) + Warehouse/GRN/Ship | DRAFT → register |

---

## 🚨 R8 Verification Matrix

**Rule:** ทุก mutation API มี ≥ 1 Function/Engine
| API (mutation) | Functions | Engines | ✅/❌ |
|---|---|---|---|
| POST /payment-terms | 4 | 1* | ✅ |
| PUT /:id | 4 | 1* | ✅ |
| PATCH /:id/status | 1 | 0 | ✅ |
| POST /bulk-status | 1 | 0 | ✅ |
| POST /bulk-delete | 1 | 0 | ✅ |

**Rule:** No orphan Function/Engine
| Function/Engine | Traced in §3.3? |
|---|---|
| FN-01 createPaymentTerm | ✅ (API-02) |
| FN-02 updatePaymentTerm | ✅ (API-04) |
| FN-03 validatePaymentTerm | ✅ (API-02, 04) |
| FN-04 buildTermListQuery | ✅ (API-01) |
| FN-05 setTermStatus | ✅ (API-05) |
| FN-06 bulkSetStatus | ✅ (API-06) |
| FN-07 bulkDeleteTerms | ✅ (API-07) |
| FN-08 enforceDefaultUniqueness | ✅ (API-02, 04) |
| FN-09 resolveTypeFieldSet | ✅ (API-02, 04) |
| FN-10 buildTermSummary | ✅ (API-01, 03, 08) |
| FN-11 getActiveTermsForPicker | ✅ (API-08) |
| ENG-PT-01 installment-validator | ✅ (API-02, 04) |
| ENG-PT-02 payment-trigger-resolver | ✅ (API-08 + downstream) |

**Result:** R8 PASS — no orphan, ทุก mutation traced ✅

---

## 📊 Pack Statistics

| Metric | Count |
|---|---|
| Pages | 5 (P-01..05) |
| APIs | 8 |
| Functions | 11 |
| Engines | 2 (ENG-PT-01/02) |
| DB Tables | 2 |
| Business Rules | 13 (BR-01..13) |
| Core Validations | 7 (+name) |
| Edge Cases | 11 (EC-01..11) |
| Error codes | 18 |
| Locked Decisions | 6 (LD-F-01..06) + 11 Scope Locks |
| Payment Types | 7 |
| use_in docs | **7 (PR excluded)** |
| Open Questions | 10 (2 blocking: OQ-PAY-04, OQ-PAY-07) |

---

## Coverage Manifest Pointer ⭐
- **00_OVERVIEW §0.12** — Stories 8/8 · Rules 13/13 · Edges (10 confirmed + 9 probe) — ไม่มี requirement หล่น (unresolved → OQ, ไม่หายเงียบ)
- **Scope Lock:** 07_LOCKED §7.0 (11 locks, drift=none)
- **PR exclusion (D-08):** verified 6 จุด — 04_DB enum · 02_API-02/04/08 validation · 05_RULES BR-06 · 06_TESTS AT-06 · 01_UI use_in group · 03_LOGIC FN-03/FN-11

---

## 🎯 Reading Order
1. 00_OVERVIEW (scope + coverage) → 2. 01_UI §1.3 Journey → 3. drill per role (FE:01 / BE:02+03 / DBA:04 / QA:05+06) → 4. 07_LOCKED (constraints).
