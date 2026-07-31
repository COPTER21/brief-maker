# HTML UI Brief — F-VENDOR ทะเบียนคู่ค้า

> เอกสารนี้เป็น **AS-BUILT extraction** จาก HTML ที่อนุมัติแล้ว ไม่ใช่เอกสารออกแบบ UI ใหม่  
> ทุกข้ออ้างอิง `vendor.html:Lx` หมายถึงบรรทัดใน `./vendor.html`

---

## §0 Document Control + Pairing

| Field | Value |
|---|---|
| Feature | F-VENDOR / Vendor Master / ทะเบียนคู่ค้า |
| Brief version | 1.1 · 2026-07-31 · HTML↔FRD sync |
| HTML source of truth | `./vendor.html` · 1,541 lines · user-approved + sync revision |
| FRD pair | `./FRD_F-VENDOR_Pack/` v1.1 sync |
| Routable pages | 1 (`#/vendors`) |
| Drawer modes | 3 (`view`, `create`, `edit`) |
| Modal types | 9 (`address_remove`, `approve`, `reject`, `kyc`, `bank_disable`, `unblock`, `inactive`, `block`, `blacklist`) |
| Other overlays | user menu + toast |
| Extraction method | manual source read + mechanical anchor/count checks |
| Drift status | critical HTML↔FRD drift ถูกปิดแล้ว; ยังมี implementation gaps ที่ระบุใน §11.2 |

### §0.1 Source precedence for this brief

1. HTML เป็น authority ของ **สิ่งที่แสดง/ทำได้จริงใน prototype**
2. FRD เป็น authority ของ **backend contract, security และ business behavior**
3. เมื่อสองแหล่งขัดกัน เอกสารนี้บันทึกทั้งสองฝั่งใน Drift Log; ห้าม AI Coding Agentเลือกเอง

### §0.2 Anchor convention

| Anchor type | Example |
|---|---|
| Selector | `.drawer`, `#modalBackdrop`, `.pill-pending_kyc` |
| Renderer | `renderList()`, `renderForm()`, `modalKyc()` |
| Handler | `openDrawer()`, `confirmKyc()`, `showToast()` |
| State | `state.drawer`, `state.modal`, `ROLE`, `RAW` |
| Source line | `vendor.html:L825` |

## §1 Design Tokens — AS-BUILT

### §1.1 Root tokens

Source: `:root` at `vendor.html:L13` — 44 variables.

| Group | Token → value |
|---|---|
| z-index | `--z-sticky:10`; `--z-shell:20`; `--z-dropdown:30`; `--z-backdrop:50`; `--z-drawer:51`; `--z-modal:60`; `--z-toast:80` |
| Core colors | `--c-navy:#111111`; `--c-navy-2:#111111`; `--c-primary:#FF3B30`; `--c-primary-hover:#E62E24`; `--c-teal:#FF9A1F`; `--c-teal-light:#FFB763`; `--c-ink:#111111` |
| Muted/line/background | `--c-mute:#54565C`; `--c-mute-2:#73757B`; `--c-mute-3:#9A9CA2`; `--c-line:#DEDAD4`; `--c-line-2:#E9E5E0`; `--c-line-3:#F1EEEA`; `--c-bg-off:#FAF8F5` |
| Semantic colors | `--c-success:#1F9D55`; `--c-warning:#E8870F`; `--c-danger:#E62E24` |
| Shell size | `--sidebar-w:232px`; `--shell-h:52px` |
| Type scale | `--fs-h1:22px`; `--fs-h2:17px`; `--fs-h3:15px`; `--fs-body:14px`; `--fs-sub:13px`; `--fs-meta:12px`; `--fs-cap:11px`; `--fs-kpi:28px` |
| Spacing | `--sp-xs:4px`; `--sp-sm:8px`; `--sp-md:12px`; `--sp-lg:20px`; `--sp-xl:28px` |
| Radius | `--r-xs:4px`; `--r-sm:6px`; `--r-md:8px`; `--r-lg:12px`; `--r-full:999px` |

### §1.2 Typography

| Usage | AS-BUILT stack | Anchor |
|---|---|---|
| Body/UI | `'Satoshi','Noto Sans Thai',system-ui,sans-serif` | `body`, L15 |
| Thai headings | `'Noto Sans Thai',sans-serif` | `.ph-title`, `.drawer-title`, `.modal-title` |
| Numeric/code helpers | `'Inter',ui-monospace,monospace` | `.mono`, L174 |
| Price-list code | `'SF Mono',Menlo,Consolas,monospace` | `.pl-code`, L212 |

Fonts load from Fontshare and Google Fonts (`vendor.html:L8-L11`). `Inter` is referenced but not explicitly loaded.

### §1.3 Radius, shadow, scrollbar and motion

| Item | AS-BUILT | Anchor |
|---|---|---|
| Main card | radius `10px`, overflow hidden | `.card` |
| Drawer | right fixed, shadow `-16px 0 40px rgba(17,17,17,.18)` | `.drawer`, L85 |
| Modal | radius `12px`, shadow `0 24px 64px rgba(11,29,58,.28)` | `.modal`, L122 |
| User menu | radius `10px`, shadow `0 12px 32px rgba(11,29,58,.12)` | `.user-menu`, L44 |
| Toast | radius `10px`, shadow `0 12px 32px rgba(17,17,17,.24)` | `.toast`, L127 |
| Body scroll | `scrollbar-gutter:stable`; no custom width | `body`, L15 |
| Drawer scroll | body `overflow-y:auto`, stable gutter | `.drawer-body`, L92 |
| Tab scroll | horizontal; scrollbar hidden | `.drawer-tabs`, L90 |
| Drawer motion | transform 280ms cubic-bezier | `.drawer`, L85 |
| Modal motion | opacity/scale 200ms | `.modal-backdrop`, `.modal`, L121-L122 |
| Toast motion | transform/opacity 250ms | `.toast`, L127 |

### §1.4 z-index map

| High → low | Token/value | Used by | Finding |
|---:|---|---|---|
| 80 | `--z-toast` | `.toast` | visible above modal |
| 60 | `--z-modal` | `.modal-backdrop` | backdrop and modal share one stacking context |
| 51 | `--z-drawer` | `.drawer` | above drawer backdrop |
| 50 | `--z-backdrop` | `.drawer-backdrop` | below drawer |
| 30 | `--z-dropdown` | `.user-menu` | below drawer/modal |
| 20 | `--z-shell` | `.sidebar` | fixed navigation |
| 10 | `--z-sticky` | `.shell-bar` | sticky top bar |
| local 1 | literal `z-index:1` | `.vendor-step`, `.appr-node` | local stacking |
| local 0 | literal `z-index:0` | `.vendor-stepper::before` | connector behind steps |

