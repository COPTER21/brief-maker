# BRD · F-WH-ROP · จุดสั่งซื้อซ้ำ (Reorder Point)

**สถานะ:** APPROVED FOR FRD · **ฉบับ:** 2.0 · **วันที่:** 2026-09-18 · **ประเภท:** New Feature · **โมดูล:** Warehouse · **Wave:** W4 FULL

## 1. การควบคุมเอกสาร

ฉบับนี้ sync จาก HTML ที่ PM/BA ผ่าน, PREBRIEF, Function Checklist, feedback fix order และคำตอบ PM/BA เรื่อง NTF/CSQ วันที่ 2026-09-18 โดยแทนที่ข้อกำหนดเก่าที่เรียก PR ว่า mock และสูตรที่ใช้ Min อย่างเดียว

## 2. ปัญหาและเป้าหมาย

คลังต้องรู้ว่าสินค้าใดกำลังจะไม่พอใช้ และต้องเริ่มจัดซื้อจำนวนเท่าไรโดยไม่สร้างใบขอซื้อซ้ำ ระบบจึงต้องตั้งนโยบายรายสินค้า×คลัง อ่าน ATP สำเร็จรูป ประเมินทุกวันและทุก movement แจ้งเตือน และสร้าง PR Draft ให้คนตรวจสอบก่อนส่งอนุมัติ

### 2.1 ตัวชี้วัด

| ตัวชี้วัด | เป้าหมาย |
|---|---:|
| คู่สินค้า×คลังที่มีนโยบายพร้อมใช้ | 100% ของคู่ที่เปิดใช้งาน |
| สูตรและการปัด Pack Size ถูกต้อง | 100% ของชุดทดสอบ |
| PR Draft ซ้ำต่อคลังต่อรอบ | 0 |
| Draft ถูก auto-submit เข้า DOA | 0 |
| ATP ถูกหัก hold/reserved ซ้ำ | 0 |

## 3. ขอบเขต

### 3.1 ในขอบเขต

- ตั้ง Min, Max, Safety Stock, Lead Time, ADU Window, Pack Size, Preferred Vendor และวันที่เริ่มใช้ต่อสินค้า×คลัง
- เก็บนโยบายเป็น version และรักษาประวัติแบบ append-only
- อ่าน ATP, ADU และ On-Order จาก contract ของ F009 โดยใช้ ATP สำเร็จรูป
- ประเมินอัตโนมัติทุกวัน 06:00 ต่อ tenant และเมื่อ movement ทำให้ ATP เปลี่ยน
- แสดงสถานะ ต่ำกว่าจุด / ใกล้จุด / ปกติ พร้อมที่มาของตัวเลข
- ส่ง Notification แบบ idempotent
- สร้าง F072 PR Draft อัตโนมัติ รวมหนึ่งใบต่อคลังต่อรอบ และไม่แบ่งตาม vendor
- แสดงเลข PR Draft และสถานะ “รอตรวจสอบและส่งอนุมัติ” ในประวัติ

### 3.2 นอกขอบเขต

- ไม่คำนวณ Quality Hold เองและไม่ query hold แยก
- ไม่สร้าง PO, ไม่เลือก vendor ขั้นสุดท้าย และไม่ทำ Compare Vendors
- ไม่ auto-submit PR เข้า DOA
- ไม่แก้ stock หรือ movement
- ไม่แสดงผลท่อ 7C บนหน้า UI
- ไม่มีเอกสารพิมพ์หรือเลขเอกสารของ F085

## 4. ผู้ใช้งานและสิทธิ์

| บทบาท | ทำได้ | ข้อควบคุม |
|---|---|---|
| ผู้ดูแลนโยบายคลัง | เพิ่ม/แก้นโยบาย | ต้องผ่าน tenant/warehouse scope และ optimistic version |
| นักวางแผนเติมสินค้า | ดูคำแนะนำ รันตรวจ ส่งแจ้งเตือน สร้าง Draft | สร้างได้เฉพาะผลที่ต่ำกว่าจุดและ qty > 0 |
| ผู้ตรวจสอบ | ดูประวัติและเลข Draft | แก้หรือลบประวัติไม่ได้ |
| Scheduler/Movement subscriber | เรียกประเมิน | ต้องใช้ idempotency key |

