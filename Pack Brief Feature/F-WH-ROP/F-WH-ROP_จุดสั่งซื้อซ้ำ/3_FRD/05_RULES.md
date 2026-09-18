# 05_RULES · F-WH-ROP

| Rule | Enforce | Error / exception | BRD and UI/logic |
|---|---|---|---|
| R-01 exact pair and effective version | server FN-03; UI shows scoped list | NO_POLICY explicit `ยังไม่มีนโยบาย`; future version inactive | BR-01 / ropPolicyActive |
| R-02 configurable min/max/safety/date | server policy version and `expectedVersion` | VERSION_CONFLICT, BAD_REFERENCE | BR-02 / ropSavePolicy |
| R-03 bounds and valid input | FN-01 + UI guard | REQUIRED, POLICY_BOUNDS, BAD_EFFECTIVE_DATE; no event | BR-03 / ropValidate |
| R-04 min boundary and qty formula | FN-05; UI result | equal triggers, above produces qty0; no PR for qty0 | BR-04 / ropEvaluatePair |
| R-05 held handling | FN-04/05 | SNAPSHOT_UNAVAILABLE/STALE; held>onHand data-quality flag | BR-05 / ropSnapshot |
| R-06 NC ownership | FN-07 | NC_RULE_MISSING; candidate does not assert delivery | BR-06 / ropNcCandidate |
| R-07 PR soft-link | FN-06 | NO_POSITIVE_SUGGESTION, MOCK_UNAVAILABLE retryable | BR-07 / ropPreparePR |
| R-08 append-only/idempotency | DB+FN-02/06/07/08 | same key+body same ack; different body IDEMPOTENCY_CONFLICT | BR-08 / ropEvents |

Policy validation uses finite decimals, valid calendar date, scoped master refs and ordered values. Current HTML `ropSaveFromDrawer` rejects blank fields before Number conversion; `ropValidate` rejects nonfinite and malformed calendar dates. Production server must still enforce independently. NC candidate can be above ROP min, because external NC threshold is independent; do not treat candidate as actual notification. No stock/movement write permission exists in ROP service.

## Error matrix and control
`ACCESS_DENIED`→hide data and audit denied attempt; `BAD_REFERENCE`→reject unknown pair; `NO_POLICY`→show empty state; `SNAPSHOT_UNAVAILABLE/STALE`→no positive suggestion; `POLICY_BOUNDS/BAD_EFFECTIVE_DATE/REQUIRED`→field error; `VERSION_CONFLICT`→reload and re-review; `MOCK_UNAVAILABLE`→retry safely; `IDEMPOTENCY_CONFLICT`→reject divergent replay. Never report success when mock adapter is unavailable. D-CLASS: Confidential stock/policy scoped by tenant/warehouse; Restricted actor field filtered from non-auditors. Rule values marked `[ASSUMED]` retain BRD §15 owners.

## CSQ 7C and NTF declaration rules
BR-CSQ-01: only a successful policy version commit may later emit the declared `master.changed` candidate to the central CSQ engine; no feature-local 7C calculation or tube stamp. BR-CSQ-02: producer envelope carries unique (feature,ref,action) idempotency and correlation. BR-CSQ-03: mask Restricted actor fields; current declaration payload avoids raw actor name. BR-CSQ-04: reversal is a new version/event with `reversal_of`, not delete. BR-CSQ-05: do not declare OC or document-level DC from this feature, and SC is reserved. Current master-policy DC classification is provisional and requires CSQ owner confirmation; `CSQ_BRIEF_F-WH-ROP.md` is not registered. NTF/NC owns all alert thresholds, recipients and channels; ROP only prepares candidate envelope with ruleRef. No DOA auto-events are redeclared. No external engine execution is a local acceptance claim.

## §5.7 D-CLASS enforcement
Policy and stock values are Confidential and server-side tenant/warehouse filtered; actor refs Restricted/PII and masked to non-auditors. No raw actor or NC recipient in CSQ/NTF envelopes. The classification metadata is enforced at DB grant, API response, UI field and audit export; overrides belong to Policy Center, not ROP. A classification error is `ACCESS_DENIED` and is audit logged. The local HTML has no actual auth and cannot pass this control test.
