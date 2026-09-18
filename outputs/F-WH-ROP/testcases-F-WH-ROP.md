# AI Test Cases · F-WH-ROP · Reorder Point

## 0. Control

- Target: `outputs/F-WH-ROP/F-WH-ROP.html`
- Routes: `#/records`, `#/history`, `#/settings`
- Source: BRD v2.0 + FRD Pack v2.0 + approved HTML
- Run date: ____ · Tester: ____ · Build: ____
- Result per case: `☐ NOT RUN  ☐ PASS  ☐ FAIL  ☐ BLOCKED`

## 1. Test Data

| Set | Policy/Snapshot | Expected |
|---|---|---|
| A | ITEM-101/WH-01: Min10 Max30 Safety5 Lead7 ADU2 ATP8 On-Order0 Pack12 | ROP19, triggered, raw27, qty36 |
| B | same policy; ATP19 | not triggered; near |
| C | same policy; ATP23 | normal |
| D | ITEM-116/WH-01 | no policy |
| E | valid policy but no F009 snapshot | unavailable; no side effect |

## 2. Manual UI Cases

### TC-001 — เปิดหน้าและสลับครบสามแท็บ

Trace: FN-01, UI P-01..03

| Step | Action | Expected visible result |
|---:|---|---|
| 1 | เปิด `#/records` | เห็นหัวข้อ **Reorder Point** และแท็บ **นโยบายเติมสินค้า** ทำงาน |
| 2 | กด **คำแนะนำเติม** | URL เป็น `#/history`; เห็น **รันตรวจตอนนี้** |
| 3 | กด **ประวัติ** | URL เป็น `#/settings`; เห็นตารางประวัติ |
| 4 | เปิด hash ที่ไม่รู้จัก | กลับหน้า `#/records` โดยหน้าไม่พัง |

Result: ☐ NOT RUN ☐ PASS ☐ FAIL ☐ BLOCKED · Evidence: ____

### TC-002 — ค้นหา กรอง เรียง และล้างตัวกรอง

Trace: FN-01, BR-ROP-01

| Step | Action | Expected visible result |
|---:|---|---|
| 1 | ที่ `#/records` กรอก `ITEM-101` ในช่อง **ค้นหาชื่อ / รหัสสินค้า / รหัสเก่า…** | เหลือเฉพาะแถว ITEM-101 และ footer แสดงจำนวนตรงข้อมูล |
| 2 | กดหัวคอลัมน์สินค้า | ลำดับสลับแต่จำนวนไม่เปลี่ยน |
| 3 | เลือกตัวกรองที่มีข้อมูล | ตารางเหลือรายการตรงเงื่อนไข |
| 4 | กด **ล้างตัวกรอง** | กลับมาเห็นรายการทั้งหมด |
| 5 | ค้นหาค่าที่ไม่มี | เห็น **ไม่พบรายการที่ตรงกับตัวกรอง** |

Result: ☐ NOT RUN ☐ PASS ☐ FAIL ☐ BLOCKED · Evidence: ____

### TC-003 — เพิ่มนโยบายด้วย searchable dropdown

Trace: FN-02, AT-01,07

| Step | Action | Expected visible result |
|---:|---|---|
| 1 | กด **เพิ่มนโยบาย** | Drawer **เพิ่มนโยบาย** เปิด |
| 2 | กดช่องสินค้าและพิมพ์ `ITEM-116` | รายการค้นหาเปิดเหนือ Drawer และเหลือ ITEM-116 |
| 3 | เลือก ITEM-116 และ WH-01 | ช่องแสดงรหัสและชื่อจากรายการ ไม่ใช่ข้อความอิสระ |
| 4 | กรอก Min10 Max30 Safety5 Lead7 ADU30 Pack12 วันที่วันนี้ | ทุกช่องไม่มี error |
| 5 | กด **บันทึก** | ปุ่มเป็น **กำลังบันทึก…**, Drawer ปิด และเห็น toast **บันทึกนโยบายแล้ว** |

Result: ☐ NOT RUN ☐ PASS ☐ FAIL ☐ BLOCKED · Evidence: ____

### TC-004 — Validation แสดงใต้ช่องที่ผิด

Trace: FN-02, AT-03..07

