# 02_API — F-WH-PICK Picking

> HTTP layer only. All mutations require auth, tenant context, `Idempotency-Key`, and state-changing updates require `If-Match`.

## §2.1 Endpoint inventory

| ID | Method/path | Roles | Calls |
|---|---|---|---|
| API-01 | GET `/api/v1/pick-queue` | all | FN-01 |
| API-02 | GET `/api/v1/picks` / `/:id` | all scoped | FN-02 |
| API-03 | POST `/api/v1/picks` | wh_lead | FN-03, FN-04, ENG-01 |
| API-04 | POST `/api/v1/picks/:id/assign` | wh_lead | FN-05 |
| API-05 | POST `/api/v1/picks/:id/start` | lead/assigned picker | FN-06 |
| API-06 | POST `/api/v1/picks/:id/lines/:lineId/pick` | lead/assigned picker | FN-07 |
| API-07 | POST `/api/v1/picks/:id/lines/:lineId/short` | lead/assigned picker | FN-08 |
| API-08 | POST `/api/v1/picks/:id/lines/:lineId/relocate` | lead/assigned picker | FN-09, ENG-01 |
| API-09 | POST `/api/v1/picks/:id/lines/:lineId/refresh` | lead/assigned picker | FN-10, ENG-01 |
| API-10 | POST `/api/v1/picks/:id/replenishment-requests` | authorized role pending OQ | FN-11 |
| API-11 | POST `/api/v1/picks/:id/finish` | lead/assigned picker | FN-12 |
| API-12 | POST `/api/v1/picks/:id/close-short` | lead/assigned picker | FN-13 |
| API-13 | POST `/api/v1/picks/:id/hold` / `/resume` | lead/assigned picker | FN-14 |
| API-14 | POST `/api/v1/picks/:id/cancel` | wh_lead | FN-15 |
| API-15 | POST `/api/v1/picks/:id/send-to-packing` | lead/assigned picker | FN-16 |
| API-16 | GET `/api/v1/picks/:id/print` | scoped view | FN-17 |

## §2.2 Common contract

Success envelope `{data, meta:{request_id, version}}`; errors `{code,message,details,request_id}`. List supports `q,warehouse_id,status,assignee_id,cursor,limit`. Source input enum for create is exactly `SO`; any other value returns `BR_PICK_SOURCE_NOT_ALLOWED`.

Mutation bodies use snake_case and include only action data. Examples:

```json
{"source_type":"SO","source_refs":["SO-2026-0207"],"assignee_id":"EMP-02","priority":"normal"}
```

```json
{"picked_qty":710,"scan_location":"PF-A01-01","scan_item":"FG-1001","reason":null}
```

## §2.3 Responses and side effects

| API group | Success | Side effects |
|---|---|---|
| create | 201 Pick | insert header/lines/audit; Inventory allocation contract |
| assign/start/state | 200 Pick | update status/version/audit; selected NTF events |
| pick/short/relocate | 200 line+progress | Inventory/SO changes atomically + audit/events |
| send-to-packing | 200 `{pick,pack_refs[]}` | Packing intake idempotently; status to_pack |
| print | 200 PDF/print model | none; log print access if policy requires |

## §2.4 Error catalog mapping

400 validation; 401 unauthenticated; 403 insufficient/ownership; 404 not found; 409 stale/idempotency/allocation conflict; 422 business transition/source/location/quantity; 500 internal. Exact codes in `05_RULES §5.6`.

## §2.5 Cross-module contracts

| Module | Contract |
|---|---|
| Sales Order | read queue gates; atomic reserve→picked/backorder adjustments by source line |
| Inventory | allocate/release/pick movements with `pick_id,so_id,line_id,location_id,lot_no,qty` |
| Employee/IAM | search assignee and authorize role/own assignment at mutation time |
| Packing | idempotent intake per source SO after picked; return one pack ref per SO |
| ENG-NOTIFY | emit declared event with ref/payload; feature never chooses channel/preferences |

If downstream call fails before commit, rollback. If asynchronous notification fails after commit, queue retry without reversing Pick.
