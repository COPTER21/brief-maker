# 02_API — F-LOCATION-MASTER-001 · Warehouse & Bin

> Audience: BE dev (HTTP layer only). Business logic → 03_LOGIC. All mutations = RBAC-gated + WORM audit + IDOR check on id.
> Convention: path `/api/v1/...`, field_key snake_case, error UPPER_SNAKE, status snake_case past-tense.
> Node endpoints are level-parameterized (`:level` ∈ warehouse|zone|area|rack) — mirrors single `submitNode`/`askDeleteNode` in HTML.

---

## §2.1 Node — read
### WHB-API-01 · GET /warehouses — root list + KPI + branch filter
- Query: `branch_id?`, `q?`, `page?`, `size?`
- Returns: `{ rows:[{id,code,name,branch_id,status,childCount}], kpi:{warehouse,zone,area,rack,location}, page }`
- Roles: all (view). Filter branch = UX only, not security scope (D8).

### WHB-API-02 · GET /nodes/:level — drill children
- `:level` zone|area|rack. Query: `parent_id` (warehouse_id/zone_id/area_id). area+`allows_direct` → also returns direct locations (areaTab).
- Returns list rows per level (columns per §renderTableHead).

### WHB-API-06 · GET /nodes/:level/:id — view node
- Returns `{ fields, full_path, childStats:{...} }`. `full_path` from ENG-HIER-PATH.

## §2.2 Node — mutations
### WHB-API-03 · POST /nodes/:level — create node
- Body (warehouse): `{code,name,branch_id,addr_line?,province?,district?,subdistrict?,postcode?}`
- Body (zone): `{code,name,warehouse_id,temp_controlled,temp_min?,temp_max?}`
- Body (area): `{code,name,zone_id,allows_direct}`
- Body (rack): `{code,name,area_id,rows,cols,levels}`
- 201 → toast "สร้าง{คลัง|โซน|พื้นที่|ชั้นวาง} \"{code}\" สำเร็จ"
- Errors: `MISSING_REQUIRED` (400, "กรุณากรอกข้อมูลให้ครบถ้วน"), `BRANCH_REQUIRED` (400, "กรุณาเลือกสาขา"), `DUPLICATE_CODE` (409 — WH "รหัสซ้ำในระบบ" / zone "…ภายในคลังเดียวกัน" / area "…ภายในโซนเดียวกัน" / rack "…ภายในพื้นที่เดียวกัน"), `TEMP_RANGE_INVALID` (400, "อุณหภูมิต่ำสุดต้องไม่เกินสูงสุด" / "กรุณากรอกช่วงอุณหภูมิ")

### WHB-API-04 · PUT /nodes/:level/:id — update node
- 200 → "บันทึกการแก้ไขแล้ว". Errors as create + `ALLOWS_DIRECT_HAS_CHILDREN` (409, area only — "ปิด allows_direct ไม่ได้ — ยังมีตำแหน่งวางตรงอยู่ {n} รายการ", BR-007/EC-08).

