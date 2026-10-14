# BRD — F-AGM-010 Cane Check-In (เช็คอินรับอ้อยที่โรงงาน)

> Constraint mode (จาก invariants.md 🔒) · Module เกษตรกรรม (AGM)/หน้างานโรงงาน · WKN · สถานะ: APPROVED

## §1 Business Context
หน้าจอ **เช็คอินรับอ้อยที่ประตูโรงงาน/เครื่องชั่ง** — บันทึกการเข้าโรงงานของรถอ้อย ผูกเลขเหรียญชั่ง (weigh token) และประเภทการเข้าโรงงาน (จองคิว/ไม่จองคิว/โควต้ากลาง). เป็นจุดเชื่อมกับ **Cane Booking (F-AGM-007)**: เช็คอินรถจองคิว → ยิง event CHECK_IN ดัน booking → **"รอผลการเท"** (ตรงกับ CBM system-event ingestion).

## §2 Problem / Opportunity
ของเดิม (React prototype) มี integration + sync/retry ครบแต่ CI shadcn gray, pagination mock, ไม่มี stats. Refactor → CUBE Warm Light + governance (weighToken บังคับ, idempotent sync + retry, void reason) และเชื่อม chain AGM.

## §3 Goals & Scope
### §3.4 Locked Decisions (LOCK — จาก invariants)
| LOCK | Decision |
|---|---|
| LOCK-01 | คงพฤติกรรม AS-BUILT 100% (model, methods, sync, validation) |
| LOCK-02 | **3 วิธีเช็คอิน**: จาก CBM (รหัส/QR) · ไม่มีคิว-สมาชิก (ค้นโควต้า) · ไม่มีคิว-โควต้ากลาง (BR-01) |
| LOCK-03 | **weighToken (เลขเหรียญชั่ง) บังคับ** ทุกการเช็คอิน (BR-02) |
| LOCK-04 | **CBM sync**: เช็คอิน CBM booked → event CHECK_IN → booking "รอผลการเท" (idempotent X-Idempotency-Key=checkin_id) (BR-03) |
| LOCK-05 | **Sync fail + retry**: syncPending + badge "ซิงก์ล้มเหลว" + ปุ่ม retry (idempotent) (BR-04) |
| LOCK-06 | Entry type → doc prefix: จองคิว=CBM-#### · ไม่จองคิว/กลาง=NBM-#### (BR-05) |
| LOCK-07 | Payment bill 2 งวด (บิลเขียว/บิลขาว) สำหรับ Member/Central (BR-06) |
| LOCK-08 | Void + เหตุผล (ไม่บังคับ) (BR-07) |
| LOCK-09 | 2-tab lifecycle: ต้องส่ง → เช็คอินแล้ว (BR-08) |
| LOCK-10 | สถานะ Booking column (checked-in, CBM only) · non-CBM = "-" (BR-09) |
| LOCK-11 | QR scan / manual CBM entry (BR-10) |

### Out of Scope
Scale hardware integration (weighToken auto) · Quota/Member lookup จริง + NBM doc gen · auto-retry backoff · void reversal event.

## §4 Entities & State
- **CheckInItem** (documentId CBM/NBM · weighToken · entryType 3 แบบ · status จัดส่ง/รอทำจ่าย/เสร็จสิ้น · booking sync fields)
State machine → invariants §4.

## §5 Key Business Rules
BR-01..10 (invariants §3). สำคัญ: 3 methods (BR-01), weighToken บังคับ (BR-02), CBM sync → รอผลการเท (BR-03), sync fail + retry idempotent (BR-04), doc prefix (BR-05), void reason (BR-07).

## §6 Functional Requirements (สรุป → FRD)
1. **US-01 Check-In List** — 2 แท็บ (ต้องส่ง/เช็คอินแล้ว) · search + filter สถานะ/แผนก/วันที่ · Export CSV · pagination · stats
2. **US-02 CBM Check-In** — ป้อนรหัส/สแกน QR → lookup → weighToken → sync booking
3. **US-03 Member Check-In** — ค้นโควต้า → ข้อมูลรถ + payment bill → NBM doc
4. **US-04 Central Quota Check-In** — ข้อมูลรถ + payment bill (ไม่มีโควต้า)
5. **US-05 QR Scan** — สแกน/ป้อนรหัส CBM
6. **US-06 Booking Sync + Retry** — badge สถานะ Booking / ซิงก์ล้มเหลว + retry
7. **US-07 Detail Drawer** — ดูรายละเอียดการเช็คอิน
8. **US-08 Void** — ยกเลิกเช็คอิน + เหตุผล
9. **US-09 Cross-module** — feed CBM (CHECK_IN → รอผลการเท)

## §7 Non-Functional
list p95<3s · check-in action<2s (inc sync) · sync idempotent + retry · weighToken บังคับ · CSV ไทย · เครื่องชั่ง integration ready.

## §18 Stats (list dashboard)
4 การ์ด: รอเช็คอิน (ต้องส่ง) · เช็คอินวันนี้ · ซิงก์ล้มเหลว (syncPending) · เสร็จสิ้น.

## §Cross-Module Map
```
Cane Booking (F-AGM-007) ──dispatching──▶ Check-In (pending list "ต้องส่ง")
Check-In (F-AGM-010) ──event CHECK_IN──▶ Cane Booking (booking → "รอผลการเท")
Quota/Member ──read──▶ Check-In (member method)
เครื่องชั่ง ──weighToken──▶ Check-In
```
