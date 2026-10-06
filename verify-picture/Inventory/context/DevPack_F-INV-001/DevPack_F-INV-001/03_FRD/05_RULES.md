# 05_RULES — F-INV-001 Stock by Location

> Audience: BE dev + QA

---

## §5.1 Business Rules (BR-01..BR-11)

### BR-01 — 2-code model only
**Statement:** Every product reference on this screen shows exactly `code` (รหัสกลาง) and
`old_code` (รหัสเก่า, nullable) — `code_item`/`code_sku` must never appear.
**Enforcement point:** `04_DB.md T_product` field shape (external master, but this feature must
never introduce a 3rd/4th code column of its own); `03_LOGIC.md` FN-05.
**Error code:** n/a (a display-shape rule, not a runtime validation).
**Scenario:** S-01, OB-2.

### BR-02 — Service-item exclusion
**Statement:** Products of `type = 'SV'` must never carry a stock balance, and must never appear
in any list, picker, aggregate, or export on this screen — even if a stale/dirty balance record
somehow exists for one.
**Enforcement point:** `isStockable()` guard (FN-03) at **every** read path client-side, AND at the
query level server-side (`is_stock_item = false` excluded from source — this is a backend-only
requirement not observable in the client mock, per L829 comment).
**Error code:** `ERR_SERVICE_ITEM_NOT_STOCKABLE` (if a mutation is attempted against one anyway).
**Scenario:** S-09, OB-3.

