# 02_API · F-WH-ROP

All endpoints below are **proposed production contracts**, not live endpoints. Tenant inferred from verified auth, never trusted from client body. Require warehouse scope; writes require policy-maintainer role and expectedVersion. Errors use `{code,message,correlationId,fieldErrors?}` and no silent success. JSON quantities are decimal strings/validated decimal, not JS floating point in production.

| ID | Method/path | Request → response | Function | Errors |
|---|---|---|---|---|
| API-01 | GET `/v1/rop/policies?itemCode&warehouseRef&asOf` | filters → `{rows:[PolicyVersion],cursor}` | FN-03 | ACCESS_DENIED, BAD_REFERENCE |
| API-02 | POST `/v1/rop/policies` | `{itemCode,warehouseRef,minQty,maxQty,safetyQty,effectiveDate,ncRuleRef,expectedVersion}` → `{policy,version,eventRef}` | FN-01→FN-02 | REQUIRED, BAD_REFERENCE, POLICY_BOUNDS, BAD_EFFECTIVE_DATE, VERSION_CONFLICT |
| API-03 | GET `/v1/rop/suggestions?itemCode&warehouseRef&asOf` | filters → `{rows:[{policyRef,policyVersion,snapshotRef,onHand,held,available,triggered,suggestedQty,status}]}` | FN-03→FN-04→FN-05 | NO_POLICY, SNAPSHOT_UNAVAILABLE, SNAPSHOT_STALE |
| API-04 | POST `/v1/rop/pr-preparations` | `{policyRef,snapshotRef,suggestedQty,idempotencyKey}` → `{mockRef,accepted,payload,replay}` | FN-06 | NO_POSITIVE_SUGGESTION, STALE_SNAPSHOT, MOCK_UNAVAILABLE, IDEMPOTENCY_CONFLICT |
| API-05 | POST `/v1/rop/nc-candidates` | `{policyRef,snapshotRef,ruleRef,idempotencyKey}` → `{candidateRef,envelope,replay}` | FN-07 | NC_RULE_MISSING, STALE_SNAPSHOT, MOCK_UNAVAILABLE |
| API-06 | GET `/v1/rop/events?itemCode&warehouseRef&cursor` | filters → immutable `{events,cursor}` | FN-08 | ACCESS_DENIED |
| API-07 | GET `/v1/rop/options?kind=item\|warehouse&q` | query → scoped `{options:[{code,name}]}` | upstream Item/Warehouse read adapter | ACCESS_DENIED, BAD_QUERY |

API-04 is a mock/TODO boundary for Procurement W2-PUR-LITE. Its acceptance means only the local adapter accepted a request envelope; no PR record is created. API-05 is a mock/TODO boundary for NC; no threshold decision, channel selection, recipient or notification delivery is asserted. CSQ declaration is a downstream read context only. Both mock routes need 24-hour or owner-configured idempotency retention `[ASSUMED contract]`; durable dedup/outbox is a production design requirement.

## Cross-module declaration producer contract
After successful FN-02 commit, a future CSQ adapter may emit `master.changed` with tenant_id, policy_ref, item_code, warehouse_ref, version, effective_date, idempotency_key and correlation_id; the central CSQ contract/catalog is absent, so the event/tube are `[DEFAULT — รอยืนยัน]` and **no live emit** is implemented or tested in this HTML. `POST /csq/events` is an external TODO and must use the central envelope after CSQ owner review. After FN-05 evaluation, FN-07 prepares NC candidate facts under NTF/NC brief; the local API-05 mock does not call ENG-NOTIFY or select recipients/channels. Neither event should fire on validation failure, read-only history, duplicate replay or stock mutation (none exists).
