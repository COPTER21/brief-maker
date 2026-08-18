# 05_RULES — F-SALES-PROMO Promotion

## §5.1 Calculation Rules

| ID | Rule | Engine behavior |
|---|---|---|
| BR-PROMO-01 | input price is after Price List + TA, pre-VAT | reject missing resolved unit; never lookup/guess |
| BR-PROMO-02 | active/date/scope/coupon/quota/budget/TA eligibility | every skip returns code + visible reason |
| BR-PROMO-03 | LINE_DISC per line/base qty; pct or amount×base qty; cap at line amount; honor promo_allowed | decimal-safe line discount |
| BR-PROMO-04 | FREE_GOODS aggregate buy qty; repeat or once; output zero-price lines | stock not checked here |
| BR-PROMO-05 | THRESHOLD highest reached tier after prior line promo discounts; BUNDLE complete-set min | non-marginal tier, bundle savings ≥0 |
| BR-PROMO-06 | priority asc, valid_from desc tie-break; exclusive stops after applied | deterministic stable order |
| BR-PROMO-09 | zero budget/quota unlimited; do not apply an occurrence that exceeds remaining budget | skip/exhaustion trace |
| BR-PROMO-10 | per-customer usage is promotion occurrences confirmed by Invoice | event-driven, idempotent |
| BR-PROMO-13 | free goods price 0; downstream SO owns ATP; Inventory owns movement | output only |
| BR-PROMO-14 | each applied result contains configured GL ref | downstream Invoice posts |

## §5.2 Authoring Rules

| ID | Rule |
|---|---|
| BR-PROMO-07 | overlap iff same type + intersecting dates + intersecting scope + relevant target intersection; submit requires ack |
| BR-PROMO-08 | overlap never auto-cancels or truncates existing promotion |
| BR-PROMO-11 | only draft editable; approved/pending business terms require copy |
| BR-PROMO-15 | coupon normalized uppercase, regex `^[A-Z0-9_-]{3,20}$`, case-insensitive active uniqueness |
| BR-PROMO-16 | scope customer-id is invalid; customer-specific deal belongs to TA |
| BR-PROMO-17 | all create/update/submit/decision/lifecycle/usage actions append audit |

## §5.3 Lifecycle Matrix

| From | Action | To | Role | Required |
|---|---|---|---|---|
| — | create/copy | draft | create | valid base payload |
| draft | submit | pending_approval | submit | complete, DOA slots, overlap ack if conflict |
| pending_approval | approve non-final | pending_approval | current assignee | SoD/current step |
| pending_approval | approve final | scheduled/active | current assignee | valid_from vs clock |
| pending_approval | reject | draft | current assignee | reason |
| active | pause | paused | manage | reason |
| paused | resume | active | manage | within validity/not exhausted |
| active | exhaust | budget_exhausted | system | usage reaches limit |
| active/scheduled/paused/budget_exhausted | end early | ended_early | manage | reason + effective date |
| draft/pending_approval | cancel | cancelled | cancel | reason |
| scheduled | clock start | active | system | date |
| active | clock end | ended | system | date |

Any omitted transition returns `BR_PROMO_INVALID_TRANSITION`.

## §5.4 Validation Catalog

| ID | Condition | Code |
|---|---|---|
| VR-01 | name/owner/GL/from required; until≥from; from≥authoring date | BR_PROMO_REQUIRED / INVALID_DATE |
| VR-02 | priority integer 1..999 | BR_PROMO_INVALID_PRIORITY |
| VR-03 | group/channel scope refs ≥1; customer scope forbidden | BR_PROMO_INVALID_SCOPE |
| VR-04 | LINE value>0, pct≤100, minQty≥1, target ref required | BR_PROMO_INVALID_LINE_RULE |
| VR-05 | FREE all refs/UOM/qty required and qty≥1 | BR_PROMO_INVALID_FREE_RULE |
| VR-06 | THRESHOLD tiers ≥1, min ascending/unique, value>0, pct≤100 | BR_PROMO_INVALID_TIERS |
| VR-07 | BUNDLE unique products ≥2, qty≥1, 0<price<list total | BR_PROMO_INVALID_BUNDLE |
| VR-08 | coupon format/uniqueness | ERR_DUPLICATE_COUPON / BR_PROMO_INVALID_COUPON |
| VR-09 | submit assignees complete and valid candidates | BR_PROMO_APPROVER_REQUIRED |
| VR-10 | reject/cancel/pause/end reason nonblank | BR_PROMO_REASON_REQUIRED |

