# BRD — ESS Portal (พนักงานทำเอง) · F-HR-ESS · Lane Mode v2 · APPROVED · W6 · Phase A
## §1 Overview: portal รวมมุมมองพนักงาน self-service — สลิป/ลา/OT/เวลา/เบิก/หนังสือรับรอง/สวัสดิการ/อบรม/แจ้งเตือน ไว้ที่เดียว. display-only · deep-link ไปหน้า feature เจ้าของ. ไม่ CRUD ซ้ำ (OQ-HR-04). home dashboard + 4 tabs. ไม่มี doa/doccfg/pdfdoc.
## §2 KPIs: self-service adoption · %คำขอที่เริ่มจาก portal · เวลาเข้าถึงสลิป/สิทธิ์ของตัวเอง
## §3 Scope In: home dashboard(สรุป read) · payslip อ่าน PS-1 self · leave/OT/attendance read · expense read · cert read · welfare/training read · profile read · my notifications · self-access guard · Out: form ยื่นลา/เบิก/OT เอง(=deep-link หน้าเจ้าของ) · แก้โปรไฟล์เอง · ออกเอกสาร/เลขรันเอง · เข้าถึงข้อมูลคนอื่น
### §3.4 Scope Lock: LK-1 display-only ทุก surface · ห้าม CRUD feature อื่น(OQ-HR-04·BR-01) · LK-2 ยื่นคำขอ=navigate หน้า feature เจ้าของ(BR-03) · LK-3 สลิปอ่าน Payroll PS-1 self · all-or-nothing(BR-02) · LK-4 self-access เท่านั้น · เข้าถึงคนอื่น=403(SecC·BR-06) · LK-5 surface ba-done=[ASSUMED contract] soft ref(BR-07) · LK-6 CSQ SecC เท่านั้น + NTF อ่าน feed(ไม่นับ doa_*) · ไม่มี doa/doccfg/pdfdoc · audit อ่าน
## §4 Roles: พนักงานทุกคน (เห็นเฉพาะข้อมูลของตัวเอง · mobile-friendly)
## §5 Journey: login→home dashboard(สลิป/โควตาลา/OT/ใบเบิกค้าง/แจ้งเตือน)→เลือก tab→ดูรายละเอียด read→ยื่นคำขอ=deep-link หน้าเจ้าของ
## §6 Data: ไม่มี entity ของตัวเอง (aggregator) — อ่าน surface self-scope: Payroll(PS-1)·Leave·OT·Attendance·Expense·Cert·Welfare·Training·Notification·Employee(profile)
## §7 Stories FN-01..94(15) ## §8 Lifecycle: ไม่มี lifecycle ของตัวเอง — แสดงสถานะจาก feature ต้นทาง(read)
## §9 Rules BR-01..08 ### §9.5 ทุก surface อ่านนอก feature (display-only) · masking ตาม self
## §10 Edge: self-access 403 · surface ba-done soft ref · ยื่น=deep-link · mobile responsive · สลิป all-or-nothing
## §12.1 Downstream/Upstream: อ่าน 10 surface (upstream) · deep-link → Leave/Expense/OT/Training/Welfare/Cert(navigate) · ENG-NOTIFY(อ่าน feed) · ENG-CSQ SecC(self-access) · ไม่มี DOA/DOCCFG/PDFDOC
## §13 Phase A→ba-done ## §14.6 Functions Cut: form ยื่นลา/เบิก/OT เอง(deep-link) · แก้โปรไฟล์เอง(link/ขออนุมัติ) · ออกสลิป/หนังสือรับรอง PDF เอง(มาจาก feature ต้นทาง) · เข้าถึงข้อมูลคนอื่น(403) · config(#107)
## §16 Security: self-access เท่านั้น(SecC) · personal/salary RESTRICTED masking ตาม self · เข้าถึงคนอื่น=403 · audit(อ่าน) append-only · SC ไม่ประกาศ
## §OQ: A-ESS-01 อ่านทุก surface display-only(OQ-HR-04) · A-ESS-02 ยื่น=deep-link หน้าเจ้าของ · A-ESS-03 surface ba-done=[ASSUMED contract] soft ref
## Quality Gate C01–C23: APPROVED (§14.6 · Scope Lock LK-1..6 · SecC · NTF read-feed · no doa/doccfg/pdfdoc)
