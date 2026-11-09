# 05_RULES — F-TMP-003
> [AI-DEFAULT] = มติที่ AI ตอบตาม unattended-policy — ต้องให้ลูกค้ายืนยันในใบลงนามก่อน UAT

## §5.1 Business Rules
| ID | Rule | Tag | อ้าง |
|---|---|:-:|---|
| BR-01 | ประเภทข้อมูล · เหตุผล · วิธีการ เลือกได้หลายข้อ อย่างน้อย 1 ต่อกลุ่ม [AI-DEFAULT] | FIXED | DEC-04 · DEC-17 |
| BR-02 | ติ๊ก อื่นๆ(โปรดระบุ) ต้องระบุข้อความ | FIXED | DEC-16 |
| BR-03 | ช่วงเวลาของข้อมูล ถึง ต้องไม่ก่อน จาก | FIXED | DEC-15 |
| BR-04 | ช่วงเวลาของข้อมูล ถึง หลังวันที่ขอ = เตือน ไม่บล็อก [AI-DEFAULT] | CONFIGURABLE | DEC-04 · DEC-15 |
| BR-05 | สายอนุมัติ resolve จาก DOA ตอนส่งแล้ว freeze · จำนวนขั้นตาม DOA (ค่าเริ่ม 2 ขั้น role-line-manager → role-mgr-it) [AI-DEFAULT] | FIXED | DEC-03 |
| BR-06 | ไม่อนุมัติ (ขั้นใดก็ได้) → กลับร่างเลขเดิม (BR-DOA-03 ตามปกติ) [AI-DEFAULT] | FIXED | DEC-08 |
| BR-07 | เลข DRITS ออกตอนบันทึกครั้งแรก · no-gap ✗ | CONFIGURABLE | DEC-10 |
| BR-08 | ร่างเห็นเฉพาะเจ้าของ + role-it-officer | FIXED | DEC-09 |
| BR-09 | ช่องลงชื่อ PDF = ผู้ร้องขอ + 1 ช่อง/ขั้น DOA + เจ้าหน้าที่ IT · ข้อความในระบบ ไม่ใช้ภาพ | FIXED | DEC-07 |
| BR-10 | บันทึกการทำลายแล้ว = role-it-officer · status approved เท่านั้น [AI-DEFAULT] | FIXED | DEC-03 · DEC-09 |
| BR-11 | ไม่เปลี่ยนค่าในระบบ · ไม่ส่งต่อระบบอื่น | FIXED | DEC-01 · DEC-02 |
| BR-12 | ช่อง/ป้ายตามกระดาษ 1:1 · แก้สะกด ตำแหน่ง · อนุมัติ · ☐ ครบทุกตัวเลือก | FIXED | DEC-06 · DEC-12 · DEC-13 · DEC-14 |
| BR-13 | Doc. No./Rev. แบบพิมพ์จาก print_config (FM-ITS-02 · Rev.00 : 01/07/2569) | CONFIGURABLE | DEC-10 |
| BR-14 | แนบไฟล์ ✓ · CSV ✓ · ทำซ้ำ ✗ · ประกาศ ✗ | FIXED | DEC-11 |
| BR-15 | ไม่มีรายการซ้ำบนแบบฟอร์ม | FIXED | DEC-05 |
| BR-DOA-01..05 | ส่งได้เฉพาะ draft · resolve ตอนส่ง freeze · ไม่อนุมัติ→draft · ผู้ขออนุมัติตัวเองไม่ได้ · (ไม่มีวงเงิน) | FIXED | DOA contract |

## §5.2 ENG-NOTIFY
| event | trigger | ผู้รับ |
|---|---|---|
| drits_cancelled | pending → cancelled | ผู้พิจารณาขั้นปัจจุบัน |
| drits_ready_for_it | pending → approved | role-it-officer |
| drits_destroyed | approved → done | ผู้ร้องขอ |

