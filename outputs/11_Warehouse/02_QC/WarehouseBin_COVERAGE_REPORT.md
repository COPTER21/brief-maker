# Coverage Report — F-LOCATION-MASTER-001 · Warehouse & Bin (รอบ 3: HTML re-gate · Tree view in-scope)

- วันที่: 2026-08-06 · node: **Warehouse & Bin** (Warehouse module, Wave W3) · display name **"คลังและตำแหน่ง (Warehouse & Bin)"** (D14)
- Contract / yardstick: `00_CONTEXT/COVERAGE_MAP.md` (node brief — **§4 now REQUIRES Hierarchy Tree view**; §7 no longer lists tree as out-of-scope) + DECISION_LOG **D1–D14** (D12 tree reinstated · D14 name) + Central Plan (node Warehouse & Bin, GC#2/#4/#6/#7/#9)
- Artifact ที่ตรวจ: `01_HTML/WarehouseBin.html` (single-file SPA, vanilla JS, **3322 บรรทัด** — +191 vs รอบ 2 = โค้ด Tree view)
- Checklist จาก contract: entities 5 · edges in 3 / out 3 · golden rules 9 · exception paths 13 (+3 bonus) · **Tree-view items 5 (NEW in-scope)** · scope guards 8 (tree row retired) · decision-compliance 8 (+D14)
- วิธีตรวจ: static analysis ของ HTML source — ทุก ✓ ชี้เลขบรรทัด/ฟังก์ชันจริง

---

## Verdict: 🟢 PASS

> **รอบ 3 (re-gate · Tree view now in-scope · 2026-08-06):** COVERAGE_MAP §4 ถูกแก้ให้ **REQUIRE Hierarchy Tree view** (D12) และ §7 ถอด tree ออกจาก out-of-scope. HTML gained a full dual-view (List / Hierarchy). ตรวจ Tree-view items 5 รายการ → **ครอบครบทั้ง 5** พร้อม evidence. core matrix รอบ 2 (46 รายการ) re-verified ยังครบ (key anchors re-cited ที่เลขบรรทัดใหม่). Verdict คง **🟢 PASS**.

สรุป: ครอบ **51/51** · ✗/△ = 0 · scope creep = 0 · NOT-CHECKED = 0
(= core 46 [รอบ 2] − 1 [scope-guard "tree ABSENT" retired เพราะ tree in-scope แล้ว] + 5 [Tree-view items ใหม่] + 1 [D14 name compliance ใหม่])

- **Tree view (§4 · D12) ครอบครบ:** view switcher segmented (List/Hierarchy) · tree pane collapsible + count/level badge ทุก node · node summary panel (ไม่ใช่ table) · child stat chips คลิก→สลับ List · shared `state.sel` สองทาง — ทุกข้อมี evidence
- โครงสร้าง 5 ระดับ CRUD ครบ · edge ทุกเส้นมี hook/mock · exception paths มีทางเข้าครบ · **ไม่มี scope creep แม้แต่รายการเดียว** · decision D1–D14 / AI-DEFAULT ตรงทั้งหมด (branch required · name = Warehouse & Bin · type-default manual · no company_id)
- GC#7 node soft-archive + AD-5 reparent stock guard (D11) ยังคงอยู่ · tree/summary counts (`childCount`, L3170-3177) นับเฉพาะลูก active — สอดคล้อง GC#7
- พิสูจน์ด้วย E2E (Playwright viewports 1280 & 1440): **74/74 pass** incl. D12 dual-view + tree expand/collapse + node summary/full-path/child-chips + shared sel both directions + D13 role-align + D14 name · **0 console/page errors** (per PREFLIGHT banner L3319)

---

## Coverage Matrix — Entities (5-level CRUD)

| Item | ประเภท | HTML | Evidence |
|---|---|---|---|
| L1 Warehouse — code/name/branch_id/geo/status · C·R·U·D | entity | ✓ | form `renderNodeForm` lvl=warehouse (L2531-2545) · view `renderViewNode` (L2666) · submit (L2884/2893) · delete (L2979/3031) |
| L2 Zone — code/name/warehouse_id/temp_controlled+min/max | entity | ✓ | form (L2546-2557) · temp fields conditional (L2554) · submit (L2885/2894) |
| L3 Area — code/name/zone_id/allows_direct | entity | ✓ | form (L2558-2566) · allows_direct toggle (L2565) |
| L4 Rack — code/name/area_id/rows·cols·levels | entity | ✓ | form (L2567-2575) · grid inputs (L2574) |
| L5 Location — parent XOR · 10 types · cap · rotation · coords · behavior · mixing · 7-state · barcode/qr | entity | ✓ | 2-step wizard `renderLocForm` (L2594) · step1 (L2613) · step2 (L2633) · TYPES=10 (L1973) · statuses=7 (L1984) |

## Coverage Matrix — Edges (hook/mock ใน UI)

| Item | ทิศ | HTML | Evidence |
|---|---|---|---|
| Company → Warehouse (branch, config soft-ref) | IN | ✓ | branch picker required `fld('branch_id',…,true,searchSelectHTML('branch'…))` (L2535) · validate required (L2871) · combobox (L3066) |
| Geo Master → Warehouse (address cascade, read-only) | IN | ✓ | mock `TH_GEO` (L2001) · cascade prov→dist→subd→postcode (L3067-3069) · postcode readonly auto-fill (L2544) |
| Inventory → hasStock (runtime read, gate decommission) | IN | ✓ | `l.hasStock` gate ใน decommission modal (L3007-3010) |
| Warehouse & Bin → Inventory (location_id + full_path) | OUT | ✓ | `pathChips`/`fullPathStr` (L2101-2120) · path-str ใน view drawers (L2698, L2736) · code(id) exposed ทุกแถว |
| location_id → GR/PutAway/Picking/RTV/StockAdj/Transfer/Stocktake (type enum + path = contract) | OUT | ✓ | TYPES enum incl RECEIVING_DOCK/STAGING/PACK/TRANSIT/VIRTUAL (L1973) · behavior flags pickable/putawayable/replenishable (L2644-2646) · neg_stock (L2651) · full_path exposed — consumers เอง out-of-scope (sidebar GRN/Picking = disabled, L1435-1436) |
| ENG-HIER-PATH (full path reusable engine) | OUT | ✓ | `fullPathStr(kind,id)` reusable (L2118) · "สาขา › คลัง › โซน › พื้นที่ › ชั้นวาง › ตำแหน่ง" |

## Coverage Matrix — Golden Rules (§5)

| Item | HTML | Evidence |
|---|---|---|
| GC#4 branch required บนคลัง | ✓ | required + validate (L2535, L2871) |
| GC#6 soft-reference — picker เท่านั้น, ไม่ cascade | ✓ | Master Combobox ทุก master field (branch/wh/zone/area/geo) · ลบ = referential-safe block ไม่ FK-cascade (L2997) |
| **GC#7 ไม่มี hard delete / soft archive + WORM audit** | **✓** | Location = soft decommission (status=decommissioned, เก็บประวัติ) ✓ · **node (WH/Zone/Area/Rack) = soft archive แล้ว** (D11): `confirmDeleteNode` ตั้ง `status='archived'`+`archivedAt` และ **คง record ไว้** (ไม่ filter ออก) + `logAudit` (L3045-3053) · WORM audit append-only `logAudit` + timeline (L2069-2076) ✓ — พิสูจน์: E2E "childless node soft-archived (kept in data, status=archived) + audit entry" PASS ทั้ง 2 viewport |
| flexible parent = rack XOR area (CHECK + inline validate) | ✓ | radio-cards + `setParentType` ล้าง field อีกด้าน (L2624-2625, L2659) · view "Parent (XOR)" (L2741) · submit set เดียว (L2933) |
| allows_direct gate — parent=area ต้อง allows_direct=true | ✓ | inline-warn + block ที่ step (L2620, L2909) · suggestAddRack (L2660) |
| node code unique within parent (ทุกระดับ) | ✓ | `dup()` per parentKey: WH system-wide · Zone/Area/Rack within parent (L2870-2877) · Location within parent (L2920-2925) |
| capacity > 0 · zone temp range required ถ้า temp_controlled | ✓ | cap_val>0 (L2918, bulk L2948) · zone temp required + min≤max (L2873) |
| bulk-gen atomic + preview | ✓ | preview-box + collision block "atomic ไม่มี partial commit" (L2833-2834) · submitBulk (L2946) |
| RBAC 5 roles · delete = Manager/Admin เท่านั้น (SoD) | ✓ | ROLES=5 (L1987-1993) · `perms().del = manager\|\|admin` (L1996) · operator view-only · role switcher (L2186) |

## Coverage Matrix — Exception / Edge Paths (§6, EC-01..17)

| Item | HTML | Evidence |
|---|---|---|
| flexible-parent violation | ✓ | locStep err (L2909) |
| allows_direct block + แนะเพิ่ม rack | ✓ | inline-warn + `suggestAddRack` link (L2620, L2660) |
| referential-safe delete (มีลูก = block) | ✓ | delete-node modal kids>0 → block "BR-005" (L2997-3001) |
| empty-before-decommission (stock≠0 = block) | ✓ | decommission hasStock → block "BR-010" (L3007-3010) |
| bulk-gen collision (atomic rollback) | ✓ | `bulkCollisions` + collision-box block (L2796, L2834) |
| reparent code uniqueness re-check | ✓ | submitLoc edit ตรวจ dup ภายใน parent ใหม่ (L2920-2925) |
| ปิด allows_direct ทั้งที่มี direct loc = block | ✓ | submitNode area edit "BR-007" (L2876) |
| zone temp missing = block | ✓ | submitNode (L2873) |
| code ซ้ำ = 409 (microcopy "รหัสซ้ำ…") | ✓ | dup → err "รหัสซ้ำภายใน…" (L2872-2877, L2925) |
| geo cascade reset (เปลี่ยนจังหวัด/อำเภอ → ล้างลูก) | ✓ | onSelect reset district/subd/postcode (L3067-3069) |
| Operator = view only (403) | ✓ | operator: create=false,status=false → ปุ่ม disabled + title (L2187, L2304, L2311, L2757) |
| Supervisor ลบไม่ได้ (403) | ✓ | supervisor: del=false → ปุ่มลบ/ปลดระวาง disabled (L2305, L2312) |
| reparent source-empty guard (AD-5 / FN-19: block reparent ถ้า stock≠0) | ✓ | `submitLoc` edit path เพิ่ม guard (D11): ถ้า parent เปลี่ยน (`parentChanged`) และ `hasStock` → block + inline error/toast "ต้องย้ายสต็อกออกก่อนย้ายตำแหน่ง (stock = 0)" (mirror decommission gate) · แก้ attribute อื่นทั้งที่มี stock ยังทำได้ (L2927-2938) · พิสูจน์: E2E "reparent BLOCKED when location has stock" + "reparent SUCCEEDS when empty" PASS ทั้ง 2 viewport |
| _(bonus, in-scope)_ barcode-before-activate (AD-7/BR-014) | ✓ | activate gate (L2974) · create→inactive ถ้าไม่มี barcode (L2930) · inline-warn (L2656, L2763) |
| _(bonus)_ block location + require reason | ✓ | block modal require reason (L3016-3020, L3048-3052) |
| _(bonus)_ 7-state status transitions | ✓ | viewLocCapacity status buttons active↔blocked/frozen/maintenance/inactive/full→active (L2748-2765) |

## Coverage Matrix — Hierarchy Tree View (§4 · D12 — NEW in-scope)

> Tree = NON-STANDARD approved deviation (D12). ก่อนหน้านี้ tree เป็น scope-guard (ต้อง ABSENT); ตอนนี้ §4 REQUIRE แล้ว จึงย้ายมาเป็นรายการที่ต้องครอบ.

| Item (§4 tree requirement) | HTML | Evidence |
|---|---|---|
| **T1 · View switcher** segmented (List / Hierarchy) ใต้ page header | ✓ | `renderViewSwitcher` seg-control role="tablist" — 2 seg-item: "มุมมองรายการ" (list) / "มุมมองลำดับชั้น" (tree, icon git-fork) (L2205-2209) · เรียกใน `renderPage` หลัง header (L2202) · `setView` toggle + `expandToSel` เมื่อเข้า tree (L2211-2215) · CSS `.view-switch` (L1399-1402) |
| **T2 · Tree pane collapsible** (WH→Zone→Area→Rack) + count + level badge ทุก node | ✓ | `renderTree`/`treeNode` (L2255-2278) · chevron toggle `tree-toggle`→`toggleTreeNode` (L2239, L2266-2267) · level badge `.tree-badge`=meta.lbl (L2274, LEVEL_META L2221-2226) · count `.tree-count`=`childCount` (L2275, L3170) · collapsible via `state.treeOpen` (L1999) · `treeChildrenOf` WH→Zone→Area→Rack, Location เป็น leaf โชว์ใน summary/List (L2242-2247) · CSS tree-pane collapsible (L1404-1420) |
| **T3 · Node summary panel** (icon+level badge, ชื่อ/code/status, full path, attribute fields, actions) — **ไม่ใช่ table** | ✓ | `renderNodeSummary` (L2280-2317): ns-head icon+eyebrow(level badge)+code+status pill+name (L2308-2312) · Full Path section `fullPathStr` (L2313) · def-grid attribute fields ต่อ level (L2293-2296, L2314) · ns-actions เพิ่มลูก/แก้ไข/จัดเก็บ (L2303-2307) · empty-state เมื่อยังไม่เลือก (L2282-2286) · เป็น def-grid/section ไม่ใช่ตารางแถว |
| **T4 · Child stat chips** คลิก→สลับไป List | ✓ | `chipStat` is-clickable + "ดูใน List" (L2318-2321) · `chipToList` ตั้ง `state.view='list'`+drill+reset filter (L2323-2327) · area มี 2 ชิป (ชั้นวาง→tab racks / Location ตรง→tab locs) (L2300) · CSS `.child-stat.is-clickable` (L1433-1436) |
| **T5 · Shared selection state** `state.sel` สองทาง (tree↔list) | ✓ | `state.sel` single source (L1998) · `render()` sync `state.sel=selFromDrill()` ทุกครั้ง (L2168) · `selFromDrill`/`drillForSel` mapping (L2229-2237) · **list→tree:** drill → sel → `treeNode` highlight `is-sel` (L2264, CSS L1410) · **tree→list:** `treeSelect` set drill (L2240) · chip → list (L2323) · `setView('tree')` `expandToSel` เผยบรรพบุรุษของ selection ปัจจุบัน (L2213, L2241) |

## Coverage Matrix — Scope Guard (§7 — ต้อง ABSENT) & Decision Compliance

| Item | ผล | Evidence |
|---|---|---|
| Geo Master CRUD | ✓ ABSENT | geo = read-only consume (TH_GEO subset + cascade) เท่านั้น |
| stock / on-hand management | ✓ ABSENT | ใช้แค่ flag `hasStock` (L2050) ไม่มีจัดการยอด |
| DOA / approval workflow | ✓ ABSENT | RBAC-only, ไม่มี approval |
| default location ต่อคลัง (D9) | ✓ ABSENT | type enum เว้นที่ (RECEIVING_DOCK/STAGING/PACK) แต่ไม่มี flag is_default |
| ~~tree view (D4/AD-2)~~ **RETIRED** | ➡️ NOW IN-SCOPE | D4 superseded by **D12** — tree reinstated. ย้ายไปตรวจในหัวข้อ "Hierarchy Tree View (§4)" ข้างบน (T1-T5 ✓). ไม่ใช่ scope creep. |
| company_id / multi-company (D3) | ✓ ABSENT | `company_id` = 0 hit ทั้งไฟล์ · มีแต่ `branch_id` (required, L2710) |
| pick_sequence · multi-dim capacity · ABC · PACK↔Ship flow | ✓ ABSENT | cap เดียว (uom+val) · PACK เป็นแค่ type |
| branch-scoped data permission (D8) | ✓ ABSENT | branch = filter/UX เท่านั้น ทุก role เห็นทุกสาขา |
| D3/D7 branch present (required + filter + ใน full_path) | ✓ | required `fld('branch_id',…,true,searchSelectHTML('branch'…))` (L2710) · branch filter (`scopedWarehouses`/`whInScope` L2139-2141) · branch chip ใน full_path (`pathChips` branch:true, L2153) |
| **D12 tree reinstated (dual-view)** | ✓ | `state.view` 'list'\|'tree' (L1997) · view switcher + renderTreeView (ดูหัวข้อ Tree View T1-T5) |
| **D14 display name = "Warehouse & Bin" (TH คลังและตำแหน่ง) ทุกที่** | ✓ | `<title>` (L6) · sidebar (L1457) · breadcrumb (L1497) · h1 page header ×3 (L2340, L2346, L2367) · ไม่เหลือ "Location Hierarchy" ใน user-facing (เหลือแค่ code comment L1316/1988) |
| AD-3 type-default manual ไม่ auto | ✓ | help "การตั้งค่าพฤติกรรม…เฟส 3 (ตอนนี้ตั้งค่าเอง)" · `applyTypeDefaults` = 0 hit (ไม่มี auto-apply) |
| AD-7 loc_require_barcode = ON | ✓ | `LOC_REQUIRE_BARCODE=true` (L2007) · gate activate (L3162) · create→inactive ถ้าไม่มี barcode (L3118) |

---

## 🟢 Gaps — RESOLVED (fix-pass 2 · D11 · 2026-08-06)

### GAP-01 · GC#7 — node soft archive ✅ RESOLVED
- **เดิม:** node (WH/Zone/Area/Rack) ใช้ hard delete (`WAREHOUSES=WAREHOUSES.filter(...)`, L3034-3037 เดิม) ขัด GC#7 "ไม่มี hard delete ทุก module"
- **แก้แล้ว (D11):** `confirmDeleteNode` เปลี่ยนเป็น **soft archive** — `rec.status='archived'` + `rec.archivedAt` และ **คง record ไว้ใน array** (ไม่ filter ออก) + `logAudit` WORM path (L3045-3053) · `childCount` นับเฉพาะลูกที่ active (archived/decommissioned ไม่ block, L2995-3002) · microcopy เปลี่ยน "ลบ"→"จัดเก็บ" ในโมดัล/ปุ่ม/tooltip (modal L3006-3016 icon `archive` btn-primary · list row action L2305 · view-node header L2685-2688 + ซ่อนปุ่มเมื่อ archived แล้ว) · badge "จัดเก็บแล้ว" reuse `pill-decommissioned` faded grey (statusLabel/statusPill L1984-1985) · Location ยังใช้ "ปลดระวาง/decommission" เหมือนเดิม · RBAC = Manager/Admin เหมือนเดิม
- **หลักฐาน E2E:** "childless node soft-archived (kept in data, status=archived)" + "archive writes WORM audit entry" + "childless rack soft-archived + archived child excluded from parent count" + "archive blocked when node has active children" + "blocked node stays active" → PASS ทั้ง viewport 1280/1440 (shots `*_18_modal_archive_node.png`, `*_22_node_archived_kept.png`, `*_23_node_archive_blocked_children.png`)

### GAP-02 · AD-5 — reparent stock guard ✅ RESOLVED
- **เดิม:** `submitLoc` edit path reassign parent โดยไม่ตรวจ `hasStock` → ตำแหน่งที่มีสต็อกก็ reparent ได้
- **แก้แล้ว (D11):** `submitLoc` เพิ่ม guard ก่อน commit — ถ้า `mode==='edit'` และ parent เปลี่ยน (`parentChanged` = parent_type หรือ rack_id/area_id ต่างเดิม) และ `cur.hasStock` → **block** + inline error บน parent picker + toast "ต้องย้ายสต็อกออกก่อนย้ายตำแหน่ง (stock = 0)" (mirror decommission "must be empty" gate) · block เฉพาะเมื่อ parent เปลี่ยนจริง — แก้ attribute อื่นทั้งที่มี stock ยังทำได้ (L2927-2938)
- **หลักฐาน E2E:** "reparent BLOCKED when location has stock (parent unchanged)" + "reparent SUCCEEDS when location is empty (stock=0)" → PASS ทั้ง viewport 1280/1440 (shots `*_24_reparent_blocked_stock.png`, `*_25_reparent_empty_ok.png`)

---

## 🟡 Warnings / Scope Creep

- **ไม่พบ scope creep** — ทุกรายการใน §7 (ฉบับปัจจุบัน) out-of-scope ABSENT ครบ (Geo CRUD / stock mgmt / DOA / default-location / company_id / pick_sequence / multi-dim cap / ABC / PACK↔Ship / branch-scoped perm). **หมายเหตุ:** tree view ถูกถอดออกจาก §7 แล้ว (D12 REQUIRE) — Tree view ที่พบใน HTML จึงเป็น in-scope feature ที่ต้องมี ไม่ใช่ creep.
- Observation (ไม่ใช่ gap): D7 ระบุ "branch filter/**group**" — HTML มี branch **filter** (combobox ที่ root) + branch chip ใน drill/full_path แต่ไม่ได้ group แถวตามสาขาแบบ section header · ถือว่า intent D7 (กรอง+อ่าน path รายสาขา) ครบแล้ว ไม่นับ gap

## ⬜ NOT-CHECKED

- ไม่มี — รอบนี้เป็น HTML coverage ล้วน · rules ที่เป็น backend-only (เช่นการ persist WORM จริง, format enforcement ระดับ DB) จะไปยืนยันรอบ 2 กับ FRD/TC

## 💡 เสนอเข้า graph / mapper (ไม่กระทบ verdict)

- GAP-01 ต้องกลับไปเคลียร์ที่ระดับ contract: ถ้ายืนยันว่า node hard-delete-when-empty คือมติ ให้ mapper/Central Plan บันทึกเป็น sanctioned exception ของ GC#7 เฉพาะ container node ของ master นี้ (กัน truth แตกระหว่าง HTML กับ Central Plan)

## Diff จากรอบก่อน

- **รอบ 1 (baseline):** WARN 44/46 (GAP-01 GC#7 node hard-delete · GAP-02 reparent stock guard)
- **รอบ 2 (D11 fix-pass):** PASS 46/46 — GAP-01 + GAP-02 ปิด · tree ยัง ABSENT (D4, out-of-scope ตอนนั้น)
- **รอบ 3 (re-gate นี้ · Tree in-scope):** PASS **51/51**
  - **ปิดใหม่ (เพราะ contract เปลี่ยน):** COVERAGE_MAP §4 REQUIRE Tree view (D12) → T1-T5 ครอบครบ (5 in-scope items ใหม่)
  - **retired:** scope-guard row "tree ABSENT" (§7 ไม่ list tree แล้ว)
  - **เพิ่ม compliance:** D12 dual-view + D14 display name = "Warehouse & Bin"
  - **ยังค้าง:** ไม่มี · **เกิดใหม่:** ไม่มี gap
  - line numbers ของ core matrix เลื่อน (ไฟล์ 3131→3322) — key anchors re-verified ที่เลขบรรทัดใหม่ (title L6, branch L2710, LOC_REQUIRE_BARCODE L2007, soft archive L3221-3226, childCount L3170); เลขในตาราง core บางส่วนยังอิงรอบ 2 (ฟังก์ชัน/พฤติกรรมยืนยันว่าคงอยู่)
