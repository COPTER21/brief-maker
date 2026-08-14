# 02_API — F-CUST-CL-001

All paths are versioned REST contracts; server calculates authorization and derives money values.

| ID | Method / path | Purpose | Reads/Writes |
|---|---|---|---|
| API-01 | GET `/api/v1/customer-credit-profiles` | list/search/filter/sort | T_credit_profile |
| API-02 | GET `/api/v1/customer-credit-profiles/{id}` | profile, outstanding, audit, pending request | profile/read projections |
| API-03 | POST `/api/v1/customer-credit-profiles/{id}/change-requests` | create draft | T_credit_change_request, audit |
| API-04 | POST `/api/v1/credit-change-requests/{id}/submit` | resolve/freeze DOA and send | request, approval snapshot, audit |
| API-05 | POST `/api/v1/credit-change-requests/{id}/approve` | sign current step | request, audit; profile on final step |
| API-06 | POST `/api/v1/credit-change-requests/{id}/reject` | reject with reason | request, audit |
| API-07 | POST `/api/v1/customer-credit-profiles/{id}/hold` | set hold | profile, audit |
| API-08 | POST `/api/v1/customer-credit-profiles/{id}/unhold` | remove hold | profile, audit |
| API-09 | POST `/api/v1/customer-credit-profiles/{id}/review` | record review | profile, audit |
| API-10 | POST `/internal/events/customer-created` | idempotent profile creation | profile, audit |

### API-04 Contract
Request: `{ idempotency_key }`. Response: `{ approval_status, doa_entry_ref, approval_chain, current_step }`.
Errors: `REQUEST_NOT_DRAFT`, `DOA_RESOLVE_FAILED`, `DOA_NO_AMOUNT_TIER`, `SELF_APPROVAL_FORBIDDEN`.

### API-05/06 Contract
Approve input has optional comment; reject input requires `reason`. Both verify authenticated My Profile identity against the resolved current role, reject self approval, and use optimistic version / idempotency protection.

## Cross-module contracts
| Contract | Direction | Minimum payload |
|---|---|---|
| Customer created | inbound | customer_id, code, name, group, rep, payment_term |
| DOA resolve | outbound synchronous | feature key, requested amount, requester context |
| Approved projection | outbound | customer_id, approved_limit, hold, effective_at, request_no |
| Outstanding projection | inbound read | customer_id, open_invoice_amount, confirmed_unbilled_so_amount, as_of |
| SO credit check | outbound read/event | customer_id, approved_limit, hold, available_amount |
