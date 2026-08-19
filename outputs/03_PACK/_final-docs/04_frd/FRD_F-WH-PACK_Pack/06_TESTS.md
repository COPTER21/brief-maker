# 06_TESTS — F-WH-PACK Packing

## §6.1 Acceptance Inventory

| ID | Scenario | Expected |
|---|---|---|
| AT-01 | Picking handoff one SO | one queued job/stable ref |
| AT-02 | wave two SO + retry | two refs, no duplicate |
| AT-03 | start job | in_progress, no carton, audit/event |
| AT-04 | open master/custom carton | one active; snapshot correct |
| AT-05 | scan code/qty/UOM/lot/name | allocation/remaining/weight exact |
| AT-06 | over-pack/concurrent scan | never exceeds picked; loser 409/422 |
| AT-07 | empty vs non-empty close | empty blocked; valid closes+label version |
| AT-08 | computed/actual weight | decimal result; missing source guarded; override audited |
| AT-09 | finish valid | packed + slip available + event |
| AT-10 | finish invalid | disabled/API reject with exact reason |
| AT-11 | reopen pack/carton | before DN only; label invalidated/reprint |
| AT-12 | cancel | reason required; returns job; new pack number later |
| AT-13 | BOXLABEL | 150×100, one page/carton, required fields/barcode/QR |
| AT-14 | PACKSLIP/print failure | A4 required fields; failure leaves state unchanged |
| AT-15 | audit | all mutations present once, chronological, immutable |
| AT-16 | idempotency/network retry | same response; different body conflict |
| AT-17 | tenant/warehouse isolation | no cross-scope read/write/export |
| AT-18 | role/ownership/mid-session revoke | server denies correctly |
| AT-19 | shipped lock | all mutations rejected for all roles |
| AT-20 | responsive/keyboard | 1024/1280 no body hscroll; Enter/F2/F3/Ctrl+Z/Esc/focus |

## §6.2 FN Coverage

| FN range | Tests |
|---|---|
| FN-01..04 | AT-01/02/03 + XT-01/02 |
| FN-05..15 | AT-03..08/16 |
| FN-16..17 | AT-13/14 |
| FN-18..25 | AT-09..12/18/19 |
| FN-90..95 | AT-15/17/20 + UI test cases generated downstream |

## §6.3 Test Data

Three tenants; two warehouses; wh_lead/packer/viewer; Picking records including wave two SO, free item, cold item, pickup, large quantity, lot/expiry, zero-picked/service exclusions; cartons S/M/L/pallet/custom; packs in each state and stale versions.

## §6.4 Definition of Done

- all P0/P1 acceptance/API/integration/E2E pass; zero open critical/high defects
- logic unit coverage ≥80%; invariant/property tests cover allocation and weight
- RLS/ABAC/security and migration rollback verified
- print dimensions/font/pagination validated on Chromium and target printer profile
- outbox retry/idempotency/monitoring dashboards verified
- OQ-gated Transfer/DN code remains disabled until locked contracts exist
- UX waiver debt is not treated as passing; production implementation meets §1.8

## §6.5 Performance

| Area | Target [AI-DEFAULT pending baseline] |
|---|---|
| queue/list | p95 <500ms at 100k packs/tenant |
| scan mutation | p95 <300ms at 10 commands/sec/tenant |
| detail 1,000 lines/200 cartons | p95 <2s excluding binaries |
| print | p95 <10s; async queue under load |

## §6.6 API/Logic Trace

AT-01/02→FN-01; AT-03→FN-02; AT-04→FN-03/ENG-01; AT-05/06→FN-04/ENG-01; AT-07/08→FN-05/ENG-01; AT-09/10→FN-07; AT-11→FN-06/08; AT-12→FN-09; AT-13/14→FN-13/ENG-02; AT-15→FN-11/12; AT-16→all mutation coordinators; AT-17/18→API middleware+functions; AT-19→rules/FN-06..10.

## §6.7 Cross-Module Tests

| ID | Scenario | Expected |
|---|---|---|
| XT-01 | Picking `picked` sends wave | Pick becomes to_pack only after stable pack refs; one per SO |
| XT-02 | Transfer input attempted | rejected/feature disabled until OQ-XT-01; no invented job |
| XT-03 | DN unavailable/retry/success | remain packed on fail; no duplicate; lock only after stable dn_ref |
| XT-04 | ENG-NOTIFY unavailable/retry | Packing commits once; outbox retries/dedupes declared event |
| XT-05 | master item/carton changes after start | stored snapshots/old prints unchanged |

## §6.8 Microcopy

AI/browser tests must anchor to verbatim visible strings and routes extracted from root HTML. FRD error codes are stable; displayed Thai text may come from HTML/central microcopy and must not be independently hardcoded in test logic.
