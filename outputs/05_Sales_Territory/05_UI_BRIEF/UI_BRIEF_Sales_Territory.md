# HTML UI Brief — Sales Territory

## 0. Document Control & Pairing

| Item | Value |
|---|---|
| Feature | F-05 Sales Territory / ผังเขตขาย |
| UI source of truth | `../01_HTML/sales-territory.html` (approved) |
| FRD pairing | `../04_FRD/FRD_F-05_Pack/00_OVERVIEW.md` through `06_TESTS.md` |
| Route count | 1 |
| Page ID | P-01 |
| Extraction mode | Manual targeted extraction; extraction script/template/checklist referenced by the skill package are absent |
| Scope rule | This brief records the current HTML 1:1. It does not introduce pages, controls, APIs, or business scope. |

Pairing rule: when this brief and the HTML disagree on presentation or client interaction, follow the approved HTML. When HTML behavior conflicts with the FRD business contract, do not silently choose one: use the Drift Log in §11 and obtain a BA/PM decision before production implementation.

Future-module boundary: Sales Team / Salesperson, Customer Master, Sales Order, Sales Target, and Visit Operation do not exist yet. Every visible reference to them is a fixture, mock metric, or future navigation/filter hook. F-05 must remain standalone and must not call or require those modules at runtime.

## 1. Design Tokens, Typography, Layering

### 1.1 CSS tokens extracted from `:root`

| Group | Tokens and exact values |
|---|---|
| Brand | `--c-navy:#111111`; `--c-navy-2:#111111`; `--c-primary:#FF3B30`; `--c-primary-hover:#E62E24`; `--c-teal:#FF9A1F`; `--c-teal-light:#FFB763`; `--c-orange:#FF9A1F` |
| Text | `--c-ink:#111111`; `--c-mute:#54565C`; `--c-mute-2:#73757B`; `--c-mute-3:#9A9CA2` |
| Lines/surfaces | `--c-line:#DEDAD4`; `--c-line-2:#E9E5E0`; `--c-line-3:#F1EEEA`; `--c-bg-off:#FAF8F5`; `--c-surface-2:#F1EEEA` |
| Semantic | `--c-success:#1F9D55`; `--c-warning:#E8870F`; `--c-danger:#E62E24` |
| Shell | `--sidebar-w:232px`; `--shell-h:52px` |
| Type scale | `--fs-h1:22px`; `--fs-h2:17px`; `--fs-h3:15px`; `--fs-body:14px`; `--fs-sub:13px`; `--fs-table:12.5px`; `--fs-meta:12px`; `--fs-cap:11px`; `--fs-kpi:28px` |
| Spacing | `--sp-xs:4px`; `--sp-sm:8px`; `--sp-md:12px`; `--sp-lg:20px`; `--sp-xl:28px` |
| Radius | `--r-xs:4px`; `--r-sm:6px`; `--r-md:8px`; `--r-lg:12px`; `--r-full:999px` |

Typography is `Noto Sans Thai` first, then `Satoshi`, then system sans-serif for body/form/button text. Page title uses `Satoshi`, then `Noto Sans Thai`. The HTML loads Noto Sans Thai 400/500/600/700/800 from Google Fonts and Satoshi 500/600/700 from Fontshare. Core operation must remain usable if either external font fails (BR-ST-20).

The viewport baseline is desktop-first: `body` has `min-width:768px` and `overflow:hidden`. At `max-width:1180px`, the structure table hides columns 4, 5, and 7. At `max-width:900px`, KPI cards become one column. The outer `.content` is the page's vertical scroll container (`overflow-y:auto`); the structure list must not introduce an independent vertical list scrollbar.

### 1.2 Layer and shadow map

