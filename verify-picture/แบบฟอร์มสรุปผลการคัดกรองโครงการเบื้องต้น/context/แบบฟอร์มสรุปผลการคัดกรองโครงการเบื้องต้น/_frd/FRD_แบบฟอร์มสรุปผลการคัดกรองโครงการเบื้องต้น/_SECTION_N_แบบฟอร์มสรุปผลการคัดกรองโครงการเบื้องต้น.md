# FRD lint — Section N

| ระดับ | ข้อ | ผล |
|---|---|---|
| PASS | N1 | DEC ครบ 17 ข้อใน 07 |
| PASS | N4 | มีเคส "ผู้อนุมัติไม่เห็นร่างของคนอื่น" |
| PASS | N4 | เคสปฏิเสธสิทธิ์ใน 06_TESTS: 8 จุด |
| PASS | N2 | ทุกช่องในฟอร์มมีคีย์ใน 04/01 |
| PASS | N3 | "8 เกณฑ์ประเมิน + น้ำหนัก 15/15/15/20/10/10/10/5" ไม่ถูก hardcode (อ่านจาก ScreeningCriteria.items[] (name, weight_pct)) |
| PASS | N3 | "≥80 เสนอให้ดำเนินการต่อ · ≥60 ดำเนินการต่อแบบมีเงื่อนไข · <60 ไม่เสนอให้ดำเนินการต่อ" ไม่ถูก hardcode (อ่านจาก ScreeningCriteria.recommend_bands) |
| PASS | N3 | "คะแนน 1-5 · หาร 5" ไม่ถูก hardcode (อ่านจาก ScreeningCriteria.score_max) |
| PASS | N5 | ไม่อ้าง F185 API-23 |
| PASS | N5 | header_snapshot ใน 04_DB |
| PASS | N5 | จุดออกเลขใน 03: ['F-TMP-003-FN-03'] |
| PASS | N6 | approval_chain ใน 04_DB |
| PASS | N6 | doa_ref ใน 04_DB |
| PASS | N7 | event scr_cancelled ถูกอ้าง |
| PASS | N7 | event scr_not_proceed_approved ถูกอ้าง |
| PASS | N8 | ไม่อ้างเวอร์ชันที่ไม่ได้ติดตั้ง |
