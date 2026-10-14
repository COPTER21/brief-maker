# 03_LOGIC — F-AGM-013 Cane Payment

> R8: mutation API → ≥1 Function · calc centralized (ENG-CALC shared with F-AGM-012) · no HTTP ใน function · formulas EXACT จาก payment-calculations.ts

## §3.1 Functions
| FN | Name | Purpose | Invoked by |
|---|---|---|---|
| FN-CCS-SYNC | `syncCcsSingle` | waiting_ccs → lookup legacy CCS → set ccs_value + status pending | API-03 |
| FN-CCS-SYNCALL | `syncCcsAll` | bulk over waiting_ccs → SyncAllResult {total,success,failed,details[]}; partial fail ไม่แตะแถว | API-04 |
| FN-PRICE ⭐ | `computeCanePrice` | `price_per_ton = base_price_ccs10 × [1 + (ccs_value − 10) × k_factor]` · cane_total_base = net_tons × price_per_ton | preview/confirm |
| FN-CANETYPE-ADJ ⭐ | `calculateCaneTypeAdjustment` | `= net_tons × adjustment_price_per_ton` (±) → cane_total_adjusted = base + adj — **หลัง CCS ก่อนแบ่งงวด**; code not found → 0 + warn | preview/confirm |
| FN-SPLIT | `splitInstallments` | inst{n}_amount = cane_total_adjusted × inst{n}_percent (50/50) | preview/confirm |
| FN-INSTALLMENT-PIPELINE ⭐ | `calculateInstallmentAmount` | **7 ขั้นตายตัว**: base → VAT → charges → หักหนี้ → ดอกเบี้ย(บิลขาว) → ค่าธนาคาร(โอน) → final | preview/confirm |
| FN-VAT | (in pipeline) | amount_tax_total = base × vatRate/100 · after_tax = base − tax | FN-INSTALLMENT-PIPELINE |
| FN-CHARGE | `calculateAdditionalChargeAmount` | FLAT → amount_per_unit · PER_TON → amount_per_unit × net_tons_inst; before_debt = after_tax − Σcharges | FN-INSTALLMENT-PIPELINE |
| FN-DEBT | (in pipeline) | desired = before_debt × debt%/100 · actual = min(desired, outstanding) · after_debt; โปรไม่หักหนี้ | FN-INSTALLMENT-PIPELINE |
| FN-INTEREST ⭐ | `calculateInterest` | บิลขาว: `daily_rate = interest%/100/base_days` · `days_early = max(0, ceil((normal−actual)/day))` · `interest = after_debt × daily_rate × days_early` · after_interest; GREEN/days_early=0 → 0 | FN-INSTALLMENT-PIPELINE |
| FN-BANKFEE ⭐ | `calculateBankFee` | โอน: branch==factory → in(IN_PROVINCE) · ต่าง → out(OUT_PROVINCE) · ไม่มี → out(UNKNOWN)+warn; เงินสด/เช็ค → 0 | FN-INSTALLMENT-PIPELINE |
| FN-PROMOTION | `computePromotion` | promo_amount = net_tons × promo_rate_per_ton; ไม่ใช้ CCS; ไม่แบ่งงวด; ไม่หักหนี้; แยกใบ | preview/confirm |
| FN-PAY ⭐ | `confirmPayment` | validate bill combo + method + due + bank account → save + **5-state transition** (waiting_ccs→pending→pending_inst2→pending_promotion→completed) + auto-switch งวด | API-06/12 |
| FN-PRINT | `printBill` | บิล INST1/INST2/PROMOTION | API-13 |
| FN-RECEIPT | `issueFinalReceipt` | ใบเสร็จรวม (completed only) | API-14 |
| FN-AUDIT | `recordAudit` | before/after append-only | ทุก mutation |
| FN-OPTIMISTIC | `guardOptimistic` | If-Match ETag + dedupe Idempotency-Key | pay/confirm/attach |
| FN-VALIDATE | `validateBillTypeCombination` | ห้าม inst1=WHITE & inst2=GREEN | FN-PAY, preview |