## 5. เส้นทางธุรกิจ

1. ผู้ดูแลเลือกสินค้าและคลัง แล้วบันทึกนโยบายรุ่นใหม่
2. ระบบประเมินจากรอบ 06:00, movement event หรือ manual run สำหรับทดสอบ
3. ระบบอ่าน snapshot จาก F009 แล้วคำนวณจุดสั่งเติมและจำนวนแนะนำ
4. ถ้าต่ำกว่าจุด ระบบส่ง Notification และสร้าง PR Draft รวมตามคลัง
5. ผู้ใช้เปิดประวัติเพื่อดูเลข Draft แล้วไปตรวจ/แก้และ submit ใน F072 ตาม flow ปกติ

## 6. ข้อมูลธุรกิจ

| กลุ่ม | ข้อมูลสำคัญ | เจ้าของ |
|---|---|---|
| Policy | item, warehouse, min, max, safety, lead time, ADU window, pack size, preferred vendor, effective date, version, enabled | F085 |
| Snapshot | ATP, ADU, On-Order, asOf, snapshotRef | F009 contract |
| Suggestion | ROP, triggered, near, raw qty, rounded qty, reason | F085 |
| PR Draft | prDraftId, warehouse, lines, origin_type, origin_ref, submitted=false | F072 |
| Events | policy saved, suggestion evaluated, notification emitted, PR Draft created | append-only audit |

## 7. กฎธุรกิจ

| ID | กฎ | ประเภท |
|---|---|---|
| BR-01 | หนึ่งนโยบายที่มีผลต่อสินค้า×คลัง×วันที่; การแก้สร้าง version ใหม่ | Fixed |
| BR-02 | `0 ≤ Safety ≤ Min ≤ Max`, Lead Time ≥ 0, Pack Size ≥ 1, ADU Window ∈ {30,60,90} | Fixed |
| BR-03 | ATP มาจาก F009 และรวมผล reserved/hold แล้ว ห้ามหักซ้ำ | Fixed |
| BR-04 | `ROP = max(Min, Safety + ADU × Lead Time)` และ trigger เมื่อ `ATP < ROP` | Fixed ตาม HTML ที่อนุมัติ |
| BR-05 | `raw = max(0, Max + Safety − ATP − On-Order)` แล้วปัดขึ้นตาม Pack Size | Fixed ตาม HTML ที่อนุมัติ |
| BR-06 | ADU นับ DN, เบิกใช้ภายใน, ตัดผลิต; ไม่นับ Transfer, Adjustment ลบ, RTV; ไม่มี history ให้ 0 | Fixed |
| BR-07 | On-Order รวม PO เปิดค้างรับและ PR Draft ที่ยังไม่ปิด | Fixed |
| BR-08 | หนึ่ง PR Draft ต่อคลังต่อ evaluation round; รวมหลายสินค้า; vendor เป็นเพียงข้อเสนอ | Fixed |
| BR-09 | Draft ต้องมี `submitted=false`; คนเป็นผู้ submit เข้า DOA ใน F072 | Fixed |
| BR-10 | ทุกเส้นทาง side effect ต้อง replay-safe และไม่สร้าง event/Draft ซ้ำ | Fixed |

## 8. สถานะและวงจรชีวิต

- Policy: Future → Effective → Superseded โดยไม่แก้ย้อนหลัง
- Suggestion: Normal / Near / Triggered; เป็น derived state ไม่เก็บแทน snapshot
- PR: F085 รับ acknowledgment สถานะ Draft เท่านั้น; lifecycle ต่อจากนั้นเป็นของ F072
- Notification: F085 ส่ง event ให้ ENG-NOTIFY; ผู้รับ ช่องทาง และ template เป็น config กลาง

## 9. หน้าจอ

| Route | หน้าที่ |
|---|---|
| `#/records` | รายการนโยบาย ค้นหา กรอง เรียง เพิ่มและแก้ผ่าน Drawer |
| `#/history` | คำแนะนำ 3 ระดับ รันตรวจ ตรวจคู่ ส่งแจ้งเตือน และสร้าง PR Draft |
| `#/settings` | ประวัติภาษาคน ดูเลข PR Draft และสถานะถัดไปแบบ read-only |

