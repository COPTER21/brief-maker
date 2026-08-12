# 03_LOGIC — F-BOM-001 สูตรการผลิต (Bill of Materials)

> **Audience:** Backend business-logic layer  
> Functions are HTTP-agnostic. ENG-01 is a pure deterministic candidate for CUBIC Registry.

---

## §3.1 Scope-Local Functions

### F-BOM-FN-01 — `buildBomListQuery`

- **Purpose:** normalize allowed filters/sort/pagination, enforce tenant scope, enrich current Item display/usage, and suppress cost unless authorized.
- **Input:** `{tenantId, actor, q?, status?, parentCode?, sort?, direction?, limit, offset}`
- **Output:** `{rows, summary, total}`
- **Invoked by:** API-01
- **Calls:** ENG-01 for visible row rollups only
- **Side effects:** none
- **Errors:** `ERR_INVALID_QUERY_PARAMS`, `ERR_INSUFFICIENT_ROLE`

### F-BOM-FN-02 — `getBomDetail`

- **Purpose:** load one aggregate plus audit and case-insensitive sibling versions for the same parent.
- **Input:** `{tenantId, actor, bomId}`
- **Output:** `BomDetail`
- **Invoked by:** API-03
- **Calls:** ENG-01 when cost is permitted
- **Side effects:** protected-data access audit when Confidential cost is returned
- **Errors:** `ERR_BOM_NOT_FOUND`, `ERR_INSUFFICIENT_ROLE`

### F-BOM-FN-03 — `createBom`

- **Purpose:** create header and lines in one transaction after authoritative validation.
- **Input:** `{tenantId, actor, command, idempotencyKey}`
- **Output:** persisted `BomDetail`
- **Invoked by:** API-02
- **Calls:** FN-05, FN-08, ENG-01
- **Side effects:** INSERT `T_bom_header`, `T_bom_line`, `T_bom_audit_log`; stores idempotency result
- **Errors:** validation/master/duplicate/default transaction codes from §5.6
- **Algorithm:** validate → allocate internal BOM code → normalize target/default → insert aggregate → set default atomically → audit → commit.

### F-BOM-FN-04 — `updateBom`

- **Purpose:** amend a BOM without changing code or any historical MO snapshot.
- **Input:** `{tenantId, actor, bomId, expectedVersionNo, command, idempotencyKey}`
- **Output:** updated `BomDetail`
- **Invoked by:** API-04
- **Calls:** FN-05, FN-08, ENG-01
- **Side effects:** lock/update header, replace lines, increment `version_no`, append before/after audit
- **Errors:** `ERR_BOM_NOT_FOUND`, `ERR_STALE_DATA`, validation/master errors
- **Algorithm:** lock row → compare version → load before image → validate current masters → replace aggregate → normalize default → audit → commit.

### F-BOM-FN-05 — `validateBomCommand`

- **Purpose:** apply VR-01..08 and BR-01..07/09/14/15 using current master data.
- **Input:** `{tenantId, bomId?, parentCode, version, name, outQty, targetStatus, isDefault, effFrom?, lines[]}`
- **Output:** `{normalizedCommand, masterSnapshotsForResponse, warnings[]}` or `ValidationError[]`
- **Invoked by:** FN-03, FN-04
- **Calls:** Item Master adapter, UoM adapter
- **Side effects:** none
- **Key checks:** trim and case-fold version for comparison; parent active FG; component active RM/PM/TR and not parent; unique components; qty >0; scrap 0..100; compatible active UoM; active-only default; decimal bounds.
- **Errors:** `BR_BOM_VERSION_DUPLICATE`, `BR_BOM_PARENT_INVALID`, `BR_BOM_COMPONENT_INVALID`, `BR_BOM_UOM_INVALID`, `BR_BOM_NUMERIC_RANGE`

### F-BOM-FN-06 — `changeBomStatuses`

- **Purpose:** process one or many all-direction status changes with an independent transaction/result per record.
- **Input:** `{tenantId, actor, items[{id,versionNo}], targetStatus, idempotencyKey}`
- **Output:** `{summary, results[]}`
- **Invoked by:** API-05
- **Calls:** FN-08 per record
- **Side effects:** UPDATE header/version/default; append audit; store idempotency result
- **Errors:** per-record `ERR_NOT_FOUND`, `ERR_STALE_DATA`, `ERR_INSUFFICIENT_ROLE`
- **Atomicity:** transaction per record `[AI-DEFAULT]`; a failure does not undo another record.

### F-BOM-FN-07 — `deleteEligibleBoms`

- **Purpose:** delete only selected BOMs with no live MO reference while returning a complete ledger.
- **Input:** `{tenantId, actor, items[{id,versionNo}], idempotencyKey}`
- **Output:** `{summary, results[]}`
- **Invoked by:** API-06
- **Calls:** MO usage adapter
- **Side effects:** for each eligible row, delete lines/header and append immutable tombstone audit
- **Errors:** per-record `BR_BOM_IN_USE`, `ERR_STALE_DATA`, `ERR_NOT_FOUND`, `ERR_INSUFFICIENT_ROLE`
- **Atomicity:** lock/recount/delete per record in one transaction; never trust UI count.

