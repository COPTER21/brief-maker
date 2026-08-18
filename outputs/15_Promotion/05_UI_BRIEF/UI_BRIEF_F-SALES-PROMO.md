# HTML UI Brief — F-SALES-PROMO Promotion

## 0. Document Control + Pairing

| Field | Value |
|---|---|
| AS-BUILT HTML | `outputs/15_Promotion/Promotion.html` |
| Title | “โปรโมชัน (Promotion) · CUBE 4.0” |
| Route | `#/promotions` |
| FRD | `FRD_Pack/01_UI.md`, `02_API.md`, `05_RULES.md` |
| Extraction | shared `ui-brief-check.py`; source has 20 CSS variables, 121 functions, 7 detected overlays |
| Drift status | no business drift; persona selector is demo-only |

This brief is extraction-based. HTML remains the visual/microcopy source of truth; FRD defines production contracts.

## 1. Design Tokens AS-BUILT

### 1.1 Core variables

| Token | Value |
|---|---|
| `--c-navy` / `--c-navy-2` | `#111111` / `#1C1C1E` |
| `--c-primary` / hover | `#FF3B30` / `#E62E24` |
| `--c-teal` / light | `#FF9A1F` / `#FFC46B` |
| `--c-ink` | `#111111` |
| `--c-mute` / `--c-mute-2` / `--c-mute-3` | `#54565C` / `#73757B` / `#9A9CA2` |
| `--c-line` / 2 / 3 | `#DEDAD4` / `#E9E5E0` / `#F1EEEA` |
| `--c-bg-off` / `--c-surface-2` | `#FAF8F5` / `#F1EEEA` |
| `--c-success` / warning / danger | `#1F9D55` / `#E8870F` / `#E62E24` |
| `--sidebar-w` / `--shell-h` | `232px` / `52px` |

Font stack is `'Noto Sans Thai','Satoshi',system-ui,sans-serif`; sources are Google Fonts and Fontshare. If unavailable, system UI fallback is used.

### 1.2 z-index map

| z | Selector | Purpose |
|---:|---|---|
| 500 | `.dd-panel.is-portal`, `.cb-menu` | master combobox/dropdown portal |
| 90 | `.toast-wrap` | toast |
| 70 | `.modal-backdrop` | modal layer; `.modal` card is child |
| 60 | `.dd-panel` | local dropdown |
| 51 | `.drawer` | drawer |
| 50 | `.drawer-backdrop` | drawer backdrop |
| 40 | `.sidebar` | navigation shell |
| 30 | `.topbar` | sticky topbar |
| 2 | table header / stepper circle | local stacking |
| 1 | stepper connector | local stacking |

## 2. Route Map

| Route | Handler | Refresh behavior |
|---|---|---|
| `#/promotions` | `route()` → `render()` | missing hash or `#/` is replaced with `#/promotions`; `hashchange` rerenders |

No other feature route exists. Drawers/modals are state within this route.

## 3. Layout Shell

| Region | Selector | AS-BUILT behavior |
|---|---|---|
| Sidebar | `.sidebar` | fixed left, full height, charcoal, z40 |
| Top bar | `.topbar` | sticky top, white, z30 |
| Main content | `.content#page-content` | renders list workbench |
| Drawer roots | `#drawerBackdrop`, `#drawerEl` | right-side stateful overlay |
| Modal root | `#modalBackdrop`, `#modalCard` | centered card over drawer |
| Toast root | `#toastWrap.toast-wrap` | bottom-right transient messages |
| Portal root | `#dd-portal` | fixed dropdown menus outside clipped containers |

## 4. Page Anatomy

### 4.1 Promotion list (`#/promotions`)

| Region/component | Anchor | Render/handler |
|---|---|---|
| Page heading/actions | `.page-head` | `renderList()`, `openSim()`, `exportCsv()`, `openCreate()` |
| Persona demo | role selector/user card | `switchPersona()` |
| Status tabs | tab controls | `state.tab`, `filtered()`, `render()` |
| Search/type/scope/sort | toolbar controls | state setters + `filtered()` |
| Promotion rows | main table row | `openView(id)` |
| Status pill | pill element | `pStatus()`, `pill()` |

### 4.2 Detail drawer

| Region | Anchor | Behavior |
|---|---|---|
| Drawer | `.drawer#drawerEl` | `openView()`, `renderDrawerOnly()` |
| Header/hero | drawer header + hero classes | code/name/status and rule sentence |
| Four tabs | tab controls | rule/scope, usage/budget, approval/info, history |
| Approval timeline | `.audit-timeline`-style timeline | `chainOf()`, `currentStep()`, audit data |
| Footer actions | drawer footer buttons | state/persona derived through `canActStep()` |

### 4.3 Create/edit drawer

| Region | Anchor | Behavior |
|---|---|---|
| Wide drawer | `.drawer` with wide mode | `openCreate()`, `openEdit()` |
| Stepper | `.stepper-*` | state step 1–3; `nextStep()` |
| Form fields | `.field`, `.input`, `.select`, combobox | `state.form`, `formErrors()` |
| Variant rule editor | rule sections/tables | rendered by `promotion_type` |
| Footer | action buttons | `saveForm('draft'|'submit')` |

