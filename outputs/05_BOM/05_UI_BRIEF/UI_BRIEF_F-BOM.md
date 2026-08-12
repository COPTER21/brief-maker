# HTML UI Brief — F-BOM สูตรการผลิต

> เอกสารนี้อธิบาย **AS-BUILT เท่านั้น** จาก `outputs/05_BOM/01_HTML/f-bom.html` และใช้คู่กับ FRD Pack. ทุก behavior อ้าง selector/function/text ที่มีจริง; ข้อเสนอแยกอยู่ §13.

---

## §0 Document Control + Pairing

| Item | Value |
|---|---|
| Feature | F-BOM-001 · สูตรการผลิต (Bill of Materials) |
| HTML source of truth | `outputs/05_BOM/01_HTML/f-bom.html` |
| HTML title | `BOM — สูตรการผลิต (CUBE 4.0)` |
| FRD pairing | `outputs/05_BOM/04_FRD/FRD_F-BOM_Pack/` |
| Routes | 4 hash states: list/create/edit/view |
| Source style | single-file SPA; vanilla JS; in-memory mock `RAW` |
| Extraction tool | ไม่ได้รัน — `scripts/extract_anchors.py` ไม่พบใน skill directory; อ่าน HTML ทั้งไฟล์โดยตรง |
| Drift status | มี 5 รายการใน §11.3; business/security drift ต้องยึด FRD ตอน implement |

## §1 Design Tokens AS-BUILT

### §1.1 Root tokens

| Token | Value | Anchor |
|---|---|---|
| `--c-navy` | `#111111` | `:root` |
| `--c-navy-2` | `#1C1C1E` | `:root` |
| `--c-primary` | `#FF3B30` | `:root` |
| `--c-primary-hover` | `#E62E24` | `:root` |
| `--c-teal` | `#FF9A1F` | `:root` |
| `--c-teal-light` | `#FFC46B` | `:root` |
| `--c-ink` | `#111111` | `:root` |
| `--c-mute` | `#54565C` | `:root` |
| `--c-mute-2` | `#73757B` | `:root` |
| `--c-mute-3` | `#9A9CA2` | `:root` |
| `--c-line` | `#DEDAD4` | `:root` |
| `--c-line-2` | `#E9E5E0` | `:root` |
| `--c-line-3` | `#F1EEEA` | `:root` |
| `--c-bg-off` | `#FAF8F5` | `:root` |
| `--c-success` | `#1F9D55` | `:root` |
| `--c-warning` | `#E8870F` | `:root` |
| `--c-danger` | `#E62E24` | `:root` |
| `--sidebar-w` | `232px` | `:root` |
| `--shell-h` | `52px` | `:root` |

Font stack on `body`: `'Noto Sans Thai','Satoshi',system-ui,sans-serif`; remote font links load Satoshi, Inter and Noto Sans Thai. Monospace-like codes use `'Satoshi',monospace`. Body background is `--c-bg-off`, size 14px, line-height 1.5, minimum width 768px.

Recurring radius/shadow anchors: `.btn/.input` 9px; `.table-card/.toolbar` 12px; `.modal` 14px; drawer shadow `-8px 0 40px rgba(11,29,58,.16)`; modal shadow `0 20px 60px rgba(11,29,58,.3)`; combobox shadow `0 10px 30px rgba(17,17,17,.16)`. Scrollbar is 5px with transparent track.

### §1.2 Z-index map (high → low)

| z | Element | Positioning/anchor |
|---:|---|---|
| 200 | `.cbx-suggest` | fixed in `#suggest-portal` |
| 200 | `#toast-root` | fixed bottom-center |
| 120 | `#modal-root` | fixed full viewport |
| 100 | `#overlay-root` | fixed full viewport; drawer/backdrop |
| 80 | `.pop-menu` | absolute under status trigger |
| 70 | `.sidebar` at ≤1180px | fixed/off-canvas |
| 60 | `.hint:hover::after` | absolute tooltip; class exists but no rendered `.hint` instance |
| 20 | `.shell` | sticky top |
| 2 | `.table-scroll thead th` | sticky table header |
| 1 | `.step .dot`, `.tl-dot` | local stacking |

## §2 Route Map

