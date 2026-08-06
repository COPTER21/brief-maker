# 03_LOGIC — F-LOCATION-MASTER-001 · Warehouse & Bin

> Audience: BE dev (business logic layer). All non-HTTP logic: functions, state transitions, validations, integrations.
> Convention: Function code = camelCase · Engine code = kebab-case.

---

## §3.1 Functions (Scope-Local)

### WHB-FN-01: createNode
- **Purpose:** สร้าง node (warehouse/zone/area/rack) ใหม่ตาม level
- **Input:** `{ level, fields }` · **Output:** `Node | ValidationError[]`
- **Invoked by:** WHB-API-03 POST /nodes/:level
- **Calls:** WHB-FN-04 (validateNodeUniqueness), WHB-FN-14 (auto postcode for WH)
- **Side effects:** INSERT warehouses/zones/areas/racks; logAudit
- **Iron rule:** ✅ no HTTP terms

### WHB-FN-02: updateNode
- **Purpose:** แก้ไข node; area edit บังคับ BR-007 guard
- **Input:** `{ level, id, fields }` · **Output:** `Node | ValidationError[]`
- **Invoked by:** WHB-API-04 PUT /nodes/:level/:id
- **Calls:** WHB-FN-04, WHB-FN-06 (assertAllowsDirectSafe)
- **Side effects:** UPDATE + logAudit

