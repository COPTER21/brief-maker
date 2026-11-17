# 05_RULES — F-TMP-002

## §5.1 Business Rules
| ID | Rule | Tag | ที่มา |
|---|---|---|---|
| BR-01 | รายการตรวจทั้ง 3 กลุ่มอ่านจาก ForkliftChecklistConfig (config) แล้ว snapshot ลงใบ | CONFIGURABLE [AI-DEFAULT] | DEC-04 |
| BR-02 | คอลัมน์วันตามปฏิทินของ inspection_month · PDF พิมพ์หัววันตามกระดาษ | FIXED | DEC-04 |
| BR-03 | กรอกได้เฉพาะ general + ประเภทรถที่เลือก · เปลี่ยนประเภท = ล้างส่วนเฉพาะเดิม · PDF คงตารางอีกประเภทว่าง | FIXED | DEC-14 (VALID) |
| BR-04 | ห้ามวันเกินเดือน/วันอนาคต (บล็อก) | FIXED | DEC-15 (VALID) |
| BR-05 | วันที่มีผลต้องครบทุกรายการ · ต้องมีอย่างน้อย 1 วันครบก่อนบันทึก | FIXED [AI-DEFAULT] | DEC-04 |
| BR-06 | ng เพิ่มจากครั้งก่อน → เตือนบนจอ + fli_defect_found ถึงหัวหน้างาน (ไม่บล็อก) | CONFIGURABLE | DEC-16 (VALID) |
| BR-07 | 1 ใบ = ผู้ตรวจสอบ × ประเภทรถ × เดือน · ไม่บังคับไม่ซ้ำ (ไม่มีหมายเลขรถ) | FIXED [AI-DEFAULT] | DEC-04 · DEC-17 (VALID) |
| BR-08 | ช่องตามกระดาษ 1:1 ไม่เพิ่มช่อง · หมายเหตุสะกด "ปฏิบัติ" | FIXED [AI-DEFAULT] | DEC-08 |
| BR-09 | เลขออกตอนบันทึกครั้งแรก · ส่งกลับใช้เลขเดิม · no-gap ✗ | FIXED | DEC-12 |
| BR-10 | approved ล็อกแก้ไขและยกเลิกไม่ได้ | FIXED | DEC-10 |
| BR-11 | ไม่เปลี่ยนค่าในระบบ · ไม่ส่งต่อระบบอื่น (fli.defect_recorded ประกาศไม่ยิง) | FIXED [AI-DEFAULT] | DEC-01 · DEC-02 |
| BR-12 | ช่องลงชื่อใน PDF = ผู้ตรวจสอบ + 1 ช่องต่อขั้นที่ตั้งใน DOA (dynamic · ห้าม fix จำนวน) · แถวละ ≤ max_per_row · คำตัดสินตาม role (role-supervisor = ตรวจสอบแล้ว/ส่งกลับแก้ไข) · ข้อความ "ส่ง/พิจารณาในระบบ" | FIXED (จำนวน = DOA) [AI-DEFAULT] | DEC-03 · DEC-09 |
| BR-13 | แนบไฟล์ระดับใบ ✓ · CSV ✓ · ทำซ้ำ ✗ · ประกาศ ✗ | FIXED [AI-DEFAULT] | DEC-13 |
| BR-DOA-01 | ส่งได้เฉพาะ draft/returned | FIXED | DOA |
| BR-DOA-02 | resolve สายตอนส่งแล้ว freeze | FIXED | DOA |
| BR-DOA-03 | reject → กลับร่าง (status returned) แก้ได้ · ประวัติ append-only (ตรงกับ DEC-10 — ไม่มีข้อยกเว้น) | FIXED | DEC-10 |
| BR-DOA-04 | ผู้ตรวจสอบ (ผู้บันทึก) พิจารณาใบตัวเองไม่ได้ | FIXED | DOA |
| BR-DOA-05 | ไม่ใช้ (ไม่มีวงเงิน DEC-03) | — | |

## §5.2 State Machine
| จาก | event | ไป | guard |
|---|---|---|---|
| — | save | draft | FN-03 ออกเลข |
| draft/returned | save results | (เดิม) | owner · VR-01..04 |
| draft/returned | submit | pending(1) | owner · assignees ครบ · ≠ owner |
| pending(n) | approve | pending(n+1) / approved | assignee ขั้น n |
| pending(n) | reject | returned | assignee ขั้น n · เหตุผล |
| draft/pending/returned | cancel | cancelled | owner / role-mgr-wh · เหตุผล |