## 10. ข้อยกเว้น

- ไม่มีนโยบาย: แสดงการ์ด “ยังไม่มีนโยบายเติมสินค้า” พร้อมปุ่มเพิ่มนโยบาย
- ไม่มี snapshot: ไม่คำนวณ ไม่แจ้ง และไม่สร้าง Draft
- ค่าไม่ถูกต้อง: แสดง error ใต้ช่องและไม่เขียน version/event
- F072/Notification ไม่พร้อม: แสดง error ที่ retry ได้และไม่แสดงผลสำเร็จ
- replay key เดิม: คืนผลเดิมโดยไม่เพิ่ม event หรือ Draft

## 11. การเชื่อมต่อ

| ทิศทาง | Contract |
|---|---|
| F009 → F085 | ATP/ADU/On-Order snapshot พร้อม asOf; F085 ไม่หัก hold ซ้ำ |
| F085 → ENG-NOTIFY | `reorder_point.triggered` พร้อม policy/snapshot/idempotency refs |
| F085 → F072 | สร้าง PR Draft รวมตามคลัง; `origin_type=reorder_point` และ `origin_ref` |
| F072 → DOA | เกิดหลังคน submit เท่านั้น ไม่ใช่หน้าที่ F085 |
| F072 → F073 | เลือก/เปรียบเทียบ vendor ภายหลัง |

## 12. ผลกระทบ Value Stream

ลดการขาดสต๊อกและงานสร้าง PR ซ้ำ โดยยังคงการตรวจสอบของคนและสายอนุมัติเดิม ไม่มี commitment ทางงบ/เงินสดที่ F085; commitment เกิดใน flow จัดซื้อปลายทาง

## 13. Security และ Audit

- บังคับ tenant/warehouse scope ฝั่ง server
- ตรวจ master reference และสิทธิ์เขียนทุกครั้ง
- version conflict ต้องตอบ 409 ไม่ overwrite
- event/outbox เขียน transaction เดียวกับ policy commit
- ประวัติและ idempotency key ห้ามแก้/ลบ
- log ใช้ actor reference ไม่เปิดเผยชื่อบุคคลเกินจำเป็น

## 14. Declarations

- NTF: `reorder_point.triggered`; ENG-NOTIFY เป็นเจ้าของผู้รับ ช่องทาง และข้อความ
- CSQ: profile ชั่วคราว `CSQ-ROP-01`, event `master.changed`, ท่อ `SecC`, เกิดเมื่อ sensitive config commit สำเร็จเท่านั้น
- ไม่ประกาศ CSQ สำหรับ `rop.threshold_breached` หรือ `rop.pr_draft_created`
- ไม่มี DOA/DOCCFG declaration ของ F085

## 15. Open Questions ที่ไม่บล็อกเอกสารรอบนี้

| OQ | สถานะ/เจ้าของ |
|---|---|
| profile_id และ vocabulary `master.changed` ใน registry กลาง | รอยืนยันกับเจ้าของ F-CSQ-01 ก่อน register |
| `enabled` นับ sensitive change หรือไม่ | Strike |
| F072 รับ `origin_type/origin_ref` รอบใด | เจ้าของ F072 |
| Data Classification ของ Inventory Config | Security/Data owner verify ก่อน production |

## 16. Delivery และ Regression

ลำดับทำ: policy/version → F009 snapshot → formula/status → NTF → grouped F072 Draft → audit/monitoring. Regression ต้องครอบ Item/Warehouse picker, F009 snapshot, F072 idempotency, Notification retry และการซ่อน `.demo-only` ใน production

## 17. Health Checks

ติดตาม policy coverage, snapshot age, evaluation failures, duplicate idempotency key, notification failures, PR Draft failures และจำนวน Draft ที่ค้างตรวจสอบ โดยไม่อ้างตัวเลข production จนกว่าจะมี baseline จริง

## 18. AI Review

ไม่พบ scope conflict หลัง sync มติ PM/BA ล่าสุด ความเสี่ยงที่เหลือเป็น registry/coordination ก่อน deployment ตาม §15 ไม่กระทบการออก FRD และชุดทดสอบ
