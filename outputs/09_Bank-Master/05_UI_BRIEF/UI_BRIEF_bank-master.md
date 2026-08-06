# HTML UI Brief — ธนาคาร / บัญชีบริษัท (F-BNK Bank Master)

> **EXTRACTION-BASED (Iron Rule R1):** ทุกบรรทัดในบรีฟนี้ trace กลับหา selector / function / ข้อความจริงใน `BankMaster.html` ได้ · ไม่มีการแต่งสเปคเพิ่ม · ข้อเสนอที่ไม่ใช่ AS-BUILT ถูกแยกไว้ท้ายไฟล์ (§13) เท่านั้น
> **HTML = SOURCE OF TRUTH.** ตัวเลขบรรทัด (`L####`) อ้างอิงไฟล์ต้นทางเวอร์ชันปัจจุบัน (2970 บรรทัด)

---

## §0 · Document Control + Pairing

| ฟิลด์ | ค่า |
|---|---|
| Feature | **F-BNK — Bank Master** (ธนาคาร / บัญชีบริษัท) |
| HTML source of truth | `outputs/09_Bank-Master/01_HTML/BankMaster.html` · 2970 บรรทัด · single-file SPA |
| `<title>` | `ธนาคาร / บัญชีบริษัท · CUBE NATIVE` (L6) |
| Base-kit | BASE-KIT v6.4 (comment L22) + page-specific CSS หลัง `END BASE-KIT` marker (L1318) |
| CI theme | **CUBE CI Warm Light rebrand v2.0** (comment L23) — Ivory/Charcoal + Red `#FF3B30` / Orange `#FF9A1F` |
| Version stamp | `Sandbox · v1.0.0` (sidebar footer L1468) · PREFLIGHT stamp: date 2026-08-04, QC-round2 2026-08-05 (L2966) |
| FRD Pack | `outputs/09_Bank-Master/04_FRD/FRD_F-BNK_Pack/` (9 ไฟล์) — paired (see §11) |
| Context | `00_CONTEXT/DECISION_LOG.md` |
| Persistence | **In-memory เท่านั้น** — comment L1987 "in-memory, no storage"; ไม่มี localStorage/fetch ในไฟล์ |
| Drift status | 2 FRD Section-M drifts ถูก resolve ไปทาง HTML แล้ว (audit action naming, tab label) — ดู §11 Drift Log |

**Bug fixes ที่อยู่ในไฟล์นี้ (verbatim จาก code comments):**
| Tag | จุดแก้ | Anchor |
|---|---|---|
| Bug A | drawer `is-open` preserve ข้าม re-render (`renderDrawerEl` เก็บ `wasOpen`) | L2370 |
| Bug B | toast `pointer-events:none` — informational toast ต้องไม่บังปุ่ม submit ใน drawer | L1155 |
| Bug C | `.modal-backdrop z-index:var(--z-modal)` = 60 อยู่ **เหนือ** drawer (51) — เดิม 50 อยู่ใต้ drawer ทำให้ปุ่มใน modal ใน drawer กดไม่ได้ | L1067 |
| I-06 | render-after-close: `setTimeout(render, 300)` refresh list หลัง drawer ปิด (state reset ที่ 280ms) | L2544, L2880 |
| W1 | delete guard: ห้าม hard-delete ธนาคารที่ยังมีบัญชีอ้างอิง (`used>0`) | L2335, L2355 |

---

## §1 · Design Tokens AS-BUILT

### 1.1 CSS Variables (`:root` L24–L60)
**Colors**
| Token | Value | หมายเหตุ |
|---|---|---|
| `--c-navy` / `--c-navy-2` | `#111111` | ink / charcoal |
| `--c-primary` | `#FF3B30` | brand red (CTA) |
| `--c-primary-hover` | `#E62E24` | |
| `--c-teal` | `#FF9A1F` | brand orange (accent — ชื่อ token คือ teal แต่ค่าเป็นส้ม) |
| `--c-teal-light` | `#FFB763` | |
| `--c-ink` | `#111111` | ตัวอักษรหลัก |
| `--c-mute` / `--c-mute-2` / `--c-mute-3` | `#54565C` / `#73757B` / `#9A9CA2` | ลำดับสีจาง |
| `--c-line` / `--c-line-2` / `--c-line-3` | `#DEDAD4` / `#E9E5E0` / `#F1EEEA` | เส้น/ขอบ |
| `--c-bg-off` | `#FAF8F5` | พื้นหลัง (ivory) |
| `--c-success` | `#1F9D55` | |
| `--c-warning` | `#E8870F` | |
| `--c-danger` | `#E62E24` | |

**Layout / Type / Space / Radius**
| Token | Value |
|---|---|
| `--sidebar-w` | `232px` |
| `--shell-h` | `52px` |
| type scale | `--fs-h1:22 · --fs-h2:17 · --fs-h3:15 · --fs-body:14 · --fs-sub:13 · --fs-meta:12 · --fs-cap:11 · --fs-kpi:28` (px) |
| spacing | `--sp-xs:4 · --sp-sm:8 · --sp-md:12 · --sp-lg:20 · --sp-xl:28` (px) |
| radius | `--r-xs:4 · --r-sm:6 · --r-md:8 · --r-lg:12 · --r-full:999` (px) |

### 1.2 Fonts
- Stack (body L82): `'Satoshi','Noto Sans Thai', system-ui, sans-serif` · base 14px / line-height 1.5
- Headings ไทย (`.ph-title`, `.stat-value`, `.drawer-title`, `.modal-title`, `.empty-title`) บังคับ `'Noto Sans Thai'`
- แหล่ง: Google Fonts (Noto Sans Thai 400–800, L11) + Fontshare (Satoshi 300–900, L12) — **โหลดผ่าน CDN**

