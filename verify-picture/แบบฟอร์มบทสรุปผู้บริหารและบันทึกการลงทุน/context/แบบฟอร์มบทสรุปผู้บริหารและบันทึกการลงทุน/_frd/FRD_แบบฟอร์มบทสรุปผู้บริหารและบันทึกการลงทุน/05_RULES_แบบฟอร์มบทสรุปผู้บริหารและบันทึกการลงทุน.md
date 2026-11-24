# 05_RULES — F-TMP-005

## §5.1 Business Rules
| ID | Rule | Tag | ที่มา |
|---|---|---|---|
| BR-01 | หัวข้อบทสรุปผู้บริหาร 13 หัวข้อตามกระดาษ ลำดับตายตัว · หัวข้อบังคับ 7 ข้อ | FIXED | DEC-06 |
| BR-02 | วงเงินหรือมูลค่าโดยประมาณ เป็นตัวเลข ≥ 0 (บาท · 2 ตำแหน่ง) | FIXED | DEC-14 (VALID) |
| BR-03 | แถวเงื่อนไขที่มีข้อมูลต้องมีรายการเอกสาร / เงื่อนไข และสถานะ · แถวว่างทั้งแถวไม่บันทึก (server ตัดซ้ำ) | FIXED | DEC-12 (VALID) |
| BR-04 | สถานะที่ยังไม่ "แล้วเสร็จ" ต้องมีผู้รับผิดชอบและกำหนดเสร็จ | FIXED | DEC-13 (VALID) |
| BR-05 | เงื่อนไขยังไม่แล้วเสร็จตอนส่ง/อนุมัติ = เตือน (แสดงจำนวน) ไม่บล็อก | CONFIGURABLE [AI-DEFAULT] | DEC-04 · DEC-15 (VALID) |
| BR-06 | สถานะเงื่อนไขอ่านจาก InvestmentMemo.condition_statuses (config) เท่านั้น | CONFIGURABLE | DEC-04 |
| BR-07 | ช่องตรงกระดาษ 1:1 · ไม่เพิ่มช่องเลขที่โครงการ (เสนอเป็นคำถามลูกค้าใน 00 §0.8) | FIXED [AI-DEFAULT] | DEC-06 · DEC-16 (VALID) |
| BR-08 | เงื่อนไขประกอบไม่จำกัดจำนวนแถว · wizard เริ่ม 1 แถวว่าง · ผู้เสนอค่าเริ่ม = ผู้จัดทำ | CONFIGURABLE [AI-DEFAULT] | DEC-05 · Rule #107 |
| BR-DOA-01 | ส่งอนุมัติได้เฉพาะ draft | FIXED | DOA |
| BR-DOA-02 | resolve สายตอนส่งแล้ว freeze | FIXED | DOA |
| BR-DOA-03 | reject → กลับ draft แก้ได้ · ประวัติ append-only (ตรงกับ DEC-08 — ไม่มีข้อยกเว้น) | FIXED | DEC-08 |
| BR-DOA-04 | ผู้จัดทำพิจารณาใบตัวเองไม่ได้ | FIXED | DOA |
| BR-DOA-05 | ส่ง estimated_amount ให้ DOA กลาง · ช่วงวงเงินตั้งที่ DOA กลางเท่านั้น (รอบนี้ matrix เดียว · TODO: DOA engine) | CONFIGURABLE | DEC-03 · OQ-06 |
| BR-09 | เลขออกตอนบันทึกครั้งแรก · กลับร่างใช้เลขเดิม | FIXED [AI-DEFAULT] | DEC-10 |
| BR-10 | approved ล็อกแก้ไขและยกเลิกไม่ได้ | FIXED | DEC-08 |
| BR-11 | ตารางลงชื่อใน PDF = ผู้จัดทำ + 1 แถวต่อขั้นที่ตั้งใน DOA (dynamic · ห้าม fix จำนวน) · คำตัดสินตาม role (print_config) · บล็อกลงชื่อไม่ถูกตัดข้ามหน้า | FIXED (จำนวน = DOA) | DEC-03 · DEC-07 |
| BR-12 | แบบพิมพ์ 2 หน้าทุกสถานะ (thai-doc R10) · ตัดหน้าก่อนเอกสารและเงื่อนไขประกอบ/บล็อกลงชื่อ · เงื่อนไขขั้นต่ำ 6 แถว · "หน้า N/2" | FIXED | DEC-05 |
| BR-13 | มองเห็น: เจ้าของ · ผู้อนุมัติหลังส่ง · admin_role ฝ่ายพัฒนาธุรกิจเห็นทั้งหมด | FIXED [AI-DEFAULT] | DEC-09 |
| BR-14 | ไม่เปลี่ยนค่าในระบบ ไม่ส่งต่อระบบอื่น (ไม่สร้างงบลงทุน/โครงการ) · แนบไฟล์ ✓ CSV ✓ ทำซ้ำ ✗ ประกาศ ✗ | FIXED [AI-DEFAULT] | DEC-01 · DEC-02 · DEC-11 |

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
| VR-01 | project_name · project_type · proposer | required | กรุณากรอกชื่อโครงการ / กรุณากรอกประเภทโครงการ / ธุรกรรม / กรุณาเลือกผู้เสนอ / ผู้รับผิดชอบ |
| VR-02 | estimated_amount | required · ตัวเลข ≥ 0 | กรุณาระบุวงเงินเป็นตัวเลขตั้งแต่ 0 ขึ้นไป |
| VR-03 | decision_requested · project_summary · strategic_rationale · financial_analysis · investment_framework · key_risks · bd_recommendation | required | กรุณากรอก{ชื่อหัวข้อ} |
| VR-04 | conditions[].item · status (แถวที่มีข้อมูล) | required · status ∈ config | แถวที่กรอกต้องมีรายการเอกสาร / เงื่อนไข และสถานะ |
| VR-05 | conditions[].owner · due_date (status ≠ แล้วเสร็จ) | required | สถานะที่ยังไม่ "แล้วเสร็จ" ต้องมีผู้รับผิดชอบและกำหนดเสร็จ |
| VR-06 | assignees | ครบทุกขั้น · ≠ ผู้จัดทำ | กรุณาเลือกผู้พิจารณา |
| VR-07 | reason (reject/cancel) | required | กรุณาระบุเหตุผล |

