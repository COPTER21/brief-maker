# _COVERAGE_R2_REPORT — F-MKT-CONSENT · ความยินยอม PDPA (F058)

> **Step 10 · qc-coverage · รอบ 2 (FRD Pack + Test Cases vs Contract)** — **RE-RUN 2026-09-14** หลัง BA-gate fixes (FIX-01..08) + FRD v1.1 + testcases re-gen (83 เคส)
> **ไม่ซ้ำรอบ 1** (รอบ 1 = HTML vs PREBRIEF → PASS ที่ `_COVERAGE_REPORT.md`, re-run 2026-09-14)
> รอบนี้ตอบ 2 คำถาม: (ก) FRD v1.1 ครอบทุก FN/BR/story/edge/lock + BA-fix rules ใหม่มั้ย · (ข) ทุก FN/BR/EC/lock/negative + BA-fix มี TC ผูก trace มั้ย
> Artifacts: `FRD_Pack/` (INDEX+00–07 · v1.1) · `testcases-consent-pdpa.md` (83 เคส · G1–G10) · contract = `FUNCTION_CHECKLIST` (20 FN + 10 FN-40) + `PREBRIEF Part C` (locks) + BRD v1.1 manifest §7/§9/§10
> Declaration: plan `dec=["csq"]` · `CSQ_BRIEF_F-MKT-CONSENT.md` ออกแล้ว (step 7)
> ทุก ✓ อ้าง section FRD / TC id จริง (grep -F verify) — ไม่มี "น่าจะมี"

## VERDICT: **PASS** ✅ (มี governance/drift OQ ระดับ WARN — ไม่มี block-severity gap)

- **FRD ครอบ FN 20/20** — ทุก FN map ใน Coverage Manifest §0.12 + 03_LOGIC §3.1/§3.3 + AC (06 §6.1) · FN-21 `snapshotVers` (helper ใหม่ · ไม่อยู่ใน FUNCTION_CHECKLIST) มีใน 03_LOGIC §3.1
- **TC ครอบ FN 20/20** — ทุก FN มี TC ≥1 ที่ trace กลับ S/BR (Coverage Ledger self = 20/20) · FN-21 = TC-FIX-03
- **Business Rules 31/31** ปรากฏใน `05_RULES §5.1` เนื้อหาตรง ไม่มี block rule ถูกเจือจาง · ทุก BR มี TC (BR-01..22 + BR-CSQ-01..05 + **BR-23..26 ใหม่**)
- **BA-fix rules ใหม่ครบ**: BR-23..26 · FN-21 · AT-21..25 · EC-12/13/14 · XT-06/07 — **ทุกตัวมี TC ผูก (G10 TC-FIX-01..11)**
- **FN-40 negatives 10/10** อยู่ครบใน `06_TESTS §6.2` (NEG-40.1…10) + TC (TC-NEG-01…10)
- **Locks 13/13** ใน `07_LOCKED §7.0` + มีเคส verify (Scope Lock ledger 13/13)
- **Cross-module XT 7/7** (`06_TESTS §6.9` — เพิ่ม XT-06 F031 / XT-07 F157) · **EC 14/14** · **Error catalog 14/14**
- ไม่พบ **scope creep** ใน FRD/TC — BA fixes ทั้งหมดเป็น **guard/anchor/idempotency backstop** ไม่ใช่ scope ใหม่
- **DECL-CSQ ↔ FRD**: sync ครบ (03_LOGIC §3.4) · declare-only 7 events · ไม่มี OC/DC/SC · doa/ntf/doccfg ไม่เลือก (ยืนยันใน 07 LD-03)
- Contract anchors **F136/F031/F157 = display-only** (comment) — XT-06/07 ครอบ consumer (data) · ไม่มีจอ feature อื่นถูก mock

---

## Coverage Matrix — FN บวก (รอบ 2 = FRD + TC · HTML = อ้างจากรอบ 1)

