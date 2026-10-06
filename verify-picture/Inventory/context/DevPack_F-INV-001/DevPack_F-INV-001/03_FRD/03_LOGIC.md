# 03_LOGIC — F-INV-001 Stock by Location

> Audience: BE dev (business logic layer)
> Scope: All non-HTTP logic — pure functions, state transitions, calculations, validations

---

## §3.1 Functions (Scope-Local)

### FN-01: buildStockQuery
- **Purpose:** Filter/sort the raw balance set by warehouse scope, zone, location type, status,
  search text, hide-zero toggle
- **Input:** `{ warehouse, filters: {search, zone, ltype, status, hideZero}, sort: {col, dir} }`
- **Output:** `StockBalance[]`
- **Invoked by:** API-02 (view=location branch)
- **Observed as:** `getFiltered()` L1152
- **Side effects:** none (pure read)

### FN-02: computeAvailable
- **Purpose:** `available = on_hand − allocated`
- **Input:** `{ on_hand, allocated }`
- **Output:** `number` (may be negative — EC-INV-05, S-08b by design)
- **Invoked by:** FN-01, FN-04, FN-15 (adjustment ceiling check)
- **Observed as:** `avail()` L1059

### FN-03: isStockable
- **Purpose:** Guard — service-type (`SV`) products must never appear in any list, picker, or
  aggregate on this screen
- **Input:** `Product`
- **Output:** `boolean`
- **Invoked by:** FN-01, FN-04, product picker in Manual Adjustment, Break/Pack product list —
  **every** call site that touches `PRODUCTS`
- **Observed as:** `isStockable()` L830. **Backend requirement (not visible client-side): the
  underlying query must exclude `is_stock_item = false` at the SQL/query level, not filter
  in-application** (per L829 comment) — a defense-in-depth requirement, not merely UI polish
- **Iron rule check:** ✅ no HTTP terms, pure

### FN-04: aggregateByProduct
- **Purpose:** Build the "1 product = 1 row" aggregate (OB-5) — sums `on_hand`/`allocated`/
  `in_transit` across all balances of a product within the warehouse scope, classifies
  low/negative/master-inactive flags
- **Input:** `{ warehouse, filters }`
- **Output:** `[{ pid, on, alloc, transit, locs, av, low, neg, inact, min }]`
- **Invoked by:** API-02 (view=sku branch)
- **Observed as:** `skuAgg()` L1221
- **Calls:** FN-02, FN-03

### FN-05: buildProductCodeChips
- **Purpose:** Render the 2-code reference block (รหัสกลาง + รหัสเก่า) — enforces that only `code`/
  `old_code` are ever surfaced, never a `code_item`/`code_sku` remnant
- **Input:** `Product`
- **Output:** `{ main: code, old: old_code|null }`
- **Invoked by:** D-01/D-02 drawer render
- **Observed as:** `fourCodeChips()` L2572 (name is a naming leftover from a 4-code precedent; the
  implementation itself only ever emits 2 — flagged here so the real build uses a correctly-named
  function, not the observed name verbatim)

### FN-06: resolveRowUnit
- **Purpose:** Resolve which unit a given balance row displays in (the location's own unit, per
  "1 location = 1 UoM"), and compute the on-screen quantity + base-unit-equivalent quantities
- **Input:** `StockBalance` (with resolved `Location`)
- **Output:** `{ unit, factor, baseUom, qty_in_unit, allocated_in_unit, available_in_unit }`
- **Invoked by:** all quantity display paths (list row, overview tab, location contents table)
- **Observed as:** `rowUnit()` L1062
- **Calls:** FN-08 (`convsFor`/`locUomIdx`)

### FN-07: formatQuantityCell
- **Purpose:** Render "N unit" with a base-unit-equivalent sub-label when `factor > 1`
- **Input:** `{ baseVal, resolvedUnit }`
- **Output:** `string` (HTML fragment)
- **Invoked by:** list/table renderers
- **Observed as:** `qtyCell()` L1068

### FN-08: resolveLocationUom
- **Purpose:** Given a product's conversion chain and a location's type, pick the unit that
  location stores in — bulk/reserve/pack/receiving-dock/transit → largest unit; everything else
  (incl. pick-face) → smallest (base) unit
- **Input:** `{ location, conversions[] }`
- **Output:** `index into conversions[]`
- **Invoked by:** FN-06, FN-09 (bucket calc), Manual Adjustment line resolution
- **Observed as:** `locUomIdx()` L1088
- **Business rule encoded:** "1 location = 1 UoM" (OB-4) — this function is the single source of
  truth for that mapping and **must not be duplicated** elsewhere

### FN-09: checkLowStock
- **Purpose:** Compare a product's available quantity (per warehouse scope) against its
  `min_stock` threshold from Item Master
