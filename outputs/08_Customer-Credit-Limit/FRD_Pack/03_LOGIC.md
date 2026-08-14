# 03_LOGIC — F-CUST-CL-001

## 3.1 Functions
| ID / Function | Purpose | Invoked by | Side effects |
|---|---|---|---|
| FN-01 `buildCreditProfileQuery` | filter/sort profile list | API-01 | none |
| FN-02 `createCreditChangeDraft` | validate different amount/reason and create draft | API-03 | insert request, audit |
| FN-03 `submitCreditChangeRequest` | resolve DOA, freeze snapshot, transition draft | API-04 | update request, audit |
| FN-04 `approveCreditChangeStep` | verify current signer, advance or apply limit | API-05 | update request/profile, audit, projection |
| FN-05 `rejectCreditChangeRequest` | validate reject reason and finalize rejection | API-06 | update request, audit |
| FN-06 `setCreditHold` | validate reason and change hold state | API-07/API-08 | profile/audit/projection |
| FN-07 `recordCreditReview` | stamp review time | API-09 | profile/audit |
| FN-08 `buildOutstandingView` | compose used/available/utilization | API-02 | none |
| FN-09 `createDefaultCreditProfile` | idempotent customer event handling | API-10 | insert profile/audit |

## 3.2 Engines
### `credit-utilization-engine`
Pure input `{ credit_limit, open_invoice_amount, confirmed_unbilled_so_amount }`; output `{ used_amount, available_amount, utilization_percent, state }`. No HTTP/DB I/O. State uses configured threshold.

### `doa-resolution-adapter`
Integration boundary that calls Policy Center DOA; it returns role-id steps and no display-name chain. It does not own or calculate approval tiers.

## 3.3 API ↔ Logic Trace
| API | Functions | Engines |
|---|---|---|
| API-01 | buildCreditProfileQuery | — |
| API-02 | buildOutstandingView | credit-utilization-engine |
| API-03 | createCreditChangeDraft | — |
| API-04 | submitCreditChangeRequest | doa-resolution-adapter |
| API-05 | approveCreditChangeStep | — |
| API-06 | rejectCreditChangeRequest | — |
| API-07/08 | setCreditHold | — |
| API-09 | recordCreditReview | — |
| API-10 | createDefaultCreditProfile | — |
