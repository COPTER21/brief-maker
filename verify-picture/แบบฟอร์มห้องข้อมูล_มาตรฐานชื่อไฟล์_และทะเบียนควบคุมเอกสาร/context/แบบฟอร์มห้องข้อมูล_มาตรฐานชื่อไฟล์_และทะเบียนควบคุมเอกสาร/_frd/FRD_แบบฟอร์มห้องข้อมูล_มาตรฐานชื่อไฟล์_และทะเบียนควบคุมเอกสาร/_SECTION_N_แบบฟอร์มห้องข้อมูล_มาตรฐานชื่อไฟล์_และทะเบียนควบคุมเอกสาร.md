# FRD lint — Section N

| ระดับ | ข้อ | ผล |
|---|---|---|
| PASS | N1 | DEC ครบ 22 ข้อใน 07 |
| PASS | N4 | มีเคส "ผู้อนุมัติไม่เห็นร่างของคนอื่น" |
| PASS | N4 | เคสปฏิเสธสิทธิ์ใน 06_TESTS: 9 จุด |
| PASS | N2 | ทุกช่องในฟอร์มมีคีย์ใน 04/01 |
| PASS | N3 | "V01 / V02 / Final" ไม่ถูก hardcode (อ่านจาก FileNamingPolicy.version_format) |
| PASS | N3 | "20260701_Information_Memorandum_V03_Final.pdf" ไม่ถูก hardcode (อ่านจาก FileNamingPolicy.example) |
| PASS | N3 | "01–08 เอกสารบริษัท / อำนาจลงนาม … เอกสารปิดงาน" ไม่ถูก hardcode (อ่านจาก DataRoomPolicy.default_folders) |
| PASS | N5 | ไม่อ้าง F185 API-23 |
| PASS | N5 | header_snapshot ใน 04_DB |
| PASS | N5 | จุดออกเลขใน 03: ['F-TMP-006-FN-04'] |
| PASS | N6 | approval_chain ใน 04_DB |
| PASS | N6 | doa_ref ใน 04_DB |
| PASS | N7 | event ivmd_cancelled ถูกอ้าง |
| PASS | N7 | event ivmd_register_approved ถูกอ้าง |
| PASS | N8 | ไม่อ้างเวอร์ชันที่ไม่ได้ติดตั้ง |
