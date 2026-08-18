# 03_LOGIC — F-WH-PICK Picking

## §3.1 Scope-local functions

| ID / function | Purpose | Input → output | Side effects / calls |
|---|---|---|---|
| FN-01 `buildPickQueue` | derive SO eligibility/remaining | filters → queue rows | read SO |
| FN-02 `getScopedPick` | apply role/ownership projection | user,id → Pick | read Pick/audit |
| FN-03 `createPickRecord` | orchestrate create | source refs/assignment → Pick | ENG-01, insert, audit, Inventory allocate |
| FN-04 `validateWaveSelection` | same warehouse/max/gate/open-pick | SO refs → validation | none |
| FN-05 `assignPicker` | assign/change picker | pick,employee → Pick | IAM recheck, audit, `pick_assigned` |
| FN-06 `startPick` | assigned→in_progress | pick,user → Pick | audit |
| FN-07 `recordPickedQuantity` | scan/quantity/pick movement | line,input → line/progress | Inventory + SO + audit |
| FN-08 `recordShortQuantity` | release/backorder/short event | line,input → line/progress | Inventory + SO + NTF |
| FN-09 `relocatePickLine` | release old and allocate new | line,balance → line(s) | ENG-01 + audit |
| FN-10 `refreshAllocation` | retry allocation latest balance | line → allocated/short | ENG-01 + Inventory |
| FN-11 `requestInventoryTask` | ask Inventory replenish/transfer | missing lines → task ref | Inventory + NTF |
| FN-12 `finishPick` | validate all terminal lines | pick → picked | audit + `pick_done` |
| FN-13 `closePickShort` | short all remaining | pick,reason → picked | release/SO backorder/audit/NTF |
| FN-14 `holdOrResumePick` | pause/resume | pick,reason/action → Pick | audit |
| FN-15 `cancelPick` | cancel pre-start | pick,reason → cancelled | release all + audit |
| FN-16 `sendPickToPacking` | idempotent pack handoff | pick → pack refs | Packing + audit |
| FN-17 `buildPickPrintModel` | route-sorted A4 model | pick → print model | read only |

Every function takes tenant/user context explicitly, rechecks authorization and version, and contains no HTTP request/response terms.

## §3.2 Engine candidate

### F-WH-PICK-ENG-01: `pick-allocation-engine` (DRAFT)

| Field | Value |
|---|---|
| category | matcher / scheduler |
| owner | F-WH-PICK pending architect confirmation |
| stateless | true |
| input | item strategy, required qty, warehouse, eligible balances, location hierarchy/rank |
| output | ordered allocations plus unallocated qty and evidence rule |

Algorithm: filter active/unblocked available balances in same warehouse and allowed types; lot item orders FEFO, non-lot FIFO; order type Pick Face→Reserve→Bulk then route; split until fulfilled; never mutate balances. Caller performs atomic allocation.

Errors: `ENG_PICK_INVALID_INPUT`, `ENG_PICK_NO_ELIGIBLE_BALANCE`. Candidate registration and configurability remain OQ-03.

## §3.3 API ↔ Logic trace

| API | Functions | Engine |
|---|---|---|
| 01 | FN-01 | — |
| 02 | FN-02 | — |
| 03 | FN-03,FN-04 | ENG-01 |
| 04 | FN-05 | — |
| 05 | FN-06 | — |
| 06 | FN-07 | — |
| 07 | FN-08 | — |
| 08 | FN-09 | ENG-01 |
| 09 | FN-10 | ENG-01 |
| 10 | FN-11 | — |
| 11 | FN-12 | — |
| 12 | FN-13 | — |
| 13 | FN-14 | — |
| 14 | FN-15 | — |
| 15 | FN-16 | — |
| 16 | FN-17 | — |

No orphan function/engine; every mutation traces to at least one function.

## §3.4 Transaction boundaries

- create/relocate/refresh/pick/short/close-short/cancel commit Pick + Inventory/SO contract changes atomically or use a durable outbox/saga with compensating release
- Idempotency key result binds tenant+endpoint+body hash for 24 hours `[AI-DEFAULT]`
- optimistic version rejects stale write with 409; user reloads latest Pick
- notification outbox is after business commit and does not roll back the transaction