| Route | Parsed state | Renderer | Result |
|---|---|---|---|
| `#/bom` | `mode` undefined | `syncHash()` closes drawer/modal + `renderList()` | P-01 list |
| `#/bom/create` | `mode=create` | `openForm('create',null)` → `renderForm()` | P-02 create drawer |
| `#/bom/edit/:id` | `mode=edit` | `openForm('edit',id)` → `renderForm()` | P-03 edit drawer |
| `#/bom/view/:id` | `mode=view` | `openView(id)` → `renderView()` | P-04 detail drawer |

Anchors: `navTo()`, `parseHash()`, `syncHash()`, `hashchange`. If hash is empty the script sets `#/bom`. Refresh safety comes from `syncHash()` at script end. Unknown mode returns list; unknown edit/view ID calls `navTo('bom')` and silently returns to list.

## §3 Layout Shell

| Region | Selector | AS-BUILT |
|---|---|---|
| application | `.app` | flex, min-height 100vh |
| sidebar | `.sidebar` | fixed left, 232px, dark, scrollable; ≤1180px translates off-screen and has no visible opener in this HTML |
| brand/nav | `.sb-brand`, `.sb-sec`, `.sb-item` | BOM item is `.is-active`; other items are visual only (no route handlers) |
| top shell | `.shell` | 52px sticky; breadcrumb + user chip `สมชาย (Planner)` |
| content | `.content#page-content` | flex column, viewport-height list region, own vertical scroll |
| overlays | `#overlay-root`, `#modal-root`, `#toast-root`, `#suggest-portal` | siblings under `<body>` to avoid clipping |

At 768–1180px `.main` loses left margin, content padding becomes 16px and drawer width is capped to viewport. HTML/body keep `min-width:768px`; no mobile layout below 768px.

## §4 Page Anatomy

### §4.1 P-01 `#/bom` — List

Rendered by `renderList()` into `#page-content`.

| Region | Selector/function | Content/behavior |
|---|---|---|
| header | `.page-h` | title `สูตรการผลิต (BOM)`, description, primary `สร้างสูตรใหม่` → `navTo('bom/create')` |
| stats | `.stats > .stat` + `quickFilter()` | สูตรทั้งหมด/ใช้งาน/ไม่ใช้งาน/ร่าง; active filter gets `.is-on`; clicking same status toggles off |
| filters | `.toolbar .filter-bar` | `#bomSearch`, parent select, status select, `ล้าง`; `filtered()` composes all filters and sort |
| bulk bar | `.bulkbar` | only when selection count >0; status actions, delete, cancel |
| table | `.table-card .table-scroll table` | sticky head; checkbox, product, version/default, name, line count, cost, effective date, status, chevron |
| rows | `tr.row-click` | click → detail; selected row `.is-sel`; checkbox stops row propagation |
| empty | `.empty` | `ไม่พบสูตรการผลิต` |
| footer | `.footer-row` | `แสดง ${rows.length} จาก ${total} สูตร`, `หน้า 1` |

Search rerenders through `renderInline()` and restores caret/focus in `setFilter()`. Sorting toggles direction in `sortBy()`. Pagination is visual only: always `หน้า 1` and no page control.

### §4.2 P-02/P-03 — Form drawer

Rendered by `renderForm()` inside `#overlay-root`; same 920px drawer for create/edit.

| Region | Anchor | AS-BUILT |
|---|---|---|
| header | `.drawer-head` | `สร้างสูตรการผลิตใหม่` or `แก้ไขสูตร ${f.code}`; X calls `navTo('bom')` |
| stepper | `.stepper`, `.step`, `.dot`, `.lb` | exactly 2 steps: `ข้อมูลสูตร`, `ส่วนประกอบ`; active/done visual states |
| Step 1 | `.fsec`, `.fgrid` | FG combobox (disabled plain input on edit), version, name, output qty, effective date, default switch |
| Step 2 | `.lines`, `.line-row` | component combobox, qty, compatible UoM select, scrap, delete line, add line, live total |
| footer | `.drawer-foot` | cancel/back, draft save, next, active save according to current step |

State is copied by `blankForm()` or deep clone in `openForm()`. `captureForm()` copies rendered inputs before rerender. `nextStep()` checks parent/version/name and exact-case duplicate; `saveForm()` rechecks required values plus case-insensitive duplicate and `validateLines()`.

### §4.3 P-04 — Detail drawer

Rendered by `renderView()`.

