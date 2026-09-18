# UI BRIEF — F-WH-STKTRF Stock Transfer

## 0. Document control and pairing

| Item | Value |
|---|---|
| HTML source | `F-WH-STKTRF.html` · preflight html-generator-v9.1 · 2026-09-17 |
| FRD pair | `FRD_Pack/` v1.0 |
| Status | AS-BUILT · verified against HTML |
| Scope | One single-file SPA; four route forms and ten business surfaces |

## 1. Design tokens AS-BUILT

Anchor: `:root` near HTML start. Color tokens: `--c-navy`, `--c-navy-2`, `--c-primary`, `--c-primary-hover`, `--c-teal`, `--c-teal-light`, `--c-orange`, `--c-ink`, `--c-mute`, `--c-mute-2`, `--c-mute-3`, `--c-placeholder`, `--c-line`, `--c-line-2`, `--c-line-3`, `--c-bg-off`, `--c-success`, `--c-warning`, `--c-danger`, plus Pattern-Q aliases `--c-border`, `--c-border-soft`, `--c-text`, `--c-text-mute`, `--c-text-soft`, `--c-off-white`, `--c-white`, `--c-slate`, `--c-purple`, and state alpha tokens.

Sizing/type anchors: `--sidebar-w`, `--shell-h`, `--fs-h1`, `--fs-h2`, `--fs-h3`, `--fs-body`, `--fs-sub`, `--fs-meta`, `--fs-cap`, `--fs-kpi`, spacing `--sp-xs` through `--sp-xl`, radius `--r-xs` through `--r-full`/`--r`, shadows `--sh-md`, `--sh-lg`, `--sh-xl`. Font stack: Satoshi, Noto Sans Thai, system-ui. Scrollbar is thin with a light thumb; sidebar uses a light-on-dark variant.

### Z-index map

| Token | Value | Main anchors |
|---|---:|---|
| `--z-toast` | 80 | `.toast` |
| `--z-modal` | 60 | `.modal-overlay` |
| `--z-drawer` | 51 | `.overlay-wrap` drawer panel |
| `--z-backdrop` | 50 | drawer backdrop |
| `--z-dropdown` | 30 | `.combo-pop`, `.menu-fixed`, `.disabled-tip-msg` |
| `--z-sticky` | 10 | shell/table sticky heads |
| `--z-shell` | 10 | `.sidebar` |
| `--z-content` | 1 | content base |

## 2. Route map

| Route | Render/open anchor | Refresh behavior |
|---|---|---|
| `#/list` | `render()` → `renderList()` | default/fallback landing |
| `#/create`, `#/create/dup-:id` | `openCreateDrawer(null, r.arg)` | list remains under overlay |
| `#/edit/:id` | `openCreateDrawer(r.id)` | non-draft redirects to view |
| `#/view/:id` | `openViewDrawer(r.id)` / `renderViewDrawer()` | drawer restored from hash |

`navigate()` writes the hash; the `hashchange` listener calls `render()`. `preserveRenderState()`/`restoreRenderState()` retain page/drawer scroll and focused input after rerender.

## 3. Layout shell

Anchors: `.sidebar`, `.main`, `.shell-bar`, `.breadcrumb`, `.content`, `.page-fill`. Desktop uses fixed sidebar and sticky white shell. At the declared media breakpoint the content becomes full-width and sidebar moves off-canvas with `.sidebar.open`. Landing `.table-wrap` and `.table-scroll` provide horizontal scrolling; `.scroll-table` prevents column overlap.

## 4. Page anatomy

### 4.1 Landing — `#/list`

`renderList()` builds `.ph`, KPI cards, tabs, `renderFilterBar()`, `#table-wrap`, `renderTableHtml()`, footer/pagination, and `renderAttachmentsLanding()`. Filters include global search/creator, warehouse pair, mode/status/date/reason. Table exposes creator and transfer reason and uses scroll rather than clipping.

### 4.2 Create/Edit — `#/create`, `#/edit/:id`

`openCreateDrawer()` renders `.overlay-wrap` + wide drawer. Five steps: source choice, main data/mode route, B2 v2 line table, upload attachment, review/approvers. Functions `goStep()`, `validateStep()`, `renderCreateDrawer()`, `persist()` and submit/DOA handlers own behavior.

### 4.3 View — `#/view/:id`

`openViewDrawer()` + `renderViewDrawer()` render header/action bar and tabs from `renderDetailTab()`, `renderTransitTab()`, PDF, signatures and history. Actions depend on committed status/identity. Receive-disabled reasons are rendered with `.disabled-tip`/`.disabled-tip-msg`.

