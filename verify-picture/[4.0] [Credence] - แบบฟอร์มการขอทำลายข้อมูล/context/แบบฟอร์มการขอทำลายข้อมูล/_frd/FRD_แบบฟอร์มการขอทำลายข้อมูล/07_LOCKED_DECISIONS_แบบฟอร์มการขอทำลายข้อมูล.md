# 07_LOCKED_DECISIONS — F-TMP-003

## §7.0 Scope Lock — IMMUTABLE (= DECISIONS.lock REQ-TMP-003 · แทนใบเซ็นจนลูกค้าเซ็น · OQ-02)
> โหมดไม่เฝ้า: DEC-01..11 = AI-DEFAULT ทั้งหมด (ตอบตาม unattended-policy) — ต้องยืนยันในใบลงนาม (newfeature-signoff-generator) ก่อน UAT · DEC-12..17 = VALID จาก FORM_SPEC

| DEC | หมวด | มติ | ที่มา | ใช้ที่ |
|---|---|---|---|---|
| DEC-01 | G1 | อนุมัติแล้วไม่เปลี่ยนค่าในระบบ | AI-DEFAULT | html, thai-doc, brd, frd, tests, ntf-declaration |
| DEC-02 | G1 | ไม่ส่งต่อระบบอื่นรอบนี้ (ประกาศ event ไว้ใน FRD แต่ไม่ยิง) | AI-DEFAULT | brd, frd |
| DEC-03 | G2 | สายอนุมัติตั้งที่ DOA กลาง (dynamic) · ค่าเริ่ม 2 ขั้น: role-line-manager, role-mgr-it · วงเงิน: ไม่มี | AI-DEFAULT | html, doa-declaration, frd, tests |
| DEC-04 | G3 | คำนวณให้อัตโนมัติ ผู้ใช้ปรับได้ · เกินเกณฑ์ = เตือน · ช่วงเวลาของข้อมูล ถึง ต้องไม่ก่อน จาก (บังคับ) · ช่วงเวลาของข้อมูล ถึง ไม่ควรเกินวันที่ขอ (เตือน) · ติ๊ก อื่นๆ(โปรดระบุ) ในเหตุผล/วิธีการ ต้องระบุข้อความ · ประเภทข้อมูล · เหตุผล · วิธีการ ต้องเลือกอย่างน้อย 1 ข้อต่อกลุ่ม (เลือกได้หลายข้อ ตาม ☐ บนกระดาษ) | AI-DEFAULT | html, thai-doc, brd, frd, tests |
| DEC-05 | G4 | รายการซ้ำ: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย None แถวตามกระดาษ | AI-DEFAULT | html, thai-doc, frd |
| DEC-06 | G5 | ช่องตรงกระดาษ 1:1 · ไม่เพิ่มช่อง (เช่น หมายเหตุ) | AI-DEFAULT | html, thai-doc, brd, frd |
| DEC-07 | G6 | ลายเซ็นแถวล่าง 1 ช่องต่อขั้น DOA · ไม่ใช้ภาพลายมือชื่อ (ข้อความส่งในระบบ/พิจารณาในระบบ) | AI-DEFAULT | thai-doc, html, doccfg-declaration, frd |
| DEC-08 | G7 | ไม่อนุมัติ = กลับเป็นร่าง แก้แล้วส่งใหม่ · ยกเลิกได้โดย owner, admin_role สถานะ draft, pending · ต้องมีเหตุผล | AI-DEFAULT | html, frd, tests, doa-declaration |
| DEC-09 | G8 | มองเห็น: เจ้าของ · ผู้อนุมัติเห็นหลังส่ง · admin role เห็นทั้งหมด | AI-DEFAULT | html, frd, tests |
| DEC-10 | G9 | ออกเลขเมื่อบันทึกครั้งแรก · รหัส DRITS | AI-DEFAULT | doccfg-declaration, html, frd |
| DEC-11 | G10 | ของเสริม (กระดาษไม่มี): แนบไฟล์, ส่งออก CSV | AI-DEFAULT | html, brd, frd, ntf-declaration |
| DEC-12 | VALID | กฎตรวจจากตัวอย่างลูกค้า: แก้คำสะกดเป็น ตำแหน่ง (G5) (พบ: สะกด ตําแหน่ง (ํ + า) ไม่ใช่ สระอำ) | FORM_SPEC | html, frd, tests |
| DEC-13 | VALID | กฎตรวจจากตัวอย่างลูกค้า: แก้คำสะกดเป็น อนุมัติ (G5) (พบ: สะกด อนุมัมติ) | FORM_SPEC | html, frd, tests |
| DEC-14 | VALID | กฎตรวจจากตัวอย่างลูกค้า: แสดง ☐ ครบทุกตัวเลือก (พบ: ตัวเลือก เข้ารหัสและทำลายข้อมูลอย่างปลอดภัย ไม่มี ☐ ในไฟล์ต้นฉบับ (Excel checkbox ขาด 1 ตัว)) | FORM_SPEC | html, frd, tests |
| DEC-15 | VALID | กฎตรวจจากตัวอย่างลูกค้า: ถึง ≥ จาก (บังคับ) · ถึง ไม่เกินวันที่ขอ (เตือน) (พบ: กระดาษไม่กำหนดว่า ถึง ต้องไม่ก่อน จาก) | FORM_SPEC | html, frd, tests |
| DEC-16 | VALID | กฎตรวจจากตัวอย่างลูกค้า: ติ๊ก อื่นๆ = ต้องระบุข้อความ (พบ: มีเส้นให้ระบุเฉพาะตัวเลือก อื่นๆ) | FORM_SPEC | html, frd, tests |
| DEC-17 | VALID | กฎตรวจจากตัวอย่างลูกค้า: เลือกอย่างน้อย 1 ต่อกลุ่ม (พบ: กระดาษไม่บอกว่าต้องเลือกอย่างน้อย 1) | FORM_SPEC | html, frd, tests |

