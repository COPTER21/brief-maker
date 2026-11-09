# 07_LOCKED_DECISIONS — F-TMP-004

## §7.0 Scope Lock — IMMUTABLE (= DECISIONS.lock REQ-TMP-004 · แทนใบเซ็นจนลูกค้าเซ็น · OQ-02)
> โหมดไม่เฝ้า: DEC-01..11 = AI-DEFAULT ทั้งหมด (ตอบตาม unattended-policy) — ต้องยืนยันในใบลงนาม (newfeature-signoff-generator) ก่อน UAT · DEC-12..18 = VALID จาก FORM_SPEC

| DEC | หมวด | มติ | ที่มา | ใช้ที่ |
|---|---|---|---|---|
| DEC-01 | G1 | อนุมัติแล้วไม่เปลี่ยนค่าในระบบ | AI-DEFAULT | html, thai-doc, brd, frd, tests, ntf-declaration |
| DEC-02 | G1 | ไม่ส่งต่อระบบอื่นรอบนี้ (ประกาศ event ไว้ใน FRD แต่ไม่ยิง) | AI-DEFAULT | brd, frd |
| DEC-03 | G2 | สายอนุมัติตั้งที่ DOA กลาง (dynamic) · ค่าเริ่ม 1 ขั้น: role-line-manager · วงเงิน: ไม่มี | AI-DEFAULT | html, doa-declaration, frd, tests |
| DEC-04 | G3 | คำนวณให้อัตโนมัติ ผู้ใช้ปรับได้ · เกินเกณฑ์ = เตือน · วันที่ต้องการส่งมอบ ต้องไม่ก่อนวันที่แจ้ง (เตือน) · ติ๊กประเภท อื่นๆ ต้องระบุข้อความ · เลือกประเภทได้ 1 ข้อ (1 ใบ = 1 อุปกรณ์) · ผลตรวจเช็คแบบส่งบริษัท/สั่งซื้อ ต้องกรอก ระยะเวลา-ถึง · ร้านค้า · วันที่ส่งเคลม · ถึง ≥ ระยะเวลา (เตือน) · ผลการซ่อม ไม่สามารถแก้ไขได้ ต้องระบุรายละเอียด | AI-DEFAULT | html, thai-doc, brd, frd, tests |
| DEC-05 | G4 | รายการซ้ำ: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย None แถวตามกระดาษ | AI-DEFAULT | html, thai-doc, frd |
| DEC-06 | G5 | ช่องตรงกระดาษ 1:1 · ไม่เพิ่มช่อง (เช่น หมายเหตุ) | AI-DEFAULT | html, thai-doc, brd, frd |
| DEC-07 | G6 | ลายเซ็นแถวล่าง 1 ช่องต่อขั้น DOA · ไม่ใช้ภาพลายมือชื่อ (ข้อความส่งในระบบ/พิจารณาในระบบ) | AI-DEFAULT | thai-doc, html, doccfg-declaration, frd |
| DEC-08 | G7 | ไม่อนุมัติ = กลับเป็นร่าง แก้แล้วส่งใหม่ · ยกเลิกได้โดย owner, admin_role สถานะ draft, pending · ต้องมีเหตุผล | AI-DEFAULT | html, frd, tests, doa-declaration |
| DEC-09 | G8 | มองเห็น: เจ้าของ · ผู้อนุมัติเห็นหลังส่ง · admin role เห็นทั้งหมด | AI-DEFAULT | html, frd, tests |
| DEC-10 | G9 | ออกเลขเมื่อบันทึกครั้งแรก · รหัส CRR | AI-DEFAULT | doccfg-declaration, html, frd |
| DEC-11 | G10 | ของเสริม (กระดาษไม่มี): แนบไฟล์, ส่งออก CSV | AI-DEFAULT | html, brd, frd, ntf-declaration |
| DEC-12 | VALID | กฎตรวจจากตัวอย่างลูกค้า: แก้คำสะกดเป็น ตำแหน่ง (G5) (พบ: สะกด ตําแหน่ง (ํ + า)) | FORM_SPEC | html, frd, tests |
| DEC-13 | VALID | กฎตรวจจากตัวอย่างลูกค้า: แก้เป็น ส่งเคลม (G5) (พบ: สะกด ส่งเครม (3 จุด) ขณะที่บรรทัดถัดไปสะกด ส่งเคลม) | FORM_SPEC | html, frd, tests |
| DEC-14 | VALID | กฎตรวจจากตัวอย่างลูกค้า: แก้เป็น สั่งซื้อ (G5) (พบ: สะกด สั้งซื้อ) | FORM_SPEC | html, frd, tests |
| DEC-15 | VALID | กฎตรวจจากตัวอย่างลูกค้า: คงคำตามกระดาษ (G5 1:1) · บันทึกเป็นคำถามลูกค้า (OQ) ว่าควรเป็น ร้านค้าที่สั่งซื้อ/วันที่สั่งซื้อ หรือไม่ (พบ: บรรทัดใต้ตัวเลือกใช้คำ ร้านค้าที่ส่งเคลม / วันที่ส่งเคลม เหมือน 2 ตัวเลือกบน (น่าจะคัดลอกมา) แต่กรณีสั่งซื้อไม่ใช่การเคลม) | FORM_SPEC | html, frd, tests |
| DEC-16 | VALID | กฎตรวจจากตัวอย่างลูกค้า: ถึง ≥ ระยะเวลา (เตือน) (พบ: กระดาษไม่กำหนดว่าวันสิ้นสุดต้องไม่ก่อนวันเริ่ม) | FORM_SPEC | html, frd, tests |
| DEC-17 | VALID | กฎตรวจจากตัวอย่างลูกค้า: วันที่ต้องการส่งมอบ ≥ วันที่แจ้ง (เตือน) (พบ: กระดาษไม่กำหนดว่าต้องไม่ก่อนวันที่แจ้ง) | FORM_SPEC | html, frd, tests |
| DEC-18 | VALID | กฎตรวจจากตัวอย่างลูกค้า: ติ๊ก อื่นๆ = ต้องระบุข้อความ (พบ: มีเส้นประให้ระบุเฉพาะตัวเลือก อื่นๆ) | FORM_SPEC | html, frd, tests |