## 5. Component inventory and states

| Component | Selector/function anchors | States present |
|---|---|---|
| Buttons | `.btn`, `.btn-primary`, `.btn-secondary`, `.btn-danger`; action handlers | default, hover, disabled, busy/loading; no generic error state |
| Filters | `.filter-grid`, `renderFilterBar()` | collapsed/expanded, active values, clear; invalid state — none |
| Data table | `.table-wrap`, `renderTableHtml()` | data, filtered empty, no-data, sorted, paged, horizontal scroll |
| Line editor | B2 table in `renderCreateDrawer()` | empty row, valid, field warning, duplicate, insufficient stock |
| Combobox | `.combo-pop`, picker open/close functions | closed/open/search/no match; Esc dismiss |
| Status pills | `ST_LABEL`, status class mapper | all eleven labels in §8 |
| File upload | file input + attachment renderers | idle, selected/uploaded, invalid type, remove |
| Toast | `.toast`, `showToast()` | info/success/warning/error, timed dismiss |
| Disabled explanation | `.disabled-tip`, `.disabled-tip-msg` | hidden, hover/focus/focus-within visible |

## 6. Overlay Registry

| Overlay | Anchor | Open/close/dismiss |
|---|---|---|
| Create/view drawer | `.overlay-wrap`, drawer IDs | route opens; close functions/navigate; Esc after modal/menu |
| Business modal | `.modal-overlay`, `modalShell()`, `closeModal()` | explicit cancel/action; Esc closes; business mutation only on confirm |
| Combobox | `.combo-pop` | picker opens; Esc removes first |
| Row action menu | `.menu-fixed`, `#row-menu` | action/open; Esc removes after combobox |
| Disabled tooltip | `.disabled-tip-msg` | hover/focus only; pointer-events none |
| Sidebar | `.sidebar` | responsive toggle; not in main Esc chain |
| Toast | `.toast` | `showToast()` and timer |

Extractor also sees `.overlay-wrap`. There is no focus trap and no explicit global scroll lock in this HTML; focus/scroll restoration exists via `preserveRenderState()`.

## 7. Interaction spec

Esc handlers are at HTML lines **1368** and **2454** in the verified source. The main chain at 2454 is: `.combo-pop` → `#row-menu` → `.modal-overlay` → `#create-drawer` → `#view-drawer`. Modal `ยกเลิก` only closes. Shipment confirmation uses `openShipModal()`/`modalShell()`, never native `confirm`. Mutation handlers set busy/disabled UI and complete after their guarded callback. Overlay focus trapping is absent; this is AS-BUILT, not a recommendation.

## 8. State-driven UI matrix

| Value | Verbatim label | Main action |
|---|---|---|
| `draft` | ร่าง | edit/submit/cancel |
| `pending_approval` | รออนุมัติ | current approver action |
| `approved` | อนุมัติแล้ว | move/ship/cancel |
| `moved` | ย้ายสำเร็จ | print/reversal |
| `in_transit` | ส่งออกแล้ว — อยู่ระหว่างทาง | receive/return |
| `partial` | รับบางส่วน | receive/return/shortage |
| `closed` | ปิดใบ (รับครบ) | print/reversal |
| `closed_diff` | ปิดใบพร้อมส่วนต่าง | print/reversal |
| `returned` | ตีกลับคืนต้นทางแล้ว | view/print |
| `cancelled` | ยกเลิก | view/audit |
| `reversed` | กลับรายการแล้ว | view/audit |

Transit label map is also verbatim: `ไม่มีของค้าง`, `ยังค้างระหว่างทาง`, `ถึงปลายทางครบ`.

Prototype label-map inventory (not a production authorization source): `ธนกฤต ศรีวิชัย`, `ธก`, `คลังสินค้า`; role labels `เจ้าหน้าที่คลัง`, `หัวหน้าคลัง`, `ผู้จัดการคลังสินค้า`, `ผู้จัดการฝ่ายบัญชี`, `ผู้อำนวยการสายงาน`.

## 9. Microcopy verbatim

### Buttons

