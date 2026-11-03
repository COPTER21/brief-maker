# 07_LOCKED_DECISIONS — F-TMP-001

## §7.0 Scope Lock — IMMUTABLE (= DECISIONS.lock REQ-TMP-001 · แทนใบเซ็นจนลูกค้าเซ็น · OQ-02)
> unattended — AI-DEFAULT ทุกหมวด รอลูกค้ายืนยันในใบลงนาม (newfeature-signoff-generator) ก่อน UAT
| DEC | หมวด | มติ | ที่มา | ใช้ที่ |
|---|---|---|---|---|
| DEC-01 | G1 | อนุมัติแล้วไม่เปลี่ยนค่าในระบบ | AI-DEFAULT | html, thai-doc, brd, frd, tests, ntf-declaration |
| DEC-02 | G1 | ไม่ส่งต่อระบบอื่นรอบนี้ (ประกาศ event ไว้ใน FRD แต่ไม่ยิง) | AI-DEFAULT | brd, frd |
| DEC-03 | G2 | ไม่มีการอนุมัติ | AI-DEFAULT | html, frd |
| DEC-04 | G3 | คำนวณให้อัตโนมัติ ผู้ใช้ปรับได้ · เกินเกณฑ์ = เตือน · ชื่อบริษัทในหัวเรื่องและข้อ 2 ดึงจาก Organization.legal_name ค่าเดียวกัน (ไม่พิมพ์ตายตัว) | AI-DEFAULT | html, thai-doc, brd, frd, tests |
| DEC-05 | G4 | รายการซ้ำ: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย None แถวตามกระดาษ | AI-DEFAULT | html, thai-doc, frd |
| DEC-06 | G5 | ช่องตรงกระดาษ 1:1 · ไม่เพิ่มช่อง (เช่น หมายเหตุ) | AI-DEFAULT | html, thai-doc, brd, frd |
| DEC-07 | G6 | ลายเซ็นแถวล่าง 1 ช่องต่อขั้น DOA · ไม่ใช้ภาพลายมือชื่อ (ข้อความส่งในระบบ/พิจารณาในระบบ) | AI-DEFAULT | thai-doc, html, doccfg-declaration, frd |
| DEC-08 | G8 | มองเห็น: เจ้าของ · ผู้อนุมัติเห็นหลังส่ง · admin role เห็นทั้งหมด | AI-DEFAULT | html, frd, tests |
| DEC-09 | G9 | ออกเลขเมื่อบันทึกครั้งแรก · รหัส CSE | AI-DEFAULT | doccfg-declaration, html, frd |
| DEC-10 | G10 | ของเสริม (กระดาษไม่มี): แนบไฟล์, ส่งออก CSV | AI-DEFAULT | html, brd, frd, ntf-declaration |
| DEC-11 | VALID | กฎตรวจจากตัวอย่างลูกค้า: ทั้งสองจุดดึงชื่อนิติบุคคลเดียวกันจาก Organization.legal_name — ไม่พิมพ์ตายตัว (พบ: หัวเรื่องเขียน 'บริษัทครีเดนซ์ จำกัด (มหาชน)' แต่ข้อ 2 พิมพ์ 'บริษัท ครีเดนซ์ จำกัด' (ไม่มี มหาชน)) | FORM_SPEC | html, frd, tests |
| DEC-12 | VALID | กฎตรวจจากตัวอย่างลูกค้า: ตีความเป็น 1–<3 ปี / 3–5 ปี / มากกว่า 5 ปี · เลือกได้ 1 ตัว (คำบนกระดาษคงเดิม) (พบ: ช่วง '1-3 ปี' กับ '3-5 ปี' ทับกันที่ 3 ปี) | FORM_SPEC | html, frd, tests |
| DEC-13 | VALID | กฎตรวจจากตัวอย่างลูกค้า: คะแนนต้องเป็นจำนวนเต็ม 1–5 เท่านั้น · ครบ 9 ข้อก่อนส่ง (พบ: กระดาษให้เขียนตัวเลขเอง ไม่มีกรอบตัวเลือก) | FORM_SPEC | html, frd, tests |

หมายเหตุ: ข้อความ DEC มาจาก decisions_lock.py ตรงตัว — DEC-01 "อนุมัติแล้วไม่เปลี่ยนค่าในระบบ" ในเอกสารนี้หมายถึง "ส่งแล้ว" (ไม่มีสายพิจารณา DEC-03) · DEC-05 "None แถว" = ไม่มีรายการซ้ำ · DEC-07 "1 ช่องต่อขั้น DOA" = ผู้ประเมิน 1 ช่อง (0 ขั้น) · G7 ไม่ได้ออก DEC เพราะไม่มีสายพิจารณา → ใช้ BR-07 [AI-DEFAULT]

## §7.1 Locked Decisions (LD)
| LD | ตัดสิน | เหตุผล |
|---|---|---|
| LD-01 | ไม่สร้าง DOA_BRIEF · DOA hook ใน prototype ค่าเริ่มต้น 0 ขั้น | DEC-03 · doa-declaration "ห้ามยัด DOA เข้า feature ที่ไม่มีอนุมัติ" · Q-form audit ต้องมี MOCK_DOA_RESOLVED/slot-row (dynamic) |
| LD-02 | ชื่อบริษัทหัวเรื่อง + ข้อ 2 เป็นค่าเดียวจาก Organization | DEC-11 แก้ความไม่ตรงในต้นฉบับ (OQ-05) |
| LD-03 | ข้อเสนอแนะในแบบพิมพ์เป็นกล่อง R8 แทนเส้น 2 บรรทัด | รองรับข้อความยาว · ไม่เพิ่มช่อง (DEC-06) |
| LD-04 | ผู้ประเมิน = ผู้บันทึกในระบบ (ไม่เพิ่มช่องชื่อผู้ประเมิน) | DEC-06 1:1 · OQ-04 |
| LD-05 | mdoc source = declaration (ไม่ใช่ request) จนได้เลขคำขอจริง | REQ-TMP-001 ไม่ผ่านรูปแบบ REQ-YYYY-NNNN (G10) · OQ-03 |

## §7.2 Convention Deviations
- ไม่มี
