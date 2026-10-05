# API contract · proposed; all production calls TODO
Base `/api/warehouse/qhold/v1` scoped tenant/warehouse. UTC timestamps and decimal quantity strings. HTTP status 400 validation, 403 scope/slot, 404 ref, 409 version/idempotency, 503 upstream unavailable. Never use client fixture as authority.

| ID | Method/path | Request → response | FN |
|---|---|---|---|
| API-01 | GET `/slices?warehouseRef&itemRef&search&status` | scoped Inventory snapshot + quarantine projection, `version`, available/ATP | FN-01,02,10 |
| API-02 | GET `/doa-policy?kind&warehouseRef&qty&asOf` | effective policyRef, requiredSlots[{slotId,eligiblePersonRefs}], named-person lookup token | FN-03 |
| API-03 | POST `/requests` | `{kind:hold|release,sliceId,qty,reason,origin,sourceRef,selectedSlots,expectedSliceVersion,idempotencyKey}` → requestId,status=requested, projection/version | FN-02,03,04,06,08 |
| API-04 | POST `/decisions/events` **DOA adapter only** | `{requestId,decision,sourceEventId,actorRef,expectedRequestVersion}` → approved/rejected, prior result on replay | FN-05,07,08 |
| API-05 | GET `/requests?status&sliceId` | pending queue with approved scope and selected person snapshots | FN-09 |
| API-06 | GET `/events?requestId&sliceId` | immutable event list actor/time/source/decision | FN-09 |
| API-07 | POST `/availability/check` | `{sliceId,kind:sell|transfer,qty}` → `{allowed,available,reason}` only; no transaction | FN-10 |

API-02/04 integration belongs to DOA; UI POST API-04 is forbidden in production. API-01 onHand/reservedSales read from Inventory, QHold writes only reservation/projection transaction and own events. `POST /requests` with same key+same body returns prior result; same key different body => IDEMPOTENCY_CONFLICT. `POST /decisions/events` sourceEventId is unique per DOA event and atomic with projection. W3-LITE GRN/RTV and NC/CSQ adapters are mock envelopes; no actual GRN posting or notification/stamp. Outbox transaction belongs production build.
