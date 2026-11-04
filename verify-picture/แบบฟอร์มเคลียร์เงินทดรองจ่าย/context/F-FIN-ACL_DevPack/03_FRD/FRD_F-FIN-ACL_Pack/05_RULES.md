# 05_RULES — F-FIN-ACL

## §5.1 Business Rules
| ID | Rule | Tag | ที่มา |
|---|---|---|---|
| BR-01 | รวมค่าใช้จ่าย = Σ จำนวนเงิน | FIXED | DEC-04 |
| BR-02 | เหลือส่งคืน = ยอดเบิก − รวม · TOTAL = เหลือส่งคืน · ตัวอักษรตรงยอดเสมอ | FIXED | DEC-04 · DEC-12 (VALID) |
| BR-03 | ติดลบ = เตือน ไม่บล็อก · แจ้งการเงินเมื่ออนุมัติครบ | CONFIGURABLE [AI-DEFAULT] | DEC-04 · DEC-13 (VALID) |
| BR-04 | เหลือคืน > 0 ต้องมีไฟล์ refund_slip ก่อนขั้น role-finance-officer อนุมัติ | CONFIGURABLE [AI-DEFAULT] | DEC-04 |
| BR-05 | หมายเหตุเส้นตาย = ExpensePolicy.advance_clear_due_day (ไม่เตือนเลยกำหนดรอบนี้) | CONFIGURABLE | DEC-04 |
| BR-06 | บัญชีรับเงินคืนจาก Company.bank_accounts[purpose=advance_refund] | CONFIGURABLE | DEC-04 |
| BR-07 | ป้ายช่อง "ฝ่าย/แผนก" (แก้จาก "ผ่าย") · ช่อง 1:1 ไม่เพิ่มช่อง | FIXED [AI-DEFAULT] | DEC-06 · DEC-14 (VALID) |
| BR-08 | แนบไฟล์ระดับใบ (ใบเสร็จ + สลิป) · ไม่ผูกหมวดบัญชีรอบนี้ | FIXED [AI-DEFAULT] | DEC-11 · DEC-15 (VALID) |
| BR-DOA-01 | ส่งอนุมัติได้เฉพาะ draft | FIXED | DOA |
| BR-DOA-02 | resolve สายตอนส่งแล้ว freeze | FIXED | DOA |
| BR-DOA-03 | reject → กลับ draft แก้ได้ · ประวัติ append-only (ตรงกับ DEC-08 — ไม่มีข้อยกเว้น) | FIXED | DEC-08 |
| BR-DOA-04 | ผู้ขอพิจารณาใบตัวเองไม่ได้ | FIXED | DOA |
| BR-DOA-05 | ไม่ใช้ (ไม่มีวงเงิน DEC-03) | — | |
| BR-09 | เลขออกตอนบันทึกครั้งแรก · กลับร่างใช้เลขเดิม | FIXED | DEC-10 |
| BR-10 | approved ล็อกแก้ไขและยกเลิกไม่ได้ | FIXED | DEC-08 |
| BR-12 | ช่องลงชื่อใน PDF = ผู้ขอ + 1 ช่องต่อขั้นที่ตั้งใน DOA (dynamic · ห้าม fix จำนวน) · แถวละ ≤4 · คำตัดสินตาม role (print_config) · บล็อกลงชื่อไม่ถูกตัดข้ามหน้า | FIXED (จำนวน = DOA · CONFIGURABLE ที่ DOA กลาง) | DEC-03 · DEC-07 |

## §5.2 State Machine
| จาก | event | ไป | guard |
|---|---|---|---|
| — | save | draft | FN-03 ออกเลข |
| draft | submit | pending(1) | owner · assignees ครบ |
| pending(n) | approve | pending(n+1) / approved | assignee ขั้น n · BR-04 ที่ขั้น finance-officer |
| pending(n) | reject | draft | assignee ขั้น n · เหตุผล |
| draft/pending | cancel | cancelled | owner/finance-officer · เหตุผล |

## §5.3 Permission Matrix
| Action | owner | ผู้พิจารณาขั้นปัจจุบัน | อยู่ในสาย (ไม่ใช่ขั้นปัจจุบัน) | role-finance-officer | อื่น |
|---|:-:|:-:|:-:|:-:|:-:|
| ดู draft | ✓ | ✗ | ✗ | ✓ | ✗ |
| ดู pending/approved/cancelled | ✓ | ✓ | ✓ | ✓ | ✗ |
| แก้ draft | ✓ | ✗ | ✗ | ✗ | ✗ |
| ตัดสิน | ✗ | ✓ | ✗ | (เฉพาะขั้นตน) | ✗ |
| ยกเลิก | ✓ | ✗ | ✗ | ✓ | ✗ |

## §5.4 Validation
| VR | ช่อง | กฎ | ข้อความ |
|---|---|---|---|
| VR-01 | advance_ref | required | กรุณาใส่เลขที่ใบเบิก |
| VR-02 | advance_amount | > 0 | ใส่ยอดที่เบิกมากกว่า 0 |
| VR-03 | lines | ≥1 · description required · amount > 0 | ใส่รายละเอียดและจำนวนเงิน (มากกว่า 0) ให้ครบทุกรายการ |
| VR-04 | assignees | ครบทุกขั้น · ≠ ผู้ขอ | กรุณาเลือกผู้พิจารณา |
| VR-05 | reason (reject/cancel) | required | กรุณาระบุเหตุผล |

## §5.5 Edge Cases
| EC | กรณี | ผล | อ้าง |
|---|---|---|---|
| EC-01 | ใช้พอดี | TOTAL 0.00 · ไม่ต้องสลิป | BR-02 |
| EC-02 | ใช้เกิน | ติดลบ · เตือน · acl_overspent_approved | DEC-13 |
| EC-03 | >10 รายการ | PDF dense 1 หน้า (14 แถวผ่าน) | DEC-05 |
| EC-04 | ผู้ขอ = การเงิน | slot ขั้น 2 ว่าง ต้องเลือกคนอื่น | BR-DOA-04 |
| EC-05 | DOA แก้ระหว่างรอ | ใช้ snapshot | BR-DOA-02 |
| EC-06 | อนุมัติชนกัน | 409 STALE สถานะไม่เปลี่ยน | |
| EC-07 | doc_type ปิดใช้ | สร้างไม่ได้ 409 DOC_TYPE_INACTIVE | DEC-10 |
| EC-08 | เคลียร์ใบเบิกซ้ำ | ไม่ตรวจรอบนี้ → OQ-05 | DEC-02 |
| EC-09 | TOTAL ว่าง/ตัวอักษรไม่ตรง (บั๊กในต้นฉบับ) | คำนวณเสมอ | DEC-12 |

## §5.6 Error Catalog
NOT_FOUND 404 · NOT_OWNER 403 · NOT_CURRENT_APPROVER 403 · NOT_DRAFT 409 · NOT_CANCELLABLE 409 · STALE 409 · DOC_TYPE_INACTIVE 409 · ASSIGNEE_REQUIRED 422 · SELF_APPROVAL 422 · REASON_REQUIRED 422 · REFUND_SLIP_REQUIRED 422 · VALIDATION 422

## §5.7 Security
D5 Financial: คำนวณฝั่ง server · SoD · audit · D7 PII: ชื่อ snapshot · D9 Audit append-only

## §5.8 Notifications (NTF_BRIEF)
acl_cancelled · acl_overspent_approved · acl_refund_due — ดู 03 FN-09
