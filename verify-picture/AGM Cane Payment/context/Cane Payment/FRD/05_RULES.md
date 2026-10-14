# 05_RULES — F-AGM-013 Cane Payment

## §5.1 Business Rules (→ invariants §3 BR-01..19)
| BR | Rule |
|---|---|
| BR-01 | price_per_ton = base_price_ccs10 × [1 + (ccs_value − 10) × k_factor] |
| BR-02 | cane_total_base = net_tons × price_per_ton |
| BR-03 | cane_type_adjustment_total = net_tons × adjustment_price_per_ton (±); adjusted = base + adj — **หลัง CCS ก่อนแบ่งงวด** |
| BR-04 | Split: inst{n} = cane_total_adjusted × inst{n}_percent (50/50) |
| BR-05 | **Pipeline ต่องวด ตายตัว 7 ขั้น:** base → VAT → charges (config+manual) → หักหนี้ → ดอกเบี้ย(บิลขาว) → ค่าธนาคาร(โอน) → final |
| BR-06 | VAT: amount_tax_total = base × vatRate/100; after_tax = base − tax |
| BR-07 | Charge FLAT → per_unit · PER_TON → per_unit × net_tons_inst (net_tons × inst_percent); before_debt = after_tax − Σ |
| BR-08 | Debt: desired = before_debt × debt%/100; actual = min(desired, outstanding); **โปรไม่หักหนี้** |
| BR-09 | Interest (บิลขาว): daily_rate = interest%/100/base_days; days_early = max(0, ceil((normal−actual)/day)); interest = after_debt × daily_rate × days_early; GREEN/days_early=0 → "ไม่คิดดอกเบี้ย" |
| BR-10 | Bank fee (โอน): branch==factory → in(IN_PROVINCE) · ต่าง → out(OUT_PROVINCE) · ไม่มี → out(UNKNOWN); เงินสด/เช็ค → 0 |
| BR-11 | final = max(0, after_interest − bank_fee) |
| BR-12 | Bill cases: A GREEN/GREEN · B GREEN/WHITE · C WHITE/WHITE · **ห้าม WHITE/GREEN** |
| BR-13 | Promotion: promo = net_tons × promo_rate_per_ton; ไม่ใช้ CCS; ไม่แบ่งงวด; แยกใบ; หลังงวด 1+2 ครบ |
| BR-14 | 1 การส่งอ้อย = สูงสุด 3 บิล (งวด1 · งวด2 · โปร) + ใบเสร็จรวม (completed) |
| BR-15 | Sync CCS เดี่ยว+bulk: waiting_ccs → ccs_value + pending; bulk = SyncAllResult |
| BR-16 | Debt integration: bank_transfer/post-proof → Debt service; 424 → keep receipt + banner + retry |
| BR-17 | Snapshot ประเภทอ้อย + จังหวัดสาขา ณ confirm |
| BR-18 | Idempotency-Key + If-Match/ETag ทุก mutation |
| BR-19 | Export CSV sync: `cane_payments_{tab}_{YYYYMMDD}.csv` |

## §5.2 State Machine (5 states → invariants §4)
`waiting_ccs` → (Sync CCS) → `pending` → (pay inst1 any method) → `pending_inst2` → (pay inst2) → มีโปร ? `pending_promotion` → (pay promo) → `completed` : `completed`.
AA (inst2=null): pending → completed. Per-installment: pending → paid.
> **ไม่มี waiting_cash_proof** — proof optional, ทุกวิธีจ่าย transition ทันที (invariants C-01).

## §5.3 Permission (RBAC → invariants §6)
| Action | Roles |
|---|---|
| view list/detail | ทุก role (Cane Office Clerk, Accounting, Finance Officer, Cashier, System Admin) |
| sync CCS / sync all | Finance Officer, Cashier, System Admin |
| pay (bank_transfer) | Finance Officer, System Admin |
| pay (cash) | Cashier, Finance Officer |
| export CSV | Accounting, Finance Officer, System Admin |
| unmask bank_account | Finance Officer, System Admin (PII) |
> insufficient → redirect list + toast "403: สิทธิ์ไม่เพียงพอ" / "คุณไม่มีสิทธิ์ดำเนินการนี้".

