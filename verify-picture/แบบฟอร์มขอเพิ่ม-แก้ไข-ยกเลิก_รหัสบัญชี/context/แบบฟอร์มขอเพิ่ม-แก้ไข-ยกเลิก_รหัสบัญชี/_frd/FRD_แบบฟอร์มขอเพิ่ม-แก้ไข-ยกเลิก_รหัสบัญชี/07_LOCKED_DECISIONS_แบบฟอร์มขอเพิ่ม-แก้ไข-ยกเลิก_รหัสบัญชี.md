# 07_LOCKED_DECISIONS — F-TMP-003

## §7.0 Scope Lock — IMMUTABLE (= DECISIONS.lock REQ-TMP-003 · แทนใบเซ็นจนลูกค้าเซ็น · OQ-02)
| DEC | หมวด | มติ | ที่มา | ใช้ที่ |
|---|---|---|---|---|
| DEC-01 | G1 | อนุมัติแล้วไม่เปลี่ยนค่าในระบบ | AI-DEFAULT | html, thai-doc, brd, frd, tests, ntf-declaration |
| DEC-02 | G1 | ไม่ส่งต่อระบบอื่นรอบนี้ (ประกาศ event ไว้ใน FRD แต่ไม่ยิง) | AI-DEFAULT | brd, frd |
| DEC-03 | G2 | สายอนุมัติตั้งที่ DOA กลาง (dynamic) · ค่าเริ่ม 2 ขั้น: role-line-manager, role-mgr-acc · วงเงิน: ไม่มี | AI-DEFAULT | html, doa-declaration, frd, tests |
| DEC-04 | G3 | คำนวณให้อัตโนมัติ ผู้ใช้ปรับได้ · เกินเกณฑ์ = เตือน · 1 ใบ = 1 ประเภทคำขอ (เพิ่ม/แก้ไข/ยกเลิก) · ส่วนที่ไม่ได้เลือกต้องว่าง · เพิ่ม: ต้องมีชื่อบัญชีอย่างน้อย 1 แถว · ไม่อนุมัติ → เหตุผลบังคับ | AI-DEFAULT | html, thai-doc, brd, frd, tests |
| DEC-05 | G4 | ชื่อบัญชีที่ต้องการขอเพิ่ม: ไม่จำกัดจำนวนแถว · PDF อย่างน้อย 4 แถวตามกระดาษ | AI-DEFAULT | html, thai-doc, frd |
| DEC-06 | G5 | ช่องตรงกระดาษ 1:1 · ไม่เพิ่มช่อง (เช่น หมายเหตุ) | AI-DEFAULT | html, thai-doc, brd, frd |
| DEC-07 | G6 | ลายเซ็นแถวล่าง 1 ช่องต่อขั้น DOA · ไม่ใช้ภาพลายมือชื่อ (ข้อความส่งในระบบ/พิจารณาในระบบ) | AI-DEFAULT | thai-doc, html, doccfg-declaration, frd |
| DEC-08 | G7 | ไม่อนุมัติ = กลับเป็นร่าง แก้แล้วส่งใหม่ · ยกเลิกได้โดย owner, admin_role สถานะ draft, pending · ต้องมีเหตุผล | AI-DEFAULT | html, frd, tests, doa-declaration |
| DEC-09 | G8 | มองเห็น: เจ้าของ · ผู้อนุมัติเห็นหลังส่ง · admin role เห็นทั้งหมด | AI-DEFAULT | html, frd, tests |
| DEC-10 | G9 | ออกเลขเมื่อบันทึกครั้งแรก · รหัส ACR | AI-DEFAULT | doccfg-declaration, html, frd |
| DEC-11 | G10 | ของเสริม (กระดาษไม่มี): แนบไฟล์, ส่งออก CSV | AI-DEFAULT | html, brd, frd, ntf-declaration |
| DEC-12 | VALID | กฎตรวจจากตัวอย่างลูกค้า: แสดงเป็น "วัตถุประสงค์ในการยกเลิก" (G5 แก้คำผิดชัดเจน) · key แยก cancel.purpose (พบ: หัวช่องพิมพ์ว่า "วัตถุประสงค์ในการแก้ไข" ทั้งที่อยู่ในส่วนยกเลิก (คัดลอกจากส่วนแก้ไข)) | FORM_SPEC | html, frd, tests |
| DEC-13 | VALID | กฎตรวจจากตัวอย่างลูกค้า: 1 ใบ = 1 ประเภทคำขอ · ส่วนที่ไม่ได้เลือกต้องว่าง (validation) (พบ: ☐ 3 ตัวเลือกไม่ได้บอกว่าเลือกได้ข้อเดียวหรือหลายข้อ) | FORM_SPEC | html, frd, tests |
| DEC-14 | VALID | กฎตรวจจากตัวอย่างลูกค้า: เลือก ไม่อนุมัติ → เหตุผลบังคับ (พบ: ไม่อนุมัติ มีช่องเหตุผล แต่ไม่บังคับบนกระดาษ) | FORM_SPEC | html, frd, tests |

## §7.1 Locked Decisions (LD)
| LD | ตัดสิน | เหตุผล |
|---|---|---|
| LD-01 | ไม่อนุมัติ → draft (ไม่มี status rejected) | DEC-08 · ร่างไม่รั่วให้ผู้อนุมัติ (#109) |
| LD-02 | คำตัดสินของ role-line-manager = "ตรวจสอบแล้ว / ไม่ผ่านการตรวจสอบ" (print_config.decision_words.by_role) · ขั้นอื่น = อนุมัติ/ไม่อนุมัติ | กระดาษแยก "ผู้ตรวจสอบ" กับ "ผู้อนุมัติ" · ผูก role ไม่ผูกลำดับขั้น |
| LD-03 | "ผู้บันทึกเข้าระบบ" = action หลังอนุมัติของ admin ฝ่ายบัญชี ไม่ใช่ขั้น DOA · บรรทัดคงที่ตามกระดาษ | ไม่ใช่การอนุมัติ · DEC-01 ระบบไม่แก้ COA เอง |
| LD-04 | "สำหรับผู้อนุมัติ ☐ อนุมัติ ☐ ไม่อนุมัติ เหตุผล" = สรุปผลของสาย DOA (☑ อนุมัติเมื่อผ่านครบทุกขั้น) | กระดาษมีช่องผลรวม 1 จุด · สายจริง dynamic |
| LD-05 | แบบพิมพ์ Replica เส้นประ (R4) + ลงชื่อแถวล่าง (B6) · 1 หน้า A4 | ต้นฉบับ Word 1 หน้า · DEC-07 |
| LD-06 | รหัสเอกสาร ACR (Account Code Request · ไม่ชน ACL/RPR/ALN ใน registry) | DEC-10 |
| LD-07 | สถานะ approved แสดงเป็น "อนุมัติแล้ว · รอบันทึก" · recorded = "บันทึกเข้าระบบแล้ว" | ให้ฝ่ายบัญชีเห็นงานค้าง |

> มติ AI-DEFAULT ทุกข้อต้องให้ลูกค้ายืนยันในใบลงนาม (newfeature-signoff-generator) ก่อน UAT
