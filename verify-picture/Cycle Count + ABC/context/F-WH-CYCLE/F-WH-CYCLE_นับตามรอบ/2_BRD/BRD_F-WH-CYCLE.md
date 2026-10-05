# BRD · F-WH-CYCLE นับตามรอบ
2026-09-14 · AI-reviewed specification, no human sign-off. Sources W4 §2–3, F086 checklist, RIF_v2, PREBRIEF S01–10 and Scope Lock. Owner Warehouse Product Owner.

## 1. Outcome
Use configurable ABC to plan assigned rotating counts, preserve blind counter input, review discrepancies, then send only reviewed nonzero delta to Stock Adjustment W3-LITE mock. Never mutate onHand or movement ledger. Targets: deterministic S01–10 fixtures, zero blind leaks/duplicate mock requests; baseline unknown `[ASSUMED]`.
## 2. Scope
In: ABC policy/effective date, class/due snapshot, plan assignment, blind submit, authorized review/recount, mock StockAdj acknowledgement, append-only audit, csq draft. Out: Stocktake, actual StockAdj approval/posting, GRN/PO/JE, DOA/NTF, Inventory mutation. Console/master, no wizard.
## 3. Source interpretation
W4 §3 OQ-ABC-01 monetary VALUE70/20/10 default, A monthly/B quarterly/C half-year. W4 §2 value×frequency becomes optional effective policy basis `[ASSUMED]`; do not relabel weighted score as monetary value. OQ-ST-02 detail absent: counter API/UI/export omit expected/value/variance even after submit/recount `[ASSUMED]` owner Warehouse Product Owner. Prototype JS fixture is no security boundary.
## 4. Actors
Policy maker configures effective policy/plan; assigned counter sees refs/UoM/own count only and submits; reviewer sees comparison after submit and accepts/recounts; auditor reads immutable history. Production tenant/warehouse RLS, assignment/version and separation enforced server-side. DEMO persona switch only reviewer harness.
## 5. Entity contract
ABCPolicy(id,basis,windowDays,thresholdA/B/C,cadence,effectiveDate,version); ItemSnapshot(itemRef,warehouseRef,value,movementCount,asOf); Plan(id,policySnapshot,classSnapshot,dueDate,assignedCounterRef,status); Session(id,version,lines[item/lot/location/uom/expectedBaseQtySnapshot/factorSnapshot],attempts[],reviewReason,stockAdjMockRef); Attempt(id,countedQty,countedBase,factorSnapshot,at,actorRef); immutable Event. OnHand/movement Inventory owned read-only. Soft Item/Warehouse/Lot/UoM refs.
## 6. Business stories
US01 default values40/30/20/10→A,A,B,C. US02 optional weighted X100×1,Y50×4 ranks Y only weighted, X default. US03 tie30/30/20/20→A,A,A,B actual80/20/0; zero total all C. US04 invalid sum105 rejected/new valid policy leaves old plan unchanged. US05 Jan31 due A Feb28,B Apr30,C Jul31. US06 blank count blocked/zero accepted, counter blind, reviewer sees expected12−0=12 variance−12. US07 100/100 review closes no StockAdj. US08 100/104 +4 after review yields one mock ref only. US09 first97/recount99 latest−1. US10 1box=12pcs expected24 count3boxes→36/+12, later mapping change no rewrite and retry same ref.
## 7. Lifecycle
Assigned→Submitted→Reviewed or RecountRequested→Submitted(new attempt)→Reviewed. Review accept requires reason; recount opens blank blind form, old attempt locked. Reviewed zero closes. Reviewed nonzero may become AdjustmentRequested after mock ack. Submit never dispatches. Stale/old attempt rejected.
## 8. ABC algorithm
Policy percentages nonnegative and sum100; value/frequency nonnegative. Score default=value, optional value×qualifying movement count in 90-day window `[ASSUMED]`. Sort descending score, stable itemCode tie. Class uses cumulative percentage BEFORE each indivisible item: <A→A, <A+B→B, otherwise C; actual shares may overshoot. Total0→all C. Policy version/effective date frozen into plan, no retroactive class rewrite.
## 9. Cadence
A1/B3/C6 calendar months from last accepted review; clamp Jan31→month end `[ASSUMED]`, owner Warehouse Product Owner. Effective policy changes future plans only. Frequency may prioritize due items within class; no invented notification threshold.
## 10. Blind count
Counter server projection/view/export omits expected qty/value/variance even after submit; reviewer only after submitted. Counted null invalid, zero valid; finite nonnegative. Base conversion uses captured factor, not current UoM mapping. No CSS-only security. Assignment checked on every submit.
## 11. Reviewer and StockAdj mock
Reviewer accepts with reason or requests recount, never auto-recount from variance threshold. Latest accepted nonzero payload includes sourceSessionId,attemptId,policySnapshotId,item/lot/location/warehouse,baseUom,expectedBase,countedBase,delta,reviewerRef,reason,idempotencyKey. W3-LITE mock returns ack/ref only; retry same key same ref. No stock/movement edit or actual approval/posting.
## 12. Exceptions
Reject invalid policy sum/negative score/bad date, zero-total division, missing snapshot/factor, unassigned counter, blank/negative/NaN count, stale version, duplicate/conflicting key, review before submit, old attempt after recount, missing review reason, dispatch before review/zero delta, W3 unavailable. Preserve state on failure.
## 13. Dependencies
Warehouse/Bin F008 and Inventory ATP F009 done; Item/UoM mapping `[ASSUMED contract]` absent; Lot F087 soft ref. StockAdj F082 W3-LITE mock; Stocktake F084 separate and not implemented. Movement append-only.
## 14. UI inventory
Three tabs directly below page-head: จัดชั้น ABC (score/share/policy drawer), แผนนับและงานนับ (list/create/blank counter drawer), ตรวจทานและประวัติ (comparison/recount/accept/mock/history). Canonical toolbar, top-right actions, no hint/banner. DEMO persona switch marked data-demo+badge and omitted production.
## 15. OQ/default owners
OQ-ABC-01 value default source W4 §3; weighted optional, 90-day window/cumulative-before/ties/zero class C/month-end `[ASSUMED]` Warehouse Product Owner. OQ-ST-02 blind detail `[ASSUMED]` Warehouse Product Owner. Item/UoM snapshot `[ASSUMED]` Inventory/Item owner. StockAdj payload `[ASSUMED contract]` W3 owner. CSQ event/profile CSQ owner.
## 16. Security
Counter expected/value/variance redacted server-side; reviewer permission only after submission, tenant+warehouse scope, immutable attempts/events, version/idempotency. Actor refs Restricted PII, value/expected Confidential. Demo switch cannot authorize API. No actual W3 token in HTML.
## 17. Measures and risk
Class/cadence fixture accuracy100%; blind leaks0; unauthorized submit0; duplicate mock0; stock mutation0; trace completeness100%. Baselines unknown `[ASSUMED]`. Browser render, keyboard/Thai layout and actual server security/integration NOT-CHECKED; development must test.
## 18. AI gate/handoff
C01–C23 evidence in `_lane/BRD_GATE_C01_C23.md`; AI approval is document quality only. Developer starts FRD and CTX; no human handoff wait. No actual downstream claim.