| FN | HTML (รอบ1) | FRD | TC | Evidence |
|---|:--:|:--:|:--:|---|
| FN-01 สร้าง purpose + upload v1 | ✓ | ✓ | ✓ | Manifest US-01 · 03_FN-01 · 05 BR-05 · 06 AT-01 · TC-PUR-01/02/03/04/05 |
| FN-02 อัปโหลดเวอร์ชันใหม่ + stale N | ✓ | ✓ | ✓ | 03_FN-02 · 05 BR-05/06 · AT-02 · TC-PUR-07/08 |
| FN-03 ตาราง purpose + สถิติ | ✓ | ✓ | ✓ | 01_UI P-03 · 03_FN-03 · AT-03 · TC-PUR-06 |
| FN-04 ปิด purpose (consent เดิมอยู่) | ✓ | ✓ | ✓ | 05 BR-14 · EC-07 · AT-04 · TC-PUR-09 |
| FN-05 สร้างคำขอ single-screen | ✓ | ✓ | ✓ | 03_FN-05 · LOCK-07 · AT-05 · TC-REQ-01/02/03/04 |
| FN-06 ส่งทางอีเมล (mock) + snapshot vers | ✓ | ✓ | ✓ | 03_FN-06 (guard draft/pending + FN-21) · 05 BR-07/18/24 · AT-06 · TC-REQ-05 |
| FN-07 ส่งซ้ำ = ส่งครั้งที่ N | ✓ | ✓ | ✓ | 05 BR-18 · AT-07 · TC-REQ-06 |
| FN-08 คัดลอกลิงก์ / QR | ✓ | ✓ | ✓ | 03_FN-07 · AT-08 · TC-REQ-07/08 |
| FN-09 ดาวน์โหลดเอกสารคำขอ | ✓ | ✓ | ✓ | 03_FN-07 · AT-09 · TC-REQ-09 |
| FN-10 recipient view + evidence 5 | ✓ | ✓ | ✓ | 03_FN-08/09 · 05 BR-15 · AT-10 · TC-RCP-01/02/05 |
| FN-11 ยินยอมรายวัตถุประสงค์ | ✓ | ✓ | ✓ | 03_FN-09 · EC-06 · AT-11 · TC-RCP-03/04 |
| FN-12 ดูหลักฐาน 5 ฟิลด์ | ✓ | ✓ | ✓ | 03_FN-12 · 05 BR-15 · AT-12 · TC-REG-05 |
| FN-13 ทะเบียน + กรองทุกมิติ | ✓ | ✓ | ✓ | 03_FN-11 · AT-13 · TC-REG-01/02/03 |
| FN-14 Customer 360 | ✓ | ✓ | ✓ | AT-14 · TC-REG-07 (label "ดูรายคน") · XT-06 |
| FN-15 ถอนแทนลูกค้า (ทันที) | ✓ | ✓ | ✓ | 03_FN-13 (granted-only guard) · 05 BR-09/10 · LOCK-04 · AT-15 · TC-REG-08/09/10 |
| FN-16 ใกล้หมดอายุ ≤30 วัน | ✓ | ✓ | ✓ | 03_FN-18 · 05 BR-12 · AT-16 · TC-REG-04 |
| FN-17 ต่ออายุ = คำขอใหม่อ้างเดิม | ✓ | ✓ | ✓ | 03_FN-14 · 05 BR-13 · AT-17 · TC-REG-11 |
| FN-18 ประวัติ append-only | ✓ | ✓ | ✓ | 03_FN-12 · 05 BR-16 · AT-18 · TC-REG-06 |
| FN-19 resolve simulator | ✓ | ✓ | ✓ | 03_ENG-01/FN-20 · 05 BR-19/20 · AT-19 · TC-RES-01/03/04/05/06/07 |
| FN-20 never_asked (ไม่ 404/declined) | ✓ | ✓ | ✓ | 03_ENG-01 · EC-01 · 05 BR-04/08/19 · AT-20 · TC-RES-02/08 |
| FN-21 `snapshotVers` (helper · FIX-03) | ✓ | ✓ | ✓ | 03_FN-21 · 05 BR-24 · AT-22 · **TC-FIX-03** — ไม่อยู่ใน FUNCTION_CHECKLIST (ไม่นับในตัวหาร 20) |

