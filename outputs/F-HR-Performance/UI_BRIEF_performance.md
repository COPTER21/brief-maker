# UI Brief — F-HR-Performance · ประเมินผลงาน (Performance)

> **EXTRACTION-BASED (Iron Rule R1)** — ทุกบรรทัดในบรีฟนี้ trace กลับหา selector / function / ข้อความจริงใน `performance.html` ได้
> อ้าง `Lxxxx` = เลขบรรทัดใน HTML · ข้อเสนอที่ไม่มีในจอ อยู่ท้ายไฟล์ §13 เท่านั้น
> คู่กับ: **HTML (source of truth)** + **FRD Pack** (ระบบ) + บรีฟนี้ (design intent)

---

## §0 · Document Control + Pairing

| | |
|---|---|
| Feature | F-HR-Performance / **F131** · ประเมินผลงาน (Performance) |
| HTML source | `outputs/F-HR-Performance/performance.html` · `<title>` = "ประเมินผลงาน (Performance) · CUBE NATIVE" (L6) · 2810 บรรทัด · BASE-KIT v6.4 |
| Archetype | **master + cycle** — จงใจ **NOT Pattern Q** (ไม่มีเลขรัน / PDF / เอกสารคนถือ · comment L2131–2132) |
| FRD Pack | `FRD_F-HR-Performance_Pack/` (00_OVERVIEW · 01_UI · 02_API · 03_LOGIC · 04_DB · 05_RULES · 06_TESTS · 07_LOCKED · INDEX) — **paired** |
| BRD | `BRD_performance.md` |
| HTML เก่า (diff) | — ไม่มี (บรีฟนี้เป็น full AS-BUILT รอบแรก · §12 = N/A) |
| Gate สถานะ | PREFLIGHT L2803–2808: `audit.sh FAIL=0` · round2 7/7 · residual = custom_tabs / JS-in-HTML false-positive (non-gate) · date 2026-09-09 |
| Drift | บันทึกใน §11 — ทั้งหมดเป็น HTML-only display-only surface หรือ FRD-only cross-module · ไม่มี business drift ที่ block |