## §5.5 Approval (DOA)

| ID | Contract |
|---|---|
| BR-DOA-01 | submit only from draft |
| BR-DOA-02 | resolve central entry at submit and freeze entry/version/steps |
| BR-DOA-03 | reject returns draft; previous round preserved append-only |
| BR-DOA-04 | submitter cannot approve own promotion or appear as selectable assignee |
| BR-DOA-05 | selected employee required for every config slot |
| BR-DOA-06 | sequential; only current assignee may decide |
| BR-DOA-07 | rejection reason required; approval note optional |

Feature has **no amount dimension**. Do not add amount thresholds or hardcode step roles; see `DOA_BRIEF_F-SALES-PROMO.md`.

## §5.6 Edge Cases

### Confirmed

- EC-01 invalid numeric/date/coupon/item/tier/bundle values block persistence/step
- EC-02 overlap ack is required and records confirmer/time/codes
- EC-03 SoD filters picker and blocks API even if UI bypassed
- EC-04 required reason blocks destructive/workflow actions
- EC-05 wrong/missing coupon skips only that promotion
- EC-06 TA no-repeat skips affected line rule
- EC-07 exclusive applied stops remaining candidates
- EC-08 budget/quota/per-customer limit skips and exposes reason
- EC-09 ATP shortage is not evaluated by promo-engine
- EC-10 deactivated master is unavailable to new selection; historical snapshot remains readable
- EC-11 non-draft edit returns business error with copy option
- EC-12 duplicate usage event returns prior result without increment

### Conservative `[AI-DEFAULT]`

- EC-AI-01 stale `If-Match` → 409; no merge/overwrite
- EC-AI-02 duplicate mutation idempotency key → prior result; mismatched body → 409
- EC-AI-03 DOA config changes after submit do not mutate frozen steps
- EC-AI-04 unauthenticated/forbidden → 401/403 + security audit
- EC-AI-05 money uses decimal, currency rounding at output, never negative net

## §5.7 Error Catalog

| Code | HTTP | User-visible outcome |
|---|---:|---|
| ERR_VALIDATION_FAILED | 400 | inline error + “กรุณากรอกข้อมูลให้ครบถ้วน” |
| ERR_FORBIDDEN | 403 | action hidden; API rejects |
| ERR_SOD_VIOLATION | 403 | “ผู้ส่งต้องไม่สามารถอนุมัติรายการของตัวเองได้” concept; no action |
| ERR_VERSION_CONFLICT | 409 | record changed; ask reload |
| ERR_DUPLICATE_COUPON | 409 | coupon already used by non-final promotion |
| BR_PROMO_INVALID_TRANSITION | 422 | action not allowed in current state |
| BR_PROMO_APPROVER_REQUIRED | 422 | “เลือกผู้อนุมัติให้ครบทุกขั้น” |
| BR_PROMO_OVERLAP_ACK_REQUIRED | 422 | “ต้องยืนยันการทับซ้อนก่อนส่ง” |
| BR_PROMO_REASON_REQUIRED | 422 | required reason error |
| ENG_ERR_INVALID_INPUT/RULE | 422 | evaluation skipped/failed with trace |

## §5.8 Permission Matrix

| Permission | Officer | Sales Manager | BU Head | Invoice service |
|---|:---:|:---:|:---:|:---:|
| view/simulate | allow | allow | allow | deny |
| create/edit/submit/copy/export | allow | allow | deny | deny |
| approve/reject | deny unless assigned role policy says; never own | allow if current | allow if current | deny |
| pause/resume/end | deny | allow | deny | deny |
| usage event | deny | deny | deny | allow service credential |

## §5.9 Data Classification (D-CLASS)

- API and DB enforce highest class Confidential
- exports require explicit permission, tenant filter and audit; coupon/employee/customer data minimized
- logs store IDs and error codes, not full request bodies or coupon in plain application logs
- no Restricted field; if future campaign/customer segmentation adds sensitive attributes, reclassify before implementation
