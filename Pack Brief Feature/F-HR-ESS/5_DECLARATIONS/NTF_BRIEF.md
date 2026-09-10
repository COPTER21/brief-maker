# NTF_BRIEF — F-HR-ESS · พนักงานทำเอง
> ESS **อ่าน feed** ของ ENG-NOTIFY (แจ้งเตือนของฉัน) — ไม่ผลิต event เอง (event มาจาก feature ต้นทาง: Leave/OT/Expense/Welfare/Training/Payroll)
| Event ID | Trigger | ผู้รับ | หมายเหตุ |
|---|---|---|---|
| (aggregate feed) | รวมแจ้งเตือนของพนักงานจากทุก feature | พนักงานเจ้าของ | ESS แสดง feed · deep-link ไปหน้า feature ต้นทาง · ไม่สร้าง event ใหม่ |
## Dev: ESS เรียก ENG-NOTIFY.list(employee_id, self) — read feed เท่านั้น · ห้าม emit event ของตัวเอง (event ต้นทางประกาศแล้วในแต่ละ feature)
