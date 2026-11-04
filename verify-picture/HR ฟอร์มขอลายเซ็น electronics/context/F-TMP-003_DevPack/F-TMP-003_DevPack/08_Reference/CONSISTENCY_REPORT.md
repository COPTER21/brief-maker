# CONSISTENCY_REPORT — F-TMP-003 · **READY**

| ระดับ | ข้อ | ผล |
|---|---|---|
| PASS | K1 | ไฟล์บังคับครบ |
| PASS | K2 | ไม่มีไฟล์ซ้ำ |
| WARN | K3 | run_log: ไฟล์ถูกแก้หลังลงทะเบียน — รัน manifest_scan ใหม่ |
| PASS | K4 | microcopy FRD 06 ↔ prototype ตรง (9 ข้อความ) |
| PASS | K5 | route ใน FRD มีใน prototype (4) |
| PASS | K6 | FRD 07 อ้างมติครบ 17 ข้อ |
| PASS | K6 | BRD อ้างมติครบ |
| PASS | K7 | declaration ครบและเป็นฉบับจริง |
| PASS | K8 | testcases_ai 22 เคส ตรงกับเอกสารคน/QA_AUDIT |
| WARN | K9 | ไม่มี report e2e_standard (html-generator v9.2 #111) |
| PASS | K9 | frd_lint BLOCK 0 |