| z-index | Token / selector | Purpose |
|---:|---|---|
| 1 | `--z-content` | Declared content baseline |
| 2 | `thead th` | Sticky table header (hard-coded in CSS) |
| 10 | `--z-sticky` | Declared sticky layer |
| 19 | `--z-shell`, `.topbar` | Top bar |
| 20 | `--z-sidebar`, `.sidebar` | Fixed sidebar |
| 30 | `--z-dropdown`; `.map-tip` | Local dropdown/tooltip layer |
| 50 | `--z-backdrop`, `.drawer-backdrop` | Drawer dimming backdrop |
| 51 | `--z-drawer`, `.drawer` | Right drawer |
| 52 | `--z-dropdown-portal`, `.cb-menu-fixed` | Master combobox menu above drawer/backdrop |
| 60 | `--z-modal`, `.modal-backdrop` | Archive confirmation modal |
| 80 | `--z-toast`, `.toast-wrap` | Toast stack |

Observed shadows: drawer `-16px 0 40px rgba(17,17,17,.16)`; dropdown `0 10px 30px rgba(17,17,17,.14)`; modal `0 24px 60px rgba(17,17,17,.25)`; toast `0 10px 30px rgba(17,17,17,.28)`; combobox menu `0 10px 28px rgba(17,17,17,.16)`; map tooltip `0 6px 20px rgba(17,17,17,.28)`.

Scrollbars are 5px WebKit / `thin` Firefox, transparent-track, charcoal translucent thumb. Sidebar uses a white translucent thumb.

## 2. Route Map

| Page | Route | Entry | Renderer | Surfaces on route |
|---|---|---|---|---|
| P-01 Sales Territory | `#/sales-territory` | active sidebar link `[data-feature="sales-territory"]` | `route()` → `render()` | tabs `structure`, `workload`, `map`; create/edit/view drawer; archive modal; combobox portal; toasts |

There is exactly one feature route. On empty hash or `#/`, `route()` assigns `#/sales-territory`. `hashchange` and `DOMContentLoaded` invoke it. As built, an unrecognized non-empty hash still renders P-01 because `route()` does not reject it; this is recorded in §11, not promoted to a product requirement.

## 3. Application Shell

- `.sidebar`: fixed 232px navigation, CUBE 4.0 mark, Sales module expanded, Platform module collapsed, `UAT · v1.0.0` footer. `toggleModule(button)` toggles `data-expanded`.
- `.topbar`: fixed-height 52px flex header; breadcrumb `Sales > ผังเขตขาย`; notification icon; user fixture `มานพ ขายเก่ง`, role `Sales · CUBE 4.0`, avatar `มข`.
- `#page-content.content.page-fill`: single render mount and outer page scroll owner.
- Page header: title `ผังเขตขาย`; subtitle `โครงสร้างเขต/เส้นทางขาย (Route) — พื้นที่ · จังหวัด · พนักงานขายผู้รับผิดชอบ · ร้านในเขตจาก survey — ใช้เป็นมิติบนเอกสารขายและรายงาน`; primary action `สร้างเขต`.
- KPI cards derive only from active fixture Routes: `Route ใช้งาน`, `จังหวัดที่ครอบคลุม`, `ร้านในเขต / ลูกค้า`, and `Coverage`. Province KPI counts only values found in the 77-province dataset; blank/invalid values do not increment it.

## 4. P-01 Page Anatomy

### 4.1 Primary tabs

`state.tab` is one of `structure`, `workload`, `map`. The visible labels are `โครงสร้างเขต`, `ภาระงาน`, and `แผนที่`. `setTab(t)` updates the tab, clears `mapHover`, clears the remembered map hover, and calls `render()`.

### 4.2 Structure tab

Selectors/anchors: `#qInput`, `.filter-bar`, `.search-box`, `.filter-select-width`, `.table-wrap`, `.region-row`, `.row-actions`.

- Search placeholder is exactly `ค้นหา รหัส / ชื่อ / จังหวัด / พนักงานขาย`; `setQ()` calls `renderKeepFocus()` so focus and caret position survive rendering.
- Status native select values/labels: `active` / `ใช้งาน`, `archived` / `เก็บเข้าคลัง`, `all` / `ทั้งหมด`.
- `filtered()` applies query and status. Rows are grouped in the fixed `REGIONS` order.
- Row click calls `openView(id)`. Row actions stop propagation before edit/archive/restore.
- Active row pill is `ใช้งาน`; archived pill is `เก็บเข้าคลัง`.
- Empty state is exactly `ไม่พบ Route`, `ลองเปลี่ยนคำค้นหรือตัวกรองสถานะ`, and button `ล้างตัวกรอง`.
- List scrolling is owned by `.content` (whole page). Table header is sticky at z=2.

