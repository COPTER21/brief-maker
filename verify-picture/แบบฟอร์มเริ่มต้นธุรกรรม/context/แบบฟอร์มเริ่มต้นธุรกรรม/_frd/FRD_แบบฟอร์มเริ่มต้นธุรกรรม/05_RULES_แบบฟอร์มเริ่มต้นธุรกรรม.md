# 05_RULES — F-TMP-001

## §5.1 Business Rules
| ID | Rule | Tag | ที่มา |
|---|---|---|---|
| BR-01 | ช่องตรงกระดาษ 1:1 ไม่เพิ่มช่อง · แถวป้ายว่างในหมวดขอบเขตงานไม่ทำเป็นช่อง (แบบพิมพ์คงแถวว่าง) | FIXED [AI-DEFAULT] | DEC-06 · DEC-13 (VALID) |
| BR-02 | ผู้รับผิดชอบเลือกจากพนักงานในระบบ (F-EMP-001) · snapshot ชื่อ | FIXED | FORM_SPEC F06 |
| BR-03 | ผู้อนุมัติไม่ hardcode — สาย resolve จาก DOA ตอนส่ง แล้ว freeze | FIXED | DEC-03 · DEC-14 (VALID) · BR-DOA-02 |
| BR-04 | ส่งกลับแก้ไข/ไม่อนุมัติ → draft เลขเดิม · resolve ใหม่ตอนส่งรอบถัดไป | FIXED [AI-DEFAULT] | DEC-08 |
| BR-05 | ประวัติการแก้ไข: ฉบับ 00 = จัดทำครั้งแรก · ส่งใหม่หลังถูกส่งกลับ = ฉบับถัดไป · ผู้อนุมัติ = ผู้อนุมัติขั้นสุดท้าย · ไม่จำกัดแถว · PDF ≥ 2 แถว | FIXED [AI-DEFAULT] | DEC-05 |
| BR-06 | Doc No. บนแบบพิมพ์ = FM-IVM-01 (ไม่ใช่ INV-FM-01) · Rev จาก print_config | CONFIGURABLE | DEC-12 (VALID) |
| BR-07 | ลายเซ็น 1 แถวต่อขั้น DOA · ข้อความ "ส่งในระบบ / พิจารณาในระบบ วันที่ เวลา" ไม่ใช้ภาพ | FIXED [AI-DEFAULT] | DEC-07 |
| BR-08 | แนบไฟล์ระดับใบ · ส่งออก CSV · ไม่มีทำซ้ำเป็นชุด/ประกาศ | FIXED [AI-DEFAULT] | DEC-11 |
| BR-09 | อนุมัติแล้วไม่เปลี่ยนค่าในระบบ · ไม่ส่งต่อระบบอื่น (ประกาศ ivma.approved ไม่ยิง) | FIXED [AI-DEFAULT] | DEC-01 · DEC-02 |
| BR-10 | ไม่มีสูตร/ค่าคงที่บนกระดาษ — ค่าเสนอมาตรฐาน G3 ไม่มีจุดใช้ในเอกสารนี้ | — | DEC-04 |
| BR-DOA-01 | ส่งอนุมัติได้เฉพาะ draft | FIXED | DOA |
| BR-DOA-02 | resolve สายตอนส่งแล้ว freeze | FIXED | DOA |
| BR-DOA-03 | reject → กลับ draft แก้ได้ · ประวัติ append-only (ตรงกับ DEC-08 — ไม่มีข้อยกเว้น) | FIXED | DEC-08 |
| BR-DOA-04 | ผู้จัดทำพิจารณาใบตัวเองไม่ได้ | FIXED | DOA |
| BR-DOA-05 | ไม่ใช้ (ไม่มีวงเงิน DEC-03) | — | |
| BR-11 | เลขออกตอนบันทึกครั้งแรก · กลับร่างใช้เลขเดิม | FIXED | DEC-10 |
| BR-12 | approved ล็อกแก้ไขและยกเลิกไม่ได้ | FIXED | DEC-08 |
| BR-13 | ร่างเห็นเฉพาะเจ้าของ + admin role ฝ่ายบริหารการลงทุน · ผู้อนุมัติเห็นหลังส่ง | FIXED [AI-DEFAULT] | DEC-09 |
| BR-14 | ช่องลงชื่อใน PDF = ผู้จัดทำ + 1 แถวต่อขั้นที่ตั้งใน DOA (dynamic ห้าม fix) · คำตัดสินตาม role (print_config.decision_words.by_role: role-line-manager = ตรวจสอบแล้ว/ส่งกลับแก้ไข · role-gm = อนุมัติ/ไม่อนุมัติ) | FIXED (จำนวน = DOA) | DEC-03 · DEC-07 |

