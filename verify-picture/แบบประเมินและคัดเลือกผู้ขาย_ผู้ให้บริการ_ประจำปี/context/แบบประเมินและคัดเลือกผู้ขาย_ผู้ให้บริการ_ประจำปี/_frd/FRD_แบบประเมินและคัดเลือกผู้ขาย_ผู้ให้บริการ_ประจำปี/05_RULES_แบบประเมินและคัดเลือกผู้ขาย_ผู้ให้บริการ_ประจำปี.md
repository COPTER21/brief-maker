# 05_RULES — F-TMP-004

## §5.1 Business Rules
| ID | Rule | Tag | ที่มา |
|---|---|---|---|
| BR-01 | หัวข้อ + เกณฑ์ย่อย + คะแนนเต็ม อ่านจาก VendorEvaluationConfig แล้ว snapshot ลงใบ | CONFIGURABLE [AI-DEFAULT] | DEC-04 |
| BR-02 | คะแนนที่ได้ 0..คะแนนเต็มของหัวข้อ ทศนิยม ≤1 · เกิน/ผิดรูปแบบ = บล็อก | FIXED | DEC-12 · DEC-15 (VALID) |
| BR-03 | ส่งได้เมื่อคะแนนครบทุกหัวข้อ · ร่างไม่บังคับครบ | FIXED | DEC-15 (VALID) |
| BR-04 | คะแนนรวม = Σ คะแนนที่ได้ · สรุปผล = รวม < pass_threshold ? ไม่ผ่าน : ผ่าน — คำนวณที่ server ผู้ใช้แก้ไม่ได้ | FIXED (เกณฑ์ CONFIGURABLE) | DEC-04 · DEC-13 |
| BR-05 | ผลไม่ผ่าน → สายอนุมัติเพิ่มขั้นผู้บริหาร (role-gm) ตามเงื่อนไขที่ DOA กลาง — TODO: DOA engine · ห้าม hardcode | CONFIGURABLE [AI-DEFAULT role] | DEC-14 (VALID) |
| BR-06 | ส่งใบที่ผลไม่ผ่าน → vev_evaluation_failed ถึง role-mgr-pur + role-gm | CONFIGURABLE | DEC-14 · NTF |
| BR-07 | เลือกสินค้า และ/หรือ บริการ ≥1 · เลือกแล้วต้องระบุ · ยกเลิกประเภท = ล้างรายละเอียด | FIXED [AI-DEFAULT] | DEC-04 |
| BR-08 | มาตรฐานจาก config (8 ตัวเลือก) · อื่นๆ ต้องระบุ | CONFIGURABLE [AI-DEFAULT] | DEC-04 |
| BR-09 | ผู้ขายรหัสเดียวกัน ปีเดียวกัน (ไม่นับยกเลิก) → เตือน ไม่บล็อก | FIXED [AI-DEFAULT] | DEC-04 |
| BR-10 | ช่องตามกระดาษ 1:1 ไม่เพิ่มช่อง · คงคำ "คะแนนเฉลี่ย" · แก้สะกด 5 คำ | FIXED [AI-DEFAULT] | DEC-06 · DEC-16 |
| BR-11 | เลขออกตอนบันทึกครั้งแรก · ส่งกลับใช้เลขเดิม · no-gap ✗ | FIXED | DEC-10 |
| BR-12 | approved ล็อกแก้ไขและยกเลิกไม่ได้ | FIXED | DEC-08 |
| BR-13 | ไม่เปลี่ยนค่าในระบบ · ไม่ส่งต่อระบบอื่น (vev.evaluation_approved ประกาศไม่ยิง) | FIXED [AI-DEFAULT] | DEC-01 · DEC-02 |
| BR-14 | ช่องลงชื่อใน PDF = ผู้ประเมิน + 1 ช่องต่อขั้นที่ตั้งใน DOA (dynamic · ห้าม fix จำนวน) · แถวละ ≤ max_per_row · คำตัดสินตาม role (role-pur-officer = เห็นด้วย/ไม่เห็นด้วย · role-mgr-pur/role-gm = อนุมัติ/ไม่อนุมัติ) · ข้อความ "ส่ง/พิจารณาในระบบ" | FIXED (จำนวน = DOA) [AI-DEFAULT] | DEC-03 · DEC-07 |
| BR-15 | แนบไฟล์ระดับใบ ✓ · CSV ✓ · ทำซ้ำ ✗ · ประกาศ ✗ | FIXED [AI-DEFAULT] | DEC-11 |
| BR-DOA-01 | ส่งได้เฉพาะ draft/returned | FIXED | DOA |
| BR-DOA-02 | resolve สายตอนส่งแล้ว freeze | FIXED | DOA |
| BR-DOA-03 | reject → กลับร่าง (status returned) แก้ได้ · ประวัติ append-only (ตรงกับ DEC-08 — ไม่มีข้อยกเว้น) | FIXED | DEC-08 |
| BR-DOA-04 | ผู้ประเมิน (ผู้ส่ง) พิจารณาใบตัวเองไม่ได้ | FIXED | DOA |
| BR-DOA-05 | ไม่ใช้ (ไม่มีวงเงิน DEC-03) | — | |