## §5.5 Edge Cases
| EC | กรณี | ผล | อ้าง |
|---|---|---|---|
| EC-01 | วงเงิน "250 ล้าน" / ติดลบ | บล็อก VR-02 | DEC-14 |
| EC-02 | แถวเงื่อนไขมีสถานะแต่ไม่มีรายการ | บล็อกที่แถว | DEC-12 |
| EC-03 | สถานะยังไม่แล้วเสร็จ ไม่มีผู้รับผิดชอบ/กำหนดเสร็จ | บล็อกที่แถว · เปลี่ยนเป็นแล้วเสร็จ = ปลดบังคับ | DEC-13 |
| EC-04 | ข้อความยาวทุกหัวข้อ + เงื่อนไข 12 แถว (ทดสอบ long-12conditions) | PDF ยัง 2 หน้า · > 20 แถวตารางข้ามหน้า (thead ซ้ำ · OQ-07) | DEC-05 |
| EC-05 | ผู้จัดทำเป็นผู้จัดการเอง | slot ขั้น 1 ว่าง ต้องเลือกคนอื่น | BR-DOA-04 |
| EC-06 | DOA แก้ระหว่างรอ | ใช้ snapshot | BR-DOA-02 |
| EC-07 | ตัดสินชนกัน | 409 STALE สถานะไม่เปลี่ยน | |
| EC-08 | doc_type ปิดใช้ | สร้างไม่ได้ 409 DOC_TYPE_INACTIVE | DEC-10 |
| EC-09 | ส่ง/อนุมัติขณะมีเงื่อนไขค้าง | แถบเตือนจำนวน · ไม่บล็อก · อนุมัติแล้วแจ้งผู้จัดทำ | DEC-15 |
| EC-10 | ไม่มีเลขโครงการบนกระดาษ | ไม่ผูกรอบนี้ → คำถามลูกค้า (00 §0.8) | DEC-16 |
| EC-11 | ไม่มีรายการเงื่อนไขเลย | ส่งได้ · drawer แผงไม่มีข้อมูล · PDF 6 แถวว่าง | DEC-05 |

## §5.6 Error Catalog
NOT_FOUND 404 · NOT_OWNER 403 · NOT_CURRENT_APPROVER 403 · NOT_DRAFT 409 · NOT_CANCELLABLE 409 · STALE 409 · DOC_TYPE_INACTIVE 409 · ASSIGNEE_REQUIRED 422 · SELF_APPROVAL 422 · REASON_REQUIRED 422 · VALIDATION 422

## §5.7 Security
SoD · ตรวจ/ตัดแถวฝั่ง server · audit append-only · PII ชื่อ snapshot · ข้อมูลการลงทุนเห็นตาม §5.3 เท่านั้น

## §5.8 Notifications (NTF_BRIEF)
ivm_cancelled · ivm_approved_open_conditions — ดู 03 FN-09
