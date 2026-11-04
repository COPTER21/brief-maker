# 05_RULES — F-TMP-002

## §5.1 Business Rules
| BR | กฎ | ระดับ | ที่มา |
|---|---|---|---|
| BR-01 | อายุตัว/อายุงานคำนวณถึง ref_date (วันที่ลาออก หรือ contract_end_date) · ผู้ใช้ปรับได้ (calc_manual) | CONFIGURABLE [AI-DEFAULT] | DEC-04 |
| BR-02 | ลักษณะพ้นงานเลือก 1 · resign ⇒ resign_date บังคับ ≥ hire_date · contract_end ⇒ ข้อ 5 บังคับ · อื่น ๆ ต้องระบุ | FIXED | DEC-14 (VALID) |
| BR-03 | ส่วนที่ 2 ตอบครบ 26 ข้อ ข้อละ 1 ระดับก่อนส่ง | FIXED | DEC-16 (VALID) |
| BR-04 | ส่วนที่ 3 ≥ 1 ปัจจัย · rank 1..N ไม่ซ้ำ ต่อเนื่อง · other ⇒ exit_reasons_other_text บังคับ | FIXED | DEC-15 (VALID) · DEC-05 |
| BR-05 | ส่วนที่ 4 ไม่จำกัดแถว ไม่บังคับ · PDF ≥ 5 แถว (print_config.min_rows) | FIXED [AI-DEFAULT] | DEC-06 |
| BR-06 | ความลับ: เห็นได้เฉพาะ owner · ผู้ให้ข้อมูล · role-mgr-hr (+ผู้พิจารณาหลังส่ง ถ้าตั้ง DOA) · ผู้บังคับบัญชาไม่มีสิทธิ์ | FIXED [AI-DEFAULT] | DEC-09 · DEC-17 (VALID) |
| BR-07 | เลข EXI ออกตอนบันทึกครั้งแรก · ส่งกลับใช้เลขเดิม | FIXED | DEC-10 |
| BR-08 | ไม่มีขั้นพิจารณา — ส่งแล้วจบที่ submitted · HR รับรู้ผ่านแจ้งเตือน exi_submitted · ต้องการขั้นเพิ่ม = change request (OQ-02) | FIXED [AI-DEFAULT] | DEC-03 |
| BR-09 | ช่องลงชื่อ PDF = ผู้ให้ข้อมูล + 1 ช่องต่อขั้น DOA · ข้อความ "ส่งในระบบ วันที่ เวลา" ไม่ใช้ภาพ | FIXED | DEC-08 |
| BR-10 | ไม่มีการเปลี่ยนค่าในระบบ / ไม่ส่งต่อ (สถานะพนักงานทำที่ HR · Offboard) | FIXED [AI-DEFAULT] | DEC-01 · DEC-02 |
| BR-11 | ยกเลิก: owner/ผู้ให้ข้อมูล/HR · draft/submitted · เหตุผลบังคับ | CONFIGURABLE [AI-DEFAULT] | policy G7 |
| BR-12 | แนบไฟล์ ✓ · CSV ✓ (ตามสิทธิ์) · ทำซ้ำ ✗ · ประกาศ ✗ | FIXED [AI-DEFAULT] | DEC-11 |
| BR-13 | ถ้อยคำตามกระดาษ 1:1 · แก้ "โปรดกรอบ"→"โปรดกรอก" · "P"→✓ | FIXED | DEC-07 · DEC-12 · DEC-13 (VALID) |
| BR-14 | ส่งแล้วล็อกแก้ไข | FIXED | DEC-07 |

## §5.2 State Machine
| จาก | การกระทำ | ไป | ผู้ทำ |
|---|---|---|---|
| — | บันทึกครั้งแรก | draft | owner |
| draft | ส่ง (0 ขั้น) | submitted | owner |
| draft/submitted | ยกเลิก | cancelled | owner · ผู้ให้ข้อมูล · role-mgr-hr |

## §5.3 Permission Matrix
| action | owner | ผู้ให้ข้อมูล (ไม่ใช่ owner) | role-mgr-hr | ผู้บังคับบัญชา | อื่น ๆ |
|---|---|---|---|---|---|
| ดูรายการ/ใบ | ✓ | ✓ | ✓ ทุกใบ | ✗ (404) | ✗ |
| สร้าง | ✓ (ของตัวเอง) | — | ✓ แทนผู้อื่น | ✓ ของตัวเองเท่านั้น | ✓ ของตัวเอง |
| แก้ร่าง / ส่ง | ✓ | ✗ | เฉพาะร่างที่ตัวเองสร้าง | ✗ | ✗ |
| ยกเลิก | ✓ | ✓ | ✓ | ✗ | ✗ |
| พิมพ์ / CSV | ✓ (ใบที่เห็น) | ✓ | ✓ | ✗ | ✗ |

## §5.4 Validation
| VR | field | กฎ | ข้อความ |
|---|---|---|---|
| VR-01 | employee_id | required (HR สร้างแทน) | กรุณาเลือกผู้ให้ข้อมูล |
| VR-02 | resign_date | required เมื่อ resign · ≥ hire_date | กรุณาเลือกวันที่ลาออก (ไม่ก่อนวันเริ่มงาน) |
| VR-03 | contract_end_reason | required เมื่อ contract_end | เลือกเหตุผลกรณีครบสัญญาจ้าง |
| VR-04 | contract_end_other | required เมื่อ other | กรุณาระบุ |
| VR-05 | age_years / service_months | 15–80 · 0–11 | 15–80 ปี · เดือน 0–11 |
| VR-06 | ratings | ครบ q01..q26 ค่า 1..5 | ยังไม่ได้ตอบ n ข้อ — ตอบให้ครบทุกข้อ |
| VR-07 | exit_reasons | ≥1 · rank unique ต่อเนื่อง | เลือกอย่างน้อย 1 ปัจจัย |
| VR-08 | exit_reasons_other_text | required เมื่อเลือก other | กรุณาระบุ |
| VR-09 | reason (cancel/return) | required | กรุณาระบุเหตุผล |

## §5.5 Edge Cases
| EC | กรณี | ผล | อ้าง |
|---|---|---|---|
| EC-01 | ไม่มี birth_date | age_years ว่าง กรอกเอง | BR-01 |
| EC-02 | resign_date < hire_date | บล็อก VR-02 | BR-02 |
| EC-03 | contract_end ไม่มี contract_end_date | คิดถึงวันนี้ · ปรับได้ | BR-01 |
| EC-04 | เลือกครบ 21 ปัจจัย | PDF [1]..[21] | DEC-05 |
| EC-05 | ข้อเสนอแนะ 12 แถว | PDF dense · แถวไม่ถูกตัด | DEC-06 |
| EC-06 | ผู้บังคับบัญชาเปิด URL ใบลูกน้อง | 404 | DEC-17 |
| EC-07 | HR สร้างแทน → พนักงานเปิดดู | เห็นได้ · แก้ร่างไม่ได้ | BR-06 |
| EC-08 | ส่งแล้วต้องแก้ | ยกเลิก + สร้างใหม่ | BR-14 |
| EC-09 | F-DOCCFG ปิด EXI | 409 DOC_TYPE_INACTIVE · ปุ่มสร้าง disabled | BR-07 |
| EC-10 | ลูกค้าขอเพิ่มขั้นพิจารณาภายหลัง | change request (OQ-02) · ใบที่ส่งแล้วไม่ย้อน | BR-08 |
