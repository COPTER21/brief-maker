# 03_LOGIC — F-SALES-PROMO Promotion

## §3.1 Scope-Local Functions

### F-SALES-PROMO-FN-01 `validatePromotionDraft`

- Purpose: validate shared fields plus exact rule variant
- Input: draft payload + master snapshots + existing promotions
- Output: normalized draft or `ValidationError[]`
- Invoked by: API-02, API-03
- Calls: FN-03 for overlap preview; no HTTP terms

### F-SALES-PROMO-FN-02 `savePromotionDraft`

- Purpose: create/update header and rule graph atomically
- Input: validated draft, actor, expectedVersion
- Output: promotion id/code/version
- Invoked by: API-02, API-03
- Side effects: INSERT/UPDATE T_promotion/rules/items; audit via FN-09

### F-SALES-PROMO-FN-03 `findPromotionOverlaps`

- Purpose: find same-type/date/scope/target intersections without changing existing records
- Input: candidate promotion + comparable active/scheduled/pending/paused records
- Output: conflict list `{id,code,priority,exclusive}`
- Invoked by: API-04 and UI preview data

### F-SALES-PROMO-FN-04 `submitPromotionForApproval`

- Purpose: revalidate, resolve DOA no-amount matrix, validate assignees, freeze chain
- Input: promotion, DOA entry/version, selected employees, overlap ack, submitter
- Output: pending record + frozen steps
- Invoked by: API-04
- Side effects: header/approval steps/audit; enqueue DOA pending hook

### F-SALES-PROMO-FN-05 `decidePromotionApproval`

- Purpose: enforce current step/SoD, record decision, advance or return draft/activate
- Input: promotion, actor, approve|reject, note/reason, clock
- Output: updated approval/lifecycle state
- Invoked by: API-05, API-06
- Side effects: approval step, approval history, audit, DOA result hook

### F-SALES-PROMO-FN-06 `copyPromotionToDraft`

- Purpose: copy rule/scope to new draft, clear coupon/approval/usage, set start date today
- Invoked by: API-07
- Output: new draft

### F-SALES-PROMO-FN-07 `transitionPromotionLifecycle`

- Purpose: enforce cancel/pause/resume/end-early transition and reason/effective date
- Invoked by: API-08..11
- Output: new state/version

### F-SALES-PROMO-FN-08 `applyPromotionUsageEvent`

- Purpose: idempotently increment uses, amount, unique customers and per-customer count
- Invoked by: API-14
- Output: applied/prior result, exhaustion state
- Side effects: T_promotion_usage, T_promotion aggregate, audit

### F-SALES-PROMO-FN-09 `appendPromotionAudit`

- Purpose: standardized append-only audit
- Invoked by: every mutation function
- Output: audit id; failure rolls back business mutation

### F-SALES-PROMO-FN-10 `buildPromotionListQuery`

- Purpose: tenant-safe query for search/filter/status/sort/export
- Invoked by: API-01/API-15
- Output: parameterized query specification

### F-SALES-PROMO-FN-11 `buildPromotionDetail`

- Purpose: compose detail tabs from header/rule/usage/approval/audit
- Invoked by: API-12
- Output: detail read model

### F-SALES-PROMO-FN-12 `loadEligiblePromotionInputs`

- Purpose: load candidate promotions and verified master/usage snapshots for engine
- Invoked by: API-13
- Output: normalized engine input
- Calls: F-SALES-PROMO-ENG-01

## §3.2 Engine Candidate

### F-SALES-PROMO-ENG-01 `promo-engine` (DRAFT / NEW)

| Field | Value |
|---|---|
| category | financial-calculation / rule-applier |
| version | 1.0.0 |
| owner | F-SALES-PROMO pending Architect registration |
| stateless | true |
| pure | true; no DB/HTTP/clock lookup inside |

**Input:** `{ promotions[], document, lines[] }` where prices and `promo_allowed` already reflect Price List + TA.

**Output:** `{ applied[], line_disc, order_disc, free_items[], skipped[], trace }`.

**Algorithm:**

1. Normalize coupon uppercase and sort promotions by priority asc, valid_from desc, stable id.
2. For each promotion, test lifecycle/date/scope/coupon/quota/budget/stackTA eligibility.
3. Evaluate exactly one type:
   - LINE_DISC per eligible line/base-UOM quantity
   - FREE_GOODS using aggregate buy quantity and repeat policy
   - THRESHOLD against subtotal after prior line promotion discounts, highest reached tier
   - BUNDLE by minimum complete-set count and repeat policy
4. Cap line/order discount so net never becomes negative; use decimal-safe rounding.
5. If no effect, add skipped reason. If effect, add GL/source trace and free item rows.
6. If applied promotion is exclusive, mark remaining candidates skipped and stop.
7. Return deterministic result without checking stock or updating usage.

**Errors:** `ENG_ERR_INVALID_INPUT`, `ENG_ERR_INVALID_RULE`, `ENG_ERR_DECIMAL_OVERFLOW`.

## §3.3 API ↔ Logic Trace

| API | Functions | Engine |
|---|---|---|
| API-01 | FN-10 | — |
| API-02 | FN-01,FN-02,FN-09 | — |
| API-03 | FN-01,FN-02,FN-09 | — |
| API-04 | FN-03,FN-04,FN-09 | — |
| API-05/06 | FN-05,FN-09 | — |
| API-07 | FN-06,FN-09 | — |
| API-08..11 | FN-07,FN-09 | — |
| API-12 | FN-11 | — |
| API-13 | FN-12 | ENG-01 |
| API-14 | FN-08,FN-09 | — |
| API-15 | FN-10 | — |

No mutation API is orphaned; every declared function has a caller.

## §3.4 Integration and Transaction Boundaries

- draft save: header+rule+items+audit one transaction
- submit: lock promotion row, resolve DOA, insert frozen steps, update state, audit one transaction
- approve/reject/lifecycle: row lock + current state/assignee recheck inside transaction
- usage: unique event insert + aggregates + possible exhaustion + audit one transaction
- evaluate: read-only snapshot; no side effects; consumer freezes result in its own document transaction