## §5.3 สิทธิ์ (DEC-09)
| Action | เจ้าของ | ผู้พิจารณาขั้นปัจจุบัน | ผู้อยู่ในสาย (ไม่ใช่ขั้นปัจจุบัน) | role-it-officer | คนอื่น |
|---|:-:|:-:|:-:|:-:|:-:|
| ดูร่าง | ✓ | ✗ | ✗ | ✓ | ✗ |
| ดูหลังส่ง | ✓ | ✓ | ✓ | ✓ | ✗ |
| แก้ไข | ร่าง | ✗ | ✗ | ✗ | ✗ |
| อนุมัติ/ไม่อนุมัติ | ✗ | ✓ | ✗ | ✗ | ✗ |
| บันทึกการทำลายแล้ว | ✗ | ✗ | ✗ | approved | ✗ |
| ยกเลิก | ร่าง/รอ | ✗ | ✗ | ร่าง/รอ | ✗ |

## §5.4 Validation
| VR | ช่อง | เงื่อนไข | ข้อความ |
|---|---|---|---|
| VR-01 | detail | required | ระบุรายละเอียดของข้อมูลที่ต้องการทำลาย |
| VR-02 | program | required | ระบุโปรแกรมที่เก็บข้อมูล |
| VR-03 | data_types | ≥1 | เลือกประเภทข้อมูลอย่างน้อย 1 ข้อ |
| VR-04 | period_from | required | เลือกวันที่เริ่มต้นของข้อมูล |
| VR-05 | period_to | required · ≥ period_from | เลือกวันที่สิ้นสุดของข้อมูล / วันที่ "ถึง" ต้องไม่ก่อนวันที่ "จาก" |
| VR-06 | destroy_reasons | ≥1 | เลือกเหตุผลอย่างน้อย 1 ข้อ |
| VR-07 | destroy_reason_other | required เมื่อ other | โปรดระบุเหตุผลอื่นๆ |
| VR-08 | destroy_methods | ≥1 | เลือกวิธีการอย่างน้อย 1 ข้อ |
| VR-09 | destroy_method_other | required เมื่อ other | โปรดระบุวิธีการอื่นๆ |
| VR-10 | assignees | ครบทุกขั้น · ≠ ผู้ร้องขอ | กรุณาเลือกผู้พิจารณา |
| VR-11 | reason (ไม่อนุมัติ/ยกเลิก) | required | กรุณาระบุเหตุผล |

## §5.5 Edge Cases
| EC | กรณี | ผล |
|---|---|---|
| EC-01 | period_to < period_from (DEC-15) | VR-05 บล็อก |
| EC-02 | period_to > req_date (DEC-15) | warning ส่งได้ |
| EC-03 | other ไม่ระบุ (DEC-16) | VR-07 / VR-09 |
| EC-04 | ข้อความเกินบรรทัดกระดาษ | PDF dense 1 หน้า |
| EC-05 | DOA 6 ขั้น | ลายเซ็น 8 ช่อง 4+4 |
| EC-06 | ผู้ร้องขอไม่มีผู้บังคับบัญชา / เป็นผู้จัดการฝ่าย IT เอง | slot ว่าง/ต้องเลือกคนอื่น (SELF_APPROVE) |
| EC-07 | แก้ DOA ระหว่างรอ | ใช้ snapshot |
| EC-08 | stale | 409 STALE |
| EC-09 | doc_type ปิด | 409 DOC_TYPE_INACTIVE · ปุ่มสร้าง disabled |
| EC-10 | เปิดใบที่ไม่มีสิทธิ์ | 404 / ไม่เปิด drawer |
| EC-11 | ไม่อนุมัติที่ขั้น 2 | กลับร่างทั้งใบ · ส่งใหม่เริ่มขั้น 1 |

## §5.6 Errors
DOC_TYPE_INACTIVE · NOT_OWNER · NOT_DRAFT · STALE · ASSIGNEE_REQUIRED · SELF_APPROVE · NOT_CURRENT_APPROVER · REASON_REQUIRED · NOT_IT_OFFICER · NOT_APPROVED · NOT_FOUND
