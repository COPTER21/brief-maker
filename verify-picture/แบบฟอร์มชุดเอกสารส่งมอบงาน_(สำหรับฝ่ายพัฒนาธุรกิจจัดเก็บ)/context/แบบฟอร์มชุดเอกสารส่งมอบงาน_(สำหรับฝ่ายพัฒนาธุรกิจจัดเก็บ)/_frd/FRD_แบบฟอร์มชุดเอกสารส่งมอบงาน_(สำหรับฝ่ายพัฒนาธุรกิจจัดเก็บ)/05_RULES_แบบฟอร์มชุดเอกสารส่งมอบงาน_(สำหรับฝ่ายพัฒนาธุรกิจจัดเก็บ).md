# 05_RULES — F-TMP-007

## §5.1 Business Rules
| ID | Rule | Tag | ที่มา |
|---|---|---|---|
| BR-01 | สถานะข้อมูล / สถานะเอกสาร อ่านจาก HandoverPackageConfig เท่านั้น | CONFIGURABLE | DEC-04 · DEC-12 (VALID) |
| BR-02 | ไม่มีช่องคำนวณ · ไม่ใช้ตัวเลือกค้าง 1–5 (C13:C18) | FIXED | DEC-12 (VALID) |
| BR-03 | สถานะข้อมูล = สมบูรณ์ ขณะมีเอกสาร ขาดเอกสาร/มีข้อจำกัด = เตือน ไม่บล็อก | CONFIGURABLE [AI-DEFAULT] | DEC-04 · DEC-13 (VALID) |
| BR-04 | สถานะข้อมูลหรือรายการใด = มีข้อจำกัด → ข้อจำกัดของข้อมูลบังคับ | FIXED | DEC-14 (VALID) |
| BR-05 | วันที่เอกสาร > วันที่ส่งมอบ = เตือน | CONFIGURABLE [AI-DEFAULT] | DEC-16 (VALID) |
| BR-06 | ขั้นรับทราบ (role-mgr-bu) ค่าเริ่มผู้พิจารณา = ผู้รับมอบที่เลือก · บล็อกลงชื่อมาจาก DOA เท่านั้น | FIXED | DEC-15 (VALID) |
| BR-07 | ช่องตรงกระดาษ 1:1 · ไม่เพิ่มช่อง | FIXED [AI-DEFAULT] | DEC-06 |
| BR-08 | แถวรายการเอกสารไม่จำกัด · PDF แสดงอย่างน้อยตาม print_config.min_rows | FIXED [AI-DEFAULT] | DEC-05 |
| BR-DOA-01 | ส่งอนุมัติได้เฉพาะ draft | FIXED | DOA |
| BR-DOA-02 | resolve สายตอนส่งแล้ว freeze | FIXED | DOA |
| BR-DOA-03 | reject → กลับ draft แก้ได้ · ประวัติ append-only (ตรงกับ DEC-08 — ไม่มีข้อยกเว้น) | FIXED | DEC-08 |
| BR-DOA-04 | ผู้จัดทำพิจารณาใบตัวเองไม่ได้ | FIXED | DOA |
| BR-DOA-05 | ไม่ใช้ (ไม่มีวงเงิน DEC-03) | — | |
| BR-09 | เลขออกตอนบันทึกครั้งแรก · กลับร่างใช้เลขเดิม | FIXED | DEC-10 |
| BR-10 | approved ล็อกแก้ไขและยกเลิกไม่ได้ | FIXED | DEC-08 |
| BR-11 | ตารางลงชื่อใน PDF = ผู้จัดทำ + 1 แถวต่อขั้นที่ตั้งใน DOA (dynamic · ห้าม fix จำนวน) · คำตัดสินตาม role (print_config) · บล็อกลงชื่อไม่ถูกตัดข้ามหน้า | FIXED (จำนวน = DOA) | DEC-03 · DEC-07 |
| BR-12 | แบบพิมพ์ 2 หน้าทุกสถานะ (thai-doc R10) · หัวตารางซ้ำ · "หน้า N/2" | FIXED | DEC-05 |
| BR-13 | มองเห็น: เจ้าของ · ผู้อนุมัติหลังส่ง · admin_role ฝ่ายพัฒนาธุรกิจเห็นทั้งหมด | FIXED [AI-DEFAULT] | DEC-09 |
| BR-14 | ไม่เปลี่ยนค่าในระบบ ไม่ส่งต่อระบบอื่น · แนบไฟล์ ✓ CSV ✓ ทำซ้ำ ✗ ประกาศ ✗ | FIXED [AI-DEFAULT] | DEC-01 · DEC-02 · DEC-11 |
| BR-15 | รับมอบครบแล้วยังมีเอกสารขาด/มีข้อจำกัด → แจ้งผู้จัดทำ (hob_received_with_gaps) | FIXED | DEC-13 |

