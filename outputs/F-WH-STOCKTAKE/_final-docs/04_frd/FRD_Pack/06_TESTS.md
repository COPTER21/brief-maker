# 06_TESTS — F084 Stocktake

## §6.1 Acceptance Inventory

| ID | Acceptance |
|---|---|
| AT-01 | valid name+scope creates draft and moves to sheets |
| AT-02 | missing name/scope stays create and shows exact validation |
| AT-03 | supervisor freeze captures snapshot and active lock atomically |
| AT-04 | overlapping/empty scope is blocked without partial snapshot |
| AT-05 | first assignment changes to counting and shows named person |
| AT-06 | counter response is blind; other counter cannot edit/submit |
| AT-07 | complete nonnegative count appends once; zero is valid |
| AT-08 | blank/negative/direct unauthorized submission is blocked |
| AT-09 | over-threshold first count requires independent recount |
| AT-10 | equal/below threshold goes review; same recount person blocked |
| AT-11 | supervisor variance uses frozen snapshot/cost and final count |
| AT-12 | DOA resolve uses absolute value and requires correct slot count |
| AT-13 | counters/duplicate approvers/missing slot are blocked |
| AT-14 | only current sequential approver may decide |
| AT-15 | reject requires reason, appends event and releases lock |
| AT-16 | final approve reaches approved only after all steps |
| AT-17 | F082 handoff is once/idempotent and close occurs after ack |
| AT-18 | F082 failure keeps approved+locked; Stocktake never changes on-hand |
| AT-19 | history shows flat handoff summary; count action buttons have usable gap |
| AT-20 | demo persona element is absent from production build |

## §6.2 Test Inventory

UI/E2E regression: existing shared suite 20/20, FN 12/12, console errors 0. AI test set `testcases-F-WH-STOCKTAKE.md` expands happy/negative/permission/concurrency/integration cases

## §6.3 Data

- ST-2026-001 snapshot ITM-001=12 cost 25,000; ITM-002=20 cost 1,200
- P1 กิตติพงษ์ first counter; P2 พิมพ์ดาว recount; P3 นลิน approver step1; P4 อรทัย step2; P5 วิชญ์ step3
- first count 9/20 → recount; second 11/20 → final diff -1/0; absolute value 25,000 → 2 steps in prototype DOA mock

## §6.4 Definition of Done

- all P0/P1 UI, API and logic tests pass
- no counter data leak; unauthorized direct call denied
- no duplicate snapshot/decision/handoff under retry/concurrency
- F082 contract and lock release verified in integration environment
- DOA entry wired and role mapping confirmed
- production bundle excludes demo-only selector

## §6.5 Performance

List P95 <500ms; variance ≤5,000 lines P95 <2s; freeze snapshot 50,000 lines completes within agreed maintenance window and never exposes partial state

## §6.8 Trace

| Acceptance | API | Logic |
|---|---|---|
| AT-01/02 | API-02 | FN-02 |
| AT-03/04 | API-03 | FN-03/04 |
| AT-05/06 | API-04/05/06 | FN-05/06/08 |
| AT-07..10 | API-05 | FN-06/07, ENG-01 |
| AT-11..16 | API-06/07/08 | FN-08/09/10, ENG-01 |
| AT-17/18 | API-09 | FN-11, ENG-02 |
| AT-19/20 | UI/build | — |

## §6.9 Cross-Module Tests

| ID | Scenario | Expected |
|---|---|---|
| XT-01 | approved round handoff to F082 | draft ack contains ref_count_doc and exact signed lines; no stock movement by F084 |
| XT-02 | F082 unavailable/retry | round remains approved+locked; retry does not create two drafts |
| XT-03 | movement within/outside lock | overlapping scope blocked; outside scope remains allowed |
| XT-04 | DOA registry changes after submit | in-flight round keeps frozen chain/person sequence |
| XT-05 | F089 scan hook | UI explains prototype uses manual entry; no false barcode result |

## §6.10 Microcopy

Expected UI messages must match `01_UI §1.8` verbatim; HTML wins if future drift is found
