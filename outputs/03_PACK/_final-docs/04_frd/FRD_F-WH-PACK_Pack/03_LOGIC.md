# 03_LOGIC — F-WH-PACK Packing

## §3.1 Scope-Local Functions

| ID | Function | Purpose | Side effects / Errors |
|---|---|---|---|
| F-WH-PACK-FN-01 | `ingestPickingHandoff` | validate/split incoming Pick per source SO idempotently | create jobs; return stable refs; `ERR_SOURCE_CONTRACT`, `ERR_IDEMPOTENCY_MISMATCH` |
| F-WH-PACK-FN-02 | `startPackingJob` | lock available job and create active pack | pack/job/audit/outbox; `BR_JOB_UNAVAILABLE` |
| F-WH-PACK-FN-03 | `openPackBox` | enforce one-active and snapshot master/custom | box/audit; `BR_ACTIVE_BOX_EXISTS` |
| F-WH-PACK-FN-04 | `mutateBoxAllocation` | apply scan/add/set/remove atomically | items/box/pack/audit; `BR_QTY_EXCEEDS_PICKED` |
| F-WH-PACK-FN-05 | `closePackBox` | verify non-empty, persist weight, close, create label version | box/label/audit/outbox |
| F-WH-PACK-FN-06 | `reopenPackBox` | validate lead/no DN/no active; invalidate label | box/label/audit |
| F-WH-PACK-FN-07 | `finishPack` | reconcile all lines and transition packed | pack/audit/outbox |
| F-WH-PACK-FN-08 | `reopenPack` | `packed→in_progress` before DN | pack/audit |
| F-WH-PACK-FN-09 | `cancelPack` | require reason, cancel, return job queue | pack/job/audit/outbox |
| F-WH-PACK-FN-10 | `handoffDeliveryNote` | invoke disabled/versioned DN port idempotently | outbox/integration result; OQ-DN-01 |
| F-WH-PACK-FN-11 | `appendPackAudit` | append standardized event in same transaction | insert only |
| F-WH-PACK-FN-12 | `buildPackingReadModel` | filter/scope/compose list/detail/audit responses | read only |
| F-WH-PACK-FN-13 | `requestPackPrint` | validate state/version and enqueue renderer | print job/audit |
| F-WH-PACK-FN-14 | `buildPackExport` | role-scoped streaming CSV | export audit |

All functions accept explicit `{tenant_id,actor,warehouse_scope,input,expected_version,idempotency_key}` context and contain no HTTP request/response objects.

## §3.2 Engines

### F-WH-PACK-ENG-01: `pack-carton-engine` [DRAFT]

| Field | Value |
|---|---|
| category | matcher/calculation |
| owner | F-WH-PACK; candidate shared |
| stateless/pure/deterministic | true/true/true |

Input: picked source lines with UOM/lot/weight, existing carton allocations, carton tare/capacity and requested operation. Output: validated allocations, remaining per line, computed weight, capacity warning, suggested carton split. It performs no DB/HTTP/printing and never substitutes mock production weights.

Errors: `ENG_ERR_INVALID_INPUT`, `ENG_ERR_WEIGHT_SOURCE_MISSING`, `ENG_ERR_ALLOCATION_OVERFLOW`.

### F-WH-PACK-ENG-02: `packing-document-renderer` [DRAFT]

Generation engine receiving immutable pack/box snapshot + template/version and returning document bytes/metadata. It must support PACKSLIP A4 and BOXLABEL 150×100, embedded Sarabun, deterministic pagination and no mutable DB reads. Storage/queue orchestration remains FN-13.

Errors: `ENG_ERR_TEMPLATE_VERSION`, `ENG_ERR_RENDER_FAILED`, `ENG_ERR_FONT_MISSING`.

## §3.3 API ↔ Logic Trace

| API | Functions | Engines |
|---|---|---|
| API-01/02/03/04/16 | FN-12 | — |
| API-05 | FN-02, FN-11 | — |
| API-06 | FN-03, FN-11 | ENG-01 |
| API-07 | FN-04, FN-11 | ENG-01 |
| API-08 | FN-05, FN-11 | ENG-01 |
| API-09 | FN-06, FN-11 | — |
| API-10 | FN-07, FN-11 | ENG-01 |
| API-11 | FN-08, FN-11 | — |
| API-12 | FN-09, FN-11 | — |
| API-13 | FN-10, FN-11 | — |
| API-14/15 | FN-13, FN-11 | ENG-02 |
| API-17 | FN-14, FN-11 | — |
| Picking inbound port | FN-01, FN-11 | — |

No orphan function/engine. Every mutation traces to function(s); calculations/rendering stay out of HTTP.

## §3.4 Transaction and Concurrency

- Use one DB transaction per command; pack/box row lock or atomic version condition prevents over-pack.
- Unique keys enforce intake/idempotency/box numbering/label versions.
- Audit and outbox inserts commit with aggregate mutation.
- Failed renderer/notification/DN delivery runs after commit and cannot rollback Packing state.
- Retry worker uses `FOR UPDATE SKIP LOCKED`, exponential backoff and dedupe key.

## §3.5 Undo

Prototype undo-10 is UI/session behavior. Production backend should expose allocation mutations that are individually reversible before carton close; frontend may keep last 10 command inverses in memory. Closed/reopened transitions require explicit API/audit and are not generic Ctrl+Z.