## §5.2 State Machine
| จาก | event | ไป | guard |
|---|---|---|---|
| — | save | draft | FN-03 ออกเลข · ชื่อ/รหัสผู้ขาย |
| draft/returned | save | (เดิม) | owner · VR-01/02/06/07/08 |
| draft/returned | submit | pending(1) | owner · VR ครบ · assignees ครบ · ≠ owner |
| pending(n) | approve | pending(n+1) / approved | assignee ขั้น n |
| pending(n) | reject | returned | assignee ขั้น n · เหตุผล |
| draft/pending/returned | cancel | cancelled | owner / role-mgr-pur · เหตุผล |

## §5.3 Permission Matrix (DEC-09)
| Action | owner | ผู้อยู่ในสาย | role-mgr-pur | อื่น |
|---|:-:|:-:|:-:|:-:|
| ดูร่างของตน | ✓ | ✗ ไม่เห็นร่าง | ✓ | ✗ |
| ดูหลังส่ง | ✓ | ✓ | ✓ | ✗ (404) |
| แก้ไข | ✓ draft/returned | ✗ | ✗ | ✗ |
| ตัดสิน | ✗ | ขั้นปัจจุบันเท่านั้น | ขั้นของตน | ✗ |
| ยกเลิก | ✓ | ✗ | ✓ | ✗ |

## §5.4 Validation Rules
| VR | ช่อง | เงื่อนไข | ข้อความ | ผูก |
|---|---|---|---|---|
| VR-01 | vendor_name | required | กรุณากรอกข้อมูล | DEC-04 |
| VR-02 | vendor_code | required | กรุณากรอกข้อมูล | DEC-04 |
| VR-03 | supply_goods/supply_service | ≥1 (ตอนส่ง) | เลือกสินค้า และ/หรือ บริการ อย่างน้อย 1 | DEC-04 |
| VR-04 | goods_specific / service_specific | required เมื่อเลือก | กรุณากรอกข้อมูล | DEC-04 |
| VR-05 | scores[i] | required ตอนส่ง | กรอกคะแนน | DEC-15 |
| VR-06 | scores[i] | ตัวเลข ทศนิยม ≤1 | ตัวเลข ทศนิยมไม่เกิน 1 ตำแหน่ง | DEC-15 |
| VR-07 | scores[i] | ≤ max_score | เกินคะแนนเต็ม {max} | DEC-12 |
| VR-08 | cert_other_text | required เมื่อเลือก อื่นๆ | ระบุชื่อมาตรฐาน | DEC-04 |
| VR-09 | slot ผู้พิจารณา | ครบทุกขั้น · ≠ owner | กรุณาเลือกผู้พิจารณา | BR-DOA-04 |
| VR-10 | เหตุผล ไม่เห็นด้วย/ไม่อนุมัติ/ยกเลิก | required | กรุณาระบุเหตุผล | DEC-08 |

## §5.5 Edge Cases
| EC | กรณี | ผล | ผูก |
|---|---|---|---|
| EC-01 | คะแนนรวม = 6 พอดี | ผ่าน | DEC-13 |
| EC-02 | คะแนนรวม 5.9 | ไม่ผ่าน + ขั้นผู้บริหาร + แจ้ง | DEC-13/14 |
| EC-03 | 3.5 ในหัวข้อเต็ม 3 · 2.25 · "ก" | บล็อก + แถวแดง | VR-06/07 |
| EC-04 | ส่งกลับจากไม่ผ่าน → แก้คะแนนเป็นผ่าน | ส่งใหม่ resolve 2 ขั้น | FN-07 |
| EC-05 | กดส่งร่างที่คะแนนไม่ครบจากหน้าดู | toast + เปิดแก้ไข · API 422 SCORE_INCOMPLETE | BR-03 |
| EC-06 | ผู้ประเมินคือผู้ที่ resolve เป็นผู้จัดทำ | resolve คนอื่น · slot ไม่มีตัวเอง | BR-DOA-04 |
| EC-07 | แก้ DOA ระหว่างรออนุมัติ | ใช้สาย snapshot | BR-DOA-02 |
| EC-08 | stale | 409 → toast รีเฟรช | |
| EC-09 | doc_type ปิดใช้ | ปุ่มสร้าง disabled | DEC-10 |
| EC-10 | config เกณฑ์เปลี่ยนกลางปี | ใบเดิมใช้ criteria_snapshot | BR-01 |
| EC-11 | ผู้ขายเดียวกันประเมินซ้ำในปี | เตือน ไม่บล็อก | BR-09 |
| EC-12 | ยกเลิกประเภทที่เลือกไว้ | ล้างรายละเอียดประเภทนั้น | BR-07 |

## §5.6 Notification (NTF_BRIEF_F-TMP-004)
| Event | Trigger | ผู้รับ | ช่องทาง | ปิดได้ |
|---|---|---|---|---|
| vev_evaluation_failed | ส่งใบที่ eval_result=fail (FN-05 → FN-10) | ผู้จัดการแผนกจัดซื้อ (role-mgr-pur) · ผู้บริหาร (role-gm) | in-app+email | ✗ บังคับ |
| vev_cancelled | pending → cancelled (FN-08) | ผู้อนุมัติขั้นปัจจุบัน | in-app | ✓ |
DOA engine เป็นเจ้าของ doa_pending · doa_result · doa_escalate
