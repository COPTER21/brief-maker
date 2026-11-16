# FRD lint — Section N

| ระดับ | ข้อ | ผล |
|---|---|---|
| PASS | N1 | DEC ครบ 17 ข้อใน 07 |
| PASS | N4 | มีเคส "ผู้อนุมัติไม่เห็นร่างของคนอื่น" |
| PASS | N4 | เคสปฏิเสธสิทธิ์ใน 06_TESTS: 11 จุด |
| PASS | N2 | ทุกช่องในฟอร์มมีคีย์ใน 04/01 |
| PASS | N3 | "หัวข้อการประเมิน 4 ข้อ + เกณฑ์ย่อย (3-5 วันทำการ · 0.5-1% · 24 ชม. · 3 วันทำการ)" ไม่ถูก hardcode (อ่านจาก VendorEvaluationConfig.criteria[].text) |
| PASS | N3 | "คะแนนเฉลี่ย 3 / 4 / 2 / 1 (รวม 10)" ไม่ถูก hardcode (อ่านจาก VendorEvaluationConfig.criteria[].max_score) |
| PASS | N3 | "น้อยกว่า 6 / มากกว่า หรือ เท่ากับ 6" ไม่ถูก hardcode (อ่านจาก VendorEvaluationConfig.pass_threshold) |
| PASS | N5 | ไม่อ้าง F185 API-23 |
| PASS | N5 | header_snapshot ใน 04_DB |
| PASS | N5 | จุดออกเลขใน 03: ['F-TMP-004-FN-03'] |
| PASS | N6 | approval_chain ใน 04_DB |
| PASS | N6 | doa_ref ใน 04_DB |
| PASS | N7 | event vev_evaluation_failed ถูกอ้าง |
| PASS | N7 | event vev_cancelled ถูกอ้าง |
| PASS | N8 | ไม่อ้างเวอร์ชันที่ไม่ได้ติดตั้ง |
