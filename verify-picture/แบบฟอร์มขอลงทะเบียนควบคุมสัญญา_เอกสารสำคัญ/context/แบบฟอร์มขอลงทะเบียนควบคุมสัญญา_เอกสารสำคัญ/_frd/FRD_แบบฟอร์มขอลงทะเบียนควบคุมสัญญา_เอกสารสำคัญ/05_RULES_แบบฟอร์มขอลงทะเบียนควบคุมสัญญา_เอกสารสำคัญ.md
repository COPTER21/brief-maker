# 05_RULES — F-TMP-009

## §5.1 Business Rules
| ID | Rule | อ้าง |
|---|---|---|
| BR-01 | ประเภทของสัญญาเลือก 1 · จุดประสงค์ร้องขอเลือก 1 | FORM_SPEC choices |
| BR-02 | purpose=amend → change_reason บังคับ · อื่น ๆ บันทึกเป็นว่าง | DEC-04 |
| BR-03 | contract_end ≥ contract_start | DEC-04 · DEC-14 |
| BR-04 | owner_unit ค่าเริ่ม = หน่วยงานผู้ขอ เปลี่ยนได้จาก OrgUnit | F-ORG-001 |
| BR-05 | สายพิจารณา resolve จาก DOA ตอนส่ง แล้ว freeze (BR-DOA-02) · จำนวนขั้นตั้งที่ DOA กลาง | DEC-03 |
| BR-06 | คำตัดสินผูก role: default อนุมัติ/ไม่อนุมัติ · role-compliance รับทราบ/ส่งกลับแก้ไข | print_config.decision_words |
| BR-07 | ไม่อนุมัติ/ส่งกลับแก้ไข → draft เลขเดิม (BR-DOA-03 ตามปกติ — ไม่ใช่ข้อยกเว้น) | DEC-08 |
| BR-08 | ออกเลข CTR ตอนบันทึกครั้งแรก · no-gap ✗ | DEC-10 |
| BR-09 | ลงทะเบียนได้เฉพาะ approved โดยผู้ดูแลสัญญา · register_no ไม่ซ้ำ | FN-08 |
| BR-10 | original_received_date ≤ วันนี้ · บันทึกได้เฉพาะ registered | FN-08 |
| BR-11 | ร่างเห็นเฉพาะเจ้าของ (+ ผู้ดูแลสัญญา) · ผู้พิจารณาเห็นหลังส่ง | DEC-09 |
| BR-12 | ช่องลงชื่อ PDF = ผู้รับผิดชอบ + 1 ช่อง/ขั้น DOA (dynamic) แถวละ ≤4 · >4 ขั้น dense | DEC-03 · DEC-07 |
| BR-13 | อนุมัติแล้วไม่เปลี่ยนค่าในระบบอื่น ไม่ส่งต่อ | DEC-01 · DEC-02 |
| BR-14 | ผู้ขอพิจารณาใบตัวเองไม่ได้ (BR-DOA-04) | DOA |
| BR-15 | ลำดับการอนุมัติ (approval) แบบ sequential — ขั้นถัดไปรอจนขั้นก่อนหน้าอนุมัติ | DOA |

## §5.2 State Machine
draft → pending (ส่ง) → approved (ครบทุกขั้น) → registered (ลงทะเบียน) → completed (รับต้นฉบับ) · pending → draft (ไม่อนุมัติ/ส่งกลับ) · draft/pending → cancelled · สถานะ ≠ draft ล็อกแก้ไข

## §5.3 Permission Matrix
| Action | Maker | ผู้พิจารณาขั้นปัจจุบัน | ผู้ดูแลสัญญา | อื่น |
|---|:-:|:-:|:-:|:-:|
| ดู | ของตน | หลังส่ง | ทั้งหมด | ✗ (404) |
| สร้าง/แก้ร่าง | ✓ ของตน | ✗ | ✗ | ✗ |
| ส่ง | ✓ ของตน (draft) | ✗ | ✗ | ✗ |
| ตัดสินขั้น | ✗ | ✓ | ✗ (เว้นอยู่ในสาย) | ✗ |
| ลงทะเบียน / รับต้นฉบับ | ✗ | ✗ | ✓ | ✗ |
| ยกเลิก | ✓ ของตน (draft/pending) | ✗ | ✓ | ✗ |

## §5.4 Validation
| VR | ช่อง | เงื่อนไข | ข้อความ |
|---|---|---|---|
| VR-01 | contract_type | required | เลือกประเภทของสัญญา |
| VR-02 | purpose | required | เลือกจุดประสงค์ร้องขอ |
| VR-03 | change_reason | required เมื่อ amend | กรุณาระบุสาเหตุ |
| VR-04 | counterparty_name | required ≤300 | กรุณาระบุชื่อคู่สัญญา |
| VR-05 | contract_start / contract_end | required · end ≥ start (DEC-14) | เลือกวันที่เริ่มต้น / วันที่สิ้นสุดต้องไม่ก่อนวันที่เริ่มต้น |
| VR-06 | owner_unit_id | required | เลือกหน่วยงานเจ้าของสัญญา |
| VR-07 | assignees | ครบทุกขั้น · ≠ ผู้ขอ | กรุณาเลือกผู้พิจารณา |
| VR-08 | reason (reject/cancel) | required | กรุณาระบุเหตุผล |
| VR-09 | original_received_date | required · ≤ วันนี้ | เลือกวันที่ได้รับ |

## §5.5 Edge Cases
| EC | กรณี | ผล |
|---|---|---|
| EC-01 | สัญญาสิ้นสุดไปแล้ว | เตือนในขั้นตรวจสอบ ไม่บล็อก |
| EC-02 | ผู้ขอเป็นผู้ถือ role-compliance | resolve ข้ามตัวเอง → slot ว่างต้องเลือกคนอื่น |
| EC-03 | DOA > 4 ขั้น | PDF 2 แถว dense 1 หน้า |
| EC-04 | แก้ DOA ระหว่างรอพิจารณา | ใช้สาย snapshot |
| EC-05 | stale | 409 STALE → toast รีเฟรช |
| EC-06 | doc_type ปิดใช้ | ปุ่มสร้าง disabled · API-03 409 |
| EC-07 | "เอกสารสำคัญอื่นๆ" ไม่มีช่องระบุชื่อ | ระบุในไฟล์แนบ — DEC-12 (OQ-05) |
| EC-08 | เบิก/ยืม·แก้ไข·ยกเลิกทำใหม่ ไม่มีช่องอ้างทะเบียนเดิม | ผู้ดูแลค้นเอง — DEC-13 (OQ-04) |

## §5.6 Events
ctr_registered · ctr_original_received · ctr_cancelled (NTF_BRIEF_F-TMP-009)
