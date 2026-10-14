# 00_OVERVIEW — F-AGM-013 Cane Payment

## §0.1 Identity
| | |
|---|---|
| Feature ID | F-AGM-013 |
| ชื่อ | การทำจ่ายเงินอ้อย (Cane Payment) |
| Module | เกษตรกรรม (AGM) > Cane Payment · WKN |
| Pack | FRD_F-AGM-013_Pack (7 ไฟล์ STANDARD) |
| Reverse | invariants.md 🔒 (T4+ base code + AS-BUILT v4.1 + FRD/UI/API-DB/Testcase + Enhancement v2/v3.1/v4.1) |
| BRD | BRD_F-AGM-013 APPROVED (LOCK-01..13) |
| SSoT | Enhancement v4.1 (ประเภทอ้อย + ค่าธนาคารจังหวัดสาขา) |

## §0.2 Purpose
ตัวรัน (runtime) ที่นำ config จาก **Payment Setting (F-AGM-012)** มาคำนวณและ **ทำจ่ายเงินอ้อยให้เกษตรกรจริง** ต่อ 1 ใบรับอ้อย — Sync CCS → มูลค่าอ้อย → **ปรับประเภทอ้อย** → แบ่งงวด 1/2 (50/50) → pipeline 7 ขั้น (VAT/charge/หักหนี้/ดอกเบี้ยบิลขาว/ค่าธนาคารจังหวัดสาขา) → ยอดสุทธิ → เลือกวิธีจ่าย (โอน/เงินสด/เช็ค) → ออกบิล/ใบเสร็จ. รองรับ **บิลโปรโมชันแยกใบ** + **ใบเสร็จการจ่ายเงินอ้อยรวม**.

## §0.3 Scope
In: List (tabs/filter/export) · Sync CCS เดี่ยว+bulk · All-in-One Payment modal (3 tabs + step calc) · Detail Drawer · print บิล/ใบเสร็จ · ประเภทอ้อย · ค่าธนาคารจังหวัดสาขา · additional charges (FLAT/PER_TON) · หลักฐานไฟล์ (optional).
Out: Payment Setting UI/schema (F-AGM-012) · Debt internals · Quota bank-branch capture (upstream) · CCS legacy source · Receiving/Booking capture · reporting/BI.

## §0.4 Entities
Payment (header + weights/ccs/pricing/amounts/debt/cane_type/bank) + Installment 1/2 (InstallmentDetails) + Promotion (แยกใบ) + AdditionalCharge (config/manual, FLAT/PER_TON) + Receipt + cane_type_master. → 04_DB.

## §0.5 Actors / RBAC (5 roles)
Cane Office Clerk (view) · Accounting (view + export) · Finance Officer (sync + pay โอน + export + unmask bank) · Cashier (sync + pay เงินสด) · System Admin (ทั้งหมด). → 05_RULES §5.3.

## §0.6 Cross-Module
read **Payment Setting (F-AGM-012, active)**: base@10CCS/K/interest/bank fee/green-white schedule/VAT/charges/cane type master/factory province · read **Receiving (F-AGM-011)**: net_tons + cane_type · read **Quota/Farmer bank info**: bank_branch_province_code · read **CCS legacy**: ccs_value · feed **Debt (F-AGM-008)**: deduct · feed **เกษตรกร**: บิลงวด1/2 + บิลโปร + ใบเสร็จรวม.

## §0.7 Status Model (5 states — v4.1, **ไม่มี waiting_cash_proof**)
`waiting_ccs` (รอความหวาน) → `pending` (รอทำจ่ายงวด 1) → `pending_inst2` (รอทำจ่ายงวด 2) → `pending_promotion` (รอทำจ่ายโปรโมชั่น) → `completed` (เสร็จสิ้น).
> proof optional — ทุกวิธีจ่าย transition ทันที ไม่มีสถานะกลางรอหลักฐาน (types/payment.ts §3.1.3 · invariants §7 C-01). AA (ไม่มีงวด 2) → pending → completed.

## §0.8 Pages (→ 01_UI)
P-01 List (tabs รอความหวาน/รอทำจ่าย/เสร็จสิ้น) · P-02 All-in-One Payment modal (3 tabs + step calc) · P-03 Detail Drawer · Overlays: Sync CCS · Sync All progress · Cash proof upload/view (optional).

## §0.11 Scope Lock (← BRD §3.4)
LOCK-01..13. สำคัญ: มูลค่าอ้อย CCS (02), ปรับประเภทอ้อยก่อนแบ่งงวด (03), pipeline 7 ขั้น (05), หักหนี้ (06), ดอกเบี้ยบิลขาว (07), ค่าธนาคารจังหวัดสาขา (08), บิล 3 กรณี ห้าม WHITE/GREEN (09), โปรโมชันแยกใบไม่หักหนี้ (10), 5 states (11).

## §0.9 Enhancement Lineage
base (single net_amount + Sync CCS + cash-proof-waiting) → **v2** (Promotion bonus per ton) → **v3.1** (installment pipeline + green/white bill + 3 pay methods + promotion แยกใบ) → **v4.1** (cane type adjustment + bank branch province fee = SSoT). ที่ base ขัด v4.1 → **v4.1 ชนะ** (invariants §7).

## §0.10 Open Questions
OQ-01 interest rounding (runtime raw vs Setting roundUp 7) · OQ-02 VAT order (per-installment vs gross-then-split) · OQ-03 white schedule API-EXT contract · OQ-04 debt service contract · OQ-05 proof optional at completed · OQ-06 PER_TON net_tons_inst (invariants §8).
