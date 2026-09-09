# _COVERAGE_REPORT (ROUND 2) — F131 Performance / ประเมินผลงาน

> **Gate:** WF-01 step 10 · qc-coverage-checker **รอบ 2** (FRD Pack + Test Cases ก่อนส่ง dev)
> **Mode:** REPORT (ไม่แก้ artifact) · **Date:** 2026-09-09
> **รอบ 1** (HTML vs contract) = 🟢 PASS แล้ว (`_COVERAGE_REPORT.md`) — รอบ 2 ตรวจคนละคำถาม: *spec + test ผูกเรื่องครบมั้ย*

---

## VERDICT: 🟢 **PASS**

| มิติ | ผล |
|---|---|
| FN ↔ TC ledger | **18 / 18** checklist FN มี TC ≥1 (dedicated + master sweep TC-TM02) |
| Rules ใน 05_RULES ↔ TC | **BR 13/13 · VR 10/10 · EC 10/10** มี TC ≥1 — ไม่มี orphan rule |
| Cross-module (XT) | **5 / 5** (XT-01..05 → TC-XT01..05) |
| Declaration coverage | **DOA · NTF · CSQ** brief มีครบ + sync-read ใน FRD + align (NTF 6 event 1:1 · CSQ SecC/DC only · DOA slot no-hardcode) |
| Scope-lock | **LK-1..6 verified** (TC-LK01..06) · exclusions = negative "ไม่มีบนจอ" (TC-LK02/03/05) — ไม่ทดสอบของนอกขอบเขต |
| Orphan TC / scope creep | ไม่มี — 77 TC ทุกตัว trace กลับ FN/AC/BR/VR/EC/XT/LK |
| **Total TC** | **77** cases |

**block-severity ครบทุกข้อ → ไม่มีเหตุ BLOCK · ไม่มี WARN.**

---

## 1. FN ↔ TC Ledger (18/18) ⭐

FN namespace = FUNCTION_CHECKLIST / PREBRIEF (FN-01..13 + FN-90..94). ยืนยันตรงกับ 00_OVERVIEW §0.12 Coverage Manifest.

| FN | ความสามารถ | AC (06_TESTS) | TC (testcases-performance.md) |
|---|---|:--:|---|
| FN-01 | สร้างรอบจาก HR Config → เปิดกรอก | AC-01 | TC-CY01, CY02, CY03, CY06, CY07 |
| FN-02 | ตั้งเป้า/KPI Σweight=100 | AC-03 | TC-KP01, KP02, KP03, KP04, KP05 |
| FN-03 | พนักงานประเมินตนเอง | AC-04 | TC-SF01, SF02, SF03 |
| FN-04 | หัวหน้าประเมิน + weighted | AC-05 | TC-MG01, MG02, MG03, MG04 |
| FN-05 | สอบทาน (calibration) + decision | AC-07 | TC-CB03, CB04, CB06, CB07 |
| FN-06 | gap → Training hook | AC-09 | TC-PB01, PB05, XT-02 |
| FN-07 | ผล → Movement event | AC-10 | TC-PB02, PB03, PB04, XT-01, XT-03 |
| FN-08 | สอบทานผ่าน DOA slot picker (staged, no-hardcode) | AC-08 | TC-CB01, CB02, CB05, LK-01 |
| FN-09 | ประเมินไม่ครบ/overdue → เตือน + re-open | AC-06 | TC-OD01, OD02, RO01..RO05 |
| FN-10 | คะแนนต่ำ/ทบทวน → PIP | AC-11 | TC-PP01, PP02 |
| FN-11 | ปิดรอบ (ล็อกแก้จริง) | AC-02 | TC-CY04, CY05 |
| FN-12 | แจ้งเตือน 3 event | AC-12 | TC-NT01 |
| FN-13 | รายงาน distribution + filter | AC-13 | TC-RP01, RP02, RP03, RP04 |
| FN-90 | ค้นหา/filter + empty state | AC-14 | TC-SR01, SR02, SR03, SR04 |
| FN-91 | ปิด/ยกเลิกผ่าน confirm + soft archive | AC-02 | TC-CY04 |
| FN-92 | field validate + กัน double-submit | AC-15 | TC-GD05, AU02 |
| FN-93 | audit append-only ทุก create/แก้/สอบทาน | AC-16 | TC-AU01, AU02, SC07 |
| FN-94 | ปิดบังผล (RESTRICTED) ตาม role | AC-17 | TC-SC01..07, SR04 |

