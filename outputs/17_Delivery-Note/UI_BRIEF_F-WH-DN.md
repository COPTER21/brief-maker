# UI_BRIEF — F-WH-DN Delivery Note (AS-BUILT)

## 0. Document Control + Pairing

| Item | Value |
|---|---|
| HTML source | `f-wh-delivery-note.html` |
| FRD | `FRD_Pack/` P-01..P-03 / API-01..17 / BR-DN-01..22 |
| Routes | `#/list`, `#/create/:packIds`, `#/view/:dnId` |
| Drift | none; Manual/Transfer/transport refinements are present in both HTML and FRD |

## 1. Design Tokens AS-BUILT

Anchor `:root` contains 38 variables: color family `--c-*`, radius `--r-*`, shadows `--sh-*`, shell dimensions and typography support. Font sources are Satoshi/Fontshare and Noto Sans Thai/Google Fonts with local/system fallbacks. There is no JavaScript CDN dependency.

### z-index map (raw values in CSS)

| Value | Anchor/use |
|---:|---|
| 100 | `#toast-root` |
| 90 | `.combo-pop` search dropdown portal |
| 60 | `.modal-overlay`, fixed header/hint/suggestion layers |
| 50 | `.overlay-wrap`, sticky header |
| 2 / 1 | local stepper/progress/content stacking |

The HTML does not declare named `--z-*` tokens; values above are extracted from the actual selectors.

## 2. Route Map

| Route | Parser/renderer | Refresh behavior |
|---|---|---|
| `#/list` | `getRoute()` → `renderListPage()` | default; no drawer |
| `#/create/:packIds` | `render()` → `createDN(r.packs)` | renders list then opens Reference confirmation modal |
| `#/view/:dnId` | `render()` → `openViewDrawer(r.id)` | current prototype clears overlay and resolves back to list on full refresh per approved fix |

`hashchange` calls `render()`. Unknown hashes become list. Render clears `#overlay-root` before opening route-specific UI.

## 3. Layout Shell

The ERP shell contains sidebar navigation, top/header region and `#page-content`. “ใบส่งของ (Delivery Note)” is active. List/table remains the page base while route overlays are displayed. Responsive desktop behavior is proven by Step-5 E2E and screenshots.

## 4. Page Anatomy

### 4.1 P-01 `#/list`

Page header/actions → KPI cards → queue/DN tabs → search/filter toolbar → `.tbl` rows/pagination. Queue rows show pack/source/recipient/warehouse-or-transfer route/boxes/weight/deadline. Selection is disabled when combine key differs. Main actions call `createFromSel()` or `openManualCreate()`.

### 4.2 P-02 `#/create/:packIds`

`createDN()` opens `.modal-overlay` containing selected-pack summary, total boxes/weight, assignee and transport inputs, schedule and confirmation footer. `bindPickers()`/combobox functions populate searchable Employee/carrier/driver/vehicle options. Confirm creates Reference draft; cancel creates nothing.

### 4.3 P-03 `#/view/:dnId`

`#view-drawer`/`renderViewDrawer()` render status header, action group, tabs and body. Tabs are delivery information, items/boxes, printable delivery note and append-only history. State/mode decides editable cards and footer actions. Manual records insert the Manual-status action.

## 5. Component Inventory + States

| Component / anchor | Default/active | Disabled/empty/loading/error |
|---|---|---|
| `.combo-pop`, `cbOpen/cbKey`, `gcOpen/gcKey` | open/search/highlight/select/keyboard/manual option | no match; invalid manual form; no explicit loading |
| assignee PEOPLE list | employee-only selected state | no manual option; inactive filtered in production |
| driver/vehicle forms | master/manual snapshot | blank/phone/plate warnings |
| `.tbl`, list renderers | hover/selected/tab-filtered | incompatible checkbox disabled; “ไม่มีใบแพ็ครอออกใบส่งของ” |
| status `.pill` maps | draft/ready/in_transit/failed/delivered/partial/returned/cancelled | no loading state |
| `.btn` | primary/secondary/ghost/danger | native disabled/state hidden |
| `.modal-overlay` | open/confirm/cancel | inline/toast validation |
| view drawer | open/tab/state actions | missing ID shows “ไม่พบข้อมูล” |
| toast | info/success/warning/error | timed dismiss |
| A4 document tab | before POD/after POD/print | long content wraps; no edit state |