| Region | Anchor | AS-BUILT |
|---|---|---|
| header | `.drawer-head`, `prodAvatar()` | product image/fallback, product name, version, BOM code/name |
| actions | `.dh-actions` | `แก้ไขสูตร`, `เปลี่ยนสถานะ`, X |
| tabs | `.tabs .tab`, `setTab()` | `ภาพรวม`, `ส่วนประกอบ (${b.lines.length})`, `ประวัติ` |
| overview | `.dfields` | code, product, version/default, name, output, effective date, status |
| sibling versions | `.fsec .lines .line-row` | `เวอร์ชันอื่นของสินค้านี้ (${others.length})`; each row calls `navTo('bom/view/${x.id}')` |
| components | `.vtable` | quantity/UoM/scrap/current cost/line total + total footer |
| history | `.tl`, `.tl-item` | audit title and `${fmtDT(a.at)} · ${a.by}` |
| footer | `.drawer-foot` | `ปิด` → list |

## §5 Component Inventory and States

| Component | Anchor | Default/active | Hover/focus | Disabled/empty/loading/error |
|---|---|---|---|---|
| primary button | `.btn.btn-primary` | red, white text | darker red on hover | no general disabled style; no loading state |
| danger button | `.btn-danger` | red | — | `:disabled` opacity .5, default cursor |
| stat card | `.stat` | white card | cursor pointer | `.is-on` red border/inset ring; no disabled/empty |
| text/search input | `.input`, `#bomSearch` | 38px white field | browser focus; no explicit focus CSS | edit parent input disabled opacity .6; no error class |
| select | `.select` | native select with SVG chevron | browser states | no loading/error |
| status pill | `.pill-*`, `statusPill()` | draft gray, active green, inactive orange | none | unknown status falls back text but class has no defined style |
| default badge | `.badge-def` | yellow star badge | none | rendered only if `is_default` |
| checkbox | `.ck` | native, red accent | browser state | no disabled state |
| bulk bar | `.bulkbar` | hidden until selection | buttons lighten on hover | no loading/error; delete opens modal |
| row | `.row-click`, `.is-sel` | clickable | hover light background/chevron red | empty handled at table level |
| stepper | `.step.active/.done` | line/dot state | none | no disabled/click; display only |
| toggle | `.sw`, `.sw.on` | gray/off | none | orange/on; div is click-only, no disabled/keyboard state |
| line editor | `.lines`, `.line-row` | rows from state | add/delete hover styles | empty text `ยังไม่มีส่วนประกอบ — กดเพิ่มด้านล่าง`; no loading/error style |
| tabs | `.tab`, `.tab.active` | gray | cursor pointer | red active underline; no keyboard/disabled state |
| timeline | `.tl-item`, `.tl-dot` | neutral dot | none | success/warning variants; empty audit renders blank |
| product avatar | `.parent-ic`, `prodAvatar()` | image over initials | none | `onerror="this.remove()"` reveals initials |
| status menu item | `.pm-item`, `.is-current` | click target | light hover | current opacity .45 and handler only stops propagation |

No explicit global loading state, fetch error state, inline validation style, skeleton, retry UI, focus ring customization, or unsaved-change prompt exists.

## §6 Overlay Registry

| Overlay | Root/content | Open | Dismiss rules | Position/z |
|---|---|---|---|---|
| form/detail drawer | `#overlay-root`, `.backdrop`, `.drawer-panel` | `openForm()`/`openView()` + `_renderNow()` | backdrop click, X, footer cancel/close, Esc all call/navigate list; no dirty guard | fixed root z100; 920px right panel; slide transform |
| status popover | `#statusMenu.pop-menu` | `toggleStatusMenu(event)` | same trigger toggles; document click; Esc via `closeMenus()`; selecting new state | absolute under trigger, z80 |
| bulk-delete modal | `#modal-root`, `.modal-bd`, `.modal` | `openBulkDelete()` | backdrop, `ยกเลิก`, Esc, successful confirm | fixed centered, 440px, z120 |
| FG suggest | `#suggest-portal #fgSuggest.cbx-suggest` | input focus/type | choose option, outside mousedown; no Esc-specific branch | fixed from `placeSuggest()`, z200 |
| line suggest | `#suggest-portal #lnSuggest-${i}` | component focus/type | choose option, outside mousedown; no Esc-specific branch | fixed from `placeSuggest()`, z200 |
| toast | `#toast-root .toast` | `toast(msg,kind)` | automatic remove after 2600ms only | fixed bottom-center, z200 |

Modal backdrop is dismissible even though action is destructive. Drawer backdrop is also dismissible during an edited form. No focus trap, initial-focus placement, body scroll lock, or focus restoration is implemented.

## §7 Interaction Specification

### §7.1 Escape chain