`ยืนยันส่งออก`, `ยืนยันย้ายสินค้า`, `ส่งออกจากต้นทาง`, `ย้ายสินค้า`, `Export CSV`, `กลับรายการ`, `ดาวน์โหลด`, `ตีกลับคืนต้นทาง`, `บันทึกแบบร่าง`, `บันทึกและส่งอนุมัติ`, `พิมพ์`, `ยืนยันตัดส่วนต่าง`, `ยืนยันรับ`, `ย้อนกลับ`, `ล้าง`, `ล้างตัวกรอง`, `สร้างใบย้ายสินค้า`, `ส่งอนุมัติ`, `อนุมัติ`, `อนุมัติตัดส่วนต่าง`, `เปลี่ยน`, `เพิ่มรายการ`, `เลือกผู้อนุมัติ`, `เลือกไฟล์`, `แก้ไข`, `แนบเพิ่ม`, `ไม่อนุมัติ`.

### Toast inventory (extractor strings, exact substrings)

```text
) — แก้จำนวนตามยอดล่าสุด หรือตีกลับไปแก้
bin ต้นทางและปลายทางต้องต่างกัน
กรุณากรอกข้อมูลให้ครบถ้วน
กรุณาระบุเหตุผล
กรุณาเพิ่มรายการสินค้าอย่างน้อย 1 รายการ
กรุณาเลือกใบย้ายต้นแบบ หรือเปลี่ยนเป็น "สร้างใหม่"
กลับรายการได้เฉพาะใบที่ของขยับแล้ว — ใบค้างระหว่างทางใช้ “ตีกลับคืนต้นทาง”
กำลังดำเนินการ กรุณารอสักครู่
ของกักกันย้ายได้เฉพาะไปช่องเก็บกักกันด้วยกัน — ล้าง bin ปลายทางแล้ว
ข้าม
คู่คลังนี้ยังไม่มีจุดพักระหว่างทาง — ติดต่อผู้ดูแลผังตำแหน่ง
คู่คลังนี้ยังไม่มีจุดพักระหว่างทาง — ติดต่อผู้ดูแลผังตำแหน่งให้ตั้งค่าก่อน
จำนวนที่ย้ายต้องมากกว่า 0 ทุกบรรทัด
จำนวนที่ย้ายเกินยอดคงเหลือของ
ตีกลับ
ตีกลับคืนต้นทางแล้ว — ของกลับเข้าช่องเก็บเดิมครบ
ตีกลับได้เฉพาะเจ้าหน้าที่ของคลังปลายทาง
ต้องอนุมัติครบสายก่อน
ถูกล็อก —
ทุกบรรทัดต้องระบุ bin ต้นทางและ bin ปลายทาง
บันทึกการรับแล้ว — ต่อไปคือขออนุมัติตัดส่วนต่างระหว่างทาง
บันทึกการรับแล้ว — ยังค้างระหว่างทาง
บันทึกร่างแล้ว
ผู้ที่กดส่งออกจากต้นทาง ยืนยันรับเองไม่ได้ (แยกหน้าที่)
ผู้ที่กดส่งออกจากต้นทางเซ็นอนุมัติการตัดส่วนต่างไม่ได้
พร้อมย้ายสินค้า
พร้อมส่งออกจากต้นทาง
มีบรรทัดซ้ำ (bin ต้นทาง + สินค้า + bin ปลายทาง):
มีแถวที่ยังไม่ได้เลือกสินค้า — เลือกหรือลบแถวก่อน
ยกเลิก
ยกเลิกการตัดส่วนต่าง — ส่วนต่างยังค้างระหว่างทาง
ยกเลิกได้เฉพาะก่อนของขยับ — ใบนี้ส่งของออกไปแล้ว ใช้ “ตีกลับคืนต้นทาง” หรือ “กลับรายการ” แทน
ยอดคงเหลือที่
ยังส่งอนุมัติไม่ได้ —
ยังไม่มีการแจ้งเตือนใหม่
ยังไม่มีรายการสินค้าในใบนี้
ยังไม่ได้ระบุจำนวนที่รับ
ยืนยันรับได้เฉพาะเจ้าหน้าที่ของคลังปลายทาง (
ระบุ bin ที่ลงจริงของทุกบรรทัดที่รับ
รับครบแล้ว — ปิดใบ
รับเกินจำนวนที่ส่งออกไม่ได้ — ถ้าของงอกจริงต้องใช้ใบปรับยอดสต๊อก
รายการ (ตัวอย่าง)
สร้างใบกลับรายการ
ส่ง
ส่งขออนุมัติตัดส่วนต่างแล้ว — รอ
ส่งอนุมัติได้เฉพาะฉบับร่าง
ส่งออก CSV
หน่วย
อนุมัติขั้น
อนุมัติครบสาย —
อนุมัติครบสาย — ปิดใบพร้อมส่วนต่าง
อนุมัติครบสาย — ยังมีของค้างระหว่างทาง
อนุมัติแล้ว — ส่งต่อ
เปลี่ยนไป (เหลือ
เปลี่ยนไป — ตรวจจำนวนก่อนส่งอนุมัติ
เพื่ออนุมัติแล้ว — รอ
เพื่อแก้ไข
เมนูผู้ใช้ (ตัวอย่าง)
เรียบร้อย
เลือกผู้อนุมัติให้ครบทุกขั้น
เลือกเหตุผลของส่วนต่างให้ครบ
แก้ไขได้เฉพาะฉบับร่าง
แนบหลักฐานอย่างน้อย 1 ไฟล์ก่อนขออนุมัติ
แนบไฟล์แล้ว
แล้ว — ส่งต่อ
แล้ว — เลือกผู้อนุมัติก่อนส่ง
ใบนี้ถูกกลับรายการไปแล้ว — กลับรายการซ้ำไม่ได้
ใบนี้ไม่อยู่ในสถานะรอรับ
ใบร่าง
ไฟล์
ไฟล์ — รองรับเฉพาะ PDF, JPG และ PNG
ไม่มีรายการตัดส่วนต่างที่รออนุมัติ
ไม่ใช่ผู้มีสิทธิ์ในขั้นปัจจุบัน
ไม่ใช่ผู้อนุมัติขั้นปัจจุบัน หรือเป็นผู้ส่งออกจากต้นทาง
```

