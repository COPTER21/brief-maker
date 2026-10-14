# 00_OVERVIEW — F-AGM-011 Cane Receiving

## §0.1 Identity
| | |
|---|---|
| Feature ID | F-AGM-011 |
| ชื่อ | การรับอ้อย (Cane Receiving) |
| Module | เกษตรกรรม (AGM)/หน้างานโรงงาน · WKN |
| Pack | FRD_F-AGM-011_Pack (7 ไฟล์ STANDARD) |
| Reverse | RIF v2 + invariants.md 🔒 (T3 enhanced code + T1 Enhancement spec) |
| BRD | BRD_F-AGM-011 APPROVED (LOCK-01..11) |
| Enhancement | Dump Result v2 & Sync All (truth ล่าสุดสำหรับ Sync) |

## §0.2 Purpose
ออกใบรับอ้อย (CRN) — ดึงผลการเท (dump v2) จากโรงงานผูกคันรถที่ Check-in แล้ว → ออกใบ+PDF/QR + side effects (CBM awaiting_payment, free coin). Receiving = SoT ของ net_weight + cane_type ให้ Payment.

## §0.3 Scope
In: 3 แท็บ (รอผลเท/เทแล้ว/ยกเลิก) · Issue drawer (dump v2 auto/manual) · Sync All (bulk) · Void (rollback) · PDF/QR · QR scan/search · Export CSV. Out: CCS (Payment), แก้ Check-in flow, scale/factory API จริง.

## §0.4 Entities
ReceivingItem (CHK-#### → CRN-YYYY-#####) + DumpResult v2 (caneType/timeIn-out/gross/tare/net) + CheckinSnapshot. → 04_DB.

## §0.5 Actors / RBAC
Receiving Staff (dump+ออกใบ+Sync All) · Supervisor/Admin (manual override+void) · Viewer (read) · CBM/Payment (cross). → 05_RULES §5.3.

## §0.6 Cross-Module
read Check-in (F-AGM-010 Draft) + Factory dump API · write CBM (F-AGM-007) awaiting_payment/awaiting_dump_result · free Weigh Coin · feed Payment (net+cane_type SoT).

## §0.11 Scope Lock (← BRD §3.4)
LOCK-01..11. สำคัญ: dump v2 no-CCS (02), auto-lock/manual (03), issue side effects (05), Sync All (07), Receiving=SoT (09), void rollback (10).

## §0.7 Pages (→ 01_UI)
P-01 Receiving List (3 tabs) · P-02 Issue Receiving Drawer · P-03 Detail · OV Sync All result · OV Void · OV PDF viewer · OV QR scan · OV Search.

## §0.8 Open Questions
OQ-01 cane_type master · OQ-02 factory API + net cross-check · OQ-03 Sync All idempotency · OQ-04 dump logs · OQ-05 void-when-paid (invariants §8).
