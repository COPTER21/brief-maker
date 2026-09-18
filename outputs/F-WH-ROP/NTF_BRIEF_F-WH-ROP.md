# NTF_BRIEF · F-WH-ROP · จุดสั่งซื้อซ้ำ

> Producer declaration only. Emit through ENG-NOTIFY; F085 must not hardcode recipient, template or channel. DOA events are not declared here.

| Event ID | Trigger | Required facts | Recipient/template/channel owner | Replay |
|---|---|---|---|---|
| `reorder_point.triggered` | FRD 03_LOGIC FN-04/FN-06: valid active policy + valid F009 snapshot and `ATP < ROP`; emit after suggestion event is durably recorded | tenant_id, item_id, warehouse_id, policy_ref, policy_version, snapshot_ref, as_of, atp, reorder_point, suggested_qty, idempotency_key, correlation_id | ENG-NOTIFY central configuration | Same key returns prior accepted result; no second notification event |

## UI behavior

On accepted emit, show toast **ส่งแจ้งเตือนแล้ว**. On replay, show **รายการนี้แจ้งเตือนไปแล้ว**. Do not show event code/payload in the drawer. Dependency failure stays in the drawer as a retryable error.

## Exclusions

- No `doa_pending`, `doa_result` or `doa_escalate`; F085 never submits PR.
- No recipient/channel preference check in F085.
- No notification when policy/snapshot is invalid, status is Near/Normal, or qty calculation is unavailable.

## Dev wiring

Call `ENG-NOTIFY.emit('reorder_point.triggered', facts)` from the outbox consumer after the evaluation transaction commits. Template and delivery settings are looked up centrally.