## §5.2 State Machine
| จาก | event | ไป | guard |
|---|---|---|---|
| — | save | draft | FN-03 ออกเลข |
| draft | submit | pending(1) | owner · assignees ครบ · ≠ owner |
| pending(n) | approve | pending(n+1) / approved | assignee ขั้น n |
| pending(n) | reject | draft | assignee ขั้น n · เหตุผล |
| draft/pending | cancel | cancelled | owner/admin · เหตุผล |

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
| VR-01 | txn.name · txn.owner · txn.source · txn.type | required | กรุณากรอก{ป้าย} |
| VR-02 | txn.start_date | required · วันที่ถูกต้อง (ปฏิทิน พ.ศ.) | กรุณาเลือกวันที่เริ่มโครงการ |
| VR-03 | txn.responsible_id | required · พนักงาน active | กรุณาเลือกผู้รับผิดชอบ |
| VR-04 | scope.objective · scope.work_scope · scope.deliverables | required | กรุณากรอก{ป้าย} |
| VR-05 | assignees | ครบทุกขั้น · ≠ ผู้จัดทำ | กรุณาเลือกผู้พิจารณา |
| VR-06 | reason (reject/cancel) | required | กรุณาระบุเหตุผล |

## §5.5 Edge Cases
| EC | กรณี | ผล | อ้าง |
|---|---|---|---|
| EC-01 | ผู้จัดทำไม่มีผู้บังคับบัญชาในผัง | slot ขั้น 1 ว่าง ต้องเลือกเอง | FN-04 |
| EC-02 | ผู้จัดทำถือ role-gm เอง | slot ขั้น 2 ไม่ใช่ตัวเอง | BR-DOA-04 |
| EC-03 | DOA 6 ขั้น | PDF 7 แถวลงนาม · dense · 2 หน้า | BR-14 |
| EC-04 | ข้อความยาวในขอบเขตงาน | ตัดหน้าก่อนบล็อกลงชื่อ (R10) | FN-08 |
| EC-05 | ส่งกลับหลายรอบ | ฉบับเพิ่มทีละ 1 | BR-05 · DEC-05 |
| EC-06 | DOA แก้ระหว่างรอ | ใช้ snapshot | BR-DOA-02 |
| EC-07 | อนุมัติชนกัน | 409 STALE สถานะไม่เปลี่ยน | |
| EC-08 | doc_type ปิดใช้ | สร้างไม่ได้ 409 DOC_TYPE_INACTIVE | DEC-10 |
| EC-09 | ต้นฉบับชื่อชีต INV-FM-01 ขัด footer | แบบพิมพ์ใช้ FM-IVM-01 | DEC-12 |

## §5.6 Error Catalog
NOT_FOUND 404 · NOT_OWNER 403 · NOT_CURRENT_APPROVER 403 · NOT_DRAFT 409 · NOT_CANCELLABLE 409 · STALE 409 · DOC_TYPE_INACTIVE 409 · ASSIGNEE_REQUIRED 422 · SELF_APPROVAL 422 · REASON_REQUIRED 422 · VALIDATION 422

## §5.7 Security
SoD · audit append-only · PII: ชื่อ snapshot + บุคคลภายนอก · ไฟล์แนบตาม file_policy

## §5.8 Notifications (NTF_BRIEF)
ivma_cancelled · ivma_responsible_assigned — ดู 03 FN-09
