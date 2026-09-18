# 03 LOGIC · F-WH-ROP

## FN-01 List policies

Authorize tenant/warehouse scope, select latest effective version per exact pair/date, then filter/sort/page. Counts derive from the same authorized query.

## FN-02 Save policy version (`config-save`)

1. Resolve Item/Warehouse/Vendor masters and authorize write scope.
2. Validate `0≤safety≤min≤max`, lead≥0, pack≥1, ADU window 30/60/90 and date.
3. Compare expected_version; on conflict return 409.
4. Insert immutable policy version plus audit/outbox in one transaction.
5. If any sensitive field changed, enqueue CSQ `master.changed` once with SecC profile metadata.
6. Never emit CSQ on invalid/no-effect save.

Sensitive candidates: min, max, safety_stock, lead_time_days, adu_window_days and provisionally enabled. Preferred vendor/note changes are no-effect for CSQ.

## FN-03 Resolve active policy

Match tenant+item+warehouse, enabled=true, effective_date≤asOf; choose highest effective_date then version. No match returns `NO_POLICY`, never default thresholds.

## FN-04 Evaluate pair

Read F009 snapshot. Reject missing/stale contract as `SNAPSHOT_UNAVAILABLE`. Compute:

```text
rop = max(min, safety + adu * lead_time)
triggered = atp < rop
near = !triggered && atp <= rop * 1.20
raw = triggered ? max(0, max + safety - atp - on_order) : 0
qty = raw > 0 ? ceil(raw / pack_size) * pack_size : 0
```

Store reason with all operands. New item/history gives ADU=0 from F009. Do not query Quality Hold.

## FN-05 Run triggers

- Scheduler: daily 06:00 tenant-local for enabled catalog.
- Movement subscriber: GRN/Issue/Transfer/Adjust/Reserve event evaluates only affected pair.
- Manual: UI test/operational retry; same semantics.

Idempotency key includes tenant, pair/scope, run window, policy version and snapshot ref. Replay returns prior outcome without new events.

## FN-06 Notification

For triggered result, emit `reorder_point.triggered` through ENG-NOTIFY with tenant, policy/snapshot refs, item/warehouse, ATP/ROP/qty/asOf and idempotency key. No local recipient/channel/template logic.

## FN-07 PR Draft

Collect triggered qty>0 results by warehouse and run. Call F072 once per group. Response must be draft and `submitted=false`. Failure is retryable; success or replay appends one local reference event. Never auto-submit or split by vendor.

## FN-08 History

Append policy, evaluation, notification and PR reference events. UI maps internal kinds to Thai human-readable labels. No update/delete endpoint.
