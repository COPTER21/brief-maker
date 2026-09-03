# BRD — Recruit (สรรหา) · F-HR-RECRUIT · Lane Mode v2 · Status: **APPROVED** · W5 · Phase A
## §1 Overview
สรรหาบุคลากร: เปิดอัตรา → คลังผู้สมัคร → pipeline board (คัดกรอง/สัมภาษณ์/ข้อเสนอ) → ข้อเสนอจ้าง (DOA) → รับ → ส่งเข้า On/Offboard. ไม่จ้างจริง/ไม่สร้าง employee เอง. 4 tabs.
## §2 KPIs: time-to-hire · funnel conversion · %offer accepted · %ผู้สมัครมี consent
## §3 Scope
In: requisition · candidate pool(PDPA) · pipeline · interview · scorecard · offer(DOA) · hire handoff · report
Out: จ้างจริง/employee/สัญญา · external job board · assessment/agency · offer letter PDF · config band
### §3.4 Scope Lock: LK-1 offer/req อนุมัติ=DOA(17ส.ค.) ไม่ hardcode · LK-2 hired→Onboard handoff (ไม่สร้าง employee) · LK-3 PDPA consent+retention (SecC) เก็บได้เมื่อยินยอม · LK-4 band อ่าน HR Config(#107) · LK-5 ผู้สมัคร RESTRICTED masking · audit append-only · LK-6 CSQ SecC/EC เท่านั้น
## §4 Roles: HR สรรหา · Hiring Manager (ประเมิน/อนุมัติ) · ผู้สมัคร(ตอบรับ)
## §5 Journey: req(DOA)→pool(consent)→board→interview(NTF)→scorecard→offer(DOA)→accepted→onboarding handoff
## §6 Data: Requisition(ตำแหน่ง/จำนวน/ระดับ/band soft ref/hm/manpower_ref hook) · Candidate(ชื่อ/ติดต่อ RESTRICTED/consent_pdpa/stage/score) · Offer(ตำแหน่ง/เงินเดือน/วันเริ่ม/chain)
## §7 Stories: FN-01..94 (21 FN)
## §8 Lifecycle: req ร่าง→อนุมัติเปิด→ประกาศ→สรรหา→ปิด · candidate สมัคร→คัดกรอง→สัมภาษณ์→ข้อเสนอ→รับ · rejected/withdrawn/talent_pool
## §9 Rules BR-01..10 (ดู PREBRIEF) ### §9.5 band/DOA ตั้งนอก feature
## §10 Edge: no-consent บล็อก · duplicate เตือน · เปิดอัตราไม่มี MP เตือน · hired handoff
## §12.1 Downstream: On/Offboard(hire handoff event) · Manpower(อัตรา hook) [ASSUMED A-REC-01/03] · ENG-CSQ SecC(PDPA)/EC · ENG-NOTIFY 4 · DOA req+offer
## §13 Phase A→ba-done · Phase B ทีม
## §14.6 Functions Cut: จ้างจริง/employee/สัญญา · external board · assessment/agency · offer PDF · config band(#107)
## §16 Security: ผู้สมัคร RESTRICTED+PDPA masking · consent gate · audit append-only · SC ไม่ประกาศ
## §OQ: A-REC-01 เปิดอัตราไม่มี MP=hook · A-REC-02 offer DOA ตามระดับ · A-REC-03 handoff Onboard=event · A-REC-04 PDPA consent+retention
## Quality Gate C01–C23: APPROVED (§14.6 ไม่รองรับ · Scope Lock LK-1..6 · SecC PDPA)
