# HTML UI Brief — F-LOCATION-MASTER-001 Warehouse & Bin

> **AS-BUILT specification** — ทุกข้อสกัดจาก `warehouse-bin.html`; เอกสารนี้ไม่แทน FRD และไม่เพิ่ม business behavior ใหม่

## §0 Document Control + Pairing

| Field | Value |
|---|---|
| Feature | `F-LOCATION-MASTER-001` Warehouse & Bin |
| HTML source of truth | `outputs/06_Warehouse-Bin/warehouse-bin.html` |
| HTML title | `Warehouse & Bin · คลังและตำแหน่ง · CUBE 4.0` |
| HTML shell version | `UAT · v1.1.0` — anchor `.sb-footer` |
| FRD pair | `outputs/06_Warehouse-Bin/04_FRD/FRD_F-LOCATION-MASTER-001_Pack/` |
| BRD pair | `outputs/06_Warehouse-Bin/03_BRD/BRD_Warehouse_Bin.md` |
| Old HTML for diff | — ไม่มีใน input |
| Route strategy | state-driven SPA; ไม่มี hash route / `hashchange` handler |
| Drift status | 3 known behavior gaps; ดู §11.3 |

Extractor helper `scripts/extract_anchors.py` และ template/reference ที่ `SKILL.md` อ้างไม่อยู่ในโฟลเดอร์ skill นี้ จึงใช้ mechanical inventory จาก HTML โดยตรงและตรวจซ้ำกับ source lines/functions.

## §1 Design Tokens AS-BUILT

### §1.1 Root variables

Anchor: CSS `:root`.

| Group | Variables/value |
|---|---|
| dark shell | `--c-navy:#111111`, `--c-navy-2:#1C1C1E` |
| brand | `--c-primary:#FF3B30`, `--c-primary-hover:#E62E24`, `--c-teal:#FF9A1F`, `--c-teal-light:#FFC46B` |
| text | `--c-ink:#111111`, `--c-mute:#54565C`, `--c-mute-2:#73757B`, `--c-mute-3:#9A9CA2` |
| line/background | `--c-line:#DEDAD4`, `--c-line-2:#E9E5E0`, `--c-line-3:#F1EEEA`, `--c-bg-off:#FAF8F5` |
| semantic | `--c-success:#1F9D55`, `--c-warning:#E8870F`, `--c-danger:#E62E24` |
| shell size | `--sidebar-w:232px`, `--shell-h:52px` |

### §1.2 Typography, radius, shadow, motion

- Body font: `'Noto Sans Thai','Satoshi',system-ui,sans-serif`; sources are Google Fonts and Fontshare `<link>` elements
- Heading family: `'Noto Sans Thai',sans-serif`; code sample deliberately uses same UI stack
- Repeated radius anchors: `.btn` 8px, `.card` 10px, `.drawer` no outer radius, `.modal` 12px, pills/toggles 999px
- Shadow anchors: `.drawer`, `.modal`, `.toast`, `.sm-portal-menu`, `.mb-list/.mb-portal`
- Motion anchors: `.drawer` 280ms, `.drawer-backdrop` 220ms, `.modal` 200ms, `.toast` 250ms, common hover 120ms, `.spin` 0.7s
- Scrollbar: 5px WebKit + `scrollbar-width:thin`; `html{scrollbar-gutter:stable}`

### §1.3 Z-index map (high → low)

| z | Selector | Position/use |
|---:|---|---|
| 500 | `.sm-portal-menu`, `.mb-portal` | fixed body portal for status and Branch options |
| 80 | `.toast` | fixed bottom-right feedback |
| 60 | `.modal-backdrop`; `.mb-list` default | fixed modal layer; combobox list before portal override |
| 51 | `.drawer` | fixed right drawer |
| 50 | `.drawer-backdrop` | fixed drawer scrim |
| 30 | `.user-menu` | absolute shell account menu |
| 20 | `.sidebar` | fixed app nav |
| 19 | `.shell-bar` | sticky top bar |

