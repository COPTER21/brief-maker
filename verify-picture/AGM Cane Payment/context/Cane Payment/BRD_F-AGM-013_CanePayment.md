# BRD — F-AGM-013 Cane Payment (การทำจ่ายเงินอ้อย)

> Constraint mode (จาก invariants.md 🔒 · base FRD/UI/API-DB/Testcase + Enhancement v2/v3.1/v4.1) · Module เกษตรกรรม (AGM) > Cane Payment · WKN · สถานะ: APPROVED

## §1 Business Context
หน้า **การทำจ่ายเงินอ้อย (Cane Payment)** — ตัวรัน (runtime) ที่นำ config จาก **Payment Setting (F-AGM-012)** มาคำนวณและ **ทำจ่ายเงินอ้อยให้เกษตรกรจริง** ต่อ 1 ใบรับอ้อย: Sync ค่าความหวาน (CCS) → คำนวณมูลค่าอ้อย → **ปรับตามประเภทอ้อย** → แบ่ง **งวด 1/2 (50/50)** → หัก VAT/ภาษี, รายการหัก, **หักหนี้**, **ดอกเบี้ย (บิลขาว)**, **ค่าธนาคาร (ตามจังหวัดสาขา)** → ยอดสุทธิ → เลือก **วิธีจ่าย (โอน/เงินสด/เช็ค)** → ออกบิล/ใบเสร็จ. รองรับ **บิลโปรโมชันแยกใบ** และ **ใบเสร็จการจ่ายเงินอ้อยรวม**. เป็น feature ที่ผ่าน enhancement 3 รอบ (v2 โปรโมชัน → v3.1 บิลเขียว/ขาว+วิธีจ่าย+pipeline → v4.1 ประเภทอ้อย+ค่าธนาคารจังหวัดสาขา = SSoT ล่าสุด).

## §2 Problem / Opportunity
ของเดิม (base): จ่ายเงินอ้อยรายการเดียว — Sync CCS → net_amount → make payment (โอน/เงินสด) → รอหลักฐานเงินสด → ใบเสร็จ. ธุรกิจจริงต้องการ **2 งวด**, **บิลเขียว/บิลขาว** (เงินยืมล่วงหน้า + ดอกเบี้ย), **3 วิธีจ่าย**, **บิลโปรโมชันแยก**, **ปรับตามประเภทอ้อย**, **ค่าธนาคารตามจังหวัดสาขา** + breakdown แบบ step ที่ตรวจย้อนหลังได้. Refactor → CUBE Warm Light + pipeline การคำนวณตายตัว 7 ขั้น.

## §3 Goals & Scope
### §3.4 Locked Decisions (LOCK — จาก invariants)
| LOCK | Decision |
|---|---|
| LOCK-01 | คงพฤติกรรม AS-BUILT (enhanced code v4.1) 100% · enhancement = truth · List + All-in-One payment modal (3 tabs) + Detail drawer |
| LOCK-02 | **มูลค่าอ้อย**: price_per_ton = base@10CCS × [1 + (CCS − 10) × K]; cane_total_base = net_tons × price_per_ton (BR-01/02) |
| LOCK-03 | **ปรับประเภทอ้อย**: adj_total = net_tons × adj_price_per_ton (±) → cane_total_adjusted = base + adj — **หลัง CCS ก่อนแบ่งงวด** (BR-03) |
| LOCK-04 | แบ่งงวด: inst{n} = cane_total_adjusted × inst{n}_percent (50/50) (BR-04) |
| LOCK-05 | **Pipeline ต่องวด (ตายตัว):** base → VAT/ภาษี → additional charges (config+manual, FLAT/PER_TON) → หักหนี้ → ดอกเบี้ย(บิลขาว) → ค่าธนาคาร(โอน) → สุทธิ; final = max(0, …) (BR-05/06/07/11) |
| LOCK-06 | **หักหนี้**: desired = before_debt × debt%; actual = min(desired, outstanding); โปรโมชัน**ไม่หักหนี้** (BR-08) |
| LOCK-07 | **ดอกเบี้ย (บิลขาว only)**: daily_rate = interest%/base_days; days_early = max(0, normal − actual); interest = after_debt × daily_rate × days_early; GREEN/days_early=0 → "ไม่คิดดอกเบี้ย" (BR-09) |
| LOCK-08 | **ค่าธนาคาร (โอน only)**: branch_province==factory → in-fee (IN_PROVINCE) · ต่าง → out-fee (OUT_PROVINCE) · ไม่มี → out (UNKNOWN) + warning · เงินสด/เช็ค → 0 (BR-10) |
| LOCK-09 | **บิล 3 กรณี**: A GREEN/GREEN · B GREEN/WHITE · C WHITE/WHITE · **ห้าม WHITE/GREEN** (BR-12/VR-01) |
| LOCK-10 | **โปรโมชันแยกใบ**: promo = net_tons × โปร/ตัน; ไม่ใช้ CCS; ไม่แบ่งงวด; เข้าหลังงวด 1+2 ครบ (BR-13) |
| LOCK-11 | **สถานะ 5 states (v4.1)**: waiting_ccs → pending → pending_inst2 → pending_promotion → completed · **ไม่มี waiting_cash_proof** (proof optional) (§4/C-01) |
| LOCK-12 | Snapshot ประเภทอ้อย + จังหวัดสาขา ตอน confirm · Idempotency + If-Match/ETag ทุก mutation (BR-17/18) |
| LOCK-13 | เอกสาร: บิลงวด 1/2 · บิลโปรโมชัน · **ใบเสร็จการจ่ายเงินอ้อยรวม** (completed) (BR-14) |