### 4.4 Cart simulator drawer

| Region | Anchor | Behavior |
|---|---|---|
| Context | `#cbi-sim-coupon`, customer/channel combos | `simSet()`; channel blank uses selected customer default |
| Line editor | `.sim-cart-table` | `simLineSet()`, `simLineDel()` |
| Product combobox | `cbx-*`, `.cb-menu` in `#dd-portal` | `cbInput/focus/key`, `renderPortal()` |
| Results | summary + evaluation ladder | `calcPromo(lines,doc)` |
| Free goods | row with “ของแถม” pill | output from calculation |

### 4.5 Confirmation modals

`openModal(type,id)` + `renderModal()` render submit, approve, reject, cancel, pause and end-early states into `#modalCard`.

## 5. Component Inventory and States

| Component | Anchor | default/active | disabled/error/empty/loading |
|---|---|---|---|
| Status tab | tab controls | selected from `state.tab` | empty list handled by render branch; synchronous prototype has no loading |
| Primary/secondary/danger buttons | `.btn-*` | hover/focus CSS | busy guarded by `state.busy`; production must bind disabled |
| Field | `.field .input/.select` | focus border/ring | `.is-error`, `.field-error`; no loading |
| Master combobox | `.cbx`, `.cb-menu`, `.cb-item` | open/highlight/selected | no-match branch; keyboard arrows/Enter/Escape |
| Status pill | `.pill-*` | mapped via `PST`/`pStatus()` | no interactive/loading state |
| Table | `.rule-tbl`, `.sim-cart-table` | sticky header/row interaction | filtered empty branch; no skeleton in prototype |
| Drawer | `.drawer`, `.drawer-backdrop` | transform open/closed | busy prevents mutation; no focus trap |
| Modal | `.modal-backdrop`, `.modal` | display open/closed | required reason/ack/slots show errors; no focus trap |
| Toast | `.toast-wrap`, `.toast` | success/info/warning | auto remove after 3500ms |
| Timeline | `.audit-timeline` | pending/approved/rejected/history states | empty state not explicitly specialized |

Explicitly absent in HTML: scroll lock on body, focus trap inside overlay, focus restoration after render. Production implementation should not claim these as AS-BUILT behavior.

## 6. Overlay Registry

| Overlay selector | Open/close | Dismiss rule | z |
|---|---|---|---:|
| `.drawer-backdrop` | state drawer open / `closeDrawer()` | backdrop click + Esc when no modal/menu | 50 |
| `.drawer` | `openView/openCreate/openEdit/openSim` | close control/backdrop/Esc | 51 |
| `.modal-backdrop` | `openModal()` / `closeModal()` | backdrop click, close button, Esc; card stops propagation | 70 |
| `.dd-panel` | combobox focus/input | selection/click outside/Esc | 60 |
| `.dd-panel.is-portal` | portalized dropdown | same; fixed position | 500 |
| `.cb-menu` | `renderPortal()` | selection/click outside/Esc | 500 |
| `.toast-wrap` | `showToast()` | timeout only; not user-dismissible | 90 |
| `.sidebar` | always visible shell layer | not an overlay despite checker classification | 40 |

## 7. Interaction Spec

### 7.1 Esc chain

- Combobox keyboard handler includes Escape branch near HTML line **1117**.
- Global handler at HTML line **1132** checks Escape, then closes `cb.open`, otherwise modal, otherwise drawer.
- Required order: dropdown/combobox → modal → drawer.

### 7.2 Click / scroll / focus

- Drawer backdrop calls `closeDrawer()`; modal backdrop calls `closeModal()`; modal card stops bubbling
- `#dd-portal` avoids clipping; `.cb-menu` has its own vertical scroll and scroll events must not trigger click-outside closure
- Coupon/quantity inputs preserve typed value and focus across calculation rerender through keyed input restoration logic
- No drag/pan/zoom behavior exists

## 8. State-Driven UI Matrix

| Code | Label | Main allowed UI |
|---|---|---|
| draft | ร่าง | แก้ไข, ส่งอนุมัติ, ทำสำเนา, ยกเลิก |
| pending | รออนุมัติ | current assignee อนุมัติ/ไม่อนุมัติ; maker ยกเลิก/สำเนา |
| scheduled | รอถึงวันเริ่ม | ทำสำเนา, ปิดก่อนกำหนด |
| active | กำลังใช้ | ระงับ, ทำสำเนา, ปิดก่อนกำหนด |
| paused | ระงับชั่วคราว | เปิดต่อ, ทำสำเนา, ปิดก่อนกำหนด |
| exhausted | งบ/โควตาหมด | ทำสำเนา, ปิดก่อนกำหนด |
| ended | สิ้นสุดแล้ว | ทำสำเนา |
| cancelled | ยกเลิก | ทำสำเนา |