> **ทุก FN ยังถูก sweep ด้วย TC-TM02 (master coverage)** · logic-layer FN-18 (guardMutation) → TC-GD01..04 · FN-19 (weighted) → TC-MG02.
> Chain: **FN → AC (06_TESTS §6.1) → TC** ครบทุกเส้น · Coverage Manifest §0.12 = FN 18/18 ✅.

---

## 2. Rule ↔ TC (05_RULES)

**Business Rules (BR) 13/13**

| BR | TC (ตัวอย่าง) | | BR | TC |
|---|---|---|---|---|
| BR-01 config cycle | TC-CY01, LK03 | | BR-08 RESTRICTED/mask | TC-LK04, RP04, SC01..07 |
| BR-02 Σweight=100 | TC-KP01, KP02 | | BR-09 audit append-only + close lock | TC-AU01, AU02, CY04, RO04 |
| BR-03 self ก่อน mgr | TC-SF01, SF03, SC04 | | BR-10 snapshot ณ รอบ | **TC-SC03** |
| BR-04 weighted score | TC-MG01, MG02 | | BR-11 scope SELF/DEPT/ALL | TC-SC01, SC03, SC05 |
| BR-05 staged DOA + decision | TC-CB01, CB03, CB04, PP01 | | BR-12 re-open published | TC-RO01..05, PB05 |
| BR-06 gap → Training | TC-PB01, LK05, XT02 | | BR-13 CSQ per-person publish | TC-CB04, XT04, RO05, LK06 |
| BR-07 ผล → Movement event | TC-PB02, PB04, LK02, XT01 | | | |

**Field Validation (VR) 10/10** — VR-01 TC-KP02 · VR-02 TC-CB02 · VR-03 TC-RO02 · VR-04 TC-CY05 · **VR-05 (role 403) TC-GD03, SC06, SC07** · VR-06 TC-GD05 · VR-07 TC-GD01 · VR-08 TC-MG03, SF02 · VR-09 TC-KP03 · VR-10 TC-PP02.

**Edge Cases (EC) 10/10** — EC-01 TC-GD01 · EC-02 TC-GD02, KP05 · EC-03 TC-GD03, SC06 · EC-04 TC-SC01, SC02 · EC-05 TC-GD06 · EC-06 TC-CFG-01/TM02 · EC-07 TC-CY05, GD04 · EC-08 TC-CB01, CB05, LK01 · EC-09 TC-OD01 · EC-10 TC-SC03.

> BR-10 และ VR-05 มี TC จริง (ผ่าน rule↔TC ledger ในตัว testcases §บน — line 89/101) — **ไม่มี rule ใดใน 05_RULES ที่ไม่มี TC.**
> State machine (§5.2) guard cascade (closed→role→stage→scope) → TC-GD01..06 (AC-19 P1-P4). Error catalog map ครบ (ERR_STAGE_INVALID/BR_CYCLE_CLOSED/ERR_INSUFFICIENT_ROLE/…).

---

## 3. Declaration ↔ FRD (Phase 0b)

