# 00_OVERVIEW — F-AGM-012 Cane Payment Setting

## §0.1 Identity
| | |
|---|---|
| Feature ID | F-AGM-012 |
| ชื่อ | ตั้งค่าการจ่ายเงินอ้อย (Cane Payment Setting) |
| Module | เกษตรกรรม (AGM) > Cane Payment · WKN |
| Pack | FRD_F-AGM-012_Pack (7 ไฟล์ STANDARD) |
| Reverse | RIF v2 + invariants.md 🔒 (T3 enhanced code + T1 docs/Enhancement) |
| BRD | BRD_F-AGM-012 APPROVED (LOCK-01..11) |

## §0.2 Purpose
Source of truth ของค่าพื้นฐานที่ Cane Payment ใช้คำนวณจ่ายจริง ต่อรอบหีบ — ราคา/CCS(K)/charges/VAT/**ดอกเบี้ยบิลขาว**/**ค่าธนาคาร**/**ตารางวันจ่ายบิลเขียว-บิลขาว** + preview.

## §0.3 Scope
In: 6 sections (General/CCS Delta/Additional Charges/Tax/Payout Schedule/Preview) · season selector · save/deactivate. Out: Payment runtime, CCS dump, approval, reporting, import/export.

## §0.4 Entities
PaymentSetting (season×product) + GreenSchedule + WhiteSchedule (FIXED_DATE/WITH_CANE) + AdditionalCharge. → 04_DB.

## §0.5 Actors / RBAC
Finance Manager (CRUD+status) · Finance Officer (update+preview) · Operations (view+preview) · Auditor (read) · Cane Payment (read active). → 05_RULES §5.3.

## §0.6 Cross-Module
read Season/Product/Price List (Base @10CCS) · **feed Cane Payment** (active setting: K/interest/bank fee/VAT/charges/pay dates).

## §0.11 Scope Lock (← BRD §3.4)
LOCK-01..11. สำคัญ: CCS formula (02), ดอกเบี้ยบิลขาว (04), WITH_CANE (05), bank fee province (07), unique Active + no-overlap (10).

## §0.7 Pages (→ 01_UI)
P-01 Payment Setting config (6 sidebar sections) · OV payout schedule modal (green/white) · OV additional charge · OV deactivate confirm.

## §0.8 Open Questions
OQ-01 create/duplicate/deactivate flow (list vs single) · OQ-02 rounding_mode · OQ-03 duplicate month-adjust · OQ-04 optimistic lock field · OQ-05 gap tolerance (invariants §8).
