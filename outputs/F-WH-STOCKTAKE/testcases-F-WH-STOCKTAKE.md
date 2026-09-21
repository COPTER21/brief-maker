# AI Test Cases — F-WH-STOCKTAKE

## Meta

| Field | Value |
|---|---|
| Feature | Stocktake รอบตรวจนับใหญ่ |
| Source | BRD_F-WH-STOCKTAKE.md + FRD_Pack + F-WH-STOCKTAKE.html |
| Version | 1.0 — 2026-09-20 |
| Run target | `F-WH-STOCKTAKE.html` |
| Primary routes | `#/rounds`, `#/create`, `#/sheets`, `#/variance`, `#/history` |

> ทุกเคสต้องเริ่มด้วยการ Refresh หน้าเพื่อคืนค่า Demo ก่อนทดสอบ เว้นแต่เคสระบุให้ทำต่อเนื่องกัน ค่าบุคคล P1–P5 เป็นตัวจำลองบทบาทสำหรับ prototype เท่านั้น

## Coverage Manifest

| Area | Covered by |
|---|---|
| FN-01–FN-04 รอบนับ, scope, lock, snapshot | TC-ST-01–TC-ST-05 |
| FN-05–FN-09 ใบนับ, blind count, validation, recount | TC-ST-06–TC-ST-13 |
| FN-10 DOA approval | TC-ST-14–TC-ST-18 |
| FN-11 handoff / unlock | TC-ST-19–TC-ST-20 |
| FN-12 boundary Stocktake/Cycle Count | TC-ST-21 |
| Permission / error / concurrency / integration | TC-ST-22–TC-ST-27 |

## Data Sets

| Set | Values |
|---|---|
| DS-A | รอบตัวอย่าง `ST-2026-001`; ยอดระบบ ITM-001 = 12, ITM-002 = 20 |
| DS-B | นับครั้งแรก ITM-001 = 9, ITM-002 = 20; นับซ้ำ = 11, 20 |
| DS-C | ผู้ตรวจครั้งแรก P1; ผู้ตรวจซ้ำ P2; ผู้อนุมัติ P3 แล้ว P4; ผู้รับช่วงการเงิน P5 |
| DS-D | มูลค่าผลต่างจาก DS-B = 25,000 บาท; prototype แสดงสายอนุมัติ 2 ขั้น |

## Test Cases

### TC-ST-01 — เปิดรายการรอบนับและใช้ตัวกรอง

- Priority: High
- Trace: FN-01, UI-01, BR-ST-01
- Setup: Refresh แล้วเปิด `#/rounds`
- Steps:
  1. ตรวจหัวหน้า “รอบตรวจนับใหญ่” และตารางรายการ
  2. พิมพ์ข้อความในช่องค้นหา แล้วเลือกสถานะหนึ่งค่า
  3. กดล้างตัวกรอง
- Expected: ตารางเปลี่ยนตามคำค้น/สถานะ และกลับมาแสดงรายการเดิมหลังล้าง โดยไม่เปลี่ยนข้อมูลรอบนับ

### TC-ST-02 — สร้างรอบนับด้วยข้อมูลครบ

- Priority: High
- Trace: FN-01, UI-02, API-01
- Setup: Refresh แล้วเปิด `#/create`
- Steps:
  1. กรอกชื่อรอบ เลือกคลัง โซน และตำแหน่ง
  2. กด “สร้างรอบนับ”
- Expected: drawer ปิด ระบบแสดงข้อความสำเร็จ และมีรอบใหม่ในรายการพร้อมสถานะก่อนล็อกยอด

### TC-ST-03 — กันการสร้างรอบเมื่อข้อมูลจำเป็นไม่ครบ

- Priority: High
- Trace: FN-01, BR-ST-01, ERR-01
- Setup: Refresh แล้วเปิด `#/create`
- Steps:
  1. เว้นชื่อรอบหรือพื้นที่อย่างน้อยหนึ่งช่อง
  2. กด “สร้างรอบนับ”
- Expected: ระบบไม่สร้างรอบ ระบุช่องที่ต้องกรอก และ drawer ยังเปิดให้แก้ไข

### TC-ST-04 — ล็อกยอดและสร้าง snapshot

- Priority: High
- Trace: FN-03, FN-04, BR-ST-02, API-02
- Setup: มีรอบใหม่ที่ยังไม่ล็อกและไม่ทับพื้นที่รอบอื่น
- Steps:
  1. เปิดรอบดังกล่าว
  2. กดปุ่มล็อกยอด/เริ่มรอบ แล้วยืนยัน
- Expected: สถานะรอบเปลี่ยน ระบบแสดงเวลา lock และสร้างใบนับจากยอด ณ เวลานั้น โดยยอดเดิมไม่เปลี่ยนตาม movement ภายหลัง

