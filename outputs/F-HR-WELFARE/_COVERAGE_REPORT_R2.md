# _COVERAGE_REPORT_R2 — F-HR-WELFARE · Welfare (สวัสดิการ)

> **Round 2** (FRD Pack + Test Cases · ก่อนส่ง dev) — แยกจากรอบ 1 (`_COVERAGE_REPORT.md` = HTML hook)
> **Skill:** qc-coverage-checker · **Question:** "spec + test ผูกเรื่องครบมั้ย" (ไม่ตรวจ HTML hook ซ้ำ · ไม่ตรวจ CI/iron rules)
> **Date:** 2026-09-08 · **Contract:** PREBRIEF + FUNCTION_CHECKLIST (24 FN + 5 unsupported) · FRD Pack v1.0 · testcases-welfare.md (60 cases)

---

## VERDICT: **PASS** 🟢

FN↔TC ledger **24/24** · rules ครบ (BR-01..12 + BR-DOA-1..8 + BR-BAL-1..3 = 23/23 มี TC) · VR **12/12** · declarations **DOA+NTF+CSQ ครบ · consistent** (DOCCFG/PDFDOC = N/A justified) · scope lock 5 NS = negative verify ครบ · **gap block 0** · scope creep 0.
**WARN (non-block · advisory):** 3 ข้อ — chip≠declare divergence (OQ-06 · NTF justified) · R15 cross-artifact parity deferred (QA HTML = step 11 ยังไม่ทำ) · OQ ปลายทาง blocking ที่ Phase B/wire (OQ-03/04/05 · OQ-DOA-01) ยกให้ BA แล้ว — ไม่ใช่ coverage gap.

---

## §1 · FN ↔ TC Ledger (24/24) + Rule presence

| FN | สรุป | Rule ใน 05_RULES | TC (testcases-welfare.md) | ✓ |
|---|---|---|---|:--:|
| FN-01 | สร้างประเภท + กลุ่ม/โควตา/effective | BR-03 · VR-01/03 | TC-REG-01, TC-REG-02 | ✓ |
| FN-02 | แก้ = เวอร์ชันใหม่ | BR-03 · VR-02 | TC-REG-03, TC-REG-04 | ✓ |
| FN-03 | ปิดใช้ (soft archive) | BR-07 · BR-DOA-8 | TC-REG-05 | ✓ |
| FN-04 | quota≤0 / effective ทับ → บล็อก | VR-01/VR-02 · BR-03 | TC-REG-06, TC-REG-07 | ✓ |
| FN-05 | เพิ่มผู้ติดตาม | VR-06/VR-07 | TC-DEP-01, TC-DEP-03 | ✓ |
| FN-06 | ผู้ติดตามเกิน/บุตรอายุเกิน | VR-06/VR-07 | TC-DEP-02, TC-DEP-04 | ✓ |
| FN-07 | สร้างคำขอ type มีสิทธิ์ + self/dep + แนบ | BR-01 · BR-10 | TC-REQ-01, TC-REQ-02 | ✓ |
| FN-08 | ส่งอนุมัติ DOA slot picker | BR-04 · VR-09 · BR-DOA-2 | TC-DOA-01, TC-DOA-02 | ✓ |
| FN-09 | ใช้บางส่วน — คงเหลือถูกต้อง | BR-02/BR-05 · BR-BAL-1 | TC-BAL-02 | ✓ |
| FN-10 | ขอเกินคงเหลือ → บล็อก + ยอด | VR-04 · BR-02 | TC-REQ-03 | ✓ |
| FN-11 | type ไม่มีสิทธิ์ → บล็อก+เหตุ | VR-05 · BR-01/BR-06 | TC-REQ-04, TC-REQ-05 | ✓ |
| FN-12 | ดูสถานะ + สาย DOA (อ่าน) | BR-DOA-2 | TC-VIEW-01 | ✓ |
| FN-13 | อนุมัติ final → ตัดคงเหลือ + 7C EC + hook | BR-05/BR-09 · BR-DOA-3/4 | TC-APR-01, TC-ADV-01 | ✓ |
| FN-14 | ไม่อนุมัติ → ไม่ตัด + เหตุ + NTF | VR-08 · BR-05 | TC-REJ-01, TC-REJ-02 | ✓ |
| FN-15 | ยกเลิกก่อนอนุมัติ | VR-10 · BR-DOA-7 | TC-CAN-01, TC-CAN-02 | ✓ |
| FN-16 | leaver → revoked · null≠ทำงาน | BR-06 | TC-BAL-03 | ✓ |
| FN-17 | สถานะจ่าย display-only | BR-10 (pay hook) · LK-2 | TC-VIEW-02 | ✓ |
| FN-18 | joiner → สิทธิ์เปิดอัตโนมัติ [STD] | BR-06 | TC-BAL-04 | ✓ |
| FN-19 | รายงานใช้สิทธิ์ + filter | BR-08 | TC-RPT-01, TC-RPT-02 | ✓ |
| FN-90 | ค้นหา/filter + empty state | — (UI) | TC-LIST-01, TC-LIST-02 | ✓ |
| FN-91 | ปิดใช้/ยกเลิก confirm + soft archive | BR-07 · BR-DOA-7/8 | TC-REG-05, TC-CAN-01 | ✓ |
| FN-92 | field validate + กัน double-submit | §5.4 · VR-12 | TC-VAL-01, TC-REG-02, TC-REJ-01 | ✓ |
| FN-93 | audit append-only ทุก transition | BR-07 | TC-AUD-01, TC-REV-01 | ✓ |
| FN-94 | RESTRICTED masking ตาม role | BR-08 · §5.7 D-CLASS | TC-MASK-01/02/03 | ✓ |