### WHB-API-05 · POST /nodes/:level/:id/archive — soft archive
- Referential-safe: **active children block** (BR-005). Success → status `archived` + audit; NO hard delete (GC#7/D11).
- 200 → "จัดเก็บ{lbl}แล้ว"
- Errors: `HAS_ACTIVE_CHILDREN` (409 — "จัดเก็บไม่ได้ — ยังมีรายการลูกใช้งานอยู่ {n} รายการ" + level msg), `FORBIDDEN_ROLE` (403 — del=Manager/Admin only, SoD)

## §2.3 Location — read
### WHB-API-07 · GET /locations — list under rack/area + type/status filter
- Query: `rack_id?`|`area_id?`, `type?`, `status?`, `q?`, page. Roles: all.
### WHB-API-10 · GET /locations/:id — view (3 tabs data)
- Returns overview + capacity/flags + audit history + `hasStock` (runtime Inventory read) + `full_path`.

## §2.4 Location — mutations
### WHB-API-08 · POST /locations — create (2-step payload)
- Body: `{parent_type, rack_id|area_id, code, name?, type, cap_uom, cap_val, rotation, coords?, pickable,putawayable,replenishable, mixed_lot,mixed_item,neg_stock, barcode?, qr?}`
- Server resolves initial status: no barcode + `loc_require_barcode` ON → `inactive` (BR-014).
- 201 → "สร้างตำแหน่ง \"{code}\" สำเร็จ" (+ " (ปิดใช้ — ต้องเพิ่มบาร์โค้ดก่อนเปิดใช้งาน)" if inactive)
- Errors: `PARENT_XOR_VIOLATION` (400, BR-002), `ALLOWS_DIRECT_REQUIRED` (400 — "พื้นที่นี้ allows_direct = false — เลือกพื้นที่อื่น หรือเพิ่มชั้นวางก่อน", BR-003), `CAPACITY_INVALID` (400, "ความจุต้องมากกว่า 0", BR-006), `DUPLICATE_CODE` (409, "รหัสซ้ำภายใน parent เดียวกัน"), `MISSING_REQUIRED` (400)

### WHB-API-09 · PUT /locations/:id — update / reparent
- Reparent guard: if new parent ≠ old AND `hasStock` → block (BR-012/AD-5). Errors: `REPARENT_STOCK_NOT_EMPTY` (409, "ต้องย้ายสต็อกออกก่อนย้ายตำแหน่ง (stock = 0)"), + create errors. 200 → "บันทึกการแก้ไขแล้ว".

### WHB-API-11 · PATCH /locations/:id/status — change status
- Body: `{status ∈ active|blocked|frozen|maintenance|full, block_reason?}`. 
- Gates: activate needs barcode if `loc_require_barcode` ON (BR-014) → `BARCODE_REQUIRED` (409, "ต้องเพิ่มบาร์โค้ดก่อนถึงจะเปิดใช้งานตำแหน่งได้"); block needs reason → `BLOCK_REASON_REQUIRED` (400, "ระบุเหตุผลที่บล็อก", BR-013).
- 200 → "เปลี่ยนสถานะเป็น \"{label}\" แล้ว" / "บล็อกตำแหน่งแล้ว". Roles: status ≠ Operator.

### WHB-API-12 · POST /locations/:id/decommission — soft decommission
- Gate: `hasStock` → block (BR-010). Success → status `decommissioned` (terminal, soft) + audit. NO hard delete.
- 200 → "ปลดระวางตำแหน่งแล้ว". Errors: `DECOMMISSION_STOCK_NOT_EMPTY` (409, "ต้องย้ายสต็อกออกก่อน … (BR-010)"), `FORBIDDEN_ROLE` (403).

## §2.5 Bulk Generate
### WHB-API-13 · POST /locations/bulk/preview — plan + collision
- Body: `{target_area, rackPat, rackQty, locPat, rows, cols, levels, cap_uom, cap_val, ...}`
- Returns `{ qty, per, total, collisions:[codes] }` (ENG-BULK-PLAN). No writes.
### WHB-API-14 · POST /locations/bulk/generate — atomic
- **Single transaction, all-or-nothing** (BR-015). Precheck collisions; any collision → 409 rollback. Recommend idempotency key (Phase 2.5 PR-7, `[AI-DEFAULT]`).
- 200 → "สร้าง {N} ชั้นวาง × {M} ตำแหน่งสำเร็จ (atomic)". Errors: `BULK_TEMPLATE_INVALID` (400, "ไม่สามารถสร้างได้ — ตรวจแม่แบบ/รหัสชน"), `BULK_COLLISION` (409), `CAPACITY_INVALID` (400, "ความจุต้องมากกว่า 0").

## §2.6 Reference (read-only, mock — Phase 2 real)
### WHB-API-15 · GET /branches — mock branch list (AD-6, soft-ref source)
### WHB-API-16 · GET /geo?level=provinces|districts|subdistricts&parent=… + postcode resolve — geo cascade (mock TH_GEO, AD-1)
### WHB-API-17 · GET /locations/:id/stock — hasStock passthrough (Inventory runtime read; gate source for BR-010/BR-012)

## §2.7 Audit
### WHB-API-18 · GET /audit/:refId — WORM trail (append-only, read-only)

---

## §2.9 Cross-Module Contract (from BRD §12.1 — Value Stream, R12)
| Consumer (downstream) | Contract | Trigger |
|---|---|---|
| Inventory (on-hand) | `location_id` + `full_path` (WH code › zone/area/rack name › location code — **no branch**, D15) | location active |
| GR / Put Away / Picking / RTV / Stock Adj / Transfer / Stocktake | `location_id` + `type` enum + `full_path` | อ้างตำแหน่ง |
| **Events emitted:** | `location.decommissioned {location_id}` · `location.reparented {location_id, old_path, new_path}` · `location.blocked/frozen {location_id, status}` | downstream gates หยิบ/วาง; must re-read cached path (EC-18) |
| ENG-HIER-PATH | reusable full-path builder (03_LOGIC §3.2) | render/export |

> **Cross-module edge:** decommission/reparent ต้อง `stock=0` ก่อน → กัน orphan stock (BR-010/BR-012). Downstream ที่ cache `full_path` ต้อง re-read เมื่อ parent เปลี่ยนชื่อ (EC-18 → test 06_TESTS §6.9).
