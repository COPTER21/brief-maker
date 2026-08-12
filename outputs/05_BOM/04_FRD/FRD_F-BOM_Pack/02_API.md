# 02_API — F-BOM-001 สูตรการผลิต (Bill of Materials)

> **Audience:** Backend HTTP layer, Frontend, QA  
> Business logic lives in `03_LOGIC.md`; every mutation below traces to at least one function.  
> Base headers: authenticated session/token and `X-Tenant-Id`; mutation headers additionally require `Idempotency-Key`.

---

## §2.1 API Overview

| ID | Method | Path | Summary | Roles |
|---|---|---|---|---|
| F-BOM-API-01 | GET | `/api/v1/boms` | list/filter/sort BOM | Planner, Costing, Auditor |
| F-BOM-API-02 | POST | `/api/v1/boms` | create draft/active BOM | Planner |
| F-BOM-API-03 | GET | `/api/v1/boms/:id` | detail, lines, audit, sibling versions | Planner, Costing, Auditor |
| F-BOM-API-04 | PUT | `/api/v1/boms/:id` | amend BOM aggregate | Planner |
| F-BOM-API-05 | POST | `/api/v1/boms/status` | change status for one/many records | Planner |
| F-BOM-API-06 | POST | `/api/v1/boms/bulk-delete` | guarded delete with result ledger | Planner |
| F-BOM-API-07 | GET | `/api/v1/boms/eligible` | active BOM choices/snapshot contract for MO | Production service/user |

## §2.2 Common Resource Shapes

```json
{
  "id": "uuid",
  "code": "BOM-000001",
  "parent_code": "FG-001",
  "version": "v1",
  "name": "สูตรมาตรฐาน",
  "out_qty": "1.000000",
  "out_uom_code": "PCS",
  "eff_from": "2026-08-12",
  "is_default": true,
  "status": "active",
  "used": 3,
  "version_no": 4,
  "created_by": "user-id",
  "created_date": "2026-08-12T08:00:00Z",
  "modified_by": "user-id",
  "modified_date": "2026-08-12T09:00:00Z"
}
```

Compatibility fields `approver_role`, `approved_by`, `approved_at`, and `approval_chain` are returned as `null`; they are not persisted and do not imply an approval workflow.

Line shape:

```json
{
  "id": "uuid",
  "line_no": 1,
  "component_code": "RM-001",
  "qty": "2.500000",
  "uom_code": "KG",
  "scrap_pct": "3.0000",
  "standard_cost": "12.340000",
  "line_cost": "31.775500"
}
```

`standard_cost`, `line_cost`, and `total_cost` are included only when the caller passes the D-CLASS access check; otherwise values are `null` with `cost_masked: true`.

## §2.3 Per-API Contract

### F-BOM-API-01 — GET `/api/v1/boms`

Query: `q`, `status=draft|active|inactive`, `parent_code`, `sort`, `direction=asc|desc`, `limit` (default 20, max 100), `offset` (default 0). Allowed sort fields: `code`, `parent_code`, `version`, `status`, `modified_date`.

**Response 200:** `{ "data": [BomSummary], "summary": {"total":0,"draft":0,"active":0,"inactive":0}, "total": 0, "limit": 20, "offset": 0 }`

Errors: `400 ERR_INVALID_QUERY_PARAMS`, `401 ERR_NOT_AUTHENTICATED`, `403 ERR_INSUFFICIENT_ROLE`.  
Calls: F-BOM-FN-01 `buildBomListQuery`; F-BOM-ENG-01 only when caller may view rollup.

### F-BOM-API-02 — POST `/api/v1/boms`

Headers: `Idempotency-Key` required. Body:

```json
{
  "parent_code": "FG-001",
  "version": "v1",
  "name": "สูตรมาตรฐาน",
  "out_qty": "1",
  "eff_from": null,
  "is_default": true,
  "target_status": "active",
  "lines": [
    {"component_code":"RM-001","qty":"2.5","uom_code":"KG","scrap_pct":"3"}
  ]
}
```

Field-level shape validation occurs at the HTTP boundary; all master/invariant/cross-line validation calls F-BOM-FN-05. The server ignores client-supplied code, usage, cost, audit, approval, and version-lock fields.

**Response 201:** `{ "data": BomDetail }`.  
Errors: `400 ERR_VALIDATION_FAILED`, `403 ERR_INSUFFICIENT_ROLE`, `409 ERR_IDEMPOTENCY_CONFLICT`, `409 BR_BOM_VERSION_DUPLICATE`, `422 BR_BOM_RULE_VIOLATION`, `503 ERR_MASTER_DATA_UNAVAILABLE`.  
Side effects: insert header/lines/audit; atomically clear previous default if applicable.  
Calls: F-BOM-FN-03, F-BOM-FN-05, F-BOM-FN-08, F-BOM-ENG-01.

### F-BOM-API-03 — GET `/api/v1/boms/:id`

Returns `{ "data": { ...Bom, "lines": [...], "total_cost": "...", "cost_as_of": "ISO-8601", "audit": [...], "other_versions": [...] } }`. `other_versions` excludes current `id` and includes enough identity/status/default data to navigate.

Errors: `401`, `403`, `404 ERR_BOM_NOT_FOUND`.  
Calls: F-BOM-FN-02 and F-BOM-ENG-01 when cost access is allowed.

### F-BOM-API-04 — PUT `/api/v1/boms/:id`

