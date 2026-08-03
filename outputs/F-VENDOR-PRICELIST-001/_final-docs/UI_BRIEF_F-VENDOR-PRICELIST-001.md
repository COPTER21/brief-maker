# HTML UI Brief — F-VENDOR-PRICELIST-001 Vendor Price List

> AS-BUILT extraction จาก `vendor-price-list-v6.html` เท่านั้น; จุดที่ FRD ต้องการแต่ HTML ไม่มีอยู่ใน §11 Drift Log

## §0 Document Control + Pairing

| Field | Value |
|---|---|
| Feature | F-VENDOR-PRICELIST-001 Vendor Price List |
| HTML source of truth | `vendor-price-list-v6.html` |
| `<title>` | `รายการราคาคู่ค้า · CUBE` |
| FRD pair | `FRD_F-VENDOR-PRICELIST-001_Pack/` v1.0 |
| Brief status | AS-BUILT / IN-REVIEW |
| Extraction date | 2026-08-03 |
| Primary code anchors | `render()`, `state`, `renderList()`, `renderBatch()`, `renderCompare()`, `renderVendorDetail()` |

HTML เก่าใน `vendor-pricelist/vendor-pricelist.html` ไม่ได้ใช้ทำ diff เชิง design ใน Brief นี้ เพราะ current HTML ถูกล็อกเป็น source of truth; ดู §12.

## §1 Design Tokens AS-BUILT

### 1.1 CSS variables — `:root`

| Group | Tokens |
|---|---|
| Z-index | `--z-sticky:10`, `--z-shell:20`, `--z-dropdown:30`, `--z-backdrop:50`, `--z-drawer:51`, `--z-modal:60`, `--z-toast:80` |
| Brand/action | `--c-navy:#111111`, `--c-primary:#FF3B30`, `--c-primary-hover:#E62E24`, `--c-teal:#FF9A1F`, `--c-teal-light:#FFB763` |
| Text | `--c-ink:#111111`, `--c-mute:#54565C`, `--c-mute-2:#73757B`, `--c-mute-3:#9A9CA2` |
| Lines/background | `--c-line:#DEDAD4`, `--c-line-2:#E9E5E0`, `--c-line-3:#F1EEEA`, `--c-bg-off:#FAF8F5` |
| Semantic | `--c-success:#1F9D55`, `--c-warning:#E8870F`, `--c-danger:#E62E24` |
| Shell | `--sidebar-w:232px`, `--shell-h:52px` |
| Typography | `--fs-h1:22px`, `--fs-h2:17px`, `--fs-h3:15px`, `--fs-body:14px`, `--fs-sub:13px`, `--fs-meta:12px`, `--fs-cap:11px`, `--fs-kpi:28px` |
| Spacing | `--sp-xs:4px`, `--sp-sm:8px`, `--sp-md:12px`, `--sp-lg:20px`, `--sp-xl:28px` |
| Radius | `--r-xs:4px`, `--r-sm:6px`, `--r-md:8px`, `--r-lg:12px`, `--r-full:999px` |

Font stack anchor: `body { font-family:'Satoshi','Noto Sans Thai',system-ui,sans-serif }`; Thai font import uses Noto Sans Thai. `trace` uses `ui-monospace,monospace`. Scrollbar is 5px via `::-webkit-scrollbar`; Firefox uses `scrollbar-width:thin`.

### 1.2 Z-index map — high to low

| Layer | z | Anchor |
|---|---:|---|
| Toast | 80 | `.toast`, `#toast` |
| Modal backdrop + modal | 60 | `.modal-backdrop`, `.modal`, `#modalBackdrop`, `#modalEl` |
| Search list | 60 | `.ss-list` appended to `document.body` in `ssRenderList()` |
| Drawer | 51 | `.drawer`, `#drawer` |
| Drawer backdrop | 50 | `.drawer-backdrop`, `#drawerBackdrop` |
| User dropdown | 30 | `.user-menu`, `#userMenu` |
| Sidebar | 20 | `.sidebar` |
| Sticky shell bar | 10 | `.shell-bar` |
| Sticky table header | 3 | `.table-scroll.is-sticky thead th` |
| Stepper internals | 2/1 | `.stepper-circle`, connector pseudo-element, `.doa-step-dot` |

