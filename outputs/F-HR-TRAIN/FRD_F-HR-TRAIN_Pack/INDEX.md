# INDEX — FRD F-HR-TRAIN · Training (อบรม)

> **Variant:** FULL (9 files + INDEX) · **Archetype:** master
> **Source of truth:** อบรม.html (12 จอ · route `#/train/<tab>`) — FRD 1:1 กับจอ (R14 HTML Fidelity)

---

## 📂 Pack Contents

| # | File | Audience | Content |
|---|---|---|---|
| 00 | OVERVIEW.md | All | Meta + Scope + Roles + Dependencies + OQ + **Coverage Manifest §0.12** |
| 01 | UI.md | FE dev | **Layout Decision Log §1.0** + 12 Pages + Journey + NTF |
| 02 | API.md | BE dev (HTTP) | 28 API contracts + Cross-Module §2.X |
| 03 | LOGIC.md | BE dev (logic) | 21 Functions + 2 Engines + Trace §3.3 |
| 04 | DB.md | DBA / BE | 5 Tables + Classification §4.6 |
| 05 | RULES.md | BE + QA | 18 BR + State Machines + Edge (EC-01..08) + Errors + Security |
| 06 | TESTS.md | QA | 29 AC + 22 TC + DoD + XT cross-module |
| 07 | LOCKED_DECISIONS.md | All | Scope Lock §7.0 (LOCK-01..07) + LD-01..05 |

---

## 🔍 Quick Nav by Question
- **FE dev เริ่มไหน?** → 01_UI (§1.0 Decision Log + §1.2 per-page action → API)
- **BE dev endpoint ใหม่?** → 02_API §2.2 → 03_LOGIC §3.3 → 04_DB → 05_RULES
- **DBA?** → 04_DB (§4.2 schema + §4.6 classification)
- **QA?** → 06_TESTS §6.1 AC + 05_RULES §5.5 Edge
- **PM/SEC risk/OQ?** → 00_OVERVIEW §0.8 (OQ-01..07) + 07_LOCKED §7.5
- **Architect engines?** → 03_LOGIC §3.2 (ENG-TRN-01/02 DRAFT) + 07_LD-02

---

## 🔗 Cross-Reference Tables

### Page → API
| Page | Action | Calls |
|---|---|---|
| P-01 หลักสูตร | คลิกแถว / filter / สร้าง | API-03 / API-01 / API-02 |
| P-02 แผน | คลิกแถว / สร้างรอบ | API-09 / API-08 |
| P-03 ผล | บันทึกผล / ออกใบรับรอง / ประวัติ | API-20 / API-21 / API-27 |
| P-04 รายงาน | filter | API-23 |
| P-08 รอบ (ผู้เรียน) | ลงทะเบียน / เช็คชื่อ / ยกเลิก | API-14 / API-19 / API-18 |
| P-08 (อนุมัติ) | อนุมัติ / ไม่อนุมัติ / ส่ง EC | API-16 / API-17 / API-22 |
| P-10 DOA | ส่งอนุมัติ | API-15 |

### API → Logic (R8)
ดู 03_LOGIC §3.3 (ครบทุก mutation → ≥1 Function; FN-21 audit ทุกตัว)

### API → DB
| API | Reads | Writes |
|---|---|---|
| API-02 | HR Config | T_training_course, audit |
| API-08 | T_training_course | T_training_session, audit |
| API-14 | T_training_session, T_employee, Perf gap | T_training_enrollment, audit |
| API-15 | (DOA resolve) | T_training_approval_step, enrollment, audit |
| API-16 | T_training_approval_step | approval_step, enrollment, audit |
| API-20 | T_training_enrollment/session | enrollment, audit |
| API-22 | T_training_enrollment | enrollment(expense_sent), audit |
| API-23 | enrollment, course | — (mask) |

### Engine ↔ Feature
| Engine | Used by | Status |
|---|---|---|
| ENG-TRN-01 training-completion-metrics | F-HR-TRAIN (report) · HR analytics (planned) | DRAFT |
| ENG-TRN-02 training-hours-accumulator | F-HR-TRAIN (history) · competency (planned) | DRAFT |
| (ext) DOA / ENG-NOTIFY / Rate Card | F-DLG-001 / F-NOTIFY / F060(pending) | EXTERNAL |

---

## 🚨 R8 Verification Matrix

**Rule:** ทุก mutation API มี ≥1 Function/Engine

| API (mutation) | Functions | Engines | ✅ |
|---|---|---|---|
| API-02/04 course | 2 (FN-01/02 + FN-21) | 0 | ✅ |
| API-05/06 publish/close | FN-03/04 + FN-21 | 0 | ✅ |
| API-08/10 session | FN-05 + FN-21 | 0 | ✅ |
| API-11/12 open/close | FN-06/07 + FN-21 | 0 | ✅ |
| API-14 enroll | FN-08/FN-20 + FN-21 | 0 | ✅ |
| API-15 submit-approval | FN-09 + FN-21 | 0 | ✅ |
| API-16 approve | FN-10 + FN-21 | 0 | ✅ |
| API-17 reject | FN-11 + FN-21 | 0 | ✅ |
| API-18 cancel | FN-12 + FN-21 | 0 | ✅ |
| API-19 attendance | FN-13 + FN-21 | 0 | ✅ |
| API-20 result | FN-14 + FN-21 | 0 | ✅ |
| API-21 certificate | FN-15 + FN-21 | 0 | ✅ |
| API-22 expense | FN-16 + FN-21 | 0 | ✅ |

**No orphan Function/Engine:** FN-01..21 + ENG-TRN-01/02 traced ใน 03_LOGIC §3.3 ✅

---

## 📊 Pack Statistics
| Metric | Count |
|---|---|
| Pages (จอ) | 12 (4 tabs + 8 overlay) |
| Routes | 4 (`#/train/course·plan·result·report`) |
| APIs | 28 (17 mutation + read/ref/report + 1 pending) |
| Functions | 21 |
| Engines | 2 (DRAFT) + 3 external |
| DB Tables | 5 |
| Business Rules | 18 (BR-01..18) |
| Edge Cases | 8 (EC-01..08 · Phase 2.5) |
| Error codes | 24 |
| FN coverage | **18/18** (FN-01..13 + FN-90..94) + FIX-01..07 |
| Locked Decisions | 5 (LD-01..05) + Scope Lock LOCK-01..07 |
| Open Questions | 7 (OQ-01..07) |

---

## 🎯 Reading Order
1. 00_OVERVIEW (scope + coverage) → 2. INDEX (this) → 3. 01_UI (FE) / 02_API+03_LOGIC (BE) / 04_DB (DBA) → 4. 05_RULES → 5. 06_TESTS

## Coverage Manifest Pointer
- ทุก BRD requirement + 18 FN → ที่อยู่ใน pack: **00_OVERVIEW §0.12** · Scope Lock: **07_LOCKED §7.0**