## §2 Route Map

| UI route | State anchor | Entry | Refresh safety |
|---|---|---|---|
| P-01 root/list drill | `state.view='list'`, `state.sel.level='root|warehouse|zone|area|rack'` | `selectNode()` / default `state` | refresh resets to root because state is in memory |
| P-02 all Locations | `state.sel.level='all-locations'` | clickable Location `.stat` → `selectNode('all-locations',null)` | refresh resets to root |
| P-03 hierarchy | `state.view='hierarchy'` | `setView('hierarchy')` | refresh resets to list |

ไม่มี URL route, `location.hash`, `hashchange`, history state หรือ persisted route ใน HTML นี้. `renderPage()` is the page router.

## §3 Layout Shell

| Region | Anchor | AS-BUILT anatomy |
|---|---|---|
| Sidebar | `aside.sidebar`, `#sb-nav` | fixed 232px; CUBE brand; Master Data/Inventory/System modules; disabled neighbor features; UAT footer |
| Top bar | `header.shell-bar` | sticky 52px; breadcrumb; notification icon; user chip/menu |
| Main content | `main.main`, `#page-content`, `.content` | left offset by sidebar; 22px content padding; `render()` replaces page content |
| Page header | `.ph`, `.ph-title`, `.ph-count`, `.ph-sub` | name/count/subtitle; contextual actions live inside list card filter bar via `phActions()` |
| View switch | `.view-switch .seg`, `.seg-btn` | List view / Hierarchy view |
| KPI strip | `.stats`, `.stat` | Warehouse, Zone, Area, Rack, clickable Location |

Shell interaction anchors: `toggleModule()`, `toggleUserMenu()`, outside document `click`, `toggleNotif()`.

## §4 Page Anatomy

### §4.1 P-01 Warehouse & Bin — List/drill

Renderer chain: `renderPage()` → `drillPath()` + `contentBody()` → `listCard()`.

```text
#page-content
├─ .ph → .ph-title-row + .ph-sub
├─ .view-switch → .seg
├─ .stats → 5 × .stat
├─ .drill-path → .drill-chip / .drill-sep
└─ .card
   ├─ .card-head (Area subview only)
   ├─ .filter-bar → #flt-search + filters + contextual actions
   ├─ .table-scroll → table.table → row/action/status controls
   └─ .table-footer → count + .pagination
```

Per-level row anchors: `whRow()`, `znRow()`, `arRow()`, `rkRow()`, `locRow()`. Area may show `.seg` for `Racks` / `Location ตรง`; Rack/direct-Area Location lists append `.qa-row` from `quickAddRow()`.

### §4.2 P-02 Location ทั้งหมด

State: `state.sel.level==='all-locations'`; renderer `contentBody()` + `locRowFlat()`.

- card title `Location ทั้งหมด (ทุกคลัง · ข้ามชั้น)`
- search `#flt-search`; type/status `.select`; reset; checkbox `.chk`
- selection adds `.bulk-bar` from `bulkBar()`
- row click → `openView('location',id)`; status pill → `openStatusMenu()`

### §4.3 P-03 Hierarchy view

State: `state.view==='hierarchy'`; renderer `renderTree()` + `nodeSummary()`.

```text
.explorer
├─ .pane
│  ├─ .pane-head
│  └─ .tree-body → .tree-root-row / .tn / .tn-row / .tn-children
└─ .pane → .ds-head + .ds-body
```

Tree collapse uses `state.collapsed`, `toggleNode()`; selection shares `state.sel` with List view. Explorer height is `calc(100vh - 330px)`, minimum 420px; each pane owns internal scroll.

### §4.4 D-01 Parent create/edit

State: `state.drawer.mode='create|edit'` and level Warehouse/Zone/Area/Rack. Renderer `renderSimpleForm()`; handlers `captureForm()`, `submitForm()`.

