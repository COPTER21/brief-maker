# UI BRIEF — F-TAX · ทะเบียนรหัสภาษี (Tax Code Master)

> **AS-BUILT · Extraction-based** — ทุกบรรทัดในบรีฟนี้ trace กลับ selector / function / ข้อความจริงใน `f-taxcode.html` ได้ (Iron Rule R1). Microcopy = verbatim (R2). ห้ามใช้บรีฟนี้แทน HTML — HTML คือ source of truth, บรีฟคือ "แผนที่ design intent".
> คู่กับ: **HTML** (`f-taxcode.html`) + **FRD Pack** (`FRD_F-TAX_Pack/`, 7 ไฟล์). Dev handoff = HTML + FRD + บรีฟนี้.

---

## §0 · Document Control + Pairing

| Field | Value |
|---|---|
| Feature | F-TAX · ทะเบียนรหัสภาษี (Tax Code Master) |
| HTML (SoT) | `Pack Brief Feature/3. Tax Code/f-taxcode.html` (สำเนา `outputs/03_Tax-Code/f-taxcode.html`) · 959 บรรทัด · single-file SPA |
| HTML `<title>` | `ทะเบียนรหัสภาษี · CUBE` (L6) |
| Kit / CI | CUBE Warm Light (html-generator-**v8**) — comment L12 "mirrored from product-master golden reference (healed)" · PREFLIGHT v8 RESULT=PASS (L955) |
| FRD paired | ✅ `FRD_F-TAX_Pack/` 00–06 (Step 6). Layer refs: 01_UI (P-01..06), 02_API (F-TAX-API-01..10), 05_RULES (BR-01..10 / VR / EC / 6 import codes) |
| HTML เวอร์ชันเก่า | **ไม่มี** → §12 Diff / Drift baseline = **N/A** |
| Drift status | ดู §11 — ไม่มี business drift (HTML ↔ FRD สอดคล้อง); มี 2 รายการ "โครงสร้าง" (API-10 downstream ไม่มี UI trigger, downloadTemplate ไม่มี API) = by-design, ลง Drift Log |
| Lucide | `lucide@0.469.0` UMD (L359, external CDN) — icons render ผ่าน `renderIcons()` → `lucide.createIcons()` |
| Fonts | Noto Sans Thai (Google) + Satoshi (Fontshare) — external `<link>` L7-10 |

---

## §1 · Design Tokens AS-BUILT

ทั้งหมดจาก `:root` (L13). ห้าม pin ค่าใหม่ — ใช้ token name.

### 1.1 z-index map (เรียงสูง→ต่ำ) — ครบ 8 ตัวที่ประกาศ
| Token | ค่า | ใช้กับ (selector) |
|---|---|---|
| `--z-toast` | **80** | `.toast` (L293) |
| `--z-sidebar-mobile` | **70** | `.sidebar` off-canvas <1180px (L96) |
| `--z-modal` | **60** | `.modal-backdrop` (L279) — modal + backdrop ชั้นเดียวกัน |
| `--z-drawer` | **51** | `.drawer` (L231) |
| `--z-backdrop` | **50** | `.drawer-backdrop` (L229) |
| `--z-dropdown` | **30** | `.pop-menu` / `.status-menu` (L77, L199) |
| `--z-shell` | **20** | `.sidebar` (L32), `.main` shell |
| `--z-sticky` | **10** | `.shell-bar` sticky top (L59) |