### 1.3 Radius / Shadow / Scrollbar
- Scrollbar (Iron Rule #49, L69–80): thin 5px, thumb `rgba(17,17,17,.14)`; บนพื้นเข้ม (`.sidebar`,`.slide`) เป็นขาวโปร่ง
- `html { scrollbar-gutter: stable; }` (L67, Rule #35 layout stability) · `body { min-width:1180px; }` (L89 — admin tool บังคับ horizontal scroll จอแคบ)
- Shadow เด่น: drawer `-16px 0 40px rgba(17,17,17,.18)` (L854) · modal `0 24px 64px rgba(17,17,17,.28)` (L1086) · toast `0 12px 32px rgba(17,17,17,.30)` (L1169)

### 1.4 z-index Map (เรียงสูง→ต่ำ) — declared `:root` L26–27
| ระดับ | Token | ค่า | ใช้กับ |
|---|---|---|---|
| สูงสุด | `--z-toast` | **80** | `.toast` (L1165) |
| | `--z-modal` | **60** | `.modal-backdrop` (L1067) — **Bug C**: ต้องอยู่เหนือ drawer |
| | `--z-drawer` | **51** | `.drawer` (L849) |
| | `--z-backdrop` | **50** | `.drawer-backdrop` (L837) **และ** `.ss-list` combobox popover (L542) |
| | `--z-dropdown` | **30** | `.user-menu` (L316), `.info-tip::after` tooltip (L1313) |
| | `--z-shell` | **20** | `.sidebar` (L107) |
| ต่ำสุด | `--z-sticky` | **10** | `.shell-bar` (L244), `.wizard-footer` (L1220) |

> **สำคัญ (Bug C):** modal (60) นั่งเหนือ drawer (51) โดยเจตนา — เพราะ archive/deactivate/doc-picker modal ถูกเปิดได้จากภายใน view/edit drawer; ถ้า modal อยู่ใต้ drawer ปุ่มยืนยัน/ยกเลิกจะคลิกไม่ได้ (comment verbatim L1067). Combobox popover `.ss-list` ใช้ `--z-backdrop`(50) — ต่ำกว่า drawer(51) แต่ render **ภายใน** drawer body จึงเห็นได้ปกติ (stacking context ของ drawer).

---

## §2 · Route Map

| Route | ที่มา | Refresh-safe? |
|---|---|---|
| `#/` หรือ `#` (ว่าง) | `getRoute()` → `'home'` (L1607–1611) | ✅ |
| `#/bank-master` | hash route เดียวของ feature; `state.currentRoute='bank-master'` (L1991) | ✅ hash-based |

- **Router:** hash-based, `getRoute()`/`navigate()` (L1607–1614); `window.addEventListener('hashchange', render)` (L1936, late-binding เพื่อชี้ `render()` ตัวที่ feature override)
- **Feature มี route เดียว** — ไม่มี sub-route ต่อ tab. 2 แท็บ (`accounts` / `banks`) สลับด้วย **in-memory `state.tab`** (L1993) ผ่าน `setTab()` (L2152) → `render()` เท่านั้น (ไม่แตะ hash → refresh คืนสู่ `accounts` เสมอ)
- **Company selection** = in-memory `state.currentCompany` (default `'C1'`, L1992) ผ่าน `changeCompany()` (L2153) — ล้าง filter ทุกครั้งที่สลับบริษัท
- Boot: รอ `domReady && lucideReady` ก่อน first `render()` (`bootIfReady()` L1943–1968) + safety net 5s ถ้า lucide ไม่โหลด (L1962)

---

## §3 · Layout Shell

| ส่วน | selector | ขนาด/ค่าจริง |
|---|---|---|
| Sidebar | `.sidebar` (fixed, L101) | width `--sidebar-w`=232px · พื้น `#111111` · z=20 |
| Brand | `.sb-brand` / `.sb-logo` (L112,120) | logo 34×34 gradient red→orange · ชื่อ `CUBE NATIVE` / sub `Finance` (L1409–1410) |
| Nav module (collapsible, Rule #27) | `.sb-module[data-expanded]` (L138,160) | header กด toggle เท่านั้น (ไม่ navigable) ผ่าน `toggleModule()` (L1597) |
| Main | `.main` (L228) | `margin-left:232px` |
| Shell bar | `.shell-bar` (sticky top, L235) | height `--shell-h`=52px · z=10 · breadcrumb + notif + user chip |
| Content host | `#page-content` (L1505) | `.content` padding 24px · rendered โดย `render()` |

**Sidebar nav (L1413–1465):**
- Module **การเงิน** (`finance`, `data-expanded="true"`): `ธนาคาร / บัญชีบริษัท` (`is-active`, `data-feature="bank-master"`), + `ใบสำคัญจ่าย` · `ใบสำคัญรับ` · `กระทบยอดธนาคาร` — ทั้งหมด `is-disabled`
- Module **บัญชี** (`accounting`, collapsed): `ผังบัญชี` (disabled)
- Module **System** (collapsed): `ตั้งค่า` (disabled)
- Footer: `.pulse-dot` + `Sandbox · v1.0.0`

**Shell bar (L1474–1503):**
- Breadcrumb: `การเงิน` › `ธนาคาร / บัญชีบริษัท` (current)
- Notif icon-btn `bell` + `.notif-dot` → `toggleNotif()` → toast `ยังไม่มีการแจ้งเตือนใหม่` (L1516)
- User chip: `ศศิธร บุญมี` / `Finance Admin · 2BSimple` / avatar `ศบ` → `toggleUserMenu()` (L1510). Dropdown `.user-menu` (L1495): `โปรไฟล์ของฉัน` · `ตั้งค่า` · (divider) · `ออกจากระบบ` (is-danger) — เป็น mock (ไม่มี handler ต่อ item)

---

## §4 · Page Anatomy (ต่อหน้า/แท็บ)

Render tree: `render()` (L2102) → `renderPage()` (L2112) = `headerHTML()` + `tabsHTML()` + (`accountsTabHTML()` | `banksTabHTML()`).
`render()` ห่อด้วย `preserveRenderState()`/`restoreRenderState()` (Rule #29) เพื่อคง scroll+focus ข้าม innerHTML rebuild.

### 4.1 Page Header — `headerHTML()` (L2116)
- `.ph-title` = `ธนาคาร / บัญชีบริษัท` (คงที่ทั้ง 2 แท็บ)
- `.ph-sub` เปลี่ยนตามแท็บ:
  - accounts: `จัดการบัญชีธนาคารของบริษัท ผูกบัญชีแยกประเภท (GL) และตั้งค่าบัญชีจ่าย/รับเริ่มต้น`
  - banks: `รายชื่อธนาคารมาตรฐาน (อ้างอิงรหัส ธปท.) — สร้างธนาคารต่างประเทศพร้อมรหัส SWIFT ได้`
- `.ph-actions` เปลี่ยนตามแท็บ:
  - accounts: `[จำลองเลือกในเอกสาร]` (secondary, `openDocPicker()`) + `[สร้างบัญชี]` (primary, `openCreate()`)
  - banks: `[สร้างธนาคาร]` (primary, `openBankCreate()`)

### 4.2 Tabs — `tabsHTML()` (L2136)
- `.ptabs` 2 ปุ่ม: `บัญชีบริษัท` (icon `building-2`, count = `accounts.length`) · `ธนาคาร` (icon `landmark`, count = `banks.length`)
- active = `.ptab.is-active` (border-bottom primary). สลับผ่าน `setTab()` (L2152)

### 4.3 Tab A — บัญชีบริษัท (`accountsTabHTML()` L2158)
Region tree:
1. **Company bar** `.co-bar` (L2173) — label `บริษัท` + `<select>` (companies) → `changeCompany()`. `.co-meta` (ชิดขวา): `เลขผู้เสียภาษี <b>{taxId}</b>` · `บัญชีจ่ายเริ่มต้น <b>{abbr+mask | ยังไม่ตั้ง}</b>` · `บัญชีรับเริ่มต้น <b>…</b>`
2. **Stats** `.stats` 4 การ์ด (L2186): `บัญชีทั้งหมด` (all.length / `ในบริษัทนี้`) · `ใช้งานอยู่` (active.length / `พร้อมใช้ในเอกสาร`) · `บัญชีจ่ายเริ่มต้น` (abbr หรือ `—` / `{type}·{mask}` หรือ `ยังไม่ได้ตั้งค่า`) · `บัญชีรับเริ่มต้น` (เหมือนกัน). ค่า abbr ใช้ class `.stat-value.is-abbr` (20px, L2945)
3. **Card** `.card` = filter-bar + body:
   - **Filter bar** `.filter-bar` (L2194): search input (`ค้นหาธนาคาร / ชื่อบัญชี / เลขบัญชี`, `onSearch()`) + status `<select>` (`ทุกสถานะ/ใช้งาน/ปิดใช้งาน/เก็บถาวร`, `onStatusFilter()`, class `.filter-status` max 180px) + `[ล้างตัวกรอง]` ghost (`resetFilters()`, `.filter-reset` margin-left auto)
   - **Table** `.table` (L2222): คอลัมน์ `ธนาคาร · ชื่อบัญชี · เลขบัญชี · ประเภท · บัญชี GL · ค่าเริ่มต้น · สถานะ · จัดการ(ชิดขวา)`. rows = `rowHTML()` (L2239)
   - **Footer** `.table-footer` (L2230): `แสดง {n} จาก {all} รายการ` · ชื่อบริษัท
   - **Empty** (rows=0): `emptyStateHTML()` — ต่างกันตามว่ามี filter หรือไม่ (ดู §9)

**Row (`rowHTML()` L2239):** `<tr class="is-clickable" onclick="openView(id)">` (Rule #41 — คลิกแถวเปิด view, ไม่มีไอคอนดวงตา)
- เลขบัญชี cell = masked/revealed toggle (ดู §4.6 security)
- `ค่าเริ่มต้น` = `.dflags`: `จ่าย` (dflag-pay, arrow-up-right) / `รับ` (dflag-rcv, arrow-down-left) / `—` (dflag-none)
- `สถานะ` = pill (`statusMeta()` L2076)
- `จัดการ` (stopPropagation) = `.row-actions`: `[แก้ไข]` (pencil, `openEdit`) + `[เก็บถาวร]` (archive, is-danger, `openArchive`) — ปุ่มเก็บถาวรซ่อนถ้า `status==='archived'`

### 4.4 Tab B — ธนาคาร (`banksTabHTML()` L2286)
1. **Card** = filter-bar (search `ค้นหาธนาคาร / SWIFT / รหัส`, `onBankSearch()`) + table + audit section
2. **Table** (L2299): คอลัมน์ `รหัส ธปท. · ธนาคาร · ชื่อย่อ · SWIFT / BIC · ประเภท · บัญชีที่ใช้ · จัดการ`. rows = `bankRowHTML()` (L2326)
   - Footer: `{n} จาก {banks.length} ธนาคาร` · `อ้างอิงรหัสสถาบันการเงิน ธปท.`
3. **Bank audit section** `.bank-audit-sec` (`bankAuditSectionHTML()` L2312): title `ประวัติการเปลี่ยนแปลงรายชื่อธนาคาร`; แสดงเฉพาะ log ที่มี `bankCode` (append-only bank-preset scope); empty = `ยังไม่มีการสร้างหรือลบธนาคารที่สร้างเอง`

**Bank row (`bankRowHTML()` L2326):** `<tr class="is-clickable" onclick="openBankView(code)">`
- `ประเภท`: pill `ต่างประเทศ` (pill-warning) / `ในประเทศ` (pill-info)
- `บัญชีที่ใช้`: `{n} บัญชี` หรือ `—`
- `จัดการ`:
  - **preset (ธปท.)** = read-only `<span>มาตรฐาน</span>` (mute-3, L2339)
  - **custom** (`b.custom`) = `[แก้ไขธนาคาร]` (pencil, `openBankEdit`) + delete: ถ้า `used>0` → ปุ่ม `is-disabled` disabled title `มี {used} บัญชีอ้างอิงธนาคารนี้ — ลบไม่ได้` (W1); ถ้า `used===0` → `[ลบธนาคารที่สร้างเอง]` (trash-2, is-danger, `removeBank`)

### 4.5 Overlays anatomy (สรุป — รายละเอียด §5/§6)
- **Account create/edit drawer** — `accountFormHTML()` (L2398)
- **Account view drawer** (tabbed) — `accountViewHTML()` (L2559)
- **Bank create/edit drawer** — `bankFormHTML()` (L2792)
- **Bank view drawer** — `bankViewHTML()` (L2888)
- **Archive modal** — `archiveModalHTML()` (L2687)
- **Deactivate modal** — `deactivateModalHTML()` (L2718)
- **Doc-picker modal (mock)** — `docPickerHTML()` (L2745)

### 4.6 🔒 Account-number masking / reveal (security-critical)
> ดูสถานะละเอียดใน §8.3. สรุปกลไก:
- **Masking** `maskAccNo()` (L2075): ถ้า `len<=4` คืนเลขเต็ม; ไม่งั้น `'•'×(len-4) + 4 หลักท้าย`. ใช้ทุกที่ที่แสดงเลขบัญชีเป็น default (table row, stats, drawer subtitle, modal subtitle, doc-picker, toast)
- **Reveal** `revealAccNo(id)` (L2273): เช็ค `currentUser.canRevealFull` — ถ้าไม่มีสิทธิ์ → toast `คุณไม่มีสิทธิ์ดูเลขบัญชีเต็ม` (warning) และหยุด; ถ้ามีสิทธิ์ → `state.revealed.add(id)`, `pushAudit(id,'revealed', 'เปิดดูเลขบัญชีเต็ม '+abbr)`, render, toast `บันทึกการเข้าถึงเลขบัญชีเต็มแล้ว` (info)
- **Hide** `hideAccNo(id)` (L2281): `state.revealed.delete(id)` + render (ไม่ลง audit)
- `state.revealed` = `Set` (L1994) — per-session, ถูก reset ใน `openCreate()` (L2512)
- `currentUser = { name:'ศศิธร บุญมี', canRevealFull:true }` (L1998) — permission gate ตรงนี้ (BACKEND anchor: ต่อ RBAC จริง)

---

## §5 · Component Inventory (anchor + states)

> States: default / hover / focus / active / disabled / empty / loading / error — เขียน "—" เมื่อไม่มีจริง

### 5.1 Buttons `.btn` (L382)
| variant | selector | hover | disabled |
|---|---|---|---|
| primary | `.btn-primary` | bg→`--c-primary-hover` + shadow | `.is-disabled`/`:disabled` opacity .55, pointer-events none (L405) |
| secondary | `.btn-secondary` | bg line-3 | ↑ |
| ghost | `.btn-ghost` | bg line-3 | ↑ |
| danger | `.btn-danger` (ขาว/แดง) | bg `#FFE9E7` | ↑ |
| link | `.btn-link` | underline | — |
| sm | `.btn-sm` (30px) | — | — |
- height 36px, radius 8px, padding-top 2px (Thai optical centering Rule #36) · icon 15px
- **Loading state:** submit ปุ่มเปลี่ยนเป็น `<i loader-2 spin>` + `กำลังบันทึก…` แล้ว add `.is-disabled` (`submitAccount` L2524 / `submitBank` L2862)

### 5.2 Search-select combobox `.search-select` (Iron Rule #34/#94, L522) — master lookup
- Markup: `searchSelectHTML(key,opt)` (L1727) · init: `initSearchSelect(key,cfg)` (L1740)
- ใช้ 2 จุด: `acc-bank` (ธนาคาร; options=banks map, icon landmark, right=abbr) + `acc-gl` (บัญชี GL; options=coa, icon book-open) — init ใน `renderDrawerEl()` (L2379)
- โครง: lead icon `search` + `<input>` + clear button `x` (`.ss-clear`, ซ่อนเมื่อไม่มีค่า) + caret `chevron-down` (ซ่อนเมื่อมีค่า) + popover `.ss-list` (absolute, z=50, max-h 280)
- States:
  - default: caret แสดง, clear ซ่อน (`ssSyncChrome` L1759)
  - focus/open: `ssOpen()` (L1792) — query ล้าง, list แสดง
  - typing: `ssOnInput()` (L1793) — filter + highlight `<mark>`, `value=null` จนกว่าจะเลือก
  - active option: `.ss-opt.is-active` (L553) + keyboard hi (`s.hi`)
  - selected: input โชว์ label, clear แสดง, caret ซ่อน
  - empty: `.ss-empty` = `emptyText` (`ไม่พบธนาคาร` / `ไม่พบบัญชี GL`, ค่า default `ไม่พบรายการ`)
  - keyboard: `ssOnKey()` (L1796) — ↓/↑ เลื่อน, Enter เลือก, **Esc ปิด popover + `stopPropagation`** (Esc chain — ดู §7)
  - click-outside: document listener (L1803) ปิด popover ทุกตัวที่ open
- error: field ห่อ `.field.is-invalid` (border danger) + `.field-error` (จาก `fieldErr()`)

### 5.3 Table `.table` (L564)
- thead `.table thead` bg off; th uppercase mute; `.is-sortable` (มี CSS แต่ **feature นี้ไม่ได้ประกาศ sortable/sort-arrow บนคอลัมน์ใด** — sort state ใน shared `state.sort` ไม่ถูกใช้)
- row hover bg off; `.is-clickable` cursor pointer (row เปิด view)
- `.is-selected` (มี CSS L594 แต่ feature นี้ไม่มี checkbox/bulk — `state.selectedIds` ไม่ถูกใช้)
- truncation `.cell-truncate` (มีใน kit; ไม่ถูกใช้ในแท็บนี้)

### 5.4 Pills (status/type/flags)
| ใช้กับ | class | label |
|---|---|---|
| status active | `pill-info` | `ใช้งาน` (`statusMeta` L2077) |
| status inactive | `pill-muted` | `ปิดใช้งาน` |
| status archived | `pill-muted` | `เก็บถาวร` |
| bank type foreign | `pill-warning` | `ต่างประเทศ` |
| bank type local | `pill-info` | `ในประเทศ` |
| default-pay flag | `.dflag.dflag-pay` | `จ่าย` (arrow-up-right, สีส้ม #B8690B) |
| default-rcv flag | `.dflag.dflag-rcv` | `รับ` (arrow-down-left, สีเขียว #157A41) |
| no flag | `.dflag-none` | `—` |

### 5.5 Toggle switch `.toggle` (L1370)
- 42×24 pill; `.is-on` → bg primary + slider translateX(18px)
- ใช้ 2 บริบท:
  - **form** (create/edit): `toggleFormDefault(field)` (L2499) — sync DOM ก่อน flip แล้ว render
  - **view drawer default tab**: `toggleDefault(id,field)` (L2654) — เช็ค `status==='active'` ก่อน (ถ้าไม่ → toast warning หยุด), flip + enforce unique + audit + toast

### 5.6 Definition grid `.def-grid` (L1360) — 150px/1fr; ใช้ใน account view detail tab + bank view
### 5.7 Audit list `.audit-item` (L1379); reveal item = `.audit-ic.is-reveal` (พื้นแดงจาง). icon map `AUDIT_META` (L2086)
### 5.8 Notes `.note` (L1396): `.is-info` (ฟ้า) / `.is-warn` (ส้ม) — ใช้ใน modal + view drawer + doc-picker
### 5.9 Stats card `.stat` (L430); KPI value `.stat-value` 26px (Noto Sans Thai)
### 5.10 Info tooltip `.info-tip` (L1309, Rule #33/#67) — hover แสดง `data-tip`; ใช้ที่ field สกุลเงิน + SWIFT
### 5.11 Empty-hint `.empty-hint` (L2946) — inline empty ใน audit/doc-picker (ต่างจาก full `.empty`)

---

## §6 · Overlay Registry

| Overlay | selector / render fn | ขนาด | z | เปิด | ปิด (dismiss rules) |
|---|---|---|---|---|---|
| **Account create/edit drawer** | `#drawer` / `accountFormHTML()` | `.drawer.standard` = **680px** (L857), max 96vw | 51 | `openCreate()`/`openEdit()`→`openDrawer('create'/'edit')` | backdrop click (`closeDrawer`), ปุ่ม `ยกเลิก`, top X, **Esc** |
| **Account view drawer** | `#drawer` / `accountViewHTML()` | 680px | 51 | `openView(id)` | backdrop, `ปิด`, top X, Esc |
| **Bank create/edit drawer** | `#drawer` / `bankFormHTML()` | 680px | 51 | `openBankCreate()`/`openBankEdit(code)` | backdrop, `ยกเลิก`, top X, Esc |
| **Bank view drawer** | `#drawer` / `bankViewHTML()` | 680px | 51 | `openBankView(code)` | backdrop, `ปิด`, top X, Esc |
| **Archive modal** | `#modalBackdrop .modal` / `archiveModalHTML()` | `.modal` = **440px** (L1079), max 92vw | 60 | `openArchive(id)` | backdrop click, `ยกเลิก`, **Esc**; ยืนยัน = `confirmArchive()` |
| **Deactivate modal** | ↑ / `deactivateModalHTML()` | 440px | 60 | `openDeactivate(id)` | backdrop, `ยกเลิก`, Esc; ยืนยัน = `confirmDeactivate()` |
| **Doc-picker modal (mock)** | ↑ / `docPickerHTML()` | 440px | 60 | `openDocPicker()` | backdrop, `ปิด`, Esc |
| **Combobox popover** | `.ss-list` | absolute เต็ม width field | 50 | focus/typing ใน ss-input | Esc (popover ก่อน), click-outside, เลือก option |
| **User menu** | `.user-menu#userMenu` | 240px | 30 | `toggleUserMenu()` | click-outside (L1511); **ไม่ผูก Esc** |
| **Toast** | `.toast#toast` | max 380px, bottom-right | 80 | `showToast()` | auto-hide หลัง `durationMs` (default 2800); **pointer-events:none** (Bug B) |

**หมายเหตุ dismiss สำคัญ:**
- **ทุก drawer เดียวใช้ container เดียว** `#drawer` — render เปลี่ยนตาม `state.drawer.mode`. Drawer เป็น `.standard` (680px) ทุกโหมด (`renderDrawerEl` L2371) — ไม่มีการใช้ 920px wide ในฟีเจอร์นี้
- **backdrop drawer** `onclick="closeDrawer()"` (L1520); **backdrop modal** `onclick="closeModal()"` (L1526); `.modal` มี `onclick="event.stopPropagation()"` (L1527) กันปิดเมื่อคลิกในตัว modal
- **ไม่มี scroll-lock** ที่ body — อาศัย `scrollbar-gutter:stable` กัน jank
- Animation: drawer `transform translateX` 280ms (L851) via rAF add `.is-open`; modal `scale .96→1` 200ms (L1085); toast translateY 250ms
- Focus management: `restoreRenderState()` คืน focus/selection ให้ input ที่ตรง placeholder+type+name (L1910) — ไม่มี focus-trap ใน overlay

---

## §7 · Interaction Spec

### 7.1 Esc chain (ลำดับจริง)
มี **สอง** keydown listener สำหรับ Escape:
1. **Combobox-level** — `ssOnKey()` (L1796–1802): ถ้า popover `s.open` → `e.stopPropagation()` + `e.preventDefault()` + ปิด popover. **`stopPropagation` กันไม่ให้ Esc ทะลุไปปิด drawer** (นี่คือ Bug A / qc-ux Esc-chain fix — verified ใน PREFLIGHT L2961: "esc1 ปิด combobox drawer เปิดค้าง / esc2 ปิด drawer")
2. **Global** — `window keydown` (L1665–1670): `if(state.modal.open) closeModal(); else if(state.drawer.open) closeDrawer();`

**ลำดับ Esc:** (1) combobox popover เปิดอยู่ → Esc ปิด popover ก่อน (ไม่ถึง global) → (2) modal เปิด → Esc ปิด modal → (3) drawer เปิด → Esc ปิด drawer. Modal มาก่อน drawer เสมอ (เพราะ modal เปิดทับ drawer ได้)

### 7.2 Click-outside
- Combobox: document listener (L1803) — ปิด popover ทุก key ที่ open เมื่อคลิกนอก `#ss-{key}`
- User menu: document listener (L1511) — ปิดเมื่อคลิกนอก `.user-chip`/`.user-menu`
- Base-kit overlay: `[data-overlay]` listener (L1981) — feature นี้ไม่ได้ใช้ `data-overlay`
- Backdrop drawer/modal: onclick ปิด (ดู §6)

### 7.3 Render preservation (Rule #29)
- `render()` (L2102) snapshot `preserveRenderState()` → rebuild `#page-content` + drawer + modal → `restoreRenderState()`. คง: scrollTop ของ `.drawer-body`/`.modal-body`, window.scrollY, focus+selection ของ input/textarea (match ด้วย placeholder+type+name L1914)
- **Bug A fix** (L2370): `renderDrawerEl()` อ่าน `wasOpen = classList.contains('is-open')` แล้วคง `is-open` ตอน re-render — กัน drawer เด้งปิดเมื่อ `setViewTab`/`toggle`/`validate` เรียก render ระหว่างเปิด. First-open ยัง animate ผ่าน rAF ของ `openDrawer` (L1623)

### 7.4 Positioning
- Drawer: `position:fixed; top/right/bottom:0` slide จากขวา (L843)
- Modal: fixed inset:0 + flex center (L1063)
- Combobox popover: `position:absolute` (ไม่ดันเนื้อหา — สอดคล้อง Rule #35, L523)
- Toast: `position:fixed; bottom:24 right:24`
- ไม่มี drag / pan / zoom / resize ในฟีเจอร์นี้ (—)

### 7.5 Number/format helpers
`fmtDateTime()` (L1821) ใช้แสดง audit ts + `สร้างเมื่อ` (view footer). `fmtNumber/fmtMoney/fmtDate` มีใน kit แต่ฟีเจอร์นี้ไม่เรียก (ไม่มีการแสดงเงิน)

---

## §8 · State-Driven UI Matrix

### 8.1 Account status enum (`statusMeta()` L2076)
| status | pill class | label | ผลต่อ UI |
|---|---|---|---|
| `active` | `pill-info` | ใช้งาน | view footer แสดง `[ปิดใช้งาน]`; ตั้ง default ได้; อยู่ใน doc-picker |
| `inactive` | `pill-muted` | ปิดใช้งาน | view แสดง `[เปิดใช้งาน]`; ตั้ง default ไม่ได้ (note is-warn L2608); ไม่อยู่ใน doc-picker |
| `archived` | `pill-muted` | เก็บถาวร | ไม่มีปุ่ม toggle active; ปุ่มเก็บถาวรถูกซ่อน (row + view + header); default ถูกเคลียร์ |

**Transitions:**
- `activateAccount()` (L2666): →active, audit `activated`, toast `เปิดใช้งานบัญชีแล้ว` (success)
- `confirmDeactivate()` (L2735): →inactive, เคลียร์ defaultPay/Receive, audit `deactivated`, toast `ปิดใช้งานบัญชีแล้ว`
- `confirmArchive()` (L2707): →archived, เคลียร์ default, audit `archived`, ปิด drawer ถ้าเปิด, toast `เก็บถาวรบัญชีแล้ว`

### 8.2 Default account uniqueness (FN-02)
- `enforceDefaultUnique(rec)` (L2547) + `toggleDefault()` (L2654): ต่อบริษัท มี defaultPay/defaultReceive ได้ **1 บัญชี** — เลือกใหม่ล้างของเดิมทุกใบในบริษัทเดียวกัน
- Guard: `toggleDefault` ถ้า `status!=='active'` → toast `บัญชีต้องอยู่สถานะใช้งานก่อนตั้งเป็นค่าเริ่มต้น` (warning) แล้วหยุด

### 8.3 🔒 Masked ↔ Revealed (per row/view, `state.revealed`)
| state | cell (row `rowHTML` L2244) | view line (L2567) | ปุ่ม |
|---|---|---|---|
| **masked** (default) | `maskAccNo` + ปุ่ม `ดูเต็ม` (scan-line) title `ต้องมีสิทธิ์ · ระบบจะบันทึกการเข้าถึง` | `maskAccNo` + `ดูเต็ม` | `revealAccNo(id)` (stopPropagation ใน row) |
| **revealed** | เลขเต็ม + ปุ่ม `ซ่อน` (eye-off) | เลขเต็ม + `ซ่อน` | `hideAccNo(id)` |
| **no permission** | (คลิกดูเต็ม) → toast warning, ไม่เปลี่ยน | ↑ | gate `currentUser.canRevealFull` |
- reveal บันทึก audit `revealed` (ไอคอน scan-line, `.is-reveal`) — irreversible log (append-only)

### 8.4 Bank source enum (preset vs custom)
| source | จัดการ (row/view) | note ใน view |
|---|---|---|
| preset (ธปท., `!b.custom`) | read-only `มาตรฐาน` | `รายการมาตรฐาน ธปท. — เป็นข้อมูลอ้างอิงกลาง แก้ไข/ลบไม่ได้` (is-info) |
| custom (`b.custom`) & used=0 | แก้ไข + ลบ | — (footer meta: `ธนาคารที่สร้างเอง — แก้ไข/ลบได้…`) |
| custom & used>0 | แก้ไข + **ลบ disabled** (W1) | ปุ่มลบ disabled title `มี {used} บัญชีอ้างอิงธนาคารนี้ — ลบไม่ได้` |
- `openBankEdit` บน preset → toast `ธนาคารมาตรฐาน ธปท. แก้ไขไม่ได้` (warning, L2785)

### 8.5 Drawer mode enum (`state.drawer.mode`, `renderDrawerEl` L2372)
`create` | `edit` → `accountFormHTML` · `view` → `accountViewHTML` (tab: detail/default/audit) · `bank-create` | `bank-edit` → `bankFormHTML` · `bank-view` → `bankViewHTML`

### 8.6 View drawer tabs (`state.drawer.tab`, L2637)
`detail` (def-grid) · `default` (toggles + warn ถ้าไม่ active) · `audit` (count = logs.length; empty `ยังไม่มีประวัติ`)

---

## §9 · Microcopy (VERBATIM)

### 9.1 Buttons / actions
`สร้างบัญชี` · `สร้างธนาคาร` · `จำลองเลือกในเอกสาร` · `ล้างตัวกรอง` · `ยกเลิก` · `ยืนยันสร้าง` · `บันทึกการแก้ไข` · `กำลังบันทึก…` · `ปิด` · `แก้ไข` · `เก็บถาวร` · `ปิดใช้งาน` · `เปิดใช้งาน` · `ลบ` · `เลือก` · `ดูเต็ม` · `ซ่อน`

### 9.2 Toasts (ทุก `showToast` call)
| ข้อความ | variant | ที่มา |
|---|---|---|
| `ยังไม่มีการแจ้งเตือนใหม่` | info | `toggleNotif` L1516 |
| `คุณไม่มีสิทธิ์ดูเลขบัญชีเต็ม` | warning | `revealAccNo` L2275 |
| `บันทึกการเข้าถึงเลขบัญชีเต็มแล้ว` | info | `revealAccNo` L2279 |
| `กรุณากรอกข้อมูลให้ครบถ้วน` | warning | `submitAccount` L2522 / `submitBank` L2860 |
| `สร้างบัญชีธนาคารสำเร็จ` / `บันทึกการแก้ไขแล้ว` | success | `commitAccount` L2543 |
| `ตั้งเป็นบัญชี{จ่าย/รับ}เริ่มต้นแล้ว` / `ยกเลิกค่าเริ่มต้นแล้ว` | info | `toggleDefault` L2662 |
| `บัญชีต้องอยู่สถานะใช้งานก่อนตั้งเป็นค่าเริ่มต้น` | warning | `toggleDefault` L2656 |
| `เปิดใช้งานบัญชีแล้ว` | success | `activateAccount` L2670 |
| `ปิดใช้งานบัญชีแล้ว` | success | `confirmDeactivate` L2740 |
| `เก็บถาวรบัญชีแล้ว` | success | `confirmArchive` L2714 |
| `เลือกบัญชี {abbr} {mask} แล้ว (จำลอง)` | success | `pickDocAccount` L2775 |
| `ธนาคารมาตรฐาน ธปท. แก้ไขไม่ได้` | warning | `openBankEdit` L2785 |
| `ลบไม่ได้ — มี {used} บัญชีอ้างอิงธนาคารนี้อยู่ (ย้าย/ปิดบัญชีก่อน)` | warning | `removeBank` L2356 |
| `ลบธนาคารแล้ว` | success | `removeBank` L2360 |
| `สร้างธนาคารสำเร็จ` / `บันทึกการแก้ไขแล้ว` | success | `submitBank` L2871/L2878 |

### 9.3 Placeholders / help
- Account search: `ค้นหาธนาคาร / ชื่อบัญชี / เลขบัญชี` · Bank search: `ค้นหาธนาคาร / SWIFT / รหัส`
- Combobox: `ค้นหาธนาคาร (พิมพ์ชื่อ / รหัส / SWIFT)` · `ค้นหาบัญชีจากผังบัญชี (CoA)`
- `เลขที่บัญชี` placeholder `ตัวเลข 10-15 หลัก` · help `กรอกเฉพาะตัวเลข ไม่ต้องมีขีดหรือเว้นวรรค`
- `ชื่อบัญชี` placeholder `ชื่อเจ้าของบัญชี` · `สาขา` placeholder `เช่น สยามพารากอน`
- GL help: `ใช้สำหรับตั้งรายการบันทึกบัญชี (posting) เมื่อมีการรับ-จ่ายผ่านบัญชีนี้`
- Bank form: `เช่น ธนาคาร HSBC` · `เช่น HSBC` · `3 หลัก` · `เช่น HSBCTHBK` · SWIFT help `8 หรือ 11 หลัก — ตัวอักษรและตัวเลข`

### 9.4 Field labels
`ธนาคาร *` · `เลขที่บัญชี *` · `ชื่อบัญชี *` · `ประเภทบัญชี *` · `สาขา` · `สกุลเงิน` · `บัญชี GL (ผังบัญชี) *` · `ชื่อธนาคาร *` · `ชื่อย่อ *` · `รหัส ธปท. (ถ้ามี)` · `รหัส SWIFT / BIC *` · `ประเภท`

### 9.5 Read-only / hint notes (VERBATIM)
- 🔒 สกุลเงิน readonly value: `THB — บาทไทย`; tooltip: `เฟสนี้รองรับ THB เท่านั้น — สกุลเงินอื่นจะเปิดใช้พร้อม multi-currency (OQ-2)`
- SWIFT tooltip: `รหัสสากล 8 หรือ 11 หลัก (ตัวอักษร/ตัวเลข) ใช้ระบุธนาคารในการโอนระหว่างประเทศ`
- Reveal button title (masked): `ต้องมีสิทธิ์ · ระบบจะบันทึกการเข้าถึง`
- W1 delete-guard tooltip (row): `มี {used} บัญชีอ้างอิงธนาคารนี้ — ลบไม่ได้`
- **ธปท. read-only note** (bank view preset): `รายการมาตรฐาน ธปท. — เป็นข้อมูลอ้างอิงกลาง แก้ไข/ลบไม่ได้`
- Default toggle desc (form): `ตั้งค่าได้เพียง 1 บัญชีต่อบริษัท — เลือกใหม่จะย้ายค่าเริ่มต้นมาบัญชีนี้` / `ตั้งค่าได้เพียง 1 บัญชีต่อบริษัท`
- Default toggle desc (view): `ใช้เป็นค่าเริ่มต้นในใบสำคัญจ่าย — มีได้ 1 บัญชีต่อบริษัท` / `…ในใบสำคัญรับ — มีได้ 1 บัญชีต่อบริษัท`
- View default-tab warn (non-active): `บัญชีที่ไม่ได้อยู่สถานะใช้งาน ไม่สามารถตั้งเป็นค่าเริ่มต้นได้`

### 9.6 Modals
- **Archive:** title `เก็บถาวรบัญชีนี้?` · body `ต้องการเก็บถาวรบัญชี "{accName}" ใช่หรือไม่ บัญชีจะถูกย้ายไปสถานะเก็บถาวร`
  - used-in-doc note (is-warn): `บัญชีนี้ถูกใช้ในเอกสารและรายการกระทบยอดธนาคารแล้ว จึงลบถาวรไม่ได้ — ระบบจะเก็บถาวร (soft archive) เท่านั้น เอกสารและรายการกระทบยอดเดิมยังอ้างอิงบัญชีนี้ได้ตามปกติ`
  - not-used note (is-info): `การเก็บถาวรจะทำให้บัญชีนี้ไม่ปรากฏในตัวเลือกของเอกสารใหม่และรายการกระทบยอดธนาคาร และไม่สามารถตั้งเป็นค่าเริ่มต้นได้`
  - default-loss note (is-warn, only when account is a default — EC-14): `บัญชีนี้เป็น{บัญชีจ่ายเริ่มต้น|บัญชีรับเริ่มต้น|บัญชีจ่ายและรับเริ่มต้น}ของบริษัท — เมื่อเก็บถาวร ค่าเริ่มต้นนี้จะถูกยกเลิก บริษัทจะไม่มีค่าเริ่มต้นดังกล่าว กรุณาตั้งบัญชีอื่นแทนภายหลัง`
- **Deactivate:** title `ปิดใช้งานบัญชีนี้?` · body `"{accName}" จะไม่ปรากฏในตัวเลือกบัญชีของเอกสารใหม่และรายการกระทบยอดธนาคาร (เช่น ใบสำคัญจ่าย/รับ · การกระทบยอดธนาคาร)` · note (is-info): `เอกสารและรายการกระทบยอดธนาคารเดิมที่อ้างอิงบัญชีนี้ยังแสดงและใช้งานได้ตามปกติ — คุณเปิดใช้งานใหม่ได้ภายหลัง`
  - default-loss note (is-warn, only when account is a default — EC-14): `บัญชีนี้เป็น{บัญชีจ่ายเริ่มต้น|บัญชีรับเริ่มต้น|บัญชีจ่ายและรับเริ่มต้น}ของบริษัท — เมื่อปิดใช้งาน ค่าเริ่มต้นนี้จะถูกยกเลิก บริษัทจะไม่มีค่าเริ่มต้นดังกล่าว กรุณาตั้งบัญชีอื่นแทนภายหลัง`
- **Doc-picker:** title `จำลอง: เลือกบัญชีในเอกสาร` · subtitle `แสดงเฉพาะบัญชี "ใช้งาน" ของ {company}` · empty `ไม่มีบัญชีที่ใช้งานอยู่` · existing note (is-info): `ตัวอย่างเอกสารเดิม PV-2025-014 อ้างอิงบัญชี {bank} ({mask}) ซึ่งปัจจุบันปิดใช้งาน — เอกสารเดิมยังแสดงบัญชีนี้ตามปกติ แต่บัญชีดังกล่าวจะไม่อยู่ในรายการให้เลือกด้านบน`

### 9.7 Empty states
- Accounts (มี filter): title `ไม่พบรายการที่ค้นหา` · desc `ลองปรับคำค้นหรือล้างตัวกรอง` · action `ล้างตัวกรอง`
- Accounts (ไม่มี filter): title `ยังไม่มีบัญชีธนาคาร` · desc `เริ่มต้นด้วยการสร้างบัญชีธนาคารแรกของบริษัทนี้` · action `สร้างบัญชี`
- Banks: title `ไม่พบธนาคารที่ค้นหา` · desc `ลองปรับคำค้น` (ไม่มีปุ่ม action)
- Bank audit empty: `ยังไม่มีการสร้างหรือลบธนาคารที่สร้างเอง` · Account audit empty: `ยังไม่มีประวัติ`
- `emptyStateHTML` default fallback: title `ยังไม่มีข้อมูล`, icon `inbox` (L1850)

### 9.8 Validation error messages (VERBATIM)
- Account (`validateAccForm` L2501): `กรุณาเลือกธนาคาร` · `กรุณากรอกเลขที่บัญชี` · `เลขบัญชีต้องเป็นตัวเลข 10-15 หลัก` · `เลขบัญชีนี้มีอยู่แล้วในบริษัทนี้` · `กรุณากรอกชื่อบัญชี` · `กรุณาเลือกบัญชี GL`
- Bank (`submitBank` L2853): `กรุณากรอกชื่อธนาคาร` · `กรุณากรอกชื่อย่อ` · `กรุณากรอกรหัส SWIFT` · `SWIFT ต้องมี 8 หรือ 11 หลัก` · `รหัส SWIFT นี้มีอยู่แล้ว` · `รหัส ธปท. ต้องเป็นตัวเลข 3 หลัก`

### 9.9 Audit detail templates (`pushAudit`/`pushBankAudit`)
`สร้างบัญชี {abbr} {type}` · `แก้ไขข้อมูลบัญชี {abbr}` · `เปิดดูเลขบัญชีเต็ม {abbr}` · `ตั้งเป็นบัญชี{จ่าย/รับ}เริ่มต้น` / `ยกเลิกบัญชี{จ่าย/รับ}เริ่มต้น` · `เปิดใช้งานบัญชี {abbr}` · `ปิดใช้งานบัญชี {abbr}` · `เก็บถาวรบัญชี {abbr}` · `สร้างธนาคาร {abbr} (SWIFT {swift})` · `แก้ไขธนาคาร {abbr} (SWIFT {swift})` · `ลบธนาคาร {abbr} (SWIFT {swift})`

---

## §10 · Data Binding & BACKEND anchors

> ฟีเจอร์เป็น in-memory prototype — ไม่มี fetch/localStorage. จุดต่อไปนี้คือที่ dev ต้องต่อ API จริง (mapping API ดู §11).

### 10.1 Mock data structures
| ตัวแปร | โครง | L |
|---|---|---|
| `companies` (2) | `{id, name, taxId}` | L2001 |
| `banks` (22 preset) | `{code, nameTh, abbr, swift, type('local'/'foreign'), color}`; custom เพิ่ม `custom:true` | L2007 |
| `coa` (6) | `{code, name}` — cash/bank subset ของผังบัญชี | L2033 |
| `ACCT_TYPES` | `{savings:'ออมทรัพย์', current:'กระแสรายวัน', fixed:'ฝากประจำ'}` | L2042 |
| `accounts` (5: C1=4,C2=1) | `{id, company, bankCode, accNo, accName, acctType, branch, glCode, currency, status, defaultPay, defaultReceive, usedInDoc, createdAt}` | L2045 |
| `auditLog` (seed 5) | `{id, accountId, bankCode, action, detail, user, ts}` — append-only, unshift | L2055 |
| `accForm` / `bankForm` | form buffers (`blankAccForm`/`blankBankForm`) | L2064–68 |

### 10.2 Client-side gates / logic ที่ต้อง enforce ฝั่ง server
| logic | fn | หมายเหตุ BACKEND |
|---|---|---|
| Reveal permission | `revealAccNo` เช็ค `currentUser.canRevealFull` | ต่อ RBAC จริง; ต้อง server-side gate การคืนเลขเต็ม |
| Reveal audit | `pushAudit(...,'revealed',...)` | server ต้อง log ทุกครั้งที่คืนเลขเต็ม (data-classification) |
| Duplicate acc-no | `validateAccForm` — unique ต่อ company | server ต้อง enforce unique(company, accNo) |
| Default uniqueness | `enforceDefaultUnique` / `toggleDefault` | server: 1 defaultPay + 1 defaultReceive ต่อ company |
| Soft archive | `confirmArchive` set `status='archived'` (ไม่ลบ) | ห้าม hard-delete เมื่อ `usedInDoc` |
| Delete-guard bank (W1) | `removeBank` เช็ค `used>0` | server: block delete ธนาคารที่มี account อ้างอิง |
| SWIFT validate | regex `^[A-Z0-9]{8}$|^[A-Z0-9]{11}$` + dup check | server ต้อง validate ซ้ำ |
| Acc-no format | regex `^[0-9]{10,15}$` | ↑ |
| Masking | `maskAccNo` (client display) | server ควรส่ง masked โดย default, คืนเต็มเมื่อ authorized |

### 10.3 Icon/asset dependency
- Lucide `0.469.0` โหลด multi-CDN fallback (unpkg→jsdelivr→cdnjs, L1550) — **ต้องต่อ internet/มี proxy**; ถ้า fail UI ยังใช้ได้แต่ไม่มี icon (no-op fallback L1560). Icons ใช้ทั้งหมดผ่าน `data-lucide` + `renderIcons()`

---

## §11 · Traceability + Drift Log

> **3 ทาง:** Brief §x ↔ FRD (P/M · API · BR/EC · FN) ↔ HTML anchor. FRD ใช้รหัส `F-BNK-…` (ในตารางย่อเป็น API-05 = F-BNK-API-05 ฯลฯ).

### 11.1 Screen / Surface ↔ FRD P/M ↔ HTML
| Brief § | FRD (01_UI) | HTML anchor |
|---|---|---|
| §4.3 Tab บัญชีบริษัท | **P-01** (Pattern A) | `accountsTabHTML()` L2158 · `rowHTML()` L2239 · tab `state.tab='accounts'` |
| §4.4 Tab ธนาคาร | **P-02** (Pattern A) | `banksTabHTML()` L2286 · `bankRowHTML()` L2326 · `bankAuditSectionHTML()` L2312 |
| §4.5/§6 Account create/edit drawer | **P-03** (Pattern B, 680) | `accountFormHTML()` L2398 · `renderDrawerEl` L2373 |
| §4.5/§6 Account view drawer | **P-04** (Pattern C, tabbed) | `accountViewHTML()` L2559 (tabs detail/default/audit) |
| §4.5/§6 Bank create/edit drawer | **P-05** (Pattern B) | `bankFormHTML()` L2792 |
| §4.5/§6 Bank view drawer | **P-06** (Pattern C) | `bankViewHTML()` L2888 |
| §6/§9.6 Archive modal | **M-01** (Pattern D) | `archiveModalHTML()` L2687 |
| §6/§9.6 Deactivate modal | **M-02** (Pattern D) | `deactivateModalHTML()` L2718 |
| §6/§9.6 Doc-picker (mock) | **M-03** (Pattern D, sim I-05) | `docPickerHTML()` L2745 |
| §2 Route | route `#/bank-master` เดียว | `state.currentRoute='bank-master'` L1991 |

### 11.2 Action ↔ FRD API / FN ↔ HTML fn
| Action | FRD API | FRD FN | HTML fn |
|---|---|---|---|
| List accounts (masked, per-company, status filter) | API-01 | FN-04 `buildAccountListQuery` | `accountsTabHTML`/`companyAccounts` L2074 |
| Create account | API-02 (Idempotency-Key) | FN-01 `createBankAccount` + FN-03 validate | `submitAccount` L2519 → `commitAccount` L2528 |
| Get account detail | API-03 | FN-04 (single) | `openView`/`accountViewHTML` |
| Edit account | API-04 (If-Match) | FN-02 `updateBankAccount` | `openEdit` L2513 → `commitAccount` (isEdit) |
| 🔒 **Reveal full acc_no** | **API-05** (ACL + audit-first) | **FN-05** `revealAccountNumber` · ENG-BNK-01 | `revealAccNo` L2273 (+`hideAccNo` L2281) |
| Deactivate | API-06 | FN-07 `transitionAccountStatus` | `confirmDeactivate` L2735 |
| Activate | API-07 | FN-07 | `activateAccount` L2666 |
| Soft archive | API-08 (terminal) | FN-07 | `confirmArchive` L2707 |
| Set default pay/receive | API-09 | FN-06 `enforceDefaultUnique` | `toggleDefault` L2654 / `enforceDefaultUnique` L2547 |
| List banks | API-10 | — | `banksTabHTML` |
| Create custom bank | API-11 | FN-08 `createCustomBank` · ENG-BNK-02 | `submitBank` (create) L2872 |
| Edit custom bank | API-12 | FN-09 `updateCustomBank` | `submitBank` (edit) L2864 · `openBankEdit` L2783 |
| 🔒 **Delete custom bank (W1 guard)** | **API-13** (used=0 guard) | **FN-10** `deleteCustomBank` | `removeBank` L2353 |
| Account audit stream | API-14 | FN-12 `appendAudit` | `auditTab` (L2611) · `pushAudit` L2083 |
| Bank audit stream | API-15 | FN-12 | `bankAuditSectionHTML` L2312 · `pushBankAudit` L2084 |
| Pickable accounts (active-only, cross-module) | **API-16** | FN-11 `buildPickableAccounts` | `docPickerHTML` (active filter) L2747 |

### 11.3 Business rule ↔ HTML enforcement
| FRD BR | HTML anchor (client-side reflection) |
|---|---|
| BR-BNK-01 unique (company, accNo) | `validateAccForm` dup check L2506 · err `เลขบัญชีนี้มีอยู่แล้วในบริษัทนี้` (EC-01) |
| BR-BNK-02 ≤1 default pay/receive/company + must be active | `enforceDefaultUnique` L2547 · `toggleDefault` active-guard L2656 (EC-03) |
| BR-BNK-03 accNo `^[0-9]{10,15}$` + strip | regex L2505 · input strip L2422 (EC-02) |
| BR-BNK-04 SWIFT 8/11 alnum + upper/strip | regex L2856 · input transform L2829 (EC-07) · ENG-BNK-02 |
| BR-BNK-05 inactive/archived hidden from picker | `docPickerHTML` active-only + existing-doc note L2756 (EC-04) |
| BR-BNK-06 no hard-delete accounts (soft archive) | `confirmArchive` set archived L2709 · no delete path (EC-06) |
| BR-BNK-07 append-only audit (2 streams) | `pushAudit`/`pushBankAudit` unshift L2083–84 (no update/delete) |
| BR-BNK-08 custom-bank delete only used=0; preset never | `removeBank` guard L2355 + disabled btn L2335 · `openBankEdit` preset block L2785 (EC-08, W1) |
| 🔒 BR-BNK-09 mask last-4; reveal only w/ perm + audit-first | `maskAccNo` L2075 · `revealAccNo` perm+audit L2273 (EC-05) — **security spine** |
| BR-BNK-10 THB forced+readonly | readonly input `THB — บาทไทย` L2449 + tooltip (OQ-2) |
| BR-BNK-11 gl_code required | `validateAccForm` L2508 err `กรุณาเลือกบัญชี GL` |
| BR-BNK-12 22 preset ธปท. immutable | preset `มาตรฐาน` cell L2339 · preset note L2904 |

### 11.4 ⚠️ Drift Log
| # | ประเภท | รายละเอียด | สถานะ |
|---|---|---|---|
| D-1 | **FRD↔BRD naming (resolved→HTML)** | Audit action: BRD §6 E3 = `default-changed`; **HTML ใช้ `set-default`** (L2057,L2090,L2660) **และ `bank-edited`** (L2095,L2868). FRD §1.9 Section M + **LD-04**: "Spec follows HTML (R14)". | ✅ Resolved toward HTML — non-blocking, no scope change |
| D-2 | **FRD↔BRD naming (resolved→HTML)** | Tab label: BRD §14.6 P-01 = "บัญชีธนาคาร"; **HTML tab = "บัญชีบริษัท"** (L2142) (page title `ธนาคาร / บัญชีบริษัท`). FRD §1.9 + §7.0: "Spec follows HTML". | ✅ Resolved toward HTML |
| D-3 | **FN numbering mismatch (HTML↔FRD)** | HTML comments/PREFLIGHT ใช้ `FN-01..FN-06 + FN-90` (audit, L2053/L2964); **FRD ใช้ `F-BNK-FN-01..12`** (ไม่มี FN-90 — audit = FN-12 `appendAudit`). ชื่อกลุ่มงานตรงกัน แต่รหัสต่าง scheme. | ℹ️ Doc-only — mapping ใน §11.2; ไม่กระทบ behavior |
| D-4 | **HTML-only (kit leftovers)** | `state.selectedIds`/bulk-bar, `state.sort`/`.is-sortable`, drawer wide 920px มีในโค้ดแต่ไม่ถูกใช้ — ไม่มีใน FRD scope | ℹ️ ไม่ใช่ drift ทางธุรกิจ — ดู §13 ข้อ 2 |
| D-5 | **FRD-only (backend, ยังไม่มีใน HTML — ตามเจตนา prototype)** | Idempotency-Key (API-02), If-Match/409 stale (API-04/EC-17), rate-limit reveal 429 (BR-BNK-09), `ERR_AUDIT_WRITE_FAILED` audit-first invariant, 403 re-check at mutation (EC-13/OQ-BNK-04) — เป็น server contract ที่ prototype in-memory ไม่ได้จำลอง | ✅ คาดหมาย — dev ต้อง implement ฝั่ง server (ดู §10.2) |
| D-6 | **EC-14 default-on-deactivate (RESOLVED)** | เดิม FRD [AI-DEFAULT] = "warn + keep flag"; HTML `confirmDeactivate`/`confirmArchive` เคลียร์ `defaultPay/Receive` **และแสดง warn note (`.note.is-warn`)** ในทั้งสอง confirm modal เมื่อบัญชีเป็น default. | ✅ **RESOLVED 2026-08-06 — warn+clear**; FRD updated to match HTML (EC-14/OQ-BNK-05 → 07 LD-06) — no scope change |

> **สรุป drift:** ไม่มี drift เชิงธุรกิจที่ขยาย scope (FRD §7.0: "Neither expands scope … No spec written against the screen"). D-1/D-2 ถูกเคาะให้ตาม HTML แล้ว (R14 source-of-truth wins). D-5 คือชั้น backend ที่ prototype ไม่จำลอง — ไม่ใช่ความขัดแย้ง.

### 11.5 Open Questions ที่สะท้อนใน UI (จาก DECISION_LOG / 00_OVERVIEW §0.8 — ส่วนใหญ่ [AI-DEFAULT] OPEN · OQ-BNK-05 RESOLVED)
| OQ | สาระ | ร่องรอยใน HTML |
|---|---|---|
| OQ-BNK-01 | role/tier ที่ได้ `canRevealFull` | mock `currentUser.canRevealFull=true` L1998 (ต่อ RBAC จริง) |
| OQ-BNK-02 (=OQ-2) | multi-currency เมื่อไร | THB readonly + tooltip L2447 |
| OQ-BNK-03 | mask ตอน export/print | — (ยังไม่มี export ใน HTML) |
| OQ-BNK-04 | backend enforce reveal/edit (ไม่ใช่แค่ซ่อนปุ่ม) | client มีแค่ gate + audit; **server ต้อง re-check** (§10.2) |
| OQ-BNK-05 ✅ RESOLVED | default account ถูก deactivate/archive → เคลียร์ + เตือน | **RESOLVED 2026-08-06 (warn+clear):** HTML เคลียร์ default ตอน deactivate/archive (`confirmDeactivate`/`confirmArchive`) **และแสดง warn note (`.note.is-warn`)** เมื่อบัญชีเป็น default; FRD ปรับให้ตรงแล้ว |
| OQ-BNK-06 | register `acc_no` ใน Restricted Resources | — (governance, นอก UI) |

> ✅ **หมายเหตุ EC-14 — RESOLVED 2026-08-06 (warn + clear):** HTML `confirmDeactivate`/`confirmArchive` เคลียร์ `defaultPay/defaultReceive` **และแสดง warn note (`.note.is-warn`)** ในทั้งสอง confirm modal เมื่อบัญชีเป็น default (`บัญชีนี้เป็นบัญชีจ่าย/รับเริ่มต้น — … ค่าเริ่มต้นนี้จะถูกยกเลิก …`). FRD ปรับให้ตรงกับ HTML แล้ว — ไม่มี divergence ค้าง.

> _อ้างอิงเสริม: 04_DB (T_company_bank_account · T_bank · T_bank_audit_log) และ 06_TESTS (AC-01..18 · XT-01..04) ไม่ได้อยู่ใน scope การสกัดรอบนี้ — ดึงเพิ่มเมื่อ matrix ต้องการ field ระดับ DB หรือ test-case id._

---

## §12 · Diff จากเวอร์ชันก่อน
— ไม่มี HTML เวอร์ชันเก่าส่งมาเทียบ (ข้าม). อย่างไรก็ดี ไฟล์ปัจจุบันบันทึกการแก้ที่ผ่าน QC-round2 (2026-08-05) ไว้ในตัว: Bug A/B/C, I-06, W1 + banks-tab CRUD (view/edit/delete) — ดู §0 และ PREFLIGHT stamp (L2953–2967).

---

## §13 · 💡 ข้อเสนอ (ไม่ใช่ AS-BUILT — R1)
> จุดที่พบระหว่างสกัด — **ยังไม่มีในโค้ด**, dev อย่านำไปสร้างโดยไม่เคาะสเปคก่อน:
1. **Focus-trap ใน overlay** — drawer/modal ไม่มี focus-trap; Tab หลุดออกนอก overlay ได้ (มีแค่ Esc + click-outside). พิจารณาเพิ่มเพื่อ a11y
2. **Unused kit affordances** — `state.selectedIds`/bulk-bar, `.table th.is-sortable`/`state.sort`, `.cell-truncate`, drawer wide 920px มีในโค้ดแต่ **ฟีเจอร์นี้ไม่ได้ใช้** — ระบบจริงถ้าไม่ต้องการ ควรตัดออกกันสับสน
3. **User-menu ไม่มี Esc dismiss** (ปิดได้แค่ click-outside) — ต่างจาก overlay อื่น; พิจารณาให้สอดคล้อง
4. **`fmtNumber/fmtMoney/fmtDate`** ประกาศแต่ไม่ถูกเรียก — ถ้าระบบจริงเพิ่มยอดเงิน/วันที่ ให้ใช้ helper ชุดนี้ (Rule #43) แทน format เอง
5. **`b.color`** (brand color 22 ธนาคาร) เก็บใน data แต่ไม่ถูกใช้แสดงผล (ไม่มี `.bank-logo`) — เผื่อ future logo/badge

---
_บรีฟนี้สร้างโดยสกิล html-ui-brief — extraction-based จาก BankMaster.html (source of truth) จับคู่ FRD_F-BNK_Pack._