## §2 Route Map

| Hash route | Renderer | Breadcrumb |
|---|---|---|
| `#/vendor-price-list` | `renderList()` | Purchase › Vendor Price List |
| `#/vendor-price-list/vendor/:vendorId` | `renderVendorDetail()` | Purchase › Vendor Price List › `{vendor name}` |
| `#/vendor-price-list/batch` | `renderBatch()` | Purchase › Vendor Price List › Batch Entry |
| `#/vendor-price-list/compare` | `renderCompare()` | Purchase › Vendor Price List › เปรียบเทียบราคา |

- Default: `DOMContentLoaded` sets `#/vendor-price-list` when hash is empty.
- Refresh safety: renderer derives route from `location.hash` in `getRoute()` and reruns on `hashchange`.
- Unknown hash: `render()` falls through to `renderList()`; no Not Found page in HTML.
- Navigation anchor: `navigate(route)` assigns `location.hash='#/'+route`.

## §3 Layout Shell

| Region | Anchor | AS-BUILT anatomy |
|---|---|---|
| Sidebar | `.sidebar` | fixed 232px; brand; `.sb-nav`; module groups Purchase/Master Data/Policy; footer `Prototype · v6` |
| Active navigation | `.sb-item.is-active[data-feature="vendor-price-list"]` | `Vendor Price List`; calls `navigate('vendor-price-list')` |
| Disabled nav | `.sb-item.is-disabled` | Purchase Request, Purchase Order, Vendor Master, Product Master, DOA Matrix |
| Main shell | `.main` | left offset by sidebar; contains shell bar and page content |
| Shell bar | `.shell-bar` | sticky 52px; `#breadcrumb`; notification icon; `.user-chip`; `#userMenu` |
| Content mount | `#page-content.content` | replaced wholesale by `render()` |

Responsive rule present in HTML: only `@media(max-width:1280px){.breakdown{grid-template-columns:repeat(2,minmax(0,1fr))}}`. No mobile/sidebar-collapse behavior exists.

## §4 Page Anatomy

### 4.1 Main list — `renderList()` / P-01

```text
#page-content
├─ pageHead(): title/subtitle/count + Import/Batch/Compare/Create actions
├─ statsHTML(): KPI cards
├─ .section-head
│  ├─ .view-switch: ทุกรายการ / แยกตามคู่ค้า
│  └─ .section-sub
└─ .card
   ├─ toolbarHTML(): #listSearch + status select + reset
   └─ priceTable() or vendorTable()
```

Rows come from `filtered()`, `priceTable()`, `vendorTable()`, `rowHTML()`. Full codes are rendered by row/cell templates. Sort triggers `sortBy()`; pagination/page size are driven by `state.page` and `state.pageSize=8`.

### 4.2 Vendor drill-in — `renderVendorDetail()` / P-02

`.back-link` → `pageHead(vendor name, vendor code...)` → `.card` with `priceTable(list)`. Active vendor gets `สร้างรายการราคา`; other vendor state gets `.pill.pill-archived` text `คู่ค้าไม่พร้อมใช้งาน`. Create calls `openDrawer('create',null,vendor.id)`.

### 4.3 Batch Entry — `renderBatch()` / P-03

`.back-link` → header actions `เพิ่มแถว` and submit/loading → `.card > .table-scroll > .table.batch-table` → `.batch-summary`. Per-row rendering is `batchRow()`; master fields use `searchSelectHTML()`; remove uses `.batch-remove-btn`; validation class is `.batch-error`.

