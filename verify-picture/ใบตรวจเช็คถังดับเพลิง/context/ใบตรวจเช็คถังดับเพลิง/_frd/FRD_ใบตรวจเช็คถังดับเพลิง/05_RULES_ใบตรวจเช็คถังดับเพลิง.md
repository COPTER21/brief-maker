# 05_RULES — F-TMP-001

## §5.1 Business Rules
| ID | Rule | Tag | ที่มา |
|---|---|---|---|
| BR-01 | ทุกแถวต้องเลือกครบ 4 หัวข้อ (มาตรวัด · ซีล/สลัก · สายฉีด · สภาพถัง) | FIXED [AI-DEFAULT] | DEC-04 |
| BR-02 | แถวมีหัวข้อ x ≥ 1 = ผิดปกติ · ผลล่าสุดของใบ = แถววันที่ล่าสุด | FIXED | DEC-04 |
| BR-03 | ผิดปกติ → fec_abnormal_found ถึง role-mgr-wh (บังคับ) | CONFIGURABLE (ผู้รับตาม role) | DEC-13 (VALID) |
| BR-04 | 1 จุดติดตั้งมีใบสถานะใช้งานได้ 1 ใบ · พิมพ์ 1 ใบ = 1 สถานที่ | FIXED [AI-DEFAULT] | DEC-11 (VALID) |
| BR-05 | วันที่ตรวจ ≤ วันนี้ · ไม่ซ้ำวันในใบ | FIXED [AI-DEFAULT] | DEC-04 |
| BR-06 | ผู้ตรวจ = ผู้บันทึก (ระบบใส่) | FIXED | DEC-04 · DEC-07 |
| BR-07 | แก้แถวได้เฉพาะผู้บันทึกภายในวันที่บันทึก | CONFIGURABLE [AI-DEFAULT] | DEC-04 |
| BR-08 | ออกเลขตอนบันทึกครั้งแรก (ENG-DOC-NUM) · no-gap ✗ | CONFIGURABLE | DEC-09 |
| BR-09 | การมองเห็นตาม §5.3 · ไม่มีสิทธิ์ = 404 | FIXED | DEC-08 |
| BR-10 | PDF ≥ 12 แถว · > 12 แถว dense 1 หน้า · ไม่มีช่องลงชื่อ | FIXED | DEC-05 · DEC-07 |
| BR-11 | ช่องตามกระดาษ 1:1 ไม่เพิ่มช่อง · ข้อความท้ายใช้ "ผู้จำหน่าย" (แก้คำสะกด) | FIXED [AI-DEFAULT] | DEC-06 · DEC-12 (VALID) |
| BR-12 | ยกเลิก: เจ้าของหรือ role-mgr-wh · สถานะใช้งาน · เหตุผลบังคับ · fec_cancelled | FIXED | DEC-10 · NTF |
| BR-13 | ไม่มีขั้นพิจารณา/ลงนาม · ไม่เปลี่ยนค่าในระบบ · ไม่ส่งต่อระบบอื่น | FIXED [AI-DEFAULT] | DEC-01 · DEC-02 · DEC-03 |

## §5.2 State Machine
| จาก | event | ไป | guard |
|---|---|---|---|
| — | save | active | FN-01 · FN-03 ออกเลข |
| active | add_check / edit_check | active | FN-02 · BR-07 |
| active | cancel | cancelled | เจ้าของ/role-mgr-wh · เหตุผล |
cancelled = ล็อก (ไม่มี transition ออก)

## §5.3 Permission Matrix (G8 · DEC-08)
| Action | warehouse_staff | role-mgr-wh | นอกแผนก |
|---|:-:|:-:|:-:|
| ดู | ทั้งหมด | ทั้งหมด | ของตน |
| สร้าง | ✓ | ✓ | ✓ |
| บันทึกผลตรวจ | ใบที่เห็น (active) | ✓ | ของตน |
| แก้แถว | ของตน วันเดียวกัน | ของตน วันเดียวกัน | ของตน วันเดียวกัน |
| ยกเลิก | ของตน | ✓ | ของตน |

## §5.4 Validation
| VR | ช่อง | เงื่อนไข | ข้อความ | API |
|---|---|---|---|---|
| VR-01 | สถานที่ | required | กรุณาเลือกสถานที่ | 422 LOCATION_REQUIRED |
| VR-02 | สถานที่ | ไม่มีใบใช้งาน | สถานที่นี้มีใบตรวจที่ใช้งานอยู่แล้ว | 409 LOCATION_HAS_ACTIVE_CARD |
| VR-03 | วันที่ | ≤ วันนี้ | วันที่ตรวจห้ามเป็นวันในอนาคต | 422 DATE_IN_FUTURE |
| VR-04 | วันที่ | ไม่ซ้ำในใบ | วันที่นี้บันทึกผลตรวจแล้ว | 409 DATE_DUPLICATE |
| VR-05 | 4 หัวข้อ | ครบ | เลือกผลให้ครบทั้ง 4 หัวข้อ | 422 MARKS_INCOMPLETE |
| VR-06 | เหตุผลยกเลิก | required | กรุณาระบุเหตุผล | 422 REASON_REQUIRED |

## §5.5 Edge Cases
EC-01 ใบเปล่า → last_result none · EC-02 > 12 แถว → dense · EC-03 ย้ายถัง → ยกเลิก + สร้างใหม่ · EC-04 บันทึกย้อนหลังได้ (≤ วันนี้) · EC-05 แก้ข้ามวัน → 403 · EC-06 stale → 409 · EC-07 doc_type ปิด → 409 DOC_TYPE_INACTIVE · EC-08 ต้นฉบับ 2 การ์ด → 1 การ์ดต่อหน้า (DEC-11)

## §5.7 D-CLASS
inspector_name_snapshot = Confidential·PII — export CSV แสดงตามสิทธิ์ · prototype ใช้ชื่อสมมติ
