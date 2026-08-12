# 03_LOGIC — F-LOCATION-MASTER-001 Warehouse & Bin

> Business logic only; no HTTP request/response terms inside functions/engines

## §3.1 Scope-local Functions

| ID / function | Purpose | Calls | Side effects / errors |
|---|---|---|---|
| F-LOC-FN-01 `buildHierarchyQuery` | load child/tree graph tenant-safely | ENG-HIER-PATH | read only |
| F-LOC-FN-02 `buildLocationListQuery` | filter/search/paginate flat Locations | ENG-HIER-PATH | read only |
| F-LOC-FN-03 `loadNodeDetail` | load node, counts and path | ENG-HIER-PATH | read only / `ERR_NOT_FOUND` |
| F-LOC-FN-04 `createWarehouse` | validate Branch, code, temperature then create | FN-22, FN-23 | insert Warehouse+audit |
| F-LOC-FN-05 `updateWarehouse` | stale/Branch/temperature validation | FN-22, FN-23 | update+audit |
| F-LOC-FN-06 `createZone` | validate parent/sibling code | FN-23 | insert+audit |
| F-LOC-FN-07 `updateZone` | validate stale/sibling code | FN-23 | update+audit |
| F-LOC-FN-08 `createArea` | validate parent/sibling code | FN-23 | insert+audit |
| F-LOC-FN-09 `updateArea` | validate stale/re-parent policy | FN-23 | update+audit |
| F-LOC-FN-10 `createRack` | validate Area/sibling code | FN-23 | insert+audit |
| F-LOC-FN-11 `updateRack` | validate stale/re-parent policy | FN-23 | update+audit |
| F-LOC-FN-12 `deleteHierarchyNode` | block child-bearing parent, delete allowed node | FN-23 | delete+audit / `BR_PARENT_HAS_CHILDREN` |
| F-LOC-FN-13 `createLocation` | validate fields/type then create active | FN-14, FN-23 | insert+audit |
| F-LOC-FN-14 `validateLocationParent` | enforce Rack XOR Area/direct rule/unique code | — | validation only |
| F-LOC-FN-15 `updateLocation` | stale check; guard UOM; apply allowed fields | FN-14, FN-23 | update+audit |
| F-LOC-FN-16 `validateStatusTransition` | enforce lifecycle/reason/derived state | — | validation only |
| F-LOC-FN-17 `changeLocationStatus` | apply one manual transition | FN-16, FN-23 | update+audit |
| F-LOC-FN-18 `bulkGenerateLocations` | generate plan, validate all, commit transaction | ENG-LOC-GEN, FN-14, FN-23 | batch inserts+audits, atomic |
| F-LOC-FN-19 `bulkChangeLocationStatus` | validate all selected and commit atomic changes | FN-16, FN-23 | updates+audits |
| F-LOC-FN-20 `bulkSetStorageUom` | query stock; skip stocked IDs; update allowed IDs | FN-23, Inventory provider | updates+audits |
| F-LOC-FN-21 `decommissionLocation` | require no stock then terminal status | FN-23, Inventory provider | update+audit |
| F-LOC-FN-22 `resolveBranchSoftReference` | active picker; resolve stored inactive ref | Company provider | none / `BR_BRANCH_INVALID` |
| F-LOC-FN-23 `appendNodeAudit` | append immutable before/after/result once | — | insert audit |
| F-LOC-FN-24 `resolveGeoCascade` | adapt Geo lookup/postcode | Geo provider | none / `ERR_DEPENDENCY_UNAVAILABLE` |
| F-LOC-FN-25 `applyCapacitySignal` | derive `full`, remember/restore previous status | FN-16, FN-23 | update+audit |

### Critical algorithms

**`validateLocationParent(input)`**

1. require exactly one of `rack_id`/`area_id`; resolve same-tenant parent
2. if Area parent, require `allows_direct=true`
3. normalize code for comparison `[AI-DEFAULT: trim + case-insensitive]`
4. reject duplicate code within resolved parent; never compare across parents

**`bulkGenerateLocations(input)`**

1. pass pattern/dimensions to `ENG-LOC-GEN`; obtain deterministic plan and five-code preview
2. validate every planned Rack/Location and all sibling uniqueness before writes
3. start one DB transaction; insert all records and per-node/batch audit
4. any failure rolls back all records/audits; idempotent replay returns original batch

**Inventory guarded mutations**

Stock presence must be read inside the mutation decision window `[AI-DEFAULT]`. If provider is unavailable, fail closed with `ERR_DEPENDENCY_UNAVAILABLE`; do not assume `hasStock=false`.

