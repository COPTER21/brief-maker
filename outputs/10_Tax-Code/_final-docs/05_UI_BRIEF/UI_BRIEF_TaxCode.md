# UI BRIEF — F-TAX · รหัสภาษี (Tax Code)

> **EXTRACTION-BASED (Iron Rule R1)** — ทุกบรรทัดในบรีฟนี้ trace กลับหา anchor จริงใน HTML ได้ (CSS class / function / ข้อความ / บรรทัด `Lxxxx`). ข้อเสนอที่ไม่มีในโค้ดอยู่หมวด §13 เท่านั้น
> **หมายเหตุ skill:** `.claude/skills/html-ui-brief/` มีเฉพาะ `SKILL.md` — ไม่มี `templates/ui-brief.template.md`, `references/extraction-checklist.md`, `scripts/extract_anchors.py` ในโปรเจกต์นี้ จึงยึดโครง 13 sections + Iron Rules R1–R10 + Verification Gate ตามที่ระบุใน SKILL.md เอง (L104-122, L83-96) และสกัดด้วยการอ่านโค้ด + grep เต็มไฟล์แทน extractor

---

## §0 · Document Control + Pairing

| Field | Value |
|---|---|
| Feature | F-TAX · รหัสภาษี (Tax Code) |
| HTML source of truth | `outputs/10_Tax-Code/01_HTML/TaxCode.html` (2839 บรรทัด, single-file SPA) |
| `<title>` | `รหัสภาษี · CUBE NATIVE` (L6) |
| Base-kit | BASE-KIT v6.4 (L22) · PREFLIGHT v6.4 (L2829) · patterns A/B/C/D (L2834) |
| Feature version | Sandbox · v1.0.0 (L1522) · `const state`, in-memory (L1648) |
| FRD Pack | `outputs/10_Tax-Code/04_FRD/FRD_F-TAX_Pack/` (FULL variant — INDEX + 9 files) |
| FRD files paired | 00_OVERVIEW · 01_UI (5 pages P-01..P-05) · 02_API (12 APIs) · 05_RULES (17 BR + 13 VR + 19 EC) · INDEX |
| Pairing status | ✅ paired — Traceability §11 + Drift Log ครบ |
| TODAY (mock clock) | `2026-08-05` (`const TODAY`, L2065) |
| Company scope | `COMP-001 · บริษัท 2BSimple จำกัด · TH · THB` (`CURRENT_COMPANY`, L2066) |
| Permissions (mock user) | ครบ 6 สิทธิ์ `tax_code.view/create/update/activate/deactivate/view_audit` (`CURRENT_PERMISSIONS`, L2067-2070) — single-user sandbox |
| Assets | Fonts: Google `Noto Sans Thai` + Fontshare `Satoshi` (L9-12, CDN) · Icons: Lucide `0.469.0` multi-CDN fallback unpkg→jsdelivr→cdnjs (`loadLucide`, L1617-1623) |

---

## §1 · Design Tokens (AS-BUILT)

### 1.1 CSS Variables — `:root` (L24-57, CUBE CI v2.0 "Warm Light")
| Token | ค่า | Token | ค่า |
|---|---|---|---|
| `--c-navy` / `--c-navy-2` | `#111111` | `--c-ink` | `#111111` |
| `--c-primary` | `#FF3B30` | `--c-primary-hover` | `#E62E24` |
| `--c-teal` | `#FF9A1F` | `--c-teal-light` | `#FFB763` |
| `--c-mute` | `#54565C` | `--c-mute-2` | `#73757B` |
| `--c-mute-3` | `#9A9CA2` | `--c-line` | `#DEDAD4` |
| `--c-line-2` | `#E9E5E0` | `--c-line-3` | `#F1EEEA` |
| `--c-bg-off` | `#FAF8F5` | `--c-success` | `#1F9D55` |
| `--c-warning` | `#E8870F` | `--c-danger` | `#E62E24` |
| `--sidebar-w` | `232px` | `--shell-h` | `52px` |

**Type scale (locked, L44-52):** `--fs-h1 22px` · `--fs-h2 17px` · `--fs-h3 15px` · `--fs-body 14px` · `--fs-sub 13px` · `--fs-meta 12px` · `--fs-cap 11px` · `--fs-kpi 28px`
**Spacing (L54):** `--sp-xs 4 / -sm 8 / -md 12 / -lg 20 / -xl 28px`
**Radius (L56):** `--r-xs 4 / -sm 6 / -md 8 / -lg 12 / -full 999px`
**Page-specific overrides (L1315-1319):** `--fs-table 12.5px` · `--row-h 44px`

### 1.2 Fonts / body
- `body` font stack: `'Satoshi', 'Noto Sans Thai', system-ui, sans-serif` (L79) · base `font-size:14px` · `line-height:1.5` · `background:var(--c-bg-off)` · **`min-width:1180px`** (admin tool, forces horizontal scroll เมื่อจอแคบ — L86)
- Thai titles ใช้ `'Noto Sans Thai'` เฉพาะจุด: `.ph-title` (L360), `.drawer-title` (L894), `.modal-title` (L1106)