## §2 Route Map

| Route | Default | Renderer | Refresh/hash behavior | FRD |
|---|---:|---|---|---|
| `#/vendors` | YES | `render()` → `renderList()` | missing hash is replaced with `#/vendors`; any other hash redirects to `/vendors` | UI-01 |

**Anchors**

- Active sidebar link: `a.sb-item[data-feature="vendor-master"][href="#/vendors"]` at L292
- Route reader: `currentRoute()` at L797
- Hash writer: `navTo()` at L798
- Unknown-route guard: `hashchange` handler at L1530
- Refresh/default safety: `history.replaceState(...,'#/vendors')` at L1532

ไม่มี route แยกสำหรับ create/edit/view; ทั้งหมดเป็น overlay state บน route เดียว

## §3 Layout Shell

```text
body (min-width 1180)
├─ aside.sidebar [fixed, 232px]
│  ├─ .sb-brand
│  ├─ #sb-nav
│  │  ├─ Master Data → Vendor Master active
│  │  ├─ Procurement → disabled PR/PO
│  │  └─ System → disabled Settings
│  └─ .sb-footer
└─ main.main [margin-left: sidebar width]
   ├─ header.shell-bar [sticky, 52px]
   │  ├─ breadcrumb
   │  └─ notification + #userChip + #userMenu
   └─ #page-content

overlay roots after main:
├─ #drawerBackdrop
├─ #drawer
├─ #modalBackdrop > #modalEl
└─ #toast
```

| Region | Selector | Size/position | Renderer/handler |
|---|---|---|---|
| Sidebar | `.sidebar` | fixed left; `--sidebar-w` | static DOM + `toggleModule()` |
| Main | `.main` | left margin = sidebar width | static |
| Shell bar | `.shell-bar` | sticky top; `--shell-h` | static |
| User chip/menu | `#userChip`, `#userMenu` | top-right; menu absolute | `renderUserChip()`, `toggleUserMenu()` |
| Content | `#page-content` | padding 24px | `render()` |
| Drawer root | `#drawer` | fixed right; 920px, max 96vw | `renderDrawer()` |
| Modal root | `#modalBackdrop`, `#modalEl` | viewport center; 440px max 92vw | `renderModal()` |
| Toast | `#toast` | fixed bottom-right | `showToast()` |

## §4 Page Anatomy

### §4.1 UI-01 — Vendor list (`#/vendors`)

Renderer: `renderList()` (`vendor.html:L820-L869`)

```text
#page-content
├─ .ph
│  ├─ .ph-title-row → "ทะเบียนคู่ค้า" + count
│  ├─ .ph-sub
│  └─ .ph-actions → create button OR read-only role badge
└─ .card
   ├─ .filter-bar
   │  ├─ .input-search
   │  ├─ type .select
   │  ├─ status .select
   │  └─ reset .btn
   ├─ .table-scroll > table.table
   │  ├─ sortable headers
   │  ├─ vendor rows + status pill
   │  └─ .row-actions by role/state
   └─ .table-footer
      ├─ page-size select
      └─ range + .pagination
```

| Behavior | Handler/state |
|---|---|
| search/type/status filter | `applyFilter()` → reset page to 1 |
| reset | `resetFilters()` |
| sort | `sortBy()`; arrow `↑/↓/↕` |
| pagination | `goToPage()`, `setPageSize()` |
| click row | `openDrawer('view', id)` |
| row actions | edit/KYC/approve/block/unblock conditions at L850-L855 |
| empty | `pg.records.length===0` |
| loading/error | ไม่มีใน HTML (—) |

### §4.2 UI-03 — View drawer

Renderer: `renderView()` (`vendor.html:L875-L912`)  
Root: `#drawer.drawer`; open via `openDrawer('view', id)`

| Region | Selector / function | Contents |
|---|---|---|
| Header | `.drawer-header` | avatar, legal name, code, vendor/KYC pills, close |
| Action strip | `.vl-28` | state/role-driven edit, submit, KYC, approve, reject, block, inactive, unblock, blacklist |
| Tabs | `.drawer-tabs`, `.drawer-tab` | 5 tabs |
| Tab body | `.drawer-body` | renderer below |
| Footer | `.drawer-footer` | version/date + `ปิด` |

| Tab key / text | Renderer | Main selector |
|---|---|---|
| `overview` / `ภาพรวม` | `viewOverview()` | `.drawer-fields`, `.message-box` |
| `bank` / `ธนาคาร & ติดต่อ` | `viewBank()` | `.bm-card`, `.addr-badge` |
| `attach` / `เอกสารแนบ` | `viewAttachments()` | `.bm-card` |
| `approval` / `การอนุมัติ` | `viewApproval()` | `.appr-chain`, `.appr-step` |
| `pricelist` / `สินค้า/บริการ` | `viewPriceList()` | `.pl-table` / empty block |

### §4.3 UI-02 — Create/Edit drawer wizard

Renderer: `renderForm()` (`vendor.html:L1031-L1053`)  
Open: `openDrawer('create')` / `openDrawer('edit', id)`

| Step | Renderer | Key anchors |
|---:|---|---|
| 1 `ข้อมูล & ภาษี` | `formStep1()` | `#f-type`, `#f-country`, `#f-name`, `#f-display`, `#f-tax`, `#f-vat`, `#f-creg`, branch/VAT/currency controls |
| 2 `ติดต่อ & ธนาคาร` | `formStep2()` | `.ctc-card`, `.addr-card`, `.bank-card` |
| 3 `เอกสารแนบ & ชำระ` | `formStep3()` | `#f-term`, `#f-wht`, `#f-credit`, `#f-attach` |

Footer actions: `ยกเลิก/กลับ`, `บันทึกร่าง`, `ถัดไป`, and dynamic `บันทึก (amend)` or `บันทึก + ส่ง KYC`; submitting text is `กำลังบันทึก...`.

### §4.4 UI-04..UI-07 — Modal surfaces

Modal anatomyร่วม:

```text
#modalBackdrop.modal-backdrop
└─ #modalEl.modal
   ├─ .modal-header
   ├─ .modal-body
   └─ .modal-footer
```

Specific renderers are registered in §6.

## §5 Component Inventory + States

