# 05_RULES — F-TMP-007
> [AI-DEFAULT] = มติที่ AI ตอบตาม unattended-policy — ต้องให้ลูกค้ายืนยันในใบลงนามก่อน UAT

## §5.1 Business Rules
| ID | Rule | Tag | อ้าง |
|---|---|:-:|---|
| BR-01 | วัตถุประสงค์ เลือก 1 ข้อ (ขึ้นทะเบียนใหม่ · แก้ไขเอกสาร · ยกเลิก · อื่นๆ) [AI-DEFAULT] | FIXED | DEC-04 |
| BR-02 | ISSUE เลือก 1 ข้อ (DOA · Policy · WI · Form) [AI-DEFAULT] | FIXED | DEC-04 · DEC-14 |
| BR-03 | แก้ไขเอกสาร → ต้องกรอก Revision / ISSUE เดิม และ ใหม่ · ขึ้นทะเบียนใหม่ / อื่นๆ → ต้องกรอก ใหม่ (อื่นๆ อธิบายในกล่องใหม่) [AI-DEFAULT] | FIXED | DEC-04 · DEC-13 |
| BR-04 | ที่มา = อื่นๆ → ต้องกรอกรายละเอียด [AI-DEFAULT] | FIXED | DEC-04 |
| BR-05 | หน่วยงานที่ต้องได้รับการแจกจ่าย ≥1 · วิธีรับ ≥1 · E-mail → E-Mail รูปแบบถูก ≥1 ที่อยู่ [AI-DEFAULT] | FIXED | DEC-04 · DEC-16 |
| BR-06 | วันที่บังคับใช้เอกสาร ก่อนวันที่เขียนใบ DAR = เตือน ไม่บล็อก [AI-DEFAULT] | CONFIGURABLE | DEC-04 · DEC-15 |
| BR-07 | แถวเอกสารที่ต้องจัดทำ/ทบทวน: กรอก Document No. หรือ ชื่อเอกสาร ช่องใดช่องหนึ่ง ต้องกรอกอีกช่อง · ไม่จำกัดแถว · PDF ≥14 แถว (print_config.min_rows) [AI-DEFAULT] | FIXED | DEC-04 · DEC-05 |
| BR-08 | สายอนุมัติ resolve จาก DOA ตอนส่งแล้ว freeze · จำนวนขั้นตาม DOA (ค่าเริ่ม 4 ขั้น role-line-manager "ผู้ตรวจสอบ" → role-mgr-bu "ผู้อนุมัติ" → role-doc-controller "ผู้ควบคุมเอกสาร" → role-mgr-ocs "ผู้จัดการฝ่ายสำนักเลขานุการบริษัท") · ไม่มีวงเงิน [AI-DEFAULT] | FIXED | DEC-03 |
| BR-09 | ไม่อนุมัติ (ขั้นใดก็ได้) → กลับร่างเลขเดิม (BR-DOA-03 ตามปกติ) [AI-DEFAULT] | FIXED | DEC-08 |
| BR-10 | เลข DAR ออกตอนบันทึกครั้งแรก · no-gap ✗ [AI-DEFAULT] | CONFIGURABLE | DEC-10 |
| BR-11 | ร่างเห็นเฉพาะเจ้าของ + role-doc-controller (admin) · ผู้พิจารณาเห็นหลังส่ง [AI-DEFAULT] | FIXED | DEC-09 |
| BR-12 | ช่องลงชื่อ PDF = ผู้จัดทำ + 1 ช่อง/ขั้น DOA · แถวละ ≤4 · ข้อความในระบบ ไม่ใช้ภาพ [AI-DEFAULT] | FIXED | DEC-07 |
| BR-13 | ไม่เปลี่ยนค่าในระบบ · ไม่ส่งต่อระบบอื่น · อนุมัติครบแจ้งหน่วยงานแจกจ่าย + อีเมล (dar_distributed) [AI-DEFAULT] | FIXED | DEC-01 · DEC-02 |
| BR-14 | ช่อง/ป้ายตามกระดาษ 1:1 · หน่วยงานแจกจ่าย 27 ช่อง ชุดซ้ำติด "(2)" · ไม่เพิ่มช่อง [AI-DEFAULT] | FIXED | DEC-06 · DEC-12 |
| BR-15 | ลงนามรับเอกสารควบคุม = ข้อความระบบหลังอนุมัติครบ · role-doc-controller บันทึกผู้รับ · ไม่ใช่ขั้น DOA [AI-DEFAULT] | FIXED | DEC-07 |
| BR-16 | Doc. No./Rev. แบบพิมพ์จาก print_config (FM-CCC-03 · Rev.00 : 01/07/2569) · A4 2 หน้า | CONFIGURABLE | DEC-10 |
| BR-17 | แนบไฟล์ ✓ · CSV ✓ · ทำซ้ำ ✗ · ประกาศ ✗ [AI-DEFAULT] | FIXED | DEC-11 |
| BR-DOA-01..05 | ส่งได้เฉพาะ draft · resolve ตอนส่ง freeze · ไม่อนุมัติ→draft · ผู้จัดทำอนุมัติตัวเองไม่ได้ · (ไม่มีวงเงิน) · field approver_role / approved_by / approval_chain + `TODO: DOA engine` | FIXED | DOA contract |

## §5.2 ENG-NOTIFY
| event | trigger | ผู้รับ |
|---|---|---|
| dar_cancelled | pending → cancelled | ผู้พิจารณาขั้นปัจจุบัน |
| dar_distributed | pending → approved | หน่วยงานใน distribution_units + distribution_emails (บังคับ) |
| dar_received | approved → received | เจ้าของ + role-doc-controller |

