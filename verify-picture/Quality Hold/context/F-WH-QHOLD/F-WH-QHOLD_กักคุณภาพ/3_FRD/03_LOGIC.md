# Logic and state · production design + local proof boundary
| FN | Logic | Local proof |
|---|---|---|
| FN-01 | scope slices then compute summary from onHand/reservedSales/held | list/filter stats source inspection |
| FN-02 | resolve existing slice and origin; GRN QC requires mock sourceRef, later issue reason | domain tests |
| FN-03 | fetch effective DOA slots/person eligibility for action+warehouse+qty; persist selected person snapshots | domain tests |
| FN-04 | validate hold, reserve pendingHeld immediately | domain tests |
| FN-05 | DOA approved pending→active or rejected pending→0 | domain tests |
| FN-06 | reserve pendingRelease≤activeHeld−pendingRelease; ATP unchanged | domain tests |
| FN-07 | DOA release approved activeHeld−qty / rejected clears reservation | domain tests |
| FN-08 | compare expected slice/request version and idempotency/event keys atomically | isolated tests; DB transaction TODO |
| FN-09 | append request and decision events, scoped read | local append-only test; persistence TODO |
| FN-10 | query availability, do not perform sale/transfer | isolated test |

`effectiveBlocked=activeHeld+pendingHeld`, `ATP=max(0,onHand−reservedSales−effectiveBlocked)`, `holdable=onHand−reservedSales−effectiveBlocked`, `releasable=activeHeld−Σ pendingRelease`. Pending hold quarantine immediately is `[ASSUMED]` owner Warehouse Product Owner. Pending release never increases ATP. On approved release activeHeld decrements once, which increases ATP once. Reject hold restores ATP; reject release leaves existing held. Qty must be finite >0 and within Item/UoM precision; EA demo integers. Never clamp invalid qty.

Production transaction boundaries: lock slice/version and request, validate policy effective version and eligible persons, write request/projection/outbox/events atomically. DOA event adapter verifies signature/actor/SoD and sourceEventId; stale/conflicting event rejected. Backoff on unavailable Inventory/DOA, no provisional success. HTML implementation is fixture-side only; it does not prove server locks, RLS, signing or actual integration.
