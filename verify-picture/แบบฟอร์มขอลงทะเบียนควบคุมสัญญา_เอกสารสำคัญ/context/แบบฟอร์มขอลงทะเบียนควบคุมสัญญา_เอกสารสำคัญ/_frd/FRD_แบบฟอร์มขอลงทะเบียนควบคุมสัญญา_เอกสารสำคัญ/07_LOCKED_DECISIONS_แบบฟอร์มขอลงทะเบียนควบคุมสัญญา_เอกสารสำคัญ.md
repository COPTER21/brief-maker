# 07_LOCKED_DECISIONS — F-TMP-009

## §7.0 Scope Lock — IMMUTABLE (= DECISIONS.lock REQ-TMP-009 · แทนใบเซ็นจนลูกค้าเซ็น · OQ-02)
> โหมดไม่เฝ้า: มติ G1–G10 เป็น AI-DEFAULT ทั้งหมด (11 ข้อ) + VALID จาก FORM_SPEC 3 ข้อ — ต้องให้ลูกค้ายืนยันในใบลงนาม (newfeature-signoff-generator) ก่อน UAT

| DEC | หมวด | มติ | ที่มา | ใช้ที่ |
|---|---|---|---|---|
| DEC-01 | G1 | อนุมัติแล้วไม่เปลี่ยนค่าในระบบ | AI-DEFAULT | html, thai-doc, brd, frd, tests, ntf-declaration |
| DEC-02 | G1 | ไม่ส่งต่อระบบอื่นรอบนี้ (ประกาศ event ไว้ใน FRD แต่ไม่ยิง) | AI-DEFAULT | brd, frd |
| DEC-03 | G2 | สายอนุมัติตั้งที่ DOA กลาง (dynamic) · ค่าเริ่ม 2 ขั้น: role-line-manager, role-compliance · วงเงิน: ไม่มี | AI-DEFAULT | html, doa-declaration, frd, tests |
| DEC-04 | G3 | คำนวณให้อัตโนมัติ ผู้ใช้ปรับได้ · เกินเกณฑ์ = เตือน · วันที่สิ้นสุดสัญญาต้องไม่ก่อนวันที่เริ่มต้น · เลือกจุดประสงค์ แก้ไข/เปลี่ยนแปลง ต้องระบุสาเหตุ | AI-DEFAULT | html, thai-doc, brd, frd, tests |
| DEC-05 | G4 | รายการซ้ำ: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย None แถวตามกระดาษ | AI-DEFAULT | html, thai-doc, frd |
| DEC-06 | G5 | ช่องตรงกระดาษ 1:1 · ไม่เพิ่มช่อง (เช่น หมายเหตุ) · รวม/แยก: วันที่เริ่มต้นและสิ้นสุดสัญญา = เก็บ 2 ค่า (เริ่ม/สิ้นสุด) แสดงบรรทัดเดียวตามกระดาษ | AI-DEFAULT | html, thai-doc, brd, frd |
| DEC-07 | G6 | ลายเซ็นแถวล่าง 1 ช่องต่อขั้น DOA · ไม่ใช้ภาพลายมือชื่อ (ข้อความส่งในระบบ/พิจารณาในระบบ) | AI-DEFAULT | thai-doc, html, doccfg-declaration, frd |
| DEC-08 | G7 | ไม่อนุมัติ = กลับเป็นร่าง แก้แล้วส่งใหม่ · ยกเลิกได้โดย owner, admin_role สถานะ draft, pending · ต้องมีเหตุผล | AI-DEFAULT | html, frd, tests, doa-declaration |
| DEC-09 | G8 | มองเห็น: เจ้าของ · ผู้อนุมัติเห็นหลังส่ง · admin role เห็นทั้งหมด | AI-DEFAULT | html, frd, tests |
| DEC-10 | G9 | ออกเลขเมื่อบันทึกครั้งแรก · รหัส CTR | AI-DEFAULT | doccfg-declaration, html, frd |
| DEC-11 | G10 | ของเสริม (กระดาษไม่มี): แนบไฟล์, ส่งออก CSV | AI-DEFAULT | html, brd, frd, ntf-declaration |
| DEC-12 | VALID | กฎตรวจจากตัวอย่างลูกค้า: คง 1:1 ตาม G5 — ผู้ขอระบุในไฟล์แนบ/ชื่อเรื่อง (OQ ให้ลูกค้ายืนยันว่าต้องเพิ่มช่องระบุไหม) (พบ: ไม่มีเส้นให้ระบุชื่อเอกสาร) | FORM_SPEC | html, frd, tests |
| DEC-13 | VALID | กฎตรวจจากตัวอย่างลูกค้า: คง 1:1 — ผู้ดูแลสัญญาค้นทะเบียนเดิมเอง (OQ) (พบ: กระดาษไม่มีช่องอ้างอิงเลขทะเบียนสัญญาเดิม) | FORM_SPEC | html, frd, tests |
| DEC-14 | VALID | กฎตรวจจากตัวอย่างลูกค้า: สิ้นสุด ≥ เริ่มต้น (validation) (พบ: บรรทัดเดียวแต่มี 2 ค่า) | FORM_SPEC | html, frd, tests |

## §7.1 ผลต่อ FRD
- DEC-03 → 03 FN-04/05 · 04 approval_chain/doa_ref · 05 BR-05/06 · declarations/DOA_BRIEF
- DEC-07 → 03 FN-09 · print_config sign_boxes doa_step:* · 05 BR-12
- DEC-08 → 03 FN-06/07 · 05 BR-07 (กลับร่าง = BR-DOA-03 ปกติ ไม่ใช่ข้อยกเว้น)
- DEC-09 → 03 FN-11 · 06 TC-D01/02
- DEC-10 → 03 FN-03 · declarations/DOCCFG_BRIEF (CTR)
- DEC-11 → แนบไฟล์ + CSV · ไม่มีทำซ้ำ/ประกาศ
- DEC-12/13/14 → 05 EC-07/EC-08/VR-05