### 4.4 Compare — `renderCompare()` / P-06

`.back-link` → page header → `.page-stack` → `.card.compare-controls` with product search, qty, date, target currency and aligned calculate action → results `.card` containing `compareRunbar()` and `compareTable()`.

Result construction filters Active VPL/vendor/product/date, applies `applicablePrice()`/`netUnit()`/`FX`, then `.sort((a,b)=>a.thb-b.thb)`. Rank marker anchor `.rank-best` includes trophy + `1` and title/accessible context in result template.

## §5 Component Inventory + States

| Component | Selector / renderer | States in HTML |
|---|---|---|
| Primary/secondary/ghost/danger button | `.btn` variants | default, hover, focus-visible, disabled; loading by icon + text in compare/batch/import/submit |
| Icon action | `.icon-btn`, `.ra-btn`, `.batch-remove-btn` | hover; danger/success; disabled when only one batch row |
| Search dropdown | `.search-select`, `searchSelectHTML()`, `ss*()` | closed/open, query, highlighted option, selected, empty, clear; keyboard Arrow/Enter/Escape/Tab |
| Text/select | `.input`, `.select`, `.batch-input` | default/focus/disabled; error text containers exist; batch row error class |
| Status pill | `.pill-*`, `statusLabel()`, `statusClass()` | draft/pending_approval/active/inactive/rejected |
| View tabs | `.view-switch button` | active/inactive |
| Drawer tabs | `.drawer-tabs`, `tabBtn()` | overview/versions/approval active state |
| Table scroll | `.table-scroll` | horizontal scroll where table min-width requires it; sticky header variant |
| Empty state | `emptyHTML()` | no records / no comparison result variants |
| Stepper | `stepperHTML()` | step 1 active, step 2 active/completed |
| Import outcome | `.import-outcome`, `importOutcomeHTML()` | appears after commit until dismissed |
| Toast | `#toast`, `showToast()` | success/info/warning class + visible/hidden animation |

### 5.1 Status-driven table actions — `rowStatusActions()`

| Status | Label/class | Row actions |
|---|---|---|
| `draft` | `ร่าง` / `pill-draft` | pencil `แก้ไขร่าง` |
| `pending_approval` | `รออนุมัติ` / `pill-pending` | no row icon; actions available in view drawer |
| `active` | `ใช้งาน` / `pill-active` | pencil `สร้างราคาฉบับใหม่`; power `ปิดใช้งาน` |
| `inactive` | `ปิดใช้งาน` / `pill-archived` | restore `เปิดใช้งาน` |
| `rejected` | `ปฏิเสธ` / `pill-discontinued` | no dedicated row action in current records |

### 5.2 Form mode matrix — `openDrawer()`, `formDrawerHTML()`, `formStep1()`

| Mode | Title | Identity |
|---|---|---|
| create | `สร้างรายการราคา` | vendor/product searchable; UOM dependent; currency editable/default |
| edit draft | `แก้ไขร่าง` | vendor/product/UOM/currency editable |
| edit active | `สร้างราคาฉบับใหม่` | vendor/product/UOM/currency locked + helper |
| clone active | `สร้างรายการใหม่จากรายการเดิม` | vendor/product locked; UOM/currency editable and must change |
| view | product name + status | tabbed, no form |

## §6 Overlay Registry

