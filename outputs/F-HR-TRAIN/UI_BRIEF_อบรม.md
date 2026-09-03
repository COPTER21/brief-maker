# UI Brief — F-HR-TRAIN · อบรม (Training)

> **AS-BUILT UI spec** สกัดจาก HTML prototype แบบ 1:1 (Extraction-based · Iron Rule R1)
> ทุกบรรทัด trace กลับ selector / function / ข้อความจริงใน `อบรม.html` ได้
> ใช้คู่กับ **HTML (source of truth) + FRD Pack (สเปคระบบ)** — บรีฟนี้ = design intent handoff

---

## §0 · Document Control + Pairing

| หัวข้อ | ค่า |
|---|---|
| Feature | F-HR-TRAIN · อบรม (Training & Development · F133) |
| HTML source | `outputs/F-HR-TRAIN/อบรม.html` (3029 บรรทัด · `<title>อบรม (Training) · CUBE NATIVE`) |
| Archetype | **master** (แคตตาล็อกหลักสูตร + การลงทะเบียน · **ไม่ใช่** Pattern Q เอกสาร) |
| BASE-KIT | v6.4 (CUBE Warm Light · Iron Rule #104 "1 feature = 1 เมนู") |
| Shell | 1 เมนู "พัฒนาบุคลากร" → feature "อบรม" · ส่วนย่อย = **4 tabs** ในหน้าเดียว route `#/train/<tab>` |
| จอทั้งหมด | 12 จอ (4 tab + 4 drawer + 5 modal type · overlay ไม่มี route แยก) |
| FRD Pair | `FRD_F-HR-TRAIN_Pack/` (01_UI P-01..P-12 · 02_API API-01..28 · 05_RULES BR-01..18) — **paired ✅** |
| Drift status | ไม่มี business-blocking drift · HTML-only = prototype scaffolding (Iron Rule #105) — ดู §11 Drift Log |
| ไลบรารี | Lucide 0.469.0 (multi-CDN fallback: unpkg → jsdelivr → cdnjs · pinned) · ฟอนต์ Satoshi (fontshare) + Noto Sans Thai (googleapis) |
| ⚠️ CDN dependency | ฟอนต์ 3 แหล่ง + Lucide 3 CDN — **offline จะ fallback ฟอนต์/ไม่มี icon** (UI ยังใช้งานได้ · loader มี no-op fallback + 5s safety net) |

---

## §1 · Design Tokens AS-BUILT

**Selector anchor:** `<style>` `:root` (บรรทัด 24-67 · BASE-KIT v6.4 — DO NOT EDIT Rule #69)

### สี (CUBE CI · Warm Light — ห้าม hardcode hex ในระบบจริง ใช้ var)
| token | ค่า | ใช้ |
|---|---|---|
| `--c-primary` | `#FF3B30` | ปุ่มหลัก · active · error accent |
| `--c-primary-hover` | `#E62E24` | hover ปุ่มหลัก |
| `--c-teal` | `#FF9A1F` | accent รอง (gradient logo/avatar · gap chip) |
| `--c-ink` / `--c-navy` | `#111111` | ตัวอักษรหลัก · sidebar bg · bulk bar · toast bg |
| `--c-mute` / `--c-mute-2` / `--c-mute-3` | `#54565C` / `#73757B` / `#9A9CA2` | ตัวอักษรรอง 3 ระดับ |
| `--c-line` / `--c-line-2` / `--c-line-3` | `#DEDAD4` / `#E9E5E0` / `#F1EEEA` | เส้นขอบ 3 ระดับ |
| `--c-bg-off` | `#FAF8F5` | พื้นหลังหน้า · thead |
| `--c-success` / `--c-warning` / `--c-danger` | `#1F9D55` / `#E8870F` / `#E62E24` | pill/toast/note สถานะ |

### Type scale (Iron Rule locked · บรรทัด 54-62)
`--fs-h1:22px` · `--fs-h2:17px` · `--fs-h3:15px` · `--fs-body:14px` · `--fs-sub:13px` · `--fs-meta:12px` · `--fs-cap:11px` · `--fs-kpi:28px`
Font stack: `'Satoshi','Noto Sans Thai',system-ui,sans-serif` · หัวข้อ/ตัวเลขใหญ่ = `'Noto Sans Thai'`

### Spacing / Radius (บรรทัด 63-66)
`--sp-xs:4px … --sp-xl:28px` · `--r-xs:4px … --r-lg:12px · --r-full:999px`

### Layout tokens
`--sidebar-w:232px` · `--shell-h:52px` · scrollbar 5px (Iron Rule #49) · `scrollbar-gutter:stable` (Rule #35 กัน jank)

### ⭐ Z-INDEX MAP (สูง → ต่ำ · บรรทัด 44-53 · Rule: ขาด var = computed auto = overlay ซ้อนพัง)
| token | ค่า | ใช้กับ |
|---|---|---|
| `--z-toast` | **90** | toast (สูงสุด — เห็นเหนือทุกอย่าง) |
| `--z-portal` | **60** | เมนู portal → `#overlay-root` (Rule #95) · **modal-backdrop ก็ = 60** |
| `--z-drawer` | **55** | ตัว drawer `.drawer` |
| `--z-backdrop` | **50** | ฉากหลัง drawer + `.ss-list` (search-select list) |
| `--z-dropdown` | **40** | user menu · tooltip · demo-strip |
| `--z-sticky` | **30** | shell-bar · thead sticky |
| `--z-shell` | **20** | sidebar |

> **สำคัญ (บรรทัด 1111):** `.modal-backdrop` ตั้ง z = `--z-portal` (60) **เท่ากับ** portal โดยตั้งใจ — เพื่อให้ combobox ที่ portal ออกไปใน modal โผล่เหนือ modal ได้ตาม DOM order · **ห้ามตั้ง > portal** ไม่งั้น dropdown ใน modal จะจม

---

## §2 · Route Map

**Anchor:** `getRoute()` (บรรทัด 1666) · `render()` (บรรทัด 2304-2318) · `window.hashchange` (บรรทัด 2035)

| route | จอ | default | refresh-safe |
|---|---|---|---|
| `#/` หรือ `#` หรือ ว่าง | → `home` → fallback **course** | ✅ | ✅ (hash-based) |
| `#/train/course` | Tab 1 หลักสูตร | | ✅ |
| `#/train/plan` | Tab 2 แผน/ลงทะเบียน | | ✅ |
| `#/train/result` | Tab 3 ผล/ใบรับรอง | | ✅ |
| `#/train/report` | Tab 4 รายงาน | | ✅ |

- **Tab parse:** `render()` → `TC.tab = rt.indexOf('train/')===0 ? rt.split('/')[1] : 'course'` · ถ้าไม่อยู่ใน `['course','plan','result','report']` → บังคับ `'course'` (บรรทัด 2307-2308)
- **ทุก tab click** = `go('train/<tab>')` → `navigate()` → `location.hash='#/'+route` (ไม่ reload · SPA)
- **Overlays ไม่มี route** — drawer/modal เปิดผ่าน state (`state.drawer` / `state.modal` + `TC.dctx` / `TC.mctx`) ไม่ผูก hash · refresh แล้ว overlay หาย (ตั้งใจ · ตรง FRD "overlay เป็น drawer/modal ไม่มี route แยก")

---

## §3 · Layout Shell

**Anchor:** `<aside class="sidebar">` (บรรทัด 1497) · `<header class="shell-bar">` (บรรทัด 1534) · `<main class="main">` (บรรทัด 1533)

| region | selector | ขนาด/พฤติกรรม |
|---|---|---|
| Sidebar | `.sidebar` (fixed · z=`--z-shell` 20) | width `--sidebar-w` 232px · bg `#111111` · 1 module "พัฒนาบุคลากร" collapsible (`toggleModule()` · Rule #27 header ไม่ navigable) |
| Feature item | `.sb-item[data-feature="train"]` | active = `.is-active` (แถบ ::before ซ้าย) · sibling `perf`/`expense`/`hr-config` = `ctxStub()` (นอก scope · toast) |
| Shell bar | `.shell-bar` (sticky top · z=`--z-sticky` 30) | height `--shell-h` 52px · breadcrumb `พัฒนาบุคลากร › อบรม` · bell (stub toast) · user-chip |
| Main | `.main` | `margin-left:232px` · `<1180px` → sidebar off-canvas (`.nav-toggle` โผล่ · Rule #97) |
| Content host | `#page-content` | render โดย `renderPage()` · list ใช้ `.page-fill` (ยืดเต็มสูง · Rule #96) |
| Demo strip | `.demo-strip` (fixed ล่างซ้าย · z=`--z-dropdown` 40) | persona switch (prototype · Iron Rule #105 — **ไม่ใช่ส่วนของ feature จริง**) |

---

## §4 · Page Anatomy (ต่อจอ)

โครงร่วมทุก tab: `renderPage()` (บรรทัด 2321) → `.ph` (page header: title + sub + actions) → `.tabs` (4 tab bar) → body ต่อ tab

**Tab bar (`.tabs` · บรรทัด 2336):** 4 tab พร้อม count chip `.tab-ct` — course=จำนวนหลักสูตร · plan=จำนวนรอบ · result=จำนวนลงทะเบียน(≠cancelled) · report=ไม่มี count
**Page action ต่อ tab (บรรทัด 2331-2334):**
- course + non-viewer → `สร้างหลักสูตร` (primary · `openCourseCreate()`)
- plan + non-viewer → `สร้างรอบอบรม` (primary · `openSessionCreate()`)
- report → `Export CSV` (secondary · toast "ต่อ dev")

### P-01 · Tab หลักสูตร (`renderCourseTab()` บรรทัด 2359)
- Filter bar: search (ชื่อ/รหัส/ผู้สอน) · select หมวด (จาก `CATEGORIES`) · select สถานะ (จาก `COURSE_STATUS`) · ปุ่ม `ล้างตัวกรอง`
- Table 7 คอลัมน์: หลักสูตร/รหัส · หมวด · ผู้สอน · ระยะเวลา · ค่าใช้จ่าย(chip) · งบ(`col-num` · mask) · สถานะ(pill)
- แถว `.is-clickable` → `openCourseView(id)` (P-06)
- Empty: `ไม่พบหลักสูตร`
- Footer: `${n} รายการ`

### P-02 · Tab แผน/ลงทะเบียน (`renderPlanTab()` บรรทัด 2392)
- **approvalHook** (`.note.is-info` · บรรทัด 2397): แสดงเมื่อ `persona==='manager'` และมี enroll `pending_doa` → `งานรออนุมัติของฉัน · N รายการ` (My Approval)
- Filter: search (หลักสูตร/รหัสรอบ/สถานที่) · select สถานะ (จาก `SESSION_STATUS`) · `ล้างตัวกรอง`
- Table 6 คอลัมน์: หลักสูตร/รอบ · ประเภท(cost chip) · วันเวลา · สถานที่(cell-truncate) · ผู้เรียน(`capBar`) · สถานะ(pill)
- แถว → `openSessionView(id)` (P-08) · Empty: `ไม่พบรอบอบรม`

### P-03 · Tab ผล/ใบรับรอง (`renderResultTab()` บรรทัด 2426)
- list ทุก enroll ยกเว้น `cancelled` · Filter: search (ผู้เรียน/หลักสูตร) · select สถานะ (`pending_doa/confirmed/passed/failed`) · `ล้างตัวกรอง`
- Table 6 คอลัมน์: ผู้เรียน(avatar + ชื่อคลิก→ประวัติ + gap chip) · หลักสูตร/รอบ · สถานะลงทะเบียน(pill) · ผล(`resultChip`+`evalChip`) · ใบรับรอง(`certChip`) · จัดการ(state-driven action cell)
- **Action cell (state-driven · บรรทัด 2443-2451):** ดู §8 State Matrix
- ชื่อผู้เรียน `.lnk-name` → `openEmpHistory(empId)` (P-12) · แถว → `openSessionView(sessionId,'learner')`
- Empty: `ไม่พบรายการลงทะเบียน`

### P-04 · Tab รายงาน (`renderReportTab()` บรรทัด 2466 · Pattern J3 mixed dashboard)
- Filter (กรองตามหลักสูตร) · 5 stat cards (หลักสูตร · รอบอบรม · ลงทะเบียนทั้งหมด · ผ่าน · อัตราผ่าน %)
- **Funnel** completion rate ต่อหลักสูตร (`.funnel-row` · `x.rt%` + `(ผ่าน/บันทึกแล้ว)`) — นับเฉพาะ `isClosedResult` (รอบ closed · FIX-01)
- **Cost-per-head cards** (`.cph-grid` · หลักสูตร has_cost): งบ · ผู้ผ่าน · ต้นทุนต่อหัว = งบ÷ผู้ผ่าน (mask ตาม role · ผู้ผ่าน=0/ฟรี → "—" กันหารศูนย์)
- **oos block** (`.oos` · ขอบเขตที่ไม่รองรับ 5 รายการ — "ระบบไม่มีปุ่ม/ทางลัดให้ทำ")

---

## §5 · Component Inventory (anchor + states)

| component | selector / fn | states (R4) |
|---|---|---|
| Table row | `.table tbody tr.is-clickable` | default · hover (`bg-off`) · selected (`.is-selected`) · disabled action = `.is-disabled`+`disabled` attr |
| Filter search | `.input-search input` (`oninput` → `renderPageOnly()`) | default · focus (primary ring) — ไม่มี debounce (client filter) |
| Select filter | `.select` (`onchange`) | default · focus · **ไม่มี** loading/error (client mock) |
| Cost chip | `costChip(has)` | `.is-cost` (มีค่าใช้จ่าย) / `.is-free` (ไม่มีค่าใช้จ่าย) |
| Result chip | `resultChip(e)` | pass=`.is-free` ผ่าน · fail=`.is-fail` ไม่ผ่าน · null="—" |
| Eval chip | `evalChip(e)` | มี evalScore → `.is-cert` "ประเมิน N/5" (title=comment) · ไม่มี = ว่าง |
| Attendance chip | `attChip(e)` | attended=true "เข้าอบรม" · false "ขาดอบรม" · null=ว่าง |
| Cert chip | `certChip(e)` | มี cert → "ออกใบรับรองแล้ว" · ไม่มี="—" |
| Capacity bar | `capBar(sid)` | `.cap-fill` gradient · เต็ม → `.is-full` (warning) · แสดง `n/capacity` |
| Status pill | `courseStatusPill`/`sessionStatusPill`/`enrollStatusPill` | map ตาม §8 (`.pill-muted/info/success/warning/danger`) |
| Search-select | `searchSelectHTML(key)` + `initSearchSelect()` (Iron Rule #34) | closed · open (`.ss-list`) · typing (highlight `<mark>`) · empty (`.ss-empty`) · selected (ปุ่ม X `.ss-clear` โผล่ · caret ซ่อน) · keyboard (↑↓ Enter Esc · บรรทัด 1886) |
| Pass/fail picker | `.rf-pick` + `pickResult(v)` | default · `.on-pass` (success) · `.on-fail` (danger) |
| Eval picker 1-5 | `.ev-pick` + `pickEval(n)` | default · `.on` (primary) — ไม่บังคับ |
| Attendance toggle | `.att-toggle` + `setAttendance(eid,val)` | `.on-in` (เข้า·success) / `.on-out` (ขาด·danger) |
| has_cost toggle | `.bm-card` + checkbox `.cb` (course form) | `.is-checked` เปิด → เผยงบ + EC ref card |
| Busy button | `TC.busy` → `disabled` + icon `loader-2 spin` | idle · busy "กำลังบันทึก" (300ms mock delay) |
| Empty state | `emptyStateHTML()` (Iron Rule #39) | icon + title + desc + (optional action button) |

---

## §6 · Overlay Registry

**Anchor:** container ประกาศ HTML บรรทัด 1576-1592 · toggle fn บรรทัด 1678-1721 / `tcOpenModal()` 2893

| overlay | selector | ขนาด | เปิด | ปิด (dismiss) | z-index |
|---|---|---|---|---|---|
| **Sidebar** | `.sidebar` | 232px (fixed) | เสมอ (off-canvas <1180px) | — (nav-toggle บนจอเล็ก) | `--z-shell` 20 |
| **User menu** | `.user-menu` | 240px | `toggleUserMenu()` (คลิก user-chip) | click-outside (บรรทัด 2293) | `--z-dropdown` 40 |
| **Drawer** | `.drawer` + `.drawer-backdrop` | 920px (standard 680px · max 96vw) | `openDrawer()`/`tcOpen()` — slide `transform 280ms` | Esc · คลิก `.drawer-backdrop` → `closeDrawer()` · ปุ่ม X/ปิด | drawer `--z-drawer` 55 · backdrop `--z-backdrop` 50 |
| **Modal** | `.modal` + `.modal-backdrop` | 440px (max 92vw · 90vh) | `openModal()`/`tcOpenModal()` — `scale(0.96)→1` 200ms | Esc · คลิก `.modal-backdrop` → `closeModal()` · ปุ่มยกเลิก/ปิด | `--z-portal` 60 (=portal ตั้งใจ) |
| **Search-select list** | `.ss-list` | ตาม input (portal → `.menu-fixed`) | focus/พิมพ์ในช่อง search-select | click-outside (บรรทัด 1895) · Esc (ปิดแค่ list · บรรทัด 1893) · เลือก option | `--z-backdrop` 50 (portal ยกเป็น `--z-portal` 60) |
| **Portal menu** | `.menu-fixed` (`#overlay-root`) | ตาม trigger | `portalMenu()` (Rule #95 · หนี overflow clip) | คืนที่เดิมตอนปิด list | `--z-portal` 60 |
| **Toast** | `.toast` | max 380px (fixed ล่างขวา) | `showToast(msg,variant,dur)` | auto-hide (default 2800ms) | `--z-toast` 90 |
| **Demo strip** | `.demo-strip` | fixed ล่างซ้าย | เสมอ (prototype) | — (scaffolding) | `--z-dropdown` 40 |

**Backdrop click map:**
- `.drawer-backdrop #drawerBackdrop` → `closeDrawer()`
- `.modal-backdrop #modalBackdrop` → `closeModal()` · ตัว `.modal` มี `event.stopPropagation()` (คลิกในกล่องไม่ปิด)

**Drawer types (4 · `renderDrawer()` บรรทัด 2527):**
1. `courseFormDrawer()` — create/edit หลักสูตร (P-05)
2. `courseViewDrawer()` — รายละเอียดหลักสูตร (P-06 · header action state-driven)
3. `sessionFormDrawer()` — create/edit รอบ (P-07)
4. `sessionViewDrawer()` — รายละเอียดรอบ + **4 drawer-tabs** (P-08): `รายละเอียด › ผู้เรียน › อนุมัติ/ค่าใช้จ่าย › ประวัติ` (`setSessionTab()` · **ไม่ใช่ route**)

**Modal types (5 + shared · `renderModal()` บรรทัด 2895):**
1. `enroll` — ลงทะเบียนผู้เรียน (P-09 · gap picker + search-select คน portal)
2. `doa` — ส่งอนุมัติ (P-10 · slot picker ต่อขั้น + search-select ผู้อนุมัติ)
3. `result` — บันทึกผล + ประเมิน (P-11 · pass/fail + eval 1-5 + comment)
4. `emphist` — ประวัติอบรมรายคน (P-12 · read · ชม.สะสม)
5. `confirm` / `reason` — shared (ปิด/ยกเลิก/ปฏิเสธ · reason ต้องระบุ)

---

## §7 · Interaction Spec

### Esc chain (anchor: handler จริง)
1. **บรรทัด 1740** — `window keydown` `if (e.key === 'Escape')`: ถ้า `state.modal.open` → `closeModal()` · else if `state.drawer.open` → `closeDrawer()` (modal ก่อน drawer — ปิดชั้นบนสุดก่อน)
2. **บรรทัด 1893** — `ssOnKey()` `else if(e.key === 'Escape')`: `e.stopPropagation()` + ปิดแค่ search-select list (ห้ามทะลุไปปิด drawer/modal · Rule #94 Esc chain)

### Click-outside
- User menu: `document click` ถ้าไม่อยู่ใน `.user-chip`/`.user-menu` → ปิด (บรรทัด 2293)
- Search-select: `document click` ถ้าไม่อยู่ใน `ss-<key>` → ปิด list (บรรทัด 1895)
- Backdrop click = ปิด overlay (ดู §6)

### Focus / scroll management (BASE-KIT · บรรทัด 2105-2135)
- `lockScroll(on)` → `body.is-overlay-open{overflow:hidden}` · นับชั้น (modal ปิดแล้ว drawer ยังเปิด → ยัง lock · บรรทัด 1717)
- `trapFocus(box)` → กัน Tab หลุด + โฟกัสตัวแรก + คืนโฟกัสเดิมตอนปิด (`releaseFocus`)
- `preserveRenderState()`/`restoreRenderState()` (Rule #29) → เก็บ scrollTop drawer/modal/page + focus+selection ข้าม innerHTML rebuild
- **BUG-04 guard (บรรทัด 2893):** `tcOpenModal` หลัง trapFocus ถ้าช่องแรกเป็น `.ss-input` → บังคับปิด dropdown + blur (กัน search-select เผลอเปิดเองตอน auto-focus)

### Positioning
- Drawer/modal/toast/backdrop = `position:fixed`
- `.ss-list` ปกติ = `position:absolute` (ไม่ดันเนื้อหา · Rule #35) · ใน modal → portal เป็น `.menu-fixed` (`portalMenu()`) หนี overflow clip + reposition ตอน scroll/resize

### Render pattern
- `render()` (full) — rebuild page + drawer + modal · เรียก `renderIcons()` + `mountCombos()` (init search-select หลัง markup อยู่ DOM)
- `renderPageOnly()` — rebuild เฉพาะ `#page-content` (ใช้ตอน filter · ไม่แตะ overlay)

---

## §8 · State-Driven UI Matrix

**Anchor status maps:** `COURSE_STATUS` (2198) · `SESSION_STATUS` (2199) · `ENROLL_STATUS` (2200)

### Course status (`COURSE_STATUS`)
| enum | label | pill | header action (P-06 · non-viewer) |
|---|---|---|---|
| `draft` | ร่าง | `pill-muted` | แก้ไข + เผยแพร่ |
| `published` | เผยแพร่ | `pill-success` | แก้ไข + ปิดหลักสูตร (confirm) |
| `closed` | ปิดหลักสูตร | `pill-muted` | — |

### Session status (`SESSION_STATUS`)
| enum | label | pill | header action (P-08 · non-viewer) |
|---|---|---|---|
| `draft` | ร่าง (ยังไม่เปิดรับ) | `pill-muted` | แก้ไข + เปิดรับสมัคร |
| `open` | เปิดรับสมัคร | `pill-success` | ปิดรอบ (confirm) |
| `closed` | ปิดรอบ | `pill-muted` | — (ปลดล็อกเช็คชื่อ+บันทึกผล) |

### Enrollment status (`ENROLL_STATUS` · 5 states)
| enum | label | pill |
|---|---|---|
| `pending_doa` | รออนุมัติ (DOA) | `pill-warning` |
| `confirmed` | ยืนยันลงทะเบียน | `pill-info` |
| `passed` | ผ่าน | `pill-success` |
| `failed` | ไม่ผ่าน | `pill-danger` |
| `cancelled` | ยกเลิก | `pill-muted` |

### Action cell — Tab ผล (P-03 · บรรทัด 2443) & Learner row (P-08 · บรรทัด 2701)
| เงื่อนไข | ปุ่ม/สถานะที่แสดง |
|---|---|
| `confirmed` + รอบ **ยังไม่** closed | `บันทึกผล` **disabled** (tooltip "บันทึกผลได้หลังปิดรอบ") |
| `confirmed` + closed + `attended≠true` | `บันทึกผล` **disabled** (tooltip "ต้องเช็คชื่อเข้าอบรมก่อน") + att-toggle (learner tab) |
| `confirmed` + closed + `attended===true` | `บันทึกผล` เปิดใช้ → `openResultModal()` |
| `passed` + `!cert` | `ออกใบรับรอง` → `issueCert()` |
| `pending_doa` (Tab ผล) | chip "รออนุมัติ" (read) |
| `pending_doa` (learner tab · **approver**) | ปุ่ม X (reject) + `อนุมัติ` (`enrollApprove`) |
| `pending_doa` (learner tab · **non-approver**) | `ยกเลิก` (`cancelEnroll`) |
| viewer (ทุก state) | ไม่มีปุ่ม action (RO) |

### Persona / Masking (Iron Rule #105 · `PERSONAS` บรรทัด 2148 · `maskMoney` 2283)
| persona | canApprove | unmask money | ปุ่มสร้าง/แก้ | อนุมัติ |
|---|:--:|:--:|:--:|:--:|
| `hr` (เจ้าหน้าที่อบรม) | ❌ | ✅ | ✅ | ❌ |
| `manager` (หัวหน้า/ผู้อนุมัติ) | ✅ | ✅ | ✅ | ✅ |
| `viewer` (ผู้ชมทั่วไป) | ❌ | ❌ (`••••••`) | ❌ | ❌ |
- money mask (FN-94): งบ · มูลค่า EC · ต้นทุนต่อหัว → viewer เห็น `••••••` (ทั้ง UI + report/export)
- viewer กระทำ action → `viewerRO()` → toast `สิทธิ์อ่านอย่างเดียว`

---

## §9 · Microcopy (verbatim — R2 · คัดตรงตัวจากโค้ด)

### Toast ทั้งหมด (43 ข้อความ · `showToast()`/`ntf()` — ห้าม paraphrase)
| variant | ข้อความ (verbatim) |
|---|---|
| warning | `กรุณากรอกข้อมูลที่ไฮไลต์ให้ครบ` |
| warning | `กรุณาระบุเหตุผล` |
| warning | `กรุณาเลือกผล (ผ่าน/ไม่ผ่าน)` |
| warning | `กรุณาเลือกผู้อนุมัติให้ครบทุกขั้น` |
| warning | `กรุณาเลือกผู้เรียน` |
| warning | `กรุณาเลือกหมวดหลักสูตร` |
| warning | `กรุณาเลือกหลักสูตร` |
| warning | `จำนวนรับเต็มแล้ว` |
| warning | `จำนวนรับเต็มแล้ว — ลงทะเบียนเพิ่มไม่ได้` |
| warning | `ต้องเช็คชื่อเข้าอบรมก่อน` |
| success | `บันทึกการแก้ไขแล้ว` |
| success | `บันทึกผลและประกาศผลแล้ว` |
| warning | `บันทึกผลได้หลังปิดรอบอบรม (จบการอบรม)` |
| warning | `บันทึกผลได้เฉพาะผู้เรียนที่ยืนยันลงทะเบียนแล้ว` |
| success | `บันทึกร่างแล้ว` |
| success | `ปิดรอบแล้ว` |
| success | `ปิดหลักสูตรแล้ว` |
| warning | `ผู้เรียนคนนี้ลงทะเบียนรอบนี้แล้ว` |
| success | `ยกเลิกการลงทะเบียนแล้ว` |
| success | `ลงทะเบียนสำเร็จ (ยืนยันแล้ว)` |
| info | `ศูนย์แจ้งเตือน (ENG-NOTIFY) — เชื่อมจริงตอน dev` |
| success | `สร้างรอบอบรมแล้ว (ร่าง) — กด “เปิดรับสมัคร” จากหน้ารายละเอียด` |
| warning | `สร้างรอบได้เฉพาะหลักสูตรที่เผยแพร่` |
| success | `สร้างหลักสูตรแล้ว` |
| warning | `สิทธิ์อ่านอย่างเดียว` |
| info | `ส่ง Expense Claim ไปแล้ว` |
| success | `ส่งอนุมัติแล้ว — รอผู้อนุมัติ (DOA)` |
| info | `ส่งออกรายงาน (CSV) — ต่อ dev` |
| warning | `ส่งได้หลังการลงทะเบียนได้รับอนุมัติ` |
| info | `ส่งไปยัง Expense Claim (hook) แล้ว — ไม่จ่าย/ไม่ post` |
| success | `อนุมัติขั้นนี้แล้ว` |
| success | `อนุมัติและยืนยันลงทะเบียนแล้ว` |
| success | `ออกใบรับรอง (soft ref) แล้ว` |
| warning | `ออกใบรับรองได้เฉพาะผู้ผ่านการอบรม` |
| warning | `เฉพาะผู้อนุมัติ (DOA) เท่านั้น` |
| warning | `เช็คชื่อได้หลังปิดรอบอบรม` |
| warning | `เช็คชื่อได้เฉพาะผู้เรียนที่ยืนยันลงทะเบียน` |
| success | `เปิดรับสมัครแล้ว` |
| success | `เผยแพร่หลักสูตรแล้ว` |
| info | `เลือกผู้เรียนจาก gap แล้ว` |
| info | `แจ้งเตือน (NTF):` *(prefix ของ `ntf()` · ต่อด้วยข้อความ event เช่น "ยืนยันลงทะเบียน {ชื่อ}")* |
| info | `ไม่อนุมัติแล้ว` |
| warning | `— feature ข้างเคียงของ module (นอก scope รอบนี้)` *(suffix ของ `ctxStub()` · นำหน้าด้วยชื่อ feature)* |

> **หมายเหตุ verbatim:** curly quote `“ ”` ใน "สร้างรอบอบรมแล้ว (ร่าง)" ต้องคงไว้ · em-dash `—` ทุกตัวคงตามต้นฉบับ

### Empty states (4 · `emptyStateHTML`)
| จอ | title | desc |
|---|---|---|
| หลักสูตร | `ไม่พบหลักสูตร` | ลองปรับคำค้นหรือล้างตัวกรอง แล้วลองอีกครั้ง (+ปุ่ม ล้างตัวกรอง) |
| รอบอบรม | `ไม่พบรอบอบรม` | ลองปรับคำค้น/ตัวกรอง หรือสร้างรอบอบรมใหม่ (+ปุ่ม สร้างรอบอบรม) |
| ผล | `ไม่พบรายการลงทะเบียน` | ลองปรับคำค้น/ตัวกรอง — บันทึกผลได้เมื่อผู้เรียนยืนยันลงทะเบียนแล้ว |
| ประวัติอบรม | `ยังไม่มีประวัติอบรม` | พนักงานคนนี้ยังไม่มีการลงทะเบียนอบรมในระบบ |

### ปุ่มหลัก (verbatim · `<span>…</span>`)
`สร้างหลักสูตร` · `สร้างรอบอบรม` · `Export CSV` · `เผยแพร่` (form: `เผยแพร่หลักสูตร`) · `บันทึกร่าง` · `แก้ไข` · `บันทึกการแก้ไข` · `ปิดหลักสูตร` · `เปิดรับสมัคร` · `ปิดรอบ` · `ลงทะเบียนผู้เรียน` (เต็ม → `จำนวนเต็มแล้ว`) · `บันทึกผล` · `บันทึก + ประกาศผล` · `ออกใบรับรอง` · `อนุมัติ` · `ส่ง Expense Claim (มูลค่า EC)` · `ส่งอนุมัติ` · `ยกเลิก` · `ล้างตัวกรอง`
Enroll modal footer: has_cost → `ลงทะเบียน + ส่งอนุมัติ` · ฟรี → `ลงทะเบียน (ยืนยัน)`

### Note/banner สำคัญ (action-context · verbatim ย่อ)
- capacity เต็ม: `จำนวนรับเต็มแล้ว (n/capacity) — ลงทะเบียนเพิ่มไม่ได้จนกว่าจะมีการยกเลิก`
- disabled tooltip: `บันทึกผลได้หลังปิดรอบ` · `ต้องเช็คชื่อเข้าอบรมก่อน (แท็บผู้เรียน)`
- EC: `ค่าอบรม → ส่ง Expense Claim (hook · display-only) — ไม่จ่ายเงินจริง / ไม่ลงบัญชีในหน้านี้`
- Rate Card: `อ้างอิง Rate Card · เชื่อมเมื่อ Rate Card พร้อม` (display-only · ไม่ hardcode)

---

## §10 · Data Binding & BACKEND Anchors

**Mock structures (แทน API จริง):** `DB.courses`/`sessions`/`enrolls` (บรรทัด 2209) · `EMPLOYEES` (2155) · `CATEGORIES` (2170) · `GAPS` (2180) · `doaResolve()` (2190)

| UI action | fn | API (FRD 02_API) | หมายเหตุ plug |
|---|---|---|---|
| list หลักสูตร / filter | `renderCourseTab` | API-01 GET /training/courses | client filter → server filter |
| ดูหลักสูตร | `openCourseView` | API-03 GET /courses/:id | |
| สร้าง/เผยแพร่/แก้ | `submitCourse` | API-02 POST · API-05 publish · API-04 PUT | Idempotency-Key |
| ปิดหลักสูตร | `courseClose` | API-06 close | confirm ที่ UI |
| list รอบ | `renderPlanTab` | API-07 GET /sessions | |
| สร้าง/แก้รอบ | `submitSession` | API-08 POST (guard published BR-11) · API-10 PUT | |
| เปิดรับ / ปิดรอบ | `sessionOpen`/`sessionClose` | API-11 open (→NTF) · API-12 close | |
| ลงทะเบียน | `submitEnroll` | API-14 (has_cost gate) | ฟรี→confirmed+NTF · has_cost→pending_doa→เปิด DOA modal |
| gap picker | `pickGap` / `gapsForCourse` | API-25 GET /performance/gaps (read-only hook) | ไม่สร้าง gap เอง |
| ส่งอนุมัติ | `submitDoa` | API-15 submit-approval | slot ไม่ hardcode · สายจาก F-DLG-001 |
| อนุมัติ/ไม่อนุมัติ | `enrollApprove`/`enrollReject` | API-16 approve · API-17 reject (reason req) | re-check canApprove ที่ mutation |
| ยกเลิกลงทะเบียน | `cancelEnroll` | API-18 cancel (soft archive) | OQ-06: expense_sent → ไม่ auto-reverse |
| เช็คชื่อ | `setAttendance` | API-19 attendance (รอบ closed) | |
| บันทึกผล+ประเมิน | `submitResult` | API-20 result (→NTF) | closed+attended gate |
| ออกใบรับรอง | `issueCert` | API-21 certificate (soft ref) | ไม่มีเลขรัน/PDF |
| ส่ง Expense | `sendExpense` | API-22 expense (hook display-only) | expense_sent กันซ้ำ |
| รายงาน | `renderReportTab` | API-23 GET /report (mask money) | |
| ประวัติรายคน | `openEmpHistory`/`empHistoryHTML` | API-27 GET /employees/:id/history | ชม.สะสมเฉพาะ passed |
| EC/Rate Card | ec-ref card (display-only) | **API-28 PENDING (F060)** | ห้าม hardcode — render "เชื่อมเมื่อพร้อม" |

**Notification (3 จุด · `ntf()` → wire `ENG-NOTIFY` ตอน dev):**
1. `train_session_opened` — เปิดรับรอบ (API-11)
2. `train_enroll_confirmed` — ยืนยันลงทะเบียน (API-14 ฟรี / API-16 ครบ DOA)
3. `train_result` — บันทึกผล (API-20)
> `doa_pending`/`doa_result` มาจาก DOA engine อัตโนมัติ — ห้ามประกาศซ้ำในฟีเจอร์

**Cross-module hooks:** Expense Claim (F101 · `training.expense_hook` display-only) · CSQ `train.enrolled_paid` (EC · confirmed has_cost) · DOA F-DLG-001 (resolve chain) · Rate Card F060 (pending)

---

## §11 · Traceability + Drift Log

### Brief ↔ FRD ↔ HTML
| Brief § | FRD (P-xx / API / BR) | HTML anchor |
|---|---|---|
| §2 Routes | 01_UI §1.0 (route `#/train/<tab>`) | `getRoute` 1666 · `render` 2307 |
| §4 P-01 หลักสูตร | P-01 · API-01/02/03 | `renderCourseTab` 2359 |
| §4 P-02 แผน | P-02 · API-07/08 · approvalHook | `renderPlanTab` 2392 |
| §4 P-03 ผล | P-03 · API-20/21 · action cell | `renderResultTab` 2426 |
| §4 P-04 รายงาน | P-04 · API-23 · BR-16 | `renderReportTab` 2466 |
| §6 P-05/06 course drawer | P-05/P-06 · API-02/04/05/06 · BR-01/BR-11 | `courseFormDrawer` 2533 · `courseViewDrawer` 2581 |
| §6 P-07/08 session drawer | P-07/P-08 · API-08/10/11/12 · BR-11 | `sessionFormDrawer` 2623 · `sessionViewDrawer` 2668 |
| §6 P-09 enroll | P-09 · API-14 · BR-02/03/04/10 | `renderModal t==='enroll'` 2902 |
| §6 P-10 DOA | P-10 · API-15 · BR-14 | `t==='doa'` 2930 · `submitDoa` 2941 |
| §6 P-11 result | P-11 · API-20 · BR-05/05b | `t==='result'` 2914 · `submitResult` 2786 |
| §6 P-12 emp history | P-12 · API-27 · BR-15 | `empHistoryHTML` 2859 |
| §8 State matrix | 05_RULES §5.2 state machines | `COURSE/SESSION/ENROLL_STATUS` 2198-2200 |
| §8 Permission/mask | 05_RULES §5.3 · FN-94 · BR-08 | `PERSONAS` 2148 · `maskMoney` 2283 · `viewerRO` 2295 |
| §10 EC/Rate Card | API-22/28 · BR-06/17 · OQ-03 | `sendExpense` 2837 · ec-ref card |

### ⚠️ Drift Log (HTML ↔ FRD)
| # | ประเภท | รายการ | ประเมิน | สถานะ |
|---|---|---|---|---|
| D-01 | HTML-only | Demo strip persona switch (hr/manager/viewer · `.demo-strip`) | Prototype scaffolding (Iron Rule #105) — ไม่ใช่ feature จริง · FRD ระบุ persona เป็น role matrix ถูกต้อง | **non-blocking** ✅ |
| D-02 | HTML-only | Bell icon → toast `ศูนย์แจ้งเตือน (ENG-NOTIFY) — เชื่อมจริงตอน dev` | stub ของ shell · จริงต่อด้วย Notification Center | **non-blocking** ✅ |
| D-03 | HTML-only | Sidebar sibling `ctxStub` (ประเมินผลงาน/เบิกค่าใช้จ่าย/ตั้งค่า HR) | placeholder feature ข้างเคียง module · นอก scope · FRD ไม่ต้องมี | **non-blocking** ✅ |
| D-04 | ตรงกัน (note) | Rate Card / มูลค่า EC = display-only "เชื่อมเมื่อพร้อม" | HTML + FRD API-28/BR-17 ตรงกัน (pending F060 · OQ-03) — ห้าม hardcode | **ตรง** ✅ |
| D-05 | ตรงกัน (note) | DOA slot ไม่ hardcode สาย · reject ต้องระบุเหตุผล | ตรง BR-14/BR-18 · แต่ role-id ปลายทาง + drift `role-hr-ld-head` vs `role-hr-dev-head` = **OQ-04** (BA เคาะ) | **non-blocking** (OQ ค้าง) |

> **ไม่พบ business-blocking drift** · HTML สกัดจาก FRD เดียวกัน (12 จอตรง) · verdict qc = PASS

---

## §12 · Diff จากเวอร์ชันก่อน
— ไม่มี (ไม่ได้รับ HTML เวอร์ชันเก่ามา diff)

---

## §13 · 💡 ข้อเสนอ (ไม่ใช่ AS-BUILT · R1 · คิดเพิ่ม)

> ต่อไปนี้ **ไม่มีใน HTML** — เสนอให้ dev/BA พิจารณา ห้ามถือเป็นสเปค
1. **Export CSV จริง** (ปัจจุบัน toast "ต่อ dev") — ต้อง mask money ตาม role (§10.2 PM edge · EC-08)
2. **Rate Card wiring** (API-28 pending F060) — เมื่อ F060 dev เสร็จ → เปลี่ยน ec-ref card จาก display-only เป็นค่าจริง
3. **OQ ค้างให้ BA/SEC เคาะ:** OQ-03 (Rate Card) · OQ-04 (DOA role-id + drift role name) · OQ-05 (หัวหน้า "สร้างได้" หรือ "อนุมัติอย่างเดียว") · OQ-06 (reverse EC เมื่อ cancel หลังส่ง)
4. **Loading/error state จริง** — mock ไม่มี network state · production ต้องมี skeleton/retry (FRD §1.6 ระบุ API 403/500)

---
*Generated by html-ui-brief v1.0 · Extraction-based · source: อบรม.html (3029 บรรทัด)*