### BR-03 — One location, one unit of measure
**Statement:** A given location always stores exactly one UoM at a time. `on_hand`/`allocated` in
the DB are always base units; the UI/API display in the location's own unit, with the base-unit
equivalent shown whenever `factor > 1`.
**Enforcement point:** `ENG-INV-01 unit-conversion-engine`, `FN-06`/`FN-08`.
**Scenario:** S-02, S-03, OB-4. **Open question on rule ownership:** OQ-INV-03 (when/who may
change a location's unit) is unresolved — this rule describes current runtime behavior, not the
governance of changing it.

### BR-04 — Product-level list aggregation
**Statement:** The "by product" list view always shows exactly 1 row per product (aggregated
across all its balances in base units) — never a per-UoM or per-location breakdown at that level,
and never a "total on-hand across units" statistic that would sum incompatible units.
**Enforcement point:** `FN-04 aggregateByProduct`.
**Scenario:** S-01, OB-5.

### BR-05 — Low stock threshold
**Statement:** A product is "low stock" (badge: ต้องเติม) when its `min_stock` (from Item Master,
nullable) is set AND its available quantity (warehouse-scoped) is below that threshold.
**Enforcement point:** `FN-09 checkLowStock`.
**Scenario:** S-08, OB-6. **Open question:** OQ-INV-02 (is `min_stock` per-item or
per-item-per-warehouse?) — this rule currently compares against the currently-open warehouse's
available quantity against one global threshold value, which is the behavior as built, pending
that question's resolution.

### BR-06 — 3-value list status vocabulary
**Statement:** The list view's stock-status column shows exactly one of 3 short labels — ปกติ
(normal), ต้องเติม (low, per BR-05), ขาดสต็อก (negative, per BR-XX below) — mutually exclusive,
with negative taking priority over low. Per-row detail statuses (available/damaged/blocked/
quarantine) are reserved for drawer-level display only.
**Enforcement point:** inline classification in `FN-04`.
**Scenario:** S-01, OB-7.

### BR-07 — Manual Adjustment: create-new-balance-in-empty-location
**Statement:** A Manual Adjustment line targeting a `(product, location)` pair with no existing
balance is valid (provided the location itself is not locked/blocked/frozen and the product is
addable) and creates a new balance record on submit, starting from an implicit 0.
**Enforcement point:** `FN-17 detectNewBalanceLine` + `FN-18 submitAdjustmentBatch` (upsert path).
**Scenario:** S-05, S-05b, OB-8.

### BR-08 — Manual Adjustment: location/master readiness + allocated ceiling
**Statement:** A line is rejected if: (a) its location is currently locked by an active Break/Pack
order; (b) its location status is blocked/frozen/inactive/maintenance/decommissioned; (c) it is an
`add` against an inactive product master (reduce is still allowed, to clear out stock); (d) its
quantity is not a positive integer; (e) on `reduce`, the requested base quantity exceeds
`on_hand − allocated` — **allocated is never touched by this rule, only read as a ceiling.** Any
single invalid line blocks the entire batch submission (no partial commit).
**Enforcement point:** `ENG-INV-02 adjustment-ceiling-engine`, `FN-15 validateAdjustmentLine`,
re-verified server-side in API-08 (client-side validation is advisory only).
**Error codes:** `ERR_LOCATION_LOCKED`, `ERR_LOCATION_UNAVAILABLE`, `ERR_MASTER_INACTIVE_ADD`,
`ERR_QTY_INVALID`, `ERR_EXCEEDS_ALLOCATED_CEILING` (message must state the max-reduce quantity, per
the verbatim HTML copy in `06_TESTS.md`).
**Scenario:** S-06, S-07, OB-11.

### BR-09 — Append-only audit
**Statement:** Every Manual Adjustment submission creates exactly one ADJ document (with N lines)
and N movement entries; no ADJ document or line, once created, may ever be edited or deleted by
any application role.
**Enforcement point:** `ENG-INV-03 audit-log-engine`; `04_DB.md §4.7` DB-permission-level
enforcement (defense in depth beyond just omitting the endpoint).
**Scenario:** S-12, OB-11.

### BR-10 — RBAC on stock mutation
**Statement:** Only `warehouse_staff` and `finance` roles may open or submit Manual Adjustment or
Break/Pack mutations. All other roles (`inventory_viewer`, `procurement`, `auditor`) see no such
entry point anywhere on screen, and any attempt to invoke the mutation directly is rejected
server-side.
**Enforcement point:** `FN-19 canAdjust`, re-checked server-side on every mutation endpoint
(API-08, API-11, API-14, API-15, API-16) — not merely at page load (PR-3).
**Error code:** `ERR_PERMISSION_DENIED`.
**Scenario:** S-10, OB-12.

### BR-11 — Break/Pack locking as a bounded exception to "allocated is read-only"
**Statement:** Creating a Break/Pack order increases the source balance's `allocated` by the
locked base quantity (a deliberate, audited exception to "allocated belongs to Sales") and locks
both the source and all destination locations against Manual Adjustment (BR-08a) until the order
is completed or cancelled. Completing the order performs the actual stock move (decrease source,
increase/create destinations) and releases the lock; cancelling releases the reservation and lock
without moving stock.
**Enforcement point:** `FN-25 submitBreakPackOrder`, `FN-26 completeBreakPackOrder`,
`cancelBPOrder` equivalent.
**Precondition on completion:** the order must have an assignee, else `ERR_UNASSIGNED`.
**Scenario:** S-11, OB-1 (part of the ENC superset), S-07 (cross-link to the lock guard).

---

## §5.2 Negative Stock (design-accepted, not a defect)

**Statement:** Available quantity (`on_hand − allocated`) may be negative when Sales has allocated
more than is physically on hand (over-reservation upstream). This screen displays it (badge:
ขาดสต็อก, red) and does not block it — it is not this feature's job to prevent Sales
over-allocation, only to surface it for reconciliation.
**Observed as:** mock balance `S011` (RM-2010 at L017), `allocated=75 > on_hand=60`.
**Scenario:** S-08b, EC-INV-05. **Open question:** OQ-INV-04 (who owns reconciliation; should
Sales be blocked from over-allocating at the source?) is unresolved — this rule describes the
current display-only behavior, not a permanent policy stance.

---

## §5.3 Edge Cases (EC) — including Phase 2.5 `[AI-DEFAULT]` items

| EC | Trigger | Behavior | Source |
|---|---|---|---|
| EC-INV-01 | Concurrent adjustment writes to the same balance | Server re-reads `on_hand`/`allocated` at write time; a stale second writer's request fails with `ERR_STALE_DATA` (409) | `[AI-DEFAULT]` (PR-1) |
| EC-INV-02 | Balance viewed in a drawer while another user adjusts it | No live-refresh guarantee — the drawer shows a "ข้อมูล ณ" (as-of) timestamp; a re-open re-fetches | `[AI-DEFAULT]` (PR-2) |
| EC-INV-03 | Role changes (or is revoked) while a mutation modal is open | Server re-checks `canAdjust()`-equivalent role/scope at submit time, not just at modal-open time | `[AI-DEFAULT]` (PR-3) |
| EC-INV-04 | Double-submit of Manual Adjustment or Break/Pack (network retry, double-click) | `Idempotency-Key` required on API-08/API-11; same key + different body → `ERR_IDEMPOTENCY_CONFLICT` (409); same key + same body → returns the original result | `[AI-DEFAULT]` (PR-7) |
| EC-INV-05 | Available quantity goes negative (over-allocation) | Displayed, not blocked — see §5.2 | Corroborated by PREBRIEF S-08b, not defaulted |
| EC-INV-06 | Lot-quantity sum drifts from parent balance's `on_hand` | Not resolved by this pass — `04_DB.md §4.2` notes it as a data-quality concern, no OQ raised (out of the 12 PREBRIEF obligations) | Observed in mock (`S010`) |
| EC-INV-07 | Product/location does not resolve on drawer route entry (bad id, cross-warehouse id, service-item id) | Drawer silently does not open (no error toast in the observed HTML) — **flagged for QA as a UX gap to verify in the real build**, not specified as "correct" behavior by this FRD | Observed in `syncRouteToState()` fallthrough branches |

---

## §5.4 Error Catalog

| Code | HTTP | Message (Thai, verbatim from HTML where available) | Trigger |
|---|---|---|---|
| `ERR_REASON_REQUIRED` | 400 | "เลือกเหตุผลการปรับก่อน" | Manual Adjustment submit without a reason (L2698) |
| `ERR_DUPLICATE_LINE` | 400 | "มีสินค้า+ตำแหน่งซ้ำกันหลายบรรทัด — รวมเป็นบรรทัดเดียวก่อน" | duplicate `(pid, loc)` in one batch (L2701) |
| `ERR_LINE_INCOMPLETE` | 400 | "เลือกสินค้าและตำแหน่งให้ครบ" | line missing pid/loc (L2703) |
| `ERR_LOCATION_LOCKED` | 400 | "ตำแหน่งถูกล็อกโดยคำสั่งแตก/แพ็ค — รอดำเนินการเสร็จก่อน" | L2601 |
| `ERR_LOCATION_UNAVAILABLE` | 400 | "ตำแหน่งถูกกันไว้/ปิดใช้งาน — ปรับไม่ได้" | L2602 |
| `ERR_MASTER_INACTIVE_ADD` | 400 | "Master สินค้าหยุดใช้งาน — เพิ่มสต็อกใหม่ไม่ได้ (ลดเพื่อเคลียร์ของออกได้)" | L2603 |
| `ERR_QTY_INVALID` | 400 | "ระบุจำนวนเต็มมากกว่า 0" | L2605 |
| `ERR_NO_STOCK_TO_REDUCE` | 400 | "ไม่มีสต็อกในตำแหน่งนี้ให้ลด" | L2607 |
| `ERR_EXCEEDS_ALLOCATED_CEILING` | 400 | "ลดได้สูงสุด {N} {unit} — ห้ามแตะยอดจอง (จองอยู่ {N} ชิ้นฐาน)" | L2608 |
| `ERR_PERMISSION_DENIED` | 403 | "ไม่มีสิทธิ์ปรับสต็อก (Warehouse Staff / Finance เท่านั้น)" | L2578 |
| `ERR_EXPORT_DENIED` | 403 | "ไม่มีสิทธิ์ส่งออก/ดูมูลค่า (Finance/Auditor เท่านั้น)" | L1361 |
| `ERR_BP_NO_SOURCE` | 400 | "เลือกต้นทางที่มีของก่อน" | L2329 |
| `ERR_BP_QTY_RANGE` | 400 | "จำนวนต้นทางต้องอยู่ 1–{N} {unit} (มี {N})" | L2330 |
| `ERR_BP_TARGET_UOM_REQUIRED` | 400 | "เลือกหน่วยปลายทาง (จะแตก/แพ็คเป็นหน่วยอะไร)" | L2331 |
| `ERR_BP_NO_DEST` | 400 | "ระบุปลายทางอย่างน้อย 1 รายการ" | L2334 |
| `ERR_BP_QTY_MISMATCH` | 400 | "ปลายทางรวม {N} ต้องเท่าต้นทาง {N} ชิ้นฐาน" | L2336 |
| `ERR_BP_DEST_EQ_SOURCE` | 400 | "ปลายทางต้องไม่ใช่ตำแหน่งต้นทาง" | L2337 |
| `ERR_UNASSIGNED` | 400 | "กรุณามอบหมายผู้รับผิดชอบก่อนดำเนินการ" | L2358 |
| `ERR_STALE_DATA` | 409 | (server-only, `[AI-DEFAULT]` — no client copy exists) | EC-INV-01 |
| `ERR_IDEMPOTENCY_CONFLICT` | 409 | (server-only, `[AI-DEFAULT]`) | EC-INV-04 |

---

## §5.5 `[AI-DEFAULT]` Register

All 4 tagged in §5.3 (EC-INV-01, 02, 03, 04) map to `00_OVERVIEW.md §0.8.1` Phase 2.5 probes
PR-1/PR-2/PR-3/PR-7 respectively, and are consolidated for BA confirmation alongside
OQ-INV-01..06.

---

## §5.6 Not-in-Scope Rule (explicit non-rule, for clarity)

**Costing/valuation (G-01) has no business rule specified in this pack.** No rule number is
assigned to it, and none of BR-01..BR-11 above govern it. This is intentional — see
`00_OVERVIEW.md §0.1.4` and **OQ-INV-06**. Do not infer a rule for it from the HTML's
implementation; the HTML's behavior there is unreviewed.

---

## §5.7 Data Classification Enforcement Summary (D-CLASS, R10 pairing with `04_DB.md §4.6`)

| Level | Fields | Enforcement |
|---|---|---|
| Internal (all in-scope fields) | stock quantities, location/product references, ADJ log, BP orders | RLS + warehouse row-scoping (server) + conditional UI render (§0.4) |
| Confidential (conditional, not built) | `cost`/valuation | **Not enforced because not built** — see G-01/OQ-INV-06. Must not be added to any response without a prior Security Bible D5 pass |
| Restricted | none | n/a |

No field in this pack defaults to `Public` (R10 compliance verified).