**FN↔TC = 24/24 ✅** · ทุก FN มี rule ใน 05_RULES + TC ≥1 · ไม่มี FN ไร้ TC · ไม่มี TC ไร้ FN/rule.

---

## §2 · Governance Rules (BR-DOA) — present in 05_RULES **และ** มี TC

| Rule | ข้อ | 05_RULES | TC | ✓ |
|---|---|---|---|:--:|
| approve pending-only | BR-DOA-1 (FIX-01) | §5.1 BR-DOA ✓ | TC-PERM-03 | ✓ |
| DOA resolve-at-submit + freeze (per-step) | BR-DOA-2 (LK-1) | §5.1 ✓ | TC-DOA-01, TC-VIEW-01 | ✓ |
| one-step advance (ห้าม collapse) | BR-DOA-3 (FIX-03) | §5.1 + §5.2 ✓ | TC-ADV-01 | ✓ |
| quota re-check ณ final approval (atomic) | BR-DOA-4 (FIX-02) | §5.1 ✓ | TC-APR-01, TC-CC-01 | ✓ |
| soft-reserve = NONE (exposure display-only) | BR-DOA-5 (OQ-WEL-03) | §5.1 ✓ | TC-EXP-01, TC-CC-01 | ✓ |
| permission enforce backend | BR-DOA-6 (FIX-04) | §5.1 + §5.3 ✓ | TC-PERM-01/02/04 | ✓ |
| cancel guard (draft/pending only) | BR-DOA-7 (FIX-05) | §5.1 ✓ | TC-CAN-01, TC-CAN-02 | ✓ |
| archive-warn pending | BR-DOA-8 (FIX-06) | §5.1 ✓ | TC-REG-05 | ✓ |
| **reversal append-only** | BR-11 (OQ-WEL-01) | §5.1 + §5.2 + EC-06 ✓ | TC-REV-01..04, TC-XT-03/04 | ✓ |

ทุก governance guard ที่ถามใน task (approve pending-only · DOA per-step · quota re-check · permission · cancel guard · archive-warn · reversal append-only) = **present + มี TC ครบ**.

---

## §3 · Declaration Coverage (Phase 0b) — DOA / NTF / CSQ

| ท่อ | เข้าเงื่อนไข | Brief | Consistency กับ FRD | ✓ |
|---|---|---|---|:--:|
| **DOA** | ✅ มี approval + status pending_approval | `DOA_BRIEF_F-HR-WELFARE.md` | 2-step (หัวหน้า→HR สวัสดิการ) · **no amount tier · no exec path** · resolve+freeze (LK-1) · ตรงกับ 03_LOGIC FN-10/11 + BR-DOA-1..8 · **ไม่ hardcode chain** (role ids = placeholder → OQ-DOA-01 ให้ BA) | ✓ |
| **NTF** | ✅ business events (มอบหมาย/ผล/leaver/reversed) | `NTF_BRIEF_F-HR-WELFARE.md` | **5 events**: submitted · result · quota_near_limit · eligibility_ended · **reversed** ⭐ · ทุก event map กลับ FN (FN-10/11/12/14/18) · **ไม่ประกาศ doa_pending/doa_result** (DOA engine เจ้าของ) · ตรงกับ XT-05 + 03_LOGIC | ✓ |
| **CSQ** | ✅ กระทบมูลค่า/เงินได้ 7C | `CSQ_BRIEF_F-HR-WELFARE.md` | **EC-only** (LK-6) · forward `welfare.granted` + **EC reverse (negative offset)** on reversal · basis=declared · **ไม่มี OC/DC/SC/AC/FC** (กัน register 422) · ตรงกับ BR-09/BR-11 + 03_LOGIC step 5 | ✓ |
| **DOCCFG** | ❌ ไม่ออกเลขรัน/เอกสาร (NS-5) | `NOT_NEEDED.md` | N/A — justified: request_no = internal display id · ไม่มีเอกสารที่คนถือ | N/A |
| **PDFDOC** | ❌ ไม่มีแบบฟอร์มพิมพ์ (step 2 skip) | `NOT_NEEDED.md` | N/A — justified | N/A |

**Declaration = DOA+NTF+CSQ ครบ + consistent (brief ⊆ FRD · FRD sync read brief · ไม่มี hardcoded chain/channel/running-number ใน FRD)** · doccfg/pdfdoc NOT needed ตามที่ task ระบุ ✅

---

## §4 · Scope Lock — 5 unsupported = negative verify (FN-40 equivalent)

