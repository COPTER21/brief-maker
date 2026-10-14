# 03_LOGIC — F-AGM-012 Cane Payment Setting

> R8: mutation API → ≥1 Function · calc/validation centralized · no HTTP ใน function

## §3.1 Functions
| FN | Name | Purpose | Invoked by |
|---|---|---|---|
| FN-01 | `loadSettingBySeason` | อ่าน setting + green/white + charges | API-01 |
| FN-02 | `saveSetting` ⭐ | validate + **compute dailyRate** + no-overlap + unique Active + audit + If-Match | API-03/04 |
| FN-DAILY | `computeDailyRate` ⭐ | roundUp(rate_year / base_days, scale=7, ROUND_UP) | FN-02, General preview |
| FN-CCS | `computeCcsPrice` ⭐ | ราคาต่อตัน = Base@10CCS + (CCS − 10) × (Base@10CCS × K) | CCS Delta, Preview |
| FN-PREVIEW | `computePreview` ⭐ | จาก inputs → per-งวด: normal/actual pay date, days_early, debt, interest (บิลขาว), bank fee (province), amount_final · VAT ก่อนแบ่งงวด | Preview & Test |
| FN-INT | `computeInterest` ⭐ | days_early = max(0, normal − actual) · interest = inst_after_debt × daily_rate × days_early · WITH_CANE → 0 | FN-PREVIEW, Payment runtime |
| FN-BANK | `computeBankFee` ⭐ | โอน + จังหวัดบัญชี=จังหวัดหลัก → in-fee · ต่าง → out-fee · เช็ค/เงินสด → 0 · หักหลังหักหนี้+ดอกเบี้ย | FN-PREVIEW, Payment runtime |
| FN-SCHED | `validateSchedule` | green/white: from≤to (1–31), pay dates, FIXED_DATE⇒payDate/WITH_CANE⇒null, no-overlap | FN-02, API-GS/WS |
| FN-DUP | `duplicateSetting` | month-adjust payout + unique Active | API-05 |
| FN-DEACT | `deactivateSetting` | Active → Inactive + guard | API-06 |
| FN-10 | `recordAudit` | audit before/after | ทุก mutation |
| FN-11 | `guardOptimistic` | If-Match ETag + unique Active | FN-02/DUP/DEACT |

## §3.2 Engines
- **ENG-EXT-MASTER** `season-product-price-connector` [read] — Season/Product/Price List (Base @10CCS)
- **ENG-CALC** `payment-calc` ⭐ — CCS price + interest + bank fee + VAT + งวด 50/50 (shared with Payment runtime)
- **ENG-EXPOSE** `active-setting-provider` ⭐ — expose active setting → Cane Payment (API-EXT)
- **ENG-AUDIT** `audit-logger` — before/after append-only

## §3.3 API ↔ Logic Trace (R8)
| API | Functions |
|---|---|
| API-01/02 | FN-01 |
| API-03/04 | FN-02,DAILY,SCHED,11,10 |
| API-05 | FN-DUP,11,10 |
| API-06 | FN-DEACT,11,10 |
| API-EXT | FN-01 (ENG-EXPOSE) |
| (preview UI) | FN-PREVIEW,CCS,INT,BANK,DAILY |
> ทุก mutation มี FN + FN-11 optimistic + FN-10 audit · calc centralized (ENG-CALC) ✅

## §3.5 Locked Decisions
- LOCK-02: FN-CCS formula
- LOCK-04: FN-DAILY roundUp 7 + FN-INT (บิลขาว only)
- LOCK-05: FN-INT WITH_CANE → 0
- LOCK-07: FN-BANK province-based
- LOCK-08: payment method not fixed (FN-PREVIEW ตาม input)
- LOCK-10: FN-02 unique Active + FN-SCHED no-overlap
- LOCK-11: FN-11 optimistic + FN-10 audit
