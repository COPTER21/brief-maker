# 05_RULES — F-TMP-005

## §5.1 Business Rules
| ID | Rule | Tag | ที่มา |
|---|---|---|---|
| BR-01 | หน่วยงาน และ ฝ่าย/แผนกขอซื้อ เลือกจากผังองค์กร (active) · snapshot ชื่อ | FIXED | DEC-04 |
| BR-02 | หน่วย เลือกจาก UOM Master (active) · snapshot ชื่อ | FIXED | DEC-04 |
| BR-03 | แต่ละแถวต้องมี เลขที่ PR หรือ PO อย่างน้อย 1 · ต้องมี ≥1 แถว | FIXED | DEC-14 (VALID) |
| BR-04 | มีเลขที่ PO → วันที่สั่งซื้อ และ ผู้ผลิต/ผู้จัดจำหน่าย บังคับ (บล็อก) | FIXED | DEC-14 (VALID) |
| BR-05 | บังคับ รายละเอียด · จำนวนสั่งซื้อ > 0 · หน่วย · ฝ่าย/แผนก · สาเหตุคงค้าง · สถานะปัจจุบัน · แนวทางการแก้ไข | FIXED [AI-DEFAULT] | DEC-04 |
| BR-06 | วันที่รายงาน ≤ วันนี้ · วันที่สั่งซื้อ ≤ วันนี้ และ ≤ วันที่รายงาน · วันที่รับ ≥ วันที่สั่งซื้อ (ว่างได้ · อนาคตได้ = กำหนดรับ) | FIXED | DEC-04 · DEC-13 (VALID) |
| BR-07 | เลขที่ PR หรือ PO ซ้ำในรายงานเดียวกัน → เตือนในแถว + แถบในหน้าดู (ไม่บล็อก) | FIXED [AI-DEFAULT] | DEC-14 |
| BR-08 | เกณฑ์ "ค้างนาน" (วัน) อ่านจาก PurchaseConfig.outstanding_days เมื่อลูกค้ายืนยัน — รอบนี้ไม่ตรวจ/ไม่บล็อก/ไม่แสดงอายุค้าง · ห้ามตัวเลขใน code | CONFIGURABLE [AI-DEFAULT] | DEC-04 · DEC-15 (VALID) |
| BR-09 | ช่องตามกระดาษ 1:1 ไม่เพิ่มช่อง · ต้นแบบชีต 1 Rev.02 · รหัสฟอร์ม/Rev อ่านจาก doccfg | FIXED [AI-DEFAULT] | DEC-06 · DEC-12 (VALID) |
| BR-10 | เลขออกตอนบันทึกครั้งแรก · ไม่อนุมัติใช้เลขเดิม · no-gap ✗ | FIXED | DEC-10 |
| BR-11 | approved ล็อกแก้ไขและยกเลิกไม่ได้ | FIXED | DEC-08 |
| BR-12 | ไม่เปลี่ยนค่าในระบบ · ไม่ปิด/ยกเลิก PR-PO · ไม่ส่งต่อระบบอื่น (ppo.approved ประกาศไม่ยิง) | FIXED [AI-DEFAULT] | DEC-01 · DEC-02 |
| BR-13 | ช่องลงชื่อใน PDF = ผู้จัดทำ + 1 ช่องต่อขั้นที่ตั้งใน DOA (dynamic · ห้าม fix จำนวน) · แถวละ ≤ max_per_row · คำตัดสินตาม role (role-mgr-pur = อนุมัติ/ไม่อนุมัติ) · ข้อความ "ส่ง/พิจารณาในระบบ" | FIXED (จำนวน = DOA) [AI-DEFAULT] | DEC-03 · DEC-07 · DEC-16 (VALID) |
| BR-14 | แนบไฟล์ระดับรายงาน ✓ · CSV ✓ · ทำซ้ำ ✗ · ประกาศ ✗ | FIXED [AI-DEFAULT] | DEC-11 |
| BR-15 | แบบพิมพ์: แถวหน้า 1/หน้า 2 และแถวว่างขั้นต่ำมาจาก print_config (rows_page1 · rows_page1_min · rows_page2_min · rows_page2_max) ไม่ fix ใน code · เกิน rows_page1 + rows_page2_max → เตือน (OQ-08) | CONFIGURABLE | DEC-05 |
| BR-DOA-01 | ส่งได้เฉพาะ draft/returned | FIXED | DOA |
| BR-DOA-02 | resolve สายตอนส่งแล้ว freeze | FIXED | DOA |
| BR-DOA-03 | reject → กลับร่าง (status returned) แก้ได้ · ประวัติ append-only (ตรงกับ DEC-08 — ไม่มีข้อยกเว้น) | FIXED | DEC-08 |
| BR-DOA-04 | ผู้จัดทำพิจารณารายงานตัวเองไม่ได้ | FIXED | DOA |
| BR-DOA-05 | ไม่ใช้ (ไม่มีวงเงิน DEC-03) | — | |

## §5.2 State Machine
| จาก | event | ไป | guard |
|---|---|---|---|
| — | save | draft | FN-03 ออกเลข |
| draft/returned | save items | (เดิม) | owner · VR-01..10 |
| draft/returned | submit | pending(1) | owner · assignees ครบ · ≠ owner |
| pending(n) | approve | pending(n+1) / approved | assignee ขั้น n |
| pending(n) | reject | returned | assignee ขั้น n · เหตุผล |
| draft/pending/returned | cancel | cancelled | owner / admin · เหตุผล |

