# 06_TESTS — F-AGM-013 Cane Payment

> Audience: QA + ai-testcase-md-generator · microcopy-aware · pipeline/interest/bank-fee/bill-case heavy

## §6.1 Acceptance Criteria

### List / Tabs / Export (US-01)
- **AC-01** 3 tabs: รอความหวาน (waiting_ccs) · รอทำจ่าย (pending/inst2/promotion) · เสร็จสิ้น (completed) + count
- **AC-02** columns: เลขที่ · เกษตรกร (masked) · **ประเภทอ้อย** badge · **บิลงวด 1/2** badge · promo badge · CCS · สถานะ
- **AC-03** ค้นหา scale_ticket_no/quota_no/farmer_name + กรอง season/product/checkin_type/unload_date
- **AC-04** Export CSV → `cane_payments_{tab}_{YYYYMMDD}.csv`

### Sync CCS (US-02)
- **AC-05** Sync CCS เดี่ยว (waiting_ccs) → ccs_value set + status pending
- **AC-06** Sync CCS ซ้ำ → 409 "รายการนี้ได้ทำการดึงค่า CCS แล้ว"
- **AC-07** Sync All → progress modal + summary {total/success/failed} + details[]; ไม่มี waiting_ccs → "ไม่มีรายการที่สถานะ waiting_ccs"

### All-in-One Modal (US-03)
- **AC-08** 3 tabs: งวดที่ 1 · งวดที่ 2 · โปรโมชัน (แสดงเฉพาะมีโปร)
- **AC-09** step calc แสดง 7 ขั้น: มูลค่าอ้อย → ปรับประเภทอ้อย → VAT → charges → หักหนี้ → ดอกเบี้ย → ค่าธนาคาร → ยอดสุทธิ

### Step calc รายขั้น
- **AC-10** มูลค่าอ้อย: price_per_ton = base@10CCS × [1+(CCS−10)×K] · cane_total_base = net_tons × price_per_ton
- **AC-11** ปรับประเภทอ้อย: adj = net_tons × ±บาท/ตัน (FRESH +10 / RATOON +5 / BURN −20) → adjusted **ก่อนแบ่งงวด**
- **AC-12** cane_type ไม่พบ → adj = 0 + "⚠️ ไม่มีข้อมูลประเภทอ้อย"
- **AC-13** VAT: tax = base × vatRate/100 · after_tax = base − tax
- **AC-14** charge FLAT: amount = per_unit
- **AC-15** charge PER_TON: amount = per_unit × net_tons_inst (net_tons × inst_percent)
- **AC-16** หักหนี้: desired = before_debt × debt% · actual = min(desired, outstanding)
- **AC-17** ดอกเบี้ยบิลขาว: interest = after_debt × daily_rate × days_early (daily_rate = interest%/100/base_days)
- **AC-18** days_early = 0 → interest 0 "ไม่คิดดอกเบี้ย"
- **AC-19** ค่าธนาคาร: จังหวัดสาขา=โรงงาน → IN_PROVINCE(in fee) · ต่าง → OUT_PROVINCE(out fee) · ไม่มี → UNKNOWN(out fee) + warning
- **AC-20** ยอดสุทธิ: final = max(0, after_interest − bank_fee); clamp ที่ 0

### Bill cases (US-03)
- **AC-21** Case A GREEN/GREEN → ดอกเบี้ย 0 ทั้ง 2 งวด
- **AC-22** Case B GREEN/WHITE → งวด 2 มีดอกเบี้ย
- **AC-23** Case C WHITE/WHITE → งวด 1 white schedule + งวด 2 พร้อมงวด 1
- **AC-24** WHITE/GREEN → block "ไม่อนุญาตให้งวด 1 เป็นบิลขาว…และงวด 2 เป็นบิลเขียว จ่ายตามงวด"

### Pay methods / auto-switch / promotion (US-03)
- **AC-25** 3 วิธีจ่าย: โอน (bank fee + ต้องมี bank_account quota) · เงินสด (fee 0) · เช็ค (fee 0 + เลขเช็ค)
- **AC-26** ยืนยันงวด 1 สำเร็จ → modal ไม่ปิด → auto ไป tab งวด 2 → ยืนยันทำจ่ายทั้งหมด (/confirm)
- **AC-27** บิลโปรโมชัน: promo = net_tons × โปร/ตัน · ไม่ใช้ CCS · ไม่หักหนี้ · แยกใบ → pending_promotion

### Detail / Print / Receipt (US-04/08)
- **AC-28** Drawer 5 tabs (Summary/งวด1/งวด2/โปร/Timeline) + breakdown + หลักฐาน (optional)
- **AC-29** พิมพ์: บิลงวด 1 · บิลงวด 2 · บิลโปรโมชัน · ใบเสร็จรวม (completed เท่านั้น)