## §5.4 Validation (VR-01..13 → invariants §2)
| VR | Rule | Message |
|---|---|---|
| VR-01 | ห้าม inst1=WHITE & inst2=GREEN | "ไม่อนุญาตให้งวด 1 เป็นบิลขาว (เงินยืมระหว่างงวด) และงวด 2 เป็นบิลเขียว จ่ายตามงวด" |
| VR-02 | scale_ticket_no `^\d{4}$` (eligibility Sync CCS) | — |
| VR-03 | pay only when today ≥ due date | "ยังไม่ถึงวันที่กำหนดชำระ" |
| VR-04 | Quota + โอน ต้องมี bank_account | "บัญชีธนาคารสำหรับรายการนี้ยังไม่ระบุ" |
| VR-05 | CHEQUE ต้องมี cheque_number | — |
| VR-06 | amount_final ≥ 0 (clamp 0) | — |
| VR-07 | proof jpg/png/pdf ≤5MB (optional) | "ไฟล์ต้องเป็น jpg/png/pdf ขนาดไม่เกิน 5MB" |
| VR-08 | filter params valid | "พารามิเตอร์ตัวกรองไม่ถูกต้อง" |
| VR-09 | Sync CCS only when waiting_ccs | "รายการนี้ได้ทำการดึงค่า CCS แล้ว" (409) |
| VR-10 | Sync All ต้องมี ≥1 waiting_ccs | "ไม่มีรายการที่สถานะ waiting_ccs" |
| VR-11 | final-receipt only when completed | — |
| VR-12 | cane_type_code not in master → adj 0 + warn | "⚠️ ไม่มีข้อมูลประเภทอ้อย" |
| VR-13 | bank_branch_province_code empty → OUT default + warn | "⚠️ ไม่มีข้อมูลจังหวัดสาขาธนาคาร - ใช้อัตราต่างจังหวัดเป็น default" |

## §5.5 Edge Cases
| EC | Case | Expected |
|---|---|---|
| EC-01 | inst1=WHITE, inst2=GREEN | VR-01 block |
| EC-02 | cane_type not found | adj = 0 + "⚠️ ไม่มีข้อมูลประเภทอ้อย" |
| EC-03 | ไม่มี branch province | bank_fee_type=UNKNOWN + out fee + warning |
| EC-04 | days_early = 0 (จ่ายตรงวัน/ช้า) | interest = 0 "ไม่คิดดอกเบี้ย" |
| EC-05 | GREEN bill | ไม่มีดอกเบี้ย |
| EC-06 | after_interest − bank_fee < 0 | amount_final = max(0,…) = 0 |
| EC-07 | pay ก่อนถึง due | 422 PAYMENT_NOT_DUE |
| EC-08 | Quota + โอน ไม่มี bank_account | 422 BANK_ACCOUNT_MISSING |
| EC-09 | stale ETag ตอน pay | 412/409 CONFLICT_UPDATE_STALE |
| EC-10 | Sync CCS ซ้ำ | 409 CCS_ALREADY_SYNCED |
| EC-11 | เงินสด/เช็ค | bank_fee = 0 |
| EC-12 | promotion | ไม่หักหนี้ · แยกใบ · pending_promotion |
| EC-13 | Debt API fail | 424 → keep receipt + banner + retry (ไม่ถอนใบเสร็จ) |
| EC-14 | AA (inst2=null) | pending → completed (ไม่มีงวด 2) |

## §5.6 Error Catalog
VALIDATION_FAILED(400) · UNAUTHORIZED/INSUFFICIENT_ROLE(401/403) "คุณไม่มีสิทธิ์ดำเนินการนี้" · NOT_FOUND/CCS_NOT_FOUND(404) · CCS_ALREADY_SYNCED(409) "รายการนี้ได้ทำการดึงค่า CCS แล้ว" · CONFLICT_UPDATE_STALE(409/412) "ข้อมูลล้าสมัย กรุณารีเฟรชแล้วลองใหม่" · PAYMENT_NOT_DUE(422) "ยังไม่ถึงวันที่กำหนดชำระ" · BANK_ACCOUNT_MISSING(422) "บัญชีธนาคารสำหรับรายการนี้ยังไม่ระบุ" · UNSUPPORTED_FILE_TYPE/FILE_TOO_LARGE(422) · DEBT_API_ERROR(424) · STORAGE_UPLOAD_FAILED/RECEIPT_ISSUE_FAILED(5xx).
