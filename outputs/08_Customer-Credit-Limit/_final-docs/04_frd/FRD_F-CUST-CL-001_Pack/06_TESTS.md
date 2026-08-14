# 06_TESTS — F-CUST-CL-001

| ID | Acceptance test | Expected |
|---|---|---|
| AT-01 | cash customer creates draft then submits | `บันทึกคำขอ` creates `รอส่งอนุมัติ`; `ส่งอนุมัติ` sends only when valid |
| AT-02 | approve all resolved steps | approved limit changes only at final step |
| AT-03 | increase and decrease | both create DOA-governed requests |
| AT-04 | tier resolve | UI shows resolved snapshot; no feature hardcoded chain |
| AT-05 | amount has no tier | submit is blocked fail-closed |
| AT-06 | invalid form | disabled button is visibly disabled |
| AT-07 | reject | reason mandatory; current limit unchanged |
| AT-08 | hold/unhold | reason mandatory and audit appended |
| AT-09 | review | last review timestamp and audit updated |
| AT-10 | audit | six mutation types are append-only |
| AT-11 | utilization | used/available/utilization derives correctly |
| AT-12 | near/over/cash | labels and filters work at threshold / >100 / 0 |
| AT-13 | AR view | outstanding items, aging, DSO render read-only |
| AT-14 | status central | same request state for all viewers; no My Approval view |
| AT-15 | Customer Master event | one idempotent 0-limit profile per customer |
| AT-16 | self approval | server denies requester's own approval |
| AT-17 | DOA snapshot | DOA reconfiguration does not change submitted chain |
| AT-18 | stale request | version conflict does not overwrite later action |
| AT-19 | Esc | modal → change drawer → detail drawer → close |
| AT-20 | search | sequential input preserves focus/caret |

## 6.9 Cross-module tests
| ID | Contract test | Expected |
|---|---|---|
| XT-01 | Customer Master customer_created | creates one cash profile only |
| XT-02 | DOA resolve failure/no tier | no request becomes pending |
| XT-03 | My Profile signer | role/SoD validation occurs server-side |
| XT-04 | SO/AR projection | updated outstanding changes display only; no direct source mutation |
| XT-05 | approved projection to Customer Master/SO | only approved limit/hold is published |