**สถาปัตยกรรม:** Single-file vanilla-JS SPA · state-driven `render()` (L2790) — innerHTML rebuild ของ `#page-content` / `#drawer` / `#modalBackdrop .modal` + Render Preservation (`preserveRenderState`/`restoreRenderState`, Rule #29) · Lucide icon multi-CDN fallback pin `0.469.0` (L1604–1630, unpkg → jsdelivr → cdnjs) · ฟอนต์ Noto Sans Thai + Satoshi (L11–12).

**Roles / persona (demo · L2146–2150):** `hr` = สุนิสา คำแก้ว (HRBP · `manage:true` · `mask:false`) · `mgr` = ประสงค์ ชัยมงคล (หัวหน้าสายงาน · `dept:'ฝ่ายผลิต'`) · `staff` = สมชาย ใจดี (`mask:true`). สลับด้วย `.seg-control` ใน `.demo-strip` → `setRole()` (L2236).

---

## §1 · Design Tokens AS-BUILT (`:root` L24–67)

### Palette (CUBE Warm Light rebrand v2.0 · L25–41)
| token | ค่า | ใช้ |
|---|---|---|
| `--c-navy` / `--c-navy-2` | `#111111` | sidebar / heading |
| `--c-primary` / `--c-primary-hover` | `#FF3B30` / `#E62E24` | ปุ่มหลัก / active tab |
| `--c-teal` / `--c-teal-light` | `#FF9A1F` / `#FFB763` | accent |
| `--c-ink` | `#111111` | ตัวอักษรหลัก |
| `--c-mute` / `--c-mute-2` / `--c-mute-3` | `#54565C` / `#73757B` / `#9A9CA2` | ตัวอักษรรอง / masked |
| `--c-line` / `--c-line-2` / `--c-line-3` | `#DEDAD4` / `#E9E5E0` / `#F1EEEA` | เส้น |
| `--c-bg-off` | `#FAF8F5` | พื้นหลังหน้า |
| `--c-success` / `--c-warning` / `--c-danger` | `#1F9D55` / `#E8870F` / `#E62E24` | สถานะ (pill / banner) |

### Type scale (fixed · Iron Rule L54–62)
`--fs-h1:22px` · `--fs-h2:17px` · `--fs-h3:15px` · `--fs-body:14px` · `--fs-sub:13px` · `--fs-meta:12px` · `--fs-cap:11px` · `--fs-kpi:28px`
font stack (L91): `'Satoshi','Noto Sans Thai',system-ui,sans-serif` · body `14px` · line-height `1.5`

### Spacing / Radius (L64–66)
`--sp-xs:4px --sp-sm:8px --sp-md:12px --sp-lg:20px --sp-xl:28px` · `--r-xs:4px --r-sm:6px --r-md:8px --r-lg:12px --r-full:999px`

### Shell dims
`--sidebar-w:232px` (L42) · `--shell-h:52px` (L43) · body `min-width:768px` (L99) · `scrollbar-gutter:stable` (L74 · Rule #35 กัน jank) · scrollbar 5px (L81)

### ⭐ Z-INDEX MAP (สูง → ต่ำ · L47–53)
| token | ค่า | ใช้กับ |
|---|---:|---|
| `--z-toast` | **90** | `.toast` (สูงสุด — เห็นเหนือทุกอย่าง) |
| `--z-portal` | **60** | เมนู portal `#overlay-root` (Rule #95) · **`.modal-backdrop` override เป็นค่านี้** (DSP-01 fix L1112 — modal ต้องเหนือ drawer) |
| `--z-drawer` | **55** | ตัวลิ้นชัก `.drawer` (L892) |
| `--z-backdrop` | **50** | ฉากหลัง drawer/modal · `.ss-list` search list |
| `--z-dropdown` | **40** | `.user-menu` · tooltip · **`.notif-panel`** (L1486) · `.demo-strip` |
| `--z-sticky` | **30** | shell-bar · thead sticky |
| `--z-shell` | **20** | `.sidebar` (L117) |

> **หมายเหตุ latent:** `.modal-backdrop` ประกาศ `z-index:var(--z-portal)` (=60) ที่ L1112 ทับค่า BASE-KIT เดิม (`--z-backdrop` 50) — เป็น **สำเนา feature ของ DSP-01 fix** เพื่อให้ modal ที่ซ้อนบน drawer(55) ลอยเหนือ และ portal menu ใน modal ยังโผล่เหนือได้ตาม DOM order · latent BASE-KIT bug ยังไม่แก้ต้นทาง (mirror F-HR-WELFARE).

---

## §2 · Route Map

| | |
|---|---|
| Router | Hash-based · `getRoute()` L1663 · `navigate()` L1668 · default `'home'` (L1637/L1665) — refresh-safe |
| **การใช้จริง** | **feature นี้ไม่ผูก hash route** — "1 feature = 1 เมนู" (Rule 104). การสลับหน้าย่อยทำด้วย **in-page tab state** `state.tab` (L2134 default `'cycle'`) ผ่าน `onclick="state.tab='...';render()"` (L2266) ไม่แตะ `location.hash` |
| Tabs (4 · L2251–2256) | `cycle` รอบประเมิน · `appr` แบบประเมินรายคน · `review` สอบทาน + ผล & Gap · `report` รายงาน |
| Dispatcher | `viewHTML()` L2269 map `{cycle:cycleView, appr:apprView, review:reviewView, report:reportView}` |

> ⚠️ **Drift-note (ไม่ใช่ bug):** ตัว extractor นับ route = 0 เพราะจอไม่ประกอบ `#/route` — ถูกต้องตาม archetype. Dev สร้างระบบจริงใช้ tab-state เดียวได้ (หรือ map เป็น 4 sub-route ถ้าต้อง deep-link — ดู §13).

---

## §3 · Layout Shell

| region | selector | ขนาด/พฤติกรรม |
|---|---|---|
| Sidebar | `.sidebar#sidebar` (L1520) | fixed ซ้าย `--sidebar-w:232px` · z=`--z-shell` · มือถือ toggle `.open` ผ่าน `.nav-toggle` (L1547) |
| — module HR | `.sb-module[data-module="hr"]` (L1526) | collapse/expand ด้วย `toggleModule()` (L1653) · item active = `performance` (L1532) |
| — เมนูข้างเคียง | payroll · welfare · recruit · **performance (active)** · training · movement (L1529–1534) · โมดูล "ระบบ" → `hrconfig` (L1539) |
| Shell bar | `.shell-bar` (L1546) | สูง `--shell-h:52px` · z=`--z-sticky` · breadcrumb "ทรัพยากรบุคคล › ประเมินผลงาน" (L1548) |
| Bell (แจ้งเตือน) | `.icon-btn#notifBtn` + `.notif-dot` (L1551) | `toggleNotif(event)` (L2238) → เปิด `.notif-panel#notifPanel` |
| User chip / menu | `.user-chip` + `.user-menu#userMenu` (L1555–1556) | `toggleUserMenu()` (L2237) · applyRole() เติม `#uName/#uRole/#uAv` (L2232) |
| Content mount | `.content#page-content` (L1560) | `render()` เติม `pageHTML()` |

---

## §4 · Page Anatomy (ต่อ tab)

ทุกหน้าเริ่มด้วย `pageHTML()` (L2250): **demo-strip** (role switcher) → **page header** (`.ph` title + sub + action) → **tabs** (`.tabs.page-tabs`) → `#view`.

- **Demo strip** `.demo-strip` (L2258): label "มุมมองสาธิต (สิทธิ์)" + "ผลประเมิน/คะแนน = RESTRICTED — ปิดบังตามสิทธิ์" + `.seg-control` 3 ปุ่ม role.
- **Header action** (L2264): ปุ่ม **สร้างรอบประเมิน** โผล่เฉพาะ `state.tab==='cycle' && curRole().manage`.
- **Tab badges** (L2251–2255): cycle=จำนวนรอบ · appr=จำนวนแบบประเมิน · review=นับ `calibration|published` · report=ไม่มี badge (null).

### §4.1 · Tab `cycle` — รอบประเมิน · `cycleView()` L2273
ตาราง `.tbl` คอลัมน์ รหัส / รอบประเมิน (+ sub-note "อ้าง …(อ่านจาก ตั้งค่า HR)") / ช่วงเวลา / แบบประเมิน (นับคน) / สถานะ (`pill(CST,…)`). แถว `is-clickable` → `openDrawer('viewCycle',id)`.

### §4.2 · Tab `appr` — แบบประเมินรายคน · `apprView()` L2285
- **Overdue banner** `.note.is-warn` (L2293): "มี N แบบประเมินเกินกำหนด — ต้องเตือนผู้ประเมิน" + ปุ่ม **ส่งการเตือน** → `sendReminder()`.
- **Filter row** `.filter-row` (L2294): ช่องค้นหา `oninput=state.f.search` + `<select>` สถานะ (7 ตัวเลือก L2291) + ปุ่ม **ล้างตัวกรอง** (โผล่เมื่อมีตัวกรอง).
- **ตาราง** (L2302): พนักงาน / รอบ / น้ำหนัก KPI (`.wtag ok|bad`) / คะแนน (หัวหน้า) (`mask()`) / สถานะ (`pill(AST,…)`) / กำหนด (เกินกำหนด|ตามกำหนด) / ผลการตัดสิน. แถว → `openAppr(id)` (L2318) เปิด view-drawer tab `detail`.
- **Empty** → `emptyStateHTML(...)` (L2300).
- **Scope:** rows ผ่าน `scopeSelf()` (L2287) — คนนอก scope **ไม่อยู่ใน DOM** (ไม่ใช่แค่ mask).

### §4.3 · Tab `review` — สอบทาน + ผล & Gap · `reviewView()` L2340
- **Team Calibration** `teamCalibHTML()` (L2322) — โชว์เฉพาะ `!isStaff`: ตารางพนักงาน / คะแนนถ่วงน้ำหนัก / เกรดเสนอ (`gradeOf`) / `<select>` ปรับเกรด A–D + hookbox distribution "A n · B n · C n · D n". (mock · มติ OQ-PERF-04 KEPT)
- **คิวรอสอบทาน** `.sec` "รอสอบทาน (calibration · DOA)" (L2348) — เฉพาะ `!isStaff`: ปุ่ม **สอบทาน (DOA)** → `openModal('doaCalib',…)` เมื่อ `canReview && !cycleClosed`; ไม่งั้นโชว์ "รอบปิดแล้ว" / "รอผู้มีสิทธิ์สอบทาน".
- **ผล & Gap (เผยแพร่แล้ว)** `.sec` (L2358): ต่อคน — ปุ่ม **เปิดแผน PIP** (เฉพาะ decision มี "ทบทวน") · **เปิดแก้ไขผล** (reopen) · hookbox ส่งต่อ: **ส่งไปอบรม** (เฉพาะมี gap) · **ส่งเรื่องปรับตำแหน่ง/เงินเดือน** · **ส่งเข้า Succession Planning** (เฉพาะ topPerf). ปุ่ม mutation ทั้งหมด gate ด้วย `canReview && !closed`.

### §4.4 · Tab `report` — รายงาน · `reportView()` L2387
3 stat tiles (แบบประเมินในรอบ / เผยแพร่ผลแล้ว / ทบทวน (PIP)) + filter `<select>` รอบ (`state.f.repCycle`) + distribution funnel 4 bucket (ต่ำ <3.0 / ปานกลาง 3.0–3.9 / ดี 4.0–4.5 / ดีเยี่ยม >4.5).

---

## §5 · Component Inventory (anchor + states)

| component | anchor | states (R4) |
|---|---|---|
| Role seg-control | `.seg-control .seg-item` (L2260) · `setRole()` | default / `.is-active` (role ปัจจุบัน) |
| Page tab | `.tab` (L2266) | default / `.is-active` (สี primary + border-bottom) / hover / `.tab-badge` |
| List table row | `.tbl tbody tr.is-clickable` (L1396) | default / hover (`bg-off`) / clickable pointer |
| Weight tag | `.wtag.ok` / `.wtag.bad` (L1431–1433) | ok = 100% (เขียว) / bad = ≠100 (ส้ม) |
| Status pill | `.pill.*` ผ่าน `pill(CST/AST,…)` (L2228) | ดู §8 matrix |
| Masked value | `.masked` (L1496) · `mask()` (L2204) | โชว์ค่า (mask=false) / `•••` (mask=true) |
| Search-select | `.search-select .ss-input .ss-list` (L1815) | default / focus (open list) / typing (filter+`<mark>`) / picked (แสดง clear ซ่อน caret) / empty ("ไม่พบรายการ") / keyboard hi |
| KPI editor input | `.kpitbl .in` / `.in.w` / `.in.s` / `.in.ro` (L1424–1428) | default / focus (border primary) / readonly (`.ro`) |
| Weight-sum tag (live) | `#wsumTag` (L2551) · `onKpiEdit` (L2564) | ok/bad live update |
| Progress | `.progress` / `.progress.warn` (L1438) | width `--w` % |
| Timeline | `.tl li` / `.on` / `.wait` (L1451–1456) | done (เขียว) / current (`.wait` ส้ม) / pending (เทา) |
| Hookbox (display-only) | `.hookbox` (L1462) | dashed surface · ปุ่มส่งต่อ |
| Warn banner | `.note.is-warn` (L1472) | action-bound (มีปุ่ม) หรือ ล้วน |
| Primary btn busy | `#btnNewCycle/#btnKpi/#btnSelf/#btnMgr/#btnCalib/#btnCalibStage/#btnClose/#btnPip/#btnReopen` | default / `.is-disabled` + spinner `loader-2 spin` + "กำลัง…" (guard `state._busy`) |
| Empty state | `emptyStateHTML()` (L2300) | icon `clipboard-x` + title + desc + action "ล้างตัวกรอง" |

---

## §6 · Overlay Registry

| overlay | selector / id | เปิดด้วย | z-index | dismiss rules |
|---|---|---|---|---|
| Drawer | `.drawer#drawer` (L1577) | `openDrawer(mode,id)` (L1675) | `--z-drawer` **55** | Esc (L1755) · คลิก `.drawer-backdrop` → `closeDrawer()` (L1576) · ปุ่ม ปิด/ยกเลิก. animate `.is-open` + `lockScroll(true)` + `trapFocus` + `guardOverlayAutoCombo` |
| Drawer backdrop | `.drawer-backdrop#drawerBackdrop` (L1576) | (คู่กับ drawer) | `--z-backdrop` **50** | `onclick="closeDrawer()"` |
| Modal | `.modal-backdrop#modalBackdrop` > `.modal` (L1582) | `openModal(type,data)` (L1700) | `.modal-backdrop`=`--z-portal` **60** (DSP-01) | Esc (L1754 · เหนือ drawer) · คลิก backdrop → `closeModal()` (L1582) · `.modal` มี `event.stopPropagation()` (L1583) — คลิกในกล่องไม่ปิด · ปุ่ม ยกเลิก |
| Toast | `.toast#toast` (L1589) | `showToast(msg,variant,2800)` (L1739) | `--z-toast` **90** | **auto-dismiss 2800ms** (L1746) — ไม่มีปุ่มปิด |
| Notif panel | `.notif-panel#notifPanel` (L1552) | `toggleNotif(event)` (L2238) | `--z-dropdown` **40** | คลิกนอก `#notifBtn/#notifPanel` → ปิด (doc handler L2246) · **ไม่ผูก Esc** |
| User menu | `.user-menu#userMenu` (L1556) | `toggleUserMenu()` (L2237) | dropdown (kit) | คลิกนอก `.user-chip/.user-menu` → ปิด (L2245) · **ไม่ผูก Esc** |
| Search-select list | `.ss-list#ss-list-<key>` (L1825) | `ssOpen()` (L1880) | `--z-backdrop` (kit) | Esc = ปิดเฉพาะ list (L1891 · `stopPropagation`) · คลิกนอก `.ss-*` wrapper (L1893) · เลือก option |
| Portal menu (kit) | `.menu-fixed` (BASE-KIT UTILS L2062–2127) | portal จาก combobox ใน scroll container | `--z-portal` **60** | ตาม BASE-KIT (#95) — reposition on scroll |
| Sidebar (มือถือ) | `.sidebar#sidebar` (L1520) | `.nav-toggle` (L1547) | `--z-shell` **20** | toggle `.open` — shell ไม่ผูก Esc/backdrop |

**scroll lock:** `lockScroll()` (BASE-KIT UTILS · นับชั้นได้ modal-ซ้อน-drawer) → `body.is-overlay-open{overflow:hidden}` (L76). `closeModal()` ปลดล็อกเฉพาะเมื่อ drawer ไม่เปิดค้าง (L1730).
**focus:** `trapFocus`/`releaseFocus` ล็อกโฟกัสใน overlay · `guardOverlayAutoCombo()` (L1714) ป้องกัน trapFocus auto-focus ช่อง `.ss-input` แล้วเปิด dropdown เอง (DSP-02b สำเนา feature).

---

## §7 · Interaction Spec

### Esc chain (ตามลำดับ handler จริง)
1. **L1891** — `ssOnKey()` (search-select) : `Escape` → `e.stopPropagation()` + ปิดเฉพาะ dropdown list · **กัน event ทะลุไปปิด drawer/modal** (Rule #94). ทำงานก่อนเมื่อโฟกัสอยู่ในช่อง `.ss-input`.
2. **L1753** — global `keydown` : `if(state.modal.open) closeModal(); else if(state.drawer.open) closeDrawer();` — modal มาก่อน drawer เสมอ.

### Click-outside
- Search-select: `document.click` L1893 — ปิด list ที่ `open && !wrap.contains(target)`.
- User menu + Notif panel: `document.click` L2244–2247 — ปิดเมื่อคลิกนอกปุ่ม/พาเนล.

### Focus / RAF
- `openDrawer/openModal` ใช้ `requestAnimationFrame` เพิ่มคลาส `.is-open` (trigger CSS transition) แล้ว `trapFocus` + `guardOverlayAutoCombo` (rAF ซ้อน rAF กัน auto-combo).
- `render()` ใช้ `preserveRenderState()`/`restoreRenderState()` เก็บ scroll (รวม `.drawer-body`) + focus ข้าม innerHTML rebuild (Rule #29).
- `refreshView()` (L2270) rebuild เฉพาะ `#view` (ไม่ทั้งหน้า) เมื่อกรอง/ค้นหา — ลด rebuild.

### Positioning
`.drawer` = fixed ขวา `translateX(100%)` → `.is-open` translateX(0) (L886–899). `.notif-panel` = absolute ใต้ shell-bar `top:calc(var(--shell-h) - 4px);right:0` (L1486). `.ss-list` = absolute ใต้ input (ไม่ดันเนื้อหา).

### Busy guard
ทุก mutation เช็ค `if(state._busy) return;` ก่อน แล้ว set `state._busy=true` + disable ปุ่ม + spinner · reset ใน setTimeout callback.

---

## §8 · State-Driven UI Matrix

### รอบประเมิน — `CST` (L2226)
| status | pill label | class | ปุ่ม |
|---|---|---|---|
| `open` | เปิดกรอก | `pill-success` | ปิดรอบ (ถ้า manage) |
| `calibration` | สอบทาน | `pill-warning` | — |
| `closed` | ปิดรอบ | `pill-muted` | (read-only) |

### แบบประเมินรายคน — `AST` (L2227) · flow: goal → self → mgr → calibration → published
| status | pill label | class | ปุ่ม/พฤติกรรมหลัก |
|---|---|---|---|
| `goal` | ตั้งเป้า | `pill-muted` | KPI editor (เฉพาะ manage) → **บันทึกเป้า/KPI** (L2560) |
| `self` | ประเมินตนเอง | `pill-info` | ช่องคะแนนตนเอง + note → **บันทึกประเมินตนเอง** (L2536) |
| `mgr` | หัวหน้าประเมิน | `pill-info` | ช่องคะแนนหัวหน้า + live score → **บันทึกผลหัวหน้า** (L2540) |
| `calibration` | รอสอบทาน | `pill-warning` | **สอบทาน (DOA)** → staged modal |
| `published` | เผยแพร่ผล | `pill-success` | ส่งต่อผล / PIP / **เปิดแก้ไขผล** (reopen) |

### KPI editability gates (L2516–2519)
`editable` = `!closed && goal && manage` · `selfEdit` = `!closed && self` · `mgrEdit` = `!closed && mgr && (mgr∥manage)`. **`closed` (รอบปิด) = read-only ตั้งแต่ render** + banner "รอบนี้ปิดแล้ว — ดูได้อย่างเดียว แก้ไขไม่ได้" (L2526).

### Scope-driven UI (SEC · L2218–2224 · comment L1563)
| role | scope | เห็นอะไร |
|---|---|---|
| `staff` (mask=true) | **SELF** | เฉพาะแบบประเมินที่ `emp===r.name` · คะแนน mask `•••` · ซ่อนคิวสอบทาน · เปิดแบบคนอื่น = RESTRICTED banner (L2483) |
| `mgr` (dept) | **DEPT** | เฉพาะ `dept===r.dept` (ฝ่ายผลิต · OQ-PERF-03) · เปิดนอกแผนก = RESTRICTED banner (L2486) · ไม่มีปุ่มสร้าง/ปิดรอบ |
| `hr` (manage) | **ALL** | ทุกคน · ทุกปุ่ม mutation (สร้าง/ปิดรอบ/สอบทาน/PIP/reopen/ส่งต่อ) |

### DOA staged modal (`doaCalib` L2623) — 2 จังหวะ
- **จังหวะ 1 · เลือกผู้สอบทาน** (`!started`, `approvals` ว่าง): 2 slot ว่าง (`.slot-row` slot-no 1/2 · role "หัวหน้าสายงาน" / "ผู้สอบทาน (HRBP/ผู้บริหาร)") search-select `doa0`/`doa1` (preset `value:null` · L2786) → **ส่งสอบทาน** freeze รายชื่อ (คง `calibration`).
- **จังหวะ 2 · บันทึกผลรายขั้น** (`started`): timeline `.tl` ต่อขั้น (done/current/pending) · ขั้นสุดท้ายมี `<select>` ผลการตัดสิน (ผ่าน / ทบทวน (PIP) / ไม่ผ่าน) · ปุ่ม "บันทึกผลสอบทานขั้น N" หรือ (ขั้นสุดท้าย) "บันทึกผล + เผยแพร่ผล".

### view-drawer 4 sub-tabs (`dwViewAppr` L2464)
`detail` (L2482) / `kpi` (KPI/คะแนน · L2514) / `calib` (สอบทาน timeline 2 ขั้น · L2602) / `history` (ประวัติ audit append-only · L2613). สลับด้วย `state.view.tab='...';render()`.

---

## §9 · Microcopy (verbatim · R2)

### §9.1 Toast — ทุกข้อความ `showToast(...)` (คัดตรงตัวอักษรจากโค้ด · verifier-anchor)
```
[info]    " ไปหลักสูตรอบรม (ส่งต่อ ไม่แก้ที่นี่) — ไม่สร้างหลักสูตรในหน้านี้
[warning] กรุณากรอกชื่อ KPI ให้ครบ
[warning] กรุณาระบุประเด็นที่ต้องพัฒนา
[warning] กรุณาเลือกผู้สอบทานให้ครบทุกขั้น
[warning] กรุณาเลือกรอบจากตั้งค่า HR
[warning] กรุณาให้คะแนน (หัวหน้า) ครบทุก KPI (1–5)
[warning] กรุณาให้คะแนนตนเองครบทุก KPI (1–5)
[warning] น้ำหนัก KPI รวมต้องเท่ากับ 100% (ตอนนี้
[success] บันทึกประเมินตนเองแล้ว · ส่งต่อหัวหน้าประเมิน
[info]    บันทึกผลสอบทานขั้น
[warning] บันทึกผลสอบทานได้เฉพาะแบบประเมินที่รอสอบทาน
[success] บันทึกผลหัวหน้าแล้ว · ส่งเข้าสอบทาน (DOA)
[warning] บันทึกผลหัวหน้าได้เฉพาะขั้นหัวหน้าประเมิน
[success] บันทึกเป้า/KPI แล้ว · เปิดให้พนักงานประเมินตนเอง
[warning] บันทึกเป้า/KPI ได้เฉพาะขั้นตั้งเป้า
[warning] ประเมินตนเองได้เฉพาะขั้นประเมินตนเอง
[info]    ปิดรอบแล้ว · ล็อกการแก้ไข (soft archive)
[warning] รอบนี้ปิดแล้ว — แก้ไขไม่ได้
[success] สร้างรอบ · เปิดกรอก · แจ้งเตือนผู้เข้าร่วมแล้ว
[warning] สอบทานได้เฉพาะแบบประเมินที่ให้คะแนนหัวหน้าครบและรอสอบทาน
[warning] สิทธิ์ไม่พอ
[info]    ส่งการเตือนผู้ที่ประเมินไม่ครบ/เกินกำหนดแล้ว
[info]    ส่งจุดที่ต้องพัฒนา "
[info]    ส่งผลเข้า Succession Planning (ส่งต่อ ไม่แก้ที่นี่)
[info]    ส่งสอบทานแล้ว · รอผู้สอบทานขั้นที่ 1 บันทึกผล
[info]    ส่งเรื่องปรับเงินเดือน/เลื่อนตำแหน่งให้ระบบโยกย้าย (ไม่ปรับเอง)
[success] เปิดแก้ไขผลแล้ว · ส่งกลับขั้นหัวหน้าประเมิน · บันทึกผู้แก้ไว้ในประวัติ
[warning] เปิดแก้ไขได้เฉพาะผลที่เผยแพร่แล้ว
[success] เปิดแผน PIP แล้ว
[success] เผยแพร่ผล · บันทึกผลเข้า 7C · RESTRICTED · แจ้งเตือนพนักงานแล้ว
[info]    แล้ว · รอผู้สอบทานขั้นถัดไป
```

> **หมายเหตุ dev (การประกอบสตริงจริง):** บางบรรทัดข้างบนเป็น **fragment ที่ extractor ตัดตรงจุดต่อ `+ ตัวแปร`** — ข้อความเต็มบนจอคือ:
> - `ส่งจุดที่ต้องพัฒนา "` + `{gap}` + `" ไปหลักสูตรอบรม (ส่งต่อ ไม่แก้ที่นี่) — ไม่สร้างหลักสูตรในหน้านี้` (L2770)
> - `บันทึกผลสอบทานขั้น ` + `{no}` + ` แล้ว · รอผู้สอบทานขั้นถัดไป` (L2722)
> - `น้ำหนัก KPI รวมต้องเท่ากับ 100% (ตอนนี้ ` + `{sum}` + `%)` (L2574)

### §9.2 ปุ่ม (verbatim · L-anchors)
สร้างรอบประเมิน (L2264) · สร้างและเปิดกรอก (L2428) · เพิ่ม KPI (L2559) · บันทึกเป้า/KPI (L2560) · บันทึกประเมินตนเอง (L2536) · บันทึกผลหัวหน้า (L2540) · สอบทาน (DOA) (L2352/2476) · เริ่มสอบทาน + เลือกผู้สอบทาน (L2610) · ส่งสอบทาน (L2634) · บันทึกผลสอบทานขั้น N / บันทึกผล + เผยแพร่ผล (L2644) · ปิดรอบ (L2459/2656) · เปิดแผน PIP (L2366/2665) · เปิดแก้ไขผล (L2367/2679) · ส่งไปอบรม (L2374/2507) · ส่งเรื่องปรับตำแหน่ง/เงินเดือน (L2375/2508) · ส่งเข้า Succession Planning (L2376/2509) · ส่งการเตือน (L2293) · ล้างตัวกรอง (L2297) · ยกเลิก / ปิด (footer).

### §9.3 Placeholder / label / empty
- ค้นหา: "ค้นหาพนักงาน / ตำแหน่ง / แผนก…" (L2295) · search-select "ค้นหารอบที่ประกาศไว้…" (L2421) / "เลือกผู้สอบทาน…" (L2631/2632).
- KPI editor: "ชื่อ KPI" / "เป้าหมาย" (L2554/2556) · self note "สรุปผลงานของตนเองในรอบนี้…" (L2535) · mgr note "ความเห็น/ข้อเสนอแนะ…" (L2538).
- reopen: "ระบุเหตุผล เช่น คะแนนผิด / decision ผิด / ข้อมูลไม่ครบ" (L2676) · error "กรุณาระบุเหตุผล" (L2677).
- **Empty state (verbatim):** title "**ไม่พบแบบประเมินที่ค้นหา**" / desc "ลองปรับคำค้นหรือล้างตัวกรอง" (L2300).
- hookbox ว่าง: "ยังไม่มีคะแนนในทีมสำหรับ calibrate" (L2336) · "ไม่มีแบบประเมินที่รอสอบทาน" (L2354) · "ยังไม่มีผลที่เผยแพร่" (L2381).
- notif head: "การแจ้งเตือน (รอบเปิด · ครบกำหนด · ผล)" (L2240).

### §9.4 Banner / confirm (verbatim)
- reopen modal note-list (L2673): "ส่งแบบประเมินกลับขั้น "หัวหน้าประเมิน" — แก้คะแนน → สอบทาน (DOA) → เผยแพร่ผลใหม่" · "บันทึกผู้เปิดแก้ไข + เวลา + เหตุผล ลงประวัติ (audit · append-only) — ผลเดิมไม่ถูกลบ".
- closeCycle (L2654): "ปิดรอบจะล็อกการแก้ไขทั้งหมด (soft archive) — ย้อนกลับไม่ได้".
- RESTRICTED (L2484): "ข้อมูลนี้เป็นความลับ (RESTRICTED) — ดูได้เฉพาะแบบประเมินของตนเอง" · (L2487) "…หัวหน้าดูได้เฉพาะแผนกของตน".
- DOA note (L2643): "ขั้นสุดท้าย: บันทึกแล้วเผยแพร่ผล · ผล/คะแนน = RESTRICTED · แจ้งเตือนพนักงาน".

---

## §10 · Data Binding & BACKEND anchors

**Mock roots:** `state` (L1636 + Object.assign L2133) · `PERF` (L2145) = `{roles, people, cycles, configCycles, apprs, audit, notifs}`. `TODAY='2026-09-09'` (L2144).

| จุด plug (mock function) | ↔ FRD API (02_API) |
|---|---|
| `PERF.cycles` list / `cycleView` | `F131-API-01 GET /cycles` |
| `submitNewCycle()` (L2431) | `F131-API-02 POST /cycles` (อ่าน HR Config) |
| `dwViewCycle()` per-person status | `F131-API-03 GET /cycles/:id` |
| `doCloseCycle()` (L2734) | `F131-API-04 POST /cycles/:id/close` |
| `PERF.configCycles` (soft-ref) L2164 | `F131-API-05 GET /config/appraisal-cycles` (HR Config #107 · **feature อ่านไม่สร้าง**) |
| `apprView()` scoped+masked | `F131-API-06 GET /appraisals` |
| `dwViewAppr()` detail | `F131-API-07 GET /appraisals/:id` |
| `saveKpi()` (L2567) Σ=100 | `F131-API-08 PUT /appraisals/:id/kpis` |
| `saveSelf()` (L2583) | `F131-API-09 POST /appraisals/:id/self` |
| `saveMgr()` (L2592) | `F131-API-10 POST /appraisals/:id/manager-review` |
| `doCalibSend()` (L2685) freeze reviewers | `F131-API-11 POST /appraisals/:id/calibration/send` |
| `doCalibStage()` (L2706) publish บนขั้นสุดท้าย | `F131-API-12 POST /appraisals/:id/calibration/stage` |
| `doPip()` (L2741) | `F131-API-13 POST /appraisals/:id/pip` |
| `doReopen()` (L2753) | `F131-API-14 POST /appraisals/:id/reopen` (OQ-PERF-01) |
| `sendReminder()` (L2774) | `F131-API-15 POST /appraisals/:id/reminder` |
| `sendTraining()` (L2770) | `F131-API-16 POST …/dispatch/training` (gap → Training hook) |
| `sendMovement()` (L2771) | `F131-API-17 POST …/dispatch/movement` (→ Movement event) |
| `sendSuccession()` (L2773) | `F131-API-18 POST …/dispatch/succession` (FIX-09) |
| `reportView()` distribution | `F131-API-19 GET /reports/distribution` |
| `pushAudit()` (L2618) append-only | 04_DB `T_perf_audit` (ใครแก้ + at) |
| CSQ 7C hook (L2727 `บันทึกผลประเมินเข้า 7C` + L1565 comment) | `perf.result.published` → ยิงท่อ 7C ตอนเผยแพร่ผล **รายคน** (มติ OQ-PERF-02) · ไม่ประกาศ OC/DC ซ้ำ |

> **จุดสำคัญ dev:** ทุก dispatch (`sendTraining/Movement/Succession`) เป็น **display-only** — "ส่งต่อ ไม่แก้ที่นี่" (toast) · ไม่ mutate ปลายทางในหน้านี้. Person resolve ใน DOA slot = `PERF.people` (L2151), slot **preset null** บังคับผู้ส่งเลือกคนจริงต่อตำแหน่ง (L2785–2787).

---

## §11 · Traceability + Drift Log

### §11.1 · 3-way map (Brief ↔ FRD ↔ HTML)
| Brief §/หน้า | FRD (P-xx / API / BR) | HTML anchor |
|---|---|---|
| §4.1 cycle | P-01 · API-01/02/03/04/05 · BR-01/09 | `cycleView` L2273 · `dwNewCycle` L2416 · `dwViewCycle` L2447 |
| §4.2 appr + KPI | P-02 · API-06/07/08/09/10 · BR-02/03/04 · VR-01 (Σ=100) | `apprView` L2285 · `tabKpi` L2514 · `saveKpi/Self/Mgr` |
| §4.3 review/calib | P-03 · API-11/12/13/14/16/17/18 · BR-05 · ENG-DOA | `reviewView` L2340 · `doaCalib` modal L2623 · `doCalibSend/Stage` |
| §4.4 report | P-04 · API-19 · BR-08 | `reportView` L2387 |
| §8 scope/mask | FN-17 applyScopeAndMask · BR-08/11 · D-CLASS · OQ-PERF-03 (LD-04) | `scopeSelf` L2220 · `mask` L2204 · guards L2483/2486 |
| §8 reopen | API-14 · OQ-PERF-01 (LD-05) | `doReopen` L2753 · `reopen` modal L2667 |
| §10 CSQ 7C | OQ-PERF-02 (per-person publish) · CSQ 7C | L2727 · comment L1565 |
| §6 audit | FN-16 pushAudit · 04_DB T_perf_audit · BR-09 | `pushAudit` L2618 · `tabHistory` L2613 |

### §11.2 · ⚠️ Drift Log
| # | ประเภท | รายการ | ข้อเสนอ |
|---|---|---|---|
| D1 | **HTML-only** | Team Calibration ระดับทีม (`teamCalibHTML` L2322) + `<select>` ปรับเกรด — mock, ยังไม่ผูกปลายทาง (มติ OQ-PERF-04 KEPT) | คงไว้ · FRD ควรระบุเป็น mock/future (ไม่มี API) — dev ไม่ต้อง persist รอบนี้ |
| D2 | **HTML-only** | Succession dispatch (`sendSuccession` L2773 · ปุ่ม L2376/2509) | มี API-18 ใน FRD แล้ว (FIX-09) — **aligned**, ระบุไว้กันสับสน |
| D3 | **display-only surface** | dispatch training/movement/succession = toast อย่างเดียว (ไม่ mutate) | dev bind เป็น POST hook (API-16/17/18) ปลายทางจริง — จอไม่รับผล |
| D4 | **route** | จอใช้ tab-state ไม่ใช่ hash route (§2) | dev เลือก: single-page tab (ตามจอ) หรือ map 4 sub-route เพื่อ deep-link |
| D5 | **soft-ref** | รอบ/แบบฟอร์มอ่านจาก HR Config #107 (`configCycles` L2164) · id จริง `appraisal_cycle #107` ไม่โชว์ snake_case (Rule #81) | dev = soft-ref (API-05) · ห้าม hardcode รอบในฟีเจอร์ |

**ไม่มี business drift ที่ block.** ทุก mutation มี role/stage/closed guard ครบ (FIX-01..10 + OQ-PERF-01/03).

---

## §12 · Diff จากเวอร์ชันก่อน
— N/A (บรีฟรอบแรก · ไม่มี HTML เก่าให้ diff)

---

## §13 · 💡 ข้อเสนอ (ไม่ใช่ AS-BUILT — R1)

1. **Deep-link tabs** — ผูก `state.tab` เข้ากับ hash (`getRoute/navigate` มีอยู่แล้ว L1663–1670) เพื่อ refresh กลับ tab เดิม + แชร์ลิงก์ตรงหน้า `review`.
2. **Team Calibration persistence** — ถ้าจะทำจริง (นอกรอบนี้) ต้องมี API save เกรดที่ปรับ + audit ผู้ปรับ (ตอนนี้ `<select>` L2333 ไม่ผูก handler).
3. **Notif "N ใหม่"** — `.notif-dot` (L1551) เป็นจุดคงที่ ไม่มีตัวนับ · เสนอผูกจำนวน unread จาก `PERF.notifs`.
4. **DOA slot > 2 ขั้น** — ปัจจุบัน hardcode 2 slot (L2631–2632). ถ้าสาย DOA จริงมี >2 ขั้น dev ต้อง generate slot จาก DOA engine (feature ประกาศเท่านั้น — ห้าม hardcode chain, ตรงตาม `doa-declaration`).

---

*จบ UI Brief — F-HR-Performance · ประเมินผลงาน (Performance)*