- **Input:** `{ available, min_stock }` (nullable `min_stock` = not checked)
- **Output:** `boolean`
- **Invoked by:** FN-04
- **Observed as:** inline in `skuAgg()` L1233: `(p.min_stock>0) && av<p.min_stock`

### FN-10: mergeProductMovements
- **Purpose:** Merge the movement timelines of all balances belonging to a product, tag each entry
  with its originating location, sort newest-first, cap at 30
- **Input:** `pid`
- **Output:** `Movement[]` (each with `_loc` tag)
- **Invoked by:** D-01 "การเคลื่อนไหว" tab
- **Observed as:** inline in `renderProductDrawer()` L1919 + `getMoves()` L1129

### FN-11: computeLocationUtilization
- **Purpose:** Resolve a location's utilization percentage and health classification
- **Input:** `Location`
- **Output:** `{ util_pct, health: 'empty'|'occupied'|'full'|'blocked' }`
- **Invoked by:** P-03 list, D-03 drawer
- **Observed as:** `locUtil()` L984, `locHealth()` L985, `utilClass()` L992

### FN-12: getLocationContents
- **Purpose:** List all balances physically present at a location (`on_hand > 0`), in the
  location's own unit
- **Input:** `location_id`
- **Output:** `StockBalance[]` (with FN-06 resolution applied per row)
- **Invoked by:** D-03 Location Drawer
- **Observed as:** `balancesAtLoc()` L973, consumed in `renderLocationDrawer()` L1859

### FN-13: buildAdjustmentLineContext
- **Purpose:** Resolve a Manual Adjustment line's full computed context — target unit/factor,
  existing balance (or none = new balance), current/allocated quantities, max-reduce ceiling,
  projected after-quantity
- **Input:** `{ pid, loc, dir, qty }` (one adjustment line)
- **Output:** `{ l, c, row, q, base, on, al, cur_n, maxRed, after, after_n }`
- **Invoked by:** FN-14, FN-15, FN-16, FN-18
- **Observed as:** `adjLineInfo()` L2588
- **Calls:** FN-08

### FN-14: renderAdjustmentLine
- **Purpose:** Render one line of the Manual Adjustment grid — product/location comboboxes,
  direction toggle, quantity input, live before→after preview, inline error
- **Input:** `{ line, index }`
- **Output:** HTML fragment
- **Invoked by:** P-05 modal body
- **Observed as:** `adjLineHTML()` L2612
- **Calls:** FN-13, FN-15

### FN-15: validateAdjustmentLine
- **Purpose:** Full per-line validation gate — see `05_RULES.md BR-07/BR-08` for the complete rule
  set (location lock, location/master status, service-item block, quantity format, allocated
  ceiling on reduce)
- **Input:** one adjustment line
- **Output:** `string | null` (error message, or null = valid)
- **Invoked by:** FN-14 (live), API-08 submit gate (server-side, authoritative)
- **Observed as:** `adjLineError()` L2598
- **Calls:** FN-13, FN-03, FN-08

### FN-16: computeAdjustmentPreview
- **Purpose:** Compute the "ปัจจุบัน N → หลังปรับ M" (or "รายการใหม่ · ปัจจุบัน 0 → N") preview text
- **Input:** adjustment-line context (FN-13 output)
- **Output:** `string`
- **Invoked by:** FN-14
- **Observed as:** inline in `adjLineHTML()` L2646-2648

### FN-17: detectNewBalanceLine
- **Purpose:** Identify whether an adjustment line targets a `(pid, loc)` pair with no existing
  balance row — if so, the line creates a new balance on submit (OB-8/S-05b)
- **Input:** adjustment-line context
- **Output:** `boolean` (`isNew`)
- **Invoked by:** FN-14, FN-18
- **Observed as:** `const isNew = inf && !inf.row;` L2633

### FN-18: submitAdjustmentBatch
- **Purpose:** Validate the full batch (all lines, no duplicate `(pid,loc)` keys), then atomically
  upsert balances, append one ADJ document with all lines, and append one movement record per line
- **Input:** `{ reason, note, lines[] }`
- **Output:** `{ adj_doc_no, lines_saved }`
- **Invoked by:** API-08
- **Observed as:** `submitAdjust()` L2696
- **Calls:** FN-13, FN-15 (re-validated server-side, authoritative), FN-17, ENG-INV-03
  `recordAuditEntry`
- **Side effects:** INSERT/UPDATE `T_stock_balance`, INSERT `T_stock_adjustment_log` (+lines),
  INSERT `T_stock_movement` (×N)

### FN-19: canAdjust
- **Purpose:** RBAC gate — only `warehouse_staff` or `finance` may open/submit Manual Adjustment or
  Break/Pack mutations
