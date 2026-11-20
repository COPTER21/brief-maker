# 05_RULES — F-TMP-003

## §5.1 Business Rules
| ID | Rule | Tag | ที่มา |
|---|---|---|---|
| BR-01 | คะแนนถ่วงน้ำหนัก = น้ำหนัก × คะแนน ÷ score_max (config) · ว่างจนให้คะแนน | FIXED | DEC-04 |
| BR-02 | คะแนนรวมถ่วงน้ำหนัก = ผลรวม 8 เกณฑ์ · ว่างจนให้คะแนนครบ (ไม่แสดง 0 / ไม่แสดงผลเสนอ) | FIXED | DEC-04 · DEC-13 (VALID) |
| BR-03 | ผลเสนอจากคะแนนตาม ScreeningCriteria.recommend_bands (config) | CONFIGURABLE | DEC-04 |
| BR-04 | เกณฑ์/น้ำหนัก อ่านจาก ScreeningCriteria.items และ snapshot ลงเอกสารตอนสร้าง · ผลรวมน้ำหนักต้องครบ 100 ตรวจที่ config (เอกสารแก้น้ำหนักไม่ได้) | CONFIGURABLE | DEC-04 · DEC-17 (VALID) |
| BR-05 | คะแนนรับเฉพาะจำนวนเต็ม 1..score_max (ไม่มีตัวเลือก ผ่าน/ไม่ผ่าน) | FIXED | DEC-12 (VALID) |
| BR-06 | ผลการพิจารณา = ดำเนินการต่อแบบมีเงื่อนไข → เงื่อนไข / ข้อสั่งการ บังคับ | CONFIGURABLE [AI-DEFAULT] | DEC-04 · DEC-15 (VALID) |
| BR-07 | ผลการพิจารณาไม่ตรงผลเสนอ = เตือน ไม่บล็อก + บังคับเงื่อนไข / ข้อสั่งการ เป็นเหตุผล | CONFIGURABLE [AI-DEFAULT] | DEC-04 · DEC-14 (VALID) |
| BR-08 | ช่องตรงกระดาษ 1:1 · ไม่เพิ่มช่องโครงการ (เสนอเป็นคำถามลูกค้าใน 00 §0.8) | FIXED [AI-DEFAULT] | DEC-06 · DEC-16 (VALID) |
| BR-09 | เกณฑ์ 8 แถวคงที่จาก config (เพิ่ม/ลบในเอกสารไม่ได้) · PDF แสดงครบทุกแถว | FIXED [AI-DEFAULT] | DEC-05 |
| BR-DOA-01 | ส่งอนุมัติได้เฉพาะ draft | FIXED | DOA |
| BR-DOA-02 | resolve สายตอนส่งแล้ว freeze | FIXED | DOA |
| BR-DOA-03 | reject → กลับ draft แก้ได้ · ประวัติ append-only (ตรงกับ DEC-08 — ไม่มีข้อยกเว้น) | FIXED | DEC-08 |
| BR-DOA-04 | ผู้จัดทำพิจารณาใบตัวเองไม่ได้ | FIXED | DOA |
| BR-DOA-05 | ไม่ใช้ (ไม่มีวงเงิน DEC-03) | — | |
| BR-10 | เลขออกตอนบันทึกครั้งแรก · กลับร่างใช้เลขเดิม | FIXED | DEC-10 |
| BR-11 | approved ล็อกแก้ไขและยกเลิกไม่ได้ | FIXED | DEC-08 |
| BR-12 | ตารางลงชื่อใน PDF = ผู้จัดทำ + 1 แถวต่อขั้นที่ตั้งใน DOA (dynamic · ห้าม fix จำนวน) · คำตัดสินตาม role (print_config) · บล็อกลงชื่อไม่ถูกตัดข้ามหน้า | FIXED (จำนวน = DOA) | DEC-03 · DEC-07 |
| BR-13 | แบบพิมพ์ 2 หน้าทุกสถานะ (thai-doc R10) · "หน้า N/2" · หน้า 2 มีหัวย่อ (ชื่อเอกสาร (ต่อ) + เลขที่) | FIXED | DEC-05 |
| BR-14 | มองเห็น: เจ้าของ · ผู้อนุมัติหลังส่ง · admin_role ฝ่ายพัฒนาธุรกิจเห็นทั้งหมด | FIXED [AI-DEFAULT] | DEC-09 |
| BR-15 | ไม่เปลี่ยนค่าในระบบ ไม่ส่งต่อระบบอื่น (ผลไม่ดำเนินการต่อ = แจ้งเตือนเท่านั้น) · แนบไฟล์ ✓ CSV ✓ ทำซ้ำ ✗ ประกาศ ✗ | FIXED [AI-DEFAULT] | DEC-01 · DEC-02 · DEC-11 |

