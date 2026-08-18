# UI_BRIEF — F-WH-PICK Picking (AS-BUILT)

## 0. Document Control + Pairing

| Item | Value |
|---|---|
| HTML source | `f-wh-picking.html` |
| FRD | `FRD_Pack/` P-01..P-03 / API-01..16 / BR-PICK-01..17 |
| Routes | `#/list`, `#/create/:soId`, `#/view/:pickId` |
| Drift | none; LOCK-12 removes replenishment/download-like row icon |

## 1. Design Tokens AS-BUILT

Anchor `:root`: color tokens `--c-navy`, `--c-primary`, `--c-teal`, `--c-success`, `--c-slate`, `--c-off-white`, `--c-white`, borders/text/warning/danger plus alpha variants; radius `--r-sm/--r/--r-lg`; shadows `--sh-sm/md/lg/xl`; shell `--sw`, `--hh`. Fonts: Noto Sans Thai then Satoshi and system fallback. External font stylesheets may fall back offline; no JS CDN dependency.

### z-index high→low

| Token | Value | Use |
|---|---:|---|
| `--z-toast` | 80 | toast |
| `--z-portal` | 70 | combobox portal |
| `--z-modal` | 60 | modal |
| `--z-drawer` | 51 | drawer |
| `--z-backdrop` | 50 | backdrop |
| `--z-dropdown` | 30 | dropdown |
| `--z-shell` | 19 | shell |
| `--z-sticky` | 10 | sticky region |
| `--z-content` | 1 | content |

## 2. Route Map

| Route | Parser/renderer | Refresh behavior |
|---|---|---|
| `#/list` | `getRoute()` → `renderListPage()` | default and refresh-safe |
| `#/create/:soId` | `openCreateDrawer(route.from)` | list renders first, then create drawer |
| `#/view/:pickId` | `openViewDrawer(route.id)` | list renders first, then view drawer |

`hashchange` invokes `render`; unknown route falls back to list. `closeAllOverlays()` clears overlay root before route overlay opens.

## 3. Layout Shell

`.shell` contains `.sb` ERP sidebar and main area. Sidebar active item is “ใบหยิบสินค้า (Picking)”; list page header/title/actions and cards render in `#page-content`. Desktop base has minimum width and responsive evidence at 1024/1440.

## 4. Page Anatomy

### 4.1 P-01 `#/list`

`.ph` title/summary/actions → `.drawer-tabs` queue/picks → `.card` toolbar/search/filter → `.tbl` body/pagination. Queue checkbox state derives from `gate()` and `soPickStatus()`; rows drill into SO modal. Pick rows open P-03.

### 4.2 P-02 `#/create/:soId`

`#create-drawer` and backdrop: header/stepper/body/footer. Step 1 SO selection, step 2 `.combo-selection` assignee + equipment/priority/note, step 3 route-sorted lines. Save actions call create logic. `.combo-pop` is portalled outside clipped drawer.

### 4.3 P-03 `#/view/:pickId`

`#view-drawer`: header status/action group → 4 `.drawer-tab` values → content. Line tab uses `.line-tbl`; details tab shows SO values; print tab embeds A4 view; history tab uses timeline/audit. Footer actions derive from Pick status and persona.

## 5. Component Inventory + States

| Component/anchor | Default/active | Disabled/empty/loading/error |
|---|---|---|
| `.combo-selection`, `.combo-pop`, `assigneeCombo`, `cbKey` | selected/open/search/keyboard | no match handled; disabled not used |
| `.tbl`, `renderQueueTable`, `renderPicksTable` | hover/selected/sorted/paged | gate rows disabled; loading marker exists; empty renderer supported |
| `.pill`, `statusPill` | queue/Pick status labels | no loading/error state |
| `.btn` | primary/secondary/ghost/danger/success | native disabled prevents action |
| `.prog` | normal/warn/bad | zero progress supported |
| `showToast` | info/success/warning/error | timed dismiss |
| reason modal | open/form/confirm | missing reason warns |
| pick-line modal `#pl-modal` | scan/qty/full/short/relocate | confirm disabled until valid |
| print view | preview/print | long rows wrap; no edit state |

## 6. Overlay Registry

| Overlay | Anchor/open function | Dismiss | Stack |
|---|---|---|---|
| drawer/backdrop | `#create-drawer`, `#view-drawer`; open/close functions | close control/Esc/route | `--z-backdrop` + `--z-drawer` |
| `.modal-overlay` | `modalShell`, reason/assign/pick/relocate/SO functions | close button, Esc; backdrop per rendered handler | `--z-modal` |
| `.combo-pop` | `assigneeCombo`, `cbOpen/cbKey` | selection, click outside, Esc in `cbKey` | `--z-portal` |
| `.overlay-wrap` | shell overlay wrapper | handler-defined | modal/drawer layer |
| `.suggest-list` | suggestion list | selection/outside | dropdown layer |
| toast | `showToast` | timed | `--z-toast` |

No explicit scroll lock, focus trap, or focus restoration exists in this HTML.

## 7. Interaction Spec

Global Esc handler at HTML line **1094** closes `.modal-overlay` first, then create drawer, then view drawer. Combobox keyboard handler at line **1166** processes its own Escape plus arrow/enter behavior. Click/outside handlers dismiss combo as implemented. Route navigation changes hash. Allocation/pick mock mutates in-memory state and rerenders; production binding must use FRD APIs.

