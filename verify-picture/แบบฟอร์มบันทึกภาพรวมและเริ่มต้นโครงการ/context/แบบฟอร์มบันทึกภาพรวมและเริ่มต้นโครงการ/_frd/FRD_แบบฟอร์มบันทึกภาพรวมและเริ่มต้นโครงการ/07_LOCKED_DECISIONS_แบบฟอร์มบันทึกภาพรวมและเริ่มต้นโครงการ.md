# 07_LOCKED_DECISIONS — F-TMP-001

## §7.0 Scope Lock — IMMUTABLE (= DECISIONS.lock REQ-TMP-001 · แทนใบเซ็นจนลูกค้าเซ็น · OQ-02)
> โหมดไม่เฝ้า — AI-DEFAULT ทุกหมวด (12 ข้อ) ต้องให้ลูกค้ายืนยันในใบลงนาม (newfeature-signoff-generator) ก่อน UAT
| DEC | หมวด | มติ | ที่มา | ใช้ที่ |
|---|---|---|---|---|
| DEC-01 | G1 | อนุมัติแล้วไม่เปลี่ยนค่าในระบบ | AI-DEFAULT | html, thai-doc, brd, frd, tests, ntf-declaration |
| DEC-02 | G1 | ไม่ส่งต่อระบบอื่นรอบนี้ (ประกาศ event ไว้ใน FRD แต่ไม่ยิง) | AI-DEFAULT | brd, frd |
| DEC-03 | G2 | สายอนุมัติตั้งที่ DOA กลาง (dynamic) · ค่าเริ่ม 2 ขั้น: role-line-manager, role-gm · วงเงิน: ไม่มี | AI-DEFAULT | html, doa-declaration, frd, tests |
| DEC-04 | G3 | คำนวณให้อัตโนมัติ ผู้ใช้ปรับได้ · เกินเกณฑ์ = เตือน · วันที่เป้าหมาย ≥ วันที่เริ่มต้น · แผนงาน: วันครบกำหนด ≥ วันเริ่มต้น (ต่อแถว) | AI-DEFAULT | html, thai-doc, brd, frd, tests |
| DEC-05 | G4 | แผนงานเบื้องต้น: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 6 แถวตามกระดาษ | AI-DEFAULT | html, thai-doc, frd |
| DEC-06 | G4 | ประวัติการแก้ไข: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 1 แถวตามกระดาษ | AI-DEFAULT | html, thai-doc, frd |
| DEC-07 | G5 | ช่องตรงกระดาษ 1:1 · ไม่เพิ่มช่อง (เช่น หมายเหตุ) · รวม/แยก: วันที่เริ่มต้น / วันที่เป้าหมาย → 2 ค่า, ระดับความสำคัญ / สถานะ → 2 ค่า | AI-DEFAULT | html, thai-doc, brd, frd |
| DEC-08 | G6 | ลายเซ็นแถวล่าง 1 ช่องต่อขั้น DOA · ไม่ใช้ภาพลายมือชื่อ (ข้อความส่งในระบบ/พิจารณาในระบบ) | AI-DEFAULT | thai-doc, html, doccfg-declaration, frd |
| DEC-09 | G7 | ไม่อนุมัติ = กลับเป็นร่าง แก้แล้วส่งใหม่ · ยกเลิกได้โดย owner, admin_role สถานะ draft, pending · ต้องมีเหตุผล | AI-DEFAULT | html, frd, tests, doa-declaration |
| DEC-10 | G8 | มองเห็น: เจ้าของ · ผู้อนุมัติเห็นหลังส่ง · admin role เห็นทั้งหมด | AI-DEFAULT | html, frd, tests |
| DEC-11 | G9 | ออกเลขเมื่อบันทึกครั้งแรก · รหัส PJI | AI-DEFAULT | doccfg-declaration, html, frd |
| DEC-12 | G10 | ของเสริม (กระดาษไม่มี): แนบไฟล์, ส่งออก CSV | AI-DEFAULT | html, brd, frd, ntf-declaration |
| DEC-13 | VALID | กฎตรวจจากตัวอย่างลูกค้า: เก็บแยก 2 ค่า · วันที่เป้าหมาย ≥ วันที่เริ่มต้น (พบ: กระดาษรวม 2 ค่าไว้ในช่องรายละเอียดช่องเดียว) | FORM_SPEC | html, frd, tests |
| DEC-14 | VALID | กฎตรวจจากตัวอย่างลูกค้า: วันครบกำหนด ≥ วันเริ่มต้น (ต่อแถว) (พบ: วันเริ่มต้น/วันครบกำหนดของกิจกรรมไม่มีเงื่อนไขบนกระดาษ) | FORM_SPEC | html, frd, tests |
| DEC-15 | VALID | กฎตรวจจากตัวอย่างลูกค้า: แยก 2 ค่า · ตัวเลือกระดับความสำคัญรอลูกค้ายืนยัน (พบ: กระดาษรวม 2 ค่าไว้ในช่องเดียวและไม่ระบุตัวเลือก) | FORM_SPEC | html, frd, tests |

## §7.1 Locked Decisions (LD)
| LD | เรื่อง | อ้าง |
|---|---|---|
| LD-01 | สายอนุมัติจาก DOA กลาง ไม่ hardcode (DOA-ENGINE-HOOK) | DEC-03 |
| LD-02 | แบบพิมพ์ = form.tpl.html logic-less + data contract เดียวกันทั้ง prototype/server | DEC-08 |
| LD-03 | ไม่อนุมัติ = กลับร่างเลขเดิม (BR-DOA-03 ปกติ) | DEC-09 |
| LD-04 | แยก 2 ค่าในแถวรวมของกระดาษ แต่แสดงแถวเดียวเหมือนกระดาษ | DEC-07 · DEC-13 |

## §7.2 Convention Deviations
- PDF 2 หน้า (R10) — ต้นฉบับ xlsx พิมพ์ 1 หน้าที่ scale 46% (ตัวอักษร ≈ 5pt) · ห้ามบีบ < 8pt
- ตาราง "การตรวจทาน / อนุมัติ" ใช้ 1 แถวต่อขั้นตามกระดาษ (แทนกล่องลงชื่อแนวนอน B6) — วนจาก sign_rows[].signs[]

## §7.3 Open Questions → 00 §0.8 (OQ-01..05)

## §7.5 Deferred
ติดตามความคืบหน้ากิจกรรมหลังอนุมัติ · เชื่อมงบประมาณ · ทำซ้ำ
