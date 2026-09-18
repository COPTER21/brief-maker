# HTML UI Brief · F-WH-ROP · Reorder Point

## 0. Document Control

- AS-BUILT source: `outputs/F-WH-ROP/F-WH-ROP.html`
- Paired FRD: `FRD_Pack/01_UI.md`, `02_API.md`, `03_LOGIC.md`, `05_RULES.md`
- Extraction date: 2026-09-18
- Mode: single-file SPA, three hash routes, in-memory prototype

## 1. Design Tokens

| Token | Value | Use |
|---|---|---|
| `--bg` | `#FAF8F5` | page background |
| `--ink` | `#111111` | primary text/sidebar |
| `--muted` | `#73757B` | secondary text |
| `--line` | `#DEDAD4` | borders |
| `--red` | `#FF3B30` | primary/action/critical |
| `--orange` | `#FF9A1F` | pending/demo/near |
| `--white` | `#FFFFFF` | surfaces |
| `--good` | `#157A41` | normal/found |

Font: `Satoshi, 'Noto Sans Thai', sans-serif`. Sidebar 232px and 58px rail at ≤1024. Topbar 52px. Table rows 44px. Drawer `min(920px,100vw)`.

## 2. Z-index Map

| Layer | Token/value | Anchor |
|---|---:|---|
| sticky table header | 1 | `.tbl th` |
| backdrop | `--z-backdrop:50` | `#backdrop` |
| drawer | `--z-drawer:60` | `#drawer` |
| picker portal | `--z-dropdown:65` | `.combo-menu` under `#overlay-root` |
| toast | `--z-toast:70` | `#toast` |

## 3. Route Map

`route()` accepts `records`, `history`, `settings`; invalid/empty hash falls back to `#/records`. `tabs()` renders the labels **นโยบายเติมสินค้า**, **คำแนะนำเติม**, **ประวัติ**. `hashchange` invokes `route()` then `render()`.

| Route | Page | Primary functions |
|---|---|---|
| `#/records` | policies | `ropLatestPolicies`, `ropRows`, `ropOpenPolicy`, `ropSaveFromDrawer` |
| `#/history` | suggestions | `ropSuggestions`, `ropEvaluatePair`, `ropRecompute`, `ropOpenCheck` |
| `#/settings` | audit history | `ropEvents`, `ropEventLabel`, `ropEventDetail`, `openView` |

## 4. Shared Page Anatomy

`.sidebar` → `.shell` → `.topbar` → `main.content` → `.page-head`/`.ph-actions` → `#tabs.drawer-tabs` → `#stats.stats` → `#mainPanel.panel.page-fill`. List shell contains `.toolbar.toolbar-flex`, `#search`, `#typeFilter`, `#statusFilter`, `#thead`, `#tbody`, `#empty`, and `#tableFoot`.

`renderTableOnly()` is the only filter/sort redraw path. Table scroll stays inside `.table-wrap`; header is sticky and footer remains below it. Stats derive from current data in `stats()`.

## 5. P-01 Policies (`#/records`)

- Page action **เพิ่มนโยบาย** opens `ropOpenPolicy()`.
- Clicking a row calls `openView(id)` and opens a read-only policy drawer.
- **แก้ไขนโยบาย** calls `ropEditSelected()` then the same policy form.
- Searchable master fields use `#ropItem`, `#ropWarehouse`, and optional `#ropVendor`; menus are `#ropItemMenu/#ropWarehouseMenu/#ropVendorMenu` with `.combo-option`.
- Numeric/date fields: `#ropMin`, `#ropMax`, `#ropSafety`, `#ropLeadTime`, `#ropAduWindow`, `#ropPackSize`, `#ropEffective`.
- `ropSetError()` writes to `{inputId}Error` and toggles `aria-invalid` on the input.
- `ropSaveFromDrawer()` disables `#saveBtn`, shows **กำลังบันทึก…**, calls `ropSavePolicy()`, closes on success and shows **บันทึกนโยบายแล้ว**.

## 6. P-02 Suggestions (`#/history`)

- Header shows **ตรวจอัตโนมัติล่าสุด:** separately from the manual button **รันตรวจตอนนี้**.
- `ropRecompute()` disables the button and uses **กำลังตรวจ…** while busy.
- The list displays three `.pill` states: **ต่ำกว่าจุด**, **ใกล้จุด**, **ปกติ**.
- Suggestion drawer displays **ATP จาก F009**, **จุดสั่งเติม**, **ที่มาของจุดสั่งเติม**, **On-Order (PO เปิด + PR Draft)**, **ADU / Lead Time**, **เป้าหมาย Max + Safety**, **สูตรก่อนปัด / Pack Size**, **จำนวนแนะนำ**, and **สถานะ**.
- Triggered rows expose **ส่งแจ้งเตือน**; triggered qty>0 rows also expose **สร้าง PR Draft ของคลังนี้**.
- Success stays in toast only: **ส่งแจ้งเตือนแล้ว**, **รายการนี้แจ้งเตือนไปแล้ว**, **สร้าง PR Draft แล้ว · {n} รายการ**, or **คลังนี้มี PR Draft ของรอบนี้แล้ว**.
- `#ropActionResult` is empty on success and reserved for retryable errors.

