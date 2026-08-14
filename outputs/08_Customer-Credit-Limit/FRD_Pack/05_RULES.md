# 05_RULES — F-CUST-CL-001

## 5.1 Core rules
BR-01..BR-13 are implemented exactly as BRD §9. The authoritative plain-language source is the BRD; this file provides executable constraints.

## 5.2 Approval (DOA)
- **BR-DOA-01:** only `draft` can submit.
- **BR-DOA-02:** resolve chain at submit and freeze `approval_chain`; later DOA changes do not change this request.
- **BR-DOA-03:** reject requires reason, ends request, retains current limit and audit.
- **BR-DOA-04:** requester cannot approve own request; server checks My Profile identity and current resolved role.
- **BR-DOA-05:** a changed requested amount requires a new draft/re-resolve.
- Feature never contains approval tier logic or display-name authority. See `DOA_BRIEF_F-CL-001.md`.

## 5.3 Validation and error catalog
| Error | Condition | UI outcome |
|---|---|---|
| REQUEST_AMOUNT_UNCHANGED | requested equals current | submit disabled |
| REASON_REQUIRED | required action has no reason | confirm/submit disabled |
| DOA_NO_AMOUNT_TIER | no DOA result | block submission, explain DOA setup needed |
| REQUEST_NOT_DRAFT | submit non-draft | reject request |
| SELF_APPROVAL_FORBIDDEN | requester signs own request | deny action |
| APPROVAL_STEP_MISMATCH | signer is not current step | deny action |
| PROFILE_ALREADY_EXISTS | duplicate customer event | idempotent success |

## 5.4 State rules
No direct update of `credit_limit`; only `approved` transition applies it. Hold does not cancel a pending credit change. Audit is append-only for submit, approve, reject, hold, unhold, and review.

## 5.5 Derived credit rules
`used = open_invoice_amount + confirmed_unbilled_so_amount`; `available = credit_limit - used`. Near full is `>= configured threshold`; over is `>100%`; limit 0 means cash.

## 5.6 Edge cases
EC-01..EC-08 from BRD §10 apply. Concurrency default `[AI-DEFAULT]`: request version mismatch returns conflict and reloads latest state. Submit has required idempotency key `[AI-DEFAULT]`.

## 5.7 D-CLASS
Credit limits, outstanding balances, reasons, signer identity, and audit are Confidential. Mask or deny details where the authenticated role lacks credit permission; log access to audit export.
