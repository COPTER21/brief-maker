# 02_API — F-WH-PACK Packing

## §2.1 Common Contract

- Base `/api/v1`; JWT auth; `X-Tenant-Id` required.
- Mutations require `Idempotency-Key`; versioned pack/box mutations require `If-Match`.
- Pagination `limit` default 20 max 100; cursor preferred for audit.
- Errors: `{ "error": { "code": "UPPER_SNAKE", "message": "localized", "details": {}, "correlation_id": "uuid" } }`.
- Status codes: 400 malformed, 401 unauthenticated, 403 forbidden, 404 not found, 409 state/version/idempotency conflict, 422 business validation, 429 limit, 500/503 service.

## §2.2 Inventory

| ID | Method/Path | Purpose | Roles | Logic |
|---|---|---|---|---|
| API-01 | GET `/api/v1/packing-jobs` | queue/filter | scoped users | FN-12 |
| API-02 | GET `/api/v1/packs` | pack list/export filters | scoped users | FN-12 |
| API-03 | GET `/api/v1/packing-jobs/:id` | picked job detail | scoped users | FN-12 |
| API-04 | GET `/api/v1/packs/:id` | pack/detail tabs | scoped users | FN-12 |
| API-05 | POST `/api/v1/packing-jobs/:id/start` | create/start pack | wh_lead, packer | FN-02 |
| API-06 | POST `/api/v1/packs/:id/boxes` | open master/custom carton | editor | FN-03, ENG-01 |
| API-07 | PATCH `/api/v1/packs/:id/boxes/:box_id/items` | add/set/remove allocation | editor | FN-04, ENG-01 |
| API-08 | POST `/api/v1/packs/:id/boxes/:box_id/close` | close and version label | editor | FN-05, ENG-01 |
| API-09 | POST `/api/v1/packs/:id/boxes/:box_id/reopen` | reopen carton | wh_lead | FN-06 |
| API-10 | POST `/api/v1/packs/:id/finish` | complete pack | authorized owner/lead | FN-07 |
| API-11 | POST `/api/v1/packs/:id/reopen` | reopen packed document | wh_lead | FN-08 |
| API-12 | POST `/api/v1/packs/:id/cancel` | cancel with reason | authorized owner/lead | FN-09 |
| API-13 | POST `/api/v1/packs/:id/delivery-note` | DN handoff | wh_lead | FN-10 (disabled pending OQ) |
| API-14 | POST `/api/v1/packs/:id/boxes/:box_id/labels` | render/reprint label | print role | FN-13, ENG-02 |
| API-15 | POST `/api/v1/packs/:id/packing-slip` | render/reprint slip | print role | FN-13, ENG-02 |
| API-16 | GET `/api/v1/packs/:id/audit` | cursor audit | scoped users | FN-12 |
| API-17 | GET `/api/v1/packs/export` | CSV export | export role | FN-14 |

IDs are fully qualified as `F-WH-PACK-API-NN` in implementation and trace tables.

## §2.3 Mutation Contracts

### F-WH-PACK-API-05 Start

Body `{ "station_id":"uuid", "assignee_id":"uuid?" }`; response 201 `{pack}` or idempotent 200 same pack. Preconditions: job available, source contract valid, role/warehouse scope. Writes pack/job/audit/outbox.

### F-WH-PACK-API-06 Open Carton

Body one-of `{ "box_type_id":"uuid" }` or `{ "custom": {"name":"string","tare_weight":"decimal"} }`. Response 201 `{box,pack_version}`. Preconditions: pack in_progress; no active carton. Master values are snapshotted.

### F-WH-PACK-API-07 Allocate

Body `{ "operation":"add|set|remove", "source_line_id":"uuid", "qty":"decimal", "scan_token":"string?", "uom_code":"string?" }`. One request is one undo unit even when distributed across lots. Response 200 `{box,remaining,computed_weight,pack_version}`. No partial commit.

### F-WH-PACK-API-08 Close Carton

Body `{ "actual_weight":"decimal?" }`; response 200 `{box,label_ref,pack_summary}`. Preconditions non-empty, active, current version. Atomically closes, increments label version, audits and queues `pack.box_closed`.

### F-WH-PACK-API-09 Reopen Carton

Body `{ "reason":"string" }`; preconditions pack not shipped, no other active carton, wh_lead. Atomically invalidates active label version and opens box.

### F-WH-PACK-API-10 Finish

Body `{}`; preconditions remaining=0, no active carton, ≥1 closed carton. Response `{pack:{status:"packed"},packing_slip_available:true}`. Queues `pack.done` only after commit.

### F-WH-PACK-API-11 Reopen Pack

Body `{ "reason":"string" }`; `packed→in_progress`; no DN; wh_lead; label/slip reprint policy follows rule.

### F-WH-PACK-API-12 Cancel

Body `{ "reason":"nonblank" }`; allowed in_progress/packed before DN. Response `{pack:{status:"cancelled"},job:{status:"queued"}}`; queues `pack.cancelled`.

### F-WH-PACK-API-13 Delivery Note Handoff

No production implementation until OQ-DN-01. Contract shell only: Idempotency-Key required; precondition packed; success must return stable `dn_ref`; failures leave pack packed. Packing must not update SO/Inventory directly unless future locked contract explicitly assigns ownership.

### F-WH-PACK-API-14/15 Print

Body `{ "copy_type":"original|copy", "reason":"string?" }`; response 202 `{print_job_id,status:"queued"}` or 200 binary/URL per shared print platform decision. Rendering failure never changes pack/carton state. Reprint audit records template version, actor, reason and label version.

## §2.4 Read Models

Pack response includes IDs, source refs, status/version, assignee/station, source/customer snapshots, ordered/picked/packed/remaining totals, boxes with items and label state, permissions booleans and print availability. Confidential fields are omitted/masked by role.

## §2.5 Picking Inbound Contract

Owned by Picking: `POST /api/v1/picks/:id/send-to-packing`; allowed only `picked`; success `to_pack`; returns `{pick,pack_refs[]}`; one ref per source SO; retry safe; Packing unavailable leaves Pick `picked`. Packing exposes an internal idempotent intake port, not a second public competing endpoint.

## §2.6 Cross-Module Contracts

| Target | Contract | Trigger | Status |
|---|---|---|---|
| Print | API-14/15 + templates | close/finish/manual reprint | defined |
| ENG-NOTIFY | outbox event envelope | committed business event | declaration follows |
| Delivery Note | API-13 adapter | packed | OQ-DN-01; disabled |
| Transfer | intake adapter | external trigger | OQ-XT-01; not implemented |

## §2.7 Trace Summary

Authoritative trace is `03_LOGIC.md §3.3`; every mutation API has ≥1 function. HTTP layer performs parsing/auth/schema/response only.