## §5.3 Permission Matrix (DEC-09)
| Action | owner | ผู้อยู่ในสาย | admin (role-mgr-pur ฝ่าย) | อื่น |
|---|:-:|:-:|:-:|:-:|
| ดูร่างของตน | ✓ | ✗ ไม่เห็นร่าง | ✓ | ✗ |
| ดูหลังส่ง | ✓ | ✓ | ✓ | ✗ (404) |
| แก้ไข | ✓ draft/returned | ✗ | ✗ | ✗ |
| ตัดสิน | ✗ | ขั้นปัจจุบันเท่านั้น | ขั้นของตน | ✗ |
| ยกเลิก | ✓ | ✗ | ✓ | ✗ |

## §5.4 Validation Rules
| VR | ช่อง | เงื่อนไข | ข้อความ | ผูก |
|---|---|---|---|---|
| VR-01 | report_date | required · ≤ วันนี้ | เลือกวันที่รายงาน / วันที่รายงานเป็นวันในอนาคตไม่ได้ | DEC-04 |
| VR-02 | org_unit | required | เลือกหน่วยงาน | DEC-04 |
| VR-03 | items | ≥1 แถว (แถวว่างทั้งแถวตัดทิ้ง) | บันทึก PR/PO ค้างอย่างน้อย 1 รายการ | DEC-04 |
| VR-04 | pr_no · po_no | อย่างน้อย 1 | ระบุเลขที่ PR หรือ PO อย่างน้อย 1 | DEC-14 |
| VR-05 | order_date | required เมื่อมี po_no · ≤ วันนี้ · ≤ report_date | มีเลขที่ PO ต้องระบุวันที่สั่งซื้อ / วันที่สั่งซื้อเป็นวันในอนาคตไม่ได้ / วันที่สั่งซื้อต้องไม่หลังวันที่รายงาน | DEC-14 · DEC-04 |
| VR-06 | receive_date | ≥ order_date | วันที่รับต้องไม่ก่อนวันที่สั่งซื้อ | DEC-13 |
| VR-07 | vendor_name | required เมื่อมี po_no | มีเลขที่ PO ต้องระบุผู้ผลิต/ผู้จัดจำหน่าย | DEC-14 |
| VR-08 | description · uom · request_dept | required (uom/dept active) | ระบุรายละเอียด / เลือกหน่วย / เลือกฝ่าย/แผนก | DEC-04 |
| VR-09 | order_qty | required · > 0 | ระบุจำนวนสั่งซื้อ / จำนวนต้องมากกว่า 0 | DEC-04 |
| VR-10 | outstanding_reason · current_status · corrective_action | required | ระบุสาเหตุคงค้าง / ระบุสถานะปัจจุบัน / ระบุแนวทางการแก้ไข | DEC-04 |
| VR-11 | slot ผู้พิจารณา | ครบทุกขั้น · ≠ owner | กรุณาเลือกผู้พิจารณา | BR-DOA-04 |
| VR-12 | เหตุผล ไม่อนุมัติ/ยกเลิก | required | กรุณาระบุเหตุผล | DEC-08 |

## §5.5 Edge Cases
| EC | กรณี | ผล | ผูก |
|---|---|---|---|
| EC-01 | แถวว่างทั้งแถว | ตัดทิ้งตอนบันทึก (ถ้ามีแถวอื่น) | VR-03 |
| EC-02 | PR ยังไม่ออก PO | กรอกเฉพาะ PR · วันที่สั่งซื้อ/ผู้ผลิตว่างได้ · นับ "ยังไม่ออก PO" | DEC-14 |
| EC-03 | เลข PR/PO ซ้ำ | เตือน ไม่บล็อก | BR-07 |
| EC-04 | วันที่รับเป็นวันในอนาคต | ผ่าน (กำหนดรับ) | DEC-13 |
| EC-05 | หน่วย/หน่วยงานถูกปิดใช้หลังบันทึก | แถวเดิมคง snapshot · แก้แถวต้องเลือกค่าที่ active | BR-01 · BR-02 |
| EC-06 | ผู้จัดทำ = ผู้จัดการจัดซื้อเอง | resolve ไปผู้บังคับบัญชาถัดไป · ตัวเองไม่อยู่ในรายชื่อ | BR-DOA-04 |
| EC-07 | แก้ DOA ระหว่างรออนุมัติ | ใช้สาย snapshot | BR-DOA-02 |
| EC-08 | stale | 409 → toast รีเฟรช | |
| EC-09 | doc_type ปิดใช้ | ปุ่มสร้าง disabled | DEC-10 |
| EC-10 | แถวเกิน rows_page1 + rows_page2_max (24) | แบบพิมพ์แสดง 24 แถวแรก · เตือนในขั้นตรวจสอบ/PDF Preview · แนะนำ CSV · OQ-08 | BR-15 |
| EC-11 | ข้อความยาวมากในคอลัมน์แคบ (แบบพิมพ์) | ตัดบรรทัดในช่อง · dense เมื่อ > 12 แถว · ถ้ายังล้น A4 → OQ-08 | BR-15 |

## §5.6 Notification (NTF_BRIEF_F-TMP-005)
| Event | Trigger | ผู้รับ | ช่องทาง | ปิดได้ |
|---|---|---|---|---|
| ppo_cancelled | pending → cancelled (FN-08) | ผู้อนุมัติขั้นปัจจุบัน | in-app | ✓ |
DOA engine เป็นเจ้าของ doa_pending · doa_result · doa_escalate