- **Input:** current role
- **Output:** `boolean`
- **Invoked by:** every mutation entry point (UI gating) AND API-08/API-11/API-14/API-15/API-16
  (server-side, authoritative — **must be re-checked at request time, not just page-load time**,
  PR-3)
- **Observed as:** `canAdjust()` L1032

### FN-20: manageOverlayPortal
- **Purpose:** Move an opened dropdown panel to a document-level portal container, position it via
  `getBoundingClientRect()`, flip up on bottom-edge collision, restore it to its home wrapper on
  close; close-all is invoked on any outside click and as the first stage of the Esc chain
- **Input:** dropdown key
- **Output:** none (DOM side effect)
- **Invoked by:** every search-combobox (product/location/assignee pickers)
- **Observed as:** `ddTog()`/`ddCloseAll()`/`ddRestore()`/`ddFil()` L2241-2292
- **Iron rule check:** ✅ implements Rule #95 Overlay Portal + the two-stage Esc chain (OB-9)

### FN-21: syncRouteToState
- **Purpose:** Single reconciliation point between the URL hash and application state — resolves
  warehouse context, view, and drawer open/closed/which-record on every navigation and on page load
- **Input:** `location.hash`
- **Output:** mutates `state` (route, warehouse context, drawer)
- **Invoked by:** `hashchange` listener + initial load
- **Observed as:** `syncRouteToState()` L1275
- **Note for BE:** this is a pure FE routing concern; documented here because it is the mechanism
  that makes every drawer route refresh-safe, which `01_UI.md §1.1` depends on

### FN-22: applyListFilters
- **Purpose:** Search/hide-zero/quick-flag filter application + reset, shared shape across P-02
- **Input:** filter key/value
- **Output:** mutates filter state, resets to page 1
- **Invoked by:** P-02 filter bar
- **Observed as:** `applyFilter()`/`toggleHideZero()`/`resetFilters()`/`quickFlag()` L1216-1219

### FN-23: buildBreakPackCandidates
- **Purpose:** List eligible source locations (has available stock) and eligible unit-conversion
  targets (break = smaller unit, pack = larger unit) for a chosen product
- **Input:** `{ pid, type: 'break'|'pack' }`
- **Output:** `{ sourceLocations[], targetUnitOptions[] }`
- **Invoked by:** M-02 Break/Pack create modal
- **Observed as:** `bpLocsWithStock()` L2219, `bpTargetOpts()` L2231

### FN-24: validateBreakPackOrder
- **Purpose:** Validate a Break/Pack order before creation — source quantity within available,
  target unit chosen, destination total base quantity exactly equals source base quantity, no
  destination equals source
- **Input:** BP form state
- **Output:** `string | null`
- **Invoked by:** FN-25 (pre-submit gate), API-11 (server-side, authoritative)
- **Observed as:** inline validation in `submitBPOrder()` L2329-2337

### FN-25: submitBreakPackOrder
- **Purpose:** Create the order, lock the source+destination locations, and reserve
  (`allocated += locked_base`) the source quantity — all in one transaction
- **Input:** validated BP form state
- **Output:** `BPOrder`
- **Invoked by:** API-11
- **Observed as:** `submitBPOrder()` L2327
- **Calls:** FN-24
- **Side effects:** INSERT `T_bp_order`, UPDATE `T_stock_balance.allocated` (source), locks 1+N
  locations

### FN-26: completeBreakPackOrder
- **Purpose:** Execute the actual stock move — decrease source, increase (or create) destination
  balances, mark order done, release all locks
- **Input:** `order_id`
- **Output:** updated order + updated balances
- **Invoked by:** API-15
- **Observed as:** `completeBPOrder()` L2355
- **Precondition:** order must have an assignee (`ERR_UNASSIGNED` otherwise)

### FN-27: buildAuditLogQuery
- **Purpose:** Filter the ADJ log by warehouse (any line touching a location in that warehouse),
  search text, and direction
- **Input:** `{ warehouse, filters }`
- **Output:** `AdjDocument[]`
- **Invoked by:** API-09
- **Observed as:** `renderAdjLogView()` filter block L2738-2746

---

## §3.2 Engines (Reusable / CUBIC-Registered)

### ENG-INV-01: unit-conversion-engine (NEW)
- **code:** `unit-conversion-engine`
- **name:** Stock Unit Conversion Engine
- **category:** inventory-calculation
- **input schema:** `{ pid: string, location: Location, conversions: [{unit: string, factor: number}] }`
- **output schema:** `{ resolvedUnit: string, factor: number, baseUom: string,
  toBase(qtyInUnit) -> number, fromBase(qtyInBase) -> number }`
- **logic outline:**
  1. Look up the product's conversion chain (largest → smallest unit, factor 1 = base)
  2. Resolve which unit the given location stores in, per location `type` (FN-08)
  3. Expose bidirectional conversion helpers so every screen (list, drawers, adjustment, break/pack)
     uses one authoritative conversion path
