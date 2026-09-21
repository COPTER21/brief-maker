# 03_LOGIC — F084 Stocktake

## §3.1 Functions

| ID / function | Purpose | Invoked by | Side effects |
|---|---|---|---|
| F084-FN-01 `buildRoundListQuery` | filter/search rounds by tenant/status | API-01 | none |
| F084-FN-02 `createStocktakeRound` | create draft + audit | API-02 | insert round/event |
| F084-FN-03 `acquireScopeLock` | canonicalize scope and reject parent/child overlap | API-03 | insert lock |
| F084-FN-04 `captureInventorySnapshot` | capture qty/cost/watermark atomically | API-03 | insert snapshot/event |
| F084-FN-05 `assignCountSheet` | validate state/person/independence | API-04 | insert sheet/event, state |
| F084-FN-06 `appendCountSubmission` | validate active assignee and append lines | API-05 | insert submission/lines/event |
| F084-FN-07 `evaluateRecountGate` | pin policy version and decide recount/review | API-05 | state/event |
| F084-FN-08 `buildVarianceProjection` | assemble authorized variance DTO | API-06 | none |
| F084-FN-09 `submitVarianceForApproval` | resolve DOA, validate people, freeze chain | API-07 | approval steps/event/state |
| F084-FN-10 `recordApprovalDecision` | enforce current step/SoD/reason/concurrency | API-08 | step/event/state/optional unlock |
| F084-FN-11 `handoffAdjustmentDraft` | build/send F082 once, persist ack, close/unlock | API-09 | handoff/event/state/lock |
| F084-FN-12 `buildAuditTimeline` | return authorized append-only history | API-10 | none |

ทุก function รับ plain object/context ไม่รับ HTTP request/response โดยตรง

## §3.2 Engines

### F084-ENG-01 `stocktake-variance-engine` [DRAFT]

- Category: financial-calculation
- Input: `{snapshot_lines, count1, count2?, threshold, unit_cost_snapshot}`
- Output: `{lines:[{diff,abs_qty,exceeds,value_diff}], absolute_variance_value, needs_recount}`
- Logic: final count = count2 เมื่อมี submission ไม่เช่นนั้น count1; diff=count-system; recount เมื่อ `abs(diff)>threshold`; approval basis=sum(abs(diff*cost))
- Pure/deterministic/no I/O: yes
- Planned reuse: F084 and F086 Cycle Count

### F084-ENG-02 `stock-adjustment-draft-adapter` [DRAFT]

- Category: integration
- Input: approved round projection
- Output: F082 payload + normalized ack
- Validates `ref_count_doc`, signed qty diff, cost snapshot and unique item/location lines
- External I/O ถูกเรียกผ่าน FN-11; adapter contract แยกเพื่อ reuse กับ F086

## §3.3 API ↔ Logic Trace

| API | Functions | Engines |
|---|---|---|
| API-01 GET list | FN-01 | — |
| API-02 POST create | FN-02 | — |
| API-03 POST freeze | FN-03,FN-04 | — |
| API-04 POST assign | FN-05 | — |
| API-05 POST count | FN-06,FN-07 | ENG-01 |
| API-06 GET variance | FN-08 | ENG-01 |
| API-07 POST submit-approval | FN-09 | ENG-01 + DOA external |
| API-08 POST decision | FN-10 | — |
| API-09 POST adjustment-draft | FN-11 | ENG-02 |
| API-10 GET audit | FN-12 | — |

Verification: mutation 7/7 trace; functions 12/12 used; engines 2/2 used; no orphan or HTTP logic
