# FRD lint — Section N

| ระดับ | ข้อ | ผล |
|---|---|---|
| PASS | N1 | DEC ครบ 15 ข้อใน 07 |
| PASS | N4 | มีเคส "ผู้อนุมัติไม่เห็นร่างของคนอื่น" |
| PASS | N4 | เคสปฏิเสธสิทธิ์ใน 06_TESTS: 13 จุด |
| PASS | N2 | ทุกช่องในฟอร์มมีคีย์ใน 04/01 |
| PASS | N3 | "Doc No. FM-HRM-31 · Rev. 00 : 01/07/2569" ไม่ถูก hardcode (อ่านจาก DocConfig.form_code + DocConfig.revision) |
| WARN | N3 | "รายการความยินยอม 8 ข้อ (ข้อมูล + วัตถุประสงค์)" อาจถูก hardcode: ['ดู 02_API §2.4 — ทุก mutation API มี FN ปลายทางครบ (R8)'] |
| PASS | N5 | ไม่อ้าง F185 API-23 |
| PASS | N5 | header_snapshot ใน 04_DB |
| PASS | N5 | จุดออกเลขใน 03: ['F-TMP-008-FN-03'] |
| PASS | N7 | event pdc_consent_recorded ถูกอ้าง |
| PASS | N7 | event pdc_consent_withdrawn ถูกอ้าง |
| PASS | N7 | event pdc_sensitive_refused ถูกอ้าง |
| PASS | N8 | ไม่อ้างเวอร์ชันที่ไม่ได้ติดตั้ง |
