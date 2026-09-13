# _COVERAGE_R2_REPORT — F-MKT-CONSENT · ความยินยอม PDPA (F058)

> **Step 10 · qc-coverage · รอบ 2 (FRD Pack + Test Cases vs Contract)** — 2026-09-13
> **ไม่ซ้ำรอบ 1** (รอบ 1 = HTML vs PREBRIEF → PASS ที่ `_COVERAGE_REPORT.md` 2026-09-11)
> รอบนี้ตอบ 2 คำถาม: (ก) FRD ครอบทุก FN/BR/story/edge/lock มั้ย · (ข) ทุก FN/BR/EC/lock/negative มี TC ผูก trace มั้ย
> Artifacts: `FRD_Pack/` (INDEX+00–07) · `testcases-consent-pdpa.md` · contract = `FUNCTION_CHECKLIST` (20 FN + 10 FN-40) + `PREBRIEF Part C` (13 locks) + BRD manifest §7/§9/§10
> Declaration: plan `dec=["csq"]` · `CSQ_BRIEF_F-MKT-CONSENT.md` ออกแล้ว (step 7)
> ทุก ✓ อ้าง section FRD / TC id จริง — ไม่มี "น่าจะมี"

## VERDICT: **PASS** ✅ (มี 3 governance/drift OQ ระดับ WARN — ไม่บล็อก)

- **FRD ครอบ FN 20/20** — ทุก FN map ใน Coverage Manifest §0.12 + 03_LOGIC + AC (06 §6.1)
- **TC ครอบ FN 20/20** — ทุก FN มี TC ≥1 ที่ trace กลับ S/BR (Coverage Ledger + Audit self = 20/20)
- **Business Rules 27/27** ปรากฏใน `05_RULES §5.1` เนื้อหาตรง ไม่มี block rule ถูกเจือจาง · ทุก BR มี TC
- **FN-40 negatives 10/10** อยู่ครบใน `06_TESTS §6.2` (NEG-40.1…10) + มี TC (TC-NEG-01…10)
- **Locks 13/13** ใน `07_LOCKED §7.0` + มีเคส verify (Scope Lock ledger 13/13)
- **Edges/XT 5/5** (`06_TESTS §6.9` + TC-XT-01…05) · **EC 11/11** · **Error catalog 12/12**
- ไม่พบ **scope creep** ใน FRD/TC · **DECLARED-01** (เอกสารอัปโหลด vs free-text) = divergence ที่ประกาศ = governance OQ ไม่ใช่ coverage fail
- **DECL-CSQ ↔ FRD**: sync ครบ (03_LOGIC §3.4 + LD-05) · declare-only ไม่มี OC/DC/SC · doa/ntf/doccfg ไม่เลือก (ยืนยันใน LD-03)

---

## Coverage Matrix (รอบ 2 = FRD + TC · HTML = อ้างจากรอบ 1)

