# 05_RULES — F-WH-PACK Packing

## §5.1 Business Rules

| ID | Rule | Enforcement | Error |
|---|---|---|---|
| BR-PACK-01 | intake only confirmed Picking `picked→to_pack`, picked qty>0, no service | FN-01/source contract | `BR_SOURCE_NOT_ELIGIBLE` |
| BR-PACK-02 | free item allocates normally; print marks no tax value | FN-04/ENG-02 | — |
| BR-PACK-03 | one job per Pick source SO; replay stable | unique key/FN-01 | `ERR_IDEMPOTENCY_MISMATCH` |
| BR-PACK-04 | max one active carton | partial unique/FN-03 | `BR_ACTIVE_BOX_EXISTS` |
| BR-PACK-05 | sum allocation ≤ picked per source line; qty>0 | transaction/ENG-01 | `BR_QTY_EXCEEDS_PICKED` |
| BR-PACK-06 | master/custom snapshots; capacity overage warns only | FN-03/ENG-01 | `BR_INVALID_CARTON` |
| BR-PACK-07 | computed=tare+Σqty×weight; actual override persists | ENG-01 | `BR_WEIGHT_SOURCE_MISSING` |
| BR-PACK-08 | close requires non-empty active carton; label version created | FN-05 | `BR_EMPTY_CARTON` |
| BR-PACK-09 | finish iff remaining=0, no active, closed≥1 | FN-07 | `BR_PACK_INCOMPLETE` |
| BR-PACK-10 | reopen only before DN; previous label invalid | FN-06/08 | `BR_PACK_LOCKED_BY_DN` |
| BR-PACK-11 | shipped only on confirmed stable DN ref | FN-10 | `BR_DN_CONTRACT_UNAVAILABLE` |
| BR-PACK-12 | cancel before DN with nonblank reason; job returns queue | FN-09 | `BR_CANCEL_REASON_REQUIRED` |
| BR-PACK-13 | BOXLABEL 150×100 per carton; PACKSLIP A4 per pack | ENG-02 | `ERR_PRINT_FAILED` |
| BR-PACK-14 | workspace editable only in_progress | API permission/read model | `BR_PACK_NOT_EDITABLE` |
| BR-PACK-15 | every mutation/state/print/integration is append-only audited | FN-11 | `ERR_AUDIT_WRITE_FAILED` |
| BR-PACK-16 | notification settings/recipients/channels owned by ENG-NOTIFY | outbox/NTF | `ERR_EVENT_PUBLISH_FAILED` |

## §5.2 State Machine

| From | Action | To | Roles/Conditions |
|---|---|---|---|
| queue | start | in_progress | wh_lead or scoped packer; job free |
| in_progress | finish | packed | BR-PACK-09; permission OQ-03 |
| packed | reopen | in_progress | wh_lead; no DN |
| packed | DN success | shipped | wh_lead; versioned contract |
| in_progress/packed | cancel | cancelled | authorized; reason; no DN |

Carton active→closed; closed→active only by wh_lead/no DN/no other active.

## §5.3 Permission Matrix

Server authority matches BRD §4. Tenant/warehouse/ownership are conjunctive, not alternatives. Permission is rechecked at mutation time; shipped is immutable for all roles.

## §5.4 Validation

- UUIDs/schema valid; scan token length/charset bounded and sanitized.
- `qty`, tare, weight are decimal, finite and within DB precision; no float arithmetic.
- reason trimmed and bounded; required for cancel/reopen/override according to policy.
- source line, lot and UOM must belong to job snapshot; UOM converts exactly to base quantity.
- `If-Match` must equal current version; idempotency key+body hash must match prior request.

## §5.5 Edge Cases / Probes

| ID | Probe | Resolution | Test |
|---|---|---|---|
| EC-01 | PR-7/PR-4 intake or mutation retry | same key+body returns same result; no duplicate audit | AT-02/16 |
| EC-02 | PR-2 concurrent allocation | atomic version/lock; one wins, other 409 | AT-06 |
| EC-03 | PR-3 permission revoked | mutation recheck returns 403 | AT-18 |
| EC-04 | PR-9 two scans use last qty | source-line reconcile in transaction | AT-06 |
| EC-05 | PR-8 cancel/reopen | explicit compensating state + label invalidation | AT-11/12 |
| EC-06 | missing weight master | block production auto-compute or require authorized actual weight path | AT-08 |
| EC-07 | print/render outage | queue retry; business state unchanged | AT-14 |
| EC-08 | notification outage | outbox retry; no rollback | XT-04 |
| EC-09 | DN outage/replay | remain packed; stable idempotency | XT-03 |
| EC-10 | Transfer mock path | disabled until locked contract | XT-02 |

## §5.6 Error Catalog

Common: `ERR_NOT_AUTHENTICATED` 401, `ERR_INSUFFICIENT_ROLE`/`ERR_PERMISSION_REVOKED` 403, `ERR_NOT_FOUND` 404, `ERR_STALE_DATA`/`ERR_IDEMPOTENCY_MISMATCH` 409, rule codes above 422 or 409 where state conflict, `ERR_RATE_LIMITED` 429, `ERR_INTERNAL` 500, `ERR_DEPENDENCY_UNAVAILABLE` 503. Messages localize at presentation boundary.

## §5.7 Security

- JWT/session via shared IAM; ABAC tenant+warehouse+role+ownership.
- Request schema validation and scan sanitization; rate limits on scan/export/print.
- Confidential contact/employee data excluded from logs/events unless explicitly necessary.
- Audit failure blocks mutation because BR-PACK-15 requires atomic evidence.
- Event/print payloads have version/hash and least-data principle.

## §5.8 Rule → Edge Coverage

BR-01/03→EC-01; BR-04/05→EC-02/04; BR-06/07→EC-06; BR-08/09→AT-07/09/10; BR-10/12→EC-05; BR-11→EC-09; BR-13→EC-07; BR-14→EC-03; BR-15→atomic audit tests; BR-16→EC-08.
