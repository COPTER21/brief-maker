# 00_OVERVIEW — F-AGM-010 Cane Check-In

## §0.1 Identity
| | |
|---|---|
| Feature ID | F-AGM-010 |
| ชื่อ | เช็คอินรับอ้อย (Cane Check-In) |
| Module | เกษตรกรรม (AGM)/หน้างานโรงงาน · WKN |
| Pack | FRD_F-AGM-010_Pack (7 ไฟล์ STANDARD) |
| Reverse | RIF v2 + invariants.md 🔒 (T3 code-only) |
| BRD | BRD_F-AGM-010 APPROVED (LOCK-01..11) |

## §0.2 Purpose
หน้าจอเช็คอินรับอ้อยที่โรงงาน/เครื่องชั่ง — บันทึกรถเข้าโรงงาน + weighToken + ประเภทเข้า. เช็คอิน CBM booked → event CHECK_IN ดัน Cane Booking → "รอผลการเท".

## §0.3 Scope
In: 2 แท็บ (ต้องส่ง/เช็คอินแล้ว) · เช็คอิน 3 วิธี (CBM/สมาชิก/โควต้ากลาง) · QR scan · void · booking sync + retry · list (filter/CSV/pagination/detail). Out: scale hardware, Member/Central doc gen จริง, auto-retry, void reversal event.

## §0.4 Entities
CheckInItem (documentId CBM/NBM · weighToken · entryType · status · booking sync fields). → 04_DB.

## §0.5 Actors / RBAC
เจ้าหน้าที่ชั่ง/ประตู (เช็คอิน+retry+void) · หัวหน้ากะ (void) · Cane Booking (รับ event). → 05_RULES §5.3.

## §0.6 Cross-Module
**feed CBM (F-AGM-007)** — event CHECK_IN → booking "รอผลการเท" (idempotent) · read CBM dispatching (pending list) · read Quota/Member (สมาชิก) · weighToken จากเครื่องชั่ง.

## §0.11 Scope Lock (← BRD §3.4)
LOCK-01..11. สำคัญ: 3 methods (01/02), weighToken บังคับ (03), CBM sync (02), retry (05), void (05).

## §0.7 Pages (→ 01_UI)
P-01 Check-In List (2 tabs) · P-02 Detail drawer · OV method-chooser · OV CBM/Member/Central check-in · OV QR scan · OV void.

## §0.8 Open Questions
OQ-01 scale hardware · OQ-02 Member/Central doc+lookup · OQ-03 auto-retry · OQ-04 void reversal event (invariants §8).