- Warehouse: Branch combobox, code/name, Geo cascade/postcode
- Zone: Warehouse, code/name, temperature toggle/range
- Area: Zone, code/name, direct-Location toggle
- Rack: Area, code/name, Rows/Columns/Levels

### §4.5 D-02 Location wizard

State: drawer level Location, step 1/2; renderer `renderLocationForm()`.

- step 1 parent radio cards + parent select + code/name/type
- step 2 storage UOM/capacity/rotation/coordinates/flags/mixing/barcode
- `locNext()`, `locPrev()`, `submitLoc()`; `.stepper-band`, `.step-dot`, `.step-line`

### §4.6 D-03 Bulk generation

State `state.drawer.mode='bulk'`; renderer `renderBulkDrawer()`; `BULK_PRESETS`, `bulkPreviewNames()`, `submitBulk()`.

Sections: Area target, Rack template, Location template, five-code `.code-sample`, `.preview-box`, dynamic primary button.

### §4.7 D-04 Detail

State `state.drawer.mode='view'`; renderer `renderViewDrawer()`.

- parent nodes show full path, field grid and `ดูรายการลูก (เจาะลงระดับถัดไป)`
- Location uses `renderLocViewTabsBody()` with `ภาพรวม`, `ความจุ & flags`, `ประวัติ`
- history `.timeline` reads `auditOf(id)`

### §4.8 M-01/M-02 Modals

- M-01 `state.modal.level='status-reason'`: reason input `#sr-reason`; `confirmStatusReason()`
- M-02 typed node: `renderModal()` + `blockReason()` + `confirmModal()`; guarded destructive button has pointer-events disabled

## §5 Component Inventory + States

| Component | Selector/function | Default | Hover/focus/active | Disabled/empty/loading/error |
|---|---|---|---|---|
| primary/secondary/ghost/danger button | `.btn*` | visible by context | CSS hover | busy: `disabled`, opacity, pointer-events, spinner; no generic error state |
| text/select | `.input`, `.select` | white/line border | red focus ring | disabled gray; validation via toast/`.field-error` |
| list table | `.card .table`, `listCard()` | paged 10 | row hover | empty `.empty`; no skeleton/loading table |
| pagination | `.pg-btn`, `paginate()` | page number | hover/`.is-active` | `.is-disabled` visual class; click handler still clamps page |
| drill path | `.drill-chip`, `drillPath()` | ancestor clickable | hover | current `.is-current`; no disabled/error |
| view switch/Area segment | `.seg-btn` | inactive | `.is-active` | no disabled/loading/error |
| tree | `.tn-row`, `.tn-toggle` | expanded | hover/selected | collapsed `.tn.is-collapsed`; no empty/error renderer |
| status pill | `.pill-*`, `statusPillMenu()` | label/color | cursor/title; portal menu | no menu if `!canManage`; `full` absent from manual options |
| Branch combobox | `#f-branch-combo`, `#branch-portal` | active-only input | focus opens; hover/`.is-hl`; keyboard | empty `.mb-empty`; no loading/error state |
| radio cards | `.radio-card`, `setLocParentType()` | unselected | hover/`.is-sel` | no disabled/loading/error |
| toggle | `.toggle-track`, `toggleFormFlag()` | off | `.is-on` | no disabled/loading/error |
| drawer tabs | `.drawer-tab`, `setTab()` | overview | hover/active underline | no disabled/loading/error |
| quick add | `.qa-row`, `quickAdd()` | inputs/selects | button/input states | validation toast; no loading |
| toast | `#toast`, `showToast()` | translated off-screen | `.is-visible`; semantic class | auto dismiss after `ms`, default 2600 |

## §6 Overlay Registry

