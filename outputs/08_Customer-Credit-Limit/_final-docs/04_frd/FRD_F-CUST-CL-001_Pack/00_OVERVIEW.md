# 00_OVERVIEW — F-CUST-CL-001 Customer Credit Limit

## 0.1 Control
| Item | Value |
|---|---|
| Variant | FULL — 4 UI surfaces, approval workflow, money and cross-module contracts |
| Source | BRD v1.0 APPROVED + `01_HTML/f-credit-limit.html` |
| Status | Ready for implementation subject to OQs / external wires |

## 0.2 Scope
Own and govern customer credit limits; request changes, DOA approval, credit hold/review, read-only utilization and audit. Customer Master, Sales Order, AR Invoice, My Profile, and DOA remain separately owned systems.

## 0.3 Roles
Credit Officer/Sales Admin: request, hold/unhold, review. DOA Approver: sign/reject current step only. System: resolve/freeze chain, apply approved limit, append audit.

## 0.7.1 Data classification
Highest: **Confidential**. Customer commercial terms, credit limit, outstanding amount, approver identity, and audit are confidential. No Restricted field is designed here; identity is referenced from My Profile.

## 0.8 Dependencies
Customer Master create/projection; Policy Center DOA resolve; My Profile signer; Sales Order + AR Invoice read model and credit enforcement. Until wired, prototype values are mock only.

## 0.10 Open Questions
- OQ-CL-01: resolve by absolute requested limit or delta.
- OQ-CL-02: direct-set band exists or not.
- OQ-CL-03: confirm real `role-*` ids and matrix in DOA.
- OQ-CL-04: whether hold/unhold requires DOA.
- OQ-CL-05: risk calculation and 85% threshold confirmation.
- OQ-CL-06: event/API contract ownership and delivery dates for Customer Master, SO, AR, My Profile.

## 0.11 Scope lock
LOCK-CL-01..05 imported verbatim from BRD §3.4: this feature owns limit; all changes use DOA; profile/audit are immutable in ownership; no My Approval; external modules are contracts only.

## 0.12 Coverage manifest
| BRD ref | Requirement | FRD location |
|---|---|---|
| §7 S-01/S-02 | request and apply approved limit | 01_UI P-03; 02_API API-03..06; 03_LOGIC FN-02..05; 06_TESTS AT-01..04 |
| §7 S-03 | sequential approval / reject | 01_UI P-02; 05_RULES BR-DOA-01..05; 06_TESTS AT-05..07 |
| §7 S-04 | hold/unhold/review | 02_API API-07..09; 03_LOGIC FN-06..08; 06_TESTS AT-08..10 |
| §7 S-05 | credit/AR display | 01_UI P-01/P-02; API-01/02; 06_TESTS AT-11..13 |
| §7 S-06 | auto profile | API-10; FN-09; 06_TESTS XT-01 |
| §9 BR-01..13 | business rules | 05_RULES BR-01..13 + DOA section |
| §10 EC-01..08 | exception paths | 05_RULES EC-01..08; 06_TESTS AT-14..20 |
