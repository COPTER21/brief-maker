# BRD — Welfare (สวัสดิการ) · F-HR-WELFARE
> Lane Mode v2 · source: PREBRIEF + FUNCTION_CHECKLIST (FN-01..94) + declarations (DOA/NTF/CSQ) + welfare.html (master · 4 tabs) + LANE_BRIEF (LOCK/ASSUMED)
> Status: **APPROVED** (Quality Gate C01–C23 ผ่าน · §14.6 = "ไม่รองรับ") · Wave W4 · Phase A (BA)

## §1. Overview
ระบบสวัสดิการพนักงาน: ทะเบียนสิทธิ์สวัสดิการต่อกลุ่มพนักงาน (โควตา/วงเงินต่อปีต่อคน) · ผู้ติดตาม (คู่สมรส/บุตร) · คำขอใช้สิทธิ์ → อนุมัติ (DOA) → บันทึกการใช้ + คงเหลือ · **ไม่จ่ายเงินเอง** (ส่งต่อ Payroll/Expense เป็น hook). 1 เมนูซ้าย ย่อยเป็น 4 tabs: ทะเบียนสวัสดิการ · คำขอใช้สิทธิ์ · คงเหลือรายคน · รายงาน.

## §2. Objectives & KPIs (วัดได้)
- O1 ลดเวลาจัดการคำขอสวัสดิการ (จากกระดาษ → ยื่น-อนุมัติในระบบ) · KPI: %คำขอที่อนุมัติในระบบ, รอบเวลาเฉลี่ยยื่น→อนุมัติ
- O2 คุมโควตา/วงเงินต่อคนต่อปีได้แม่นยำ · KPI: จำนวนเคสใช้เกินสิทธิ์ = 0 (บล็อกที่ระบบ)
- O3 สิทธิ์สอดคล้องสภาพการจ้าง · KPI: %สิทธิ์ที่ปิด/เปิดอัตโนมัติตาม joiner/leaver
- O4 มูลค่าสวัสดิการเข้าฐานเงินได้ครบ · KPI: %คำขออนุมัติที่ยิง CSQ EC สำเร็จ

