# UX Check Report — Sales Territory

- วันที่: 2026-08-13 · Iteration: 1 (fix mode)
- Generator spec: `html-generator-v8` · authoritative Iron Rules #1–97 (รวม #94–97)
- ไฟล์ที่ตรวจ: `../01_HTML/sales-territory.html` (1,078 บรรทัด · 150,243 bytes)
- Route: `#/sales-territory`
- Scope lock: ตรวจและแก้เฉพาะ UI/UX; ไม่เพิ่ม business scope และ future modules ยังคงเป็น mock/future hooks

## Verdict: 🟢 PASS (with 2 warnings)

| BLOCK | WARN | INFO | NOT-CHECKED |
|---:|---:|---:|---:|
| 0 | 2 | 3 | 1 |

## 🔴 BLOCK

ไม่พบ BLOCK ค้างหลัง fix และ rerun checks

## 🟡 WARN

### UX-01 · Token audit · ทั้งไฟล์

- **พบ:** `audit.sh` รายงาน `WARN=1` จาก `font-size` แบบ hardcoded บางส่วน เช่น input/sidebar (หลักฐานเริ่มที่บรรทัด 33, 52–58)
- **ผลกระทบ:** ไม่ทำให้ layout/interaction เสีย และ `self_audit.py` ยืนยัน `font_off=0`, `font_count=8` ตามเพดาน
- **ข้อเสนอ:** รอบปรับ design-token ถัดไปค่อยย้ายค่าที่ audit ระบุไปใช้ `--fs-*`; ไม่แก้ใน fix mode นี้เพื่อลด drift จาก source UI

### UX-02 · Drawer shell compatibility · create/view/edit drawer

- **พบ:** prototype เดิมใช้ backdrop และ drawer เป็น sibling (`#drawerBackdrop`, `#drawerEl`) แทนชื่อโครง `overlay-wrap/drawer-panel` ใน locked anatomy
- **หลักฐานพฤติกรรม:** static scan พบ backdrop + `translateX`; ภาพ `../../test-artifacts/05_Sales_Territory/_shots/route_sales-territory__overlay_btn-primary.png` แสดง drawer 680px, dim backdrop, header/body/footer และปุ่มปิดครบ โดย footer อยู่ขอบล่าง
- **ผลกระทบ:** พฤติกรรมใช้งานผ่าน แต่ dev ควรยึด behavior contract และ z-index map ไม่ยึดชื่อ class legacy เป็น API

## ℹ️ INFO — สิ่งที่แก้ใน fix mode

### UX-F01 · Rule #1 / CI colors

- เปลี่ยน non-whitelist hex ของแผนที่/coverage/semantic state ไปเป็น CUBE v8 whitelist
- เปลี่ยนสถานะ “ใช้งาน” เป็น semantic blue และคง red/orange สำหรับ action/warning
- **ผลตรวจหลังแก้:** `self_audit.py` → `hex_off=0`, `RESULT: PASS`

### UX-F02 · Empty state / dismiss contract

- เพิ่ม action “ล้างตัวกรอง” ใน empty state พร้อม handler `resetRouteFilters()`
- เพิ่มปุ่ม X ใน archive confirmation modal; modal ยังปิดได้ด้วย Cancel, backdrop และ Esc

### UX-F03 · Keyboard focus

- เพิ่ม `focusDrawerFirst()` ให้ create/edit drawer ส่ง focus ไป control แรกหลังเปิด
- static scan ยืนยันมี Escape handler, aria attributes และ disabled/loading guards

## Visual / Runtime Evidence

- `render_shots.py`: สร้างภาพ 4 ไฟล์ใน `../../test-artifacts/05_Sales_Territory/_shots/`
  - `route_sales-territory.png`
  - `route_sales-territory__overlay_btn-primary.png`
  - `route_sales-territory__tab0.png`
  - `route_sales-territory__tab1.png`
- ภาพตรวจด้วยตาที่ 1440×900: sidebar/topbar/main tabs/table aligned, Thai text ไม่ชน, drawer ไม่ล้นจอ, footer action อยู่ขอบล่าง
- `render-check.py`: สร้าง `../../test-artifacts/05_Sales_Territory/render-1440-qc.png` และ `../../test-artifacts/05_Sales_Territory/render-1024-qc.png` สำเร็จ
- Responsive 1024×768: desktop-base ยังใช้งานได้; ตารางคงอยู่ใน content surface และไม่พบ overlay จม

## Automated Check Evidence

| Check | Result |
|---|---|
| `static_scan.py` | PASS; Lucide 43, emoji 0, external scripts 0, storage 0, route/hash/Esc/backdrop/scrollbar hooks present |
| `self_audit.py` | PASS; ทุก violation counter = 0 |
| `audit.sh` | FAIL=0 · WARN=1 (font-size token ตาม UX-01) |
| `render_shots.py` | 4 screenshots; helper แจ้ง stale-element interaction skip หลัง DOM rerender แต่ไฟล์หลัก/overlay/tab ถูกสร้างครบ |
| `render-check.py` 1440/1024 | screenshots created successfully |

## ⬜ NOT-CHECKED

- ไม่ได้ทดสอบ end-to-end กับ backend/feature ปลายทาง เพราะ Sales Team/Salesperson, Customer Master, Sales Order, Sales Target และ Visit Operation ยังไม่มีตามคำยืนยัน PM/BA; จุดเชื่อมต่อจึงเป็น mock/future hook เท่านั้น

## Gate Note

ผ่าน UX gate สำหรับส่งต่อไป coverage check ได้ โดย WARN ทั้งสองข้อไม่เปลี่ยน business scope และไม่บล็อก prototype review

