# HTML UI Brief — F084 Stocktake

## 0. Document Control

- Source: `F-WH-STOCKTAKE.html` final after ST feedback
- Pair: `FRD_Pack/01_UI.md`, `02_API.md`, `05_RULES.md`
- Mode: AS-BUILT extraction; no invented component
- Routes: `#/rounds`, `#/sheets`, `#/variance`, `#/history`, `#/create`
- Drift: none material

## 1. Design Tokens AS-BUILT

CSS variables: `--sidebar-w`, `--c-navy`, `--c-primary`, `--c-teal`, `--c-bg`, `--c-line`, `--c-mute`, `--fs-sm`, `--fs-md`, `--r`, `--sp-2`, `--sp-4`

Z-index high→low: `--z-toast` 80, `--z-modal` 60, `--z-drawer` 51, `--z-backdrop` 50, `--z-pop` 30, `--z-dropdown` 30, `--z-sidebar` 20, `--z-sticky` 10, `--z-content` 1

Fonts: Satoshi + Noto Sans Thai with system fallback. Lucide loads from CDN; offline icon fallback must be accepted or bundled in production

## 2. Route Map

| Route | Visible page | Render anchor |
|---|---|---|
| `#/rounds` | รอบนับ | `renderRounds()` / `#rows` |
| `#/sheets` | ใบนับ | `renderSheets()` |
| `#/variance` | ผลต่าง | `renderVariance()` |
| `#/history` | ประวัติ | `renderHistory()` |
| `#/create` | drawer สร้างรอบ | `openCreate()` / `renderDrawer()` |

Default/refresh: `route()` reads the hash; unknown hash retains current tab and renders shell. `closeDrawer()` returns create route to rounds

## 3. Layout Shell

`.sidebar` fixed left; `.main` holds `.shell-bar` and `main#app.content`. Header from `header()` renders title, subtitle, demo persona switcher, create button and `.tabs.drawer-tabs`. At 1024px sidebar collapses to icon rail and stats become 2 columns

## 4. Page Anatomy

### P-01 รอบนับ

`.stats` → `section.card.page-fill` → `.toolbar` search/type/status/reset → `.table-wrap#rows` → `.table-foot`. `renderRows()` opens selected round and switches to sheets

### P-02 ใบนับ

`renderSheets(r)` builds section header with lock/status/person, conditional freeze/assign/recount action, item table and footer. Footer action wrapper `.table-actions` uses an 8px gap for “สแกน” and “ส่งผลนับ”. Only `currentPersonId===assigned` gets inputs/actions

### P-03 ผลต่าง

Counter receives `.card.empty` “ไม่มีสิทธิ์ดูผลต่าง”. Supervisor receives threshold and approval-basis summary, variance table and state-dependent action footer

### P-04 ประวัติ

`renderHistory(r)` renders `.timeline` entries. F082 acknowledgment is a flat `.history-handoff` section separated by a top border; it is not a nested `.card`

### O-01 สร้างรอบ

`#drawer` has `.dw-head`, `.dw-body` form grid and `.dw-footer`. Scope uses `.combo` + `.combo-pop`

## 5. Component Inventory and States

| Component | Anchor/function | States |
|---|---|---|
| tabs | `.tab`, `setTab()` | default/active; no disabled/loading |
| round table | `.tbl`, `renderRows()` | loaded/filtered-empty; loading/error not implemented |
| person combobox | `.combo`, `suggest/choose` | closed/open/no result; keyboard arrow selection not implemented |
| quantity input | `aria-label="ผลนับ …"`, `recordCount()` | blank/value; browser min plus submit validation |
| status pill | `.pill`, `pill()` | draft/frozen/counting/recount/review/pending/approved/rejected/closed |
| toast | `#toast-root`, `toast()` | one message; auto-clear after 3500ms |
| action button | `.btn`, `beginSubmit()` | normal/disabled/loading spinner |
| approval timeline | active step paragraph + history `.timeline` | pending/completed/rejected via event text |

## 6. Overlay Registry

| Overlay | Anchor | Open | Dismiss | z |
|---|---|---|---|---:|
| sidebar shell | `.sidebar` | always | none | 20 |
| picker popover | `.combo-pop` | focus/input `suggest()` | Esc hides; selection rerenders | 30 |
| drawer backdrop | `.drawer-backdrop` | `renderDrawer()` | backdrop calls `closeDrawer()` | 50 |
| drawer | `.drawer` | `openCreate()` | X, cancel, Esc, backdrop | 51 |
| modal backdrop/modal | `.modal-backdrop` / `.modal` | `renderModal()` | cancel, Esc, backdrop | 60 |

