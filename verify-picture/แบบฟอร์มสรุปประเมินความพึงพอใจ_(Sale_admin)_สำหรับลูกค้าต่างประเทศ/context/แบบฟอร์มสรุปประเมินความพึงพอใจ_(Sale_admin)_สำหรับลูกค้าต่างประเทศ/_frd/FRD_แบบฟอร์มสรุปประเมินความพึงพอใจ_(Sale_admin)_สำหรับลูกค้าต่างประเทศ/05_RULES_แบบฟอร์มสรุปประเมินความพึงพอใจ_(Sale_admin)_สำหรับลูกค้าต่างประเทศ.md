# 05_RULES — F-TMP-007

## §5.1 Business Rules
| ID | Rule | Tag | อ้าง |
|---|---|:-:|---|
| BR-01 | คอลัมน์ = แบบประเมิน SEA สถานะ recorded ของลูกค้าในเดือนที่เลือก · คะแนนอ่านอย่างเดียว (แก้ที่ SEA ต้นทาง) | FIXED | DEC-01 · DEC-04 |
| BR-02 | ลูกค้าซ้ำในใบเดียวกัน = บล็อก · หลายใบในเดือน = ใบล่าสุด + เตือน | FIXED | DEC-14 |
| BR-03 | ลูกค้าสูงสุดต่อใบอ่านจาก config ses_max_customers (8) · เกิน = บล็อก · แจ้งให้ทำใบสรุปเพิ่ม | CONFIGURABLE | DEC-05 |
| BR-04 | หัวข้อ 10 ข้อ (3 กลุ่ม) (SalesConfig.sea_topics) จับคู่ q1–q10 · ถ้อยคำตามกระดาษ FM-SAL-23 · snapshot ลงเอกสาร | CONFIGURABLE | DEC-04 · DEC-13 |
| BR-05 | คะแนน (SalesConfig.sea_scale weight 1–5) แสดงเป็นตัวเลข · weight ≤ เกณฑ์คะแนนต่ำใน config (2) = ไฮไลต์เตือน ไม่บล็อก | CONFIGURABLE | DEC-04 |
| BR-06 | ร่างเก็บ snapshot ค่าที่ดึง · SEA ถูกยกเลิกหลังดึง = เตือน + ส่งไม่ได้จนเอาคอลัมน์ออก · ใบที่ส่งแล้วไม่เปลี่ยนตาม SEA | FIXED | DEC-04 |
| BR-07 | สรุปผลการประเมินบังคับตอนส่ง · ข้อเสนอแนะไม่บังคับ · ยาวไม่เกิน 1,000 | FIXED | DEC-04 |
| BR-08 | สายพิจารณา resolve จาก DOA ตอนส่ง แล้ว freeze | FIXED | BR-DOA-02 · DEC-03 |
| BR-09 | ไม่ผ่านการพิจารณา → draft เลขเดิม (BR-DOA-03) · resolve ใหม่ตอนส่งรอบถัดไป | FIXED | DEC-08 |
| BR-10 | ออกเลขตอนบันทึกครั้งแรก · no-gap ✗ | CONFIGURABLE | DEC-10 (F-DOCCFG) |
| BR-11 | ร่างเห็นเฉพาะเจ้าของ + role-mgr-sales | FIXED | DEC-09 |
| BR-12 | ช่องลงชื่อ PDF = ผู้สรุป + 1 ช่องต่อขั้น DOA (dynamic) · แถวละ ≤ print_config max_per_row · เส้นลงชื่อเท่ากัน | FIXED (จำนวน = DOA) | DEC-03 · DEC-07 · DEC-15 |
| BR-13 | ปิดใบขั้นสุดท้าย และมีช่องคะแนนต่ำ → ses_low_score_approved | CONFIGURABLE | NTF |
| BR-14 | ไม่เปลี่ยนค่าในระบบ · ไม่ส่งต่อระบบอื่น · ses.approved ประกาศไม่ยิง · แนบไฟล์/CSV เป็นของเสริม · ไม่มีทำซ้ำ/ประกาศ | FIXED | DEC-01 · DEC-02 · DEC-11 |
| BR-15 | ช่องตามกระดาษ + ประจำเดือน (บังคับ) · หัวข้อ/กลุ่ม/สเกลอ่านจาก config (SalesConfig.sea_topics[] / sea_topic_groups[] / sea_scale[]) | FIXED | DEC-06 · DEC-12 · DEC-13 |