| Step | Action | Expected visible result |
|---:|---|---|
| 1 | เปิดเพิ่มนโยบาย เลือกสินค้า/คลัง แล้วกรอก Safety11, Min10, Max30 | แบบฟอร์มพร้อมบันทึก |
| 2 | กด **บันทึก** | ใต้ **Stock ปลอดภัย** แสดง **ต้องไม่มากกว่าค่าขั้นต่ำ** และช่องมีกรอบแดง |
| 3 | แก้ Safety5, Min31, Max30 แล้วบันทึก | error อยู่ใต้ **ขั้นต่ำ** ว่าต้องไม่มากกว่าค่าสูงสุด |
| 4 | ล้าง Min แล้วบันทึก | ใต้ Min แสดง **กรอกค่าขั้นต่ำ** |
| 5 | กรอก Lead Time -1 / Pack Size 0 | error อยู่ใต้ช่องนั้น; Drawer ไม่ปิดและไม่มี toast สำเร็จ |

Result: ☐ NOT RUN ☐ PASS ☐ FAIL ☐ BLOCKED · Evidence: ____

### TC-005 — แก้นโยบายสร้าง version ใหม่

Trace: FN-02,03, AT-02

| Step | Action | Expected visible result |
|---:|---|---|
| 1 | เปิดแถว ITEM-101/WH-01 แล้วกด **แก้ไขนโยบาย** | ค่าเดิมถูกเติมในฟอร์ม |
| 2 | เปลี่ยน Safety และวันที่เริ่มใช้ แล้วบันทึก | บันทึกสำเร็จและรายการล่าสุดสะท้อนค่าใหม่ |
| 3 | ไปแท็บ **ประวัติ** | เห็นรายการบันทึกนโยบายใหม่; ไม่มีปุ่มแก้/ลบประวัติ |

Result: ☐ NOT RUN ☐ PASS ☐ FAIL ☐ BLOCKED · Evidence: ____

### TC-006 — สูตรตัวอย่างครบทุกตัวเลข

Trace: FN-04, AT-08,10,13,14

| Step | Action | Expected visible result |
|---:|---|---|
| 1 | เปิด `#/history` และเปิด ITEM-101/WH-01 | Drawer คำแนะนำเปิด |
| 2 | อ่าน **ATP จาก F009** | เป็น 8 และไม่มีการแสดงว่าหัก hold ซ้ำ |
| 3 | อ่าน **จุดสั่งเติม** และเหตุผล | ROP=19 จาก max(10,5+2×7); เหตุผลแสดงตัวเลขครบ |
| 4 | อ่าน target/raw/pack | Max+Safety=35, raw=27, Pack=12 |
| 5 | อ่าน **จำนวนแนะนำ** | เป็น 36 |

Result: ☐ NOT RUN ☐ PASS ☐ FAIL ☐ BLOCKED · Evidence: ____

### TC-007 — Boundary และสามระดับสถานะ

Trace: FN-04,05, AT-09,16

| Step | Action | Expected visible result |
|---:|---|---|
| 1 | ใช้ snapshot ATP=ROP | ไม่เป็น **ต่ำกว่าจุด** เพราะเงื่อนไขเป็น `<` |
| 2 | ใช้ ATP ต่ำกว่า ROP หนึ่งหน่วย | เป็น **ต่ำกว่าจุด** |
| 3 | ใช้ ATP อยู่ระหว่าง ROP ถึง 1.2×ROP | เป็น **ใกล้จุด** |
| 4 | ใช้ ATP สูงกว่า 1.2×ROP | เป็น **ปกติ** |
| 5 | ตรวจ KPI และ pill | เห็นครบ ต่ำกว่าจุด/ใกล้จุด/ปกติ และสีแยกกัน |

Result: ☐ NOT RUN ☐ PASS ☐ FAIL ☐ BLOCKED · Evidence: ____

### TC-008 — Safety Stock ต้องเปลี่ยนผลจริง

Trace: FN-04, AT-11

| Step | Action | Expected visible result |
|---:|---|---|
| 1 | ประเมิน snapshot ATP16, ADU2, Lead7, Min10 เมื่อ Safety0 | ROP14; ไม่ trigger; qty0 |
| 2 | เปลี่ยนเฉพาะ Safety เป็น 5 แล้วประเมิน snapshot เดิม | ROP19; trigger; raw19; ปัด Pack12 เป็น qty24 |
| 3 | เปิด Drawer | เห็นเหตุผลที่อธิบาย Safety+ADU×Lead และ target Max+Safety |

Result: ☐ NOT RUN ☐ PASS ☐ FAIL ☐ BLOCKED · Evidence: ____

### TC-009 — สินค้าไม่มีนโยบาย

Trace: FN-05, AT-17

| Step | Action | Expected visible result |
|---:|---|---|
| 1 | กด **ตรวจคู่สินค้า×คลัง** | Drawer เปิดและ dropdown อยู่เหนือ Drawer |
| 2 | เลือก ITEM-116 และ WH-01 แล้วกด **ตรวจนโยบาย** | การ์ดอยู่ห่างจากช่องเลือกและแสดง **ยังไม่มีนโยบายเติมสินค้า** |
| 3 | ตรวจรายละเอียด | การ์ดแสดง ITEM-116 และ WH-01 ที่เลือก |
| 4 | กด **เพิ่มนโยบาย** | Drawer เพิ่มนโยบายเปิดพร้อม Item/Warehouse เดิม |

