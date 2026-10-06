# 02_API — F-INV-001 Stock by Location

> Audience: BE dev (HTTP layer only — business logic lives in `03_LOGIC.md`)
> Convention: CUBIC API Entity schema (see `references/cubic-schema-templates.md`)

---

## §2.1 API Index

| ID | Method | Path | Purpose | Mutation? |
|---|---|---|---|---|
| API-01 | GET | `/inventory/warehouses` | List warehouses for the Gate page (P-01) | No |
| API-02 | GET | `/inventory/stock/balances` | Aggregated + raw balance list (P-02/P-03), server-side filter/sort/paginate | No |
| API-03 | GET | `/inventory/stock/products/{pid}` | Product-level aggregate for the Product Drawer (D-01) | No |
| API-04 | GET | `/inventory/stock/balances/{balanceId}` | Single balance detail for the Balance Drawer (D-02) | No |
| API-05 | GET | `/inventory/stock/locations/{locId}` | Location contents + metadata for the Location Drawer (D-03) | No |
| API-06 | GET | `/inventory/stock/movements` | Movement timeline (product- or balance-scoped) | No |
| API-07 | GET | `/inventory/stock/uom-locations` | Per-location UoM breakdown for the "ตำแหน่งจัดเก็บ" tab | No |
| API-08 | POST | `/inventory/stock/adjustments` | Submit a Manual Adjustment (multi-line) | **Yes** |
| API-09 | GET | `/inventory/stock/adjustments` | Audit log list (P-06) | No |
| API-10 | GET | `/inventory/stock/adjustments/{id}` | Audit log detail (D-05) | No |
| API-11 | POST | `/inventory/stock/bp-orders` | Create a Break/Pack order | **Yes** |
| API-12 | GET | `/inventory/stock/bp-orders` | List Break/Pack orders (P-04) | No |
| API-13 | GET | `/inventory/stock/bp-orders/{id}` | Break/Pack order detail (D-04) | No |
| API-14 | PATCH | `/inventory/stock/bp-orders/{id}/assign` | Assign/reassign a Break/Pack order | **Yes** |
| API-15 | POST | `/inventory/stock/bp-orders/{id}/complete` | Complete a Break/Pack order (moves real stock) | **Yes** |
| API-16 | POST | `/inventory/stock/bp-orders/{id}/cancel` | Cancel a locked Break/Pack order (releases lock) | **Yes** |
| API-17 | POST | `/inventory/stock/export` | Generate export file (Excel/CSV, filtered/scoped) | No (read-only side effect: writes export log) |

---

## §2.2 Contract Blocks

### API-01 GET `/inventory/warehouses`
- **RBAC:** all roles; `warehouse_staff` should receive only their own scoped warehouse (server
  enforces §0.4 row-scoping — client-side `roleScope()` is not sufficient, PR-3)
- **Response:** `[{ code, name, item_count, location_count }]`
- **Maps to:** P-01 `renderGate()`, `pickWh()`

### API-02 GET `/inventory/stock/balances`
- **Query params:** `warehouse` (required unless caller is `warehouse_staff`), `view`
  (`sku`\|`location`), `search`, `zone`, `location_type`, `status`, `hide_zero` (bool), `flag`
  (`low`\|`neg`), `sort`, `dir`, `page`, `page_size`
- **RBAC:** all roles (read); `warehouse_staff` forced to own warehouse server-side regardless of
  `warehouse` param (mirrors `getFiltered()` L1152 + `skuAgg()` L1221 warehouse-scope guard)
- **Server-side requirement (backend-only, not visible in the mock):** exclude
  `is_stock_item = false` (service items) **at the query level**, not just in application code —
  per OB-3 / comment at L829 ("BACKEND exclude ตั้งแต่ query")
- **Response (view=sku):** `[{ pid, code, name, on_hand_base, allocated_base, available_base,
  location_count, in_transit_base, low, negative, master_inactive, base_uom }]`
- **Response (view=location):** `[{ location_id, code, type, loc_status, util_pct, primary_sku,
  primary_sku_qty }]`
- **Maps to:** `getFiltered()` FN-01, `skuAgg()` FN-04

### API-03 GET `/inventory/stock/products/{pid}`
- **Response:** product master fields (JOINed, read-only here) + aggregated balance summary
  (`on_hand_base`, `allocated_base`, `available_base`, `in_transit_base`, `location_count`,
  `min_stock`, unit conversion chain) — 404 if `pid` does not exist or resolves to a service item
  (`isStockable` guard applies server-side too, not just client routing)
- **Maps to:** D-01 `renderProductDrawer()`

