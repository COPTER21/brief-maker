# 07_LOCKED_DECISIONS — F-TMP-003

## §7.0 Scope Lock — IMMUTABLE (= DECISIONS.lock REQ-TMP-003 · แทนใบเซ็นจนลูกค้าเซ็น · OQ-02)
> โหมดไม่เฝ้า — ทุก DEC (ยกเว้น VALID) เป็น **AI-DEFAULT** ต้องให้ลูกค้ายืนยันในใบลงนาม (newfeature-signoff-generator) ก่อน UAT
| DEC | หมวด | มติ | ที่มา | ใช้ที่ |
|---|---|---|---|---|
| DEC-01 | G1 | อนุมัติแล้วไม่เปลี่ยนค่าในระบบ | AI-DEFAULT | html, thai-doc, brd, frd, tests, ntf-declaration |
| DEC-02 | G1 | ไม่ส่งต่อระบบอื่นรอบนี้ (ประกาศ event ไว้ใน FRD แต่ไม่ยิง) | AI-DEFAULT | brd, frd |
| DEC-03 | G2 | ไม่มีการอนุมัติ | AI-DEFAULT | html, frd |
| DEC-04 | G3 | คำนวณให้อัตโนมัติ ผู้ใช้ปรับได้ · เกินเกณฑ์ = เตือน · จำนวน ต้องมากกว่า 0 (บล็อก) · วันที่นัดส่ง ก่อน รอบวันที่ = เตือน ไม่บล็อก · ส่งงานได้เมื่อมีอย่างน้อย 1 แถวที่กรอกครบ 5 ช่อง · แถวว่างทั้งแถวไม่นับ · แถวกรอกไม่ครบ = บล็อก | AI-DEFAULT | html, thai-doc, brd, frd, tests |
| DEC-05 | G4 | รายการงานขนส่ง: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 20 แถวตามกระดาษ | AI-DEFAULT | html, thai-doc, frd |
| DEC-06 | G5 | ช่องตรงกระดาษ 1:1 · ไม่เพิ่มช่อง (เช่น หมายเหตุ) | AI-DEFAULT | html, thai-doc, brd, frd |
| DEC-07 | G6 | ลายเซ็นแถวล่าง  · ไม่ใช้ภาพลายมือชื่อ (ข้อความส่งในระบบ/พิจารณาในระบบ) | AI-DEFAULT | thai-doc, html, doccfg-declaration, frd |
| DEC-08 | G8 | มองเห็น: เจ้าของ · ผู้อนุมัติ none · admin role เห็นทั้งหมด | AI-DEFAULT | html, frd, tests |
| DEC-09 | G9 | ออกเลขเมื่อบันทึกครั้งแรก · รหัส OTN | AI-DEFAULT | doccfg-declaration, html, frd |
| DEC-10 | G10 | ของเสริม (กระดาษไม่มี): แนบไฟล์, ส่งออก CSV | AI-DEFAULT | html, brd, frd, ntf-declaration |
| DEC-11 | VALID | กฎตรวจจากตัวอย่างลูกค้า: label บนแบบพิมพ์คงตามกระดาษ (Replica) · บนหน้าจอใช้ "รอบวันที่" — รอยืนยันให้แก้คำบนแบบพิมพ์ Rev.01 (พบ: พิมพ์ "รอบวันที" ขาดไม้เอก) | FORM_SPEC | html, frd, tests |
| DEC-12 | VALID | กฎตรวจจากตัวอย่างลูกค้า: ระบบใส่ลำดับแถวอัตโนมัติ (ไม่พิมพ์ถ้าไม่ตกลง) · จำนวน > 0 (พบ: ไม่มีเลขลำดับ ไม่มีหน่วยของจำนวน และไม่มีช่องหมายเหตุ) | FORM_SPEC | html, frd, tests |
| DEC-13 | VALID | กฎตรวจจากตัวอย่างลูกค้า: วันที่นัดส่ง ≥ รอบวันที่ (เตือน ไม่บล็อก) (พบ: ไม่มีกฎเทียบกับรอบวันที่) | FORM_SPEC | html, frd, tests |
| DEC-14 | VALID | กฎตรวจจากตัวอย่างลูกค้า: ออกเลขที่ตาม G9 · ผู้อนุมัติตาม G2 (พบ: ไม่มีเลขที่เอกสาร/ผู้อนุมัติ/ผู้รับงานลงชื่อ) | FORM_SPEC | html, frd, tests |
| DEC-15 | VALID | กฎตรวจจากตัวอย่างลูกค้า: แบบพิมพ์ทำ 1 หน้า 5 คอลัมน์ตาม print area A1:E26 (พบ: คอลัมน์ วันที่นัดส่ง ตกไปหน้า 2 · ฟอนต์ไทยในเครื่องไม่มี → ตัวไทยเป็นกล่อง) | FORM_SPEC | html, frd, tests |

## §7.1 การใช้มติใน FRD
- DEC-03 → 03 FN-03 (resolve 0 ขั้น · approval_chain = [] · TODO: DOA engine) · 04 approver_role/approved_by/approval_chain เตรียมไว้ · archetype Q-form คงโครง DOA-ENGINE-HOOK แต่ไม่มีปุ่มพิจารณา
- DEC-04/12/13 → 05 BR-01..04 · VR-03..05 · DEC-05/15 → 05 BR-10 · DEC-11 → 05 BR-12 · DEC-09/14 → 03 FN-02 · DEC-08 → 05 §5.3 · 06 §6.2 · DEC-06 → 05 BR-11 · DEC-01/02 → 05 BR-13 · DEC-07 → 03 FN-07 (sign_rows) · DEC-10 → 01 P-01 CSV · P-02 ขั้น 2
- G7 ยกเลิก (decisions.yaml · ไม่มี DEC แยกเพราะไม่มีการอนุมัติ) → 05 BR-08
