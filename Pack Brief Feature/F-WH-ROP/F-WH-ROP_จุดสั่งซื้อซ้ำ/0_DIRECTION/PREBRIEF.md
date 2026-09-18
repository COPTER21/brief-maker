# PREBRIEF · F-WH-ROP · Reorder Point

> W4A FULL · 2026-09-14 · console/master · AI 100%

## 1. Source and obligation
Configure Min/Max/Safety/Lead Time and ADU window per Item×Warehouse. Read ATP and movement history from F009 only; F009 already excludes reserved and Quality Hold. Evaluate daily and on every movement that drops ATP below Min, emit Notification, and automatically create one editable F072 PR Draft per warehouse per evaluation round. Drafts are never auto-submitted to DOA and are not split by vendor. Confirmed PM/BA scope dated 2026-09-17 supersedes the former PR mock wording.

## 2. Scenarios with observable expected outcome
| ID | Type | Given/When | Expected |
|---|---|---|---|
| S-01 | happy | policy maintainer selects ITEM-101/WH-01, min10/max30/safety5, future effective date and saves | one new version for this pair, history event; other warehouse policy unchanged |
| S-02 | negative | safety>min or min>max or negative input | field error, no version/event |
| S-03 | boundary | ATP=10 equals min10 | not triggered because the confirmed boundary is strictly below Min |
| S-04 | boundary | ATP8, min10, max30, ADU2/day, lead time7, on-order0, pack12 | triggered; raw quantity36 and rounded quantity36 |
| S-05 | alternate | ATP=11 above min10 | no positive replenishment suggestion or PR Draft |
| S-06 | isolate | ITEM-101 WH-01 and WH-02 have different policies | evaluation uses exact pair, never cross-warehouse threshold |
| S-07 | change | change WH-01 min/max with effective date | new policy version; suggestions recompute from active version; old history preserved |
| S-08 | missing | no policy for selected Item×Warehouse | explicit `ยังไม่มีนโยบาย` state, no invented min/max |
| S-09 | held | F009 returns ATP8 after reserved/hold exclusion | use ATP8 directly; never query or subtract hold again |
| S-10 | PR | more than one item is below Min in WH-01 during one evaluation round | create one F072 PR Draft for WH-01 with multiple lines and optional suggested vendors |
| S-11 | retry/error | repeat the same warehouse/round/snapshot key or F072 is unavailable | reuse the same Draft/no duplicate event, or show retryable unavailable state |
| S-12 | `#/history` emit Notification event | idempotent event |
| S-13 | `#/settings` | append-only |

## 3. Data dictionary
| Field | Required/validation | Source/owner |
|---|---|---|
| `itemCode`, `warehouseRef` | yes, soft refs, unique pair policy | existing Item/Warehouse |
| `minQty`, `maxQty`, `safetyQty`, `leadTimeDays` | nonnegative and safety≤min≤max; values are per Item×Warehouse | policy config/Warehouse Product Owner |
| `effectiveDate`, `version` | date and optimistic version; no silent overwrite | policy config |
| `aduWindowDays`, `packSize` | window 30/60/90 (default 30); pack size >0 | policy config / purchase UoM |
| `adu` | average daily outbound from F009 movement history; DN/internal issue/production only | Inventory F009 |
| `onOrder` | outstanding open PO receipts plus unclosed PR Drafts for Item×Warehouse | Purchase |
| `atp`, `asOf` | read directly from F009; already excludes reserved/hold | Inventory F009 |
| `triggered`, `suggestedQty` | `ATP<Min`; `max(0,(Max−ATP−OnOrder)+(ADU×LeadTime))`, rounded up to Pack Size | this feature |
| `notificationEvent` | `reorder_point.triggered` | Notification |
| `prDraftId`, `idempotencyKey` | one Draft per warehouse/evaluation round; replay-safe | F072 |

## 4. Pages and actions
`#/records` searchable policy list with Item/Warehouse filters and create/edit drawer; `#/history` recomputed suggestions from ATP/ADU/On-Order with actions to emit Notification and create the warehouse PR Draft; `#/settings` immutable policy/suggestion/notification/PR Draft history. Empty/error/disabled states are explicit. Stats are data-derived.

## 5. Rules and ownership
| ID | Rule | Source/status |
|---|---|---|
| BR-01 | one effective policy per Item×Warehouse/date, versioned | W4 §2/Golden Rule 4 |
| BR-02 | min/max/safety and effective date are config | W4 §2/§5 |
| BR-03 | `0≤safety≤min≤max` | `[ASSUMED]` Warehouse Product Owner |
| BR-04 | trigger only when `ATP<Min`; quantity `max(0,(Max−ATP−OnOrder)+(ADU×LeadTime))`, rounded up to purchase Pack Size | PM/BA 2026-09-17 |
| BR-05 | read ATP from F009 as-is; never query/subtract Quality Hold again | PM/BA 2026-09-17 |
| BR-06 | emit idempotent `reorder_point.triggered` through Notification | PM/BA 2026-09-17 |
| BR-07 | create one editable F072 PR Draft per warehouse/evaluation round; do not split by vendor or auto-submit | PM/BA 2026-09-17 |
| BR-08 | version/suggestion/notification/PR Draft audit append-only and idempotent | Golden Rule 4 |

## 6. Dependencies, OQ and declarations
References: F009 Inventory/ATP and movement history; F088/F090 are already reflected inside F009 ATP and must not be queried again; F072 creates the editable PR Draft; F073 Compare Vendors occurs after PR and vendor does not split the Draft; Notification receives `reorder_point.triggered`. Declaration selected for this run: `ntf-declaration`. F072 retains its normal DOA only after a human submits the Draft. No DOCCFG for F085.

## 7. Planned coverage route
| Scenarios | Route/handler planned | Boundary |
|---|---|---|
| S-01/02/06/07/08 | `#/records` list and drawer save | local config, server version contract |
| S-03/04/05/09 | `#/history` evaluate pair and availability | read-only snapshot |
| S-10/11 | `#/history` create grouped F072 PR Draft | one warehouse per round; Draft only |
| S-12 | NTF | an item drops below Min | emit idempotent `reorder_point.triggered` event through Notification |
| S-13 | history | auditor opens policy/suggestion/notification/PR history | records are append-only with no edit/delete action |
