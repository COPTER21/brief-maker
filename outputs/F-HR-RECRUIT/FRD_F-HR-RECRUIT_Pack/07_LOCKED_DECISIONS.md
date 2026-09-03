# 07_LOCKED_DECISIONS — F-HR-RECRUIT (F127) สรรหา / Recruit

> **Audience:** All roles
> **Purpose:** Scope Lock (immutable) + Locked Decisions + Convention deviations
> **Variant:** FULL — Scope Lock อยู่ที่ §7.0 (ไม่ใช่ 00_OVERVIEW §0.11)

---

## §7.0 Scope Lock (Imported from BRD §3.4) ⭐ — IMMUTABLE

> ข้อยืนยันจาก LANE_BRIEF + current-state — **ห้าม override** ตลอด pack และ chain ปลายน้ำ (HTML/Test/Dev). spec ใดขัด LOCK → LOCK ชนะ.

| LOCK-ID | ข้อยืนยัน | อ้างเอกสาร | สถานะใน FRD |
|---|---|---|---|
| LOCK-OB1 | ผู้สมัครที่รับ → ส่ง On/Offboard (handoff) · **ไม่ทำ onboarding เอง / ไม่สร้าง employee** | F-HR-ONBOARD S-10, BR-05 | ✅ สอดคล้อง — F127-FN-19 emit event only (02_API §2.X · 06 XT-01) |
| LOCK-OB2 | PDPA: consent + retention ผู้สมัคร (CSQ SecC) | S-05, BR-02, BR-06 | ✅ — consent gate (BR-02) + retention display-only (04_DB §4.7 · OQ-16) |
| LOCK-OB3 | offer/req อนุมัติ = DOA (slot picker 2026-08-17) · **ไม่ hardcode สายอนุมัติ** | current-state §3 | ✅ — F127-FN-26 resolveDoaChain (VR-04 · Policy Center runtime) |
| LOCK-OB4 | เปิดอัตราอ้าง Manpower = hook · null = ไม่บังคับ | A-REC-01 | ✅ — manpower_ref nullable + warn (BR-08 · AT-02) |
| LOCK-OB5 | ข้อมูลผู้สมัคร RESTRICTED · audit append-only | current-state §3 · BR-06,07 | ✅ — 04_DB §4.6 Restricted + T_recruit_audit append-only |
| LOCK-DOA | DOA offer/req **ไม่ผูก threshold ยอดเงิน** — resolve ตามตำแหน่ง (slot) | PREBRIEF §12 | ✅ — slot-based, ไม่มี money threshold ในโค้ด feature |
| LOCK-DOCCFG | ไม่มีเลขรันเอกสาร (offer letter = soft-ref) | PREBRIEF §12 | ✅ — requisition.code ≠ เลขรันเอกสาร · ไม่มี doccfg/pdfdoc |

**unsupported[] scope lock (5 · จาก FUNCTION_CHECKLIST — R11):**
1. จ้างจริง/สร้าง employee/สัญญาจ้าง — ✅ ไม่มีใน FRD (LOCK-OB1)
2. job board ภายนอก — ✅ ไม่มี (announce = internal เท่านั้น)
3. assessment/sourcing agency — ✅ ไม่มี (มีแค่ scorecard = FN-09)
4. offer letter PDF เลขรัน — ✅ ไม่มี (soft-ref · LOCK-DOCCFG)
5. สร้าง/แก้ band เงินเดือน — ✅ ไม่มี (band อ่านอย่างเดียว · resolveBand read)

- **Scope Lock Ref:** LANE_BRIEF F-HR-RECRUIT (Phase A · 2026-08-31) + current-state §3 (DOA slot picker 2026-08-17)
- **Drift พบระหว่างเขียน FRD (ชั้นที่ 3):** ไม่มี SCOPE DRIFT — ทุก In Scope อยู่ใต้ LOCK

---

## §7.1 Locked Decisions (LD)

### LD-01: Hire route เดียว (candHireHandoff) — ห้าม skip board → hired
- **Date:** 2026-09-03 (จาก REVIEW_FIX_ORDER FIX-01)
- **Context:** board move-stage อาจข้ามไป hired โดยไม่ผ่าน offer accepted
- **Decision:** hired เข้าได้ทาง F127-API-22 hire เท่านั้น (offer.status=accepted) · move-stage→hired = บล็อก (BR_HIRE_ROUTE_ONLY)
- **Implications:** 03_LOGIC FN-12 guard · FN-19 route เดียว · 06 AT-16
- **Reversibility:** LOW (คุมความถูกต้องของ pipeline)

### LD-02: ENG-RCT-01/02 register CUBIC ที่ dev hand-off (ไม่รอบนี้)
- **Context:** funnel-engine + duplicate-matcher มี reuse potential (HR Dashboard / rehire)
- **Decision:** build scope-local ก่อน (status DRAFT) · register Phase 2 เมื่อ 2nd consumer ยืนยัน
- **Implications:** 03_LOGIC §3.2 status=DRAFT
- **Reversibility:** EASY

