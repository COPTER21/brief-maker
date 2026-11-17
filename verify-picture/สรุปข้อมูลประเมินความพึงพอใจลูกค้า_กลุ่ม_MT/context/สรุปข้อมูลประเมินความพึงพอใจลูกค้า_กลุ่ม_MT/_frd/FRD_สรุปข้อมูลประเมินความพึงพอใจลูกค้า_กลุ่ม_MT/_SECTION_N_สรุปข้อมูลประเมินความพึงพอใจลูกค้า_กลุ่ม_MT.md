# FRD lint — Section N

| ระดับ | ข้อ | ผล |
|---|---|---|
| PASS | N1 | DEC ครบ 20 ข้อใน 07 |
| PASS | N4 | เคสปฏิเสธสิทธิ์ใน 06_TESTS: 12 จุด |
| PASS | N2 | ทุกช่องในฟอร์มมีคีย์ใน 04/01 |
| PASS | N3 | "มาตรฐานที่กำหนด 95%" ไม่ถูก hardcode (อ่านจาก SalesConfig.mt_csat_standard_pct (=95)) |
| PASS | N3 | "(80–94%) / ต่ำกว่า 80%" ไม่ถูก hardcode (อ่านจาก SalesConfig.mt_csat_low_pct (=80)) |
| PASS | N3 | "คะแนน (1-5) = 5 ทุกหัวข้อ" ไม่ถูก hardcode (อ่านจาก SalesConfig.mt_csat_criteria[].max_score (=5)) |
| PASS | N3 | "หัวข้อประเมิน 9 ข้อ" ไม่ถูก hardcode (อ่านจาก SalesConfig.mt_csat_criteria[] (ตามกระดาษ Rev.00)) |
| PASS | N3 | "บิ๊กซี … PT (15 ช่องทาง)" ไม่ถูก hardcode (อ่านจาก SalesConfig.mt_channels[] (ผูก Customer master กลุ่ม MT)) |
| PASS | N3 | "100%" ไม่ถูก hardcode (อ่านจาก คงที่ (ไม่ใช่ค่าตั้ง)) |
| PASS | N5 | ไม่อ้าง F185 API-23 |
| PASS | N5 | header_snapshot ใน 04_DB |
| PASS | N5 | จุดออกเลขใน 03: ['F-TMP-008-FN-03'] |
| PASS | N7 | event mts_low_channel ถูกอ้าง |
| PASS | N7 | event mts_cancelled ถูกอ้าง |
| PASS | N8 | ไม่อ้างเวอร์ชันที่ไม่ได้ติดตั้ง |
