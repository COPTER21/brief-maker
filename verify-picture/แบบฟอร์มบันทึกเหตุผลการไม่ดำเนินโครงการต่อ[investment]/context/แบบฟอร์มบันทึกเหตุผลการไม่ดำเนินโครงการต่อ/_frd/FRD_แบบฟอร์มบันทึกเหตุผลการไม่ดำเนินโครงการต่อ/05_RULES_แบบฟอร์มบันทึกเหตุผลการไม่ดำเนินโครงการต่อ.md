# 05_RULES — F-TMP-002

## §5.1 Business Rules
| BR | Rule | Tag | อ้าง |
|---|---|:-:|---|
| BR-01 | ต้องมีเหตุผลที่เลือก ใช่ ≥ 1 แถวก่อนบันทึก/ส่ง | FIXED | DEC-04 · DEC-13 |
| BR-02 | แถวที่เลือก ใช่ ต้องมีรายละเอียดประกอบ | FIXED | DEC-13 |
| BR-03 | result = continue_conditional → instruction บังคับ (ตอนเสนอและตอนผู้อนุมัติขั้นสุดท้ายเปลี่ยนผล) | FIXED | DEC-14 |
| BR-04 | ผลการพิจารณา: ผู้จัดทำเสนอ · ผู้อนุมัติขั้นสุดท้ายยืนยัน/เปลี่ยนได้ · เก็บ result_proposed + audit before/after | CONFIGURABLE | DEC-04 [AI-DEFAULT] |
| BR-05 | ตัวเลือกผลการพิจารณา 4 ค่าตามแบบฟอร์ม (master list) | CONFIGURABLE | FORM_SPEC choices.result |
| BR-06 | ผู้มีอำนาจพิจารณา = ผู้พิจารณาขั้นสุดท้ายใน approval_chain (อ่านอย่างเดียว) | FIXED | FORM_SPEC F05 |
| BR-07 | สายอนุมัติ resolve จาก DOA ตอนส่ง แล้ว freeze (BR-DOA-02) · ผู้จัดทำอนุมัติใบตัวเองไม่ได้ (BR-DOA-04) | FIXED | DEC-03 |
| BR-08 | ส่งกลับ/ไม่อนุมัติ → draft เลขเดิม · resolve ใหม่ตอนส่งรอบถัดไป (BR-DOA-03 ตามปกติ ไม่ใช่ข้อยกเว้น) | FIXED | DEC-08 |
| BR-09 | ออกเลขตอนบันทึกครั้งแรก · no-gap ✗ · รหัส IVMJ | CONFIGURABLE | DEC-10 |
| BR-10 | ร่างเห็นเฉพาะเจ้าของ (+ admin) · ผู้พิจารณาเห็นหลังส่ง | FIXED | DEC-09 |
| BR-11 | ช่องลงชื่อ PDF = ผู้จัดทำ + 1 แถวต่อขั้นที่ตั้งใน DOA (dynamic) · คำตัดสินตาม role (role-line-manager: ตรวจสอบแล้ว/ส่งกลับ · role-gm: อนุมัติ/ไม่อนุมัติ) · ข้อความ "ส่งในระบบ / พิจารณาในระบบ วันที่ เวลา" ไม่ใช้ภาพ | FIXED (จำนวน = DOA) | DEC-03 · DEC-07 |
| BR-12 | ตารางเหตุผลไม่จำกัดแถว · PDF ≥ 8 แถว · แบบพิมพ์ 2 หน้า (ตัดหน้าก่อน "ข้อสรุป…") | FIXED | DEC-05 |
| BR-13 | อนุมัติแล้วไม่เปลี่ยนค่าในระบบอื่น · ไม่ส่งต่อ (`ivmj.approved` ประกาศไม่ยิง) | FIXED | DEC-01 · DEC-02 |
| BR-14 | รหัสแบบฟอร์ม = FM-IVM-10 (ตาม footer · ไม่ใช่ชื่อชีต INV-FM-10) | FIXED | DEC-12 |
| BR-15 | ช่องตามกระดาษ 1:1 · ตารางเหตุผล 8 คอลัมน์ตามหัว (คอลัมน์ไม่มีหัวไม่ใช้) · ของเสริม: แนบไฟล์ · CSV | FIXED | DEC-06 · DEC-15 · DEC-11 |
| (NTF) | ivmj_cancelled · ivmj_result_recorded ยิงผ่าน ENG-NOTIFY (03 FN-09) | — | NTF_BRIEF |

