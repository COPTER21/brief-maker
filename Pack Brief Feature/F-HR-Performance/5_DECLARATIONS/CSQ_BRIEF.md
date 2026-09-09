# CSQ_BRIEF — F-HR-PERF
## Declared Events
| event_id | trigger | ท่อ | เงื่อนไข | payload |
|---|---|---|---|---|
| perf.result_recorded | สอบทาน→เผยแพร่ผล (S-05·BR-08) | **SecC** | เข้าถึง/เก็บผลประเมิน (ข้อมูลอ่อนไหว) | ref:appraisal_id · employee_id · action(view/store) |
| perf.decision_made | สอบทาน decision go/no-go/PIP (S-05/S-09) | **DC** | terminal decision (ผ่าน/ไม่ผ่าน/ทบทวน) — ไม่ใช่การเซ็นอนุมัติเอกสาร | ref:appraisal_id · decision · basis: declared |
## ไม่ประกาศ: OC(OP) · DC-เอกสาร+doa_*(DOA) · AC/FC(ไม่ลงบัญชี/เงินสด) · SC(สงวน)
