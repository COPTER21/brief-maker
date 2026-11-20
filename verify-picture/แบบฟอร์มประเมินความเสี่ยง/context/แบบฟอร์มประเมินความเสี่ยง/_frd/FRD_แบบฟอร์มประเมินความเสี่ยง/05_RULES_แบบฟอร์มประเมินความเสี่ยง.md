# 05_RULES — F-TMP-002

## §5.1 Business Rules
| ID | Rule | Tag | ที่มา |
|---|---|---|---|
| BR-01 | คะแนนก่อนควบคุม = โอกาสเกิด × ผลกระทบ · ว่างจนกรอกครบทั้งสองช่อง (ไม่แสดง 0) | FIXED | DEC-04 · DEC-14 (VALID) |
| BR-02 | ระดับความเสี่ยงจาก RiskMatrix.level_bands (config) · ใช้แสดงสี/ป้าย ไม่เพิ่มคอลัมน์บนแบบพิมพ์ | CONFIGURABLE | DEC-04 · DEC-16 (VALID) |
| BR-03 | คะแนนคงเหลือเลือกได้เฉพาะชุดผลคูณจาก RiskMatrix config (ตัดค่า 7 ที่ต้นฉบับใส่ผิด) | FIXED | DEC-12 (VALID) |
| BR-04 | คะแนนคงเหลือ > คะแนนก่อนควบคุม = เตือน ไม่บล็อก | CONFIGURABLE [AI-DEFAULT] | DEC-04 · DEC-13 (VALID) |
| BR-05 | สถานะรายการ "ปิดแล้ว" ต้องมีคะแนนคงเหลือ | CONFIGURABLE [AI-DEFAULT] | DEC-04 |
| BR-06 | เกณฑ์ 1–5 · ช่วงระดับ · ประเภทความเสี่ยง อ่านจาก RiskMatrix config เท่านั้น | CONFIGURABLE | DEC-04 |
| BR-07 | ช่องตรงกระดาษ 1:1 · ไม่เพิ่มช่องโครงการ (เสนอเป็นคำถามลูกค้าใน 00 §0.8) | FIXED [AI-DEFAULT] | DEC-06 · VALID ช่องโครงการ (07 §7.0) |
| BR-08 | แถวทะเบียนไม่จำกัด · PDF แสดงอย่างน้อยตาม print_config.min_rows | FIXED [AI-DEFAULT] | DEC-05 |
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
| VR-01 | items[] category · description · likelihood · impact · status | ≥1 แถว · required ทุกแถว | กรอกประเภท รายละเอียด โอกาสเกิด ผลกระทบ และสถานะให้ครบทุกรายการ |
| VR-02 | residual_score | อยู่ในชุดผลคูณ (RiskMatrix config) · บังคับเมื่อปิดแล้ว | สถานะ "ปิดแล้ว" ต้องระบุคะแนนคงเหลือ |
| VR-03 | assignees | ครบทุกขั้น · ≠ ผู้จัดทำ | กรุณาเลือกผู้พิจารณา |
| VR-04 | reason (reject/cancel) | required | กรุณาระบุเหตุผล |

## §5.5 Edge Cases
| EC | กรณี | ผล | อ้าง |
|---|---|---|---|
| EC-01 | แถวยังไม่ใส่โอกาส/ผลกระทบ | คะแนนว่าง (ไม่ใช่ 0) | DEC-14 |
| EC-02 | คงเหลือ > ก่อนควบคุม | เตือนแถว + สรุป · บันทึกได้ | DEC-13 |
| EC-03 | > min_rows รายการ (ทดสอบ 24 แถว) | PDF หน้า 2 ต่อตาราง หัวซ้ำ · ยัง 2 หน้า | DEC-05 |
| EC-04 | ผู้จัดทำเป็นผู้จัดการเอง | slot ขั้น 1 ว่าง ต้องเลือกคนอื่น | BR-DOA-04 |
| EC-05 | DOA แก้ระหว่างรอ | ใช้ snapshot | BR-DOA-02 |
| EC-06 | ตัดสินชนกัน | 409 STALE สถานะไม่เปลี่ยน | |
| EC-07 | doc_type ปิดใช้ | สร้างไม่ได้ 409 DOC_TYPE_INACTIVE | DEC-10 |
| EC-08 | ใช้ประเมินหลายโครงการ ไม่มีช่องโครงการ | ไม่ตรวจรอบนี้ → คำถามลูกค้า (00 §0.8) | DEC-06 |
| EC-09 | ค่าคงเหลือที่คูณไม่ได้ (เช่น 7 จากไฟล์เดิม) | ไม่มีในตัวเลือก · API 422 | DEC-12 |
| EC-10 | ไม่มีคอลัมน์ระดับบนกระดาษ | แสดงสีบนจอเท่านั้น | DEC-16 |

## §5.6 Error Catalog
NOT_FOUND 404 · NOT_OWNER 403 · NOT_CURRENT_APPROVER 403 · NOT_DRAFT 409 · NOT_CANCELLABLE 409 · STALE 409 · DOC_TYPE_INACTIVE 409 · ASSIGNEE_REQUIRED 422 · SELF_APPROVAL 422 · REASON_REQUIRED 422 · VALIDATION 422

## §5.7 Security
SoD · คำนวณคะแนนฝั่ง server · audit append-only · PII ชื่อ snapshot

## §5.8 Notifications (NTF_BRIEF)
rsk_cancelled · rsk_very_high_approved — ดู 03 FN-09
