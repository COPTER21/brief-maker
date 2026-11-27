# 07_LOCKED_DECISIONS — F-TMP-001

## §7.0 Scope Lock — IMMUTABLE (= DECISIONS.lock REQ-TMP-001 · แทนใบเซ็นจนลูกค้าเซ็น · OQ-02)
> โหมดไม่เฝ้า: AI-DEFAULT ทุกหมวด (11 มติ) — ต้องให้ลูกค้ายืนยันในใบลงนาม (newfeature-signoff-generator) ก่อน UAT · VALID = กฎตรวจจากแบบฟอร์มลูกค้า (ผูกใน 05 BR-01/03/06 · EC-09)

| DEC | หมวด | มติ | ที่มา | ใช้ที่ |
|---|---|---|---|---|
| DEC-01 | G1 | อนุมัติแล้วไม่เปลี่ยนค่าในระบบ | AI-DEFAULT | html, thai-doc, brd, frd, tests, ntf-declaration |
| DEC-02 | G1 | ไม่ส่งต่อระบบอื่นรอบนี้ (ประกาศ event ไว้ใน FRD แต่ไม่ยิง) | AI-DEFAULT | brd, frd |
| DEC-03 | G2 | สายอนุมัติตั้งที่ DOA กลาง (dynamic) · ค่าเริ่ม 2 ขั้น: role-line-manager, role-gm · วงเงิน: ไม่มี | AI-DEFAULT | html, doa-declaration, frd, tests |
| DEC-04 | G3 | คำนวณให้อัตโนมัติ ผู้ใช้ปรับได้ · เกินเกณฑ์ = เตือน | AI-DEFAULT | html, thai-doc, brd, frd, tests |
| DEC-05 | G4 | ประวัติการแก้ไข: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 2 แถวตามกระดาษ | AI-DEFAULT | html, thai-doc, frd |
| DEC-06 | G5 | ช่องตรงกระดาษ 1:1 · ไม่เพิ่มช่อง (เช่น หมายเหตุ) | AI-DEFAULT | html, thai-doc, brd, frd |
| DEC-07 | G6 | ลายเซ็นแถวล่าง 1 ช่องต่อขั้น DOA · ไม่ใช้ภาพลายมือชื่อ (ข้อความส่งในระบบ/พิจารณาในระบบ) | AI-DEFAULT | thai-doc, html, doccfg-declaration, frd |
| DEC-08 | G7 | ไม่อนุมัติ = กลับเป็นร่าง แก้แล้วส่งใหม่ · ยกเลิกได้โดย owner, admin_role สถานะ draft, pending · ต้องมีเหตุผล | AI-DEFAULT | html, frd, tests, doa-declaration |
| DEC-09 | G8 | มองเห็น: เจ้าของ · ผู้อนุมัติเห็นหลังส่ง · admin role เห็นทั้งหมด | AI-DEFAULT | html, frd, tests |
| DEC-10 | G9 | ออกเลขเมื่อบันทึกครั้งแรก · รหัส IVMA | AI-DEFAULT | doccfg-declaration, html, frd |
| DEC-11 | G10 | ของเสริม (กระดาษไม่มี): แนบไฟล์, ส่งออก CSV | AI-DEFAULT | html, brd, frd, ntf-declaration |
| DEC-12 | VALID | กฎตรวจจากตัวอย่างลูกค้า: ยึด FM-IVM-01 ตาม footer (Doc No. บนกระดาษ) (พบ: ชื่อชีต INV-FM-01 แต่ footer = Doc. No. : FM-IVM-01) | FORM_SPEC | html, frd, tests |
| DEC-13 | VALID | กฎตรวจจากตัวอย่างลูกค้า: ไม่สร้างช่องจากแถวว่าง (G5 1:1) · แบบพิมพ์คงแถวว่างไว้เพื่อหน้าตาเท่ากระดาษ (พบ: มีแถวป้ายว่าง 1 แถวหลัง 'ประเด็นคงค้างหรือข้อมูลที่ต้องขอเพิ่ม' (แถวสำรองไม่มีชื่อ)) | FORM_SPEC | html, frd, tests |
| DEC-14 | VALID | กฎตรวจจากตัวอย่างลูกค้า: ไม่ hardcode ผู้อนุมัติ — อ่านจาก DOA (approval_chain) · TODO: DOA engine (พบ: บทบาทเดียวรวม 'อนุมัติ' กับ 'รับทราบ' และระบุผู้มีอำนาจหลายระดับ (รองกรรมการผู้จัดการ / กรรมการผู้จัดการ / ตามตารางอำนาจอนุมัติ)) | FORM_SPEC | html, frd, tests |

## §7.1 กติกา
- สกิล/ทีมปลายน้ำห้ามตัดสินขัดตารางนี้ · เปลี่ยนมติ = แก้ decisions.yaml → ล็อกใหม่ → ทำเฉพาะส่วนที่ "ใช้ที่" ระบุ
