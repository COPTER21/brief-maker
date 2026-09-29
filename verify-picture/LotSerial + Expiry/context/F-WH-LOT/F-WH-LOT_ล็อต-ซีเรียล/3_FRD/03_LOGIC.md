# 03_LOGIC — F-WH-LOT

## §3.1 Scope-local functions
| ID/function | Input | Deterministic business behavior | Output | Side effect |
|---|---|---|---|---|
| FN-01 `listLotIdentities` | tenant, filter/sort/page | filter and count visible identities; tenant scope | page | read only |
| FN-02 `createLotIdentity` | tenant,item,lot,serial?,expiry?,key | resolve item policy; validate; enforce same-item serial uniqueness transactionally | identity/ref or UPPER_SNAKE error | insert identity + append audit, never movement |
| FN-03 `saveTrackingPolicy` | tenant,item,mode,expiry,effective_date,version,key | reject `none+expiry`; optimistic version; retain old version | new policy version | append policy + audit |
| FN-04 `recommendLots` | tenant,item,warehouse,date,required_qty? | read availability snapshot, compute eligible, FEFO or receipt-order, tie-break | ranked candidates | none; no reservation |
| FN-05 `listLotMovements` | tenant,lot,direction | read W3-LITE mock by exact lot, follow previous/next movement ids | movement refs or empty/source-unavailable | none |
| FN-06 `openNcRules` | tenant,item | form URL/soft ref to NC rule view | destination ref | none |
| FN-08 `listLotAudit` | tenant,lot,page | return authorized immutable audit rows | page | read only |
| FN-07 `appendLotAudit` | actor,subject,before/after,key | insert immutable event once after successful mutation | event id | append only |

### FN-04 algorithm
`available_qty=max(0,on_hand_qty-held_qty)` from read-only snapshot. Candidate if available_qty>0; if item.expiry_enabled, require nonnull `expiry_date>=at_date`. Rank expiry ASC, then `received_at` ASC, then `lot_id` ASC. If expiry disabled, rank `received_at` ASC then `lot_id` ASC. No mutation; cost method is never read. Exact tie/date semantics [ASSUMED], owner Warehouse Product Owner.

### FN-02 invariant
If tracking is none, reject identity create. Lot code required for lot/serial tracking. Serial code required and quantity=1 for serial mode [ASSUMED]. Expiry date required iff expiry_enabled. Unique `(tenant_id,item_code,serial_code)` if serial not null. Item master snapshot is a soft ref; server checks policy existence, not Item FK. A duplicate or permission failure writes nothing.

## §3.2 Engine registry / CUBIC placement
No new reusable engine. `rankEligibleLots` is scope-local pure calculation called by FN-04, not a registered cross-feature Engine. ENG-NOTIFY/NC and ENG-CSQ are existing external owners; feature emits configured events only. No HTTP concepts enter a reusable engine; API handlers delegate to scope-local functions.

## §3.3 API ↔ Logic trace
| API | Function | Table/adaptor | Event |
|---|---|---|---|
| API-01 | FN-01 | T_lot_identity | none |
| API-02 | FN-02→FN-07 | T_lot_identity,T_lot_audit | identity.created (CSQ candidate only if profile says so) |
| API-03 | FN-03→FN-07 | T_item_tracking_policy,T_lot_audit | master.changed CSQ |
| API-04 | FN-04 | T_lot_identity + availability adapter | none |
| API-05 | FN-05 | W3-LITE movement adapter | none |
| API-06 | FN-08 | T_lot_audit | none |
| API-X2 | FN-06 | NC central soft link | none locally |
All mutation APIs have scope-local functions; all listed functions are called. No orphan Engine.

## §3.4 Integration
W3-LITE supplies immutable movement and availability read adapters only. NC owns expiry threshold/channel. Picking consumes ranked candidates but must revalidate before reservation. CSQ receives event envelope after committed policy change, with idempotency key; no feature-local consequence calculation.

## §3.5 Locked/OQ
LOCK-W4-LOT; OQ-LOT-01; [ASSUMED] tie-break, qty=1, effective date and external payload; owners in 07_LOCKED.
