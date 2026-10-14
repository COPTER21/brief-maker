# 06_TESTS — F-AGM-012 Cane Payment Setting

> Audience: QA + ai-testcase-md-generator · microcopy-aware · interest/bank-fee/schedule/preview heavy

## §6.1 Acceptance Criteria

### General + Interest + Bank Fee (US-01) ⭐
- **AC-01** section ข้อมูลทั่วไป: สินค้าอ้อย + หมายเหตุ + Base @10CCS (read-only)
- **AC-02** กลุ่มดอกเบี้ยบิลขาว: ดอกเบี้ยต่อปี (%) + วันฐาน + ดอกเบี้ยต่อวัน (read-only, auto)
- **AC-03** กรอก ดอกเบี้ยต่อปี 7 + วันฐาน 365 → ดอกเบี้ยต่อวัน = roundUp(7/365, 7) แสดง
- **AC-04** ดอกเบี้ยต่อปี ≤ 0 → "ดอกเบี้ยต่อปีต้องมากกว่า 0"
- **AC-05** กลุ่มค่าธนาคาร: จังหวัดหลัก + ค่าในจังหวัด + ค่าต่างจังหวัด
- **AC-06** bank fee ไม่เลือกจังหวัดหลัก → "กรุณาเลือกจังหวัดหลัก"

### CCS Delta (US-02)
- **AC-07** สูตร "ราคาต่อตัน = Base @10CCS + (CCS − 10) × (Base @10CCS × K)" แสดง · K default 0.060
- **AC-08** CCS preview: Base Price @10CCS / ราคาต่อ 1 CCS / ราคาต่อตัน @CCS / ราคาต่อกิโลกรัม (คำนวณตาม K)

### Additional Charges (US-03)
- **AC-09** table (ชื่อรายการ/ประเภท/ค่า/หมายเหตุ) + เพิ่ม/แก้ไข/ลบ

### Tax (US-04)
- **AC-10** VAT switch "หัก VAT ก่อนแบ่งงวด" → เปิด → rate

### Payout Schedule (US-05) ⭐
- **AC-11** 2 sub-tabs: ตารางวันจ่ายบิลเขียว / ตารางวันจ่ายบิลขาว
- **AC-12** บิลเขียว columns: # · ช่วงวันที่ส่ง/ขึ้นเงิน · วันจ่ายงวด 1 · วันจ่ายงวด 2 · การใช้งาน(toggle) · จัดการ
- **AC-13** บิลขาว columns: # · ช่วงวันที่เบิกบิลขาว · วันจ่าย · การใช้งาน · จัดการ
- **AC-14** บิลขาว WITH_CANE → วันจ่าย = "ตามตารางบิลเขียว (ไม่คิดดอกเบี้ย)"
- **AC-15** เพิ่มช่วง (modal): เดือน/ปี พ.ศ./วันเริ่มต้น/วันสิ้นสุด + (green: วันจ่ายงวด 1/2) / (white: ประเภทวันจ่าย)
- **AC-16** white modal: เลือก "วันที่กำหนด" → ต้องกรอกวันจ่าย · "พร้อมค่าอ้อย" → ไม่กรอก
- **AC-17** toggle การใช้งาน เปิด/ปิด row

### Preview & Test (US-06) ⭐
- **AC-18** inputs: CCS · น้ำหนัก · วันที่ส่ง/ขึ้นเงิน · ประเภทบิลงวด 1 (บิลเขียว/บิลขาว) · งวด 2 · % หักหนี้ · จังหวัดบัญชีเกษตรกร
- **AC-19** คำนวณ → ราคาต่อตัน/กก. · ยอดรวม · ต่องวด (วันจ่ายปกติ/จริง/วันล่วงหน้า/หนี้/ดอกเบี้ย/ค่าธนาคาร/สุทธิ)
- **AC-20** บิลขาว → มีดอกเบี้ย (days_early × daily_rate) · บิลเขียว → ไม่มีดอกเบี้ย
- **AC-21** จังหวัดบัญชี = จังหวัดหลัก → in-province fee · ต่าง → out-province fee

