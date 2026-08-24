# 02_API — F-WH-DN Delivery Note

> Thin HTTP contracts only. Business logic belongs in `03_LOGIC`; declarative rules in `05_RULES`.

## §2.1 Endpoint registry

| ID | Method / Path | Purpose | Auth | Reads/Writes |
|---|---|---|---|---|
| API-01 | GET `/api/v1/delivery-notes/queue` | eligible Packing queue | warehouse read | Packing/source snapshot |
| API-02 | GET `/api/v1/delivery-notes` | list/filter DN | warehouse read | delivery tables |
| API-03 | POST `/api/v1/delivery-notes/reference` | create from selected packs | wh_lead | DN/pack/line/audit |
| API-04 | PUT `/api/v1/delivery-notes/{id}/delivery` | update draft/ready delivery info | wh_lead | DN/audit |
| API-05 | GET `/api/v1/delivery-notes/lookups` | employee/carrier/driver/vehicle search | authorized user | master APIs |
| API-06 | POST `/api/v1/delivery-notes/{id}/ready` | mark ready | wh_lead | DN/audit/outbox |
| API-07 | POST `/api/v1/delivery-notes/{id}/dispatch` | dispatch reference DN | owner/lead | DN/GI/source/audit/outbox |
| API-08 | POST `/api/v1/delivery-notes/{id}/tracking` | append forward tracking | owner/lead | tracking/audit/outbox |
| API-09 | POST `/api/v1/delivery-notes/{id}/failed` | append failed attempt | owner/lead | attempt/DN/audit/outbox |
| API-10 | POST `/api/v1/delivery-notes/{id}/pod` | complete POD full/partial/reject | owner/lead | line/POD/DN/stock/source/outbox |
| API-11 | POST `/api/v1/delivery-notes/{id}/reschedule` | failed→ready | wh_lead | DN/audit/outbox |
| API-12 | POST `/api/v1/delivery-notes/{id}/return` | return all | wh_lead | reverse/source/queue/audit/outbox |
| API-13 | POST `/api/v1/delivery-notes/{id}/cancel` | cancel pre/post dispatch | wh_lead | reverse/source/queue/audit |
| API-14 | POST `/api/v1/delivery-notes/{id}/backorder-decision` | retry or close-short | wh_lead | source/AR event/audit |
| API-15 | POST `/api/v1/delivery-notes/manual` | create Manual DN | wh_lead | DN/line/audit |
| API-16 | POST `/api/v1/delivery-notes/{id}/manual-transition` | change Manual status | authorized manager | DN/manual transition/audit |
| API-17 | GET `/api/v1/delivery-notes/{id}` | drawer/tabs/print data | authorized read | all DN child data |

## §2.2 Common contract

- Tenant/company/branch context from authenticated session; never accepted as trusted body fields
- Mutation headers: `Idempotency-Key`, `If-Match`/version and correlation id
- Response envelope: `{ data, meta, errors[] }`; timestamps ISO-8601; quantity in base UOM
- 400 invalid shape, 403 permission, 404 missing, 409 stale/idempotency conflict, 422 business guard, 503 downstream unavailable

## §2.3 Mutation request highlights

- API-03: `{ pack_ids[], assignee_employee_id, carrier, vehicle|manual_vehicle, driver|manual_driver, ship_date, slot }`
- API-04: same delivery block; manual driver `{first_name,last_name,phone}` and vehicle `{plate}`; no manual assignee
- API-07: `{ version }`; validates tracking for 3PL; `creation_mode=reference` only
- API-09: `{ reason_code, note, version }`; attempt number is server-derived
- API-10: `{ receiver_name, lines[{line_id,rejected_qty,reason}], signature_ref?, photo_refs[] }`
- API-12/13/14/16: `{ reason|decision, version }`; reason mandatory where specified
- API-15: manual header/recipient/lines only; source refs, automatic GI/source sync fields rejected

## §2.4 Cross-module contracts

| XT | Contract | Producer/Consumer | Idempotency / failure |
|---|---|---|---|
| XT-01 | Packing eligibility/bind/release | Packing ↔ DN | pack lock + DN ref; rollback create or retry release |
| XT-02 | `issue`, `issue_reverse`, `return_in` | DN → Inventory | DN+movement_type key; atomic with DN transition |
| XT-03 | SO issued/shipped/returned/status | DN → Sales | only `source_type=sales_order`; recalculated/idempotent |
| XT-04 | transfer dispatched/delivered/reversed | DN → Stock Transfer | only transfer source; exact final contract OQ-04 |
| XT-05 | billing-ready/close-short | DN → AR | transactional outbox; no duplicate request |
| XT-06 | number/snapshot engines | DN → F-DOCCFG | engine owns format/policy; no direct config write |
| XT-07 | business events | DN → ENG-NOTIFY | outbox retry; preferences resolved centrally |

Manual DN APIs must not emit XT-01..05 automatically. Audit remains mandatory.