| Component | Anchor | Render/handler | States found in HTML |
|---|---|---|---|
| Sidebar module | `.sb-module`, `.sb-module-header` | `toggleModule()` | expanded; collapsed via `data-expanded=false`; hover |
| Sidebar item | `.sb-item` | static | default, hover, `.is-active`, `.is-disabled` |
| User menu | `#userMenu.user-menu` | `renderUserChip()`, `toggleUserMenu()` | closed, `.is-open`, item hover, `.is-sel`, `.is-danger` |
| Button | `.btn` variants | many handlers | default, hover, disabled; primary/secondary/ghost/danger/small |
| Input/select | `.input`, `.select` | form handlers | default, focus, disabled; HTML has no bound `.field-error` state |
| Table | `.table` | `renderList()` | loaded, row hover, sortable/sorted, empty; no loading/error |
| Pagination | `.pg-btn` | `goToPage()` | default, hover, active, disabled class |
| Vendor pill | `.pill-${status}` + `.dot-${status}` | `statusLabel()` | all 7 vendor states |
| KYC pill | `.pill-${kyc}` | `kycLabel()` | pending/passed/failed/expired |
| Drawer | `#drawer.drawer`, `#drawerBackdrop` | `openDrawer()`, `closeDrawer()` | closed, `.is-open`; `.standard` CSS exists but is never applied |
| Drawer tab | `.drawer-tab` | `setTab()` | default, hover, active |
| Stepper | `.vendor-stepper`, `.vendor-step`, `.step-dot` | `renderForm()` | current/prior steps use `.is-active`; prior number becomes check icon |
| Contact card | `.ctc-card` | `contactCard()` | list/empty; delete only when total >1 |
| Address card | `.addr-card` | `addressCard()` | default, `.is-billing`, `.is-primary`, both; delete vs soft-disable action |
| Address role guard | `.message-box.info-amber` | `formStep2()` | hidden when role assigned; visible when missing |
| Bank card | `.bank-card` | `bankCard()` | unverified editable, primary, verified read-only; disabled appears in view pill |
| Attachment | `.bm-card`, `#f-attach` | `formStep3()`, `addAttachments()` | empty/list; verification text verified/unverified |
| Approval chain | `.appr-step`, `.appr-node` | `viewApproval()` | pending, current, approved, rejected |
| Price List | `.pl-table` | `viewPriceList()` | empty; active row; inactive/expired row |
| Message box | `.message-box` | many renderers | blue/amber/green/red |
| Modal | `.modal-backdrop`, `.modal` | `openModal()`, `renderModal()` | closed/open; content varies by type |
| KYC pass button | `.btn-primary[disabled]` | `modalKyc()` | enabled normally; disabled on sanctions hit |
| Approval confirm | `.btn-primary` + inline style | `modalApprove()` | enabled if all guards; pointer-disabled/opacity otherwise |
| Toast | `#toast.toast` | `showToast()` | info/success/warning/error; hidden/visible |
| Loader | `.loader-2` | `submitForm()` | only while `state.submitting=true` |

ไม่มี component state ต่อไปนี้ใน HTML: list skeleton, list API error/retry, focus trap, dirty-form prompt, server conflict UI, offline banner.

## §6 Overlay Registry

| # | Overlay | Root / renderer | Open | Dismiss rules AS-BUILT | Size / z |
|---:|---|---|---|---|---|
| O-01 | View/Create/Edit drawer | `#drawer`, `renderDrawer()` | `openDrawer()` | backdrop, X, footer close/cancel, Esc; programmatic after save/role switch | 920px/max96vw; z51; backdrop z50 |
| O-02 | User menu | `#userMenu` | `toggleUserMenu()` | chip toggle, click outside, role selection; Esc does not close it | 240px; z30 |
| O-03 | Address remove | `modalAddressRemove()` | `requestRemoveAddress()` | backdrop, X, `ยกเลิก`, Esc, confirm | modal 440px; z60 |
| O-04 | Approve | `modalApprove()` | `openModal('approve')` | backdrop, X, `ยกเลิก`, Esc, confirm if guards pass | 440px; z60 |
| O-05 | Reject | `modalReject()` | `openModal('reject')` | backdrop, X, `ยกเลิก`, Esc, confirm | 440px; z60 |
| O-06 | KYC | `modalKyc()` | `openModal('kyc')` | backdrop, X, `ยกเลิก`, Esc, result buttons | 440px; z60 |
| O-07 | Bank deactivate | `modalBankDisable()` | `disableBank()` | backdrop, X, `ยกเลิก`, Esc, confirm with required reason | 440px; z60 |
| O-08 | Unblock | `modalUnblock()` | `openModal('unblock')` | backdrop, X, `ยกเลิก`, Esc, confirm only when KYC/policy gates pass | 440px; z60 |
| O-09 | Inactive | `modalInactive()` | `openModal('inactive')` | backdrop, X, `ยกเลิก`, Esc, confirm | 440px; z60 |
| O-10 | Block | `modalBlock(r,false)` | `openModal('block')` | backdrop, X, `ยกเลิก`, Esc, confirm | 440px; z60 |
| O-11 | Blacklist | `modalBlock(r,true)` | `openModal('blacklist')` | backdrop, X, `ยกเลิก`, Esc, confirm/permission guard | 440px; z60 |
| O-12 | Toast | `#toast`, `showToast()` | any toast call | auto-hide after 2,800ms; replaced/reset by next toast; no close button/Esc | max380px; z80 |

All modal backdrops call `closeModal()`; click inside `.modal` stops propagation (`vendor.html:L324`). ไม่มี overlay ที่ห้าม backdrop-dismiss และไม่มี scroll lock.

## §7 Interaction Specification

### §7.1 Esc and dismiss chain

Actual handler (`vendor.html:L1529`):

```text
Escape
├─ if state.modal.open → closeModal()
├─ else if state.drawer.open → closeDrawer()
└─ else → no action
```

- User menu is not part of this Esc chain.
- `closeModal()` waits 200ms before clearing state/re-render (`L1387`).
- `closeDrawer()` waits 280ms before clearing state/re-render (`L1230`).
- Modal backdrop click closes; modal content stops propagation.
- Drawer backdrop click closes.
- No dirty-state confirmation exists before close.

### §7.2 Click and pointer behavior

| Interaction | AS-BUILT behavior | Anchor |
|---|---|---|
| click vendor row | opens view drawer | row `onclick`, L845 |
| click row action | `event.stopPropagation()` prevents view drawer | table action cell, L850 |
| click outside user menu | closes menu | document click handler, L800 |
| click notification | shows count toast only | `toggleNotif()` |
| sidebar module header | toggles expanded state | `toggleModule()` |
| disabled sidebar items | visual/cursor disabled; no href | `.sb-item.is-disabled` |
| address removal | direct if ordinary draft address; modal if designated or active persisted | `requestRemoveAddress()` |
| file attach | hidden multiple file input; local metadata only | `#f-attach`, `addAttachments()` |