| Overlay | Anchor | Size/z | Open / Dismiss AS-BUILT |
|---|---|---|---|
| Form/View drawer | `#drawer.drawer`, `#drawerBackdrop`, `renderDrawer()` | width 920px, max 96vw; z 51/50 | open via `openDrawer()`/`openClonePrice()`; close X, footer button, backdrop, Esc; slide 280ms / backdrop 220ms |
| Confirm modal | `#modalEl.modal`, `#modalBackdrop`, `renderModal()` | 440px, max 92vw/90vh; z 60 | close X, Cancel, backdrop, Esc, success action; scale/fade 200ms |
| Import modal | `.modal.is-lg`, `importHTML()` | 680px | same dismiss rules as modal |
| Search result popover | `.ss-list`, `ssRenderList()` | fixed, max-height 320px; z 60 | focus/click open; select/clear/Escape/Tab/`ssCloseAll()` close; positioned by `ssPosition()` and appended to body |
| User menu | `#userMenu.user-menu` | 240px; z 30 | `.user-chip` toggles; click outside closes; Esc closes only after no modal/drawer |
| Toast | `#toast.toast` | max 380px; z 80 | auto hides after 3500ms; no manual close |

No notification popover exists; `toggleNotif()` only shows toast `ไม่มีการแจ้งเตือนใหม่`.

## §7 Interaction Spec AS-BUILT

### 7.1 Escape chain

Global `document.keydown` executes exactly:

1. if `state.modal.open` → `closeModal()`
2. else if `state.drawer.open` → `closeDrawer()`
3. else → remove `is-open` from `#userMenu`

Search dropdown handles its own Escape and stops propagation in `ssOnKey()`, so it closes before the global overlay chain.

### 7.2 Keyboard and semantics

- `ssOnKey()`: ArrowDown/ArrowUp move highlight; Enter picks; Escape/Tab closes and restores selected text.
- `enhanceInteractiveSemantics()` adds `role=button` + `tabindex=0` to non-native `[onclick]` elements, excluding buttons/links/inputs/backdrops/stopPropagation containers.
- Global CSS applies focus-visible outline to native controls and role buttons/links.
- No explicit global key handler converts Enter/Space on the dynamically enhanced non-native role buttons; see Drift D-06.

### 7.3 Focus preservation and positioning

- `render()` records active element ID and text selection, rerenders, then restores focus/selection when the same ID exists.
- Search list is `position:fixed`, appended to body and placed using bounding rect in `ssPosition()` to avoid clipping inside drawer/table scroll.
- `positionOpenSearchSelects()` runs on resize/scroll pathways in code.
- Drawer/modal do not implement focus trap, initial focus, opener restore or body scroll lock.

### 7.4 Prototype async behavior

`calculateCompare()`, `submitBatch()`, `submitPrice()` and `confirmImport()` use fixed `setTimeout` to simulate backend latency. This is AS-BUILT prototype behavior, not a production wait strategy.

## §8 State-Driven UI Matrix

### 8.1 Global `state`

| Branch | Values / consumers |
|---|---|
| `view` | `flat|vendor` → `renderList()` |
| `filters` | search/status → `filtered()`/toolbar |
| `sort`, `page`, `pageSize` | table sort/pagination |
| `drawer` | `open,mode,id,vendorId,productId,uom,tax,currency,step,tab` |
| `modal` | `open,type,id`; type import/deactivate/activate/approve/reject |
| `submitting` | Batch submit button loading state |
| `lastImportResult` | main list import outcome |
| `compareDraft` vs `compare` | dirty input vs last calculated result |
| `compareLoading`, `compareCalculatedAt` | disabled loading button/run metadata |
| `batch[]` | editable row data + `error` |

### 8.2 View drawer action matrix — `viewDrawerActions()`

| Record state | Actions |
|---|---|
| pending_approval | `ปฏิเสธ`, `อนุมัติ` |
| inactive | `เปิดใช้งาน` |
| draft | `แก้ไขร่าง` |
| active | `สร้างราคาฉบับใหม่` |

### 8.3 Confirmation result — `confirmAction()`

approve → active; reject → draft; deactivate → inactive; activate → active. Deactivate/activate increment prototype `version`. Approval blocks when requester fixture equals current user fixture; activate blocks invalid current master eligibility.

## §9 Microcopy Verbatim Inventory

### 9.1 Main pages / actions