### 4.3 Workload tab

`workloadBody()` builds a read-only fixture table by salesperson with customer count, required monthly work, utilization, 90-day sales, and condition label. Utilization labels are `เกินกำลัง`, `ตึงมือ`, `รับได้`; platform work displays `งานแพลตฟอร์ม` and no utilization.

Exact explanatory footer:

> งาน/เดือน = เยี่ยมลูกค้าตามความถี่ (F4×4 · F2×2 · F1×1) + เปิดร้านใหม่ (ร้าน universe ที่ยังไม่เป็นลูกค้า ÷ 3 เดือน) · capacity: GT Field 220 · Key Account 20 · B2B 30 งาน/เดือน · คำนวณเฉพาะ Route ใช้งาน

This formula and its values are `[AI-DEFAULT]` prototype fixtures (BR-ST-17/OQ-06), not a production engine or persisted KPI.

### 4.4 Map tab

Anchors/functions: `.map-canvas`, `[data-prov]`, `[data-pin]`, `.map-tip`, `mapBody()`, `mapPanel()`, `mapSetRegion()`, `mapSelect()`, `validMapPointer()`, `mapHover()`, `mapMove()`, `clearMapHover()`, `renderMapOnly()`.

- Region chips filter with `state.mapRegion='all'` or one of the 10 region labels in §5.4; changing region clears selection and hover.
- An active province path supports hover preview and click-to-pin selection. The side panel shows the hovered province first, otherwise selected province, otherwise overview.
- Selected view exposes `ยกเลิกการเลือก`; clicking a Route in the panel opens its view drawer.
- `validMapPointer(e,name)` requires a known province, coordinates inside `.map-canvas`, and a matching `[data-prov]`/`[data-pin]` target. Leaving the map calls `clearMapHover()`. A pointer outside the visible map frame must not update hover, selection, panel, or tooltip (BR-ST-19).
- `.map-tip` follows valid pointer coordinates only and is hidden after invalid/outside movement.
- Routes with no valid province stay in the non-province summary rather than being plotted.

## 5. Components and States

### 5.1 Drawer (`#drawerBackdrop`, `#drawerEl`)

Width is 680px, max 100vw. Backdrop fades at 220ms; drawer slides at 280ms. `.drawer-body` owns drawer-only vertical scrolling.

| Mode | Title | Entry | Primary controls | Exit |
|---|---|---|---|---|
| `create` | `เพิ่ม Route` | `openCreate()` / `สร้างเขต` | `ยืนยันสร้าง` | `ยกเลิก`, X, backdrop, Esc |
| `view` | `{code} — {name}` | row/map panel | active: `แก้ไข`, `เก็บเข้าคลัง`; archived: `กู้คืน` | `ปิด`, X, backdrop, Esc |
| `edit` | `แก้ไข Route — {code}` | `openEdit(id)` | `บันทึกการแก้ไข` | `ยกเลิก` or Esc returns to view; X/backdrop closes |

Create subtitle is `รหัสตั้งได้ครั้งเดียว — ใช้อ้างอิงบนเอกสารขายและรายงาน`. View/edit subtitle renders Route type, last editor, and timestamp.

View sections/labels are `ข้อมูล Route`, `รหัส Route`, `ชื่อ`, `ประเภท`, `ภาค`, `จังหวัด`, `พนักงานขาย`, `ร้านในเขต (universe)`, `สถิติในเขต`, `ลูกค้า`, `ยอด 90 วัน`, and `งาน/เดือนในเขต`. The future buttons `ดูลูกค้าในเขต ({n})` and `แผนเยี่ยมในเขต` only emit warning toasts; they do not navigate or call another module.