Drag, pan, zoom and resize interactions: — ไม่มีใน HTML

### §7.3 Focus and render preservation

| Behavior | Implementation |
|---|---|
| Add address focus | after 60ms focuses last `[data-addr-line]` (`addAddress()`, L1266) |
| Re-render preservation | `preserveRenderState()` captures drawer/modal/page scroll and active input selection |
| Restore | `restoreRenderState()` uses RAF to restore scroll/focus/selection |
| Modal focus trap | — ไม่มี |
| Initial focus on open | — ไม่มี |
| Return focus to trigger | — ไม่มี |
| aria-live toast | — ไม่มี |

### §7.4 Form and collection behavior

- Form scalar fields are copied into `state.form` by `captureForm()`.
- `nextStep()` captures current values then runs `validateStep(currentStep)`.
- `prevStep()` captures without validation.
- Save draft requires only a non-empty name, except editing an active vendor also runs step-2 validation.
- Create submit validates steps 1 and 2, shows loader for 450ms, persists mock data and closes.
- Address:
  - first new address starts as billing + primary shipping unless a role was explicitly removed;
  - selecting a role makes it exclusive across active addresses;
  - removing designated address clears the role and sets a selection guard;
  - active persisted address is copied to `archivedAddresses` with `is_active=false`.
- Bank:
  - any unverified form bank can be removed, including the first;
  - if removed bank was primary, first remaining bank becomes primary;
  - verified bank renderer is read-only;
  - duplicate `setPrimaryBank()` declarations exist; the later ID-based function is the effective runtime definition.

### §7.5 Positioning and responsiveness

- Sidebar/drawer/backdrops/modal/toast use fixed positioning.
- User menu uses absolute positioning relative to wrapper.
- Shell bar uses sticky positioning.
- Body has `min-width:1180px`; this prototype is desktop-fixed rather than responsive.
- Drawer still caps at `96vw`; modal caps at `92vw`/`90vh`.

## §8 State-Driven UI Matrices

### §8.1 Vendor lifecycle

Source: `statusLabel()` L670; pill/dot CSS L131-L133 and L219-L226; action renderer L879-L889.

| Value | Visible label | CSS | View/list actions exposed |
|---|---|---|---|
| `draft` | `แบบร่าง` | `.pill-draft`, `.dot-draft` | edit; Procurement `ส่ง KYC`; Compliance `ตรวจ KYC`; Director/Admin blacklist |
| `pending_kyc` | `รอ KYC` | `.pill-pending_kyc`, `.dot-pending_kyc` | edit; Procurement `ส่งอนุมัติ`; Compliance `ตรวจ KYC`; Director/Admin blacklist |
| `pending_approval` | `รออนุมัติ` | `.pill-pending_approval`, `.dot-pending_approval` | eligible approver `ตีกลับ` + `อนุมัติ (ขั้น N)`; Director/Admin blacklist |
| `active` | `ใช้งาน` | `.pill-active`, `.dot-active` | edit; block; inactive; Director/Admin blacklist |
| `blocked` | `บล็อกชั่วคราว` | `.pill-blocked`, `.dot-blocked` | unblock; Director/Admin blacklist |
| `inactive` | `ปิดใช้งาน` | `.pill-inactive`, `.dot-inactive` | Director/Admin blacklist only |
| `blacklisted` | `แบล็คลิสต์` | `.pill-blacklisted`, `.dot-blacklisted` | no header mutation action |

### §8.2 KYC

| Value | Label | CSS | Modal behavior |
|---|---|---|---|
| `pending` | `รอตรวจ` | `.pill-pending` | pass/fail available |
| `passed` | `ผ่าน` | `.pill-passed` | tax field locks on edit |
| `failed` | `ไม่ผ่าน` | `.pill-failed` | without sanctions vendor remains/returns `pending_kyc`; sanctions hit also blocks vendor |
| `expired` | `หมดอายุ` | `.pill-expired` | display only; no expiry action |

Sanctions sub-state is `state.modal.sanctionHit`:

| `sanctionHit` | Source field | Pass button | Fail button | Required |
|---:|---|---|---|---|
| false | checkbox unchecked | enabled | `ไม่ผ่าน` | note only when fail |
| true | checkbox checked | disabled + title | `ไม่ผ่านและบล็อกคู่ค้า` | source + note |

### §8.3 Bank verification

| Value | View/Edit state | Finance action |
|---|---|---|
| `unverified` | editable in form; view shows pending action | `ส่งตรวจ` |
| `pending_verification` | view pending | `ยืนยันผล` |
| `verified` | verified pill; edit renderer read-only | `ปิดใช้บัญชี` opens reason-required confirmation |
| `disabled` | historical/read-only | no re-enable; add a new account |
| `disabled` | `ปิดใช้` pill | no further action |

### §8.4 Approval step

| Value/condition | CSS | Visible content |
|---|---|---|
| `approved` | `.appr-step.is-approved` | check icon, approver, datetime |
| `rejected` | `.appr-step.is-rejected` | X icon |
| first pending | `.appr-step.is-current` | `รออนุมัติขั้นนี้` |
| later pending | default | `รอขั้นก่อนหน้า` |
| no chain | empty block | `ยังไม่มีรายการอนุมัติ` |

### §8.5 Price List item

| Value | Row/dot | Visible effect |
|---|---|---|
| `active` | normal row + `.dot-active` | normal name/price |
| any non-active (`expired` in mock) | `.is-inactive` + `.dot-blocked` | row opacity + name line-through |
| no items | empty block | navigation button to stub |

### §8.6 Role-driven capability

Source: `ROLES`, permission helpers at L338-L370.

| HTML role key | Visible role | Capability |
|---|---|---|
| `procurement_officer` | Procurement Officer | create/edit/submit; block/unblock/inactive |
| `procurement_manager` | Procurement Manager | approval when current step; block/unblock/inactive |
| `procurement_director` | Procurement Director | approve current step; override only when `policyDecision.allow_director_override=true`; block/unblock/inactive; blacklist |
| `finance` | Finance | full tax/bank; bank submit/verify/deactivate |
| `compliance` | Compliance | full tax; KYC |
| `admin` | Admin | administrative gates; approval override only when `policyDecision.allow_admin_override=true` |

Prototype role aliases are explicit and narrow: `finance` maps to FRD/IAM `finance_officer`; `compliance` maps to `compliance_officer`.

Changing role via user menu closes any open modal/drawer, re-renders, and shows a toast.

