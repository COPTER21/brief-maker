# 05_RULES — F-TMP-004

## §5.1 Business Rules
| BR | กฎ | ระดับ | ที่มา |
|---|---|---|---|
| BR-01 | ชื่อตำแหน่ง (ไทย)/แผนก/ฝ่าย จาก Position master (snapshot ตอนบันทึก) · reports_to ค่าเริ่มจาก master แก้ได้ · ไม่แก้ master | CONFIGURABLE [AI-DEFAULT] | DEC-04 · DEC-01 |
| BR-02 | position_name_en · reports_to · job_purpose · key_responsibilities · job_specification · kpi บังคับก่อนส่ง · other_qualifications ไม่บังคับ | FIXED [AI-DEFAULT] | DEC-04 |
| BR-03 | superiors ≥ 1 แถวที่มีตำแหน่ง (บล็อก) · superiors[0].position ≠ reports_to = เตือน ไม่บล็อก | FIXED | DEC-14 (VALID) |
| BR-04 | headcount จำนวนเต็ม ≥ 1 เมื่อมีตำแหน่ง · มี headcount ไม่มีตำแหน่ง = บล็อก | FIXED | DEC-15 (VALID) |
| BR-05 | subordinate_summary คำนวณจาก subordinates (ไม่ให้กรอกซ้ำ) | FIXED | DEC-13 (VALID) |
| BR-06 | แถวหัวหน้า/ลูกน้องไม่จำกัด · PDF ≥ 3 แถว (print_config.min_rows) | FIXED [AI-DEFAULT] | DEC-05 · DEC-06 |
| BR-07 | สายอนุมัติ resolve จาก DOA กลางตอนส่ง แล้ว freeze ใน approval_chain · ค่าเริ่ม 1 ขั้น role-line-manager · ห้าม hardcode | CONFIGURABLE (DOA กลาง) [AI-DEFAULT] | DEC-03 |
| BR-08 | ไม่อนุมัติ = กลับร่างเลขเดิม (BR-DOA-03 มาตรฐาน) · เหตุผลบังคับ | FIXED [AI-DEFAULT] | DEC-09 |
| BR-09 | ผู้จัดทำอนุมัติใบตัวเองไม่ได้ (BR-DOA-04) | FIXED | DEC-03 |
| BR-10 | อนุมัติขั้นสุดท้าย → ใบ approved/acknowledged อื่นของ position_id เดียวกัน → superseded | FIXED [AI-DEFAULT] | DEC-04 |
| BR-11 | รับทราบได้เฉพาะ acknowledged_by และ status = approved · ไม่บังคับ (ตำแหน่งว่าง) · HR ระบุ/เปลี่ยนผู้ดำรงตำแหน่งได้เมื่อ approved | FIXED | DEC-16 (VALID) · DEC-04 |
| BR-12 | เห็น: owner · ผู้อนุมัติหลังส่ง · role-mgr-hr ทั้งหมด · ผู้ดำรงตำแหน่งเฉพาะใบ approved/acknowledged/superseded ของตน | FIXED [AI-DEFAULT] | DEC-10 |
| BR-13 | เลข JD ออกตอนบันทึกครั้งแรก · ไม่อนุมัติใช้เลขเดิม | FIXED | DEC-11 |
| BR-14 | ช่องลงชื่อ PDF = ผู้จัดทำ + 1 ช่องต่อขั้น DOA + ผู้ดำรงตำแหน่ง · ข้อความ "ส่งในระบบ/พิจารณาในระบบ/รับทราบในระบบ วันที่ เวลา" ไม่ใช้ภาพ | FIXED | DEC-08 |
| BR-15 | ยกเลิก: owner/HR · draft/pending · เหตุผลบังคับ · แนบไฟล์ ✓ · CSV ✓ (ตามสิทธิ์) · ทำซ้ำ ✗ · ประกาศ ✗ · ไม่ส่งต่อระบบอื่น | CONFIGURABLE [AI-DEFAULT] | DEC-09 · DEC-12 · DEC-02 |
| BR-16 | ถ้อยคำตามกระดาษ 1:1 · ส่งแล้วล็อกแก้ไข | FIXED | DEC-07 · DEC-17 (VALID) |

## §5.2 State Machine
| จาก | การกระทำ | ไป | ผู้ทำ |
|---|---|---|---|
| — | บันทึกครั้งแรก | draft | owner |
| draft | ส่งอนุมัติ | pending | owner |
| pending | อนุมัติ (ไม่ใช่ขั้นสุดท้าย) | pending (ขั้นถัดไป) | ผู้อนุมัติขั้นปัจจุบัน |
| pending | อนุมัติขั้นสุดท้าย | approved | ผู้อนุมัติขั้นปัจจุบัน |
| pending | ไม่อนุมัติ | draft (เลขเดิม) | ผู้อนุมัติขั้นปัจจุบัน |
| approved | รับทราบ | acknowledged | ผู้ดำรงตำแหน่ง |
| approved/acknowledged | ฉบับใหม่ของตำแหน่งเดียวกันอนุมัติ | superseded | ระบบ |
| draft/pending | ยกเลิก | cancelled | owner · role-mgr-hr |

