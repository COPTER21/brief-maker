# 05_RULES — F-TMP-008

## §5.1 Business Rules
| ID | Rule | Tag | ที่มา |
|---|---|---|---|
| BR-01 | ผลการรับมอบ / ได้รับแล้ว / ความครบถ้วน อ่านจาก HandoverConfig เท่านั้น | CONFIGURABLE | DEC-04 |
| BR-02 | ผลการรับมอบ = รับมอบครบถ้วน ได้เมื่อทุกแถว ได้รับ + ครบถ้วน (บังคับ) | FIXED | DEC-12 (VALID) |
| BR-03 | แถว ไม่ได้รับ → ความครบถ้วน ≠ ครบถ้วน | FIXED | DEC-13 (VALID) |
| BR-04 | แถวไม่ผ่าน ต้องมี ประเด็นที่พบ + ผู้รับผิดชอบแก้ไข + กำหนดส่งเพิ่มเติม | FIXED | DEC-14 (VALID) |
| BR-05 | กำหนดส่งเพิ่มเติม / กำหนดการติดตาม ≥ วันที่รับมอบ · วันที่รับมอบ ≤ วันนี้ | FIXED | DEC-15 (VALID) |
| BR-06 | ผลการรับมอบ ≠ รับมอบครบถ้วน → ประเด็นค้างจากการรับมอบ บังคับ | FIXED | DEC-16 (VALID) |
| BR-07 | ช่องตรงกระดาษ 1:1 · ไม่เพิ่มช่องอ้าง FM-BDM-07/โครงการ (เสนอเป็นคำถามลูกค้าใน 00 §0.8) | FIXED [AI-DEFAULT] | DEC-06 · DEC-17 (VALID) |
| BR-08 | แถวตรวจรับไม่จำกัด · PDF แสดงอย่างน้อยตาม print_config.min_rows (12) | FIXED [AI-DEFAULT] | DEC-05 |
| BR-DOA-01 | ส่งอนุมัติได้เฉพาะ draft | FIXED | DOA |
| BR-DOA-02 | resolve สายตอนส่งแล้ว freeze | FIXED | DOA |
| BR-DOA-03 | reject → กลับ draft แก้ได้ · ประวัติ append-only (ตรงกับ DEC-08 — ไม่มีข้อยกเว้น) | FIXED | DEC-08 |
| BR-DOA-04 | ผู้จัดทำพิจารณาใบตัวเองไม่ได้ | FIXED | DOA |
| BR-DOA-05 | ไม่ใช้ (ไม่มีวงเงิน DEC-03) | — | |
| BR-09 | เลขออกตอนบันทึกครั้งแรก · กลับร่างใช้เลขเดิม | FIXED | DEC-10 |
| BR-10 | approved ล็อกแก้ไขและยกเลิกไม่ได้ | FIXED | DEC-08 |
| BR-11 | ตารางลงชื่อใน PDF = ผู้จัดทำ + 1 แถวต่อขั้นที่ตั้งใน DOA (dynamic · ห้าม fix จำนวน) · คำตัดสินตาม role (print_config) · บล็อกลงชื่อไม่ถูกตัดข้ามหน้า | FIXED (จำนวน = DOA) | DEC-03 · DEC-07 |
| BR-12 | แบบพิมพ์ 2 หน้าทุกสถานะ (thai-doc R10) · หัวตารางซ้ำ · "หน้า N/2" | FIXED | DEC-05 |
| BR-13 | มองเห็น: เจ้าของ · ผู้อนุมัติหลังส่ง · admin_role ฝ่ายบริหารการลงทุนเห็นทั้งหมด | FIXED [AI-DEFAULT] | DEC-09 |
| BR-14 | ไม่เปลี่ยนค่าในระบบ ไม่ส่งต่อระบบอื่น · แนบไฟล์ ✓ CSV ✓ ทำซ้ำ ✗ ประกาศ ✗ | FIXED [AI-DEFAULT] | DEC-01 · DEC-02 · DEC-11 |
| BR-15 | รับทราบแล้วและยังมีแถวไม่ผ่าน → แจ้งผู้จัดทำ (hoi_acknowledged_open_items) | CONFIGURABLE [AI-DEFAULT] | DEC-04 · DEC-14 |
| BR-16 | เวลารับมอบรูปแบบ HH:MM (24 ชม.) | FIXED | FORM_SPEC F04 |

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
| VR-01 | handover project_name · sender · receiver · package_version · result | required | กรุณาระบุชื่อโครงการ / ผู้ส่งมอบ / ผู้รับมอบ / ฉบับชุดเอกสาร · กรุณาเลือกผลการรับมอบ |
| VR-02 | handover received_at | วันที่ required ≤ วันนี้ · เวลา HH:MM | กรุณาระบุวันที่และเวลา (รูปแบบ 10:30) |
| VR-03 | items[] doc_name · received · completeness | ≥1 แถว · required ทุกแถว | กรอกชื่อเอกสาร ได้รับแล้ว และความครบถ้วนให้ครบทุกรายการ |
| VR-04 | items[] completeness | received = ไม่ได้รับ → ≠ ครบถ้วน | รายการที่ "ไม่ได้รับ" เลือกความครบถ้วนเป็น "ครบถ้วน" ไม่ได้ |
| VR-05 | items[] issue · fix_owner · due_date | required เมื่อแถวไม่ผ่าน | รายการที่ไม่ได้รับหรือไม่ครบถ้วน ต้องระบุประเด็นที่พบ ผู้รับผิดชอบแก้ไข และกำหนดส่งเพิ่มเติม |
| VR-06 | items[] due_date · followup_date | ≥ received_at | กำหนดส่งเพิ่มเติมต้องไม่ก่อนวันที่รับมอบ · กำหนดการติดตามต้องไม่ก่อนวันที่รับมอบ |
| VR-07 | handover result | = รับมอบครบถ้วน ได้เมื่อทุกแถวผ่าน | มีเอกสารไม่ได้รับหรือไม่ครบถ้วน — เลือก "รับมอบแบบมีเงื่อนไข" หรือ "ยังไม่รับมอบ" |
| VR-08 | followup open_issues | required เมื่อ result ≠ รับมอบครบถ้วน | กรุณาระบุประเด็นค้างจากการรับมอบ |
| VR-09 | assignees | ครบทุกขั้น · ≠ ผู้จัดทำ | กรุณาเลือกผู้พิจารณา |
| VR-10 | reason (reject/cancel) | required | กรุณาระบุเหตุผล |