### 5.2 Create/edit fields

| Field / selector | HTML behavior | Visible validation/help |
|---|---|---|
| Route code / `#fld-code` | create only; uppercase pattern `A-Z 0-9 - _`, length 2–12, fixture uniqueness; immutable in edit | `ระบุรหัส A-Z 0-9 - _ ยาว 2-12 ตัว และห้ามซ้ำกับที่มีอยู่` |
| Route name / `#fld-name` | required text | `ระบุชื่อ Route` |
| Type | required native select | 10 fixed prototype values in §5.4 |
| Region | required native select | 10 labels in §5.4 |
| Province / `#fld-province`, `#cbi-prov` | searchable combobox; visible label says optional | `เว้นว่างได้ (เขตข้ามจังหวัด / ออนไลน์)` |
| Salesperson / `#fld-rep`, `#cbi-rep` | searchable fixture combobox; current HTML requires a fixture match | `1 เขตต่อพนักงานขาย 1 คน · จัดการรายชื่อที่ Salesperson`; error `เลือกพนักงานขายจากทะเบียน Sales Team / Salesperson` |
| Universe / `#universeInput` | number input, min 0, step 1; blank accepted | placeholder `กรอกจำนวนจาก survey หรือเว้นว่าง`; help `กรอกจำนวนเต็มตั้งแต่ 0 ขึ้นไปจากผลสำรวจ · เว้นว่างได้` |

Save state disables `#btn-save`, changes it to `กำลังบันทึก…`, waits 450ms in the prototype, then mutates fixture data. Invalid required fields produce warning toast `กรุณากรอกข้อมูลให้ครบถ้วน`.

### 5.3 Master combobox and portal

Selectors/functions: `#cbx-prov`, `#cbi-prov`, `#cbx-rep`, `#cbi-rep`, `#dd-portal`, `.cb-menu`, `.cb-item`, `.cb-empty`, `cbFocus`, `cbInput`, `cbKey`, `cbPick`, `cbClear`, `renderPortal`.

- State is `{key:null|'prov'|'rep', query:string, open:boolean, highlight:number}`.
- Focus/input opens the menu and resets highlight to 0. Arrow Down/Up moves within bounds, Enter selects, Esc closes. Keyboard highlight is scrolled into nearest view.
- Menu is a fixed portal above the drawer at z=52. It opens upward when less than 240px remains below and the anchor top exceeds 260px; otherwise downward. It tracks window/document scrolling and resize and preserves its own scroll position.
- Selecting closes the portal. Clear resets the selected value and returns focus to the input. Clicking outside closes surgically without re-rendering the drawer.
- Province placeholder `ค้นหาจังหวัด...`; empty `ไม่พบจังหวัด "{query}" ในชุดข้อมูลระบบ`.
- Salesperson placeholder `ค้นหาพนักงานขาย...`; empty `ไม่พบ "{query}" ในทะเบียนพนักงานขาย — เพิ่มคนใหม่ที่ Sales Team / Salesperson`.

### 5.4 Enumerations shown by HTML

Regions: `เหนือ`, `ตะวันออกเฉียงเหนือ`, `ตะวันออก`, `ตะวันออกเฉียงใต้`, `ใต้`, `ตะวันตกเฉียงใต้`, `ตะวันตก`, `ตะวันตกเฉียงเหนือ`, `ภาคกลาง`, `ส่วนกลาง / ออนไลน์`.

Route Types:

- `area`: `Area Route (GT)`
- `van`: `Van Sales`
- `wholesale`: `Wholesale (ยี่ปั๊ว/ซาปั๊ว)`
- `key_account`: `Key Account (MT)`
- `horeca`: `HORECA (โรงแรม/ร้านอาหาร/จัดเลี้ยง)`
- `b2b`: `B2B / องค์กร`
- `project`: `งานโครงการ (Project)`
- `platform`: `Platform (Online/Marketplace)`
- `telesale`: `Telesale`
- `export`: `Export (ต่างประเทศ)`

These type values are prototype compatibility only pending OQ-07/BR-ST-18.

