# 06_TESTS · F-WH-ROP

**Evidence boundary:** AT-01–18 are executable isolated domain assertions in `_lane/DOMAIN_TEST.json` (18/18); they do not establish UI rendering or API contract. Manual HTML cases in 4_TC validate text/routes when a browser is available. Production API/permission and W3/NC integration cases are specifications pending backend harness and owner signoff, never marked locally passed.

| AT | Stimulus | Expected / route/handler |
|---|---|---|
| AT-01 | 30 configured pairs, ITEM-116 missing | `NO_POLICY` / check drawer, FN-03 |
| AT-02 | 0≤safety≤min≤max | accept equality / drawer, FN-01 |
| AT-03 | inversion/negative | bounds error, no event / drawer, FN-01 |
| AT-04 | nonfinite or invalid date | reject, no event / drawer, FN-01 |
| AT-05 | ITEM-103 WH-01 available10=min10/max30 | qty20 / history, FN-05 |
| AT-06 | ITEM-104 WH-01 available9/min10/max30 | qty21 / history, FN-05 |
| AT-07 | ITEM-101 WH-02 available35>min25 | qty0, PR disabled / history, FN-05 |
| AT-08 | same Item different Warehouse | distinct policy refs / records/history, FN-03 |
| AT-09 | ITEM-101 WH-01 onHand20 held12 | available8, qty22, stock unchanged / history, FN-04/05 |
| AT-10 | future policy saved | current unchanged, future date selects new version / records, FN-02/03 |
| AT-11 | policy save | new version and event append / records/settings, FN-02 |
| AT-12 | positive PR action | mock payload pair/qty/version/key and mockRef only / history, FN-06 |
| AT-13 | same PR key | same ack, one event / history, FN-06 |
| AT-14 | PR mock unavailable | retryable, no new event / history, FN-06 |
| AT-15 | NC candidate above ROP min | envelope ruleRef/available; no delivered claim / history, FN-07 |
| AT-16 | same NC key | replay one event / history, FN-07 |
| AT-17 | after policy/PR/NC actions | stock fixture unchanged / all, BR-05 |
| AT-18 | valid policy list base | 30 configured policies and missing pair, no invented policy / records, FN-03 |

Cross-module contract cases XT-PR-01/02 validate payload/ack/idempotency only; XT-NC-01/02 validate candidate envelope and absence of delivery assertion only; XT-INV-01 validates onHand/held read shape and unchanged upstream state. Do not test actual PR, notification recipient/channel, GRN/PO/RTV or JE. Access-control tests must use backend harness; demo sample user badge is not authorization.

Release DoD: source coverage R1/R2, exact frozen hash, TC case ledger 1:1, no rule/exception dropped, visual browser test before production, contract owner approval for PR/NC, server-side permissions and data-class enforcement.
