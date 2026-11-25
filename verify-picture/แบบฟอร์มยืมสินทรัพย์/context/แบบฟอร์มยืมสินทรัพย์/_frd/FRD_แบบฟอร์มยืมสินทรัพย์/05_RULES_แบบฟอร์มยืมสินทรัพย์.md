# 05_RULES — F-TMP-002

## §5.1 Business Rules
| ID | Rule | Tag | ที่มา |
|---|---|---|---|
| BR-01 | ชื่อรายการ = Asset Master.name ของทะเบียนที่เลือก (snapshot) | FIXED | DEC-06 |
| BR-02 | จำนวนที่ให้ยืม 1 ≤ qty_lent ≤ qty_requested · ค่าเริ่ม = qty_requested · บังคับเมื่ออนุมัติ | FIXED [AI-DEFAULT] | DEC-04 · DEC-12 (VALID) |
| BR-03 | วันที่ส่งคืน ≥ วันที่ยืม (บล็อก) · รับคืนจริงบันทึกที่ส่วนรับคืน | FIXED | DEC-04 · DEC-13 (VALID) |
| BR-04 | ทะเบียนสินทรัพย์ซ้ำในใบเดียว = บล็อก | FIXED [AI-DEFAULT] | DEC-04 |
| BR-05 | เลยกำหนดคืน = เตือน (ป้าย · แบนเนอร์ · aln_overdue) ไม่บล็อก | CONFIGURABLE [AI-DEFAULT] | DEC-04 |
| BR-06 | ไม่จำกัดจำนวนแถว · PDF ≥ 11 แถว | CONFIGURABLE (print_config.min_rows) | DEC-05 |
| BR-07 | ช่องตรงกระดาษ 1:1 · ไม่เพิ่มช่อง | FIXED [AI-DEFAULT] | DEC-06 |
| BR-08 | อนุมัติ/รับคืนไม่เปลี่ยนค่าใน Asset Master · ไม่ส่งต่อระบบอื่น | FIXED [AI-DEFAULT] | DEC-01 · DEC-02 |
| BR-09 | แนบไฟล์ระดับใบ · ส่งออก CSV | FIXED [AI-DEFAULT] | DEC-11 |
| BR-DOA-01 | ส่งอนุมัติได้เฉพาะ draft | FIXED | DOA |
| BR-DOA-02 | resolve สายตอนส่งแล้ว freeze | FIXED | DOA · DEC-03 |
| BR-DOA-03 | reject → กลับ draft เลขเดิม แก้ได้ · ประวัติ append-only (ตรงกับ DEC-08 — ไม่มีข้อยกเว้น) | FIXED | DEC-08 |
| BR-DOA-04 | ผู้ยืมพิจารณาใบตัวเองไม่ได้ | FIXED | DOA |
| BR-DOA-05 | ไม่ใช้ (ไม่มีวงเงิน DEC-03) | — | |
| BR-10 | เลขออกตอนบันทึกครั้งแรก · กลับร่างใช้เลขเดิม | FIXED | DEC-10 |
| BR-11 | approved/returned ล็อกแก้ไข · ยกเลิกได้เฉพาะ draft/pending โดยเจ้าของหรือ admin · เหตุผลบังคับ | FIXED [AI-DEFAULT] | DEC-08 |
| BR-12 | ช่องลงชื่อ PDF = ผู้ยืม + 1 ช่องต่อขั้นที่ตั้งใน DOA (dynamic · ห้าม fix) · แถวละ ≤4 · คำตัดสินตาม role · ข้อความ "ส่ง/พิจารณาในระบบ" ไม่ใช้ภาพ · ส่วนรับคืน 2 ช่องตามกระดาษ | FIXED (จำนวน = DOA) | DEC-03 · DEC-07 |
| BR-13 | บันทึกรับคืนได้เฉพาะ approved · ผู้รับคืน = ผู้ให้ยืมในสาย หรือ admin · วันที่รับคืน ≤ วันนี้ ∧ ≥ วันที่ยืมแรก | FIXED [AI-DEFAULT] | DEC-04 · DEC-13 |
| BR-14 | การมองเห็น: เจ้าของ · ผู้อนุมัติเห็นหลังส่ง · admin ฝ่ายบริหารสินทรัพย์เห็นทั้งหมด · ร่างไม่เห็นโดยผู้อนุมัติ | FIXED [AI-DEFAULT] | DEC-09 |

