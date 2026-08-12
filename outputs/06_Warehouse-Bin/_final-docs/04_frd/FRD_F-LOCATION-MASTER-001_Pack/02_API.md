# 02_API — F-LOCATION-MASTER-001 Warehouse & Bin

> Base: `/api/v1` · JSON · JWT required · tenant resolved by platform middleware  
> Mutations require `canManage`, `Idempotency-Key` and `If-Match` where an existing record changes `[AI-DEFAULT]`

## §2.1 Common Contract

Success envelope: `{ "data": ..., "meta": { "correlation_id": "uuid" } }`. Error envelope: `{ "error": { "code": "...", "message_key": "...", "fields": {} }, "meta": { "correlation_id": "uuid" } }`.

- list params: `search`, `status`, `type`, `cursor`, `limit` (default 25, max 100) `[AI-DEFAULT]`
- mutation transaction includes the business write and one append to `T_location_audit`
- same idempotency key + same body returns original result; same key + different body → `ERR_DUPLICATE_IDEMPOTENCY_KEY`
- stale `If-Match` → `ERR_STALE_DATA`; permission is rechecked at commit

## §2.2 Endpoint Inventory

| ID | Method/path | Purpose | Reads | Writes | Logic |
|---|---|---|---|---|---|
| API-01 | GET `/location-nodes?parent_type&parent_id` | root/child list | hierarchy tables | — | FN-01, ENG-HIER-PATH |
| API-02 | GET `/location-hierarchy?warehouse_id` | full tree | hierarchy tables | — | FN-01, ENG-HIER-PATH |
| API-03 | GET `/locations` | flat Location list/filter | `T_location` + parents | — | FN-02, ENG-HIER-PATH |
| API-04 | GET `/location-nodes/{node_type}/{id}` | node detail/path | hierarchy tables | — | FN-03, ENG-HIER-PATH |
| API-05 | POST `/warehouses` | create Warehouse | Company Branch ref | `T_warehouse`, audit | FN-04, FN-22 |
| API-06 | PUT `/warehouses/{id}` | update Warehouse | Warehouse/Branch | `T_warehouse`, audit | FN-05, FN-22 |
| API-07 | POST `/zones` | create Zone | Warehouse | `T_zone`, audit | FN-06 |
| API-08 | PUT `/zones/{id}` | update Zone | Zone | `T_zone`, audit | FN-07 |
| API-09 | POST `/areas` | create Area | Zone | `T_area`, audit | FN-08 |
| API-10 | PUT `/areas/{id}` | update Area | Area | `T_area`, audit | FN-09 |
| API-11 | POST `/racks` | create Rack | Area | `T_rack`, audit | FN-10 |
| API-12 | PUT `/racks/{id}` | update Rack | Rack | `T_rack`, audit | FN-11 |
| API-13 | DELETE `/location-nodes/{node_type}/{id}` | delete parent node | child existence | parent table, audit | FN-12 |
| API-14 | POST `/locations` | create Location | parent/type config | `T_location`, audit | FN-13, FN-14 |
| API-15 | PUT `/locations/{id}` | update Location | Location/Inventory | `T_location`, audit | FN-14, FN-15 |
| API-16 | PATCH `/locations/{id}/status` | manual status | Location | `T_location`, audit | FN-16, FN-17 |
| API-17 | POST `/locations/bulk-generate` | generate Rack/Locations | Area/type config | Rack/Location/audit | FN-18, ENG-LOC-GEN |
| API-18 | PATCH `/locations/bulk-status` | atomic bulk status | Locations | Location/audit | FN-19 |
| API-19 | PATCH `/locations/bulk-storage-uom` | guarded bulk UOM | Locations/Inventory | Location/audit | FN-20 |
| API-20 | POST `/locations/{id}/decommission` | terminal soft status | Location/Inventory | Location/audit | FN-21 |
| API-21 | GET `/location-nodes/{node_type}/{id}/audit` | audit timeline | `T_location_audit` | — | FN-23 |
| API-22 | GET `/references/branches?active=true` | Company active picker | external Company API | — | FN-22 |
| API-23 | GET `/references/geo` | Geo cascade proxy/adapter | external Geo API | — | FN-24 |
| API-24 | PATCH `/locations/{id}/capacity-signal` | set/restore derived `full` | Location | Location/audit | FN-25 |

API IDs in trace tables use full prefix `F-LOC-API-NN`; short `API-NN` above is equivalent.

## §2.3 Resource Schemas

### Hierarchy node

