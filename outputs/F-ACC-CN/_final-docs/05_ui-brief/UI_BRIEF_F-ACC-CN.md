# UI Brief (AS-BUILT) — ใบลดหนี้ลูกค้า (Credit Note) · F-ACC-CN / F096

> **EXTRACTION-BASED (Iron Rule R1)** — ทุกบรรทัดสกัดจาก `F-ACC-CN_credit-note.html` (source of truth) เท่านั้น · ทุก claim ชี้ selector / function / ข้อความจริงได้ · ข้อเสนอที่ไม่ได้ AS-BUILT อยู่ §13 เท่านั้น
> คู่กับ: **HTML (จอจริง)** + **FRD Pack** (`FRD_Pack/` — anchor ระบบ) + บรีฟนี้ (design intent)

---

## §0 · Document Control + Pairing

| | |
|---|---|
| Feature | F-ACC-CN · F096 · ใบลดหนี้ลูกค้า (Credit Note) |
| HTML source | `outputs/F-ACC-CN/F-ACC-CN_credit-note.html` · 988 บรรทัด · single-file SPA (vanilla JS) |
| `<title>` | `ใบลดหนี้ลูกค้า (Credit Note) · CUBE 4.0` (บรรทัด 6) |
| Generator | html-generator-v9.1 · Pattern Q Transaction Document Archetype (locked to SO) · B2 v2 line editor · Z-Index Registry |
| PREFLIGHT | บรรทัด 988 · `audit.sh FAIL=0 WARN=2` (archetype px-scale + locked SO stepper = canonical residual) · `node --check PASS` |
| FRD Pack | `FRD_Pack/` (00_OVERVIEW · 01_UI · 02_API · 03_LOGIC · 04_DB · 05_RULES · 06_TESTS · 07_LOCKED · INDEX) — paired ✅ |
| Kernel | Q-DOC KERNEL (บรรทัด 683–987) generic · feature file ให้ config object `DOC` (บรรทัด 601–670) + data + hooks |
| Personas | 4 คน (บรรทัด 483–488) — DEMO harness สลับบทบาท (flag §5.9) |
| สถานะ drift | ดู §11 Drift Log — 0 blocking; 3 informational (`.suggest-list` legacy unused, `couponAmt` engine-carry, VAT ม.86/10 recompute) |

---

## §1 · Design Tokens AS-BUILT

**`:root`** (บรรทัด 35–73) — CUBE 4.0 Warm Light

| กลุ่ม | token → ค่า |
|---|---|
| Brand | `--c-primary` #FF3B30 · `--c-primary-h` #E62E24 · `--c-navy` #111111 · `--c-teal` #1F9D55 · `--c-purple` #FF9A1F (ใช้เป็นสีตัวเลขภาษี/สถานะ sent) |
| พื้น/เส้น | `--c-off-white` #FAF8F5 · `--c-white` #FFFFFF · `--c-border` #DEDAD4 · `--c-border-soft` #EFEBE6 |
| ตัวอักษร | `--c-text` #111111 · `--c-text-mute` #73757B · `--c-text-soft` #9A9CA2 · `--c-placeholder` #B4B6BC (v9.1 #104 — จางกว่า text-soft) |
| สถานะ | `--c-warning` #E8870F · `--c-danger` #E62E24 + alpha ramps `--c-primary-04/08/12/18`, `--c-teal-08`, `--c-warning-08`, `--c-danger-08` |
| รัศมี | `--r-sm` 6px · `--r` 10px · `--r-lg` 14px |
| เงา | `--sh-sm` · `--sh-md` · `--sh-lg` · `--sh-xl` (drawer/modal ใช้ xl) |
| shell | `--sw` 224px (sidebar) · `--hh` 52px (topbar) |

**Fonts** (บรรทัด 9–12): Satoshi (api.fontshare.com) + Noto Sans Thai (fonts.googleapis.com) · body stack `'Satoshi','Noto Sans Thai',…` (บรรทัด 79) · หัวข้อ h1–h4 = Noto Sans Thai ก่อน (บรรทัด 89) · **CDN 0 แหล่ง** (icon inline `ICONS` object บรรทัด 473–474, ไม่มี Tailwind/lucide CDN — shim `.w-*/.h-*` บรรทัด 16–24)

