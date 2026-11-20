# 05_RULES — F-TMP-006

## §5.1 Business Rules
| ID | Rule | Tag | ที่มา |
|---|---|---|---|
| BR-01 | สถานะข้อแก้ไข / สถานะการอนุมัติ อ่านจาก ReviewApprovalConfig เท่านั้น | CONFIGURABLE | DEC-04 · DEC-13 (VALID) |
| BR-02 | ไม่มีช่องคำนวณ · ไม่ใช้ตัวเลือก/สูตรค้างจาก FM-BDM-02 | FIXED | DEC-13 · DEC-14 (VALID) |
| BR-03 | อนุมัติครบถ้วน ขณะข้อแก้ไข เปิด/กำลังดำเนินการ = เตือน ไม่บล็อก | CONFIGURABLE [AI-DEFAULT] | DEC-04 · DEC-15 (VALID) |
| BR-04 | วันที่มีผลบังคับเมื่อ อนุมัติครบถ้วน/อนุมัติแบบมีเงื่อนไข (final_needs_effective) · สถานะอื่นต้องว่าง | FIXED | DEC-18 (VALID) |
| BR-05 | สถานะข้อแก้ไข "ปิด" ไม่มีผู้รับผิดชอบหรือข้อคิดเห็น = เตือน | CONFIGURABLE [AI-DEFAULT] | DEC-04 |
| BR-06 | ผลพิจารณา DOA ทุกขั้นเติมแถวบันทึกการอนุมัติภายใน source=doa · แก้/ลบไม่ได้ · บล็อกลงชื่อมาจาก DOA เท่านั้น | FIXED | DEC-16 (VALID) |
| BR-07 | ช่องตรงกระดาษ 1:1 · ไม่เพิ่มช่องโครงการ (เสนอเป็นคำถามลูกค้าใน 00 §0.8) | FIXED [AI-DEFAULT] | DEC-07 · DEC-17 (VALID) |
| BR-08 | แถวตรวจทาน/อนุมัติภายในไม่จำกัด · PDF แสดงอย่างน้อยตาม print_config.min_rows / min_rows_approvals | FIXED [AI-DEFAULT] | DEC-05 · DEC-06 |
| BR-DOA-01 | ส่งอนุมัติได้เฉพาะ draft | FIXED | DOA |
| BR-DOA-02 | resolve สายตอนส่งแล้ว freeze | FIXED | DOA |
| BR-DOA-03 | reject → กลับ draft แก้ได้ · ประวัติ append-only (ตรงกับ DEC-09 — ไม่มีข้อยกเว้น) | FIXED | DEC-09 |
| BR-DOA-04 | ผู้จัดทำพิจารณาใบตัวเองไม่ได้ | FIXED | DOA |
| BR-DOA-05 | ไม่ใช้ (ไม่มีวงเงิน DEC-03) | — | |
| BR-09 | เลขออกตอนบันทึกครั้งแรก · กลับร่างใช้เลขเดิม | FIXED | DEC-11 |
| BR-10 | approved ล็อกแก้ไขและยกเลิกไม่ได้ | FIXED | DEC-09 |
| BR-11 | ตารางลงชื่อใน PDF = ผู้จัดทำ + 1 แถวต่อขั้นที่ตั้งใน DOA (dynamic · ห้าม fix จำนวน) · คำตัดสินตาม role (print_config) · บล็อกลงชื่อไม่ถูกตัดข้ามหน้า | FIXED (จำนวน = DOA) | DEC-03 · DEC-08 |
| BR-12 | แบบพิมพ์ 2 หน้าทุกสถานะ (thai-doc R10) · หัวตารางซ้ำ · "หน้า N/2" | FIXED | DEC-05 · DEC-06 |
| BR-13 | มองเห็น: เจ้าของ · ผู้อนุมัติหลังส่ง · admin_role ฝ่ายพัฒนาธุรกิจเห็นทั้งหมด | FIXED [AI-DEFAULT] | DEC-10 |
| BR-14 | ไม่เปลี่ยนค่าในระบบ ไม่ส่งต่อระบบอื่น · แนบไฟล์ ✓ CSV ✓ ทำซ้ำ ✗ ประกาศ ✗ | FIXED [AI-DEFAULT] | DEC-01 · DEC-02 · DEC-12 |
| BR-15 | วันที่ตรวจทาน/วันที่พิจารณา ไม่เกินวันนี้ | FIXED | FORM_SPEC |

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
| VR-01 | reviews[] item · reviewer · review_date · result · status | ≥1 แถว · required ทุกแถว · วันที่ ≤ วันนี้ | กรอกรายการเอกสาร ผู้ตรวจทาน วันที่ ผลการตรวจทาน และสถานะให้ครบทุกรายการ |
| VR-02 | approvals[] (manual) approver_name · position · decision · decided_date | required ทุกแถวที่เพิ่ม | กรอกผู้พิจารณา ตำแหน่ง ผลการพิจารณา และวันที่ให้ครบทุกแถว (หรือลบแถวที่ไม่ใช้) |
| VR-03 | final.approval_status | required · ∈ final_statuses | กรุณาเลือกสถานะการอนุมัติ |
| VR-04 | final.effective_date | required เมื่อ ∈ final_needs_effective · ว่างเมื่อไม่ใช่ | กรุณาระบุวันที่มีผล |
| VR-05 | assignees | ครบทุกขั้น · ≠ ผู้จัดทำ | กรุณาเลือกผู้พิจารณา |
| VR-06 | reason (reject/cancel) | required | กรุณาระบุเหตุผล |