## §9 Microcopy — Verbatim

### §9.1 Page, navigation and table

| Context | Exact text | Anchor |
|---|---|---|
| HTML title | `ทะเบียนคู่ค้า · CUBE` | `<title>`, L7 |
| Page title | `ทะเบียนคู่ค้า` | `renderList()`, L825 |
| Subtitle | `จัดการข้อมูลคู่ค้า เอกสาร และสถานะการใช้งานในที่เดียว` | L826 |
| Create | `เพิ่มคู่ค้า` | L827 |
| Read-only | `โหมดอ่านอย่างเดียว ({role label})` | L827 |
| Search | `ค้นหา รหัส / ชื่อ / เลขภาษี...` | L830 |
| Filters | `ทุกประเภท`; `ทุกสถานะ`; `รีเซ็ต` | L831-L833 |
| Columns | `คู่ค้า`; `ประเภท`; `เลขภาษี`; `สถานะ` | L837-L840 |
| Empty | `ไม่พบคู่ค้า`; `ลองปรับตัวกรอง หรือเพิ่มคู่ค้าใหม่` | L844 |
| Page sizes | `10 / หน้า`; `20 / หน้า`; `50 / หน้า` | L861 |
| Range | `{start} – {end} จาก {total} รายการ` | L862 |
| Sidebar | `CUBE NATIVE`; `P2P · Master Data`; `Master Data`; `Vendor Master`; `Procurement`; `System`; `UAT · v1.0.0` | L286-L308 |
| Breadcrumb | `Master Data`; `Vendor Master` | L312 |

### §9.2 Drawer/tab/action text

| Group | Exact text patterns |
|---|---|
| View tabs | `ภาพรวม`; `ธนาคาร & ติดต่อ`; `เอกสารแนบ`; `การอนุมัติ`; `สินค้า/บริการ` |
| View actions | `แก้ไข`; `ส่ง KYC`; `ส่งอนุมัติ`; `ตรวจ KYC`; `ตีกลับ`; `อนุมัติ (ขั้น {seq})`; `บล็อก`; `ปิดใช้งาน`; `ปลดบล็อก`; `แบล็คลิสต์`; `ปิด` |
| Wizard title | `เพิ่มคู่ค้าใหม่`; `แก้ไขคู่ค้า` |
| Wizard steps | `ข้อมูล & ภาษี`; `ติดต่อ & ธนาคาร`; `เอกสารแนบ & ชำระ` |
| Wizard footer | `ยกเลิก`; `กลับ`; `บันทึกร่าง`; `ถัดไป`; `บันทึก (amend)`; `บันทึก + ส่ง KYC`; `กำลังบันทึก...` |
| Repeatable actions | `เพิ่มผู้ติดต่อ`; `เพิ่มที่อยู่`; `เพิ่มบัญชี`; `แนบไฟล์`; `ใช้เป็นที่อยู่ใบกำกับ`; `ตั้งเป็นจัดส่งหลัก`; `ตั้งเป็นบัญชีหลัก` |
| Price List | `ไปที่ Price List feature`; `ดู Price List เต็ม →` |
| Address confirm | `ลบที่อยู่นี้?`; `ปิดใช้ที่อยู่นี้?`; `ลบและเคลียร์การตั้งค่า`; `ปิดใช้และเคลียร์การตั้งค่า` |
| Bank view | `ส่งตรวจ`; `ยืนยันผล`; `ปิดใช้บัญชี` |
| Approval | `อนุมัติคู่ค้า — ขั้น {current}/{total}`; `อนุมัติ → ใช้งาน`; `อนุมัติขั้นนี้`; `ตีกลับคู่ค้า`; `ส่ง {code} กลับไปแก้ไขและตรวจ KYC ใหม่`; `ตีกลับ` |
| KYC | `ตรวจ KYC (Compliance)`; `ไม่ผ่าน`; `ไม่ผ่านและบล็อกคู่ค้า`; `ผ่าน KYC` |
| Bank deactivate | `ปิดใช้บัญชีธนาคาร`; `บัญชีนี้จะไม่ถูกใช้สำหรับการจ่ายเงินใหม่ แต่ประวัติเดิมยังคงอยู่`; `เหตุผลที่ปิดใช้บัญชี`; `ยืนยันปิดใช้บัญชี` |
| Availability | `ปลดบล็อกคู่ค้า`; `คู่ค้าผ่านเงื่อนไขสำหรับกลับมาใช้งาน`; `ยังปลดบล็อกไม่ได้ กรุณาดำเนินการตามเงื่อนไขที่แสดง`; `KYC`; `นโยบายอนุมัติ`; `การจ่ายเงิน`; `ปลดบล็อก`; `ปิดใช้งานคู่ค้า`; `ยืนยันปิดใช้งาน`; `บล็อกคู่ค้า`; `แบล็คลิสต์คู่ค้า`; `บล็อก`; `แบล็คลิสต์` |

### §9.3 Placeholders and title attributes

| Type | Exact text |
|---|---|
| Search | `ค้นหา รหัส / ชื่อ / เลขภาษี...` |
| Names | `ชื่อนิติบุคคลเต็ม`; `ชื่อย่อ/ชื่อเรียก`; `ชื่อ-นามสกุล`; `name@example.com`; `02-xxx-xxxx` |
| Tax/company | `13 หลัก`; `ถ้ามี` |
| Address | `เช่น สำนักงานใหญ่ / โกดัง / บ้าน`; `เลขที่ / หมู่ / ซอย / ถนน / อาคาร / ชั้น` |
| Bank | `0123456789`; `ชื่อตรงสมุดบัญชี`; `ระบุเหตุผลที่ปิดใช้บัญชี...` |
| Credit | `0 = ไม่จำกัด` |
| Reject/reason | `ระบุเหตุผลการตีกลับ...`; `ระบุเหตุผล...`; `เช่น สิ้นสุดสัญญา หรือเลิกใช้บริการ` |
| KYC normal note | `ระบุเหตุผลหรือข้อสังเกตจากการตรวจ` |
| KYC sanctions note | `ระบุชื่อที่พบ รายละเอียดการจับคู่ และข้อมูลประกอบการตัดสินใจ` |
| Action titles | `แก้ไข`; `ตรวจ KYC`; `อนุมัติ`; `บล็อก`; `ปลดบล็อก`; `ลบผู้ติดต่อนี้`; `ลบบัญชีนี้`; `ลบไฟล์`; `ปิดใช้บัญชี`; `วันที่ออกเอกสาร`; `วันหมดอายุ` |
| KYC disabled title | `พบรายชื่อต้องห้าม จึงไม่สามารถให้ผ่าน KYC ได้` |

