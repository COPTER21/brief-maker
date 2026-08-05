# INDEX — FRD F-TAX Tax Code (รหัสภาษี)

> **Variant:** FULL (9 files + INDEX) · **Entry point for navigation**
> **Purpose:** Cross-reference + Function Trace + Quick Nav

---

## 📂 Pack Contents

| # | File | Audience | Content |
|---|---|---|---|
| 00 | OVERVIEW.md | All | Meta + Scope + Variant decision + Coverage Manifest + Open Questions |
| 01 | UI.md | FE dev | Layout Decision Log (5 pages) + Journey |
| 02 | API.md | BE dev (HTTP) | 12 API contracts + Cross-Module Contract (5 downstream) |
| 03 | LOGIC.md | BE dev (logic) | 14 Functions + 3 Engines + Trace |
| 04 | DB.md | DBA / BE | 3 tables + CoA/Snapshot references + Classification |
| 05 | RULES.md | BE + QA | 15 BR + 13 VR + 19 Edge cases + Errors + Security |
| 06 | TESTS.md | QA | 12 AC + DoD + 5 Cross-Module cases |
| 07 | LOCKED_DECISIONS.md | All | Scope Lock (12) + 5 LD + Convention deviations |

---

## 🔍 Quick Nav by Question

- **FE dev เริ่มที่ไหน?** → 01_UI (Layout Decision Log §1.0 → per-page §1.2 → action→API)
- **BE dev สร้าง endpoint?** → 02_API §2.2 → 03_LOGIC §3.3 (Functions/Engines) → 04_DB → 05_RULES
- **DBA?** → 04_DB (§4.2 schema, §4.6 classification, §4.4 seed)
- **QA?** → 06_TESTS §6.1 AC + 05_RULES §5.5 edge + §6.9 cross-module
- **PM / risk?** → 00_OVERVIEW §0.8 Open Questions + 07 §7.5
- **Architect / CUBIC?** → 03_LOGIC §3.2 (ENG DRAFT) + 07 §7.1 LD-02

---

## 🔗 Cross-Reference Tables

### Page → API
| Page | Action | Calls |
|---|---|---|
| P-01 List | row click | F-TAX-API-02 |
| P-01 List | สร้าง / picker / deactivate | API-03 / API-09 / API-06 |
| P-01 List | filter/tab | API-01 |
| P-02 Form | บันทึกร่าง | API-03 (draft) / API-04 |
| P-02 Form | ยืนยันสร้าง/บันทึกการแก้ไข | API-03/04 (+API-05 activate) |
| P-02 Form | GL combobox / income type | API-11 / API-12 |
| P-02 Form | สร้างรหัสแทน | API-08 |
| P-03 View | audit | API-10 |
| P-04 Picker | resolve | API-09 |
| P-05 Confirm | deactivate/archive | API-06/07 |

### API → Logic (จาก 03_LOGIC §3.3)
| API | Functions | Engines |
|---|---|---|
| API-01 GET /tax-codes | FN-01 | — |
| API-02 GET /:id | — | — |
| API-03 POST /tax-codes | FN-02,04,14,12,13,(05) | ENG-03 |
| API-04 PUT /:id | FN-03,04,13 | — |
| API-05 POST /:id/activate | FN-05,04,13 | ENG-03 |
| API-06 POST /:id/deactivate | FN-06,13 | — |
| API-07 POST /:id/archive | FN-07,13 | — |
| API-08 POST /:id/replacement | FN-08,04,05,13 | — |
| API-09 GET /pickable | FN-09 | ENG-02, ENG-01 |
| API-10 GET /:id/audit | FN-13 | — |
| API-11 GET /gl-accounts | FN-11 | ENG-03 |
| API-12 GET /income-types | — | — |

