# 03_LOGIC — F-WH-DN Delivery Note

> Non-HTTP business logic. Functions are feature-local; engines are pure/reusable or shared-service adapters.

## §3.1 Functions

| ID / code | Purpose | Input → Output | Invoked by | Side effects / calls |
|---|---|---|---|---|
| FN-01 `buildDeliveryQueue` | derive eligible unbound packs | filters/context → queue rows | API-01 | read Packing/SO/Transfer |
| FN-02 `loadDeliveryNote` | compose drawer/print model | dn_id → aggregate | API-17 | read only |
| FN-03 `createReferenceDelivery` | validate combine key and create draft | packs+delivery → DN | API-03 | pack bind, insert header/lines/audit; ENG-DOC-NUM at approved trigger |
| FN-04 `validateDeliveryAssignment` | employee/carrier/driver/vehicle validation | assignment → errors/warnings | API-03/04/06 | read masters; capacity warning |
| FN-05 `updateDeliveryData` | save reference delivery snapshot | DN+changes → DN | API-04 | update/audit |
| FN-06 `markDeliveryReady` | draft→ready | DN → ready | API-06 | audit/outbox |
| FN-07 `dispatchDelivery` | ready→in_transit | DN → dispatched | API-07 | ENG-DN-01, source update, audit/outbox |
| FN-08 `appendTrackingStage` | forward-only tracking | DN+stage → event | API-08 | tracking/audit/outbox |
| FN-09 `recordFailedAttempt` | derive attempt number from count | DN+reason → failed | API-09 | append attempt/audit/outbox |
| FN-10 `completeProofOfDelivery` | calculate result and apply accepted/rejected | DN+POD → result | API-10 | ENG-DN-02, source sync, audit/outbox |
| FN-11 `rescheduleDelivery` | failed→ready | DN+schedule → ready | API-11 | preserve attempts; audit/outbox |
| FN-12 `returnDeliveryAll` | failed/rejected→returned | DN+reason → returned | API-12 | ENG-DN-01 reverse, release packs/source, audit/outbox |
| FN-13 `cancelDelivery` | cancel pre/post dispatch | DN+reason → cancelled | API-13 | conditional reverse, release packs/source, audit |
| FN-14 `applyBackorderDecision` | retry or close-short | DN+decision → source result | API-14 | Sales/AR event when applicable |
| FN-15 `createManualDelivery` | create isolated manual DN | manual body → DN | API-15 | insert manual header/lines/audit only |
| FN-16 `changeManualStatus` | update any allowed manual status with reason | DN+target+reason → DN | API-16 | manual transition/audit only |

All functions are free of HTTP request/response terms. Every mutation appends actor/time/version and uses transaction/outbox boundaries.

## §3.2 Engines

### ENG-DN-01 `delivery-inventory-movement-engine`

- Category: inventory transaction orchestration
- Input: `{ tenant_id, dn_id, movement_type, lines[], source_refs[], occurred_at, actor_id, idempotency_key }`
- Output: `{ movement_refs[], committed, reconciliation_hash }`
- Logic: validate quantities/source → build issue/reverse/return movements → commit atomically → return references
- Used by: dispatch, POD partial/reject, return all, cancel after dispatch
- Iron check: pure contract input/output; inventory adapter performs I/O; no HTTP coupling

### ENG-DN-02 `delivery-result-engine`

- Category: delivery calculation
- Input: `{ delivered_lines[{qty,rejected_qty,reason}] }`
- Output: `{ result, accepted_total, rejected_total, line_results[] }`
- Logic: validate 0≤rejected≤qty and reason when rejected → sum → accepted/partial/rejected
- Used by: POD only; deterministic and independently testable

Shared engines invoked through adapters: `ENG-DOC-NUM.next`, `ENG-DOC-STORE.store`, `ENG-NOTIFY.emit`. They are not reimplemented here.

## §3.3 API ↔ Logic trace

| API | Functions | Engines/shared services |
|---|---|---|
| API-01 | FN-01 | — |
| API-02 | FN-02 (list projection) | — |
| API-03 | FN-03, FN-04 | ENG-DOC-NUM |
| API-04 | FN-04, FN-05 | — |
| API-05 | FN-04 (lookup projection) | — |
| API-06 | FN-04, FN-06 | ENG-NOTIFY |
| API-07 | FN-07 | ENG-DN-01, ENG-NOTIFY |
| API-08 | FN-08 | ENG-NOTIFY |
| API-09 | FN-09 | ENG-NOTIFY |
| API-10 | FN-10 | ENG-DN-01, ENG-DN-02, ENG-NOTIFY |
| API-11 | FN-11 | ENG-NOTIFY |
| API-12 | FN-12 | ENG-DN-01, ENG-NOTIFY |
| API-13 | FN-13 | ENG-DN-01 when GI exists |
| API-14 | FN-14 | ENG-NOTIFY |
| API-15 | FN-15 | ENG-DOC-NUM only; no integration automation |
| API-16 | FN-16 | none; audit only |
| API-17 | FN-02 | ENG-DOC-STORE on configured external snapshot event only |

## §3.4 Transaction boundaries

1. Reference create: pack locks + DN + lines + audit + number assignment commit together.
2. Dispatch: DN state + GI + source issued update + audit + outbox commit together.
3. POD: result + return movements + source counters/status + audit + outbox commit together.
4. Return/cancel after GI: reverse succeeds before pack/source release; any failure rolls back.
5. Manual create/status explicitly excludes movement/source calls; a guard rejects accidental engine invocation.