- Titles: `รายการราคาคู่ค้า`, `Batch Entry`, `เปรียบเทียบราคา`.
- Header actions: `Import`, `Batch Entry`, `เปรียบเทียบราคา`, `สร้างรายการราคา`, `เพิ่มแถว`, `ตรวจสอบและส่งอนุมัติ`, `คำนวณ`, `กำลังคำนวณ…`, `กำลังส่ง…`.
- Navigation: `กลับหน้ารายการ`, `ทุกรายการ`, `แยกตามคู่ค้า`, `ล้างตัวกรอง`.
- Search placeholder: `ค้นหาคู่ค้า สินค้า หรือรหัส`.
- Page subtitle: `จัดการราคาซื้อที่ผ่านการอนุมัติ พร้อมประวัติราคาและรายละเอียดการคำนวณ`.
- Confidential note: `ข้อมูลราคาสำหรับใช้ภายในบริษัทเท่านั้น`.
- Batch subtitle: `กรอกหลายรายการ ตรวจสอบคู่ค้ากับ F-VENDOR และสินค้า/UOM กับ Product Master ก่อนส่งอนุมัติ`.
- Batch summary: `ผ่าน {N} แถว`, `ต้องแก้ {N} แถว`, `ข้อมูลจะยังไม่ถูกบันทึกจนกว่าทุกแถวผ่านและผู้ใช้ยืนยัน`.

### 9.2 Master controls / form

- Placeholders: `ค้นหารหัสหรือชื่อคู่ค้า`, `ค้นหารหัสหรือชื่อสินค้า`, `ค้นหาคู่ค้า`, `ค้นหาสินค้า`, `ค้นหารหัสหรือชื่อสินค้า`, `ค้นหา...`, `0.00`, `ระบุเหตุผลการสร้างหรือเปลี่ยนราคา`.
- Empty/option copy: `ไม่พบรายการ`, `เลือกสินค้าก่อน`, `เลือกสินค้า active และ purchasable`.
- Labels: `คู่ค้า`, `สินค้า`, `Purchase UOM`, `สกุลเงิน`, `ประเภทราคา`, `ราคาตั้ง`, `ราคาต่อจำนวน`, `ส่วนลด %`, `ค่าขนส่งต่อหน่วย`, `ภาษีซื้อ`, `เริ่มใช้`, `สิ้นสุด`, `เหตุผล`.
- Buttons: `ยกเลิก`, `บันทึกร่าง`, `ถัดไป`, `กลับ`, `ยืนยันและส่งอนุมัติ`, `สร้างรายการใหม่จากรายการนี้`, `ปิด`.
- Review labels: `ราคาฉบับที่จะส่ง`, `สถานะหลังส่ง`, `การเปลี่ยนแปลงจากราคาปัจจุบัน`, `ขั้นตอนการอนุมัติ`, `เกณฑ์ตรวจสอบเพิ่มเติม`, `ระยะเวลาดำเนินการ`.
- Locked label/helper anchors: `ล็อก`, `ข้อมูลนี้เป็นส่วนหนึ่งของรายการเดิม จึงไม่สามารถแก้ไขได้`, `คัดลอกจากรายการเดิม`, `เลือกหน่วยซื้อใหม่จาก Product Master`, `เลือกสกุลเงินสำหรับรายการใหม่`.

### 9.3 View/approval

- Tabs: `ภาพรวม`, `ประวัติราคา`, `Approval & Audit`.
- Actions: `แก้ไขร่าง`, `สร้างราคาฉบับใหม่`, `อนุมัติ`, `ปฏิเสธ`, `เปิดใช้งาน`, `ปิดใช้งาน`.
- Footer pattern: `ราคาฉบับที่ {N} · รหัสอ้างอิง {VPL-ID}`.
- History: `ฉบับที่ {N} · {status}`, `ฉบับที่ {N} · เก็บเป็นประวัติ`, `ข้อมูลราคาฉบับก่อนหน้าถูกเก็บไว้และตรวจสอบย้อนหลังได้`.