| Overlay | Anchor/render | Size/position/z | Open | Dismiss rules AS-BUILT |
|---|---|---|---|---|
| User menu | `#userMenu.user-menu`, `toggleUserMenu()` | absolute 240px / z30 | user chip click | outside document click; no Esc branch |
| Drawer | `#drawer`, `#drawerBackdrop`, `openDrawerFx()` | fixed right 680px, max 96vw / z51+50 | create/edit/view/bulk | close icon/footer, backdrop click, Esc when no higher overlay |
| Modal | `#modalEl` inside `#modalBackdrop`, `openModal()` | centered 440px, max 92vw/90vh / z60 | status reason/delete/decommission | close icon/cancel, backdrop click, Esc; modal body stops propagation |
| Branch portal | `#branch-portal.mb-portal`, `syncBranchPortal()` | fixed/body, width=input, flip-up / z500 | input focus/type/clear | selection mousedown, outside mousedown, Esc; scroll/resize repositions |
| Status portal | `#sm-portal-menu`, `openStatusMenu()` | fixed/body, min 170px, flip-up / z500 | status pill click | option, outside capture click, Esc |
| Toast | `#toast`, `showToast()` | fixed bottom-right, max 380px / z80 | function call | timer only; no click/Esc dismiss |

No scroll-lock class or focus trap exists. `preserveRenderState()` / `restoreRenderState()` restore drawer/modal/tree/page scroll and active text selection after render.

## §7 Interaction Spec

### §7.1 Esc chain

Anchor: global `window.addEventListener('keydown',...)`.

1. if `#sm-portal-menu` exists → `closeStatusMenu()` and return
2. else if `state.branchCombo.open` → `closeBranchList()` and return
3. else if `state.modal.open` → `closeModal()`
4. else if `state.drawer.open` → `closeDrawer()`

`onBranchKey()` intercepts Escape and calls `stopPropagation()`; this keeps the drawer open.

### §7.2 Click/outside/positioning

- User menu: document click outside `.user-chip/.user-menu`
- Branch portal: document `mousedown`; option selection also occurs on `mousedown` to survive node replacement; fixed position from `getBoundingClientRect()`, viewport flip, scroll/resize reposition
- Status portal: capture-phase document click; fixed position and viewport flip
- Modal backdrop closes; `.modal` stops propagation
- Drawer backdrop closes directly

### §7.3 Render/focus/loading

- `render()` replaces page/drawer/modal innerHTML, redraws icons, restores state, syncs Branch portal
- `busySubmit()` guards `_submitBusy`, disables clicked button, shows `กำลังบันทึก…`, waits 550ms then callback
- boot waits for DOM + Lucide readiness, with 5-second fallback
- no drag, pan, zoom, persisted draft or URL navigation exists

## §8 State-driven UI Matrix

### §8.1 Location status

| State | Label from `statusLabel()` | CSS | Manual option | Detail/actions |
|---|---|---|---:|---|
| `active` | `ใช้งาน` | `.pill-active` | ✅ | ordinary |
| `inactive` | `ปิดใช้`; menu text `พักใช้งาน` | `.pill-inactive` | ✅ | ordinary |
| `blocked` | `บล็อก` | `.pill-blocked` | ✅ reason modal | reason shown if present |
| `frozen` | `แช่แข็ง`; menu `Freeze (cycle count)` | `.pill-frozen` | ✅ reason modal | reason shown if present |
| `full` | `เต็ม` | `.pill-full` | — | display only |
| `decommissioned` | `ปลดระวาง` | `.pill-decommissioned` | — | destructive action hidden in view drawer |
| `maintenance` | `ซ่อมบำรุง` | `.pill-maintenance` | — | mapping exists; no seeded/manual path |

### §8.2 Permission and data conditions

| Condition | HTML behavior/anchor |
|---|---|
| `canManage=false` | `phActions()` empty; row edit/delete hidden; mutation drawer call returns `ไม่มีสิทธิ์ดำเนินการ` |
| `hasStock=true` | Location UOM select disabled; warning shown; bulk UOM skips; decommission blocked |
| Area `allows_direct=false` | direct wizard field error and `locNext()` error; Location direct action absent |
| no selection | `.bulk-bar` absent |
| submission busy | one guarded submit, spinner/disabled button |
| filters return zero | `ไม่พบรายการ` plus conditional description |