## §5.2 State Machine
| จาก | Action | ไป | ใคร | FN |
|---|---|---|---|---|
| — | บันทึกครั้งแรก | draft | Maker | FN-03 |
| draft | ส่ง | pending | Maker | FN-04 |
| pending | ผ่านขั้น n<N | pending | ผู้พิจารณาขั้น n | FN-05 |
| pending | ผ่านขั้น N | approved | ขั้น N | FN-05 |
| pending | ไม่ผ่าน | draft (เลขเดิม) | ผู้พิจารณาขั้นปัจจุบัน | FN-06 |
| draft / pending | ยกเลิก | cancelled | Maker / role-mgr-sales | FN-06 |

## §5.3 Permission Matrix
| Action | Maker (ของตน) | ผู้พิจารณา (ในสาย) | role-mgr-sales | คนอื่น |
|---|:-:|:-:|:-:|:-:|
| ดู draft | ✓ | ✗ | ✓ | ✗ (404) |
| ดู pending/approved/cancelled | ✓ | ✓ | ✓ | ✗ (404) |
| สร้าง/แก้ร่าง | ✓ | ✗ | ✗ | ✗ |
| ส่ง | ✓ | ✗ | ✗ | ✗ |
| ตัดสินขั้น | ✗ (SoD) | ✓ เฉพาะขั้นปัจจุบัน | ✗ | ✗ |
| ยกเลิก | ✓ (draft/pending) | ✗ | ✓ (draft/pending) | ✗ |

## §5.4 Validation
| VR | ช่อง | เงื่อนไข | ข้อความ |
|---|---|---|---|
| VR-01 | period_month | required | กรุณาเลือกเดือน |
| VR-02 | columns | ≥ 1 | เพิ่มลูกค้าที่ประเมินอย่างน้อย 1 ราย |
| VR-03 | columns.customer_id | ไม่ซ้ำ | ลูกค้านี้อยู่ในใบสรุปแล้ว |
| VR-04 | columns | ≤ ses_max_customers (8) | ใบสรุป 1 ใบมีลูกค้าได้สูงสุด 8 ราย — ทำใบสรุปเพิ่ม |
| VR-05 | conclusion | required ตอนส่ง · ≤ 1000 | กรุณาเขียนสรุปผลการประเมิน |
| VR-06 | assignees | ครบทุกขั้น · ≠ ผู้สรุป | กรุณาเลือกผู้พิจารณา |
| VR-07 | reason | required (ไม่ผ่าน/ยกเลิก) | กรุณาระบุเหตุผล |

## §5.5 Edge Cases
| EC | กรณี | ผล | อ้าง |
|---|---|---|---|
| EC-01 | เดือนไม่มี SEA บันทึกผลแล้ว | ดึงแล้ว "ไม่มีลูกค้าเพิ่ม" · ส่งไม่ได้ (VR-02) | DEC-04 |
| EC-02 | ลูกค้ามี SEA > 8 ราย | ดึง 8 · แจ้งที่เหลือ | DEC-05 |
| EC-03 | ลูกค้ามี SEA 2 ใบในเดือน | ใบล่าสุด + เตือน | DEC-14 |
| EC-04 | SEA ถูกยกเลิกหลังดึงเข้าร่าง | banner + 422 SOURCE_SURVEY_CANCELLED ตอนส่ง | BR-06 |
| EC-05 | เปลี่ยนเดือนหลังดึง | ล้างคอลัมน์เดิม + แจ้ง | DEC-12 |
| EC-06 | สร้างซ้ำเดือนเดียวกัน | ไม่บล็อก (OQ-06) | — |
| EC-07 | แก้ DOA ระหว่างรอพิจารณา | ใช้ snapshot | BR-08 |
| EC-08 | แก้หัวข้อ/สเกลใน config หลังออกเอกสาร | ใบเดิมใช้ snapshot | BR-04 |
| EC-09 | stale version | 409 → รีเฟรช | API |
| EC-10 | F-DOCCFG ปิดใช้ | สร้างไม่ได้ (409) | FN-03 |
| EC-11 | DOA 6 ขั้น | ช่องลงชื่อ 7 ช่อง (4+3) หน้า 2 | BR-12 |
| EC-12 | สรุป/ข้อเสนอแนะยาวเต็ม 1,000 | PDF ยัง 2 หน้า | BR-07 |