| FN | HTML (รอบ1) | FRD | TC | Evidence |
|---|:--:|:--:|:--:|---|
| FN-01 สร้าง purpose + upload v1 | ✓ | ✓ | ✓ | Manifest US-01 · 05 BR-05 · 06 AT-01 · TC-PUR-01/02/03/04/05 |
| FN-02 อัปโหลดเวอร์ชันใหม่ + stale N | ✓ | ✓ | ✓ | 03_FN-02 · 05 BR-05/06 · AT-02 · TC-PUR-07/08 |
| FN-03 ตาราง purpose + สถิติ | ✓ | ✓ | ✓ | 01_UI P-03 · AT-03 · TC-PUR-06 |
| FN-04 ปิด purpose (consent เดิมอยู่) | ✓ | ✓ | ✓ | 05 BR-14 · EC-07 · AT-04 · TC-PUR-09 |
| FN-05 สร้างคำขอ single-screen | ✓ | ✓ | ✓ | LOCK-07 · AT-05 · TC-REQ-01/02/03/04 |
| FN-06 ส่งทางอีเมล (mock) | ✓ | ✓ | ✓ | 05 BR-07 · AT-06 · TC-REQ-05 |
| FN-07 ส่งซ้ำ = ส่งครั้งที่ N | ✓ | ✓ | ✓ | 05 BR-18 · AT-07 · TC-REQ-06 |
| FN-08 คัดลอกลิงก์ / QR | ✓ | ✓ | ✓ | AT-08 · TC-REQ-07/08 |
| FN-09 ดาวน์โหลดเอกสารคำขอ | ✓ | ✓ | ✓ | AT-09 · TC-REQ-09 |
| FN-10 recipient view + evidence 5 | ✓ | ✓ | ✓ | 05 BR-15 · AT-10 · TC-RCP-01/02/05 |
| FN-11 ยินยอมรายวัตถุประสงค์ | ✓ | ✓ | ✓ | EC-06 · AT-11 · TC-RCP-03/04 |
| FN-12 ดูหลักฐาน 5 ฟิลด์ | ✓ | ✓ | ✓ | 05 BR-15 · AT-12 · TC-REG-05 |
| FN-13 ทะเบียน + กรองทุกมิติ | ✓ | ✓ | ✓ | AT-13 · TC-REG-01/02/03 |
| FN-14 Customer 360 | ✓ | ✓ | ✓ | AT-14 · TC-REG-07 (label "ดูรายคน") |
| FN-15 ถอนแทนลูกค้า (ทันที) | ✓ | ✓ | ✓ | 05 BR-09/10 · LOCK-04 · AT-15 · TC-REG-08/09/10 |
| FN-16 ใกล้หมดอายุ ≤30 วัน | ✓ | ✓ | ✓ | 05 BR-12 · AT-16 · TC-REG-04 |
| FN-17 ต่ออายุ = คำขอใหม่อ้างเดิม | ✓ | ✓ | ✓ | 05 BR-13 · AT-17 · TC-REG-11 |
| FN-18 ประวัติ append-only | ✓ | ✓ | ✓ | 05 BR-16 · AT-18 · TC-REG-06 |
| FN-19 resolve simulator | ✓ | ✓ | ✓ | ENG-01 · 05 BR-19/20 · AT-19 · TC-RES-01/03/04/05/06/07 |
| FN-20 never_asked (ไม่ 404/declined) | ✓ | ✓ | ✓ | EC-01 · 05 BR-04/08/19 · AT-20 · TC-RES-02/08 |

**FRD FN 20/20 · TC FN 20/20 · ไม่มี FN ไร้ TC · ไม่มี BR block ถูกเจือจาง**

### FN-40 Negatives — FRD 10/10 · TC 10/10

| # | FRD (06 §6.2) | TC | หมายเหตุ |
|---|:--:|:--:|---|
| 40.1 cookie consent | ✓ NEG-40.1 | ✓ TC-NEG-01 | LOCK-05 |
| 40.2 สายอนุมัติก่อนส่ง | ✓ NEG-40.2 | ✓ TC-NEG-02 | LOCK-04 |
| 40.3 ส่งอีเมล/LINE จริง | ✓ NEG-40.3 | ✓ TC-NEG-03 | mock toast |
| 40.4 คำนวณมูลค่า/คอลัมน์ผลท่อ | ✓ NEG-40.4 | ✓ TC-NEG-04 | LOCK-CSQ-04/05 |
| 40.5 การ์ดผล 7 ท่อ | ✓ NEG-40.5 | ✓ TC-NEG-05 | LOCK-CSQ-06 |
| 40.6 ประกาศ OC/DC/SC | ✓ NEG-40.6 | ✓ TC-NEG-06/XT-04 | LOCK-CSQ-01/02/03 |
| 40.7 ธง opt-out เดียว | ✓ NEG-40.7 | ✓ TC-NEG-07 | triple partial-unique |
| 40.8 ไม่ตอบ=ไม่ยินยอม | ✓ NEG-40.8 | ✓ TC-NEG-08/RES-08 | lapsed≠declined |
| 40.9 บล็อกการส่งเอง | ✓ NEG-40.9 | ✓ TC-NEG-09 | resolve read-only |
| 40.10 wizard 5 ขั้น | ✓ NEG-40.10 | ✓ TC-NEG-10/REQ-01 | LOCK-07 single-screen |

### Declaration ↔ FRD (Phase 0b · รอบ 2)

