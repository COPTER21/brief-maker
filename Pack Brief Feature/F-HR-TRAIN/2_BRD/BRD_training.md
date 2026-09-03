# BRD — Training & Development (อบรม) · F-HR-TRAIN · Lane Mode v2 · APPROVED · W5 · Phase A
## §1 Overview: แคตตาล็อกหลักสูตร → ลงทะเบียน (จาก gap Performance) → อนุมัติถ้ามีค่าใช้จ่าย (DOA) → ผล/ใบรับรอง. ค่าอบรม = hook Expense. 4 tabs.
## §2 KPIs: completion rate · %ลงทะเบียนจาก gap · จำนวนหลักสูตรมีค่าใช้จ่ายที่อนุมัติ
## §3 Scope In: หลักสูตร · รอบ · ลงทะเบียน · DOA(cost) · ผล/ใบรับรอง(soft ref) · ค่าอบรม hook Expense · report · Out: จ่ายค่าอบรม/GL · ประเมิน/gap เอง · SCORM/competency · config หมวด
### §3.4 Scope Lock: LK-1 DOA เมื่อ has_cost(17ส.ค.) · LK-2 ค่าอบรม=hook Expense(ไม่จ่าย/post เอง) · LK-3 gap=hook Performance · LK-4 audit append-only · LK-5 CSQ EC เท่านั้น(ไม่มี AC · Expense ลงบัญชี · ห้าม OC/DC-doc/SC) · LK-6 config หมวดอ่าน HR Config(#107)
## §4 Roles: HR L&D · หัวหน้า(อนุมัติ cost) · พนักงาน(เข้าอบรม)
## §5 Journey: หลักสูตร→ลงทะเบียน(gap/เลือก)→[has_cost?DOA:ข้าม]→เข้าอบรม→ผล→ใบรับรอง · ค่าอบรม→Expense hook
## §6 Data: Course(has_cost·งบ) · Session(วันเวลา·จำนวนรับ) · Enrollment(employee snapshot·สถานะ·ผล·gap_ref·cost·expense_hook)
## §7 Stories FN-01..94(18) ## §8 Lifecycle: หลักสูตร ร่าง→เผยแพร่→ปิด · ลงทะเบียน→[อนุมัติ]→เข้าอบรม→ผล→ใบรับรอง · ยกเลิก
## §9 Rules BR-01..10 ### §9.5 หมวด/งบ ตั้งนอก feature
## §10 Edge: เกินจำนวนรับ · has_cost→DOA · ค่าอบรม→Expense hook · gap→หลักสูตร
## §12.1 Downstream: Expense(ค่าอบรม hook) · Performance(gap hook) [ASSUMED A-TRN-01/02] · ENG-CSQ EC · ENG-NOTIFY 3 · DOA cost
## §13 Phase A→ba-done ## §14.6 Functions Cut: จ่ายค่าอบรม/GL(hook Expense) · ประเมิน/gap เอง(hook Performance) · SCORM/competency · ใบรับรอง PDF เลขรัน · config หมวด(#107)
## §16 Security: masking · audit append-only · SC ไม่ประกาศ
## §OQ: A-TRN-01 ค่าอบรม→Expense hook · A-TRN-02 gap→หลักสูตร hook · A-TRN-03 ใบรับรอง soft ref
## Quality Gate C01–C23: APPROVED (§14.6 · Scope Lock LK-1..6 · EC no AC)
