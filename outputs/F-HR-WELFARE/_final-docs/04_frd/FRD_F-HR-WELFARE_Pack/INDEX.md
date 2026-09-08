# INDEX — FRD F-HR-WELFARE · Welfare (สวัสดิการ)

> **Variant:** FULL · **Audience:** All (entry point) · **Purpose:** Cross-reference + Function Trace + Quick Nav

---

## 📂 Pack Contents
| # | File | Audience |
|---|---|---|
| 00 | OVERVIEW.md | All — meta + scope + Coverage Manifest §0.12 |
| 01 | UI.md | FE — Layout Decision Log + Pages (route จริง) |
| 02 | API.md | BE (HTTP) — 17 API + Cross-Module Contract |
| 03 | LOGIC.md | BE (logic) — 19 Functions + 2 Engines (NEW) + externals |
| 04 | DB.md | DBA — 6 tables + Classification |
| 05 | RULES.md | BE+QA — BR-01..12 + BR-DOA guards + State Machine + Errors |
| 06 | TESTS.md | QA — AT-01..27 + Cross-Module XT-01..05 |
| 07 | LOCKED_DECISIONS.md | All — Scope Lock §7.0 (LK-1..6) + LD-01..05 |

---

## 🔍 Quick Nav
- **FE dev:** 01_UI (route `#/welfare/*` + Layout Decision Log §1.0)
- **BE dev:** 02_API §2.2 → 03_LOGIC §3.3 (trace) → 04_DB → 05_RULES
- **QA:** 06_TESTS §6.1 (AT) + 05_RULES §5.5 (EC) + §6.9 (XT)
- **PM:** 00 §0.8 (OQ) · 07 §7.3 · 00 §0.12 (Coverage)
- **Architect:** 03 §3.2 (ENG-WEL-01/02 DRAFT) · 07 §7.4

---

## 🔗 Cross-Reference

### Page → API
| Page/Overlay | Action | Calls |
|---|---|---|
| P-01 registry | create/edit/archive/view | API-02/04/05/03 |
| P-02 requests | create / row / filter | API-09 / API-10 / API-08 |
| P-03 balance | เลือกคน / add-dep / remove-dep | API-16 / API-06 / API-07 |
| P-04 report | filter | API-17 |
| M-01 doa | ส่งอนุมัติ | API-11 |
| M-02 approve | อนุมัติ | API-12 |
| M-03 reject | ไม่อนุมัติ | API-13 |
| M-04 reverse | กลับรายการ | API-15 |
| M-05 cancel | ยกเลิก | API-14 |

### API → Logic (จาก 03_LOGIC §3.3)
| API | Functions | Engines |
|---|---|---|
| API-02/04 | FN-01/02, FN-03 | — |
| API-09 | FN-07, FN-08 | ENG-WEL-01/02 |
| API-11 | FN-10 | ENG-DOA |
| API-12 | FN-11, FN-19 | ENG-WEL-01/02, ENG-CSQ, ENG-NOTIFY |
| API-15 | FN-14, FN-19 | ENG-WEL-02, ENG-CSQ, ENG-NOTIFY |
| API-16 | FN-15, FN-16 | ENG-WEL-02 |

### API → DB
| API | Reads | Writes |
|---|---|---|
| API-02/04 | benefit_type | benefit_type, audit_log |
| API-09 | benefit_type, employee(soft), hr-config | request(+attachment), audit_log |
| API-11 | request, doa/resolve | request_approval[], request(status), audit_log |
| API-12 | request, request_approval | request_approval, request(status/pay), audit_log |
| API-15 | request | request(reverse fields), audit_log |

### Engine ↔ Feature
| Engine | Used by | Status |
|---|---|---|
| ENG-WEL-01 eligibility-resolver | F-HR-WELFARE (+HR planned) | DRAFT |
| ENG-WEL-02 balance-calculator | F-HR-WELFARE | DRAFT |
| ENG-DOA (F-DLG-001) | F-HR-WELFARE + all approval features | EXISTING |
| ENG-CSQ (F-CSQ-01) | F-HR-WELFARE (EC only) | EXISTING |
| ENG-NOTIFY (F-NOTIFY) | F-HR-WELFARE (5 events) | EXISTING |

---

## 🚨 R8 Verification Matrix
| API (mutation) | Functions | Engines | ✅ |
|---|---|---|---|
| POST /benefit-types | 2 | 0 | ✅ |
| PUT /benefit-types/:id | 2 | 0 | ✅ |
| POST archive | 1 | 0 | ✅ |
| POST/DELETE dependents | 1 | 0 | ✅ |
| POST /requests | 2 | 2 | ✅ |
| POST submit | 1 | 1 | ✅ |
| POST approve | 2 | 4 | ✅ |
| POST reject | 2 | 1 | ✅ |
| POST cancel | 2 | 0 | ✅ |
| POST reverse | 2 | 3 | ✅ |

**No orphan:** FN-01..19 + ENG-WEL-01/02 traced ใน §3.3 ✅.

---

## 📊 Pack Statistics
| Metric | Count |
|---|---|
| Pages (tabs) | 4 · +5 drawer +7 modal |
| APIs | 17 (+5 external reads/hook) |
| Functions | 19 |
| Engines | 2 NEW (DRAFT) + 3 external |
| DB Tables | 6 (owned) + soft refs |
| Business Rules | 12 BR + 8 BR-DOA + 3 BR-BAL |
| States (request) | 9 (incl. **reversed**) |
| Edge Cases | 6 confirmed + 8 probes |
| Error codes | 21 |
| Locked Decisions | 5 (LD) + Scope Lock LK-1..6 |
| FN coverage | 24/24 |

---

## Coverage Manifest Pointer
- ทุก BRD/FN requirement → 00_OVERVIEW §0.12 (24 FN mapped · Phase 3.5 K verify)
- Scope Lock → 07_LOCKED §7.0 (LK-1..6)
- OQ ค้าง (blocking): OQ-03 (hook contract) · OQ-04 (atomic re-check) · OQ-05 (backend enforce) → 00 §0.8
