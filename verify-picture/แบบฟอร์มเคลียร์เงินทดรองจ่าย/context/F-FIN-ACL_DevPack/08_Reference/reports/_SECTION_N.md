# FRD lint — Section N

| ระดับ | ข้อ | ผล |
|---|---|---|
| PASS | N1 | DEC ครบ 15 ข้อใน 07 |
| PASS | N4 | มีเคส "ผู้อนุมัติไม่เห็นร่างของคนอื่น" |
| PASS | N4 | เคสปฏิเสธสิทธิ์ใน 06_TESTS: 8 จุด |
| PASS | N2 | ทุกช่องในฟอร์มมีคีย์ใน 04/01 |
| WARN | N3 | "ภายในวันที่ 5 ของเดือนถัดไป" อาจถูก hardcode: ['- Input `{advance_ref, advance_amount, lines[]}` → errors VR-01..03 (05 §5.4)', '## §5.1 Business Rules', '## §5.2 State Machine'] |
| PASS | N3 | "บริษัท ครีเดนซ์ จำกัด (มหาชน) · ธนาคารยูโอบี สาขาสำนักสาทร · 601-119725-3" ไม่ถูก hardcode (อ่านจาก Company.bank_accounts[purpose=advance_refund]) |
| PASS | N5 | ไม่อ้าง F185 API-23 |
| PASS | N5 | header_snapshot ใน 04_DB |
| PASS | N5 | จุดออกเลขใน 03: ['F-FIN-ACL-FN-03'] |
| PASS | N6 | approval_chain ใน 04_DB |
| PASS | N6 | doa_ref ใน 04_DB |
| PASS | N7 | event acl_cancelled ถูกอ้าง |
| PASS | N7 | event acl_overspent_approved ถูกอ้าง |
| PASS | N7 | event acl_refund_due ถูกอ้าง |
| PASS | N8 | ไม่อ้างเวอร์ชันที่ไม่ได้ติดตั้ง |
| ตอบ | N3 | WARN = false positive: regex จับเลข 5 ในหัวข้อ §5.x — ไม่มีเลขเส้นตายใน logic |
