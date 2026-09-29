# PREBRIEF — F-WH-LOT · Lot/Serial + Expiry

> Source: RIF_v2.md plus W4 context/checklist. `[ASSUMED]` defaults require owner review in handoff; they do not pause FULL lane.

## 1. Obligations
| Obligation | Source | Section |
|---|---|---|
| Item-level tracking and expiry | W4 §2.4 | §3–5 |
| FEFO/OQ-LOT-01 | W4 §3 | §2, §5 |
| Movement trace mock | W4 §2.3 | §2, §6 |
| Expiry notification via NC | W4 §2.4 | §7 |
| Append-only / soft refs | GOLDEN 4–5 | §3, §6 |
| UI #67.1/#104/#106 | GOLDEN 8–11 | §4 |

## 2. Scenarios and expected results
| ID | Type | Preconditions/action | Expected state or UI |
|---|---|---|---|
| S-01 | Happy | Expiry-enabled ITEM-101, choose lot code and valid ISO expiry, save | New master row; no movement added; count rises 1 |
| S-02 | Negative | ITEM-101 date blank | Error on expiry, row count unchanged |
| S-03 | Alternate | ITEM-103 expiry disabled, date blank | Save succeeds with `expiryDate=null` |
| S-04 | Negative | ITEM-102 serial `SN-102` already exists on same item | Duplicate error; no row added |
| S-05 | Happy | Item settings: change ITEM-101 lot→serial | Only ITEM-101 config changes; create form requires serial; historical movement immutable |
| S-06 | Happy | ITEM-101 FEFO with Oct01, Oct15, expired Sep01, fully-held Nov01 | Oct01 first, Oct15 second; expired/held excluded; onHand unchanged |
| S-07 | Alternate | ITEM-103 non-expiry lots with different receipts | Oldest `receivedAt` first, then stable lot code tie-break |
| S-08 | Happy | Select LOT-2609-011 then LOT-2609-012 in trace | First shows GRN-2609-014 and Transfer-2609-009 linked; second GRN-2609-016; no cross-lot history |
| S-09 | Exception | New lot has no movement | Empty trace state; no invented GRN reference |
| S-10 | Negative | Save same input twice | Idempotency guard blocks second local prototype save |

## 3. Data dictionary
| Field | Type | Required | Source |
|---|---|---|---|
| itemCode | master key snapshot | yes | Item picker, soft-reference |
| lotCode | string | tracking=lot/serial | this feature |
| serialCode | string/null | tracking=serial | this feature; unique per item |
| expiryDate | ISO date/null | expiryEnabled | this feature |
| tracking | enum none/lot/serial | yes | item configuration |
| expiryEnabled | boolean | yes | item configuration |
| receivedAt | ISO date | movement-backed lots | W3-LITE mock |
| onHand, held | decimal ≥0 | read-only | inventory/QHold snapshots |
| movementId, previousMovementId | string/null | read-only | W3-LITE mock |
| sourceRef | type/id snapshot | read-only | W3-LITE mock |

## 4. Pages and actions
`#/records`: list/search/filter/sort, data-derived KPIs, create and view drawer. `#/history`: selected lot's real movement rows and previous/next detail. `#/settings`: item picker, tracking and expiry controls, FEFO/FIFO recommendation. Tabs sit directly below page header; canonical toolbar block is required. No hint/banner. No Pattern Q.

## 5. Business rules
- BR-01 expiry required iff chosen item's expiryEnabled; never infer from item name.
- BR-02 serial unique within item. Serial quantity=1 [ASSUMED], owner Warehouse Product Owner.
- BR-03 eligible=onHand−held>0 and unexpired when expiryEnabled. FEFO by expiry ASC; tie by receivedAt then lot code [ASSUMED]. Non-expiry by receivedAt ASC. Recommendation never reserves stock.
- BR-04 editing settings is append-only audit event and does not modify past lot/movement snapshots.
- BR-05 master refs use picker snapshots; no hard FK validation.

## 6. Dependency hooks
GRN/Transfer W3-LITE movement is a read-only mock containing source reference, target, qty, time and predecessor movement id. No receiving/transfer UI or stock mutation. This contract is [ASSUMED], owner W3-LITE. QHold held qty is read-only mock; NC expiry threshold lives in NC rules.

## 7. OQ, declarations and divergence
OQ-LOT-01 default as W4 §3. `csq` declaration chip only. Expiry notification requirement detects `ntf`, creating DIVERGENCE against feature-list chip; log and leave chip unchanged pending registry owner.

## 8. Coverage matrix
| Scenario | BR | Route/selector | Function |
|---|---|---|---|
| S-01/S-02/S-03/S-04 | BR-01/02 | drawer #f0–#f3 | `validate`, `saveRecord` |
| S-05 | BR-04 | #/settings | `lotSaveSetting` |
| S-06/S-07 | BR-03 | #lotRecommendation | `eligibleLots`, `lotRecommend` |
| S-08/S-09 | BR-05 | #/history, #movementDetail | `lotTrace`, `lotShowMovement` |
| S-10 | BR-02 | drawer #saveBtn | `saveRecord` |
