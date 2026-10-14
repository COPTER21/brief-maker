# 03_LOGIC — F-AGM-008 Debt Management

> R8: mutation API → ≥1 Function · allocation/ledger centralized · no HTTP in function

## §3.1 Functions
| FN | Name | Purpose | Invoked by |
|---|---|---|---|
| FN-01 | `searchQuotaForDebtor` (FN-AT-DEBT-359) | ค้นโควตา → existing debtor? → preview verified | API-04 |
| FN-02 | `createDebtor` (FN-SEQ-DEBT-360) | สร้างลูกหนี้ + idempotent per quota + snapshot | API-02 |
| FN-03 | `buildDebtorListQuery` | list + filter(status/aging) + stats + aging derive | API-01 |
| FN-OB | `createObligation` | source gating + date-order validate + ledger charge entry | API-OB1 |
| FN-ALLOC | `computeAllocation` (FN-AT-DEBT-370) ⭐ | **waterfall**: sort obligations by priority↑ → each: interest→penalty→principal → allocations[] + remaining | API-PAY1, FN-PAY |
| FN-PAY | `recordPayment` (FN-SEQ-DEBT-372) | validate→save · idempotent · emit ledger(payment) · update outstanding | API-PAY2 |
| FN-WO | `writeOff` (FN-AT-DEBT-375) ⭐ | amount≤outstanding + reason+confirm · **DOA>100k → PENDING_APPROVAL** · ledger(write_off) · status→written_off | API-WO1 |
| FN-ADJ | `postAdjustment` | อ้างอิงรายการเดิม + adjustment_type · principal อาจติดลบ · ledger(adjustment/reverse) | API-ADJ1 |
| FN-LED | `appendLedger` ⭐ | **double-entry**: dr/cr + running balance_after · append-only | ทุก FN mutation |
| FN-AGING | `computeAging` | จาก maturity/txn → bucket 0-30/31-60/61-90/90+ | FN-03, detail |
| FN-EXT | `getOutstandingByQuota` | read-only outstanding → CBM/Contract | API-EXT |
| FN-10 | `recordHistory` | audit append-only | ทุก FN |
| FN-11 | `guardMutation` | idempotency + optimistic(row_version) + RBAC + contract-lock(423) + DOA gate | FN-OB/PAY/WO/ADJ |

## §3.2 Engines
- **ENG-EXT-SRC** `debt-source-connector` [read] — Quota (verified) · Contract (contract_id 🔒)
- **ENG-LEDGER** `ledger-poster` ⭐ — double-entry posting + running balance · append-only (REVOKE UPDATE/DELETE)
- **ENG-ACCRUAL** `interest-penalty-accrual` [NEW/out-of-scope demo] — nightly simple_daily_365 (OQ-03)
- **ENG-DOC** `statement-generator` — export statement/CSV

## §3.3 API ↔ Logic Trace (R8)
| API | Functions |
|---|---|
| API-01 | FN-03,AGING |
| API-02 | FN-02,11,10,LED(charge?) |
| API-04 | FN-01 |
| API-OB1 | FN-OB,11,10,LED |
| API-PAY1 | FN-ALLOC |
| API-PAY2 | FN-PAY,ALLOC,11,10,LED |
| API-WO1 | FN-WO,11,10,LED |
| API-ADJ1 | FN-ADJ,11,10,LED |
| API-EXT | FN-EXT |
> ทุก mutation มี FN + FN-11 guard + FN-10 audit + FN-LED ledger ✅

## §3.5 Locked Decisions
- LOCK-03/04: FN-ALLOC waterfall (priority→ดอก→ค่าปรับ→ต้น) + validate-then-save (FN-PAY)
- LOCK-05: FN-WO DOA 100k → PENDING_APPROVAL
- LOCK-06: FN-11 contract-lock (423 LOCKED)
- LOCK-07: FN-ADJ reference origin + negative principal
- LOCK-08: FN-LED double-entry append-only
- LOCK-10: FN-EXT outstanding read (CBM/Contract)
