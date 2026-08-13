# E2E Test Report — Sales Territory HTML

- วันที่: 2026-08-13
- Target: `sales-territory.html` · `#/sales-territory`
- Runner: Playwright 1.61.0 / Chromium ผ่าน workspace-local `.tools/playwright.cmd` + `.tools/python.cmd`
- Test harness: `e2e_sales_territory.py`
- Raw result: `_e2e_results.json`
- Mode: 2 independent clean runs — fresh browser + fresh context + in-memory state ใหม่ทุกครั้ง

## Verdict: PASS — 66/66 checks

| Run | Viewport | Passed | Failed | App console errors | Font resource errors* | Page errors |
|---|---:|---:|---:|---:|---:|---:|
| Confirmation 1 | 1440×900 | 33 | 0 | 0 | 2 | 0 |
| Confirmation 2 | 1024×768 | 33 | 0 | 0 | 2 | 0 |
| **รวม** | — | **66** | **0** | **0** | **4** | **0** |

\* Source HTML declares external Google Fonts and Fontshare stylesheets. The restricted/offline test environment reports `ERR_NETWORK_ACCESS_DENIED`; this is recorded separately and not hidden as an application error.

Discovery/pre-fix runs ไม่ถูกนับในผลยืนยันข้างต้นตามกติกา clean confirmation runs

## Per-case Results

ทุก case ด้านล่างผ่านทั้ง Run 1 และ Run 2

| TC | Flow / assertion | Run 1 | Run 2 | Evidence |
|---|---|---|---|---|
| TC-01 | initial load, title, canonical hash, 4 stats | PASS | PASS | `01-initial.png` |
| TC-02 | initial console/page errors = 0 | PASS | PASS | `_e2e_results.json` |
| TC-03 | workload tab renders capacity/workload content | PASS | PASS | `02-workload.png` |
| TC-04 | map tab renders offline map; region chip filter toggles and resets | PASS | PASS | `03-map.png` |
| TC-05 | return to structure tab | PASS | PASS | raw results |
| TC-06 | search by Route code | PASS | PASS | raw results |
| TC-07 | no-result empty state + recovery action | PASS | PASS | `04-empty-search.png` |
| TC-08 | reset search/status from empty state | PASS | PASS | raw results |
| TC-09 | archived status filter | PASS | PASS | raw results |
| TC-10 | all → active filter transition | PASS | PASS | raw results |
| TC-11 | row click opens view-first detail drawer | PASS | PASS | `05-view-drawer.png` |
| TC-12 | Customer future hook stays on page and says “ยังไม่พร้อม” | PASS | PASS | raw results |
| TC-13 | Visit future hook stays on page and says “ยังไม่พร้อม” | PASS | PASS | raw results |
| TC-14 | Esc closes view drawer | PASS | PASS | raw results |
| TC-15 | create drawer opens, first field focused, geometry in viewport | PASS | PASS | raw results |
| TC-16 | blank create flags code/name/salesperson + warning toast | PASS | PASS | `06-create-validation.png` |
| TC-17 | duplicate Route code blocked | PASS | PASS | raw results |
| TC-18 | master combobox empty copy + Esc closes combo before drawer | PASS | PASS | `07-combobox-empty.png` |
| TC-19 | valid create; button disabled/loading; row created | PASS | PASS | raw results |
| TC-20 | edit flow; code locked; name updated | PASS | PASS | raw results |
| TC-21 | drawer backdrop closes drawer | PASS | PASS | raw results |
| TC-22 | destructive modal opens; Esc closes modal before drawer | PASS | PASS | `08-after-modal-esc.png` |
| TC-23 | modal backdrop closes modal but keeps drawer | PASS | PASS | raw results |
| TC-24 | archive loading/disabled → archived filter → restore | PASS | PASS | `09-archive-modal.png`, `10-final.png` |
| TC-25 | responsive geometry/no page horizontal overflow/drawer footer visible | PASS | PASS | viewport-specific screenshots |
| TC-26 | final console/page errors = 0 after all mutations | PASS | PASS | `_e2e_results.json` |
| TC-27 | font imports and declarations exactly match source HTML | PASS | PASS | raw results |
| TC-28 | create Route with unspecified province does not increment province count | PASS | PASS | raw results |
| TC-29 | positive inside hover; first exit clears; eight outside coordinates and side panel cause zero calls/state changes | PASS | PASS | `03-map.png`, raw results |
| TC-30 | province and salesperson searchable dropdowns scroll by wheel and keyboard | PASS | PASS | raw results |
| TC-31 | universe is editable in edit drawer and optional affordance is explicit | PASS | PASS | raw results |
| TC-32 | Central Area Route mock appears under visible `ภาคกลาง` group | PASS | PASS | raw results |
| TC-33 | document is taller than viewport; no nested structure scroller; browser reaches final row | PASS | PASS | `10-final.png`, raw results |

## Screenshot Evidence

แต่ละ run มี 10 ภาพใน:

- `_e2e_evidence/run-1/` — 1440×900
- `_e2e_evidence/run-2/` — 1024×768

ภาพที่ตรวจด้วยตาตัวแทน: map layout, create validation, combobox state และ archive modal ไม่พบ component overlap, clipped drawer footer หรือ sticky element ทะลุ overlay หลังแก้

## Bugs Found and Surgical HTML Changes

### FIX-01 · Offline console errors

- พบ external Google Fonts/Fontshare requests ล้มด้วย `ERR_NETWORK_ACCESS_DENIED`
- แก้โดยถอด external font links; CSS fallback stack ยังคง Satoshi/Noto Sans Thai/system ตามเครื่องที่มี

### FIX-02 · Master combobox portal อยู่ใต้ drawer