| ท่อ | เข้าเงื่อนไข | brief | sync ใน FRD | ผล |
|---|:--:|:--:|:--:|:--:|
| **CSQ** | ✅ | ✓ `CSQ_BRIEF` (step 7) | ✓ 03_LOGIC §3.4 + LD-05 · event ⊆ brief (7 events) · ไม่มี OC/DC/SC · TC-XT-04 | **✓ PASS** |
| DOA | ❌ | — | LD-03 ระบุ "doa ไม่เลือก" | **N/A** — script `doa:true` = false positive (keyword "อนุมัติ" โดนประโยคปฏิเสธ BR-09; C3.9) |
| NTF | ❌ | — | 06 §6.5 "N/A ไม่มี WS/realtime event" | **N/A** |
| DOCCFG | ❌ | — | LD-03 "ไม่ใช่เอกสารธุรกรรม/ไม่มีเลขรัน" | **N/A** — REQ/CNS = internal id ไม่ hardcode รูปแบบเลข |

---

## FRD Completeness (รอบ 2 หลัก)

| ตรวจ | ผล | Evidence |
|---|:--:|---|
| ทุก block rule ปรากฏใน 05_RULES เนื้อหาตรง ไม่เจือจาง | ✓ | BR-01…22 + BR-CSQ-01…05 ครบใน §5.1 · BR-04/14/19/03 ยัง FIXED (ไม่ลดเป็น warn) |
| N/A-UI จากรอบ 1 ถูกเก็บใน FRD | ✓ | BR-21 caller cache → 02_API §2.X + §5.5 EC-02 + OQ-02 · BR-22 F143 → §0.5 + OQ-04 |
| Edges/cross-module มี hook ใน API/LOGIC | ✓ | XT-01…05 (06 §6.9) · resolve contract LD-02 · CSQ outbox 03 §3.4 |
| Lock refs ไม่ถูกเขียนขัด | ✓ | 07_LOCKED §7.0 ทั้ง 13 lock = "สอดคล้อง" · ไม่มี spec ขัด |
| Coverage Manifest ไม่มีแถว "อยู่ที่" ว่าง | ✓ | §0.12 self = Stories 20/20 · Rules 22+CSQ · Edges 5/5 |
| Standard gap (02_STANDARD_GAP) | N/A | pack นี้ไม่มีไฟล์ 02_STANDARD_GAP (standalone lane · ไม่ merge จาก standard) |

---

## Diff กับรอบ 1 (2026-09-11)

- **ปิดแล้ว**: (1) CSQ_BRIEF ออกแล้ว step 7 → DECL-CSQ ครบ · (2) FRD 05_RULES/03_LOGIC + FN↔TC ledger = เดิมเป็น NOT-CHECKED → ตรวจแล้วครบ · (3) BR-21/BR-22 N/A-UI carry → เก็บใน FRD + OQ ครบ
- **ยังค้าง (carry)**: OQ-01 (BA sync PREBRIEF โมเดลอัปโหลด) · OQ-03 (วิธี id-verify จริง) · OQ-04 (F143 register) — ทั้งหมดเป็น OQ ที่ประกาศไว้ ไม่ใช่ coverage gap
- **เกิดใหม่ (รอบ 2)**: 3 drift ระดับ WARN ด้านล่าง (microcopy FRD↔HTML · count TC ในเอกสาร)

---

## 🟡 WARN / Governance OQ (ไม่บล็อก — ส่งให้ BA/QA sync ก่อน/หลัง handoff)

### OQ-A · DECLARED-01 — โมเดลเนื้อหา = เอกสารอัปโหลด (versioned) vs PREBRIEF free-text
- FRD ยึดโมเดล **upload** (LD-01 · BR-05/06 tag DECLARED-01 · OQ-01) — เป็นมติ PM/BA 2026-09-11 ที่บันทึกไว้แล้ว
- ขัด PREBRIEF **BR-05/06 + S-01/02/09 + FN-01/02/09/10/11** (เดิม "แก้ข้อความ/พิมพ์ข้อความ")
- **สถานะ: divergence ที่ประกาศ — ไม่นับตก** (ตามคำสั่งงาน + LD-01 governance)
- **แก้ที่**: BA อัปเดต `PREBRIEF_F-MKT-CONSENT.md` BR-05/06 + S-01/02/09 + FN ให้ตรงโมเดลอัปโหลด (owner: BA · OQ-01)

