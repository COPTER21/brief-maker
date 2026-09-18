# 06_TESTS — F-INV-001 Stock by Location

> Audience: QA
> Expected text below is quoted **verbatim from the gated HTML** (Mode A / R14 HTML Fidelity) —
> where no on-screen text exists for a server-only behavior, `microcopy.md` central conventions are
> used and marked `[central microcopy]`.

---

## §6.1 Acceptance Criteria — View & Read (S-01..S-04)

### AC-01 — First load shows 4 stats + 1-row-per-product list (S-01, OB-1/2/3/5/7)
1. Navigate to `#/stock` → warehouse Gate shown, click a warehouse row
2. Land on `#/stock/{wh}/sku` — 4 stat cards visible: "สินค้า (SKU)", "ต่ำกว่าขั้นต่ำ", "สต็อกติดลบ",
   "ตำแหน่ง HOLD"
3. Table shows exactly one row per product (no duplicate product rows across locations)
4. No row for any `type='SV'` product (verify against `SV-8001` in seed data — must not appear)
5. Product reference shows only code + old_code format — no `code_item`/`code_sku` label anywhere

### AC-02 — Product drawer, 3 tabs, unit displayed with base equivalent (S-02, OB-4)
1. Click a product row → drawer opens, tabs "ภาพรวม" (default) / "ตำแหน่งจัดเก็บ" / "การเคลื่อนไหว"
2. On "ภาพรวม": 3 stat blocks "คงเหลือรวม" / "จองแล้ว" / "พร้อมใช้"
3. Refresh the page with the drawer open (hash has the product id) → drawer re-opens on reload
   (route refresh-safe)
4. On "ตำแหน่งจัดเก็บ": every row shows quantity in that location's unit; when `factor > 1`, a
   base-unit sub-value is shown (format: "= N unit")

### AC-03 — By-location view + location drawer (S-03, OB-4)
1. Switch view toggle to "ตามตำแหน่ง" → cards/rows per location with a utilization bar
2. Click a location → drawer "สิ่งที่อยู่ในตำแหน่งนี้" table, quantities in the location's own unit
3. From the location drawer, click a product row → drills into the Balance Drawer at
   `#/stock/{wh}/sku/S{id}`

### AC-04 — Search + filter (S-04)
1. Type a central code, old code, or product name fragment into search → list narrows accordingly
2. Toggle "ซ่อนสต็อก 0" → rows with `on_hand = 0` disappear
3. Click the "ต่ำกว่าขั้นต่ำ" stat → list filters to low-stock products only; click it again → filter
   clears (toggle behavior)
4. Sort by "คงเหลือ"/"จองแล้ว"/"พร้อมใช้" — values compared must be **base-unit** values (verify a
   product with `factor > 1` sorts correctly against one with `factor = 1`)

---

## §6.2 Acceptance Criteria — Manual Adjustment (S-05, S-05b, S-06, S-07)

### AC-05 — Happy path multi-line adjustment (S-05)
1. As `warehouse_staff` or `finance`, click "ปรับสต็อก" → modal opens: title "ปรับสต็อก (Manual
   Adjustment)"
2. Select เหตุผลการปรับ (required — leaving it blank and submitting shows toast **"เลือกเหตุผลการปรับก่อน"**)
3. Add 2+ lines with different valid `(product, location)` pairs, mixed add/reduce directions
4. Summary bar reads "พร้อมบันทึก 2 / 2 บรรทัด" (or however many are valid) with correct
   "เพิ่มรวม +N ชิ้นฐาน" / "ลดรวม −N ชิ้นฐาน" totals
5. Submit → toast **"บันทึก {ADJ-YYYY-NNNN} · ปรับ {N} รายการ · เก็บ log แล้ว"**, modal closes

### AC-06 — Service item cannot be selected (S-09, OB-3)
1. Open the product search-combobox inside a Manual Adjustment line
2. Confirm `SV-8001` (or any `type='SV'` product) never appears in the option list, even when
   searching by its exact code