## §3.2 Exact Formulas (payment-calculations.ts)
```
price_per_ton   = base_price_ccs10 × [1 + (ccs_value − 10) × k_factor]
cane_total_base = net_tons × price_per_ton
cane_type_adj   = net_tons × adjustment_price_per_ton          (FRESH +10 / RATOON +5 / BURN −20 บาท/ตัน)
cane_total_adjusted = cane_total_base + cane_type_adj          (หลัง CCS ก่อนแบ่งงวด)
inst_amount     = cane_total_adjusted × inst_percent           (50/50)
─ pipeline ต่องวด ─
amount_tax_total = base × (vatRate/100);  after_tax = base − tax
charge_total = config + manual  (FLAT: per_unit · PER_TON: per_unit × net_tons_inst)
before_debt = after_tax − charge_total
desired = before_debt × (debt%/100);  actual = min(desired, outstanding);  after_debt = before_debt − actual
daily_rate = interest% / 100 / base_days
days_early = max(0, ceil((normal − actual)/day))
interest   = (WHITE) ? after_debt × daily_rate × days_early : 0
after_interest = after_debt − interest
bank_fee = (TRANSFER) ? feeByProvince : 0                       (default in=10 out=25)
amount_final = max(0, after_interest − bank_fee)
promo_amount = net_tons × promo_rate_per_ton
```

## §3.3 Engines
- **ENG-CALC** `payment-calc` ⭐ — price/canetype/split/pipeline/interest/bankfee (shared with F-AGM-012 Setting preview)
- **ENG-EXT-SETTING** `active-setting-provider` ⭐ — read active config จาก F-AGM-012 (API-EXT)
- **ENG-DEBT** `debt-connector` — call Debt service (bank_transfer/post-proof); 424 → keep receipt + retry queue
- **ENG-STORAGE** `file-storage` — upload proof (optional) → signed url
- **ENG-AUDIT** `audit-logger` — before/after append-only

## §3.4 API ↔ Logic Trace (R8)
| API | Functions |
|---|---|
| API-01/02 | (read) |
| API-03/04 | FN-CCS-SYNC / FN-CCS-SYNCALL, FN-AUDIT |
| API-06/12 | FN-VALIDATE, FN-PRICE, FN-CANETYPE-ADJ, FN-SPLIT, FN-INSTALLMENT-PIPELINE, FN-INTEREST, FN-BANKFEE, FN-PROMOTION, FN-PAY, FN-OPTIMISTIC, FN-AUDIT, ENG-DEBT |
| API-11 | FN-PRICE, FN-CANETYPE-ADJ, FN-SPLIT, FN-INSTALLMENT-PIPELINE, FN-INTEREST, FN-BANKFEE (non-persistent) |
| API-13 | FN-PRINT |
| API-14 | FN-RECEIPT (completed guard) |
| API-EXT | ENG-EXT-SETTING |
> ทุก mutation มี FN + FN-OPTIMISTIC + FN-AUDIT · calc centralized (ENG-CALC) ✅

## §3.5 Locked Decisions
- LOCK-02: FN-PRICE formula · LOCK-03: FN-CANETYPE-ADJ ก่อนแบ่งงวด · LOCK-04: FN-SPLIT 50/50
- LOCK-05: FN-INSTALLMENT-PIPELINE 7 ขั้น + final=max(0,…) · LOCK-06: FN-DEBT min + โปรไม่หักหนี้
- LOCK-07: FN-INTEREST บิลขาว only · LOCK-08: FN-BANKFEE province-based (in/out/unknown)
- LOCK-09: FN-VALIDATE ห้าม WHITE/GREEN · LOCK-10: FN-PROMOTION แยกใบ
- LOCK-11: FN-PAY 5-state transition (ไม่มี waiting_cash_proof) · LOCK-12: snapshot ณ confirm + FN-OPTIMISTIC + FN-AUDIT
> OQ-01: FN-INTEREST runtime ใช้ raw rate (Setting displays roundUp 7) — reconcile (invariants C-05).