### 9.4 Confirm modals

| Type | Title | Body |
|---|---|---|
| deactivate | `ปิดใช้งานรายการราคา?` | `รายการนี้จะไม่ถูกใช้ในการเลือกราคาและเปรียบเทียบราคา` |
| activate | `เปิดใช้งานรายการราคา?` | `รายการนี้จะกลับมาใช้ในการเลือกราคาและเปรียบเทียบราคา` |
| approve | `อนุมัติราคาฉบับนี้หรือไม่?` | `ราคาใหม่จะเริ่มใช้ตามวันที่ที่กำหนดและถูกเก็บไว้สำหรับตรวจสอบย้อนหลัง` |
| reject | `ปฏิเสธราคาฉบับนี้หรือไม่?` | `รายการจะกลับไปเป็นร่างและต้องระบุเหตุผล` |

Reject placeholder: `ระบุเหตุผลที่ปฏิเสธ`. Secondary button: `ยกเลิก`.

### 9.5 Import

- `Import Vendor Price List`, `อัปโหลดไฟล์ ตรวจสอบข้อมูล และยืนยันก่อนนำเข้า`.
- Steps: `เลือกไฟล์`, `ตั้งค่าการนำเข้า`, `ผลการตรวจสอบ`, `ตัวอย่างข้อมูล`.
- File: `ไฟล์ Vendor Price List`, `เลือกไฟล์ที่จัดคอลัมน์ตาม Template`, `เลือกไฟล์`, `Template`, `ยังไม่ได้เลือกไฟล์`, `กรุณาเลือกไฟล์เพื่อเริ่มตรวจสอบข้อมูล`.
- Modes: `เพิ่มรายการใหม่และอัปเดตรายการเดิม`, `แทนที่รายการที่ยังไม่ถูกนำไปใช้`.
- Notes: `ระบบจะอัปเดตรายการเดิมที่ตรงกัน และเพิ่มรายการใหม่โดยไม่ลบข้อมูลที่มีอยู่`; `ระบบจะแทนที่ได้เฉพาะรายการร่างหรือรายการที่รออนุมัติ และจะข้ามรายการที่เริ่มใช้งานแล้ว`.
- Validation: `ยังไม่ได้ตรวจสอบข้อมูล`, `ผลการตรวจสอบจะแสดงหลังจากเลือกไฟล์ CSV`, `รายการทั้งหมด`, `ผ่านการตรวจ`, `ไม่ผ่าน`, `คู่ค้า active ใน F-VENDOR`, `สินค้า active และสั่งซื้อได้`, `UOM ตรงกับ Purchase UOM`, `พร้อมนำเข้า 4 แถว`, `ยืนยันนำเข้า`, `กำลังนำเข้า…`.

### 9.6 Toasts — every `showToast()` call pattern

