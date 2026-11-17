# 05_RULES — F-TMP-002

## §5.1 Business Rules
| ID | Rule | Tag | อ้าง |
|---|---|:-:|---|
| BR-01 | รวมต่อแถว = ผลรวมจำนวนทุกระดับ (c5…c1 ตามระดับใน config csat_scale) | FIXED | FN-02 |
| BR-02 | แถว "รวม" ครบทุกคอลัมน์ระดับ + รวมทั้งหมด (ต้นฉบับขาดบางคอลัมน์) | FIXED | DEC-16 · DEC-17 |
| BR-03 | % ต่อด้าน = Σ (จำนวน × น้ำหนักจาก config csat_scale) ÷ (น้ำหนักสูงสุด × รวม) × 100 · ROUND_HALF_UP 2 ตำแหน่ง · รวม = 0 → ไม่คำนวณ ("—") | CONFIGURABLE | DEC-04 · DEC-18 |
| BR-04 | % โดยรวม = ถ่วงตามจำนวนคำตอบรวมทุกด้าน (ไม่ใช่เฉลี่ย % ด้าน) | CONFIGURABLE | DEC-19 (AI-DEFAULT) |
| BR-05 | ข้อความแปลผลตามช่วงใน config csat_bands | CONFIGURABLE | DEC-04 · DEC-19 |
| BR-06 | เกณฑ์ลูกค้าที่ประเมินอ่านจาก config csat_min_orders_per_month · ต่ำกว่าเกณฑ์ = เตือน ไม่บล็อก | CONFIGURABLE | DEC-20 |
| BR-07 | หัวข้อ/ระดับอ่านจาก config · snapshot ลงเอกสาร (เปลี่ยน config ไม่กระทบใบเดิม) | CONFIGURABLE | DEC-04 · DEC-05..07 |
| BR-08 | สายอนุมัติ resolve จาก DOA ตอนส่ง แล้ว freeze | FIXED | BR-DOA-02 · DEC-03 |
| BR-09 | ไม่อนุมัติ → draft เลขเดิม (ตาม BR-DOA-03 มาตรฐาน — ไม่ใช่จบใบ) · resolve ใหม่ตอนส่งรอบถัดไป | FIXED | DEC-11 |
| BR-10 | ออกเลขตอนบันทึกครั้งแรก · no-gap ✗ | CONFIGURABLE | DEC-13 (F-DOCCFG) |
| BR-11 | ร่างเห็นเฉพาะเจ้าของ + Sales admin | FIXED | DEC-12 |
| BR-12 | ช่องลงชื่อ PDF = ผู้จัดทำ + 1 ช่องต่อขั้น DOA (dynamic) · แถวละ ≤ print_config max_per_row | FIXED (จำนวน = DOA) | DEC-03 · DEC-10 |
| BR-13 | อนุมัติขั้นสุดท้าย และ overall_pct < ช่วงกลางใน config → csm_low_csat | CONFIGURABLE | NTF |
| BR-14 | รหัสฟอร์มในแบบพิมพ์ = FM-SAL-11 (print_config) | FIXED | DEC-15 |
| BR-15 | ไม่เปลี่ยนค่าในระบบ · ไม่ส่งต่อระบบอื่น · csm.approved ประกาศไม่ยิง | FIXED | DEC-01 · DEC-02 |
| BR-16 | ช่องตรงกระดาษ 1:1 ไม่เพิ่มช่อง · แนบไฟล์/CSV เป็นของเสริม · ไม่มีทำซ้ำ/ประกาศ | FIXED | DEC-09 · DEC-14 |
| BR-17 | PDF รายชื่อลูกค้าอย่างน้อยตาม print_config.min_rows · ไม่จำกัดจำนวน (dense เมื่อเกิน) | CONFIGURABLE | DEC-08 |

## §5.2 State Machine
| จาก | Action | ไป | ใคร | FN |
|---|---|---|---|---|
| — | บันทึกครั้งแรก | draft | Maker | FN-03 |
| draft | ส่ง | pending | Maker | FN-05 |
| pending | อนุมัติขั้น n<N | pending | ผู้พิจารณาขั้น n | FN-06 |
| pending | อนุมัติขั้น N | approved | ขั้น N | FN-06 |
| pending | ไม่อนุมัติ | draft (เลขเดิม) | ผู้พิจารณาขั้นปัจจุบัน | FN-07 |
| draft / pending | ยกเลิก | cancelled | Maker / Sales admin | FN-07 |

## §5.3 Permission Matrix
| Action | Maker (ของตน) | Approver (ในสาย) | Sales admin | คนอื่น |
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
| VR-02 | c5..c1 | จำนวนเต็ม ≥ 0 (ว่าง = 0) — บล็อก | ใส่เป็นจำนวนเต็ม 0 ขึ้นไป (จำนวนลูกค้า) |
| VR-03 | lines | Σ ทั้งเอกสาร > 0 | กรอกคะแนนอย่างน้อย 1 ด้าน |
| VR-04 | customers | ≥ 1 · ทุกแถวเลือก · ไม่ซ้ำ | เลือกลูกค้า / ลูกค้าซ้ำกับแถวที่ n |
| VR-05 | assignees | ครบทุกขั้น · ≠ ผู้จัดทำ | กรุณาเลือกผู้พิจารณา |
| VR-06 | reason | required (ไม่อนุมัติ/ยกเลิก) | กรุณาระบุเหตุผล |

## §5.5 Edge Cases
| EC | กรณี | ผล | อ้าง |
|---|---|---|---|
| EC-01 | ด้านใดรวม = 0 | % "—" ไม่นับในโดยรวม | DEC-18 |
| EC-02 | ทุกด้านว่าง | บล็อก VR-03 | DEC-04 |
| EC-03 | ค่าติดลบ/ทศนิยม/ตัวอักษร | บล็อก VR-02 | DEC-04 |
| EC-04 | ลูกค้าสั่งซื้อต่ำกว่าเกณฑ์ config | ป้ายเตือน · ส่งได้ | DEC-20 |
| EC-05 | ลูกค้าเกิน min_rows ใน PDF | dense · 2 หน้าเท่าเดิม | DEC-08 |
| EC-06 | สร้างซ้ำเดือนเดียวกัน | ไม่บล็อก (OQ-06) | — |
| EC-07 | แก้ DOA ระหว่างรออนุมัติ | ใช้ snapshot | BR-08 |
| EC-08 | แก้หัวข้อใน config หลังออกเอกสาร | ใบเดิมใช้ snapshot | BR-07 |
| EC-09 | stale version | 409 → รีเฟรช | API |
| EC-10 | F-DOCCFG ปิดใช้ | สร้างไม่ได้ (409) | FN-03 |
| EC-11 | ข้อความสรุป % ในต้นฉบับพิมพ์ตายตัว | คำนวณเสมอ | DEC-19 |