### LD-03: band/DOA/employee = external read wrapper (ไม่ own engine/entity)
- **Context:** Salary Structure (band) · Policy Center (DOA) · Employee Master = feature อื่น
- **Decision:** เรียกผ่าน integration function (FN-25 resolveBand · FN-26 resolveDoaChain · EXT-EMP snapshot) — **read-only · freeze/snapshot ที่ caller** · ไม่ CRUD
- **Implications:** ไม่แตะ schema feature อื่น (Scope Lock) · offer ยึด freeze snapshot (BR-09)
- **Reversibility:** LOW

### LD-04: manpower_ref = hook nullable (F124 ยังไม่ dev)
- **Decision:** display-only, null = ไม่บังคับ + warn — [AI-DEFAULT ที่ตัดสินแล้ว] ตรงสถานะ F124 · A-REC-01
- **Reversibility:** EASY (bind เมื่อ F124 พร้อม)

### LD-05: retention_until = display-only จาก Policy Center (ห้าม hardcode)
- **Context:** FIX-03 ลบ copy "ไม่มีวันหมดอายุ"
- **Decision:** retention period อ่านจาก Policy Center config runtime · retention/withdraw job = Phase 4 หลัง OQ-16 · **ไม่ใส่ค่า default ในโค้ด/DB**
- **Reversibility:** N/A (รอ OQ-16)

---

## §7.2 Convention Deviations

### CD-01: state-change actions ใช้ POST custom action (ไม่ PATCH)
- **Convention default:** PATCH partial update
- **Deviation:** POST `/submit-approval` `/approve` `/announce` `/close` `/hire` `/move-stage` `/terminate`
- **Reason:** semantic clarity — เป็น action ไม่ใช่ property update
- **Approved by:** BA (2026-09-03)

### CD-02: Feature ID prefix = F127 (แทน F-XX ยาว)
- **Deviation:** ใช้ `F127-API-NN` / `F127-FN-NN` เป็น scope-local ID (feature code F127)
- **Reason:** อ่านง่าย + traceable กับ BRD/Cube_Feature_List · Feature ชื่อเต็ม = F-HR-RECRUIT
- **Global Engine ID:** ENG-RCT-01/02 assigned at CUBIC Registry registration (LD-02)

---

## §7.3 Open Questions Promoted from 00_OVERVIEW

> ยังไม่ resolve — ค้างที่ 00_OVERVIEW §0.8:
- **OQ-15** inbound handoff On/Offboard (Strike · FRD กัน scope ไว้ · fire-and-forget เท่านั้น)
- **OQ-16** PDPA retention period + withdraw consent (Strike/พี่เบิร์ด · Policy Center · Phase 4)
- **OQ-17** req closed ขณะ pipeline ค้าง (BA/HR · conservative default EC-08)
- **OQ-R1** Restricted Resources per-person ACL wiring (Security · รอบนี้ role masking)
- **OQ-D1..D4** `[AI-DEFAULT]` concurrency/idempotency/permission/ntf-retry (BA confirm ตอน review)

> resolved เมื่อไหร่ → ย้ายมาเป็น LD ที่นี่

---

## §7.4 Architecture Tradeoffs Acknowledged

### AT-01: fire-and-forget handoff (ไม่รอ ack) — V1
- **Tradeoff:** simplicity vs. delivery guarantee — ฝั่งรับ On/Offboard ยังไม่ออกแบบ (OQ-15)
- **Accepted:** YES for V1 (event stub) · re-evaluate เมื่อฝั่งรับพร้อม (ack/retry/rollback)

### AT-02: role masking แทน per-person Restricted Resources ACL — V1
- **Tradeoff:** coarse (role-level) vs. fine (person-level ACL) — OQ-R1
- **Accepted:** YES for launch (recruiter unmask / manager·viewer mask) · wire Policy Center Restricted Resources Phase 2

### AT-03: optimistic lock (ไม่ pessimistic) สำหรับ concurrent stage move
- **Tradeoff:** rare contention → optimistic 409 · penalize 1% conflict ไม่ใช่ 99% (OQ-D1)
- **Accepted:** YES

---

## §7.5 Decisions Deferred to Implementation
| Item | Owner | Deadline |
|---|---|---|
| PDPA retention period ค่าจริง + withdraw/anonymize job | Strike/พี่เบิร์ด | หลัง OQ-16 (Phase 4) |
| On/Offboard inbound contract + ack | Strike | หลัง OQ-15 (integration phase) |
| DOA slot chain ค่าจริง (role ids) | Policy Center / BA | pre-deploy (declaration) |
| ENG-RCT register CUBIC | Architect | dev hand-off |
| Export CSV format | dev | sprint |

---

## §7.6 References
- Scope Lock source: BRD §3.4 + LANE_BRIEF + current-state §3
- Convention: `knowledge/conventions.md`
- CUBIC: `references/cubic-schema-templates.md`
- Related: F-HR-ONBOARD (handoff) · F-HR-SALSTRUCT (band) · Policy Center F-DLG-001 (DOA)