### AC-07 — Low stock badge + note (S-08, OB-6)
1. Find (or set up via adjustment) a product where available < `min_stock`
2. List row shows pill **"ต้องเติม"**
3. Drawer overview shows note: **"ต่ำกว่าขั้นต่ำ — พร้อมใช้ {N} {unit} < threshold {N} {unit} (ตั้งจาก
   Item Master)"**

### AC-08 — Negative stock badge + note (S-08b)
1. Use seed data `RM-2010` at location `L017` (allocated=75 > on_hand=60)
2. List row shows pill **"ขาดสต็อก"** (red)
3. Drawer overview shows note: **"พร้อมใช้ติดลบ (จอง > คงเหลือ) — ต้อง reconcile"**

### AC-09 — New balance in empty location (S-05b, OB-8)
1. In a Manual Adjustment line, pick a `(product, location)` pair with no existing balance
2. Location combobox option shows the label suffix **"· ว่าง — เพิ่มเข้าได้"**
3. Quantity preview shows **"รายการใหม่ในตำแหน่งนี้"** and "ปัจจุบัน 0 → {N} {unit}" once a quantity
   is entered
4. Submit → new balance record created; summary bar's "รายการใหม่ {N} ตำแหน่ง" count reflected it

### AC-10 — Allocated ceiling blocks over-reduction (S-06, OB-11)
1. Pick a balance with `allocated > 0` (e.g. `FG-1001` at `L003`, on_hand=48, allocated=12)
2. Select "ลด" direction, enter a quantity that would take `on_hand` below `allocated`
3. Inline error appears: **"ลดได้สูงสุด {N} {unit} — ห้ามแตะยอดจอง (จองอยู่ {N} ชิ้นฐาน)"**
4. Attempting submit anyway is blocked — toast shows the same error prefixed with the line number:
   "บรรทัดที่ {N}: {error}"