## 6. Overlay Registry

| Overlay | Anchor / open | Dismiss | Stack |
|---|---|---|---|
| `.overlay-wrap` | `openViewDrawer`, drawer shell | close control/Esc/route render | raw z 50 |
| `.modal-overlay` | `modalShell`, create/reason/POD/dispatch/manual functions | cancel/close/Esc; backdrop where handler exists | raw z 60 |
| `.combo-pop` | `cbOpen`, `gcOpen` | select, click-outside, own Escape | raw z 90 |
| `.suggest-list` | searchable suggestions | select/click-outside | raw z 60 |
| toast root | `showToast` | timed | raw z 100 |

No explicit scroll lock, focus trap or focus restoration exists in this HTML. Production implementation should not invent different dismiss behavior without a UI revision.

## 7. Interaction Spec

Global Escape handler at HTML line **1014** closes `.modal-overlay` first, then view drawer. General combobox handler at line **1090** and transport combobox handler at line **1183** consume Escape to close `.combo-pop` before it reaches the global chain; they also handle arrows and Enter. `navigate()` changes hash. Data mutations in the prototype are in-memory and reset on refresh.

## 8. State-driven UI Matrix

| Mode/status | Visible behavior |
|---|---|
| reference draft | editable delivery data, ready/cancel/print |
| reference ready | read view plus explicit edit, dispatch/cancel/print |
| reference in_transit | tracking, failed, POD, cancel |
| reference failed | reschedule, return all, cancel |
| delivered/partial/returned/cancelled | read/print/history and eligible downstream decision |
| manual any allowed status | “อัปเดตสถานะ Manual”; target+reason; no automatic GI/source sync |

Source labels include Sales Order and Stock Transfer. Transfer presentation uses origin→destination. Role rendering covers head warehouse, assigned operator/driver and read-only viewer.

## 9. Microcopy Verbatim

### Buttons

“จัดส่งซ้ำ (backorder)”, “ดาวน์โหลด”, “บันทึกผลส่ง (POD)”, “พร้อมส่งอีกครั้ง”, “พิมพ์”, “พิมพ์เอกสารก่อน”, “ยืนยันพร้อมส่ง”, “ยืนยันออกรถ · ตัดสต๊อก”, “ยืนยันออกใบส่งของ”, “รีเซ็ต”, “สร้างเอกสาร Manual”, “สร้างแบบ Manual”, “ส่งต่อวางบิล”, “ส่งออก CSV”, “ออกรถ / ส่งมอบขนส่ง”, “ออกใบส่งของ”, “อัปเดตสถานะ Manual”, “แก้ไขข้อมูลส่ง”, “แนบภาพลายเซ็น”.

### Toast strings found by shared extractor