## §5.2 State Machine
draft →(ส่ง)→ pending[1..N] →(อนุมัติขั้น N)→ approved · pending →(ส่งกลับ/ไม่อนุมัติ)→ draft · draft/pending →(ยกเลิก)→ cancelled · approved = ล็อก

## §5.3 Permission
| Action | owner | ผู้พิจารณาขั้นปัจจุบัน | ผู้ในสาย (ไม่ใช่ขั้นปัจจุบัน) | admin | อื่น |
|---|:-:|:-:|:-:|:-:|:-:|
| ดู | ✓ | ✓ (หลังส่ง) | ✓ (หลังส่ง) | ✓ | ✗ 404 |
| แก้/ส่ง | ✓ draft | ✗ | ✗ | ✗ | ✗ |
| ตัดสิน | ✗ | ✓ | ✗ 403 | ✗ | ✗ |
| ยกเลิก | ✓ draft/pending | ✗ | ✗ | ✓ draft/pending | ✗ 403 |

## §5.4 Validation
| VR | ช่อง | เงื่อนไข | ข้อความ |
|---|---|---|---|
| VR-01 | project_name | required | กรุณากรอกชื่อโครงการ / ธุรกรรม |
| VR-02 | owner · proposed_date (≤ วันนี้) · stopped_at_step | required | กรุณาเลือกผู้รับผิดชอบ · กรุณาเลือกวันที่ · กรุณาระบุขั้นตอนที่ยุติ |
| VR-03 | reasons[].reason · reasons[].detail (เมื่อ yes) | required | ใส่เหตุผลหลัก · เลือก ใช่ ต้องมีรายละเอียดประกอบ (DEC-13) |
| VR-04 | reasons | ≥ 1 yes | ต้องมีเหตุผลที่เลือก ใช่ อย่างน้อย 1 ข้อ (DEC-13) |
| VR-05 | summary_reason · archive_plan | required | กรุณากรอกสรุปเหตุผล · กรุณากรอกแนวทางจัดเก็บเอกสารและปิดงาน |
| VR-06 | instruction | required เมื่อ continue_conditional | เลือก ดำเนินการต่อแบบมีเงื่อนไข ต้องระบุข้อสั่งการ / เงื่อนไข (DEC-14) |
| VR-07 | assignees | ทุกขั้น · ≠ ผู้จัดทำ | กรุณาเลือกผู้พิจารณา |
| VR-08 | reason (ส่งกลับ/ไม่อนุมัติ/ยกเลิก) | required | กรุณาระบุเหตุผล |

## §5.5 Edge Cases
| EC | กรณี | ผล |
|---|---|---|
| EC-01 | ทุกแถว ไม่ใช่ | บล็อก VR-04 |
| EC-02 | เหตุผล > 8 แถว | PDF หัวตารางซ้ำ · ยัง 2 หน้า (12 แถว) |
| EC-03 | resolve ขั้น 1 = ผู้จัดทำ | slot ว่าง ต้องเลือกคนอื่น |
| EC-04 | แก้ DOA ระหว่างใบรออนุมัติ | ใช้สาย snapshot |
| EC-05 | DOA 6 ขั้น | PDF 7 แถวลงชื่อ · 2 หน้า |
| EC-06 | stale | 409 STALE · สถานะไม่เปลี่ยน |
| EC-07 | doc_type IVMJ ปิดใช้ | สร้างไม่ได้ (409 DOC_TYPE_INACTIVE) |
| EC-08 | ผู้อนุมัติเปลี่ยนเป็นมีเงื่อนไขไม่ใส่ข้อสั่งการ | 422 INSTRUCTION_REQUIRED |
| EC-09 | วันที่เสนออนาคต | 422 (max วันนี้) |
| EC-10 | ชื่อชีต ≠ Doc No. | ใช้ FM-IVM-10 (DEC-12) |