## §5.3 Permission Matrix
| action | owner | ผู้อนุมัติ (ใน chain) | ผู้ดำรงตำแหน่ง | role-mgr-hr | อื่น ๆ |
|---|---|---|---|---|---|
| ดูรายการ/ใบ | ✓ | ✓ หลังส่ง (ไม่เห็นร่าง) | ✓ เฉพาะ approved+ ของตน | ✓ ทุกใบ | ✗ (404) |
| สร้าง | ✓ | ✓ | ✓ | ✓ | ✓ |
| แก้ร่าง / ส่ง | ✓ | ✗ | ✗ | ✗ (เว้นร่างที่ตัวเองสร้าง) | ✗ |
| อนุมัติ / ไม่อนุมัติ | ✗ (BR-09) | ✓ เฉพาะขั้นปัจจุบัน | ✗ | ✗ | ✗ |
| ระบุผู้ดำรงตำแหน่ง | ✗ | ✗ | ✗ | ✓ (approved) | ✗ |
| รับทราบ | ✗ | ✗ | ✓ | ✗ | ✗ |
| ยกเลิก | ✓ (draft/pending) | ✗ | ✗ | ✓ | ✗ |
| พิมพ์ / CSV | ✓ (ใบที่เห็น) | ✓ | ✓ | ✓ | ✗ |

## §5.4 Validation
| VR | field | กฎ | ข้อความ |
|---|---|---|---|
| VR-01 | position_id | required | กรุณาเลือกตำแหน่ง |
| VR-02 | position_name_en | required | กรุณาระบุชื่อตำแหน่งภาษาอังกฤษ |
| VR-03 | reports_to | required | กรุณาระบุตำแหน่งที่รายงานต่อ |
| VR-04 | job_purpose · key_responsibilities · job_specification · kpi | required | กรุณากรอก{หัวข้อ} |
| VR-05 | superiors | ≥1 แถวมีตำแหน่ง (DEC-14) | ต้องมีผู้บังคับบัญชาโดยตรงอย่างน้อย 1 แถว |
| VR-06 | superiors[]/subordinates[].headcount | จำนวนเต็ม ≥1 เมื่อมีตำแหน่ง (DEC-15) | จำนวน (คน) ต้องเป็นจำนวนเต็มตั้งแต่ 1 |
| VR-07 | superiors[]/subordinates[].position | required เมื่อมี headcount | กรอกจำนวนแล้วต้องระบุตำแหน่ง |
| VR-08 | assignees (submit) | ครบทุกขั้น · ≠ owner | กรุณาเลือกผู้อนุมัติ |
| VR-09 | reason (cancel/reject) | required | กรุณาระบุเหตุผล |
- เตือน (ไม่บล็อก) W-01: superiors[0].position ≠ reports_to — "หัวหน้าแถวแรกไม่ตรงกับ "รายงานต่อ"" (DEC-14)
- DEC-13 → BR-05 · DEC-16 → BR-11 / EC-06 · DEC-17 → BR-16

## §5.5 Edge Cases
| EC | กรณี | ผล | อ้าง |
|---|---|---|---|
| EC-01 | ตำแหน่งไม่มี reports_to (สูงสุด) | reports_to/superiors ว่าง ให้กรอกเอง | BR-01 · BR-03 |
| EC-02 | resolve role-line-manager ไม่ได้ | slot ว่าง บังคับเลือกตอนส่ง | BR-07 |
| EC-03 | ตำแหน่งมีฉบับใช้งานอยู่ | เตือนตอนสร้าง/ส่ง · อนุมัติแล้วฉบับเดิม superseded | BR-10 |
| EC-04 | ลูกน้อง 12 แถว + ข้อความยาว | PDF dense · บล็อกลงนามไม่ตัดกลาง | BR-06 |
| EC-05 | DOA ตั้ง 6 ขั้น | ลงนาม 8 ช่อง 2 แถว (4+4) | BR-14 |
| EC-06 | ผู้ดำรงตำแหน่งเปิดใบที่ยังรออนุมัติ | 404 | BR-12 · DEC-16 |
| EC-07 | ผู้จัดทำเป็นผู้ดำรงตำแหน่งเอง | รับทราบได้หลังอนุมัติ (ไม่ใช่อนุมัติตัวเอง) | BR-11 |
| EC-08 | ส่งแล้วต้องแก้ | ผู้อนุมัติไม่อนุมัติ → ร่าง หรือยกเลิกแล้วสร้างใหม่ | BR-08 · BR-15 |
| EC-09 | F-DOCCFG ปิด JD | 409 DOC_TYPE_INACTIVE · ปุ่มสร้าง disabled | BR-13 |
| EC-10 | headcount พิมพ์ตัวอักษร/0 | ตัดเหลือตัวเลข · 0 = บล็อก VR-06 | BR-04 |

## §5.6 การอนุมัติ (DOA)
- ดู `declarations/DOA_BRIEF_F-TMP-004.md` (entry DOA-JD-01 · document_sign · dynamic · ไม่มีวงเงิน · merged) · field approval_required / approver_role / approved_by / approval_chain / approved_at / doa_ref · `TODO: DOA engine`
