# STANDARD_BASELINE — F-HR-ESS · พนักงานทำเอง (S0.5)
> Odoo Employees(self) · D365 (Employee self-service) · SAP SF (Employee Central self-service)
## 1. Capability matrix (MUST = ทั้ง 3 ค่ายมี) — ESS = aggregator
| # | Capability | Odoo | D365 | SAP SF | CUBE-fit | เหตุผล |
|---|---|---|---|---|---|---|
| 1 | หน้ารวมของฉัน (self dashboard) | ✓ | ✓ | ✓ | **MUST** | home |
| 2 | สลิปเงินเดือน + ประวัติ (payslip) | ✓ | ✓ | ✓ | **MUST** | อ่าน Payroll PS-1 (display-only) |
| 3 | วันลา/โควตาคงเหลือ + ยื่นลา | ✓ | ✓ | ✓ | **MUST** | อ่าน Leave · ยื่น=ลิงก์ |
| 4 | OT/เวลา/สแกน ของฉัน | ✓ | ✓ | ✓ | **MUST** | อ่าน OT/Attendance |
| 5 | ใบเบิกค่าใช้จ่าย ของฉัน | ✓ | ✓ | ✓ | **MUST** | อ่าน Expense · ยื่น=ลิงก์ |
| 6 | เอกสาร/หนังสือรับรอง ของฉัน | ✓ | ✓ | ✓ | **MUST** | อ่าน Cert |
| 7 | ข้อมูลส่วนตัว/โปรไฟล์ | ✓ | ✓ | ✓ | **MUST** | อ่าน Employee (แก้=ลิงก์/ขออนุมัติ) |
| 8 | แจ้งเตือนของฉัน (my notifications) | ✓ | ✓ | ✓ | **MUST** | ENG-NOTIFY (ของฉัน) |
| 9 | สวัสดิการ/คงเหลือ · อบรม/ใบรับรอง | △ | ✓ | ✓ | **MUST** | อ่าน Welfare/Training |
| 10 | ยื่นคำขอ (ลา/เบิก/OT) = deep-link ไปหน้า feature | ✓ | ✓ | ✓ | **MUST** | ไม่ทำ form เอง (A-ESS-02) |
| 11 | audit + masking (self-access · SecC) | — | ✓ | ✓ | **MUST** | เห็นเฉพาะของตัวเอง |
| 12 | mobile-first / responsive | ✓ | ✓ | ✓ | SHOULD | v9 responsive |
| 13 | ทีมของฉัน (manager self-service · อนุมัติ) | △ | ✓ | ✓ | NICE→ไม่รองรับ | รอบนี้ ESS พนักงาน |
**MUST = 11 (≥5 ✅)** · ★ ทุก capability = **อ่าน surface ของ feature ต้นทาง (display-only) — ไม่ CRUD (OQ-HR-04)**
## 2. Lifecycle: portal ไม่มี document lifecycle ของตัวเอง — แสดงสถานะจาก feature ต้นทาง (read) · การกระทำ (ยื่น) = navigate ไปหน้า feature เจ้าของ
## 3. Archetype = portal(aggregate) · หน้า home + cards/tabs ต่อโดเมน · surface: อ่านทุกอย่าง · action = deep-link · ไม่มีเอกสาร/เลขรัน/PDF/DOA ของตัวเอง
## 4. Declarations: ntf ✓ (my notifications) · csq ✓ (SecC self-access) · doa ✗ · doccfg ✗ · pdfdoc ✗
## 5. scope ตัด→OQ: manager self-service/อนุมัติ = NICE ไม่รองรับ (ESS พนักงาน) · ยื่นคำขอ = deep-link (ไม่ทำ form เอง)