> หมายเหตุ overlay stacking: drawer (51) > backdrop (50) > modal (60 > drawer) — modal เปิดทับ drawer ได้ (import/bulk-delete). `<div id="overlay-root">` มีใน DOM (L956) แต่ **ไม่ถูกใช้** (drawer/modal เป็น static node #drawer/#modalBackdrop, ไม่ portal เข้า overlay-root) — Iron #95 comment ระบุ "n/a" (L955).

### 1.2 สี (16 tokens)
`--c-navy #111111` · `--c-primary #FF3B30` · `--c-primary-hover #E62E24` · `--c-primary-tint rgba(255,59,48,.05)` · `--c-teal #FF9A1F` · `--c-ink #111111` · `--c-mute #54565C` · `--c-mute-2 #73757B` · `--c-mute-3 #9A9CA2` · `--c-line #DEDAD4` · `--c-line-2 #E9E5E0` · `--c-line-3 #F1EEEA` · `--c-bg-off #FAF8F5` · `--c-success #1F9D55` · `--c-warning #E8870F` · `--c-danger #E62E24`

**สีเฉพาะจุด (hardcoded ในคลาส pill/tag — ไม่ใช่ token):** type-pill `#E6F0FF/#1A5FCC` (L166) · pill.is-active `#E4F4EB/#157A41` (L175) · pill.is-inactive `#FFF1DD/#B8690B` (L176) · lock-tag `#FFF1DD/#B8690B` (L178) · modal-header-icon danger `#FFE9E7` (L285) · hint-card `#E6F0FF/#1A5FCC` (L264).

### 1.3 Layout / spacing / radius / type
- `--sidebar-w 232px` · `--shell-h 52px`
- spacing: `--sp-xs 4` · `--sp-sm 8` · `--sp-md 12` · `--sp-lg 20` · `--sp-xl 28`
- radius: `--r-xs 4` · `--r-sm 6` · `--r-md 8` · `--r-lg 12` · `--r-full 999`
- `--fs-body 14px` · body line-height 1.5
- **Font stack:** body `'Satoshi','Noto Sans Thai',system-ui,sans-serif` (L25) · หัวข้อ (`.ph-title` L107, `.dw-title` L237, `.stat-value` L133) = `'Noto Sans Thai',sans-serif`
- Radius/shadow: drawer shadow `-16px 0 40px rgba(17,17,17,.18)` (L231) · modal shadow `0 24px 60px rgba(17,17,17,.28)` (L281) · toast shadow `0 12px 32px rgba(17,17,17,.30)` (L293)
- Scrollbar: `scrollbar-width:thin`, webkit 5px, thumb `rgba(17,17,17,.14)` (L17-22); ในsidebar thumb `rgba(255,255,255,.28)` (L23-24)
- Responsive breakpoint เดียว: `@media (max-width:1180px)` (L95) — sidebar off-canvas, `.main` margin 0, drawer → `min(920px,100vw)`. body `min-width:768px` (Iron #97, L15).

---

## §2 · Route Map

| Route | Trigger | Handler | หมายเหตุ |
|---|---|---|---|
| `#/tax-codes` | `navTo('tax-codes')` (L938 → `location.hash='#/'+route`) | `hashchange` → `render()` → `renderList()` (L941-942) | route เดียวของทั้ง feature |
| (ทุก hash / โหลดครั้งแรก) | `DOMContentLoaded` → `render()` (L943) | `render()` = `renderList()` เสมอ (L941) | **refresh-safe**: `render()` ไม่อ่านค่า hash เลย → hash อะไรก็ render list |

- **ไม่มี route ย่อยของ create/edit/view/import/delete** — ทั้งหมดเป็น **overlay** (drawer/modal) ทับ list, ไม่เปลี่ยน hash (สอดคล้อง FRD 01_UI §1.0: trigger จริงแทน route)
- Deep-link เข้า record ไม่ได้ (state ใน memory; overlay ไม่ผูก URL)

---

## §3 · Layout Shell (ทุกหน้าใช้ร่วม)

| Region | Selector | ขนาด/ค่า | เนื้อหา verbatim |
|---|---|---|---|
| Sidebar | `.sidebar` (L304) | fixed left, `--sidebar-w 232px`, bg `#111111`, `--z-shell 20` | brand `CUBE NATIVE` / `P2P · Master Data` (L305) |
| Nav modules | `.sb-module` ×3, `toggleModule()` (L934) | expandable (`data-expanded`) | **Master Data**: `ทะเบียนสินค้า` (disabled), `ทะเบียนรหัสภาษี` (**is-active**, `navTo('tax-codes')`), `ทะเบียนผู้ขาย` (disabled) · **Inventory**: `สต็อกตามตำแหน่ง`, `รับสินค้า` (disabled) · **System**: `การตั้งค่า` (disabled) |
| Sidebar footer | `.sb-footer` (L327) | — | `UAT · v6` |
| Main | `.main` (L329) | `margin-left:232px` | wrapper |
| Shell bar | `.shell-bar` (L330) | sticky top, `--shell-h 52px`, `--z-sticky 10` | breadcrumb + topbar-right |
| Breadcrumb | `.breadcrumb` (L331) | — | `Master Data` (link `navTo('tax-codes')`) › `ทะเบียนรหัสภาษี` (current) |
| Notif | `.icon-btn` + `#notifMenu`, `toggleNotif()` (L936) | pop-menu `--z-dropdown 30` | title `การแจ้งเตือน` + `เพิ่มรหัสภาษีใหม่ 2 รายการเมื่อวานนี้` + `"WHT15 — หัก ณ ที่จ่าย 15%" ถูกหยุดใช้งานเมื่อวานนี้` (L336-338) — placeholder, ไม่มี logic (FRD LOCK-NO-NOTIF) |
| User chip | `.user-chip` + `#userMenu`, `toggleUserMenu()` (L937) | — | `วิภา ผลิตภัณฑ์` / `Master Data · CUBE NATIVE` · avatar `วผ` · menu: `โปรไฟล์` / `การตั้งค่า` / `ออกจากระบบ` (L344-347) |
| Content mount | `.content#page-content` (L352) | full-height `calc(100vh - var(--shell-h))` (Iron #96, L89) | `renderList()` เขียน innerHTML |

> mock user drift: shell = `วิภา ผลิตภัณฑ์`, แต่ mock records `updated_by='พิมพ์ใจ บัญชี'` — FRD ยก OQ-TAX-06 (cosmetic).

---

## §4 · Page Anatomy (ต่อหน้า)

### P-01 · List — `renderList()` (L437) · FRD P-01
Region tree (จาก innerHTML template L510-544):
```
.content#page-content
├─ .ph (page header)
│  ├─ .ph-title-row: h1 "ทะเบียนรหัสภาษี" + .ph-count "{total} รายการ"
│  └─ .ph-actions: [ส่งออก CSV] [นำเข้า CSV] [สร้างรหัสภาษี]
├─ .stats (grid auto-fit): stat ×4 (all/active/inactive/draft) — .stat.is-on เมื่อ filter ตรง
└─ .card
   ├─ .filter-bar: search(.fld-width-search) + select หมวด + select สถานะ + .filter-spacer + [ล้างตัวกรอง]
   └─ tableInner:
      ├─ .bulkbar (เฉพาะเมื่อ selN>0)
      ├─ .table-scroll > table.utbl (thead sticky + tbody)
      └─ .tbl-foot: info "แสดง a–b จาก n รายการ" + renderPager()
```
- **Table columns** (L491-503, header `th()` L466): `checkbox` · `รหัส`(code) · `ชื่อรหัสภาษี`(name_th+name_en) · `อัตรา`(ta-r, `{rate}%`) · `ประเภท`(`.type-pill` catLabel) · `ใช้ในสินค้า/เอกสาร`(ta-r, `{used} รายการ`, icon package) · `สถานะ`(statusPill) · `จัดการ`(ปุ่ม `แก้ไข` เท่านั้น — **ไม่มีลบเดี่ยว**, ยืนยัน LOCK-BULK-DEL)
- Row click `onclick="openView(id)"`; checkbox/actions cell `onclick="stop(event)"` กันเปิด view
- sortable header: `sortBy(col)` toggle asc/desc; icon `chevrons-up-down` (default) / `arrow-up` / `arrow-down` (L467). `rate`+`used` sort เชิงตัวเลข (L424)
- pagination: `pageSize:8` (L380), pager 1..N + prev/next (`renderPager` L548)

### P-02/P-03 · Create/Edit drawer — `formHTML(mode,r)` (L589) · FRD P-02/P-03
```
#drawer (680px)
├─ .dw-head: avatar + eyebrow("รหัสภาษีใหม่"/"แก้ไขรหัสภาษี") + title + subtitle "ทะเบียนรหัสภาษีกลาง" + [x close]
├─ .dw-body > .dw-section "ข้อมูลรหัสภาษี" > .form-grid (2-col):
│   #fld-code(รหัสภาษี) · #fld-rate(อัตรา (%)*) · in-name-th(ชื่อ (ไทย)*) · in-name-en(ชื่อ (อังกฤษ))
│   · in-category(ประเภทภาษี*, onTypeChange) · in-status(สถานะ)
└─ .dw-footer: [ยกเลิก] ... [ยืนยันสร้าง / บันทึกการแก้ไข #saveBtn]
```
- **Lock (IR-TAX-01):** `locked = isEdit && (r.used||0)>0` (L592) → `#in-code`,`#in-rate`,`#in-category` = `disabled` + `.lock-tag "ล็อก — ถูกใช้งานแล้ว"` (L593) ที่ label 3 ช่อง. name_th/name_en/status ยังแก้ได้
- **Exempt:** `onTypeChange('exempt')` (L650) → `#in-rate`.value='0' + disabled + `#rate-exempt-tag` = `.lock-tag "ยกเว้นภาษี = อัตรา 0"`; ประเภทอื่น → เคลียร์ tag + enable
- autofocus field แรกที่ไม่ disabled หลังเปิด 80ms (L579-580)

### P-04 · View drawer (tabbed) — `viewHTML(r)` (L744) · FRD P-04
```
#drawer (680px)
├─ .dw-head: avatar(initials) + eyebrow "รหัสภาษี · {code}" + title name_th + subtitle(statusPill + catLabel)
│   + actions: [แก้ไข] [เปลี่ยนสถานะ ▾ #statusMenu] | [x]
├─ .drawer-tabs: [ภาพรวม][การใช้งาน {used}][ประวัติ]  (switchTab, L712)
├─ .dw-body#viewBody: viewBody(r,tab) (L713)
└─ .dw-footer: meta "แก้ไขล่าสุด {date}" ... [ปิด]
```
- tab `overview`: def-grid 6 แถว (รหัสภาษี/อัตรา/ชื่อ (ไทย)/ชื่อ (อังกฤษ)/ประเภทภาษี/สถานะ)
- tab `usage`: "การอ้างอิงจากสินค้า" → "จำนวนที่ถูกอ้างอิง" = `{used} รายการ` (**ไม่มีปุ่มลบออกจากทะเบียน**)
- tab `history`: timeline 2 จุด — `แก้ไขล่าสุด` ({updated_by · date}) / `สร้างรายการ` ({created_by · date})
- **status menu** `#statusMenu` (L757): title `เปลี่ยนสถานะเป็น` + 3 ค่า; ค่าปัจจุบัน `.is-current` + `disabled` + mark `ปัจจุบัน`; อื่น → `setStatus(id,st)` เปลี่ยนทันที (ไม่มี gate)

### P-05 · Import modal (3-step) — `bulkModalHTML()` (L830) · FRD P-05
`#modalEl.is-wide` (640px, toggled เมื่อ `state.modal.type==='bulk'` L781). Step ตาม `state.bulk.step`:
- **pick** (L838): `.upload-box "เลือกไฟล์ CSV / Excel"` (คลิก → trigger `#bulkFile` hidden input `.vhide` L842) + สถานะไฟล์ + footer `[ดาวน์โหลด template ตัวอย่าง] ... [ปิด]`
- **preview** (L846): summary bar + `table.utbl` รายแถว (รหัส/ชื่อรหัสภาษี/ประเภท/อัตรา/สถานะ/ผลตรวจ) + footer `[ยกเลิก] [นำเข้า {ok} แถว]` (disabled ถ้า ok=0)
- **done** (L860): summary + (ถ้ามี err) table แถวข้าม (รหัส/ชื่อ/สาเหตุ) + footer `[ปิด]`
- **Guard:** preview เกิดเฉพาะเมื่อเลือกไฟล์จริง — `bulkFileChosen(input)` เช็ค `input.files[0]` (L818) ก่อนเรียก `bulkPick`

### P-06 · Bulk-delete confirm modal — `openBulkDelete()` (L887) · FRD P-06
`#modalEl` (440px default). header icon `trash-2` + title `ลบรหัสภาษี {n} รายการ?` + desc (used>0 → เตือนข้าม / else ย้อนกลับไม่ได้) + footer `[ยกเลิก] [ลบ {n-used} รายการ]`.

---

## §5 · Component Inventory (anchor + states, R3/R4)

| Component | Selector หลัก | render/handler | States (มีจริงใน HTML) |
|---|---|---|---|
| Button primary | `.btn.btn-primary` | — | default / `:hover` (shadow) / `:disabled`+`.is-disabled` (opacity .55, L123) / loading (`.spin` loader ใน saveBtn L690) |
| Button secondary/ghost/danger | `.btn-secondary`/`.btn-ghost`/`.btn-danger` | — | default / hover / disabled — ไม่มี focus-visible แยก (—) |
| Stat card | `.stat` | `quickFilter(key)` (L562) | default / hover / `.is-on` (active filter) — คลิกซ้ำ toggle |
| Filter search | `.fld-width-search .input` | `onSearch(v)` (L560) | default / `:focus` (ring primary) · re-focus + caret ท้าย หลัง re-render (L560) |
| Select (หมวด/สถานะ) | `.select` | `onFilter(key,v)` (L561) | default / focus · custom chevron bg (L140) |
| Table row | `.utbl tbody tr` | `openView(id)` | default / `:hover` (bg-off) / `.is-selected` (primary-tint, L181) |
| Checkbox | `.ck` | `toggleSel`/`toggleSelPage` (L871-872) | unchecked / checked · accent primary |
| Sort header | `.utbl th.sortable` | `sortBy(col)` | idle(`chevrons-up-down`) / asc(`arrow-up`) / desc(`arrow-down`) / hover |
| Status pill | `.pill.is-{status}` | `statusPill(st)` (L374) | is-active / is-inactive / is-draft (สี+icon ต่างกัน — ดู §8) |
| Type pill | `.type-pill` | `catLabel()` | สีเดียว (#E6F0FF/#1A5FCC) |
| Use-count | `.use-count` | inline | ปกติ / `.is-zero` (used===0 → mute-3, L169) |
| Lock tag | `.lock-tag` | `formHTML`/`onTypeChange` | โผล่เมื่อ locked หรือ exempt (—ไม่มี state อื่น) |
| Row action | `.ra-btn` | `openEdit(id)` | default / hover(primary) / `.is-danger:hover` / `.is-disabled` (มี CSS L212 แต่ **ไม่ถูกใช้ในหน้านี้** — ปุ่มเดียวคือแก้ไข) |
| Bulk bar | `.bulkbar` | render เมื่อ `selN>0` | มี/ไม่มี (conditional) |
| Pager button | `.pg-btn` | `goToPage(n)` (L569) | default / hover / `.is-active` / `.is-disabled` (หน้าแรก/สุดท้าย) |
| Drawer tab | `.drawer-tab` | `switchTab(tab)` | default / hover / `.is-active` (underline primary) · badge `.count-badge` (usage) |
| Empty state | `.empty` | inline ใน renderList | 2 แบบ: filtered / no-data (§9) |
| Form field | `.field` | validation ใน `saveUnit` | default / `.has-err` (border danger + `.err` แสดง, L259-260) / disabled |
| pop-menu | `.pop-menu` (notif/user/status) | toggle* + `closeMenus` | `.is-open` / ปิด · status-menu `.pm-item.is-current` (dim .5, L205) |
| Toast | `.toast` | `showToast(msg,variant)` | is-success / is-info / is-warning (+ is-visible slide) · auto-hide 3500ms |
| Import row result | `.import-sum` + `.pill` | `bulkValidateRow` | `.is-success`/`.is-warning` (summary) · pill พร้อมนำเข้า/error |

---

## §6 · Overlay Registry (dismiss rules + z)

| Overlay | Node | ขนาด | z-index | เปิด | ปิดได้โดย | Backdrop click | Scroll/anim |
|---|---|---|---|---|---|---|---|
| **Drawer** (create/edit/view) | `#drawer` + `#drawerBackdrop` (L354-355) | 680px (max 96vw; <1180 → 920) | drawer 51 / backdrop 50 | `openDrawerShell()` (L573) | `[x]` close btn · Esc · **backdrop** · save/delete สำเร็จ (`closeDrawer()`) | ✅ ปิด (`onclick="closeDrawer()"` L354) | slide translateX 280ms cubic-bezier; ไม่มี body scroll-lock |
| **Modal — Import** | `#modalEl.is-wide` in `#modalBackdrop` (L356) | 640px | modal 60 | `bulkImport()` (L817) | `[x]`/`[ปิด]`/`[ยกเลิก]` · Esc · **backdrop** | ✅ ปิด (`onclick="closeModal()"` L356); inner `stop(event)` กันปิด (L356) | fade 180ms + scale .96→1 |
| **Modal — Bulk delete** | `#modalEl` (440px) | 440px | modal 60 | `openBulkDelete()` (L887) | `[ยกเลิก]` · Esc · **backdrop** · ลบสำเร็จ | ✅ ปิด | เหมือนบน |
| **pop-menu — Notif** | `#notifMenu` (L335) | 240px | dropdown 30 | `toggleNotif()` | Esc(อันดับ 1) · document click(`closeMenus`) · toggle ซ้ำ | — (ปิดผ่าน global click) | display none↔block |
| **pop-menu — User** | `#userMenu` (L343) | 240px | dropdown 30 | `toggleUserMenu()` | เหมือน notif | — | — |
| **pop-menu — Status** | `#statusMenu` (L757) | 210px | dropdown 30 | `toggleStatusMenu()` (L881) | Esc · document click · toggle ซ้ำ · เลือก `setStatus` | — | absolute ใต้ปุ่ม (`top:calc(100%+6px);right:0` L199) |
| **Toast** | `#toast` (L357) | max 380px | toast 80 | `showToast()` (L922) | auto-hide 3500ms (`toastTimer` L930) | — (ปิดเอง) | slide-up 250ms |

> **ห้ามพลาด:** ไม่มี overlay ไหน "ห้ามปิด" — ทุกตัวปิดด้วย Esc/backdrop ได้หมด (รวม confirm-delete). ไม่มี scroll-lock บน body เมื่อ overlay เปิด (ไม่มี code เพิ่ม/ลบ class ที่ body).

---

## §7 · Interaction Spec

### 7.1 Esc chain (keydown handler L945-952) — ลำดับ verbatim
```
Escape:
 1) ถ้ามี .pop-menu.is-open  → closeMenus(); return   (เมนูก่อนเสมอ)
 2) else ถ้า state.modal.open  → closeModal(); return
 3) else ถ้า state.drawer.open → closeDrawer(); return
 4) else closeMenus()
```
→ ลำดับ: **menu > modal > drawer**. (modal เปิดทับ drawer ได้ → Esc ปิด modal ก่อน แล้วค่อย drawer รอบถัดไป)

### 7.2 Click-outside
- `document.addEventListener('click', closeMenus)` (L944) — คลิกที่ไหนก็ปิด pop-menu ทุกตัว
- toggle handlers (`toggleNotif/User/StatusMenu`) เรียก `stop(e)` + `closeMenus()` ก่อนเปิด → เปิดได้ทีละเมนู (L936-937, 881)
- Backdrop = click-outside ของ drawer/modal (ผ่าน `onclick` บน backdrop node)

### 7.3 Focus management
- เปิด drawer → autofocus field แรกที่ไม่ disabled (`setTimeout 80ms`, L579-580)
- หลัง `onSearch` re-render → คืน focus + วาง caret ท้าย input (L560) เพื่อพิมพ์ต่อเนื่อง
- ไม่มี focus-trap ใน overlay (—)

### 7.4 Positioning
- Drawer: `position:fixed; top/right/bottom:0` (L231) — fixed viewport, ไม่ผูก scroll
- Modal: `position:fixed; inset:0` flex center (L279) — คลุมเต็มจอ
- pop-menu (notif/user): `position:absolute; top:42px; right:0` ใน `.rel-wrap` (L66,77)
- status-menu: `absolute` ใน wrapper `position:relative;display:inline-block` (L755) — ไม่มี flip logic (จอเดียว, ปุ่มขวาบน)

### 7.5 Loading / double-submit guard
- Save: `#saveBtn` → `.is-disabled` + innerHTML loader `กำลังบันทึก…` + `setTimeout 600ms` mock (L689-702) แล้วปิด drawer + toast
- ไม่มี debounce บน search (render ทุก keystroke)

### 7.6 Drag/zoom/pan — **ไม่มีใน HTML นี้** (—)

---

## §8 · State-Driven UI Matrix

### 8.1 สถานะ record (statusLabel L373 / statusPill L374)
| enum | label (verbatim) | pill class | สี (bg/fg) | icon |
|---|---|---|---|---|
| `draft` | `ร่าง` | `.pill.is-draft` | `--c-line-3` / `--c-mute-2` | `file-pen` |
| `active` | `ใช้งาน` | `.pill.is-active` | `#E4F4EB` / `#157A41` | `circle-check` |
| `inactive` | `ไม่ใช้งาน` | `.pill.is-inactive` | `#FFF1DD` / `#B8690B` | `circle-slash` |

### 8.2 ประเภทภาษี (CATEGORIES L366)
| id | label (verbatim) | ผลต่อ UI |
|---|---|---|
| `vat` | `ภาษีมูลค่าเพิ่ม (VAT)` | rate แก้ได้ |
| `wht` | `หัก ณ ที่จ่าย (WHT)` | rate แก้ได้ |
| `exempt` | `ยกเว้นภาษี` | rate = 0 locked + tag "ยกเว้นภาษี = อัตรา 0" |

### 8.3 Stat card ↔ filter (stat() L451, quickFilter L562)
| key | label / meta (verbatim) | icon | filter action |
|---|---|---|---|
| `all` | `รหัสภาษีทั้งหมด` / `ทุกประเภทรวมกัน` | percent | reset status+category=all |
| `active` | `ใช้งานอยู่` / `พร้อมใช้ในเอกสาร` | circle-check | toggle status=active |
| `inactive` | `ไม่ใช้งาน` / `ซ่อนจากการเลือกใหม่` | circle-slash | toggle status=inactive |
| `draft` | `ร่าง` / `ยังไม่เปิดให้ใช้` | file-pen | toggle status=draft |

### 8.4 Lock / disabled matrix (form)
| เงื่อนไข | code | rate | category | name_th/en | status |
|---|---|---|---|---|---|
| create | ✎ | ✎ | ✎ | ✎ | ✎ |
| edit, used=0 | ✎ | ✎ | ✎ | ✎ | ✎ |
| edit, used>0 (IR-TAX-01) | 🔒 disabled+tag | 🔒 | 🔒 | ✎ | ✎ |
| category=exempt (ทุกโหมด, ยังไม่ locked) | ✎ | 🔒=0+tag | ✎ | ✎ | ✎ |

### 8.5 Import row result (bulkValidateRow L796)
ผ่าน → pill `.is-active` `พร้อมนำเข้า`; ผิด → pill `.is-inactive` + 1 ใน 6 error codes (§9.5).

---

## §9 · Microcopy (verbatim)

### 9.1 ปุ่ม / action
List: `ส่งออก CSV` · `นำเข้า CSV` · `สร้างรหัสภาษี` · `ล้างตัวกรอง`
Bulk bar: `เลือก {selN} รายการ` · `ตั้งเป็น ใช้งาน` · `ตั้งเป็น ร่าง` · `ตั้งเป็น ไม่ใช้งาน` · `ลบ` · `ยกเลิกการเลือก`
Row: title `แก้ไข`
Form footer: `ยกเลิก` · `ยืนยันสร้าง` (create) · `บันทึกการแก้ไข` (edit) · loader `กำลังบันทึก…`
View: `แก้ไข` · `เปลี่ยนสถานะ` · `ปิด` · status-menu title `เปลี่ยนสถานะเป็น` · current mark `ปัจจุบัน`
Import: `ดาวน์โหลด template ตัวอย่าง` · `ปิด` · `ยกเลิก` · `นำเข้า {ok} แถว`
Delete: `ยกเลิก` · `ลบ {n-used} รายการ`

### 9.2 Toast (ทุก `showToast()` — 8 จุด, verbatim)
| # | ที่มา (fn) | ข้อความ | variant |
|---|---|---|---|
| 1 | saveUnit(edit) L696 | `บันทึกการแก้ไข "{name}" แล้ว` | success |
| 2 | saveUnit(create) L700 | `สร้างรหัสภาษี "{name}" สำเร็จ` | success |
| 3 | downloadTemplate L815 | `ดาวน์โหลด template ตัวอย่างแล้ว` | success |
| 4 | bulkConfirm L828 | `นำเข้าแล้ว {ok} รายการ` (+ ` · ข้าม {err} แถว (IMPORT_ERROR)` ถ้ามี err) | warning/success |
| 5 | setStatus L879 | `เปลี่ยนสถานะ "{name}" เป็น {statusLabel} แล้ว` | success |
| 6 | bulkSetStatus L885 | `เปลี่ยนสถานะ {n} รายการ เป็น {statusLabel} แล้ว` | success |
| 7 | confirmBulkDelete L908 | `ลบแล้ว {del} รายการ` (+ ` · ข้าม {skip} (ถูกใช้ในสินค้า/เอกสาร)` ถ้ามี) | warning/success |
| 8 | exportCSV L917 | `ส่งออก {n} รายการเป็น CSV แล้ว` | success |

toast icon map (L924): success→`check-circle` · info→`info` · warning→`alert-triangle` · error→`x-circle`

### 9.3 Placeholder / label / hint
Search placeholder: `ค้นหารหัส ชื่อ หรืออัตรา…`
Filter options: `ทุกประเภท` · `ทุกสถานะ` / `ร่าง` / `ใช้งาน` / `ไม่ใช้งาน` · aria-label `กรองตามหมวด` / `กรองตามสถานะ`
Form labels: `รหัสภาษี` · `อัตรา (%)` * · `ชื่อ (ไทย)` * · `ชื่อ (อังกฤษ)` · `ประเภทภาษี` * · `สถานะ`
Form placeholders: `เช่น VAT7` · `เช่น 7` · `เช่น ภาษีมูลค่าเพิ่ม 7%` · `เช่น VAT 7%`
Tags: lock `ล็อก — ถูกใช้งานแล้ว` · exempt `ยกเว้นภาษี = อัตรา 0`
Drawer eyebrow: `รหัสภาษีใหม่` / `แก้ไขรหัสภาษี` · subtitle `ทะเบียนรหัสภาษีกลาง` · view eyebrow `รหัสภาษี · {code}`
Table headers: `รหัส` · `ชื่อรหัสภาษี` · `อัตรา` · `ประเภท` · `ใช้ในสินค้า/เอกสาร` · `สถานะ` · `จัดการ`
Cell/foot: `{used} รายการ` · `{rate}%` · `แสดง {a}–{b} จาก {n} รายการ`
View tabs: `ภาพรวม` · `การใช้งาน` · `ประวัติ` · def-grid labels `รหัสภาษี`/`อัตรา`/`ชื่อ (ไทย)`/`ชื่อ (อังกฤษ)`/`ประเภทภาษี`/`สถานะ`
Usage tab: `การอ้างอิงจากสินค้า` · `จำนวนที่ถูกอ้างอิง` · `{used} รายการ`
History tab: `ประวัติการเปลี่ยนแปลง` · `แก้ไขล่าสุด` · `สร้างรายการ`
View footer: `แก้ไขล่าสุด {date}`
Import: title `นำเข้ารหัสภาษีจากไฟล์` · desc `CSV / Excel — ระบุสถานะได้ในไฟล์` · `เลือกไฟล์ CSV / Excel` · `ยังไม่ได้เลือกไฟล์` / `ไฟล์ที่เลือก: {name}` · `จากไฟล์: {name}` · summary `ตรวจแล้ว {n} แถว — นำเข้าได้ {ok} · ติดปัญหา {err} (แถวผิดจะถูกข้าม)` · headers `รหัส`/`ชื่อรหัสภาษี`/`ประเภท`/`อัตรา`/`สถานะ`/`ผลตรวจ` · `พร้อมนำเข้า` · done `นำเข้าเสร็จ {ok} รายการ (สถานะตามไฟล์)` (+ ` · ข้าม {err} แถว (IMPORT_ERROR)`) · done headers `รหัส`/`ชื่อ`/`สาเหตุ`
Delete: title `ลบรหัสภาษี {n} รายการ?` · desc (used>0) `มี {used} รายการถูกอ้างอิงในสินค้า/เอกสาร — จะถูกข้าม ไม่ลบ` / (else) `การกระทำนี้ย้อนกลับไม่ได้`

### 9.4 Empty states
| แบบ | title | desc | ปุ่ม |
|---|---|---|---|
| filtered (มี filter/search) | `ไม่พบรหัสภาษีที่ตรงกับตัวกรอง` | `ลองปรับคำค้นหรือล้างตัวกรองเพื่อดูรายการทั้งหมด` | `ล้างตัวกรอง` (resetFilters) |
| no-data | `ยังไม่มีรหัสภาษีในระบบ` | `เริ่มต้นด้วยการสร้างรหัสภาษีแรกเข้าสู่ทะเบียน` | `สร้างรหัสภาษี` (openCreate) |

### 9.5 Validation (form) + 6 import error codes (verbatim)
Form (`saveUnit` L666-687): name ว่าง → `กรุณากรอกชื่อภาษาไทย` (L623) · dup → `รหัส {finalCode} ถูกใช้แล้ว` (L681, default text `รหัสนี้ถูกใช้แล้ว` L613) · rate ผิด → `กรุณากรอกอัตรา 0–100` (L618)
Import (`bulkValidateRow` L796-803):
1. `ข้อมูลบังคับไม่ครบ (REQUIRED)`
2. `ประเภทไม่ถูกต้อง (BAD_TYPE)`
3. `อัตราไม่ถูกต้อง 0–100 (RATE_INVALID)`
4. `ยกเว้นภาษีต้องอัตรา 0 (EXEMPT_RATE)`
5. `สถานะไม่ถูกต้อง (BAD_STATUS — ใช้ ใช้งาน/ไม่ใช้งาน/ร่าง)`
6. `รหัสซ้ำ (CODE_DUPLICATE)`

### 9.6 CSV artifacts
Export filename `taxcode_export_{YYYY-MM-DD}.csv` · header `code,name_th,name_en,type,rate,status,used_in` (L912) · BOM `﻿`
Template filename `taxcode_import_template.csv` · header `code,name_th,name_en,type,rate,status` (L807)

---

## §10 · Data Binding & BACKEND anchors

### 10.1 Mock structure
- `state` (L377): filters / sort / pagination(pageSize 8) / drawer / bulkSel / bulk(step) / modal / records
- `state.records` (L389-400): 10 seed records — field: `id, code, name_th, name_en, category, rate, status, used, created_by, created_at, updated_by, updated_at`
- DOA placeholder (L402-403): ทุก record set `approver_role/approved_by/approved_at/approval_chain = null` — เตรียม wire Policy Center (LOCK-DOA-NULL)

### 10.2 BACKEND comment anchors (ในโค้ด)
| บรรทัด | anchor | ความหมาย |
|---|---|---|
| L364 | `// BACKEND: Tax Code = master กลางระดับระบบ ... GL Posting Setup อ้างรหัสจากที่นี่` | master กลาง, soft-ref |
| L365 | `// production: GET /tax-codes — เอกสาร/สินค้าเก็บแค่ code (soft reference)` | → F-TAX-API-01 |
| L402 | `[DOA-ENGINE placeholder]` | DOA null (LOCK-DOA-NULL) |
| L404 | `[NOTIF] รหัสภาษีไม่ emit event เอง` | LOCK-NO-NOTIF |
| L788 | `// mock ไฟล์ที่เลือก — Dev: แทนด้วย parser จริง` | import parser จุด plug (OQ-TAX-IMPORT-PARSE) |

### 10.3 UI trigger → FRD API (จุด plug จริง)
| UI trigger (fn) | FRD API | หมายเหตุ |
|---|---|---|
| `renderList`/`onSearch`/`onFilter`/`quickFilter`/`sortBy`/`goToPage` | **F-TAX-API-01** GET /tax-codes | client-side filter/sort ทั้งหมด → ย้ายเป็น query param |
| `openView(id)` | **F-TAX-API-03** GET /:id | โหลด detail (overview/usage/history) |
| `openCreate` + `saveUnit('create')` | **F-TAX-API-02** POST /tax-codes | auto-code + validate → server |
| `openEdit(id)` + `saveUnit('edit')` | **F-TAX-API-03** (load) + **F-TAX-API-04** PUT /:id | IR-TAX-01 server guard (F-TAX-FN-03) |
| `setStatus(id,st)` (view menu, เดี่ยว) | **F-TAX-API-05** PATCH /:id/status | free transition |
| `bulkSetStatus(st)` | **F-TAX-API-06** POST /bulk-status | หลาย id |
| `openBulkDelete` + `confirmBulkDelete` | **F-TAX-API-07** POST /bulk-delete | used>0 skip |
| `bulkImport`/`bulkPick`/`bulkConfirm` | **F-TAX-API-08** POST /import (`?mode=preview`/`commit`) | 6 error codes รายแถว |
| `exportCSV` | **F-TAX-API-09** GET /export | ตาม filter, BOM |

---

## §11 · Traceability + Drift Log (Brief ↔ FRD ↔ HTML)

### 11.1 3-way traceability
| Brief § | FRD | HTML anchor |
|---|---|---|
| §3 Shell / P-01 List | 01_UI P-01 · API-01 | `renderList()` L437 |
| §4 P-02 Create | 01_UI P-02 · API-02 | `openCreate`/`formHTML('create')` L662/589 |
| §4 P-03 Edit + lock | 01_UI P-03 · API-04 · BR-04 IR-TAX-01 | `openEdit`/`locked` L663/592 |
| §4 P-04 View tabs | 01_UI P-04 · API-03 | `viewHTML`/`switchTab` L744/712 |
| §4 P-04 status menu (เดี่ยว) | API-05 · BR-06 §5.2 | `setStatus` L874 |
| §4 P-05 Import 3-step | 01_UI P-05 · API-08 · §5.6 (6 codes) | `bulkModalHTML`/`bulkValidateRow` L830/796 |
| §4 P-06 Bulk delete | 01_UI P-06 · API-07 · BR-05 | `openBulkDelete`/`confirmBulkDelete` L887/902 |
| §5 bulk status | API-06 · BR-06 | `bulkSetStatus` L882 |
| §8.4 exempt lock | BR-03 LOCK-EXEMPT-0 | `onTypeChange` L650 |
| §8.4 used>0 lock | BR-04 LOCK-IR-TAX-01 | `formHTML` L592-593 · `saveUnit` L694 |
| §9.6 export CSV | API-09 · S-09 | `exportCSV` L910 |
| §9.5 form validation | 05_RULES VR-01..03 | `saveUnit` L674-686 |
| §9.5 import 6 codes | 05_RULES §5.6 | `bulkValidateRow` L796-803 |
| §7.1 Esc chain | 01_UI §1.7 (menu>modal>drawer) | keydown L945-952 |
| §10.2 DOA/NOTIF null | LOCK-DOA-NULL / LOCK-NO-NOTIF | L402-404 |

### 11.2 ⚠️ Drift Log
| # | ประเภท | รายการ | สถานะ / ข้อเสนอ |
|---|---|---|---|
| D-1 | **FRD-only** | **F-TAX-API-10** GET /lookup — ไม่มี UI trigger ใน HTML นี้ | **By-design**: lookup ถูกเรียกจาก downstream (Item Master/เอกสาร) ไม่ใช่หน้านี้ (FRD §2.X Cross-Module). ไม่ใช่ business drift — HTML feature นี้เป็น "ผู้ให้ข้อมูล" ไม่ใช่ผู้เรียก |
| D-2 | **HTML-only** | `downloadTemplate()` (L805) สร้าง CSV template ฝั่ง client — ไม่มี API เฉพาะใน FRD | **By-design**: static template blob (ไม่ต้องมี endpoint). FRD 01_UI P-05 กล่าวถึงปุ่มนี้ แต่ 02_API ไม่ list เป็น API (ถูกต้อง) |
| D-3 | **HTML-only (cosmetic)** | `#overlay-root` (L956) มีใน DOM แต่ไม่ถูกใช้ (drawer/modal เป็น static node) | ไม่กระทบ — Iron #95 comment ระบุ "n/a" เอง |
| D-4 | **cosmetic** | mock user drift: shell `วิภา ผลิตภัณฑ์` vs records `พิมพ์ใจ บัญชี` | ตรงกับ OQ-TAX-06 (FRD ยกไว้แล้ว) — ไม่เงียบ |

> **ไม่มี business drift** — ทุก scope ใน HTML อยู่ใน 9 LOCK ของ FRD §0.11; ไม่มี UI action ที่ FRD ไม่รองรับ, ไม่มี API mutation ที่ HTML ไม่มีทาง trigger (ยกเว้น API-10 downstream by-design).

---

## §12 · Diff จากเวอร์ชันก่อน

**N/A** — ไม่มี HTML เก่าให้ diff (ระบุใน §0). Baseline นี้ = รอบแรก.

> เกร็ดจาก comment ในโค้ด (ประวัติ in-file, ไม่ใช่ diff จริง): L783 `[ถอดออก 2026-08-09] ลบเดี่ยว/หยุดใช้งานผ่าน modal เดิม — แทนด้วย bulk delete + เมนูเปลี่ยนสถานะอิสระ` · L955 PREFLIGHT re-run round 2 (post user-found UX fixes: file-input import / exempt lock-tag / status-menu current-mark).

---

## §13 · 💡 ข้อเสนอ (ไม่ใช่ AS-BUILT — R1)

> ที่เดียวที่คิดเพิ่มได้ — Dev **อย่า** treat เป็น spec.
1. **Search debounce** — ปัจจุบัน `onSearch` re-render ทุก keystroke (L560); production ควร debounce ~250ms + call API-01
2. **Focus-trap ใน drawer/modal** — ไม่มี trap (Tab หลุดออกนอก overlay ได้); เพิ่มเพื่อ a11y
3. **Body scroll-lock** เมื่อ overlay เปิด — ปัจจุบันไม่มี; background list เลื่อนได้ขณะ drawer เปิด
4. **used=mock** — bulk-delete guard พึ่ง `used` ปลอม (FRD OQ-TAX-04, EC-A7 ข้อมูลสูญหาย) — ห้าม enable hard-delete จริงก่อน sync used จริง
5. **`ra-btn.is-disabled`** มี CSS (L212) แต่ไม่ถูกใช้ — ถ้า future เพิ่มปุ่ม row action ที่ conditional ก็พร้อม

---

## 🔍 Verification Gate — F-TAX (Phase 4)

- [x] ทุก route ใน HTML มี section — 1/1 (`#/tax-codes` §2) ✅
- [x] ทุก overlay (3 drawer-mode + 2 modal + 3 pop-menu + toast) มีแถวใน Overlay Registry — 7/7 ✅
- [x] ทุก `showToast` ปรากฏใน Microcopy verbatim — 8/8 ✅
- [x] ทุก component ใน anatomy มี selector anchor ✅
- [x] state matrix ครอบทุก enum (status ×3, category ×3, lock/exempt) ✅
- [x] Esc chain ตรงลำดับ handler จริง (L945-952, menu>modal>drawer) ✅
- [x] z-index map ครบ 8 ตัวที่ประกาศ ✅
- [x] (FRD) ทุก P-01..06 + API-01..10 มีแถว traceability; Drift Log 4 รายการ ไม่เงียบ ✅
- [x] ไม่มีสเปคที่ trace ไม่ได้ (R1) — audit 10 จุด, ทุกจุดชี้บรรทัด/fn ได้ ✅

**Verdict: PASS**