## §5.3 สิทธิ์ (DEC-09)
| Action | เจ้าของ | ผู้พิจารณาขั้นปัจจุบัน | ผู้อยู่ในสาย (ไม่ใช่ขั้นปัจจุบัน) | role-doc-controller (admin) | คนอื่น |
|---|:-:|:-:|:-:|:-:|:-:|
| ดูร่าง | ✓ | ✗ | ✗ | ✓ | ✗ |
| ดูหลังส่ง | ✓ | ✓ | ✓ | ✓ | ✗ |
| แก้ไข | ร่าง | ✗ | ✗ | ✗ | ✗ |
| อนุมัติ/ไม่อนุมัติ | ✗ | ✓ | ✗ | เมื่อเป็นขั้นปัจจุบัน | ✗ |
| ยกเลิก | ร่าง/รอ | ✗ | ✗ | ร่าง/รอ | ✗ |
| บันทึกลงนามรับ | ✗ | ✗ | ✗ | อนุมัติแล้ว | ✗ |

## §5.4 Validation
| VR | ช่อง | เงื่อนไข | ข้อความ |
|---|---|---|---|
| VR-01 | purpose | required (1) | เลือกวัตถุประสงค์ 1 ข้อ |
| VR-02 | issue_type | required (1) | เลือก ISSUE 1 ข้อ |
| VR-03 | target_doc_name | required | ระบุชื่อเอกสาร |
| VR-04 | origin_detail | required เมื่อ origin = other | ระบุรายละเอียดที่มาอื่นๆ |
| VR-05 | change_before | required เมื่อ purpose = revise | แก้ไขเอกสาร — ระบุ Revision / ISSUE เดิม |
| VR-06 | change_after | required เมื่อ purpose = revise/new/other | ระบุ Revision / ISSUE ใหม่ (อื่นๆ: อื่นๆ — อธิบายใน Revision / ISSUE ใหม่) |
| VR-07 | dar_related_document | ครบคู่ต่อแถว | ระบุชื่อเอกสาร / ระบุ Document No. |
| VR-08 | distribution_units | ≥1 | เลือกหน่วยงานที่ต้องได้รับการแจกจ่ายอย่างน้อย 1 หน่วยงาน |
| VR-09 | receive_methods | ≥1 | เลือกวิธีการรับเอกสารอย่างน้อย 1 วิธี |
| VR-10 | distribution_emails | required + รูปแบบ เมื่อ email | ระบุ E-Mail อย่างน้อย 1 ที่อยู่ / รูปแบบ E-Mail ไม่ถูกต้อง |
| VR-11 | assignees | ครบทุกขั้น · ≠ ผู้จัดทำ | กรุณาเลือกผู้พิจารณา |
| VR-12 | reason (ไม่อนุมัติ/ยกเลิก) | required | กรุณาระบุเหตุผล |
| VR-13 | receiver_id (ลงนามรับ) | required | กรุณาเลือกผู้รับเอกสาร |

## §5.5 Edge Cases
| EC | กรณี | ผล |
|---|---|---|
| EC-01 | effective_date < dar_date (DEC-15) | warning ส่งได้ |
| EC-02 | origin other ไม่ระบุ | VR-04 บล็อก |
| EC-03 | purpose อื่นๆ ไม่มีช่องระบุบนกระดาษ (DEC-13) | VR-06 บังคับอธิบายในกล่องใหม่ |
| EC-04 | ISSUE 4 ตัวเลือก (DEC-14) | radio 4 · PDF ☐ 4 |
| EC-05 | หน่วยงานชุดซ้ำ V–AA (DEC-12) | 27 ช่อง · ชุด 2 ติด (2) · OQ-04 |
| EC-06 | E-Mail หลายที่อยู่ / ผิดรูปแบบ (DEC-16) | ทุกที่อยู่ต้องถูก · VR-10 |
| EC-07 | ยกเลิกติ๊ก E-mail | ล้าง distribution_emails · PDF ว่าง |
| EC-08 | เอกสารเกี่ยวข้อง > 14 / แก้ไขหลายบรรทัด | PDF 2 หน้า · ตารางต่อหน้า 2 หัวซ้ำ · > 18 = dense |
| EC-09 | แถวเอกสารเกี่ยวข้องครึ่งแถว | VR-07 บล็อก |
| EC-10 | DOA 6 ขั้น | ลายเซ็น 7 ช่อง 4+3 · 2 หน้า |
| EC-11 | ผู้จัดทำอยู่ในสายเอง | slot ต้องเลือกคนอื่น (SELF_APPROVE) |
| EC-12 | แก้ DOA ระหว่างรอ | ใช้ snapshot |
| EC-13 | stale | 409 STALE |
| EC-14 | doc_type ปิด | 409 DOC_TYPE_INACTIVE · ปุ่มสร้าง disabled |
| EC-15 | เปิดใบที่ไม่มีสิทธิ์ | 404 / ไม่เปิด drawer |
| EC-16 | ไม่อนุมัติที่ขั้น 3 | กลับร่างทั้งใบ · ส่งใหม่เริ่มขั้น 1 |
| EC-17 | ยกเลิก/ขึ้นทะเบียนใหม่ ไม่มี Document No. | ไม่บังคับ · PDF ว่าง |

## §5.6 Errors
DOC_TYPE_INACTIVE · NOT_OWNER · NOT_DRAFT · STALE · ASSIGNEE_REQUIRED · SELF_APPROVE · NOT_CURRENT_APPROVER · REASON_REQUIRED · NOT_ADMIN · NOT_APPROVED · RECEIVER_REQUIRED · NOT_FOUND