**Scrollbar** (v9.1 #35/#49): `scrollbar-gutter: stable` (บรรทัด 77) กันหน้าขยับ · webkit thumb 5px (บรรทัด 97–101)

### z-index map (สูง → ต่ำ) — v9.1 Z-Index Registry (บรรทัด 69–72)

| token | ค่า | ใช้กับ |
|---|--:|---|
| `--z-toast` | 80 | `#toast-root` (บรรทัด 471) · row-menu (`.menu-fixed` hard-code 80 บรรทัด 966) |
| `--z-portal` | 70 | `.combo-pop` combobox portal · `.suggest-list` legacy · `.hint`/`.info-tip` tooltip |
| `--z-modal` | 60 | `.modal-overlay` + modal card (`> *:not(.backdrop)` บรรทัด 282) |
| `--z-drawer` | 51 | `.overlay-wrap` + `.drawer-panel` |
| `--z-backdrop` | 50 | `.backdrop` |
| `--z-dropdown` | 40 | (reserved — inline dropdown) |
| `--z-shell` | 20 | `.sb` sidebar |
| `--z-sticky` | 10 | `.top` topbar · `.table-wrap thead th` sticky header |
| `--z-content` | 1 | base |

**กฎ overlay ordering (DSP-01, บรรทัด 70/274/328):** portal(70) > modal(60) > drawer(51) > backdrop(50) — combobox / DOA slot-picker ต้องลอยเหนือ **ทั้ง** modal และ drawer เสมอ (slot-picker เปิดในกล่อง submit modal)

---

## §2 · Route Map (hash SPA)

Router: `getRoute()` (บรรทัด 975) · `navigate(path)` = `location.hash = '#/'+path` (บรรทัด 976) · `hashchange → render()` (บรรทัด 977) · boot guarded `__booted` (บรรทัด 978–980)

| Route | name | หน้าจอ | handler |
|---|---|---|---|
| `#/list` (หรือว่าง) | `list` | หน้ารายการ (default) | `renderListPage()` (บรรทัด 941) |
| `#/create` · `#/create/dup-<id>` | `create` | drawer wizard 5 ขั้น (ใหม่/ทำสำเนา) | `openCreateDrawer(null, from)` (บรรทัด 792) |
| `#/edit/:id` | `edit` | drawer wizard (แก้ร่าง เริ่ม step 2) | `openCreateDrawer(id)` (บรรทัด 792–793) |
| `#/view/:id` | `view` | drawer 5 แท็บ | `openViewDrawer(id)` (บรรทัด 851) |

**Refresh-safety:** `render()` (บรรทัด 981) เรนเดอร์ list page เป็น base เสมอ แล้วเปิด overlay ตาม route — refresh ที่ `#/view/:id` = เห็น list + drawer ซ้อน (ไม่ค้างจอเปล่า) · route ที่ไม่รู้จัก → `{name:'list'}` (fallback บรรทัด 975)

---

## §3 · Layout Shell

`.shell` = grid `224px 1fr` (บรรทัด 111) · sfull-height, overflow ในแต่ละ pane

- **Sidebar `.sb`** (บรรทัด 112–135, 414–457): navy #111111, `--z-shell`, sticky · logo `CUBE 4.0 / Accounting` · เมนู `.sb-item` จัดกลุ่ม `.sb-grp` (บัญชี·ตั้งค่า / ลูกหนี้ AR / เจ้าหนี้ AP / บัญชีทั่วไป / การเงิน / Policy Center) · item ที่ active = `data-feature="cn"` "ใบลดหนี้ลูกค้า" (บรรทัด 433) · badge "My Approval 3" (บรรทัด 422) · footer `© 2026 CUBE 4.0 · F-ACC-CN` (บรรทัด 456)
- **Topbar `.top`** (บรรทัด 138, 459–466): 52px, breadcrumb `Accounting › ใบลดหนี้ลูกค้า` (`.top-bc`) · ปุ่มแจ้งเตือน (`.top-icon-btn` + red dot) · **DEMO persona switch** (`.demo-wrap.demo-only` บรรทัด 463 — flag §5.9) · user chip `#uc-n/#uc-r/#uc-av` (บรรทัด 464, อัปเดตโดย `switchPersona`)
- **Page host** `#page-content` (บรรทัด 467) · overlay host `#overlay-root` (บรรทัด 470) · toast host `#toast-root` (บรรทัด 471)
- **Adaptive** (บรรทัด 85, 403–409): `min-width: 768px` (v9.1 #97 desktop-base) · ≤1180px → stat 2 คอลัมน์ + drawer width clamp `min(…,100vw)`

---

## §4 · Page Anatomy

### §4.1 · List (`#/list`) — `renderListPage()` (บรรทัด 941–953)
`.page-fill` → ph (title `DOC.titleFull` + sub `DOC.sub` + chip "N รายการ · รออนุมัติ N") → actions → stat-row → list-card

- **ph-actions** (บรรทัด 944): `ส่งออก CSV` (`exportCSV()`) · `สร้างใบลดหนี้` (`DOC.createLabel`, `navigate('create')`)
- **stat-row** 4 การ์ด (`.stat-card`, `DOC.listStats()` บรรทัด 610–611) คลิก = filter (`setStat`, toggle): `รออนุมัติ` (pen-tool · จำนวน+฿) · `ลดหนี้เดือนนี้ (อนุมัติแล้ว)` (file-minus · ฿ + N ใบ) · `ฉบับร่าง` (file-text) · `ภาษีขายที่ลดเดือนนี้` (scale · ฿ + ภ.พ.30 เดือน MM/YYYY)
- **toolbar `.toolbar`** (บรรทัด 947–951): search `#searchInput` placeholder `ค้นหาเลขที่ / ลูกค้า / ใบแจ้งหนี้ / ใบรับคืน…` (`DOC.searchPh`) + 3 select filter (สถานะ / เหตุผล / ลูกค้า — `DOC.filterSelects()` บรรทัด 612) + `ล้างตัวกรอง` (`clearFilters`)
- **table `.table-wrap`** sticky thead (บรรทัด 380): head 10 คอลัมน์ (`DOC.listHead()` บรรทัด 616) เลขที่·วันที่·ลูกค้า·ใบแจ้งหนี้อ้างอิง·เหตุผล·สถานะเอกสาร·ลายเซ็น·ยอดลดหนี้·ภาษีขายที่ลด·(เมนู) · sort ได้ที่ เลขที่/วันที่/ยอดลดหนี้ (`sortBy`) · row cells `DOC.rowCells()` (บรรทัด 617) · row click → `navigate('view/id')` · kebab `openRowMenu` (บรรทัด 966)
- **table-foot**: page-size select 10/25/50 + page info `N – M จาก K รายการ` (`getPageInfo` บรรทัด 959)
- **empty**: `.empty-state` inbox icon + `ไม่พบรายการที่ตรงกับเงื่อนไข` + ปุ่ม `ล้างตัวกรอง` (บรรทัด 954)

### §4.2 · Create/Edit wizard (`#/create`, `#/edit/:id`) — 5 ขั้น (locked)
`openCreateDrawer` (บรรทัด 792) → `.overlay-wrap > .backdrop + .drawer-panel.wide` (max 1290px) · stepper `renderStepperItem` (บรรทัด 798, 803) · body `.cw-body` · footer ย้อนกลับ/ยกเลิก/ถัดไป หรือ (step 5) บันทึกแบบร่าง/submit (บรรทัด 806–808)

| # | ขั้น (stepper label บรรทัด 803) | render | สาระ |
|---|---|---|---|
| 1 | เลือกแหล่งที่มา | `renderStep1()` (บรรทัด 578) | 2 การ์ด: "จากใบแจ้งหนี้" (active) · "ลดหนี้ไม่อ้างใบ **ปิดไว้**" (disabled, คลิก → toast OQ-CN-01) + ตารางเลือกใบแจ้งหนี้ที่คงค้าง (`srcPickerCard` + `INV_COLS` บรรทัด 572) |
| 2 | ข้อมูลหลักใบลดหนี้ | `renderStep2()` (บรรทัด 582) | ใบแจ้งหนี้อ้างอิง(ro) · ยอดคงค้างที่ลดได้(ro) · ลูกค้า(ro) · วันที่ · **เหตุผล** (select `CN_REASONS` → แสดง legal_basis) · ใบรับคืน (เฉพาะ RET, `needSR`) หรือ "วิธีลด" · พนักงานขาย (`combo('rep')`) · เลขที่(ro "(ออกเลขเมื่ออนุมัติครบ)") · คำอธิบายเหตุผล(≥10) · ที่อยู่ · หมายเหตุภายใน |
| 3 | รายการสินค้า | `renderStep3()` (บรรทัด 737) | B2 v2 line editor (§5.3) — บรรทัด lock (มาจากใบเดิม), line-cap meta, **ส่วนลดท้ายบิล** (§4.4), summary |
| 4 | เอกสารแนบ | `renderStep4()` (บรรทัด 816) | `.upload-zone` + `<input type="file" id="att-file-input" multiple>` (real, บรรทัด 817) · list ไฟล์ + `แนบไฟล์เพิ่ม` / ลบ |
| 5 | ตรวจสอบและยืนยัน | `renderStep5()` (บรรทัด 823) | review pairs (`DOC.reviewPairs`) + **DOA tier preview** (`DOC.step5Extra` บรรทัด 639) + ตารางรายการ + แนบ |

Validation ต่อขั้น: `wizardNext` (บรรทัด 831) → step1 `DOC.step1Validate` · step2 `DOC.step2Validate` (mark `.is-error` ราย field id `f-cnDate/f-reason/f-sr/f-rep/f-reasonText`) · step3 `validateLines` (บรรทัด 836). Submit ปุ่มถูก disable เมื่อ `createWizard._block` (บรรทัด 808) = `DOC.blockReason()` (บรรทัด 637).

### §4.3 · View drawer (`#/view/:id`) — 5 แท็บ (locked order) — `renderViewDrawer()` (บรรทัด 855)
`.drawer-panel` (max 920px) · header: `DOC.titleFull` + `s.code || (ร่าง · ยังไม่ออกเลข)` + `docPill(status)` + head-chip "ถูกตีกลับ N ครั้ง" (`DOC.headChips`) + summary (`DOC.viewSummary`) · header icon-btn: ทำสำเนา(`dupRec`)/พิมพ์/ดาวน์โหลด PDF/ปิด · **status-guarded action buttons** `DOC.viewActions` (§8) · footer "แก้ไขล่าสุด … · [lock] อนุมัติแล้ว ล็อกแก้ไข" เมื่อ status ∈ approved/sent (บรรทัด 879)

แท็บ (บรรทัด 874, `tabBtn` บรรทัด 853):
1. **รายละเอียด** (`detail`, file-text) — `DOC.renderDetailTab` (บรรทัด 657): warn เกินคงค้าง / cancel note / ข้อมูลเอกสาร / สถานะ / เอกสารอ้างอิง / ลูกค้า+ขาย / หมายเหตุ / สรุปยอด / รายการที่ลดหนี้ / แนบ / ข้อมูลระบบ
2. **ใบแจ้งหนี้อ้างอิง · ภาษีขาย** (`ref`, receipt-text) — `renderRefTab` (บรรทัด 671): ยอดใบเดิม/รับชำระ(RV)/ลดหนี้แล้ว/คงค้างก่อน-หลัง/ใบที่รอ(กันยอด) · ตารางบรรทัดใบเดิม ลดแล้ว/ลดได้อีก · ผลกระทบ ภ.พ.30 · **DEMO** จำลองรับชำระ (§5.9) · รายการบัญชี (JE mock, demo-only note)
3. **PDF Preview** (`pdf`, file) — `renderPdfTab` (บรรทัด 890): A4 `.a4` — หัวบริษัท 2BSimple · ลูกค้า/อ้างอิง · ตาราง line + totals (มี end-bill rows) · เหตุผลกฎหมาย · 3 ช่องเซ็น (`ผู้จัดทำ/ผู้อนุมัติ/ลูกค้า (ผู้รับ)`) · ปุ่ม `ดาวน์โหลด`(mock toast) / `พิมพ์`(`window.print()`)
4. **ลายเซ็น / อนุมัติ** (`sign`, pen-tool) — `renderSignTab` (บรรทัด 897): DOA entry + tier · timeline `.tl` ส่งอนุมัติ → ขั้น 1..N (roles + assignee chip + pill สถานะ + ปุ่ม อนุมัติ/ไม่อนุมัติ ที่ขั้นปัจจุบันถ้ามีสิทธิ) → ผลลัพธ์ · รอบก่อนหน้า (ตีกลับ, append-only)
5. **ประวัติ** (`history`, history) — `renderHistoryTab` (บรรทัด 909): timeline `s.audit` (append-only, สีตามชนิด act)

### §4.4 · End-bill (ส่วนลดท้ายบิล) — FN-19 · `DOC.step3Block` (บรรทัด 629–633) + `totals()` (บรรทัด 724–734)
- **การ์ด toggle** ใน step 3: `.toggle` เปิด/ปิด `createWizard.data.endbill.enabled` · ปิด → `value=0` (บรรทัด 632)
- **โหมด ฿/%**: segmented 2 ปุ่ม `จำนวนเงิน (฿)` (`amount`) · `เปอร์เซ็นต์ (%)` (`percent`) เขียน `endbill.mode` · input `type=number` (+ป้าย ฿ หรือ %) → `updateLineSummaryOnly()`
- **เพดาน (cap) + hard-warn**: `ebCap = max(0, after − coupon)` (บรรทัด 727) · แสดง "ลดได้สูงสุด ฿{ebCap}" · เกิน → `ebOver` (บรรทัด 728) → ข้อความแดง "— ที่กรอกเกินเพดาน (ยอดสุทธิห้ามติดลบ)" + `.hard-warn` "**ส่วนลดท้ายบิลเกินยอดที่ลดได้**" (`DOC.lineSummaryWarn` บรรทัด 635) + **block submit** (`blockReason`/`submitGuard`)
- **VAT คิดใหม่ (ม.86/10)**: end-bill ลดฐานภาษีตามสัดส่วน — `ebVat = ebAmt*(vat/after)`, `ebBase = ebAmt−ebVat`, `netBefore = before−ebBase`, `netVat = vat−ebVat` (บรรทัด 730–733) → summary/PDF โชว์แถว "ส่วนลดท้ายบิล · ลดฐานภาษี", "ฐานภาษีหลังหักส่วนลด", "ภาษีมูลค่าเพิ่ม (VAT) · คิดจากฐานใหม่ (ม.86/10)" (บรรทัด 768, 787, 894)

---

## §5 · Component Inventory (anchor + states)

### §5.1 · Buttons `.btn` (บรรทัด 166–183)
variants: `.btn-primary/-secondary/-ghost/-success/-danger/-link` · sizes `.sm`/`.lg` · states: hover (เฉพาะ `:not(:disabled)`), `:focus-visible` outline primary, `:disabled` opacity .6 + not-allowed. ปุ่มทั้งหมด (`<span>…</span></button>` ที่สกัดได้): จำลองรับชำระใบเดิม (แทน RV W6) · ดาวน์โหลด · บันทึกแบบร่าง · พิมพ์ · ย้อนกลับ · ล้างตัวกรอง · ส่งสำเนาซ้ำ · ส่งอนุมัติ · ส่งออก CSV · ส่งให้ลูกค้า · อนุมัติ · ออกเอกสารแก้ไข · เปลี่ยน · เพิ่มรายการ · แก้ไข · แนบไฟล์เพิ่ม · ใช้ราคาระบบ

### §5.2 · Pills `.pill` (บรรทัด 186–193)
`draft` (slate) · `pending` (warning #8A5200) · `approved` (teal) · `sent` (purple) · `rejected` (danger) · `cancelled` (slate). map สถานะเอกสาร ↔ pill = `DOC.statusMap` (§8), แสดงผ่าน `docPill()` (บรรทัด 911).

### §5.3 · B2 v2 Line editor — `renderLineRow` (บรรทัด 743–763)
ตาราง `.line-tbl`: # · สินค้า (combobox item, §5.4) · จำนวน (`number`, `.qty-over` แดงเมื่อเกิน cap) · หน่วย (select ถ้ามีหลาย unit และไม่ lock) · ราคา/หน่วย (`CFG.allowPriceOverride`, override → เส้นขอบ warning) · ส่วนลด % · ภาษี badge (`taxBadgeV` บรรทัด 735 — ไม่คิด/NET/VAT) · จำนวนเงิน · expand(ขั้นสูง)/ลบ.
- **แถวจากใบเดิม lock**: `l.lock=true` → input สินค้า `readonly` (บรรทัด 748), ไม่มีปุ่ม "เพิ่มรายการ" (`DOC.lineAddAllowed → false` บรรทัด 624)
- **line-cap display** (`DOC.lineMeta` บรรทัด 626): "ใบเดิม {qty} × ฿{price} · ลดแล้ว ฿{netDone} · ลดจำนวนได้อีก {capLeft} (ตามใบรับคืน) · ลดมูลค่าได้อีก ฿{netLeft}" + ข้อความ over "— เกินจำนวนที่ลดได้ / — ราคาลดเกินราคาเดิม / — เกินมูลค่าที่ลดได้" (`.line-meta.bad`)
- **expand panel** (บรรทัด 757–763): VAT segmented `ไม่คิด/บวกเพิ่ม/รวมแล้ว (NET)` + `%` + หมายเหตุ + "ระบบเสนอ ฿… (price_src)" + ปุ่ม `ใช้ราคาระบบ` (undo, เมื่อ override)
- states: default / focus (border primary + shadow) / over (`.qty-over`) / lock (readonly bg off-white) / expanded (bg primary-08)

### §5.4 · Combobox (2 ชนิด — portal)
- **สินค้า** (`.item-combo` + `#item-pop`): `onItemInput/Focus/Key` (บรรทัด 777–779) → `showItemSuggestions` สร้าง `.combo-pop` แนบ `document.body` position fixed คำนวณ up/down (บรรทัด 780) · `paintItemPop` แสดง code·หมวด·ชื่อ·ราคา/หน่วย·สินค้า/บริการ (บรรทัด 781) · เลือก `pickItem` · keyboard ↑↓/Enter/Esc (บรรทัด 779) · click-outside close (listener หน่วง setTimeout 0)
- **คน (rep / slot อนุมัติ)** (`#combo-pop`): `combo()` (บรรทัด 842) → `comboOpen` (บรรทัด 845) portal fixed · `comboItems` (บรรทัด 843): `rep`=พนักงานขาย (`DOC.repRoles` = role-officer-sales/role-mgr-sales) · `slot-N`=พนักงานตาม role ของขั้น (ตัด `ME.name` ออก) · `comboKey` ↑↓/Enter/Esc (บรรทัด 847) · empty = "ไม่พบรายการ" (บรรทัด 846)
- **`.suggest-list`** (บรรทัด 334–335): legacy inline suggest (portal `--z-portal`, `.hidden` toggle) — **นิยามไว้แต่ JS ปัจจุบันไม่เรียก** (ใช้ `.combo-pop` แทน) → §11 drift

### §5.5 · Empty-state chip พนักงาน `.emp-chip.is-empty` (บรรทัด 312) → `empChip()` "ยังไม่ระบุคน" (บรรทัด 910)

### §5.6 · Stat cards / Toggle / Stepper / Upload-zone / Notes — ตาม token §1 (บรรทัด 260–307, 386–395)
`.hard-warn` (บรรทัด 323) = กล่องแดงเตือนแบบ block · `.note / .note.warn/.danger/.ok` (บรรทัด 324–327) · `.stepper-item.active/.done` (บรรทัด 264–265) · `.upload-zone.has-files` (บรรทัด 295)

### §5.7 · Timeline `.tl` (บรรทัด 343–353) — ใช้ทั้ง sign tab และ history tab (dot ok/warn/bad)

### §5.8 · Row kebab menu `.menu-fixed` (`openRowMenu` บรรทัด 966) — ดูรายละเอียด/แก้ไข(ร่าง)/ทำสำเนา/พิมพ์/ยกเลิก(ร่าง·pending) · z-index 80 (hard-code ตรงกับ `--z-toast`) · click-outside close

### §5.9 · DEMO-only elements (flag — prod inject `.demo-only{display:none}`, บรรทัด 393)
- **Persona switch** (`.demo-wrap.demo-only[data-demo="persona-switch"]` บรรทัด 463) → `switchPersona()` (บรรทัด 702) — สลับ 4 บทบาทรีวิวสิทธิ์
- **จำลองรับชำระ** (`.demo-wrap.demo-only[data-demo="rv-simulate"]` บรรทัด 675) → `demoPay()` (บรรทัด 677) — พิสูจน์ S-11 (re-check คงค้างตอนอนุมัติขั้นสุดท้าย)
- ป้ายกำกับ demo-only ใน PDF tab ("template ตาม thai-doc-pdf-generator") + ref tab ("จำลอง · รอเชื่อม Journal Entry F093")
> **dev: ห้าม render `.demo-only` ใน production build** — ไม่ใช่ฟีเจอร์จริง

---

## §6 · Overlay Registry + Dismiss Rules

| Overlay (selector) | ชนิด | z-index | เปิดโดย | ปิดโดย | scroll-lock |
|---|---|--:|---|---|---|
| `.overlay-wrap` | ตัวห่อ drawer | `--z-drawer` 51 | `openCreateDrawer`/`openViewDrawer` (บรรทัด 795/851) | — (ห่อ backdrop+panel) | ✅ `body:has(.overlay-wrap){overflow:hidden}` (บรรทัด 88, CSS-only DSP-01) |
| `.backdrop` | ฉากหลัง | `--z-backdrop` 50 | ภายใน overlay-wrap / modal | **คลิก backdrop** → `closeCreateDrawer`/`closeViewDrawer` (drawer) หรือ `this.parentElement.remove()` (modal, บรรทัด 916) | — |
| `.drawer-panel` | drawer ขวา | `--z-drawer` 51 | create(`.wide` 1290px) · view(920px) | ปุ่มปิด / backdrop / **Esc** | (ผ่าน overlay-wrap) |
| `.modal-overlay` | modal กลางจอ | `--z-modal` 60 | `modalShell()` (บรรทัด 916) | backdrop / ปุ่มยกเลิก·ปิด / **Esc** · `closeModal()` (บรรทัด 917) | — (ไม่มี overlay-wrap → **ไม่** ล็อก scroll · §11) |
| `.combo-pop` | combobox portal | `--z-portal` 70 | `showItemSuggestions`/`comboOpen` แนบ body | เลือก / click-outside / **Esc (ชั้นแรก)** | — |
| `.suggest-list` | legacy suggest | `--z-portal` 70 | (ไม่ถูกเรียกใน JS ปัจจุบัน) | `.hidden` | — |

**modal card เหนือ backdrop:** `.modal-overlay > *:not(.backdrop){position:relative; z-index:var(--z-modal)}` (บรรทัด 282) — fix v9.1 regression ที่การ์ด z:auto ทำให้คลิกทะลุไปโดน backdrop แล้ว modal ปิดเอง.

**Modals (สร้างผ่าน `modalShell`/`confirmModal`/`reasonModal`):** submit (`#submit-modal` DOA slot-picker) · approve · reject · cancel · send/resend · revise-doc · demoPay · (row-menu = `.menu-fixed` ไม่ใช่ modal). ทุกตัวเป็น `.modal-overlay` เดี่ยว, ปิดด้วย `closeModal()` เคลียร์ทั้งหมด.

**Toast** `#toast-root` (บรรทัด 471, `showToast` บรรทัด 700): มุมขวาบน `--z-toast` 80 · auto-dismiss 3500ms fade 200ms · ชนิด success/error/warning/info (สี+ไอคอน) · ไม่มีปุ่มปิด.

---

## §7 · Interaction Spec

### §7.1 · Esc chain (global handler บรรทัด 983) — ลำดับปิดทีละชั้น
`document.addEventListener('keydown', …)` ที่ **บรรทัด 983**: ถ้า key ≠ Escape → return; มิฉะนั้นปิดตามลำดับ (ปิดชั้นบนสุดชั้นเดียวต่อการกด 1 ครั้ง):
1. มี `.combo-pop` → ลบ combo-pop ทั้งหมด แล้ว return (combobox ปิดก่อน)
2. มี `.modal-overlay` → `m.remove()` return (modal ปิดก่อน drawer)
3. มี `#create-drawer` → `closeCreateDrawer()`
4. มิฉะนั้น `#view-drawer` → `closeViewDrawer()`

Esc ระดับ combobox (กันไม่ให้ทะลุไปปิด drawer): `onItemKey` **บรรทัด 779** และ `comboKey` **บรรทัด 847** ดัก `e.key==='Escape'` → ลบ `.combo-pop` + `e.stopPropagation()` (ปิดเฉพาะ popup, ไม่ลามถึง global handler). สาม anchor ของ `'Escape'` = บรรทัด **779 · 847 · 983**.

### §7.2 · Click-outside
combobox (item + คน): เพิ่ม `document.addEventListener('click', close)` แบบหน่วง `setTimeout(…,0)` กันจับ event เปิดตัวเอง (บรรทัด 780, 845) · row-menu (บรรทัด 970) เช่นเดียวกัน · modal/drawer ปิดผ่าน backdrop คลิก.

### §7.3 · Focus / render preservation
- `updateLine` (บรรทัด 771–774) เก็บ `oninput` + `selectionStart` ของ input ที่ focus ก่อน re-render ทั้ง drawer แล้วคืน focus/caret (กัน caret เด้งตอนพิมพ์)
- `renderCreateDrawer`/`renderViewDrawer` เก็บ `scrollTop` ของ body แล้วคืนหลัง re-render (บรรทัด 799/810, 857/880)
- `addLine` (บรรทัด 769) focus ช่องสินค้าแถวใหม่หลัง 30ms
- **ไม่มี** focus-trap / focus-restore หลังปิด overlay (extractor: focus_trap ❌, focus_restore ❌) — R4: ไม่มี (—)

### §7.4 · Combobox positioning (บรรทัด 780, 845)
`getBoundingClientRect()` → position fixed; ถ้าพื้นที่ล่างเหลือ < 260px (item) / 280px (คน) → เปิดขึ้นบน (`bottom:…`) มิฉะนั้นเปิดลง (`top:…`). ป้องกัน popup ล้นจอ.

### §7.5 · Re-entrancy guard `busyGate()` (บรรทัด 705, FIX-08) — กัน double-submit ของ commit action (confirmSubmit/confirmApprove/reject/cancel/revise-doc); dev = idempotency key + version (FRD §2.3).

---

## §8 · State-Driven UI Matrix

`DOC.statusMap` (บรรทัด 606) · action buttons `DOC.viewActions(s, st)` (บรรทัด 656) · guards.

| status | pill (docPill) | ปุ่มใน view header (`viewActions`) | แก้ไข? | ยกเลิก? |
|---|---|---|---|---|
| `draft` | ฉบับร่าง (draft) | `ยกเลิก` · `แก้ไข`(→edit) · `ส่งอนุมัติ`(openSubmitModal) | ✅ | ✅ (openCancelCN) |
| `pending_approval` | รออนุมัติ (pending) | ผู้มีสิทธิ์ขั้นปัจจุบัน: `ไม่อนุมัติ`·`อนุมัติ` · ผู้ส่ง: `ยกเลิก` | ❌ | ✅ (owner/pending) |
| `approved` | อนุมัติแล้ว · รอส่ง (approved) | `ออกเอกสารแก้ไข`(openReviseDocCN) · `ส่งให้ลูกค้า`(openSendCN) | ❌ lock | ❌ → revise-doc |
| `sent` | ส่งลูกค้าแล้ว (sent) | `ออกเอกสารแก้ไข` · `ส่งสำเนาซ้ำ`(resend) | ❌ lock | ❌ |
| `cancelled` | ยกเลิก (cancelled) | — (ไม่มีปุ่ม) | ❌ | ❌ |

**Guards (ยึด HTML):**
- `openCreateDrawer` แก้ non-draft → toast `แก้ไขได้เฉพาะฉบับร่าง` + เด้งไป view (บรรทัด 793)
- `submitGuard` (บรรทัด 645) / `openSubmitModal` (บรรทัด 920) / `confirmSubmit` (บรรทัด 927): non-draft → `ส่งอนุมัติได้เฉพาะฉบับร่าง` · ebOver → block · grand > available → block · reasonText<10 → block · slot ว่าง → `เลือกผู้อนุมัติให้ครบทุกขั้น`
- `confirmApprove`/`confirmSubmit` re-check: ไม่ใช่ผู้มีสิทธิ์ → `ไม่ใช่ผู้มีสิทธิ์ในขั้นปัจจุบัน` (บรรทัด 931) · `approveGuard` ขั้นสุดท้าย re-check คงค้าง (S-11, บรรทัด 648)
- `openCancelCN` (บรรทัด 678): status ที่ออกเลขแล้ว → `ใบลดหนี้ที่ออกเลขแล้วยกเลิกไม่ได้ — ใช้ "ออกเอกสารแก้ไข"`
- `openSendCN` (บรรทัด 679): ไม่ approved/sent → `ต้องอนุมัติครบก่อนส่ง`
- **ออกเอกสารแก้ไข** `openReviseDocCN` (บรรทัด 681, FIX-06/OQ-CN-02): display-only — ไม่เปลี่ยนสถานะ/ไม่ถอนยอด/ไม่ลบใบ; เสนอ 2 ทาง (ใบเพิ่มหนี้ Debit Note / ใบลดหนี้ใหม่อ้างใบนี้) → toast `ทำเครื่องหมายรอเอกสารทดแทนแล้ว — สถานะและยอดคงเดิม`

**DOA tier (มีวงเงิน) — `MOCK_DOA_ENTRY`/`resolveDoa` (บรรทัด 541–542):** ≤฿50,000 = 1 ขั้น (ผจก.ขาย) · ฿50,000.01–300,000 = 2 ขั้น (+ผจก.บัญชี) · >฿300,000 = 3 ขั้น (+CFO). tier คิดจาก `totals().grand` (หลัง end-bill, LD-05). Sequential chain, เลือก "คน" ต่อขั้นใน submit modal (`.slot-row` บรรทัด 924).

**Reason master `CN_REASONS` (บรรทัด 538):** RET (รับคืนสินค้า, mode qty, `needSR`) · DISC (ส่วนลดภายหลัง, mode price, `trade_discount_warn`) · PRICE (ผิดราคา, price) · QTY (คิดจำนวนเกิน, qty).

---

## §9 · Microcopy (verbatim)

### §9.1 · Toasts — `showToast(msg, type)` (สกัดครบทุก call)
| ข้อความ (คัดตรงตัว) | ชนิด |
|---|---|
| กรุณากรอกข้อมูลให้ครบถ้วน | warning |
| กรุณาระบุเหตุผล | warning |
| ดาวน์โหลด PDF (mock) | info / success |
| ตีกลับเพื่อแก้ไข | info |
| ต้องอนุมัติครบก่อนส่ง | warning |
| ทำเครื่องหมายรอเอกสารทดแทนแล้ว — สถานะและยอดคงเดิม | info |
| ยกเลิกเรียบร้อย | success |
| ส่งออก CSV {n} รายการ | success |
| ลดหนี้ไม่อ้างใบแจ้งหนี้ถูกปิดไว้ (OQ-CN-01) | warning |
| สลับบทบาทเป็น {roleLabel} (DEMO) | info |
| ส่งอนุมัติได้เฉพาะฉบับร่าง | warning |
| เลือกผู้อนุมัติให้ครบทุกขั้น | warning |
| แก้ไขได้เฉพาะฉบับร่าง | warning |
| ใบลดหนี้ที่ออกเลขแล้วยกเลิกไม่ได้ — ใช้ "ออกเอกสารแก้ไข" | warning |
| ไม่ใช่ผู้มีสิทธิ์ในขั้นปัจจุบัน | warning |

Toast ประกอบตัวแปร (verbatim template): `บันทึกแบบร่างใบลดหนี้เรียบร้อย` · `ส่งเพื่ออนุมัติแล้ว — My Approval ของ {ชื่อ}` · `อนุมัติขั้น {n} แล้ว — ส่งต่อ {ชื่อ}` · `อนุมัติครบสาย — ออกใบลดหนี้ {code} · ลดยอดคงค้าง {inv}` · `ส่ง {code} ให้ลูกค้าแล้ว` · `ส่งสำเนา {code} ซ้ำแล้ว` · `{inv} คงค้างเหลือ ฿{x}`.

### §9.2 · ปุ่มหลัก / label (verbatim)
สร้างใบลดหนี้ · บันทึกแบบร่าง · บันทึกและส่งอนุมัติ (`DOC.submitLabel`) · ส่งอนุมัติ · อนุมัติ · ไม่อนุมัติ · ยกเลิก · ส่งให้ลูกค้า · ส่งสำเนาซ้ำ · ออกเอกสารแก้ไข · ทำเครื่องหมายรอเอกสารทดแทน · เพิ่มรายการ · แนบไฟล์เพิ่ม · เลือกไฟล์ · ใช้ราคาระบบ · เปลี่ยน · ล้างตัวกรอง · ส่งออก CSV · ถัดไป · ย้อนกลับ · ยืนยันยกเลิก.

### §9.3 · Placeholder / hint / empty
- ค้นหาใบแจ้งหนี้: `พิมพ์เลขที่ใบแจ้งหนี้ / ลูกค้า…` (บรรทัด 581)
- ค้นหาสินค้า: `ค้นหารหัสหรือชื่อสินค้า...` (บรรทัด 748) · คน: `พิมพ์ชื่อพนักงานขาย...` / `ค้นหาชื่อคนในตำแหน่ง … …`
- คำอธิบายเหตุผล placeholder: `เช่น รับคืนสินค้าชำรุด 2 กล่อง ตามใบรับคืน SR-…` (บรรทัด 593)
- field-error: `ต้องไม่ก่อนวันที่ใบแจ้งหนี้` · `เลือกเหตุผล` · `เลือกใบรับคืนของใบแจ้งหนี้นี้` · `ระบุพนักงานขาย` · `ระบุคำอธิบายอย่างน้อย 10 ตัวอักษร` · `เลือกผู้อนุมัติขั้นนี้`
- empty list: `ไม่พบรายการที่ตรงกับเงื่อนไข` · empty src: `ไม่พบเอกสารที่ตรงเงื่อนไข` · combobox empty: `ไม่พบรายการ`
- lock footer: `อนุมัติแล้ว ล็อกแก้ไข` (`DOC.lockedLabel`)
- hard-warn: `ส่วนลดท้ายบิลเกินยอดที่ลดได้` · `ยอดลดหนี้เกินยอดคงเหลือของใบแจ้งหนี้อ้างอิง`
- blockReason (title ปุ่ม disabled): `ส่วนลดท้ายบิลเกินยอดที่ลดได้ (สูงสุด ฿…)` · `ยอดลดหนี้เกินยอดคงเหลือ (บันทึกร่างได้)` · `ระบุคำอธิบายเหตุผลอย่างน้อย 10 ตัวอักษร` · `เหตุผลรับคืนต้องอ้างใบรับคืน`

---

## §10 · Data Binding & BACKEND anchors

**ไม่มี `// BACKEND:` literal** — ไฟล์นี้ใช้ mock in-file + คอมเมนต์ผูก engine กลาง (สกัดตรง ๆ):
- **เลขเอกสาร**: `nextCode()` (บรรทัด 718) mock; คอมเมนต์ "เลขจริงจาก **ENG-DOC-NUM.next()** ตาม doc_type CN ใน DOCCFG_BRIEF_F096 — ห้าม feature รันเลขเอง (F003)" → FRD API-06 (issue) / DOCCFG declaration
- **สำเนา PDF**: ENG-DOC-STORE (บรรทัด 717, 679, 890) → FRD API-13
- **DOA resolve**: `resolveDoa` mock (บรรทัด 542); จริง = **ENG-DOA** freeze ตอน submit → FRD API-05
- **CSQ**: `pushAudit(s,'บันทึกเข้า 7C ตาม CSQ_BRIEF_F096')` (บรรทัด 652); event `cn.issued → AC/FC` (บรรทัด 650) → FRD API-06 emit `ar_cn.approved`
- **NTF**: คอมเมนต์ `cn.issued → ผู้สร้าง+AR` (บรรทัด 651), `cn.sent → ลูกค้า` (บรรทัด 679); doa_pending/result มาจาก DOA engine ห้ามซ้ำ → NTF_BRIEF_F096
- **ar_open_item (F094)**: `INVOICES` mock (บรรทัด 519) contract `ar_open_item`; `invGrand/cnApplied/cnHeld/invOutstanding/invAvailable` (บรรทัด 560–564) → FRD API-11 / cross-module write `cn_applied += grand`
- **Sales Return (F090)**: `SRS` mock [ASSUMED] (บรรทัด 530) → FRD API-12
- **Journal Entry (F093)**: JE mock ใน ref tab (บรรทัด 671) demo-only → cross-module event
- **Idempotency/version**: HTML `busyGate` (บรรทัด 705); dev = Idempotency-Key + If-Match (FRD §2.3)

Master mock: `PERSONAS`(483) `EMPLOYEES`(490) `PRODUCTS`(501) `PARTNERS`(511) `PAYMENT_TERMS`(509) `TAX_CODES`(510) `CN_REASONS`(538) `CFG`(482, vatPct 7) · `TODAY_ISO='2026-09-20'`.

---

## §11 · Traceability + Drift Log

### §11.1 · Brief ↔ FRD ↔ HTML
| Brief § | FRD (01_UI P-xx / 02_API) | HTML anchor |
|---|---|---|
| §2 route list | P-01 · API-01/10 | `renderListPage` (941) · `getRoute` (975) |
| §4.2 create s1 (invoice picker) | P-02 · API-11 | `renderStep1` (578) · `invList` (571) |
| §4.2 create s2 (reason/SR/rep) | P-02 · API-12/15 | `renderStep2` (582) · `CN_REASONS` (538) |
| §4.2 create s3 lines | P-02 · API-03 (validate FN-05) | `renderStep3`/`renderLineRow` (737/743) |
| §4.4 end-bill (FN-19) | 05_RULES ม.86/10 · LD-05 · API-05 (tier=grand) | `totals` (724) · `step3Block` (629) |
| §4.3 view/edit | P-03/P-04 · API-02/04 | `renderViewDrawer` (855) · `openCreateDrawer` (792) |
| §8 submit + DOA | API-05 · ENG-DOA | `openSubmitModal`/`confirmSubmit` (920/927) |
| §8 approve/reject | API-06/07 · FN-07/08/11 | `confirmApprove`/`openRejectModal` (931/934) |
| §8 cancel | API-08 · FN-09 | `openCancelCN` (678) |
| §8 send/resend | API-09 · FN-10 | `openSendCN` (679) |
| §8 ออกเอกสารแก้ไข | API-14 · FN-13 · OQ-CN-02 | `openReviseDocCN` (681) |
| §4.3 PDF tab | API-13 · CN_print-spec | `renderPdfTab` (890) |
| §10 issue/ar_open_item | API-06 side-effect · cross-module F094/F105/F093 | `onFinalApprove` (649) · `renderRefTab` (671) |

ครบ 4 route + 15 API mutation/read มี anchor. FN-19 (end-bill) จับคู่ครบ (toggle+cap+recompute-VAT+summary/PDF rows).

### §11.2 · ⚠️ Drift Log
| # | ประเภท | รายละเอียด | ข้อเสนอ |
|---|---|---|---|
| D-1 | HTML-only (dead CSS) | `.suggest-list` (334–335) + `.combo-option*` (336–341) นิยามไว้แต่ JS ปัจจุบันใช้ `.combo-pop` (329) แทน — ไม่มีจุดเรียก | ไม่กระทบ dev; อาจตัดออกรอบ cleanup (ไม่ใช่ business drift) |
| D-2 | HTML behavior | `.modal-overlay` เปิดโดยไม่ผ่าน `.overlay-wrap` → **body scroll ไม่ถูกล็อก** ระหว่าง modal (scroll-lock ผูกกับ `body:has(.overlay-wrap)` บรรทัด 88) | dev: ตัดสินใจว่าต้องล็อก scroll ตอน modal ด้วยหรือไม่ (drawer ล็อกอยู่แล้ว) |
| D-3 | engine-carry | `totals()` อ้าง `couponAmt` (บรรทัด 724/727) แต่ feature CN ไม่มี UI คูปอง (=0 เสมอ) — ตกทอดจาก B2 v2 SO engine | ไม่กระทบ; ห้ามแก้ engine (kernel locked) |
| D-4 | FRD-only (declare) | FRD ระบุ Declarations `doa+ntf+csq+doccfg+pdfdoc` (INDEX บรรทัด 110) — HTML เห็นเป็นคอมเมนต์ผูก engine เท่านั้น | ปกติ (declaration = ประกาศ, dev wire ภายนอก) |

> ไม่มี drift ระดับ business ที่บล็อก · D-2 ให้ dev เคาะ (พฤติกรรม), ที่เหลือ informational.

---

## §12 · Diff จากเวอร์ชันก่อน
— ไม่มี HTML เก่าให้ diff ในรอบนี้ (—)

---

## §13 · 💡 ข้อเสนอ (ไม่ใช่ AS-BUILT)
1. **D-2**: พิจารณาห่อ modal ใน `.overlay-wrap` (หรือเพิ่มคลาส scroll-lock) เพื่อล็อก body scroll ตอน modal เปิด — ให้พฤติกรรมเท่ากับ drawer.
2. **D-1**: ตัด `.suggest-list`/`.combo-option*` ที่ไม่ถูกเรียก เพื่อลดขนาดไฟล์ (ยืนยัน grep ก่อนตัด — เป็น dead CSS จริง).
3. เพิ่ม focus-trap + focus-restore ให้ drawer/modal (ปัจจุบันไม่มี) เพื่อ a11y (นอกขอบเขต AS-BUILT).
> ทั้งหมดนี้เป็นข้อเสนอ — ห้ามถือเป็นสเปคที่ต้องสร้าง จนกว่าจะเคาะ.
