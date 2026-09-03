# PREBRIEF · Training — อบรม
archetype_confirmed: master  (หลักสูตร + การลงทะเบียน · ไม่ใช่ Q-document)
source: LANE_BRIEF + STANDARD_BASELINE (MUST 9)
## 0. Obligations
| # | พันธะ | จาก | § |
|---|---|---|---|
| OB-1 | ค่าอบรม → hook Expense Claim (ไม่จ่ายเอง) | F-HR-EXPENSE | S-08, BR-06 |
| OB-2 | gap → หลักสูตร (hook Performance) | F-HR-PERF | S-09, BR-07 |
| OB-3 | มีค่าใช้จ่าย = อนุมัติ DOA | current-state §3 | S-04, BR-04 |
| OB-4 | มูลค่าอบรม → CSQ EC (ไม่มี AC) | STANDARD_BASELINE cap.7 | S-04, §12 |
| OB-5 | audit append-only · masking | current-state §3 | BR-08 |
## 1. สรุป: แคตตาล็อกหลักสูตร → ลงทะเบียน (จาก gap/เลือก) → อนุมัติถ้ามีค่าใช้จ่าย → ผล/ใบรับรอง. ผู้ใช้: HR อบรม · หัวหน้า(อนุมัติ) · พนักงาน(เข้าอบรม). ค่าอบรม = hook Expense.
## 2. Scenarios
| S-XX | ประเภท | เรื่อง | ข้อมูล |
|---|---|---|---|
| S-01 | Happy | สร้างหลักสูตร (ชื่อ·หมวด·ผู้สอน·ระยะเวลา·มีค่าใช้จ่าย?·งบ) | course fields |
| S-02 | Happy | สร้างรอบอบรม (วันเวลา·สถานที่·จำนวนรับ) | session |
| S-03 | Happy | ลงทะเบียน/มอบหมายผู้เรียน (จาก gap Performance หรือเลือกเอง) | enroll |
| S-04 | Alt | มีค่าใช้จ่าย → ขออนุมัติ (DOA) → อนุมัติ → ยิง EC | approval + EC |
| S-05 | Alt | ไม่มีค่าใช้จ่าย → ลงทะเบียนได้เลย (ไม่ผ่าน DOA) | no-cost path |
| S-06 | Happy | เข้าอบรม → บันทึกผล (ผ่าน/ไม่ผ่าน) | completion |
| S-07 | Alt | ออกใบรับรอง (soft ref) | cert |
| S-08 | Alt | ค่าอบรม → ส่ง Expense Claim (hook display-only) | expense hook |
| S-09 | Alt | gap จาก Performance → แนะนำหลักสูตร (hook) | gap hook |
| S-10 | Alt | ยกเลิกการลงทะเบียน | cancel |
| S-11 | Alt | แจ้งเตือน (เปิดรับ/ยืนยัน/ผล) | notify |
| S-12 | Alt | รายงานการอบรม (completion rate) + filter | metrics |
## 3. Data: Course(ชื่อ·หมวด·ผู้สอน·ระยะเวลา·has_cost·งบ·สถานะ) · Session(วันเวลา·สถานที่·จำนวนรับ) · Enrollment(employee snapshot·course·สถานะ·ผล·gap_ref·cost·expense_hook) · §3.4 อ่าน Employee · Performance(gap) · Expense(cost hook)
## 4. Rules
BR-01 หลักสูตรมีค่าใช้จ่าย=ต้องมีงบ · BR-02 จำนวนลงทะเบียน≤จำนวนรับ · BR-03 ลงทะเบียนจาก gap หรือเลือก · BR-04 มีค่าใช้จ่าย→DOA ก่อนยืนยัน (ไม่มีค่าใช้จ่าย ข้าม DOA) · BR-05 บันทึกผลหลังเข้าอบรม · BR-06 ค่าอบรม=hook Expense (ไม่จ่าย/ไม่ post เอง) · BR-07 gap→หลักสูตร hook Performance · BR-08 audit append-only·masking · BR-09 มูลค่าอบรมอนุมัติ→CSQ EC · BR-10 snapshot ชื่อผู้เรียน
## 5. State: หลักสูตร ร่าง→เผยแพร่→ปิด · ลงทะเบียน ลงทะเบียน→(อนุมัติ DOA ถ้ามีค่าใช้จ่าย)→เข้าอบรม→ผล(ผ่าน/ไม่ผ่าน)→ใบรับรอง · ยกเลิก
## 6. Actions (4 tabs): หลักสูตร · แผน/ลงทะเบียน · ผล/ใบรับรอง · รายงาน · view drawer(รายละเอียด›ผู้เรียน›อนุมัติ/ค่าใช้จ่าย›ประวัติ) · อนุมัติ=DOA slot
## 7. behaviour: has_cost→DOA gate · ค่าอบรม→Expense hook · ผลเผยแพร่หลังบันทึก
## 8. Mock: 4 หลักสูตร (2 มีค่าใช้จ่าย · 2 ฟรี) · 2 รอบ · 6 ลงทะเบียน (ต่าง state · 1 จาก gap · 1 รออนุมัติ · 1 ผ่าน+cert) · พ.ศ.
## 9. Edges: เกินจำนวนรับ · มีค่าใช้จ่ายต้อง DOA · ค่าอบรม→Expense hook · gap→หลักสูตร
## 10. OQ: A-TRN-01 ค่าอบรม→Expense hook · A-TRN-02 gap→หลักสูตร hook · A-TRN-03 ใบรับรอง soft ref
## 11. Coverage
| S | BR | หน้าจอ | FN |
|---|---|---|---|
| S-01 | BR-01 | course create | FN-01 |
| S-02 | BR-02 | session create | FN-02 |
| S-03 | BR-03 | enroll | FN-03 |
| S-04 | BR-04,09 | DOA approve+EC | FN-04,FN-08 |
| S-05 | BR-04 | no-cost path | FN-05 |
| S-06 | BR-05 | record result | FN-06 |
| S-07 | BR-05 | certificate | FN-07 |
| S-08 | BR-06 | expense hook | FN-09 |
| S-09 | BR-07 | gap hook | FN-10 |
| S-10 | BR-08 | cancel enroll | FN-11 |
| S-11 | BR-08 | notify | FN-12 |
| S-12 | BR-08 | report | FN-13 |
## §12 สัญญาณประกาศ
| ท่อ | สัญญาณ | chip | สรุป |
|---|---|---|---|
| DOA | S-04 อนุมัติเมื่อหลักสูตร**มีค่าใช้จ่าย** (ไม่มีค่าใช้จ่าย=ข้าม) · [ASSUMED ตามงบ/ไม่มีวงเงิน] | ✓ | need |
| NTF | S-02 เปิดรับ · S-04 ยืนยันลงทะเบียน · S-06 ผลอบรม (ไม่นับ doa_*) | ✓ | need |
| CSQ | S-04/BR-09 มูลค่าอบรมอนุมัติ → **EC** เท่านั้น (ไม่มี AC · Expense ลงบัญชี) | ✓ | need |
| DOCCFG | ไม่มีเลขรัน | — | no |
| PDF DOC | ใบรับรอง = soft ref รอบนี้ | — | no |
DIVERGENCE: —
