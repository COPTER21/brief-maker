# FRD lint — Section N

| ระดับ | ข้อ | ผล |
|---|---|---|
| PASS | N1 | DEC ครบ 13 ข้อใน 07 |
| PASS | N4 | เคสปฏิเสธสิทธิ์ใน 06_TESTS: 9 จุด |
| PASS | N2 | ทุกช่องในฟอร์มมีคีย์ใน 04/01 |
| PASS | N3 | "18-27°C" ไม่ถูก hardcode (อ่านจาก ServerRoomCheckConfig.temp_min_c / temp_max_c) |
| PASS | N3 | "40-55 %RH" ไม่ถูก hardcode (อ่านจาก ServerRoomCheckConfig.rh_min / rh_max) |
| PASS | N5 | ไม่อ้าง F185 API-23 |
| PASS | N5 | header_snapshot ใน 04_DB |
| PASS | N5 | จุดออกเลขใน 03: ['F-TMP-002-FN-03'] |
| PASS | N7 | event src_abnormal_found ถูกอ้าง |
| PASS | N7 | event src_submitted ถูกอ้าง |
| PASS | N7 | event src_cancelled ถูกอ้าง |
| PASS | N8 | ไม่อ้างเวอร์ชันที่ไม่ได้ติดตั้ง |
