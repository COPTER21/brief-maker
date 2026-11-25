# 05_RULES — F-TMP-003

## §5.1 Business Rules
| ID | Rule | Tag | ที่มา |
|---|---|---|---|
| BR-01 | 1 ใบ = 1 request_type · ฟิลด์ของประเภทอื่นเป็นค่าว่าง | FIXED [AI-DEFAULT] | DEC-04 · DEC-13 (VALID) |
| BR-02 | add: ชื่อบัญชี ≥ 1 แถว · ไม่ซ้ำในใบ · ไม่จำกัดแถว · PDF ≥ 4 แถว | CONFIGURABLE (print_config.min_rows) [AI-DEFAULT] | DEC-04 · DEC-05 |
| BR-03 | รหัสบัญชี/ชื่อบัญชีเป็นข้อความอิสระ — ยังไม่ตรวจกับ COA | CONFIGURABLE | OQ-04 |
| BR-04 | ช่องตรงกระดาษ 1:1 · ไม่เพิ่มช่อง · ป้ายส่วนยกเลิก "วัตถุประสงค์ในการยกเลิก" | FIXED [AI-DEFAULT] | DEC-06 · DEC-12 (VALID) |
| BR-05 | อนุมัติ/บันทึกเข้าระบบไม่แก้ COA อัตโนมัติ · ไม่ส่งต่อระบบอื่น | FIXED [AI-DEFAULT] | DEC-01 · DEC-02 |
| BR-06 | แนบไฟล์ระดับใบ · ส่งออก CSV · ไม่มีทำซ้ำ | FIXED [AI-DEFAULT] | DEC-11 |
| BR-DOA-01 | ส่งอนุมัติได้เฉพาะ draft | FIXED | DOA |
| BR-DOA-02 | resolve สายตอนส่งแล้ว freeze | FIXED | DOA · DEC-03 |
| BR-DOA-03 | reject → กลับ draft เลขเดิม แก้ได้ · ประวัติ append-only (ตรงกับ DEC-08 — ไม่มีข้อยกเว้น) | FIXED | DEC-08 |
| BR-DOA-04 | ผู้ขอพิจารณาใบตัวเองไม่ได้ | FIXED | DOA |
| BR-DOA-05 | ไม่ใช้ (ไม่มีวงเงิน DEC-03) | — | |
| BR-07 | ไม่อนุมัติ → เหตุผลบังคับ | FIXED | DEC-14 (VALID) |
| BR-08 | เลขออกตอนบันทึกครั้งแรก · กลับร่างใช้เลขเดิม | FIXED | DEC-10 |
| BR-09 | approved/recorded ล็อกแก้ไข · ยกเลิกได้เฉพาะ draft/pending โดยเจ้าของหรือ admin · เหตุผลบังคับ | FIXED [AI-DEFAULT] | DEC-08 |
| BR-10 | ช่องลงชื่อ PDF = ผู้ขอ + 1 ช่องต่อขั้นที่ตั้งใน DOA (dynamic · ห้าม fix) · แถวละ ≤4 · คำตัดสินตาม role · ข้อความ "ส่ง/พิจารณาในระบบ" ไม่ใช้ภาพ · บรรทัดผู้บันทึกเข้าระบบคงที่ตามกระดาษ | FIXED (จำนวน = DOA) | DEC-03 · DEC-07 |
| BR-11 | บันทึกเข้าระบบแล้ว ได้เฉพาะ approved · โดย admin ฝ่ายบัญชี · วันที่ ≤ วันนี้ ∧ ≥ วันที่อนุมัติ | FIXED [AI-DEFAULT] | DEC-01 |
| BR-12 | การมองเห็น: เจ้าของ · ผู้อนุมัติเห็นหลังส่ง · admin ฝ่ายบัญชีเห็นทั้งหมด · ร่างไม่เห็นโดยผู้อนุมัติ | FIXED [AI-DEFAULT] | DEC-09 |
| BR-13 | อนุมัติครบ → แจ้งฝ่ายบัญชี acr_ready_to_record · บันทึกแล้ว → แจ้งผู้ขอ acr_recorded · ยกเลิกระหว่างรอ → acr_cancelled | FIXED | NTF_BRIEF |

