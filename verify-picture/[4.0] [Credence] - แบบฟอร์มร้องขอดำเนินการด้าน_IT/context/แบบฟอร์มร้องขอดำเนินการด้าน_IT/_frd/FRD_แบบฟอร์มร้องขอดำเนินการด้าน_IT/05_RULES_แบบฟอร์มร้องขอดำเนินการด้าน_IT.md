# 05_RULES — F-TMP-001
> [AI-DEFAULT] = มติที่ AI ตอบตาม unattended-policy — ต้องให้ลูกค้ายืนยันในใบลงนามก่อน UAT

## §5.1 Business Rules
| ID | Rule | Tag | อ้าง |
|---|---|:-:|---|
| BR-01 | ประเภทงานเลือกได้หลายข้อ อย่างน้อย 1 [AI-DEFAULT] | FIXED | DEC-04 |
| BR-02 | ติ๊ก อื่นๆ ต้องระบุข้อความ | FIXED | DEC-15 |
| BR-03 | วันที่ต้องการส่งมอบก่อนวันที่ขอ = เตือน ไม่บล็อก [AI-DEFAULT] | CONFIGURABLE | DEC-04 · DEC-14 |
| BR-04 | สายอนุมัติ resolve จาก DOA ตอนส่งแล้ว freeze · จำนวนขั้นตาม DOA (ค่าเริ่ม 1 ขั้น role-line-manager) [AI-DEFAULT] | FIXED | DEC-03 |
| BR-05 | ไม่อนุมัติ → กลับร่างเลขเดิม (BR-DOA-03 ตามปกติ) [AI-DEFAULT] | FIXED | DEC-08 |
| BR-06 | เลข ITRS ออกตอนบันทึกครั้งแรก · no-gap ✗ | CONFIGURABLE | DEC-10 |
| BR-07 | ร่างเห็นเฉพาะเจ้าของ + role-it-officer | FIXED | DEC-09 |
| BR-08 | ช่องลงชื่อ PDF = ผู้ร้องขอ + 1 ช่อง/ขั้น DOA + ดำเนินการโดย · ข้อความในระบบ ไม่ใช้ภาพ | FIXED | DEC-07 |
| BR-09 | ดำเนินการแล้ว = role-it-officer · status approved เท่านั้น [AI-DEFAULT] | FIXED | DEC-03 · DEC-09 |
| BR-10 | ไม่เปลี่ยนค่าในระบบ · ไม่ส่งต่อระบบอื่น | FIXED | DEC-01 · DEC-02 |
| BR-11 | ช่อง/ป้ายตามกระดาษ 1:1 · แก้สะกด ตำแหน่ง | FIXED | DEC-06 · DEC-13 |
| BR-12 | Rev. แบบพิมพ์จาก print_config (ค่าเริ่ม Rev.00) | CONFIGURABLE | DEC-12 |
| BR-13 | แนบไฟล์ ✓ · CSV ✓ · ทำซ้ำ ✗ · ประกาศ ✗ | FIXED | DEC-11 |
| BR-14 | ไม่มีรายการซ้ำบนแบบฟอร์ม | FIXED | DEC-05 |
| BR-DOA-01..05 | ส่งได้เฉพาะ draft · resolve ตอนส่ง freeze · ไม่อนุมัติ→draft · ผู้ขออนุมัติตัวเองไม่ได้ · (ไม่มีวงเงิน) | FIXED | DOA contract |

## §5.2 ENG-NOTIFY
| event | trigger | ผู้รับ |
|---|---|---|
| itrs_cancelled | pending → cancelled | ผู้พิจารณาขั้นปัจจุบัน |
| itrs_ready_for_it | pending → approved | role-it-officer |
| itrs_completed | approved → done | ผู้ร้องขอ |

## §5.3 สิทธิ์ (DEC-09)
| Action | เจ้าของ | ผู้พิจารณาขั้นปัจจุบัน | ผู้อยู่ในสาย (ไม่ใช่ขั้นปัจจุบัน) | role-it-officer | คนอื่น |
|---|:-:|:-:|:-:|:-:|:-:|
| ดูร่าง | ✓ | ✗ | ✗ | ✓ | ✗ |
| ดูหลังส่ง | ✓ | ✓ | ✓ | ✓ | ✗ |
| แก้ไข | ร่าง | ✗ | ✗ | ✗ | ✗ |
| อนุมัติ/ไม่อนุมัติ | ✗ | ✓ | ✗ | ✗ | ✗ |
| ดำเนินการแล้ว | ✗ | ✗ | ✗ | approved | ✗ |
| ยกเลิก | ร่าง/รอ | ✗ | ✗ | ร่าง/รอ | ✗ |

## §5.4 Validation
| VR | ช่อง | เงื่อนไข | ข้อความ |
|---|---|---|---|
| VR-01 | subject | required | ระบุเรื่องที่ต้องการ |
| VR-02 | job_types | ≥1 | เลือกประเภทงานอย่างน้อย 1 ข้อ |
| VR-03 | job_type_other | required เมื่อ other | ระบุงานอื่นๆ |
| VR-04 | due_date | required | เลือกวันที่ต้องการส่งมอบ |
| VR-05 | delivery_location | required | ระบุสถานที่ส่งมอบ |
| VR-06 | detail | required | ระบุรายละเอียดการร้องขอ |
| VR-07 | reason | required | ระบุเหตุผล วัตถุประสงค์ หรือความจำเป็น |
| VR-08 | assignees | ครบทุกขั้น · ≠ ผู้ร้องขอ | กรุณาเลือกผู้พิจารณา |
| VR-09 | reason (ไม่อนุมัติ/ยกเลิก) | required | กรุณาระบุเหตุผล |

## §5.5 Edge Cases
| EC | กรณี | ผล |
|---|---|---|
| EC-01 | due_date < req_date (DEC-14) | warning ส่งได้ |
| EC-02 | other ไม่ระบุ (DEC-15) | VR-03 |
| EC-03 | ข้อความเกินบรรทัดกระดาษ | PDF dense 1 หน้า |
| EC-04 | DOA 6 ขั้น | ลายเซ็น 8 ช่อง 4+4 |
| EC-05 | ผู้ร้องขอไม่มีผู้บังคับบัญชา | slot ว่างให้เลือก |
| EC-06 | แก้ DOA ระหว่างรอ | ใช้ snapshot |
| EC-07 | stale | 409 STALE |
| EC-08 | doc_type ปิด | 409 DOC_TYPE_INACTIVE · ปุ่มสร้าง disabled |
| EC-09 | เปิดใบที่ไม่มีสิทธิ์ | 404 / ไม่เปิด drawer |
| EC-10 | ไม่มี Rev. (DEC-12) | Rev.00 จาก print_config |

## §5.6 Errors
DOC_TYPE_INACTIVE · NOT_OWNER · NOT_DRAFT · STALE · ASSIGNEE_REQUIRED · SELF_APPROVE · NOT_CURRENT_APPROVER · REASON_REQUIRED · NOT_IT_OFFICER · NOT_APPROVED · NOT_FOUND