### §9.4 Empty, hint, warning and lock text

| Context | Exact text |
|---|---|
| Tax lock | `ล็อก — ผ่าน KYC แล้ว แก้ไขไม่ได้ (IR-01)` |
| Tax hint | `13 หลัก · checksum · ห้ามซ้ำ`; `One-time ยกเว้นได้` |
| Code hint | `รูปแบบ V-CC-TT-NNNNN · Country (ISO) + Type + running ...` |
| Contact empty | `ยังไม่มีผู้ติดต่อ`; `ต้องมีผู้ติดต่ออย่างน้อย 1 ราย (ชื่อ + อีเมล)` |
| Address empty | `ยังไม่มีที่อยู่`; `กดปุ่ม "เพิ่มที่อยู่" เพื่อกรอกที่อยู่แรก` |
| Address view empty | `ยังไม่มีที่อยู่ที่ใช้งาน`; `เพิ่มที่อยู่ใหม่ก่อนเริ่มทำรายการ` |
| Address role warnings | `ยังไม่ได้กำหนดที่อยู่ใบกำกับ กรุณาเลือกที่อยู่ใหม่{gate}`; `ยังไม่ได้กำหนดที่อยู่จัดส่งหลัก กรุณาเลือกที่อยู่ใหม่{gate}` |
| Bank empty | `ยังไม่มีบัญชีธนาคาร`; `เพิ่มบัญชีสำหรับใช้ในการรับ-จ่ายเงิน (optional)` |
| Bank no-data view | `คู่ค้านี้ไม่มีบัญชีธนาคาร (เช่น ครั้งเดียว / ชำระเงินสด)` |
| Bank mask | `เลขบัญชีถูกปกปิด (Restricted)` |
| Verified bank | `บัญชีที่ยืนยันแล้วเป็น read-only หากต้องเปลี่ยนให้เพิ่มบัญชีใหม่และปิดใช้บัญชีเดิม` |
| Attachment empty form | `ยังไม่มีไฟล์แนบ`; `กดปุ่ม "แนบไฟล์" เพื่อแนบเอกสาร (ถ้ามี)` |
| Attachment empty view | `ไม่มีไฟล์แนบ` |
| Approval empty | `ยังไม่มีรายการอนุมัติ`; `รายการจะแสดงเมื่อส่งคู่ค้าเข้าสู่ขั้นตอนอนุมัติ` |
| Price List empty | `ยังไม่มี Price List สำหรับคู่ค้านี้`; `เพิ่ม items + ราคาผ่าน feature Vendor Price List (F-VENDOR-PRICE-LIST)` |
| Sanctions | `ไม่สามารถให้ผ่าน KYC ได้`; `คู่ค้ารายนี้จะถูกระงับการใช้งานเมื่อยืนยันผล` |

### §9.5 Toast registry — all 62 call sites

Dynamic values are shown in `{braces}`; the surrounding text is verbatim.

| Source | Variant | Exact rendered text/template |
|---|---|---|
| L792 | info | `รีเซ็ตตัวกรองแล้ว` |
| L801 | info | `มี {pk} คู่ค้ารอ KYC และ {pa} รออนุมัติ` |
| L804 | info | `สลับบทบาทเป็น {ROLES[r].label}` |
| L1022 | info | `Feature Vendor Price List ยังไม่เปิดให้บริการ — Phase 2 (vendor: {vendorId})` |
| L1207 | error | `ไม่มีสิทธิ์ดำเนินการ (โหมดปัจจุบัน: {U().label})` |
| L1254 | warning | `ต้องมีอย่างน้อย {min} รายการ` |
| L1263 | warning | `ต้องมีผู้ติดต่ออย่างน้อย 1 ราย` |
| L1277 | info | `ปิดใช้ที่อยู่แล้ว — กรุณาเลือกที่อยู่หลักใหม่` OR `ลบที่อยู่แล้ว — กรุณาตรวจสอบการตั้งค่าที่อยู่` |
| L1296 | warning | `กรุณากรอกชื่อตามกฎหมาย` |
| L1298 | warning | `กรุณากรอกเลขประจำตัวผู้เสียภาษี` |
| L1299 | error | `INVALID_TAX · เลขภาษีต้องเป็นตัวเลข 13 หลัก` |
| L1300 | error | `TAX_DUPLICATE · เลขภาษีซ้ำ — แนะนำ merge` |
| L1305 | warning | `ต้องมีผู้ติดต่ออย่างน้อย 1 ราย (ชื่อ + อีเมล)` |
| L1307 | warning | `ต้องมีที่อยู่อย่างน้อย 1 รายการ (ที่อยู่ + จังหวัด + ตำบล)` |
| L1308 | warning | `กรุณากำหนดที่อยู่ใบกำกับ` |
| L1309 | warning | `กรุณากำหนดที่อยู่จัดส่งหลัก` |
| L1337 | warning | `กรุณากรอกชื่อคู่ค้าก่อนบันทึกร่าง` |
| L1339 | info | `บันทึกร่างแล้ว` |
| L1342 | success | `บันทึกการแก้ไขแล้ว (version +1)` |
| L1343 | success | `สร้างคู่ค้าแล้ว — ส่งเข้ากระบวนการ KYC` |
| L1347 | error | `ไม่มีสิทธิ์ส่ง` |
| L1348 | info | `ส่งเข้ากระบวนการ KYC` |
| L1351 | error | `KYC_NOT_PASSED · ต้องผ่าน KYC ก่อนส่งอนุมัติ` |
| L1353 | warning | `NOT_READY · ต้องมีผู้ติดต่อ (อีเมล+โทร) อย่างน้อย 1 ราย` |
| L1354 | warning | `NOT_READY · ต้องมีบัญชีธนาคารที่ยืนยันแล้วอย่างน้อย 1 บัญชี` |
| L1355 | error/success | `ยังไม่พบสายอนุมัติ กรุณาลองใหม่อีกครั้ง` OR `ส่งอนุมัติ — รอ {first-step label}` |
| L1359 | error | `FORBIDDEN · ยืนยันบัญชีได้เฉพาะฝ่ายการเงิน` |
| L1360 | info | `ส่งบัญชีเข้าคิวตรวจสอบแล้ว` |
| L1363 | success | `ยืนยันบัญชีธนาคารแล้ว — PV gate ปลดล็อก` |
| L1364 | error | `ปิดใช้บัญชีได้เฉพาะฝ่ายการเงิน` OR `ไม่พบบัญชีธนาคารที่เลือก` |
| L1367 | error/warning | `ปิดใช้บัญชีได้เฉพาะฝ่ายการเงิน`; `ไม่พบบัญชีธนาคารที่เลือก`; `กรุณาระบุเหตุผลที่ปิดใช้บัญชี`; `ปิดใช้บัญชีแล้ว — ประวัติยังคงอยู่` |
| L1379 | error | `ไม่มีสิทธิ์` |
| L1380 | error | `ต้องผ่าน KYC ก่อนปลดบล็อก` OR `นโยบายการอนุมัติของคู่ค้านี้ยังไม่พร้อมใช้งาน` |
| L1381 | warning | `REASON_REQUIRED · กรุณาระบุเหตุผล` |
| L1383 | success | `ปลดบล็อกแล้ว → ใช้งาน` |
| L1438 | error | `KYC_NOT_PASSED` |
| L1439 | error | `SOD_VIOLATION · ผู้อนุมัติต้องไม่ใช่ผู้สร้าง` |
| L1440 | warning | `ไม่มีขั้นที่รออนุมัติ` |
| L1441 | error | `WRONG_APPROVER · ขั้นนี้ต้อง {step label}` |
| L1445 | success | `อนุมัติครบทุกขั้น — "{vendor code}" → ใช้งาน` |
| L1446 | success | `อนุมัติขั้น {seq} แล้ว — รอ {next label|ขั้นต่อไป}` |
| L1452 | warning | `REASON_REQUIRED · กรุณาระบุเหตุผล` |
| L1454 | info | `ตีกลับคู่ค้าแล้ว → รอ KYC (แก้ไขแล้วส่งใหม่)` |
| L1470 | error | `FORBIDDEN · KYC ทำได้เฉพาะ Compliance` |
| L1472 | error | `พบรายชื่อต้องห้าม จึงไม่สามารถให้ผ่าน KYC ได้` |
| L1473 | warning | `กรุณาเลือกแหล่งข้อมูลที่ตรวจพบ` |
| L1474 | warning | `กรุณาระบุรายละเอียดผลการตรวจ` |
| L1477 | error | `บันทึกผลแล้ว — ไม่ผ่าน KYC และบล็อกคู่ค้า` |
| L1482 | success/warning | `บันทึกผล KYC: {ผ่าน|ไม่ผ่าน}` |
| L1489, L1504 | error | `ไม่มีสิทธิ์` |
| L1490, L1505 | warning | `REASON_REQUIRED · กรุณาระบุเหตุผล` |
| L1492 | warning | `ปิดใช้งานคู่ค้าแล้ว — รายการใหม่ถูกระงับ` |
| L1503 | error | `BLACKLIST_REQUIRES_DIRECTOR` |
| L1507 | error/warning | `แบล็คลิสต์คู่ค้าแล้ว (terminal)` OR `บล็อกคู่ค้าแล้ว` |

