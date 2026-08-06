# 03_LOGIC — F-LOCATION-MASTER-001 (v2 · Functions + Engines + Trace)

> Audience: BE dev (business logic layer). All non-HTTP logic.

## §3.1 Functions (Scope-Local)

### Hierarchy node (generic, `{level}` = warehouse/zone/area/rack)
- **FN-01 buildNodeQuery** — filters (parent_id/q/status/sort) → query for children of a level. Invoked: API-01.
- **FN-02 buildHierarchyPath** — สร้าง full path "WH › Zone › Area › [Rack ›] node". Invoked: API-01/02. → ENG-HIER-PATH.
- **FN-03 getNode** — fetch single node + child counts. Invoked: API-02.
- **FN-04 validateNodeParent** — parent FK active + code unique within parent. Invoked: API-03/04. Side: none (read).
- **FN-05 createNode** — INSERT node (per-level fields) + audit. Invoked: API-03. Side: write + audit.
- **FN-06 updateNode** — UPDATE attrs + audit. Invoked: API-04. Side: write + audit.
- **FN-07 validateNodeDeletable** — assert no children (zones/areas/racks/locations under node). Invoked: API-05.
- **FN-08 deleteNode** — DELETE node (hard, only if FN-07 passes) + audit. Invoked: API-05. Side: write + audit.
- **FN-09 validateZoneTemp** — ถ้า temp_controlled=true → temp_min/max required + min≤max. Invoked: API-03/04 (zones).
- **FN-10 validateAreaDirectToggle** — block ปิด allows_direct_location เมื่อยังมี direct locations อยู่ (EC-14). Invoked: API-04 (areas).

### Location-specific
- **FN-13 validateFlexibleParent** — บังคับ rack XOR area (mirror DB CHECK); reject both/neither. Invoked: API-10/11/13. ⭐
- **FN-14 validateAllowsDirect** — parent=area → area.allows_direct_location must true. Invoked: API-10/13. ⭐
- **FN-15 createLocation** — INSERT + audit. Invoked: API-10.
- **FN-16 updateLocation** — UPDATE attrs + audit. Invoked: API-11.
- **FN-17 validateStatusTransition** — ตรวจ transition (state machine) + empty check (deactivate/decommission) + block_reason required (→blocked). Invoked: API-12.
- **FN-18 applyStatusChange** — UPDATE status + reason + audit. Invoked: API-12.
- **FN-19 reparentLocation** — ตรวจ source empty/migrate → re-point FK + audit old→new path. Invoked: API-13.
- **FN-20 previewBulk** — คำนวณจำนวน rack×location + collision check (ไม่ persist). Invoked: API-14.
- **FN-21 generateLocations** — เรียก ENG-LOC-GEN, atomic insert. Invoked: API-14.
- **FN-22 getEligibleParents** — active racks / areas(allows_direct=true). Invoked: API-15.
- **FN-23 applyTypeDefaults** ⭐ — map location `type` → default behavior flags (เช่น PACK ⇒ pickable=false, putawayable=false, work-location; PICK_FACE ⇒ pickable+replenishable; HOLD/DAMAGED ⇒ not pickable). Invoked: API-10 (create). *Phase 3 — Phase 1 = manual flags (OQ-3).*

### Geo
- **FN-24 listGeo(level, parent_code)** — proxy read-only lookup ไป Geo Master (provinces / districts by province / subdistricts+postcode by district). Invoked: API-20/21/22.

## §3.2 Engines (Reusable / CUBIC)

### ENG-LOC-GEN: location-generation-engine
- category: master-data-generation
- input: `{ area_id|rack_id, rack_template{pattern,qty,rows,cols,levels}, location_template{pattern,type,capacity_uom,capacity_value,rotation} }`
- output: `{ generated: Location[], rack_count, location_count }`
- logic: expand templates → render codes ({rack}/{r}/{c}/{l}/{n}) → dedupe/collision check → build rows. **Pure, no HTTP.**
- used by: F-LOCATION-MASTER (bulk-gen, warehouse-setup wizard).

### ENG-HIER-PATH: hierarchy-path-builder
- input `{ node|location }` → output `full_path` string (WH › Zone › Area › [Rack ›] node). **Pure.** Reusable by Stock/GRN/Putaway displays.

## §3.3 API ↔ Logic Trace
| API | Functions | Engines |
|---|---|---|
| API-01 GET /hierarchy/{level} | FN-01, FN-02 | ENG-HIER-PATH |
| API-02 GET /hierarchy/{level}/{id} | FN-03, FN-02 | ENG-HIER-PATH |
| API-03 POST /hierarchy/{level} | FN-04, FN-09 | — |
| API-04 PUT /hierarchy/{level}/{id} | FN-04, FN-10, FN-06 | — |
| API-05 DELETE /hierarchy/{level}/{id} | FN-07, FN-08 | — |
| API-10 POST /locations | FN-13, FN-14, FN-23, FN-15 | — |
| API-11 PUT /locations/{id} | FN-13, FN-16 | — |
| API-12 PATCH /locations/{id}/status | FN-17, FN-18 | — |
| API-13 PATCH /locations/{id}/reparent | FN-13, FN-14, FN-19 | — |
| API-14 POST /locations/bulk-generate | FN-20, FN-21 | ENG-LOC-GEN |
| API-15 GET /locations/parents | FN-22 | — |
| API-20 GET /geo/provinces | FN-24 | — |
| API-21 GET /geo/districts | FN-24 | — |
| API-22 GET /geo/subdistricts | FN-24 | — |

> Missing FN-03 createNode? No — FN-05 createNode covers POST. (FN numbering keeps location block 13+ aligned with v1.)
> **R8:** every mutation API (POST/PUT/PATCH/DELETE) traces ≥1 Function. No orphan Functions/Engines.