### TC-ST-05 — บล็อกรอบพื้นที่ทับซ้อน

- Priority: High
- Trace: FN-03, BR-ST-01, ERR-02
- Setup: มีรอบที่กำลังทำงานในคลัง/โซน/ตำแหน่งเดียวกัน
- Steps:
  1. สร้างอีกรอบด้วยพื้นที่เดียวกัน
  2. พยายามล็อกยอด
- Expected: ระบบไม่ล็อกยอดและแจ้งว่าพื้นที่มีรอบที่ยังทำงานอยู่

### TC-ST-06 — เปิดใบนับและมอบหมายผู้ตรวจครั้งแรก

- Priority: High
- Trace: FN-02, FN-05, API-03
- Setup: Refresh แล้วเปิด `#/sheets`
- Steps:
  1. เปิดใบนับของรอบ `ST-2026-001`
  2. กด “มอบหมาย” เลือก P1 แล้วบันทึก
- Expected: ใบนับแสดงชื่อผู้ได้รับมอบหมาย P1 และสถานะพร้อมนับ

### TC-ST-07 — กันการมอบหมายโดยไม่เลือกคน

- Priority: Medium
- Trace: FN-05, ERR-03
- Setup: อยู่ในหน้าต่างมอบหมายใบนับ
- Steps:
  1. ไม่เลือกบุคคล
  2. กดยืนยัน
- Expected: หน้าต่างไม่ปิดและแจ้งให้เลือกผู้ตรวจนับ

### TC-ST-08 — ผู้ตรวจนับเห็นเฉพาะช่องยอดจริง

- Priority: Critical
- Trace: FN-06, BR-ST-03, SEC-02
- Setup: มอบหมาย P1 แล้วสลับผู้ใช้งาน Demo เป็น P1
- Steps:
  1. เปิดใบนับที่ได้รับมอบหมาย
  2. ตรวจคอลัมน์และข้อมูลทุกแถว
- Expected: เห็นรหัสสินค้า/ตำแหน่งและช่องกรอกยอดนับ แต่ไม่เห็นจำนวนในระบบหรือผลต่าง

### TC-ST-09 — คนที่ไม่ได้รับมอบหมายส่งผลไม่ได้

- Priority: Critical
- Trace: FN-05, FN-06, BR-ST-03, SEC-01
- Setup: ใบนับมอบหมายให้ P1 แต่สลับผู้ใช้งานเป็นบุคคลอื่น
- Steps:
  1. เปิดใบนับ
  2. พยายามกด “ส่งผลนับ”
- Expected: ระบบไม่รับผลและแจ้งว่าต้องเป็นผู้ที่ได้รับมอบหมาย

### TC-ST-10 — รับค่า 0 แต่ไม่รับช่องว่างหรือค่าติดลบ

- Priority: High
- Trace: FN-07, BR-ST-03, ERR-04
- Setup: เป็นผู้ได้รับมอบหมายและเปิดใบนับ
- Steps:
  1. กรอก `0` ในทุกแถวแล้วตรวจว่าปุ่มส่งทำงานได้
  2. Refresh กลับมาใหม่ เว้นหนึ่งช่องว่างแล้วกดส่ง
  3. กรอก `-1` แล้วกดส่ง
- Expected: ค่า 0 ถือเป็นจำนวนที่ถูกต้อง ส่วนช่องว่างและค่าติดลบถูกปฏิเสธพร้อมข้อความชี้ช่อง

### TC-ST-11 — ส่งผลครั้งแรกที่เกิน threshold

- Priority: Critical
- Trace: FN-08, FN-09, BR-ST-04, API-05
- Setup: มอบหมาย P1 และเปิดใบนับในฐานะ P1
- Steps:
  1. กรอก DS-B ครั้งแรก: `9` และ `20`
  2. กด “ส่งผลนับ”
- Expected: ระบบรับผล เปลี่ยนสถานะเป็น “รอนับซ้ำ” และแสดงว่าต้องมอบหมายผู้ตรวจคนอื่น โดยผู้ตรวจยังไม่เห็นยอดระบบ

### TC-ST-12 — ห้ามผู้ตรวจคนเดิมนับซ้ำ

- Priority: Critical
- Trace: FN-09, BR-ST-04, ERR-05
- Setup: ใบนับอยู่สถานะ “รอนับซ้ำ” และผู้ตรวจครั้งแรกคือ P1
- Steps:
  1. เปิดการมอบหมายผู้ตรวจซ้ำ
  2. เลือก P1 แล้วกดยืนยัน
- Expected: ระบบไม่บันทึกและแจ้งว่าผู้ตรวจซ้ำต้องเป็นคนละคน

### TC-ST-13 — ผู้ตรวจซ้ำส่งยอดแล้วเข้าสู่ตรวจผลต่าง

