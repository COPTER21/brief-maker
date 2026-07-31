# INDEX — FRD F-CP-001 เปรียบเทียบราคา (Price Comparison)

> **Variant:** FULL · **Audience:** All roles (entry point)
> **Purpose:** Cross-reference + Function Trace + Quick Nav

---

## 📂 Pack Contents

| # | File | Audience | Size hint |
|---|---|---|---|
| 00 | OVERVIEW.md | All | Meta + Scope + Roles + OQ |
| 01 | UI.md | FE dev | 3 Pages (List/Wizard/View) + Components |
| 02 | API.md | BE dev (HTTP) | 10 API contracts |
| 03 | LOGIC.md | BE dev (logic) | 11 Functions + 4 Engines + Trace |
| 04 | DB.md | DBA / BE | 5 Tables + Classification |
| 05 | RULES.md | BE + QA | 11 BR + 8 Edge + Errors + Security |
| 06 | TESTS.md | QA | 15 AC + DoD |
| 07 | LOCKED_DECISIONS.md | All | 6 LD + 2 CD |

---

## 🔍 Quick Nav by Question

- **FE dev เริ่มที่ไหน?** → 01_UI.md (action → API ID อยู่ในแต่ละ page) → 02_API response schema
- **BE dev สร้าง endpoint?** → 02_API §2.2 → 03_LOGIC §3.3 (Functions/Engines) → 04_DB → 05_RULES
- **DBA?** → 04_DB §4.2 (schema + RLS) + §4.4 migration
- **QA?** → 06_TESTS §6.1 AC + 05_RULES §5.5 Edge + §6.4 DoD
- **PM risk/open?** → 00_OVERVIEW §0.8 OQ + 07_LD §7.5
- **Architect — CUBIC engine?** → 03_LOGIC §3.2 (ENG-01/02 DRAFT) + 07_LD §7.1

---

## 🔗 Cross-Reference Tables

### Page → API
| Page | Actions | Calls |
|---|---|---|
| P-01 List | row click | API-02 |
| P-01 List | filter/search/sort/page | API-01 |
| P-01 List | export | API-09 |
| P-02 Wizard | บันทึกร่าง/สร้าง | API-03 (create) / API-04 (update) |
| P-03 View | ส่งเซ็น | API-05 |
| P-03 View | อนุมัติ / ตีกลับ | API-06 / API-07 |
| P-03 View | ออกใบสั่งซื้อ | API-08 |
| P-03 View | PDF (ดาวน์โหลด/preview) | API-10 |

### API → Logic (จาก 03_LOGIC §3.3)
| API | Functions | Engines |
|---|---|---|
| API-01 GET /comparisons | FN-04 | — |
| API-02 GET /comparisons/:id | FN-04 | — |
| API-03 POST /comparisons | FN-01, FN-03, FN-05*, FN-06* | ENG-01, ENG-02, ENG-03, ENG-04* |
| API-04 PUT /comparisons/:id | FN-02 | ENG-01, ENG-02, ENG-03 |
| API-05 POST /submit | FN-05, FN-06 | ENG-04 |
| API-06 POST /approve | FN-07 | ENG-04 |
| API-07 POST /reject | FN-08 | — |
| API-08 POST /award | FN-09 | ENG-02 |
| API-09 GET /export | FN-10 | — |
| API-10 GET /document | FN-11 | ENG-02 |

### API → DB
| API | Reads | Writes |
|---|---|---|
| API-01/02 | T_comparison(+children) | — |
| API-03 | T_purchase_requisition, T_vendor, T_vendor_price | T_comparison(+pr_ref+line+quote), T_audit_log |
| API-04 | T_comparison(+children) | T_comparison_line/quote, T_audit_log |
| API-05/06/07 | T_comparison | T_comparison(status), T_audit_log |
| API-08 | T_comparison(+po_split) | T_comparison(status), T_comparison_po_split(po_id), T_audit_log |

### Engine ↔ Feature
| Engine | Used by | Status |
|---|---|---|
| F-CP-001-ENG-01 price-comparison-winner-engine | F-CP-001 (this), F-RFQ (planned) | DRAFT |
| F-CP-001-ENG-02 po-split-engine | F-CP-001 (this), F-PO-001 (consume) | DRAFT |
| ENG-03 vendor-price-list-resolver | F-PR-001, F-CP-001, F-PO-001 | EXISTING |
| ENG-04 doa-approval-resolver | ทุก feature ที่มี approval | EXISTING |

---

## 🚨 R8 Verification Matrix

**Rule:** ทุก mutation API ต้องมี ≥ 1 Function/Engine

| API (mutation) | Functions | Engines | ✅/❌ |
|---|---|---|---|
| POST /comparisons | 2–4 | 3–4 | ✅ |
| PUT /comparisons/:id | 1 | 3 | ✅ |
| POST /submit | 2 | 1 | ✅ |
| POST /approve | 1 | 1 | ✅ |
| POST /reject | 1 | 0 | ✅ |
| POST /award | 1 | 1 | ✅ |

**Rule:** No orphan Function/Engine

| Function/Engine | Traced? |
|---|---|
| FN-01..FN-03 | ✅ (API-03) |
| FN-04 | ✅ (API-01, API-02) |
| FN-05, FN-06 | ✅ (API-05, API-03*) |
| FN-07 | ✅ (API-06) |
| FN-08 | ✅ (API-07) |
| FN-09 | ✅ (API-08) |
| FN-10 | ✅ (API-09) |
| FN-11 | ✅ (API-10) |
| ENG-01 | ✅ (API-03, API-04) |
| ENG-02 | ✅ (API-03, API-04, API-08, API-10) |
| ENG-03 | ✅ (API-03, API-04) |
| ENG-04 | ✅ (API-05, API-06, API-03*) |

---

## 📊 Pack Statistics

| Metric | Count |
|---|---|
| Pages | 3 (List / Wizard 4-step / View 4-tab) |
| APIs | 10 |
| Functions | 11 |
| Engines | 4 (2 DRAFT + 2 EXISTING) |
| DB Tables | 5 (+4 referenced) |
| Business Rules | 11 |
| Edge Cases | 8 |
| Error codes | 17 |
| Acceptance Criteria | 15 |
| Locked Decisions | 6 (+2 CD) |

---

## 🎯 Reading Order

### First-time (any role)
1. 00_OVERVIEW → scope + roles
2. 01_UI §1.3 Journey → flow PR→CP→PO
3. drill ตาม role

### New dev onboarding
00 → INDEX → (FE: 01) / (BE: 02+03) / (DBA: 04) → 05 → 06

### Architect review
03_LOGIC §3.2 (ENG candidates) → 04_DB → 07_LD → INDEX matrices

---

## 🔄 Pipeline Status

```
HTML prototype (CP_F-CP-001.html, locked) ─┐
PDF document (CP_template.html + print-spec)─┤→ frd-generator-v5 ✅ (FRD_F-CP-001_Pack)
                                             │       ├──→ html-generator-v3 (มี HTML แล้ว ✅)
                                             │       └──→ frd-qa-generator-v2 (next: QA pack)
BRD (ยังไม่มี — reverse mode, ควร back-fill)─┘
```
