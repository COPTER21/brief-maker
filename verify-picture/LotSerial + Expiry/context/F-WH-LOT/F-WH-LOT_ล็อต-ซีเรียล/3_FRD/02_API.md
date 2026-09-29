# 02_API — F-WH-LOT

## HTTP contracts (proposed implementation; [ASSUMED] paths pending API owner)
All endpoints require tenant auth, permission, correlation ID. Error envelope `{code:UPPER_SNAKE,message,field?,correlation_id}`. `POST/PATCH` require `Idempotency-Key`; replay returns prior result, no new event.

| ID | Method/path | Request | Response | Errors | Logic / DB |
|---|---|---|---|---|---|
| API-01 | GET `/api/warehouse/lot-identities` | item_code?, warehouse_ref?, query?, status?, sort?, page? | rows + count | FORBIDDEN | FN-01 / T_lot_identity |
| API-02 | POST `/api/warehouse/lot-identities` | item_code, lot_code, serial_code?, expiry_date?, idempotency_key | 201 lot_id/status | ITEM_NOT_FOUND, TRACKING_DISABLED, EXPIRY_REQUIRED, SERIAL_REQUIRED, SERIAL_DUPLICATE, LOT_REQUIRED, IDEMPOTENCY_CONFLICT | FN-02 / T_lot_identity,T_lot_audit |
| API-03 | PUT `/api/warehouse/items/{item_code}/tracking-policy` | tracking_mode, expiry_enabled, effective_date, expected_version, idempotency_key | 200 version | INVALID_POLICY, VERSION_CONFLICT, FORBIDDEN | FN-03 / T_item_tracking_policy,T_lot_audit |
| API-04 | GET `/api/warehouse/lot-recommendations` | item_code, warehouse_ref, at_date, required_qty? | ranked eligible candidates + available_qty, no reservation id | ITEM_NOT_FOUND, NO_ELIGIBLE_LOTS | FN-04 / T_lot_identity + external availability |
| API-05 | GET `/api/warehouse/lots/{lot_id}/movements` | direction?, page? | immutable movement refs + predecessor/successor | LOT_NOT_FOUND, SOURCE_UNAVAILABLE | FN-05 / W3-LITE adapter |
| API-06 | GET `/api/warehouse/lots/{lot_id}/events` | page? | append-only audit rows | LOT_NOT_FOUND, FORBIDDEN | FN-08 / T_lot_audit |

## Cross-module mock/TODO contracts
- API-X1 W3-LITE movement reader [ASSUMED contract]: `movement_id,tenant_id,lot_id,item_code,kind,qty,at,source_ref{type,id},from_ref,to_ref,previous_movement_id`. Mock fixture only. If source is unavailable, return `SOURCE_UNAVAILABLE`/empty trace; never fabricate a GRN/Transfer transaction. Reversal is a new movement at source, not an edit.
- API-X2 NC rules existing: open central rule view; expiry candidate event has `tenant_id,item_code,lot_id,expiry_date,ref_id,idempotency_key`. NC owns thresholds, recipients and channel. Since FEATURE_LIST chip is csq only, `ntf` detection is DIVERGENCE pending registry owner; no unapproved NTF declaration is silently registered.
- API-X3 Picking consumer: read API-04 recommendation; it remains responsible for reservation/issue. The W4 prototype never performs these calls.
- API-X4 CSQ event producer: `master.changed` at successful item policy change using envelope from CSQ brief; registration/7C evaluation external. Contract file referenced by skill is absent in pack, so declaration is [ASSUMED] pending CSQ owner.

## Failure and retry
Atomic unique tenant+item+serial and idempotency store are required in production. Conflict must not append audit. Network retry uses same key. All external mocks are tested only for payload shape, acknowledgement/unavailability and unchanged local movement/balance; no W3/NC/CSQ end-to-end claim.
