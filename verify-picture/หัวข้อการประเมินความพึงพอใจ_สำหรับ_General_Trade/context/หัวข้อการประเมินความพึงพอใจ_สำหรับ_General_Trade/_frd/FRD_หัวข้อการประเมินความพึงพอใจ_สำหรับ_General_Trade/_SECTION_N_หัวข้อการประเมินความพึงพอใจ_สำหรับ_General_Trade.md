# FRD lint — Section N

| ระดับ | ข้อ | ผล |
|---|---|---|
| PASS | N1 | DEC ครบ 20 ข้อใน 07 |
| PASS | N4 | มีเคส "ผู้อนุมัติไม่เห็นร่างของคนอื่น" |
| PASS | N4 | เคสปฏิเสธสิทธิ์ใน 06_TESTS: 9 จุด |
| PASS | N2 | ทุกช่องในฟอร์มมีคีย์ใน 04/01 |
| PASS | N3 | "ตั้งแต่ 3 ครั้งขึ้นไป / เดือน" ไม่ถูก hardcode (อ่านจาก SalesConfig.csat_min_orders_per_month (=3)) |
| PASS | N3 | "80% – 100%: ลูกค้ามีความพึงพอใจสูง" ไม่ถูก hardcode (อ่านจาก SalesConfig.csat_bands[high].min (=80)) |
| PASS | N3 | "60% – 79%: ลูกค้าพึงพอใจในระดับปานกลาง" ไม่ถูก hardcode (อ่านจาก SalesConfig.csat_bands[mid].min (=60)) |
| PASS | N3 | "ต่ำกว่า 60%: ลูกค้าอาจมีความไม่พึงพอใจ" ไม่ถูก hardcode (อ่านจาก SalesConfig.csat_bands[low]) |
| PASS | N3 | "หัวข้อการประเมิน 3 ด้าน 16 ข้อ" ไม่ถูก hardcode (อ่านจาก SalesConfig.csat_topics[] (ตามกระดาษ Rev.00)) |
| PASS | N5 | ไม่อ้าง F185 API-23 |
| PASS | N5 | header_snapshot ใน 04_DB |
| PASS | N5 | จุดออกเลขใน 03: ['F-TMP-002-FN-03'] |
| PASS | N6 | approval_chain ใน 04_DB |
| PASS | N6 | doa_ref ใน 04_DB |
| PASS | N7 | event csm_cancelled ถูกอ้าง |
| PASS | N7 | event csm_low_csat ถูกอ้าง |
| PASS | N8 | ไม่อ้างเวอร์ชันที่ไม่ได้ติดตั้ง |