### Out of Scope
Payment Setting UI/schema (F-AGM-012) · Debt Management internals · Quota bank-branch-province capture (upstream) · CCS legacy source · Receiving/Booking capture · reporting/BI.

## §4 Entities & State
- **Payment** (1 ใบรับอ้อย): header + weights/ccs/pricing/amounts/debt/installments/charges/bank/cane_type
- **Installment 1/2** (InstallmentDetails) · **Promotion** (แยกใบ) · **AdditionalCharge** (config/manual, FLAT/PER_TON)
State machine → invariants §4 (5 states; per-installment pending→paid).

## §5 Key Business Rules
BR-01..19 (invariants §3). สำคัญ: pipeline 7 ขั้น (BR-05), ปรับประเภทอ้อยก่อนแบ่งงวด (BR-03), ดอกเบี้ยบิลขาว (BR-09), ค่าธนาคารจังหวัดสาขา (BR-10), โปรโมชันแยกใบไม่หักหนี้ (BR-13/08), ห้าม WHITE/GREEN (BR-12), 5-status ไม่มี waiting_proof (§4).

## §6 Functional Requirements (สรุป → FRD)
1. **US-01 List** — tabs ตามสถานะ (รอความหวาน/รอทำจ่าย/เสร็จสิ้น) + คอลัมน์ (เลขที่/เกษตรกร/ประเภทอ้อย/บิลงวด1-2/สถานะ/promo badge) + ค้นหา/กรอง + Export CSV
2. **US-02 Sync CCS** — เดี่ยว (modal) + Sync All (bulk progress + summary total/success/failed)
3. **US-03 ทำจ่าย (All-in-One modal)** — 3 tabs (งวด1/งวด2/โปรโมชัน) + step calc + เลือกวิธีจ่าย (โอน/เงินสด/เช็ค) + ยืนยันทีละงวด → auto-switch งวด 1→2 → ยืนยันทั้งหมด
4. **US-04 Detail Drawer** — Summary/งวด1/งวด2/โปรโมชัน/Timeline + breakdown + หลักฐานไฟล์แนบ + ปุ่มพิมพ์
5. **US-05 ประเภทอ้อย** — แสดง + ปรับเงิน ±บาท/ตัน (FRESH/RATOON/BURN)
6. **US-06 ค่าธนาคารจังหวัดสาขา** — เปรียบเทียบจังหวัดโรงงาน vs สาขาธนาคาร → in/out/unknown + warning
7. **US-07 Additional charges** — FLAT/PER_TON (config read-only + manual add/remove ต่องวด)
8. **US-08 พิมพ์เอกสาร** — บิลงวด 1/2, บิลโปรโมชัน, ใบเสร็จรวม (completed)
9. **US-09 Cross-module** — อ่าน active setting (F-AGM-012) + receiving (net_tons/cane_type) + debt deduct + CCS

## §7 Non-Functional
List P95 ≤300ms · write ≤500ms · bulk sync ≤500/job · amount_final ≥0 clamp · Idempotency + optimistic lock (409/412) · Debt 424 → keep receipt + retry · bank account masked (PII, RBAC unmask) · RBAC 5 roles · Thai i18n error messages · Thai date display.

## §18 Stats / List summary
สถานะ tabs + count · ประเภทอ้อย column · promo badge (ไม่มีโปร/รอจ่ายโปร/จ่ายโปรแล้ว).

## §Cross-Module Map
```
Payment Setting (F-AGM-012, active) ──config──▶ Cane Payment (base@10CCS, K, green/white schedule, interest, bank fee, VAT, charges, cane type master, factory province)
Receiving (F-AGM-011) ──net_tons + cane_type──▶ Cane Payment
Quota/Farmer bank info ──bank_branch_province_code──▶ Cane Payment (bank fee)
CCS legacy API ──ccs_value──▶ Cane Payment (Sync CCS)
Cane Payment ──deduct──▶ Debt Management (F-AGM-008)
Cane Payment ──บิลงวด1/2 + บิลโปร + ใบเสร็จรวม──▶ เกษตรกร
```
