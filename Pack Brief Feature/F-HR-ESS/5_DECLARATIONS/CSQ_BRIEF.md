# CSQ_BRIEF — F-HR-ESS · พนักงานทำเอง
## Declared Events
| event_id | trigger | ท่อ | เงื่อนไข | payload |
|---|---|---|---|---|
| ess.self_access | พนักงานเปิดดูข้อมูลตัวเอง (สลิป/ลา/OT/เบิก… S-10·BR-06) | **SecC** | การเข้าถึงข้อมูลส่วนบุคคลของตัวเอง (self-access log) | ref:employee_id · surface(payslip/leave/…) · action(view) |
## ไม่ประกาศ: OC(OP) · DC-เอกสาร+doa_*(ไม่มี DOA) · AC/FC(ไม่ลงบัญชี/เงินสด · portal อ่านอย่างเดียว) · SC(สงวน)
## หมายเหตุ: ESS ไม่ประกาศ event ของ feature ต้นทางซ้ำ (payslip/leave/expense event ประกาศแล้วในแต่ละ feature) — ประกาศเฉพาะ self-access ของ portal