## §9 Microcopy Verbatim

### §9.1 Primary navigation/actions

`Warehouse & Bin` · `List view` · `Hierarchy view` · `เพิ่ม Warehouse` · `เพิ่ม Zone` · `เพิ่ม Area` · `เพิ่ม Rack` · `เพิ่ม Location` · `สร้างจำนวนมาก` · `แก้ไข` · `ลบ` · `ปลดระวาง` · `ยกเลิก` · `ปิด` · `ยืนยันสร้าง` · `บันทึกการแก้ไข` · `ถัดไป` · `กลับ` · `ยืนยัน` · `เพิ่มเร็ว` · `รีเซ็ต` · `ล้างที่เลือก`

### §9.2 Search/placeholders/empty/help

- `ค้นหาคลัง...`, `ค้นหา Zone...`, `ค้นหา Area...`, `ค้นหา Rack...`, `ค้นหา Location...`, `ค้นหา รหัส/ชื่อตำแหน่ง...`
- `ค้นหาสาขา (รหัส/ชื่อ)...`; empty=`ไม่พบสาขาที่เปิดใช้งานตรงกับคำค้น`; help=`แสดงเฉพาะสาขาที่เปิดใช้งาน`
- list empty title=`ไม่พบรายการ`; descriptions=`ลองปรับตัวกรอง หรือกดรีเซ็ต` / `กดปุ่มเพิ่มด้านบนเพื่อสร้างรายการแรก`
- Branch/Geo options: `— เลือกจังหวัด —`, `— เลือก —`, `เลือกจังหวัดก่อน`, `เลือกอำเภอก่อน`, `เติมอัตโนมัติจากตำบล`
- Location stocked help=`ตำแหน่งมีสต็อกอยู่ — เปลี่ยนหน่วยเก็บไม่ได้ (1 ตำแหน่ง 1 หน่วย)`

### §9.3 Validation and guard text

`กรุณากรอกรหัส` · `กรุณากรอกชื่อ` · `กรุณาเลือกสาขาสังกัด` · `กรุณากรอกช่วงอุณหภูมิ` · `กรุณาเลือก Rack` · `กรุณาเลือก Area` · `Area นี้ไม่อนุญาตวางตำแหน่งตรง — เพิ่ม Rack ก่อน` · `กรุณากรอกรหัสตำแหน่ง` · `ความจุต้องมากกว่า 0` · `รหัสซ้ำภายใน parent เดียวกัน` · `template ไม่ถูกต้อง` · `กรอกเหตุผลก่อน` · `เลือกหน่วยเก็บก่อน` · `กรอกรหัสตำแหน่งก่อน`

Guard templates from `blockReason()`:

- `ยังมี Zone อยู่ภายใต้คลังนี้ — ต้องลบ/ย้าย Zone ก่อน`
- `ยังมี Area อยู่ภายใต้ Zone นี้ — ต้องลบ/ย้าย Area ก่อน`
- `ยังมี Rack หรือ Location อยู่ภายใต้ Area นี้ — ต้องลบก่อน`
- `ยังมี Location อยู่ภายใต้ Rack นี้ — ต้องลบก่อน`
- `ตำแหน่งนี้ยังมีสต็อกอยู่ — ต้องย้ายสต็อกออก (stock=0) ก่อนปลดระวาง`

### §9.4 Dynamic toast/log templates

