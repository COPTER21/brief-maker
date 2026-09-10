# PREBRIEF · ESS Portal — พนักงานทำเอง
archetype_confirmed: portal(aggregate)  (home dashboard + cards/tabs ต่อโดเมน · อ่าน surface feature ต้นทาง display-only · ไม่มีเอกสาร/CRUD ของตัวเอง)
source: LANE_BRIEF + STANDARD_BASELINE (MUST 11)
## 0. Obligations
| # | พันธะ | จาก | § |
|---|---|---|---|
| OB-1 | อ่านทุก surface (display-only) · ห้าม CRUD ซ้ำ (OQ-HR-04) | มติ · CONTEXT_PACK | ทุก S, BR-01 |
| OB-2 | สลิปอ่านจาก Payroll PS-1 (all-or-nothing · self เท่านั้น) | F-HR-PAYROLL §0.13.2 | S-02, BR-02 |
| OB-3 | ยื่นคำขอ (ลา/เบิก/OT) = deep-link ไปหน้า feature เจ้าของ (ไม่ทำ form เอง) | A-ESS-02 | S-03,S-05, BR-03 |
| OB-4 | เห็นเฉพาะข้อมูลของตัวเอง (self-access · SecC) | current-state §3 | S-10, BR-06, §12 |
| OB-5 | surface ba-done = [ASSUMED contract] soft ref | CONTEXT_PACK | S-11, BR-07 |
## 1. สรุป: portal รวมมุมมองพนักงาน (self-service) — สลิป/ลา/OT/เวลา/เบิก/หนังสือรับรอง/สวัสดิการ/อบรม/แจ้งเตือน. ผู้ใช้: พนักงานทุกคน (เห็นเฉพาะของตัวเอง). **display-only · deep-link · ไม่ CRUD**.
## 2. Scenarios
| S-XX | ประเภท | เรื่อง | ข้อมูล |
|---|---|---|---|
| S-01 | Happy | หน้ารวมของฉัน (สลิปล่าสุด · โควตาลา · OT · ใบเบิกค้าง · แจ้งเตือน) | dashboard summary (read) |
| S-02 | Happy | ดูสลิปเงินเดือน + ประวัติ + YTD (อ่าน Payroll PS-1 · self) | payslip read |
| S-03 | Happy | ดูวันลา/โควตาคงเหลือ · **ยื่นลา = ไปหน้า "การลา"** | leave read + deep-link |
| S-04 | Happy | ดู OT/เวลา/สแกน ของฉัน (อ่าน OT/Attendance) | ot/time read |
| S-05 | Happy | ดูใบเบิก ของฉัน · **ยื่นเบิก = ไปหน้า "เบิกค่าใช้จ่าย"** | expense read + deep-link |
| S-06 | Alt | ดูหนังสือรับรอง/เอกสาร ของฉัน (อ่าน Cert) | cert read |
| S-07 | Alt | ดูสวัสดิการ/คงเหลือ · อบรม/ใบรับรอง ของฉัน | welfare/training read |
| S-08 | Alt | ดูโปรไฟล์ · **ขอแก้ข้อมูล = ลิงก์/ขออนุมัติ** (ไม่แก้เอง) | profile read + link |
| S-09 | Happy | แจ้งเตือนของฉัน (my notifications) | notify feed |
| S-10 | Exception | เห็นเฉพาะข้อมูลของตัวเอง — เข้าถึงคนอื่นไม่ได้ (SecC) | self-access guard |
| S-11 | Exception | surface ที่ feature ยัง ba-done → display-only + [ASSUMED contract] | soft ref note |
## 3. Data: ไม่มี entity ของตัวเอง (aggregator) — อ่าน view/surface: Payroll(PS-1) · Leave · OT · Attendance · Expense · Cert · Welfare · Training · Notification · Employee(profile) · ทั้งหมด self-scope
## 4. Rules
BR-01 ห้าม CRUD surface feature อื่น (display-only · deep-link) · BR-02 สลิปอ่าน PS-1 self เท่านั้น (all-or-nothing) · BR-03 ยื่นคำขอ=navigate หน้า feature เจ้าของ · BR-04 dashboard = สรุป read จากหลาย surface · BR-05 responsive (พนักงานใช้มือถือ) · BR-06 self-access เท่านั้น (SecC · เข้าถึงคนอื่น=403) · BR-07 surface ba-done=[ASSUMED contract] soft ref · BR-08 audit(อ่าน) · masking ตาม self
## 5. State: ไม่มี lifecycle ของตัวเอง — แสดงสถานะจาก feature ต้นทาง (read)
## 6. Actions (home + 4 tabs/มุมมอง): หน้าหลัก(dashboard cards) · เงินเดือน&เวลา(สลิป/ลา/OT/เวลา) · เอกสาร&สิทธิ์(เบิก/หนังสือรับรอง/สวัสดิการ/อบรม) · แจ้งเตือน · ทุก action ปุ่ม "ไปที่ [feature]" (deep-link)
## 7. behaviour: read-only · deep-link นำทาง · self-scope · ไม่มี drawer แก้ข้อมูล (มี drawer ดูรายละเอียด read-only)
## 8. Mock: พนักงาน 1 คน (สมชาย ใจดี) · สลิป 3 เดือน · โควตาลา · OT · ใบเบิก 2 · หนังสือรับรอง 1 · สวัสดิการคงเหลือ · อบรม · แจ้งเตือน 4 · พ.ศ.
## 9. Edges: self-access 403 · surface ba-done soft ref · ยื่น=deep-link · mobile responsive
## 10. OQ: A-ESS-01 อ่านทุก surface display-only (OQ-HR-04) · A-ESS-02 ยื่น=deep-link · A-ESS-03 surface ba-done=[ASSUMED contract]
## 11. Coverage
| S | BR | หน้าจอ | FN |
|---|---|---|---|
| S-01 | BR-04 | home dashboard | FN-01 |
| S-02 | BR-02 | payslip view | FN-02 |
| S-03 | BR-03 | leave + deep-link | FN-03 |
| S-04 | BR-01 | ot/time view | FN-04 |
| S-05 | BR-03 | expense + deep-link | FN-05 |
| S-06 | BR-01 | cert view | FN-06 |
| S-07 | BR-01 | welfare/training view | FN-07 |
| S-08 | BR-03 | profile + link | FN-08 |
| S-09 | BR-08 | my notifications | FN-09 |
| S-10 | BR-06 | self-access guard | FN-10 |
| S-11 | BR-07 | soft-ref note | FN-11 |
## §12 สัญญาณประกาศ
| ท่อ | สัญญาณ | chip | สรุป |
|---|---|---|---|
| DOA | ไม่มีการอนุมัติ (portal อ่านอย่างเดียว) | — | no |
| NTF | S-09 แจ้งเตือนของฉัน (อ่าน feed ของ ENG-NOTIFY · ไม่นับ doa_*) | ✓ | need |
| CSQ | S-10/BR-06 พนักงานเข้าถึงข้อมูลตัวเอง (self-access) → **SecC** | ✓ | need |
| DOCCFG | ไม่มีเลขรัน (ไม่ออกเอกสารเอง) | — | no |
| PDF DOC | ไม่มี (สลิป/หนังสือรับรอง PDF มาจาก feature ต้นทาง) | — | no |
DIVERGENCE: —
