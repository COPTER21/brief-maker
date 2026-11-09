# 07_LOCKED_DECISIONS — F-TMP-005

## §7.0 Scope Lock — IMMUTABLE (= DECISIONS.lock REQ-TMP-005 · แทนใบเซ็นจนลูกค้าเซ็น · OQ-02)
> โหมดไม่เฝ้า: DEC-01..11 = AI-DEFAULT ทั้งหมด (ตอบตาม unattended-policy) — ต้องยืนยันในใบลงนาม (newfeature-signoff-generator) ก่อน UAT · DEC-12..17 = VALID จาก FORM_SPEC

| DEC | หมวด | มติ | ที่มา | ใช้ที่ |
|---|---|---|---|---|
| DEC-01 | G1 | อนุมัติแล้วไม่เปลี่ยนค่าในระบบ | AI-DEFAULT | html, thai-doc, brd, frd, tests, ntf-declaration |
| DEC-02 | G1 | ไม่ส่งต่อระบบอื่นรอบนี้ (ประกาศ event ไว้ใน FRD แต่ไม่ยิง) | AI-DEFAULT | brd, frd |
| DEC-03 | G2 | สายอนุมัติตั้งที่ DOA กลาง (dynamic) · ค่าเริ่ม 2 ขั้น: role-line-manager, role-mgr-it · วงเงิน: ไม่มี | AI-DEFAULT | html, doa-declaration, frd, tests |
| DEC-04 | G3 | คำนวณให้อัตโนมัติ ผู้ใช้ปรับได้ · เกินเกณฑ์ = เตือน · วันที่ต้องการส่งมอบ ต้องไม่ก่อนวันที่ขอ (เตือน) · ประเภทของการเปลี่ยนแปลง เลือกอย่างน้อย 1 ข้อ เลือกได้หลายข้อ (บล็อก) · ติ๊กประเภท อื่นๆ ต้องระบุข้อความ (บล็อก) | AI-DEFAULT | html, thai-doc, brd, frd, tests |
| DEC-05 | G4 | รายการซ้ำ: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย None แถวตามกระดาษ | AI-DEFAULT | html, thai-doc, frd |
| DEC-06 | G5 | ช่องตรงกระดาษ 1:1 · ไม่เพิ่มช่อง (เช่น หมายเหตุ) | AI-DEFAULT | html, thai-doc, brd, frd |
| DEC-07 | G6 | ลายเซ็นแถวล่าง 1 ช่องต่อขั้น DOA · ไม่ใช้ภาพลายมือชื่อ (ข้อความส่งในระบบ/พิจารณาในระบบ) | AI-DEFAULT | thai-doc, html, doccfg-declaration, frd |
| DEC-08 | G7 | ไม่อนุมัติ = กลับเป็นร่าง แก้แล้วส่งใหม่ · ยกเลิกได้โดย owner, admin_role สถานะ draft, pending · ต้องมีเหตุผล | AI-DEFAULT | html, frd, tests, doa-declaration |
| DEC-09 | G8 | มองเห็น: เจ้าของ · ผู้อนุมัติเห็นหลังส่ง · admin role เห็นทั้งหมด | AI-DEFAULT | html, frd, tests |
| DEC-10 | G9 | ออกเลขเมื่อบันทึกครั้งแรก · รหัส ITCR | AI-DEFAULT | doccfg-declaration, html, frd |
| DEC-11 | G10 | ของเสริม (กระดาษไม่มี): แนบไฟล์, ส่งออก CSV | AI-DEFAULT | html, brd, frd, ntf-declaration |
| DEC-12 | VALID | กฎตรวจจากตัวอย่างลูกค้า: แก้คำสะกดเป็น ตำแหน่ง (G5) (พบ: สะกด ตําแหน่ง (ํ + า)) | FORM_SPEC | html, frd, tests |
| DEC-13 | VALID | กฎตรวจจากตัวอย่างลูกค้า: คงคำตามกระดาษ (G5 1:1) · บันทึก OQ ลูกค้าว่าควรเป็น ผู้ขอ/ผู้ร้องขอ หรือไม่ (พบ: ป้าย ผู้ขอซื้อ ไม่ตรงกับเอกสาร Change Request (ไม่ใช่การขอซื้อ)) | FORM_SPEC | html, frd, tests |
| DEC-14 | VALID | กฎตรวจจากตัวอย่างลูกค้า: วันที่ต้องการส่งมอบ ≥ วันที่ขอ (เตือน) (พบ: กระดาษไม่กำหนดว่าต้องไม่ก่อนวันที่ขอ) | FORM_SPEC | html, frd, tests |
| DEC-15 | VALID | กฎตรวจจากตัวอย่างลูกค้า: ติ๊ก อื่นๆ = ต้องระบุข้อความ (พบ: มีเส้นให้ระบุเฉพาะตัวเลือก อื่นๆ) | FORM_SPEC | html, frd, tests |
| DEC-16 | VALID | กฎตรวจจากตัวอย่างลูกค้า: เลือกอย่างน้อย 1 ข้อ (บล็อก) (พบ: กระดาษไม่ระบุว่าเลือกได้กี่ข้อ) | FORM_SPEC | html, frd, tests |
| DEC-17 | VALID | กฎตรวจจากตัวอย่างลูกค้า: ระบบออกเลขตามมาตรฐาน (G9) แสดงที่ footer แบบพิมพ์ + หัวหน้าจอ — ไม่ใช่ช่องกรอก ไม่เพิ่มแถวในตาราง (G5) (พบ: กระดาษไม่มีช่องเลขที่) | FORM_SPEC | html, frd, tests |

## §7.1 การนำไปใช้ใน FRD
| DEC | ผูกกับ |
|---|---|
| DEC-01/02 | 03 FN-04 (ไม่เปลี่ยนค่า/ไม่ส่งต่อ) · 05 BR-09 · 02 event itcr.approved ไม่ยิง |
| DEC-03 | 03 FN-03 · 05 BR-04 · declarations/ITCR.doa.yaml (2 ขั้น ตรวจสอบโดย → อนุมัติโดย) |
| DEC-04 | 05 BR-01/03 · VR-02 |
| DEC-05 | 05 BR-13 |
| DEC-06/12/13/17 | 01 §1.3 ป้ายตามกระดาษ · 05 BR-10 |
| DEC-07 | 03 FN-07 sign_rows · 05 BR-08 |
| DEC-08 | 03 FN-05/06 · 05 BR-05 (BR-DOA-03 ปกติ = กลับร่าง) |
| DEC-09 | 01 §1.6 · 05 §5.3 · 06 §6.2 |
| DEC-10 | 03 FN-02 · 05 BR-06/11 · declarations/ITCR.doccfg.yaml |
| DEC-11 | 01 (แนบไฟล์ · CSV · ไม่มีทำซ้ำ) · 05 BR-12 |
| DEC-14 | 05 BR-03 · EC-01 |
| DEC-15 | 05 BR-02 · VR-03 · EC-02 |
| DEC-16 | 05 BR-01 · VR-02 · EC-03 |

## §7.2 Convention deviations
- กระดาษไม่มีช่องเลขที่ — แสดงเลข ITCR ที่ footer แบบพิมพ์ + หัว drawer (DEC-17)
- ป้ายลงชื่อ "ผู้ขอซื้อ" คงตามกระดาษ แม้ไม่ใช่การขอซื้อ (DEC-13 · OQ-05)
- role-mgr-it · role-it-officer ยังไม่อยู่ใน DOA roles contract (OQ-03)
