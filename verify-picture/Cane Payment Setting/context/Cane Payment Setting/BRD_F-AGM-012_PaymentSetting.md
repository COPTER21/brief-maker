# BRD — F-AGM-012 Cane Payment Setting (ตั้งค่าการจ่ายเงินอ้อย)

> Constraint mode (จาก invariants.md 🔒 · base FRD + Enhancement) · Module เกษตรกรรม (AGM) > Cane Payment · WKN · สถานะ: APPROVED

## §1 Business Context
หน้า **ตั้งค่าการจ่ายเงินอ้อย (Payment Setting)** — เป็น **แหล่งความจริง (source of truth)** ของค่าพื้นฐานทั้งหมดที่ **Cane Payment** ใช้คำนวณจ่ายจริง ต่อ 1 รอบหีบ (crushing season): ราคาอ้อยฐาน @10CCS, สูตร CCS (K), รายการหักเพิ่มเติม, ภาษี VAT, **ดอกเบี้ยบิลขาว**, **ค่าธนาคาร**, และ **ตารางวันจ่าย (บิลเขียว/บิลขาว)** + ทดสอบดูตัวอย่าง. เอกสารรวม **Enhancement** (Dump Result → flow จ่ายเงินใหม่: บิลเขียว-บิลขาว, งวด 1-2, หักหนี้, ดอกเบี้ย, ค่าธนาคาร).

## §2 Problem / Opportunity
ของเดิม: ตั้งค่า ราคา/CCS/charges/VAT/payout/preview. Flow จ่ายเงินใหม่ต้องการค่าพื้นฐานเพิ่ม (ดอกเบี้ยบิลขาว, ค่าธนาคารตามจังหวัด, ตารางวันจ่ายแยกบิลเขียว/บิลขาว). Refactor → CUBE Warm Light + Payment Setting เป็น SoT ครบทุกค่า.

## §3 Goals & Scope
### §3.4 Locked Decisions (LOCK — จาก invariants)
| LOCK | Decision |
|---|---|
| LOCK-01 | คงพฤติกรรม AS-BUILT (enhanced code) 100% + Enhancement เป็น truth · 6 sections config |
| LOCK-02 | **CCS formula**: ราคาต่อตัน = Base@10CCS + (CCS − 10) × (Base@10CCS × K) (BR-02) |
| LOCK-03 | งวด 1/2 = 50/50 (ค่าคงที่) (BR-03) · VAT ก่อนแบ่งงวด (BR-04) |
| LOCK-04 | **ดอกเบี้ยบิลขาว**: daily_rate = roundUp(rate_year/base_days, 7) · days_early = max(0, normal − actual) · interest = inst_after_debt × daily_rate × days_early (BR-05) |
| LOCK-05 | **บิลขาว WITH_CANE (พร้อมค่าอ้อย)** = ใช้วันจ่ายบิลเขียว + ไม่คิดดอกเบี้ย (BR-06) |
| LOCK-06 | Green = normal_pay_date งวด 1/2 · White = actual_pay_date (FIXED_DATE) (BR-07) |
| LOCK-07 | **ค่าธนาคารตามจังหวัด**: โอน + จังหวัดบัญชี=จังหวัดหลัก → in-fee · ต่าง → out-fee · เช็ค/เงินสด → 0 · หักหลังหักหนี้+ดอกเบี้ย (BR-08) |
| LOCK-08 | Payment Setting ไม่ fix วิธีจ่าย (เลือกตอนจ่ายจริง) (BR-09) |
| LOCK-09 | Preview non-persistent (BR-10) |
| LOCK-10 | unique Active per season×product · payout no-overlap (BR-11) |
| LOCK-11 | audit + optimistic lock (ETag/If-Match) ทุก mutation (BR-12) |

### Out of Scope
หน้าทำจ่ายจริง (Payment runtime) · CCS dump · multi-step approval · reporting · import/export.

## §4 Entities & State
- **PaymentSetting** (season×product): Active/Inactive · ถือ ราคา/K/interest/bank fee/VAT/charges
- **GreenSchedule / WhiteSchedule** (FIXED_DATE/WITH_CANE) · **AdditionalCharge**
State machine → invariants §4.

## §5 Key Business Rules
BR-01..12 (invariants §3). สำคัญ: SoT (BR-01), CCS formula (BR-02), ดอกเบี้ยบิลขาว (BR-05), WITH_CANE ไม่คิดดอกเบี้ย (BR-06), bank fee by province (BR-08), unique Active + no-overlap (BR-11).

## §6 Functional Requirements (สรุป → FRD)
1. **US-01 General** — สินค้า/หมายเหตุ + ดอกเบี้ยบิลขาว (rate/base_days/daily_rate) + ค่าธนาคาร (จังหวัดหลัก/in/out)
2. **US-02 CCS Delta** — ค่า K + สูตร + preview per CCS
3. **US-03 Additional Charges** — table (ชื่อ/ประเภท/ค่า/หมายเหตุ) add/edit/delete/reorder
4. **US-04 Tax** — VAT switch + rate (ก่อนแบ่งงวด)
5. **US-05 Payout Schedule** — 2 sub-tab (บิลเขียว/บิลขาว) + modal (ประเภทวันจ่าย FIXED_DATE/WITH_CANE)
6. **US-06 Preview & Test** — inputs (CCS/น้ำหนัก/วันที่/บิลงวด1-2/หักหนี้/จังหวัด) → outputs (ราคา/ยอด/วันจ่าย/ดอกเบี้ย/ค่าธนาคาร/สุทธิ)
7. **US-07 Save/Deactivate** — บันทึก + unique Active + validate
8. **US-08 Cross-module** — feed Cane Payment (active setting)

## §7 Non-Functional
config save<1s · preview calc instant · unique Active + no-overlap enforce · audit + optimistic lock · daily_rate ปัดขึ้น 7 ตำแหน่ง · RBAC (4 roles) · Thai date พ.ศ. display / ISO store.

## §18 Stats (context bar)
Crushing Season · Product (อ้อยสด) · Base @10CCS (900.00 บาท/ตัน) · Status.

## §Cross-Module Map
```
Season/Product/Price List ──read──▶ Payment Setting (season×product, Base@10CCS)
Payment Setting (F-AGM-012) ──active config──▶ Cane Payment runtime
  (K/interest/bank fee/VAT/charges/green-white pay dates → คำนวณจ่ายจริง)
Receiving (F-AGM-011) ──net_weight + cane_type──▶ Cane Payment (ใช้ config นี้)
```
