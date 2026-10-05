# PREBRIEF · F-WH-QHOLD · Quality Hold

> W4B FULL · source W4 §2–3, F088 checklist, Golden Rules, Astra planning; all cross-lane contracts mock. Console/master. No wizard, no banner/hint.

## 1. Surface and journey
Three tabs directly under page-head: **รายการกัก**, **รออนุมัติ**, **ประวัติ**. Canonical toolbar filter in each list. Create/view drawer for hold/release; DOA required slot rows appear as searchable person pickers with avatar/initial, name, position and department, populated from mock policy response. Distinguish selected approver snapshot from active user; any demo decision harness uses `data-demo` and orange DEMO badge with FRD/UI Brief Demo-only section. Main actions in page-head, not tab control. No Pattern Q. Source GRN QC mock reference or later-issue reason is recorded, but no GRN transaction is created.

## 2. Data and arithmetic
`stockSlice={id,itemRef,warehouseRef,locationRef,lotRef,onHand,reservedSales,activeHeld,pendingHeld,version}`. `holdRequest={id,key,kind,qty,reason,origin,sourceRef,selectedSlots,status,version}`. `approvalPolicy` from DOA mock provides required slot IDs and eligible actual person records; do not hardcode role chain. `quarantineEvent` append-only has event ID, request ID, type, qty, time, actorRef, sourceEventId. `pendingRelease` is sum of requested release not yet decided; `releasable=activeHeld−pendingRelease`. `effectiveBlocked=activeHeld+pendingHeld`; `ATP=max(0,onHand−reservedSales−effectiveBlocked)` and transferable uses same eligible amount `[ASSUMED]`. Requested hold temporarily sets pendingHeld immediately; approve moves pendingHeld→activeHeld with ATP unchanged; reject removes pendingHeld. Requested release reserves releasable but does **not** reduce activeHeld or increase ATP; approve reduces activeHeld once; reject releases reservation only. Neither flow changes onHand or movement ledger. Validate finite qty>0, Item UoM precision and no over-hold/over-release; reject rather than clamp.

## 3. Observable scenarios
| ID | Given / action | Expected local result |
|---|---|---|
| S-01 | baseline onHand100 reservedSales10 held0; request hold30 with valid DOA slots | status requested; pendingHeld30, ATP60, onHand100; not auto-approved |
| S-02 | after S-01 mock DOA approve event E1 then replay E1 | activeHeld30, pendingHeld0, ATP60, onHand100; one applied event |
| S-03 | reset baseline; request hold30 then reject | pendingHeld0, activeHeld0, ATP90, rejected; no movement change |
| S-04 | after approved hold30; request release12 then approve E2 | pending release12 keeps ATP60/releasable18; approval activeHeld18, ATP72, onHand100 |
| S-05 | approved hold30; request release12 then reject | activeHeld30, pending release0, releasable30, ATP60 |
| S-06 | approved hold30; concurrent release20 and15 at same version | first reserves20, second stale/over-limit rejected; approve20 → held10, ATP80; retry15 fails >10 |
| S-07 | baseline: hold91, 0, negative, NaN, overprecision; then hold90 and extra1 | invalid attempts no request, ATP90; hold90 pending, ATP0; extra1 rejected |
| S-08 | approved hold30; release31 and0 rejected; release30 approved/replay | pending state ATP60; approved held0, ATP90; replay stays90 |
| S-09 | DOA mock two required slots, distinct eligible people | missing/ineligible choice blocks; valid named person snapshots persist; policy changes revalidate; rejected request cannot be approved |
| S-10 | approved hold30; ask transfer/sale availability qty61 then qty60 | qty61 rejected, qty60 contract-valid only; onHand100/held30 unchanged; other slice unaffected; no transaction |

## 4. Other acceptance and exceptions
Partial hold/release by lot/location, cancel drawer no data mutation, duplicate submit key returns same request, approval event sourceEventId idempotent, stale/conflicting decision rejected, history append-only with request/decision actor and time, filter source GRN details mock, status/stat/count recomputed from stock/request data. Outbound availability is **contract validation only**, not an actual sale/transfer. A hold request from GRN QC needs sourceRef mock; later issue may have nullable sourceRef with reason. Stock slice picker is a soft-ref snapshot. If some lot/location has zero eligible qty, show explicit unavailable state; never reserve a different slice. No hard delete or movement edit controls.

## 5. Rule table and owners
| ID | Rule | Source/owner |
|---|---|---|
| BR-01 | slice identity and origin required, partial qty | W4 §2; Warehouse owner |
| BR-02 | DOA slot selected people from external policy, no fixed chain | Golden Rule 3; DOA owner |
| BR-03 | held onHand, excluded ATP/transfer | W4 OQ-QH-01 `[ASSUMED]`; Inventory owner |
| BR-04 | append-only events and stock/movement unchanged | Golden Rule 4 |
| BR-05 | qty finite/UoM precision, hold≤free, release≤releasable | `[ASSUMED]` Warehouse/Inventory owners |
| BR-06 | pending hold blocks ATP immediately, pending release does not free | `[ASSUMED]` Warehouse Product Owner |
| BR-07 | approval/reject atomic/idempotent with sourceEventId/version | `[ASSUMED contract]` DOA owner |
| BR-08 | GRN QC, NC/NTF, CSQ are mock/declaration only | W4 §2/5; respective owners |

## 6. Declarations and dependency gaps
Chips are `doa,ntf,csq` exactly. DOA brief needs actual slot policy reference/eligible-person contract and no duplicate automatic DOA notification events. NTF declares business hold/release result only, central NC owns channels/recipients. CSQ declares consequence candidate only, no local 7C stamp. GRN F079 W3-LITE is pending; its QC origin is mock `[ASSUMED contract]`. Existing Item/UoM master entry is absent from FEATURE_LIST_ALL though UI needs picker: log source gap; no master implementation. Mock assertions are payload/ack/idempotency and unchanged stock/ledger target, not external end-to-end. OQ-QH-02/03/04/05/06 owners in RIF and HANDOFF.