Headers: `Idempotency-Key` and `If-Match: <version_no>` required. Body matches API-02. Record code and `used` remain immutable/derived.

**Response 200:** `{ "data": BomDetail }`.  
Errors include API-02 errors plus `404 ERR_BOM_NOT_FOUND`, `409 ERR_STALE_DATA`.  
Side effects: replace aggregate lines in one transaction, update header, increment `version_no`, write before/after audit, adjust default atomically. Existing MO snapshots are never mutated.  
Calls: F-BOM-FN-04, F-BOM-FN-05, F-BOM-FN-08, F-BOM-ENG-01.

### F-BOM-API-05 — POST `/api/v1/boms/status`

Headers: `Idempotency-Key` required. Body:

```json
{"items":[{"id":"uuid","version_no":4}],"target_status":"inactive"}
```

Maximum 100 items. Transaction boundary is per record; response preserves all result rows.

**Response 200:**

```json
{"summary":{"success":1,"skipped":0,"failed":0},"results":[{"id":"uuid","result":"success","status":"inactive","version_no":5}]}
```

If any record is skipped/failed, return `207 Multi-Status` with per-record `code`; never roll back unrelated successful records. Target non-active clears default.  
Errors for request envelope: `400`, `401`, `403`, `409 ERR_IDEMPOTENCY_CONFLICT`.  
Calls: F-BOM-FN-06, F-BOM-FN-08.

### F-BOM-API-06 — POST `/api/v1/boms/bulk-delete`

Headers: `Idempotency-Key` required. Body: `{"items":[{"id":"uuid","version_no":2}]}`; maximum 100.

Per-record outcomes: `success`, `skipped` with `BR_BOM_IN_USE`, or `failed` with error code. Response status follows API-05 (`200` all success, `207` mixed). The server derives MO usage inside the transaction; it never trusts an input `used` count.

Calls: F-BOM-FN-07. Side effects: delete eligible header/lines, append audit tombstone; audit rows are retained.

### F-BOM-API-07 — GET `/api/v1/boms/eligible`

Query: `parent_code` required, `include_lines=true|false` (default false). Returns active versions only, default first, with current `version_no`. When `include_lines=true`, response supplies a snapshot-ready aggregate including lines and `snapshot_generated_at`; the MO service must persist its own immutable copy.

Errors: `400 ERR_PARENT_REQUIRED`, `403 ERR_INSUFFICIENT_ROLE`, `404 ERR_ACTIVE_BOM_NOT_FOUND`. Cost fields are excluded from this production contract.  
Calls: F-BOM-FN-09.

## §2.4 Common Concerns

### Idempotency (PR-4/PR-7)

- every mutation requires `Idempotency-Key`; cache normalized request hash + complete result for 24 hours `[AI-DEFAULT]`
- same key/body returns the original status and body without duplicate DB/audit effects
- same key/different body returns `409 ERR_IDEMPOTENCY_CONFLICT`
- clients may retry transport failures with the same key; three exponential-backoff attempts are a client guideline, not server business logic

### Optimistic locking (PR-2)

API-04 requires `If-Match`; bulk requests carry `version_no` per item. Mismatch returns/records `409 ERR_STALE_DATA`; no last-write-wins overwrite.

### Tenant isolation and audit

`X-Tenant-Id` is derived/verified against authenticated membership; PostgreSQL RLS applies the same tenant. Every mutation writes standardized Who/What/When/Where/Result and before/after data without secrets.

### Decimal and date encoding

Decimal values are JSON strings to prevent binary-float drift. Dates use `YYYY-MM-DD`; timestamps use ISO-8601 UTC. Server owns rounding described in ENG-01.

## §2.5 API ↔ Logic Trace (R8)

| API | Functions | Engine |
|---|---|---|
| API-01 GET list | FN-01 | ENG-01 conditionally |
| API-02 POST create | FN-03, FN-05, FN-08 | ENG-01 |
| API-03 GET detail | FN-02 | ENG-01 conditionally |
| API-04 PUT update | FN-04, FN-05, FN-08 | ENG-01 |
| API-05 POST status | FN-06, FN-08 | — |
| API-06 POST bulk-delete | FN-07 | — |
| API-07 GET eligible | FN-09 | — |

All four mutation APIs have a scope-local function. There is no business decision embedded solely in the HTTP layer.

## §2.X Cross-Module Contracts

| Direction | Module | Contract | Trigger | Failure behavior |
|---|---|---|---|---|
| inbound | Item Master `F-PDM` | active/type/name/image/base-UoM/standard-cost lookup | picker, validate, rollup | fail mutation if validation source unavailable; existing detail remains readable with explicit cost-unavailable state |
| inbound | UoM `F-UOM-001` | code/category/status lookup | component/UoM select and save | reject incompatible/inactive new choice |
| inbound | Policy D-CLASS | cost-view decision | list/detail/Costing read | default deny/mask; audit protected access |
| outbound | Production/MO | API-07 | MO selects recipe | active only; MO persists immutable snapshot |
| outbound | Costing | API-03 with cost permission | review/recalculate | current Item standard cost + `cost_as_of`; no persisted posting |
| outbound | Audit | shared append API/transactional outbox adapter | every mutation | mutation fails closed if immutable audit cannot be recorded `[AI-DEFAULT]` |

No business notification event is declared. BOM amendment/status changes do not rewrite an existing MO snapshot; there is therefore no compensating update event.

