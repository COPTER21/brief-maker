# RIF v2 · F-WH-ROP

> W4A FULL · 2026-09-14 · source W4 §2/W4A CHECKLIST/GOLDEN_RULES · unresolved defaults marked `[ASSUMED]`

## 1. Trigger, actors and result
Warehouse policy maintainer configures Item×Warehouse min/max/safety and effective date. Replenishment planner observes an availability snapshot and evaluates a policy; the result is a read-only suggestion, threshold status and optional PR soft-link mock payload. NC owns notification rules, recipients and delivery. Auditor reads versioned policy/suggestion events. No live PR/PO/GRN or inventory posting.

## 2. Locked requirements
| ID | Requirement | Evidence |
|---|---|---|
| BR-01 | one effective policy per Item×Warehouse at an evaluation date; Item/Warehouse soft refs | W4 §2; Golden Rule 4 |
| BR-02 | min/max/safety stored as versioned config with effective date, not code constant | W4 §2/§5 |
| BR-03 | validate `0≤safety≤min≤max` `[ASSUMED]` | Warehouse Product Owner default |
| BR-04 | evaluate available snapshot, trigger at `available≤min`, suggest `max(0,max-available)` `[ASSUMED]` | Warehouse Product Owner default |
| BR-05 | QHold excluded from available/ATP though on-hand retained | W4 OQ-QH-01 `[ASSUMED]` |
| BR-06 | NC rules decide notification threshold/channel; feature emits candidate with rule ref only | W4 §2/§5 |
| BR-07 | PR action is soft-link mock context only, no procurement record | W4A CHECKLIST/W4 mock rule |
| BR-08 | config/suggestion events append-only; replay cannot duplicate PR mock request | Golden Rule 4 |

## 3. Data contract and dependencies
| Data | Source/required | Boundary |
|---|---|---|
| Item code, Warehouse ref | existing master picker, soft refs | no hard FK UI validation |
| min/max/safety, effective date, version | feature config | policy owner edit only, history append-only |
| available/onHand/held snapshot, asOf | Inventory/QHold read model | no stock write |
| suggested qty, reason, policyVersion | derived read model | can prepare PR mock payload |
| NC rule ref/event candidate | NC external config | no local threshold/channel/delivery |
| PR context/ack | Purchase soft-link mock `[ASSUMED contract]` | no PR/PO implementation |

## 4. Exceptions and state
Missing policy → explicit no-policy state, no suggestion. Invalid bounds → field errors and no version. Equal-to-min boundary triggers under default; zero suggested qty produces no PR. Stale availability snapshot or policy version → warning/re-evaluate before PR mock; no source mutation. Duplicate same key returns prior mock acknowledgement. Policy `draft→effective→superseded` with append-only versions; suggestion `candidate→mock-linked` without procurement state. Warehouse-specific values never leak across locations.

## 5. OQ/ASSUMED and owner
ROP-01 inequality, trigger/equal boundary and suggested qty formula: Warehouse Product Owner. ROP-02 availability semantics/QHold and snapshot staleness: Inventory/QHold owners. ROP-03 policy effective-time and tie/version conflict: Warehouse Product Owner. ROP-04 NC event/rule envelope: NC owner. ROP-05 PR soft-link payload/ack: Purchase owner. ROP-06 CSQ declaration event: CSQ owner. All remain documented defaults; lane does not pause for OQ.

## 6. Scope/standard gap
Three tabs: policies, suggestions, history. Item/Warehouse use searchable master picker; canonical filter toolbar on list, tabs under page-head, no hint/banner. No Pattern Q or configurable notification number hardcoded. Declarations `ntf,csq` per chip. The graph does not provide live PR/NC contract; both are mock/TODO and tested only to payload/ack limits. A missing declaration or later detector mismatch must be recorded in DIVERGENCE/gate, not inferred as delivered.