### API-04 GET `/inventory/stock/balances/{balanceId}`
- **Response:** one `RAW` row joined with product + location context — `on_hand`, `allocated`,
  `in_transit`, `status`, `lot`/`serial`/`exp` breakdown (`LOTS`), `received`, `moved`
- **RBAC:** valuation fields (`cost`, computed value) — **NOT included in this response per this
  pack's scope decision (G-01 unresolved).** If OQ-INV-06 is ratified to keep valuation, this
  contract must be revised with an explicit `finance`/`auditor`-gated sub-object, reviewed under
  Security Bible D5, before implementation
- **Maps to:** D-02 `renderDrawer()`/`renderOverviewTab()`

### API-05 GET `/inventory/stock/locations/{locId}`
- **Response:** location metadata (hierarchy path, type, `loc_status`, capacity, utilization) +
  contents array (all balances at this location with `on_hand > 0`, in the location's own unit)
- **404** if `locId` does not belong to the caller's warehouse context
- **Maps to:** D-03 `renderLocationDrawer()`

### API-06 GET `/inventory/stock/movements`
- **Query params:** `pid` (product-scoped, merges across all its balances) OR `balance_id`
  (single-balance-scoped), `limit` (default 30)
- **Response:** `[{ type, qty_base, ref, by, at, location_code }]`, sorted newest-first
- **Maps to:** `renderMovesTab()`, D-01 "การเคลื่อนไหว" tab

### API-07 GET `/inventory/stock/uom-locations`
- **Query params:** `pid`
- **Response:** `{ conversions: [{ unit, factor }], rows: [{ location_code, qty_in_unit, unit,
  allocated_base, free_base, total_base }], grand_total_base, grand_allocated_base }`
- **Maps to:** `renderUomLocTab()` / `bucketsFor()`

### API-08 POST `/inventory/stock/adjustments` — Manual Adjustment
- **RBAC:** `warehouse_staff` OR `finance` only (`canAdjust()`, OB-12). Server MUST re-check this
  at request time, not trust a prior page load (PR-3)
- **Request body:**
  ```json
  {
    "reason": "นับสต็อกประจำงวด (Cycle Count)",
    "note": "string, optional",
    "lines": [
      { "pid": "FG-1001", "location_id": "L003", "direction": "add|reduce", "qty": 5 }
    ],
    "idempotency_key": "required, see 05_RULES EC-INV-04"
  }
  ```
- **Server-side validation (all-or-nothing — a single invalid line rejects the whole batch,
  mirroring `submitAdjust()` L2702-2705):**
  - `reason` required, must be one of the 6 fixed values (`ADJ_REASONS`)
  - No duplicate `(pid, location_id)` pairs within one submission
  - Every line must pass `05_RULES.md` BR-07/BR-08 (location/master state guards, allocated
    ceiling on reduce)
  - `qty` must be a positive integer in the **location's own unit** — server converts to base
    using the same `locUomIdx` resolution as the client (see `03_LOGIC.md ENG-INV-01`)
- **Side effects (single transaction):**
  1. Upsert `T_stock_balance` — update `on_hand` if the `(pid, location_id)` row exists, else
     **create it** (OB-8/S-05b new-balance path)
  2. Append one `T_stock_adjustment_log` header row + N `T_stock_adjustment_log_line` rows
  3. Append N `T_stock_movement` rows (`type='adjustment'`)
- **Response:** `{ adj_doc_no: "ADJ-2026-0036", lines_saved: N }` → drives the toast
- **Errors:** `ERR_REASON_REQUIRED`, `ERR_DUPLICATE_LINE`, `ERR_LINE_INVALID` (with per-line detail
  array), `ERR_PERMISSION_DENIED`, `ERR_IDEMPOTENCY_CONFLICT` (409, PR-7)
- **Maps to:** FN-13..18, `submitAdjust()` L2696

### API-09 GET `/inventory/stock/adjustments`
- **Query params:** `warehouse`, `search`, `direction` (`all`\|`add`\|`reduce`)
- **Response:** `[{ doc_no, at, actor_name, actor_role, reason, line_count, add_base, reduce_base }]`
- **Maps to:** P-06 `renderAdjLogView()`

### API-10 GET `/inventory/stock/adjustments/{id}`
- **Response:** full ADJ document incl. all lines with before/after quantities
- **Maps to:** D-05 `renderAdjDrawer()`

### API-11 POST `/inventory/stock/bp-orders` — Create Break/Pack order
- **RBAC:** same as API-08 (`canAdjust()` scope — Break/Pack is a stock-mutating action)
- **Request body:** `{ pid, type: "break"|"pack", source_location_id, source_qty, target_uom,
  destinations: [{ location_id, qty }] }`
- **Server-side validation:**
  - Source quantity must not exceed available quantity at the source location
  - `target_uom` must be a smaller unit (break) or larger unit (pack) than the source's current unit
  - Destination total base quantity must exactly equal source base quantity (`submitBPOrder()`
    L2336 exact-balance check)
  - No destination may equal the source location
  - At least one destination required
- **Side effects (single transaction):** create `T_bp_order` (`status='locked'`) + increase
  `allocated` on the source balance by the locked base quantity + mark source and all destination
  locations as locked (`LOCKED_LOCS` equivalent — see `03_LOGIC.md` FN-25)
- **Maps to:** FN-23/24, `submitBPOrder()` L2327

### API-12 GET `/inventory/stock/bp-orders`
- **Query params:** `warehouse`, `assignee` (`all`\|`mine`\|`none`\|employee code)
- **Maps to:** P-04 `renderBreakPackView()`

### API-13 GET `/inventory/stock/bp-orders/{id}`
- **Maps to:** D-04 `renderBPDrawer()`

### API-14 PATCH `/inventory/stock/bp-orders/{id}/assign`
- **Request body:** `{ assignee_employee_code }`
- **Constraint:** only while `status = 'locked'`
- **Maps to:** `assignBP()` L2348

### API-15 POST `/inventory/stock/bp-orders/{id}/complete`
- **Constraint:** must have an `assignee` (else `ERR_UNASSIGNED`, mirroring the "กรุณามอบหมายผู้รับผิดชอบก่อน"
  warn toast at L2358)
- **Side effects (single transaction):** decrease source `on_hand`/`allocated` by the locked base
  quantity, increase (or create) destination balances by their base quantities, set order
  `status='done'` + `done_at`, release all location locks
- **Maps to:** FN-26, `completeBPOrder()` L2355

### API-16 POST `/inventory/stock/bp-orders/{id}/cancel`
- **Constraint:** only while `status = 'locked'`
- **Side effects:** release the source `allocated` reservation, release all location locks, remove
  (or soft-cancel) the order
- **Maps to:** `cancelBPOrder()` L2373

### API-17 POST `/inventory/stock/export`
- **RBAC:** `finance` OR `auditor` only (`canExport()`, gated separately from `canValExport()` for
  the `include_valuation` flag — **which per G-01 is not specified further in this pack**)
- **Request body:** `{ scope: "current"|"all", format: "excel"|"csv" }` — **`include_valuation` is
  deliberately omitted from this contract pending OQ-INV-06**
- **Side effect:** writes an export-log entry (per L1373 comment `FN-10 writeExportLog`)
- **Maps to:** `confirmExport()` L1369

---

## §2.3 Cross-Module Contract (PREBRIEF §1 เส้นเข้า/เส้นออก)

### Inbound (this feature reads, config/runtime, no cascade)

| From | What | Direction | Notes |
|---|---|---|---|
| Item Master | `code`, `old_code`, `type`, `uom`, `cost`, `status`, `min_stock` | PULL (per-request JOIN) | `cost` is read but **not surfaced** in any in-scope response per G-01 |
| Location Hierarchy | Warehouse/Zone/Area/Rack/Location tree, `loc_status`, `type`, `cap_uom`/`cap_val` | PULL | Soft reference, no FK cascade (LD-4C-02 pattern) |
| Sales system | `allocated` | PUSH (Sales writes it) | This feature only reads `allocated`, except its own Break/Pack lock write (§ below) |
| GRN | `in_transit`, `received` (FIFO timestamp) | PUSH (GRN writes it) | Read-only here |

### Outbound (other features consume this feature's data — none produced yet)

| To | What | Production status |
|---|---|---|
| Accounting | ADJ log → adjustment value | 🔴 not produced — **and not specified in this pack**, because valuation is the unresolved G-01 gap. No endpoint is defined for this until OQ-INV-06 resolves |
| Purchase | Low-stock signal | 🔴 not produced — **OQ-INV-05** unresolved (notification vs. auto-PR vs. report-only); no endpoint defined |

### Self-referential write (Break/Pack → Sales' `allocated` field)

Break/Pack order creation (API-11) increases `allocated` on the source balance as a locking
mechanism. This is the **one exception** to "allocated is Sales-owned, read-only here" and must be
implemented as an explicit, audited write path — not folded into the general adjustment endpoint.
`05_RULES.md BR-11` documents the rationale and boundary.