- Priority: Critical
- Trace: FN-08, FN-09, API-06
- Setup: ต่อจาก TC-ST-11 มอบหมายผู้ตรวจซ้ำเป็น P2 และสลับเป็น P2
- Steps:
  1. เปิดใบนับซ้ำ
  2. กรอก `11` และ `20`
  3. กด “ส่งผลนับ”
- Expected: สถานะเปลี่ยนเป็น “ตรวจผลต่าง”; ผลสุดท้ายเทียบ snapshot 12/20 จึงเป็น -1/0 แต่ P2 ยังไม่เห็นยอดระบบหรือผลต่าง

### TC-ST-14 — หัวหน้างานเห็นผลต่างและมูลค่าถูกต้อง

- Priority: Critical
- Trace: FN-06, FN-08, FN-10, BR-ST-05
- Setup: ต่อจาก TC-ST-13 แล้วสลับเป็น P3 เปิด `#/variance`
- Steps:
  1. เปิดรายการ `ST-2026-001`
  2. ตรวจยอดระบบ ยอดนับสุดท้าย ผลต่าง และมูลค่า
- Expected: ITM-001 แสดง 12, 11, -1 และมูลค่าผลต่าง 25,000 บาท; ITM-002 แสดง 20, 20, 0

### TC-ST-15 — ต้องระบุผู้อนุมัติทุก slot

- Priority: Critical
- Trace: FN-10, BR-ST-05, ERR-06
- Setup: อยู่หน้า variance ที่มีสายอนุมัติ 2 ขั้น
- Steps:
  1. เว้นผู้อนุมัติอย่างน้อยหนึ่งขั้น
  2. กดส่งอนุมัติ
- Expected: ระบบไม่ส่งคำขอและชี้ว่าต้องเลือกผู้อนุมัติให้ครบทุกขั้น

### TC-ST-16 — กันบุคคลต้องห้ามและผู้อนุมัติซ้ำ

- Priority: Critical
- Trace: FN-10, BR-ST-05, SEC-03
- Setup: ผู้ตรวจคือ P1/P2 และมี 2 approval slots
- Steps:
  1. เลือก P1 หรือ P2 เป็นผู้อนุมัติ
  2. จากนั้นเลือกบุคคลเดียวกันทั้งสองขั้น
- Expected: ทั้งสองแบบถูกปฏิเสธ ผู้ตรวจนับไม่สามารถอนุมัติ และแต่ละขั้นต้องเป็นคนละคน

### TC-ST-17 — อนุมัติตามลำดับสองขั้น

- Priority: Critical
- Trace: FN-10, BR-ST-05, API-07
- Setup: ส่งสายอนุมัติ P3 → P4 สำเร็จ
- Steps:
  1. ขณะเป็น P4 พยายามอนุมัติก่อน P3
  2. สลับเป็น P3 แล้วอนุมัติ
  3. สลับเป็น P4 แล้วอนุมัติ
- Expected: ขั้น 2 ทำก่อนขั้น 1 ไม่ได้; หลัง P3 อนุมัติจึงเปิดให้ P4; เมื่อครบทั้งสองขั้นสถานะพร้อมส่งต่อใบปรับยอด และประวัติบันทึกผู้ทำ/เวลา

### TC-ST-18 — ปฏิเสธต้องมีเหตุผล

- Priority: High
- Trace: FN-10, BR-ST-05, ERR-07
- Setup: มีคำขอรออนุมัติที่ผู้ใช้งานปัจจุบันเป็นผู้อนุมัติขั้นนั้น
- Steps:
  1. กดปฏิเสธโดยไม่กรอกเหตุผล
  2. กรอกเหตุผลแล้วกดยืนยัน
- Expected: ครั้งแรกระบบไม่รับ; ครั้งที่สองสถานะเป็นปฏิเสธและประวัติมีเหตุผล

### TC-ST-19 — ส่งต่อใบปรับยอดและปลดล็อก

- Priority: Critical
- Trace: FN-11, BR-ST-06, XT-ST-01, API-08
- Setup: อนุมัติครบทุกขั้นแล้ว
- Steps:
  1. กด “ส่งต่อใบปรับยอด”
  2. เปิด `#/history`
- Expected: รอบปิด, movement lock ถูกปลด, ประวัติมีเลขอ้างอิง draft จาก F-WH-ADJUST และไม่มีการปรับสต๊อกจริงจากหน้านี้

### TC-ST-20 — กันการส่งต่อซ้ำ

- Priority: High
- Trace: FN-11, BR-ST-06, API-08
- Setup: รอบถูกส่งต่อสำเร็จแล้ว
- Steps:
  1. กลับมาที่รายการเดิมหรือส่งคำขอซ้ำด้วย request เดิม
- Expected: ไม่มี draft ซ้ำและประวัติไม่เพิ่มเหตุการณ์ซ้ำ

### TC-ST-21 — แยก Stocktake จาก Cycle Count

