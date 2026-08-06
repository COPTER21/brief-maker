# UX Check Report — WarehouseBin.html (F-LOCATION-MASTER-001 · Warehouse & Bin / Location Hierarchy)

---

## 🔁 RE-GATE — Iteration 3 (2026-08-06) · after material change (Hierarchy Tree added · role switcher realigned · display name renamed)

> Trigger: HTML changed materially since the iter-2 PASS — (a) **Hierarchy Tree view** added as an approved NON-STANDARD dual-view (DECISION_LOG **D12**), (b) **role switcher realigned** to the create button (**D13**), (c) **display name renamed** to `คลังและตำแหน่ง (Warehouse & Bin)` (**D14**). This is a re-gate: verify the new tree UI's own quality + the two realign/rename changes introduced no regression + the two known latent bugs stay clean.
> Method: Sync-Read authoritative rules from **html-generator-v7** (iron-rules #1-94, ci-tokens CUBE Warm Light v2.0, layout-integrity #50-#80, component-contracts, page-anatomy) → `self_audit.py` + `static_scan.py` (mechanical) → heuristic code read of tree/summary/switcher → **Render Gate: Playwright E2E, 54/54 assertions × viewports 1280 & 1440, 0 console / 0 page errors** + visual review of fresh `regate3_*` screenshots.
> File now 3,323 lines / 188 KB (was 3,105 / 166 KB — +217 lines = tree view + summary panel). PREFLIGHT stamp = `v7 · fix-pass 3` with **real** self_audit numbers.

### Verdict: 🟢 PASS  (no regression)

| BLOCK | WARN | INFO | NOT-CHECKED |
|---|---|---|---|
| 0 | 0 | 3 | 0 |

`self_audit.py` core counters all **0** (`spacing_off · font_off · flex_noalign · grid_nogap · inline_layout · z_adhoc · hex_off · preflight · jargon_leak · undefined_handlers · long_banners`); `font_count=8` (limit). The 3 remaining script hits (`missing_ids=8`, `fullwidth_select=3`, `custom_tabs=1`) are the **same documented static-scan false-positives** carried unchanged from the passing iter-2 (runtime-built combobox ids · widths moved to CSS class · `.drawer-tab` kit class inside a template string). `static_scan.py`: all **22 distinct hex are inside the CUBE Warm Light whitelist** — off-palette hex introduced by the tree view = **0**. Fonts in-stack. z-scale registry intact.

### Status of the four items this re-gate must clear

| Item | Status | Evidence |
|---|---|---|
| **Tree-view UX quality** | ✅ **GOOD** | See sub-checklist below — states/scroll/highlight/consistency all clean; no off-palette hex |
| **Role-switcher alignment (D13)** | ✅ **CLEAN** | `.role-switch`(36px)+`.role-select`(36px) inside `.ph-actions` (align-items:center) → E2E measured `dTop=0`, `selH=btnH=36` vs create btn, both viewports · label `มุมมองบทบาท` (no "QA") · shot `regate3_*_02_role_align_header.png` |
| **Rename correctness (D14)** | ✅ **CLEAN** | `คลังและตำแหน่ง (Warehouse & Bin)` in `<title>`(6), h1 (renderHeader/loading/error 2340/2346/2367), breadcrumb(1497), sidebar feature label(1457) · internal id/route `F-LOCATION-MASTER-001` / `location-master` unchanged (correct) |
| **Latent bug #1 — drawer re-render** | ✅ **CLEAN** | `render()` rebuilds `#drawer.innerHTML` with `preserveRenderState`/`restoreRenderState` (2171/1884/1902) · E2E: view-loc drawer + in-drawer tab switch → still open, innerText 344→397 (rebuilt, not lost), both viewports · shot `regate3_*_R8_LB1_drawer_rerender.png` |
| **Latent bug #2 — in-drawer modal z-index** | ✅ **CLEAN** | z registry `--z-drawer:55 · --z-modal:70` (1319) + `.modal-backdrop{z-index:var(--z-modal)}` (1322) · E2E from inside view-loc drawer: `modalBackdrop=70 > drawer=55 > drawerBackdrop=50`, `elementFromPoint(modal center)=modal`, both viewports · shot `regate3_*_R9_LB2_modal_over_drawer.png` |

### Tree-view UX quality — sub-checklist (the checker's mandate for the D12 deviation)

D12 = **approved** deviation → the tree pattern being absent from the A–O library is **NOT** a finding. Its own quality is what is checked:

| Aspect | Result | Detail |
|---|---|---|
| Empty state | ✅ | tree pane → `emptyStateHTML('ยังไม่มีคลัง' + CTA)` (2257) when no warehouses; summary root → prompt empty `เลือกโหนดจากผังด้านซ้าย` + desc (2283) |
| Not-found / error state | ✅ | summary handles missing selected node → `ไม่พบข้อมูลโหนดที่เลือก` (2290); list `renderErrorState()` unaffected |
| Loading state | ✅ | shared `renderLoading()` skeleton (unchanged) still gates before tree/list render |
| Deep-tree overflow / scroll | ✅ | `.tree-pane{ max-height:calc(100vh-220px); overflow:auto }` (1405) — pane scrolls independently (E2E: computed maxHeight=680px, overflow≠visible); children indent with `border-left` connector (1407) |
| Selected-node highlight | ✅ | `.tree-row.is-sel{ background:rgba(255,59,48,.08) }` + red code/icon (1410-1416); E2E confirmed `.tree-row.is-sel` present after select; visually distinct |
| Summary ↔ CUBE consistency | ✅ | summary reuses central `pillHtml` status pill, `.def-grid`, `.path-str`, `.child-stat` chips, `.btn btn-sm` secondary/danger — all standard components/tokens (verified in `regate3_*_05_tree_node_summary.png`) |
| Shared selection (tree ↔ list) | ✅ | single `state.sel` derived from `state.drill`; list drill → switch to tree preserves selection + `expandToSel()` opens ancestors; child chip → `chipToList` jumps to List with drill context (E2E both directions pass) |
| Segmented view switcher | ✅ | standard base-kit `.seg-control`/`.seg-item.is-active` (700-706); real `<button role="tab" aria-selected>` — keyboard-operable |
| Tree toggle | ✅ | real `<button class="tree-toggle">` with `event.stopPropagation()` so expand doesn't trigger row-select — keyboard-operable |
| Off-palette hex in tree/summary CSS | ✅ | tree/summary use only `var(--c-*)` + token-derived `rgba(255,59,48,…)` (D10-style sanctioned) — `hex_off=0` |

### ℹ️ INFO (non-blocking — no fix required to pass)

- **UX-08 · Tree row = `<div onclick>` (no `role="treeitem"` / `tabindex` / arrow-key nav).** The tree *toggle* and the *view-switcher* are real keyboard-operable buttons, but selecting a tree node is mouse-only — **consistent with the file's established Pattern-A list rows** (`<tr class="is-clickable" onclick>`), which passed the gate. Container has `role="tree"` but children omit `role="treeitem"`/`aria-expanded`/`aria-selected`. Not a regression; flag for dev handoff if full keyboard/AT support is required in production. (Location: `treeNode()` 2260-2278.)
- **UX-06 (carried) · SPA refresh does not restore drill/tree position** — `state.drill`/`state.sel` are in-memory; refresh returns to root list. Acceptable for a master drill-down; reflect into `location.hash` only if deep-link/back-button is wanted.
- **UX-07 (carried) · Role switcher is a prototype/demo affordance** in `.ph-actions` — correctly realigned per D13; dev must remove it in production (role comes from auth, per D13). Brand label reads **"Warm Light"** in sidebar/user-chip (iter-2 fix of the deprecated "CUBE NATIVE"); it is a theme name rather than a product name — cosmetic, out of scope of this change, left as-is since iter-2 gated it PASS.

### Render Gate — E2E summary (this iteration)

Script: `02_QC/regate_e2e.py` · JSON: `02_QC/regate_result.json` · Shots: `02_QC/ux-shots/regate3_{1280,1440}_*.png` (existing shots preserved).
**54/54 assertions pass · 0 console errors · 0 page errors** across viewports 1280 & 1440. Covered: D14 rename (title/h1/breadcrumb) · D13 alignment measurement · tree switch/expand/select→summary/chip→List · shared-selection both directions · deep-tree overflow · regression sweep (list root → drill 5 levels → create drawer → view drawer → archive modal → operator RBAC disabled) · Esc chain (modal→drawer) · LB#1 drawer re-render · LB#2 in-drawer modal z-index.

---

## ✅ FIX PASS — Iteration 2 (2026-08-06) · surgical fix, no regenerate

### Verdict: 🟢 PASS  (was 🔴 BLOCK)

| BLOCK | WARN | INFO | NOT-CHECKED |
|---|---|---|---|
| 0 | 0 | 2 | 0 |

ทั้ง 2 BLOCK + 3 WARN แก้ครบและ verify แล้ว. เหลือ INFO 2 ข้อ (UX-06 hash-drill · UX-07 role switcher = dev-handoff note) — ไม่บังคับ. โครง/flow/behavior ไม่แตะ — E2E เดินซ้ำ **38/38 pass · 0 console · 0 page error** ทั้ง viewport 1280 & 1440 (ไม่ regress). Latent bug #1/#2 ยัง CLEAN (z: modalBackdrop=70 > drawer=55, topmost=modal).

| # | เดิม | สถานะ | หลักฐาน / บรรทัด |
|---|---|---|---|
| **UX-01** | BLOCK · CI token drift (pills+types) | **FIXED ✓** | ตัด `TYPE_COLOR` map ทิ้ง → type = **pill กลาง neutral เดียว** (var tokens) + `TYPE_ICON` (Lucide) แยกด้วย icon+label ตาม **D10** · สถานะ 7 ตัว recolor เป็น CUBE variant/token-derived tint (active=info · full=warning · maintenance=orange tint `rgba(255,154,31,.18)` · blocked=danger · frozen/inactive=grey · decommissioned=faded grey) · temp-badge→info-blue(#E6F0FF/#1A5FCC) · is-branch/tag/collision-box/inline-warn เปลี่ยน hex นอก palette เป็น whitelisted + rgba token tint. **off-palette hex = 0 ทั้งไฟล์** (22 distinct hex อยู่ใน whitelist ทั้งหมด). CSS ~1318-1396 + JS TYPE_ICON/typePillHtml |
| **UX-02** | BLOCK · empty pre-flight stamp | **FIXED ✓** | รัน `self_audit.py` จริง แล้วกรอกตัวเลขจริง — core counters = 0 ทุกตัว + documented false-positives + date. ไม่มี `_` เหลือ. (ท้ายไฟล์) |
| **UX-03** | WARN · "CUBE NATIVE" label | **FIXED ✓** | เปลี่ยน 4 จุด → **"Warm Light"**: title(6) · sidebar sb-name(1405) · user-chip uc-role(1464) · `syncRoleChip()` JS(2136). สีธีมไม่แตะ |
| **UX-04** | WARN · "บทบาท (QA)" jargon | **FIXED ✓** | relabel → **"มุมมองบทบาท"** (ตัด "QA") · คง switcher ไว้ (จำเป็นสำหรับ demo/RBAC preview) · แปลง inline style ของ label เป็น `.role-switch`/`.role-switch-label` (2194) |
| **UX-05** | WARN · 22 inline layout styles | **FIXED ✓** | ย้าย inline layout ทั้ง **22 จุด** เข้า class ใน `<style id="page-late">` (Rule #69) → `inline_layout=0`. เพิ่ม `.shell-right .ml-auto .sk-line .sk-a..d .sk-search .branch-filter-wrap .filter-select-type/-status .pagesize-select .postcode-input .tempfields-row .parent-picker-wrap .drill-child-btn .dw-head-flush .empty-compact .bulk-sample .collision-mt .decomm-note` |

**self_audit.py (round 1) — ตัวเลขจริงหลังแก้:** `spacing-off=0 · font-off=0 · font-count=8(limit8) · flex-noalign=0 · grid-nogap=0 · inline-layout=0 · z-adhoc=0 · hex-off=0`
เหลือ 3 ตัวที่ script รายงานแต่เป็น **static-scan false-positive** (แบบเดียวกับ Bank Master ที่ผ่าน gate): `missing_ids=8` (id combobox `f-*/ss-*` สร้าง runtime) · `fullwidth_select=3` (width ย้ายไป CSS class แล้ว static เห็นแค่ tag) · `custom_tabs=1` (`.drawer-tab` kit-class ใน template-string). ไม่ใช่ violation จริง.

**Extra fixes (เพื่อให้ pre-flight เป็นศูนย์จริงตามมาตรฐาน sibling Bank/Tax):** normalize spacing/font นอก scale ใน page-CSS (13→12, 9→8, 7→8, 11→12, 14→16 · font 10→11, 11.5→12, 13.5→14, 22→20, 30→26) + `.status-actions` เพิ่ม `align-items` + z-index registry เพิ่ม `--z-modal:70` แทนเลขลอย. เป็น mechanical token-normalization ไม่กระทบ layout/flow.

**Fresh screenshots (ใหม่ — เก็บของเดิมไว้ที่ `ux-shots/_iter1_bak/`):**
`ux-shots/{1280,1440}_PILLS_gallery.png` (7 status + 10 type pills), `_PILLS_location_list.png` (live table), `_PILLS_view_loc_drawer.png` (blocked loc: red status pill + neutral type + flags).

---

## (ด้านล่าง = รายงาน Iteration 1 เดิม — เก็บไว้เพื่อ trace)


- วันที่: 2026-08-06 · Iteration: 1 (first UX gate)
- Generator spec (Sync-Read authoritative): **html-generator-v7** — iron-rules `#1-94`, ci-tokens CUBE Warm Light v2.0, layout-integrity #50-#80, component-contracts, page-anatomy #70-#77. File carries a `PREFLIGHT v6.4` kit stamp.
- ไฟล์ที่ตรวจ: `01_HTML/WarehouseBin.html` (3,105 บรรทัด · 166 KB · single-file SPA vanilla JS)
- Method: Sync-Read rules → static_scan.py (mechanical facts) → heuristic code read → **browser E2E (Playwright, 38 assertions × viewports 1280 & 1440, 0 console/page errors)** → visual render-gate review of 22 screenshots.

---

## Verdict: 🔴 BLOCK

| BLOCK | WARN | INFO | NOT-CHECKED |
|---|---|---|---|
| 2 | 3 | 2 | 0 |

ประเมินเวลาแก้: **~25–40 นาที** (ทั้งสอง BLOCK เป็นงาน mechanical, ไม่ต้องรื้อ flow)

> BLOCK ทั้งสองเป็นเรื่อง "form compliance" ล้วน — โครง UX/flow/behavior **ผ่านหมด** (ดู E2E section). ระบบทำงานถูกต้อง 100% รวมถึง **ทั้งสอง latent bug จาก feature ก่อนหน้า = CLEAN** (พิสูจน์ด้วยภาพ). สิ่งที่ block คือ CI-token drift + pre-flight stamp เปล่า ตามกฎ #1 / #60 ซึ่งเป็น hard rule ของ v7.

---

## 🔴 BLOCK — ต้องแก้ก่อนผ่าน gate

### UX-01 · Rule #1 CI Tokens (hex นอก whitelist) · lines 1324–1394 (CSS) + 1973–1977 (JS `TYPE_COLOR`)
- **พบ:** สีทั้งสองก้อนอยู่นอก CUBE Warm Light whitelist (ci-tokens อนุมัติ pill variants แค่ 5 ชุด). มีสี **ฟ้า/น้ำเงิน/ม่วง/teal ของ Tailwind** ที่ไม่มีในพาเลต CUBE เลย:
  - CSS extra pills / badges: `#FDECC8` `#92400E` (`.pill-full`), `#E0F2FE` `#0369A1` (`.pill-frozen`, `.temp-badge`), `#8a5a12` (`.drill-chip.is-branch`, `.tag.is-on`, `.inline-warn`), `#f3b6b1` `#991B1B` (`.collision-box`), `#f0d7a8` (`.inline-warn`).
  - JS `TYPE_COLOR` map (10 location types, inline-styled onto `.type-pill`): `#DBEAFE/#1E40AF`, `#E0E7FF/#3730A3`, `#FEF3C7`, `#FEE2E2/#DC2626`, `#F1F5F9/#475569`, `#CCFBF1/#0F766E`, `#EDE9FE/#6D28D9`, `#64748B`.
- **ราก:** feature มี 10 location types + 7 lifecycle states จริง ซึ่งเกิน pill vocabulary 5 ชุดของ CUBE → generator ประดิษฐ์ tint เอง (หยิบพาเลต Tailwind มาตรง ๆ) แทนที่จะ map เข้า CUBE-derived tints.
- **แก้ (concrete):** นิยามชุดสีเป็น CSS custom properties ที่ derive จากพาเลต CUBE (ivory/charcoal/red/orange + semantic success/warning/danger) แล้วอ้างผ่าน `var(--...)`; ตัดโทนฟ้า/น้ำเงิน/ม่วง (`#1E40AF #3730A3 #6D28D9 #0F766E #0369A1`) ที่ไม่เข้าธีมออก — หรือถ้าจำเป็นต้องใช้ palette 10-type จริง ให้ผู้ถือ gate อนุมัติเป็น **ส่วนขยาย ci-tokens อย่างเป็นทางการ** แล้วบันทึกใน DECISION_LOG (ตอนนี้ยังไม่มีมติรองรับ → ถือเป็น drift). สถานะ status ที่ map เข้า 5 pill เดิมได้ (`pill-info/success/warning/danger/muted`) ให้ใช้ของเดิม.

### UX-02 · Rule #60 Pre-flight Stamp · lines 3098–3102
- **พบ:** stamp `<!-- PREFLIGHT v6.4 -->` มีอยู่ แต่ **ตัวเลขเป็น placeholder ทั้งหมด** — `round1: spacing-off=_ font-sizes=_ flex-noalign=_ inline-layout=_ z-adhoc=_ hex-off=_`, `round2: _/7 checked`, `date: _`.
- **ตัดสิน:** ตาม Rule #60 + Pass G ของ checker — "stamp ไม่มีตัวเลข = NOT-CHECKED = BLOCK". generator ยังไม่ได้รัน self-audit/self-review รอบสุดท้ายจริง (โดยเฉพาะ `hex-off=_` ซึ่งจริง ๆ ควรจับ UX-01 ได้).
- **แก้ (concrete):** รัน `html-generator-v7/scripts/self_audit.py` (หรือไล่นับมือ) แล้วกรอกตัวเลขจริงทั้ง 6 ช่อง round1 + `round2: N/7` + วันที่. คาดว่า `hex-off` จะ > 0 (จาก UX-01) → ต้องแก้ UX-01 ให้จบก่อน stamp ถึงจะเป็น 0 ได้.

---

## 🟡 WARN

### UX-03 · Brand label ผิดธีม · lines 6, 1405, 1464, 2136
- **พบ:** ข้อความแบรนด์เขียน **"CUBE NATIVE"** 4 จุด — `<title>` (6), sidebar `.sb-name` (1405), user chip `.user-role` (1464), และ `syncRoleChip()` (2136 `r.en+' · CUBE NATIVE'`). "CUBE NATIVE" = ชื่อธีมเก่า (Navy/Blue/Teal) ที่ ci-tokens v2.0 ระบุว่า **ถูกแทนด้วย Warm Light แล้ว**. ธีมที่ render จริง = Warm Light ถูกต้อง แต่ป้ายชื่อยังเป็นของเก่า → ขัดแย้งในตัว.
- **แก้:** เปลี่ยนเป็น `CUBE` / `CUBE Design System` (หรือชื่อผลิตภัณฑ์จริง) ทั้ง 4 จุด — เอา "NATIVE" ออก.

### UX-04 · Rule #81 (ศัพท์ทดสอบรั่วขึ้นจอ) · line 2194
- **พบ:** role switcher มี label **"บทบาท (QA)"** โผล่บน `.ph-actions` — "(QA)" เป็นคำ testing/affordance ภายใน ไม่ใช่ภาษาผู้ใช้.
- **แก้:** เปลี่ยน label เป็น `มุมมองบทบาท (พรีวิว)` หรือ `จำลองบทบาท` แล้วตัด "(QA)" ออก.

### UX-05 · Rule #69 Inline layout styles · 22 จุด (เช่น lines 2260 `min-width:220px`, 2261/2263 `max-width`, 2268 `margin-left:auto`, 2403 `height:30px`, 2542 `max-width:160px`, 2693 `width:100%;margin-top`, 2718 `padding-bottom`)
- **พบ:** feature JS ฝัง inline layout style (min/max-width, height, width, margin, padding) 22 จุด ทั้งที่ไฟล์มี `<style id="page-late">` (line 3097) ว่างอยู่ให้ใช้.
- **หมายเหตุความรุนแรง:** ส่วนใหญ่เป็น pragmatic เล็ก ๆ (skeleton `width:%`, filter-select max-width, ปุ่ม `margin-left:auto`) ความเสี่ยง re-theme ต่ำ — จึงจัดเป็น **WARN**. แต่ **ตามตัวอักษรของ Rule #69 (มี page-late = ปิดข้ออ้าง "จำเป็น") ก้อนนี้นับเป็น BLOCK** — ฝากผู้ถือ gate ตัดสินว่าจะบังคับหรือรับได้.
- **แก้:** ย้ายเป็น utility class หรือ selector ใน `#page-late` (เช่น `.filter-select-sm{max-width:170px}`, `.w-full{width:100%}`, `.ml-auto{margin-left:auto}`).

---

## ℹ️ INFO (ไม่บังคับ)

### UX-06 · SPA refresh ไม่คง drill position
- `getRoute()/navigate()` มีใน skeleton แต่ feature ใช้ `state.drill` (in-memory) + `render()` ในการเจาะระดับ ไม่ผูกกับ `location.hash` → refresh กลับไปหน้า root list เสมอ. รับได้สำหรับ master drill-down (ไม่ใช่ deep-link เอกสาร) แต่ถ้าต้องการ deep-link/back-button ในอนาคต ให้ reflect `state.drill` ลง hash.

### UX-07 · Role switcher = prototype affordance ใน `.ph-actions`
- dropdown สลับบทบาท (5 roles) วางร่วมกับปุ่มสร้างใน `.ph-actions` — เป็น control สำหรับ demo/QA เท่านั้น (production ไม่มี). ถูกต้องในฐานะ prototype แต่พึงรู้ว่าเป็น affordance ที่ dev ต้องถอดออกตอน implement. (เกี่ยวเนื่องกับ UX-04.)

---

## ⬜ NOT-CHECKED
- ไม่มี. Render Gate ครบ — E2E เดิน 6 หน้าจอจริง × 2 viewport + screenshot ทุก state (ดูโฟลเดอร์ `ux-shots/`).
- Emoji ที่ static scan จับ (⚠️/✅ 4 ครั้ง, lines 387/392/600/1638) = อยู่ใน **CSS/JS comment เท่านั้น ไม่ขึ้นจอ** → clean (Rule #5).

---

## 🐞 Latent-Bug Verification (บังคับ — จาก feature ก่อนหน้า) — ทั้งคู่ CLEAN ✅

### LB#1 — Drawer content re-render หลัง in-drawer action → **CLEAN**
- `render()` (line 2123) rebuild `#drawer.innerHTML = state.drawer.open ? renderDrawer() : ''` ทุกครั้ง พร้อม `preserveRenderState()/restoreRenderState()` (Rule #29).
- E2E: เปิด view-loc drawer → สลับ tab (in-drawer action) → drawer **ยังเปิด + เนื้อหาไม่หาย/ไม่ยุบ** (innerText len 320→340, open=true) ทั้ง 1280 & 1440.
- หลักฐาน: `ux-shots/1280_14_drawer_reRENDER_after_inaction.png`, `1440_14_...`

### LB#2 — In-drawer modal z-index → **CLEAN**
- generator แก้ latent bug นี้เชิงรุกแล้ว: base-kit อ้าง `var(--z-*)` แต่ไม่ define → เพิ่ม scale ที่ line 1318 (`--z-drawer:55`) + override `.modal-backdrop{ z-index:70 }` (line 1322, "modal must sit above an open drawer").
- E2E วัด computed z-index ตอนเปิด modal **จากใน view-loc drawer**: `modalBackdrop=70 > drawer=55 > drawerBackdrop=50`, และ `document.elementFromPoint(center of modal)` = **modal** (ไม่ใช่ drawer). ทั้ง 1280 & 1440.
- หลักฐานภาพ: `ux-shots/1440_15_MODAL_over_drawer_zindex.png` — modal "ปลดระวางไม่ได้ (BR-010)" ลอยกลางจอเหนือ drawer + backdrop คลุมถูกต้อง.

---

## ✅ Browser E2E — สรุปผล (38/38 pass · 0 console error · 0 page error)

Script: `02_QC/e2e_warehouse_bin.py` · JSON: `02_QC/e2e_result.json` · Shots: `02_QC/ux-shots/` (viewports 1280 & 1440)

| หมวด | ผล | หลักฐาน |
|---|---|---|
| List drill-down 5 ระดับ (WH→Zone→Area→Rack→Location) | ✅ เจาะได้จริงผ่าน row click + breadcrumb chip | shots 01,03–06 |
| Branch filter (combobox) + KPI 5 ระดับ + branch chip ใน breadcrumb | ✅ | shot 01,02 |
| Role switcher — **Operator = view-only** (create/del/status = false) | ✅ | shot 07 |
| Role switcher — **Supervisor = create ได้ แต่ลบไม่ได้** (del=false) | ✅ | shot 08 |
| Drawer: node create (WH) + branch + geo cascade | ✅ form sections + comboboxes (#94) | shot 09 |
| **Geo cascade: เลือกตำบล → postcode auto-fill** (บางพลีใหญ่ → 10540, input readonly) | ✅ ตรวจ targeted | shot 22 |
| Drawer: location 2-step wizard (ต้นทาง&ระบุ → ความจุ&พฤติกรรม) + stepper | ✅ | shots 10,11 |
| Drawer: view node / view location (3 tabs: ภาพรวม/ความจุ&flags/ประวัติ) | ✅ | shots 12,13 |
| Drawer: bulk generate + **live preview count** ("สร้าง 960 ตำแหน่ง") | ✅ | shot 17 |
| Modal: delete node / decommission (referential-safe / empty-before) | ✅ | shots 15,18 |
| **Esc chain**: combobox list ปิดก่อน → (Esc) modal ปิด (drawer อยู่) → (Esc) drawer ปิด | ✅ ครบ 3 ชั้น | shots 02,16 |
| Backdrop + X ปิด drawer/modal | ✅ (closeDrawer/closeModal wired ทั้ง backdrop click + X) | — |
| States: empty / loading / error | ✅ ครบ (empty มี icon+CTA, loading skeleton, error invalid-drill) | shots 06,19,20,21 |

---

## Mechanical facts (static_scan.py) — ที่ผ่าน (เพื่อความครบถ้วน)
- Fonts: `'Satoshi','Noto Sans Thai',system-ui` + `Noto Sans Thai` — ✅ ใน stack (Satoshi โหลดจาก Fontshare ตามสเปค; scan เห็นเฉพาะ googleapis link ของ Noto).
- Drawer/modal widths: 920 / 680 / 440 พบครบ · **540px legacy = 0** ✅ (Rule #11)
- Sidebar 232px ✅ · shell 52px ✅ · minimal scrollbar width 5px ✅ (Rule #49)
- hashchange listener ✅ · Esc handler ✅ · drawer translate ✅ · backdrop ✅
- localStorage/sessionStorage = **ไม่ใช้** ✅ · Lucide icons 90 (fontawesome=false) ✅
- markers: empty_state 9 · loading 20 · disabled 27 · confirm_modal 9 — ครบชุด states.
