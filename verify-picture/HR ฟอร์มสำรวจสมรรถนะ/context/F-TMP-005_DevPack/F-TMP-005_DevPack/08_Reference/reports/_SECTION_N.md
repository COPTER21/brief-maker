# FRD lint — Section N

| ระดับ | ข้อ | ผล |
|---|---|---|
| PASS | N1 | DEC ครบ 12 ข้อใน 07 |
| PASS | N4 | มีเคส "ผู้อนุมัติไม่เห็นร่างของคนอื่น" |
| PASS | N4 | เคสปฏิเสธสิทธิ์ใน 06_TESTS: 8 จุด |
| PASS | N2 | ทุกช่องในฟอร์มมีคีย์ใน 04/01 |
| WARN | N3 | "1 ต้องพัฒนา (ยังไม่สามารถปฏิบัติได้ตามมาตรฐาน)" อาจถูก hardcode: ["- บันทึกครั้งแรกเรียก `ENG-DOC-NUM.next('CMP', company_ctx)` (DEC-11 · `issue_on: first_sa", '- `core_lines` และ `func_lines` ต้องมีอย่างน้อย 1 แถวที่มี `competency_name`', '- แถวที่มี `competency_name` ต้องมี `level` (1–4) → ไม่มี = `LEVEL_REQUIRED`'] |
| WARN | N3 | "2 พอใช้ (ปฏิบัติได้บางส่วน แต่ยังไม่สม่ำเสมอ)" อาจถูก hardcode: ['- บันทึกประวัติ append-only 2 รายการ: ผลการพิจารณา + "กลับเป็นร่าง"'] |
| WARN | N3 | "3 ทำได้ดี (ปฏิบัติได้ตามมาตรฐานของตำแหน่ง)" อาจถูก hardcode: ['## 3.0 State machine'] |
| WARN | N3 | "4 เชี่ยวชาญ (ทำได้ดีมาก และสามารถถ่ายทอดให้ผู้อื่นได้)" อาจถูก hardcode: ['- แถวที่มี `competency_name` ต้องมี `level` (1–4) → ไม่มี = `LEVEL_REQUIRED`', '| VR-04 | แถวที่มี `competency_name` ต้องเลือก `level` 1–4 — ไม่เลือก = `LEVEL_REQUIRED` |'] |
| PASS | N5 | ไม่อ้าง F185 API-23 |
| PASS | N5 | header_snapshot ใน 04_DB |
| PASS | N5 | จุดออกเลขใน 03: ['FN-01'] |
| PASS | N6 | approval_chain ใน 04_DB |
| PASS | N6 | doa_ref ใน 04_DB |
| PASS | N7 | event cmp_cancelled ถูกอ้าง |
| PASS | N8 | ไม่อ้างเวอร์ชันที่ไม่ได้ติดตั้ง |