- Priority: Medium
- Trace: FN-12, LOCK-ST-04
- Setup: Refresh เปิดหน้ารอบนับ
- Steps:
  1. ตรวจชื่อหน้า คำอธิบาย และปุ่มสร้างรอบ
- Expected: ระบุว่าเป็น “รอบตรวจนับใหญ่/Stocktake” และไม่มีการตั้ง ABC schedule หรือหน้าจอ Cycle Count

### TC-ST-22 — สิทธิ์หัวหน้างานกับผู้ตรวจไม่ปะปน

- Priority: Critical
- Trace: SEC-01, SEC-02, UI-03, UI-04
- Setup: มีข้อมูลอยู่ทั้งหน้าใบนับและหน้าตรวจผลต่าง
- Steps:
  1. เป็น P1/P2 เปิดหน้า variance
  2. เป็น P3 เปิดหน้า variance
- Expected: ผู้ตรวจไม่มี action อนุมัติหรือข้อมูลที่เกินสิทธิ์; หัวหน้างานจึงเห็นยอดระบบ/ผลต่างและ action ตามสถานะ

### TC-ST-23 — optimistic concurrency

- Priority: High
- Trace: NFR-03, API error 409
- Setup: เปิดรายการเดียวกันสอง session ที่ revision เดียวกัน
- Steps:
  1. Session A บันทึกสำเร็จ
  2. Session B ส่งการแก้ไขจาก revision เก่า
- Expected: Session B ได้ conflict และต้อง refresh; ข้อมูลของ A ไม่ถูกทับ

### TC-ST-24 — idempotency ของคำสั่งเปลี่ยนสถานะ

- Priority: High
- Trace: NFR-03, API-05/API-07/API-08
- Setup: เตรียม request เดียวกันพร้อม idempotency key เดียวกัน
- Steps:
  1. ส่ง request ซ้ำสองครั้ง
- Expected: เกิดผลทางธุรกิจเพียงครั้งเดียว และ response ครั้งหลังอ้างผลเดิม

### TC-ST-25 — F-WH-ADJUST ปลายทางล้มเหลว

- Priority: High
- Trace: XT-ST-01, BR-ST-06
- Setup: จำลองปลายทางสร้าง draft ใช้งานไม่ได้
- Steps:
  1. กดส่งต่อใบปรับยอด
- Expected: รอบยังไม่ปิดและยังไม่ปลด lock; แสดงข้อผิดพลาดที่ลองใหม่ได้; ไม่มี draft ครึ่งสำเร็จ

### TC-ST-26 — movement ตรงขอบเขตเวลาล็อก

- Priority: High
- Trace: XT-ST-02, BR-ST-02
- Setup: มี movement ก่อนและหลัง `locked_at`
- Steps:
  1. ล็อกยอดพร้อมจำลอง movement ที่เวลาขอบเขต
  2. ตรวจ snapshot และผลต่าง
- Expected: snapshot ยึดกติกา cut-off เดียวกันทุกแถวและไม่ดึง movement หลัง lock มาปน

### TC-ST-27 — configuration และ Demo control ไม่รั่วสู่ production

- Priority: High
- Trace: XT-ST-03, LOCK-ST-05, SEC-04
- Setup: ตรวจ build production และ deployment ที่ผูก DOA จริง
- Steps:
  1. ตรวจว่า threshold/สายอนุมัติมาจาก config version ที่ถูก snapshot
  2. ตรวจว่าไม่มีตัวเลือก “สลับผู้ใช้งาน Demo” ใน production
- Expected: รอบเดิมใช้ config snapshot เดิมแม้ config ใหม่เปลี่ยน และ production ไม่มี persona switch

## Run Protocol

1. รัน TC-ST-01 ถึง TC-ST-22 บน UI ตามลำดับ โดย Refresh ก่อนเคสที่ระบุ
2. รัน TC-ST-23 ถึง TC-ST-27 ใน integration environment เพราะ prototype จำลอง backend ได้ไม่ครบ
3. เก็บ screenshot เฉพาะผลลัพธ์สำคัญ พร้อม route, persona, เวลา และเลขรอบ
4. ถ้าผลจริงต่างจาก Expected ให้บันทึก `FAIL` ห้ามตีความแทนระบบ

## Coverage Audit

| Source | Coverage |
|---|---|
| 12 Function Checklist items | 12/12 |
| 10 Business Rules | 10/10 |
| UI routes | 5/5 |
| Error/negative/permission | Covered |
| Cross-module / concurrency / idempotency | Covered by integration cases |

## Result Schema

| Case ID | Result (`PASS`/`FAIL`/`BLOCKED`) | Actual result | Evidence path | Tester | Tested at | Defect/OQ |
|---|---|---|---|---|---|---|
| TC-ST-__ | ☐ |  |  |  |  |  |

