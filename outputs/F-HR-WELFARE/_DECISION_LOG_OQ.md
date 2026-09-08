# F102 Welfare (F-HR-WELFARE) — Decision Log (OQ / research-based)

> PM/BA delegated: "AI research standard แล้วทำมาเลย" (2026-09-08).
> ทุกข้อตัดสินจาก **มาตรฐานอุตสาหกรรม/ERP** (D365, SAP) + payroll best practice — ไม่ได้เดาจาก brief.
> ผลที่ลงจอ/โค้ดรอบนี้: **OQ-WEL-01** (reversal) + **OQ-WEL-03** (exposure display). ที่เหลือเป็นการยืนยันมติเดิม.

---

## OQ-WEL-01 · การแก้คำขอที่อนุมัติแล้ว → **Reversal (กลับรายการ) · IMPLEMENTED**

**Decision:** คำขอสวัสดิการที่ "อนุมัติแล้ว" (และอาจส่งจ่ายแล้ว) **ห้ามลบ/ยกเลิกเงียบ ๆ** — การแก้ที่ถูกต้องคือ
**reversal แบบ append-only**: คงข้อมูลเดิมทั้งหมด, เพิ่มสถานะ `reversed` + เหตุผล + เวลา, คืนสิทธิ์การใช้ (คงเหลือ),
กลับ (reverse) มูลค่าที่บันทึกเข้าเงินได้ (7C · EC), และถ้าจ่ายแล้ว → ตั้ง flag แจ้ง Payroll ให้เบิกคืน (display-only).

**Standard rationale (1 บรรทัด):** ตรง D365/SAP reversal-document pattern + payroll best practice — บันทึกด้วย
**negative offsetting entry** และ **ระบุเหตุผลก่อนปรับ** เสมอ ไม่ทำลายรอยตรวจสอบเดิม.

**Implemented (welfare.html):**
- status ใหม่ `reversed` → `reqPill` (pill "กลับรายการแล้ว") + ตัวกรองสถานะแท็บคำขอ
- ปุ่ม "กลับรายการ" ใน `drawerRequestView` — โผล่เฉพาะ `status==='approved' && canApprove()`
- `doReverse(id)` — guard role (`canApprove`) → guard status (`approved` เท่านั้น) → modal บังคับเหตุผล (mirror `doReject`) → set `status/reverseReason/reversedAt` (+`payrollClawback` เมื่อ `pay==='sent'`)
- คืนคงเหลือ **อัตโนมัติ**: `usedByPerson()` นับเฉพาะ `approved` → mark `reversed` = ลดยอดใช้เอง (ไม่ปรับซ้ำ)
- audit/history เพิ่มบรรทัด "กลับรายการ · คืนมูลค่าเข้าเงินได้ (7C · EC)" (+ "แจ้ง Payroll ตั้งเบิกคืน") — append-only
- ไม่กระทบ FIX-05: cancel ยังทำได้เฉพาะ `draft/pending` (pre-approval) เท่านั้น สองขอบเขตแยกกัน

---

## OQ-WEL-02 · สวัสดิการแบบ recurring → **F102 enroll + F065 deduct (FIX-07) · ยืนยันมติเดิม**

**Decision:** สวัสดิการที่จ่ายประจำผ่านเงินเดือน (เช่น PVD %) — **F102 ทำหน้าที่ enroll/ประกาศสัดส่วนเท่านั้น**
การหักจริงเป็นของ **F065 (Payroll)**; F102 แสดงเป็น hook/display-only (ตาม FIX-07).

**Standard rationale:** benefit administration แยกจาก payroll run เป็นมาตรฐาน ERP — welfare module ไม่จ่าย/ไม่หักเอง
กันการตัดเงินซ้ำและ single source of truth ของรอบเงินเดือน.

---

## OQ-WEL-03 · exposure ของคำขอที่ยังค้าง → **check-at-approval (FIX-02) + exposure display · IMPLEMENTED (display)**

**Decision:** ใช้ **hard re-check ณ เวลาอนุมัติ** เป็นด่านจริง (มีแล้วผ่าน FIX-02 — คงไว้ ไม่แตะ) และ **เพิ่มความโปร่งใส**
ให้ผู้อนุมัติเห็น "ความต้องการอื่นที่ยังรออนุมัติ" บนสิทธิ์เดียวกัน เพื่อไม่อนุมัติเกิน (ไม่ทำ soft-reserve/lock).

**Standard rationale:** soft-reserve ระหว่างรออนุมัติสร้าง state กำกวม + เสี่ยง lock ค้าง — มาตรฐานคือ
**ตัดสินที่จุด commit (approval)** แล้วให้ผู้อนุมัติเห็น pending demand ประกอบการตัดสินใจ.

**Implemented:** `reqBalanceTab` เพิ่มบรรทัด "คำขอรออนุมัติอื่นของสิทธิ์นี้: N ใบ · รวม {amount}"
คำนวณจาก `REQUESTS.filter(empId & benefitId & status==='pending' & id!==r.id)` — display-only, ไม่แตะ FIX-02.

---

## A-WEL-03 / CL-0013 · สาย DOA → **2-step หัวหน้า→HR · no-limit · no exec path · ยืนยันมติเดิม**

**Decision:** สายอนุมัติสวัสดิการ = **2 ขั้น** (ขั้น 1 หัวหน้าสายงาน → ขั้น 2 HR สวัสดิการ), **ไม่มีวงเงิน (no-limit)**,
เลือก "คน" ในตำแหน่งจาก DOA กลาง (ไม่ hardcode สาย), ไม่มี execution/จ่ายจริงใน F102 (FIX-03 one-step-advance).

**Standard rationale:** approval chain ต้องมาจาก DOA engine กลาง (delegation-of-authority) ไม่ผูกตายในฟีเจอร์ —
รหัสสายจริงเป็นของ BA ที่หน้า DOA กลาง (feature ประกาศเท่านั้น).

---

## Declarations · **doa + ntf + csq** (เดิม) → reversal เพิ่ม event ที่ต้องประกาศตอน step 7

**Decision:** feature นี้ประกาศ 3 ตัว: `doa` (สายอนุมัติ 2 ขั้น) · `ntf` (แจ้งเตือนผู้ยื่น) · `csq` (บันทึกมูลค่าเข้า 7C·EC).

**Reversal เพิ่มสิ่งที่ต้อง declare (ทำตอน declaration skills รัน step 7 — ไม่แก้ 5_DECLARATIONS เองรอบนี้):**
- **CSQ:** event **EC-reverse** (negative offsetting entry คืนมูลค่าเข้าเงินได้ 7C·EC) — คู่กับ EC-forward เดิม
- **NTF:** event **`ntf-reversed`** (แจ้งพนักงานว่าคำขอถูกกลับรายการ · wording ทั่วไป ไม่มี raw event id บนจอ #81)
- **Payroll clawback** เป็น display-only flag (แจ้ง Payroll ตั้งเบิกคืน) — ปลายทาง F065 ไม่ใช่ event ของ F102

**Standard rationale:** ทุก financial reversal ต้องมีคู่ event (บันทึกกลับ + แจ้งผู้เกี่ยวข้อง) เพื่อ audit + payroll reconciliation.

---

_บันทึกโดย: AI (delegated by PM/BA) · 2026-09-08 · ที่มา: outputs/F-HR-WELFARE/welfare.html (surgical edits) + e2e-welfare.py (R1–R4, EX)_
