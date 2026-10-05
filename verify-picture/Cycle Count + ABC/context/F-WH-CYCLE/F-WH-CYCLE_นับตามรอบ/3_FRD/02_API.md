# Proposed production API · tenant/warehouse scoped, TODO
| ID | Method/path | Contract | FN |
|---|---|---|---|
| API-01 | GET `/cycle/abc-policy?asOf` | effective policy by requested `asOf` date (greatest effectiveDate≤asOf), version/basis/thresholds/cadence/window | FN-01 |
| API-02 | POST `/cycle/abc-policy` | validate totals/dates/version; append version and audit | FN-01,08 |
| API-03 | GET `/cycle/abc-classes?warehouseRef` | snapshot score/share/class, source asOf, actual class totals | FN-02,09 |
| API-04 | GET `/cycle/sessions?view=counter|reviewer` | counter projection excludes expected/value/variance in JSON/export; reviewer after submit includes comparison | FN-04,09 |
| API-05 | POST `/cycle/plans` | Item/Warehouse/UoM/valuation snapshot + assigned person/effective policy resolved by plan asOf date, due, version | FN-03,08 |
| API-06 | POST `/cycle/sessions/{id}/attempts` | finite count incl zero, captured conversion, assignment/version/idempotency; immutable attempt | FN-05,08 |
| API-07 | POST `/cycle/sessions/{id}/review` | latest attempt, reviewer, accept+reason or recount; version/idempotency | FN-06,08 |
| API-08 | POST `/cycle/sessions/{id}/stockadj-mock` | reviewed nonzero only, payload/ack/ref; no posting | FN-07,08 |
| API-09 | GET `/cycle/events` | scoped append-only history | FN-08,09 |

403 role/scope/assignment, 404 master/session, 409 stale/idempotency/old attempt, 422 invalid policy/count/snapshot, 503 Inventory/W3 mock unavailable. All writes transactionally version-guarded. API-08 adapter W3-LITE only; no real StockAdj creation/posting or Inventory balance change. CSQ outbox candidate owner-reviewed later. API-04 server query must not leak expected in counter JSON, headers, sort metadata, CSV or error messages. A counter cannot force `?view=reviewer`; API-03 valuation/class source and all exports must apply the same role policy or return a redacted projection while blind assignment is active.
