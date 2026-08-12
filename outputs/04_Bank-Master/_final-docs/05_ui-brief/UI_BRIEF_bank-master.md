# UI Brief — F-BNK บัญชีธนาคาร (Bank Master)

> **ประเภท:** HTML UI Brief (AS-BUILT, extraction-based) · WF-01 · หลัง FRD (SOW3.3) — ก่อน dev handoff
> **หลักการ:** ทุกบรรทัดในบรีฟนี้ trace กลับหา selector / function / ข้อความจริงใน HTML ได้ (R1). ห้ามแต่งสเปคที่ไม่มีในไฟล์ — ข้อเสนอเพิ่มอยู่ §13 เท่านั้น
> **Handoff set:** HTML (source of truth) + FRD Pack (ระบบ/สัญญา API) + **UI Brief (design intent นี้)**

---

## §0 · Document Control + Pairing

| Field | Value |
|---|---|
| Feature | F-BNK — บัญชีธนาคาร (Bank Master) |
| HTML SoT | `01_HTML/f-bank.html` · `<title>` = "บัญชีธนาคาร — CUBE NATIVE" (L6) |
| HTML footer version | Sidebar footer "UAT · v6" (L331) · CI comment "CUBE Warm Light kit — mirrored from product-master golden reference (healed)" (L12) · PREFLIGHT v6.2 self_audit v2 (L1098) |
| Arch | Single-file SPA, vanilla JS, string-template render (`innerHTML`) · Lucide icons (CDN `lucide@0.469.0` L363) · fonts: Noto Sans Thai (Google) + Satoshi (fontshare) |
| FRD Pack | `04_FRD/FRD_F-BNK_Pack/` (01_UI + 05_RULES อ้างในบรีฟนี้) — paired |
| FRD status | **PAIRED** — traceability §11 ครบ P-01..06, API-01..10, BR-01..10. Drift Log §11.2 |
| GL binding | **OPTIONAL** — บันทึกได้โดยไม่ผูกกลุ่ม GL · view เตือนอย่างเดียว (OQ-BNK-02 LOCK, ดู §8.4) |
| DOA | **null placeholder** — ไม่มี approval UI (`approver_role/approved_by/approved_at/approval_chain=null`, set ตอน create L771 + seed L420) |
| Currency | **THB-only** — `สกุลเงิน` = "THB — บาทไทย" `disabled` (L682); ไม่มี multi-currency/SWIFT/IBAN |
| Recent fixes captured | ✅ status menu ปัจจุบัน disabled + "ปัจจุบัน" tag + tidy layout (§5.11, `_fix_shots/01`) · ✅ view header actions ย้ายไปมุมบนขวา (§4 P-04, `_fix_shots/03`) · ✅ import pick ตัด alt-line "ลองด้วยไฟล์ตัวอย่าง" ออก (§4 P-05, `_fix_shots/04`) · ✅ import preview layout (`_fix_shots/02`) |

---

## §1 · Design Tokens AS-BUILT

> สกัดจาก `:root` L13. **ห้าม hardcode hex** — dev ผูกผ่าน token เหล่านี้ (CI CUBE Warm Light).

### 1.1 Color tokens (L13)
| Token | Value | ใช้ที่ |
|---|---|---|
| `--c-navy` | `#111111` | headings (ph-title, dw-title, stat-value), toast default bg |
| `--c-primary` | `#FF3B30` | brand red — ปุ่ม primary, active sidebar, focus ring, bulk count, ★ตัว hover |
| `--c-primary-hover` | `#E62E24` | primary hover |
| `--c-teal` | `#FF9A1F` | accent orange — logo/avatar gradient ปลาย, pulse-dot |
| `--c-ink` | `#111111` | body text |
| `--c-mute` / `--c-mute-2` / `--c-mute-3` | `#54565C` / `#73757B` / `#9A9CA2` | secondary/tertiary text, placeholder, "—", GL-unbound warning |
| `--c-line` / `--c-line-2` / `--c-line-3` | `#DEDAD4` / `#E9E5E0` / `#F1EEEA` | borders (dark→light), hover bg |
| `--c-bg-off` | `#FAF8F5` | ivory page bg, thead, hover |
| `--c-success` | `#1F9D55` | toast success |
| `--c-warning` | `#E8870F` | toast warning, modal warning icon |
| `--c-danger` | `#E62E24` | destructive (ลบ), notif-dot, req-star |