### 5.5 Modal, toast, icon, disabled states

- Archive modal has default and submit-loading states. The primary button becomes disabled and reads `กำลังบันทึก…` for 450ms. The card itself stops backdrop click propagation.
- Restore has no confirmation modal and mutates the fixture immediately.
- Toasts use success or warning icon/tone, stack in `#toastWrap`, and self-remove after 3.5 seconds.
- Icons are rendered from the inline `ICONS` SVG path registry by `renderIcons()`; there is no runtime Lucide dependency.
- Buttons enforce a repeat-click guard while save/archive is disabled. There is no page-level loading/error/permission UI in this prototype; those production states remain FRD-only requirements.

## 6. Overlay Registry and Dismiss Rules

| Overlay family | Anchor | Opens | Explicit dismiss | Outside/backdrop | Esc priority | Focus behavior |
|---|---|---|---|---|---|---|
| Drawer | `#drawerBackdrop` + `#drawerEl` | create/view/edit | X; cancel/close | backdrop calls `closeDrawer()` | third | create/edit focuses first enabled field; no explicit trigger-focus return |
| Archive modal | `#modalBackdrop` + `#modalCard` | `openArchive(id)` | X; `ยกเลิก`; confirm completion | backdrop calls `closeModal()`; card stops propagation | second | no initial focus, trap, or return-focus implementation |
| Master combobox | `#dd-portal .cb-menu` | province/rep focus or input | pick; clear; Esc | document `mousedown` outside closes | first | input retained/restored; caret moved to end after portal re-render |
| Toast stack | `#toastWrap .toast` | seven message templates | auto after 3.5s | none | none | non-modal; no focus transfer |
| Map tooltip | `.map-tip` | valid map hover/move | mouseleave or invalid/outside pointer | outside map clears | none | pointer-only preview; selection remains separate |

Global Esc chain is exact and ordered: (1) open combobox closes; (2) open modal closes; (3) open drawer closes, except `edit` with an existing id calls `cancelEdit()` and returns to `view`. Esc handlers run in capture mode and the first two call `stopImmediatePropagation()`.

Observed limitation: create/edit dirty state is not tracked and there is no discard confirmation. The modal does not trap focus. These are descriptions of the source HTML, not new requirements.

## 7. Interaction Contracts

| User action | HTML function/state transition | Visible result | Backend target |
|---|---|---|---|
| Load empty hash | `route()` | hash becomes `#/sales-territory`; P-01 renders | none |
| Change primary tab | `setTab(t)` | chosen surface renders; map hover resets | none |
| Search/filter | `setQ`, `setStatus`, `filtered` | structure rows/empty state update; search caret retained | API-01 in production |
| Open a Route | `openView(id)` | view drawer opens | API-02 in production |
| Start create | `openCreate()` | blank form; first field focused | none until submit |
| Submit create | `save()` create branch | loading → close drawer → `สร้างเขตสำเร็จ` | API-03 |
| Start/edit Route | `openEdit(id)` | populated form; code immutable | none until submit |
| Submit edit | `save()` edit branch | loading → view drawer → `บันทึกการแก้ไขแล้ว` | API-04 |
| Archive | `openArchive` → `confirmArchive` | confirm/loading → archived → success toast | API-05 |
| Restore | `restoreRoute(id)` | active immediately → success toast | API-06 |
| Hover outside map | `validMapPointer` false → `clearMapHover` | no selection/panel mutation; tooltip hidden | none |
| Pick combobox item | `cbPick(key,i)` | form value updates; portal closes | province local dataset; salesperson fixture only |
| Future Customer action | warning toast only | no navigation/call | future hook, no API now |
| Future Visit action | warning toast only | no navigation/call | future hook, no API now |

Archive description preserves the historical snapshot boundary: archived Route is excluded from new choices/workload but old documents/reports retain their saved Route; restore is allowed. No delete action exists.

## 8. State-Driven UI Matrix

