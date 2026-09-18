# 00_OVERVIEW — F-WH-STKTRF Stock Transfer

## 0.1 Document control

| Field | Value |
|---|---|
| FRD version | 1.0 |
| Date | 2026-09-17 |
| Status | APPROVED FOR HANDOFF |
| Variant | FULL — 10 surfaces, 11 lifecycle states, approval + inventory movement |
| Sources | `../BRD_F-WH-STKTRF.md` v1.1 + `../F-WH-STKTRF.html` |
| HTML gate | UX/Coverage/E2E passed; PM/BA manual review passed |

## 0.2 Purpose and scope

Create, approve, ship, receive, reconcile, return, cancel, and reverse stock-transfer documents. Same-warehouse transfers move directly between bins; cross-warehouse transfers always pass through the configured in-transit location. Movement history is append-only.

Out of scope: stock adjustment, cycle count, location-master maintenance, real JE posting, hard delete, and hardcoded approval/notification/document-number policy.

## 0.3 Actors

- Source warehouse officer: draft/edit/submit.
- Source warehouse supervisor: ship/direct move/cancel/reverse.
- Destination warehouse officer or supervisor: receive/return.
- DOA assignee: approve/reject the current slot.
- Shortage DOA assignee: approve write-off; must not be the shipper.
- Accounting/audit/admin: read-only audit and monitoring.

## 0.4 Status contract

`draft → pending_approval → approved → moved | in_transit → partial → closed | closed_diff | returned`; pre-movement cancellation ends at `cancelled`; completed movement can end at `reversed` only after its reversal document completes.

## 0.5 Dependencies

| Dependency | Contract |
|---|---|
| Location Master | Warehouse/zone/bin snapshots and eligible-location rules |
| Inventory ledger | Atomic append-only movement posting |
| F-DOCCFG | `ENG-DOC-NUM.next(TRF)` and `ENG-DOC-STORE.store()` |
| DOA | Resolve and execute real-person approval slots; no hardcoded chain |
| ENG-NOTIFY | Business notifications from declared events; DOA events not duplicated |
| Stock Adjustment | User guidance only when physical excess is discovered |
| W5 Accounting | Future JE posting; current state is `pending_posting` |

## 0.6 Security

Preset P2 Approval/Workflow. Enforce warehouse scope, Maker ≠ Approver, shipper ≠ receiver, shipper ≠ shortage approver, server-side transition checks, audit append-only, idempotency, optimistic concurrency, attachment authorization, and sensitive audit access.

## 0.7 Data classification

Highest level: **Confidential** (approval identities, audit actors, attachment metadata, reason/evidence). Item/location/document operational data is Internal. No field defaults to Public.

## 0.8 Assumptions and open questions

- OQ-TRF-01..08 and inherited OQs remain governed by BRD §15; implementation uses the documented interim values.
- `[AI-DEFAULT]` API mutations require `Idempotency-Key` and `If-Match`; stale writes return 409.
- Real JE posting remains disabled until W5 contract is approved.

## 0.9 Cross-module value stream

Location/on-hand → TRF draft → DOA approval → inventory movement → in-transit/receipt → audit/monitoring → future accounting posting. Cancellation before movement posts nothing. Return/reversal appends compensating movement and never edits the original ledger row.

## 0.10 UI source

Four hash routes exist: `#/list`, `#/create[/dup-:id]`, `#/edit/:id`, `#/view/:id`. The remaining six business surfaces are overlays/tabs launched from these routes. HTML is authoritative for visible wording and interaction anatomy.

## 0.11 Scope locks

Imported verbatim in `07_LOCKED_DECISIONS.md` as LK-1..LK-11; all are immutable.

## 0.12 Coverage manifest

| BRD ref | Requirement | FRD evidence |
|---|---|---|
| S-01 | Same-warehouse one-step transfer | 01_UI P-02/P-03; API-07; FN-07; AT-01 |
| S-02 | Cross-warehouse transfer via transit | 01_UI P-02/P-03; API-07/08; FN-07/08; AT-02 |
| S-03 | Ship from source | API-07; FN-07; AT-03 |
| S-04 | Full destination receipt | API-08; FN-08; AT-04 |
| S-05 | Partial receipt | API-08; FN-08; AT-05 |
| S-06 | Shortage write-off approval | API-10/11; FN-10/11; AT-06 |
| S-07 | Return to source | API-09; FN-09; AT-07 |
| S-08 | Cancel and reversal | API-12/13; FN-12/13; AT-08 |
| S-09 | Real-person DOA | API-05/06; FN-05/06; AT-09 |
| S-10 | Transit visibility | 01_UI P-01/P-03; API-01/03; AT-10 |
| BR-01..BR-08 | Line uniqueness, mode, quantity and location eligibility | 05_RULES BR-01..08; VR-01..10; RT-01 |
| BR-09..BR-13 | Numbering, eligibility, real approvers and rejection | 05_RULES BR-09..13; API-05/06; RT-02 |
| BR-14..BR-19 | SoD, transit ownership, receive/shortage/return | 05_RULES BR-14..19; API-08..11; RT-03 |
| BR-20..BR-26 | Recheck, cancel, append-only, reversal | 05_RULES BR-20..26; API-07/12/13; RT-04 |
| BR-27..BR-33 | Central config, snapshots, audit, scope exclusions | 05_RULES BR-27..33; 04_DB; RT-05 |
| V-01..V-10 | Wizard/line validation | 05_RULES §5.2; 06_TESTS VT-01..10 |
| V-11..V-21 | Approval/execution/concurrency validation | 05_RULES §5.2; 06_TESTS VT-11..21 |
| E-01..E-08 | Quantity/bin/location exceptions | 05_RULES §5.3; 06_TESTS EC-01..08 |
| E-09..E-15 | Balance/receive/transit/cancel exceptions | 05_RULES §5.3; 06_TESTS EC-09..15 |
| E-16..E-21 | Repeat reversal/master/permission/idempotency/empty states | 05_RULES §5.3; 06_TESTS EC-16..21 |

