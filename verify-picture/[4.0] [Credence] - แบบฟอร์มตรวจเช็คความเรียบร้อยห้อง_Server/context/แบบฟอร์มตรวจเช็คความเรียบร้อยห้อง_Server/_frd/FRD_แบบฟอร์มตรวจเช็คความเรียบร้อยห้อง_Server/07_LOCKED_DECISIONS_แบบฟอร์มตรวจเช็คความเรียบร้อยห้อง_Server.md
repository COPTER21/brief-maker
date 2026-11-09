# 07_LOCKED_DECISIONS — F-TMP-002

## §7.0 Scope Lock — IMMUTABLE (= DECISIONS.lock REQ-TMP-002 · แทนใบเซ็นจนลูกค้าเซ็น · OQ-02 · โหมดไม่เฝ้า: AI-DEFAULT ทุกข้อ)
| DEC | หมวด | มติ | ที่มา | ใช้ที่ |
|---|---|---|---|---|
| DEC-01 | G1 | อนุมัติแล้วไม่เปลี่ยนค่าในระบบ | AI-DEFAULT | html, thai-doc, brd, frd, tests, ntf-declaration |
| DEC-02 | G1 | ไม่ส่งต่อระบบอื่นรอบนี้ (ประกาศ event ไว้ใน FRD แต่ไม่ยิง) | AI-DEFAULT | brd, frd |
| DEC-03 | G2 | ไม่มีการอนุมัติ | AI-DEFAULT | html, frd |
| DEC-04 | G3 | ค่าคงที่อ่านจาก config: "18-27°C" → ServerRoomCheckConfig.temp_min_c / temp_max_c, "40-55 %RH" → ServerRoomCheckConfig.rh_min / rh_max · ผู้ใช้กรอกเอง · เกินเกณฑ์ = เตือน · อุณหภูมินอกช่วง 18-27°C หรือ ความชื้นนอกช่วง 40-55 %RH → เตือน (ไฮไลต์แถว) ไม่บล็อก · แนะนำให้กรอกหมายเหตุ · ทะเบียนคุมเข้าออก = ไม่มี หรือ อุปกรณ์ใด = ไม่ปกติ → เตือน (ไฮไลต์แถว) ไม่บล็อก · แนะนำให้กรอกหมายเหตุ · วันที่ซ้ำกันในใบเดียวกัน → เตือน ไม่บล็อก | AI-DEFAULT | html, thai-doc, brd, frd, tests |
| DEC-05 | G4 | รายการตรวจเช็คประจำวัน: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 30 แถวตามกระดาษ | AI-DEFAULT | html, thai-doc, frd |
| DEC-06 | G5 | ช่องตรงกระดาษ 1:1 · ไม่เพิ่มช่อง (เช่น หมายเหตุ) | AI-DEFAULT | html, thai-doc, brd, frd |
| DEC-07 | G6 | ลายเซ็นตามตำแหน่งกระดาษ  · ไม่ใช้ภาพลายมือชื่อ (ข้อความส่งในระบบ/พิจารณาในระบบ) | AI-DEFAULT | thai-doc, html, doccfg-declaration, frd |
| DEC-08 | G8 | มองเห็น: เจ้าของ · ผู้อนุมัติ none · admin role เห็นทั้งหมด | AI-DEFAULT | html, frd, tests |
| DEC-09 | G9 | ออกเลขเมื่อบันทึกครั้งแรก · รหัส SRC | AI-DEFAULT | doccfg-declaration, html, frd |
| DEC-10 | G10 | ของเสริม (กระดาษไม่มี): แนบไฟล์, ส่งออก CSV | AI-DEFAULT | html, brd, frd, ntf-declaration |
| DEC-11 | VALID | กฎตรวจจากตัวอย่างลูกค้า: G2 ต้องให้ลูกค้ายืนยันว่าต้องมีผู้ตรวจทานประจำเดือนหรือไม่ (พบ: กระดาษไม่มีช่องลงชื่อผู้ตรวจทาน/ผู้อนุมัติ — มีเฉพาะชื่อผู้ตรวจสอบต่อแถว) | FORM_SPEC | html, frd, tests |
| DEC-12 | VALID | กฎตรวจจากตัวอย่างลูกค้า: เก็บเป็นข้อความ · ลูกค้ายืนยันรูปแบบ (พบ: ไม่ระบุหน่วยหรือเกณฑ์ความดันที่ถือว่าผ่าน) | FORM_SPEC | html, frd, tests |
| DEC-13 | VALID | กฎตรวจจากตัวอย่างลูกค้า: ค่านอกช่วง = เตือน + ระบุหมายเหตุ (ไม่บล็อก) (พบ: ค่านอกช่วงเกณฑ์บนหัวตาราง (18-27°C · 40-55 %RH)) | FORM_SPEC | html, frd, tests |

raw (ไม่มี DEC แยกเพราะไม่มีการอนุมัติ): G7 reject_cancel = ยกเลิกได้โดย owner + admin_role · สถานะ draft/submitted · เหตุผลบังคับ (AI-DEFAULT) → BR-10

LD-07: prototype มีโครง DOA ของ archetype Q-form (MOCK_DOA_RESOLVED 0 ขั้น · slot-row · modal ตรวจทาน) ตาม Rule #108 — dormant ไม่อยู่ใน scope dev รอบนี้

## §7.1 Locked Decisions (LD)
| LD | ตัดสิน | เหตุผล |
|---|---|---|
| LD-01 | สถานะสุดท้าย = submitted "ปิดรอบแล้ว" (ไม่มี approved/pending) | ไม่มีการอนุมัติ (DEC-03) |
| LD-02 | 1 ใบ = 1 รอบการตรวจ · แถว 1 วัน/แถว | กระดาษ 30 แถว ≈ 1 เดือน |
| LD-03 | แบบพิมพ์ A4 แนวตั้ง 2 หน้า (R10) แทนแนวนอน 1 หน้าของต้นฉบับ | engine กลาง (base.css) รองรับแนวตั้งเท่านั้น · คอลัมน์/ถ้อยคำ 1:1 |
| LD-04 | ผู้ตรวจสอบ = ผู้บันทึกแถว (ระบบเติม) | DEC-07 · ไม่มีลายมือชื่อ |
| LD-05 | ตารางกรอกรายวันแทนการ์ดต่อแถว | แถวซ้ำ 11 ช่อง > 4 (#107) |
| LD-06 | template แบบพิมพ์มีบล็อก sign_rows (ส่งค่าว่าง = ไม่มีบล็อก) | ถ้าลูกค้าเพิ่มผู้ตรวจทานภายหลัง (enhancement + DOA_BRIEF) ไม่ต้องแก้แบบพิมพ์ |