## §7.1 การนำไปใช้ใน FRD
| DEC | ผูกกับ |
|---|---|
| DEC-01/02 | 03 FN-04 (ไม่เปลี่ยนค่า/ไม่ส่งต่อ) · 05 BR-11 · 02 event drits.destroyed ไม่ยิง |
| DEC-03 | 03 FN-03 · 05 BR-05 · declarations/DRITS.doa.yaml (2 ขั้น) |
| DEC-04 | 05 BR-01/04 · VR-03/06/08 |
| DEC-05 | 05 BR-15 |
| DEC-06/12/13/14 | 01 §1.3 ป้ายตามกระดาษ · 05 BR-12 |
| DEC-07 | 03 FN-08 sign_rows · 05 BR-09 |
| DEC-08 | 03 FN-05/06 · 05 BR-06 (BR-DOA-03 ปกติ = กลับร่าง) |
| DEC-09 | 01 §1.6 · 05 §5.3 · 06 §6.2 |
| DEC-10 | 03 FN-02 · 05 BR-07/13 · declarations/DRITS.doccfg.yaml |
| DEC-11 | 01 (แนบไฟล์ · CSV · ไม่มีทำซ้ำ) · 05 BR-14 |
| DEC-15 | 05 BR-03/04 · VR-05 · EC-01/02 |
| DEC-16 | 05 BR-02 · VR-07/09 · EC-03 |
| DEC-17 | 05 BR-01 · VR-03/06/08 |

## §7.2 Convention deviations
- ช่อง "DRITS." บนกระดาษแสดงเลขที่เต็ม (prefix เดียวกัน) — print-spec §7
- ช่อง "เจ้าหน้าที่ IT" ไม่ใช่ขั้น DOA — เป็น action ของ role-it-officer หลังอนุมัติ (print_config sign_boxes: performer) · บนกระดาษวางก่อนช่อง อนุมัติ แต่แบบพิมพ์ในระบบวางท้ายสุด (ขั้น DOA ต่อเนื่อง) → OQ-04
- role-mgr-it · role-it-officer ยังไม่อยู่ใน DOA roles contract (OQ-03)