| NS | ของที่ห้ามมี | TC (negative · render+assert absent) | ✓ |
|---|---|---|:--:|
| NS-1 | จ่ายเงินจริง/เบิก/หักเงินเดือน (LK-2) | TC-NEG-01 | ✓ |
| NS-2 | จัดการผู้ให้บริการ (รพ./ประกัน) | TC-NEG-02 | ✓ |
| NS-3 | flex credits / แต้ม | TC-NEG-03 | ✓ |
| NS-4 | สร้าง/แก้ค่านโยบาย HR กลาง (LK-3) | TC-NEG-04 | ✓ |
| NS-5 | ออกเอกสารเลขรัน/PDF ทางการ | TC-NEG-05 | ✓ |

**5/5 negative verify ครบ** · reversal/exposure = authorized additions (Decision Log OQ-WEL-01/03) → in-scope · ไม่ขัด NS-1 (append-only correction · no pay action) · **ไม่มี scope creep**.

---

## §5 · Cross-Module (XT) + Lock refs

| XT | Downstream | TC | ✓ |
|---|---|---|:--:|
| XT-01 approve → CSQ EC only | CSQ | TC-XT-01 | ✓ |
| XT-02 approve → Payroll pay=pending display-only | Payroll | TC-XT-02 | ✓ |
| XT-03 reverse → CSQ EC reverse (negative offset) | CSQ | TC-XT-03 | ✓ |
| XT-04 reverse pay=sent → payroll_clawback=true | Payroll | TC-XT-04 | ✓ |
| XT-05 state transitions → 5 NTF events (DOA ไม่ซ้ำ) | Notify | TC-XT-05 | ✓ |

**Lock refs (LK-1..6): 6/6** มีเคส verify (TC-DOA-01/TC-VIEW-02/TC-NEG-04/TC-REQ-01/TC-AUD-01/TC-XT-01) · ข้อความ FRD ไม่ขัด LOCK.

---

## §6 · WARN / Divergence (non-block · ยกให้ BA/Strike)

1. **DIVERGENCE — plan chip ≠ declare (OQ-06):** plan chip F102 dec=[doa,csq] แต่ feature ประกาศ **+ntf**. NTF justified (5 business events = state transition จริง FN-10/11/12/14/18 · ไม่ใช่ DOA event) → ควรอัปเดต chip ที่ plan. **ไม่บล็อก** (documented OQ-06). *(หมายเหตุ: helper `prebrief_checklist.py` ยัง flag `doccfg:true` = keyword false-positive จากคำว่า "เอกสาร" — resolved โดย NOT_NEEDED.md · NS-5.)*
2. **R15 cross-artifact parity — deferred:** MD ledger 60 cases ↔ meta 60 ↔ AT 27/27 = internal consistent. **QA-friendly HTML (step 11) ยังไม่ทำ** → parity MD↔QA HTML ตรวจไม่ได้รอบนี้ (NOT-CHECKED · ไปตรวจตอน step 11).
3. **OQ ปลายทาง blocking (ไม่ใช่ coverage gap):** OQ-03 (Payroll hook contract · Phase B) · OQ-04 (atomic re-check · [AI-DEFAULT]) · OQ-05 (backend permission enforce · [AI-DEFAULT]) · OQ-DOA-01 (role ids จริง 2 ตัว ที่ DOA กลาง · BLOCKER ต่อ wire) — ทุกข้อ documented + ยกให้ BA/Dev แล้ว · TC (TC-CC-01/TC-MASK-01) อิง default ปัจจุบัน (fail = default ผิด).

---

## §7 · Diff จากรอบ 1

- **Gap ที่ปิดแล้ว:** รอบ 1 (HTML) PASS 24/24 · รอบ 2 ยืนยัน spec+TC ผูกครบทุก FN/rule/edge ที่รอบ 1 เห็นบนจอ.
- **ยังค้าง:** 3 WARN §6 (OQ ปลายทาง + R15 QA HTML) — ไม่ใช่ของใหม่ · flag เดิมจากรอบ 1 §"ส่งต่อ step 7".
- **เกิดใหม่:** ไม่มี gap ใหม่ · ไม่มี scope creep ใหม่.

---

## §8 · Quality Gate (ของ checker เอง)

- [x] ทุก ✓ มี evidence (rule id ใน 05_RULES + TC id ใน testcases-welfare.md)
- [x] ไม่ invent เกณฑ์นอก contract (FN/rule/edge จาก PREBRIEF+FUNCTION_CHECKLIST+FRD เท่านั้น)
- [x] item ที่ตรวจไม่ได้ = NOT-CHECKED (R15 QA HTML step 11) ไม่ใช่ ✓
- [x] scope creep flag แล้ว (0 พบ)
- [x] Declaration coverage 0b ตรวจครบ 4 ท่อ (DOA/NTF/CSQ present · DOCCFG N/A justified)
- [x] verdict BLOCK เฉพาะเมื่อ block-severity ไม่ครอบ → **ครอบครบ = PASS**

**สรุป Coverage Audit:** FN 24/24 · AT 27/27 · BR 23/23 · VR 12/12 · XT 5/5 · LK 6/6 · NS negative 5/5 · TC total 60 · **gap block 0**.