## §5.3 Permission Matrix (DEC-11)
| Action | owner | ผู้อยู่ในสาย | role-mgr-wh | อื่น |
|---|:-:|:-:|:-:|:-:|
| ดูร่างของตน | ✓ | ✗ ไม่เห็นร่าง | ✓ | ✗ |
| ดูหลังส่ง | ✓ | ✓ | ✓ | ✗ (404) |
| บันทึกผล/แก้ | ✓ draft/returned | ✗ | ✗ | ✗ |
| ตัดสิน | ✗ | ขั้นปัจจุบันเท่านั้น | ขั้นของตน | ✗ |
| ยกเลิก | ✓ | ✗ | ✓ | ✗ |

## §5.4 Validation Rules
| VR | ช่อง | เงื่อนไข | ข้อความ | ผูก |
|---|---|---|---|---|
| VR-01 | vehicle_type | required | เลือกประเภทรถ | DEC-14 |
| VR-02 | inspection_month | required · ≤ เดือนปัจจุบัน | เลือกเดือนปัจจุบันหรือเดือนก่อนหน้า | DEC-15 |
| VR-03 | results | วันที่มีผลต้องครบทุกรายการ · day ≤ วันสุดท้ายที่กรอกได้ | วันที่ … กรอกผลไม่ครบทุกรายการ | DEC-04 · DEC-15 |
| VR-04 | results | ≥1 วันครบ | บันทึกผลตรวจอย่างน้อย 1 วัน | DEC-04 |
| VR-05 | slot ผู้พิจารณา | ครบทุกขั้น · ≠ owner | กรุณาเลือกผู้พิจารณา | BR-DOA-04 |
| VR-06 | เหตุผล ส่งกลับ/ยกเลิก | required | กรุณาระบุเหตุผล | DEC-10 |

## §5.5 Edge Cases
| EC | กรณี | ผล | ผูก |
|---|---|---|---|
| EC-01 | เดือนสั้น (ก.พ./เดือน 30 วัน) | ปุ่มวันตามจริง · PDF คอลัมน์ที่เกินเว้นว่าง | DEC-15 |
| EC-02 | เดือนปัจจุบัน | วันหลังวันนี้ disabled · API 422 DAY_OUT_OF_RANGE | DEC-15 |
| EC-03 | เปลี่ยนประเภทรถหลังกรอก | ล้างส่วนเฉพาะเดิม + toast เตือน | DEC-14 |
| EC-04 | กรอกบางรายการของวัน | บล็อก + เลื่อนไปวันที่ไม่ครบ + แถวแดง | VR-03 |
| EC-05 | ผู้ตรวจสอบ = หัวหน้างานเอง | slot ว่าง ต้องเลือกคนอื่น | BR-DOA-04 |
| EC-06 | แก้ DOA ระหว่างรอตรวจ | ใช้สาย snapshot | BR-DOA-02 |
| EC-07 | stale | 409 → toast รีเฟรช | |
| EC-08 | doc_type ปิดใช้ | ปุ่มสร้าง disabled | DEC-12 |
| EC-09 | config รายการตรวจเปลี่ยนกลางเดือน | ใบเดิมใช้ checklist_snapshot | BR-01 |
| EC-10 | รถหลายคันประเภทเดียวกัน | หลายใบได้ · ไม่มีหมายเลขรถ | DEC-17 |

## §5.6 Notification (NTF_BRIEF_F-TMP-002)
| Event | Trigger | ผู้รับ | ช่องทาง | ปิดได้ |
|---|---|---|---|---|
| fli_defect_found | บันทึกผลที่ ng เพิ่ม (FN-04 → FN-10) | หัวหน้างานตรวจสอบ (role-supervisor) | in-app+email | ✗ บังคับ |
| fli_cancelled | pending → cancelled (FN-08) | ผู้อนุมัติขั้นปัจจุบัน | in-app | ✓ |
DOA engine เป็นเจ้าของ doa_pending · doa_result · doa_escalate