**FRD FN 20/20 · TC FN 20/20 · +FN-21 helper covered · ไม่มี FN ไร้ TC · ไม่มี BR block ถูกเจือจาง**

### BA-gate fix rules (ใหม่รอบนี้) — FRD ↔ TC

| item | FRD | TC | Evidence |
|---|:--:|:--:|---|
| **BR-23** [FIX-01] answered=terminal · re-answer blocked · evidence immutable | ✓ | ✓ | 05 §5.1/§5.2 · 03_FN-09 guard order · EC-12 · AT-21 · **TC-FIX-01/02** |
| **BR-24** [FIX-03] send snapshot เวอร์ชันต่อ purpose (`vers`) | ✓ | ✓ | 05 §5.1 · 03_FN-06/FN-21 · AT-22 · **TC-FIX-03** |
| **BR-25** [FIX-02] role check ใน mutation function (auditor read-only) | ✓ | ✓ | 05 §5.1/§5.3 · 03_FN §3.1 guard note · EC-14 · AT-23/23c · **TC-FIX-04/05** |
| **BR-26** [FIX-04/05] double-submit `_busy` + sub-status guard | ✓ | ✓ | 05 §5.1/§5.4/§5.5 EC-13 · 03 guardBusy · AT-24/25 · **TC-FIX-06/07/08** |
| AT-21..25 (BA-fix acceptance) | ✓ | ✓ | 06 §6.1 ครบ 5 (grep verify) · map TC-FIX-01..08 |
| EC-12 re-answer/terminal | ✓ | ✓ | 05 §5.5 · TC-FIX-01/02 |
| EC-13 double-submit + sub-status | ✓ | ✓ | 05 §5.5 · TC-FIX-06/07/08 |
| EC-14 role bypass (auditor direct) | ✓ | ✓ | 05 §5.5 · TC-FIX-04 |
| XT-06 F031 Customer 360 (data) | ✓ | ✓ | 06 §6.9 · TC-REG-07 + TC-FIX-09 (anchor) |
| XT-07 F157 DSAR (data · evidence 5 + history) | ✓ | ✓ | 06 §6.9 · TC-REG-05/06 + TC-FIX-09 (anchor) |
| FIX-06 contract anchors display-only | ✓ | ✓ | 00 §0.5 · TC-FIX-09 |
| FIX-07 demo-only strip · FIX-08 one-pill/cell | ✓ | ✓ | 01_UI · TC-FIX-10 / TC-FIX-11 |

### FN-40 Negatives — FRD 10/10 · TC 10/10 (ไม่มี scope creep)

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
| **CSQ** | ✅ | ✓ `CSQ_BRIEF` (step 7) | ✓ 03_LOGIC §3.4 · event ⊆ brief (7 events) · declare-only ไม่มี OC/DC/SC · TC-XT-04/NEG-06 | **✓ PASS** |
| DOA | ❌ | — | 07 LD-03 "doa ไม่เลือก" · 00 §0.4 "ไม่มี approval chain" | **N/A** (DIVERGENCE — script `doa:true` = false-positive จากคำ "อนุมัติ" ในประโยคปฏิเสธ BR-09 / LOCK-04; Strike ยืนยัน N/A · C3.9) |
| NTF | ❌ | — | 06 §6.5 "N/A ไม่มี WS/realtime event" | **N/A** |
| DOCCFG | ❌ | — | 07 LD-03 "ไม่ใช่เอกสารธุรกรรม/ไม่มีเลขรัน" | **N/A** — REQ/CNS = internal id ไม่ hardcode รูปแบบเลข |

---

## FRD Completeness (รอบ 2 หลัก)