Result: ☐ NOT RUN ☐ PASS ☐ FAIL ☐ BLOCKED · Evidence: ____

### TC-010 — ส่ง Notification สำเร็จและ replay

Trace: FN-06, AT-22,23

| Step | Action | Expected visible result |
|---:|---|---|
| 1 | เปิดคำแนะนำที่ต่ำกว่าจุดแล้วกด **ส่งแจ้งเตือน** | ปุ่ม disabled และขึ้น **กำลังส่ง…** |
| 2 | รอจบ | Toast **ส่งแจ้งเตือนแล้ว**; Drawer ไม่แสดง code/payload/ข้อความสำเร็จซ้ำ |
| 3 | กดซ้ำรายการเดิม | Toast **รายการนี้แจ้งเตือนไปแล้ว** |
| 4 | ไปประวัติ | มีรายการแจ้งเตือนเพียงหนึ่งรายการและใช้ข้อความภาษาคน |

Result: ☐ NOT RUN ☐ PASS ☐ FAIL ☐ BLOCKED · Evidence: ____

### TC-011 — สร้าง PR Draft รวมต่อคลัง

Trace: FN-07, AT-24,26,27

| Step | Action | Expected visible result |
|---:|---|---|
| 1 | ใช้รอบที่ WH-01 มีสินค้าต่ำกว่าจุดสองตัว แล้วกด **สร้าง PR Draft ของคลังนี้** | ปุ่ม disabled และขึ้น **กำลังสร้าง…** |
| 2 | รอจบ | Toast **สร้าง PR Draft แล้ว · 2 รายการ**; Drawer ไม่แสดงผลสำเร็จซ้ำ |
| 3 | กดซ้ำ | Toast **คลังนี้มี PR Draft ของรอบนี้แล้ว** |
| 4 | เปิดแท็บประวัติและรายการสร้าง Draft | เห็น **เลขที่ PR Draft** และ **รอตรวจสอบและส่งอนุมัติ** |
| 5 | ตรวจ contract ผ่าน harness | Draft มี `status=draft`, `submitted=false`, warehouse เดียว, สอง lines; preferred vendor ไม่ split ใบ |

Result: ☐ NOT RUN ☐ PASS ☐ FAIL ☐ BLOCKED · Evidence: ____

### TC-012 — รันตรวจตอนนี้และ idempotency

Trace: FN-05,08, AT-19..21

| Step | Action | Expected visible result |
|---:|---|---|
| 1 | ดูข้อความ **ตรวจอัตโนมัติล่าสุด** | แยกจากปุ่ม manual; ไม่สื่อว่าปุ่มคือ scheduler |
| 2 | กด **รันตรวจตอนนี้** | ปุ่มเป็น **กำลังตรวจ…** และ disabled |
| 3 | รอจบ | Toast สรุปตรวจ/สร้าง Draft/แจ้งเตือนตามรายการที่เข้าเงื่อนไข |
| 4 | รันซ้ำด้วย key เดิม | จำนวน event และ Draft ไม่เพิ่ม |

Result: ☐ NOT RUN ☐ PASS ☐ FAIL ☐ BLOCKED · Evidence: ____

### TC-013 — ประวัติเป็นภาษาคนและ read-only

Trace: FN-08, AT-28

| Step | Action | Expected visible result |
|---:|---|---|
| 1 | เปิด `#/settings` | หัวตารางเป็น รายการ/รายละเอียด/สินค้า/คลัง/เวลา/สถานะ |
| 2 | ตรวจข้อความ | ไม่เห็น `notification.emitted`, `policy.saved`, `reorder_point.triggered`, `POL-*` หรือคอลัมน์ **อ้างอิง** |
| 3 | เปิดแต่ละประเภทเหตุการณ์ | Drawer แสดงคำอธิบายภาษาคน |
| 4 | ดู footer | มีเพียง **ปิด**; ไม่มีแก้ไข/ลบ |

Result: ☐ NOT RUN ☐ PASS ☐ FAIL ☐ BLOCKED · Evidence: ____

### TC-014 — Overlay, Esc และ production demo guard

Trace: UI overlay, scope lock