- `ไม่มีการแจ้งเตือนใหม่`
- `กรุณาเลือกคู่ค้าที่มีสถานะใช้งานจากรายการ`
- `กรุณาเลือกสินค้าที่ใช้งานและสั่งซื้อได้จากรายการ`
- `สถานะคู่ค้าเปลี่ยนแล้ว รายการใหม่นี้ไม่สามารถส่งได้`
- `กรุณาระบุสินค้า ปริมาณ และวันที่ให้ครบถ้วน`
- `คำนวณราคาใหม่แล้ว`
- `ต้องมีอย่างน้อย 1 แถว`
- `ลบแถวแล้ว`
- `กรุณากรอกข้อมูลให้ครบถ้วน`
- `ส่งรายการราคา {N} รายการเพื่ออนุมัติแล้ว`
- `สร้างรายการใหม่ได้จากรายการที่ใช้งานอยู่เท่านั้น`
- `กรุณาเปลี่ยน Purchase UOM หรือสกุลเงินก่อนดำเนินการต่อ`
- `กรุณาเลือกคู่ค้าและสินค้าที่พร้อมใช้งานก่อนบันทึกร่าง`
- `Purchase UOM ไม่ตรงกับ Product Master`
- `กรุณาเปลี่ยน Purchase UOM หรือสกุลเงินก่อนบันทึกร่าง`
- `บันทึกร่างแล้ว`
- `คู่ค้าไม่อยู่ในสถานะใช้งาน กรุณาเลือกใหม่`
- `สินค้าไม่อยู่ในสถานะใช้งานหรือซื้อไม่ได้ กรุณาเลือกใหม่`
- `กรุณาเปลี่ยน Purchase UOM หรือสกุลเงินก่อนส่งอนุมัติ`
- `ส่งรายการราคาเพื่ออนุมัติแล้ว`
- `ไม่สามารถอนุมัติรายการที่ตนเองสร้างได้`
- `ไม่สามารถเปิดใช้งานได้ เนื่องจากคู่ค้าหรือสินค้าไม่พร้อมใช้งาน`
- `อนุมัติแล้ว`, `ส่งกลับเป็นร่างแล้ว`, `ปิดใช้งานรายการแล้ว`, `เปิดใช้งานรายการแล้ว`
- `นำเข้าสำเร็จ · เพิ่มใหม่ {N} · อัปเดต {N}` หรือ `ไม่มีรายการใหม่ · ข้าม {N}`

## §10 Data Binding & BACKEND Anchors

| HTML mock/state | Render/handler | FRD API plug |
|---|---|---|
| `VENDOR_MASTER` + source comment | `vendorSearchOptions()`, `isActiveVendorId()`, `applyVendorStatusChangedEvent()` | F-VENDOR APIs/events; VPL API validation |
| `PRODUCT_MASTER` + source comment | `productSearchOptions()`, `purchaseUomOptions()`, `isPurchasableProductId()` | Product APIs/status/UOM |
| `RECORDS` / `state.records` | list/detail/compare/form/status renderers | API-01/02/03..08 |
| `IMPORT_PREVIEW_ROWS` | `validateImport()`, `applyImportRows()` | API-11/12/17 |
| `state.batch` | `batchSet()`, `submitBatch()` | API-09/10 |
| `FX` | `renderCompare()`, `compareTable()` | API-13 + FX Master |
| `POLICY` | `approvalPreviewData()`, `formStep2()`, `viewTabHuman()` | API-16 + Policy/DOA |
| `state.compareDraft/state.compare` | `setCompareDraft()`, `calculateCompare()` | API-13 |
| drawer/form state | `saveDraft()`, `submitPrice()` | API-03/04/05/07 |
| modal state | `confirmAction()` | API-06/08 |

Only explicit BACKEND comment in HTML: subscribe to `F-VENDOR vendor_status_changed_event` and invalidate cached eligibility by tenant/vendor. There are no real fetch calls; all writes mutate JS arrays.

## §11 Traceability + Drift Log

### 11.1 Three-way trace

| Brief | FRD | HTML anchor |
|---|---|---|
| §4.1 list | UI P-01 · API-01/02/03/08 | `renderList()`, `toolbarHTML()`, `priceTable()`, `vendorTable()` |
| §4.2 vendor drill-in | UI P-02 · API-01/03 | `renderVendorDetail()` |
| §4.3 batch | UI P-03 · API-09/10 · BR-VPL-02/03/06 | `renderBatch()`, `batchRow()`, `submitBatch()` |
| §5.2 form drawer | UI P-04 · API-03/04/05/07 | `openDrawer()`, `formDrawerHTML()`, `formStep1/2()` |
| §5.1/8.2 view drawer | UI P-05 · API-02/06/08 | `viewDrawerHTML()`, `viewDrawerActions()`, `viewTabHuman()` |
| §4.4 compare | UI P-06 · API-13 · BR-VPL-15/16 | `renderCompare()`, `calculateCompare()`, `compareTable()` |
| §6 confirm | UI P-07 · API-06/08 | `openConfirm()`, `renderModal()`, `confirmAction()` |
| §6 import | UI P-08 · API-11/12/17 | `openImport()`, `importHTML()`, `validateImport()`, `confirmImport()` |
| §5.1 statuses | Rules §5.2 | `statusLabel()`, `statusClass()`, `rowStatusActions()` |
| §9 toasts | Tests §6.10 | all `showToast()` calls |

