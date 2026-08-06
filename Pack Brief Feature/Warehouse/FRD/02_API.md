# 02_API — F-LOCATION-MASTER-001 (v2 · HTTP layer)

Auth: Bearer. RBAC enforced per role (§4.2 BRD). All mutation APIs trace to 03_LOGIC §3.3. `{level}` ∈ `warehouses|zones|areas|racks`.

## Hierarchy node CRUD (generic — 4 levels)

### API-01 GET /hierarchy/{level}
List children of a parent / search. Query: `parent_id?, q?, status?, sort?, dir?, page?, page_size?`. → `{data:Node[], total, page, page_size}`. Calls: buildNodeQuery(FN-01), buildHierarchyPath(FN-02), ENG-HIER-PATH.

### API-02 GET /hierarchy/{level}/{id}
→ `NodeDetail` + full path + child counts + audit. Calls: getNode(FN-03), buildHierarchyPath(FN-02).

### API-03 POST /hierarchy/{level}
Body: node payload (per-level fields, §04). Validates parent active + code unique within parent; zone → temp range (FN-09); area → allows_direct flag set. → 201 `Node`. Calls: validateNodeParent(FN-04), validateZoneTemp(FN-09, zones only), createNode(FN-05). Errors: 409 CODE_DUPLICATE, 422 PARENT_INACTIVE, 422 TEMP_RANGE_REQUIRED.

### API-04 PUT /hierarchy/{level}/{id}
Update attrs. area disabling allows_direct → guard (FN-10). Calls: validateNodeParent(FN-04), validateAreaDirectToggle(FN-10, areas only), updateNode(FN-06). Errors: 409 CODE_DUPLICATE, 422 HAS_DIRECT_LOCATIONS.

### API-05 DELETE /hierarchy/{level}/{id}
Referential-safe delete (Manager/Admin only). Calls: validateNodeDeletable(FN-07), deleteNode(FN-08). Errors: 422 HAS_CHILDREN, 403 FORBIDDEN.

## Location APIs

### API-10 POST /locations
Body: location payload. Validates flexible-parent (FN-13) + allows_direct (FN-14); applyTypeDefaults (FN-23, Phase 3). → 201. Calls: validateFlexibleParent(FN-13), validateAllowsDirect(FN-14), applyTypeDefaults(FN-23), createLocation(FN-15). Errors: 422 INVALID_PARENT, 422 AREA_NOT_DIRECT, 409 CODE_DUPLICATE, 422 CAPACITY_INVALID.

### API-11 PUT /locations/{id}
Update attrs. parent change → reparent rule. Calls: validateFlexibleParent(FN-13), updateLocation(FN-16). Errors: 409 CODE_DUPLICATE, 422 REPARENT_REQUIRES_EMPTY.

### API-12 PATCH /locations/{id}/status
Body `{status, reason?}`. Calls: validateStatusTransition(FN-17), applyStatusChange(FN-18). Errors: 422 NOT_EMPTY (deactivate/decommission with stock), 422 INVALID_TRANSITION, 422 BLOCK_REASON_REQUIRED.

### API-13 PATCH /locations/{id}/reparent
Body `{parent_type, rack_id?, area_id?, migrate?}`. Calls: validateFlexibleParent(FN-13), validateAllowsDirect(FN-14), reparentLocation(FN-19). Errors: 422 SOURCE_NOT_EMPTY.

### API-14 POST /locations/bulk-generate
Body: template spec. Calls: previewBulk(FN-20), generateLocations(FN-21 → ENG-LOC-GEN). Atomic. Errors: 409 CODE_COLLISION, 422 INVALID_TEMPLATE.

### API-15 GET /locations/parents
Query `type=rack|area, zone?`. Active racks / areas(allows_direct=true). Calls: getEligibleParents(FN-22).

## Geo lookup (consume Geo Master, read-only)

### API-20 GET /geo/provinces → `{code,name}[]`. Calls: listGeo(FN-24, 'province').
### API-21 GET /geo/districts?province_code= → `{code,name}[]`. Calls: listGeo(FN-24, 'district').
### API-22 GET /geo/subdistricts?district_code= → `{code,name,postcode}[]`. Calls: listGeo(FN-24, 'subdistrict').

## Request Validation (HTTP, trivial)
enum check level/type/status/parent_type/rotation; capacity_value>0; page bounds → 400 INVALID_PARAM.