### §9.6 Audit/log templates visible in approval timeline

Source: `seedAudit()` and mutation handlers.

| Exact template |
|---|
| `สร้างคู่ค้า (draft) · v1` |
| `ส่งเข้ากระบวนการ KYC` |
| `KYC ผ่าน — เอกสารครบ + ตรวจ sanctions ผ่าน` |
| `KYC ไม่ผ่าน` |
| `ส่งอนุมัติ (DOA chain)` |
| `อนุมัติ → ใช้งาน (active)` |
| `ยืนยันบัญชีธนาคาร ({masked account})` |
| `แบล็คลิสต์ (terminal) — {reason}` |
| `บล็อก — {reason}` |
| `แก้ไขข้อมูล (amend) · v{version}` |
| `ส่งอนุมัติ — DOA chain {count} ขั้น` |
| `ส่งบัญชีธนาคารเข้าคิวตรวจสอบ` |
| `ปิดใช้บัญชีธนาคาร ({masked account})` |
| `ปลดบล็อก → ใช้งาน — {reason}` |
| `อนุมัติขั้น {seq} ({role label})` |
| `อนุมัติครบทุกขั้น → ใช้งาน (active)` |
| `ตีกลับ → รอ KYC — {reason}` |
| `KYC ไม่ผ่านและบล็อกคู่ค้า — พบรายชื่อเฝ้าระวังจาก {source} — {note}` |
| `KYC {ผ่าน|ไม่ผ่าน} — {note}` |
| `ปิดใช้งาน (normal offboarding) — {reason}` |

## §10 Data Binding and BACKEND Anchors

### §10.1 State/data structures

| HTML structure | Purpose | Anchor |
|---|---|---|
| `RAW` | mutable in-memory vendor list | L635-L650 |
| `vendor()` | default record shape | L612-L623 |
| `state.filters/sort/pagination` | list UI state | L662-L666 |
| `state.drawer` | open/mode/id/tab/step | L663 |
| `state.modal` | open/type/id + modal-specific fields | L664, `openModal()` |
| `state.form` | create/edit draft aggregate | `openDrawer()`, `captureForm()` |
| `ROLES`, `ROLE`, `U()` | demo identity/permission | L338-L347 |
| `VTYPES`, terms/banks/currencies/countries | mock refs | L372-L395 |
| Thai address/bank arrays | cascading reference data | L397-L606 |
| `PRICE_LIST_BY_VENDOR` | read-only Price List mock | L700-L777 |

### §10.2 Explicit BACKEND comments

| HTML anchor | Current prototype | FRD target |
|---|---|---|
| L353 `POST /policy-center/v1/decisions/resolve` | `resolveApprovalChain()` reads mock `policyDecision`; empty/missing chain blocks submission without a local fallback | external Policy Center via API-08/FN-08 |
| L372 `API-11 /vendors/refs` | local constants/arrays | F-VENDOR-API-02 |
| L687 `GET /api/v1/vendors/{id}/transaction-eligibility` | `transactionEligibility()` local pure decision | F-VENDOR-API-19 / ENG-01 |
| L700-L701 Price List production comment | hardcoded map | F-VENDOR-API-20 / F-VENDOR-PRICE-LIST |

### §10.3 UI handler → FRD API plug map