Actual key names and label mapping remain in `PST`, `pStatus()` and render branches.

## 9. Microcopy Verbatim

### 9.1 Toasts detected

| Variant | Text/prefix exactly in HTML |
|---|---|
| info | `(เดโม)` |
| info | `Export CSV แล้ว` |
| warning | `กรุณากรอกข้อมูลให้ครบถ้วน` |
| success | `ตีกลับแล้ว — กลับเป็นร่าง` |
| warning | `ต้องยืนยันการทับซ้อนก่อนส่ง` |
| success | `บันทึกการแก้ไขแล้ว` |
| success | `สร้างโปรโมชันสำเร็จ (ร่าง)` |
| info | `สลับบทบาทเป็น` |
| success | `ส่งอนุมัติแล้ว — เข้ากล่อง My Approval ของ` |
| success | `อนุมัติครบสาย — โปรฯ มีผลทันที` |
| warning | `เลือกผู้อนุมัติให้ครบทุกขั้น` |
| warning | `แก้ไขได้เฉพาะร่าง — ที่อนุมัติแล้วให้ทำสำเนาออกใหม่` |
| warning | `ไม่ใช่ผู้มีสิทธิ์ในขั้นปัจจุบัน` |

Additional dynamic toasts concatenate promotion code/person/date; copy the literal templates from `showToast(...)` calls during implementation.

### 9.2 Key visible anchors

- `ทดสอบตะกร้า`, `Export CSV`, `สร้างโปรโมชัน`
- `ทุกลูกค้า`, `กลุ่มลูกค้า`, `ช่องทางการขาย`
- `เงื่อนไขและขอบเขต`, `การใช้งานและงบ`, `การอนุมัติและข้อมูล`, `ประวัติ`
- `ชนิดและขอบเขต`, `เงื่อนไข`, `ตรวจสอบและยืนยัน`
- `สินค้า`, `หน่วย`, `จำนวน`, `ราคา/หน่วย`, `รวม`, `ลดโปรฯ`, `ของแถม`
- `อนุมัติ`, `ไม่อนุมัติ`, `ระงับ`, `เปิดต่อ`, `ปิดก่อนกำหนด`, `ยกเลิก`

## 10. Data Binding & Backend Anchors

| HTML data/function | Production binding | FRD |
|---|---|---|
| `PROMOS`, `findP()`, `filtered()` | list/detail repository | API-01/API-12 |
| `PRODUCTS`, `CUST_BY`, `GROUP_BY`, `CHAN_BY` | locked master adapters | 00 overview dependencies |
| `basePrice()` / line unit | price-resolver + TA output from caller | XT-01 |
| `calcPromo()` | F-SALES-PROMO-ENG-01 via API-13 | 03_LOGIC |
| `resolveDoa()` / `MOCK_DOA_ENTRY` | DOA central resolve; no mock in production | DOA brief, API-04 |
| `saveForm()` | API-02/API-03 | 02_API |
| `confirmSubmit/Approve/Reject` | API-04/05/06 | 02_API |
| `confirmCancel/Pause/End`, `resumeP()` | API-08..11 | 02_API |
| local audit/usage values | DB read model and Invoice event | API-14, 04_DB |

## 11. Traceability + Drift Log

| Brief section | FRD | HTML anchor |
|---|---|---|
| §4.1 | P-01 | `route()`, `renderList()`, `filtered()` |
| §4.2 | P-02 | `openView()`, `renderDrawerOnly()` |
| §4.3 | P-03 | `openCreate/openEdit`, `nextStep`, `saveForm` |
| §4.4 | P-04 | `openSim`, `renderSim`, `calcPromo` |
| §4.5/§6 | P-05 | `openModal`, `renderModal`, confirm functions |
| §7 | UI interaction contract | lines 1117/1132, `closeDrawer/closeModal` |
| §8 | lifecycle/action matrix | `PST`, `pStatus`, `canActStep` |
| §9 | expected text | `showToast` calls and rendered templates |

### Drift Log

| Type | Item | Resolution |
|---|---|---|
| HTML-only/demo | persona switching | keep prototype testing aid; production authorization uses IAM |
| AS-BUILT gap | no scroll lock/focus trap/focus restore | documented as absent; FRD does not misrepresent it |
| FRD-only/backend | idempotency, ETag, persistence, service auth | expected backend contract; no visual control required |

No business drift between approved HTML and FRD.

## 12. Diff from Previous Version

No previous UI Brief exists. Current HTML includes manual-review fixes for filter selection, timeline geometry, stable coupon/quantity focus, simulator table overflow, scrollable product dropdown, restored “ทุกลูกค้า”, humanized simulator copy and bundle search icon spacing.

## 13. Proposals (not AS-BUILT)

- None. This brief intentionally contains no visual redesign proposal.

## Verification Checklist

- route: 1/1
- detected overlay rows: 7/7
- detected toast strings: 13/13
- Esc handler lines: 1117 and 1132 referenced
- state matrix and data bindings documented
- FRD P-01..P-05 traced
