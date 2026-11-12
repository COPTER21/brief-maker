# FRD lint — Section N

| ระดับ | ข้อ | ผล |
|---|---|---|
| PASS | N1 | DEC ครบ 18 ข้อใน 07 |
| PASS | N4 | มีเคส "ผู้อนุมัติไม่เห็นร่างของคนอื่น" |
| PASS | N4 | เคสปฏิเสธสิทธิ์ใน 06_TESTS: 13 จุด |
| PASS | N2 | ทุกช่องในฟอร์มมีคีย์ใน 04/01 |
| PASS | N3 | "ประจำปี 2569" ไม่ถูก hardcode (อ่านจาก CoiDisclosureConfig.current_year (ตัวแปรรอบปี)) |
| PASS | N3 | "ย่อหน้ารับรอง 2 ย่อหน้า (นิยามผลประโยชน์ทับซ้อน: บิดา มารดา สามี ภรรยา บุตร เครือญาติ …)" ไม่ถูก hardcode (อ่านจาก CoiDisclosureConfig.statement_text (ผูกเวอร์ชันนโยบาย · snapshot ลงใบตอนส่ง)) |
| PASS | N5 | ไม่อ้าง F185 API-23 |
| PASS | N5 | header_snapshot ใน 04_DB |
| PASS | N5 | จุดออกเลขใน 03: ['F-TMP-006-FN-03'] |
| PASS | N6 | approval_chain ใน 04_DB |
| PASS | N6 | doa_ref ใน 04_DB |
| PASS | N7 | event coi_conflict_declared ถูกอ้าง |
| PASS | N7 | event coi_cancelled ถูกอ้าง |
| PASS | N8 | ไม่อ้างเวอร์ชันที่ไม่ได้ติดตั้ง |
