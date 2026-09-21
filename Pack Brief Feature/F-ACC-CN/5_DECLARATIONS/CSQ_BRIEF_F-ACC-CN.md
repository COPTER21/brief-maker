# CSQ_BRIEF — F-ACC-CN Credit Note
## 1. Identity: CSQ-ACC-CN [DEFAULT] · F-ACC-CN · Accounting/AR · กลุ่ม B · v1.0
## 2. Declared Events
| event_id | trigger | ท่อ | เงื่อนไข | payload |
|---|---|---|---|---|
| ar_cn.approved | pending→approved (BR-09) | **AC** | ทุกใบ | cn_id, cn_no, inv_no, customer_code, reason_code, base_amount, vat_amount, grand_total, cn_date |
| ar_cn.approved | (เดียวกัน) | **EC** kind=actual | reason ∈ {DISC, PRICE} (รายได้ที่ลดจริงจากการให้ส่วนลด/แก้ราคา) | reason_code, base_amount |
## 3. ท่อที่ไม่ประกาศ: OC (OP) · DC (DOA engine ยิงเอง) · SC (สงวน) · FC (เงินสดไม่เปลี่ยนตอนลดหนี้) · SecC (no-effect)
## 4. Payload: จาก entity credit_note (BRD §6) · tax id ลูกค้าบุคคล = mask
## 5. Register Checklist: entity fields · emit ใน transaction อนุมัติ · Profile Registry เชื่อมแล้ว
## 6. OQ: CSQ-OQ-CN-1 EC สำหรับ DISC/PRICE ควรนับไหม [DEFAULT — รอยืนยัน] — Strike
