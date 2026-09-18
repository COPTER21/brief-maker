# 02_API — F-WH-STKTRF

Base path: `/api/v1/stock-transfers`. JSON uses snake_case. Mutations require authorization, `Idempotency-Key`, `If-Match`, audit actor, and server-side state validation.

## 2.1 Endpoints

| ID | Method/path | Purpose | Logic | Tables |
|---|---|---|---|---|
| API-01 | GET `/stock-transfers` | list/filter/page/sort | FN-01 | transfer, line |
| API-02 | POST `/stock-transfers` | create draft/duplicate | FN-02 | transfer, line, attachment |
| API-03 | GET `/stock-transfers/{id}` | detail/tabs/actions | FN-03 | all read models |
| API-04 | PATCH `/stock-transfers/{id}` | edit draft | FN-04 | transfer, line, attachment |
| API-05 | POST `/{id}/submit` | validate, allocate TRF number, freeze DOA snapshot | FN-05 | transfer, approval, audit |
| API-06 | POST `/{id}/approval-actions` | approve/reject current slot | FN-06 | approval, transfer, audit |
| API-07 | POST `/{id}/ship` | same-warehouse move or cross-warehouse shipment | FN-07 | movement, transfer, line, audit |
| API-08 | POST `/{id}/receipts` | full/partial receive | FN-08 | receipt, movement, line, audit |
| API-09 | POST `/{id}/return-to-source` | return remaining transit stock | FN-09 | movement, transfer, audit |
| API-10 | POST `/{id}/shortage-requests` | stage discrepancy/evidence and resolve DOA | FN-10 | shortage approval, attachment, audit |
| API-11 | POST `/{id}/shortage-actions` | sequential approval/final write-off | FN-11 | movement, approval, transfer, audit |
| API-12 | POST `/{id}/cancel` | cancel before movement | FN-12 | transfer, audit |
| API-13 | POST `/{id}/reversals` | create reversal draft pending approval | FN-13 | transfer, line, approval, audit |
| API-14 | GET `/{id}/document` | PDF/document snapshot metadata | FN-14 | document store |
| API-15 | POST `/{id}/attachments` | upload authorized evidence/document | FN-15 | attachment, audit |

## 2.2 Mutation contract

Success returns `{data, version, allowed_actions}`. Validation returns 422 `{code, message, fields[]}`. Permission returns 403. Invalid transition returns 409 `INVALID_STATE`; stale version returns 409 `VERSION_CONFLICT`; repeated idempotency key returns the original response. Inventory and document state changes are committed atomically.

API-08 recomputes remaining from committed ledger/receipt data and clamps/rejects client quantity above remaining. API-11 posts write-off only on the final approved slot. API-13 never pre-populates received quantity or movement rows.

## 2.3 Cross-module contracts

| Contract | Direction | Payload/result |
|---|---|---|
| `ENG-DOC-NUM.next(TRF)` | submit → DOCCFG | unique code; no allocation on draft |
| `ENG-DOC-STORE.store(TRF)` | state/document snapshot → DOCCFG | immutable rendered document version |
| DOA resolve/start/action | submit/shortage → DOA | amount, mode, real-person slots, snapshot |
| `trf.shipped`, `trf.received`, `trf.partial`, `trf.shortage`, `trf.returned`, `trf.reversed` | feature → ENG-NOTIFY | document/warehouse/actor/timestamp IDs; channel resolved centrally |
| Inventory movement append | feature → ledger | source, destination, item, qty, cost snapshot, reference, reversal link |
| JE posting | future W5 | current output only `pending_posting`; no external post |

DOA-generated `doa_pending`/`doa_result` notifications are not emitted by this feature.