| ตรวจ | ผล | Evidence |
|---|:--:|---|
| ทุก block rule ปรากฏใน 05_RULES เนื้อหาตรง ไม่เจือจาง | ✓ | BR-01…22 + BR-CSQ-01…05 + BR-23…26 ครบใน §5.1 (26 non-CSQ + 5 CSQ = 31 · grep verify) · BR-04/14/19/03/23 ยัง FIXED |
| N/A-UI จากรอบ 1 ถูกเก็บใน FRD | ✓ | BR-21 caller cache → 02_API §2.X + §5.5 EC-02 + OQ-02 · BR-22 F143 → §0.5 + OQ-04 |
| Edges/cross-module มี hook ใน API/LOGIC | ✓ | XT-01…07 (06 §6.9 · +XT-06/07) · resolve contract LD-02 · CSQ outbox 03 §3.4 |
| BA-fix rules encode ถูกใน state machine | ✓ | 03_LOGIC §3.5 request lifecycle (answered=terminal) · 05 §5.2 · guard order 03_FN-09/13 |
| Lock refs ไม่ถูกเขียนขัด | ✓ | 07_LOCKED §7.0 ทั้ง 13 lock สอดคล้อง · ไม่มี spec ขัด |
| Coverage Manifest ไม่มีแถว "อยู่ที่" ว่าง | ✓ | §0.12 self = Stories 20/20 · Rules 22+CSQ+BR-23..26 · Edges 5/5 + EC-12/13 |
| Standard gap (02_STANDARD_GAP) | N/A | pack นี้ไม่มีไฟล์ 02_STANDARD_GAP (standalone lane) |

---

## Diff กับ R2 ก่อนหน้า (2026-09-13)

- **ปิดแล้ว (resolved)**: **OQ-C (TC count drift)** — เดิม Meta 68 vs หัวข้อจริง 72 · ตอนนี้ Meta = **83** ตรงกับ `### TC-` จริง = **83** (grep verify · reconcile แล้ว) → ไม่ค้างอีก
- **เพิ่มใหม่และครอบครบ**: BR-23..26 (4 rule) · FN-21 · AT-21..25 · EC-12/13/14 · XT-06/07 · G10 TC-FIX-01..11 (11 เคส) — ทุกตัวมี FRD + TC (ไม่มีตัวไหน orphan)
- **BR total: 27 → 31** (เพิ่ม BR-23..26) · **XT: 5 → 7** · **EC: 11 → 14** · **TC: 72 → 83**
- **ยังค้าง (carry · WARN ไม่บล็อก)**: OQ-A DECLARED-01 · OQ-B microcopy drift · OQ-01/03/04 · **OQ-CNS-01/02/03 (ใหม่จาก BA-gate)**

---

## 🟡 WARN / Governance OQ (ไม่บล็อก — ส่งให้ BA/QA)

### OQ-A · DECLARED-01 — โมเดลเนื้อหา = เอกสารอัปโหลด (versioned) vs PREBRIEF free-text
- FRD ยึดโมเดล **upload** (07 LD-01 · BR-05/06 tag DECLARED-01 · OQ-01) — มติ PM/BA 2026-09-11 บันทึกแล้ว
- ขัด PREBRIEF **BR-05/06 + S-01/02/09 + FN-01/02/09/10/11** (เดิม "แก้ข้อความ/พิมพ์ข้อความ")
- **สถานะ: divergence ที่ประกาศ — ไม่นับตก** · **แก้ที่**: BA อัปเดต `PREBRIEF_F-MKT-CONSENT.md` (owner: BA · OQ-01)

