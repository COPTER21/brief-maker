# CSQ_BRIEF · F-WH-ROP · จุดสั่งซื้อซ้ำ

## §1 Identity

- `profile_id`: `CSQ-ROP-01` **[DEFAULT — รอยืนยันกับ Profile Registry]**
- `feature_code`: F085
- Module/Wave: Warehouse · W4 FULL
- Backfill group: B (SecC on sensitive change)
- Version: v0.1 — FRD Pack F085 v2.0

## §2 Declared Event

| Event | Trigger | Tube | Condition | Payload |
|---|---|---|---|---|
| `master.changed` | FRD 03_LOGIC FN-02: policy version + audit/outbox commit success | **SecC** | changed fields intersect min, max, safety_stock, lead_time_days, adu_window_days or provisional enabled; note/preferred vendor only = no effect | tenant_id, item_id, warehouse_id, policy_ref, config_version, changed_fields, old_values, new_values, actor_ref, changed_at, idempotency_key, correlation_id |

Idempotency key is unique per `(F085, tenant, item, warehouse, config_version)`. Reverting config creates a new `master.changed`; it is not a document reversal.

## §3 Not Declared

- `rop.threshold_breached`: Notification detection only; event owner is NTF declaration.
- `rop.pr_draft_created`: F072 owns PR lifecycle. F072 event carries `origin_type='reorder_point'` and `origin_ref={item_id,warehouse_id,rop_run_id}`.
- OC: Operation Process owns `sow.*`.
- DC: no terminal decision in F085; PR approval is F072/DOA.
- SC: reserved false.
- EC/AC/FC: no value, accounting or cash commitment at F085.

## §4 Controls

- Emit only after successful sensitive config commit; invalid or no-effect saves emit nothing.
- F085 has no 7C result card and stores no tube outcome.
- Central CSQ engine evaluates consequences; F085 produces facts only.
- Numeric config contains no raw person name; verify Inventory Config classification before production.

## §5 Register Checklist

- [x] FRD config-save and field names defined
- [x] BR-CSQ-01..05 defined
- [x] Cross-module producer contract documented
- [x] HTML contains ENG-CSQ contract anchor and no 7C card
- [ ] Confirm profile ID and `master.changed` vocabulary with F-CSQ-01 owner
- [ ] Confirm whether `enabled` is a sensitive change
- [ ] Confirm F072 delivery window for origin fields
- [ ] Register only after remaining registry questions are resolved

## §6 Open Questions

| OQ | Owner |
|---|---|
| Correct trigger status and central event vocabulary | F-CSQ-01 owner |
| `enabled` counts as sensitive change | Strike |
| F072 accepts origin fields in which release | F072 owner |
