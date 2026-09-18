# S6a ledger-first plan · F-WH-ROP

Before case drafting: enumerate all 18 FRD AT assertions, PREBRIEF S01–13, BR/R01–08, error/validation paths, role cells, cross-module XT and LOCK01–06. Planned IDs below are reserved; every row needs a finished case or explicit backend-only status, not silent drop.

| Coverage item | Reserved TC IDs |
|---|---|
| AT-01–04, NO_POLICY, bounds, nonfinite/date | TC-001–004, TC-019–027 |
| AT-05–09, boundary, held, warehouse isolation | TC-005–009, TC-028–035 |
| AT-10–11, effective/version/event | TC-010–011, TC-036–040 |
| AT-12–17, PR/NC mock/replay/stock | TC-012–017, TC-041–047 |
| AT-18, list/filter/empty | TC-018, TC-048–050 |
| S-01–13; BR/R-01–08 | TC-001–018 plus TC-019–047 |
| REQUIRED, BAD_REFERENCE, POLICY_BOUNDS, BAD_EFFECTIVE_DATE, VERSION_CONFLICT | TC-019–027, TC-051 (backend) |
| SNAPSHOT_UNAVAILABLE/STALE, NO_POSITIVE_SUGGESTION, MOCK_UNAVAILABLE, IDEMPOTENCY_CONFLICT, NC_RULE_MISSING | TC-034–035, TC-043–047, TC-052–054 (backend) |
| ACCESS_DENIED, role cell Maker allow/deny, Reviewer read/deny, Auditor read/deny, cross-tenant | TC-055–058 (backend harness) |
| XT-PR-01/02, XT-NC-01/02, XT-INV-01 | TC-041–047, TC-053–054; actual downstream OOS |
| LOCK-01–06 | TC-018, TC-038, TC-044, TC-047, TC-050, TC-058 |
| CSQ/NTF declaration draft | TC-059–060 backend contract-only, no engine outcome |

Audit target: 60/60 reserved cases, 18/18 AT, 13/13 S, 8/8 BR/R, 6/6 LOCK; backend-only cases explicitly marked and retained in QA mirror as `sys:true`. Out-of-scope live PR creation, NC delivery, real CSQ stamp and movement updates are excluded with reasons. Exact counts verified after generation.