Actual `document.keydown` order:

1. `state.modal.open` → `closeModal()`
2. `#statusMenu.is-open` → `closeMenus()`
3. `state.drawer.open` → `navTo('bom')`
4. otherwise no action

Combobox portal is not present in this Esc chain; pressing Esc while a suggestion is open does not explicitly close it.

### §7.2 Outside click and propagation

- document `click` always calls `closeMenus()`; `toggleStatusMenu(event)` stops propagation
- document `mousedown` ignores targets inside `#suggest-portal`; otherwise closes FG/line suggestion when target is outside its trigger container
- row checkbox cell stops propagation so selection does not open detail
- status current item calls `event.stopPropagation()` and makes no change

### §7.3 Positioning/scroll/render

- `placeSuggest()` uses input `getBoundingClientRect()`, fixed left/width, opens upward if space below <200px, otherwise downward by 4px
- capture-phase window scroll and resize call `reflowSuggest()`
- portal lives outside transformed drawer to avoid fixed-position clipping
- `_keepScroll()` stores `.content`, `.table-scroll`, `.drawer-body` offsets and restores them in `requestAnimationFrame()`
- `_renderNow()` rerenders list and active drawer/modal, then recreates active portal in a second RAF

Keyboard navigation for combobox options, tabs, switch, sibling-version rows and stat cards is not implemented beyond native controls. Sibling rows are clickable `<div>` without `tabindex`/key handler.

## §8 State-Driven UI Matrix

### §8.1 BOM status

| Value | Label | Pill | Icon in menu | Allowed action |
|---|---|---|---|---|
| `draft` | `ร่าง` | `.pill-draft` | `file-edit` | every other status via single/bulk |
| `active` | `ใช้งาน` | `.pill-active` | `check-circle-2` | every other status via single/bulk |
| `inactive` | `ไม่ใช้งาน` | `.pill-inactive` | `x-circle` | every other status via single/bulk |

`setStatus()`/`bulkSetStatus()` clears `is_default` when target is not active. Setting active does not automatically make default.

### §8.2 Drawer/form state

| State | Header | Parent | Footer |
|---|---|---|---|
| create step 1 | `สร้างสูตรการผลิตใหม่` | searchable `#fgCombo` | `ยกเลิก`, `ถัดไป` |
| create step 2 | same | line editor | `ย้อนกลับ`, `บันทึกร่าง`, `บันทึก + เปิดใช้งาน` |
| edit step 1 | `แก้ไขสูตร ${code}` | disabled text input | `ยกเลิก`, `ถัดไป` |
| edit step 2 | same | existing cloned lines | `ย้อนกลับ`, `บันทึกร่าง`, `บันทึก + เปิดใช้งาน` |
| detail overview | product/version header | — | `ปิด` |
| detail components/history | same | — | `ปิด` |

### §8.3 Bulk delete state

| Selection | Modal body | Danger button |
|---|---|---|
| all unused | `การกระทำนี้ย้อนกลับไม่ได้` | `ลบ ${ids.length} สูตร`, enabled |
| mixed | `มี ${skip} สูตร...จะถูกข้าม...` | count only eligible, enabled |
| all used | same skip explanation | `ลบ 0 สูตร`, disabled |

## §9 Microcopy Verbatim

### §9.1 Navigation/headings/actions

`สูตรการผลิต (BOM)` · `สร้างสูตรใหม่` · `สร้างสูตรการผลิตใหม่` · `แก้ไขสูตร ${f.code}` · `ข้อมูลสูตร` · `ส่วนประกอบ` · `ยกเลิก` · `ย้อนกลับ` · `ถัดไป` · `บันทึกร่าง` · `บันทึก + เปิดใช้งาน` · `แก้ไขสูตร` · `เปลี่ยนสถานะ` · `ปิด` · `ภาพรวม` · `ประวัติ`

### §9.2 Labels/placeholders/empty

- `ค้นหา รหัสสูตร / ชื่อ / สินค้า...`
- `สินค้าทั้งหมด` · `ทุกสถานะ` · `ล้าง`
- `ค้นหาสินค้าผลิตเอง (รหัส/ชื่อ)...`
- `v1, v2...`
- `เช่น สูตรมาตรฐาน / สูตรประหยัด`
- `ค้นหาวัตถุดิบ...`
- `ไม่พบสูตรการผลิต`
- `ไม่พบสินค้า`
- `ไม่พบวัตถุดิบ`
- `ยังไม่มีส่วนประกอบ — กดเพิ่มด้านล่าง`
- `เพิ่มส่วนประกอบ`
- `ตั้งเป็นสูตรหลัก`
- `สูตรที่ระบบเลือกใช้เป็น default ตอนสร้างใบสั่งผลิต (1 สินค้า = 1 สูตรหลัก)`