5. Confirm the balance's `allocated` value is unchanged after any successful adjustment on that
   line (verify via the audit log line's before/after — only `on_hand` moves)

### AC-11 — Locked/blocked location or inactive master blocks the line (S-07)
1. Pick a location currently locked by an active Break/Pack order → error:
   **"ตำแหน่งถูกล็อกโดยคำสั่งแตก/แพ็ค — รอดำเนินการเสร็จก่อน"**
2. Pick a location with `loc_status` blocked/frozen → error:
   **"ตำแหน่งถูกกันไว้/ปิดใช้งาน — ปรับไม่ได้"**
3. Pick an inactive-master product with direction="เพิ่ม" → error:
   **"Master สินค้าหยุดใช้งาน — เพิ่มสต็อกใหม่ไม่ได้ (ลดเพื่อเคลียร์ของออกได้)"**; same product with
   direction="ลด" against an existing balance → allowed

### AC-12 — Audit log created + append-only (S-12, OB-11)
1. After any successful adjustment, navigate to "ประวัติการปรับ" (`#/stock/{wh}/log`)
2. New document appears at the top of the list with correct doc no., actor, reason, line count,
   add/reduce base totals
3. Click into the document → drawer shows every line with before→after values in base units
4. Confirm no edit/delete action exists anywhere on this drawer or list row
5. Search by doc no., actor name, product code, or location code → correctly filters the log

### AC-13 — RBAC (S-10, OB-12)
1. Switch role to `inventory_viewer`, `procurement`, or `auditor` → "ปรับสต็อก" button absent from
   every entry point (list header, product drawer, balance drawer, audit log header) — not merely
   disabled
2. Switch to `warehouse_staff` → confirm the Gate page is skipped entirely and the user lands
   directly on their assigned warehouse; confirm "คลังทั้งหมด" back-button is absent
3. (Server-side, requires API access) attempt a direct POST to `/inventory/stock/adjustments` as a
   non-permitted role → `403 ERR_PERMISSION_DENIED`

---

## §6.3 Acceptance Criteria — Break/Pack (S-11)

### AC-14 — Create, lock, complete a Break order
1. Navigate to "แตก/แพ็ค" (`#/stock/{wh}/bp`), click "สร้างคำสั่ง"
2. Choose a multi-UoM product, source location with stock, source quantity within range, target
   unit smaller than source's current unit, one or more destinations summing exactly to the source
   base quantity
3. Submit → toast **"สร้างคำสั่ง {BP-NNN} · ล็อก {N} ชิ้น + {N} ตำแหน่ง"**
4. Confirm the source location now shows as locked if a Manual Adjustment is attempted against it
   (cross-link to AC-11 point 1)
5. Open the order drawer, assign a person (search-combobox), click "ดำเนินการเสร็จ"
6. Toast **"{BP-NNN} ดำเนินการเสร็จ · ย้าย stock + ปลดล็อกแล้ว"** — verify source `on_hand` decreased
   and destination(s) increased by the exact base quantity, and both locations are unlocked
7. Attempting "ดำเนินการเสร็จ" **before** assigning anyone shows warn toast:
   **"กรุณามอบหมายผู้รับผิดชอบก่อนดำเนินการ"**

### AC-14b — Cancel a locked order
1. Create an order, do not complete it, open its drawer, click "ยกเลิกคำสั่ง"
2. Toast **"ยกเลิกคำสั่ง {BP-NNN} · ปลดล็อกแล้ว"** — confirm the source `allocated` reservation is
   released and both locations unlock

---

## §6.4 Overlay / Esc Chain (OB-9)

### AC-15 — Dropdown portal + two-stage Esc
1. Open the Manual Adjustment modal, open a product/location combobox — verify the option list
   renders as an overlay that does not get clipped by the modal's scroll container
2. Press Esc once → only the dropdown closes, the modal remains open
3. Press Esc again → the modal itself closes
4. Click outside the dropdown (but still inside the modal) → dropdown closes, modal stays open

---

## §6.5 Cross-Module (XT) Cases

### XT-01 — Low stock does not (yet) create any downstream artifact (OQ-INV-05 unresolved)
Verify no Purchase requisition, notification, or report entry is created automatically when a
product crosses the low-stock threshold — this is intentional pending OQ-INV-05, and QA should
**not** file this as a bug.

### XT-02 — Negative stock does not block Sales (OQ-INV-04 unresolved)
Verify that an over-allocated (negative-available) balance does not prevent Sales from continuing
to allocate against it further — this is intentional pending OQ-INV-04, and QA should **not** file
this as a bug, only confirm the display (badge + note) is correct per AC-08.

---

## §6.6 Negative / Absence Assertions

### AC-16 — G-01 absence check (pending business decision)
Because `00_OVERVIEW.md §0.1.4`/`OQ-INV-06` leaves the costing/valuation surface unresolved, QA
must **record its current presence in the HTML as an open item**, not silently pass or fail it:
- Confirm whether "ดูมูลค่า/ซ่อนมูลค่า" and the "รวมมูลค่า" export toggle are present (as of this
  writing, they are, in the prototype) — this is **not** an acceptance criterion this FRD asks QA
  to verify pass/fail on, because it is not a specified requirement. Flag to BA if still present
  at dev-handoff time without a resolution recorded.

### AC-17 — Out-of-scope stubs remain inert
1. Confirm sidebar entries for GRN/Putaway/RTV are visible but produce no navigation/route change
   when clicked (stub only, per PREBRIEF §1 scope-out)

---

## §6.7 Rule → Test Cross-Reference

| BR/EC | Test |
|---|---|
| BR-01 | AC-01 |
| BR-02 | AC-01, AC-06 |
| BR-03 | AC-02, AC-03 |
| BR-04 | AC-01 |
| BR-05 | AC-07 |
| BR-06 | AC-01, AC-07, AC-08 |
| BR-07 | AC-09 |
| BR-08 | AC-10, AC-11 |
| BR-09 | AC-12 |
| BR-10 | AC-13 |
| BR-11 | AC-14, AC-14b, AC-11 (lock cross-link) |
| §5.2 negative stock | AC-08, XT-02 |
| EC-INV-01..04 | Not directly observable client-side — server-side integration tests required at build time (concurrency/idempotency), not expressible as UI acceptance criteria in this pass |