## §5.5 Edge Cases
| EC | กรณี | ผล | อ้าง |
|---|---|---|---|
| EC-01 | เปลี่ยนแถวเป็นไม่ได้รับขณะผลการรับมอบ = รับมอบครบถ้วน | บล็อกตอนถัดไป · ช่องผลการรับมอบแดง | DEC-12 |
| EC-02 | ผลการรับมอบ = ยังไม่รับมอบ | ประเด็นค้างบังคับ · ส่งได้ | DEC-16 |
| EC-03 | > rows_page1 แถวตรวจรับ (ทดสอบ 24 แถว) | PDF หน้า 2 ต่อตาราง หัวซ้ำ · ยัง 2 หน้า | DEC-05 |
| EC-04 | ผู้จัดทำเป็นผู้จัดการเอง | slot ขั้น 1 ว่าง ต้องเลือกคนอื่น | BR-DOA-04 |
| EC-05 | DOA แก้ระหว่างรอ | ใช้ snapshot | BR-DOA-02 |
| EC-06 | ตัดสินชนกัน | 409 STALE สถานะไม่เปลี่ยน | |
| EC-07 | doc_type ปิดใช้ | สร้างไม่ได้ 409 DOC_TYPE_INACTIVE | DEC-10 |
| EC-08 | เลื่อนวันที่รับมอบหลังกำหนดส่งที่กรอกแล้ว | บล็อก VR-06 | DEC-15 |
| EC-09 | DOA 6 ขั้น | PDF ลงชื่อ 7 แถว dense · ยัง 2 หน้า | BR-11 |
| EC-10 | เวลาไม่ใช่รูปแบบ HH:MM (เช่น 25:00 · 1030) | บล็อก VR-02 | BR-16 |
| EC-11 | ใบนี้คู่กับ FM-BDM-07 แต่ไม่มีช่องอ้าง | ไม่ตรวจรอบนี้ → คำถามลูกค้า (00 §0.8) | DEC-17 |

## §5.6 Error Catalog
NOT_FOUND 404 · NOT_OWNER 403 · NOT_CURRENT_APPROVER 403 · NOT_DRAFT 409 · NOT_CANCELLABLE 409 · STALE 409 · DOC_TYPE_INACTIVE 409 · ASSIGNEE_REQUIRED 422 · SELF_APPROVAL 422 · REASON_REQUIRED 422 · VALIDATION 422

## §5.7 Security
SoD · จำนวนค้างส่ง/กฎ DEC-12..16 คิดฝั่ง server · audit append-only · PII ชื่อ snapshot

## §5.8 Notifications (NTF_BRIEF)
hoi_cancelled · hoi_acknowledged_open_items — ดู 03 FN-09
