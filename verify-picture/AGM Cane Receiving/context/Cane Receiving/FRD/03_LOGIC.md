# 03_LOGIC — F-AGM-011 Cane Receiving

> R8: mutation API → ≥1 Function · side-effects/idempotency centralized · no HTTP ใน function

## §3.1 Functions
| FN | Name | Purpose | Invoked by |
|---|---|---|---|
| FN-01 | `buildReceivingListQuery` | list (tab draft/issued/void) + filter + stats | API-01 |
| FN-DUMP | `fetchFactoryDump` ⭐ | GET /ext/factory/dump v2 (checkin_datetime+coin+quota) → map caneType/times/weights · net = gross−tare ถ้าไม่ส่ง | API-DUMP |
| FN-C1 | `issueReceiving` ⭐ | validate (auto ready / manual net+reason) + สร้าง CRN + **side effects** (CBM awaiting_payment, free coin, PDF) + dump snapshot | API-C1 |
| FN-SYNC | `syncAllReceivings` ⭐ | date range required + lock · select Draft → loop: FN-DUMP → SUCCESS = FN-C1 · fail = collect error · summary | API-SYNC |
| FN-V | `voidReceiving` | reason≥5 + block-if-paid + status Void + rollback CBM awaiting_dump_result | API-V |
| FN-PDF | `generateReceivingPdf` | A4 + QR (idempotent) | API-PDF, FN-C1 |
| FN-SIDE | `applyIssueSideEffects` ⭐ | PATCH CBM + free coin + emit events · atomic-ish + compensation | FN-C1 |
| FN-VALID | `validateManualDump` | net regex `^\d+(\.\d{1,2})?$` non-neg + reason required | FN-C1 |
| FN-10 | `recordReceivingAudit` | append audit + dump snapshot | ทุก FN |
| FN-11 | `guardIdempotency` ⭐ | X-Idempotency-Key (create + sync-all) + etag optimistic | FN-C1/SYNC |

## §3.2 Engines
- **ENG-FACTORY** `factory-dump-connector` ⭐ — GET /ext/factory/dump v2 · timezone Asia/Bangkok · map raw
- **ENG-CBM** `cbm-status-connector` — PATCH awaiting_payment / awaiting_dump_result
- **ENG-COIN** `weigh-coin-connector` — POST /weigh-coin/free
- **ENG-PDF** `receiving-doc-generator` — A4 ไทย + QR
- **ENG-PAY-FEED** `payment-feed` — expose net_weight + cane_type (SoT) ให้ Payment

## §3.3 API ↔ Logic Trace (R8)
| API | Functions |
|---|---|
| API-01/02 | FN-01 |
| API-DUMP | FN-DUMP (ENG-FACTORY) |
| API-C1 | FN-C1,VALID,SIDE,PDF,11,10 |
| API-SYNC | FN-SYNC,DUMP,C1,SIDE,11,10 |
| API-V | FN-V,10 (ENG-CBM) |
| API-PDF | FN-PDF (ENG-PDF) |
> ทุก mutation มี FN + FN-11 idempotency + FN-10 audit · issue → FN-SIDE (CBM+coin+PDF) ✅

## §3.5 Locked Decisions
- LOCK-02: FN-DUMP v2 (checkin_datetime+coin+quota, no CCS)
- LOCK-03: FN-C1/FN-VALID auto-lock / manual
- LOCK-04: FN-DUMP net = gross − tare
- LOCK-05: FN-SIDE (CBM awaiting_payment + free coin + PDF)
- LOCK-06: FN-11 idempotent create
- LOCK-07/08: FN-SYNC bulk + date-required + lock
- LOCK-09: ENG-PAY-FEED (net+cane_type SoT)
- LOCK-10: FN-V rollback + block-if-paid