ไม่มี scroll lock, focus trap หรือ focus restore ใน HTML นี้. Esc handler อยู่บรรทัด 24 ของ single-line script source: modal → combobox popover → drawer

## 7. Interaction Spec

- Tab click sets `tab`, updates hash and rerenders
- Combobox searches id/name and rerenders on choice
- Submit actions use `beginSubmit()` then `delay()`; no `wait_for_timeout` contract in product implementation
- Backdrop closes only when click target equals the backdrop
- Esc closes one topmost categoryตาม chain §6
- Direct function calls are still guarded by role, state and person identity

## 8. State-driven UI Matrix

| state | visible label | action/person |
|---|---|---|
| draft | แบบร่าง | supervisor freeze |
| frozen | ล็อกพื้นที่แล้ว | supervisor assign |
| counting | กำลังนับ | assigned first counter input+submit |
| recount | รอนับซ้ำ | supervisor assign, then assigned second counter input+submit |
| review | ตรวจผลต่าง | supervisor submit approval |
| pending | รออนุมัติ | selected current person approve/reject |
| approved | อนุมัติแล้ว | supervisor create adjustment draft |
| rejected | ไม่อนุมัติ | read-only; lock absent |
| closed | ปิดรอบ | read-only + handoff history |

## 9. Microcopy Verbatim

Buttons: “สร้างรอบนับ”, “ล้างตัวกรอง”, “ล็อกพื้นที่และเก็บยอดตั้งต้น”, “มอบหมายใบนับ”, “มอบหมายนับซ้ำ”, “สแกน”, “ส่งผลนับ”, “ส่งอนุมัติ”, “ไม่อนุมัติ”, “อนุมัติขั้นนี้”, “สร้างร่างใบปรับยอด”, “ยืนยันสร้าง”, “ยกเลิก”, “ยืนยัน”

Placeholders: “ค้นหาชื่อ / รหัสรอบนับ / คลัง…”, “ค้นหาคลัง/ตำแหน่ง”, “ค้นหาบุคคล”, “เหตุผลที่ไม่อนุมัติ”

Messages: “กรุณาระบุชื่อรอบนับและพื้นที่นับ”, “พื้นที่นี้ทับซ้อนกับรอบนับที่กำลังใช้งาน”, “ไม่พบสินค้าในพื้นที่นับ”, “ไม่ใช่ผู้ได้รับมอบหมายให้นับในขั้นนี้”, “กรุณากรอกผลนับทุกสินค้าเป็นศูนย์หรือมากกว่า”, “ผลต่างเกินเกณฑ์ ต้องมอบหมายคนอื่นนับซ้ำ”, “ผู้นับซ้ำต้องเป็นคนละคนกับผู้นับครั้งแรก”, “กรุณาเลือกผู้อนุมัติทุกขั้น”, “ผู้อนุมัติต้องไม่ใช่ผู้นับ”, “ผู้อนุมัติแต่ละขั้นต้องเป็นคนละคน”, “กรุณาระบุเหตุผล”, “สร้างร่างใบปรับยอดและปิดรอบนับแล้ว”

Empty: “ยังไม่มีรอบนับ”, “ไม่พบรอบนับที่ตรงกับตัวกรอง”, “ไม่มีสิทธิ์ดูผลต่าง”

## 10. Data Binding / Backend Anchors

| HTML mock/function | FRD destination |
|---|---|
| `rounds`, `renderRows` | API-01 |
| `createRound` | API-02/FN-02 |
| `STOCKTAKE_LOCKS`, `freezeRound` | API-03/FN-03/04 |
| `confirmModal(assign)` | API-04/FN-05 |
| `submitCount` | API-05/FN-06/07 |
| `varianceLines/varianceTotal` | ENG-01 |
| `doaDefinition`, DOA modal | API-07/FN-09 + DOA resolve |
| `confirmModal(approve/reject)` | API-08/FN-10 |
| `handoff` | API-09/FN-11 + ENG-02 |

## 11. Traceability and Drift

Routes/pages 5/5 map FRD 01_UI. Actions map APIs 10/10. BR-ST-01..10 have visible state/guard or explicit backend contract. No business drift. Known deliberate test-only element: `[data-demo="persona-switch"]`; production excludes it

## 12. Diff from pre-feedback version

- `.table-actions` added so Scan/Submit have stable 8px separation
- `.history-handoff` replaced nested card structure
- submit guard requires exact assigned person; regression SEC-01 added

## 13. Proposals (not AS-BUILT)

- Add focus trap/restore and explicit scroll lock before production accessibility signoff
- Bundle Lucide locally if offline prototype operation is required
- Add explicit loading/error states to list and integration handoff