> **หมายเหตุ:** `--c-navy` = ดำ (#111111) ไม่ใช่ navy จริง (kit rebrand) — ชื่อ token คงไว้ backward-compat. Semantic pill tints (status/type/lock/def-star) ใช้ hex ตรงในคลาส (`.pill.is-active` #E4F4EB/#157A41, `.pill.is-inactive` #FFF1DD/#B8690B, `.pill.is-draft` line-3/mute-2 — L169–171) = intentional.

### 1.2 Layout / type / spacing / radius (L13)
- **Layout:** `--sidebar-w: 232px` · `--shell-h: 52px` · body `min-width: 1180px` (L25), html/body `min-width: 768px` (Iron Rule #97, L15)
- **Font tokens:** มีเพียง `--fs-body: 14px` — **ไม่มี --fs scale ชุดเต็ม** (ต่างจาก Payment Term); ขนาดอื่นเป็น inline px (stat-value 26 · ph-title/dw-title 20 · modal-title/empty-title 16 · body 13–14 · meta/hint 11–12.5). Dev ควรผูกเป็น scale ตอน build จริง (§13)
- **Font family:** body = `'Satoshi','Noto Sans Thai',system-ui,sans-serif` (L25) — **Satoshi นำหน้า**; headings (ph-title/dw-title/stat-value) บังคับ `'Noto Sans Thai',sans-serif` (L107,133,242) · เลขบัญชี/code = `.num`/monospace
- **Spacing:** `--sp-xs 4 · sm 8 · md 12 · lg 20 · xl 28`
- **Radius:** `--r-xs 4 · sm 6 · md 8 · lg 12 · full 999`
- **Scrollbar:** 5px, track transparent, thumb `rgba(17,17,17,.14)` (L18–22); sidebar thumb `rgba(255,255,255,.28)` (L23–24)

### 1.3 Z-Index Map (L13 — สูง→ต่ำ)
| z | Token | Layer / selector | Note |
|---|---|---|---|
| **80** | `--z-toast` | `.toast` (L297) | bottom-right host |
| **70** | (adhoc ใน media) | `.sidebar` @≤1180 off-canvas (L96) | mobile drawer sidebar |
| **60** | `--z-modal` | `.modal-backdrop` (L283) | import modal (.is-wide 640) + bulk-delete (440) |
| **51** | `--z-drawer` | `.drawer` (L236) | create/edit/view |
| **50** | `--z-backdrop` | `.drawer-backdrop` (L234) | |
| **30** | `--z-dropdown` | `.pop-menu` — notif/user/status (L77) | ⭐ status menu **คงที่ z-dropdown** (nested ใน drawer header → paint เหนือ dw-body ได้ด้วย DOM order + absolute) — **ไม่ใช้** Iron Rule #95 portal-to-z-modal (ต่างจาก Payment Term, ดู §11.2) |
| **20** | `--z-shell` | `.sidebar` (L32) | |
| **10** | `--z-sticky` | `.shell-bar` (L59) | |
| **2** | (local) | `.table-scroll thead th` sticky (L92) | local stacking ใน card |

---

## §2 · Route / Overlay Map

> HTML = single-view SPA + overlay function calls. `navTo(route)` set `location.hash='#/'+route` (L1081) แต่ทุก hash → `render()` → `renderList()` (view เดียว). Navigation = `openCreate/openEdit/openView` (drawer) · `bulkImport/openBulkDelete` (modal) mutate `state` แล้ว re-render. "route (production)" = เส้นที่เสนอให้ dev ผูก hash 1:1 (จาก 01_UI §1.0/§1.1).

| Surface | Trigger (observed) | Render fn | Route (production เสนอ) | Layer |
|---|---|---|---|---|
| **List** (P-01) | boot / `hashchange` / `render()` | `renderList()` → `#page-content` (L462,537) | `#/finance/bank-master` | in-page |
| **Create** (P-02) | `openCreate()` (L722) | `formHTML('create',{})` (L613) | `…/new` | `#drawer` |
| **Edit** (P-03) | `openEdit(id)` (L723, row pencil L506) | `formHTML('edit',r)` | `…/:id/edit` | `#drawer` |
| **View** (P-04) | `openView(id)` (row click L496) | `viewHTML(r)` (L830) | `…/:id` | `#drawer` |
| **Import CSV** (P-05) | `bulkImport()` (L906, "นำเข้า CSV" L544) | `bulkModalHTML()` 3 steps (L965) | modal overlay | `#modalEl` |
| **Bulk-delete** (P-06) | `openBulkDelete()` (L1023, bulk "ลบ" L515) | inline modal html (L1027) | modal overlay | `#modalEl` |

**Overlay hosts (static ใน body):** `#drawerBackdrop`+`#drawer` (L358–359) · `#modalBackdrop`>`#modalEl` (L360) · `#toast` (L361) · `#overlay-root` static ท้าย body (L1099, ไม่ถูกใช้). ทั้งหมด pre-rendered — เปิด = toggle `.is-open` + inject innerHTML.

**Refresh-safety:** ไม่มี URL persistence จริง — reload = กลับ List เสมอ (mock state ใน memory, E2E R2 #14 `14_reload.png`). Dev ต้อง implement hash routing + deep-link ตาม production route.

---

## §3 · Layout Shell

### 3.1 Sidebar (`.sidebar`, L308–332) — width 232px, bg #111111, z-shell 20
- **Brand:** `.sb-brand` — logo gradient (red→orange, icon `box`) + "CUBE NATIVE" / "Finance · Master Data"
- **Nav modules** (`toggleModule(this)` L1077 — collapse/expand ผ่าน `data-expanded`), ทุก module เปิด default:
  - **Finance** (`master-data`): `ผังบัญชี` (coa) **`.is-disabled`** · `บัญชีธนาคาร` (bank-master) **`.is-active`** ← feature นี้, `onclick="navTo('bank-master')"` (L315) · `วิธีชำระเงิน` (payment-method) **`.is-disabled`**
  - **Inventory:** `สต็อกตามตำแหน่ง` · `รับสินค้า` — ทั้งคู่ `.is-disabled`
  - **System:** `การตั้งค่า` — `.is-disabled`
- **Active state:** `.sb-item.is-active` = bg primary + `::before` white rail (L49–50)
- **Disabled state:** `.is-disabled` = opacity 0.4, cursor not-allowed, hover ไม่เปลี่ยน (L53–54) — ไม่มี title tooltip
- **Footer:** `.sb-footer` pulse-dot + "UAT · v6"

### 3.2 Shell bar (`.shell-bar`, L334–355) — sticky top, height 52px, bg #fff, z-sticky 10
- **Breadcrumb:** `Finance` (a → `navTo('bank-master')`) › `บัญชีธนาคาร` (current)
- **topbar-right** (L336): `.icon-btn` bell + `.notif-dot` → `toggleNotif(event)` → `#notifMenu` (pop-menu z-dropdown 30, 2 บรรทัด static: "มีบัญชีธนาคารใหม่ 2 รายการรอตรวจทาน" / "บัญชี GSB-01 ถูกปิดใช้งานเมื่อวานนี้") · `.user-chip` "พิมพ์ใจ บัญชี / Finance · CUBE NATIVE" avatar "วผ" → `toggleUserMenu(event)` → `#userMenu` (items: โปรไฟล์ / การตั้งค่า / — / ออกจากระบบ danger)
- **ไม่มี** hamburger `.nav-toggle` ใน DOM shell — CSS `.nav-toggle{display:none}` (L94) แสดง @≤1180 (L100) แต่ HTML ไม่ได้วาง element (responsive sidebar เปิดไม่มีปุ่ม trigger บนจอ — ดู §11.2)

### 3.3 Main + content
`.main` margin-left 232px (0 @≤1180) · `.content` = flex column, `height: calc(100vh - topbar 56px)`, overflow-y auto (Iron Rule #96 List Full-Height, L88–89). `.content > .card` flex:1 min-height 320px (flush bottom). `.table-scroll` flex:1 + sticky thead (L91–92). `#page-content` = render target.

### 3.4 Responsive (Iron Rule #97, L95–102, @max-width 1180)
- sidebar → off-canvas `translateX(-100%)`, `.is-open` reveal + scrim `box-shadow 0 0 0 100vmax rgba(17,17,17,0.35)`, z 70
- `.main` margin-left 0 · `.content` padding 16px · `.drawer` → `width: min(920px,100vw)` (⭐ กว้างกว่า desktop 680 — ดู §6 หมายเหตุ)

---

## §4 · Page Anatomy

### P-01 List (`_renderListNow` L463–573)
```
.content #page-content
├─ .ph  → .ph-title "บัญชีธนาคาร" + .ph-count "{total} บัญชี"
│         .ph-actions → "ส่งออก CSV"(exportCSV) · "นำเข้า CSV"(bulkImport) · "เพิ่มบัญชีธนาคาร"(openCreate, primary)
├─ .stats (grid auto-fit minmax200)  → 4× .stat button (stat() L476) : ทั้งหมด/ใช้งานอยู่/ไม่ใช้งาน/ร่าง  [§5.2]
└─ .card
   ├─ .filter-bar → search-box + bank select + status select + spacer + "ล้างตัวกรอง"(ghost)  [§5.3]
   ├─ .bulkbar (conditional selN>0)  → pink bulk bar  [§5.6]
   ├─ .table-scroll → table.utbl (9 col, sticky thead)  [§5.5]
   │     thead: checkbox·รหัส·ธนาคาร/ชื่อบัญชี·เลขที่บัญชี·ประเภทบัญชี·กลุ่มบัญชี GL·ใช้ฝั่ง·สถานะ·จัดการ
   │     tbody: row× (L496) | empty (2 แบบ, L484)
   └─ .tbl-foot → "แสดง {a}–{b} จาก {n} รายการ" + pager (8/หน้า)  [§5.5]
```

### P-02/P-03 Create/Edit drawer (`formHTML` L613–721) — 680px
```
.drawer
├─ .dw-head → avatar(landmark|plus) + eyebrow + title(code|เพิ่ม…) + subtitle(THB) + [X close]
├─ .dw-body
│  ├─ .dw-section "ข้อมูลบัญชี" (form-grid 2col) → รหัส / ธนาคาร* / เลขที่บัญชี* / ชื่อบัญชี* / สาขา / ประเภทบัญชี / พร้อมเพย์
│  ├─ .dw-section "บัญชีแยกประเภท (GL)" → กลุ่มบัญชี GL (native select active-only) + สกุลเงิน(THB disabled)
│  └─ .dw-section "การใช้งาน" → ใช้กับฝั่ง*(2 chk) + บัญชีรับหลัก(chk) + บัญชีจ่ายหลัก(chk) + สถานะ(select 3)
└─ .dw-footer → "ยกเลิก" | spacer | "ยืนยันสร้าง"|"บันทึกการแก้ไข" (#saveBtn, saveBank)
```
**IR-BNK-01 lock (edit + used>0):** `ธนาคาร` + `เลขที่บัญชี` → `disabled` + `<span class="lock-tag"><i lock></i>ล็อก — มีเอกสารผ่านแล้ว</span>` ต่อท้าย label (L618,645,649). Field อื่นแก้ได้. `_e2e_r2_shots/09_locked_fields.png`, `_e2e_shots/03_edit_used_locked.png`.

### P-04 View drawer (`viewHTML`/`viewBody` L830–862) — 680px, tabbed
```
.drawer
├─ .dw-head → avatar(landmark) + eyebrow"บัญชีธนาคาร · {code}" + title"{ธนาคาร} {maskAcct}" + subtitle(pill+ชื่อบัญชี)
│     .dw-head-actions (มุมบนขวา, recent fix) → "แก้ไข"(secondary sm) · "เปลี่ยนสถานะ"(secondary sm → #statusMenu) · divider · [X]
├─ .drawer-tabs → "ภาพรวม"(overview) | "ประวัติ"(history)  (switchTab L784)
├─ .dw-body #viewBody
│  ├─ overview: .sum-row 4 chips (ธนาคาร/เลขที่บัญชี/ใช้กับฝั่ง/กลุ่มบัญชี GL)
│  │            + section "ข้อมูลบัญชี"(def-grid) + section "บัญชีแยกประเภท (GL)"(+GL warning) + section "การใช้งานในเอกสาร"
│  └─ history: .timeline → แก้ไขล่าสุด / สร้างรายการ (actor · date)
└─ .dw-footer → meta "แก้ไขล่าสุด {date}" | spacer | "ปิด"
```
`_e2e_shots/07_view_drawer.png` · `08_view_statusmenu.png` · `09_view_history_tab.png`. GL warning = mute-3 text ใน def-grid val (L818) — **ไม่ใช่** `.hint-card` banner เต็ม (ดู §11.2).

### P-05 Import CSV modal (`bulkModalHTML` L965–1003) — .is-wide 640px, 3 steps
```
.modal.is-wide
├─ modal-header (upload icon) → "นำเข้าบัญชีธนาคารจากไฟล์" + desc + [X]
├─ step pick:    input[type=file accept=.csv hidden] + .upload-box "เลือกไฟล์ CSV" · footer "ดาวน์โหลด template ตัวอย่าง" | "ปิด"
├─ step preview: .import-sum (ok/err count) + table ✓/✗ ต่อแถว · footer "ยกเลิก" | "นำเข้า {ok} แถว"(disabled ถ้า ok=0)
└─ step done:    .import-sum "นำเข้าเสร็จ {ok}…" + skip table(สาเหตุ) · footer "ปิด"
```
`_e2e_shots/14_import_pick.png` · `15_import_preview.png` · `_fix_shots/04_import_pick_noalt.png`.

### P-06 Bulk-delete modal (`openBulkDelete` inline L1027–1036) — 440px
```
.modal
├─ modal-header (danger trash-2) → "ลบบัญชีธนาคาร {N} รายการ?" + desc(บอกยอดข้าม used>0)
└─ modal-footer → "ยกเลิก" | "ลบ {N-used} รายการ"(danger, disabled ถ้า =0)
```
`_e2e_shots/11_bulkdelete_modal.png` · `_e2e_r2_shots/10a_used_delete_blocked.png` · `10b_mixed_delete.png`.

---

## §5 · Component Inventory (anchor + states + ขนาด)

### 5.1 Buttons (`.btn` L112–125)
min-height 36px (`.btn-sm` 30px) · variants: `.btn-primary` (red), `.btn-secondary` (white+border), `.btn-ghost`, `.btn-danger` (white/red→#FFE9E7 hover). States: default/hover (shadow บน primary) · disabled = `:disabled`/`.is-disabled` (opacity .55 + `pointer-events:none`, L123). **Loading state มีจริง** — `#saveBtn` ตอน submit เพิ่ม `.is-disabled` + `<i loader-2 class="spin">กำลังบันทึก…` (L760, spin keyframe L124) = double-submit guard #44 (`_e2e_r2_shots/08_double_submit.png`).

### 5.2 Stat cards (`.stat` button, `stat()` L476)
4 ใบ grid (auto-fit minmax(200px,1fr) L127). โครง: `.stat-label`(icon primary + label) / `.stat-value`(count) / `.stat-meta`. **Interactive filter** → `quickFilter(key)` (L588). States: default · hover (border + shadow) · **`.is-on`** = border primary + ring (L130). `all` reset ทั้ง status+bank; อื่น ๆ toggle-off status (คลิกซ้ำ = กลับ all).
| key | label | meta | on-condition |
|---|---|---|---|
| all | บัญชีทั้งหมด | `{n} ธนาคาร` (unique banks) | `status==='all' && bank==='all'` |
| active | ใช้งานอยู่ | พร้อมใช้ในการรับ/จ่าย | `status==='active'` |
| inactive | ไม่ใช้งาน | ปิดบัญชี/พักใช้ | `status==='inactive'` |
| draft | ร่าง | เตรียมเปิดใช้ | `status==='draft'` |

`_e2e_r1_shots/02a_kpi_active.png` · `02b_kpi_inactive.png` · `02c_kpi_draft.png`.

### 5.3 Filter bar (`.filter-bar` L555–569)
- **Search** (`.fld-width-search` max-width 300px, lead search icon): `oninput="onSearch(this.value)"` (L558). ค้นหา `code + bankLabel + branch + account_no + account_name` (L436). **Refocus** — `onSearch` (L586) re-render แล้ว `.input.focus()` + `setSelectionRange(len,len)` คง caret ปลาย (`_e2e_r2_shots/02_focus_preserve.png`). States: default · focus (border primary + ring L139).
- **Bank select** (`.select.fld-width-sm` 170px, `onFilter('bank',v)` L560): "ทุกธนาคาร" + 9 ธนาคาร (native `<select>`)
- **Status select** (170px, `onFilter('status',v)` L561): ทุกสถานะ / ร่าง / ใช้งาน / ไม่ใช้งาน
- **"ล้างตัวกรอง"** (`.btn-ghost.btn-sm`, `resetFilters()` L568) → reset search+bank+status, page=1

### 5.4 Data table (`.utbl` L147–156, ใน `.table-scroll` sticky thead)
Rows: `td` padding 8×12, border-bottom line-3, cursor pointer, hover bg-off. **9 columns** (colgroup ไม่ fixed — auto width; checkbox th `width:36px` L519):
1. checkbox (select-page `toggleSelPage(this.checked)` L519,1007) — thead ติ๊กเมื่อทุกแถวในหน้าถูกเลือก (`pageAll` L495)
2. **รหัส** (sortable `code`) — `.cell-code` bold + `.def-star` `★รับ` (title "บัญชีรับหลัก") / `★จ่าย` (title "บัญชีจ่ายหลัก") ถ้า default (L498)
3. **ธนาคาร / ชื่อบัญชี** (sortable `bank`) — `.cell-name-th` "{bankLabel} · {branch}" + `.cell-name-en` account_name (L499)
4. **เลขที่บัญชี** (sortable `account_no`) — `.num` (แสดงเต็ม ไม่ mask ในตาราง — ดู PII OQ-BNK-08 §11.2) (L500)
5. **ประเภทบัญชี** (sortable `account_type`) — `.type-pill` acctTypeLabel (L501)
6. **กลุ่มบัญชี GL** (sortable `posting_group`) — `.num` code หรือ mute-3 "—" (L502)
7. **ใช้ฝั่ง** (NOT sortable, col='') — `useText(r)`: "รับ + จ่าย" / "ฝั่งรับ (Receipt)" / "ฝั่งจ่าย (PV)" / "—" (L404,503)
8. **สถานะ** (sortable `status`) — `statusPill(r.status)` (L504)
9. **จัดการ** — `.row-actions` → **ปุ่มแก้ไขเท่านั้น** (`.ra-btn` pencil, `openEdit`) [ไม่มีปุ่มลบเดี่ยว] (L505–507)

Row states: default · hover (bg-off) · **`tr.is-selected td`** (checkbox ติ๊ก → bg #FFF6F5, L189). Row click (นอก checkbox/actions) → `openView(id)`. `<td>` checkbox/actions มี `onclick="stop(event)"` (L497,505).
**Sort** (`sortBy(col)` L594): toggle asc/desc, คอลัมน์ใหม่เริ่ม asc. `th()` (L491) icon: active → arrow-up/arrow-down, ไม่ active → chevrons-up-down. `_e2e_r1_shots/07_sort.png`.
Empty (`rows.length===0` L482–489): **filtered** → icon `search-x` "ไม่พบบัญชีธนาคารที่ตรงกับตัวกรอง" + desc + "ล้างตัวกรอง"(secondary) · **ว่างจริง** → icon `landmark` "ยังไม่มีบัญชีธนาคารในระบบ" + desc + "เพิ่มบัญชีธนาคาร"(primary). `_e2e_shots/13_empty_filter.png` · `_e2e_r2_shots/12_empty_state.png`.
**Pager** (`.pager`/`.pg-btn`, `renderPager` L574): prev chevron (disabled `page<=1`) + เลขหน้า (`.is-active` current) + next chevron (disabled `page>=totalPages`). `goToPage(n)` guard 1..tp. pageSize **8** (L409). `_e2e_r1_shots/08_pager.png`.

### 5.5 Bulk bar (`.bulkbar` L190) ⭐ สีชมพูอ่อน
โผล่เมื่อ `selN>0` (L510), เหนือ `.table-scroll` ใน card. **bg #FFF6F5** (pink) + border line-2 (ไม่ใช่ขาว/ดำ). `.bulkbar-count` "เลือก {N} รายการ" (สี primary red) + ปุ่ม (btn-sm):
- "ตั้งเป็น ใช้งาน" (secondary, circle-check) → `bulkSetStatus('active')`
- "ตั้งเป็น ร่าง" (secondary, file-pen) → `bulkSetStatus('draft')`
- "ตั้งเป็น ไม่ใช้งาน" (secondary, circle-slash) → `bulkSetStatus('inactive')`
- "ลบ" (`.btn-danger`, trash-2) → `openBulkDelete()`
- "ยกเลิกการเลือก" (`.btn-ghost`) → `clearBulkSel()`

`_e2e_shots/10_bulkbar.png` · `_e2e_r1_shots/17a_bulkbar.png`.

### 5.6 Checkbox row — use_in / default (`.chk` L174–176, ใน form section "การใช้งาน")
`.chk-row` gap 16px. แต่ละ `label.chk`: `<input type="checkbox">` (accent primary) + `<span>`. **ใช้กับฝั่ง*** (`fld-use` L689): "ฝั่งรับเงิน (Receipt)" (`in-use-receive`, default checked สำหรับ create เพราะ `r.use_receive!==false` L692) + "ฝั่งจ่ายเงิน (Payment Voucher)" (`in-use-pay`). err "ต้องเลือกอย่างน้อย 1 ฝั่ง". **บัญชีรับหลัก** (`in-def-receive` L699): "ใช้เป็นบัญชีเริ่มต้นของ Receipt (1 บัญชีทั้งระบบ — ตัวเก่าหลุดอัตโนมัติ)". **บัญชีจ่ายหลัก** (`in-def-pay` L703): "ใช้เป็นบัญชีเริ่มต้นของ PV (1 บัญชีทั้งระบบ)".

### 5.7 Inputs / fields (`.field` L257–264)
`.input`/`.select` min-height 36px, border line, radius 8. **`.field.has-err`** → border danger + แสดง `.err` (inline, hidden default, L262–264). `.req-star` = "*" สี danger. **ไม่มี `.field .hint`** ใน form (มติเลน ตัด field-help). numeric fields ใช้ `inputmode="numeric"` (in-acct-no, in-promptpay); spinner ซ่อน (L29–30). `.select` มี custom chevron bg-image (L140). สกุลเงิน = `<input value="THB — บาทไทย" disabled>` (L682).

### 5.8 GL Posting Group picker (`#in-posting-group` `<select>`, `pgOpts` L622)
**Native `<select>`** (ไม่ใช่ sdd combobox — เลือกใช้ browser popup unclippable). Options = `"— ยังไม่ผูกกลุ่ม —"` (value="") + `BANK_POSTING_GROUPS.filter(active || code===bound)` — **active-only + คงตัวที่ผูกไว้เดิม** (SCB draft ยังโชว์ถ้า record ผูกไว้ กัน binding หลุด, L622 comment). Label = `"{code} — {name}"` (+ " (ร่าง)" ถ้าไม่ active). `_e2e_shots/04_edit_scb_glpicker.png` · `_e2e_r2_shots/11_gl_rebind.png`.

### 5.9 Summary chips (view, `.sum-chip` L179, `chip()` L795)
4 ใบ grid 2col (`.sum-row` L178). icon + `.sc-lbl` + `.sc-val`: ธนาคาร(landmark) · เลขที่บัญชี(hash) · ใช้กับฝั่ง(arrow-left-right, useText) · กลุ่มบัญชี GL(book-open, code หรือ "ยังไม่ผูก").

### 5.10 View def-grid + timeline (`.def-grid` L265, `.timeline` L271)
`.def-grid` = grid 150px/1fr, lbl mute + val ink. GL section val = `pgLabel(code)` หรือ mute-3 warning (§8.4). History tab `.timeline` = tl-dot + tl-act + tl-meta (2 รายการ: แก้ไขล่าสุด / สร้างรายการ, `fmtDate` แปลง พ.ศ. L1060).

### 5.11 Status change menu (`.pop-menu.status-menu` L207–212, `#statusMenu`)
Dropdown ใน view header (position:relative parent, z-dropdown 30). `toggleStatusMenu(e)` (L1017) — `stop(e)` + closeMenus + toggle. `.pm-label` "เปลี่ยนสถานะเป็น" + 3 `.pm-item` (active/inactive/draft, L845). **ค่าปัจจุบัน** = `.is-current` + `disabled` + `<span class="pm-cur">ปัจจุบัน</span>` (opacity .55, cursor not-allowed) — recent fix. Pick → `setStatus(id,st)` (L1009). `_fix_shots/01_statusmenu.png` · `_e2e_r2_shots/03_status_menu_zindex.png`.

---

## §6 · Overlay Registry + Dismiss Rules

| Overlay | selector | ขนาด | z | เปิด | ปิดได้โดย | Backdrop | Anim |
|---|---|---|---|---|---|---|---|
| **Create/Edit drawer** | `.drawer` | **680px** (→min(920,100vw)@≤1180) | 51 | openCreate/openEdit | Esc · backdrop click · X · "ยกเลิก" | rgba(17,17,17,.40) z50 | translateX 280ms cubic-bezier |
| **View drawer** | `.drawer` | 680px | 51 | openView | Esc · backdrop · X · "ปิด" | same | same |
| **Import modal** | `.modal.is-wide` | 640px | 60 | bulkImport | Esc · backdrop click · X · "ปิด"/"ยกเลิก" | rgba(17,17,17,.40) z60 | scale .96→1 180ms |
| **Bulk-delete modal** | `.modal` | 440px | 60 | openBulkDelete | Esc · backdrop click · X(none) · "ยกเลิก" | same | scale .96→1 |
| **notif / user menu** | `.pop-menu` | 240px | 30 | toggleNotif/User | document click (closeMenus) · toggle ซ้ำ | — | — |
| **status menu** | `.pop-menu.status-menu` | 214px | 30 | toggleStatusMenu | document click · toggle ซ้ำ · pick · Esc→closeMenus | — | — |
| **Toast** | `.toast` | ≤380px | 80 | showToast | auto (**3500ms คงที่ ทุก variant**) | — | translateY(100)→0 250ms |

**⭐ หมายเหตุขนาด drawer:** desktop (>1180) = **680px** (L236) — task brief เขียน "920px" แต่ **HTML คือ source of truth**; 920 ปรากฏเฉพาะ media query @≤1180 (`width:min(920px,100vw)` L101) ซึ่งกว้างกว่า desktop โดยตั้งใจ. Dev ยึด 680 เป็น base.

**Drawer/modal content:** drawer inner ไม่มี stopPropagation แยก (backdrop เป็น sibling element L358); modal `#modalEl` มี `onclick="stop(event)"` (L360) กัน backdrop-close. `.dw-body` overflow-y auto + `scrollbar-gutter:stable`.

**Toast (`.toast` L297, `showToast` L1065):** **bottom-right** (`bottom:24px; right:24px`). Variants icon+bg: success `check-circle`/#1F9D55 · error `x-circle`/(base navy — ไม่มี `.is-error` class, fallback navy) · warning `alert-triangle`/#E8870F · info `info`/**#FF3B30 primary** (`.is-info`=primary L300). **Duration 3500ms คงที่** (L1073, `toastTimer`) — ไม่แยกตาม variant (ต่างจาก Payment Term). [หมายเหตุ: `showToast` map icon สำหรับ `error` แต่ CSS ไม่มี `.toast.is-error` → ใช้ bg navy default; ดู §11.2.]

---

## §7 · Interaction Spec

### 7.1 Esc chain (L1088–1094) ⭐ handler เดียว, else-if
```
keydown Escape:
  1. state.modal.open   → closeModal(); return
  2. state.drawer.open  → closeDrawer(); return
  3. else               → closeMenus()   (ปิด pop-menu ทั้งหมด)
```
ลำดับ **modal > drawer > menu** (ตรง 01_UI §1.7). ไม่มีชั้น sidebar off-canvas ใน Esc.

### 7.2 Click-outside
- **pop-menu (notif/user/status):** `document.addEventListener('click', closeMenus)` (L1087) — คลิกที่ใดก็ปิดเมนูทั้งหมด. เปิดเมนูใช้ `stop(e)` กันปิดตัวเอง (L1017,1079,1080)
- **drawer:** `#drawerBackdrop onclick="closeDrawer()"` (L358)
- **modal:** `#modalBackdrop onclick="closeModal()"` + `#modalEl onclick="stop(event)"` (L360)

### 7.3 Selection / bulk
`toggleSel(id,on)` (L1006) toggle 1 row → renderList. `toggleSelPage(on)` (L1007) select/deselect ทุกแถว**ในหน้าปัจจุบัน** (getPageRows(getFiltered())). `clearBulkSel()` (L1008) reset. thead checkbox `pageAll` = ทุกแถวในหน้าถูกเลือก (L495).

### 7.4 Drawer / modal open-close (L599–610, L866–867)
`openDrawerShell(html)` = inject innerHTML + backdrop `.is-open` + drawer `.is-open` (CSS transition เล่นเอง) + `state.drawer.open=true` + renderIcons. `closeDrawer` = remove `.is-open` + reset state. `openModalShell` = inject + `.is-wide` toggle ตาม `state.modal.type==='bulk'` + backdrop open. **ไม่มี** double-rAF slide trick (ต่างจาก PT) — static host + CSS transition พอ.

### 7.5 Scroll preservation (Iron Rule #29, `_keepScroll` L450–459) ⭐
Wrap `renderList` (L462). เก็บ+คืน scrollTop **3 ชั้น**: `.content` · `.table-scroll` · `.dw-body`. คืนใน `requestAnimationFrame` **เฉพาะเมื่อ s>0** (กัน reset ไม่จำเป็น). ครอบ search/filter/sort/bulk/toggle. `_e2e_r2_shots/01_scroll_preserve.png` · `_e2e_shots/06_scroll_after_toggle.png` · `06b_scroll_short_viewport.png`.

### 7.6 Text inputs ไม่ re-render ทุกตัวอักษร
Form inputs (`in-*`) **ไม่มี oninput handler** — อ่านค่าตอน `saveBank()` ผ่าน `document.getElementById(...).value` (L728–740). ไม่ re-render ระหว่างพิมพ์ = caret ไม่กระโดด. เฉพาะ list search (`onSearch`) ที่ re-render + refocus (§5.3).

### 7.7 Shell chrome
`toggleModule(btn)` (L1077) collapse/expand module ผ่าน `data-expanded`. `navTo(route)` set hash (L1081). `renderIcons()` (L367) = `lucide.createIcons()` เรียกหลังทุก inject.

---

## §8 · State-Driven UI Matrix

### 8.1 Status enum → pill (`statusLabel` L401, `statusPill` L402)
| status | label | pill class | icon |
|---|---|---|---|
| `draft` | ร่าง | `pill is-draft` (grey line-3/mute-2) | file-pen |
| `active` | ใช้งาน | `pill is-active` (green #E4F4EB/#157A41) | circle-check |
| `inactive` | ไม่ใช้งาน | `pill is-inactive` (amber #FFF1DD/#B8690B) | circle-slash |

> **3 สถานะอิสระ** — เปลี่ยนได้ทุกทิศ, ไม่มีอนุมัติ (05_RULES §5.2). **ไม่มี dead status** (ไม่มี archived legacy). **Side effect:** ออกจาก active (menu/bulk/form) → `default_receive=false`+`default_pay=false` (★ ทั้ง 2 ฝั่งหลุด, `setStatus` L1012 / `bulkSetStatus` L1020).

### 8.2 Reference lists
- **BANKS 9** (`BANKS` L373, `bankLabel` L384): KBANK กสิกรไทย · SCB ไทยพาณิชย์ · BBL กรุงเทพ · KTB กรุงไทย · TTB ทีเอ็มบีธนชาต · BAY กรุงศรีอยุธยา · GSB ออมสิน · UOB ยูโอบี · OTHER อื่น ๆ. (05_RULES BR-10 = CONFIGURABLE, ห้าม hardcode)
- **ACCT_TYPES 3** (`ACCT_TYPES` L385, `acctTypeLabel` L390): savings ออมทรัพย์ (default) · current กระแสรายวัน · fixed ฝากประจำ
- **BANK_POSTING_GROUPS** (L393): KBANK=active · SCB=draft (mock; production ยิง F-PG-API-01 `?kind=bank&status=active` — ดู drift EC-06 §11.2)

### 8.3 use side (`useText` L404) + ★ default
| use_receive | use_pay | useText | ★ |
|---|---|---|---|
| ✓ | ✓ | รับ + จ่าย | default_receive / default_pay อิสระ |
| ✓ | ✗ | ฝั่งรับ (Receipt) | ★รับ ได้ |
| ✗ | ✓ | ฝั่งจ่าย (PV) | ★จ่าย ได้ |
| ✗ | ✗ | — | (invalid — บล็อก save) |

★ default = radio **1 ตัว/ฝั่งทั้งระบบ** — ตั้งใหม่ตัวเก่าหลุด (`saveBank` L762–763 clear other). **DEFAULT_GUARD:** ★ ต้องอยู่ฝั่งที่เปิด + status='active' (L755, ไม่ผ่าน → toast error, §9.1).

### 8.4 GL binding (OPTIONAL)
| state | UI (view, `viewBody` L818) |
|---|---|
| ผูกกลุ่ม | val = `pgLabel(code)` = "{code} — {name}" + resolve "ตามกลุ่ม {code} ใน GL Posting Group" |
| **ยังไม่ผูก** | val = mute-3 `"ยังไม่ผูก — GL post ไม่ได้จนกว่าจะผูกกลุ่ม"` + resolve "—" · summary chip = "ยังไม่ผูก" |

บันทึกได้โดยไม่ผูก (ไม่มี validation บล็อก) — view เตือนอย่างเดียว (BR-04, OQ-BNK-02 LOCK).

### 8.5 IR-BNK-01 lock (edit + used>0)
`locked = isEdit && (r.used||0)>0` (L617). → `in-bank` + `in-acct-no` `disabled` + lock-tag ต่อ label. **Logic guard** (L766): `if(!locked){ data.bank=bank; data.account_no=acctNo; }` — แม้ฝืน DOM ก็ไม่ assign 2 field นี้. `used` ไม่โชว์บนจอที่ใดเลย. bulk-delete ข้าม used>0.

### 8.6 Mode → drawer chrome
| mode | eyebrow | title | footer submit | avatar |
|---|---|---|---|---|
| create | บัญชีธนาคารใหม่ | เพิ่มบัญชีธนาคาร | ยืนยันสร้าง | plus |
| edit | แก้ไขบัญชีธนาคาร | {code} | บันทึกการแก้ไข | landmark |
| view | บัญชีธนาคาร · {code} | {ธนาคาร} {maskAcct} | ปิด | landmark |

---

## §9 · Microcopy (VERBATIM)

### 9.1 Toasts (`showToast`, ทุก call)
| ข้อความ | variant | trigger |
|---|---|---|
| `บัญชีหลักต้องอยู่ฝั่งที่เปิดใช้ และสถานะ "ใช้งาน" เท่านั้น` | error | DEFAULT_GUARD (L756) |
| `บันทึกการแก้ไข "{code}" แล้ว` | success | saveBank edit (L769) |
| `เพิ่มบัญชีธนาคาร "{code}" แล้ว` | success | saveBank create (L772) |
| `เปลี่ยนสถานะ "{code}" เป็น {label} แล้ว` | success | setStatus (L1015) |
| `เปลี่ยนสถานะ {n} รายการ เป็น {label} แล้ว` | success | bulkSetStatus (L1021) |
| `ลบแล้ว {del} รายการ` (+ ` · ข้าม {skip} (มีเอกสารผ่านแล้ว)`) | success / **warning** ถ้ามีข้าม | confirmBulkDelete (L1044) |
| `นำเข้าแล้ว {ok} รายการ` (+ ` · ข้าม {err} แถว (IMPORT_ERROR)`) | success / **warning** ถ้ามี err | bulkConfirm (L963) |
| `โหมดสาธิตรองรับเฉพาะ .csv — .xlsx ให้ save as CSV ก่อน (dev: parser จริงตอน integrate)` | warning | bulkFileChosen non-csv (L928) |
| `ไม่พบข้อมูลในไฟล์ หรือหัวคอลัมน์ไม่ตรง template` | warning | parse empty (L934) |
| `ดาวน์โหลด template ตัวอย่างแล้ว` | success | downloadTemplate (L904) |
| `ส่งออก {n} รายการเป็น CSV แล้ว` | success | exportCSV (L1054) |

### 9.2 Field errors (inline `.err`)
| ข้อความ | ที่ | dynamic |
|---|---|---|
| `รหัสนี้ถูกใช้แล้ว` → `รหัส {finalCode} ถูกใช้แล้ว` | fld-code / err-code (L642,746) | ✅ |
| `เลขบัญชี 10–12 หลัก (ใส่ขีดได้)` | fld-acct-no / err-acct (L651) | |
| `เลขบัญชีนี้มีในทะเบียนแล้ว (ACCT_DUPLICATE)` | err-acct override (L751) | ✅ |
| `กรุณากรอกชื่อบัญชี` | fld-acct-name (L656) | |
| `ต้องเป็นเบอร์ 10 หลัก หรือเลขภาษี 13 หลัก` | fld-promptpay (L669) | |
| `ต้องเลือกอย่างน้อย 1 ฝั่ง` | fld-use (L695) | |

### 9.3 Import row-validate reasons (`bulkValidateRow` L883 + `bulkLoadRows` L914)
`ข้อมูลบังคับไม่ครบ (REQUIRED)` · `ธนาคารไม่รู้จัก (BAD_BANK)` · `เลขบัญชี 10–12 หลัก (ACCT_INVALID)` · `เลขบัญชีซ้ำทะเบียน (ACCT_DUPLICATE)` · `ประเภทบัญชีไม่ถูกต้อง (BAD_TYPE)` · `ฝั่งใช้งานไม่ถูกต้อง (BAD_USE — รับ/จ่าย/ทั้งสอง)` · `สถานะไม่ถูกต้อง (BAD_STATUS — ใช้ ใช้งาน/ไม่ใช้งาน/ร่าง)` · `รหัสซ้ำ (CODE_DUPLICATE)` · `รหัสซ้ำในไฟล์ (IN_FILE_DUPLICATE)` · `เลขบัญชีซ้ำในไฟล์ (IN_FILE_DUPLICATE)`. Preview cell: `✓ พร้อมนำเข้า` (pill is-active) / `✗ {err}` (pill is-inactive, title=err) (L990).

### 9.4 Placeholders
- list search `ค้นหารหัส ธนาคาร สาขา หรือเลขบัญชี…`
- code `เช่น KBANK-01 (เว้นว่าง = สร้างอัตโนมัติ)` · เลขที่บัญชี `เช่น 012-3-45678-9` · ชื่อบัญชี `เช่น บริษัท คิวบ์ เนทีฟ จำกัด` · สาขา `เช่น สำนักงานใหญ่` · พร้อมเพย์ `เบอร์มือถือ 10 หลัก / เลขภาษี 13 หลัก (ถ้ามี)`

### 9.5 Labels / buttons / sections / notes
- **Buttons:** `เพิ่มบัญชีธนาคาร` · `ส่งออก CSV` · `นำเข้า CSV` · `ยืนยันสร้าง` · `บันทึกการแก้ไข` · `ยกเลิก` · `แก้ไข` · `เปลี่ยนสถานะ` · `ปิด` · `ล้างตัวกรอง` · `ดาวน์โหลด template ตัวอย่าง` · bulk `ตั้งเป็น ใช้งาน`/`ตั้งเป็น ร่าง`/`ตั้งเป็น ไม่ใช้งาน`/`ลบ`/`ยกเลิกการเลือก` · saving `กำลังบันทึก…`
- **Section titles:** `ข้อมูลบัญชี` · `บัญชีแยกประเภท (GL)` · `การใช้งาน` (form) · `ข้อมูลบัญชี`/`บัญชีแยกประเภท (GL)`/`การใช้งานในเอกสาร`/`ประวัติการเปลี่ยนแปลง` (view)
- **Field labels:** `รหัส` · `ธนาคาร *` · `เลขที่บัญชี *` · `ชื่อบัญชี *` · `สาขา` · `ประเภทบัญชี` · `พร้อมเพย์ผูกบัญชี` · `กลุ่มบัญชี GL (Bank Posting Group)` · `สกุลเงิน` · `ใช้กับฝั่ง *` · `บัญชีรับหลัก` · `บัญชีจ่ายหลัก` · `สถานะ`
- **GL picker options:** `— ยังไม่ผูกกลุ่ม —` · `{code} — {name}` (+ ` (ร่าง)`)
- **Currency (disabled):** `THB — บาทไทย`
- **Lock-tag:** `ล็อก — มีเอกสารผ่านแล้ว` · **def-star:** `★รับ` / `★จ่าย` (view: `★ บัญชีรับหลัก` / `★ บัญชีจ่ายหลัก`)
- **View chips/rows:** `ธนาคาร` · `เลขที่บัญชี` · `ใช้กับฝั่ง` · `กลุ่มบัญชี GL` · `บัญชีเงินฝาก (resolve)` · `ฝั่งรับเงิน (Receipt)` · `ฝั่งจ่ายเงิน (PV)` · GL warning `ยังไม่ผูก — GL post ไม่ได้จนกว่าจะผูกกลุ่ม` · resolve `ตามกลุ่ม {code} ใน GL Posting Group`
- **View footer meta:** `แก้ไขล่าสุด {date}` · **timeline:** `แก้ไขล่าสุด` / `สร้างรายการ`
- **Import modal:** title `นำเข้าบัญชีธนาคารจากไฟล์` · desc `ไฟล์ CSV — ระบุสถานะได้ในไฟล์ · เพิ่มรายการใหม่เท่านั้น` · upload `เลือกไฟล์ CSV` + hint `คลิกเพื่อเลือกไฟล์ .csv จากเครื่อง · หัวคอลัมน์ตาม template · เพิ่มรายการใหม่เท่านั้น` · preview sum `ตรวจแล้ว {N} แถว — นำเข้าได้ {ok} · ติดปัญหา {x} (แถวผิดจะถูกข้าม)` · `นำเข้า {ok} แถว` · done `นำเข้าเสร็จ {ok} รายการ (สถานะตามไฟล์)` (+ ` · ข้าม {err} แถว (IMPORT_ERROR)`) · file label `ไฟล์: {name}`
- **Import preview table headers:** `รหัส` · `ธนาคาร / สาขา` · `เลขบัญชี` · `ฝั่ง` · `สถานะ` · `ผลตรวจ`
- **Bulk-delete modal:** title `ลบบัญชีธนาคาร {N} รายการ?` · desc(used>0) `มี {used} รายการมีเอกสารรับ/จ่ายผ่านแล้ว — จะถูกข้าม ไม่ลบ (ใช้เปลี่ยนสถานะแทน)` · desc(none) `การกระทำนี้ย้อนกลับไม่ได้` · `ลบ {D} รายการ`
- **Empty states:** `ไม่พบบัญชีธนาคารที่ตรงกับตัวกรอง` / `ลองปรับคำค้นหรือล้างตัวกรองเพื่อดูรายการทั้งหมด` · `ยังไม่มีบัญชีธนาคารในระบบ` / `เริ่มต้นด้วยการเพิ่มบัญชีธนาคารแรกของบริษัท`
- **Table footer:** `แสดง {a}–{b} จาก {n} รายการ`
- **Status menu:** `เปลี่ยนสถานะเป็น` · `ปัจจุบัน`
- **Notif menu:** `การแจ้งเตือน` · `มีบัญชีธนาคารใหม่ 2 รายการรอตรวจทาน` · `บัญชี GSB-01 ถูกปิดใช้งานเมื่อวานนี้`

---

## §10 · Data Binding & BACKEND anchors

### 10.1 Mock state (`state` L406) → API (จาก 01_UI Actions)
| Mock action | ผูก API (FRD 02_API) |
|---|---|
| `state.records[]` (8 seed L419–428) | `F-BNK-API-01` GET /bank-accounts (list+filter+sort+counts) |
| row click → `openView` | `F-BNK-API-03` GET /bank-accounts/:id |
| `saveBank('create')` (L770) | `F-BNK-API-02` POST /bank-accounts |
| `saveBank('edit',id)` (L767) | `F-BNK-API-04` PUT /bank-accounts/:id (guard bank+account_no เมื่อ used>0) |
| `setStatus(id,st)` (L1009) | `F-BNK-API-05` POST /:id/status |
| `bulkSetStatus(st)` (L1018) | `F-BNK-API-06` POST /bulk-status |
| `confirmBulkDelete()` (L1038, skip used>0) | `F-BNK-API-07` POST /bulk-delete |
| `bulkLoadRows` preview (L908) | `F-BNK-API-08` (validate/preview) |
| `bulkConfirm()` merge-only (L950) | `F-BNK-API-09` (commit import) |
| `exportCSV()` (L1046, ตาม filter) | `F-BNK-API-10` GET /export |
| GL picker `pgOpts` (L622) | `F-PG-API-01` GET /gl/posting-groups?kind=bank&status=active (generic, ไม่มี endpoint เฉพาะ Bank Master) |
| Receipt/PV picker (downstream) | `F-BNK-FN-13b` GET /active?side= — **ไม่มี UI ในไฟล์นี้** (consumer ปลายทาง, BR-05) |

### 10.2 Record shape (seed L420) — fields ที่ BE ต้องรองรับ
`id · code · bank(9 enum) · branch · account_no · account_name · account_type(3 enum) · promptpay_id · posting_group(soft-ref F-PG code) · use_receive · use_pay · default_receive · default_pay · status(3) · used(int, ไม่โชว์) · created_by/at · updated_by/at · approver_role/approved_by/approved_at/approval_chain(=null)`.

### 10.3 BACKEND comments (in-file anchors)
- L369–371: Bank Master = ทะเบียนบัญชีเงินฝากบริษัท (รับ Receipt / จ่าย PV) · เอกสารเก็บ `code` soft-ref + snapshot ตอนบันทึก · `posting_group` soft-ref → GL Posting Group (kind=bank) — ไม่เก็บ COA ตรง (มาตรฐาน BC Bank Posting Group)
- L372, L682: `currency=THB` เท่านั้น (LOCK THB-only) — multi-currency นอก scope
- L615–616: IR-BNK-01 — `used>0` ล็อก ธนาคาร+เลขที่บัญชี (เปลี่ยนเลข = เปิดบัญชีใหม่แทน) · `used` = count Receipt/PV posted
- L392: cross-file as-built — KBANK=active, SCB=draft · picker active-only + คงตัวผูกเดิม · OQ-BNK-02 binding OPTIONAL

### 10.4 DOA placeholder (L420 seed, L771 create)
`approver_role/approved_by/approved_at/approval_chain=null` — comment "ไม่มีสายอนุมัติใน master นี้". **ไม่มี approval UI.** Wire → Policy Center (future).

### 10.5 Server-side mirror (Control C4)
`saveBank()` (8 validations) + `bulkValidateRow()` = mirror ของ BE. HTML = mock synchronous (setTimeout 500ms); production = server mirror ทุกข้อ (05_RULES §5.4).

---

## §11 · Traceability + Drift Log

### 11.1 3-way trace (Brief ↔ FRD ↔ HTML)
| Brief § | FRD anchor | HTML anchor |
|---|---|---|
| §2 route map | 01_UI §1.0/§1.1 P-01..06 | render fns L462/613/830/965/1027 · navTo L1081 |
| §3 shell | 01_UI §1.2 P-01 ERP context | sidebar L308 · shell-bar L334 |
| §4/§5.4 List+table | 01_UI P-01 · API-01 | _renderListNow L463 · row L496 |
| §5.5 bulk bar | 01_UI P-01 bulk · API-06/07 | .bulkbar L510,190 |
| §5.8 GL picker active-only+keep-bound | 01_UI P-02 · BR-04 · FN-14 · EC-04 | pgOpts L622 |
| §5.11 status menu (ปัจจุบัน disabled) | 01_UI P-04 · BR-09 state | statusMenu L843 · setStatus L1009 |
| §7.1 Esc chain modal>drawer>menu | 01_UI §1.7 | keydown L1088 |
| §7.5 scroll preserve #29 | 01_UI §1.0 CI Locks | _keepScroll L450 |
| §8.1 status pill (3, no dead) | 05_RULES §5.2 | statusPill L402 |
| §8.3 use side + ★ radio + DEFAULT_GUARD | 05_RULES BR-03 · FN-03/05/08 | useText L404 · saveBank L755,762 |
| §8.4 GL binding OPTIONAL + warning | 05_RULES BR-04 · OQ-BNK-02 LOCK | viewBody L818 |
| §8.5 IR-BNK-01 lock + guard | 05_RULES BR-02 · EC-01 · OQ-BNK-03 LOCK | formHTML L617 · saveBank L766 |
| §9.1 toasts | 05_RULES §5.6 · 06_TESTS §6.10 | showToast calls (§9.1) |
| §9.2/§9.3 validation | 05_RULES §5.4 (8 form + import) | saveBank L742 · bulkValidateRow L883 |
| §5.4 col4 account_no mask (PII) | 05_RULES §5.7 D11 · OQ-BNK-08 | maskAcct L398 (view header เท่านั้น) |
| §10.4 DOA null | 05_RULES §5.7 D15 | L420,771 |
| §6 import modal 3-step merge-only | 01_UI P-05 · BR-07 · API-08/09 | bulkModalHTML L965 |
| §6 bulk-delete guard used>0 | 01_UI P-06 · BR-02 · API-07 | openBulkDelete L1023 · confirmBulkDelete L1038 |

**F-BNK-FN-13b GET /active?side=** = backend-only downstream picker (Receipt/PV) — **ไม่มี UI ในไฟล์นี้** (ถูกต้อง — consumer ปลายทางเรียก, BR-05).

### 11.2 ⚠️ Drift Log
| # | ประเภท | รายการ | สถานะ / ข้อเสนอ |
|---|---|---|---|
| D-1 | **HTML-only (dead)** | `bulkPickDemo()` (L922) + `BULK_SAMPLE` (L875) — เดิม wire กับ alt-line "ลองด้วยไฟล์ตัวอย่าง" ที่ **ถูกตัดออก** (recent fix, `_fix_shots/04`) · ตอนนี้ function/data ยังอยู่แต่ **ไม่มีปุ่มเรียก** | ไม่กระทบ spec. **ข้อเสนอ:** prune ออกจาก HTML |
| D-2 | **HTML-only (dead CSS)** | `.type-pill` ประกาศ 2 ครั้ง (L163 blue #E6F0FF override → L184 paper/mute grey — ตัวหลังชนะ) · `.toast.is-info`=primary red (L300) แต่ไม่มี `.toast.is-error` class (showToast map icon `x-circle` variant error → fallback bg navy) · `.hint-card`/`.hint-card.is-warning` (L268) มี CSS แต่ view ใช้ mute-3 span แทน banner | Cosmetic. **ข้อเสนอ:** เพิ่ม `.toast.is-error` (danger bg) หรือใช้ warning; prune type-pill ซ้ำ |
| D-3 | **HTML gap (responsive)** | `.nav-toggle` มี CSS (L94,100) แต่ **ไม่มี element ใน DOM** shell — @≤1180 sidebar off-canvas เปิดไม่ได้ (ไม่มีปุ่ม hamburger trigger) | **ข้อเสนอ:** เพิ่มปุ่ม `.nav-toggle` ใน shell-bar + `toggleSidebar()` (ดู §13) |
| D-4 | **Naming (task vs HTML)** | task brief ระบุ drawer "920px" — **HTML desktop = 680px** (L236); 920 เฉพาะ media @≤1180 (L101) | HTML wins (Reverse Mode). Base = 680 |
| D-5 | **FRD-only (production)** | RBAC roles + 403 (05_RULES §5.3) · audit log + read-access-log (D9/D11) · optimistic lock `If-Match`/`ERR_STALE_DATA` (EC-08) · `Idempotency-Key` (EC-09) · multi-tenant RLS (D17) | คาดไว้ — HTML mock client-side. dev implement ฝั่ง server |
| D-6 | **FRD-only (open)** | `used` definition (นับ draft?) OQ-BNK-07 · masking level ตาราง/def-grid OQ-BNK-08 · posting_group source drift (mock KBANK+SCB vs f-postgrp as-built) OQ-BNK-06/EC-06 | ยัง OPEN — spec ก่อน dev commit guard/PII |
| D-7 | **นอก scope feature** | sidebar `ผังบัญชี`/`วิธีชำระเงิน`/Inventory/Settings = `.is-disabled` · notif/user menu = static mock (`toggleNotif` popover, ไม่มี event) | คนละ feature — ไม่ใช่ drift ของ F-BNK. ยืนยัน disabled ถูกต้อง |

> **สรุป:** ไม่มี drift เชิง business ที่ขัด LOCK. HTML-only (D-1/D-2) = สะสางฝั่ง HTML · D-3 = responsive gap ควรแก้ · FRD-only (D-5/D-6) = production/open concern ที่ไม่ปรากฏบน mock UI ตามคาด.

---

## §12 · Diff จากเวอร์ชันก่อน
ไม่ได้ diff กับไฟล์ก่อนหน้าใน brief นี้ (input = ไฟล์ปัจจุบันเดียว). Recent fixes ที่ captured จาก QC `_fix_shots/`: status menu ปัจจุบัน disabled + "ปัจจุบัน" tag (`01`) · import preview layout (`02`) · view header actions มุมบนขวา (`03`) · import pick ตัด alt-line (`04`). **ถ้าต้องการ diff จริง → รัน `html-ui-brief` โหมด Section 12 พร้อม 2 ไฟล์.**

---

## §13 · 💡 ข้อเสนอ (ไม่ใช่ AS-BUILT — R1)
> ต่อไปนี้ **ไม่ใช่สเปคปัจจุบัน** — เสนอให้พิจารณาแยกจากการ build 1:1
1. **เพิ่มปุ่ม `.nav-toggle` (hamburger)** ใน shell-bar + `toggleSidebar()` — CSS responsive มีแล้ว (L94–100) แต่ขาด trigger element → @≤1180 เปิด sidebar ไม่ได้ (D-3).
2. **เพิ่ม `.toast.is-error`** (bg danger) — ปัจจุบัน variant error ตกไป bg navy default (D-2); error สำคัญ (DEFAULT_GUARD) ควรเด่นเป็นสีแดง.
3. **--fs scale tokens** — ไฟล์นี้มีเพียง `--fs-body`; ขนาดอื่น inline px กระจาย. ผูกเป็น scale (h1/h2/kpi/meta) ตอน build จริงเพื่อ maintainability.
4. **status/notif/user menu Esc + focus trap** — ปัจจุบันปิดด้วย document-click/toggle; เพิ่ม dismiss ที่ชัดเจน + a11y focus จะดีขึ้น.
5. **PII masking ตาราง/def-grid** — account_no แสดงเต็มทุกที่ยกเว้น view header (OQ-BNK-08 OPEN, D-6) — รอ spec ปิดก่อน implement.
6. **Loading state list/bulk** — มี loader เฉพาะ save; list/bulk/import ที่ยิง API จริงควรมี skeleton/disabled (production networked).
7. **Prune dead code** (D-1/D-2): `bulkPickDemo`/`BULK_SAMPLE`, type-pill ซ้ำ, hint-card ไม่ใช้.

---

*Extraction-based · ทุก anchor อ้าง selector/function/บรรทัดจริงใน `f-bank.html`. GL binding=OPTIONAL. IR-BNK-01 lock ธนาคาร+เลขบัญชี (used ไม่โชว์). THB-only. DOA=null. Toast bottom-right 3500ms. Drawer 680px.*