| State axis | Values | UI effect |
|---|---|---|
| `tab` | `structure` (default), `workload`, `map` | switches the single-route main body |
| `q` | empty/string | filters structure by code/name/province/salesperson |
| `status` | `active` (default), `archived`, `all` | filters rows and controls empty state |
| `drawer.open` | false/true | toggles drawer/backdrop and rendered drawer content |
| `drawer.mode` | null, `create`, `view`, `edit` | determines header, form/read view, actions, footer |
| `drawer.id` | null/Route id | selects record for view/edit |
| `form` | null/object | holds unsaved create/edit values |
| `modal.open` | false/true | archive modal visibility |
| `modal.id` | null/Route id | archive target |
| combobox `cb.key` | null, `prov`, `rep` | identifies portal owner |
| combobox `cb.open` | false/true | portal visibility |
| combobox `cb.query` | string | filters candidate rows |
| combobox `cb.highlight` | bounded integer | keyboard-selected row |
| `mapRegion` | `all` or region enum | map and panel filter |
| `mapSel` | null/province | pinned province detail |
| `mapHover` | null/province | temporary province preview; overrides selection in panel |
| Route status | `active`, `archived` | pill, actions, list filter, workload/map inclusion |
| save/archive button | enabled/loading-disabled | blocks duplicate click and shows `กำลังบันทึก…` |

State combinations that matter: modal may sit above an open view drawer; combobox portal may sit above an edit/create drawer; hover preview may temporarily replace selected province content but selection returns when hover clears; archived Routes never contribute to active KPIs/workload/map.

## 9. Microcopy Registry (verbatim)

### 9.1 Core actions and feedback

| Context | Exact text |
|---|---|
| Create action | `สร้างเขต` |
| Create drawer | `เพิ่ม Route` |
| Create submit | `ยืนยันสร้าง` |
| Edit submit | `บันทึกการแก้ไข` |
| Save loading | `กำลังบันทึก…` |
| Cancel/close | `ยกเลิก`; `ปิด` |
| Archive title/action | `เก็บ Route เข้าคลัง`; `เก็บเข้าคลัง` |
| Restore | `กู้คืน` |
| Empty | `ไม่พบ Route`; `ลองเปลี่ยนคำค้นหรือตัวกรองสถานะ`; `ล้างตัวกรอง` |

### 9.2 Toast templates: 7 call sites

1. `ทะเบียนลูกค้ายังไม่พร้อม — ระบบจะใช้เขต {code} เป็นตัวกรองเมื่อเชื่อมต่อแล้ว` (warning)
2. `แผนเยี่ยมยังไม่พร้อม — ระบบจะส่งเขต {code} เมื่อเชื่อมต่อแล้ว` (warning)
3. `กรุณากรอกข้อมูลให้ครบถ้วน` (warning)
4. `สร้างเขตสำเร็จ` (success)
5. `บันทึกการแก้ไขแล้ว` (success)
6. `เก็บ Route {code} เข้าคลังแล้ว` (success)
7. `กู้คืน Route {code} แล้ว` (success)

### 9.3 Archive body

`{code} — {name} จะไม่แสดงให้เลือกบนเอกสารใหม่ และไม่ถูกนับในภาระงานเซลส์ — เอกสาร/รายงานย้อนหลังนับเขตเดิมตามที่บันทึกบนเอกสาร กู้คืนได้ทุกเมื่อ`

Conditional warning: `เขตนี้มีลูกค้า {n} ราย ผูกอยู่ — ควรย้ายลูกค้าไป Route อื่นก่อน (ทำที่ทะเบียน Customer)`.

## 10. Data Binding and BACKEND Anchors

### 10.1 Source datasets in prototype

| Variable | Purpose | Classification |
|---|---|---|
| `THMAP` / `PROVINCES` | inline Thai map + 77-province local system dataset | local/offline system asset; HTML comment maps future read to `GET /api/system/geo/provinces` |
| `REGIONS`, `REGION_COLOR`, `TYPES` | UI enums/colors | prototype configuration; type ownership unresolved |
| `SALESPERSONS` / `SP_BY_NAME` / `REPS` | combobox/workload values | `[AI-DEFAULT]` fixture; future soft reference only |
| `ROUTES` | master records | in-memory fixture; production APIs API-01–06 |
| `CUST` | customer frequency/orders metrics | fixture/read model only; future Customer/Order hooks |
| `AUDIT` | visible fixture audit trail | in-memory fixture; production immutable audit via FN-08 |