```json
{
  "id": "uuid", "node_type": "warehouse|zone|area|rack|location",
  "code": "string", "name": "string", "status": "string",
  "parent": { "type": "string|null", "id": "uuid|null" },
  "path": [{ "type": "warehouse", "id": "uuid", "code": "WH-BKK" }],
  "child_counts": { "zones": 0, "areas": 0, "racks": 0, "locations": 0 },
  "version": 1
}
```

### Location write body

```json
{
  "parent": { "type": "rack|area", "id": "uuid" },
  "code": "A-01-R01-C01-L1", "name": "string",
  "location_type_code": "RESERVE", "storage_uom": "ลัง",
  "capacity_value": 1, "capacity_uom": "pallet",
  "rotation": "fifo", "is_pickable": true, "is_putaway": true
}
```

Create returns 201 and `status=active`. Update returns 200 and next `version`; server ignores client attempts to set derived `full`.

### Status body

```json
{ "target_status": "active|inactive|blocked|frozen", "reason": "string|null" }
```

`reason` is required for blocked/frozen. `decommissioned` uses API-20; `full` uses API-24 integration only.

### Bulk generation body

```json
{
  "area_id": "uuid", "rack_pattern": "A-{n}", "rack_quantity": 5,
  "rows": 4, "columns": 12, "levels": 4,
  "location_pattern": "{rack}-R{r}-C{c}-L{l}",
  "location_type_code": "RESERVE", "storage_uom": "ลัง",
  "capacity_value": 1, "capacity_uom": "pallet", "rotation": "fifo"
}
```

Response 201: `{ "data": { "batch_id":"uuid", "rack_count":5, "location_count":960, "sample_codes":[...] } }`. Any validation/unique/write failure rolls back the entire batch.

### Bulk status/UOM

- status body: `{ "location_ids":["uuid"], "target_status":"...", "reason":"..." }`
- UOM body: `{ "location_ids":["uuid"], "storage_uom":"ลัง" }`
- response includes `updated_count`, `skipped_count`, and per-ID `skipped` reasons; API-19 skips `hasStock=true` to match HTML, while any DB failure rolls back all allowed updates

## §2.4 Key Preconditions and Responses

| Operation | 2xx | Business rejection |
|---|---:|---|
| create/update sibling code | 201/200 | 409 `BR_LOCATION_CODE_DUPLICATE` |
| direct Area Location | 201 | 422 `BR_AREA_DIRECT_NOT_ALLOWED` |
| blocked/frozen no reason | 200 | 422 `BR_STATUS_REASON_REQUIRED` |
| manual `full` | — | 422 `BR_FULL_DERIVED_ONLY` |
| update UOM with stock | —/skip bulk | 422 `BR_STORAGE_UOM_LOCKED_HAS_STOCK` |
| decommission with stock | — | 422 `BR_DECOMMISSION_HAS_STOCK` |
| delete parent with child | — | 409 `BR_PARENT_HAS_CHILDREN` |
| invalid batch | — | 422 `BR_BULK_TEMPLATE_INVALID` |

## §2.5 Cross-module Contracts

### Company Branch (upstream)

API-22 adapts the approved Company contract and returns active branches for picker. API-05/06 store only `branch_id`. Existing inactive reference is resolved by ID for view/edit; Company deletion/deactivation never cascades. Exact upstream route is reused from F-ORG-001 implementation and is not redefined here.

### Geo Master (upstream)

API-23 is an adapter seam for province/district/subdistrict/postcode. Exact route/payload is blocked by OQ-LOC-01. This feature creates no Geo tables.

### Inventory (bidirectional guard/config)

- outward read contract: GET `/api/v1/locations/{id}/storage-contract` `[AI-DEFAULT]` returns `location_id,path,storage_uom,loc_status,version`
- inward query used before API-15/19/20: Inventory stock presence returns `{location_id,has_stock,checked_at,version}`; exact owned Inventory route/event is OQ-LOC-08
- API-24 accepts trusted service capacity signal to derive `full`; authentication mechanism is platform-owned `[AI-DEFAULT]`
- no GRN/Putaway/RTV/Pick-Pack-Ship APIs are defined

## §2.6 Security and Logging

- reads require authenticated tenant context; mutations require `canManage`; API-24 requires trusted integration principal
- audit/log payload excludes tokens, credentials and personal profile data
- unauthorized/cross-tenant resource returns platform-standard 404/403 without revealing existence `[AI-DEFAULT]`
- rate/size limit for batch: exact threshold not supplied — ไม่พบข้อมูลในบทสนทนา; validate before implementation

## §2.7 API → Rule/Test Pointer

All endpoint errors map to `05_RULES §5.6`; mutation trace is authoritative in `03_LOGIC §3.3`; acceptance coverage is in `06_TESTS §6.1/§6.8`.
