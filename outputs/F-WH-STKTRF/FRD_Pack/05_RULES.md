# 05_RULES — F-WH-STKTRF

## 5.1 Business rules

BR-01..BR-33 are inherited unchanged from BRD §9.1. Server enforcement groups:

- BR-01..08: line uniqueness, single warehouse pair, derived mode, distinct/eligible bins, positive quantity within source balance.
- BR-09..13: number only on submit via DOCCFG, excluded locations, real-person slots, rejection reason and return to draft.
- BR-14..19: warehouse/identity SoD, transit ownership, partial receipt, no over-receipt, evidence-backed shortage approval, reasoned return.
- BR-20..26: final stock recheck, pre-movement cancellation only, draft-only edit, pending JE, append-only ledger, one reversal.
- BR-27..33: central thresholds/configuration, snapshots, Gregorian year, audit/idempotency, no adjustment/count/location-master scope.

## 5.2 Validation catalog

V-01..V-21 and their Thai messages are authoritative from BRD §9.2 and must be returned verbatim where applicable. In addition, disabled action explanations in HTML are presentation of the same server authorization/state result. No client-only validation grants permission.

## 5.3 Confirmed edge cases

E-01..E-21 are mandatory. Implement quantity/balance/location filters, destructive warehouse-change confirmation, missing transit configuration block, quarantine/damage/receiving/transit exclusions, locked-bin reason, final balance recheck, partial/missing/return flows, overdue flags, no cancel after movement, no repeat reversal, snapshots for retired masters, destination permission, shortage SoD, idempotency, and distinct empty states.

## 5.4 Error catalog

| Code | HTTP | Meaning |
|---|---:|---|
| INVALID_STATE | 409 | action not permitted from committed current state |
| VERSION_CONFLICT | 409 | stale browser data; reload |
| DUPLICATE_ACTION | 409 | idempotent prior result exists |
| INSUFFICIENT_STOCK | 422 | current source balance below request |
| RECEIVE_EXCEEDS_REMAINING | 422 | actual receive above committed remaining |
| TRANSIT_NOT_CONFIGURED | 422 | warehouse pair has no transit bin |
| LOCATION_NOT_ELIGIBLE | 422 | location type/lock rule failed |
| APPROVER_REQUIRED | 422 | a DOA slot lacks a real person |
| SOD_VIOLATION | 403 | maker/shipper/receiver/approver conflict |
| EVIDENCE_REQUIRED | 422 | shortage has no attachment |
| FORBIDDEN_WAREHOUSE | 403 | actor outside warehouse scope |

## 5.5 AI-default probes

`[AI-DEFAULT]` PR-1 optimistic concurrency, PR-7 idempotency, atomic ledger transaction and file validation apply until BA confirms otherwise. Failure is fail-closed; retries do not duplicate documents or movements.

## 5.6 Notification/document policy

Document numbering/storage, approval chain, and notification channels are resolved centrally. Feature code declares keys and trigger points only.

## 5.7 D-CLASS

Confidential approval/audit/reason/attachment fields require authenticated, tenant- and warehouse-scoped reads, explicit audit-export permission, logged access, encrypted transport/storage, and retention from central policy.