| ท่อ | brief | เข้าเงื่อนไข | sync-read ใน FRD | align | TC |
|---|---|---|---|:--:|---|
| **DOA** | `DOA_BRIEF_F-HR-Performance.md` | ✅ staged calibration (BR-05) | 03_LOGIC ENG-DOA · API-11/12/14 · 05_RULES BR-05 | ✓ slot-based, ไม่ hardcode chain (chain=DYNAMIC รอ CL-0013/OQ-PERF-05) | TC-CB01, CB02, CB05, LK01 |
| **NTF** | `NTF_BRIEF_F-HR-Performance.md` | ✅ cycle open/overdue/publish | 02_API + 03_LOGIC | ✓ **6 event 1:1** (`perf.cycle.opened`·`deadline.overdue`·`result.published`·`gap.training_requested`·`result.movement_requested`·`result.succession_candidate`) · doa_* ไม่ประกาศซ้ำ | TC-NT01, XT01/02/03 |
| **CSQ** | `CSQ_BRIEF_F-HR-Performance.md` | ✅ RESTRICTED + decision (BR-08/13) | 03_LOGIC ENG-CSQ · API-12 · 05_RULES BR-13/§5.7 | ✓ ประกาศ **SecC + DC เท่านั้น** (ไม่มี OC/DC-doc/SC · LK-6) · per-person publish | TC-CB04, XT04, RO05, LK06 |

**event ใน FRD ⊆ brief** ครบ · ไม่มี hardcoded chain / channel / running-number ใน FRD → **Declaration coverage OK.**
DOCCFG: checklist signal = true แต่ feature ไม่ออกเอกสารธุรกรรมเลขรัน (Pattern Q) — ไม่มี DOCCFG brief = **ถูกต้อง** (N/A · ไม่มี doc archetype).

---

## 4. Scope-Lock (07_LOCKED §7.0)

LK-1..6 verify ครบผ่าน TC-LK01..06. Exclusions ตามใบเซ็น (ปรับเงินเดือน/ตำแหน่งเอง · สร้าง/แก้ฟอร์มกลาง · สร้างหลักสูตร · 360/competency/check-in) → **ไม่สร้างเคส positive** แต่มีเคส verify "ไม่มีความสามารถนี้บนจอ" (TC-LK02/03/05) — scope-lock ถูกเคารพ ไม่มี scope creep เข้า TC.

---

## 5. Gap / Divergence

**ไม่มี coverage gap.** ทุก FN/rule/edge/XT/declaration มี evidence ชี้ตำแหน่งได้.

Carried OQ (**OQ-PERF-05..11**) = FRD-phase / downstream / config items (role-id CL-0013, EC valuation, Restricted Resources ACL, mock-data demo dept, concurrency architect-confirm) — ตาม Coverage Manifest §0.12 ระบุชัดว่า **ไม่ block FRD** และ**ไม่ใช่ coverage gap** ของ step นี้ (เป็นการตัดสินปลายทางที่ BA/Architect เคาะ ไม่ใช่ของหายจาก spec/test).

---

## 6. Diff vs รอบ 1

| | รอบ 1 (HTML) | รอบ 2 (FRD+TC) |
|---|---|---|
| Verdict | 🟢 PASS (FN 18/18 · S 12/12 · negatives 4/4 absent) | 🟢 PASS (FN↔TC 18/18 · rules ครบ · decl align) |
| Gap ที่ปิดแล้ว | — | ไม่มี gap ค้างจากรอบ 1 |
| Gap เกิดใหม่ | — | ไม่มี |

**พร้อมส่ง dev handoff** — spec (FRD) + test (77 TC) ผูกครบทุก requirement.

---

### Quality-gate ของตัว checker
- [x] ทุก ✓ มี evidence (TC id / FRD section / brief) — ไม่มีการสุ่ม
- [x] ไม่ invent เกณฑ์นอก contract (FUNCTION_CHECKLIST + 05_RULES + Coverage Manifest)
- [x] item ที่ N/A (DOCCFG) ระบุเหตุผล ไม่ mark ✓ ลอย
- [x] BLOCK เฉพาะเมื่อ block-severity ไม่ครอบ — ไม่มี → PASS
