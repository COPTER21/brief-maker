# BRD — Performance (ประเมินผลงาน) · F-HR-PERF · Lane Mode v2 · APPROVED · W5 · Phase A
## §1 Overview: ประเมินผลงานตามรอบ (จาก HR Config) → KPI → ประเมินตนเอง+หัวหน้า → สอบทาน (DOA·decision) → ผล/gap → ส่งต่อ Training/Succession/Movement. ไม่ปรับเงินเดือน/ตำแหน่งเอง. 4 tabs.
## §2 KPIs: %ประเมินตรงเวลา · การกระจายคะแนน · %gap ส่งอบรม
## §3 Scope In: รอบ · KPI/เป้า · self/mgr appraisal · สอบทาน(DOA·DC) · gap→Training(hook) · ผล→Movement(event) · report · Out: ปรับเงินเดือน/ตำแหน่งเอง · 360/competency/check-in · config รอบ
### §3.4 Scope Lock: LK-1 สอบทาน=DOA(17ส.ค.) · LK-2 ผล→Movement event (ไม่ CRUD) · LK-3 รอบ/แบบจาก HR Config(#107) · LK-4 ผลประเมิน RESTRICTED(SecC) · audit append-only · LK-5 gap→Training hook · LK-6 CSQ SecC/DC เท่านั้น (ห้าม OC/DC-doc/SC)
## §4 Roles: HR/HRBP · หัวหน้า(ประเมิน/สอบทาน) · พนักงาน(ประเมินตนเอง)
## §5 Journey: รอบ(HR Config)→ตั้งเป้า→self→mgr→สอบทาน(DOA·decision)→ผล/gap→Training/Movement
## §6 Data: Cycle(จาก HR Config appraisal_cycle) · Appraisal(employee snapshot·self/mgr score·decision·gap) · KPI(น้ำหนัก·เป้า·self·mgr)
## §7 Stories FN-01..94 (18) ## §8 Lifecycle: รอบ ร่าง→เปิด→ประเมิน→สอบทาน→ปิด · แบบ ตั้งเป้า→self→mgr→สอบทาน→เผยแพร่ · ไม่ผ่าน→PIP
## §9 Rules BR-01..10 ### §9.5 รอบ/เกณฑ์ตั้งนอก feature (HR Config)
## §10 Edge: น้ำหนัก≠100 เตือน · เกินกำหนด · คะแนนต่ำ→PIP · ผล→event
## §12.1 Downstream: Training(gap hook) · Movement(ปรับเงินเดือน/ตำแหน่ง event) · Succession(ผล) [ASSUMED A-PERF-01/02] · ENG-CSQ SecC/DC · ENG-NOTIFY 3 · DOA calibration
## §13 Phase A→ba-done ## §14.6 Functions Cut: ปรับเงินเดือน/ตำแหน่งเอง(event) · 360/competency/check-in · config รอบ(#107) · ทำหลักสูตร(hook Training)
## §16 Security: ผลประเมิน RESTRICTED masking(SecC) · audit append-only · SC ไม่ประกาศ
## §OQ: A-PERF-01 ผล→Movement event · A-PERF-02 gap→Training hook · A-PERF-03 รอบจาก HR Config
## Quality Gate C01–C23: APPROVED (§14.6 · Scope Lock LK-1..6 · SecC/DC)
