# FRD lint — Section N

| ระดับ | ข้อ | ผล |
|---|---|---|
| PASS | N1 | DEC ครบ 17 ข้อใน 07 |
| PASS | N4 | มีเคส "ผู้อนุมัติไม่เห็นร่างของคนอื่น" |
| PASS | N4 | เคสปฏิเสธสิทธิ์ใน 06_TESTS: 10 จุด |
| PASS | N2 | ทุกช่องในฟอร์มมีคีย์ใน 04/01 |
| WARN | N3 | "รายการตรวจสอบทั่วไป 15 รายการ (สภาพตัวรถโดยรวม … ตรวจสอบการรั่วซึม)" อาจถูก hardcode: ['- Input `{vehicle_type, inspection_month, results[]}` → errors VR-01..04 (05 §5.4): vehicl', '| BR-04 | ห้ามวันเกินเดือน/วันอนาคต (บล็อก) | FIXED | DEC-15 (VALID) |', '| VR-02 | inspection_month | required · ≤ เดือนปัจจุบัน | เลือกเดือนปัจจุบันหรือเดือนก่อนห'] |
| PASS | N3 | "รายการตรวจสอบเฉพาะรถฟอร์คลิฟท์น้ำมัน 8 รายการ" ไม่ถูก hardcode (อ่านจาก ForkliftChecklistConfig.items[section=fuel]) |
| PASS | N3 | "รายการตรวจสอบเฉพาะรถฟอร์คลิฟท์ไฟฟ้า 6 รายการ" ไม่ถูก hardcode (อ่านจาก ForkliftChecklistConfig.items[section=electric]) |
| PASS | N3 | "คอลัมน์วันที่ 1–31" ไม่ถูก hardcode (อ่านจาก Calendar(inspection_month).days — ปิดวันที่เกินจำนวนวันของเดือน) |
| PASS | N5 | ไม่อ้าง F185 API-23 |
| PASS | N5 | header_snapshot ใน 04_DB |
| PASS | N5 | จุดออกเลขใน 03: ['F-TMP-002-FN-03'] |
| PASS | N6 | approval_chain ใน 04_DB |
| PASS | N6 | doa_ref ใน 04_DB |
| PASS | N7 | event fli_defect_found ถูกอ้าง |
| PASS | N7 | event fli_cancelled ถูกอ้าง |
| PASS | N8 | ไม่อ้างเวอร์ชันที่ไม่ได้ติดตั้ง |
| ตอบ | N3 | WARN = false positive: regex จับเลข 15 ใน DEC-15 / §5.4 — ไม่มีจำนวนรายการตายตัวใน logic (อ่าน ForkliftChecklistConfig) |