## 8. State-driven UI Matrix

| Pick status | Main visible behavior |
|---|---|
| draft | assign/cancel/print |
| assigned | start/reassign/cancel/print |
| in_progress | line pick/relocate/refresh/hold/finish/close-short |
| on_hold | resume |
| picked | send Packing |
| to_pack | read/print/history |
| cancelled | read/print/history |

Personas: `wh_lead` all actions; `picker` assigned record; `viewer` read-only. Queue labels cover ready/locked/open/partial/done behavior through `gate()` and `soPickStatus()`.

## 9. Microcopy Verbatim

### Buttons

“จำลองของเข้า”, “บันทึกร่าง”, “บันทึกหยิบ”, “บันทึกและมอบหมาย”, “ปิดงานแบบขาด”, “พัก”, “พิมพ์”, “มอบหมาย”, “ย้อนกลับ”, “รีเซ็ต”, “สร้างงานเติม/โอน”, “สร้างใบหยิบ”, “ส่งต่อ Packing”, “ส่งออก CSV”, “หยิบครบ”, “หยิบครบทั้งหมด”, “หยิบต่อ”, “หาใหม่”, “เริ่มหยิบ”.

### Toast strings found by shared extractor

| Variant | Text |
|---|---|
| info | “(เดโม)” |
| info | “Inventory รับเข้า/เติมแล้ว:” |
| warning | “wave สูงสุด” |
| warning | “กรุณาระบุเหตุผล” |
| warning | “ตรวจสอบคลังและจำนวน SO ใน wave อีกครั้ง” |
| success | “บันทึกแล้ว” |
| success | “ปิดงานแบบขาดแล้ว — พร้อมส่ง Packing” |
| success | “มอบหมาย” |
| success | “มอบหมายแล้ว” |
| success | “ยกเลิกแล้ว” |
| warning | “รวม wave ได้เฉพาะ SO คลังเดียวกัน” |
| success | “สร้างงานเติม/โอนแล้ว (Inventory) — ENG-NOTIFY inv.replenish_request” |
| warning | “สร้างใบหยิบไม่ได้ เพราะมี SO ที่ยังไม่ผ่านเงื่อนไขการปล่อยงาน” |
| info | “สลับบทบาทเป็น” |
| success | “หยิบครบ — พร้อมส่งต่อ Packing” |
| success | “หยิบครบทุกบรรทัด” |
| warning | “เฉพาะหัวหน้าคลังสร้างใบหยิบ” |
| success | “เปลี่ยนตำแหน่งแล้ว” |
| success | “เปลี่ยนตำแหน่งแล้ว (จองจริงเมื่อบันทึก)” |
| info | “เริ่มหยิบ — บันทึกทีละบรรทัด (สแกน)” |
| warning | “เลือกผู้หยิบ” |
| warning | “เลือกใบสั่งขายอย่างน้อย 1 ใบ” |
| error | “ไม่มีบรรทัดที่หยิบได้ — ตรวจสต๊อก/เติม Pick Face ก่อน” |

No extractor-recognized empty-state pair exists; table/render logic still defines contextual no-result UI outside the extractor pattern.

## 10. Data Binding & BACKEND Map

| HTML mock/function | FRD target |
|---|---|
| SOS/gate/queueRows | API-01 + FN-01 |
| PICKS/pickRows/openViewDrawer | API-02 + FN-02 |
| savePick | API-03 + FN-03/ENG-01 |
| confirmAssign/startPick | API-04/05 + FN-05/06 |
| confirmPickLine | API-06/07 + FN-07/08 |
| confirmReloc/refreshOne | API-08/09 + FN-09/10 |
| requestReplenish | API-10 + FN-11; internal-only UI trigger after LOCK-12 |
| finish/close/hold/cancel/toPack | API-11..15 + FN-12..16 |
| printable tab | API-16 + FN-17 |

Mock-only: Finance release, simulate inbound, pick-all remaining and generated identifiers. Replace with APIs; never ship as production business shortcuts.

## 11. Traceability + Drift Log

| Brief | FRD | HTML anchor |
|---|---|---|
| P-01 list | `01_UI` P-01 / API-01,02 | `renderListPage`, queue/pick table renderers |
| P-02 create | P-02 / API-03,04,08,09 | `openCreateDrawer`, `renderCreateDrawer`, assignee combo |
| P-03 view | P-03 / API-05..16 | `openViewDrawer`, line/state modal functions |
| source SO only | BR-PICK-17 / AT-22 | `PICK_SOURCE_TYPES=['SO']` and no non-SO queue path |
| removed row icon | LOCK-12 / AT-16 | line action markup has no requestReplenish icon button |

Drift Log: none. Internal mock `requestReplenish()` remains callable by tests but is not an exposed row action, matching PM/BA decision.

## 12. Diff from prior

Latest reviewed delta: assignee popover stack/spacing fixed; selected assignee vertical spacing fixed; download-like replenishment icon removed. FRD and checklist record these outcomes.

## 13. Proposals (not AS-BUILT)

None. OQ-01..06 are business/architecture questions in FRD, not UI proposals.
