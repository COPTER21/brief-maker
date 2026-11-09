# 05_RULES — F-TMP-005
> [AI-DEFAULT] = มติที่ AI ตอบตาม unattended-policy — ต้องให้ลูกค้ายืนยันในใบลงนามก่อน UAT

## §5.1 Business Rules
| ID | Rule | Tag | อ้าง |
|---|---|:-:|---|
| BR-01 | ประเภทของการเปลี่ยนแปลง เลือกได้หลายข้อ อย่างน้อย 1 ข้อ [AI-DEFAULT] | FIXED | DEC-04 · DEC-16 |
| BR-02 | ติ๊ก อื่นๆ ต้องระบุข้อความ | FIXED | DEC-15 |
| BR-03 | วันที่ต้องการส่งมอบก่อนวันที่ขอ = เตือน ไม่บล็อก [AI-DEFAULT] | CONFIGURABLE | DEC-04 · DEC-14 |
| BR-04 | สายอนุมัติ resolve จาก DOA ตอนส่งแล้ว freeze · จำนวนขั้นตาม DOA (ค่าเริ่ม 2 ขั้น role-line-manager "ตรวจสอบโดย" → role-mgr-it "อนุมัติโดย") [AI-DEFAULT] | FIXED | DEC-03 |
| BR-05 | ไม่อนุมัติ (ขั้นใดก็ได้) → กลับร่างเลขเดิม (BR-DOA-03 ตามปกติ) [AI-DEFAULT] | FIXED | DEC-08 |
| BR-06 | เลข ITCR ออกตอนบันทึกครั้งแรก · no-gap ✗ | CONFIGURABLE | DEC-10 |
| BR-07 | ร่างเห็นเฉพาะเจ้าของ + role-it-officer | FIXED | DEC-09 |
| BR-08 | ช่องลงชื่อ PDF = ผู้ขอซื้อ + 1 ช่อง/ขั้น DOA · ข้อความในระบบ ไม่ใช้ภาพ | FIXED | DEC-07 · DEC-13 |
| BR-09 | ไม่เปลี่ยนค่าในระบบ · ไม่ส่งต่อระบบอื่น · อนุมัติครบแจ้ง role-it-officer | FIXED | DEC-01 · DEC-02 |
| BR-10 | ช่อง/ป้ายตามกระดาษ 1:1 · แก้สะกด ตำแหน่ง · คงป้าย ผู้ขอซื้อ · เลขที่แสดงที่ footer | FIXED | DEC-06 · DEC-12 · DEC-13 · DEC-17 |
| BR-11 | Doc. No./Rev. แบบพิมพ์จาก print_config (FM-ITS-07 · Rev.00 : 01/07/2569) | CONFIGURABLE | DEC-10 |
| BR-12 | แนบไฟล์ ✓ · CSV ✓ · ทำซ้ำ ✗ · ประกาศ ✗ | FIXED | DEC-11 |
| BR-13 | ไม่มีรายการซ้ำบนแบบฟอร์ม | FIXED | DEC-05 |
| BR-DOA-01..05 | ส่งได้เฉพาะ draft · resolve ตอนส่ง freeze · ไม่อนุมัติ→draft · ผู้ขออนุมัติตัวเองไม่ได้ · (ไม่มีวงเงิน) · field approver_role / approved_by / approval_chain + `TODO: DOA engine` | FIXED | DOA contract |

## §5.2 ENG-NOTIFY
| event | trigger | ผู้รับ |
|---|---|---|
| itcr_cancelled | pending → cancelled | ผู้พิจารณาขั้นปัจจุบัน |
| itcr_approved_for_it | pending → approved | role-it-officer |

## §5.3 สิทธิ์ (DEC-09)
| Action | เจ้าของ | ผู้พิจารณาขั้นปัจจุบัน | ผู้อยู่ในสาย (ไม่ใช่ขั้นปัจจุบัน) | role-it-officer | คนอื่น |
|---|:-:|:-:|:-:|:-:|:-:|
| ดูร่าง | ✓ | ✗ | ✗ | ✓ | ✗ |
| ดูหลังส่ง | ✓ | ✓ | ✓ | ✓ | ✗ |
| แก้ไข | ร่าง | ✗ | ✗ | ✗ | ✗ |
| อนุมัติ/ไม่อนุมัติ | ✗ | ✓ | ✗ | ✗ | ✗ |
| ยกเลิก | ร่าง/รอ | ✗ | ✗ | ร่าง/รอ | ✗ |

## §5.4 Validation
| VR | ช่อง | เงื่อนไข | ข้อความ |
|---|---|---|---|
| VR-01 | subject | required | ระบุเรื่องที่ต้องการ |
| VR-02 | change_types | ≥1 | เลือกประเภทของการเปลี่ยนแปลงอย่างน้อย 1 ข้อ |
| VR-03 | change_type_other | required เมื่อ other | ระบุประเภทอื่นๆ |
| VR-04 | due_date | required | เลือกวันที่ต้องการส่งมอบ |
| VR-05 | delivery_location | required | ระบุสถานที่ส่งมอบ |
| VR-06 | change_detail | required | ระบุรายละเอียดของการเปลี่ยนแปลง |
| VR-07 | objective | required | ระบุวัตถุประสงค์ของการเปลี่ยนแปลง |
| VR-08 | impact | required | ระบุระบบที่ได้รับผลกระทบและผลกระทบที่อาจเกิดขึ้น |
| VR-09 | action_plan | required | ระบุแผนการดำเนินการ |
| VR-10 | assignees | ครบทุกขั้น · ≠ ผู้ขอ | กรุณาเลือกผู้พิจารณา |
| VR-11 | reason (ไม่อนุมัติ/ยกเลิก) | required | กรุณาระบุเหตุผล |

## §5.5 Edge Cases
| EC | กรณี | ผล |
|---|---|---|
| EC-01 | due_date < request_date (DEC-14) | warning ส่งได้ |
| EC-02 | other ไม่ระบุ (DEC-15) | VR-03 บล็อก |
| EC-03 | ไม่ติ๊กประเภท (DEC-16) | VR-02 บล็อก |
| EC-04 | ข้อความเกินบรรทัดกระดาษ | PDF dense 1 หน้า |
| EC-05 | DOA 6 ขั้น | ลายเซ็น 7 ช่อง 4+3 |
| EC-06 | ผู้ขอไม่มีผู้บังคับบัญชา / เป็นผู้จัดการฝ่าย IT เอง | slot ว่าง/ต้องเลือกคนอื่น (SELF_APPROVE) |
| EC-07 | แก้ DOA ระหว่างรอ | ใช้ snapshot |
| EC-08 | stale | 409 STALE |
| EC-09 | doc_type ปิด | 409 DOC_TYPE_INACTIVE · ปุ่มสร้าง disabled |
| EC-10 | เปิดใบที่ไม่มีสิทธิ์ | 404 / ไม่เปิด drawer |
| EC-11 | ไม่อนุมัติที่ขั้น 2 | กลับร่างทั้งใบ · ส่งใหม่เริ่มขั้น 1 |

## §5.6 Errors
DOC_TYPE_INACTIVE · NOT_OWNER · NOT_DRAFT · STALE · ASSIGNEE_REQUIRED · SELF_APPROVE · NOT_CURRENT_APPROVER · REASON_REQUIRED · NOT_FOUND