## Iteration 2 — Manual-test follow-up (2026-08-13)

### Verdict: PASS

- แก้ 5 ประเด็นจาก manual test แบบ surgical โดยไม่เพิ่ม scope
- `static_scan.py`: PASS; ไม่มี external font/script, route/Esc/backdrop/scrollbar hooks ยังครบ
- `self_audit.py`: PASS; violation counters ทุกหมวด = 0
- `audit.sh`: FAIL=0, WARN=1 เฉพาะ hardcoded font-size เดิมจาก legacy source
- Playwright final confirmation: 62/62 — 31/31 ที่ 1440×900 และ 31/31 ที่ 1024×768; console errors 0, page errors 0

| Issue | Resolution / evidence |
|---|---|
| ฟอนต์หลังถอด external font | offline-first `Leelawadee UI`, `Tahoma`, `Noto Sans Thai`, `Segoe UI`; TC-27 ยืนยันไม่มี remote resource |
| จังหวัดเพิ่มเมื่อไม่ระบุจังหวัด | นับเฉพาะค่าที่อยู่ใน `PROVINCES`; TC-28 ผ่านทั้ง 2 viewport |
| map hover ค้างหลัง pointer ออก | clear timer/state/tooltip ทันที; TC-29 ผ่านทั้ง 2 viewport; click-selected state ยังคงตาม S-21 |
| searchable dropdown เลื่อนไม่ได้ | ไม่ rerender จาก menu scroll, preserve scrollTop, keyboard highlight scrollIntoView; TC-30 ทดสอบทั้ง province และ salesperson |
| universe พิมพ์ไม่ได้ | PREBRIEF §3.1 ระบุว่า editable integer ≥0/เว้นว่างได้; เพิ่ม input affordance และ TC-19/20/31 ยืนยัน create/edit typing |

หลักฐาน runner, raw JSON และ screenshots อยู่ที่ `../../test-artifacts/05_Sales_Territory/` เท่านั้น; ไม่มี test harness/raw/screenshots ใน output folder.

Residual `[AI-DEFAULT]`: ไม่มี bundled Satoshi/Noto font asset ใน workspace จึงใช้ font stack ที่มีบน Windows แบบ offline-first; หาก production ต้อง pixel-match CI ต้องให้ทีม UI ส่ง licensed/bundled webfont asset. Future 5 modules ยังคง mock/future hooks ตาม PM/BA และไม่เป็น hard dependency.

## Iteration 3 — Source-font parity + strict map boundary (2026-08-13)

### Verdict: PASS with external-font availability warning

- Iteration 2 font substitution is superseded: output now matches `Pack Brief Feature/5. Sales Territory/f-territory.html` exactly for font imports and font-family order.
- Restored Google Fonts `Noto Sans Thai` and Fontshare `Satoshi` links, body `Noto Sans Thai → Satoshi → system-ui → sans-serif`, plus the source Satoshi/Noto title, KPI, logo, and version stacks.
- Honest offline result: workspace has no bundled font assets and the restricted runner records two `ERR_NETWORK_ACCESS_DENIED` font stylesheet errors per run. The browser therefore uses the source-declared system fallback; no substitute font was chosen by QC.
- Root cause of outside-map activity: `.mp-heat-row` in the right-hand panel still called `mapHover()` although it is outside `.map-canvas`; SVG handlers also trusted caller name without validating event coordinates/hit target.
- Fix: removed side-panel hover listeners; added `validMapPointer()` coordinate + `[data-prov]/[data-pin]` validation; guarded `mapMove`; retained immediate clear/cancel on frame leave.
- Focused evidence at 1440×900 and 1024×768: positive inside pin hover passes; after first exit-clear, left/right/top/bottom + four corners + side panel produce zero additional `mapHover`/`updateTip`/`mapSelect` calls and zero state/tooltip changes.
- Final clean confirmations: 62/62 passed (31/31 each viewport), application console errors 0, page errors 0; external font resource errors 2 per run are separately recorded, not concealed.

Evidence: `../../test-artifacts/05_Sales_Territory/focused_font_map.py`, `_e2e_results.json`, `_E2E_TEST_REPORT.md`, and `_e2e_evidence/`. Output folder remains deliverables only.

## Iteration 4 — PM/BA Central Route + structure document scroll (2026-08-13)

### Verdict: PASS with `[AI-DEFAULT]` mock confirmation pending

- Targeted source search found no existing Area Route labeled `ภาคกลาง`; existing `R-NP-03`/`R-SP-02` remain west and Bangkok KAM rows remain `ส่วนกลาง / ออนไลน์`.
- Added minimal `[AI-DEFAULT]` `R-BK-01 — กรุงเทพฯ ชั้นใน สาย 1`, Area Route, `ภาคกลาง`, `กรุงเทพมหานคร`, `เอก ทวีสุข`, universe 30. Province/person are exact source examples; route identity and read-only stats require PM/BA confirmation as logged in `HTML_GENERATION_LOG.md`.
- Structure list now grows with content and uses the outer document/browser vertical scrollbar. Body/document scroll height exceeds viewport, nested `.content`/`.card`/`.table-wrap` vertical overflow is not auto/scroll, and the last row is reachable by browser scroll.
- Responsive 1024 layout hides three secondary numeric summary columns rather than creating a horizontal or nested table scrollbar; full details remain in the drawer.
- Final clean confirmation: 66/66 — 33/33 at 1440×900 and 33/33 at 1024×768; application console errors 0, page errors 0. Source-declared external font resource errors remain separately recorded (2/run).

Evidence is under `../../test-artifacts/05_Sales_Territory/`; output contains deliverables only.
