# 00_OVERVIEW · FRD F-WH-ROP

**Version:** 1.0 · **2026-09-14** · **Variant:** STANDARD+ (three routes, versioned policy, derived suggestion, two mock adapters; 9 files for full trace) · **Status:** AI-specified, not production-approved. Source: APPROVED AI BRD §1–18, RIF Scope Lock, PREBRIEF S01–13, frozen HTML hash. HTML local proof is 18/18 isolated domain assertions; actual browser rendering, persistence, permission and downstream delivery are NOT-CHECKED.

## Scope and architecture
CUBIC layers: presentation console `#/records`, `#/history`, `#/settings`; thin HTTP API; policy/suggestion functions; policy/event store and upstream Inventory/QHold snapshot. Item/Warehouse are soft refs. ROP min determines PR suggestion; NC rule reference receives candidate facts, and NC owns notification threshold/channel/recipient. No actual PR, notification, stock mutation or movement write. PR W2-PUR-LITE; PO/GRN/RTV W3-LITE and JE W5-FULL remain external mock/TODO as applicable.

## Authority and data classification
BRD §3.4 LOCK-01–06 immutable. Highest data class Confidential for stock/policy and audit refs; user identifiers Restricted when actor audit fields populated; PII flag true only for actor identity, not item/warehouse codes. Production tenant+warehouse access and Maker/Approver separation must be enforced server-side; local demo has none. `[ASSUMED]` formula/approval/freshness defaults and owner list are in 07_LOCKED and BRD §15.

## Build order
Implement DB migrations + expectedVersion, upstream snapshot adapter, pure functions, thin APIs, mock adapters, UI binding, permission/auth, event outbox, contract and UAT. Reject deployment until browser visual/interaction and live contract owners validate their parts. `08_COVERAGE_MANIFEST.md` maps every BRD story/rule/edge and PREBRIEF scenario.

## §0.7.1 Data class summary and open questions
Highest class is Restricted for audit actor identity; actor_ref must be registered/linked to Restricted Resources or masked per Security owner. The central Restricted Resources registry endpoint and policy are unavailable in this lane `[AI-DEFAULT]`; resolve before production. All other policy, stock and mock payload data is Confidential or Internal (see 04_DB §4.2/4.6). No default-to-Public classification.

## §0.11 Scope lock and §0.12 coverage
LOCK-01–06 are copied without override to 07_LOCKED §7.0. `08_COVERAGE_MANIFEST.md` enumerates every US-01–08, BR-01–08, S-01–13 and §10 exception; it is the §0.12 machine-checkable companion. `[AI-DEFAULT]` OQ-ROP-01–07 and owners are in BRD §15 and 07_LOCKED. No human decision is inferred.