| Anchor | Verbatim template |
|---|---|
| `toggleNotif()` | `ไม่มีการแจ้งเตือนใหม่` |
| `openDrawer()` | `ไม่มีสิทธิ์ดำเนินการ` |
| `done()` | `(บันทึกการแก้ไข|สร้าง) {LEVEL} "{code}" (แล้ว|สำเร็จ)` |
| `submitLoc()` | `สร้างตำแหน่ง "{code}" สำเร็จ` / `บันทึกการแก้ไขแล้ว` |
| `submitBulk()` | `สร้าง {rackQty} rack × {n} ตำแหน่งสำเร็จ (atomic)` |
| `confirmModal()` | `ปลดระวางตำแหน่งแล้ว` / `ลบ {LEVEL} แล้ว` |
| `confirmStatusReason()` | `(บล็อก|Freeze) {n} ตำแหน่ง` / `{code}: {status}` |
| `applyStatus()` | `{code}: {oldStatus} → {newStatus}` |
| `bulkStatus()` | `เปลี่ยนสถานะ {n} ตำแหน่ง → {status}` |
| `bulkUom()` | `ตั้งหน่วยเก็บ "{uom}" {done} ตำแหน่ง · ข้าม {skip} (มีสต็อก — 1 ตำแหน่ง 1 หน่วย)` when skipped |
| `quickAdd()` | `เพิ่ม {code} แล้ว — แก้ความจุ/flags ต่อได้ในหน้าแก้ไข` |
| audit templates | `สร้างรายการ`, `แก้ไขข้อมูล`, `สร้างตำแหน่ง`, `สร้างจาก bulk-gen {n} ตำแหน่ง`, `เปลี่ยนสถานะ {old} → {new}`, `ตั้งหน่วยเก็บ → {uom} (bulk)`, `สร้างตำแหน่ง (quick add)` |

## §10 Data Binding & BACKEND Anchors

HTML has no literal `// BACKEND:` comments. Plug points are inferred only from explicit data comments and mutation/render functions:

| Mock/source anchor | FE plug responsibility | FRD contract |
|---|---|---|
| `WAREHOUSES/ZONES/AREAS/RACKS/LOCATIONS` | replace in-memory list/detail reads | API-01..04 |
| Branch comment + `BRANCHES`, `activeBranches()`, `branchLabel()` | active picker + saved inactive snapshot | API-22, BR-LOC-12 |
| `TH_GEO`, `geo*()` | cascade lookup/postcode | API-23, BR-LOC-13 |
| `submitForm()` | parent create/update | API-05..12 |
| `confirmModal()` parent branch | guarded parent delete | API-13 |
| `submitLoc()` | Location create/update | API-14/15 |
| `pickStatus()/confirmStatusReason()/applyStatus*()` | single/bulk state changes | API-16/18 |
| `submitBulk()` | full atomic generation | API-17 |
| `bulkUom()` | stock-aware UOM update | API-19 |
| `confirmModal()` Location branch | stock-aware decommission | API-20 |
| `AUDIT/auditOf()` | immutable timeline | API-21 / BR-LOC-14 |
| `showToast()` | map success/known validation result to exact HTML copy | `05_RULES §5.6` |

No API key, password, token, cookie, fetch/XHR client or real endpoint call is embedded in this HTML.

## §11 Three-way Traceability + Drift Log

### §11.1 Surface trace

| Brief | FRD | HTML anchor |
|---|---|---|
| §4.1 P-01 | `01_UI §1.2 P-01`, API-01/04, S-01 | `renderPage()`, `drillPath()`, `contentBody()`, `listCard()` |
| §4.2 P-02 | `01_UI P-02`, API-03/18/19, S-02/S-05 | `state.sel.level='all-locations'`, `locRowFlat()`, `bulkBar()` |
| §4.3 P-03 | `01_UI P-03`, API-02/04, S-01 | `state.view='hierarchy'`, `renderTree()`, `nodeSummary()` |
| §4.4 D-01 | `01_UI D-01`, API-05..12 | `renderSimpleForm()`, `submitForm()` |
| §4.5 D-02 | `01_UI D-02`, API-14/15, BR-LOC-02/05/06 | `renderLocationForm()`, `locNext()`, `submitLoc()` |
| §4.6 D-03 | `01_UI D-03`, API-17, BR-LOC-11 | `renderBulkDrawer()`, `submitBulk()` |
| §4.7 D-04 | `01_UI D-04`, API-04/21 | `renderViewDrawer()`, `renderLocViewTabsBody()` |
| §4.8 M-01 | `01_UI M-01`, API-16/18, BR-LOC-07 | `renderModal()`, `confirmStatusReason()` |
| §4.8 M-02 | `01_UI M-02`, API-13/20, BR-LOC-09/10 | `blockReason()`, `confirmModal()` |