## §5.2 State Machine
| จาก | event | ไป | guard |
|---|---|---|---|
| — | save | draft | FN-03 ออกเลข |
| draft | submit | pending(1) | owner · assignees ครบ · VR-01..03 ผ่าน |
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
| VR-01 | criteria[].score | ครบทุกเกณฑ์ · จำนวนเต็ม 1..score_max | ให้คะแนน (1-5) ให้ครบทั้ง 8 เกณฑ์ |
| VR-02 | strengths · concerns · decision | required | กรุณากรอกจุดเด่นของโครงการ / กรุณากรอกข้อกังวลหลัก / กรุณาเลือกผลการพิจารณา |
| VR-03 | conditions | required เมื่อ decision = ดำเนินการต่อแบบมีเงื่อนไข หรือ decision_mismatch | กรุณาระบุเงื่อนไข / ข้อสั่งการ |
| VR-04 | assignees | ครบทุกขั้น · ≠ ผู้จัดทำ | กรุณาเลือกผู้พิจารณา |
| VR-05 | reason (reject/cancel) | required | กรุณาระบุเหตุผล |

## §5.5 Edge Cases
| EC | กรณี | ผล | อ้าง |
|---|---|---|---|
| EC-01 | ให้คะแนนยังไม่ครบ | ถ่วงน้ำหนักเกณฑ์ที่ว่าง = ว่าง · คะแนนรวม/ผลเสนอ = ว่าง · ส่งไม่ได้ | DEC-13 |
| EC-02 | ผลการพิจารณาขัดผลเสนอ | เตือนส้ม + บังคับเหตุผล · บันทึกได้ | DEC-14 |
| EC-03 | คะแนนรวมพอดีขอบช่วง (80 / 60) | ≥ เข้าช่วงบน | BR-03 |
| EC-04 | ผู้จัดทำเป็นผู้จัดการฝ่ายเอง | slot ขั้น 1 ว่าง ต้องเลือกคนอื่น | BR-DOA-04 |
| EC-05 | DOA แก้ระหว่างรอ | ใช้ snapshot | BR-DOA-02 |
| EC-06 | ตัดสินชนกัน | 409 STALE สถานะไม่เปลี่ยน | |
| EC-07 | doc_type ปิดใช้ | สร้างไม่ได้ 409 DOC_TYPE_INACTIVE | DEC-10 |
| EC-08 | ScreeningCriteria เปลี่ยนน้ำหนักภายหลัง | ใบเดิมคำนวณจาก snapshot | BR-04 |
| EC-09 | ไม่มีช่องโครงการบนกระดาษ | ไม่ตรวจรอบนี้ → คำถามลูกค้า (00 §0.8 OQ-05) | DEC-16 |
| EC-10 | ค่าคะแนน "ผ่าน/ไม่ผ่าน" จากไฟล์เดิม | ไม่มีในตัวเลือก · API 422 | DEC-12 |
| EC-11 | config น้ำหนักรวมไม่ครบ 100 | config บันทึกไม่ได้ (ตรวจที่ config) | DEC-17 |
| EC-12 | อนุมัติแล้วผล = ไม่ดำเนินการต่อ | scr_not_proceed_approved แจ้งผู้จัดทำ · ไม่สร้าง FM-BDM-04 อัตโนมัติ | DEC-02 |

## §5.6 Error Catalog
NOT_FOUND 404 · NOT_OWNER 403 · NOT_CURRENT_APPROVER 403 · NOT_DRAFT 409 · NOT_CANCELLABLE 409 · STALE 409 · DOC_TYPE_INACTIVE 409 · ASSIGNEE_REQUIRED 422 · SELF_APPROVAL 422 · REASON_REQUIRED 422 · VALIDATION 422

## §5.7 Security
SoD · คำนวณคะแนนฝั่ง server · audit append-only · PII ชื่อ snapshot

## §5.8 Notifications (NTF_BRIEF)
scr_cancelled · scr_not_proceed_approved — ดู 03 FN-09