### §9.3 Toast/error strings by call site

| Function | Kind | Text template |
|---|---|---|
| `nextStep()` | warning | `เลือกสินค้าผลผลิตก่อน` |
| `nextStep()` | warning | `ระบุเวอร์ชันสูตร` |
| `nextStep()` | warning | `ระบุชื่อสูตร` |
| `nextStep()` | error | `เวอร์ชัน ${f.ver} ของสินค้านี้มีอยู่แล้ว` |
| `saveForm()` | error | `เลือกสินค้าผลผลิตก่อน` |
| `saveForm()` | error | `ระบุเวอร์ชันสูตร (เช่น v1)` |
| `saveForm()` | error | `เวอร์ชัน ${f.ver} ของสินค้านี้มีอยู่แล้ว` |
| `saveForm()` | error | `ระบุชื่อสูตร` |
| `validateLines()` | error | `ต้องมีส่วนประกอบอย่างน้อย 1 รายการ` |
| `validateLines()` | error | `ส่วนประกอบห้ามเป็นตัวสินค้าเอง (${l.item}) — กัน BOM วน` |
| `validateLines()` | error | `ปริมาณของ ${l.item} ต้องมากกว่า 0` |
| `validateLines()` | error | `วัตถุดิบ ${l.item} ซ้ำ — รวมเป็นรายการเดียว` |
| `saveForm()` | success | `เปิดใช้งานแล้ว` or `บันทึกร่างแล้ว` |
| `setStatus()` | success | `เปลี่ยนสถานะเป็น ${STATUS_TH[st]} แล้ว` |
| `bulkSetStatus()` | success | `เปลี่ยนสถานะ ${n} สูตรเป็น ${STATUS_TH[st]} แล้ว` |
| `confirmBulkDelete()` | success/warning | `ลบแล้ว ${del.length} สูตร` + optional ` · ข้าม ${skip.length} (มีใบสั่งผลิตอ้างแล้ว)` |

### §9.4 Delete modal

- `ลบสูตรการผลิต ${ids.length} รายการ?`
- `มี ${skip} สูตรถูกใบสั่งผลิต (MO) อ้างแล้ว — จะถูกข้าม ไม่ลบ (ใช้เปลี่ยนสถานะเป็น "ไม่ใช้งาน" แทน)`
- `การกระทำนี้ย้อนกลับไม่ได้`
- `ยกเลิก`
- `ลบ ${ids.length-skip} สูตร`

## §10 Data Binding and Backend Anchors

HTML contains no literal `// BACKEND:` marker. Plug points are inferred only from mock ownership comments and render/mutation functions:

| Mock/state | Current owner/anchor | FRD endpoint/contract |
|---|---|---|
| `PRODUCTS`, `PMAP`, `PARENTS`, `COMPS` | Product Master comment; `fgMatches()`, `lineMatches()` | upstream Item Master adapter/API |
| `UOMS`, `uomsForItem()` | UOM Master comment | upstream UoM adapter/API |
| `RAW` list | `filtered()`, `renderList()` | F-BOM-API-01 |
| one `RAW` aggregate | `openView()`, `renderView()` | F-BOM-API-03 |
| create/update | `saveForm()` | API-02/API-04; UI must send server contract, not mutate array |
| status | `setStatus()`, `bulkSetStatus()` | API-05 |
| delete | `openBulkDelete()`, `confirmBulkDelete()` | API-06 result ledger |
| MO use count | `used` comment and delete guard | authoritative MO usage adapter |
| cost | `lineCost()`, `bomCost()` | ENG-01/current Item cost + D-CLASS guard |
| audit | `b.audit`, history timeline | mutation audit response/API-03 |

The prototype has no asynchronous fetch, loading/error state, pagination backend, authentication call, idempotency key, optimistic version, tenant header, or permission evaluation.

Assets: remote fonts; all product mock images are embedded SVG data URIs; icons come from the local `ICONS` object and `renderIcons()`, not an external icon runtime.

## §11 Three-way Traceability + Drift Log

### §11.1 Page/action trace