### 11.2 Drift Log

| ID | Type | Evidence | Impact / disposition |
|---|---|---|---|
| D-01 | FRD-only | FRD supports multi-tier rows; HTML `formStep2()` only has one price set and never renders tier-row editor | Dev cannot implement tier create/edit 1:1 from HTML. Keep as explicit unresolved UI coverage gap; do not invent layout in this Brief. |
| D-02 | FRD-only | DB/BRD has `incl_vat` and `vendor_item_code`; no form controls in HTML | Backend fields may exist but UI input is absent. Treat as not exposed in current HTML. |
| D-03 | FRD-only | FRD production states loading/error/403 for APIs; HTML uses mock arrays and only selected loading buttons | Dev must use FRD behavior, but visual treatment beyond existing button/empty styles is not specified by HTML. |
| D-04 | FRD-only | FRD accessibility requires focus trap/restore and scroll lock; HTML has none | Must be added using design-system behavior without changing layout; current HTML is not evidence of these behaviors. |
| D-05 | HTML-only prototype | fixed `setTimeout` simulates API actions | Replace with API state; never copy fixed delay into production. |
| D-06 | HTML defect/gap | `enhanceInteractiveSemantics()` adds role/tabindex to non-native clicks but no Enter/Space activation handler | Production should use native buttons/links or design-system keyboard behavior; AS-BUILT is incomplete. |
| D-07 | HTML-only | unknown routes fall back to list | FRD acknowledges current behavior; app shell may own 404 outside this feature. |
| D-08 | Resolved alignment | Company/Site absent from form | FRD LD-03 matches HTML: company from session, site null. |
| D-09 | Resolved alignment | threshold shown as 10 from `POLICY` fixture | FRD requires runtime API-16/config; HTML number is fixture only. |

## §12 Diff from Previous HTML

ไม่มี line-by-line historical diff ใน output นี้. Current authority is `vendor-price-list-v6.html`; old `vendor-pricelist/vendor-pricelist.html` is requirement coverage reference only per LOCK-VPL-02 and LD-01.

## §13 ข้อเสนอ (ไม่ใช่ AS-BUILT)

ไม่มีข้อเสนอ design ใหม่ใน Brief นี้. จุด D-01/D-02/D-04/D-06 ต้องให้ PM/design-system owner ตัดสินหรือกำหนด pattern ก่อน dev เพิ่ม UI; ห้ามตีความว่า Brief ได้ออกแบบส่วนที่หายไปแล้ว.

## Verification Gate

| Check | Result |
|---|---|
| Routes documented | 4/4 |
| Overlay types documented | drawer, confirm modal, import modal, search popover, user menu, toast — 6/6 |
| `showToast()` calls documented | 28/28 calls · 24/24 unique argument patterns |
| Page/component claims have selector/function anchors | PASS |
| Status enum mapping documented | 5/5 UI statuses |
| Escape chain matches actual handler | PASS |
| Declared z-index values mapped | 7/7 token layers + local internals |
| FRD P-01..P-08 trace rows | 8/8 |
| Drift log non-empty and explicit | 9 entries |
| Invented AS-BUILT behavior | 0; proposals isolated in §13 |

**Verdict:** PASS for extraction/traceability. UI coverage gaps D-01/D-02/D-04/D-06 remain deliberately visible and are not silently designed in this document.
