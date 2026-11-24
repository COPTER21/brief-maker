# 05_RULES — F-TMP-004

## §5.1 Business Rules
| ID | Rule | Tag | ที่มา |
|---|---|---|---|
| BR-01 | เหตุผลหลักแสดงครบทุกแถวตามลำดับ ProjectClosure.reason_types (config) · ไม่เพิ่ม/ลบแถว | CONFIGURABLE | DEC-04 · DEC-05 |
| BR-02 | ต้องมีเหตุผลที่เลือก "ใช่" อย่างน้อย 1 ข้อ | FIXED | DEC-12 (VALID) |
| BR-03 | แถว "ใช่" ต้องกรอกรายละเอียดประกอบ · แถวเหตุผลอื่น = ใช่ ต้องระบุว่าเหตุผลอื่นคืออะไร | FIXED | DEC-13 · DEC-14 (VALID) |
| BR-04 | แถว "ไม่ใช่" ล้างและปิดช่องข้อความในแถว (server ล้างซ้ำ) | FIXED | DEC-14 (VALID) |
| BR-05 | สถานะการปิดโครงการ "ติดตามเงื่อนไขในอนาคต" ต้องกรอกข้อเสนอให้ติดตามในอนาคต | FIXED | DEC-15 (VALID) |
| BR-06 | สถานะการปิดโครงการอ่านจาก ProjectClosure.closure_statuses (config) เท่านั้น | CONFIGURABLE | DEC-04 |
| BR-07 | ช่องตรงกระดาษ 1:1 · ไม่เพิ่มช่องเลขที่โครงการ (เสนอเป็นคำถามลูกค้าใน 00 §0.8) | FIXED [AI-DEFAULT] | DEC-06 · DEC-16 (VALID) |
| BR-08 | ค่าเริ่มช่องเลือก = "ไม่ใช่" · ผู้รับผิดชอบค่าเริ่ม = ผู้จัดทำ · วันที่มีมติค่าเริ่ม = วันนี้ (≤ วันนี้) | CONFIGURABLE [AI-DEFAULT] | DEC-05 · Rule #107 |
| BR-DOA-01 | ส่งอนุมัติได้เฉพาะ draft | FIXED | DOA |
| BR-DOA-02 | resolve สายตอนส่งแล้ว freeze | FIXED | DOA |
| BR-DOA-03 | reject → กลับ draft แก้ได้ · ประวัติ append-only (ตรงกับ DEC-08 — ไม่มีข้อยกเว้น) | FIXED | DEC-08 |
| BR-DOA-04 | ผู้จัดทำพิจารณาใบตัวเองไม่ได้ | FIXED | DOA |
| BR-DOA-05 | ไม่ใช้ (ไม่มีวงเงิน DEC-03) | — | |
| BR-09 | เลขออกตอนบันทึกครั้งแรก · กลับร่างใช้เลขเดิม | FIXED [AI-DEFAULT] | DEC-10 |
| BR-10 | approved ล็อกแก้ไขและยกเลิกไม่ได้ | FIXED | DEC-08 |
| BR-11 | ตารางลงชื่อใน PDF = ผู้จัดทำ + 1 แถวต่อขั้นที่ตั้งใน DOA (dynamic · ห้าม fix จำนวน) · คำตัดสินตาม role (print_config) · บล็อกลงชื่อไม่ถูกตัดข้ามหน้า | FIXED (จำนวน = DOA) | DEC-03 · DEC-07 |
| BR-12 | แบบพิมพ์ 2 หน้าทุกสถานะ (thai-doc R10) · ตัดหน้าก่อนสรุปและปิดโครงการ/บล็อกลงชื่อ · "หน้า N/2" | FIXED | DEC-05 |
| BR-13 | มองเห็น: เจ้าของ · ผู้อนุมัติหลังส่ง · admin_role ฝ่ายพัฒนาธุรกิจเห็นทั้งหมด | FIXED [AI-DEFAULT] | DEC-09 |
| BR-14 | ไม่เปลี่ยนค่าในระบบ ไม่ส่งต่อระบบอื่น (ไม่ปิดโครงการต้นทาง) · แนบไฟล์ ✓ CSV ✓ ทำซ้ำ ✗ ประกาศ ✗ | FIXED [AI-DEFAULT] | DEC-01 · DEC-02 · DEC-11 |

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
| VR-01 | project_name · owner · decision_date · stopped_stage | required | กรุณากรอกชื่อโครงการ / กรุณาเลือกผู้รับผิดชอบ / กรุณาเลือกวันที่มีมติ / กรุณากรอกขั้นตอนที่ยุติ |
| VR-02 | reasons[].selected | ≥1 ใช่ | เลือก "ใช่" อย่างน้อย 1 เหตุผล |
| VR-03 | reasons[].detail (แถว ใช่) | required | แถวที่เลือก "ใช่" ต้องกรอกรายละเอียดประกอบ (เหตุผลอื่น: ต้องระบุว่าเหตุผลอื่นคืออะไร) |
| VR-04 | summary · closure_status | required · closure_status ∈ config | กรุณากรอกสรุปเหตุผล / กรุณาเลือกสถานะการปิดโครงการ |
| VR-05 | future_followup | required เมื่อสถานะ follow | ต้องระบุเมื่อสถานะเป็น "ติดตามเงื่อนไขในอนาคต" |
| VR-06 | decision_date | ≤ วันนี้ | วันที่ในอนาคตเลือกไม่ได้ |
| VR-07 | assignees | ครบทุกขั้น · ≠ ผู้จัดทำ | กรุณาเลือกผู้พิจารณา |
| VR-08 | reason (reject/cancel) | required | กรุณาระบุเหตุผล |