### 10.2 Production API bindings from FRD

| API ID | UI binding | HTML function/anchor | Notes |
|---|---|---|---|
| API-01 | list/search/filter/KPI inputs | `filtered()`, `structureBody()`, `render()` | debounce, stale cancellation, pagination, errors are production work; absent in static HTML |
| API-02 | view drawer record | `openView()`, `renderDrawer()` | current fixture lookup is local |
| API-03 | create | create branch of `save()` | idempotency/version/audit enforced backend |
| API-04 | update | edit branch of `save()` | route code immutable; concurrency enforced backend |
| API-05 | archive | `confirmArchive()` | reversible; no DELETE endpoint |
| API-06 | restore | `restoreRoute()` | current fixture has immediate transition |

The only literal HTML `BACKEND:` comment identifies the system province dataset. No literal endpoint is present for the five future modules. Do not infer one. Workload, coverage, customer count, 90-day sales, and future-module buttons are explicitly non-authoritative mock/read-model surfaces.

## 11. Three-Way Traceability and Drift Log

### 11.1 Page/surface trace

| Brief | FRD | HTML evidence | Result |
|---|---|---|---|
| P-01 single route | `01_UI.md` P-01 | `href="#/sales-territory"`, `route()` | aligned |
| Structure tab | S-01 / API-01 | `structureBody()`, `filtered()` | aligned |
| Workload tab | S-02 / BR-ST-17 | `workloadBody()` | aligned as `[AI-DEFAULT]` fixture |
| Map tab | S-03 / BR-ST-19 | `mapBody()`, `validMapPointer()` | aligned |
| Create drawer | S-04 / API-03 | `openCreate()`, `save()` | aligned except D-01/D-03 |
| Edit drawer | S-05 / API-04 | `openEdit()`, `save()` | aligned except D-01/D-03 |
| View drawer | S-06 / API-02 | `openView()`, `renderDrawer()` | aligned; future actions are toast-only hooks |
| Archive modal | S-07 / API-05 | `renderModal()`, `confirmArchive()` | aligned |
| Restore action | API-06 / BR-ST-09 | `restoreRoute()` | aligned |

All FRD P-xx pages are covered: P-01 = 1/1. There are no P-02+ pages.

### 11.2 Rule anchors

- BR-ST-04/05: code format/unique-on-fixture/immutable — `save()`, `#fld-code`.
- BR-ST-06/07: optional province and 77-province dataset — `PROVINCES`, KPI filter, province combobox; see D-02.
- BR-ST-09/10: no delete; archive/restore with fixture audit — `confirmArchive()`, `restoreRoute()`, `pushAudit()`.
- BR-ST-11–13: future values are read-only fixtures and archived snapshots remain historically meaningful — workload/map/view/modal copy.
- BR-ST-15–18: overlap, green threshold, workload formula, and Route Types remain `[AI-DEFAULT]`/unresolved.
- BR-ST-19: invalid/outside pointer cannot mutate map state — `validMapPointer()`, `clearMapHover()`.
- BR-ST-20: inline icon/map assets keep core usable; external fonts have fallback stacks.

### 11.3 Drift log