## 7. Check Pair / No-policy State

**ตรวจคู่สินค้า×คลัง** calls `ropOpenCheck()`. Both fields are searchable dropdowns. `ropCheckPair()` renders `#ropCheckResult` with `.check-card` after 24px separation.

- Found: **พบนโยบายเติมสินค้า** plus ATP/On-Order/ADU/qty.
- Missing: **ยังไม่มีนโยบายเติมสินค้า**, selected item/warehouse, and **เพิ่มนโยบาย**.
- The add action calls `ropCreatePolicyFromCheck(item,warehouse)` and prefills both pickers.
- Missing snapshot: **ไม่มีข้อมูลคงเหลือ** and no side-effect action.

## 8. P-03 History (`#/settings`)

`ropEventLabel/Detail/Items/Time/Status` convert internal records to human-readable cells. The table must not expose `event kind`, raw ref, `POL-*`, or integration event IDs as user-facing columns.

PR Draft detail shows **เลขที่ PR Draft** and **รอตรวจสอบและส่งอนุมัติ**. Drawer footer has only **ปิด**; there is no edit/delete.

## 9. Overlay Registry and Dismiss Rules

| Overlay | Open | Dismiss/cleanup |
|---|---|---|
| `#drawer` | `showDrawer(title,body,footer,mode)` | close button, Cancel, backdrop, Esc → `closeDrawer()` |
| master menu | input/focus → `ropFilterPicker()` then `portalMenu()` | option, outside click, drawer close; menu returns to/clears from portal |
| `#toast` | `toast(message)` | automatic after 2600ms |

`portalMenu()` positions fixed, widths at least 320px and flips above when there is insufficient space. `#overlay-root` prevents clipping by drawer scroll. Esc closes a visible menu before the drawer. No confirmation modal or destructive action exists.

## 10. State Matrix

| Condition | Visible state | Available action |
|---|---|---|
| valid policy | latest version row | view/edit creates new version |
| invalid field | red border + error below exact field | correct then save |
| ATP < ROP | ต่ำกว่าจุด | notify; create Draft when qty>0 |
| ROP ≤ ATP ≤ 1.2×ROP | ใกล้จุด | view only |
| ATP > 1.2×ROP | ปกติ | view only |
| no policy | separated status card | add prefilled policy |
| no snapshot | unavailable card | no side effect |
| busy | disabled initiating button + กำลัง… | wait |
| replay | already-exists toast | no duplicate |

## 11. Backend Anchors ↔ FRD

| HTML anchor | FRD contract |
|---|---|
| `ropSavePolicy` | API-02 / FN-02 / BR-ROP-01,02 / CSQ `master.changed` after commit |
| `ropPolicyActive` | FN-03 |
| `ropSnapshot`, `ropEvaluatePair` | API-03 / FN-04 / BR-ROP-03..05 |
| `ropRecompute` | API-04 / FN-05 / BR-ROP-07 |
| `ropNcCandidate`, `ropSendNC` | API-05 / FN-06 / NTF brief |
| `ropPreparePR`, `ropSendPR` | API-06 / FN-07 / F072 contract |
| `ropEvents`, `ropEvent*` | API-07 / FN-08 / BR-ROP-11 |

Production-only requirements not simulated by UI: server authorization, durable transaction/outbox, 409 optimistic conflict, F009/F072/ENG-NOTIFY availability, CSQ registration and retention.

## 12. Microcopy Anchors

Verbatim strings used by automated/manual tests: **เพิ่มนโยบาย**, **แก้ไขนโยบาย**, **บันทึก**, **ยกเลิก**, **ตรวจคู่สินค้า×คลัง**, **ตรวจนโยบาย**, **รันตรวจตอนนี้**, **ส่งแจ้งเตือน**, **สร้าง PR Draft ของคลังนี้**, **ยังไม่มีนโยบายเติมสินค้า**, **ไม่มีข้อมูลคงเหลือ**, **ส่งแจ้งเตือนแล้ว**, **สร้าง PR Draft แล้ว**, **เลขที่ PR Draft**, **รอตรวจสอบและส่งอนุมัติ**, **ไม่พบรายการที่ตรงกับตัวกรอง**.

## 13. Demo-only Elements

`.demo-only` wraps sample identity/DEMO badge. Production must hide/remove it. It does not change role, permission or data.

## 14. Drift Log

- Resolved: former PR mock wording replaced by actual F072 Draft flow.
- Resolved: formula now uses Safety in ROP and Max+Safety target.
- Resolved: notification/PR success removed from drawer and kept in toast.
- Resolved: history columns use human language and show Draft number/status.
- Resolved: CSQ anchor declares only policy `master.changed → SecC`; threshold is NTF and PR lifecycle belongs to F072.
- Known production gap: `CSQ-ROP-01`, vocabulary and enabled sensitivity remain registry OQs; they are not visible UI behavior.