### RBAC / Concurrency (NFR)
- **AC-30** RBAC: pay โอน = Finance Officer/Admin · pay เงินสด = Cashier/Finance · unmask bank = Finance/Admin · insufficient → 403
- **AC-31** stale ETag ตอน pay → 412/409 CONFLICT_UPDATE_STALE · Idempotency-Key dedupe (pay/confirm/sync-all)
- **AC-32** pay ก่อน due → 422 PAYMENT_NOT_DUE · Quota+โอน ไม่มี bank → 422 BANK_ACCOUNT_MISSING · Debt fail → 424 keep receipt + retry

## §6.2 Cross-Module / Event (XT)
| XT | Scenario | Source | Expected |
|---|---|---|---|
| XT-01 | อ่าน active setting (K/base/interest/bankFee/schedule/VAT/charges/cane type/factory province) | F-AGM-012 (API-EXT) | config ที่ใช้คำนวณ |
| XT-02 | net_tons + cane_type | Receiving F-AGM-011 | ป้อนมูลค่า + ปรับประเภทอ้อย |
| XT-03 | ccs_value | Legacy CCS API | Sync CCS |
| XT-04 | debt deduct | Debt F-AGM-008 | หักหนี้ + 424 retry |
| XT-05 | bank_branch_province_code | Quota/Farmer bank | bank fee in/out/unknown |
| XT-06 | events | emit | ccs.synced · installment.paid · completed |

## §6.3 Microcopy-Aware Expected (verbatim)
| จุด | ข้อความ |
|---|---|
| bill labels | `บิลเขียว จ่ายตามงวด` · `บิลขาว (เงินยืมระหว่างงวด)` |
| cane type | `อ้อยสด` · `อ้อยตอ` · `อ้อยไฟไหม้` |
| tabs | `รอความหวาน` · `รอทำจ่าย` · `เสร็จสิ้น` · `งวดที่ 1` · `งวดที่ 2` · `โปรโมชัน` |
| steps | `มูลค่าอ้อย` · `ปรับประเภทอ้อย` · `VAT / ภาษี` · `หักหนี้` · `ดอกเบี้ย` · `ค่าธนาคาร` · `ยอดสุทธิ` |
| warnings | `⚠️ ไม่มีข้อมูลประเภทอ้อย` · `⚠️ ไม่มีข้อมูลจังหวัดสาขาธนาคาร - ใช้อัตราต่างจังหวัดเป็น default` · `ไม่คิดดอกเบี้ย` |
| promo badge | `ไม่มีโปร` · `รอจ่ายโปร` · `จ่ายโปรแล้ว` |
| errors | `รายการนี้ได้ทำการดึงค่า CCS แล้ว` · `ยังไม่ถึงวันที่กำหนดชำระ` · `บัญชีธนาคารสำหรับรายการนี้ยังไม่ระบุ` · `ไม่อนุญาตให้งวด 1 เป็นบิลขาว (เงินยืมระหว่างงวด) และงวด 2 เป็นบิลเขียว จ่ายตามงวด` |
| method | `โอน` · `เงินสด` · `เช็ค` · `ยืนยันทำจ่ายทั้งหมด` |

## §6.4 Trace: AC → FN
| AC | API | FN |
|---|---|---|
| AC-01..04 | API-01/05 | (read) |
| AC-05..07 | API-03/04 | FN-CCS-SYNC, FN-CCS-SYNCALL |
| AC-10 | API-11 | FN-PRICE |
| AC-11..12 | API-11 | FN-CANETYPE-ADJ |
| AC-13 | API-11 | FN-VAT |
| AC-14..15 | API-11 | FN-CHARGE |
| AC-16 | API-11 | FN-DEBT |
| AC-17..18 | API-11 | FN-INTEREST |
| AC-19 | API-11 | FN-BANKFEE |
| AC-20 | API-11/12 | FN-INSTALLMENT-PIPELINE |
| AC-21..24 | API-12 | FN-VALIDATE, FN-INSTALLMENT-PIPELINE |
| AC-25..27 | API-12 | FN-PAY, FN-PROMOTION |
| AC-28..29 | API-02/13/14 | FN-PRINT, FN-RECEIPT |
| AC-30..32 | API-06/12 | FN-PAY, FN-OPTIMISTIC, ENG-DEBT |
> Coverage: 7-step pipeline (AC-09..20) + 3 bill cases + WHITE/GREEN block + 5-status ✅ · XT-01..06 ✅

## §6.5 Performance
list P95 ≤300ms · write ≤500ms · bulk sync ≤500/job · amount_final ≥0 clamp · Idempotency + optimistic (409/412) · Debt 424 retry · bank masked (RBAC) · Thai i18n · Thai date display.