## §5.5 Edge Cases
| EC | กรณี | ผล | อ้าง |
|---|---|---|---|
| EC-01 | ส่งโดยไม่เลือกเหตุผลใด | บล็อก + ไฮไลต์ช่องเลือกทุกแถว | DEC-12 |
| EC-02 | เหตุผลอื่น = ใช่ ไม่มีรายละเอียด | บล็อกที่แถว + ข้อความเฉพาะ | DEC-13 |
| EC-03 | เปลี่ยน ใช่ → ไม่ใช่ หลังกรอก | ข้อความในแถวถูกล้าง · PDF แถวว่าง | DEC-14 |
| EC-04 | ข้อความยาวทุกแถว + สรุปยาว (ทดสอบ long-8reasons) | PDF ยัง 2 หน้า | DEC-05 |
| EC-05 | ผู้จัดทำเป็นผู้จัดการเอง | slot ขั้น 1 ว่าง ต้องเลือกคนอื่น | BR-DOA-04 |
| EC-06 | DOA แก้ระหว่างรอ | ใช้ snapshot | BR-DOA-02 |
| EC-07 | ตัดสินชนกัน | 409 STALE สถานะไม่เปลี่ยน | |
| EC-08 | doc_type ปิดใช้ | สร้างไม่ได้ 409 DOC_TYPE_INACTIVE | DEC-10 |
| EC-09 | ติดตามเงื่อนไขในอนาคต ไม่มีข้อเสนอ | บล็อก | DEC-15 |
| EC-10 | ไม่มีเลขโครงการบนกระดาษ | ไม่ตรวจซ้ำ/ไม่ผูกรอบนี้ → คำถามลูกค้า (00 §0.8) | DEC-16 |

## §5.6 Error Catalog
NOT_FOUND 404 · NOT_OWNER 403 · NOT_CURRENT_APPROVER 403 · NOT_DRAFT 409 · NOT_CANCELLABLE 409 · STALE 409 · DOC_TYPE_INACTIVE 409 · ASSIGNEE_REQUIRED 422 · SELF_APPROVAL 422 · REASON_REQUIRED 422 · VALIDATION 422

## §5.7 Security
SoD · ตรวจ/ล้างข้อมูลแถวฝั่ง server · audit append-only · PII ชื่อ snapshot

## §5.8 Notifications (NTF_BRIEF)
pcl_cancelled · pcl_followup_approved — ดู 03 FN-09
