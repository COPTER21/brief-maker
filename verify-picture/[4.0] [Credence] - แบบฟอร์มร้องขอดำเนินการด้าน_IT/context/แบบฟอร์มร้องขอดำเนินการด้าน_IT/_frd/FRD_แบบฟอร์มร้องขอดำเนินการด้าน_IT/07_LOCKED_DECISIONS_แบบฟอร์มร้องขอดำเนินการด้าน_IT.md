# 07_LOCKED_DECISIONS — F-TMP-001

## §7.0 Scope Lock — IMMUTABLE (= DECISIONS.lock REQ-TMP-001 · แทนใบเซ็นจนลูกค้าเซ็น · OQ-02)
> โหมดไม่เฝ้า: DEC-01..11 = AI-DEFAULT ทั้งหมด (ตอบตาม unattended-policy) — ต้องยืนยันในใบลงนาม (newfeature-signoff-generator) ก่อน UAT · DEC-12..15 = VALID จาก FORM_SPEC

| DEC | หมวด | มติ | ที่มา | ใช้ที่ |
|---|---|---|---|---|
| DEC-01 | G1 | อนุมัติแล้วไม่เปลี่ยนค่าในระบบ | AI-DEFAULT | html, thai-doc, brd, frd, tests, ntf-declaration |
| DEC-02 | G1 | ไม่ส่งต่อระบบอื่นรอบนี้ (ประกาศ event ไว้ใน FRD แต่ไม่ยิง) | AI-DEFAULT | brd, frd |
| DEC-03 | G2 | สายอนุมัติตั้งที่ DOA กลาง (dynamic) · ค่าเริ่ม 1 ขั้น: role-line-manager · วงเงิน: ไม่มี | AI-DEFAULT | html, doa-declaration, frd, tests |
| DEC-04 | G3 | คำนวณให้อัตโนมัติ ผู้ใช้ปรับได้ · เกินเกณฑ์ = เตือน · วันที่ต้องการส่งมอบ ต้องไม่ก่อนวันที่ขอ (เตือน) · ติ๊กประเภทงาน อื่นๆ ต้องระบุข้อความ · ประเภทงานต้องเลือกอย่างน้อย 1 ข้อ (เลือกได้หลายข้อ ตาม ☐ บนกระดาษ) | AI-DEFAULT | html, thai-doc, brd, frd, tests |
| DEC-05 | G4 | รายการซ้ำ: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย None แถวตามกระดาษ | AI-DEFAULT | html, thai-doc, frd |
| DEC-06 | G5 | ช่องตรงกระดาษ 1:1 · ไม่เพิ่มช่อง (เช่น หมายเหตุ) | AI-DEFAULT | html, thai-doc, brd, frd |
| DEC-07 | G6 | ลายเซ็นแถวล่าง 1 ช่องต่อขั้น DOA · ไม่ใช้ภาพลายมือชื่อ (ข้อความส่งในระบบ/พิจารณาในระบบ) | AI-DEFAULT | thai-doc, html, doccfg-declaration, frd |
| DEC-08 | G7 | ไม่อนุมัติ = กลับเป็นร่าง แก้แล้วส่งใหม่ · ยกเลิกได้โดย owner, admin_role สถานะ draft, pending · ต้องมีเหตุผล | AI-DEFAULT | html, frd, tests, doa-declaration |
| DEC-09 | G8 | มองเห็น: เจ้าของ · ผู้อนุมัติเห็นหลังส่ง · admin role เห็นทั้งหมด | AI-DEFAULT | html, frd, tests |
| DEC-10 | G9 | ออกเลขเมื่อบันทึกครั้งแรก · รหัส ITRS | AI-DEFAULT | doccfg-declaration, html, frd |
| DEC-11 | G10 | ของเสริม (กระดาษไม่มี): แนบไฟล์, ส่งออก CSV | AI-DEFAULT | html, brd, frd, ntf-declaration |
| DEC-12 | VALID | กฎตรวจจากตัวอย่างลูกค้า: revision ให้ doccfg ใส่ค่าเริ่ม Rev.00 · ลูกค้ายืนยัน (พบ: ไม่มี Rev./วันที่มีผลบนกระดาษ (มีแค่ Doc. No.)) | FORM_SPEC | html, frd, tests |
| DEC-13 | VALID | กฎตรวจจากตัวอย่างลูกค้า: แก้คำสะกดเป็น ตำแหน่ง (G5) (พบ: สะกด ตําแหน่ง (ํ + า) ไม่ใช่ สระอำ) | FORM_SPEC | html, frd, tests |
| DEC-14 | VALID | กฎตรวจจากตัวอย่างลูกค้า: วันที่ต้องการส่งมอบ ≥ วันที่ขอ (เตือน) (พบ: กระดาษไม่กำหนดว่าต้องไม่ก่อนวันที่ขอ) | FORM_SPEC | html, frd, tests |
| DEC-15 | VALID | กฎตรวจจากตัวอย่างลูกค้า: ติ๊ก อื่นๆ = ต้องระบุข้อความ (พบ: มีเส้นประให้ระบุเฉพาะตัวเลือก อื่นๆ) | FORM_SPEC | html, frd, tests |

## §7.1 การนำไปใช้ใน FRD
| DEC | ผูกกับ |
|---|---|
| DEC-01/02 | 03 FN-04 (ไม่เปลี่ยนค่า/ไม่ส่งต่อ) · 05 BR-10 · 02 event itrs.approved ไม่ยิง |
| DEC-03 | 03 FN-03 · 05 BR-04 · declarations/ITRS.doa.yaml |
| DEC-04 | 05 BR-01/03 · VR-02/03 |
| DEC-05 | 05 BR-14 |
| DEC-06/13 | 01 §1.3 ป้ายตามกระดาษ · 05 BR-11 |
| DEC-07 | 03 FN-08 sign_rows · 05 BR-08 |
| DEC-08 | 03 FN-05/06 · 05 BR-05 (BR-DOA-03 ปกติ = กลับร่าง) |
| DEC-09 | 01 §1.6 · 05 §5.3 · 06 §6.2 |
| DEC-10 | 03 FN-02 · declarations/ITRS.doccfg.yaml |
| DEC-11 | 01 (แนบไฟล์ · CSV · ไม่มีทำซ้ำ) · 05 BR-13 |
| DEC-12 | 05 BR-12 · print_config.revision |
| DEC-14/15 | 05 EC-01/02 · VR-03 |

## §7.2 Convention deviations
- ช่อง "ITRS." บนกระดาษแสดงเลขที่เต็ม (prefix เดียวกัน) — print-spec §7
- ช่อง "ดำเนินการโดย" ไม่ใช่ขั้น DOA — เป็น action ของ role-it-officer หลังอนุมัติ (print_config sign_boxes: performer)
- role-it-officer ยังไม่อยู่ใน DOA roles contract (OQ-03)