## §5.2 State Machine
| จาก | event | ไป | guard |
|---|---|---|---|
| — | save | draft | FN-03 ออกเลข |
| draft | submit | pending(1) | owner · assignees ครบ |
| pending(n) | approve | pending(n+1) / approved | assignee ขั้น n |
| pending(n) | reject | draft | assignee ขั้น n · เหตุผล |
| approved | record | recorded | admin ฝ่ายบัญชี · BR-11 |
| draft/pending | cancel | cancelled | owner/admin · เหตุผล |

## §5.3 Permission Matrix
| Action | owner | ผู้พิจารณาขั้นปัจจุบัน | อยู่ในสาย (ไม่ใช่ขั้นปัจจุบัน) | admin บัญชี | อื่น |
|---|:-:|:-:|:-:|:-:|:-:|
| ดู draft | ✓ | ✗ | ✗ | ✓ | ✗ |
| ดู pending/approved/recorded/cancelled | ✓ | ✓ | ✓ | ✓ | ✗ |
| แก้ draft | ✓ | ✗ | ✗ | ✗ | ✗ |
| ตัดสิน | ✗ | ✓ | ✗ | ✗ | ✗ |
| บันทึกเข้าระบบแล้ว | ✗ | ✗ | ✗ | ✓ | ✗ |
| ยกเลิก | ✓ | ✗ | ✗ | ✓ | ✗ |

## §5.4 Validation
| VR | ช่อง | เงื่อนไข | ข้อความ |
|---|---|---|---|
| VR-01 | request_type | required | กรุณาเลือกประเภทคำขอ |
| VR-02 | add_lines[].account_name | ≥ 1 แถวที่ไม่ว่าง (เมื่อ add) | กรุณาระบุชื่อบัญชีอย่างน้อย 1 บัญชี |
| VR-03 | add_lines[].account_name | ไม่ซ้ำในใบ | ชื่อบัญชีซ้ำกับบรรทัดที่ n |
| VR-04 | add.purpose / edit.purpose / cancel.purpose | required ตามประเภท | กรุณาระบุวัตถุประสงค์ในการเพิ่ม/แก้ไข/ยกเลิก |
| VR-05 | edit.account_code · edit.change_to | required เมื่อ edit | กรุณาระบุรหัสบัญชี · กรุณาระบุว่าแก้ไขเป็นอะไร |
| VR-06 | cancel.account_code · cancel.account_name | required เมื่อ cancel | กรุณาระบุรหัสบัญชี · กรุณาระบุชื่อบัญชี |
| VR-07 | slot ผู้พิจารณา | ทุกขั้น · ≠ ผู้ขอ | กรุณาเลือกผู้พิจารณา |
| VR-08 | เหตุผล ไม่อนุมัติ/ยกเลิก | required (DEC-14) | กรุณาระบุเหตุผล |
| VR-09 | วันที่บันทึกเข้าระบบ | required · ≤ วันนี้ · ≥ วันที่อนุมัติ | กรุณาเลือกวันที่บันทึกเข้าระบบ |

## §5.5 Edge Cases
| EC | กรณี | ผล |
|---|---|---|
| EC-01 | เปลี่ยนประเภทคำขอกลางทาง | ส่วนเดิมไม่ถูกบันทึก (FN-02) · PDF ☑ ตามประเภทสุดท้าย |
| EC-02 | ขอเพิ่ม > 4 บัญชี | PDF dense (ทดสอบ 12 แถว 1 หน้า) |
| EC-03 | ผู้ขอเป็นผู้อนุมัติเอง | resolve ข้ามตัวเอง · slot เลือกคนอื่น (BR-DOA-04) |
| EC-04 | แก้ DOA ระหว่างใบรออนุมัติ | ใบเดิมใช้สาย snapshot |
| EC-05 | ส่ง/อนุมัติชนกัน | 409 STALE → toast รีเฟรช |
| EC-06 | doc_type ปิดใช้ | ปุ่มสร้าง disabled + แถบแดง |
| EC-07 | รหัสบัญชีไม่มีจริง/ชื่อบัญชีที่ขอเพิ่มมีอยู่แล้วในผังบัญชี | ไม่ตรวจรอบนี้ — ผู้ตรวจสอบตรวจเอง (OQ-04) |
| EC-08 | DOA 6 ขั้น + เพิ่ม 12 บัญชี | PDF 2 หน้า บล็อกลงชื่อขึ้นหน้า 2 ทั้งก้อน (keep_together) |
| EC-09 | อนุมัติแล้วยังไม่บันทึกเข้าระบบ | badge "รอบันทึกเข้าระบบ n" (admin) · แบนเนอร์ในใบ |