| Step | Action | Expected visible result |
|---:|---|---|
| 1 | เปิด Drawer แล้วเปิด dropdown | dropdown อยู่เหนือ Drawerและไม่ถูกตัด |
| 2 | กด Esc | dropdown ปิดก่อน Drawer |
| 3 | กด Esc อีกครั้ง | Drawer ปิดและไม่มี menu ค้างใน overlay root |
| 4 | inject `.demo-only{display:none!important}` | ไม่มีข้อความ DEMO และ layout ไม่ขยับ/ล้นแนวนอน |

Result: ☐ NOT RUN ☐ PASS ☐ FAIL ☐ BLOCKED · Evidence: ____

## 3. Contract / System Cases

### TC-015 — F009 ATP contract

Trace: BR-ROP-03, AT-08. Given F009 returns ATP8 after reserved/hold exclusion, FN-04 must use 8 unchanged and issue no Quality Hold query or second subtraction.

Result: ☐ NOT RUN ☐ PASS ☐ FAIL ☐ BLOCKED · Evidence: ____

### TC-016 — On-Order prevents duplicate replenishment

Trace: BR-ROP-05,07, AT-15. Given target35, ATP8 and On-Order27, evaluation returns raw0/qty0 and adds no new Draft line.

Result: ☐ NOT RUN ☐ PASS ☐ FAIL ☐ BLOCKED · Evidence: ____

### TC-017 — Missing snapshot failure

Trace: AT-18. Valid policy plus unavailable F009 snapshot returns `SNAPSHOT_UNAVAILABLE`, appends no NTF/PR side effect and exposes retryable unavailable state.

Result: ☐ NOT RUN ☐ PASS ☐ FAIL ☐ BLOCKED · Evidence: ____

### TC-018 — Two warehouses never share Draft

Trace: BR-ROP-09, AT-25. Triggered WH-01 and WH-02 results cause two F072 calls, each containing one warehouse and an independent idempotency key.

Result: ☐ NOT RUN ☐ PASS ☐ FAIL ☐ BLOCKED · Evidence: ____

### TC-019 — F072 origin and ownership

Trace: BR-CSQ-05, AT-32. Verify F072 persists `origin_type=reorder_point` and `origin_ref` with item, warehouse and rop_run_id; F072 alone emits PR lifecycle events.

Result: ☐ NOT RUN ☐ PASS ☐ FAIL ☐ BLOCKED · Evidence: ____

### TC-020 — CSQ sensitive policy change

Trace: BR-CSQ-01,02, AT-29. A successful sensitive config commit yields exactly one `master.changed`, SecC, provisional profile CSQ-ROP-01, complete old/new values and unique pair+version key.

Result: ☐ NOT RUN ☐ PASS ☐ FAIL ☐ BLOCKED · Evidence: ____

### TC-021 — CSQ exclusions

Trace: BR-CSQ-03..05, AT-30..32. Invalid/no-effect saves emit no CSQ; threshold breach emits NTF only; PR creation emits no F085 CSQ event.

Result: ☐ NOT RUN ☐ PASS ☐ FAIL ☐ BLOCKED · Evidence: ____

### TC-022 — Permission isolation

Trace: Security. A user without WH-02 scope receives 403 on read/write without existence leakage; no data/event/outbox write occurs and an access audit is recorded.

Result: ☐ NOT RUN ☐ PASS ☐ FAIL ☐ BLOCKED · Evidence: ____

### TC-023 — Optimistic version conflict

Trace: API-02, BR-ROP-01. Two writes with one expected_version: first 201, second 409, with no second policy/event.

Result: ☐ NOT RUN ☐ PASS ☐ FAIL ☐ BLOCKED · Evidence: ____

### TC-024 — Dependency error and retry

Trace: API-05,06. Simulated ENG-NOTIFY/F072 failure gives 424/retryable UI error and no success event; retry after recovery yields exactly one external effect.

Result: ☐ NOT RUN ☐ PASS ☐ FAIL ☐ BLOCKED · Evidence: ____

## 4. Coverage Summary

| Coverage | Cases |
|---|---|
| Happy path | TC-001,003,006,010,011 |
| Validation/negative | TC-004,009,017,021,022,023,024 |
| Boundary/formula | TC-006,007,008,016 |
| Idempotency/race | TC-010,011,012,023,024 |
| Cross-module | TC-015,018,019,020,021,024 |
| Permission/security | TC-014,022,023 |
| FRD acceptance coverage | AT-01..32 covered |

## 5. Run Result Schema

```json
{
  "feature": "F-WH-ROP",
  "case_id": "TC-001",
  "result": "PASS|FAIL|BLOCKED|NOT_RUN",
  "observed": "ข้อความที่เห็นจริง",
  "evidence": ["screenshot-or-log-path"],
  "build": "string",
  "run_at": "ISO-8601"
}
```