### API → DB (Side effects)
| API | Reads | Writes |
|---|---|---|
| API-01/02 | T_tax_code | — |
| API-03 | T_tax_code (uniq), CoA | T_tax_code, T_tax_code_audit |
| API-04 | T_tax_code | T_tax_code (version++), audit |
| API-05 | T_tax_code, CoA | T_tax_code (status), audit |
| API-06/07 | T_tax_code | T_tax_code (status, eff_end), audit |
| API-08 | T_tax_code | T_tax_code ×2 (new+old lineage), audit ×2 |
| API-09 | T_tax_code | — |
| API-10 | T_tax_code_audit | — (log access) |
| API-11 | T_gl_account (CoA) | — |
| API-12 | T_income_type | — |

### Engine ↔ Feature
| Engine | Used by | Status |
|---|---|---|
| ENG-TAX-01 tax-snapshot-builder | F-TAX + consumer docs (planned) | DRAFT |
| ENG-TAX-02 effective-date-resolver | F-TAX + consumer pickers (planned) | DRAFT |
| ENG-TAX-03 gl-role-validator | F-TAX + CoA validations (planned) | DRAFT |

---

## 🚨 R8 Verification Matrix (Phase 3.5 Section C anchor)

**Rule:** ทุก mutation API มี ≥1 Function/Engine

| API (mutation) | Functions | Engines | ✅/❌ |
|---|---|---|---|
| POST /tax-codes | 5 (+1) | 1 | ✅ |
| PUT /:id | 3 | 0 | ✅ |
| POST /:id/activate | 3 | 1 | ✅ |
| POST /:id/deactivate | 2 | 0 | ✅ |
| POST /:id/archive | 2 | 0 | ✅ |
| POST /:id/replacement | 4 | 0 | ✅ |

**Rule:** No orphan Function/Engine

| Function/Engine | Traced? |
|---|---|
| FN-01 | ✅ API-01 |
| FN-02 | ✅ API-03 |
| FN-03 | ✅ API-04 |
| FN-04 | ✅ API-03/04/05/08 (via FN + validate) |
| FN-05 | ✅ API-05 (+03/08) |
| FN-06 | ✅ API-06 |
| FN-07 | ✅ API-07 |
| FN-08 | ✅ API-08 |
| FN-09 | ✅ API-09 |
| FN-11 | ✅ API-11 |
| FN-12 | ✅ API-03/05 (via FN-02/03) |
| FN-13 | ✅ ทุก mutation + API-10 |
| FN-14 | ✅ API-03/04 (via FN-02/03) |
| FN-15 | ✅ seed job (CD-03 documented — ไม่ใช่ orphan) |
| ENG-01 | ✅ API-09 |
| ENG-02 | ✅ API-09 |
| ENG-03 | ✅ API-03/05/11 + FN-04/11 |

> ไม่มี FN-10 (numbering ข้ามโดยตั้งใจ — 03_LOGIC §3.3 note). ไม่มี orphan.

---

## 📊 Pack Statistics

| Metric | Count |
|---|---|
| Pages | 5 (ตรง HTML) |
| APIs | 12 (6 mutation) |
| Functions | 14 |
| Engines | 3 (DRAFT) |
| DB Tables (owned) | 3 (+CoA ref +Snapshot external) |
| Business Rules | 15 BR + 13 VR |
| Edge Cases | 19 |
| Cross-Module contracts | 5 (all External) |
| Error codes | 13 |
| Scope Locks | 12 |
| Locked Decisions | 5 |
| Open Questions | 9 ค้าง (OQ-3,4,5,6,7,8,9,10,11) + 2 resolved-out |

---

## 🎯 Reading Order

- **First-time:** 00 → 01 §1.3 Journey → drill down per role
- **New dev:** 00 → INDEX → 01 (FE) / 02+03 (BE) / 04 (DBA) → 05 → 06
- **Architect:** 03 §3.2 → 04 → 07 → INDEX matrices

---

## Coverage Manifest Pointer ⭐
- **Coverage Manifest:** `00_OVERVIEW §0.12` — ทุก BRD §7/§9/§10 → ที่อยู่ใน pack (Stories 10/10, Rules 17/17, Edges 19/19)
- **Scope Lock:** `07_LOCKED §7.0` (LOCK-01..12)
- **Design-Authority sync log:** `00_OVERVIEW §0.1.1` (html-generator-v7, Warm Light)