| Brief | FRD | HTML anchor |
|---|---|---|
| §4.1 list | P-01 / API-01 | `renderList()`, `filtered()` |
| §4.2 create | P-02 / API-02 | `openForm('create')`, `renderForm()`, `saveForm()` |
| §4.2 edit | P-03 / API-04 | `openForm('edit')`, `renderForm()`, `saveForm()` |
| §4.3 detail | P-04 / API-03 | `openView()`, `renderView()` |
| §8.1 status | API-05 / BR-08/10 | `setStatus()`, `bulkSetStatus()` |
| §8.3 delete | API-06 / BR-11 | `openBulkDelete()`, `confirmBulkDelete()` |
| §4.3 siblings | S-03 / FN-02 | `others.map()` + `navTo('bom/view/${x.id}')` |
| §4.2 validation | VR-01..08 | `nextStep()`, `validateLines()`, `saveForm()` |

### §11.2 Rule trace

| FRD rule | HTML evidence |
|---|---|
| BR-01 version unique | `nextStep()` exact-case check + `saveForm()` case-insensitive check |
| BR-02 one default/active-only | default clearing exists; active-only invariant does **not** fully exist → DRIFT-02 |
| BR-03/04 Item types | `PARENTS` FG, `COMPS` RM/PM/TR; active status absent from mock |
| BR-05 single-level/self block | component options exclude FG; `validateLines()` self check |
| BR-06 UoM category | `uomCat()`, `uomsForItem()`, `selectLineItem()` |
| BR-07/09 cost | `lineCost()`, `bomCost()`; confidentiality absent → DRIFT-03 |
| BR-08/10 all-direction/no approval | `STATUS_TH`, status functions; approval fields null |
| BR-11/12 used behavior | `confirmBulkDelete()` guard; edit has no used guard |
| BR-13 no CSV | no import/export control/function |
| BR-14 scrap 0..100 | input min/max; server-like `validateLines()` does not validate max |
| BR-15 master deactivate | no active field/policy in mock |

### §11.3 Drift Log

| ID | Direction | Actual difference | Resolution for implementation |
|---|---|---|---|
| DRIFT-01 | HTML-only origin, retained in FRD | `#f-efffrom` exists although PREBRIEF dictionary omitted it | FRD preserves optional storage/display; no scheduler |
| DRIFT-02 | HTML violates FRD invariant | `saveForm(false)` can retain `is_default=true`; seed `b4` is `draft + is_default=true` | backend/DB contract in BR-02 wins; HTML needs later sync if prototype is edited |
| DRIFT-03 | FRD-only security | HTML always renders raw cost in list/form/detail; no D-CLASS state | production FE consumes masked response and must not retain raw cost |
| DRIFT-04 | FRD-only operational states | FRD requires loading/error/stale/permission states; HTML has none | implement from FRD; do not claim AS-BUILT visual reference exists |
| DRIFT-05 | behavior mismatch | FRD specifies visible not-found; `openForm()`/`openView()` silently redirect to list | choose/supply final error design before production UI freeze |

## §12 Diff from Previous HTML

Previous HTML file was not supplied as a separate artifact. From in-file comments and prior coverage evidence only: current file includes v8 Warm Light rebrand, Overlay Portal #95, full-height list #96, responsive rule #97, VR-02 recheck, and the FN-09 sibling-version renderer. A byte-level historical diff is **ไม่พบข้อมูลในบทสนทนา**.

## §13 💡 Proposals (Not AS-BUILT)

These are implementation follow-ups, not claims about the current HTML:

- sync prototype DRIFT-02 so draft can never display as default
- add designs for DRIFT-03..05 before visual acceptance of production UI
- make switch, stats, tabs, sibling rows and combobox fully keyboard-accessible; include suggestion portal in Escape handling
- add dirty-form confirmation/focus management to avoid backdrop/Esc data loss

---

## UI Brief Verification

- [x] every route in HTML has a section: 4/4
- [x] every modal/drawer/popover/toast has Overlay Registry row: 6/6 categories
- [x] every `toast(...)` call/template is represented in §9.3
- [x] every anatomy component has selector/function anchor
- [x] state matrix covers `draft`, `active`, `inactive` and form/modal states found
- [x] Escape chain matches the actual handler order
- [x] z-index map includes every declared z-index occurrence
- [x] FRD P-01..04 have trace rows and drift is explicit
- [x] sample audit ≥10 claims trace to HTML anchors

**Verdict: PASS (fallback manual extraction)** — extractor/template reference files were missing, but all required 13 sections and mechanical checks were completed from the source HTML.

