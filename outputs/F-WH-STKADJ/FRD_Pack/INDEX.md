# INDEX — FRD F082 F-WH-STKADJ ใบปรับยอดสต๊อก (Stock Adjustment)

> **Variant:** FULL · **Audience:** All roles (entry point)
> **Purpose:** Cross-reference + Function Trace + Quick Nav

---

## 📂 Pack Contents
| # | File | Audience | Content |
|---|---|---|---|
| 00 | OVERVIEW.md | All | Meta + Scope + Roles + Dependencies + **Coverage Manifest (55 FN)** + OQ |
| 01 | UI.md | FE dev | Layout Decision Log + 3 pages + 4 modals + wizard 5 steps + view 4 tabs |
| 02 | API.md | BE dev (HTTP) | 20 endpoints + Cross-Module Contract |
| 03 | LOGIC.md | BE dev (logic) | 18 Functions + 2 Engines + Trace Table |
| 04 | DB.md | DBA / BE | 7 tables + classification |
| 05 | RULES.md | BE + QA | BR-01..27 + VR-01..17 + State Machine + Edge + Errors |
| 06 | TESTS.md | QA | 26 AC + 11 XT + 9 NEG + microcopy verbatim |
| 07 | LOCKED_DECISIONS.md | All | LOCK-01..10 + LD-01..08 |

---

## 🔍 Quick Nav by Question
- **FE dev:** 01_UI (routes: `#/list` `#/create` `#/edit/:id` `#/view/:id`) → 02_API response shapes
- **BE dev:** 02_API §2.2 → 03_LOGIC §3.3 (Functions/Engines) → 04_DB → 05_RULES
- **DBA:** 04_DB (T_stock_adjustment + line/approval/attachment + T_inventory_movement)
- **QA:** 06_TESTS §6.1 AC + §6.7 negatives + 05_RULES §5.5 edge
- **PM/risk:** 00 §0.8 OQ + 07 §7.1 LD (FIX-02/03/04)
- **Architect:** 03 §3.2 (ENG-01/02 CUBIC candidate) + 07 LD-02/03

---

## 🔗 Cross-Reference Tables

### Page → API
| Page | Action | Calls |
|---|---|---|
| P-01 list | row click | F082-API-02 |
| P-01 | filter/KPI | F082-API-01 |
| P-01 | เอกสารแนบ landing | F082-API-20 |
| P-02 wizard | bin/item picker | F082-API-13/14/15 |
| P-02 | save draft | F082-API-03/04 |
| P-04 submit | ส่งอนุมัติ | F082-API-05 |
| P-05 | อนุมัติ/ตีกลับ | F082-API-06/07 |
| P-06 | ผ่านรายการ | F082-API-09 |
| P-07 | ยกเลิก/กลับรายการ | F082-API-08/10 |
| P-03 view | PDF / movements | F082-API-19/11 |

### API → Logic
| API | Functions | Engines |
|---|---|---|
| API-01 | FN-01 | — |
| API-03 | FN-02, FN-04 | — |
| API-04 | FN-03, FN-07, FN-04 | ENG-01 |
| API-05 submit | FN-06, FN-08 | ENG-01, ENG-DOC-NUM*, DOA* |
| API-06 approve | FN-09 | — |
| API-07 reject | FN-10 | — |
| API-08 cancel | FN-11 | — |
| API-09 post | FN-12, FN-13 | ENG-02, ENG-DOC-STORE*, ENG-CSQ* |
| API-10 reverse | FN-14 | ENG-01, ENG-DOC-NUM*, DOA* |
| API-11/12/13/15/19/20 | FN-16/15/05/04/17/18 | (ENG-01 @19) |

### API → DB
| API | Reads | Writes |
|---|---|---|
| API-03 create | masters | T_stock_adjustment(+line), audit |
| API-05 submit | doc | status+adj_no, T_..._approval, audit |
| API-09 post | doc, ledger | **T_inventory_movement** (append), status, audit |
| API-10 reverse | doc | ใบกลับรายการใหม่ + approval, links, audit |

### Engine ↔ Feature
| Engine | Used by | Status |
|---|---|---|
| F082-ENG-01 adjustment-valuation-engine | F082 (this), F083 (planned) | DRAFT |
| F082-ENG-02 inventory-movement-engine | F082 (this), F083 (planned) | DRAFT |
| ENG-DOC-NUM/STORE, DOA resolver, ENG-NOTIFY, ENG-CSQ | external | EXISTING (declared) |

---

## 🚨 R8 Verification Matrix

**Rule:** ทุก mutation API มี ≥1 Function/Engine
| API (mutation) | Fn | Eng | ✅ |
|---|---|---|---|
| POST create (03) | 2 | 0 | ✅ |
| PUT update (04) | 3 | 1 | ✅ |
| POST submit (05) | 2 | 1(+2 ext) | ✅ |
| POST approve (06) | 1 | 0 | ✅ |
| POST reject (07) | 1 | 0 | ✅ |
| POST cancel (08) | 1 | 0 | ✅ |
| POST post (09) | 2 | 1(+2 ext) | ✅ |
| POST reverse (10) | 1 | 1(+2 ext) | ✅ |
| POST attachments (12) | 1 | 0 | ✅ |

**No orphan:** ทุก FN-01..18 + ENG-01/02 ปรากฏใน trace (03 §3.3) ✅

---

## 📊 Pack Statistics
| Metric | Count |
|---|---|
| Top-level pages | 3 (list/wizard/view) + 4 modal groups |
| Wizard steps / view tabs | 5 / 4 |
| APIs | 20 (9 mutation) |
| Functions | 18 |
| Engines (owned) | 2 (+4 external declared) |
| DB tables (owned) | 5 (+config/masters) |
| Business Rules | 27 (BR-01..27) + 17 VR |
| Edge Cases | 7 |
| Errors | ~23 |
| Locks / LDs | 10 LOCK + 8 LD |
| **FN coverage** | **55/55** |
| Cross-module (XT) | 11 |

---

## 🎯 Reading Order
1. 00_OVERVIEW (scope + coverage) → 2. 01_UI §1.3 journey → 3. drill by role
- BE onboarding: 00 → INDEX → 02 + 03 → 04 → 05 → 06
- Architect: 03 §3.2 → 04 → 07 → INDEX matrices

## Coverage Manifest Pointer
- ดู `00_OVERVIEW §0.12` — ทุก BRD requirement (55 FN + stories + rules + edges + downstream) → ที่อยู่ใน pack
- Scope Lock: `07_LOCKED §7.0` (LOCK-01..10)
- BA re-gate fixes: **FIX-02** (07 LD-06) · **FIX-03** (LD-05) · **FIX-04** (LD-07)
