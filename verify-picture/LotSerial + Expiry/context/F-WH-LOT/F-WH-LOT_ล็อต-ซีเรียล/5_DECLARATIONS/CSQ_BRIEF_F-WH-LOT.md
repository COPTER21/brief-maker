# CSQ_BRIEF — F-WH-LOT · Lot/Serial + Expiry

> v1 draft · W4 chip `csq` · [ASSUMED contract] because `csq-declaration/references/csq-contract.md` is absent from this pack. This brief is a producer contract for dev review; it is not registered with ENG-CSQ.

## 1. Identity
profile_id: `CSQ-F-WH-LOT` [ASSUMED naming] · feature_code: `F-WH-LOT` · module: Warehouse · group: master/config · version: 1. Owner: CSQ Engine owner before registration.

## 2. Declared events
| event_id | Trigger point | Tubes | Condition | Payload fields |
|---|---|---|---|---|
| `master.changed` | FRD 03_LOGIC FN-03 commits item tracking policy and FN-07 appends audit | DC [DEFAULT — รอยืนยัน] | Successful policy change only; no event on validation/version conflict | tenant_id,item_code,tracking_mode,expiry_enabled,effective_date,idempotency_key |
No event on recommendation, trace read, blocked save or prototype fixture change. If central CSQ contract classifies this master update as no-effect, retire the declaration rather than emitting a false consequence; registry owner resolves this before deploy.

## 3. Tubes not declared
OC belongs to Operation Process; document DC belongs to DOA (this event is a master-policy change, not document approval); SC is reserved and never emitted. EC/AC/FC/SecC have no supported direct effect from this master change. No feature-local tube result or valuation is computed.

## 4. Envelope payload
| Field | Type | FRD 04_DB source | Classification |
|---|---|---|---|
| tenant_id | uuid | T_item_tracking_policy.tenant_id | Internal |
| item_code | text | T_item_tracking_policy.item_code | Internal |
| tracking_mode | enum | T_item_tracking_policy.tracking_mode | Internal |
| expiry_enabled | boolean | T_item_tracking_policy.expiry_enabled | Internal |
| effective_date | date | T_item_tracking_policy.effective_date | Internal |
| idempotency_key | text | T_lot_audit.idempotency_key | Confidential; mask in logs |
Envelope includes feature/ref/action and correlation fields per central engine contract when available. Event is emitted after commit exactly once; retry reuses idempotency key. Reversal uses a new policy version/event with `reversal_of`, never deletes prior result.

## 5. Register checklist
Confirm missing central CSQ contract file/version; confirm `master.changed` event ID and DC tube with CSQ owner; validate payload with FRD DB keys; enforce masking; test mock acknowledgement/retry only in W4; register only in deployment pipeline after review.

## 6. Open questions
CSQ owner: whether item tracking policy change warrants DC and exact profile ID; before engine registration. W4 lane proceeds with explicit [ASSUMED] brief, no live registration claim.