| Variant | Text |
|---|---|
| info | “(เดโม)” |
| warning | “กรอกข้อมูลที่มี * ให้ครบก่อนยืนยันพร้อมส่ง” |
| warning | “กรอกชื่อ นามสกุล และเบอร์โทรให้ครบ” |
| warning | “กรอกเลขติดตามพัสดุก่อนส่งมอบขนส่ง” |
| warning | “กรอกเลขอ้างอิง ผู้รับ และที่อยู่จัดส่งให้ครบ” |
| warning | “กรุณาระบุเลขทะเบียน / เลขรถ” |
| warning | “กรุณาระบุเหตุผล” |
| info | “ดาวน์โหลด PDF (mock)” |
| warning | “ตีกลับทั้งใบ — คืนสต๊อกและแจ้ง Sales แล้ว” |
| success | “นัดส่งใหม่แล้ว — รอออกรถ” |
| success | “บันทึกลายเซ็นบนหน้าจอแล้ว (mock)” |
| warning | “บันทึกส่งไม่สำเร็จ — นัดส่งใหม่หรือตีกลับทั้งใบ” |
| info | “ปิดจบเท่าที่ส่งได้ — แจ้ง Sales/บัญชี” |
| success | “พร้อมส่ง — รอออกรถ” |
| success | “ยกเลิกแล้ว — ใบแพ็คกลับเข้าคิวรอออกใบส่งของ” |
| warning | “รวมได้เฉพาะประเภทต้นทาง ลูกค้า และที่ส่งเดียวกัน” |
| warning | “ระบุชื่อผู้รับสินค้า” |
| warning | “รูปแบบเบอร์โทรไม่ถูกต้อง” |
| info | “สถานะสุดท้าย — บันทึกผลส่ง (POD) แทน” |
| success | “สร้าง” |
| info | “สลับบทบาทเป็น” |
| success | “ส่งต่อวางบิล/ออกใบกำกับ (mock · AR Invoice S6)” |
| success | “ออกรถแล้ว — ตัดสต๊อกจริงและแจ้งลูกค้าแล้ว” |
| success | “อัปเดตสถานะ Manual แล้ว” |
| info | “อัพเดตครบทุกสถานะแล้ว” |
| warning | “เฉพาะหัวหน้าคลัง” |
| warning | “เฉพาะหัวหน้าคลังสร้างใบส่งของ Manual” |
| warning | “เฉพาะหัวหน้าคลังออกใบส่งของ” |
| success | “เปิดงานค้างส่งแล้ว — กลับคิวหยิบ/แพ็ค (mock)” |
| success | “แนบภาพลายเซ็นแล้ว (mock)” |
| success | “แนบรูปหลักฐานแล้ว (mock)” |
| success | “แบบ Manual แล้ว” |
| warning | “ไม่พบใบแพ็คที่พร้อมออกใบส่งของ” |
| info | “— แจ้งลูกค้าแล้ว” |

Extractor found no structured empty-state pair; visible table empty text is recorded in §5.

## 10. Data Binding & BACKEND Map

| HTML mock/function | FRD target |
|---|---|
| PACKS/queueRows/renderRows | API-01 + FN-01 |
| DNS/dnRows/openViewDrawer | API-02/17 + FN-02 |
| createDN/confirm create | API-03 + FN-03/04 |
| delivery edit/bindPickers | API-04/05 + FN-04/05 |
| markReady/dispatch | API-06/07 + FN-06/07/ENG-DN-01 |
| advanceTrack/openFailModal | API-08/09 + FN-08/09 |
| confirmPod | API-10 + FN-10/ENG-DN-01/02 |
| reschedule/return/cancel/backorder | API-11..14 + FN-11..14 |
| openManualCreate/openManualStatusModal | API-15/16 + FN-15/16 |
| docTab/historyTab | API-17 + document snapshot contract |

Mock-only: identifiers, downloaded PDF action, real carrier tracking, billing and all in-memory mutation. Replace with the mapped contracts; do not ship mock shortcuts.

## 11. Traceability + Drift Log

| Brief | FRD | HTML anchor |
|---|---|---|
| P-01 list | `01_UI` P-01 / API-01,02,15 | `renderListPage`, `renderRows`, `openManualCreate` |
| P-02 Reference confirm | P-02 / API-03..05 | `getRoute`, `createDN`, picker/combo handlers |
| P-03 detail | P-03 / API-06..17 | `openViewDrawer`, `renderViewDrawer`, state modal functions |
| Transfer isolation | BR-DN-15 / AT-28..30 | transfer fixture/ref renderer/source-specific logic |
| Manual isolation | BR-DN-18/19 / AT-31..35 | `openManualCreate`, `openManualStatusModal` |
| transport policy | BR-DN-20 / AT-05..09 | PEOPLE vs DRIVERS/VEHICLES and manual options |

Drift Log: none. Prototype number prefix is mock; production document code policy is documented in `DOCCFG_BRIEF_F-WH-DN.md` and does not change the AS-BUILT screen fixture.

## 12. Diff from prior

Reviewed fixes include visible Manual button icon, deep-refresh drawer closure, first failed attempt numbering, Stock Transfer fixture/display, Manual isolation and PM/BA searchable assignment/transport with validated manual driver/vehicle entry.

## 13. Proposals (not AS-BUILT)

None. Unresolved business/architecture items are maintained in BRD/FRD OQs, not invented as UI requirements.