- พบเมนูแสดงแต่คลิก option ไม่ได้ เพราะ `--z-dropdown:30` ต่ำกว่า drawer `51`
- เพิ่ม `--z-dropdown-portal:52` และใช้กับ `.cb-menu-fixed`; option click ผ่านทั้งสอง viewport

### FIX-03 · Create/edit focus ผิด control

- `focusDrawerFirst()` เดิมเลือก input และ button ใน selector เดียว ทำปุ่มปิดมาก่อน input ตาม DOM
- แก้ให้เลือก enabled input/select/textarea ก่อน แล้ว fallback ไป button

### FIX-04 · Tab/content flex overlap

- workload/map content สูงทำ page head/stats/tabs ถูก flex-shrink จน pointer target ซ้อน โดยเฉพาะ 1024px
- เพิ่ม content vertical scroll และ `flex-shrink:0` ให้ page head/stats/tab bar/map container

### FIX-05 · Toast ขวาง drawer action

- warning toast ที่มุมขวาล่างทับปุ่ม submit และรับ pointer events ระหว่าง flow ต่อเนื่อง
- เพิ่ม `pointer-events:none` ที่ `.toast-wrap`

### FIX-06 · Manual-test follow-up (5 issues)

- Font: ใช้ offline-first Thai stack `Leelawadee UI → Tahoma → Noto Sans Thai → Segoe UI`; ไม่มี external font request
- Province KPI: กรองเฉพาะชื่อที่อยู่ใน `PROVINCES` ก่อนสร้าง `Set`; ค่า `—`/ออนไลน์ไม่ถูกนับเป็นจังหวัด
- Map hover: ยกเลิก timer และล้าง `state.mapHover`/tooltip ทันทีเมื่อออกจากพื้นที่; selected province จากการคลิกยังคงอยู่ตาม contract
- Searchable dropdown: ไม่ rerender portal จาก scroll ภายในเมนู, รักษา `scrollTop`, และเลื่อน keyboard highlight ให้อยู่ใน viewport
- Universe: ยืนยันจาก PREBRIEF §3.1 ว่าเป็นจำนวนเต็ม ≥0 จาก survey และเว้นว่างได้ จึงคง editable พร้อม `step`, `inputmode` และ help copy ที่ชัดเจน

ไม่มีการเปลี่ยน business scope, mock data contract หรือ future integration behavior

### FIX-07 · Manual retest: source font parity and strict map boundary

- Restored the source `<link>` declarations for Google `Noto Sans Thai` and Fontshare `Satoshi` exactly, including source order and weights.
- Restored source font-family declarations: body uses `Noto Sans Thai → Satoshi → system-ui → sans-serif`; logo/version use Satoshi; page title/KPI use Satoshi then Noto Sans Thai.
- Offline behavior is explicit: no local font assets exist, so blocked network requests fall through to the source-declared system fallback. The four font resource errors across two clean runs are preserved in raw evidence.
- Removed hover listeners from `.mp-heat-row` outside the visible map frame.
- Added `validMapPointer(event,name)` to require coordinates within `.map-canvas`, a valid `[data-prov]`/`[data-pin]` hit target, and matching province name before hover state/timer can change.
- Added a guarded `mapMove` and retained immediate timer/state/tooltip cancellation on frame leave.
- Focused runner instruments `mapHover`, `updateTip`, and `mapSelect`: after the first exit-clear, moving across left/right/top/bottom, four corners, and the side panel produces no additional calls or state changes at either viewport.

### FIX-08 · PM/BA feedback: Central Area Route + document scroll

- No Area Route labeled `ภาคกลาง` exists in PREBRIEF, checklist, source HTML, or Central Plan. Existing west Routes and Bangkok KAM/Online rows were preserved.
- Added `[AI-DEFAULT]` `R-BK-01` using source anchors: `กรุงเทพมหานคร` and salesperson `เอก ทวีสุข` from `ทีมขาย GT ภาคกลาง-ตะวันตก`. Mock values and confirmation-needed items are recorded in `outputs/05_Sales_Territory/HTML_GENERATION_LOG.md`.
- Structure tab now switches the document/body to vertical scrolling; `.content`, `.card`, and `.table-wrap` all expose `overflow-y: visible` rather than auto/scroll, and the browser reaches the final row.
- At ≤1180px, less critical numeric columns (universe, customer count, 90-day sales) are hidden in the structure summary to avoid horizontal overflow; details remain available in the row drawer. Route, province, salesperson, coverage, and actions remain visible.

## Coverage Limits / Residual Risk

- ทดสอบเฉพาะ behavior ที่ HTML standalone รองรับ; ไม่มี backend, persistence, authentication หรือ permission service
- Sales Team/Salesperson, Customer Master, Sales Order, Sales Target และ Visit Operation ยังเป็น future hooks ตามคำยืนยัน PM/BA; ตรวจว่าปุ่ม Customer/Visit ไม่ navigate และบอกผู้ใช้ว่า “ยังไม่พร้อม”
- แผนที่ตรวจ tab render, offline SVG, region filter และ hover-leave state/timer แบบ automated; ความแม่นยำเชิงภูมิศาสตร์ของ shape รายจังหวัดยังเป็น visual/manual scope ที่ GATE
- Loading ตรวจได้ใน create/edit/archive; network error state จำลองไม่ได้เพราะ prototype ไม่มี backend request
- Permission variants และ inactive salesperson ยังรอ OQ/contract จึงไม่ถูกนับว่าผ่าน
- External font availability depends on the same Google Fonts/Fontshare network access declared by the source; offline uses the browser/system fallback and cannot pixel-match the downloaded fonts.

## Gate Status

E2E confirmation รอบสุดท้ายผ่าน 66/66 และหยุดที่ GATE เพื่อ manual test/PM-BA review; ยังไม่เริ่ม skill 5+.