### OQ-B · Microcopy drift FRD ↔ HTML (HTML ชนะ · TC anchor ถูกต้องแล้ว)
ยืนยันด้วย grep -F ทั้งสองฝั่ง — เป็น drift ถ้อยคำ (ความหมายตรง · coverage ไม่กระทบ · TC ยึด HTML verbatim ถูกแล้ว):
1. resolve เลือกไม่ครบ: HTML = **"…ก่อนตรวจสิทธิ์"** · FRD 05_RULES §5.4 / 06_TESTS = "…ก่อนตรวจสอบ"
2. สร้างคำขอ purpose ไม่รองรับ: HTML = **"เลือกวัตถุประสงค์ที่รองรับช่องทางนี้อย่างน้อย 1 ข้อ"** · 05_RULES เขียนย่อ
3. Customer 360: ปุ่มจอ = **"ดูรายคน"** · 01_UI เรียก "Customer 360"/D-c360
- **แก้ที่**: sync ข้อความใน `FRD_Pack/05_RULES.md` §5.4 + `06_TESTS.md` §6.10 + `01_UI.md` ให้ตรง HTML verbatim (owner: BA — ไม่กระทบ verdict)

### OQ-C · จำนวน TC ในเอกสารไม่ตรงกันเอง (R15 ledger drift)
- `testcases-consent-pdpa.md` Meta = **"68 เคส · 10 group"** และ Result Report schema `total:68` · แต่หัวข้อ `### TC-` จริง = **72 เคส** (Coverage table ก็รวมได้ 72; groups จริง = 9 G-block / 10 TC-prefix)
- เคส**มากกว่า**ที่ประกาศ (ไม่ใช่ขาด) → ไม่ลด coverage · แต่ตัวเลขสรุปค้างเก่า
- **แก้ที่**: อัปเดต Meta "จำนวนเคส" + Result Report `summary.total` เป็น 72 (หรือระบุนิยาม "68 = executable-by-hand, 4 UX เสริม") · owner: QA/BA

---

## ⬜ NOT-CHECKED / ตรวจไม่ได้ในด่านนี้ (ตามธรรมชาติ gate)
- **BR-21/22 · XT-03/04/05 · EC-04/10/11** = `(ต้อง simulate)` — มี TC ใน ledger แต่รันด้วยมือไม่ได้ (caller cache / F143 / API idempotency / optimistic lock / timezone) → coverage นับ "มีเคส" ✓ · ผลรันจริงเป็นเรื่อง dev/integration
- **OQ-03 (id-verify จริง) · OQ-04 (F143 register)** = FRD tag **BLOCKING ก่อน implement/go-live** — เป็น open decision ที่ประกาศถูกต้อง (มี TC-RCP-02 mock + TC-XT-05) → **ไม่ใช่ coverage gap ของด่านนี้** แต่ dev ต้องเคลียร์ก่อน go-live

---

## สรุปตัวเลข (นับจริง · grep -F)

| หมวด | FRD | TC |
|---|:--:|:--:|
| FN บวก | 20/20 | 20/20 |
| FN-40 negatives | 10/10 | 10/10 |
| Business rules (BR-01…22 + CSQ-01…05) | 27/27 | 27/27 (BR-21/22 = simulate) |
| Edge cases EC-01…11 | 11/11 | 11/11 (3 simulate · EC-09 partial) |
| Error catalog | 12/12 | 12/12 |
| Locks (Scope Lock) | 13/13 | 13/13 |
| Cross-module XT | 5/5 | 5/5 |
| **Declarations** | CSQ ✓ · DOA/NTF/DOCCFG = N/A (ยืนยัน LD-03) | — |
| **Scope creep** | 0 | 0 |
| **TC ทั้งหมด (นับหัวข้อจริง)** | — | **72** (เอกสารระบุ 68 → OQ-C) |

---
*qc-coverage-checker · รอบ 2 (FRD + TC) · 2026-09-13 · ทุก ✓ อ้าง section/TC จริง · ไม่แก้ HTML/FRD/TC/skills · ไม่ commit · ไม่รัน declaration*