### §11.2 Lock trace

| Lock | HTML evidence |
|---|---|
| LOCK-LOC-01 | Branch comment, `branch_id`, child lookup chain; HTML comment mentions implicit company but no child branch field |
| LOCK-LOC-02 | `hasStock`, storage UOM only; neighbor Inventory screens are disabled shell links |
| LOCK-LOC-03 | `ROLE`, `canManage`; no approval UI |
| LOCK-LOC-04 | Warm Light root tokens and shell CSS |
| LOCK-LOC-05 | source comments mark inferred inactive Branch/UOM rule |
| LOCK-LOC-06 | §9 copies strings from HTML functions/templates |

### §11.3 Drift Log

| ID | Direction | Evidence | Impact / required resolution |
|---|---|---|---|
| DRIFT-01 | HTML behavior vs FRD/UI field | `renderLocationForm()` enables `#f-storage-uom` when no stock, but edit branch in `submitLoc()` omits `storage_uom` | production API-15 must persist allowed UOM; TC-DRIFT-01 |
| DRIFT-02 | HTML behavior vs BR-LOC-14 | Location branch in `confirmModal()` sets `status='decommissioned'` without `AUDIT` append | production API-20 must append audit; TC-DRIFT-02 |
| DRIFT-03 | HTML mock vs atomic contract | `submitBulk()` inserts one sample Location while visible copy promises total/atomic | production API-17 creates full plan; TC-DRIFT-03 |
| DRIFT-04 | HTML-only enum | `statusLabel()`/CSS include `maintenance`, but FRD lifecycle excludes it and no manual/seed path exists | retain as unused display mapping or remove during implementation review; do not add lifecycle silently |
| DRIFT-05 | FRD-only backend behavior | optimistic locking, idempotency, RLS, dependency fail-closed and trusted capacity API have no HTML implementation | expected backend-only; test via API/integration, not prototype |

## §12 Diff from Previous HTML

— ไม่มี HTML เวอร์ชันเก่าใน input จึงไม่สามารถระบุ add/change/remove เทียบเวอร์ชันก่อน. ข้อมูลก่อนหน้า: ไม่พบข้อมูลในบทสนทนา.

## §13 💡 ข้อเสนอ (ไม่ใช่ AS-BUILT)

1. ปิด DRIFT-01..03 ใน production implementation ตาม FRD ก่อน dev handoff; ไม่จำเป็นต้องแก้ prototype หากใช้เป็น visual-only source
2. ตัดสิน DRIFT-04 พร้อม OQ lifecycle เพื่อไม่ให้ enum UI กับ backend แตกต่างกัน
3. หากต้องการ refresh/deep-link safety ให้เป็น revision ใหม่ เพราะ HTML ปัจจุบันไม่มี URL route

## Verification Gate

| Check | Result |
|---|---|
| state routes documented | 3/3 page states + 4 drawer states + 2 modal states ✅ |
| overlays in registry | 6/6 ✅ |
| `showToast()` call sites represented by static/dynamic catalog | ✅ |
| every anatomy component has selector/function anchor | ✅ |
| status enums mapped | 7/7 discovered mappings, including unused `maintenance` ✅ |
| Esc chain matches handler order | ✅ |
| z-index declarations mapped | 8 selector declarations / 7 distinct values ✅ |
| FRD surfaces paired + Drift Log explicit | 9/9 surfaces ✅ |
| sample audit of traceable claims | 10/10 ✅ |

**Verdict: PASS — FAIL=0**
