# 02_API — F-SALES-PROMO Promotion

## §2.0 Common Contract

- Base `/api/v1/promotions`; auth required; `X-Tenant-Id` required
- Mutations require `Idempotency-Key`; updates require `If-Match`
- Pagination: `cursor`, `limit` max 100; filters: `q,status,type,scope,sort`
- Errors use catalog in `05_RULES.md`; API contains transport/schema only

## §2.1 Endpoint Inventory

| ID | Method/Path | Roles | Purpose | Logic calls | DB |
|---|---|---|---|---|---|
| API-01 | GET `/api/v1/promotions` | view | list/filter/sort | FN-10 | T_promotion |
| API-02 | POST `/api/v1/promotions` | create | create draft | FN-01,FN-02,FN-09 | header/rules/audit |
| API-03 | PATCH `/api/v1/promotions/:id` | edit | update draft | FN-01,FN-02,FN-09 | header/rules/audit |
| API-04 | POST `/api/v1/promotions/:id/submit` | submit | submit approval | FN-03,FN-04,FN-09 | approval/audit |
| API-05 | POST `/api/v1/promotions/:id/approve` | approve | approve current step | FN-05,FN-09 | approval/header/audit |
| API-06 | POST `/api/v1/promotions/:id/reject` | approve | reject current step | FN-05,FN-09 | approval/header/audit |
| API-07 | POST `/api/v1/promotions/:id/copy` | create | copy to draft | FN-06,FN-09 | header/rules/audit |
| API-08 | POST `/api/v1/promotions/:id/cancel` | cancel | cancel before effect | FN-07,FN-09 | header/audit |
| API-09 | POST `/api/v1/promotions/:id/pause` | manage | pause | FN-07,FN-09 | header/audit |
| API-10 | POST `/api/v1/promotions/:id/resume` | manage | resume | FN-07,FN-09 | header/audit |
| API-11 | POST `/api/v1/promotions/:id/end-early` | manage | irreversible early end | FN-07,FN-09 | header/audit |
| API-12 | GET `/api/v1/promotions/:id` | view | detail/tabs | FN-11 | all read models |
| API-13 | POST `/api/v1/promotions/evaluate` | simulate/integration | calc result | FN-12,ENG-01 | read only + trace |
| API-14 | POST `/api/v1/promotions/usage-events` | invoice service | apply usage event | FN-08,FN-09 | usage/header/audit |
| API-15 | GET `/api/v1/promotions/export` | export | CSV current filter | FN-10 | T_promotion |

## §2.2 Mutation Payloads

### API-02 / API-03 Create or update draft

```json
{
  "name": "string",
  "description": "string|null",
  "promotion_type": "LINE_DISC|FREE_GOODS|THRESHOLD|BUNDLE",
  "scope": {"type":"all|group|channel","refs":["code"]},
  "valid_from": "YYYY-MM-DD",
  "valid_until": "YYYY-MM-DD|null",
  "coupon_code": "string|null",
  "priority": 10,
  "exclusive": false,
  "stack_ta": true,
  "limit_total": 0,
  "limit_per_customer": 0,
  "budget_amount": 0,
  "gl_account_ref": "string",
  "owner_ref": "employee-id",
  "rule": {"type":"same-as-promotion_type"}
}
```

Response 201/200 returns `{id, code, status:"draft", version}`. 409 for stale ETag/duplicate idempotency; 422 for business validation.

### API-04 Submit

```json
{
  "doa_entry_ref": "DOA-SALES-PROMO",
  "assignees": [{"step_no":1,"role_id":"role-*","employee_id":"uuid"}],
  "overlap_ack": {"accepted":true,"conflict_codes":["PM-..."]}
}
```

Precondition draft. Response returns frozen `approval_chain`, `current_step`, `status=pending_approval`. Candidate/role/step validity comes from DOA adapter, never request trust.

### API-05 / API-06 Decide

Body `{ "note":"string|null" }` for approve; `{ "reason":"required string" }` for reject. Precondition caller = current assignee and caller ≠ submitter.

### API-08..11 Lifecycle

- cancel/pause: `{reason}`
- resume: `{}`
- end-early: `{reason,effective_date}`
- enforce state matrix in 05_RULES; response returns current state/version

### API-13 Evaluate

```json
{
  "document": {"customer_id":"id","customer_group":"code","channel":"code|null","date":"YYYY-MM-DD","coupon":"string|null"},
  "lines": [{"line_ref":"1","product":"code","uom":"code","qty":10,"unit":100,"promo_allowed":true}]
}
```

Response:

```json
{
  "applied": [{"promotion_id":"id","code":"PM-...","amount":100,"gl_account":"code","note":"string","free_items":[]}],
  "line_disc": {"1":100},
  "order_disc": 0,
  "free_items": [{"product":"code","uom":"code","qty":1,"unit":0,"source_promotion":"id"}],
  "skipped": [{"promotion_id":"id","reason_code":"COUPON_REQUIRED","reason":"visible text"}],
  "trace_id":"uuid"
}
```

### API-14 Usage event

```json
{
  "event_id":"invoice-id:promotion-id:occurrence",
  "invoice_id":"uuid",
  "customer_id":"uuid",
  "promotion_id":"uuid",
  "occurrences":1,
  "discount_amount":100,
  "free_goods_cost":0,
  "gl_account":"code",
  "posted_at":"ISO-8601"
}
```

Duplicate `event_id` returns 200 with prior result and does not increment usage.

## §2.3 Error Responses

| HTTP | Code | Condition |
|---:|---|---|
| 400 | ERR_VALIDATION_FAILED | malformed/simple schema |
| 401 | ERR_UNAUTHENTICATED | missing/expired auth |
| 403 | ERR_FORBIDDEN / ERR_SOD_VIOLATION | role/current assignee/submitter conflict |
| 404 | ERR_PROMOTION_NOT_FOUND | id absent in tenant |
| 409 | ERR_VERSION_CONFLICT / ERR_DUPLICATE_COUPON | concurrency/unique conflict |
| 422 | BR_PROMO_* | business/state/rule failure |

## §2.4 Cross-Module Contracts

| Consumer/provider | Contract | Failure behavior |
|---|---|---|
| price-resolver + TA → API-13 | unit and promo_allowed already resolved | reject incomplete lines; do not guess price |
| QT/SO → API-13 | evaluate after pricing/TA, then snapshot result | timeout: show retry; no partial silent apply |
| Invoice → API-14 | idempotent event after posting | queue retry; reconciliation alert |
| Inventory | consumes free_items from frozen SO result | ATP shortage handled by SO, not API-13 |
| DOA | resolve entry/candidates at submit | block submit if unavailable; no hardcoded chain |

## §2.5 Event Notes

- DOA pending/result events originate from DOA integration; Promotion must not duplicate them
- Business notification declaration is intentionally out of current artifact scope
- Audit event is synchronous with committed mutation; notification is asynchronous and non-blocking
