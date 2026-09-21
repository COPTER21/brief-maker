# 02_API — F084 Stocktake

> Base `/api/v1/stocktake-rounds`; ทุก endpoint require auth, tenant context, role re-check และ audit ตามชนิด action

## §2.1 Overview

| ID | Method/Path | Purpose | Calls |
|---|---|---|---|
| F084-API-01 | GET `/api/v1/stocktake-rounds` | list/filter | FN-01 |
| F084-API-02 | POST `/api/v1/stocktake-rounds` | create draft | FN-02 |
| F084-API-03 | POST `/:id/freeze` | atomic lock+snapshot | FN-03,FN-04 |
| F084-API-04 | POST `/:id/assign` | assign count/recount | FN-05 |
| F084-API-05 | POST `/:id/count-submissions` | submit current count | FN-06,FN-07 |
| F084-API-06 | GET `/:id/variance` | supervisor variance view | FN-08,ENG-01 |
| F084-API-07 | POST `/:id/submit-approval` | resolve/freeze DOA | FN-09 |
| F084-API-08 | POST `/:id/approval-decisions` | approve/reject step | FN-10 |
| F084-API-09 | POST `/:id/adjustment-draft` | F082 handoff once | FN-11,ENG-02 |
| F084-API-10 | GET `/:id/audit-events` | timeline | FN-12 |

## §2.2 Contracts

### F084-API-02 Create

Body `{name, scope:{warehouse_id, zone_id?, location_id?}}`. Required `Idempotency-Key`. 201 `{id,status:"draft"}`. Errors: 400 `ERR_REQUIRED_FIELD`, 403 `ERR_INSUFFICIENT_ROLE`, 409 `ERR_IDEMPOTENCY_CONFLICT`

### F084-API-03 Freeze

Precondition status=draft, supervisor, snapshot absent. Body `{expected_version}`. In one DB transaction: acquire canonical scope lock, reject overlap, read inventory watermark/on-hand/cost, append snapshot+event, status=frozen. 200 `{status,freeze_at,snapshot_count,lock_ref}`. Errors: 409 `ERR_SCOPE_OVERLAP|ERR_STALE_DATA`, 422 `ERR_SCOPE_EMPTY`

### F084-API-04 Assign

Body `{count_round:1|2, person_id}`. Round1 requires frozen; round2 requires recount. Round2 person cannot equal first assignee. 200 `{status,assignee}`. Errors: 403 role, 409 stale, 422 `BR_RECOUNT_SAME_PERSON`

### F084-API-05 Count submission

Body `{count_round, lines:[{item_id,counted_qty,evidence?}], expected_version}`. Actor must equal active assignee; all lines required; quantity >=0. Append submission/lines. If first count has any `abs(diff)>threshold_version` → recount; else review. Second complete count → review. Errors: 403 `ERR_NOT_ASSIGNED_COUNTER`, 409 stale/idempotency, 422 `BR_COUNT_INCOMPLETE|BR_COUNT_NEGATIVE`

### F084-API-06 Variance

Supervisor/policy only. Response includes snapshot, count1, count2, final diff, unit cost snapshot, value diff, `absolute_variance_value`, threshold/effective date. Counter request → 403 and no sensitive projection

### F084-API-07 Submit approval

Body `{selected_people:[{slot_no,person_id}], expected_version}`. Precondition review. Calls DOA resolve with action+absolute value, validates every resolved slot has one unique person who is not either counter, stores immutable chain snapshot, status=pending. Errors: 422 `BR_APPROVAL_SLOT_MISSING|BR_APPROVER_IS_COUNTER|BR_APPROVER_DUPLICATE|BR_DOA_NO_TIER`

### F084-API-08 Approval decision

Body `{decision:"approved"|"rejected", reason?, expected_version}`. Actor must match current pending step and must not be counter. Reject requires reason. First concurrent commit wins. Approve last step → round approved; reject → rejected and release lock. Errors: 403 `ERR_NOT_CURRENT_APPROVER`, 409 `ERR_STALE_DATA`, 422 `BR_REJECT_REASON_REQUIRED`

### F084-API-09 Adjustment draft

Precondition approved, supervisor, no prior handoff. Sends F082 payload and persists ack atomically/idempotently. Ack draft → status closed and release lock. Failure leaves status approved and lock active. 200 `{adj_id,status:"draft",round_status:"closed"}`. Errors: 409 `ERR_HANDOFF_ALREADY_EXISTS`, 502 `ERR_F082_UNAVAILABLE`

## §2.3 Common Safety

- Mutation: `Idempotency-Key` required, same key+same body returns original result 24h; different body 409
- State mutation: `If-Match`/expected_version required
- Counter GET/response uses a blind DTO excluding system qty, cost, variance and threshold result
- Audit stores Who/What/When/Where/Result; logs do not expose count values to unauthorized viewers

## §2.X Cross-Module Contract

| Target | Contract | Trigger | Payload |
|---|---|---|---|
| Inventory engine | acquire/release `STOCKTAKE_LOCKS` | freeze/rejected/closed | scope canonical key, round_id, from |
| DOA F019 | resolve `approve_variance` | submit approval | feature/action, absolute_variance_value, effective_at |
| F082 | create adjustment draft | approved handoff | `{ref_count_doc,scope,freezeAt,approvedBy,lines[{item,system_qty,counted_qty,diff,cost}]}` |

F082 ack `{adjId,status:"draft"}`; Stocktake never posts movement. Barcode F089 is UI hook only in this release
