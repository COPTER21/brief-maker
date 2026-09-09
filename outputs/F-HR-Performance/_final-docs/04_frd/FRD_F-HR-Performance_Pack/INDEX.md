# INDEX — FRD F131 Performance / ประเมินผลงาน

> **Variant:** FULL (9 files + INDEX) · **Audience:** All roles (entry point)
> **Feature:** F131 · F-HR-PERF · Module HR · Archetype master+cycle · Declarations doa+ntf+csq

---

## 📂 Pack Contents

| # | File | Audience | Content |
|---|---|---|---|
| 00 | OVERVIEW.md | All | Meta + Scope + Roles + Dependencies + OQ + **Coverage Manifest (FN 18/18)** |
| 01 | UI.md | FE dev | Layout Decision Log + 4 pages (tab-based) + Journey + Notif |
| 02 | API.md | BE dev (HTTP) | 19 API contracts + Cross-Module Contract |
| 03 | LOGIC.md | BE dev (logic) | 20 Functions + 4 Engines + R8 Trace |
| 04 | DB.md | DBA / BE | 5 tables + Data Classification (§4.6) |
| 05 | RULES.md | BE + QA | 13 BR + 2 state machines + guards + 10 EC + errors + security |
| 06 | TESTS.md | QA | 19 AC (per FN) + DoD + 5 cross-module + microcopy verbatim |
| 07 | LOCKED_DECISIONS.md | All | §7.0 Scope Lock (LK-1..6) + LD-01..08 |

---

## 🔍 Quick Nav by Question
- **FE dev เริ่มที่ไหน?** → 01_UI.md (§1.0 Layout Decision Log + §1.2 per-page actions→API)
- **BE dev endpoint ใหม่?** → 02_API §2.2 → 03_LOGIC §3.3 (Functions/Engines) → 04_DB → 05_RULES
- **DBA schema?** → 04_DB §4.2 + §4.6 (classification)
- **QA test อะไร?** → 06_TESTS §6.1 (AC per FN) + 05_RULES §5.5 (EC) + §6.9 (cross-module)
- **PM risk/OQ?** → 00_OVERVIEW §0.8 (7 OQ downstream/config)
- **Architect engine?** → 03_LOGIC §3.2 (ENG-CSQ EC · ENG-DOA chain · ENG-GRADE register)

---

## 🔗 Cross-Reference Tables

### Page → API (from 01_UI §1.2)
| Page (tab) | Actions | Calls |
|---|---|---|
| P-01 cycle | row → detail · สร้างรอบ · ปิดรอบ | API-03 · API-02 (+API-05) · API-04 |
| P-02 appr | filter · row · KPI · self · mgr · reminder | API-06 · API-07 · API-08 · API-09 · API-10 · API-15 |
| P-03 review | send · stage · pip · reopen · dispatch×3 | API-11 · API-12 · API-13 · API-14 · API-16/17/18 |
| P-04 report | filter distribution | API-19 |

### API → Logic (from 03_LOGIC §3.3)
> ดูตารางเต็มที่ 03_LOGIC §3.3 (19 rows). สรุป mutation:

| API (mutation) | Functions | Engines |
|---|---|---|
| POST /cycles | FN-01, FN-16 | ENG-NOTIFY |
| POST /cycles/:id/close | FN-02, FN-16 | — |
| PUT /kpis | FN-03, FN-18, FN-16 | — |
| POST /self | FN-04, FN-18, FN-16 | — |
| POST /manager-review | FN-05, FN-19, FN-18, FN-16 | — |
| POST /calibration/send | FN-06, FN-18, FN-16 | ENG-DOA |
| POST /calibration/stage | FN-07, FN-18, FN-16 | ENG-CSQ, ENG-NOTIFY |
| POST /pip | FN-08, FN-18, FN-16 | — |
| POST /reopen | FN-09, FN-18, FN-16 | — |
| POST /reminder | FN-13 | ENG-NOTIFY |
| POST /dispatch/{training,movement,succession} | FN-10/11/12, FN-18 | — (event) |

### API → DB (side effects)
| API | Reads | Writes |
|---|---|---|
| API-02 | HR Config #107 | T_perf_cycle, T_perf_audit |
| API-08 | T_perf_appraisal | T_perf_kpi_line, appraisal.status, T_perf_audit |
| API-10 | kpi_line | mgr_score, weighted_score, status, audit |
| API-11 | appraisal | T_perf_calibration_stage, audit |
| API-12 | calibration_stage | appraisal.status/decision, audit (+CSQ/notify emit) |
| API-14 | appraisal | audit (append), status='mgr', DELETE calibration_stage |

### Engine ↔ Feature
| Engine | Used by | Status |
|---|---|---|
| ENG-DOA delegation-of-authority | F131 + shared | EXISTING (role-id OQ-PERF-05) |
| ENG-NOTIFY notification | F131 + shared | EXISTING |
| ENG-CSQ compliance-sensitive-queue (7C) | F131 + shared | EXISTING (EC OQ-PERF-06) |
| ENG-GRADE performance-grade-mapper | F131 (+candidate reuse) | DRAFT (register Phase 2 · LD-06) |

---

## 🚨 R8 Verification Matrix (Phase 3.5 Section C)

**Rule:** ทุก mutation API มี ≥1 Function/Engine
| API (mutation) | Fn | Eng | ✅ |
|---|---|---|---|
| POST /cycles | 2 | 1 | ✅ |
| POST /cycles/:id/close | 2 | 0 | ✅ |
| PUT /kpis | 3 | 0 | ✅ |
| POST /self | 3 | 0 | ✅ |
| POST /manager-review | 4 | 0 | ✅ |
| POST /calibration/send | 3 | 1 | ✅ |
| POST /calibration/stage | 3 | 2 | ✅ |
| POST /pip | 3 | 0 | ✅ |
| POST /reopen | 3 | 0 | ✅ |
| POST /reminder | 1 | 1 | ✅ |
| POST /dispatch/×3 | 2 each | 0 (event) | ✅ |

**No orphan Function/Engine:** FN-01..20 + ENG-DOA/NOTIFY/CSQ/GRADE ทุกตัว traced (03_LOGIC §3.3 self-check ✅).

---

## 📊 Pack Statistics
| Metric | Count |
|---|---|
| Pages (tabs) | 4 |
| APIs | 19 |
| Functions | 20 |
| Engines | 4 (3 existing + 1 draft) |
| DB Tables | 5 (+2 soft-ref) |
| Business Rules | 13 |
| Edge Cases | 10 |
| Error codes | 15 |
| FN coverage | **18/18** |
| Locked Decisions | 8 (+6 LK scope lock) |
| Open Questions | 7 (downstream/config) |

---

## 🎯 Reading Order
1. 00_OVERVIEW (scope + coverage) → 2. 01_UI §1.3 (journey) → 3. role-specific file → 4. 05_RULES (guards) → 5. 06_TESTS (bar).

## Coverage Manifest Pointer
- `00_OVERVIEW §0.12` — FN 18/18 + Story/Rule/Edge → ที่อยู่ใน pack
- Scope Lock: `07_LOCKED §7.0` (LK-1..6)
- Declarations (รันหลัง step 7): 03_DOA_BRIEF · 03_NTF_BRIEF · 03_CSQ_BRIEF
