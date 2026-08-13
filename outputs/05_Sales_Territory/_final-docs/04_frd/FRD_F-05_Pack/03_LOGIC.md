# 03_LOGIC — F-05 Sales Territory

> Audience: BE business-logic developer  
> All functions are scope-local, camelCase and free of HTTP context.

---

## §3.1 Functions

### F-05-FN-01: `buildTerritoryListQuery`

- Purpose: normalize permitted list filters, permission scope and pagination into a DB query specification.
- Input: `{ tenantContext, actorContext, q?, status?, region?, provinceCode?, limit, offset }`.
- Output: `{ predicate, ordering, pagination }`.
- Invoked by: API-01.
- Calls: —.
- Side effects: read `T_sales_territory_route` only.
- Errors: `ERR_INVALID_QUERY`, `ERR_INSUFFICIENT_ROLE`.

### F-05-FN-02: `getTerritoryDetail`

- Purpose: retrieve one authorized Route and non-sensitive audit summary without resolving nonexistent providers.
- Input: `{ tenantContext, actorContext, routeId }`.
- Output: `TerritoryDetail | NotFound | Forbidden`.
- Invoked by: API-02.
- Calls: —.
- Side effects: read Route/audit.
- Errors: `ERR_ROUTE_NOT_FOUND`, `ERR_INSUFFICIENT_ROLE`.

### F-05-FN-03: `validateTerritoryInput`

- Purpose: central validation shared by create/edit; enforce BR-ST rules while preserving optional blank values.
- Input: `{ mode: create|edit, input, existing? }`.
- Output: `{ normalizedInput } | ValidationError[]`.
- Invoked by: API-03/API-04 before FN-04/FN-05.
- Calls: —.
- Side effects: none.
- Errors: `BR_ROUTE_CODE_INVALID`, `BR_ROUTE_CODE_IMMUTABLE`, `BR_REQUIRED_FIELD`, `BR_UNIVERSE_INVALID`, `BR_PROVINCE_INVALID`.

### F-05-FN-04: `createTerritoryRoute`

- Purpose: create an Active Route after validated authorization, idempotency and uniqueness checks.
- Input: `{ tenantContext, actorContext, normalizedInput, idempotencyContext }`.
- Output: `TerritoryRoute`.
- Invoked by: API-03.
- Calls: FN-08.
- Side effects: INSERT `T_sales_territory_route`; append created audit in same transaction; store idempotency result.
- Errors: `ERR_ROUTE_CODE_CONFLICT`, `ERR_PERMISSION_REVOKED`, `ERR_IDEMPOTENCY_CONFLICT`, `ERR_AUDIT_WRITE_FAILED`.

### F-05-FN-05: `updateTerritoryRoute`

- Purpose: update mutable fields with optimistic locking and preserve route code/history semantics.
- Input: `{ tenantContext, actorContext, routeId, expectedVersion, normalizedPatch, idempotencyContext }`.
- Output: updated `TerritoryRoute`.
- Invoked by: API-04.
- Calls: FN-08.
- Side effects: UPDATE owned mutable columns + version; append before/after audit atomically; store idempotency result.
- Errors: `ERR_STALE_DATA`, `BR_ROUTE_CODE_IMMUTABLE`, `ERR_PERMISSION_REVOKED`, `ERR_AUDIT_WRITE_FAILED`.

### F-05-FN-06: `archiveTerritoryRoute`

- Purpose: transition Active → Archived without deletion; record archive metadata and evidence.
- Input: `{ tenantContext, actorContext, routeId, expectedVersion, reasonCode?, idempotencyContext }`.
- Output: archived `TerritoryRoute`.
- Invoked by: API-05.
- Calls: FN-08.
- Side effects: UPDATE state/archive metadata/version; append audit; store idempotency result. No current downstream call/event.
- Errors: `BR_INVALID_STATE_TRANSITION`, `ERR_STALE_DATA`, `ERR_PERMISSION_REVOKED`, `ERR_AUDIT_WRITE_FAILED`.

### F-05-FN-07: `restoreTerritoryRoute`

- Purpose: transition Archived → Active after uniqueness/state checks `[AI-DEFAULT: block conflict]`.
- Input: `{ tenantContext, actorContext, routeId, expectedVersion, idempotencyContext }`.
- Output: active `TerritoryRoute`.
- Invoked by: API-06.
- Calls: FN-08.
- Side effects: UPDATE state/archive metadata/version; append audit; store idempotency result. No current downstream call/event.
- Errors: `BR_INVALID_STATE_TRANSITION`, `ERR_RESTORE_CODE_CONFLICT`, `ERR_STALE_DATA`, `ERR_PERMISSION_REVOKED`, `ERR_AUDIT_WRITE_FAILED`.

### F-05-FN-08: `appendTerritoryAudit`

- Purpose: build and append immutable audit evidence for each mutation inside the mutation transaction.
- Input: `{ routeId, action, actorId, before?, after?, result, correlationId?, reasonCode? }`.
- Output: `AuditRecord`.
- Invoked by: FN-04, FN-05, FN-06, FN-07; traced through their APIs.
- Calls: —.
- Side effects: INSERT `T_sales_territory_audit`; never update/delete.
- Errors: `ERR_AUDIT_WRITE_FAILED` causes mutation rollback.

## §3.2 Engines

No engine in this STANDARD feature. Validation, CRUD/state orchestration and audit coordination are scope-local; workload/coverage calculations shown in the prototype are unapproved mock rules and are not promoted into a reusable production Engine.

Future provider adapters must be designed only when their modules/contracts exist; they are not engines or runtime dependencies in this pack.

## §3.3 API ↔ Logic Trace (R8)

| API | Method | Path | Functions | Engines |
|---|---|---|---|---|
| F-05-API-01 | GET | `/api/v1/sales-territories` | FN-01 | — |
| F-05-API-02 | GET | `/api/v1/sales-territories/:id` | FN-02 | — |
| F-05-API-03 | POST | `/api/v1/sales-territories` | FN-03, FN-04, FN-08 through FN-04 | — |
| F-05-API-04 | PATCH | `/api/v1/sales-territories/:id` | FN-03, FN-05, FN-08 through FN-05 | — |
| F-05-API-05 | POST | `/api/v1/sales-territories/:id/archive` | FN-06, FN-08 through FN-06 | — |
| F-05-API-06 | POST | `/api/v1/sales-territories/:id/restore` | FN-07, FN-08 through FN-07 | — |

Verification: every mutation has ≥1 function; FN-01–FN-08 are all called directly or through a traced function; no orphan engine/function.

## §3.4 Transaction and Failure Semantics

- Route write + audit append commit together; audit failure rolls back Route mutation.
- Idempotency same key + same hash returns cached result without a second Route/audit write; same key + different hash returns 409 `[AI-DEFAULT]`.
- Version mismatch returns 409 and leaves persisted state unchanged `[AI-DEFAULT]`.
- Authorization is checked immediately before mutation `[AI-DEFAULT]`.
- Provider absence never participates in the core mutation transaction.

## §3.5 Future Snapshot Logic Boundary

When a future consumer exists, it copies the DTO declared in `02_API.md §2.5` at transaction time. F-05 does not rewrite a consumer snapshot on Route update/archive/restore. No transformer/adapter is implemented now because the consuming schemas do not exist.

## §3.6 Referenced Decisions

- Scope locks: `00_OVERVIEW.md §0.11`.
- Dynamic/default choices: OQ-02/05/07/14/16/17/20/21 and OQ-FRD-01/02.
- No DOA/DOCCFG/notification logic.