### Empty/confirmation strings seen by extractor

`ตีกลับคืนต้นทาง ` / `ของที่ยังค้างระหว่างทาง ` and the continuation ` หน่วย จะถูกส่งกลับเข้าช่องเก็บต้นทางเดิม · ไม่นับเป็นของหาย จึงไม่เข้าสายอนุมัติการตัดส่วนต่าง`.

The extractor also records the dynamic interpolation marker `?`; it is not literal UI copy but is retained here so the generated inventory is complete.

## 10. Data binding and BACKEND anchors

| UI action | HTML function anchor | FRD/API |
|---|---|---|
| list/detail | `renderList()`, `findDoc()`, `renderViewDrawer()` | API-01/API-03 |
| draft/edit | `persist()`, create state handlers | API-02/API-04 |
| submit/approve | DOA modal handlers | API-05/API-06 |
| ship | `openShipModal()`, confirmed shipment handler | API-07 |
| receive | `renderReceiveModal()`, receipt confirmation | API-08 |
| return | reason modal callback | API-09 |
| shortage | shortage request/approval functions | API-10/API-11 |
| cancel/reversal | reason/reversal functions | API-12/API-13 |
| PDF/files | `openPdf()`, attachment handlers | API-14/API-15 |

HTML `DOCCFG`, `DOA`, `NTF`, `CSQ`, `FWD-WIRE` comments are wiring anchors only. Server/engine results replace mock data without changing visible state contracts.

## 11. Three-way traceability and Drift Log

| Brief | FRD | HTML |
|---|---|---|
| §4.1 landing | P-01 / API-01 | `#/list`, `renderList()` |
| §4.2 wizard | P-02 / API-02/04/05/15 | `#/create`, `#/edit/:id`, `openCreateDrawer()` |
| §4.3 view | P-03 / API-03 | `#/view/:id`, `openViewDrawer()` |
| §6 approval modal | P-04/P-05 / API-05/06 | modal handlers + DOA anchors |
| §6 receive | P-06 / API-08 | `renderReceiveModal()` |
| §6 shortage | P-07 / API-10/11 | shortage modal/approval functions |
| §6 reason | P-08 / API-09/12/13 | reason/reversal handlers |
| §4.3 PDF/signatures | P-09/P-10 / API-14 | PDF/signature tabs |

Drift: **none material**. FRD models four routes plus six overlay/tab surfaces matching HTML. Extractor only recognizes literal `#/list`; dynamic `navigate()`/`getRoute()` forms were manually verified. `ME` and mock role/stock maps are prototype data, not production authorization contracts.

## 12. Diff from prior version

Current approved version adds custom disabled-action tooltip, CUBE shipment confirmation modal, stronger receive/reversal/shortage guards, aligned filter/line layouts, actual file upload, creator/reason columns and horizontal table scrolling. Temporary user switcher was removed before handoff.

## 13. 💡 Proposals (not AS-BUILT)

— No proposal in this handoff.
