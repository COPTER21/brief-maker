# FRD lint — Section N

| ระดับ | ข้อ | ผล |
|---|---|---|
| PASS | N1 | DEC ครบ 16 ข้อใน 07 |
| PASS | N4 | มีเคส "ผู้อนุมัติไม่เห็นร่างของคนอื่น" |
| PASS | N4 | เคสปฏิเสธสิทธิ์ใน 06_TESTS: 8 จุด |
| PASS | N2 | ทุกช่องในฟอร์มมีคีย์ใน 04/01 |
| PASS | N3 | "คะแนน 1–5 โอกาสเกิด/ผลกระทบ (ต่ำมาก…สูงมาก + คำอธิบาย)" ไม่ถูก hardcode (อ่านจาก RiskMatrix.likelihood_scale / RiskMatrix.impact_scale) |
| PASS | N3 | "1-4 ต่ำ · 5-9 ปานกลาง · 10-16 สูง · 17-25 สูงมาก" ไม่ถูก hardcode (อ่านจาก RiskMatrix.level_bands) |
| PASS | N3 | "ประเภทความเสี่ยง 9 ประเภท" ไม่ถูก hardcode (อ่านจาก RiskMatrix.categories) |
| PASS | N5 | ไม่อ้าง F185 API-23 |
| PASS | N5 | header_snapshot ใน 04_DB |
| PASS | N5 | จุดออกเลขใน 03: ['F-TMP-002-FN-03'] |
| PASS | N6 | approval_chain ใน 04_DB |
| PASS | N6 | doa_ref ใน 04_DB |
| PASS | N7 | event rsk_cancelled ถูกอ้าง |
| PASS | N7 | event rsk_very_high_approved ถูกอ้าง |
| PASS | N8 | ไม่อ้างเวอร์ชันที่ไม่ได้ติดตั้ง |