## §3.2 Engines

### ENG-LOC-GEN: `location-generation` [NEW/DRAFT]

| Field | Value |
|---|---|
| owner | F-LOCATION-MASTER-001 |
| category | generation |
| global id | OQ-LOC-07 |

Input: patterns, rack quantity, rows, columns, levels and static Location attributes. Output: ordered `{racks[],locations[],sample_codes[],counts}` or validation errors.

Logic: parse only approved placeholders; enumerate deterministically; detect duplicate output codes; calculate totals; return a pure plan. No DB, HTTP, clock or random I/O.

- ✅ pure and substantial
- ✅ reusable for warehouse templates/import preview; registration candidate

### ENG-HIER-PATH: `hierarchy-path-builder` [NEW/DRAFT]

| Field | Value |
|---|---|
| owner | F-LOCATION-MASTER-001 |
| category | matcher/generation |
| global id | OQ-LOC-07 |

Input: typed node map plus selected node ID. Output: ordered path, child tree and aggregate counts. Reject cycles, missing parents and cross-tenant graph fragments. Pure, deterministic, no I/O.

- ✅ pure and substantial
- ✅ reusable by UI, Inventory contract and reporting; registration candidate

## §3.3 API ↔ Logic Trace (R8)

| API | Method | Calls functions | Engines |
|---|---|---|---|
| F-LOC-API-01 | GET | FN-01 | ENG-HIER-PATH |
| F-LOC-API-02 | GET | FN-01 | ENG-HIER-PATH |
| F-LOC-API-03 | GET | FN-02 | ENG-HIER-PATH |
| F-LOC-API-04 | GET | FN-03 | ENG-HIER-PATH |
| F-LOC-API-05 | POST | FN-04, FN-22, FN-23 | — |
| F-LOC-API-06 | PUT | FN-05, FN-22, FN-23 | — |
| F-LOC-API-07 | POST | FN-06, FN-23 | — |
| F-LOC-API-08 | PUT | FN-07, FN-23 | — |
| F-LOC-API-09 | POST | FN-08, FN-23 | — |
| F-LOC-API-10 | PUT | FN-09, FN-23 | — |
| F-LOC-API-11 | POST | FN-10, FN-23 | — |
| F-LOC-API-12 | PUT | FN-11, FN-23 | — |
| F-LOC-API-13 | DELETE | FN-12, FN-23 | — |
| F-LOC-API-14 | POST | FN-13, FN-14, FN-23 | — |
| F-LOC-API-15 | PUT | FN-14, FN-15, FN-23 | — |
| F-LOC-API-16 | PATCH | FN-16, FN-17, FN-23 | — |
| F-LOC-API-17 | POST | FN-14, FN-18, FN-23 | ENG-LOC-GEN |
| F-LOC-API-18 | PATCH | FN-16, FN-19, FN-23 | — |
| F-LOC-API-19 | PATCH | FN-20, FN-23 | — |
| F-LOC-API-20 | POST | FN-21, FN-23 | — |
| F-LOC-API-21 | GET | FN-23 (query projection) | — |
| F-LOC-API-22 | GET | FN-22 | — |
| F-LOC-API-23 | GET | FN-24 | — |
| F-LOC-API-24 | PATCH | FN-16, FN-25, FN-23 | — |

Verification: every mutation has ≥1 function; FN-01..25 and both engines are traced; HTTP/status mapping remains in `02_API.md`.

## §3.4 Dependencies and Value Stream

| Provider/consumer | Direction | Logic behavior on change/cancel |
|---|---|---|
| Company Branch | inbound config | inactive saved ref resolves; new selection active-only; no cascade |
| Geo Master | inbound lookup | unavailable dependency fails Geo lookup without local schema fallback |
| Inventory | bidirectional | revalidate stock before UOM/decommission; publish/read latest storage contract |
| Audit Trail | outbound | every mutation result append survives node lifecycle |
| Reporting | outbound read | decommissioned nodes remain queryable historically |

## §3.5 Probe Decisions

- PR-2 stale data: optimistic `version`; second writer gets `ERR_STALE_DATA`
- PR-3 permission mid-flight: re-check `canManage` at commit
- PR-4 lost response: idempotent replay; no duplicate write/audit
- PR-5 bulk atomicity: full validation + one transaction; bulk UOM explicitly reports stock skips
- PR-7 double submit: same key/body returns first result
- PR-9 inventory race: fail closed and re-check within decision window
- wizard draft/resume: no persisted draft endpoint in current scope; closing discards mock state `[AI-DEFAULT]`