## §5.5 Edge Cases
| EC | กรณี | ผล | อ้าง |
|---|---|---|---|
| EC-01 | เปลี่ยนสถานะการอนุมัติเป็นสถานะที่ไม่ต้องมีวันที่มีผล | ล้างวันที่มีผล + disabled | DEC-18 |
| EC-02 | อนุมัติครบถ้วนแต่ข้อแก้ไขค้าง | เตือนฟอร์ม/รายละเอียด · บันทึกได้ · อนุมัติแล้ว → irv_approved_open_items | DEC-15 |
| EC-03 | > rows_page1 แถวตรวจทาน (ทดสอบ 24 แถว) | PDF หน้า 2 ต่อตาราง หัวซ้ำ · ยัง 2 หน้า | DEC-05 |
| EC-04 | ผู้จัดทำเป็นผู้จัดการเอง | slot ขั้น 1 ว่าง ต้องเลือกคนอื่น | BR-DOA-04 |
| EC-05 | DOA แก้ระหว่างรอ | ใช้ snapshot | BR-DOA-02 |
| EC-06 | ตัดสินชนกัน | 409 STALE สถานะไม่เปลี่ยน | |
| EC-07 | doc_type ปิดใช้ | สร้างไม่ได้ 409 DOC_TYPE_INACTIVE | DEC-11 |
| EC-08 | ถูกตีกลับแล้วส่งใหม่ | แถว source=doa รอบก่อนคงอยู่ · รอบใหม่ต่อท้าย | DEC-16 |
| EC-09 | DOA 6 ขั้น | PDF ลงชื่อ 7 แถว dense · ยัง 2 หน้า | BR-11 |
| EC-10 | ตัวเลือก/สูตรค้างจาก FM-BDM-02 ในไฟล์เดิม | ไม่มีในระบบ | DEC-13 · DEC-14 |
| EC-11 | ใช้กับหลายโครงการ ไม่มีช่องโครงการ | ไม่ตรวจรอบนี้ → คำถามลูกค้า (00 §0.8) | DEC-17 |

## §5.6 Error Catalog
NOT_FOUND 404 · NOT_OWNER 403 · NOT_CURRENT_APPROVER 403 · NOT_DRAFT 409 · NOT_CANCELLABLE 409 · STALE 409 · DOC_TYPE_INACTIVE 409 · ASSIGNEE_REQUIRED 422 · SELF_APPROVAL 422 · REASON_REQUIRED 422 · VALIDATION 422

## §5.7 Security
SoD · คำเตือน/จำนวนข้อแก้ไขค้างคิดฝั่ง server · audit append-only · PII ชื่อ snapshot

## §5.8 Notifications (NTF_BRIEF)
irv_cancelled · irv_approved_open_items — ดู 03 FN-09
