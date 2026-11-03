# 05_RULES — F-TMP-001

## §5.1 Business Rules
| ID | Rule | Tag | ที่มา |
|---|---|---|---|
| BR-01 | ชื่อบริษัท (หัวเรื่อง + ข้อ 2) = Organization.legal_name จาก header_snapshot ณ ออกเลข · ไม่พิมพ์ตายตัว | CONFIGURABLE [AI-DEFAULT] | DEC-04 · DEC-11 (VALID) |
| BR-02 | ประเภทธุรกิจ / ระยะเวลา เลือกได้ 1 ตัว · ระยะเวลาตีความ 1–<3 / 3–5 / >5 ปี (คำบนกระดาษคงเดิม) | FIXED | DEC-12 (VALID) |
| BR-03 | คะแนนจำนวนเต็ม 1–5 · ครบ 9 หัวข้อก่อนส่ง · ร่างไม่บังคับ | FIXED | DEC-13 (VALID) |
| BR-04 | ไม่มีสายพิจารณา: ส่งแล้ว = submitted (เสร็จ) · แก้ไม่ได้ | FIXED [AI-DEFAULT] | DEC-03 |
| BR-05 | ออกเลขตอนบันทึกครั้งแรก · no-gap ✗ | CONFIGURABLE | DEC-09 · F-DOCCFG |
| BR-06 | ร่างเห็นเฉพาะเจ้าของ (+ role-mgr-sales) · ใบของคนอื่นไม่เห็น | FIXED [AI-DEFAULT] | DEC-08 |
| BR-07 | ยกเลิก: เจ้าของ / role-mgr-sales · draft หรือ submitted · เหตุผลบังคับ | CONFIGURABLE [AI-DEFAULT] | G7 (ไม่มี DEC เพราะไม่มีสายพิจารณา) |
| BR-08 | ช่องลงชื่อ PDF = ผู้ประเมิน 1 ช่อง วนจาก sign_rows (ไม่ fix) · ข้อความ "ส่งในระบบ" ไม่ใช้ภาพ | FIXED [AI-DEFAULT] | DEC-07 |
| BR-09 | ช่องตรงกระดาษ 1:1 · ไม่เพิ่มช่อง | FIXED [AI-DEFAULT] | DEC-06 |
| BR-10 | ไม่เปลี่ยนค่าในระบบเมื่อส่ง · ไม่ส่งคะแนนต่อ CRM รอบนี้ | FIXED [AI-DEFAULT] | DEC-01 · DEC-02 |
| BR-11 | แนบไฟล์ ✓ · CSV ✓ · ทำซ้ำ ✗ · ประกาศ ✗ | FIXED [AI-DEFAULT] | DEC-10 |
| BR-12 | ไม่มีรายการซ้ำ (ตาราง 9 หัวข้อคงที่) | FIXED | DEC-05 |

## §5.2 State Machine
| จาก | event | ไป | guard |
|---|---|---|---|
| — | save | draft | FN-02 ออกเลข · VR-01 |
| draft | submit | submitted | owner · VR-01..04 · DOA resolve = 0 ขั้น |
| draft / submitted | cancel | cancelled | owner / role-mgr-sales · VR-05 |

## §5.3 Permission Matrix
| Action | owner | role-mgr-sales | อื่น |
|---|:-:|:-:|:-:|
| ดู draft | ✓ | ✓ | ✗ (ไม่เห็นร่างของคนอื่น) |
| ดู submitted / cancelled | ✓ | ✓ | ✗ |
| แก้ draft | ✓ | ✗ | ✗ |
| ส่ง | ✓ | ✗ | ✗ |
| ยกเลิก | ✓ | ✓ | ✗ |
| CSV | ของตน | ทั้งหมด | ✗ |

## §5.4 Validation
| VR | ช่อง | กฎ | ข้อความ |
|---|---|---|---|
| VR-01 | store_name | required (ร่าง+ส่ง) | กรุณาระบุชื่อห้าง/ร้านค้า |
| VR-02 | business_type | required (ส่ง) | กรุณาเลือกประเภทธุรกิจ 1 ข้อ |
| VR-03 | relationship_years | required (ส่ง) | กรุณาเลือกระยะเวลาที่ทำธุรกิจ 1 ข้อ |
| VR-04 | rating_* ×9 | 1–5 ครบ (ส่ง) | ยังไม่ได้ให้คะแนน N หัวข้อ — ต้องครบ 9 หัวข้อ (คะแนน 1–5) ก่อนส่ง |
| VR-05 | reason (cancel) | required | กรุณาระบุเหตุผล |
| VR-06 | ไฟล์แนบ | pdf/jpg/png ≤10 MB | ไฟล์ไม่ผ่านเงื่อนไข |

## §5.5 Edge Cases
| EC | กรณี | ผล | อ้าง |
|---|---|---|---|
| EC-01 | ร้านยังไม่อยู่ในทะเบียนลูกค้า | พิมพ์ชื่อเอง customer_id ว่าง | FORM_SPEC F01 |
| EC-02 | ระยะเวลา 3 ปีพอดี | เลือก 3-5 ปี | DEC-12 |
| EC-03 | คะแนนไม่ครบแล้วกดส่ง | 422 INCOMPLETE · แถวแดง | DEC-13 |
| EC-04 | ข้อเสนอแนะยาว | PDF layout.dense (ยืนยันจำนวนหน้าเมื่อ render ได้) | DEC-06 |
| EC-05 | Organization เปลี่ยนชื่อหลังออกเลข | ใช้ header_snapshot | DEC-11 |
| EC-06 | doc_type CSE ปิดใช้ | สร้างไม่ได้ 409 DOC_TYPE_INACTIVE | DEC-09 |
| EC-07 | ส่ง/ยกเลิกชนกัน | 409 STALE สถานะไม่เปลี่ยน | |
| EC-08 | DOA กลางตั้งขั้นให้ CSE ภายหลัง | นอก scope → enhancement (DOA_BRIEF) | DEC-03 |

## §5.6 Error Catalog
NOT_FOUND 404 · NOT_OWNER 403 · NOT_DRAFT 409 · NOT_CANCELLABLE 409 · STALE 409 · DOC_TYPE_INACTIVE 409 · INCOMPLETE 422 · INVALID_VALUE 422 · REASON_REQUIRED 422

## §5.7 Security
D9 Audit append-only · ไม่มี PII บนกระดาษ · RLS

## §5.8 Notifications (NTF_BRIEF)
`cse_submitted` → role-mgr-sales (in-app · ปิดได้) — ดู 03 FN-05