## §5.2 State Machine
| จาก | event | ไป | guard |
|---|---|---|---|
| — | save | draft | FN-03 ออกเลข |
| draft | submit | pending(1) | owner · assignees ครบ |
| pending(n) | approve | pending(n+1) / approved | assignee ขั้น n · BR-02 |
| pending(n) | reject | draft | assignee ขั้น n · เหตุผล |
| approved | return | returned | ผู้ให้ยืมในสาย/admin · BR-13 |
| draft/pending | cancel | cancelled | owner/admin · เหตุผล |

## §5.3 Permission Matrix
| Action | owner | ผู้พิจารณาขั้นปัจจุบัน | อยู่ในสาย (ไม่ใช่ขั้นปัจจุบัน) | admin สินทรัพย์ | อื่น |
|---|:-:|:-:|:-:|:-:|:-:|
| ดู draft | ✓ | ✗ | ✗ | ✓ | ✗ |
| ดู pending/approved/returned/cancelled | ✓ | ✓ | ✓ | ✓ | ✗ |
| แก้ draft | ✓ | ✗ | ✗ | ✗ | ✗ |
| ตัดสิน | ✗ | ✓ | ✗ | ✗ | ✗ |
| บันทึกรับคืน | ✗ | – | ✓ (ถ้า approved ในสาย) | ✓ | ✗ |
| ยกเลิก | ✓ | ✗ | ✗ | ✓ | ✗ |

## §5.4 Validation
| VR | ช่อง | เงื่อนไข | ข้อความ |
|---|---|---|---|
| VR-01 | purpose | required | กรุณาระบุว่ายืมไปใช้ทำอะไร |
| VR-02 | items[] ทะเบียน · จำนวน · วันที่ยืม · วันที่ส่งคืน | required · จำนวน ≥ 1 · ≥1 แถว | กรอกให้ครบ: … |
| VR-03 | return_date | ≥ borrow_date | วันที่ส่งคืนต้องไม่ก่อนวันที่ยืม |
| VR-04 | asset_code | ไม่ซ้ำในใบ | ทะเบียนสินทรัพย์ซ้ำกับรายการที่ n |
| VR-05 | qty_lent | 1..qty_requested | จำนวนที่ให้ยืมต้องอยู่ระหว่าง 1 ถึงจำนวนที่ยืม |
| VR-06 | slot ผู้พิจารณา | ทุกขั้น · ≠ ผู้ยืม | กรุณาเลือกผู้พิจารณา |
| VR-07 | เหตุผล ไม่ให้ยืม/ยกเลิก | required | กรุณาระบุเหตุผล |
| VR-08 | วันที่รับคืน | required · ≤ วันนี้ · ≥ วันที่ยืมแรก | กรุณาเลือกวันที่รับคืน |

## §5.5 Edge Cases
| EC | กรณี | ผล |
|---|---|---|
| EC-01 | ให้ยืมน้อยกว่าที่ขอ | qty_lent < qty_requested · PDF แสดงทั้งสองคอลัมน์ |
| EC-02 | รายการ > 11 แถว | PDF dense (ทดสอบ 14 แถว) |
| EC-03 | ผู้ยืมเป็นผู้ให้ยืมเอง | resolve ข้ามตัวเอง · slot เลือกคนอื่น (BR-DOA-04) |
| EC-04 | แก้ DOA ระหว่างใบรออนุมัติ | ใบเดิมใช้สาย snapshot |
| EC-05 | ส่ง/อนุมัติชนกัน | 409 STALE → toast รีเฟรช |
| EC-06 | doc_type ปิดใช้ | ปุ่มสร้าง disabled + แถบแดง |
| EC-07 | ยืมซ้อนข้ามใบ | ไม่ตรวจรอบนี้ (OQ-05) |
| EC-08 | วันที่ยืมย้อนหลัง | ส่งได้ · เตือนขั้นตรวจสอบ |
| EC-09 | เลยกำหนดคืน | ป้ายแดง · แบนเนอร์ · aln_overdue วันละครั้ง |