## §3. Scope
### §3.1 In-scope: ทะเบียน benefit type (CRUD + versioning effective_date) · eligibility ตามกลุ่ม · โควตา/วงเงินต่อปี · ผู้ติดตาม · คำขอใช้สิทธิ์ (สร้าง/ส่ง DOA/อนุมัติ/ไม่อนุมัติ/ยกเลิก) · balance ledger · รายงานการใช้ · hook สถานะจ่าย (อ่าน)
### §3.2 Out-of-scope: การจ่ายเงินจริง · provider management · flex credits · หน้า config HR กลาง
### §3.4 Scope Lock (สืบทอด LANE_BRIEF — ศักดิ์เท่าใบเซ็น · ห้าม drift)
- **LK-1** อนุมัติ = DOA engine `GET /doa/resolve` (มติ 17 ส.ค. slot picker) — ห้าม hardcode chain
- **LK-2** ไม่จ่ายเงินเอง — Payroll/Expense เป็นผู้จ่าย · Welfare hook display-only (A-WEL-02)
- **LK-3** policy/effective_date/company_scope อ่าน HR Configuration (#107) — ห้ามสร้างหน้า config เอง
- **LK-4** soft reference LD-4C-02 (nullable · snapshot ชื่อ · ไม่มี FK cascade)
- **LK-5** audit append-only · ไม่มี hard delete · ข้อมูลบุคคล/มูลค่า RESTRICTED (Policy Center)
- **LK-6** CSQ ประกาศ EC เท่านั้น (ห้าม OC/DC-doc/SC → 422)

## §4. Roles & Permissions
| role | เห็น/ทำ |
|---|---|
| HR Welfare Admin | จัดการทะเบียน benefit type · เพิ่มผู้ติดตาม · อนุมัติชั้น HR · เห็นมูลค่าเต็ม |
| หัวหน้าสายงาน (DOA approver) | อนุมัติ/ไม่อนุมัติคำขอชั้นต้น (ตามที่ DOA resolve) |
| พนักงาน (ESS · Phase later) | ยื่นคำขอของตัวเอง/ผู้ติดตาม · ดูคงเหลือของตัวเอง |
> ข้อมูลบุคคล/ผู้ติดตาม/มูลค่า = RESTRICTED · masking ตาม role จาก login (ไม่มี persona switch ในหน้า · demo = .demo-strip)

## §5. User Journey (trace กับ route/tab จริงใน HTML)
1. ตั้งทะเบียน: Tab ทะเบียน → สร้าง benefit type (กลุ่ม/โควตา/effective) → มีผล
2. ยื่นคำขอ: Tab คำขอ → สร้างคำขอ → เลือกพนักงาน (combobox) → ระบบ resolve สิทธิ์ (กลุ่ม/ช่วง) → เลือก type ที่มีสิทธิ์ → กรอกมูลค่า (เช็คคงเหลือ) → แนบหลักฐาน → ส่งอนุมัติ (DOA slot picker)
3. อนุมัติ: ผู้อนุมัติเปิดคำขอ → timeline DOA → อนุมัติ → ตัดคงเหลือ + ยิง CSQ EC + hook จ่าย + NTF ผู้ยื่น
4. คงเหลือ: Tab คงเหลือ → ค้นพนักงาน → เห็นสิทธิ์/โควตา/ใช้/คงเหลือ + ผู้ติดตาม + ช่วงสิทธิ์ (joiner/leaver)
5. รายงาน: Tab รายงาน → การใช้สิทธิ์ตามประเภท/กลุ่ม/ช่วง

## §6. Data Entity
**Benefit Type (master):** id · ชื่อ · หมวด · หน่วยนับ(บาท/ครั้ง/%) · โควตา/วงเงินต่อปี · กลุ่มมีสิทธิ์[] · ครอบผู้ติดตาม(bool) · effective_date/effective_to · company_scope · version_id · status(active/archived)
**Dependent:** employee_ref · ชื่อ · ความสัมพันธ์ · วันเกิด · สถานะใช้สิทธิ์
**Benefit Request:** request_no · employee_ref(snapshot) · benefit_type_ref(+version snapshot) · ผู้ใช้สิทธิ์(self/dependent) · มูลค่า · วันที่ · เหตุผล · attachment[] · status · approval_chain(snapshot) · config_version_id · pay_status(hook · read-only)
**Balance Ledger (computed/append-only):** per (employee, type, ปีสิทธิ์) = quota − Σ recorded

## §7. User Stories (จาก FN ledger — ครบ 24)
ครอบคลุม FN-01..FN-19 + FN-90..94 (ดู FUNCTION_CHECKLIST) — สร้าง/แก้(เวอร์ชัน)/ปิดใช้ type · ผู้ติดตาม · คำขอ (สร้าง/ส่ง DOA/อนุมัติ/ไม่อนุมัติ/ยกเลิก) · คงเหลือ · leaver/joiner · hook จ่าย · รายงาน · ค้นหา/audit/masking

## §8. Status Lifecycle
**Benefit type:** ร่าง → มีผล(active) → แทนที่/ปิดใช้(archived)
**Request:** ร่าง → ยื่น(submitted) → รออนุมัติ(pending) → อนุมัติ+บันทึกใช้(recorded) → ปิด(closed) · แยก: ไม่อนุมัติ(rejected) · ยกเลิก(cancelled) · ระงับพ้นสภาพ(revoked)

## §9. Business Rules (จาก PREBRIEF BR-01..10)
BR-01 eligibility ตามกลุ่ม ณ วันยื่น · BR-02 โควตา/วงเงินต่อปีต่อคน (เกิน=บล็อก) · BR-03 effective_date ไม่ทับช่วง · BR-04 ผ่าน DOA ก่อนตัดคงเหลือ · BR-05 ตัดคงเหลือเฉพาะ approved · BR-06 ผูก employment window (null≠ไม่มีวันจบ) · BR-07 append-only/soft archive · BR-08 RESTRICTED masking · BR-09 มูลค่าอนุมัติ→CSQ EC · BR-10 snapshot ชื่อ/บริษัท/config_version
### §9.5 Flexibility: โควตา/กลุ่ม/effective ตั้งได้ต่อ type (ไม่ hardcode) · DOA chain ตั้งที่ DOA กลาง

## §10. Edge Cases
พ้นสภาพระหว่างคำขอค้าง → revoke · ใช้เกินคงเหลือ → บล็อก+ยอด · type ปิดใช้แต่คำขอเก่าอ้างเวอร์ชันเดิม · ผู้ติดตามเกินเกณฑ์ → เตือน · null last-day ≠ ยังทำงาน

## §12.1 Downstream Impact
- Payroll/Expense: รับสถานะ "รอจ่าย/ส่งจ่าย" ผ่าน hook (display-only) — **[ASSUMED contract A-WEL-02 · รอ FRD Phase B]**
- ENG-CSQ 7C: event welfare.granted (EC) · ENG-NOTIFY: 4 event (submit/result/near-limit/eligibility-end) · DOA: entry ของ feature (no-limit)
- On/Offboard: consume signal joiner/leaver (read)

## §13. Delivery Phases
Phase A (BA · รอบนี้): PREBRIEF · HTML v9 · BRD · declarations · HANDOFF → ba-done · Phase B (ทีม): vibe HTML → FRD/TC/UI Brief

## §14. Dev Summary
### §14.6 Functions Cut (ไม่รองรับ — ตรงกับ FUNCTION_CHECKLIST §ไม่รองรับ)
- จ่ายเงินจริง/เบิก/หักผ่านเงินเดือน — [OQ A-WEL-02] Expense/Payroll
- provider management (รพ./ประกัน) — [OQ cap.19 NICE]
- flex credits — [OQ cap.20 NICE]
- หน้า config HR กลาง — [#107] อ่าน HR Configuration
- เอกสารเลขรัน/PDF ทางการ — [ASSUMED] ไม่มีใน feature นี้ (ไม่ doccfg/pdfdoc)

## §16. Security
ข้อมูลบุคคล/ผู้ติดตาม/มูลค่า = RESTRICTED · masking Policy Center · audit append-only ทุก create/approve/แก้/ยกเลิก · ไม่มี hard delete · CSQ SecC ไม่ประกาศ (สงวน)

## §OQ (ASSUMED · Strike/พี่เบิร์ด เคาะ · ขึ้น REVIEW_SHEET)
- A-WEL-01 benefit master เป็นของ Welfare (ไม่ใช่ HR Config group) · A-WEL-02 จ่าย=hook display-only · A-WEL-03 DOA ไม่มีวงเงิน สายเดียว · A-WEL-04 ผู้ติดตามเก็บใน Welfare · A-WEL-05 open enrolment/life-event = [AI-DRAFT]

## Quality Gate (C01–C23) — สรุป
C01 objective วัดได้ ✓ · C05 scope in/out ชัด ✓ · C08 roles+permission ✓ · C10 data entity ครบ field ✓ · C12 status lifecycle มีทางเข้า/ออก ✓ · C14 rules trace ✓ · C16 edge ✓ · C18 §14.6 = "ไม่รองรับ" ✓ · C20 security RESTRICTED ✓ · C22 downstream+declarations ✓ · C23 Scope Lock สืบทอด LANE_BRIEF ✓ → **APPROVED**
