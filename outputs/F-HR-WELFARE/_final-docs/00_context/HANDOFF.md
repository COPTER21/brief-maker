# HANDOFF — F-HR-WELFARE · Welfare (สวัสดิการ) · Phase A จบ 2026-08-31 · runner v2.4

> **อ่านไฟล์นี้ก่อนแตะ HTML** · ทิศทางอยู่ใน `0_DIRECTION/PREBRIEF.md` (source of truth business) · `FUNCTION_CHECKLIST.html` (ติ๊ก FN 24 ข้อ) · `STANDARD_BASELINE.md` (MUST 11 จาก Odoo/D365/SAP)

## 1. feature นี้ทำอะไร (3 บรรทัด)
ทะเบียนสิทธิ์สวัสดิการต่อกลุ่มพนักงาน (โควตา/วงเงินต่อปีต่อคน) + ผู้ติดตาม + คำขอใช้สิทธิ์ → อนุมัติ (DOA) → บันทึกการใช้ + คงเหลือ.
ผู้ใช้: HR สวัสดิการ (จัดการ/อนุมัติ) · หัวหน้า (อนุมัติ DOA) · พนักงาน (ยื่น · ESS ภายหลัง).
จบที่: คำขออนุมัติ ตัดคงเหลือ ยิงมูลค่าเข้า 7C EC และส่งสถานะจ่ายให้ Payroll/Expense (ไม่จ่ายเงินเอง).

## 2. ของที่ส่งมอบใน pack นี้ (Phase A)
| โฟลเดอร์ | ไฟล์ | สถานะ |
|---|---|---|
| 0_DIRECTION | HANDOFF · PREBRIEF · FUNCTION_CHECKLIST.html · STANDARD_BASELINE | ✅ |
| 1_HTML | welfare.html (master · 4 tabs · 5 routes-equiv) | ✅ audit FAIL=0 · qc-ux BLOCK=0 · coverage R1 FN 24/24 |
| 2_BRD | BRD_welfare.md/.docx | ✅ APPROVED |
| 5_DECLARATIONS | DOA · NTF · CSQ + NOT_NEEDED(doccfg/pdfdoc) | ✅ |
| 3_FRD · 4_TC | — | ⏳ Phase B (ทีม) |

## 3. ห้ามแตะ (LOCK · จาก PREBRIEF/มติ)
- **LK-1** อนุมัติ = DOA `GET /doa/resolve` (slot picker มติ 17 ส.ค.) — ห้าม hardcode chain
- **LK-2** ไม่จ่ายเงินเอง — Payroll/Expense จ่าย · Welfare = hook display-only
- **LK-3** policy/effective_date/company_scope = HR Configuration (#107) — ห้ามทำหน้า config เอง
- **LK-4** soft reference LD-4C-02 (snapshot ชื่อ · ไม่มี FK cascade) · **LK-5** audit append-only · RESTRICTED masking · **LK-6** CSQ = EC เท่านั้น (ห้าม OC/DC-doc/SC)
- ความสามารถ feature อื่น = soft reference — ดู `knowledge/CONTEXT_PACK/HR_DONE_CONTRACTS/`

## 4. จุดที่ BA เดาไว้ ([ASSUMED]) · OQ ค้าง — Strike/พี่เบิร์ด เคาะ
| # | เรื่อง | default ที่ใช้ใน HTML | owner |
|---|---|---|---|
| A-WEL-01 | benefit master เป็นของ Welfare (ไม่ใช่ group ใน HR Config) | ใช้ pattern effective_date เอง | Strike |
| A-WEL-02 | จ่ายผ่าน Payroll/Expense = hook display-only | hook + [ASSUMED contract รอ FRD Phase B] | Strike |
| A-WEL-03 | DOA ไม่มีวงเงิน สายเดียว | หัวหน้า→HR ตามตำแหน่ง | พี่เบิร์ด |
| A-WEL-04 | ผู้ติดตามเก็บใน Welfare | ชื่อ·ความสัมพันธ์·วันเกิด·สถานะ | Strike |
| A-WEL-05 | open enrolment / life-event change | [AI-DRAFT] reason ของคำขอ · window อ้าง HR Config | Strike |
> DIVERGENCE: — (chip = detect ทุกท่อ · ไม่มี)

## 5. จุดที่ vibe ได้อิสระ (ไม่ต้องถาม)
- layout/ระยะ/ลำดับคอลัมน์/microcopy/ตัวอย่างข้อมูล · เพิ่ม state ว่าง/โหลด/ผิดพลาด
- **แต่คงไว้:** FN ทุกข้อใน FUNCTION_CHECKLIST · 4 tabs ตาม PREBRIEF §6 · iron rules v9 (audit ต้อง FAIL=0 หลัง vibe) · ปี พ.ศ. ทั้งไฟล์
- หมายเหตุ tech: BASE-KIT ไม่ได้กำหนด `--z-*` tokens → feature :root กำหนดไว้ (sticky5/backdrop50/drawer51/modal70) · อย่าลบตอน vibe ไม่งั้น overlay จม

## 6. ขั้นถัดไป (Phase B — คำสั่งพร้อม paste)
```
python3 .claude/skills/feature-lane-runner/scripts/run_state.py phase briefs/W4/F-HR-WELFARE docs
ใช้ skill feature-lane-runner v2.4 → lane docs "Welfare"   (S3 re-gate → S5 FRD → S6 TC → S6.5 → S7 UI Brief → S8 → S9)
python3 .claude/skills/feature-lane-runner/scripts/pool.py set "Welfare" done --run W4
```
