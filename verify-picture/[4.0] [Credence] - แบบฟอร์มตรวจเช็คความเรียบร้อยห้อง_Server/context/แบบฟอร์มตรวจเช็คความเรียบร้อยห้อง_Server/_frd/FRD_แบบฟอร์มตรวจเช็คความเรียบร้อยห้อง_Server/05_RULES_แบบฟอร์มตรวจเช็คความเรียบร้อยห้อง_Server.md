# 05_RULES — F-TMP-002

## §5.1 Business Rules
| ID | Rule | Tag | ที่มา |
|---|---|---|---|
| BR-01 | เกณฑ์อุณหภูมิ/ความชื้นอ่านจาก ServerRoomCheckConfig (ค่าเริ่ม = หัวตารางกระดาษ) · snapshot ลงใบตอนออกเลข · หัวตาราง PDF แสดงจาก snapshot | CONFIGURABLE | DEC-04 |
| BR-02 | แถวผิดปกติ = อุณหภูมิ/ความชื้นนอกเกณฑ์ ∨ ทะเบียนคุมเข้าออก=ไม่มี ∨ อุปกรณ์ใด=ไม่ปกติ → เตือน + ไฮไลต์ · ไม่บล็อก · แนะนำหมายเหตุ | CONFIGURABLE [AI-DEFAULT] | DEC-04 · DEC-13 (VALID) |
| BR-03 | พบแถวผิดปกติใหม่ → src_abnormal_found ถึง admin role ฝ่าย IT | CONFIGURABLE | DEC-04 · NTF |
| BR-04 | ผู้ตรวจสอบของแถว = ผู้ใช้ที่บันทึก/แก้แถวนั้นล่าสุด (แก้มือไม่ได้ · ไม่ใช้ภาพลายเซ็น) | FIXED [AI-DEFAULT] | DEC-07 |
| BR-05 | ความดันถังดับเพลิงเก็บเป็นข้อความสั้น (ไม่ตรวจหน่วย) จนลูกค้ายืนยันรูปแบบ | FIXED [AI-DEFAULT] | DEC-12 (VALID) |
| BR-06 | ช่อง 1:1 ตามกระดาษ 11 คอลัมน์ · ไม่เพิ่มช่อง | FIXED [AI-DEFAULT] | DEC-06 |
| BR-07 | แถวไม่จำกัด · PDF ≥ 30 แถว · 16 แถว/หน้า · หัวตารางซ้ำ · ไม่มีบล็อกลงชื่อท้ายใบ | FIXED | DEC-05 · DEC-07 |
| BR-08 | แนบไฟล์ระดับใบ (ไม่บังคับ) · CSV ✓ · ทำซ้ำ ✗ | FIXED [AI-DEFAULT] | DEC-10 |
| BR-09 | เลขออกตอนบันทึกครั้งแรก (SRC) | FIXED | DEC-09 |
| BR-10 | submitted ล็อกแก้ไข · ยกเลิกได้ (draft/submitted) โดยเจ้าของหรือ admin role · เหตุผลบังคับ | FIXED [AI-DEFAULT] | G7 (raw) |
| BR-11 | ไม่เปลี่ยนค่าในระบบ · ไม่ส่งต่อระบบอื่น (ไม่เปิด Ticket อัตโนมัติ) | FIXED | DEC-01 · DEC-02 |
| BR-12 | การมองเห็น: เจ้าของ · admin role ฝ่าย IT เห็นทั้งหมด · ร่างไม่รั่วให้คนอื่น | FIXED | DEC-08 |
| BR-13 | ส่ง = ปิดรอบทันที · ไม่มีขั้นพิจารณา/ผู้ตรวจทาน (กระดาษไม่มีช่องลงชื่อผู้พิจารณา) · ต้องการผู้ตรวจทาน = enhancement + DOA_BRIEF (OQ-02) | FIXED [AI-DEFAULT] | DEC-03 · DEC-11 (VALID) |

## §5.2 State Machine
| จาก | event | ไป | guard |
|---|---|---|---|
| — | save | draft | FN-03 ออกเลข |
| draft | save rows | draft | owner |
| draft | submit | submitted | owner · FN-08 src_submitted |
| draft/submitted | cancel | cancelled | owner/admin role · เหตุผล · FN-08 src_cancelled |

## §5.3 Permission Matrix
| Action | owner | admin role IT | อื่น |
|---|:-:|:-:|:-:|
| ดู draft | ✓ | ✓ | ✗ |
| ดู submitted/cancelled | ✓ | ✓ | ✗ |
| สร้าง/แก้ draft | ✓ | ✗ | ✗ |
| ส่งปิดรอบ | ✓ | ✗ | ✗ |
| ยกเลิก | ✓ | ✓ | ✗ |

## §5.4 Validation Rules
| VR | ช่อง | เงื่อนไข | ข้อความ |
|---|---|---|---|
| VR-01 | ใบ | ≥ 1 แถวที่บันทึก | บันทึกผลตรวจอย่างน้อย 1 วัน |
| VR-02 | check_date · extinguisher_pressure · temperature_c · humidity_rh | required · อุณหภูมิ/ความชื้นเป็นตัวเลข 1 ตำแหน่ง | กรอกวันที่ · ความดันถังดับเพลิง · อุณหภูมิ · ความชื้น (ตัวเลข) ให้ครบทุกแถวที่บันทึก |
| VR-03 | check_date | ≤ วันนี้ | (ปฏิทินปิดวันอนาคต · API 422 FUTURE_DATE) |
| VR-04 | เหตุผลยกเลิก | required | กรุณาระบุเหตุผล |
| VR-05 | ส่งปิดรอบ | status = draft · ผู้ส่ง = owner | 409 NOT_DRAFT / 403 NOT_OWNER |

## §5.5 Edge Cases
| EC | กรณี | ผล | อ้าง |
|---|---|---|---|
| EC-01 | ค่านอกเกณฑ์ | ไฮไลต์ + เตือน · บันทึก/ส่งได้ · src_abnormal_found | BR-02/03 · DEC-13 |
| EC-02 | วันที่ซ้ำในใบ | เตือน "วันที่ซ้ำ" ไม่บล็อก | DEC-04 |
| EC-03 | 31 แถว | PDF 2 หน้า (16+15) | BR-07 |
| EC-04 | > 32 แถว | PDF หน้า 3 อัตโนมัติ · dense | BR-07 |
| EC-05 | ลูกค้าต้องการผู้ตรวจทานภายหลัง | enhancement: DOA_BRIEF + field สายพิจารณา · template แบบพิมพ์รองรับ sign_rows แล้ว (ไม่ต้องแก้แบบพิมพ์) | BR-13 · DEC-11 |
| EC-06 | stale write | 409 → toast รีเฟรช | §2.3 |
| EC-07 | doc_type ปิดใช้ | ปุ่มสร้าง disabled | FN-03 |
| EC-08 | เกณฑ์ใน config เปลี่ยนกลางเดือน | ใบเดิมประเมินด้วย criteria_snapshot เดิม | BR-01 |
| EC-09 | ความดันกรอกรูปแบบต่างกันแต่ละวัน | เก็บตามจริง (ข้อความ) | DEC-12 |