| UI handler/renderer | Mock behavior now | Backend plug point |
|---|---|---|
| `getFiltered()`, `getPaginated()`, `renderList()` | filters `RAW` | API-01 |
| reference constants/getters | local arrays | API-02 |
| `openDrawer('view'|'edit')` | finds `RAW` record | API-03 |
| `persist()` create path | `RAW.unshift()` | API-04 |
| `persist()` edit path | `Object.assign()` + version | API-05 |
| `submitFromView()` draft branch | direct state mutation | API-06 |
| `confirmKyc()` | direct KYC/status/audit mutation | API-07 |
| `submitFromView()` pending-KYC branch | `newChain()` + state mutation | API-08 |
| `confirmApprove()`, `confirmReject()` | direct chain/status/audit mutation | API-09 |
| `confirmBlock()` block branch | direct state mutation | API-10 |
| `confirmUnblock()` | direct state mutation | API-11 |
| `confirmInactive()` | direct state mutation | API-12 |
| `confirmBlock()` blacklist branch | direct state mutation | API-13 |
| `verifyBank()` first click | pending verification | API-14 |
| `verifyBank()` second click | verified | API-15 |
| `disableBank()` → `modalBankDisable()` → `confirmBankDisable()` | reason-required soft disable + audit | API-16 |
| `addAttachments()` | reads browser File metadata only | API-17 |
| `removeAttachment()` | filters local array | API-18 |
| `transactionEligibility()` | local decision | API-19 |
| `viewPriceList()`, `navPriceList()` | mock table/toast stub | API-20 + downstream navigation |

### §10.4 Integration behavior to preserve

- Keep UI state values and visible labels from §8 when replacing mock data.
- Server capability/field policy must replace client-only permission helpers; UI may still use returned capabilities to hide actions.
- Preserve `version` display and wire mutation conflict behavior; HTML currently has no conflict UI.
- Keep masked values server-authoritative; do not send Restricted raw values to unauthorized clients.
- Replace mock file metadata with private upload/scan flow from FRD; never use filename/size alone as upload completion.
- Lucide loads from three CDNs in sequence; failure installs a no-op `createIcons()` and boot has a 5-second fallback (`L328`, `L1531-L1536`).

## §11 Three-Way Traceability + Drift Log

### §11.1 Brief ↔ FRD ↔ HTML

| Brief | FRD | HTML anchor |
|---|---|---|
| §2, §4.1 | UI-01; API-01/03 | `currentRoute()`, `renderList()` |
| §4.3 | UI-02; API-02..06/17/18 | `renderForm()`, `formStep1/2/3()`, `persist()` |
| §4.2 | UI-03; API-03/19/20 | `renderView()`, `view*()` |
| §6 O-06, §8.2 | UI-04; API-07; BR-VEN-10..14 | `modalKyc()`, `confirmKyc()` |
| §6 O-04/O-05, §8.4 | UI-05; API-08/09; BR-VEN-15..19 | `modalApprove()`, `modalReject()` |
| §6 O-08..O-11 | UI-06; API-10..13; BR-VEN-20/22/27/28 | `modalUnblock()`, `modalInactive()`, `modalBlock()` |
| §6 O-03, §7.4 | UI-07; API-05; BR-VEN-24/25 | `requestRemoveAddress()`, `modalAddressRemove()` |
| §6 O-07, §8.3 | US-07; API-14..16; BR-VEN-06/07/22/26 | `verifyBank()`, `disableBank()`, `modalBankDisable()`, `bankCard()` |
| §8.6 | permission matrix / BR-VEN-13/15/16/18 | permission helpers L348-L370 |
| §10.2 | E-002/E-007 contracts | backend comments + Price List/eligibility mocks |
| §9 | 06_TESTS §6.9 microcopy | renderers and toast call sites |

FRD ใช้ `UI-01..UI-07` แทน `P-xx`; ทั้ง 7 surfaces มีแถวครบ

### §11.2 Drift Log

| ID | Status | Type/severity | Synced result / remaining handoff |
|---|---|---|---|
| D-01 | RESOLVED | business text / HIGH | reject subtitle now says return for correction and KYC; handler/FRD remain `pending_kyc` |
| D-02 | RESOLVED | security / CRITICAL | current Policy role approves; Director/Admin override requires explicit decision flags |
| D-03 | RESOLVED | business / CRITICAL | unblock UI and handler re-check KYC + Policy; payment readiness is shown separately and still requires verified bank |
| D-04 | RESOLVED | business / HIGH | HTML+FRD agree: non-sanctions fail keeps/returns vendor `pending_kyc`; sanctions hit forces `blocked` |
| D-05 | RESOLVED | audit / HIGH | verified-bank deactivate opens a reason-required modal and stores reason in audit/history |
| D-06 | OPEN | resilience / MEDIUM | list has loaded/empty only; implement FRD loading/error/retry states |
| D-07 | OPEN | UX/accessibility / MEDIUM | implement dirty prompt, focus trap, return-focus and aria-live per FRD; approve any new visible copy |
| D-08 | RESOLVED | HTML technical / MEDIUM | `.shell-bar` now uses declared `--z-sticky` |
| D-09 | RESOLVED | HTML technical / LOW | obsolete index-based `setPrimaryBank()` removed; one ID-based handler remains |
| D-10 | PARTIAL | trace / MEDIUM | user-visible `BR-S03` removed; legacy internal comments may still be normalized during implementation |
| D-11 | RESOLVED | naming / MEDIUM | explicit `finance`→`finance_officer` and `compliance`→`compliance_officer` alias mapping documented |
| D-12 | RESOLVED | integration / CRITICAL | missing/empty Policy chain blocks submission; no local fallback is created |
| D-13 | OPEN | prototype gap / HIGH | backend must implement private upload, allowlist, scan and authorization per API-17/18 |
| D-14 | RESOLVED | source comment / LOW | source comment now states 5 tabs |
| D-15 | ACCEPTED AS-BUILT | API/UI reach / LOW | inactive action remains visible only for active vendor until product explicitly expands it |

Resolved rows were changed in the HTML/FRD sync revision; open rows are production implementation requirements, not contradictions in the approved prototype.

## §12 Diff from Previous HTML

— ไม่กำหนด comparison baseline ในรอบนี้  
`Related context/vendor/Vendor/vendor-master.html` เป็น historical reference แต่ไม่ใช่ approved previous version สำหรับ diff ดังนั้นไม่มี add/change/remove claim ใน section นี้

## §13 💡 Proposals — Not AS-BUILT

> รายการนี้ไม่ใช่คำสั่ง implement จนกว่าจะได้รับอนุมัติ/ทำ sync artifact

1. เพิ่ม loading/error/conflict/accessibility behavior ในระบบจริงตาม FRD; หากมี microcopy ใหม่ต้องอนุมัติก่อน
2. ทำ private upload/scan/authorization ตาม API-17/18; ห้ามยึด local file metadata ของ prototype เป็น security behavior
3. หากขยาย action ปิดใช้งานไปยังสถานะอื่น ให้ทำเป็น product decision ใหม่และ sync HTML/FRD/Test Case
