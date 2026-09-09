# STANDARD_BASELINE — F-HR-PERF · ประเมินผลงาน (S0.5)
> Odoo Appraisal · D365 (Goals/Performance) · SAP SF Performance & Goals
## 1. Capability matrix (MUST = ทั้ง 3 ค่ายมี)
| # | Capability | Odoo | D365 | SAP SF | CUBE-fit | เหตุผล |
|---|---|---|---|---|---|---|
| 1 | รอบประเมิน (cycle/period) | ✓ | ✓ | ✓ | **MUST** | จาก HR Config appraisal_cycle |
| 2 | ตั้งเป้า/KPI (goals) | ✓ | ✓ | ✓ | **MUST** | ต่อคน/รอบ |
| 3 | ประเมินตนเอง (self-appraisal) | ✓ | ✓ | ✓ | **MUST** | — |
| 4 | ประเมินโดยหัวหน้า (manager review) | ✓ | ✓ | ✓ | **MUST** | — |
| 5 | คะแนน/rating scale | ✓ | ✓ | ✓ | **MUST** | ต่อ KPI + รวม |
| 6 | สอบทาน/อนุมัติผล (calibration/approve) | △ | ✓ | ✓ | **MUST** | = DOA · DC decision |
| 7 | gap/แผนพัฒนา → Training | ✓ | ✓ | ✓ | **MUST** | hook Training |
| 8 | แจ้งเตือน (รอบเปิด/ครบกำหนด/ผล) | ✓ | ✓ | ✓ | **MUST** | ENG-NOTIFY |
| 9 | audit + masking ผลประเมิน (RESTRICTED) | — | ✓ | ✓ | **MUST** | SecC |
| 10 | ผล→ปรับเงินเดือน/เลื่อนตำแหน่ง | ✓ | ✓ | ✓ | **MUST** | event Movement (ไม่ CRUD) |
| 11 | 360 feedback (peer/multi-rater) | △ | ✓ | ✓ | SHOULD [AI-DRAFT] | รอบนี้ self+manager |
| 12 | รายงานการกระจายคะแนน (distribution) | ✓ | ✓ | ✓ | SHOULD | report |
| 13 | competency model/library | △ | ✓ | ✓ | NICE→ไม่รองรับ | OQ |
| 14 | continuous check-in/1:1 | ✓ | ✓ | ✓ | NICE→ไม่รองรับ | OQ |
**MUST = 10 (≥5 ✅)**
## 2. Lifecycle: รอบ: ร่าง→เปิดกรอก(open)→ประเมิน(in_review)→สอบทาน(calibration·DOA)→ปิดรอบ(closed) · แบบต่อคน: ตั้งเป้า→ประเมินตนเอง→หัวหน้าประเมิน→สอบทาน→เผยแพร่ผล · **≥3 state ✅**
## 3. Archetype = master+cycle (master แบบประเมิน + cycle รอบ) · surfaces: สร้าง(รอบ/เป้า) · ส่ง(ประเมิน) · เซ็น(สอบทาน DOA) · PDF ✗ · เตือน ✓ · รายงาน ✓
## 4. Declarations: doa ✓ · ntf ✓ · csq ✓ (SecC ผลประเมิน · DC decision รอบ) · doccfg ✗ · pdfdoc ✗
## 5. scope ตัด→OQ: 360/competency/check-in = NICE ไม่รองรับ · ปรับเงินเดือน = event Movement (ไม่ทำเอง)