### OQ-B · Microcopy drift FRD ↔ HTML (HTML ชนะ · TC anchor ยึด HTML ถูกแล้ว)
Drift ถ้อยคำ (ความหมายตรง · coverage ไม่กระทบ) — testcases §Drift note ระบุไว้แล้ว:
1. resolve เลือกไม่ครบ: HTML = **"…ก่อนตรวจสิทธิ์"** · FRD 05 §5.4 / 06 = "…ก่อนตรวจสอบ"
2. สร้างคำขอ purpose ไม่รองรับ: HTML = **"เลือกวัตถุประสงค์ที่รองรับช่องทางนี้อย่างน้อย 1 ข้อ"** · 05 เขียนย่อ
3. Customer 360: ปุ่มจอ = **"ดูรายคน"** · 01_UI เรียก "Customer 360"/D-c360
- **แก้ที่**: sync `05_RULES §5.4` + `06_TESTS §6.10` + `01_UI` ให้ตรง HTML verbatim (owner: BA — ไม่กระทบ verdict)

### OQ-CNS-01/02/03 · ประเด็นใหม่จาก BA-gate (Strike เคาะ · build เลือก conservative)
- **OQ-CNS-01**: เปลี่ยนใจ **หลังตอบคำขอ** — build = answered=terminal (FIX-01/BR-23) · เส้นทางถูก = คำขอใหม่/withdraw · ใครเปิดคำขอใหม่ได้ → 03_LOGIC §3.5 state machine
- **OQ-CNS-02**: publish เวอร์ชันใหม่ระหว่างคำขอ pending — build = **ไม่ auto-expire** (แสดง sent-version + เตือน · FIX-03/BR-24)
- **OQ-CNS-03**: รอบต่ออายุ — ใคร/อะไร trigger (manual จาก registry vs batch · NTF ฝั่ง F136)
- **สถานะ**: build เลือก conservative default แขวนรอมติ · **ห้าม dev เดา** — ยกเป็น OQ (owner: Strike/BA) · ไม่ใช่ coverage gap

---

## ⬜ NOT-CHECKED / ตรวจไม่ได้ในด่านนี้ (ตามธรรมชาติ gate)
- **BR-21/22 · XT-03/04/05 · EC-04/10/11** = `(ต้อง simulate)` — มี TC ใน ledger แต่รันด้วยมือไม่ได้ (caller cache / F143 / API idempotency / optimistic lock / timezone) → coverage นับ "มีเคส" ✓ · ผลรันจริงเป็นเรื่อง dev/integration
- **OQ-03 (id-verify จริง) · OQ-04 (F143 register)** = FRD tag **BLOCKING ก่อน implement/go-live** — open decision ที่ประกาศถูกต้อง (มี TC-RCP-02 mock + TC-XT-05) → **ไม่ใช่ coverage gap ของด่านนี้** แต่ dev/Security ต้องเคลียร์ก่อน go-live

---

## สรุปตัวเลข (นับจริง · grep -F)

| หมวด | FRD | TC |
|---|:--:|:--:|
| FN บวก | 20/20 | 20/20 (+FN-21 helper) |
| FN-40 negatives | 10/10 | 10/10 |
| Business rules (BR-01..22 + CSQ-01..05 + BR-23..26) | **31/31** | 31/31 (BR-21/22 = simulate) |
| Edge cases EC-01…14 | 14/14 | 14/14 (3 simulate · EC-09 partial) |
| Error catalog | 14/14 | 14/14 (เพิ่ม BR_REQUEST_CLOSED · BR_NOT_GRANTED) |
| Locks (Scope Lock) | 13/13 | 13/13 |
| Cross-module XT | 7/7 | 7/7 (เพิ่ม XT-06/07) |
| **Declarations** | CSQ ✓ · DOA/NTF/DOCCFG = N/A (ยืนยัน LD-03) | — |
| **Scope creep** | 0 | 0 |
| **TC ทั้งหมด (นับหัวข้อจริง)** | — | **83** (Meta = 83 · ตรงกันแล้ว · G10 TC-FIX-01..11) |

---
*qc-coverage-checker · รอบ 2 (FRD v1.1 + TC 83) · RE-RUN 2026-09-14 · ทุก ✓ อ้าง section/TC จริง (grep -F) · ไม่แก้ HTML/FRD/TC/skills · ไม่ commit · ไม่รัน declaration*
