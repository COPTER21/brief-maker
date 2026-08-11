# UI Brief — F-PAY เงื่อนไขชำระเงิน (Payment Terms)

> **ประเภท:** HTML UI Brief (AS-BUILT, extraction-based) · WF-01 · หลัง FRD (SOW3.3) — ก่อน dev handoff
> **หลักการ:** ทุกบรรทัดในบรีฟนี้ trace กลับหา selector / function / ข้อความจริงใน HTML ได้ (R1). ห้ามแต่งสเปคที่ไม่มีในไฟล์ — ข้อเสนอเพิ่มอยู่ §13 เท่านั้น
> **Handoff set:** HTML (source of truth) + FRD Pack (ระบบ/สัญญา API) + **UI Brief (design intent นี้)**

---

## §0 · Document Control + Pairing

| Field | Value |
|---|---|
| Feature | F-PAY — เงื่อนไขชำระเงิน (Payment Terms) |
| HTML SoT | `01_HTML/f-payterm.html` · `<title>` = "เงื่อนไขชำระเงิน (Payment Terms) · CUBE NATIVE" |
| HTML footer version | Sidebar footer "Sandbox · v1.0.0" (L698) · CI comment "CUBE Warm Light (v8 rebrand 2026-08-09)" (L15) · PREFLIGHT v8 retrofit 2026-08-10 (L1484) |
| Arch | Single-file SPA, vanilla JS, string-template render · Lucide icons (CDN 3-fallback loader L742) · fonts: Satoshi (fontshare) + Noto Sans Thai/Inter (Google) |
| FRD Pack | `04_FRD/FRD_F-PAY_Pack/` (00–07 + INDEX) — paired |
| FRD status | **PAIRED** — traceability §11 ครบ P-01..05, API-01..08, BR-01..13. Drift Log §11.2 |
| use_in | **7 เอกสาร (NO PR)** — ยืนยัน D-08 / LD-F-01 / BR-06 (ดู §8.3) |
| DOA | **null placeholder** — ไม่มี approval UI (approver_role/approved_by/approved_at/approval_chain = null, set ตอน create L1144) |
| Recent fixes captured | ✅ white bulk bar (§5.6) · ✅ 2-line type dropdown (§5.4) · ✅ top-center toast + 5s error/warning (§6, §9) · ✅ disabled sidebar items ผังบัญชี/GL Posting Group (§3.1) · ✅ scroll-preservation Iron Rule #29 (§7.5) · ✅ inst-actions add+badge aligned (§5.9) |

---

## §1 · Design Tokens AS-BUILT

> สกัดจาก `:root` L14–40. **ห้าม hardcode hex** — dev ผูกผ่าน token เหล่านี้ (CI v8 Warm Light).