- **Used by features:** F-INV-001 only currently (single-warehouse stock); candidate for reuse by
  any future feature that displays quantities in a location-specific unit (e.g. Putaway, Picking)
- **Iron rule check:** ✅ pure, no HTTP, no direct DB I/O — reusable
- **Observed as:** `convsFor()` L1086, `locUomIdx()` L1088, `bucketsFor()` L1096

### ENG-INV-02: adjustment-ceiling-engine (NEW)
- **code:** `adjustment-ceiling-engine`
- **name:** Stock Adjustment Ceiling Validation Engine
- **category:** inventory-validation
- **input schema:** `{ line: {pid, loc, dir, qty}, currentBalance: {on_hand, allocated} | null,
  locationState: {loc_status}, productState: {status} }`
- **output schema:** `{ valid: boolean, errorCode: string | null, maxReduceQty: number }`
- **logic outline:**
  1. Reject if location is locked by an active Break/Pack order
  2. Reject if location status is blocked/frozen/inactive/maintenance/decommissioned
  3. Reject `add` direction if the product master is inactive (reduce is still allowed, to let
     stock be cleared out)
  4. Reject non-positive/non-integer quantities
  5. On `reduce`, compute `maxReduce = floor(max(0, on_hand − allocated) / factor)` and reject if
     the requested quantity exceeds it — **allocated is never touched by this engine, only read**
- **Used by features:** F-INV-001 (Manual Adjustment). This is the formal encoding of OB-11's
  "allocated แตะไม่ได้" rule and should be the single place that rule is enforced server-side
- **Iron rule check:** ✅ pure, no HTTP — reusable as the authoritative ceiling check wherever
  stock is manually reduced
- **Observed as:** `adjLineError()` L2598-2610

### ENG-INV-03: audit-log-engine (NEW)
- **code:** `stock-audit-log-engine`
- **name:** Append-Only Stock Audit Log Engine
- **category:** compliance/audit
- **input schema:** `{ actor: {name, role}, reason: string, note: string, lines: AdjLine[] }`
- **output schema:** `{ doc_no: string, entries_written: number }`
- **logic outline:**
  1. Generate the next sequential document number (`ADJ-YYYY-NNNN`)
  2. Persist one header row + N line rows in a single append (`INSERT`/`unshift` only — **no
     UPDATE or DELETE path may ever exist against this table**, per OB-11)
  3. Cross-link each line to its corresponding `T_stock_movement` entry
- **Used by features:** F-INV-001 (Manual Adjustment). Same append-only shape as Break/Pack's own
  movement trail — candidate for a shared cross-feature audit-log engine if a second feature needs
  identical guarantees
- **Iron rule check:** ✅ pure business logic (the actual persistence is a thin wrapper in
  `03_LOGIC` FN-18/API-08) — no HTTP terms in the decision logic itself
- **Observed as:** `ADJLOG.unshift(batch)` L2727 — confirmed no `splice`/`delete` exists anywhere
  against `ADJLOG` in the file

---

## §3.3 API ↔ Logic Trace Table (Phase 3.5 Anchor)

| API | Calls Functions | Calls Engines |
|---|---|---|
| API-02 GET balances | FN-01, FN-04, FN-02, FN-03 | ENG-INV-01 |
| API-03 GET product | FN-04, FN-05, FN-09 | ENG-INV-01 |
| API-04 GET balance | FN-06, FN-07 | ENG-INV-01 |
| API-05 GET location | FN-11, FN-12, FN-06 | ENG-INV-01 |
| API-06 GET movements | FN-10 | — |
| API-07 GET uom-locations | — | ENG-INV-01 |
| API-08 POST adjustments | FN-13, FN-15, FN-17, FN-18, FN-19 | ENG-INV-01, ENG-INV-02, ENG-INV-03 |
| API-09 GET adjustments (list) | FN-27 | — |
| API-10 GET adjustments/{id} | — | — |
| API-11 POST bp-orders | FN-23, FN-24, FN-25, FN-19 | ENG-INV-01 |
| API-14 PATCH bp-orders/assign | — | — |
| API-15 POST bp-orders/complete | FN-26 | ENG-INV-01 |
| API-16 POST bp-orders/cancel | — | — |
| API-17 POST export | — | — |

> **Iron Rule R8 check:** every mutation API (API-08, API-11, API-14, API-15, API-16) has ≥ 1
> Function/Engine in this table. No orphan Function/Engine — FN-20 (portal), FN-21 (routing), FN-22
> (filters) are FE-concern functions documented here for completeness but are not server-invoked;
> they are anchored to `01_UI.md` instead of an API row, which is expected for pure-client
> functions and does not violate R8 (R8 governs **mutation APIs**, not every function).
