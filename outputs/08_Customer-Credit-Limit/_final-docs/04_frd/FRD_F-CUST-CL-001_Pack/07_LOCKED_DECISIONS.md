# 07_LOCKED_DECISIONS — F-CUST-CL-001

## 7.0 Inherited scope locks
LOCK-CL-01 through LOCK-CL-05 from BRD §3.4 are immutable for this pack.

## 7.1 Technical decisions
| ID | Decision | Rationale |
|---|---|---|
| LD-01 | Snapshot approval chain at submit | preserves audit and protects pending request from policy edits |
| LD-02 | No direct credit limit API | prevents bypass of DOA |
| LD-03 | Outstanding is external read model | Sales/AR features do not exist in this delivery scope |
| LD-04 | `draft` shown as `รอส่งอนุมัติ` | PM/BA-approved lifecycle clarity |
| LD-05 | Timeline segment ends between dots | preserves visible per-step status indicator |