### 1.1 Color tokens (L16–32)
| Token | Value | ใช้ที่ |
|---|---|---|
| `--c-navy` / `--c-navy-2` | `#111111` | headings, toast default, hint tooltip bg |
| `--c-primary` | `#FF3B30` | brand red — ปุ่ม primary, active sidebar, pill/focus ring |
| `--c-primary-hover` | `#E62E24` | primary hover |
| `--c-teal` | `#FF9A1F` | accent orange — toggle-on, teal pills, pulse-dot |
| `--c-teal-light` | `#FFC46B` | — |
| `--c-ink` | `#111111` | body text |
| `--c-mute` / `--c-mute-2` / `--c-mute-3` | `#54565C` / `#73757B` / `#9A9CA2` | secondary/tertiary text |
| `--c-line` / `--c-line-2` / `--c-line-3` | `#DEDAD4` / `#E9E5E0` / `#F1EEEA` | borders (dark→light) |
| `--c-bg-off` | `#FAF8F5` | ivory page bg, thead, hover |
| `--c-success` | `#1F9D55` | (legacy toast; toast-host ใช้ #0F6E56) |
| `--c-warning` | `#E8870F` | warning |
| `--c-danger` | `#E62E24` | destructive |

> **หมายเหตุ:** `--c-navy` ถูก rebrand เป็นดำ (#111111) ไม่ใช่ navy จริง — ชื่อ token คงไว้เพื่อ backward-compat (CI comment L15). Semantic pill tints (asset/liability/equity/income/expense + status) ใช้ hex ตรง ~24 จุด = intentional (PREFLIGHT accepted residual L1488).

### 1.2 Layout / type / spacing / radius (L33–38)
- **Layout:** `--sidebar-w: 232px` · `--shell-h: 52px` · body `min-width: 1180px` (L49), html/body `min-width: 768px` (Iron Rule #97, L42)
- **Font scale:** `--fs-h1 22 · h2 17 · h3 15 · body 14 · sub 13 · meta 12 · cap 11 · kpi 28` (px)
- **Font family:** `'Noto Sans Thai','Satoshi',system-ui,sans-serif` (L44) — headings ใช้ Noto Sans Thai; code/mono ใช้ 'Satoshi',monospace (.acct-code, .sdd-opt-code)
- **Spacing:** `--sp-xs 4 · sm 8 · md 12 · lg 20 · xl 28`
- **Radius:** `--r-xs 4 · sm 6 · md 8 · lg 12 · full 999`
- **Scrollbar:** Iron Rule #49 — 5px, track transparent, thumb `rgba(17,17,17,0.18)` (L81–85)

### 1.3 Z-Index Map (L39 — สูง→ต่ำ)
| z | Token | Layer / selector | Note |
|---|---|---|---|
| **80** | `--z-toast` | `.toast-host`, `.toast` (L634) | top-center host |
| **60** | `--z-modal` | `.modal-backdrop` (L345) · `.sdd-panel` (L502) · `.menu` (L568) · `.sidebar.is-open` @≤1180 (L69) | ⭐ dropdown/menu ยกขึ้น z-modal = Iron Rule #95 Overlay Portal (กัน dropdown จมใต้ drawer) |
| **51** | `--z-drawer` | `.drawer` (L289) | |
| **50** | `--z-backdrop` | `.drawer-backdrop` (L287) · `.hint-i::after` tooltip (L471) | |
| **30** | `--z-dropdown` | `.user-menu` (L155) | |
| **20** | `--z-shell` | `.sidebar` (L90) · `.shell-bar` (L132) | |
| **10** | `--z-sticky` | sticky `thead th` (L66, L529 via inline) | |

---

## §2 · Route / Overlay Map

> **CD-01 (07_LOCKED):** ไม่มี hash router — single-view SPA + overlay function calls. Navigation = `openDrawer()`/`openModal()` mutate `state` แล้ว `render()`. "route (production)" = เส้นที่เสนอให้ dev ผูก hash 1:1 (จาก 01_UI §1.0).

| Surface | Trigger (observed) | Render fn | Route (production เสนอ) | Layer |
|---|---|---|---|---|
| **List** (P-01) | boot / `render()` | `renderPage()` → `#page-content` (L733) | `#/finance/payment-term` | in-page |
| **Create** (P-02) | `openDrawer('create')` (L980) | `renderForm(null)` (L1164) | `…/new` | `#drawerLayer` |
| **Edit** (P-03) | `openDrawer('edit',id)` (L1022,1338) | `renderForm(t)` | `…/:id/edit` | `#drawerLayer` |
| **View** (P-04) | `openDrawer('view',id)` (row click L1013) | `renderView(t)` (L1319) | `…/:id` | `#drawerLayer` |
| **Bulk-delete** (P-05) | `openModal('bulk-delete')` (L1047,970) | `renderModal()` (L1382) | modal overlay | `#modalLayer` |

**Overlay layer bootstrapping (Iron Rule #95, L1451–1454):** `#drawerLayer` / `#modalLayer` สร้าง dynamic ต่อท้าย `<body>` ครั้งแรกที่ `render()` เรียก · `#toastHost` สร้างครั้งแรกที่ `showToast()` (L1429) · `#overlay-root` static ท้าย body (L1483, ปัจจุบันไม่ถูกใช้).

**Refresh-safety:** ไม่มี URL persistence — reload = กลับ List เสมอ (mock state ใน memory). Dev ต้อง implement hash routing + deep-link ตาม production route.

---

## §3 · Layout Shell

### 3.1 Sidebar (`.sidebar`, L644–700) — width 232px, bg #111111, z-shell
- **Brand:** `.sb-brand` — logo gradient (red→orange) + "CUBE NATIVE" / "Finance"
- **Nav modules** (`toggleModule` L848 — collapse/expand, `data-expanded`):
  - **การเงิน (finance)** `data-expanded="true"`:
    - `ผังบัญชี` (coa) — **`.is-disabled`** title "ยังไม่พร้อมใช้งาน" (L660)
    - `GL Posting Group` (posting-group) — **`.is-disabled`** (L663)
    - `เงินไขชำระเงิน` (payment-term) — **`.is-active`** ← feature นี้ (L666)
    - `สมุดบัญชีแยกประเภท` (gl) — `.is-disabled` (L669)
  - **จัดซื้อ (procurement)** collapsed: PR, PO — ทั้งคู่ `.is-disabled`
  - **System** collapsed: Settings — `.is-disabled`
- **Active state:** `.sb-item.is-active` = bg primary + ::before red-on-red rail (L116–118)
- **Disabled state:** `.is-disabled` = opacity 0.4, cursor not-allowed, hover ไม่เปลี่ยน (L121–122)
- **Footer:** `.sb-footer` pulse-dot + "Sandbox · v1.0.0"

### 3.2 Shell bar (`.shell-bar`, L704–731) — sticky top, height 52px, bg #fff, z-shell
- `.nav-toggle` hamburger — `display:none` desktop, `inline-flex` @≤1180 (L67,74) → `toggleSidebar()` (L850)
- **Breadcrumb:** `การเงิน` › `เงื่อนไขชำระเงิน` (current)
- **Shell actions** (`.shell-actions` L525): bell `.icon-btn` + `.notif-dot` → `toggleNotif()` **no-op** (L851) · user-chip "Tadswan C. / Finance Lead · CUBE NATIVE" avatar "TC" → `toggleUserMenu()` → `#userMenu` (z-dropdown 30, items: My Profile / Preferences / — / Sign out danger)

### 3.3 Main + content
`.main` margin-left 232px (0 @≤1180) · `.content` = flex column, `height: calc(100vh - topbar)`, overflow-y auto (Iron Rule #96 List Full-Height, L61). `#page-content` = render target.

### 3.4 Responsive (Iron Rule #97, L68–75, @max-width 1180)
- sidebar → off-canvas `translateX(-100%)`, `.is-open` reveal + scrim `box-shadow 0 0 0 100vmax rgba(17,17,17,0.35)`, z-modal
- `.main` margin-left 0 · `.content` padding 16px · `.drawer` → `min(680px,100vw)` · hamburger แสดง

---

## §4 · Page Anatomy

### P-01 List (`renderPage` L936–1007)
```
.content #page-content
├─ .ph  → .ph-title "เงื่อนไขชำระเงิน" + .ph-count "{N} เงื่อนไข"
├─ .stats (grid 4)  → 4× .stat button (statBtn L948) : ทั้งหมด/ใช้งาน/ไม่ใช้งาน/ร่าง  [§5.2]
├─ .bulkbar (conditional selN>0)  → white bulk bar  [§5.6]
└─ .card
   ├─ .card-toolbar → title "Payment Terms" | .card-toolbar-actions → btn-primary "เพิ่มเงื่อนไข" (openDrawer('create'))
   ├─ .filter-bar → .search-box (onSearch) + .filter-type-w (sdd 'filterType')  [§5.3, §5.4]
   ├─ .tbl-scroll → table.data-table (7 col, colgroup fixed)  [§5.5]
   │     thead: checkbox·รหัส·ชื่อเงื่อนไข·ประเภท·สรุปเงื่อนไข·สถานะ·จัดการ
   │     tbody: renderRow× (L1009) | empty-row "ไม่พบเงื่อนไขที่ตรงกับการค้นหา"
   └─ .table-foot → caption + "แสดง {n} จาก {m} เงื่อนไข"
```

### P-02/P-03 Create/Edit drawer (`renderForm` L1164–1313) — 680px
```
.drawer
├─ .drawer-header → avatar(icon|plus) + title(แก้ไข|เพิ่ม…) + subtitle(code|hint) + X
├─ .drawer-body
│  ├─ section "ข้อมูลทั่วไป" → code / name TH / name EN / ประเภท (sdd 'type')
│  ├─ section "การตั้งค่าเฉพาะประเภท" → typeFields (แปรตาม 7 type) + Due basis (ยกเว้น direct)  [§8-state matrix]
│  ├─ section "การใช้งานในเอกสาร" + chk-count "{n} เลือก" → chk-groups 2 กลุ่ม (P2P/S2C)  [§5.7]
│  └─ section "ตั้งค่าทั่วไป" → status select(3) + toggle "ตั้งเป็นค่า Default"
└─ .drawer-footer → "ยกเลิก" | spacer | "บันทึกและสร้าง"|"บันทึกการแก้ไข" (submitTerm)
```

### P-04 View drawer (`renderView` L1319–1368) — 680px
```
.drawer
├─ .drawer-header → avatar(type icon) + name + [code · type-pill] + actions:
│     "แก้ไข"(secondary) · "เปลี่ยนสถานะ"(secondary → #statusMenu) · divider · X
├─ .drawer-body
│  ├─ .bm-card "สรุปเงื่อนไข" → termSummary(t)
│  ├─ section "รายละเอียดการคำนวณ" → dv-rows ต่อ type + "นับจาก"(due_basis) + "WH/GRN/Ship trigger"(ยกเว้น direct)
│  ├─ section "การใช้งานในเอกสาร" → use-tags + Default indicator
│  └─ section ชื่อ (EN) (ถ้ามี)
└─ .drawer-footer → meta "ใช้ใน PO / SO / Invoice" | "ปิด"
```

### P-05 Bulk-delete modal (`renderModal` L1384–1393) — 440px
```
.modal
├─ .modal-header → icon danger(trash-2) + title "ลบเงื่อนไขชำระเงิน" + subtitle "เลือกไว้ {N} รายการ · {M} รายการถูกใช้งานอยู่จะถูกข้าม" + X
├─ .modal-body → "ยืนยันการลบออกจากทะเบียน — รายการที่ถูกใช้ในเอกสารแล้วจะไม่ถูกลบ"
└─ .modal-footer → "ยกเลิก" | "ลบ {D} รายการ"(danger, disabled ถ้า D=0)
```

---

## §5 · Component Inventory (anchor + states + ขนาด)

### 5.1 Buttons (`.btn` L176–189)
height 36px (btn-sm 30px) · variants: `.btn-primary` (red), `.btn-secondary` (white+border), `.btn-ghost`, `.btn-danger` (white/red→#FEE2E2 hover), `.btn-link`. States: default/hover (มี shadow บน primary) · disabled = ผ่าน `disabled` attr (inline opacity เช่น modal delete L1392, inst remove L1222). ไม่มี loading state (mock — PREFLIGHT accepted residual "mock-submit-no-loader" L1485).

### 5.2 Stat cards (`.stat` button, `statBtn` L948)
4 ใบ grid (repeat(4,1fr) L582). โครง: `.stat-label`(icon+label) / `.stat-value`(count) / `.stat-meta`. **Interactive filter** → `quickFilter(key)` (L1031). States: default · hover (border-color) · **`.is-on`** = border primary + inset ring (active filter). `all` reset ทั้ง type+status; อื่น ๆ toggle-off status.
| key | label | meta |
|---|---|---|
| all | ทั้งหมด | ทุกประเภท · ทุกสถานะ |
| active | ใช้งาน | พร้อมใช้ในเอกสารซื้อ-ขาย |
| inactive | ไม่ใช้งาน | ซ่อนจากการเลือกใหม่ |
| draft | ร่าง | ยังไม่เปิดให้ใช้ |

### 5.3 Search box (`.search-box` L539)
flex max-width 340px, lead search icon, `.search-input` padding-left 32px. `oninput="onSearch(this.value)"` (L986). States: default · focus (border primary + ring L542). **Refocus behavior** — `onSearch` (L1029) เรียก `renderPageOnly()` แล้ว `inp.focus()` + `setSelectionRange(L,L)` เพื่อคง caret ปลายข้อความหลัง re-render.

### 5.4 Type filter dropdown (`searchDropdown('filterType')`, L988) ⭐ 2-line options
Master combobox (Iron Rule #94). Options = `[{value:'all',label:'ทุกประเภท'}]` + 7 type (`{value,label,sub:v.hint}`, L944). **2-line** render ผ่าน `.sdd-opt-main` + `.sdd-opt-sub` (L527–528, `sddOptsHtml` L882): บรรทัด 1 = label, บรรทัด 2 = hint (คำอธิบายสั้น). Panel z-modal 60 (portal). States: trigger default/hover/`.is-open` (border primary+ring, chevron rotate 180) · option hover/`.is-sel` (bg #FFF5F4 + check) · empty "ไม่พบรายการ" (L880). Search box ในหัว panel placeholder "ค้นหา…".

**sdd mechanics:** `toggleSdd` (L887) เปิด/ปิดโดย manipulate DOM เฉพาะตัวนั้น (ไม่ render ทั้งหน้า → กันกระตุก) + เก็บ `state._formScroll` = drawer-body.scrollTop · `sddRefreshList` (L902) อัปเดตเฉพาะ `.sdd-list` ตาม search · `onSddSearch` (L910) · `pickSdd`→`window[fn]` (L911) · click-outside handler (L916) ปิด + clear `_formScroll`. **Search filter** = label + code (`o.label+' '+(o.code||'')`).

### 5.5 Data table (`.data-table` L521, fixed layout)
colgroup fixed: col1 34px (checkbox), col2 140px (รหัส), col4 170px (ประเภท), col5 280px (สรุป), col6 120px, col7 120px. Rows height 58px. `.tbl-scroll` sticky thead (z-sticky). **7 columns:**
1. checkbox (select-all `toggleSelAll` L1037)
2. รหัส — `.acct-code` mono + `.def-star` (star) ถ้า `is_default` (title "ค่า Default")
3. ชื่อเงื่อนไข — bold + `.acct-name-en` (name_en)
4. ประเภท — `.pill {k.pill}` + icon + label (ตัด " (…)" ออก)
5. สรุปเงื่อนไข — `termSummary(t)` (L922)
6. สถานะ — `statusPill(t.status)` (L797), text-center
7. จัดการ — `.row-actions` → **ปุ่มแก้ไขเท่านั้น** (pencil, `openDrawer('edit')`) [ไม่มีปุ่มลบเดี่ยว — CD-02/VD-PDM]

Row states: default · hover (bg-off, cursor pointer) · **`.is-sel`** (checkbox ติ๊ก → `tr.is-sel td` bg #FFF6F5 L581). Row click (นอก checkbox/actions) → view drawer. `<td>` checkbox/actions มี `event.stopPropagation()`.
Empty: `<tr><td colspan="7"><div class="empty-row">ไม่พบเงื่อนไขที่ตรงกับการค้นหา</div>` (L998).
**ไม่มี pagination** ใน list นี้ (มี `.pagination` CSS แต่ไม่ render) — footer = caption + count เท่านั้น.

### 5.6 Bulk bar (`.bulkbar` L574) ⭐ WHITE
โผล่เมื่อ `selN>0` (L966), เหนือ card. **สีขาว** — `background:#fff; color:var(--c-ink); border:1px solid var(--c-line)` + shadow เบา (recent fix จากเดิม dark). โครง: `.bb-count` "เลือก {N} รายการ" + ปุ่ม (border, hover bg-off):
- "ใช้งาน" → `bulkSetStatus('active')`
- "ไม่ใช้งาน" → `bulkSetStatus('inactive')`
- "ร่าง" → `bulkSetStatus('draft')`
- "ลบ" `.is-danger` (border/text danger, hover #FEE2E2) → `bulkAskDelete()`
- spacer
- "ยกเลิก" → `state.bulkSel={}; render()`

### 5.7 Checkbox grid — use_in (`.chk-row` L621, `chk-groups` L1289) — 7 docs
2 กลุ่ม (`v.group`): "ฝั่งซื้อ (P2P)" / "ฝั่งขาย (S2C)". แต่ละ row: `.chk-box` (20px, on=primary+check) + `.chk-name` + `.chk-desc`(sub). States: default/hover · **`.is-on`** (border primary, bg #FFF5F4) · **`.is-disabled`** (opacity 0.5) + `.chk-na` "ไม่รองรับ" — ใช้กับ direct_payment ปิด po/quotation/so. `toggleUseIn(d)` (L1098). chk-count badge "{n} เลือก".

### 5.8 Toggle "ตั้งเป็นค่า Default" (`.chk-row` reuse, L1302)
ใช้ `.chk-row`/`.chk-box` แบบ checkbox (ไม่ใช่ `.toggle-track` sliding — อันนั้นมี CSS แต่ไม่ถูกใช้ในฟอร์มนี้). `toggleDefault()` (L1099). desc "ระบบเลือกอัตโนมัติในเอกสารใหม่ · มีได้ 1 รายการต่อประเภท".

### 5.9 Installment editor (`type==='installment'`, L1216–1241) ⭐
- `.inst-card` ต่องวด: head "งวด {i+1}" + ปุ่ม remove (trash-2, `removeInst` — disabled + opacity .3 เมื่อ ≤2 งวด L1222) · `.inst-desc` input · `.inst-grid2` → %input (min0 max100, `onInstPct`) + due_type (sdd `instdue__{i}`)
- **`.inst-actions` row (L1235):** `display:flex; justify-content:space-between` — ปุ่ม "เพิ่มงวด" (btn-ghost sm, `addInst`) **ซ้าย** + `.inst-total` badge **ขวา** (aligned baseline). Badge: `is-ok` (#E1F5EE) "รวม {t}% ✓" | `is-warn` (#FEF3C7) "รวม {t}% (ต้องเป็น 100%)". Live-update ใน `onInstPct` (L1104 patch textContent+class ตรง).
- field-error (hidden) "สัดส่วนงวดต้องรวมเป็น 100%".

### 5.10 Inputs / fields (`.field` L315, `fieldBlock` L1370)
`.input`/`.select` height 36px. `.field.is-invalid` → border danger + แสดง `.field-error` (L320–322). `fieldBlock` สร้าง id `fld-{name}` จาก `name="…"` หรือ `data-sdd="…"` (L1371). **field-help ถูกตัด** — `fieldBlock` รับ arg `help` แต่ render `${help?'':''}` (L1376) = ทิ้งเสมอ (VD-PDM-04 no hint/field-help). numInput helper (L1315): type=number min0, spinner ซ่อน.
Type-specific inputs: `.input-suffix` (deposit_value + %/บาท unit) · `.inst-input`/`.inst-unit` · `.note.is-warn` (direct_payment warning) · `.grn-trigger` (credit lock badge).

### 5.11 Status change menu (`.menu#statusMenu`, L1341)
Dropdown ใน view header (z-modal 60). `toggleStatusMenu` (L1056). 3 `.menu-item` (draft/active/inactive) — ค่าปัจจุบัน `disabled` (opacity .45). Pick → `setStatusFromMenu(id,st)` (L1057).

---

## §6 · Overlay Registry + Dismiss Rules

| Overlay | selector | ขนาด | z | เปิด | ปิดได้โดย | Backdrop | Anim |
|---|---|---|---|---|---|---|---|
| **Create/Edit drawer** | `.drawer` | 680px (→100vw@1180) | 51 | openDrawer | Esc · backdrop click · X · "ยกเลิก" | rgba(17,17,17,.40) z50 | translateX 280ms (double-rAF slide-in L1461) |
| **View drawer** | `.drawer` | 680px | 51 | openDrawer('view') | Esc · backdrop · X · "ปิด" | same | same |
| **Bulk-delete modal** | `.modal` | 440px | 60 | openModal | Esc · backdrop click · X · "ยกเลิก" | rgba(17,17,17,.50) z60 | scale .96→1 |
| **Type/field sdd** | `.sdd-panel` | full-width | 60 | toggleSdd | Esc · click-outside · pick | — | — |
| **Status menu** | `.menu` | min160 | 60 | toggleStatusMenu | (toggle/pick) — ไม่มี Esc/outside handler เฉพาะ | — | — |
| **User menu** | `.user-menu` | 240px | 30 | toggleUserMenu | (toggle) — ไม่มี outside-close | — | — |
| **Toast** | `.toast-host` | ≤380px | 80 | showToast | auto (2800ms / **5000ms error·warning**) | — | toastIn 200ms, is-leaving fade-out 200ms |

**Drawer body:** `overflow-anchor:none` (L302) กัน browser anchor jump. Drawer inner `event.stopPropagation()` (L1161) — click ในเนื้อ drawer ไม่ปิด. Modal เดียวกัน (L1386).

**Toast (`.toast-host` L634, `showToast` L1427):** ⭐ **top-center** (`top:16px; left:50%; translateX(-50%)`, column, align-center). Variants icon+bg: success `check-circle-2`/#0F6E56 · error `x-circle`/#B91C1C · warning `alert-triangle`/#92400E · info `info`/navy. **Duration: error/warning = 5000ms, อื่น = 2800ms** (L1428, recent fix "อยู่นานขึ้นให้อ่านทัน"). Host สร้าง dynamic (L1429). [หมายเหตุ: มี `.toast` CSS ชุดเก่า L361–369 (translateY, is-info=primary) เป็น **dead CSS** — ตัวจริงคือ block L634.]

---

## §7 · Interaction Spec

### 7.1 Esc chain (L1469–1474) ⭐ ลำดับ priority เดียว handler
```
keydown Escape:
  1. state.sdd.open      → ปิด sdd + clear _formScroll
  2. else modal.open     → closeModal()
  3. else drawer.open    → closeDrawer()
  4. else .sidebar.is-open → ปิด sidebar (mobile off-canvas)
```
ปิดทีละชั้นบนสุดก่อนเสมอ (else-if). ตรง 01_UI §1.7 + LD Esc chain.

### 7.2 Click-outside
- **sdd:** document click handler (L916) — `!e.target.closest('.sdd')` → ปิด + clear _formScroll
- **drawer/modal:** backdrop มี `onclick="closeDrawer()"`/`closeModal()`; เนื้อใน stopPropagation
- **status-menu / user-menu:** ❌ ไม่มี outside-close handler (ปิดโดยกด toggle ซ้ำ/pick เท่านั้น) — ดู Drift §11.2

### 7.3 Selection / bulk
`toggleSel(id)` (L1036) toggle 1 row → render. `toggleSelAll(ev)` (L1037) คำนวณ visible list (ใช้ filter เดียวกับ renderPage) → select/deselect ทั้งหมดที่มองเห็น. checkbox thead `allSel` = ทุก visible ติ๊ก.

### 7.4 Drawer slide-in (L1457–1462)
`state._drawerAnimated` flag: ครั้งแรก double-`requestAnimationFrame` เพิ่ม `.is-open` (ให้ browser เห็น transition จาก translateX(100%)); render ถัดไป (re-render ระหว่างเปิด) เพิ่ม is-open ทันที ไม่เล่น anim ซ้ำ. Modal L1464–1467 คล้ายกัน.

### 7.5 Scroll preservation (Iron Rule #29) ⭐
- **`_keepScroll(fn)` (L1438):** wrap ทุก render — เก็บ+คืน scrollTop 3 ชั้น: `.content` · `.tbl-scroll` · `aside.drawer .drawer-body`. `render()`=`_keepScroll(_renderAll)`, `renderPageOnly()`=`_keepScroll(page only)`.
- **`renderFormKeepScroll()` (L1071):** สำหรับ interaction ในฟอร์ม — อ่าน `state._formScroll` (เก็บตอนเปิด sdd) ถ้ามี ไม่งั้นใช้ค่าปัจจุบัน → render → คืน `drawer-body.scrollTop` (+rAF double-set). **ใช้ครั้งเดียวแล้ว clear** `_formScroll=null` (กันค่าค้างทำ scroll เด้ง — comment L1074).
- **`_formScroll` clear paths:** set = `toggleSdd` (L891) · clear = `renderFormKeepScroll` (L1074), `onTypeChange` (L1090), `closeDrawer` (L1067), `openDrawer`(implicit reset), document-click (L918), Esc sdd (L1470), pickSdd flow.
- Form pickers ที่เรียก `renderFormKeepScroll`: onFormPick, onTriggerPick, onDepMethodPick, onRemainPick, onExpensePick, onInstDuePick, toggleUseIn, toggleDefault, addInst, removeInst. (`onTypeChange` ใช้ `render()` + clear scroll เพราะเปลี่ยน field set ทั้งชุด).

### 7.6 Text inputs ไม่ re-render ทั้งหน้า
`onFormInput`/`onFormNum` (L1068–1069) แค่ set `state.form[k]` — ไม่ render (กัน caret กระโดด). `onInstPct` patch `.inst-total` ตรง ๆ (L1104). ค่าไป reflect ตอน render ครั้งถัดไป (เปลี่ยน type/pick dropdown).

### 7.7 Sidebar / responsive
`toggleSidebar()` (L850) toggle `.is-open` — hamburger แสดง @≤1180 (FN-29). `toggleModule(h)` (L848) collapse/expand module ผ่าน `data-expanded`.

---

## §8 · State-Driven UI Matrix

### 8.1 Status enum → pill (`STATUS_META` L791, `statusPill` L797)
| status | label | pill class | icon |
|---|---|---|---|
| `draft` | ร่าง | `pill-draft` (grey) | file-pen |
| `active` | ใช้งาน | `pill-on` (green #E4F4EB/#157A41) | circle-check |
| `inactive` | ไม่ใช้งาน | `pill-off` (amber #FFF1DD/#B8690B) | circle-slash |

> **Dead:** `archived` (pill-archived CSS + `doArchive`/`reactivate`/`askArchive`/`confirm-archive` modal) มีในไฟล์แต่ **ไม่ถูกเรียกจาก UI ใด** — สถานะจริง = 3 ค่า (ดู §11.2 Drift, 05_RULES §5.2 "dev ห้าม implement").

### 8.2 Type enum → field set (`PT_TYPES` L775, `onTypeChange` L1080, `renderForm` L1184)
| type | pill / icon | fields ที่ render | trigger field |
|---|---|---|---|
| `full_prepay` | pill-liability / wallet | (trigger only) + due_basis | sdd dropdown, default `after_full` |
| `full_postpay` | pill-asset / package-check | net_days(0=ทันที) + discount(opt) + due_basis | sdd, default `immediate` |
| `credit` | pill-asset / calendar-clock | net_days(>0) + discount(opt) + due_basis | **lock badge** `.grn-trigger` "ทันที (ล็อกตามประเภท)" — ไม่มี dropdown (trigLock, LD-08b) |
| `deposit` | pill-equity / piggy-bank | deposit_method(3) + deposit_value(≤100 if %) + remaining_timing(3) + net_days + due_basis | sdd, default `after_deposit` (ตัวเลือก after_deposit โผล่เฉพาะ deposit L1169) |
| `installment` | pill-income / layers | schedule editor (≥2 งวด, %, due_type, desc) + inst-total + due_basis | sdd, default `immediate` |
| `partial_delivery` | pill-expense / truck | net_days ต่อรอบ(opt) + due_basis(=delivery) | sdd, default `immediate` |
| `direct_payment` | pill-mute / receipt | expense_category(3) + note.is-warn "ไม่ผ่าน PR/PO/QUO→SO" | **ไม่มี trigger** (noTrigger) · **ไม่มี due_basis** (L1285 gate) |

`onTypeChange` (L1080) reset `state.form` เหลือ keep fields + preset ค่า default ต่อ type (เช่น deposit → method=percent, value=50, net_days=30). direct_payment → auto-remove po/quotation/so จาก use_in (L1089).

### 8.3 use_in — 7 docs (`USE_IN_DOCS` L805) ⭐ NO PR
| key | label | sub | group |
|---|---|---|---|
| `po` | Purchase Order | PO — ใบสั่งซื้อ | ฝั่งซื้อ (P2P) |
| `ap_invoice` | AP Invoice | ใบแจ้งหนี้เจ้าหนี้ | ฝั่งซื้อ (P2P) |
| `payment_voucher` | Payment Voucher | ใบสำคัญจ่าย | ฝั่งซื้อ (P2P) |
| `so` | Sales Order | SO — ใบสั่งขาย | ฝั่งขาย (S2C) |
| `quotation` | Quotation | QUO — ใบเสนอราคา (proposal) | ฝั่งขาย (S2C) |
| `ar_invoice` | AR Invoice | ใบแจ้งหนี้ลูกหนี้ | ฝั่งขาย (S2C) |
| `receipt` | Receipt | ใบเสร็จรับเงิน | ฝั่งขาย (S2C) |

**PR ถอดออก** — comment L806 "[PR removed 2026-08-10 · PM/BA decision OQ-PAY-08]". `DP_DISABLED_DOCS=['po','quotation','so']` (L816) = direct_payment ปิด. → BR-06, LD-F-01, D-08.

### 8.4 Trigger enum (`TRIGGERS` L785, `triggerLabel` L933)
| key | label | badge | note |
|---|---|---|---|
| `immediate` | ทันที (หลัง PO/SO Confirm) | pill-active | |
| `after_deposit` | หลังชำระมัดจำ | pill-equity | `depositOnly` — filter เฉพาะ type=deposit |
| `after_full` | หลังชำระเต็มจำนวน | pill-liability | |

### 8.5 Mode → drawer chrome
| mode | header title | footer submit | avatar |
|---|---|---|---|
| create | เพิ่มเงื่อนไขชำระเงิน | บันทึกและสร้าง | plus icon |
| edit | แก้ไขเงื่อนไขชำระเงิน | บันทึกการแก้ไข | type icon |
| view | {ชื่อ term} | ปิด | type icon |

---

## §9 · Microcopy (VERBATIM)

### 9.1 Toasts (`showToast`, ทุก call)
| ข้อความ | variant | trigger |
|---|---|---|
| `เปลี่ยนสถานะ {n} รายการเป็น {label} แล้ว` | success | bulkSetStatus (L1045) |
| `ลบแล้ว {n} รายการ` (+ ` · ข้าม {m} รายการที่ถูกใช้งาน`) | info/success | bulkDoDelete (L1053) |
| `เปลี่ยนสถานะเป็น {label} แล้ว` | success | setStatusFromMenu (L1057) |
| `ต้องมีอย่างน้อย 2 งวด` | error | submitTerm inst count (L1120) |
| `สัดส่วนงวดต้องรวมเป็น 100% (ตอนนี้ {t}%)` | error | inst sum (L1122) |
| `มัดจำแบบ % ต้องไม่เกิน 100` | error | deposit>100 (L1125) |
| `จำนวนวันเครดิตต้องมากกว่า 0` | error | credit net_days (L1127) |
| `เลือกเอกสารที่ใช้อย่างน้อย 1 รายการ` | error | use_in empty (L1129) |
| `วันชำระเพื่อรับส่วนลดต้องมากกว่า 0 และน้อยกว่าวันเครดิต` | error | discount_days (L1132) |
| `มัดจำแบบ % ต้องมากกว่า 0` | error | deposit %>0 (L1135) |
| `รหัสเงื่อนไขนี้มีอยู่แล้ว` | error | dup summary (L1136) |
| `ตั้งเป็นค่า Default ได้เฉพาะเงื่อนไขสถานะ "ใช้งาน"` | error | default guard (L1138) |
| `บันทึกการแก้ไขแล้ว` | success | edit ok (L1142) |
| `สร้างเงื่อนไขชำระเงินแล้ว` | success | create ok (L1145) |
| `เลิกใช้งานเงื่อนไขแล้ว` | info | doArchive (L1151) — **dead** |
| `เปิดใช้งานเงื่อนไขอีกครั้งแล้ว` | success | reactivate (L1152) — **dead** |

### 9.2 Field errors (inline `.field-error`)
| ข้อความ | ที่ |
|---|---|
| `กรุณากรอกรหัส` | fld-code default (L1113) |
| `รหัสนี้มีอยู่แล้ว — ใช้รหัสอื่น` | dup inline (L1117) ⭐ |
| `กรุณากรอก/เลือกข้อมูลนี้` | fieldBlock default (L1377) |
| `สัดส่วนงวดต้องรวมเป็น 100%` | fld-inst (L1239) |
| `เลือกอย่างน้อย 1 เอกสาร` | fld-usein (L1290) |

### 9.3 Placeholders
list search `ค้นหารหัส หรือชื่อเงื่อนไข...` · sdd search `ค้นหา...` · code `เช่น NET30` · name TH `เช่น เครดิต 30 วัน` · name EN `e.g. Net 30` · net_days(credit) `เช่น 30` · net_days(postpay) `เช่น 0 = ทันที, 7, 15` · discount_pct `เช่น 2 (เว้นว่าง = ไม่มี)` · discount_days `เช่น 10` · deposit_value(%) `เช่น 50` / (fixed) `เช่น 5000` · partial net_days `เช่น 0 = จ่ายทันทีแต่ละรอบ` · inst desc `รายละเอียดงวด (เช่น มัดจำ / งวดที่ {i+1})` · sdd default `— เลือก —` / `— เลือกประเภท —`

### 9.4 Empty / labels / buttons / notes
- Empty table: `ไม่พบเงื่อนไขที่ตรงกับการค้นหา` · sdd empty: `ไม่พบรายการ`
- Buttons: `เพิ่มเงื่อนไข` · `บันทึกและสร้าง` · `บันทึกการแก้ไข` · `ยกเลิก` · `แก้ไข` · `เปลี่ยนสถานะ` · `ปิด` · `เพิ่มงวด` · bulk `ใช้งาน`/`ไม่ใช้งาน`/`ร่าง`/`ลบ`
- Section titles: `ข้อมูลทั่วไป` · `การตั้งค่าเฉพาะประเภท` · `การใช้งานในเอกสาร` · `ตั้งค่าทั่วไป` · `รายละเอียดการคำนวณ` · `สรุปเงื่อนไข`
- Field labels: `รหัส (Code)` (help "ตัวพิมพ์ใหญ่ ไม่ซ้ำ" — ตัดแสดง) · `ชื่อเงื่อนไข (TH)` · `ชื่อเงื่อนไข (EN)` · `ประเภทเงื่อนไข` · `จำนวนวันเครดิต (credit_days)` · `ส่วนลดจ่ายเร็ว (%)` · `ภายในกี่วัน (Discount days)` · `วิธีระบุมัดจำ` · `มูลค่ามัดจำ` · `ชำระส่วนที่เหลือ (remaining)` · `ส่วนที่เหลือ ครบกำหนด (วัน)` · `Warehouse / GRN / Ship Trigger` · `นับวันครบกำหนดจาก (Due basis)` · `หมวดหมู่ค่าใช้จ่าย` · `ตารางงวดการชำระเงิน (Schedule)` · `ตั้งเป็นค่า Default`
- Credit trigger lock badge: `Warehouse/GRN trigger: {label} (ล็อกตามประเภท)` (L1175)
- Direct note: `ประเภทนี้ไม่ผ่าน PR/PO/QUO→SO — บันทึกตรงเข้า GL ที่ AP/AR Invoice · ไม่มี Warehouse Trigger · ไม่มี 3-Way Match` (L1215)
- Toggle default desc: `ระบบเลือกอัตโนมัติในเอกสารใหม่ · มีได้ 1 รายการต่อประเภท`
- Modal: title `ลบเงื่อนไขชำระเงิน` · subtitle `เลือกไว้ {N} รายการ · {M} รายการถูกใช้งานอยู่จะถูกข้าม` · body `ยืนยันการลบออกจากทะเบียน — รายการที่ถูกใช้ในเอกสารแล้วจะไม่ถูกลบ` · ปุ่ม `ลบ {D} รายการ`
- View footer meta: `ใช้ใน PO / SO / Invoice`
- Table footer: `เงื่อนไขชำระเงิน — ใช้ร่วมทุก transaction (PO/QUOT/SO/Invoice/Payment)` + `แสดง {n} จาก {m} เงื่อนไข`

### 9.5 termSummary strings (`termSummary` L922 — สรุปคอลัมน์ + view)
prepay `ชำระครบ 100% ก่อนส่งของ` · postpay `ชำระเต็มภายใน {n} วันหลังรับ`/`ชำระเต็มหลังรับของ` · credit `ครบกำหนด {n} วัน`/`จ่ายทันที` (+` · ลด {p}% ถ้าจ่ายใน {d} วัน`) · deposit `มัดจำ {v} · ที่เหลือ {n} วัน` · installment `{n} งวด ({p}% / …)` · partial `ทยอยส่ง · ชำระตามจำนวนที่รับจริงแต่ละรอบ` · direct `จ่ายตรงเข้า GL — {หมวด}`.

---

## §10 · Data Binding & BACKEND anchors

### 10.1 Mock state (`state` L824) → API
| Mock | ผูก API (FRD 02_API) |
|---|---|
| `state.terms[]` (12 seed L829–840) | `F-PAY-API-01` GET /payment-terms (list+counts) |
| row click → renderView | `F-PAY-API-03` GET /:id |
| `submitTerm` create branch (L1144) | `F-PAY-API-02` POST /payment-terms |
| `submitTerm` edit branch (L1141) | `F-PAY-API-04` PUT /:id (แก้ได้แม้ used>0) |
| `setStatusFromMenu` (L1057) | `F-PAY-API-05` PATCH /:id/status |
| `bulkSetStatus` (L1043) | `F-PAY-API-06` POST /bulk-status |
| `bulkDoDelete` (L1048, guard `used>0` skip) | `F-PAY-API-07` POST /bulk-delete |
| (downstream picker — ไม่มี UI ในไฟล์) | `F-PAY-API-08` GET /active (active-only) |

### 10.2 Term record shape (seed L829) — fields ที่ BE ต้องรองรับ
`id · code · name · name_en · type(7 enum) · trigger · due_basis(3) · net_days · discount_pct · discount_days · deposit_method(3) · deposit_value · remaining_timing(3) · expense_category(3) · installments[{pct,days,due_type,desc}] · use_in[](7 enum) · is_default · status(3) · used`.

### 10.3 DOA placeholder (L1144, L798)
create push set `approver_role:null, approved_by:null, approved_at:null, approval_chain:null` — comment L798 "master ไม่มีสายอนุมัติ — field เตรียมเชื่อม Policy Center". **ไม่มี approval UI.**

### 10.4 Engines (FRD 03_LOGIC §3.2) — anchor สำหรับ BE
- **ENG-PT-01 `installment-validator`** — FE validate (count≥2, sum=100) ที่ `submitTerm` L1119–1123 + `onInstPct`; BE = validate + downstream journal split ต่องวด (Hook-1).
- **ENG-PT-02 `payment-trigger-resolver`** — FE แสดง trigger default/lock (`PT_TYPES.trigDefault/trigLock`, renderForm L1171); BE = unlock decision Warehouse/GRN/Ship (P2P/S2C), downstream.
- Hooks: Hook-2 deposit VAT (Tax Code, OQ-PAY-04) · Hook-3 cash-discount account (GL Posting).
- Cross-module: PO/SO/Quotation/AP/AR Invoice/PV/Receipt pull ผ่าน GET /active + **snapshot** (no FK cascade, Central Plan).

### 10.5 Server-side mirror (Control C4)
`submitTerm()` 7 validations = mirror ของ BE `F-PAY-FN-03 validatePaymentTerm`. HTML = mock synchronous (client-side); production = server mirror (02_API §note L7).

---

## §11 · Traceability + Drift Log

### 11.1 3-way trace (Brief ↔ FRD ↔ HTML)
| Brief § | FRD anchor | HTML anchor |
|---|---|---|
| §2 route map | 01_UI §1.0 P-01..05 · CD-01 | render fns L936/1164/1319/1382 · openDrawer/openModal |
| §3 shell | 01_UI §1.2 P-01 ERP context | sidebar L644 · shell-bar L704 |
| §4/§5.5 List+table | 01_UI P-01 · API-01 | renderPage L936 · renderRow L1009 |
| §5.4 type dropdown 2-line | 01_UI P-01 filter (sub-desc) · #94 | searchDropdown/sdd-opt-sub L882,527 |
| §5.6 bulk bar | 01_UI P-01 bulk · API-06/07 | .bulkbar L574,966 |
| §5.9 installment editor | 01_UI P-02 · BR-04 · ENG-PT-01 | renderForm inst L1216 · inst-actions L1235 |
| §5.7 use_in 7 (no PR) | BR-06 · LD-F-01 · D-08 | USE_IN_DOCS L805 |
| §7.1 Esc chain | 01_UI §1.7 · LD | keydown L1469 |
| §7.5 scroll preserve | 01_UI §1.0 #29 | _keepScroll L1438 · renderFormKeepScroll L1071 |
| §8.2 type field matrix | 01_UI P-02 per-type · FN-09 | PT_TYPES L775 · onTypeChange L1080 |
| §8.1 status pill | 05_RULES §5.2 · FN-05 | STATUS_META L791 |
| §8.4 trigger + credit lock | BR-10/BR-11 · LD-08b · ENG-PT-02 | TRIGGERS L785 · trigLock L1174 |
| §9 microcopy | 05_RULES §5.6 · 06_TESTS §6.10 | showToast calls (§9.1) |
| §9.2 validation | 05_RULES §5.4 (7 core) · FN-03 | submitTerm L1110 |
| §10 create DOA null | 05_RULES D15 · 02_API DOA | L1144,798 |
| §6 toast top-center 5s | 01_UI §1.6 (5s) | showToast L1427 · toast-host L634 |
| P-05 delete guard | BR-08 · API-07 · CD-02 | bulkDoDelete L1048 |

**API-08 GET /active** = backend-only downstream picker — **ไม่มี UI ในไฟล์นี้** (ถูกต้อง — consumer ปลายทางเรียก). FN-04/FN-10 (query/summary) = mirror renderPage filter (L938) + termSummary (L922).

### 11.2 ⚠️ Drift Log
| # | ประเภท | รายการ | สถานะ / ข้อเสนอ |
|---|---|---|---|
| D-1 | **HTML-only (dead)** | `archived` status + `askArchive`/`doArchive`/`reactivate` (L1150–1152) + `confirm-archive` modal (`renderConfirmArchive` L1402) — CSS `.pill-archived`, `tr.is-archived` | **ไม่เป็น drift ที่เงียบ** — 05_RULES §5.2 ระบุ "dead paths … dev ห้าม implement". สถานะจริง = 3 ค่า. **ข้อเสนอ:** ลบ dead code ออกจาก HTML (สะอาด) — ไม่กระทบ spec |
| D-2 | **HTML-only (dead CSS)** | `.toast` legacy block L361–369 (translateY, is-info=primary) ซ้อนกับ toast-host จริง L634 · `.toggle-track` slider (L334) ไม่ถูกใช้ (default ใช้ chk-row) · `.pagination`/`.pg-btn` ไม่ render · CSV CSS ลบแล้ว (L443) แต่ stub fn ว่าง L1414 | Cosmetic — ไม่กระทบ dev binding. **ข้อเสนอ:** prune |
| D-3 | **FRD-only (production)** | Optimistic lock `If-Match` + Idempotency-Key (02_API §2.3, AD-04) · roles Finance Admin/Viewer/Consumer + 403 (05_RULES §5.3) · audit log · multi-tenant RLS | คาดไว้ — HTML = mock client-side (02_API §note L7). dev ต้อง implement ฝั่ง server (ไม่มีใน UI) |
| D-4 | **FRD-only** | `used` definition (นับ draft ปลายทาง?) — OQ-PAY-07 OPEN, blocking delete guard | HTML mock ใช้ `used:N` ตายตัว. **spec ก่อน dev delete** |
| D-5 | **FRD-only (open)** | Deposit VAT Hook-2 (OQ-PAY-04) · EOM cross-month due (EC-08, downstream calc) | ไม่มีใน master UI (ถูกต้อง — ปลายทาง). anchor เตรียมไว้ §10.4 |
| D-6 | **นอก scope feature** | sidebar `ผังบัญชี`/`GL Posting Group`/`สมุดบัญชี`/PR/PO/Settings = `.is-disabled` | คนละ feature — ไม่ใช่ drift ของ F-PAY. ยืนยัน disabled ถูกต้อง (ยังไม่พร้อม) |

> **สรุป:** ไม่มี drift เชิง business ที่ขัด LOCK. Dead code (D-1/D-2) = สะสางฝั่ง HTML. FRD-only (D-3..D-5) = production concern ที่ไม่ปรากฏบน mock UI ตามคาด.

---

## §12 · Diff จากเวอร์ชันก่อน
มีไฟล์ `00_CONTEXT/f-payterm.PRE-RETROFIT.bak.html` (pre-v8-retrofit) — ไม่ได้ diff ใน brief นี้ (นอกขอบเขต input). สรุป retrofit จาก PREFLIGHT comment (L1484–1493): เพิ่ม token blocks (--fs/--sp/--r/--z) · font_off 8→0 · z_adhoc 13→0 · warm-light rgba · ลบ dead static overlay markup · white bulk bar + top-center toast + 2-line dropdown (recent fixes). **ถ้าต้องการ diff จริง → รัน `html-ui-brief` โหมด Section 12 พร้อม 2 ไฟล์.**

---

## §13 · 💡 ข้อเสนอ (ไม่ใช่ AS-BUILT — R1)
> ต่อไปนี้ **ไม่ใช่สเปคปัจจุบัน** — เสนอให้พิจารณาแยกจากการ build 1:1
1. **Prune dead code** (D-1/D-2): archive/reactivate/confirm-archive, legacy `.toast`, `.toggle-track`, `.pagination`, CSV stub fns — ลดสับสน dev.
2. **status-menu / user-menu outside-close:** เพิ่ม click-outside handler ให้สอดคล้อง sdd (ตอนนี้ปิดโดย toggle ซ้ำเท่านั้น — §7.2).
3. **Loading state:** ปุ่ม submit/bulk ยังไม่มี spinner (mock). Production ที่ยิง API จริงควรมี disabled+loader (PREFLIGHT accepted residual).
4. **Pagination:** list ไม่มี paging — ถ้าจำนวน term เยอะ (>ตาราง) ควรผูก API-01 `limit/offset` (มี CSS พร้อม).

---

*Extraction-based · ทุก anchor อ้าง selector/function/บรรทัดจริงใน `f-payterm.html`. use_in=7 (no PR). DOA=null. No CSV.*
