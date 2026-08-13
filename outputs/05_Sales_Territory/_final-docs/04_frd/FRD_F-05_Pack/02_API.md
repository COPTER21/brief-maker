# 02_API — F-05 Sales Territory

> Audience: BE developer (HTTP layer)  
> Business orchestration is in `03_LOGIC.md`; declarative rules are in `05_RULES.md`.

---

## §2.1 API Overview

| ID | Method | Path | Summary | Calls Logic |
|---|---|---|---|---|
| F-05-API-01 | GET | `/api/v1/sales-territories` | list/search/filter | FN-01 |
| F-05-API-02 | GET | `/api/v1/sales-territories/:id` | detail | FN-02 |
| F-05-API-03 | POST | `/api/v1/sales-territories` | create | FN-03, FN-04, FN-08 |
| F-05-API-04 | PATCH | `/api/v1/sales-territories/:id` | edit mutable fields | FN-03, FN-05, FN-08 |
| F-05-API-05 | POST | `/api/v1/sales-territories/:id/archive` | archive | FN-06, FN-08 |
| F-05-API-06 | POST | `/api/v1/sales-territories/:id/restore` | restore | FN-07, FN-08 |

All paths are current F-05-owned contracts. No current endpoint calls the five future modules.

## §2.2 Common Transport Contract

- Auth: required.
- Roles: read access per resolved permission; mutations only `sales_admin`/`system_admin` until OQ-02.
- Tenant context: canonical platform mechanism OQ-FRD-01; examples use `X-Tenant-Id` `[AI-DEFAULT]` and must adapt to platform standard.
- Mutation headers:
  - `Idempotency-Key` required `[AI-DEFAULT]` PR-4/PR-7.
  - `If-Match` required for edit/archive/restore `[AI-DEFAULT]` PR-2/OQ-16.
- Mutations reauthorize at execution `[AI-DEFAULT]` PR-3/OQ-17.
- Error envelope:

```json
{
  "error": {
    "code": "ERR_CODE",
    "message_key": "error.i18n.key",
    "field_errors": [{ "field": "route_code", "code": "BR_ROUTE_CODE_INVALID" }],
    "correlation_id": "opaque"
  }
}
```

## §2.3 Per-API Contracts

### F-05-API-01: GET /api/v1/sales-territories

| Field | Value |
|---|---|
| id | F-05-API-01 |
| auth | required |
| roles | resolved viewers; minimum sales_admin/system_admin |
| rate limit | platform default `[AI-DEFAULT]` |

Query:

- `q`: optional string, matches code/name/province/salesperson label/index representation.
- `status`: optional `active|archived`; UI initial value follows approved HTML.
- `region`, `province_code`: optional.
- `limit`: optional, default 20, max 100 `[AI-DEFAULT]`.
- `offset`: optional, default 0.

Response 200:

```json
{
  "data": [{
    "route_id": "uuid",
    "route_code": "R-BK-01",
    "route_name": "กรุงเทพฯ ชั้นใน สาย 1",
    "route_type": "area",
    "region": "ภาคกลาง",
    "province_code": "BKK",
    "salesperson_ref": "future-ref-or-null",
    "salesperson_label": "เอก ทวีสุข",
    "universe": 30,
    "status": "active",
    "version": 1,
    "updated_at": "2026-08-13T00:00:00Z"
  }],
  "meta": { "total": 1, "limit": 20, "offset": 0 }
}
```

Errors: 400 `ERR_INVALID_QUERY`; 401 `ERR_NOT_AUTHENTICATED`; 403 `ERR_INSUFFICIENT_ROLE`.

Side effects: none. Calls: F-05-FN-01.

### F-05-API-02: GET /api/v1/sales-territories/:id

| Field | Value |
|---|---|
| id | F-05-API-02 |
| auth/roles | same resolved viewer policy |
| path param | `id` uuid |

Response 200 is one Route record plus `audit_summary` (created/updated/archived metadata only). Current response must not imply live Customer/Order/Target/Visit/Salesperson data. UI mock metrics remain fixture/read-model state outside this core response.

Errors: 401, 403, 404 `ERR_ROUTE_NOT_FOUND`. Side effects: none. Calls: F-05-FN-02.

### F-05-API-03: POST /api/v1/sales-territories

| Field | Value |
|---|---|
| id | F-05-API-03 |
| auth/roles | required; sales_admin/system_admin |
| required header | `Idempotency-Key` `[AI-DEFAULT]` |

Body:

```json
{
  "route_code": "R-BK-01",
  "route_name": "กรุงเทพฯ ชั้นใน สาย 1",
  "route_type": "area",
  "region": "ภาคกลาง",
  "province_code": "BKK",
  "salesperson_ref": null,
  "universe": 30
}
```

