# E2E Result — F-WH-ROP

- Run: 2026-09-18 (PM/BA re-gate)
- Command: `.tools\python.cmd outputs\F-WH-ROP\_e2e\e2e-f-wh-rop.py outputs\F-WH-ROP\F-WH-ROP.html`
- FN covered: 8/8
- FN-40: 0/0
- Tests: 8/8 PASS
- Console errors from feature code: 0

| Test | Result |
|---|---|
| FN-01 list/filter/sort/counts | PASS |
| FN-02 versioned policy + field-level invalid bounds + overlay cleanup | PASS |
| FN-03 exact Item×Warehouse effective policy | PASS |
| FN-04 Safety-driven ROP/target + ATP/On-Order/ADU/Lead Time/Pack Size + 3 statuses | PASS |
| FN-05 searchable dropdown + no-policy card + prefilled create action | PASS |
| FN-06 notification busy state + human-readable toast + idempotency | PASS |
| FN-07 PR busy state + grouped Draft + preferred vendor + no auto-submit | PASS |
| FN-08 recompute replay + append-only history + demo-only hide | PASS |
