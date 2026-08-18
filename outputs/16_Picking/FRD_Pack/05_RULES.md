# 05_RULES — F-WH-PICK Picking

## §5.1 Business rules

| ID | Rule |
|---|---|
| BR-PICK-01 | SO queue requires confirmed + reserved + not hold + payment gate passed |
| BR-PICK-02 | remaining = reserved − picked − open pick; service/backorder excluded |
| BR-PICK-03 | wave same warehouse and count ≤ configured waveMax |
| BR-PICK-04 | number through shared Document Config contract |
| BR-PICK-05 | FEFO/FIFO + type rank + route order, allocation evidence stored |
| BR-PICK-06 | SO owns warehouse reserve; Pick owns location allocation; changes atomic |
| BR-PICK-07 | auto/manual selection passes active/same-WH/type/status/outbound eligibility |
| BR-PICK-08 | workload threshold warns only; permission/ownership always rechecked |
| BR-PICK-09 | scan location and item/lot before confirm; short needs reason/action |
| BR-PICK-10 | short releases allocation, updates SO backorder and emits event |
| BR-PICK-11 | refresh reads latest balance and allocates atomically if found |
| BR-PICK-12 | Inventory owns replenish/transfer; no such job enters Pick queue |
| BR-PICK-13 | finish needs all lines terminal and total picked >0; Packing split per SO |
| BR-PICK-14 | close-short only in progress with prior picked qty and reason |
| BR-PICK-15 | hold keeps allocation; cancel only draft/assigned and releases all |
| BR-PICK-16 | audit append-only; all movements reference Pick and SO |
| BR-PICK-17 | create source enum accepts SO only (LOCK-11) |

## §5.2 State transition matrix

| From | Action | To | Role/guard |
|---|---|---|---|
| — | create without/with assignee | draft/assigned | wh_lead + valid wave |
| draft | assign/cancel | assigned/cancelled | wh_lead |
| assigned | start/cancel | in_progress/cancelled | owner/lead; cancel lead only |
| in_progress | hold/finish/close-short | on_hold/picked | owner/lead + guards |
| on_hold | resume | in_progress | owner/lead |
| picked | send Packing | to_pack | owner/lead + idempotent downstream |

## §5.3 Permission matrix

Same as BRD §4; backend authorization is mandatory even when buttons are hidden. Picker scope is assigned record; viewer mutation always 403.

## §5.4 Validations

- quantity numeric, ≥0, ≤ remaining; short reason required
- scans must match allocated location/item/lot
- manual candidate must satisfy hard eligibility; HOLD/STAGING/PACK and blocked/frozen/inactive forbidden
- cancel/hold/close-short reason required; state/version guards enforced
- mixed warehouse, ineligible gate, open duplicate Pick or source_type≠SO returns business error

## §5.5 Edge cases

| EC | Resolution |
|---|---|
| EC-01 gate changes | derive queue on read and revalidate create |
| EC-02 duplicate/open Pick | subtract open qty and lock source lines |
| EC-03 no eligible balance | create short line without location |
| EC-04 partial pick | commit picked part then short/relocate remainder |
| EC-05 cancel after start | block; use close-short |
| EC-06 permission changed | recheck at mutation, 403 |
| EC-07 print long Thai | wrap/page safely, embedded font |
| EC-08 `[AI-DEFAULT]` concurrent mutation | version mismatch → 409 |
| EC-09 `[AI-DEFAULT]` duplicate retry | same idempotency/body returns cached response; different body →409 |
| EC-10 `[AI-DEFAULT]` inactive master | block new allocation; retain snapshot |
| EC-11 `[AI-DEFAULT]` Packing failure | Pick stays picked; safe retry |
| EC-12 `[AI-DEFAULT]` NTF failure | business commit remains; outbox retries |

## §5.6 Error catalog

| Code | HTTP | Cause |
|---|---:|---|
| ERR_VALIDATION_FAILED | 400 | input invalid |
| ERR_INSUFFICIENT_ROLE / ERR_NOT_ASSIGNEE | 403 | role/scope |
| ERR_PICK_NOT_FOUND | 404 | missing |
| ERR_STALE_DATA / ERR_IDEMPOTENCY_CONFLICT | 409 | concurrency/retry |
| BR_PICK_SOURCE_NOT_ALLOWED | 422 | non-SO source |
| BR_PICK_QUEUE_GATE_FAILED | 422 | SO not eligible |
| BR_PICK_WAVE_INVALID | 422 | mixed warehouse/max/open pick |
| BR_PICK_LOCATION_INELIGIBLE | 422 | invalid location |
| BR_PICK_SCAN_MISMATCH | 422 | scan mismatch |
| BR_PICK_QTY_INVALID | 422 | invalid quantity |
| BR_PICK_REASON_REQUIRED | 422 | missing reason |
| BR_PICK_TRANSITION_INVALID | 422 | state guard |
| ERR_DOWNSTREAM_UNAVAILABLE | 503 | Inventory/Sales/Packing unavailable |

## §5.7 Security / D-CLASS

Tenant RLS, role/ownership recheck, audit every mutation and confidential read/export, idempotent transactional outbox, log references not employee personal detail. Confidential values are omitted from public logs and unauthorized exports. No Restricted field.