Field validation: see BR-ST-04/06/07/08/18 and `04_DB.md`. Response 201 returns full owned record with `status=active`, `version=1`. Side effects: INSERT Route + audit in one transaction; save idempotency result. Calls: FN-03, FN-04, FN-08.

Errors: 400 validation; 403 role/revoked; 409 `ERR_ROUTE_CODE_CONFLICT` or `ERR_IDEMPOTENCY_CONFLICT`; 422 unresolved config/reference rule where applicable; 500 with atomic rollback.

### F-05-API-04: PATCH /api/v1/sales-territories/:id

| Field | Value |
|---|---|
| id | F-05-API-04 |
| auth/roles | sales_admin/system_admin |
| headers | `Idempotency-Key`, `If-Match: <version/etag>` `[AI-DEFAULT]` |

Allowed body fields: `route_name`, `route_type`, `region`, `province_code`, `salesperson_ref`, `universe`. `route_code` is rejected even if unchanged field is sent by a client that attempts mutation.

Response 200 returns updated record and incremented version. Side effects: UPDATE + append before/after audit atomically; cached idempotency result. Calls: FN-03, FN-05, FN-08.

Errors: 400 validation/immutable field; 403; 404; 409 `ERR_STALE_DATA`; 422 business rule; 500 rollback.

### F-05-API-05: POST /api/v1/sales-territories/:id/archive

| Field | Value |
|---|---|
| id | F-05-API-05 |
| auth/roles | sales_admin/system_admin |
| headers | `Idempotency-Key`, `If-Match` `[AI-DEFAULT]` |

Optional body: `{ "reason_code": "user_archive" }`. Preconditions: exists, `active`. Linked-customer count is included in warning only when an approved provider exists; its absence never blocks archive in current standalone release.

Response 200: `{ "route_id":"uuid", "route_code":"...", "status":"archived", "version":2 }`.

Side effects: state update + archive metadata + audit atomically; no hard delete; no current downstream event. Calls: FN-06, FN-08.

Errors: 403, 404, 409 stale/already archived, 422 state rule.

### F-05-API-06: POST /api/v1/sales-territories/:id/restore

| Field | Value |
|---|---|
| id | F-05-API-06 |
| auth/roles | sales_admin/system_admin |
| headers | `Idempotency-Key`, `If-Match` `[AI-DEFAULT]` |

Preconditions: exists, `archived`, code still unique. Response 200 returns Active record/version. Side effects: clear archive metadata, increment version, append audit atomically. Calls: FN-07, FN-08.

Errors: 403, 404, 409 `ERR_STALE_DATA`, `ERR_RESTORE_CODE_CONFLICT`, or already active. Restore conflict block is `[AI-DEFAULT]` OQ-20.

## §2.4 API ↔ Logic Trace Summary

| API | Functions | Engine |
|---|---|---|
| API-01 | FN-01 | — |
| API-02 | FN-02 | — |
| API-03 | FN-03, FN-04, FN-08 | — |
| API-04 | FN-03, FN-05, FN-08 | — |
| API-05 | FN-06, FN-08 | — |
| API-06 | FN-07, FN-08 | — |

Authoritative table: `03_LOGIC.md §3.3`. Every mutation traces to functions; no hidden CRUD/calculation lives here.

## §2.5 Cross-Module Contracts — Future Declaration Only

The modules below do not exist. Therefore F-05 exposes no live outbound calls/events and depends on none. These payload shapes are design-time contracts and must not be wired until the owning feature and PM/BA approve an actual interface.

### Future provider inputs

| Provider | Proposed use | Current behavior |
|---|---|---|
| Sales Team/Salesperson | resolve `salesperson_ref` + label/status | nullable soft ref/mock; no request |
| Customer Master | customer count/coverage | labelled mock/unavailable; no request |
| Sales Order | sales/order metrics | labelled mock/unavailable; no request |

### Future consumer snapshot DTO

```json
{
  "territory_route_id": "uuid",
  "territory_route_code": "R-BK-01",
  "territory_route_name": "กรุงเทพฯ ชั้นใน สาย 1",
  "territory_route_type": "area",
  "territory_region": "ภาคกลาง",
  "territory_province_code": "BKK",
  "snapshot_at": "ISO-8601"
}
```

Potential consumers: Customer Master, Visit Operation, Sales Target, Sales Order/documents/reports. Contract guarantees snapshot immutability; it does not declare their endpoints/events. Archive means not selectable for new transactions, while historical snapshots remain unchanged. Every future activation requires a revised/approved contract and XT tests.

