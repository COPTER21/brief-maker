# UI BRIEF — F-LOCATION-MASTER-001 · Warehouse & Bin (คลังและตำแหน่ง)

> **AS-BUILT UI spec สกัดจาก HTML prototype 1:1** — ใช้คู่กับ HTML (source of truth) + FRD Pack
> ทุกบรรทัด trace กลับหา selector / function / ข้อความจริงใน HTML ได้ (Iron Rule R1). สเปคที่ "เสนอเพิ่ม" อยู่ §13 เท่านั้น.

---

## §0 · Document Control + Pairing

| field | value |
|---|---|
| Feature id | **F-LOCATION-MASTER-001** |
| Display name | **คลังและตำแหน่ง (Warehouse & Bin)** — `<title>` L6, h1 `renderHeader` L2367, sidebar `is-active` L2457/1458, breadcrumb L1498 (D14) |
| HTML source (SoT) | `outputs/11_Warehouse/01_HTML/WarehouseBin.html` · single-file SPA · vanilla JS · 3319 บรรทัด |
| CI | v7 CUBE **Warm Light** (Ivory/Charcoal · Red #FF3B30 · Orange #FF9A1F) · Satoshi + Noto Sans Thai |
| FRD Pack | `04_FRD/FRD_F-LOCATION-MASTER-001_Pack/` (00–07 + INDEX) — **paired** (traceability §11) |
| Decisions | `00_CONTEXT/DECISION_LOG.md` D1–D15 (LOCKED) · FRD 07_LOCKED_DECISIONS LD-01…LD-13 |
| Drift status | 8 รายการใน Drift Log §11 — ทั้งหมดเป็น **dead-code/stale-comment** (D15/LD-10/LD-08) ไม่มี business drift |
| Libraries | Lucide icons v0.469.0 (multi-CDN unpkg→jsdelivr→cdnjs, L1551) · Google Fonts + Fontshare (external `<link>` L9-12) — **ต้อง self-host ตอน production** (corp firewall) |

**หลักโครง (สกัดจริง):** SPA แบบ view-switching — ไม่มี hash route (LD-08). Dual-view **List (drill-down)** + **Hierarchy Tree** (D12, NON-STANDARD approved LD-01). Header **ไม่มี role switcher** (D15/LD-10). ลำดับ 5 ระดับ **คลัง → โซน → พื้นที่ → ชั้นวาง → ตำแหน่ง**.

---

## §1 · Design Tokens AS-BUILT

### 1.1 Color / metric variables (`:root` L24-57)
| token | ค่า | token | ค่า |
|---|---|---|---|
| `--c-navy` / `--c-ink` | `#111111` | `--c-primary` | `#FF3B30` |
| `--c-primary-hover` | `#E62E24` | `--c-teal` | `#FF9A1F` |
| `--c-teal-light` | `#FFB763` | `--c-mute` / `-2` / `-3` | `#54565C` / `#73757B` / `#9A9CA2` |
| `--c-line` / `-2` / `-3` | `#DEDAD4` / `#E9E5E0` / `#F1EEEA` | `--c-bg-off` | `#FAF8F5` |
| `--c-success` | `#1F9D55` | `--c-warning` | `#E8870F` |
| `--c-danger` | `#E62E24` | `--sidebar-w` / `--shell-h` | `232px` / `52px` |

- **Type scale** (L44-52): h1 22 / h2 17 / h3 15 / body 14 / sub 13 / meta 12 / cap 11 / kpi 28. (หมายเหตุ: `.ph-title` L361 render จริงที่ **20px**, `.stat-value` 26px — override token.)
- **Spacing** (L54): xs4 sm8 md12 lg20 xl28 · **Radius** (L56): xs4 sm6 md8 lg12 full999.
- **Scrollbar** (Iron #49, L66-77): width 5px · thumb `rgba(17,17,17,.14)` · dark panel (`.sidebar`,`.slide`) thumb `rgba(255,255,255,.28)`.
- `body min-width:1180px` (L86) — admin tool บังคับ horizontal scroll บนจอแคบ.

### 1.2 z-index map (สูง→ต่ำ · def L1319-1320, override L1323)
| z | token | ใช้ที่ | selector |
|---|---|---|---|
| **95** | `--z-toast` | Toast | `.toast` L1162 |
| **70** | `--z-modal` | Modal backdrop (override — ต้องอยู่เหนือ drawer) | `.modal-backdrop` L1323 |
| **55** | `--z-drawer` | Drawer panel | `.drawer` L846 |
| **50** | `--z-backdrop` | Drawer backdrop · combobox list | `.drawer-backdrop` L834 · `.ss-list` L539 |
| **40** | `--z-dropdown` | User menu · tooltip | `.user-menu` L313 · `.info-tip::after` L1310 |
| **30** | `--z-sticky` | Shell bar · wizard footer | `.shell-bar` L241 · `.wizard-footer` L1217 |
| **20** | `--z-shell` | Sidebar | `.sidebar` L104 |
| local | `3` / `2` / `1` | sticky `<th>` L599 · stepper-circle L819 · stepper line L825 | — |

> **สำคัญ:** modal (70) > drawer (55) โดยเจตนา — delete/decommission/block modal เปิดจากใน view-drawer แล้วต้องซ้อนทับ (comment L1322).

---

## §2 · Route Map (state-driven — NO hash · LD-08)

Prototype สลับหน้าด้วย **state** ไม่ใช่ URL. "route" = identifier ในโค้ดจริง.

| Screen | identifier จริง | ค่า | เปิดด้วย fn |
|---|---|---|---|
| List view | `state.view` | `'list'` (default L1998) | `setView('list')` L2212 |
| Hierarchy Tree | `state.view` | `'tree'` | `setView('tree')` L2212 (เรียก `expandToSel`) |
| Node form (WH/Zone/Area/Rack) | `state.drawer.view` | `'node-form'` | `openNodeCreate/openNodeEdit` L2642/2651 |
| Location form (2-step) | `state.drawer.view` | `'loc-form'` (+`state.drawer.step` 1\|2) | `openLocCreate/openLocEdit` L2657/2661 |
| Bulk Generate | `state.drawer.view` | `'bulk'` | `openBulk` L2664 |
| View Node | `state.drawer.view` | `'view-node'` | `openViewNode` L2662 |
| View Location (3 tabs) | `state.drawer.view` | `'view-loc'` (+`state.drawer.tab`) | `openViewLoc` L2663 |
| Confirm modal | `state.modal.type` | `'delete-node'` \| `'decommission'` \| `'block'` | `askDeleteNode/askDecommission/askBlock` L3163-3165 |

- **Drill state** = `state.drill{wh,zone,area,rack}` (L1997) → `curLevel()` L2186 คำนวณระดับปัจจุบัน (root→warehouse→zone→area→rack).
- **Shared selection** `state.sel` (L1999) = derived จาก drill ทุก render (`selFromDrill` L2230) → List ↔ Tree ใช้ selection เดียวกัน (S-10).
- **Refresh-safety:** ไม่มี — state อยู่ใน memory, refresh = กลับ default (loading→list root). Master `render()` L2168.
- **Master render fan-out** L2168-2178: `renderPage()` → #page-content · `renderDrawer()` → #drawer (ถ้า open) · `renderModal()` → #modalBackdrop .modal (ถ้า open) · `syncRoleChip()` · `renderIcons()` · `restoreRenderState()` · `initComboboxes()`.

---

## §3 · Layout Shell

| region | selector | ขนาด/พฤติกรรม | anchor |
|---|---|---|---|
| Sidebar | `.sidebar` (static HTML L1444) | fixed left, width **232px**, พื้น `#111111` | — |
| Brand | `.sb-brand` | logo (warehouse icon) + "**Warm Light**" / "คลังสินค้า" | L1445-1448 |
| Nav modules | `.sb-module[data-expanded]` | collapsible group (Iron #27), header non-navigable | `toggleModule` L1599 |
| — ข้อมูลหลัก | expanded | **คลังและตำแหน่ง** `is-active` · สินค้า/หน่วยนับ `is-disabled` | L1450-1467 |
| — ปฏิบัติการคลัง | expanded | GRN / จัดหยิบสินค้า (ทั้งคู่ `is-disabled`) | L1468-1478 |
| — ระบบ | collapsed | ตั้งค่า `is-disabled` | L1479-1488 |
| Sidebar footer | `.sb-footer` | pulse-dot + "**Prototype · v7**" | L1490 |
| Main | `.main` | `margin-left:232px` | L225 |
| **Shell bar** | `.shell-bar` (static L1494) | sticky top, height **52px**, พื้นขาว | L1494-1517 |
| — Breadcrumb | `.breadcrumb` | "**ข้อมูลหลัก › คลังและตำแหน่ง**" (static — ไม่ใช่ drill) | L1495-1499 |
| — Notif bell | `.icon-btn#notifBtn` | click → toast "ไม่มีการแจ้งเตือนใหม่" | L1502 |
| — User chip | `.user-chip` | name/role/avatar — อัปเดตจาก `state.role` โดย `syncRoleChip` L2179; click → user-menu | L1505-1514 |
| — User menu | `.user-menu#userMenu` | โปรไฟล์ / การตั้งค่า / **ออกจากระบบ** (danger) | L1509-1514, `toggleUserMenu` L3270 |
| **Header (page)** | `.ph` via `renderHeader` L2359 | h1 + count pill + sub + [สร้างจำนวนมาก][สร้าง…] | — |
| Content host | `.content#page-content` | render target (`renderPage`) | L1518 |

> **D15 / LD-10 (CRITICAL):** shell-bar มี **เฉพาะ** breadcrumb + bell + user-chip — **ไม่มี role switcher**. `syncRoleChip()` เพียง sync ป้ายชื่อจาก `state.role` (ไม่ใช่ switcher). `setRole()` (L2588) และ CSS `.role-switch/.role-switch-label/.role-select` (L3304-3306) = **dead code** (ดู Drift D-1/D-2).

---

## §4 · Page Anatomy

### P-01 · List view (`state.view='list'`) — `renderPage` L2199 → `renderCard` L2429
```
renderHeader (L2359)  h1 "คลังและตำแหน่ง (Warehouse & Bin)" + .ph-count "{n} {childLabel}" + .ph-sub + [สร้างจำนวนมาก?][สร้าง{level}]
renderViewSwitcher (L2206)  .seg-control: [มุมมองรายการ][มุมมองลำดับชั้น]
renderKpi (L2375)  .stats → 5 tiles: คลัง(Warehouse)/โซน(Zone)/พื้นที่(Area)/ชั้นวาง(Rack)/ตำแหน่ง
renderDrill (L2394)  .drill-bc chips: ทุกคลัง › WH(code) › Zone(name) › Area(name) › Rack(name)
.card
 ├─ card-head (area level เท่านั้น, L2446)  seg [ชั้นวาง][ตำแหน่งตรง] เมื่อ allows_direct
 ├─ filter-bar (L2439)  [branch combobox @root] [search] [type sel][status sel @loc] [รีเซ็ต]
 ├─ table-scroll.is-sticky → renderTable (L2494) / renderTableHead (L2557)
 └─ renderFooter (L2574)  pagesize [10/20/50] + "{s}–{e} จาก {total} รายการ" + pagination
```
- คอลัมน์ต่อระดับ (`renderTableHead` L2557): **root** รหัส/ชื่อคลัง/สาขา/ที่อยู่/โซน(num)/สถานะ · **wh** รหัส/ชื่อโซน/อุณหภูมิ/พื้นที่(num)/สถานะ · **zone** รหัส/ชื่อพื้นที่/วางตำแหน่งตรง?/ชั้นวาง(num)/ตำแหน่งตรง(num)/สถานะ · **area·racks** รหัส/ชื่อชั้นวาง/ขนาด(R×C×L)/ตำแหน่ง(num)/สถานะ · **loc** รหัส/ชื่อ/ประเภท/ความจุ/หมุนเวียน/สถานะ.
- แถว clickable → drill ระดับถัดไป (`drillInto` L2596); แถว location → เปิด view-loc (`openViewLoc` L2545). Row actions `rowActionsNode/rowActionsLoc` L2472/2480.
- **สาขา** ยังเป็นคอลัมน์ root (L2506) + filter (branch combobox) — **แต่ไม่อยู่ใน path** (D15/LD-05).

### P-02 · Hierarchy Tree (`state.view='tree'`) — `renderTreeView` L2250 (NON-STANDARD · LD-01)
```
.tree-layout
 ├─ .tree-pane → renderTree (L2256) / treeNode (L2261)  WH>Zone>Area>Rack collapsible
 │     row: [chevron toggle][level icon][code mono][name][level badge][child count]
 └─ renderNodeSummary (L2281)  icon+eyebrow, code+status pill, Full Path, def-grid, child stat chips, actions
```
- Rack เป็น leaf ของ tree — Locations ไม่โผล่เป็น tree node (แสดงใน summary/List, comment L2248).
- `treeSelect` L2241 · `toggleTreeNode` L2240 · chip → List `chipToList` L2324 · summary actions: เพิ่มลูก/แก้ไข/จัดเก็บ (gated) L2304-2308.
- **UX-08 gap (LD-02):** `.tree-row` มี `onclick` เท่านั้น — **ไม่มี keyboard/arrow-key nav** → บันทึกเป็น known accessibility gap (ดู §8 / dev-handoff).

### P-03…P-08 (drawer/modal) — anatomy สรุปใน §6 Overlay Registry + §5 Component states.

---

## §5 · Component Inventory (anchor + states — R4)

| Component | selector · fn | states (จริงในโค้ด) |
|---|---|---|
| Primary/secondary/ghost/danger btn | `.btn-*` L408-418 | default·hover·`:disabled/.is-disabled`(opacity .55, pointer-events none) L402. loading = `submitBtnLoading` L3035 (spinner + "กำลังบันทึก…"). |
| View switcher | `.seg-control .seg-item` `renderViewSwitcher` L2206 | `.is-active` (view ปัจจุบัน) · aria-selected · hover |
| Area sub-tab | `.seg-control` `setAreaTab` L2594 | racks/locs · โผล่เฉพาะ `area.allows_direct=true` L2449 |
| Master Combobox (#94) | `.search-select` `searchSelectHTML` L1729 · `initSearchSelect` L1742 | closed·open·query/filter·highlight `.ss-opt.is-active`·selected(caret→clear)·empty `.ss-empty` (emptyText). keyboard ↑↓/Enter/Esc `ssOnKey` L1798. ใช้ที่ branch filter/branch/prov/dist/subd/wh/zone/area/rack/btarget (`initComboboxes` L3242) |
| Status pill | `.pill` `pillHtml` L2488 · `statusPill` L2028 | 8 map (ดู §8) — color=state (D10/LD-09) |
| Type pill | `.type-pill` `typePillHtml` L2487 | neutral pill เดียว, แยกด้วย **icon+label** ไม่ color-code (10 types, `TYPE_ICON` L2019) |
| Behavior/mixing flag chip | `.flag-chip` `locFlagsHtml` L2489 / `flag()` L2922 | on (`.on` primary tint) / off (grey) |
| Toggle row | `.tgl-row` `tglRow` L3024 · `toggleField` L3025 | on `.tgl.on` / off — คลิกทั้งแถว (Iron #20) |
| Radio card (parent XOR) | `.radio-card` L1359 `setParentType` L2831 | `.is-sel` (rack XOR area) |
| Stepper (2-step) | `.d-stepper` `stepper2` L2762 | active / done (check icon) / upcoming |
| KPI tile | `.stat` `renderKpi` L2375 | hover — 5 tiles คงที่ |
| Drill chip | `.drill-chip` `renderDrill` L2394 | default·hover·`.is-current` (ink bg, ปัจจุบัน) · `.is-branch` **มี CSS แต่ไม่ถูก render** (D15 dead, Drift D-4) |
| Table | `.table` `renderTable` L2494 | row hover · `.is-clickable`(cursor) · sticky header · empty→`renderEmpty` L2567 |
| Inline-warn | `.inline-warn` | allows_direct=false (L2792) · barcode-before-activate (L2828/2936) · bulk zero (L3006) |
| Preview box | `.preview-box` L1375 `renderBulk` L3005 | live recompute `bulkCalc` L2962 (onchange `captureBulkAndRender` L3016) |
| Collision box | `.collision-box` | โผล่เมื่อ `bulkCollisions` L2969 length>0 |
| Empty state | `.empty` `emptyStateHTML` L1845 | filtered ("ไม่พบรายการที่ค้นหา") vs ว่างจริง ("ยังไม่มี{lvl}") L2567 |
| Loading skeleton | `.sk-line` `renderLoading` L2337 | boot 550ms (`state.loading` L1995→L3281) |
| Error state | `.empty` (danger) `renderErrorState` L2346 | `!drillValid()` L2201 → drill ชี้ node ที่หายแล้ว |

---

## §6 · Overlay Registry (ขนาด + dismiss rules — R5)

| overlay | selector | ขนาด | backdrop | เปิด | **dismiss** | z |
|---|---|---|---|---|---|---|
| **Drawer (wide)** | `.drawer` | **920px** (max 96vw) | `.drawer-backdrop` `rgba(17,17,17,.40)` | `openDrawerView` L2623 | backdrop click `closeDrawer()` (L1522) · ปุ่ม X (`.top-icon-btn`) · Esc · ปุ่มยกเลิก/ปิด | 55 |
| **Drawer (standard)** | `.drawer.standard` | **680px** | เหมือนบน | เหมือนบน (`standard=true`) | เหมือนบน | 55 |
| **Modal** | `.modal` | **440px** (max 92vw / 90vh) | `.modal-backdrop` `rgba(17,17,17,.50)` | `openModal` L2638 | backdrop click `closeModal()` (L1528) · X · Esc · ยกเลิก/เข้าใจแล้ว. inner `.modal` มี `stopPropagation` L1529 | 70 |
| **Combobox list** | `.ss-list` | absolute overlay (max-h 280) | — (no backdrop, ไม่ดันเนื้อหา) | focus/typing | click-outside `document click` L1805 · Esc (capture L3274) · เลือก option | 50 |
| **User menu** | `.user-menu` | 240px dropdown | — | `toggleUserMenu` L3270 | click-outside L3271 | 40 |
| **Toast** | `.toast` | bottom-right, max 380 | — | `showToast` L1654 | auto-hide (default 2800ms) | 95 |

**ขนาด drawer ที่ใช้จริง:** node-form/view-node = **wide 920** (`openDrawerView(...,true)`); loc-form/view-loc/bulk = **standard 680** (`...,false`). ตั้งโดย `setDrawerWidth` L2622.

**Dismiss เฉพาะเคส:**
- **block modal** ต้องกรอกเหตุผลจึงจะ confirm (`confirmBlock` L3232, toast "ระบุเหตุผลที่บล็อก") — แต่ยัง **ยกเลิก/Esc ได้** (ไม่ใช่ "ห้ามปิด").
- **delete-node / decommission block variant** (มีลูก active / มีสต็อก): footer เหลือปุ่มเดียว "เข้าใจแล้ว" (`.btn-secondary`) — ไม่มีปุ่มยืนยัน (บล็อกจริง) L3186/3196.
- ไม่มี overlay ประเภท "ห้ามปิด" ในไฟล์นี้.

---

## §7 · Interaction Spec

### 7.1 Esc chain (ลำดับ handler จริง — มี 3 ตัว)
1. **Feature capture-phase** `keydown` (L3274, `useCapture=true`) — วิ่งก่อน: ถ้ามี combobox เปิด (`window.__ss[k].open`) → ปิด combobox ทั้งหมด + `stopImmediatePropagation()` (drawer/modal **ไม่ถูกปิด**).
2. **Base-kit bubble-phase** `keydown` (L1667) — ถ้าไม่มี combobox เปิด: `state.modal.open` → `closeModal()` **else** `state.drawer.open` → `closeDrawer()`.
3. **Combobox local** `ssOnKey` Esc (L1803) — ปิด list เฉพาะ combobox ที่ focus (เมื่อพิมพ์อยู่ใน input).
> สรุปพฤติกรรม: Esc → ปิด combobox ก่อน; Esc อีกครั้ง → ปิด modal (ถ้าเปิด) ไม่งั้นปิด drawer. (ตรง FRD 01_UI §1.0 "Esc chain: ปิด combobox ก่อน drawer/modal".)

### 7.2 Click-outside
- Combobox: `document.click` L1805 → ปิด list ทุกตัวที่ไม่ได้คลิกใน wrap.
- User menu: `document.click` L3271.
- Drawer/Modal backdrop: `onclick` inline (L1522/1528) → close.
- `[data-overlay]` base-kit `openOverlay/closeOverlay` L1980-1984 = base-kit util (feature ไม่ได้ใช้ overlay pattern นี้).

### 7.3 Focus / render preservation
- `preserveRenderState`/`restoreRenderState` L1885/1903 (Iron #29) — เก็บ scrollTop drawer/modal/page + focus+selection ของ input ที่กำลังพิมพ์ (match ด้วย placeholder+type+name) ทุกครั้งที่ `render()` rebuild innerHTML.
- Drawer/Modal เปิดด้วย `requestAnimationFrame` เพื่อ trigger CSS transition (`.is-open`), ปิดด้วย `setTimeout` 280ms/200ms ให้ animation จบก่อนล้าง state.
- Combobox `onmousedown="event.preventDefault()"` L1783 กัน blur ก่อน click option.

### 7.4 Positioning
- Sidebar/shell-bar = `fixed`/`sticky` (L99/L233). Drawer/backdrop/modal = `fixed inset:0`. Combobox list = `absolute` overlay (ไม่ดันเนื้อหา, สอดคล้อง Iron #35 scrollbar-gutter stable).

---

## §8 · State-Driven UI Matrix

### 8.1 Status → pill (`statusLabel` L2027 · `statusPill` L2028 — verbatim)
| status | label (TH) | pill class | สี (D10/LD-09) |
|---|---|---|---|
| active | ใช้งาน | `pill-info` | ฟ้า `#E6F0FF/#1A5FCC` |
| inactive | ปิดใช้ | `pill-muted` | grey |
| blocked | บล็อก | `pill-danger` | แดง `#FFE9E7/#E62E24` |
| maintenance | ซ่อมบำรุง | `pill-maintenance` | orange tint `rgba(255,154,31,.18)/#B8690B` L1326 |
| full | เต็ม | `pill-full` | amber `#FFF1DD/#B8690B` L1325 |
| frozen | แช่แข็ง | `pill-frozen` | grey `--c-line-3/--c-mute-2` L1327 |
| decommissioned | ปลดระวาง | `pill-decommissioned` | faded grey L1328 |
| archived | จัดเก็บแล้ว | `pill-decommissioned` (reuse) | faded grey |

### 8.2 RBAC → UI (`perms()` L2037, `state.role='manager'` default L1994)
| role | create | del | status | UI ผล |
|---|---|---|---|---|
| operator | ✗ | ✗ | ✗ | ปุ่มสร้าง/bulk `is-disabled`+tooltip "**บทบาทนี้ไม่มีสิทธิ์สร้าง (ดูอย่างเดียว)**" (L2362); ไม่มี edit/archive/decommission |
| supervisor | ✓ | ✗ | ✓ | archive tooltip "**จัดเก็บได้เฉพาะผู้จัดการ/ผู้ดูแลระบบ**" (L2477); decommission tooltip "**ปลดระวางได้เฉพาะผู้จัดการ/ผู้ดูแลระบบ**" (L2484) |
| controller | ✗(create) | ✗ | ✓ | เหมือน supervisor ด้าน del |
| manager / admin | ✓ | ✓ | ✓ | ครบ |

### 8.3 Location status transitions (viewLocCapacity L2921)
- **active** → [บล็อก](modal reason) / [แช่แข็ง] / [ซ่อมบำรุง] (ถ้า `perms.status`) + [ปิดใช้งาน] (ถ้า `perms.create`).
- **blocked/frozen/maintenance/inactive/full** → [เปิดใช้งาน] (primary). Gate: ต้องมี barcode ถ้า `LOC_REQUIRE_BARCODE` (L2932/3159) → inline-warn ถ้าไม่มี (L2936).
- **decommissioned** = terminal — ไม่มีปุ่มจัดการสถานะ.
- Node (WH/Zone/Area/Rack): active → archived (soft) เท่านั้น.

### 8.4 Level → labels (verbatim)
- `levelChildLabel` L2355 / `createLabel` L2356: root→คลัง/สร้างคลัง · warehouse→โซน/สร้างโซน · zone→พื้นที่/สร้างพื้นที่ · area→(locs?ตำแหน่งตรง:ชั้นวาง) · rack→ตำแหน่ง/สร้างตำแหน่ง.

---

## §9 · Microcopy (verbatim — R2)

### 9.1 Toast (`showToast` — ทุก call)
| ข้อความ | variant | anchor |
|---|---|---|
| `ไม่มีการแจ้งเตือนใหม่` | info | L1502 |
| `กรุณากรอกข้อมูลให้ครบถ้วน` | warning | L3052/3085/3097 |
| `สร้าง{คลัง\|โซน\|พื้นที่\|ชั้นวาง} "{code}" สำเร็จ` | success | L3062 |
| `บันทึกการแก้ไขแล้ว` | success | L3071/3125 |
| `รหัสซ้ำภายใน parent เดียวกัน` | warning | L3098 |
| `ต้องย้ายสต็อกออกก่อนย้ายตำแหน่ง (stock = 0)` | warning | L3107 |
| `สร้างตำแหน่ง "{code}" สำเร็จ (ปิดใช้ — ต้องเพิ่มบาร์โค้ดก่อนเปิดใช้งาน)` | success | L3120 |
| `ไม่สามารถสร้างได้ — ตรวจแม่แบบ/รหัสชน` | warning | L3132 |
| `ความจุต้องมากกว่า 0` | warning | L3133 |
| `สร้าง {N} ชั้นวาง × {M} ตำแหน่งสำเร็จ (atomic)` | success | L3149 |
| `ต้องเพิ่มบาร์โค้ดก่อนถึงจะเปิดใช้งานตำแหน่งได้` | warning | L3159 |
| `เปลี่ยนสถานะเป็น "{label}" แล้ว` | success | L3161 |
| `จัดเก็บ{คลัง\|โซน\|พื้นที่\|ชั้นวาง}แล้ว` | success | L3225 |
| `ปลดระวางตำแหน่งแล้ว` | success | L3230 |
| `ระบุเหตุผลที่บล็อก` | warning | L3234 |
| `บล็อกตำแหน่งแล้ว` | success | L3236 |

### 9.2 Validation error (state.errors — verbatim)
`กรุณากรอกรหัส` (L3040) · `กรุณากรอกชื่อ` (L3041) · `กรุณาเลือกสาขา` (L3044) · `รหัสซ้ำในระบบ` (L3044) · `กรุณาเลือกคลัง` / `รหัสซ้ำภายในคลังเดียวกัน` (L3045) · `กรุณากรอกช่วงอุณหภูมิ` / `อุณหภูมิต่ำสุดต้องไม่เกินสูงสุด` (L3046) · `กรุณาเลือกโซน` / `รหัสซ้ำภายในโซนเดียวกัน` (L3047) · `ปิด allows_direct ไม่ได้ — ยังมีตำแหน่งวางตรงอยู่ {n} รายการ` (L3049) · `กรุณาเลือกพื้นที่` / `รหัสซ้ำภายในพื้นที่เดียวกัน` (L3050) · `กรุณาเลือกชั้นวาง` (L3081) · `พื้นที่นี้ allows_direct = false — เลือกพื้นที่อื่น หรือเพิ่มชั้นวางก่อน` (L3082) · `กรุณากรอกรหัสตำแหน่ง` (L3083) · `ความจุต้องมากกว่า 0` (L3091).

### 9.3 Empty / error / inline-warn (verbatim)
- Tree empty: "**ยังไม่มีคลัง**" / "เริ่มต้นด้วยการสร้างคลังแรกของคุณ" (L2258).
- Summary empty: "**เลือกโหนดจากผังด้านซ้าย**" / "คลิกคลัง โซน พื้นที่ หรือชั้นวาง เพื่อดูรายละเอียดและรายการลูก" (L2287).
- List filtered empty: "**ไม่พบรายการที่ค้นหา**" / "ลองปรับคำค้นหรือล้างตัวกรอง" / ปุ่ม "ล้างตัวกรอง" (L2569).
- List empty: "**ยังไม่มี{lvl}**" / "เริ่มต้นด้วยการสร้าง{lvl}แรกของคุณ" (L2572).
- Error state: "**ไม่พบข้อมูลที่กำลังดู**" / "รายการที่คุณกำลังเจาะดูอาจถูกลบหรือย้ายไปแล้ว กรุณากลับไปที่รายการคลังทั้งหมด" / ปุ่ม "กลับไปหน้ารายการ" (L2349-2351).
- History empty: "**ยังไม่มีประวัติ**" / "การเปลี่ยนแปลงทั้งหมดจะถูกบันทึกที่นี่ (WORM)" (L2951).
- allows_direct inline-warn: "พื้นที่ {code} ตั้งค่า allows_direct = false — วางตำแหน่งตรงไม่ได้ ต้องเลือกพื้นที่อื่น หรือ **เพิ่มชั้นวางในพื้นที่นี้ก่อน**" (L2792).
- barcode inline-warn (form): "ตำแหน่งต้องมีบาร์โค้ดก่อนถึงจะเปิดใช้งานได้ — ถ้ายังไม่กรอกตอนนี้ ระบบจะบันทึกไว้เป็นสถานะ **"ปิดใช้"** …" (L2828).
- bulk zero: "แม่แบบไม่ถูกต้อง — จำนวนที่จะสร้างต้องมากกว่า 0 (ตรวจ rows/cols/levels/จำนวนชั้นวาง)" (L3006).
- bulk collision: "**พบรหัสชน {n} รายการ** — การสร้างถูกบล็อก (atomic ไม่มี partial commit)" (L3007).

### 9.4 Modal microcopy (`renderModal` L3175)
- delete-node block: title "**จัดเก็บ{lbl}ไม่ได้**"; body "จัดเก็บไม่ได้ — ยังมีรายการลูกใช้งานอยู่ {n} รายการ" + blockMsg ต่อ kind (L3182); footer "เข้าใจแล้ว".
- delete-node confirm: title "**จัดเก็บ{lbl}**"; "…เก็บประวัติไว้ (soft — ไม่ลบถาวร) การกระทำนี้ถูกบันทึกใน audit log"; ปุ่ม "ยกเลิก"/"จัดเก็บ".
- decommission block: "**ปลดระวางไม่ได้**" / "ต้องย้ายสต็อกออกก่อน … (BR-010)".
- decommission confirm: "**ปลดระวางตำแหน่ง**" / "ตำแหน่งจะถูกตั้งเป็น **decommissioned** …"; ปุ่ม "ปลดระวาง".
- block: "**บล็อกตำแหน่ง**" / "บล็อก {code} — ต้องระบุเหตุผล"; field "เหตุผลที่บล็อก *" placeholder "เช่น รอซ่อมคานชั้นวาง".

### 9.5 Buttons / labels สำคัญ (verbatim)
สร้างจำนวนมาก (L2365) · ยืนยันสร้าง / บันทึกการแก้ไข (L2752/2781) · ถัดไป / กลับ / ยกเลิก · ดูรายการลูก (เจาะลงระดับถัดไป) (L2868) · เพิ่มลูก / แก้ไข / จัดเก็บ / ปลดระวาง · เปิดใช้งาน / ปิดใช้งาน / บล็อก / แช่แข็ง / ซ่อมบำรุง · มุมมองรายการ / มุมมองลำดับชั้น · รีเซ็ต / ล้างตัวกรอง · "{n}/หน้า" · "กำลังบันทึก…" (L3035). Tab: ภาพรวม / ความจุ & flags / ประวัติ (L2898). Stepper: "ต้นทาง & ข้อมูลระบุ" / "ความจุ & พฤติกรรม" (L2764).

---

## §10 · Data Binding & BACKEND anchors

> Prototype ใช้ in-memory mock arrays — dev แทนด้วย API (map ↔ 02_API §11). ไม่มี `// BACKEND:` comment ในไฟล์ แต่ mutation points ชัดเจน.

| mock array / fn | ข้อมูล | ↔ API |
|---|---|---|
| `WAREHOUSES` L2065 (`branch_id`, geo, status) | root list | WHB-API-01/03/04/05 |
| `ZONES/AREAS/RACKS` L2070/2077/2086 | drill children | WHB-API-02/03/04/05 |
| `LOCATIONS` L2094 (`mkLoc` L2093 — parent_type XOR, cap, behavior/mixing flags, `hasStock`, barcode) | locations | WHB-API-07/08/09/10/11/12 |
| `BRANCHES` L2011 / `TH_GEO` L2044 (geo cascade `geoProvinces/Districts/Subs/Postcode` L2051-2054) | reference (mock) | WHB-API-15/16 (LD-12 Phase 2) |
| `hasStock` field (seed) | reparent/decommission gate | WHB-API-17 (`GET /locations/:id/stock`, BR-010/012) |
| `AUDIT` L2112 / `logAudit` L2119 / `auditOf` L2118 | WORM history tab | WHB-API-18 |
| `LOC_REQUIRE_BARCODE` L2008 (`=true`) | config `loc_require_barcode` (BR-014) | WHB-API-08/11 |
| submit fns: `submitNode` L3038 · `submitLoc` L3089 · `submitBulk` L3131 (racks+locs loop) · `confirmDeleteNode` L3217 (status='archived', **ไม่ลบจริง**) · `confirmDecommission` L3228 · `confirmBlock` L3232 · `setLocStatus` L3157 | mutations (setTimeout 500-600ms sim latency) | WHB-API-03/04/05/08/09/11/12/13/14 |
| `bulkCalc` L2962 / `bulkCollisions` L2969 / `bulkSampleCode` L2968 | preview + collision | WHB-API-13 (ENG-BULK-PLAN) |
| `fullPathStr` L2161 / `pathChips` L2145 | full path builder | ENG-HIER-PATH (03_LOGIC) |

**Path builder (D15/LD-05 — สกัดจริง L2154-2158):** `pathChips` push **WH=code**, zone=**name**, area=**name**, rack=**name**, location=**code** — **ไม่มี branch**. (comment L2144 "branch › WH…" เป็น stale — code ไม่ push branch; ดู Drift D-5.)

---

## §11 · Traceability + Drift Log

### 11.1 3-way (Brief §x ↔ FRD ↔ HTML)
| Brief | FRD | HTML anchor |
|---|---|---|
| §4 P-01 List | 01_UI P-01 · WHB-API-01/02/07 | `renderCard` L2429 / `renderTable` L2494 |
| §4 P-02 Tree | 01_UI P-02 (LD-01) | `renderTreeView` L2250 |
| §5/§6 P-03 Node form | 01_UI P-03 · WHB-API-03/04 | `renderNodeForm` L2697 / `submitNode` L3038 |
| §6 P-04 Loc form 2-step | 01_UI P-04 · WHB-API-08 · BR-002/003/006/014 | `renderLocForm` L2766 / `submitLoc` L3089 |
| §6 P-05 Bulk | 01_UI P-05 · WHB-API-13/14 · BR-015 | `renderBulk` L2983 / `submitBulk` L3131 |
| §6 P-06 View node | 01_UI P-06 · WHB-API-06 | `renderViewNode` L2838 |
| §6 P-07 View loc (3 tab) | 01_UI P-07 · WHB-API-10/11/12 | `renderViewLoc` L2885 |
| §6/§9 P-08 Modals | 01_UI P-08 · WHB-API-05/12 · BR-005/010/013 | `renderModal` L3175 / `modalShell` L3210 |
| §8.2 RBAC | 01_UI §1.4 · BR-016 · D8 | `perms()` L2037 |
| §8.1 Esc chain | 01_UI §1.0 (combobox→drawer/modal) | L3274 (capture) + L1667 (bubble) + L1803 |
| §10 path builder | ENG-HIER-PATH · D15/LD-05 | `pathChips` L2145 |
| §1.2 z-map | LD-08/CI | L1319-1323 |

### 11.2 ⚠️ Drift Log
| # | ประเภท | รายการ | anchor | ข้อเสนอ |
|---|---|---|---|---|
| **D-1** | HTML-only dead code | `.role-switch` / `.role-switch-label` / `.role-select` CSS ไม่มี markup ใช้ | L3304-3306 | **strip ตอน production** (D15/LD-10) — ตรงกับ FRD, ไม่ใช่ feature |
| **D-2** | HTML-only dead code | `setRole()` ประกาศแต่ไม่มี caller | L2588 | strip. (`syncRoleChip` L2179 คงไว้ — sync ป้ายชื่อ ไม่ใช่ switcher) |
| **D-3** | HTML-only dead code | base-kit hash router `getRoute()`/`navigate()` — SPA ไม่ใช้ hash | L1607-1616 | strip (LD-08). ยืนยัน route map เป็น state-driven |
| **D-4** | HTML-only dead code | `.drill-chip.is-branch` CSS + comment "branch › WH…" — breadcrumb ไม่เคย render branch | L1334/1329 | strip CSS + แก้ comment (D15/LD-05) |
| **D-5** | HTML-only dead code | `fullPathStr` มี branch `<b>` branch ที่ไม่เคยทำงาน (pathChips ไม่ set `.branch`) + comment stale L2144 | L2162 | ลบสาขา code ที่ไม่ทำงาน (vestige D7 path ที่ถูก D15 reverse) |
| **D-6** | duplicate/latent | มี `keydown` Esc listener 2 ตัว (base-kit L1667 bubble + feature L3274 capture) + base-kit `openDrawer/closeDrawer/openModal/closeModal` L1621-1649 ถูก override โดย feature L2623-2639 | — | ทำงานถูกต้อง (capture→combobox, bubble→modal/drawer) แต่ base-kit duplicates ควรลบกัน regression |
| **D-7** | stale comment | PREFLIGHT banner ยังอ้าง "Role switcher (D13) aligned to create button" + "Location Hierarchy" | L3309-3317 | อัปเดต banner ให้ตรง D14/D15 (ไม่กระทบ runtime) |
| **D-8** | UX gap (known) | tree rows ไม่มี keyboard/arrow-key nav (UX-08) | `.tree-row` L2270 (onclick only) | accessibility follow-up (LD-02) — non-blocking Phase 1 |

> **ไม่มี business drift** — ทุกรายการเป็น dead-code / stale-comment / known-gap ที่ FRD 07_LOCKED_DECISIONS ระบุไว้แล้ว (LD-02/LD-08/LD-10) หรือเป็นผลจาก D15 reverse ของ D7. ไม่ขัด Scope Lock.

---

## §12 · Diff จากเวอร์ชันก่อน
— ไม่ได้รับ HTML เวอร์ชันเก่าเป็น input (legacy อยู่ `_legacy/` เป็น reference) → ข้าม. การเปลี่ยนหลักจาก legacy สรุปใน DECISION_LOG (v3→v7 CI, +tree D12, −role switcher D15, −branch in path D15, delete→soft archive D11).

---

## §13 · 💡 ข้อเสนอ (ไม่ใช่ AS-BUILT — R1)
1. **ลบ dead code** D-1…D-5 + base-kit duplicate D-6 ก่อนส่ง production (ลดพื้นที่ผิดพลาด/สับสน dev).
2. **Tree keyboard nav** (D-8/UX-08): เพิ่ม `role="treeitem"` + `tabindex` + ↑↓→← handler ให้ `.tree-row` (accessibility).
3. **Self-host fonts + Lucide** (แทน CDN external L9-12/L1551) — ตัด dependency บน network/firewall ตอน production.
4. **Refresh-safety:** ถ้าต้องการ deep-link ระดับ drill (เช่น share ลิงก์ไปที่ zone) พิจารณา sync `state.drill` → querystring (ปัจจุบัน refresh = reset) — เป็น enhancement, ขัด LD-08 เดิมได้ ต้องเคาะกับ BA.
5. อัปเดต stale comments L1329/2144/3309-3317 ให้ตรง D14/D15.

---
*Extraction-based · ทุก anchor อ้างบรรทัดใน`WarehouseBin.html` (3319 บรรทัด) · paired กับ FRD_F-LOCATION-MASTER-001_Pack · Drift Log = 8 (dead-code/stale/gap, no business drift)*