## §7.1 การนำไปใช้ใน FRD
| DEC | ผูกกับ |
|---|---|
| DEC-01/02 | 03 FN-07 (ไม่เปลี่ยนค่า/ไม่ส่งต่อ) · 05 BR-12 · 02 event crr.closed ไม่ยิง |
| DEC-03 | 03 FN-06 · 05 BR-05 · declarations/CRR.doa.yaml |
| DEC-04 | 05 BR-01/03/04/11 · VR-01/09/12 |
| DEC-05 | 05 BR-16 |
| DEC-06/12/13/14/15 | 01 §1.3/§1.5 ป้ายตามกระดาษ · 05 BR-13 · OQ-04 (DEC-15) |
| DEC-07 | 03 FN-12 sign_rows · 05 BR-09/14 |
| DEC-08 | 03 FN-08/11 · 05 BR-06 (BR-DOA-03 = กลับร่างผลตรวจเช็ค inspecting) |
| DEC-09 | 01 §1.7 · 05 §5.3 · 06 §6.2 |
| DEC-10 | 03 FN-02 · declarations/CRR.doccfg.yaml |
| DEC-11 | 01 (แนบไฟล์ · CSV · ไม่มีทำซ้ำ) · 05 BR-15 |
| DEC-16/17/18 | 05 EC-01/02/04 · VR-02 · BR-03 |

## §7.2 Convention deviations
- ช่อง "อนุมัติโดย" อยู่ในส่วนที่ 2 ของกระดาษ (อนุมัติผลตรวจเช็คของ IT) → DOA ส่งจาก `inspecting` (= ร่างผลตรวจเช็ค) ไม่ใช่ draft ของผู้แจ้ง · ไม่อนุมัติกลับ `inspecting` เลขเดิม (DEC-08)
- role-line-manager resolve จากผู้ส่งอนุมัติ (เจ้าหน้าที่ IT) ไม่ใช่ผู้แจ้งซ่อม
- ช่อง ผู้แจ้งซ่อม/ผู้รับแจ้ง/ผู้ดำเนินการ ไม่ใช่ขั้น DOA — เป็น action ตามสถานะ (print_config sign_boxes: reporter · receiver · inspector · repairer · acknowledger)
- แบบพิมพ์ 2 หน้า (R10) แม้ต้นฉบับ 1 หน้า — print-spec §1
- role-it-officer ยังไม่อยู่ใน DOA roles contract (OQ-03)
