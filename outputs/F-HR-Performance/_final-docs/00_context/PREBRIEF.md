# PREBRIEF · Performance — ประเมินผลงาน
archetype_confirmed: master  (master แบบประเมิน/KPI + cycle รอบ · ไม่ใช่ Q-document)
source: LANE_BRIEF + STANDARD_BASELINE (MUST 10)
## 0. Obligations
| # | พันธะ | จาก | § |
|---|---|---|---|
| OB-1 | รอบ/แบบประเมินจาก HR Config appraisal_cycle (#107) | F-HR-CONFIG | S-01, BR-01 |
| OB-2 | สอบทานผล = DOA + decision (DC) | current-state §3 | S-05, BR-05, §12 |
| OB-3 | ผล→ปรับเงินเดือน/ตำแหน่ง = event Movement (ไม่ CRUD) | F-HR-MOVE | S-07, BR-07 |
| OB-4 | gap→Training (hook) | A-PERF-02 | S-06, BR-06 |
| OB-5 | ผลประเมิน RESTRICTED (SecC) · audit append-only | current-state §3 | BR-08 |
## 1. สรุป: ประเมินผลงานตามรอบ → KPI → ประเมินตนเอง+หัวหน้า → สอบทาน → ผล/gap → ส่งต่อ. ผู้ใช้: HR · หัวหน้า(ประเมิน/สอบทาน) · พนักงาน(ประเมินตนเอง). ผลประเมิน RESTRICTED.
## 2. Scenarios
| S-XX | ประเภท | เรื่อง | ข้อมูล |
|---|---|---|---|
| S-01 | Happy | สร้างรอบประเมิน (จาก HR Config) → เปิดกรอก | รอบ · ช่วง · ผู้เข้าร่วม |
| S-02 | Happy | ตั้งเป้า/KPI ต่อคน (น้ำหนัก) | KPI · target · weight |
| S-03 | Happy | พนักงานประเมินตนเอง | self score+comment |
| S-04 | Happy | หัวหน้าประเมิน + คะแนน | mgr score+comment |
| S-05 | Happy | สอบทานผล (calibration · DOA · DC decision) | reviewer · decision |
| S-06 | Alt | ผลออก → gap → ส่ง Training (hook) | gap · training hook |
| S-07 | Alt | ผล → ปรับเงินเดือน/เลื่อนตำแหน่ง = **event Movement (ไม่ CRUD)** | event payload |
| S-08 | Exception | ประเมินไม่ครบ/เกินกำหนด → เตือน | overdue |
| S-09 | Exception | คะแนนต่ำ/ไม่ผ่าน → แผน PIP / decision | pip · decision |
| S-10 | Alt | ปิดรอบ (ล็อกแก้) | closed |
| S-11 | Alt | แจ้งเตือน รอบเปิด/ครบกำหนด/ผล | notify |
| S-12 | Alt | รายงานการกระจายคะแนน (distribution) | metrics |
## 3. Data: Cycle(ชื่อ·ปี·ช่วง·สถานะ·config_version) · Appraisal(employee snapshot·cycle·สถานะ·self/mgr score·decision·gap) · KPI line(หัวข้อ·น้ำหนัก·target·self·mgr) · §3.4 อ่าน HR Config(appraisal_cycle) · Employee Master
## 4. Rules
BR-01 รอบจาก HR Config(#107) · BR-02 KPI น้ำหนักรวม=100% · BR-03 self ก่อน mgr · BR-04 คะแนนรวม = weighted · BR-05 สอบทาน(DOA·DC) ก่อนเผยแพร่ผล · BR-06 gap→Training hook · BR-07 ผล→Movement event (ไม่ CRUD เงินเดือน) · BR-08 ผลประเมิน RESTRICTED masking(SecC) · BR-09 audit append-only · ปิดรอบล็อก · BR-10 snapshot ชื่อ/ตำแหน่ง ณ รอบ
## 5. State: รอบ ร่าง→เปิด→ประเมิน→สอบทาน(DOA)→ปิด · แบบ ตั้งเป้า→ประเมินตนเอง→หัวหน้า→สอบทาน→เผยแพร่ · ไม่ผ่าน→PIP
## 6. Actions (4 tabs): รอบประเมิน · แบบประเมิน(รายคน · KPI editor) · ผล & Gap · รายงาน · view drawer(รายละเอียด›KPI/คะแนน›สอบทาน›ประวัติ) · สอบทาน=DOA slot
## 7. behaviour: weighted score computed · ผลเผยแพร่หลังสอบทาน · Movement/Training = event/hook อ่าน-ส่งครั้งเดียว
## 8. Mock: 2 รอบ (เปิด/ปิด) · 5 แบบประเมิน (ต่าง state · 1 คะแนนต่ำ→PIP · 1 สอบทานแล้ว) · KPI 3-4 ต่อคน · พ.ศ.
## 9. Edges: น้ำหนัก≠100 เตือน · เกินกำหนด · คะแนนต่ำ→PIP · ผล→event ไม่ CRUD
## 10. OQ: A-PERF-01 ผล→Movement event · A-PERF-02 gap→Training hook · A-PERF-03 รอบ/แบบจาก HR Config
## 11. Coverage
| S | BR | หน้าจอ | FN |
|---|---|---|---|
| S-01 | BR-01 | รอบ create | FN-01 |
| S-02 | BR-02 | KPI editor | FN-02 |
| S-03 | BR-03 | self appraisal | FN-03 |
| S-04 | BR-04 | mgr review | FN-04 |
| S-05 | BR-05 | สอบทาน DOA | FN-05,FN-08 |
| S-06 | BR-06 | gap→Training | FN-06 |
| S-07 | BR-07 | →Movement event | FN-07 |
| S-08 | BR-09 | overdue warn | FN-09 |
| S-09 | BR-05 | PIP/decision | FN-10 |
| S-10 | BR-09 | ปิดรอบ | FN-11 |
| S-11 | BR-08 | notify | FN-12 |
| S-12 | BR-08 | report | FN-13 |
## §12 สัญญาณประกาศ
| ท่อ | สัญญาณ | chip | สรุป |
|---|---|---|---|
| DOA | S-05 สอบทานผล (ไม่มีวงเงิน) | ✓ | need |
| NTF | S-01 รอบเปิด · S-08 ครบกำหนด · S-05 ผล (ไม่นับ doa_*) | ✓ | need |
| CSQ | S-04/S-05 ผลประเมิน→**SecC** · S-05 decision go/no-go/ผ่าน→**DC** (terminal decision ไม่ใช่การเซ็น) | ✓ | need |
| DOCCFG | ไม่มีเลขรัน | — | no |
| PDF DOC | ไม่มีเอกสารคนถือ | — | no |
DIVERGENCE: —