### WHB-FN-03: archiveNode
- **Purpose:** soft archive node (status→archived) เมื่อไม่มีลูก active (referential-safe, GC#7/D11)
- **Input:** `{ level, id }` · **Output:** `ok | BlockError`
- **Invoked by:** WHB-API-05 POST /nodes/:level/:id/archive
- **Calls:** WHB-FN-05 (countActiveChildren)
- **Side effects:** UPDATE status=archived, archivedAt; logAudit ("จัดเก็บ… active → จัดเก็บแล้ว"). **No DELETE.**

### WHB-FN-04: validateNodeUniqueness
- **Purpose:** code unique — WH system-wide, others within parent (BR-004)
- **Input:** `{ level, code, parentScope }` · **Output:** `bool` · **Invoked by:** FN-01, FN-02
- **Note:** authoritative uniqueness at DB unique index (EC-15 concurrency)

### WHB-FN-05: countActiveChildren
- **Purpose:** referential guard — นับลูก **active เท่านั้น** (archived/decommissioned ไม่ block) — mirrors HTML `childCount` (L3167)
- **Input:** `{ kind, id }` · **Output:** `int` · **Invoked by:** FN-03, view node child stats

### WHB-FN-06: assertAllowsDirectSafe
- **Purpose:** BR-007 — ห้ามปิด allows_direct ถ้ามี direct location อยู่ · BR-003 gate
- **Input:** `{ areaId, newAllowsDirect }` · **Output:** `ok | Block` · **Invoked by:** FN-02, FN-05a(location parent check)

### WHB-FN-07: createLocation
- **Purpose:** สร้าง location (2-step); resolve initial status via barcode gate
- **Input:** `{ parent_type, rack_id|area_id, code, type, cap_uom, cap_val, rotation, flags..., barcode? }` · **Output:** `Location | ValidationError[]`
- **Invoked by:** WHB-API-08 POST /locations
- **Calls:** WHB-FN-04, WHB-FN-06 (allows_direct), WHB-FN-15 (resolveInitialStatus), ENG-HIER-PATH
- **Side effects:** INSERT locations; logAudit
- **Rules:** parent XOR (BR-002), cap_val>0 (BR-006)

### WHB-FN-08: updateLocation / reparentLocation
- **Purpose:** แก้ไข location; ถ้าเปลี่ยน parent และ hasStock≠0 → block (BR-012/AD-5)
- **Input:** `{ id, fields }` · **Output:** `Location | Block` · **Invoked by:** WHB-API-09
- **Calls:** WHB-FN-16 (readHasStock), WHB-FN-04, ENG-HIER-PATH (recompute path → emit location.reparented)

### WHB-FN-09: decommissionLocation
- **Purpose:** soft decommission (status→decommissioned) เมื่อ stock=0 (BR-010)
- **Input:** `{ id }` · **Output:** `ok | Block` · **Invoked by:** WHB-API-12
- **Calls:** WHB-FN-16 (readHasStock) · **Side effects:** UPDATE + logAudit + emit `location.decommissioned`. **No DELETE.**

### WHB-FN-10: setLocationStatus
- **Purpose:** transition 7-state; activate needs barcode (BR-014), block needs reason (BR-013)
- **Input:** `{ id, nextStatus, block_reason? }` · **Output:** `ok | Block` · **Invoked by:** WHB-API-11
- **Calls:** WHB-FN-17 (assertTransitionAllowed) · **Side effects:** UPDATE status(+block_reason) + logAudit

### WHB-FN-11: computeBulkPlan
- **Purpose:** จาก template (rackPat/rackQty/locPat/grid) → รายการ code ที่จะสร้าง + count (thin wrapper over ENG-BULK-PLAN)
- **Input:** template · **Output:** `{ qty, per, total, codes[] }` · **Invoked by:** WHB-API-13 preview, WHB-FN-12
- **Calls:** ENG-BULK-PLAN

### WHB-FN-12: generateLocationsAtomic
- **Purpose:** สร้าง rack+location ทั้งชุดใน transaction เดียว (all-or-nothing, BR-015); collision → rollback
- **Input:** plan · **Output:** `{ created } | CollisionError` · **Invoked by:** WHB-API-14
- **Calls:** ENG-BULK-PLAN (collision detect), WHB-FN-04 · **Side effects:** INSERT (atomic) + logAudit

### WHB-FN-13: switchViewKeepSelection
- **Purpose:** สลับ List ↔ Tree โดยคง `state.sel` (S-10) — shared selection state
- **Input:** `{ targetView }` · **Output:** view state · **Invoked by:** UI setView (P-01/P-02)
- **Note:** UI-layer state coordination (mirrors `setView`/`expandToSel`)

### WHB-FN-14: resolveGeoPostcode + cascadeGeoReset
- **Purpose:** geo cascade — เปลี่ยน province → reset district/subdistrict; auto postcode จาก subdistrict (BR-017)
- **Input:** `{ province, district, subdistrict }` · **Output:** `{ postcode, resetFields[] }` · **Invoked by:** FN-01/FN-02 (WH), UI cascade
- **Source:** mock TH_GEO (AD-1) — `[AI-DEFAULT]` not-found behavior (OQ-4)

### WHB-FN-15: resolveInitialStatus
- **Purpose:** BR-014 — create location: no barcode + `loc_require_barcode` ON → `inactive`, else `active`
- **Input:** `{ barcode, configFlag }` · **Output:** `status` · **Invoked by:** FN-07

### WHB-FN-16: readHasStock
- **Purpose:** อ่าน `hasStock` จาก Inventory runtime (integration; ไม่คำนวณเอง)
- **Input:** `{ location_id }` · **Output:** `bool` · **Invoked by:** FN-08, FN-09 (gate) · **Calls:** WHB-API-17 upstream
- **Note:** integration read (matrix #8-lite) — mock จนกว่า Inventory พร้อม

### WHB-FN-17: assertTransitionAllowed
- **Purpose:** table-driven 7-state machine guard (ห้าม hardcode transition — BRD §14.1)
- **Input:** `{ from, to }` · **Output:** `bool` · **Invoked by:** FN-10, FN-09

### WHB-FN-18: applyTypeDefaults ⚠️ DEFERRED (Phase 3, schema-ready — NOT invoked)
- **Purpose:** (future) type→default behavior flags auto-apply (BR-018/AD-3)
- **Status:** declared as contract only; **no API trace in Phase 1** (intentional, OQ-3). Not an orphan — flagged deferred.

---

## §3.2 Engines (Reusable / CUBIC-Registered)

### ENG-HIER-PATH: hierarchy-path-engine (NEW — reusable candidate)
- **code:** `hierarchy-path-engine` · **category:** master-data-derivation
- **input schema:** `{ location_id | node_ref }`
- **output schema:** `{ full_path: string }`
- **logic outline:**
  1. Walk parent chain L5→L1 (location → rack/area → zone → warehouse)
  2. Render segment: **warehouse = code**, zone/area/rack = **name**, location = **code** (D15)
  3. **Branch NOT included in path** (D15 — reverses D7 path portion)
  4. Join "code › name › name › name › code"
- **Used by:** F-LOCATION-MASTER-001 (this) + downstream Inventory/GR/Picking (contract, §12.1). Reusable → CUBIC register candidate (global id at registration, LD-11).
- **Iron rule:** ✅ pure, no HTTP, no direct DB I/O (receives graph)

### ENG-BULK-PLAN: bulk-generation-planner (NEW)
- **code:** `bulk-generation-planner` · **category:** template-expansion
- **input schema:** `{ target_area, rackPat, rackQty, locPat, rows, cols, levels }`
- **output schema:** `{ qty, per, total, codes[], collisions[] }`
- **logic outline:**
  1. Expand rack template `{n}` × rackQty → rack codes
  2. per-rack location codes = rows × cols × levels (or locPat expansion)
  3. total = qty × per
  4. Detect collisions vs existing codes within parent scope
- **Used by:** WHB-FN-11 preview, WHB-FN-12 generate. Pure (no I/O — receives existing codes).
- **Iron rule:** ✅ pure algorithm, testable

---

## §3.3 API ↔ Logic Trace Table (Phase 3.5 Anchor — R8)

| API | Functions | Engines |
|---|---|---|
| WHB-API-01 GET /warehouses | WHB-FN-05 (childCount for KPI) | — |
| WHB-API-02 GET /nodes/:level | — (read) | — |
| WHB-API-03 POST /nodes/:level | WHB-FN-01, FN-04, FN-14 | — |
| WHB-API-04 PUT /nodes/:level/:id | WHB-FN-02, FN-04, FN-06 | — |
| WHB-API-05 POST …/archive | WHB-FN-03, FN-05 | — |
| WHB-API-06 GET /nodes/:level/:id | WHB-FN-05 | ENG-HIER-PATH |
| WHB-API-07 GET /locations | — (read) | — |
| WHB-API-08 POST /locations | WHB-FN-07, FN-04, FN-06, FN-15 | ENG-HIER-PATH |
| WHB-API-09 PUT /locations/:id | WHB-FN-08, FN-16, FN-04 | ENG-HIER-PATH |
| WHB-API-10 GET /locations/:id | WHB-FN-16 | ENG-HIER-PATH |
| WHB-API-11 PATCH …/status | WHB-FN-10, FN-17 | — |
| WHB-API-12 POST …/decommission | WHB-FN-09, FN-16 | — |
| WHB-API-13 POST /bulk/preview | WHB-FN-11 | ENG-BULK-PLAN |
| WHB-API-14 POST /bulk/generate | WHB-FN-12, FN-04 | ENG-BULK-PLAN |
| WHB-API-15/16/17 references | WHB-FN-14 (geo), FN-16 (stock) | — |
| WHB-API-18 GET /audit/:refId | — (read) | — |

> **R8 check:** ทุก mutation API (03,04,05,08,09,11,12,14) มี ≥1 Function. WHB-FN-18 = deferred (documented, not orphan). No hidden CRUD/calc in 02_API.
