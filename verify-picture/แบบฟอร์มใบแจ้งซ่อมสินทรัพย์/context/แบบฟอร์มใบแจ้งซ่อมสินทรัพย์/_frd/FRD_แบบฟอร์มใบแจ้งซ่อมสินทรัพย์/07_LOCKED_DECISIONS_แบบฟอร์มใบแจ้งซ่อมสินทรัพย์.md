# 07_LOCKED_DECISIONS — F-TMP-001

## §7.0 Scope Lock — IMMUTABLE (= DECISIONS.lock REQ-TMP-001 · แทนใบเซ็นจนลูกค้าเซ็น · OQ-02)
> โหมดไม่เฝ้า: AI-DEFAULT 12 ข้อ (DEC-01..12) ต้องให้ลูกค้ายืนยันในใบลงนาม (newfeature-signoff-generator) ก่อน UAT · VALID 4 ข้อ (DEC-13..16) จากข้อมูลตัวอย่างบนกระดาษ

| DEC | หมวด | มติ | ที่มา | ใช้ที่ |
|---|---|---|---|---|
| DEC-01 | G1 | อนุมัติแล้วไม่เปลี่ยนค่าในระบบ | AI-DEFAULT | html, thai-doc, brd, frd, tests, ntf-declaration |
| DEC-02 | G1 | ไม่ส่งต่อระบบอื่นรอบนี้ (ประกาศ event ไว้ใน FRD แต่ไม่ยิง) | AI-DEFAULT | brd, frd |
| DEC-03 | G2 | สายอนุมัติตั้งที่ DOA กลาง (dynamic) · ค่าเริ่ม 2 ขั้น: role-line-manager, role-mgr-acc · วงเงิน: ไม่มี | AI-DEFAULT | html, doa-declaration, frd, tests |
| DEC-04 | G3 | คำนวณให้อัตโนมัติ ผู้ใช้ปรับได้ · เกินเกณฑ์ = เตือน · ต้องมีรายการแจ้งซ่อมอย่างน้อย 1 แถว · จำนวน > 0 · ทะเบียนสินทรัพย์ = ผู้ใช้กรอกเลขเอง (Asset Master ยังไม่มีในระบบ) · เปลี่ยนเป็นเลือกจาก Asset Master เมื่อ feature พร้อม · ประวัติการซ่อม = ผู้ตรวจสอบกรอกตอนพิจารณา (ไม่บังคับ) · ผู้แจ้งซ่อมบันทึกครั้งเดียวตอนส่ง แสดงทั้ง 2 จุดบนแบบพิมพ์ | AI-DEFAULT | html, thai-doc, brd, frd, tests |
| DEC-05 | G4 | รายการทรัพย์สินที่แจ้งซ่อม: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 10 แถวตามกระดาษ | AI-DEFAULT | html, thai-doc, frd |
| DEC-06 | G4 | ประวัติการซ่อม: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 6 แถวตามกระดาษ | AI-DEFAULT | html, thai-doc, frd |
| DEC-07 | G5 | ช่องตรงกระดาษ 1:1 · ไม่เพิ่มช่อง (เช่น หมายเหตุ) | AI-DEFAULT | html, thai-doc, brd, frd |
| DEC-08 | G6 | ลายเซ็นแถวล่าง 1 ช่องต่อขั้น DOA · ไม่ใช้ภาพลายมือชื่อ (ข้อความส่งในระบบ/พิจารณาในระบบ) | AI-DEFAULT | thai-doc, html, doccfg-declaration, frd |
| DEC-09 | G7 | ไม่อนุมัติ = กลับเป็นร่าง แก้แล้วส่งใหม่ · ยกเลิกได้โดย owner, admin_role สถานะ draft, pending · ต้องมีเหตุผล | AI-DEFAULT | html, frd, tests, doa-declaration |
| DEC-10 | G8 | มองเห็น: เจ้าของ · ผู้อนุมัติเห็นหลังส่ง · admin role เห็นทั้งหมด | AI-DEFAULT | html, frd, tests |
| DEC-11 | G9 | ออกเลขเมื่อบันทึกครั้งแรก · รหัส RPR | AI-DEFAULT | doccfg-declaration, html, frd |
| DEC-12 | G10 | ของเสริม (กระดาษไม่มี): แนบไฟล์, ส่งออก CSV | AI-DEFAULT | html, brd, frd, ntf-declaration |
| DEC-13 | VALID | กฎตรวจจากตัวอย่างลูกค้า: ระบบบันทึกผู้แจ้งครั้งเดียวตอนส่ง แล้วแสดงทั้ง 2 จุดบนแบบพิมพ์ (พบ: ผู้แจ้งซ่อมลงชื่อ 2 จุด (ใต้ตารางรายการ + แถวลงชื่อล่าง)) | FORM_SPEC | html, frd, tests |
| DEC-14 | VALID | กฎตรวจจากตัวอย่างลูกค้า: ผลพิจารณามาจาก DOA · ไม่อนุมัติต้องใส่เหตุผล (พบ: ไม่มี ☐ อนุมัติ/ไม่อนุมัติ บนกระดาษ) | FORM_SPEC | html, frd, tests |
| DEC-15 | VALID | กฎตรวจจากตัวอย่างลูกค้า: ต้องมีรายการอย่างน้อย 1 แถว · จำนวน > 0 (พบ: แถวรายการว่างทั้งหมด (ไม่มีข้อมูลตัวอย่าง)) | FORM_SPEC | html, frd, tests |
| DEC-16 | VALID | กฎตรวจจากตัวอย่างลูกค้า: คงถ้อยคำตามกระดาษ (G5 1:1) (พบ: หัวกระดาษใช้ 'สินทรัพย์' แต่ข้อความใช้ 'ทรัพย์สิน') | FORM_SPEC | html, frd, tests |


## §7.1 ผูกกับ FRD
| DEC | ใช้ที่ |
|---|---|
| DEC-01/02 | 05 BR-12 · 02 §2.4 (rpr.approved ไม่ยิง) |
| DEC-03 | 03 FN-04 · 05 BR-05/BR-09 · declarations/DOA_BRIEF |
| DEC-04 | 05 BR-03/BR-04 · 03 FN-02 |
| DEC-05/06 | 03 FN-08 (min_rows_by_group) |
| DEC-07/16 | 01 §1.2 ป้ายตามกระดาษ · 05 BR-11 |
| DEC-08 | 05 BR-09 · 03 FN-08 |
| DEC-09 | 05 BR-06 / BR-DOA-03 · 03 FN-06/FN-07 |
| DEC-10 | 05 §5.3 · 06 §6.2 |
| DEC-11 | 03 FN-03 · declarations/DOCCFG_BRIEF |
| DEC-12 | 05 BR-13 |
| DEC-13 | 05 BR-10 · 03 FN-08 |
| DEC-14 | 05 VR-04 |
| DEC-15 | 05 BR-01/02 · VR-01/02 |
