# RIF v2 — F-WH-LOT · Lot/Serial + Expiry

> 2026-09-14 · W4A · source: CENTRAL_PLAN/GOLDEN_RULES.md, CONTEXT_PACK/W4.md §2–3, W4A/CHECKLIST.md. Internal scope lock only; no customer sign-off claimed.

## 1. Intent and scope
Warehouse console/master for per-item tracking policy, lot/serial records, expiry, FEFO recommendation and forward/backward movement trace. Item/Warehouse/UoM are existing master pickers. GRN/Transfer movement references are W3-LITE mock contracts: this feature does not receive or transfer stock.

## 2. Source and confidence
4 source obligations from W4 §2 and feature checklist, 1 W4 OQ default and 5 applicable global golden rules are mapped below. Confidence 84% for local business behavior; external movement shape and eligibility policies remain [ASSUMED]. No unanswered OQ stops the lane.

## 3. Requirement ledger
| ID | Requirement | Source | HTML evidence target |
|---|---|---|---|
| LOT-R01 | Per-item tracking none/lot/serial and expiry toggle | W4 §2.4; checklist | `lotItems`, item settings controls |
| LOT-R02 | Expiry required only when item config enables it | W4 §2.4 | `validate(v)` |
| LOT-R03 | FEFO for expiry-enabled item; non-expiry lot selection by receipt order | W4 §3 OQ-LOT-01 | `eligibleLots()` and ranking table |
| LOT-R04 | Trace backwards/forwards to selected lot's GRN/Transfer references | W4 §2.4 | `lotMovements`, `lotTrace()`, `lotShowMovement()` |
| LOT-R05 | Near-expiry event via NC rule, threshold external | W4 §2.4, Golden 5 | CSQ/NTF divergence declaration; no hardcoded alert threshold in production |
| LOT-R06 | Append-only movement/audit; no hard-delete | Golden 4 and W4 §2 | `lotMovements` unchanged by local actions; `state.history.unshift()` |
| LOT-R07 | console/master, no Pattern Q; CUBE Warm Light | Golden 1–2 | `#/records`, `#/history`, `#/settings` |
| LOT-R08 | #67.1/#104/#106 UI locks | Golden 8–11 | no hint, `.tabs` below `.page-head`, canonical toolbar |

## 4. Scenario outcomes
| Scenario | Trigger | Observable outcome |
|---|---|---|
| LOT-S01 | Create expiry-enabled lot without date | Date field error; no row or movement added |
| LOT-S02 | Create lot for non-expiry item without date | Record saved with null date; historical movement unchanged |
| LOT-S03 | Create serial matching another serial of same item | Duplicate error; other item's identical serial remains allowed |
| LOT-S04 | Change one item's tracking config | Only that item's create fields change; existing records/history remain |
| LOT-S05 | FEFO recommend item/warehouse | Eligible lots sorted ascending expiry; expired/held/zero excluded; no reservation |
| LOT-S06 | Recommend non-expiry item | Earliest receivedAt first, independent of expiry values |
| LOT-S07 | Select two lots in trace | Distinct movement GRN/Transfer refs, linked previous/next, empty when no history |
| LOT-S08 | Save/cancel/search/sort | Data-derived counts, cancel unchanged, filter correct, no stock mutation |

## 5. Data and validation
| Field | Type | Required | Owner/source |
|---|---|---|---|
| itemCode | master snapshot string | yes | Item master soft-reference picker |
| trackingMode | none/lot/serial | yes per item | Warehouse Product Owner config |
| expiryEnabled | boolean | yes per item | Warehouse Product Owner config |
| lotCode | string | yes when tracking lot/serial | this feature |
| serialCode | string | yes only serial mode, unique within item | this feature |
| expiryDate | ISO date/null | yes only expiryEnabled | this feature |
| onHand/held | quantity snapshot | read-only | movement/QHold mock |
| movement ref | source type/id, previous id, qty/date | read-only append-only | GRN/Transfer mock contract |

## 6. Scope lock and gaps
LOCK-W4-LOT derives from W4 pack, not customer sign-off. No real GRN/Transfer posting, NC delivery, QHold release, valuation or stock balance mutation. The source plan gives only abstract external dependencies, so proposed movement payload is [ASSUMED contract] owned by W3-LITE. FEFO tie-break and serial qty=1 are [ASSUMED] owned by Warehouse Product Owner.

## 7. OQ defaults and ownership
- OQ-LOT-01: FEFO only expiry-enabled items; other items use receipt order for pick sequence. This does not change Weighted Avg valuation. [ASSUMED] · Warehouse Product Owner.
- NC near-expiry event despite only `csq` chip: DIVERGENCE; do not silently add `ntf` declaration. Owner: central feature registry maintainer.

## 16.3 Internal scope lock reference for document chain
LOCK-W4-LOT is documented in `_SCOPE_LOCK.md` and derived from W4 pack/checklist. It is an internal reference, not a customer sign-off. BRD §3.4 and FRD §0.11 must inherit it verbatim.
