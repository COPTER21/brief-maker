# 05_RULES — F-TMP-003

## §5.1 Business Rules
| ID | Rule | Tag | ที่มา |
|---|---|---|---|
| BR-01 | แนวทางการเคลียร์อ่านจาก SlowMoveConfig.clearance_methods (config) แล้ว snapshot ข้อความลงแถว · "อื่น ๆ" ต้องระบุ | CONFIGURABLE [AI-DEFAULT] | DEC-04 |
| BR-02 | รหัสสินค้าเลือกจาก Product Master (active) · รายละเอียด/หน่วย snapshot แก้ไม่ได้ | FIXED | DEC-04 |
| BR-03 | แต่ละแถวบังคับ รหัสสินค้า · วันที่ติดตาม · แนวทาง · ต้องมี ≥1 แถว | FIXED [AI-DEFAULT] | DEC-04 |
| BR-04 | วันที่ (เคลียร์) + จำนวน กรอกคู่กัน · จำนวน > 0 · วันที่เคลียร์ ≥ วันที่ติดตาม · วันที่ติดตาม/เคลียร์ ≤ วันนี้ (บล็อก) · วันหมดอายุเป็นอนาคตได้ | FIXED | DEC-13 (VALID) |
| BR-05 | วันหมดอายุ ≤ วันที่ติดตาม → เตือนในแถว + การ์ดสรุป + แถบในหน้าดู (ไม่บล็อก) | FIXED | DEC-14 (VALID) |
| BR-06 | รหัสสินค้าซ้ำในใบ → เตือน (อาจคนละ lot · ไม่บล็อก) | FIXED [AI-DEFAULT] | DEC-04 |
| BR-07 | 1 ใบ = ผู้จัดทำ × เดือน · ไม่บังคับไม่ซ้ำ (ไม่มีช่องคลัง) | FIXED [AI-DEFAULT] | DEC-04 · DEC-15 (VALID) |
| BR-08 | ช่องตามกระดาษ 1:1 ไม่เพิ่มช่อง · ยึดหัวตารางแถว 5 ไม่ใช้หัวร่างแถว 4 | FIXED [AI-DEFAULT] | DEC-06 · DEC-12 (VALID) |
| BR-09 | เลขออกตอนบันทึกครั้งแรก · ไม่อนุมัติใช้เลขเดิม · no-gap ✗ | FIXED | DEC-10 |
| BR-10 | approved ล็อกแก้ไขและยกเลิกไม่ได้ | FIXED | DEC-08 |
| BR-11 | ไม่เปลี่ยนค่าในระบบ · ไม่ตัดสต็อก · ไม่ส่งต่อระบบอื่น (smc.approved ประกาศไม่ยิง) | FIXED [AI-DEFAULT] | DEC-01 · DEC-02 |
| BR-12 | ช่องลงชื่อใน PDF = ผู้จัดทำ + 1 ช่องต่อขั้นที่ตั้งใน DOA (dynamic · ห้าม fix จำนวน) · แถวละ ≤ max_per_row · คำตัดสินตาม role (role-mgr-wh = อนุมัติ/ไม่อนุมัติ) · ข้อความ "ส่ง/พิจารณาในระบบ" | FIXED (จำนวน = DOA) [AI-DEFAULT] | DEC-03 · DEC-07 |
| BR-13 | แนบไฟล์ระดับใบ ✓ · CSV ✓ · ทำซ้ำ ✗ · ประกาศ ✗ | FIXED [AI-DEFAULT] | DEC-11 |
| BR-14 | แบบพิมพ์: แถวหน้า 1/หน้า 2 และจำนวนแถวว่างขั้นต่ำมาจาก print_config (rows_page1 · rows_page2_min · rows_page2_max) ไม่ fix ใน code | CONFIGURABLE | DEC-05 |
| BR-DOA-01 | ส่งได้เฉพาะ draft/returned | FIXED | DOA |
| BR-DOA-02 | resolve สายตอนส่งแล้ว freeze | FIXED | DOA |
| BR-DOA-03 | reject → กลับร่าง (status returned) แก้ได้ · ประวัติ append-only (ตรงกับ DEC-08 — ไม่มีข้อยกเว้น) | FIXED | DEC-08 |
| BR-DOA-04 | ผู้จัดทำพิจารณาใบตัวเองไม่ได้ | FIXED | DOA |
| BR-DOA-05 | ไม่ใช้ (ไม่มีวงเงิน DEC-03) | — | |

