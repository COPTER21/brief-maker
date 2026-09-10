# PROPOSALS_outbound — F-HR-ESS (F059 · ESS Portal / พนักงานทำเอง)

> 2026-09-11 · ปิดงาน WF-01 step 12 · ESS = portal **display-only** — ทุก "action" คือสัญญาที่ feature อื่น/ทีมกลางต้องรับรอง ESS ไม่ทำเอง
> รายการนี้คือข้อเสนอ/OQ ที่ต้องส่งกลับเจ้าของ feature + ทีมกลาง **ก่อน dev เริ่ม**

## A. Deep-link route contracts — **OQ-ESS-02** (ยืนยันกับเจ้าของ feature)
5 เส้น deep-link ยัง `[ASSUMED contract]` — ESS แค่ navigate ออกไป เจ้าของต้องมี route จริง:

| ปุ่มใน ESS | route ที่ ESS สมมติ | feature เจ้าของ | ต้องมี |
|---|---|---|---|
| ยื่นลา | `#/leave/new` | Leave (W2) | หน้า "ขอลา" |
| ขอทำงานล่วงเวลา | `#/ot/new` | OT (W2) | หน้า "ขอ OT" |
| ยื่นเบิก | `#/expense/new` | Expense (F101 done) | หน้า "ขอเบิก" |
| ขอแก้ข้อมูล | `#/profile/edit-request` | Employee | หน้า "ขอแก้ข้อมูล (ขออนุมัติ)" |
| ขอหนังสือรับรอง | `#/cert/new` | **Certificate F104** (ba-done W1) | หน้า "ขอหนังสือ" — F104 ระบุ "พนักงานขอผ่าน ESS" (FIX-01) |

## B. Read contracts — surfaces ที่ ESS อ่าน (self-scope)
| surface | เจ้าของ | สิ่งที่ ESS ต้องการ |
|---|---|---|
| สลิป PS-1 | Payroll (W4) | read self · all-or-nothing |
| ลา/โควตา | Leave | read self |
| OT/สแกนเวลา | OT/Attendance | read self |
| **ตารางกะ** | ระบบกะ/Time (W2) | read self — `[ASSUMED]` (FIX-02) ยืนยัน read contract |
| เบิก | Expense | read self |
| หนังสือรับรอง | Certificate | read self |
| สวัสดิการ/อบรม | Welfare/Training | read self |
| โปรไฟล์ | Employee | read self + masking (PII) |
| แจ้งเตือน | ENG-NOTIFY | **OQ-ESS-NTF-01**: read-contract (method/scope/filter) + เจ้าของ mark-read (ESS ไม่เขียนกลับ) |

## C. CSQ event — **OQ-ESS-01** (Architect + ENG-CSQ owner)
`CSQ_BRIEF` ประกาศ `ess.self_access` (1 event) · แต่ HTML/FRD วาง anchor 2 จุด `ess.access_denied` (403) + `ess.restricted_view` (เปิดดู RESTRICTED) → **เคาะว่าท่อ SecC รับ 1 event รวม หรือ 2 event แยก** ก่อน wire · ห้ามประกาศท่อ OC/DC ซ้ำ · ref `FRD_F-HR-ESS_Pack/05_RULES.md §5.7`

## D. Backend self-enforce — **OQ-ESS-05** (Security/Backend)
frontend กรอง self ได้เสมอ (โกหกได้) → **backend ต้อง enforce scope SELF ทุก query** (403 เมื่อ employee_id ≠ ตัวเอง) · TC-SEC02 เป็นเคส simulate (dev/security sign-off)

## E. Governance / รับทราบ
- **BR-05 มือถือ vs iron rule #97 desktop-base (`min-width:768`)** — ตอนนี้ desktop-base + responsive ถึง 768px · PREBRIEF บอกพนักงานใช้มือถือ → ถ้าต้องรองรับมือถือจริง (<768) ต้องขอ **exception จด CLAUDE.md** (แก้ skill BASE-KIT ไม่ได้) — **PM เคาะ**
- **Toast ไม่โชว์ route** — FIX-04 (ตัดศัพท์ contract ออกจากจอ) supersede FIX-01 (ที่ให้ toast โชว์ route) → toast = "กำลังนำทางไปหน้า X" · route เก็บใน `LINKS` + comment + e2e assert — **BA รับทราบแล้ว**
- FUNCTION_CHECKLIST/PREBRIEF ของ BA = 15 FN ตรงกับที่ทำจริง (ไม่มี governance gap แบบ F101)

## F. Design-system PENDING (ทะเบียนกลาง `_SHARED/DESIGN_SYSTEM_PENDING.md`)
- **DSP-01** (modal-in-drawer z-index) — เกิดซ้ำใน ESS, pre-wire แล้ว · รอแก้ BASE-KIT ต้นทาง
- **DSP-04 (ใหม่)** — capture-phase click delegation กลืน onclick ทั้งหน้า (qc-ux มองไม่เห็น) · แก้สำเนา + เพิ่ม uikit `assert_affordances_fire` (C3.8) · รอ generator/qc-ux ทบทวน pattern ต้นทาง
