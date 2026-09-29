# 00_OVERVIEW — F-WH-LOT Lot/Serial + Expiry

## §0.1 Document control
FRD v1 · 2026-09-14 · STANDARD · derived from BRD_F-WH-LOT APPROVED and frozen HTML F-WH-LOT. Business specification only; browser rendering is NOT-CHECKED in S3c.

## §0.2 Revision history
v1 first issue. Any post-S3 HTML edit requires S3a–c and html-to-frd-sync before reissuing this pack.

## §0.3 Scope
In: item tracking policy, lot/serial identity, FEFO recommendation, selected-lot trace, append-only audit, NC/CSQ hooks. Out: GRN/Transfer posting, reservation, stock/valuation mutation, NC delivery, QHold release. All external transaction refs are mock/TODO.

## §0.4 Roles and COSO
Operator creates identity if authorized; config owner changes policy; auditor reads trace. Server checks tenant and User Access/ENC on every API. No production persona switcher. No DOA for this csq-only feature.

## §0.5 Dependencies
Item/Warehouse existing master soft pickers; W3-LITE GRN/Transfer movement and QHold quantities [ASSUMED contract] mocks. Picking consumes recommendation read result; NC consumes expiry event via central rules. Engine registration itself is outside scope.

## §0.6 Architecture
UI hash routes call HTTP API; scope-local functions own mutation; rankEligibleLots is pure local domain function; no new CUBIC engine registered. Movement source and QHold availability remain read-only adapters. Event/audit append-only.

## §0.7 Multi-tenant/security
All records and uniqueness indices are tenant scoped. Master snapshots are soft refs (LD-4C-02). Actor identifiers are internal; expose only to authorized audit readers. OQ defaults and mock boundaries never bypass server guard.

### §0.7.1 Data classification summary
Highest classification Confidential because audit before/after JSON and idempotency keys may contain policy details; inventory identifiers and actor IDs are Internal. If central User Access classifies actor ID as Restricted, register it in Restricted Resources before production; [ASSUMED] owner Security Product Owner. No consumer PII payload is emitted.

## §0.8 OQ and ASSUMED owners
OQ-LOT-01 FEFO only expiry-enabled; non-expiry pick sequence receivedAt ASC (not Avg valuation). [ASSUMED] tie-break receipt/lot, serial qty=1, availability snapshot interpretation and policy effective date: Warehouse Product Owner before release. [ASSUMED contract] W3-LITE movement/held payload: W3-LITE owner before integration. NC chip divergence: registry owner before CSQ/NTF deployment.

## §0.9 Glossary
FEFO = earliest expiry first; FIFO pick sequence = earliest receipt first; ATP = available to promise, excludes hold; soft reference = snapshot/key without hard FK.

## §0.10 Navigation
01_UI layout, 02_API contracts, 03_LOGIC functions, 04_DB storage/classification, 05_RULES invariants, 06_TESTS acceptance, 07_LOCKED scope/defaults, 08_COVERAGE manifest.

## §0.11 Scope lock
LOCK-W4-LOT inherited from BRD §3.4 and RIF §16.3: console/master only; cross-lane refs mock/TODO; no transaction/stock mutation or Pattern Q. Internal lock, no customer sign-off claim.

## §0.12 Coverage Manifest
| BRD ID | Requirement | 01_UI | 02_API | 03_LOGIC | 05_RULES | 06_TESTS |
|---|---|---|---|---|---|---|
| S-01 | Per-item policy isolation | P-03 | API-03 | FN-03 | BR-01 | AT-01 |
| S-02 | Expiry-enabled create rejection | P-04 | API-02 | FN-02 | BR-02 | AT-02 |
| S-03 | Non-expiry null date create | P-04 | API-02 | FN-02 | BR-03 | AT-03 |
| S-04 | Same-item duplicate serial | P-04 | API-02 | FN-02 | BR-04 | AT-04 |
| S-05 | FEFO candidate order/exclusion | P-03 | API-04 | FN-04 | BR-05 | AT-05 |
| S-06 | Non-expiry receipt order | P-03 | API-04 | FN-04 | BR-06 | AT-06 |
| S-07 | Selected-lot trace | P-02 | API-05 | FN-05 | BR-07 | AT-07 |
| S-08 | Browse list | P-01 | API-01 | FN-01 | BR-08 | AT-08 |
| S-09 | NC soft hook | P-03 | API-X2 | FN-06 | BR-09 | AT-09 |
| S-10 | Retry save | P-04 | API-02 | FN-02 | BR-09 | AT-10 |
| BR-01 | Tracking none/lot/serial per item; expiry requires active tracking | P-01..04 | API-01..05 | §3.1 | BR-01 | AT-01 |
| BR-02 | Expiry required iff selected item policy enables it | P-01..04 | API-01..05 | §3.1 | BR-02 | AT-02,AT-03 |
| BR-03 | Serial unique tenant+item; serial qty=1 [ASSUMED] | P-01..04 | API-01..05 | §3.1 | BR-03 | AT-04 |
| BR-04 | Eligible=max(0,on_hand-held)>0 and unexpired if expiry enabled [ASSUMED] | P-01..04 | API-01..05 | §3.1 | BR-04 | AT-05 |
| BR-05 | Expiry item FEFO; non-expiry received_at ASC; stable tie-break [ASSUMED] | P-01..04 | API-01..05 | §3.1 | BR-05 | AT-05,AT-06 |
| BR-06 | Recommendation cannot reserve or mutate stock | P-01..04 | API-01..05 | §3.1 | BR-06 | AT-05,AT-06 |
| BR-07 | GRN/Transfer refs read-only mock until W3-LITE | P-01..04 | API-01..05 | §3.1 | BR-07 | XT-01 |
| BR-08 | Config/identity audit and movement ledger append-only | P-01..04 | API-01..05 | §3.1 | BR-08 | AT-01,AT-07 |
| BR-09 | Near-expiry threshold and delivery owned by NC rules | P-01..04 | API-01..05 | §3.1 | BR-09 | XT-02 |
| EC-01 | zero/held/expired | P-03 | API-04 | FN-04 | BR-04 | AT-05 |
| EC-02 | missing movement source | P-02 | API-05 | FN-05 | BR-07 | AT-07,XT-01 |
| EC-03 | concurrent duplicate serial | P-04 | API-02 | FN-02 | BR-03 | AT-04 |

