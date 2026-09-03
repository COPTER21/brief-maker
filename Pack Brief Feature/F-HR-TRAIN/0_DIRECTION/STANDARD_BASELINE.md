# STANDARD_BASELINE — F-HR-TRAIN · อบรม (S0.5)
> Odoo eLearning/Surveys · D365 (Learning) · SAP SF Learning (LMS)
## 1. Capability matrix (MUST = ทั้ง 3 ค่ายมี)
| # | Capability | Odoo | D365 | SAP SF | CUBE-fit | เหตุผล |
|---|---|---|---|---|---|---|
| 1 | แคตตาล็อกหลักสูตร (course catalog) | ✓ | ✓ | ✓ | **MUST** | master |
| 2 | แผนอบรม/รอบ (session/schedule) | ✓ | ✓ | ✓ | **MUST** | รอบต่อหลักสูตร |
| 3 | ลงทะเบียน/มอบหมาย (enroll/assign) | ✓ | ✓ | ✓ | **MUST** | จาก gap Performance |
| 4 | อนุมัติถ้ามีค่าใช้จ่าย (approval) | △ | ✓ | ✓ | **MUST** | = DOA |
| 5 | บันทึกผล/ผ่าน-ไม่ผ่าน (completion) | ✓ | ✓ | ✓ | **MUST** | ต่อผู้เรียน |
| 6 | ใบรับรอง/certificate | ✓ | ✓ | ✓ | **MUST** | soft ref รอบนี้ |
| 7 | ต้นทุนอบรม (cost) | △ | ✓ | ✓ | **MUST** | hook Expense · CSQ EC |
| 8 | แจ้งเตือน (เปิดรับ/ยืนยัน/ผล) | ✓ | ✓ | ✓ | **MUST** | ENG-NOTIFY |
| 9 | audit + masking | — | ✓ | ✓ | **MUST** | RESTRICTED บางส่วน |
| 10 | เชื่อม gap จากประเมิน (dev plan) | △ | ✓ | ✓ | SHOULD | hook Performance |
| 11 | รายงานการอบรม (attendance/completion) | ✓ | ✓ | ✓ | SHOULD | report |
| 12 | eLearning content/SCORM | ✓ | ✓ | ✓ | NICE→ไม่รองรับ | OQ |
| 13 | skill/competency mapping | △ | ✓ | ✓ | NICE→ไม่รองรับ | OQ |
**MUST = 9 (≥5 ✅)**
## 2. Lifecycle: หลักสูตร ร่าง→เผยแพร่→ปิด · การลงทะเบียน ลงทะเบียน→(อนุมัติถ้ามีค่าใช้จ่าย)→เข้าอบรม→บันทึกผล(ผ่าน/ไม่ผ่าน)→ใบรับรอง · ยกเลิก · **≥3 state ✅**
## 3. Archetype = master (หลักสูตร + การลงทะเบียน) · surfaces: สร้าง(หลักสูตร/ลงทะเบียน) · ส่ง(ขออนุมัติถ้ามีค่าใช้จ่าย) · เซ็น(DOA) · PDF ✗(ใบรับรอง soft ref) · เตือน ✓ · รายงาน ✓
## 4. Declarations: doa ✓ · ntf ✓ · csq ✓ (EC — ไม่มี AC เพราะ Expense ลงบัญชี) · doccfg ✗ · pdfdoc ✗
## 5. scope ตัด→OQ: SCORM/eLearning content · competency mapping = NICE ไม่รองรับ · ค่าอบรมจ่ายจริง = hook Expense
