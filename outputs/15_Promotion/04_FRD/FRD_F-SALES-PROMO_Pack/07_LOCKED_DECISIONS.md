# 07_LOCKED_DECISIONS — F-SALES-PROMO

## §7.0 Immutable Scope Locks

| ID | Decision | Implementation consequence |
|---|---|---|
| LOCK-PROMO-01 | Approved Promotion.html is AS-BUILT UI source | FRD/UI brief/tests cannot invent routes or controls |
| LOCK-PROMO-02 | No customer-specific promotion | reject scope type customer; refer to Trade Agreement |
| LOCK-PROMO-03 | Item Master source of truth | product/UOM/factor/list from master adapter; snapshot historical values |
| LOCK-PROMO-04 | DOA no amount, sequential, config-driven, SoD | no thresholds/role arrays in feature; freeze resolved chain |
| LOCK-PROMO-05 | ATP belongs to Sales Order | promo-engine never queries stock |
| LOCK-PROMO-06 | Invoice owns usage trigger; count promotion occurrences | idempotent usage event contract |
| LOCK-PROMO-07 | Campaign future | no campaign entity/API/UI in current feature |

## §7.1 Architecture Decisions

| LD | Decision | Reason |
|---|---|---|
| LD-01 | FULL pack | complex lifecycle + approval + monetary engine + integrations |
| LD-02 | single hash route with stateful overlays | fidelity to approved HTML |
| LD-03 | pure `promo-engine` candidate | reusable by QT/SO; deterministic tests |
| LD-04 | evaluate has no side effects | document consumer controls freeze/transaction |
| LD-05 | usage is event-driven/idempotent | Invoice is authoritative occurrence |
| LD-06 | no hard delete | audit/business history |
| LD-07 | optimistic lock + idempotency | conservative concurrency defaults |
| LD-08 | Confidential highest class | customer/employee refs and financial impact |

## §7.2 Deferred / Manual

- Architect registry id for engine
- DOA Admin actual configuration and `wire_status` update
- Document number / notification declarations are not authorized this round
- Campaign integration requires a future scoped change

## §7.3 Prohibited Implementation Shortcuts

- no `const APPROVAL_CHAIN=[...]` or amount-based approval rule
- no querying list price/TA/stock inside promo-engine
- no direct UI→engine or downstream→DB bypass
- no coupon/master display names as contract keys
- no usage increment from simulator, QT or SO; Invoice event only