### 1.3 Scrollbar (Iron Rule #49, L66-77)
- Global thin 5px, thumb `rgba(17,17,17,.14)` บนพื้นสว่าง / `rgba(255,255,255,.28)` บน `.sidebar`,`.slide`
- `html { scrollbar-gutter: stable; }` (L64) — จองพื้นที่ scrollbar กัน jank (Rule #35)

### 1.4 Shadow / radius patterns (สกัด ไม่ลอกทั้งดุ้น)
- Drawer: `box-shadow:-16px 0 40px rgba(17,17,17,0.18)` (L850)
- Modal: `box-shadow:0 24px 64px rgba(17,17,17,0.28)` · `border-radius:12px` (L1082/1074)
- Toast: `box-shadow:0 12px 32px rgba(17,17,17,0.30)` · `border-radius:10px` (L1163/1156)

### 1.5 ⭐ Z-INDEX MAP (L1316 — เรียงสูง→ต่ำ)
> ประกาศชุดเดียวที่ `:root` (L1316) + override 1 จุด (L1321)

| z | ตัวแปร | ใช้กับ | anchor |
|---|---|---|---|
| **80** | `--z-toast` | `.toast` | L1159 |
| **60** | `--z-modal` | `.modal-backdrop` (**override** — base `.modal-backdrop` เดิม 50) | L1321 override L1063 |
| **51** | `--z-drawer` | `.drawer` | L845 |
| **50** | `--z-backdrop` | `.drawer-backdrop` · `.ss-list` (search-select dropdown, L539) | L833 / L539 |
| **40** | `--z-dropdown` | `.user-menu` · `.info-tip::after` tooltip · `data-overlay` menus | L313 / L1307 |
| **20** | `--z-shell` | `.sidebar` | L104 |
| **19** | `--z-sticky` | `.shell-bar` | L241 |

> **ข้อสังเกต (verified):** modal-backdrop ถูกดันขึ้น z=60 ผ่าน override L1321 จึงอยู่เหนือ drawer (51) เสมอ → เปิด confirm modal ทับ drawer ได้ถูกต้อง (ดู §7 Esc chain). `.ss-list` = z-backdrop(50) แต่อยู่ใน stacking context ของ drawer(51) จึงลอยเหนือ field ในฟอร์มได้

---

## §2 · Route Map

| Route (hash) | เป็นของ feature นี้? | render | anchor |
|---|---|---|---|
| `#/accounting/setup/tax-codes` | ✅ หน้าเดียวจริงของ feature | `renderPage()` → `#page-content` | default redirect L2085-2087 |
| `#/accounting/reports/vat-return` | ❌ sidebar stub (External Contract ภ.พ.30) | — (ไม่มี handler) | L1496 `data-feature="pp30"` |
| `#/accounting/reports/withholding-tax` | ❌ sidebar stub (External ภ.ง.ด.3/53) | — | L1499 `data-feature="wht-report"` |

**Router (L1672-1682):**
- `getRoute()` (L1675): `location.hash` → ถ้าว่าง/`#`/`#/` return `'home'` มิฉะนั้น strip `#/`
- `navigate(route)` (L1680): set `location.hash = '#/'+route`
- **Refresh-safety (L2085-2087):** ถ้า hash ว่าง → `history.replaceState(null,'','#/accounting/setup/tax-codes')` — refresh ค้างที่หน้า tax-codes เสมอ
- `hashchange` → `render()` (L2010, late-binding เพื่อชี้ render() ตัวที่ feature override)
- **สำคัญ:** `render()` **ไม่ได้ switch ตาม route** — feature นี้เป็นหน้าเดียว, `renderPage()` (L2280) render list เสมอ ไม่ว่า hash เป็นอะไร (routing เชิง multi-page เป็น shell placeholder เท่านั้น)
- Boot: `bootIfReady()` รอ `domReady && lucideReady` (L2017-2042) + safety net 5s (L2036) ถ้า Lucide ไม่ ready

---

## §3 · Layout Shell

| Region | selector | ขนาด / ค่า | anchor |
|---|---|---|---|
| Sidebar | `.sidebar` `<aside>` | fixed left, `width:var(--sidebar-w)=232px`, bg `#111111`, z-shell(20) | L98-108 / L1438 |
| — Brand | `.sb-brand` / `.sb-logo` / `.sb-name` | logo gradient primary→teal, `CUBE NATIVE` / `การบัญชี` | L1440-1444 |
| — Nav (collapsible modules) | `.sb-nav` > `.sb-module[data-expanded]` | 4 modules (ดู §3.1) | L1447-1518 |
| — Footer | `.sb-footer` + `.pulse-dot` | `Sandbox · v1.0.0` | L1520-1523 |
| Main | `.main` | `margin-left:var(--sidebar-w)`, `min-height:100vh` | L225 / L1527 |
| Shell bar | `.shell-bar` `<header>` | sticky top, `height:52px`, bg `#fff`, z-sticky(19) | L232-243 / L1528 |
| — Breadcrumb | `.breadcrumb` | `การบัญชี › ตั้งค่าบัญชี › รหัสภาษี` (current) | L1529-1535 |
| — Company chip | `.company-context` | `บริษัทปัจจุบัน 2BSimple จำกัด` (read-only, LOCK-02) | L1537 |
| — Notif | `.notif-wrap` `.icon-btn#notifBtn` + `.notif-dot` | `toggleNotif()` = no-op (out of scope) | L1538-1542 / L1584 |
| — User chip + menu | `.user-chip` / `.user-menu#userMenu` | `สุนิสา ภักดี · Accounting Admin · CUBE NATIVE` avatar `สภ` | L1544-1556 |
| Content | `.content#page-content` | `padding:24px`, fluid full-width (ไม่มี max-width, Rule #30) | L339-341 / L1561 |

### 3.1 Sidebar modules (4 groups, `toggleModule()` L1665)
- Header ไม่ navigable — คลิกแค่ toggle `data-expanded` (Rule #27, L1662)
- `การบัญชี` (expanded, L1449): สมุดรายวัน / ผังบัญชี / บัญชีแยกประเภท
- `ตั้งค่าบัญชี` (expanded, L1469): **รหัสภาษี (is-active, `data-feature="tax-code"` icon `percent`, L1476)** / กลุ่มบัญชีตั้งพัก / เงื่อนไขชำระเงิน
- `รายงานภาษี` (collapsed, L1489): ภ.พ.30 / ภงด.3 / 53 (external routes)
- `System` (collapsed, L1506): ตั้งค่าระบบ
- `syncSidebar()` (L2273): บังคับ `.sb-item[data-feature="tax-code"]` เป็น `is-active` ทุก render

---

## §4 · Page Anatomy

> ทั้ง feature = 1 route แต่มี **5 view surfaces** ตรงกับ FRD P-01..P-05 (01_UI §1.0)

### P-01 · รายการรหัสภาษี — `renderPage()` (L2280-2356)
Region tree:
```
.content#page-content
├─ .ph (page header, L2314)            → .ph-title "รหัสภาษี" + .ph-count "N รหัส" + .ph-sub
│   └─ .ph-actions: btn-secondary "ดูรายการที่เลือกได้ในเอกสารใหม่" (→picker) · btn-primary "สร้างรหัสภาษี" (gated create)
├─ .stats (4 KPI, L2325-2330)          → 3 clickable filter + 1 static (ดู §5.2)
├─ .drawer-tabs.tax-family-tabs (L2332)→ VAT / WHT tab (setTab)
└─ .card (L2337)
    ├─ .filter-bar (L2338)             → .input-search + .select.filter-status + reset btn (conditional)
    ├─ .table-scroll > table.table     → 8 คอลัมน์ (L2351-2353)
    └─ .table-footer                   → "แสดง X จาก Y รหัสในกลุ่ม VAT/WHT" + company line
```
- Row: `<tr class="is-clickable" onclick="openDrawer('view',id)">` (L2297) — คลิกทั้งแถวเปิด view drawer; cell actions ห่อ `onclick="event.stopPropagation()"` (L2305)
- Table columns (L2352): รหัส·ชื่อ·อัตรา(col-num)·[ทิศทาง/ประเภทเงินได้ สลับตาม tab, `colHead` L2290]·วันมีผลเริ่ม·วันมีผลสิ้นสุด·สถานะ·actions
- Sortable headers: `sortHeader(col)` (L2363) — code/name/rate/effStart/effEnd/status; icon `arrow-up-down`→`arrow-up`/`arrow-down`

### P-02 · สร้าง/แก้ไข — `renderFormDrawer()` (L2420-2544) · drawer `.standard` 680px
```
.drawer.standard
├─ .dw-head (L2510)     → .dw-eyebrow (create="รหัสภาษีใหม่" / edit="แก้ไขรหัสภาษี" / replace="สร้างรหัสแทน") + .dw-title + close x
├─ .drawer-body (L2515)
│   ├─ replNote (ถ้า replacement, tc-alert is-info, L2497)
│   ├─ rateReplaceBtn (ถ้า used>0, tc-alert + "สร้างรหัสแทน", L2500)
│   ├─ .form-section "ข้อมูลรหัสภาษี" (L2517): familyCtl · code+name (field-row) · vatKindCtl(VAT) · rate+dir(field-row) · incomeCtl(WHT)
│   └─ .form-section "บัญชีแยกประเภท (GL) & การมีผล" (L2528): glBlock(combobox #94) · effStart+effEnd (field-row)
└─ .dw-footer (L2537)   → btn-ghost "ยกเลิก" | (btn-secondary "บันทึกร่าง" conditional) + primaryBtn
```
- Field visibility state-driven: `onFamilyChange()` (L2548) / `onVatKindChange()` (L2560) / direction (L2461) — ดู §8

### P-03 · รายละเอียด — `renderViewDrawer()` (L2688-2750) · drawer `.standard` 680px, read-only
```
.drawer.standard
├─ .drawer-header (L2716)  → .tc-avatar(is-vat/is-wht) + code + statusPill + subtitle "name · อัตรา X" + actions + close
├─ .drawer-body (L2725)
│   ├─ usedBadge (L2726)
│   ├─ .drawer-section "รายละเอียด" → .def-grid (บริษัท/ตระกูล/[ประเภท VAT]/อัตรา/ทิศทาง/[หมวดรายงาน|ประเภทเงินได้+กติกา]/GL rows/วันมีผล/[lineage])
│   └─ .drawer-section "ประวัติการเปลี่ยนแปลง (Audit)" (L2742) → .timeline (gated tax_code.view_audit)
└─ .drawer-footer (L2745)  → meta "รหัส <id> · การมีผล ..." + btn-secondary "ปิด"
```

### P-04 · Picker (ตัวเลือกตามวันที่เอกสาร) — `renderModal('picker')` (L2787-2814) · modal 440px
```
.modal
├─ .modal-header  → icon list-checks + "ตัวเลือกตามวันที่เอกสาร"
├─ .modal-body    → select "นำไปใช้กับ" (SALES/PURCHASE/PAYMENT) · date "วันที่เอกสาร" · pick-group VAT · pick-group WHT · [snapshot-card]
└─ .modal-footer  → btn-secondary "ปิด"
```

### P-05 · Confirm (deactivate / archiveDraft) — `renderModal()` (L2771-2785) · modal 440px
```
.modal → .modal-header(icon is-warning + title + subtitle) · .modal-body(tc-alert is-info) · .modal-footer(ยกเลิก + danger action)
```

---

## §5 · Component Inventory (anchor + โครง + states R4)

### 5.1 Button `.btn` (L379) — states
| State | มีจริง? | anchor |
|---|---|---|
| variants | primary/secondary/ghost/danger + `.btn-sm` | ใช้ทั่ว L2320-2321, `.btn-sm` L2501 |
| default/hover | ✅ (transition all 120ms, L397) | L397 |
| disabled | ✅ submitting → `disabled` + spinner "กำลังบันทึก…" | primaryBtn L2506 |
| focus | ✅ global `:focus-visible outline 2px primary` | L1326-1328 |
| loading | ✅ `loader-2 spin` | L2506 |
> ปุ่มไทย: `padding:2px 16px 0` optical-center, ห้าม line-height:1 (Rule #36, L385-393)

### 5.2 KPI Stat `.stat` (L2326-2329)
- 3 ใบแรก clickable filter: `is-clickable` + `role=button tabindex=0` + `onclick=setStatusFilter(v)` + `onkeydown=onStatusFilterKey(event,v)` (L2326-2328)
- `on(v)` (L2286) เติม `is-on` เมื่อ `state.filters.status===v` = active state
- ใบที่ 4 "ถูกอ้างอิงแล้ว" (nUsed) **static ไม่ clickable** (L2329)
- ค่า: รหัสทั้งหมด(nTotal) / พร้อมใช้วันนี้(nActive=isPickable) / ร่าง-ปิดใช้งาน(nPending) / ถูกอ้างอิงแล้ว(nUsed)
- States: default / hover / `is-on` (selected) — ไม่มี disabled/loading/empty (—)

### 5.3 Family tabs `.drawer-tab` (L2333-2334)
- VAT (icon receipt-text) / WHT (icon scissors) + count pill; `is-active` เมื่อ `state.tab` ตรง (L2333)
- States: default / hover(color ink, L930) / `is-active`(primary + border-bottom, L931). ไม่มี disabled (—)

### 5.4 Filter bar (L2338-2350)
- `.input-search` + lead icon search + `oninput=onSearch()` placeholder `ค้นหารหัส / ชื่อ / ประเภทเงินได้` (L2339)
- `.select.filter-status.width-filter` (max 200px) 7 options (L2340-2348): ทุกสถานะ / พร้อมใช้วันนี้ / ร่าง-ปิดใช้งาน-เก็บถาวร / ใช้งาน / ร่าง / ปิดใช้งาน / เก็บถาวร
- Reset btn `.btn-ghost.filter-reset` "ล้างตัวกรอง" — **conditional:** แสดงเมื่อ `search||status!=='all'` (L2349)

### 5.5 Table row + status pill + used cell
- `statusPill(s)` (L2208): active→`pill pill-info "ใช้งาน"` · draft→`pill-muted "ร่าง"` · inactive→`pill-muted "ปิดใช้งาน"` · else→`pill-muted "เก็บถาวร"`
- `usedCell(r)` (L2225): used>0 → `.used-chip "ใช้แล้ว N เอกสาร"` (icon file-check) · else → `.used-none "ยังไม่ถูกใช้"`
- Row actions (L2305-2309, gated): แก้ไข(pencil, update) · ปิดใช้งาน(power, active+deactivate) · เก็บร่างถาวร(archive, draft+deactivate)

### 5.6 ⭐ Search-Select combobox (Iron Rule #94/#34) — `searchSelectHTML()` (L1795) + `initSearchSelect()` (L1808)
- โครง: `.search-select` > lead search icon + `input.ss-input` + `.ss-clear`(hidden) + `.ss-caret` chevron + `.ss-list`(hidden) (L1799-1806)
- ใช้ 4 จุดในฟอร์ม (`postRender()` L2570): `glSale`(VAT_SALE) · `glPurchase`(VAT_PURCHASE) · `glWht`(WHT_PAYABLE) · `incomeType`(INCOME_TYPES)
- Handlers: `ssOpen/ssOnInput/ssPick/ssClear/ssOnKey` (L1866-1876) · keyboard: ↑↓ navigate, Enter pick, **Esc ปิด list** (L1875) · click-outside ปิด (L1877-1882)
- States: closed(selected label) / open(query) / filtered / empty (`ไม่พบรายการ` default `emptyText` L1812, override เป็น — ไม่มีในฟอร์มนี้) / highlighted `.ss-opt.is-active` (L1849) / cleared
- List positioning: `positionMenu()` (L2048) flip drop-up ถ้าที่ด้านล่างไม่พอ (L2050)

### 5.7 Field + inline validation
- `.field` + `.field-label`(+`.req` *) + input + `.field-error` (reserved space `min-height:15px visibility:hidden`, Rule #43, L1136)
- `fldErr(k)` (L2417) → เติม `is-invalid` · `errMsg(k)` (L2418) → error text
- Number input: hide spinner global (Rule #19, L93-95)
- `validateField()`/`clearFieldError()` (L1904/1912) generic — **feature นี้ validate ตอน submit ไม่ใช่ onblur** (ใช้ `validateForm()` L2592)

### 5.8 Empty state — `emptyStateHTML()` (L1917)
- โครง: `.empty` > `.empty-icon` + `.empty-title` + `.empty-desc` + (action btn optional)
- **ใช้จริงเพียง 1 จุด:** filter-empty (L2293) → icon `search-x`, title `ไม่พบรายการที่ค้นหา`, desc `ลองปรับคำค้นหรือล้างตัวกรอง`, action `ล้างตัวกรอง` (icon rotate-ccw → resetFilters)
- **No-data empty (`ยังไม่มีข้อมูล` default L1924) — ไม่มี trigger ในหน้านี้** เพราะ records seed ตายตัว 9 records (L2119-2161) ไม่มีทางว่างเป็น 0 → ดู Drift D-03

### 5.9 Timeline (audit) — `.timeline` > `.tl-item`(`.tl-dot`+`.tl-title`+`.tl-meta`) (L2703-2705)
- render จาก `r.audit[]` เรียงล่าสุดก่อน (unshift ตอน mutate) · gated `view_audit`

### 5.10 Toast `.toast#toast` (L1149, container L1601) — ดู §6.4
### 5.11 tc-alert `.tc-alert`(is-info/default) — inline notice ในฟอร์ม/modal (L2497/2501/2776/2784)

---

## §6 · Overlay Registry + Dismiss Rules

| Overlay | selector | ขนาด | z | เปิด | ปิด (dismiss) | anchor |
|---|---|---|---|---|---|---|
| **Drawer** (create/edit/view) | `.drawer#drawer` + `.drawer-backdrop#drawerBackdrop` | **680px** (`.standard`), max 96vw | drawer 51 / backdrop 50 | `openDrawer(mode,id)` (L2381) / `openReplacement()` (L2394) | ✅ Esc (ถ้าไม่มี modal) · ✅ **backdrop click** `onclick=closeDrawer()` (L1588) · ✅ ปุ่ม close x / ยกเลิก / ปิด | L839-853 |
| **Modal** (picker/deactivate/archiveDraft) | `.modal` + `.modal-backdrop#modalBackdrop` | **440px** (L1075), max 92vw / 90vh | backdrop 60 (override) | `openModal(type,data)` (L1703) via confirmDeactivate/confirmArchiveDraft/openModal('picker') | ✅ Esc (ก่อน drawer) · ✅ **backdrop click** `onclick=closeModal()` (L1594); `.modal` มี `event.stopPropagation()` กันปิดเมื่อคลิกใน content (L1595) · ✅ ปุ่ม ยกเลิก/ปิด/× | L1058-1085 |
| **User menu** | `.user-menu#userMenu` | 240px | dropdown 40 | `toggleUserMenu()` (L1566) | ✅ click-outside (L1579-1583) · toggle ซ้ำ · **ไม่ผูก Esc** | L304-317 |
| **Search-select list** | `.ss-list` | auto (max 320px, `positionMenu`) | backdrop 50 | `ssOpen()` focus/input | ✅ Esc (`ssOnKey`, L1875 — ปิด list เท่านั้น) · ✅ click-outside (L1877) · ✅ เลือก option | L539 / L1805 |
| **Tooltip** | `.info-tip::after` | max 340px | dropdown 40 | CSS `:hover` | hover ออก (pure CSS) | L1302-1308 |
| Toast | `.toast#toast` | max 380px | toast 80 | `showToast()` (L1720) | auto-hide `durationMs` (default 2800) — **ไม่ dismiss ด้วย click/Esc** | L1148-1174 |

**Backdrop:** drawer `rgba(17,17,17,0.40)` (L832) · modal `rgba(17,17,17,0.50)` (L1062)
**Scroll lock:** ❌ **ไม่มี** — ไม่พบ `body.no-scroll`/`overflow:hidden` toggle ที่ open overlay (มีเพียง `scrollbar-gutter:stable` กัน jank, L64) → ดู Drift D-05
**Animation:** drawer `transform translateX(100%)→0` 280ms cubic-bezier (L847/852) · modal `scale(0.96)→1` 200ms (L1080-1085) · toast `translateY(100px)→0` 250ms (L1164-1169) — ทั้งหมดสั่งผ่าน `requestAnimationFrame` add class `is-open`/`is-visible` (L1691/1706/1726)

---

## §7 · Interaction Spec

### 7.1 ⭐ Esc chain (ตามลำดับ handler จริง)
`window keydown` (L1733-1738):
```
if (e.key === 'Escape') {
  if (state.modal.open)      closeModal();   // 1st — modal ก่อน
  else if (state.drawer.open) closeDrawer();  // 2nd — แล้วค่อย drawer
}
```
- **ลำดับ:** modal → drawer (จาก confirm modal ที่เปิดทับ drawer, ปิด modal ก่อน 1 ครั้ง, กด Esc อีกที ปิด drawer). ตรงกับ z-order (modal 60 > drawer 51)
- `closeModal()` มี **2 นิยาม** — ตัว page-specific (L2074) override ตัว base (L1710); ตัว page set `state.modal={open:false...}` **ทันที** (L2077) เพื่อให้ Esc ติด ๆ กันปิด modal แล้วปิด drawer ได้โดยไม่ค้าง stale 200ms (comment L2072-2073)
- **Quirk (verified):** `ssOnKey` Escape (L1875) ปิด ss-list แต่ **ไม่ `stopPropagation`** → กด Esc ขณะ combobox เปิดอยู่ใน drawer จะทำให้ window handler ทำงานต่อ → ปิด drawer ไปด้วย (combobox ปิด + drawer ปิดพร้อมกัน). ดู Drift D-06
- User menu / tooltip / toast **ไม่อยู่ใน Esc chain**

### 7.2 Click-outside
- Modal/Drawer: backdrop `onclick` (L1588/1594) — drawer backdrop เป็น element แยกใต้ drawer; modal คลิกนอก `.modal` (มี stopPropagation ที่ content)
- User menu: `document click` ถ้าไม่ใช่ `.user-chip`/`.user-menu` → remove `is-open` (L1579)
- Search-select: `document click` ถ้านอก `#ss-<key>` → ปิด (L1877)
- Base-kit `data-overlay`: `document click` outside → `closeOverlay` (L2055) — **ไม่มี element `[data-overlay]` ในหน้านี้** (generic util เฉย ๆ)

### 7.3 Focus management
- `openDrawer`/`openReplacement`: หลัง RAF → focus `#drawer input:not([disabled])` ตัวแรก (L2391/2408)
- `closeOverlay` (base): คืน focus ให้ `_trigger` (L2054) — ไม่ใช้ในหน้านี้
- `ssClear`: คืน focus ให้ input (L1869)
- **Render preservation (Iron Rule #29):** `render()` wrap ด้วย `preserveRenderState()`/`restoreRenderState()` (L2253/2270) — เก็บ/คืน scrollTop ของ .drawer-body, .modal-body, window + focus+selection ของ input ที่กำลังพิมพ์ (match ด้วย placeholder+type+name, L1957-1999) กัน "เด้งกลับบน" ตอน re-render
- Modal close button ถูก inject หลัง render ถ้ายังไม่มี (L2262-2265)

### 7.4 Positioning strategy
- Sidebar/shell-bar/drawer/modal-backdrop/toast/drawer-backdrop = `position:fixed` (ยึด viewport, overlay ไม่ scroll ตามเนื้อหา)
- Shell-bar = `position:sticky top:0` (L233)
- `.ss-list` = `position:absolute` overlay ไม่ดันเนื้อหา (L539, comment L1778) + `positionMenu` คำนวณ flip drop-up (L2048-2051)
- User menu = `position:absolute` anchored `top:calc(shell-h - 4px) right:22px` (L306-307)

### 7.5 Drag / pan / zoom
- ❌ **ไม่มี (—)** — ไม่มี drag/pan/zoom/threshold logic ในไฟล์นี้

### 7.6 Keyboard อื่น ๆ
- KPI stat: `onStatusFilterKey` Enter/Space → setStatusFilter (L1573)
- User chip: `onUserMenuKey` Enter/Space → toggleUserMenu (L1567)
- Combobox: ↑↓/Enter/Esc (L1870-1876)

---

## §8 · State-Driven UI Matrix

### 8.1 Record status enum → pill/label/สี (L2208-2213)
| status | pill class | label | สี (ci) | ปุ่ม action ที่โผล่ |
|---|---|---|---|---|
| `active` | `pill-info` | ใช้งาน | info (ฟ้า) | แก้ไข(update) + ปิดใช้งาน(deactivate, power) |
| `draft` | `pill-muted` | ร่าง | เทา | แก้ไข(update) + เก็บร่างถาวร(deactivate, archive) |
| `inactive` | `pill-muted` | ปิดใช้งาน | เทา | แก้ไข(update) เท่านั้น |
| `archived` | `pill-muted` | เก็บถาวร | เทา | แก้ไข(update) เท่านั้น |
> Footer actions ต่อ status: view drawer L2708-2713 · row actions L2306-2308

### 8.2 Filter status enum (L2340-2348 + getFiltered L2232-2247)
`all` (ทุกสถานะ) · `pickable` (พร้อมใช้วันนี้ = isPickable) · `attention` (draft|inactive|archived) · `active` · `draft` · `inactive` · `archived`

### 8.3 Form field visibility ต่อ family/direction/vatKind
| เงื่อนไข | field ที่แสดง | anchor |
|---|---|---|
| family=VAT | ประเภท VAT (standard/zero/exempt) + ทิศทาง select (both/sale/purchase) | L2438-2468 |
| family=WHT | ทิศทาง = disabled "จ่าย (หัก ณ ที่จ่าย)" + ประเภทเงินได้ combobox | L2470/2475 |
| VAT dir=both | GL ภาษีขาย + GL ภาษีซื้อ | L2486-2491 |
| VAT dir=sale | GL ภาษีขาย เท่านั้น | L2487 |
| VAT dir=purchase | GL ภาษีซื้อ เท่านั้น | L2490 |
| WHT | GL — WHT ค้างจ่าย (WHT_PAYABLE เท่านั้น) | L2493 |
| VAT zero/exempt | rate disabled + forced 0 (exempt→placeholder "ยกเว้น — ไม่มีอัตรา") | L2449-2454/2563 |
| used>0 (edit) | code/family/vatKind/rate/direction = **disabled** + ป้าย "อ่านอย่างเดียว" (lock) + tc-alert "สร้างรหัสแทน" | rateLocked L2424, L2453/2500 |
| replacement | prefill code+"-N" + name "(อัตราใหม่)" + replNote alert | openReplacement L2394-2401 |

### 8.4 family switch side-effects — `onFamilyChange()` (L2548-2559)
- → WHT: `vatKind=null, direction='pay', reportMappingRule='RESOLVE_BY_PAYEE_AND_PAYMENT_CONTEXT', rate 7→3`
- → VAT: `vatKind='standard', vatReportCategory='STANDARD', direction='both', reportMappingRule=null`
- `onVatKindChange()` (L2560): set vatReportCategory + zero/exempt→rate=0, standard→7

### 8.5 vatReportCategory mapping (L2173/2445/2562)
standard→`STANDARD` · zero→`ZERO_RATED` · exempt→`EXEMPT` (แสดงเป็น `.ro-tag` "หมวดรายงาน: X", L2445)

### 8.6 incomeCategoryCode mapping (WHT, L2166-2168/2583)
ค่าขนส่ง→TRANSPORT · ค่าโฆษณา→ADVERTISING · ค่าบริการ/รับจ้างทำของ→SERVICE · ค่าเช่า→RENT · ค่าวิชาชีพอิสระ→PROFESSIONAL · ค่าสิทธิ→ROYALTY · ดอกเบี้ย→INTEREST · เงินปันผล→DIVIDEND · else→OTHER

### 8.7 Picker state (P-04) — context × date
| context | VAT group | WHT group | anchor |
|---|---|---|---|
| SALES | direction sale/both | (ไม่แสดง) | L2792/2809 |
| PURCHASE | direction purchase/both | WHT (advisory: pill-warning "แนะนำ · ยืนยันตอนจ่าย", capture ถูก block) | L2793/2798-2800/2822 |
| PAYMENT | (ไม่แสดง) | WHT (capture ได้จริง) | L2796/2810 |
- `isPickable()` (L2219): company + active + effStart≤date≤effEnd
- Empty group → `— ไม่มี —` (L2809/2810)
- Snapshot card หลัง capture (L2811): code/name/context/rate/documentDate + code chip

### 8.8 Submitting state — `state.submitting` (L2190/2505/2676)
false→ปุ่มปกติ · true→ปุ่ม disabled + spinner "กำลังบันทึก…" (650ms fake latency L2684)

### 8.9 List states
- Loaded (มี rows) · filter-empty (`ไม่พบรายการที่ค้นหา`, L2293)
- Loading/skeleton = **ไม่มี (—)** — render synchronous, in-memory
- No-data empty = **ไม่มี trigger (—)** (records seed คงที่ 9 แถว)

---

## §9 · Microcopy (VERBATIM — R2)

### 9.1 Toasts — ทุก `showToast()` call (grep-verified 8 unique strings)
| ข้อความ (verbatim) | variant | trigger | anchor |
|---|---|---|---|
| `คุณไม่มีสิทธิ์บันทึกรหัสภาษี` | warning | saveDraft no-perm | L2664 |
| `กรุณากรอกรหัสและชื่อก่อนบันทึกร่าง` | warning | saveDraft invalid | L2665 |
| `บันทึกร่างแล้ว` | info | saveDraft สำเร็จ | L2669 |
| `คุณไม่มีสิทธิ์สร้างหรือเปิดใช้รหัสภาษี` | warning | submitForm no-perm | L2673 |
| `กรุณากรอกข้อมูลให้ครบถ้วน` | warning | submitForm invalid | L2674 |
| `บันทึกการแก้ไขแล้ว` / `สร้างรหัสภาษีสำเร็จ` | success | submitForm สำเร็จ (edit/create, `msg` L2680) | L2680/2683 |
| `เก็บร่างถาวรแล้ว` / `ปิดใช้งานรหัสภาษีแล้ว` | success | doArchive (wasDraft ternary) | L2765 |
| `รหัสนี้เลือกไม่ได้ตามวันที่เอกสาร` | warning | captureSnapshot not pickable | L2821 |
| `WHT ในเอกสารซื้อเป็นเพียงคำแนะนำ โปรดยืนยันตอนจ่าย` | warning | captureSnapshot WHT+PURCHASE | L2822 |
| `เลือกและบันทึก snapshot ในเอกสารแล้ว` | success | captureSnapshot สำเร็จ | L2824 |

### 9.2 Buttons / actions (verbatim)
- `ดูรายการที่เลือกได้ในเอกสารใหม่` (L2320) · `สร้างรหัสภาษี` (L2321) · `ล้างตัวกรอง` (L2349/2293)
- Tabs: `ภาษีมูลค่าเพิ่ม (VAT)` (L2333) · `หัก ณ ที่จ่าย (WHT)` (L2334)
- Form footer: `ยกเลิก` (L2538) · `บันทึกร่าง` (L2540) · `กำลังบันทึก…` (L2506) · `ยืนยันสร้าง`/`บันทึกการแก้ไข` (`submitLabel` L2504)
- Form eyebrow/title: `รหัสภาษีใหม่`/`แก้ไขรหัสภาษี`/`สร้างรหัสแทน` (L2425) · `แก้ไข <code>`/`สร้างรหัสภาษี` (L2426)
- View actions: `แก้ไข` (L2708) · `ปิดใช้งาน` (L2710) · `เก็บร่างถาวร` (L2712) · `ปิด` (L2748)
- Rate lock: `<i lock>อ่านอย่างเดียว` (L2453) · `สร้างรหัสแทน (เปลี่ยนอัตรา + วันมีผล)` (L2501)
- Picker rows: `เลือกและบันทึกค่า` (L2800) · pill `แนะนำ · ยืนยันตอนจ่าย` (L2800)

### 9.3 Placeholders
- ค้นหา list: `ค้นหารหัส / ชื่อ / ประเภทเงินได้` (L2339)
- code: `เช่น VAT7, WHT3` (L2520) · name: `ชื่อที่แสดงบนเอกสาร` (L2521)
- rate: `เช่น 7` / (exempt) `ยกเว้น — ไม่มีอัตรา` (L2454)
- combobox glSale/glPurchase/glWht: `ค้นหาบัญชีจากผังบัญชี...` (L2487/2490/2493) · incomeType: `เลือกประเภทเงินได้...` (L2478)

### 9.4 Validation errors (verbatim, `validateForm()` L2592-2616) — pair 05_RULES VR01-VR13
| ข้อความ | field | anchor |
|---|---|---|
| `กรุณากรอกรหัส` | code required | L2594 |
| `รหัสนี้มีอยู่แล้วในบริษัทปัจจุบัน` | code dup (case-insensitive) | L2597 |
| `กรุณากรอกชื่อ` | name required | L2599 |
| `กรุณากรอกอัตรา` | rate required (activate) | L2602 |
| `อัตราต้องอยู่ระหว่าง 0 ถึง 100` | rate range | L2603 |
| `WHT ต้องระบุประเภทเงินได้` | incomeType (WHT activate) | L2604 |
| `ต้องเลือกบัญชี GL กลุ่มภาษีขายก่อนเปิดใช้งาน` | glSale | L2606 |
| `ต้องเลือกบัญชี GL กลุ่มภาษีซื้อก่อนเปิดใช้งาน` | glPurchase | L2607 |
| `ต้องเลือกบัญชี GL กลุ่มภาษีหัก ณ ที่จ่ายค้างจ่ายก่อนเปิดใช้งาน` | glWht | L2609 |
| `กรุณาระบุวันมีผลเริ่ม` | effStart (activate) | L2611 |
| `วันสิ้นสุดต้องไม่ก่อนวันเริ่ม` | effEnd < effStart | L2613 |

### 9.5 Empty / hint / meta / alerts
- filter-empty: `ไม่พบรายการที่ค้นหา` / `ลองปรับคำค้นหรือล้างตัวกรอง` (L2293)
- combobox no-match: `ไม่พบรายการ` (default `emptyText` L1812)
- used cell: `ใช้แล้ว N เอกสาร` / `ยังไม่ถูกใช้` (L2226-2227)
- eff: `ไม่มีกำหนด` (ไม่มี effEnd, L2216/2303) · null format: `—` (fmt helpers L1888-1896)
- page sub: `Master รหัสภาษีที่ทุกเอกสารการเงินอ้างอิง — VAT (ขาย/ซื้อ) และ ภาษีหัก ณ ที่จ่าย (WHT)` (L2317)
- KPI meta: `VAT n · WHT n` / `สถานะใช้งาน และวันนี้อยู่ในช่วงวันมีผล` / `ร่างรอผูก GL · ปิดใช้แล้ว` / `เก็บประวัติและ snapshot เสมอ` (L2326-2329)
- table footer: `แสดง X จาก Y รหัสในกลุ่ม VAT/WHT` (L2354)
- replNote: `กำลังสร้างรหัสแทนของ <code> — กำหนดอัตราและวันมีผลใหม่ รหัสเดิมยังคงอยู่และเอกสารเก่ายังอ้างอิงได้ตามปกติ` (L2497)
- rateReplace alert: `รหัสนี้ถูกใช้ใน N เอกสารแล้ว — แก้อัตราในรหัสเดิมไม่ได้` (L2501)
- ro-tag: `หมวดรายงาน: STANDARD/ZERO_RATED/EXEMPT` (L2445)

### 9.6 Modal microcopy
- picker: title `ตัวเลือกตามวันที่เอกสาร` (L2805) · label `นำไปใช้กับ` (L2807) options `เอกสารขาย (SO / AR Invoice)` / `เอกสารซื้อ (PO / AP Invoice)` / `ใบสำคัญจ่าย (ยืนยัน WHT)` · label `วันที่เอกสาร` · group `VAT ที่ใช้ได้` / `WHT ที่แนะนำ`|`WHT ที่ยืนยันตอนจ่าย` (L2810) / `Snapshot ที่บันทึกในเอกสาร` (L2811)
- archiveDraft: title `เก็บร่างถาวร?` · subtitle `"<code>" จะไม่แสดงในรายการทำงานปกติ แต่ระบบยังคงข้อมูลและประวัติไว้เพื่อการตรวจสอบ` · alert `ระบบไม่มีการลบถาวรสำหรับรหัสภาษี` (L2774-2776)
- deactivate: title `ปิดใช้งานรหัสภาษี?` · subtitle `"<code>" จะไม่แสดงในตัวเลือกของเอกสารใหม่ เอกสารเดิมที่อ้างอิงอยู่ยังใช้งานได้ตามปกติ` · alert `สามารถเปิดใช้งานใหม่ได้ภายหลังจากหน้าแก้ไข` (L2782-2784)

### 9.7 Audit action templates (verbatim — เก็บเป็น log template)
- `สร้างและเปิดใช้งานรหัสภาษี` (activate create, L2679) · `บันทึกการแก้ไขและเปิดใช้งาน` (edit activate) · `บันทึกร่าง — รอผูกบัญชี GL` / `แก้ไขและบันทึกเป็นร่าง` (L2667) · `เก็บร่างถาวร — คงข้อมูลและประวัติไว้` / `ปิดใช้งาน — ไม่แสดงในเอกสารใหม่` (L2762) · `สร้างรหัสแทน <code> (อัตรา N%) มีผล <date>` (L2650)

---

## §10 · Data Binding & BACKEND anchors

> **สำคัญ:** HTML **ไม่มี** `// BACKEND:` comment marker เลย (grep = 0). ข้อมูลทั้งหมดเป็น in-memory mock (`state.records` L2119). จุด plug API map จาก FRD 02_API + call site จริง:

| UI action / call site | mock ปัจจุบัน | FRD API ที่ต้อง plug |
|---|---|---|
| list/tab/filter/sort (`getFiltered` L2232) | filter `state.records` | GET F-TAX-API-01 `/tax-codes?family=&status=&q=` |
| row click (`openDrawer('view')`) | `findRec(id)` L2194 | GET API-02 `/tax-codes/:id` (+lineage) |
| combobox GL (`postRender` L2575-2581, `glOptions` L2102) | `GL_ACCOUNTS` filter tax_role (L2090-2101) | GET API-11 `/gl-accounts?tax_role=` |
| combobox incomeType (L2582) | `INCOME_TYPES` (L2107-2116) | GET API-12 `/income-types` |
| saveDraft (`commitForm('draft')` L2634/2663) | push/assign `state.records` | POST API-03 mode=draft / PUT API-04 |
| submitForm activate (`commitForm('active')` L2679) | 650ms setTimeout mock | POST API-03 mode=activate / API-05 activate |
| openReplacement + commit (L2394/2645) | set replacedBy + effEnd | POST API-08 `/replacement` |
| doArchive (L2757) | set status inactive/archived | POST API-06 deactivate / API-07 archive |
| audit timeline (`renderViewDrawer` L2703) | `r.audit[]` in-record | GET API-10 `/:id/audit` (gated view_audit) |
| picker (`renderModal('picker')` + `isPickable` L2219) | client filter | GET API-09 `/tax-codes/pickable?context=&document_date=` |
| captureSnapshot (L2820) | client snapshot object | consumer-side POST (ไม่ใช่ endpoint นี้ — 02_API §2.X) |

**Mock data structures:**
- `GL_ACCOUNTS` (L2090) filtered `companyId===COMP-001 && status==='active' && postingAllowed` (L2101) → เหลือ GL-001..008 (GL-099 inactive, GL-X01 คนละบริษัท ถูกกรองออก)
- Record shape (L2121-2178): id/code/name/family/vatKind/rate/direction/glSale/glPurchase/glWht/incomeType/effStart/effEnd/status/used/audit[] + derived (isSystemPreset/vatReportCategory/incomeCategoryCode/reportMappingRule/replaces/replacedBy)
- `formToPayload()` (L2617) = shape ที่ควรส่ง API (snake_case mapping ทำที่ dev จริง)

---

## §11 · Traceability + Drift Log (R6)

### 11.1 Page ↔ FRD P-xx ↔ HTML
| Brief § | FRD (01_UI) | HTML anchor | สถานะ |
|---|---|---|---|
| §4 P-01 list | P-01 renderList | `renderPage()` L2280 | ✅ (FRD เรียก `renderList()`/`renderList` — ชื่อจริง `renderPage()` → D-01) |
| §4 P-02 form | P-02 form drawer 680 | `renderFormDrawer()` L2420 | ✅ |
| §4 P-03 view | P-03 view drawer | `renderViewDrawer()` L2688 | ✅ |
| §4 P-04 picker | P-04 modal 440 | `renderModal('picker')` L2787 | ✅ |
| §4 P-05 confirm | P-05 confirm modal | `renderModal('deactivate'/'archiveDraft')` L2771/2779 | ✅ |

### 11.2 Action ↔ API ↔ HTML
| Action | FRD API | HTML fn |
|---|---|---|
| list/filter | API-01 | getFiltered L2232 |
| detail | API-02 | openDrawer('view') L2297 |
| create draft/activate | API-03 (+05) | saveDraft/submitForm L2663/2671 |
| edit | API-04 (+05) | submitForm edit L2671 |
| activate | API-05 | commitForm('active') L2679 |
| deactivate | API-06 | doArchive (active) L2757 |
| archive draft | API-07 | doArchive (draft) L2757 |
| replacement | API-08 | openReplacement L2394 |
| pickable | API-09 | renderModal picker / isPickable L2219 |
| audit | API-10 | audit timeline L2703 (gated) |
| GL lookup | API-11 | glOptions L2102 |
| income types | API-12 | INCOME_TYPES L2107 |

### 11.3 Rule ↔ HTML (BR/VR)
- VR01-VR13 → `validateForm()` L2594-2613 + captureSnapshot L2822 (verbatim ตรง 05_RULES §5.4 ✅)
- BR-TAX-01 dup → L2596-2597 · BR-02 rate lock → rateLocked L2424 + openReplacement · BR-03 WHT income → L2604 · BR-04/06/07 GL role → isAllowedGL L2103/2606-2609 · BR-05 no hard delete → doArchive soft L2760 (ไม่มี DELETE) · BR-07 WHT→WHT_PAYABLE เท่านั้น → glOptions('WHT_PAYABLE') L2581 · BR-08/09 pickable → isPickable L2219 · BR-10 vat category → onVatKindChange L2562 · BR-11 WHT report rule → reportMappingRule const L2552

### 11.4 ⚠️ DRIFT LOG
**HTML-only (มีใน HTML, FRD ไม่ครอบ/ต่าง):**
| # | รายการ | anchor | ข้อเสนอ |
|---|---|---|---|
| D-01 | FRD 01_UI เรียกฟังก์ชัน list ว่า `renderList()`/L2313; ชื่อจริง = `renderPage()` L2280 (L2313 คือกลาง body string ไม่ใช่ def) | L2280 | แก้ FRD ให้ตรงชื่อ |
| D-02 | KPI ใบที่ 4 จริง = "ถูกอ้างอิงแล้ว" (nUsed, static) — FRD §1.2 P-01 บอก "active-no-GL health" | L2329 | แก้ FRD |
| D-06 | Esc ใน combobox ปิด drawer พร้อมกัน (ss Esc ไม่ stopPropagation) | L1875 vs L1733 | ดู §13 ข้อเสนอ (bug UX) |

**FRD-only (FRD ระบุ, HTML ไม่มี):**
| # | รายการ | FRD | ข้อเสนอ |
|---|---|---|---|
| D-03 | No-data empty `ยังไม่มีรหัสภาษี` + CTA | 01_UI §1.6 / §1.2 P-01 States | HTML seed คงที่ ไม่มี trigger; dev ระบบจริงต้อง implement (มี `emptyStateHTML` helper พร้อม) |
| D-04 | Loading skeleton state | 01_UI §1.2 P-01 States | HTML render synchronous ไม่มี skeleton; dev ต้องเพิ่มตอนต่อ API async |
| D-05 | (system) scroll-lock ตอนเปิด overlay | (best practice, ไม่ระบุใน FRD ตรง ๆ) | HTML ไม่ lock body scroll; พิจารณาเพิ่ม |
| D-07 | Idempotency-Key / If-Match / optimistic lock / 409 handling | 02_API §2.3 / 05_RULES EC-15 | เป็น backend contract — UI ยังไม่มี handling 409 ERR_STALE_DATA (ไม่มี toast/retry) |
| D-08 | SoD จริง (Maker≠Approver) | 05_RULES §5.3 OQ-3 | mock user ถือครบ 6 สิทธิ์ (L2067) — permission gating มีจริง (`can()` L2071) แต่ demo ไม่บังคับ role แยก |
| D-09 | API 403/500 error microcopy (`คุณไม่มีสิทธิ์เข้าถึงส่วนนี้` / `เกิดข้อผิดพลาด กรุณาลองใหม่`) | 01_UI §1.6 | HTML มีเฉพาะ toast no-perm ฝั่ง client; error page/500 handling ยังไม่มี |

> ไม่มี business drift ที่ต้องส่ง `html-to-frd-sync` — ส่วนใหญ่เป็น backend contract ที่ prototype (in-memory) ไม่ครอบโดยเจตนา + naming/label mismatch เล็กน้อย

---

## §12 · Diff จากเวอร์ชันก่อน
— ไม่มี HTML เวอร์ชันเก่าให้เทียบใน task นี้ (skip)

---

## §13 · 💡 ข้อเสนอ (ไม่ใช่ AS-BUILT)

> ที่เดียวที่อนุญาตให้เสนอเพิ่ม (R1) — **ไม่ใช่สเปคที่มีในโค้ด**

1. **[D-06 bug UX] combobox Esc ทะลุปิด drawer** — `ssOnKey` case Escape (L1875) ควรเพิ่ม `e.stopPropagation()` เพื่อให้ Esc ครั้งแรกปิดแค่ combobox list ไม่ให้ window handler (L1733) ปิด drawer ต่อ
2. **Scroll lock (D-05)** — เพิ่ม toggle `body{overflow:hidden}` ตอน drawer/modal open กัน background scroll (มี `scrollbar-gutter:stable` รองรับอยู่แล้วกัน jank)
3. **No-data / loading state (D-03/D-04)** — เมื่อต่อ API จริง ควร render skeleton + no-data empty ที่มี CTA "สร้างรหัสภาษี" (helper `emptyStateHTML` L1917 พร้อมใช้)
4. **409 / optimistic-lock UI (D-07)** — เพิ่ม handling `ERR_STALE_DATA` (toast + reload record) และ inline dup ตอน create ชนกัน (E14) ฝั่ง server-response
5. **Reason/ticket field ตอน activate/deactivate** — 05_RULES §5.7 D15 (S11-02) แนะนำ; HTML ยังไม่มี field
6. **User menu / notif เข้า Esc chain** — ปัจจุบัน `toggleNotif()` เป็น no-op (L1584) และ user-menu ปิดด้วย click-outside เท่านั้น

---

## 🔍 UI Brief Verification — F-TAX Tax Code (Phase 4 Gate, R8)

```
- [x] ทุก route ใน HTML มี section                      1/1 real (+2 external stub ระบุชัด)  ✅
- [x] ทุก modal/drawer/popover มีแถวใน Overlay Registry  6/6 (drawer, modal, user-menu, ss-list, tooltip, toast) ✅
- [x] ทุก showToast ปรากฏใน Microcopy verbatim          10/10 call sites (grep L2664..2824) ✅
- [x] ทุก component ใน anatomy มี selector anchor         ✅ (§4 tree + §5 ทุกตัวมี Lxxxx)
- [x] state matrix ครอบทุกค่า enum                       ✅ status(4) / filter(7) / family×dir×vatKind / picker ctx(3) / submitting
- [x] Esc chain ตรงลำดับ handler จริง                     ✅ modal→drawer (L1733-1738) + quirk ss (L1875) ระบุ
- [x] z-index map ครบทุกตัวที่ประกาศ                      7/7 tokens (L1316 + override L1321) ✅
- [x] (FRD) ทุก P-xx มีแถว traceability + Drift ไม่เงียบ  P-01..05 ✅ · Drift 9 รายการ (3 HTML-only + 6 FRD-only) ✅
- [x] ไม่มีสเปคที่ trace ไม่ได้ (R1) — sample audit 10 จุด  ✅ (ดูด้านล่าง)
```
**Sample audit 10 claims → anchor:**
1. drawer 680px → L853 ✅ · 2. modal 440px → L1075 ✅ · 3. z-toast 80 → L1316 ✅ · 4. toast "บันทึกร่างแล้ว" → L2669 ✅ · 5. Esc modal-first → L1735 ✅ · 6. WHT→WHT_PAYABLE → L2581 ✅ · 7. rate lock used>0 → L2424 ✅ · 8. dup error text → L2597 ✅ · 9. default route redirect → L2086 ✅ · 10. isPickable logic → L2219-2223 ✅

**VERDICT: PASS (FAIL = 0)**

---
*Handoff set: HTML (source of truth) + FRD_F-TAX_Pack (ระบบ) + UI Brief นี้ (design intent). งาน manual ที่เหลือ: dev ต่อ API ตาม §10 + จัดการ Drift D-03/D-04/D-07/D-09 ฝั่ง production.*