### F-BOM-FN-08 — `setDefaultBomAtomic`

- **Purpose:** enforce at most one active default per tenant/parent even under concurrent saves.
- **Input:** `{tenantId, parentCode, bomId, targetStatus, requestedDefault, actor}`
- **Output:** `{isDefault, clearedBomIds[]}`
- **Invoked by:** FN-03, FN-04, FN-06
- **Calls:** none
- **Side effects:** row/key lock; clear old default; set new default; append default-change audit entries
- **Rules:** if target is not `active`, return `isDefault=false`; if active but not requested, preserve another active default; database partial unique index is the final guard.

### F-BOM-FN-09 — `buildMoEligibleBomList`

- **Purpose:** return active BOM versions for one FG, default first, optionally in a snapshot-ready form.
- **Input:** `{tenantId, actor, parentCode, includeLines}`
- **Output:** `{boms[], snapshotGeneratedAt?}`
- **Invoked by:** API-07
- **Calls:** none
- **Side effects:** none
- **Rules:** exclude draft/inactive and all cost fields; order default then normalized version/code; MO owns the immutable copy after selection.

## §3.2 Engine

### F-BOM-ENG-01 — `bom-cost-rollup-engine` [NEW]

| Field | Value |
|---|---|
| code | `bom-cost-rollup-engine` |
| category | financial-calculation |
| status | DRAFT — register during development hand-off |
| owner | F-BOM-001 initially; reusable by Costing |

**Input schema**

```json
{
  "out_qty": "decimal > 0",
  "lines": [
    {"component_code":"string","qty":"decimal > 0","scrap_pct":"decimal 0..100","standard_cost":"decimal|null"}
  ],
  "rounding": {"scale":6,"mode":"HALF_UP"}
}
```

**Output schema**

```json
{
  "lines":[{"component_code":"RM-001","effective_qty":"2.575000","line_cost":"31.775500","cost_status":"available"}],
  "total_cost":"31.775500",
  "unit_cost":"31.775500",
  "has_missing_cost":false
}
```

**Logic**

1. Parse arbitrary-precision decimals; reject non-finite/overflow input.
2. `effective_qty = qty × (1 + scrap_pct / 100)`.
3. `line_cost = standard_cost × effective_qty`; provisional null cost contributes zero and sets `cost_status=missing`, `has_missing_cost=true`.
4. `total_cost = Σ(line_cost)` and `unit_cost = total_cost / out_qty`.
5. Keep full internal precision; round response values to scale 6 with `HALF_UP` `[AI-DEFAULT]`.

The engine is pure: no HTTP, database, clock, identity, or master lookup. It is reusable by BOM UI/API and future Costing. No calculated cost is accepted from the client.

## §3.3 API ↔ Logic Trace (R8 Anchor)

| API ID | Method | Functions | Engine path |
|---|---|---|---|
| F-BOM-API-01 | GET | FN-01 | FN-01 → ENG-01 conditionally |
| F-BOM-API-02 | POST | FN-03 → FN-05/FN-08 | FN-03 → ENG-01 |
| F-BOM-API-03 | GET | FN-02 | FN-02 → ENG-01 conditionally |
| F-BOM-API-04 | PUT | FN-04 → FN-05/FN-08 | FN-04 → ENG-01 |
| F-BOM-API-05 | POST | FN-06 → FN-08 | — |
| F-BOM-API-06 | POST | FN-07 | — |
| F-BOM-API-07 | GET | FN-09 | — |

Self-check: every mutation has a function; FN-01..09 are invoked; ENG-01 is invoked; API has no hidden business rule.

## §3.4 Transaction and Concurrency Model

| Operation | Lock/transaction | Idempotency |
|---|---|---|
| create | transaction + parent default key/advisory or equivalent lock | request result 24h |
| update | `FOR UPDATE` header + expected `version_no` + default lock | request result 24h |
| status | transaction per record + expected version | whole request result 24h |
| bulk delete | transaction per record + current MO reference check | whole request result 24h |

The unique indexes in `04_DB.md` settle version/default races. A unique violation is mapped to a stable business error, not leaked as raw SQL.

## §3.5 Dependencies

- Item Master adapter: current Item identity/status/type/base UoM/standard cost.
- UoM adapter: current UoM status/category.
- Policy D-CLASS: cost access decision.
- MO usage adapter: authoritative live reference count and snapshot consumer.
- immutable audit adapter/table: transactionally durable evidence.

Circuit behavior: mutation validation fails closed when required master/audit dependencies are unavailable. Read detail may return structure with `cost_unavailable=true` when only cost lookup fails.

## §3.6 Locked Decisions Referenced

- no approval or notification orchestration
- `eff_from` is stored/displayed only; no scheduler
- existing MO snapshots never change after BOM amendment
- current standard cost is read at response/recalculation time; it is not persisted as BOM source-of-truth
- internal code allocation is `[AI-DEFAULT]` `BOM-` + database sequence; this is not Document Configuration