### Save (US-07)
- **AC-22** บันทึก → validate + unique Active + toast success
- **AC-23** unique Active ซ้ำ → "มีการตั้งค่า Active สำหรับรอบหีบ+สินค้านี้อยู่แล้ว"

## §6.9 Cross-Module / Event Test Cases ⭐
| XT | Scenario | Source | Expected |
|---|---|---|---|
| XT-01 | Base @10CCS | Price List (read) | read-only จาก master |
| XT-02 | Season/Product | masters (read) | selector |
| XT-03 | Cane Payment อ่าน active setting | → Cane Payment | active config (K/interest/bank fee/pay dates) |
| XT-04 | daily_rate | calc | roundUp(rate_year/base_days, 7) |
| XT-05 | Receiving net_weight+cane_type → Payment ใช้ config นี้ | F-AGM-011 → Payment | chain SoT |

## §6.10 Microcopy-Aware Expected (verbatim)
| จุด | ข้อความ |
|---|---|
| header | `Payment Setting Configuration` · `รอบหีบ (Crushing Season)` |
| sections | `ข้อมูลทั่วไป` · `สูตรคำนวณ CCS` · `รายการหักเพิ่มเติม` · `ภาษี` · `ตารางกำหนดวันจ่าย` · `ทดสอบและดูตัวอย่าง` |
| interest | `ดอกเบี้ยบิลขาว` · `ดอกเบี้ยต่อปี` · `วันฐาน` · `ดอกเบี้ยต่อวัน` |
| bank fee | `ค่าธนาคาร` · `จังหวัดหลัก` · `ในจังหวัด` · `ต่างจังหวัด` |
| CCS | `ราคาต่อตัน = Base @10CCS + (CCS − 10) × (Base @10CCS × K)` · `ราคาต่อ 1 CCS` · `ราคาต่อกิโลกรัม` |
| tax | `หัก VAT ก่อนแบ่งงวด` |
| payout tabs | `ตารางวันจ่ายบิลเขียว` · `ตารางวันจ่ายบิลขาว` |
| payout cols | `ช่วงวันที่ส่ง/ขึ้นเงิน` · `วันจ่ายงวด 1` · `วันจ่ายงวด 2` · `ช่วงวันที่เบิกบิลขาว` · `วันจ่าย` · `การใช้งาน` · `จัดการ` |
| pay type | `ประเภทวันจ่าย` · `วันที่กำหนด` · `พร้อมค่าอ้อย` · `ตามตารางบิลเขียว` |
| preview | `ประเภทบิลงวด 1` · `ประเภทบิลงวด 2` · `บิลเขียว (ปกติ)` · `บิลขาว (เบิกล่วงหน้า มีดอกเบี้ย)` · `% หักหนี้ (จาก Booking)` · `จังหวัดบัญชีเกษตรกร` · `วันจ่ายปกติ` · `วันจ่ายจริง` · `จำนวนวันล่วงหน้า` · `ยอดสุทธิ` |
| context | `Crushing Season` · `Product: อ้อยสด` · `Base: 900.00 บาท/ตัน` |
| ปุ่ม | `บันทึก` · `เพิ่มช่วง` · `แก้ไข` · `ลบ` · `คำนวณ` |

## §6.8 Trace: AC → Logic
| AC | API | FN |
|---|---|---|
| AC-01..06 | API-03 | FN-02,DAILY |
| AC-07..08 | (calc) | FN-CCS |
| AC-09 | API-CH | — |
| AC-10 | API-03 | FN-02 |
| AC-11..17 | API-GS/WS | FN-SCHED |
| AC-18..21 | (preview) | FN-PREVIEW,INT,BANK |
| AC-22..23 | API-03 | FN-02,11 |
> Coverage FN-DAILY/CCS/INT/BANK + FN-11 unique-active + FN-SCHED ✅ · XT-01..05 ✅

## §6.6 Performance
save<1s · preview instant · unique Active + no-overlap enforce · daily_rate roundUp 7 · audit + optimistic lock · Thai พ.ศ. display / ISO store