## §5.2 State Machine
| จาก | event | ไป | guard |
|---|---|---|---|
| — | save | draft | FN-03 ออกเลข |
| draft | submit | pending(1) | owner · assignees ครบ |
| pending(n) | approve | pending(n+1) / approved | assignee ขั้น n |
| pending(n) | reject | draft | assignee ขั้น n · เหตุผล |
| draft/pending | cancel | cancelled | owner/admin_role · เหตุผล |

## §5.3 Permission Matrix
| Action | owner | ผู้พิจารณาขั้นปัจจุบัน | อยู่ในสาย (ไม่ใช่ขั้นปัจจุบัน) | admin_role | อื่น |
|---|:-:|:-:|:-:|:-:|:-:|
| ดู draft | ✓ | ✗ | ✗ | ✓ | ✗ |
| ดู pending/approved/cancelled | ✓ | ✓ | ✓ | ✓ | ✗ |
| แก้ draft | ✓ | ✗ | ✗ | ✗ | ✗ |
| ตัดสิน | ✗ | ✓ | ✗ | ✗ | ✗ |
| ยกเลิก | ✓ | ✗ | ✗ | ✓ | ✗ |

## §5.4 Validation
| VR | ช่อง | กฎ | ข้อความ |
|---|---|---|---|
| VR-01 | handover.project_name | required | กรุณาระบุชื่อโครงการ |
| VR-02 | handover.sender_id · receiver_id | required | กรุณาเลือกผู้ส่งมอบ / กรุณาเลือกผู้รับมอบ |
| VR-03 | handover.handover_date · package_version · data_status | required · data_status ∈ data_statuses | กรุณาระบุวันที่ส่งมอบ / กรุณาระบุฉบับชุดเอกสาร / กรุณาเลือกสถานะข้อมูล |
| VR-04 | items[] doc_name · status | ≥1 แถว · required ทุกแถว · status ∈ doc_statuses | กรอกชื่อเอกสารและสถานะให้ครบทุกรายการ (หรือลบแถวที่ไม่ใช้) |
| VR-05 | notes.data_limits | required เมื่อ data_status = limited_data หรือมีแถว status = limited_doc (DEC-14) | มีรายการ "มีข้อจำกัด" — กรุณาระบุข้อจำกัดของข้อมูล |
| VR-06 | assignees | ครบทุกขั้น · ≠ ผู้จัดทำ | กรุณาเลือกผู้พิจารณา |
| VR-07 | reason (reject/cancel) | required | กรุณาระบุเหตุผล |

## §5.5 Edge Cases
| EC | กรณี | ผล | อ้าง |
|---|---|---|---|
| EC-01 | เปลี่ยนสถานะข้อมูลเป็น มีข้อจำกัด หลังกรอกขั้น 2 | ข้อจำกัดของข้อมูลบังคับ · ตรวจซ้ำตอนบันทึก (validAll) | DEC-14 |
| EC-02 | สมบูรณ์แต่มีเอกสารขาด | เตือนฟอร์ม/รายละเอียด · บันทึกได้ · รับมอบแล้ว → hob_received_with_gaps | DEC-13 |
| EC-03 | > rows_page1 แถวรายการ (ทดสอบ 24 แถว) | PDF หน้า 2 ต่อตาราง หัวซ้ำ · ยัง 2 หน้า | DEC-05 |
| EC-04 | ผู้จัดทำเป็นผู้จัดการเอง | slot ขั้น 1 ว่าง ต้องเลือกคนอื่น | BR-DOA-04 |
| EC-05 | DOA แก้ระหว่างรอ | ใช้ snapshot | BR-DOA-02 |
| EC-06 | ตัดสินชนกัน | 409 STALE สถานะไม่เปลี่ยน | |
| EC-07 | doc_type ปิดใช้ | สร้างไม่ได้ 409 DOC_TYPE_INACTIVE | DEC-10 |
| EC-08 | เปลี่ยนผู้รับมอบในร่าง | ค่าเริ่ม slot ขั้นรับทราบเปลี่ยนตาม | DEC-15 |
| EC-09 | DOA 6 ขั้น | PDF ลงชื่อ 7 แถว dense · ยัง 2 หน้า | BR-11 |
| EC-10 | ตัวเลือกค้าง 1–5 ในไฟล์เดิม | ไม่มีในระบบ | DEC-12 |
| EC-11 | วันที่เอกสารหลังวันที่ส่งมอบ | เตือนในตาราง + ไอคอนในรายละเอียด · บันทึกได้ | DEC-16 |

## §5.6 Error Catalog
NOT_FOUND 404 · NOT_OWNER 403 · NOT_CURRENT_APPROVER 403 · NOT_DRAFT 409 · NOT_CANCELLABLE 409 · STALE 409 · DOC_TYPE_INACTIVE 409 · ASSIGNEE_REQUIRED 422 · SELF_APPROVAL 422 · REASON_REQUIRED 422 · VALIDATION 422

## §5.7 Security
SoD · คำเตือน/จำนวนเอกสารขาดคิดฝั่ง server · audit append-only · PII ชื่อ snapshot

## §5.8 Notifications (NTF_BRIEF)
hob_cancelled · hob_received_with_gaps — ดู 03 FN-09
