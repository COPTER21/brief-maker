# 02 API · F-WH-ROP

| ID | Method/path | Request | Success | Errors |
|---|---|---|---|---|
| API-01 | GET `/v1/reorder-policies` | item/warehouse/status/search/asOf/page | policy summaries + counts | 401/403/422 |
| API-02 | POST `/v1/reorder-policies` | item_id, warehouse_id, min/max/safety, lead_time_days, adu_window_days, pack_size, preferred_vendor_id?, effective_date, enabled, expected_version | 201 policy version | 409 version, 422 validation/master |
| API-03 | GET `/v1/reorder-suggestions` | item/warehouse/status/asOf | F009 refs + formula result + status | 424 snapshot unavailable |
| API-04 | POST `/v1/reorder-runs` | scope, trigger_type, trigger_ref, idempotency_key | run summary | 409 replay returns prior result; 424 dependency |
| API-05 | POST `/v1/reorder-notifications` | suggestion_ref, policy_ref/version, snapshot_ref/asOf, idempotency_key | accepted event ref | 424 ENG-NOTIFY |
| API-06 | POST `/v1/reorder-pr-drafts` | warehouse_id, run_id, lines[], origin_type, origin_ref, idempotency_key | `{pr_draft_id,status:'draft',submitted:false}` | 409 replay; 424 F072 |
| API-07 | GET `/v1/reorder-events` | filters/page | append-only human-readable events | 401/403 |

## Cross-module contracts

- F009 snapshot is read as `{item_id,warehouse_id,atp,adu,on_order,as_of,snapshot_ref}`. ATP is final; never subtract reserved/hold.
- API-06 groups all positive lines for one warehouse/run. Each line carries policy_ref/version and snapshot_ref. Preferred vendor is suggestion only.
- F072 must persist `origin_type='reorder_point'` and `origin_ref={item_id,warehouse_id,rop_run_id}`; F072 owns `doc.created/approved/...`.
- ENG-NOTIFY owns recipients, templates and channels; F085 sends facts only.
- CSQ producer contract is `master.changed` after API-02 commit; profile `CSQ-ROP-01`, SecC, subject to registry confirmation.
