# INDEX — FRD F-HR-RECRUIT (F127) สรรหา / Recruit

> **Variant:** FULL · **Audience:** All (navigation entry point)
> **Purpose:** Cross-reference + Function Trace + Quick Nav
> **Source of truth (UI):** `outputs/F-HR-RECRUIT/สรรหา.html` (ผ่าน gate)

---

## 📂 Pack Contents

| # | File | Audience | Content |
|---|---|---|---|
| 00 | OVERVIEW.md | All | Meta + Scope + Dependencies + **Coverage Manifest (FN 21/21)** + Open Questions |
| 01 | UI.md | FE dev | Layout Decision Log (Mode A · observed) + Pages + Journey |
| 02 | API.md | BE dev (HTTP) | 25 APIs + Cross-Module Contract |
| 03 | LOGIC.md | BE dev (logic) | 26 Functions + 2 Engines + Trace |
| 04 | DB.md | DBA / BE | 6 Tables + Data Classification (RESTRICTED) |
| 05 | RULES.md | BE + QA | 10 BR + 5 VR + State Machines + 12 Edge + Errors + Security |
| 06 | TESTS.md | QA | 26 AC + Cross-Module + Microcopy verbatim |
| 07 | LOCKED_DECISIONS.md | All | Scope Lock §7.0 + 5 LD |

---

## 🔍 Quick Nav by Question
- **FE dev เริ่มที่ไหน?** → 01_UI (Layout Decision Log §1.0 + Pages §1.2)
- **BE endpoint ใหม่?** → 02_API §2.2 → 03_LOGIC §3.3 → 04_DB → 05_RULES
- **DBA schema?** → 04_DB §4.2 + §4.6 (RESTRICTED)
- **QA test อะไร?** → 06_TESTS §6.1 (AT-01..26) + 05_RULES §5.5 (Edge)
- **PM risk/open?** → 00_OVERVIEW §0.8 (OQ-15/16/17/R1 + AI-DEFAULT)
- **Architect engine?** → 03_LOGIC §3.2 (ENG-RCT-01/02 DRAFT) + 07 §7.1

---

## 🔗 Cross-Reference Tables

### Page → API
| Page | Actions | Calls |
|---|---|---|
| P-01 req list | row / สร้าง / ส่งอนุมัติ / ประกาศ / ปิด | API-03/02/05-06/07/08 |
| P-02 pool | row / เพิ่มผู้สมัคร | API-11/10 |
| P-03 board | เลื่อนสถานะ / hire | API-14/22 |
| P-04 report | funnel / export | API-24/25 |
| D-01 cand drawer | consent/interview/score/offer | API-13/15/16/17-21 |

### API → Logic (สรุป — เต็มที่ 03_LOGIC §3.3)
| API (mutation) | Functions | Engines |
|---|---|---|
| API-02 create req | FN-01, FN-25 | — |
| API-10 create cand | FN-08, FN-09 | ENG-RCT-02 |
| API-14 move-stage | FN-12, FN-24 | — |
| API-17 create offer | FN-15, FN-25 | — |
| API-22 hire | FN-19, FN-07 | — |
| API-24 funnel | FN-22 | ENG-RCT-01 |

### API → DB
| API | Reads | Writes |
|---|---|---|
| API-02 | (EXT-BAND) | T_recruit_requisition, T_recruit_audit |
| API-10 | pool (dup) | T_recruit_candidate, T_recruit_audit |
| API-14 | candidate | T_recruit_candidate (stage), T_recruit_audit |
| API-17 | (EXT-BAND) | T_recruit_offer, T_recruit_audit |
| API-22 | offer, req | T_recruit_candidate, T_recruit_requisition (filled++), T_recruit_audit + **event** |

### Engine ↔ Feature
| Engine | Used by | Status |
|---|---|---|
| ENG-RCT-01 recruitment-funnel-engine | F-HR-RECRUIT · HR Dashboard (planned) | DRAFT |
| ENG-RCT-02 candidate-duplicate-matcher | F-HR-RECRUIT · Employee rehire (planned) | DRAFT |

---

## 🚨 R8 Verification Matrix

**Rule:** ทุก mutation API มี ≥1 Function/Engine
| API (mutation) | Fn | Eng | ✅ |
|---|---|---|---|
| API-02/04/05/06/07/08 (req) | ≥1 | — | ✅ |
| API-10/12/13/14/15/16 (cand) | ≥1 | RCT-02(10) | ✅ |
| API-17/18/19/20/21 (offer) | ≥1 | — | ✅ |
| API-22 hire / API-23 terminate | ≥1 | — | ✅ |

**No orphan:** FN-01..26 ทุกตัว trace (FN-21 appendAudit + FN-24 viewerGuard = cross-cutting) · ENG-RCT-01 (API-24/25) · ENG-RCT-02 (API-09/10) ✅

---

## 📊 Pack Statistics
| Metric | Count |
|---|---|
| Pages | 4 main + 2 drawer + 6 modals |
| APIs | 25 (+ 3 external read) |
| Functions | 26 |
| Engines | 2 (DRAFT) |
| DB Tables | 6 (owned) |
| Business Rules | 10 BR + 5 VR |
| Edge Cases | 12 (6 confirmed + 6 AI-DEFAULT) |
| Error codes | 18 |
| Locked Decisions | 5 + 7 Scope Lock |
| **FN Coverage** | **21/21** ✅ |
| Open Questions | OQ-15/16/17/R1 + OQ-D1..D4 |

---

## 🎯 Reading Order
1. 00_OVERVIEW (scope + Coverage Manifest) → 2. INDEX (this) → 3. 01_UI (Journey §1.3) → 4. role-specific file → 5. 05_RULES → 6. 06_TESTS

---

## Coverage Manifest Pointer ⭐
- **00_OVERVIEW §0.12** — FN 21/21 + Story/Rule/Edge → ที่อยู่ใน pack (Phase 3.5 K)
- **Scope Lock:** 07_LOCKED §7.0 (immutable)
- **Chain ถัดไป:** step 8 html-ui-brief · step 9 ai-testcase-md-generator · step 10 qc-coverage รอบ 2 · step 11 qa-friendly-html
- **Declarations (doa/ntf/csq):** รันหลัง step 7 — **ผู้ใช้เลือก · AI ไม่เรียกเอง**
