# BRD — Expense Claim (เบิกค่าใช้จ่าย) · F-HR-EXPENSE
> Lane Mode v2 · source: PREBRIEF + FUNCTION_CHECKLIST (FN-01..94) + declarations (DOA/NTF/CSQ/DOCCFG/PDFDOC) + expense.html (Q-document + B2 line editor) + LANE_BRIEF
> Status: **APPROVED** (C01–C23 · §14.6 = "ไม่รองรับ") · W4 · Phase A

## §1. Overview
ใบเบิกค่าใช้จ่ายพนักงาน (เอกสารธุรกรรม Pattern Q): สร้างใบเบิกหลายรายการ → ตรวจเพดานหมวด → อนุมัติตามวงเงิน (DOA threshold) → ออกเลข EXP-YYYY-NNNN + PDF → เลือกช่องทางจ่าย → ส่ง GL/Payroll (hook). **ไม่จ่ายเงิน/ไม่ลงบัญชีเอง.** 1 เมนูซ้าย: list + wizard 5 ขั้น + view 4 tabs.

## §2. Objectives & KPIs
- ลดรอบเวลาเบิก-อนุมัติ · คุมเพดานหมวด (เคสเกินเพดานต้องมีเหตุผล 100%) · สายอนุมัติถูกต้องตามวงเงิน · มูลค่าเข้า 7C ครบ

## §3. Scope
### In: ใบเบิก header+lines(VAT) · เพดานหมวด · DOA threshold · เลข+PDF · ช่องทางจ่าย · hook GL/Payroll · audit
### Out: จ่ายจริง · GL posting · per diem/mileage · travel request · cash advance · multi-currency · OCR · config หมวด
### §3.4 Scope Lock
- **LK-1** DOA threshold `GET /doa/resolve` (ยอดรวม→สาย · 17ส.ค. slot picker) — ห้าม hardcode "ถ้าเกิน X ให้ Y"
- **LK-2** ไม่จ่ายเงิน/ไม่ post บัญชีเอง — Finance/Payroll/Accounting · hook display-only (A-EXP-02)
- **LK-3** เพดานหมวด/legal จาก HR Config effective_date (#107) · **LK-4** เลข EXP + สำเนา = ENG-DOC-NUM/STORE
- **LK-5** CSQ FC/AC/EC เท่านั้น (ห้าม OC/DC-doc/SC) · **LK-6** LD-4C-02 soft ref · audit append-only · เงิน RESTRICTED

## §4. Roles
ผู้เบิก (สร้าง/ยื่น/แก้/ยกเลิก) · ผู้อนุมัติตามวงเงิน (หัวหน้า/ผจก./ผอ. ตาม DOA) · HR/Finance (ติดตาม) · เงิน RESTRICTED masking

## §5. User Journey (trace HTML)
list → สร้างใบเบิก (wizard: แหล่งที่มา›ข้อมูลหลัก›รายการค่าใช้จ่าย[B2]›เอกสารแนบ›ตรวจสอบ) → ตรวจเพดาน → ส่งอนุมัติ (DOA slot ตามวงเงิน) → อนุมัติ → เลข EXP+PDF → เลือกจ่าย → hook · view (รายละเอียด/PDF/ลายเซ็น/ประวัติ)

## §6. Data Entity
**Header:** doc_no(EXP-YYYY-NNNN auto ตอนอนุมัติ) · ผู้เบิก(snapshot) · ตำแหน่ง/ศูนย์ต้นทุน(Movement snapshot) · วันที่ · ช่องทางจ่าย · สถานะ · config_version_id · pay_status(hook)
**Line (B2):** วันที่ · หมวด(HR Config) · รายละเอียด · จำนวนเงิน(>0) · vat_mode(none/add/included) · แนบใบเสร็จ · computed net/vat/total
**Computed:** subtotal/vat/grand (totals() single source) · over-cap flag ต่อหมวด

## §7. User Stories: FN-01..94 (ดู FUNCTION_CHECKLIST · 22 FN)

## §8. Status Lifecycle
ร่าง→ยื่น→รออนุมัติ(DOA)→อนุมัติ(เลข+PDF)→ส่งจ่าย(hook)→จ่ายแล้ว(hook)→ปิด · ตีกลับ(rejected)→ร่าง · ยกเลิก(cancelled)

## §9. Business Rules (BR-01..10)
line เงิน>0·หมวด·VAT calcLineVat · เพดานหมวด(เกิน=เตือน+เหตุผล) · ≥1 รายการ+ใบเสร็จก่อนส่ง · DOA ตามยอด (ไม่ hardcode) · แก้ยอดข้ามช่วง→re-resolve · เลข/สำเนา ENG-DOC · FC/AC/EC · cost center snapshot ณ วันเบิก · จ่าย/post=hook · audit append-only·RESTRICTED
### §9.5 Flexibility: เพดานหมวด/DOA threshold ตั้งนอก feature (HR Config · DOA กลาง)

## §10. Edge Cases
เกินเพดาน (warn+เหตุผล [A-EXP-05]) · แก้ยอดข้ามช่วง DOA re-resolve · null cost_center · VAT included ย้อนคำนวณ · ยอด=0 ส่งไม่ได้

## §12.1 Downstream Impact
- Payroll HK-1 / Finance: รับสถานะจ่าย + GL payload (hook display-only · Accounting ยังไม่มี → Module Linkage ปิด) **[ASSUMED contract A-EXP-02 · รอ FRD Phase B]**
- ENG-CSQ: expense.approved(FC) · expense.posted(AC) · expense.recorded(EC) · ENG-NOTIFY: 4 event · DOA: 3-tier threshold · DOCCFG: EXP-YYYY-NNNN
- Movement: consume assignment/resolve (ตำแหน่ง/ศูนย์ต้นทุน) · HR Config: เพดานหมวด

## §13. Delivery Phases: Phase A (นี้) → ba-done · Phase B (ทีม) vibe→FRD/TC/UI

## §14. Dev Summary
### §14.6 Functions Cut (ไม่รองรับ)
จ่ายจริง/GL posting [A-EXP-02] · per diem/mileage · travel request · cash advance · multi-currency · OCR · config หมวดเอง(#107)

## §16. Security: เงิน RESTRICTED masking (Policy Center) · audit append-only · ไม่มี hard delete · CSQ SecC ไม่ประกาศ

## §OQ (ASSUMED · ขึ้น REVIEW_SHEET)
A-EXP-01 ช่องทางจ่ายต่อใบ · A-EXP-02 จ่าย/GL=hook · A-EXP-03 DOA threshold 3-tier (พี่เบิร์ดเคาะ) · A-EXP-04 เพดานหมวด group ใน HR Config · A-EXP-05 เกินเพดาน warn ไม่ block

## Quality Gate (C01–C23)
C01 KPI วัดได้ ✓ · C05 scope in/out ✓ · C08 roles ✓ · C10 data header+line(B2) ✓ · C12 lifecycle 8 state ✓ · C14 rules trace ✓ · C16 edge ✓ · C18 §14.6 ไม่รองรับ ✓ · C20 RESTRICTED ✓ · C22 downstream+5 declarations ✓ · C23 Scope Lock LK-1..6 ✓ → **APPROVED**