| ID | Severity | Observed drift | Implementation instruction |
|---|---|---|---|
| D-01 | HIGH | HTML requires a salesperson fixture match (`!SP_BY_NAME[f.rep]`), while FRD BR-ST-03 and DB/API contract make `salesperson_ref` optional/nullable because Salesperson does not exist. | Flag for PM/BA. Do not create a hard dependency. Until resolved, faithfully reproduce the HTML required marker/validation in UI but keep backend reference nullable and provider-free. |
| D-02 | HIGH | Province combobox suggests dataset-only, but `save()` accepts an arbitrary non-empty typed string by falling back to `f.province.trim()`. FRD requires null or a versioned dataset member. | Production validation must not silently accept arbitrary province. Flag whether UI should reject/clear unmatched text; `[AI-DEFAULT]` is FRD 422 behavior. |
| D-03 | MEDIUM | HTML coerces negative, invalid, or decimal universe input through `parseInt()` and `Math.max(0, ...)`; FRD requires blank/null or integer ≥0 and a 422 validation error. | Preserve displayed input/help, but flag validation behavior. `[AI-DEFAULT]`: do not silently transform invalid production input. |
| D-04 | LOW | Any unknown non-empty hash renders P-01; FRD declares only `#/sales-territory`. | Router fallback/404 behavior is outside this feature and unresolved; do not document unknown hashes as supported routes. |
| D-05 | EXPECTED | HTML has no page/API loading, network error, 403, conflict, idempotency, or stale-request state. FRD requires these for production. | Implement from FRD without inventing another page; use states on P-01 and existing surfaces. Exact missing microcopy remains `[AI-DEFAULT]`/OQ where not defined. |
| D-06 | EXPECTED | Customer/order/target/visit/salesperson metrics and actions use fixtures/toasts. | Keep as mock/hooks until provider features exist; no current endpoints or runtime calls. |

No previous HTML version was supplied to this skill run, so old-vs-new selector diff is not applicable. Approved manual-test fixes observed in current source—Noto/Satoshi fonts, outer page scroll for Structure, central region, map pointer guard, scrollable portal dropdown, and editable universe input—are treated as current baseline.

## 12. Previous-Version Diff

Not performed: this run received one approved HTML source of truth and no paired historical HTML. The Drift Log compares the current HTML against the current FRD, not against an older prototype.

## 13. Proposals / Open Decisions

This extraction does not add UI proposals. Decisions that must remain flagged:

1. OQ/Drift D-01: should Salesperson remain optional as the BRD/FRD states, or should the approved HTML's required field become the business rule?
2. D-02: should unmatched typed province be rejected, cleared, or normalized to null? `[AI-DEFAULT]`: reject as FRD validation error.
3. D-03: should invalid universe input show field-level error instead of being silently clamped? `[AI-DEFAULT]`: reject negative/non-integer as FRD validation error.
4. OQ-07: who owns/configures Route Types? Until confirmed, use the HTML enumeration only for compatibility.
5. OQ-06: workload formula/capacity remains prototype-only; do not persist or expose it as a production engine.

## Verification Gate

| Check | Evidence/count | Verdict |
|---|---|---|
| Routes extracted | 1 HTML route; 1 brief route | PASS 1/1 |
| FRD P-xx trace | P-01 traced to route/render/surfaces | PASS 1/1 |
| Overlay families | drawer, archive modal, combobox portal, toast, map tooltip | PASS 5/5 |
| Toast call sites | 7 call sites/templates excluding function definition | PASS 7/7 |
| Primary tabs | structure/workload/map | PASS 3/3 |
| Drawer modes | create/view/edit | PASS 3/3 |
| Selectors/functions | all named anchors verified by targeted search in current HTML | PASS |
| State enumeration | all `state` and `cb` axes documented | PASS |
| Esc chain | combobox → modal → drawer; edit returns view | PASS |
| z-index layers | 10 declared tokens plus hard-coded table-header layer mapped (`1,2,10,19,20,30,50,51,52,60,80`) | PASS 11/11 |
| BACKEND/mock separation | province literal anchor + API-01–06 mapping; five future modules marked fixture/hooks only | PASS |
| 10-point no-untraceable sample | route, 3 tabs, create, edit, archive, restore, province combo, rep combo sampled against selector/function/text | PASS 10/10 |
| Untraceable invented UI | 0 | PASS |
| Known business/behavior drift | D-01–D-06 retained, not concealed | APPROVED WITH WARNINGS |

Final verdict: **APPROVED WITH WARNINGS**. The brief is extraction-complete and safe as a UI handoff when read with the Drift Log. No HTML changes were made.