## §5.2 State Machine
| จาก | event | ไป | guard |
|---|---|---|---|
| — | save | draft | FN-03 ออกเลข |
| draft/returned | save items | (เดิม) | owner · VR-01..06 |
| draft/returned | submit | pending(1) | owner · assignees ครบ · ≠ owner |
| pending(n) | approve | pending(n+1) / approved | assignee ขั้น n |
| pending(n) | reject | returned | assignee ขั้น n · เหตุผล |
| draft/pending/returned | cancel | cancelled | owner / admin · เหตุผล |

## §5.3 Permission Matrix (DEC-09)
| Action | owner | ผู้อยู่ในสาย | admin (role-mgr-wh ฝ่าย) | อื่น |
|---|:-:|:-:|:-:|:-:|
| ดูร่างของตน | ✓ | ✗ ไม่เห็นร่าง | ✓ | ✗ |
| ดูหลังส่ง | ✓ | ✓ | ✓ | ✗ (404) |
| แก้ไข | ✓ draft/returned | ✗ | ✗ | ✗ |
| ตัดสิน | ✗ | ขั้นปัจจุบันเท่านั้น | ขั้นของตน | ✗ |
| ยกเลิก | ✓ | ✗ | ✓ | ✗ |

## §5.4 Validation Rules
| VR | ช่อง | เงื่อนไข | ข้อความ | ผูก |
|---|---|---|---|---|
| VR-01 | clearance_month | required · ≤ เดือนปัจจุบัน | เลือกเดือน | DEC-04 |
| VR-02 | items | ≥1 แถว (แถวว่างทั้งแถวตัดทิ้ง) | บันทึกสินค้าอย่างน้อย 1 รายการ | DEC-04 |
| VR-03 | product_code | required · active | เลือกสินค้า / สินค้านี้ปิดใช้งานแล้ว | DEC-04 |
| VR-04 | follow_up_date | required · ≤ วันนี้ | ระบุวันที่ติดตาม / วันที่ติดตามเป็นวันในอนาคตไม่ได้ | DEC-13 |
| VR-05 | clearance_method | required · need_note → note | เลือกแนวทางการเคลียร์ / ระบุแนวทางการเคลียร์ | DEC-04 |
| VR-06 | cleared_date · cleared_qty | คู่กัน · qty > 0 · date ≥ follow_up_date · ≤ วันนี้ | กรอกจำนวนคู่กับวันที่ / ระบุวันที่คู่กับจำนวน / จำนวนต้องมากกว่า 0 / วันที่ต้องไม่ก่อนวันที่ติดตาม / วันที่เป็นวันในอนาคตไม่ได้ | DEC-13 |
| VR-07 | slot ผู้พิจารณา | ครบทุกขั้น · ≠ owner | กรุณาเลือกผู้พิจารณา | BR-DOA-04 |
| VR-08 | เหตุผล ไม่อนุมัติ/ยกเลิก | required | กรุณาระบุเหตุผล | DEC-08 |

## §5.5 Edge Cases
| EC | กรณี | ผล | ผูก |
|---|---|---|---|
| EC-01 | แถวว่างทั้งแถว | ตัดทิ้งตอนบันทึก (ถ้ามีแถวอื่น) | VR-02 |
| EC-02 | ยังเคลียร์ไม่ได้ | เว้นวันที่/จำนวน · สรุป "ค้าง" | DEC-13 |
| EC-03 | สินค้าหมดอายุแล้ว ณ วันที่ติดตาม | เตือน ไม่บล็อก | DEC-14 |
| EC-04 | รหัสสินค้าซ้ำ | เตือน ไม่บล็อก | BR-06 |
| EC-05 | สินค้า/แนวทางถูกปิดใช้หลังบันทึก | แถวเดิมคง snapshot · แก้แถวต้องเลือกค่าที่ active | BR-02 |
| EC-06 | ผู้จัดทำ = ผู้จัดการคลังเอง | resolve ไปผู้บังคับบัญชาถัดไป · ตัวเองไม่อยู่ในรายชื่อ | BR-DOA-04 |
| EC-07 | แก้ DOA ระหว่างรออนุมัติ | ใช้สาย snapshot | BR-DOA-02 |
| EC-08 | stale | 409 → toast รีเฟรช | |
| EC-09 | doc_type ปิดใช้ | ปุ่มสร้าง disabled | DEC-10 |
| EC-10 | แถวเกิน rows_page1 + rows_page2_max | PDF หน้า 2 แสดงเตือนใน PDF Preview · OQ-08 | BR-14 |

## §5.6 Notification (NTF_BRIEF_F-TMP-003)
| Event | Trigger | ผู้รับ | ช่องทาง | ปิดได้ |
|---|---|---|---|---|
| smc_cancelled | pending → cancelled (FN-08) | ผู้อนุมัติขั้นปัจจุบัน | in-app | ✓ |
DOA engine เป็นเจ้าของ doa_pending · doa_result · doa_escalate
