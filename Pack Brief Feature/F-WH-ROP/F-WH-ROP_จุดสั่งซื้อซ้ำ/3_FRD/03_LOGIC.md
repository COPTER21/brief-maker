# 03_LOGIC · F-WH-ROP

## Function registry and placement
All FN operate outside HTTP; HTTP layer parses/authenticates/calls only. Demo JS analogue is shown for trace, while production persistence/authorization remain unimplemented locally.

| FN | Purpose/input→output | Demo analogue | Side effect / API |
|---|---|---|---|
| FN-01 `validatePolicy` | decimals/date/refs → errors or normalized input | `ropValidate`, `ropSaveFromDrawer` blank/master checks | none; API-02 |
| FN-02 `appendPolicyVersion` | validated policy+expectedVersion → new version/event | `ropSavePolicy` | production transaction inserts policy+outbox, never UPDATE prior; API-02 |
| FN-03 `selectActivePolicy` | pair+asOf → latest effective version or NO_POLICY | `ropPolicyActive` | read; API-01/03 |
| FN-04 `readAvailability` | pair+asOf → upstream `{onHand,held,snapshotRef,asOf}` | `ropSnapshot` fixture | read-only; API-03 |
| FN-05 `computeSuggestion` | active policy+snapshot → available/triggered/qty | `ropEvaluatePair`, `ropSuggestions` | pure; API-03 |
| FN-06 `preparePRMock` | positive suggestion+key → mock ack/replay | `ropPreparePR` | append mock event, no PR/stock; API-04 |
| FN-07 `prepareNCCandidate` | policy+snapshot+ruleRef+key → envelope/replay | `ropNcCandidate` | append candidate event, no delivery; API-05 |
| FN-08 `readEventHistory` | scoped pair/cursor → immutable events | `ropEvents`, `ropRows` settings | read; API-06 |
| FN-09 `filterVisibleRows` | query/type/status/sort → visible rows/count | `fillFilters`, `renderTableOnly` | UI-only; no HTTP |

## Formula and temporal selection
`selectActivePolicy`: filter tenant, exact item and warehouse with `effectiveDate≤tenant-local asOf date`, order effectiveDate descending then version descending. A future version does not supersede current before its date. `validatePolicy`: 0≤safety≤min≤max, finite decimal, valid calendar date, known scoped refs; blank values invalid. `readAvailability` treats missing/stale snapshot as error, never as zero; stock is not modified. `computeSuggestion`: `available=max(0,onHand−held)` and data-quality event if held>onHand `[ASSUMED]`; `triggered=available≤min`, `qty=triggered?max(0,max−available):0`. The PR mock accepts only triggered positive qty; NC candidate may be sent above ROP min because NC owns its own threshold. Both include tenant, pair, policyVersion, snapshotAsOf/ref and idempotency key. Replay returns same ack, conflicting body for same key is error in production. Recompute may append a `suggestion.evaluated` event once per pair/version/asOf/available; never rewrites movement or stock.

## Engine registry
None new. Formula is scope-local FN-05; NC rule engine and Procurement workflow remain external. Do not build a ROP notification engine or PR workflow.

## §3.3 API → function trace and orphan audit
API-01→FN-03; API-02→FN-01→FN-02; API-03→FN-03→FN-04→FN-05; API-04→FN-06; API-05→FN-07; API-06→FN-08; API-07→existing master lookup adapter (external, no new FN). FN-09 is UI-only, invoked by `renderTableOnly`. No orphan function. Pure FN-05 does no HTTP/DB write; FN-02/06/07 own persistence/outbox side effects. HTTP transport/authorization remain in 02_API, declarative bounds/errors in 05_RULES.

Local demo creates no actual PR, notification, stock or movement record; all downstream acknowledgements are mock only.
