# HTML UI Brief — ใบปรับยอดสต๊อก (Stock Adjustment · F082 / F-WH-STKADJ)

> **AS-BUILT spec สกัดจาก HTML prototype 1:1** — ทุกบรรทัด trace กลับหา selector / function / ข้อความจริงในไฟล์ได้ (Iron Rule R1)
> ใช้คู่กับ **HTML (source of truth) + FRD Pack (สัญญาระบบ)** · ของที่ "เสนอเพิ่ม" อยู่ §13 เท่านั้น

---

## §0 · Document Control + Pairing

| หัวข้อ | ค่า |
|---|---|
| Feature | F-WH-STKADJ · F082 · ใบปรับยอดสต๊อก (Stock Adjustment) |
| HTML (source of truth) | `outputs/F-WH-STKADJ/F-WH-STKADJ.html` · 1,160 บรรทัด · `<title>` = "ใบปรับยอดสต๊อก (Stock Adjustment) · CUBE 4.0" · badge sidebar `F-WH-STKADJ · v1` |
| Archetype | CUBE Warm Light · Document Archetype · Pattern Q (full) + B2 v2 line editor (VAT→"โหมดกรอก", FN-49 ไม่มีคอลัมน์ VAT) · ปี ค.ศ. ล้วน |
| FRD Pack (pair) | `outputs/F-WH-STKADJ/FRD_Pack/` — 00_OVERVIEW · 01_UI (P-01..P-07) · 02_API (F082-API-01..20) · 03_LOGIC · 04_DB · 05_RULES (BR/FN) · 06_TESTS · 07_LOCKED_DECISIONS · INDEX |
| สถานะ drift | pair แล้ว — ดู §11 Traceability + Drift Log |
| Declaration ที่ประกาศแล้ว (อ้างในโค้ด) | DOA_BRIEF_F082 · NTF_BRIEF_F082 · CSQ_BRIEF_F082 · DOCCFG_BRIEF_F082 (คอมเมนต์ในโค้ดอ้างครบ) |
| Scoping | ทุก id ผ่าน `ssId(name)` → prefix `ss-` (บรรทัด 297–299) · เข้าถึงผ่าน `$ss(name)` |

---

## §1 · Design Tokens AS-BUILT

### 1.1 สี / รัศมี / เงา (`:root` บรรทัด 20–35)
| token | ค่า | token | ค่า |
|---|---|---|---|
| `--c-navy` | `#111111` | `--c-primary` | `#FF3B30` (แดง CUBE) |
| `--c-primary-h` | `#E62E24` | `--c-teal` | `#1F9D55` (เพิ่ม +) |
| `--c-danger` | `#E62E24` (ลด −) | `--c-warning` | `#E8870F` |
| `--c-purple` | `#FF9A1F` (reversed) | `--c-slate` | `#73757B` |
| `--c-off-white` | `#FAF8F5` (พื้น) | `--c-white` | `#FFFFFF` |
| `--c-border` | `#DEDAD4` | `--c-border-soft` | `#EFEBE6` |
| `--c-text` | `#111111` | `--c-text-mute` | `#73757B` |
| `--c-text-soft` | `#9A9CA2` | รัศมี | `--r-sm:6px` · `--r:10px` · `--r-lg:14px` |
| เงา | `--sh-sm` · `--sh-md` · `--sh-lg` · `--sh-xl` | ทึบ/บาง | `--c-primary-08/12/18` · `--c-teal-08` · `--c-warning-08` · `--c-danger-08` |
| shell | `--sw:232px` (sidebar) · `--hh:52px` (topbar) | | |

### 1.2 ฟอนต์
- Body: `'Noto Sans Thai','Satoshi',-apple-system,sans-serif` · 13px · line-height 1.55 (บรรทัด 37)
- Head: `'Noto Sans Thai','Satoshi'` · weight 700 · letter-spacing −.015em
- Tabular: `.num` / `.tbl-mono` (`ui-monospace,'Satoshi'`)
- แหล่ง: Google Fonts (Noto Sans Thai) + Fontshare (Satoshi) — **CDN 2 แหล่ง** → offline จะ fallback ฟอนต์ (ข้อจำกัดจริง)

### 1.3 z-index map (สูง → ต่ำ) — DSP-01/02 scale (บรรทัด 33–34)
| ลำดับ | token | ค่า | ใช้กับ |
|:--:|---|:--:|---|
| 1 | `--z-toast` | **80** | `#ss-toast-root` (toast มุมล่างขวา) |
| 2 | `--z-combopop` | **75** | `.combo-pop` + `.menu-fixed` (ต้องลอย**เหนือ** modal) |
| 3 | `--z-modal` | **70** | `.modal-overlay` |
| 4 | `--z-portal` | **60** | (สงวน) portal float เหนือ drawer |
| 5 | `--z-drawer` | **50** | `.overlay-wrap` (drawer create/view) |
| 6 | `--z-dropdown` | **40** | `.top` (sticky topbar), `.tbl thead` (2) |

> กติกาที่ต้องรักษา: combobox/row-menu (`--z-combopop` 75) **ต้องลอยเหนือ modal (70) และ drawer (50)** เพราะ combobox ถูก portal ไปที่ `#ss-overlay-root` (DSP-02) — ถ้าทำ dropdown เป็น child ของ drawer จะโดน stacking context ตัด

---

## §2 · Route Map (hash router)

| route (hash) | ความหมาย | handler / anchor |
|---|---|---|
| `#/list` | หน้า list (default) — `getRoute()` คืน `{name:'list'}` เมื่อ hash ว่าง | `renderListPage()` (บรรทัด 655) |
| `#/create` | เปิด wizard สร้างใหม่ (drawer) | `openCreateDrawer(null)` |
| `#/edit/:id` | เปิด wizard แก้ไข (เฉพาะ `status==='draft'`) | `openCreateDrawer(id)` — ถ้าไม่ใช่ร่าง toast `แก้ไขได้เฉพาะฉบับร่าง` แล้วเด้งไป view |
| `#/view/:id` | เปิด view drawer 4 tabs | `openViewDrawer(id)` — ถ้า `findDoc(id)` ไม่เจอ → `navigate('list')` |

- Router: `getRoute()` แยก `location.hash.replace(/^#\/?/,'')` เป็น `name/id` (บรรทัด 594) · `navigate(r)` = ตั้ง `location.hash='#/'+r` (595)
- **Refresh-safety:** `hashchange` → `render()` (1144) + `DOMContentLoaded` → `render()` (1145) + เรียก `render()` ตอนโหลด (1146) — เปิด `#/view/d3` ตรง ๆ แล้ว refresh กลับมาหน้าเดิมได้ · เปิด `#/edit/<ไม่ใช่ร่าง>` จะ redirect เอง
- `render()` (617) เป็น single source: sync overlay ↔ route (ถ้า route ไม่ใช่ overlay ล้าง `#ss-overlay-root` + `releaseFocus()`)

---

## §3 · Layout Shell

| region | selector | ขนาด/พฤติกรรม |
|---|---|---|
| Shell grid | `.shell#ss-app` | `grid-template-columns:var(--sw) 1fr` (232px + เนื้อหา) · min-height 100vh |
| Sidebar | `.sb` | navy `#111` · `position:sticky;top:0;height:100vh` · logo "CUBE 4.0 / 2BSimple ERP" · foot "คลังสินค้า · Warehouse / F-WH-STKADJ · v1" |
| Sidebar menu | `#ss-sidebar` (`renderSidebar` 597) | **Iron #104 One-Feature-One-Menu** — เมนูคลังสินค้ามี 4 node แต่มีเพียง `stkadj` ที่ active + `href="#/list"` · อีก 3 (putaway/stktrf/rtv) เป็น mock → toast `เปิด <ชื่อ> (mock)` |
| Topbar | `.top` | `height:var(--hh)` (52px) · sticky · `z-index:var(--z-dropdown)` · ซ้าย breadcrumb `#ss-breadcrumb` ขวา ปุ่มแจ้งเตือน + user chip "ปวีณา สุขทวี / หัวหน้าคลัง · WH-BKK-01" |
| Breadcrumb | `#ss-breadcrumb` (`renderBreadcrumb` 609) | `คลังสินค้า › ใบปรับยอดสต๊อก[· sub]` — root คลิก = `navigate('list')` |
| Page | `.page#ss-page` | เนื้อหา list |
| Overlay host | `#ss-overlay-root` | drawer + portal (combo/row-menu) แปะที่นี่ |
| Toast host | `#ss-toast-root` | fixed มุมล่างขวา |
| Responsive | — | `body{min-width:768px}` (บรรทัด 262) · `@media(max-width:1180px)` kpi 2 คอลัมน์ + form 1 คอลัมน์ · `@media(max-width:900px)` filt 1 คอลัมน์ |

---

## §4 · Page Anatomy

### 4.1 List page (`#/list` · `renderListPage` 655) — Pattern Q surface a
```
.page
├─ .ph  (page header)
│   ├─ h1.ph-title "ใบปรับยอดสต๊อก" + p.ph-sub
│   └─ .ph-right → button.btn-primary "สร้างใบปรับยอด" → navigate('create')
├─ .kpi-row (4 ใบ · toggle filter)  ← Pattern Q KPI
│   ├─ kpi 'pending'  "ใบรออนุมัติ"        → toggleKpi('pending')
│   ├─ kpi 'aged'     "ใบเกินเกณฑ์อายุ"     (pending & agedDays≥2)
│   ├─ kpi 'month'    "มูลค่าปรับสะสมเดือนนี้" (posted & sameMonth)
│   └─ kpi 'reversed' "ใบที่กลับรายการ"
├─ .card  (รายการใบปรับยอด)
│   ├─ .card-head : title + "<n> รายการ"
│   ├─ .filt : .filt-search #ss-list-search + .filt-grid(คลัง/สถานะ/ประเภท/ช่วงวันที่มีผล) + .filt-reset "ล้างตัวกรอง"
│   ├─ table.tbl : เลขที่ | คลัง | ประเภท | มูลค่าปรับ (Σ|฿|) | สถานะเอกสาร | ลายเซ็น(n/N) | วันที่มีผล | ผู้จัดทำ | ⋮
│   │   └─ tr.is-clickable → navigate('view/<id>')  ·  ปุ่ม ⋮ → openRowMenu (event.stopPropagation)
│   ├─ .empty (เมื่อ 0 แถว · emptyHtml)
│   └─ .table-foot : "แสดง n จาก N ใบ" + "ปี ค.ศ. · มูลค่าอ้างอิงจาก Item Master (mock)"
└─ .card  เอกสารแนบ (Document Center · attachmentsSection 716) ← Pattern Q "เอกสารแนบใน landing"
```
- ลายเซ็น = `renderSignProgress(d)` (577) แสดง `done/total` + `.pgline` (bar) — total = ชั้น DOA + 1 (ผู้ส่ง)
- แถวมูลค่า: `Σ|มูลค่า|` (docAbs = ฐาน DOA) เด่น + "สุทธิ ±" (docNet) ตัวเล็ก

### 4.2 Create/Edit wizard (`#/create`, `#/edit/:id` · surface b) — 5 steps
เปิดใน `.drawer-panel.wide` (max-width 1180px). Stepper กลาง `.stepper > .stepper-item > .stepper-circle` (5 จุด · บรรทัด 770). ก้าวที่ทำเสร็จ (`s>n`) คลิกย้อนได้.

| step | label (verbatim) | render fn | เนื้อหาหลัก |
|:--:|---|---|---|
| 1 | ข้อมูลใบปรับยอด | `renderStep1` (783) | คลัง* (combo) · วันที่มีผล ค.ศ.* (≤ วันนี้) · ประเภทการปรับ* (คุมชนิด bin, BR-12) · ศูนย์ต้นทุน (combo) · แหล่งที่มา seg [ปรับตรง/จากใบนับ] · เหตุผลรวมของใบ + "เติมทุกบรรทัดที่ว่าง" · หมายเหตุ · เลขที่เอกสาร(disabled) · ผู้จัดทำ |
| 2 | รายการปรับยอด | `renderStep2` (803) | B2 v2 line editor `.line-tbl` · seg "โหมดกรอก" [ระบุยอดที่ถูกต้อง/ระบุจำนวนที่ปรับ] · ปุ่ม "เพิ่มบรรทัด" · **ไม่มีคอลัมน์ VAT (FN-49)** · footer wizTotals (Σ|มูลค่า| ฐาน DOA) |
| 3 | เหตุผล + หลักฐาน | `renderStep3` (846) | reasonRow ต่อบรรทัด (combo กรองตามทิศผลต่าง) · needNote ต้องกรอกคำอธิบาย · `.upload-zone` + `#ss-attach-input` (real `<input type=file multiple>`) |
| 4 | ผู้อนุมัติ | `renderStep4` (867) | `doaTiers(abs)` → `.slot-row` เลือก "คนจริง" ต่อขั้น · จุดตัด mock 20,000 / 200,000 / 1,000,000 |
| 5 | ตรวจทานและส่ง | `renderStep5` (879) | สรุป header + lines + สายอนุมัติ + แนบ · ปุ่ม footer "บันทึกร่าง" / "ส่งอนุมัติ" |

- Footer wizard (773): step>1 มี "กลับ" · step<5 มี "ถัดไป" · step5 มี `#ss-btn-draft` "บันทึกร่าง" + `#ss-btn-submit` "ส่งอนุมัติ" · ทุก step มี "ยกเลิก"
- Header ปุ่ม X → `requestCloseCreate()`

### 4.3 View drawer (`#/view/:id` · surface c · `renderViewDrawer` 1004) — 4 tabs
เปิดใน `.drawer-panel` (max-width 920px). Header: displayCode + docPill + meta + action ปุ่มตามสถานะ (`headerActions` 997) + copy/print/download/close.

| tab (key) | label | fn | เนื้อหา |
|---|---|---|---|
| `detail` | รายละเอียด | `detailTab` (1025) | banners(returned/cancel/reverse/isReversal) · ข้อมูลเอกสาร · สรุปมูลค่า · รายการปรับยอด (RO table) · **เอกสารแนบอยู่ในแท็บนี้** · ข้อมูลระบบ |
| `pdf` | PDF Preview | `pdfTab` (1040) | A4 (`.a4`) · template thai-doc-pdf-generator · ปุ่มดาวน์โหลด/พิมพ์ · ช่องลายเซ็นตามชั้น DOA |
| `sign` | ลายเซ็น / อนุมัติ | `signTab` (1052) | ทะเบียน DOA-WH-STKADJ · timeline สายอนุมัติ · ปุ่มอนุมัติ/ตีกลับ (ถ้า canActStep) · รอบอนุมัติก่อนหน้า |
| `history` | ประวัติ | `historyTab` (1058) | audit append-only + Movement table (posted/reversed) + ผูกคู่ reversal |

> **หมายเหตุ label:** `tabBtn('sign','ลายเซ็น / อนุมัติ',...)` (1015) — brief จุดหยุดเรียก "ลายเซ็น·อนุมัติ" แต่ค่าจริงในโค้ดคือ **"ลายเซ็น / อนุมัติ"** (มีช่องว่างรอบ `/`) — ยึดตามโค้ด

---

## §5 · Component Inventory (anchor + states)

| component | anchor หลัก | states (R4) |
|---|---|---|
| ปุ่ม | `.btn` + variant `.btn-primary/-secondary/-ghost/-success/-danger/-link` · `.btn.sm` | default · `:hover:not(:disabled)` · `:disabled{opacity:.55;cursor:not-allowed}` · focus-visible `outline:2px var(--c-primary)` · loading = spinner `loader-2 .spin` (submit) |
| pill สถานะ | `.pill.<status>` (`docPill`/`statusMeta` 567) | draft/pending/approved/posted/cancelled/reversed (6 ค่า · สีต่อสถานะ · มี `.dot`) |
| chip ผลต่าง | `.chip-diff.plus/.minus/.zero` (`diffChip` 830) | ไม่เลือกครบ = `—` (zero) · df=0 = `0` (zero) · +/− = plus/minus |
| KPI | `.kpi` + `.kpi.on` | default · hover(border+shadow) · on (เมื่อ filter kpi ตรง) |
| input/select | `.input` / `.select` (34px) | default · `:focus`(border primary+ring) · `:disabled/[readonly]`(off-white) · error via `.field.is-error` |
| field | `.field` · `.field.full` · `.field.is-error` | help `.field-help` · error `.field-error` (display:none → block เมื่อ is-error) |
| combobox | `.combo-cell > input#cbi-<key>` + portal `.combo-pop` (`comboTrigger` 933) | ปิด/เปิด · highlight `.hi` · disabled item (bin ล็อก) · empty `.combo-empty` |
| line editor | `table.tbl.line-tbl` · cell `.cell-in` / `.cell-in.ro` / `.cell-in.num` | RO(หน่วย/ยอดระบบ/ต้นทุน/มูลค่า) · แก้ได้(จำนวน) · negNote ใต้ bin เมื่อยอดหลังปรับติดลบ |
| stepper | `.stepper > .stepper-item(.active/.done) > .stepper-circle` | active(วงแดง+glow) · done(เต็มแดง+เช็ค, คลิกย้อน) · รอ(เทา) |
| upload zone | `.upload-zone(.has-files)` + `#ss-attach-input` | ว่าง(placeholder) · has-files(list + "แนบเพิ่ม") · hover(border primary) |
| emp chip / slot | `.emp-chip(.is-empty/.sm)` · `.slot-row(.is-err)` · `.slot-no` · `.slot-role` | มีคน / ว่าง("ยังไม่ระบุคน") / error(border danger) |
| timeline | `.tl > .tl-i(.ok/.warn/.bad)` · `.tl-t/.tl-s/.tl-q` | ok(เขียว) · warn(ส้ม=ขั้นปัจจุบัน/reverse) · bad(แดง=ตีกลับ/ยกเลิก) · default(รอคิว) |
| segmented | `.seg > button(.on)` | ใช้กับ แหล่งที่มา + โหมดกรอก |
| toggle | `.toggle > input + .toggle-slider` | off/on (ไม่มี seed ใช้จริงในจอนี้ — component พร้อม) |
| note/warn | `.note(.warn/.danger/.ok)` · `.hard-warn` | info/warn/danger/ok |
| badge FWD | `.fwd-badge.demo-only` | **DEMO-ONLY** — production inject `.demo-only{display:none}` (คอมเมนต์ 110, 291–292) → ห้าม render จริง |

---

## §6 · Overlay Registry + Dismiss Rules

| overlay | selector | ขนาด | เปิด | ปิด (dismiss) | z |
|---|---|---|---|---|---|
| Create/Edit drawer | `.overlay-wrap#ss-create-wrap` > `.drawer-panel.wide` | ขวา · max-width 1180px · slide `translateX` | `openCreateDrawer` | backdrop `.backdrop`(onclick `requestCloseCreate`) · ปุ่ม X/ยกเลิก · Esc | `--z-drawer` 50 |
| View drawer | `.overlay-wrap#ss-view-wrap` > `.drawer-panel` | ขวา · max-width 920px | `openViewDrawer` | backdrop `.backdrop`(onclick `closeViewDrawer`) · ปุ่ม X/ปิด · Esc | `--z-drawer` 50 |
| Modal (submit/approve/confirm/reason/post) | `.modal-overlay#ss-modal` > `.modal-card`(`.lg`) | กลางจอ · max-width 520px (lg 780px) · max-height 90vh | `modalShell` (1067) | backdrop `.backdrop`(onclick `closeModal`) · ปุ่มยกเลิก/ปิด · Esc | `--z-modal` 70 |
| Combobox popup | `.combo-pop#ss-combo-pop` (portal → `#ss-overlay-root`) | fixed · min-width max(trigger,300px) · max-height 300px | `comboOpen` (954) | click-outside(`mousedown`) · เลือก item · Esc(`closeAllPops`) · **resize → ปิด** (1143) | `--z-combopop` 75 |
| Row menu (⋮) | `.menu-fixed#ss-row-menu` (portal · `portalMenu` 337) | fixed · min-width ≥190px · จัดขึ้น/ลงตามที่ว่าง | `openRowMenu` (724) | click-outside · เลือก item · Esc(`closeAllPops`) · resize | `--z-combopop` 75 |

- **ห้ามปิดโดยพลาด:** modal ยืนยัน (reason/confirm) — ปิด backdrop ได้แต่ = ยกเลิก action (ไม่ทำอะไรต่อ) · การส่ง/อนุมัติ/post ต้องกดปุ่มยืนยันชัดเจน
- animation: backdrop opacity .22s · drawer transform .28s cubic-bezier · toast `toastin .2s`
- `.overlay-wrap.on` = state เปิด (เพิ่ม class หลัง `requestAnimationFrame` เพื่อ trigger transition)

---

## §7 · Interaction Spec

### 7.1 Esc chain (global handler · **บรรทัด 1142**)
ลำดับ priority (ตัวแรกที่ match ทำงานแล้ว return):
1. ถ้ามี `#ss-combo-pop` → `closeAllPops()` + `stopPropagation()` (ปิด combobox ก่อน)
2. ถ้ามี `#ss-modal` → `closeModal()`
3. ถ้ามี `#ss-view-wrap` → `closeViewDrawer()`
4. ถ้ามี `#ss-create-wrap` → `requestCloseCreate()`

> Esc ตัวที่สอง (**บรรทัด 969** · `comboKey`) จับ Escape ภายใน input ของ combobox → `closeAllPops()` + `stopPropagation()` (กันไม่ให้ลาม global ปิด drawer พร้อมกัน)

### 7.2 Focus / scroll management
- `trapFocus(container)` (315) — วน Tab ใน overlay + set `body.is-overlay-open` (scroll-lock, บรรทัด 38) + `#ss-app aria-hidden=true` + โฟกัส element แรก (setTimeout 60ms)
- `releaseFocus()` (330) — pop trap stack, คืน focus element เดิม, ปลด scroll-lock เมื่อ stack ว่าง
- `_trapStack` เป็น stack → รองรับ modal ซ้อนบน drawer (เปิด modal บน drawer แล้วปิด กลับมา trap drawer เดิม)
- **DSP-01 drawer→drawer:** `openViewDrawer` เรียก `releaseFocus()` ก่อนถ้า `_ovState.type==='view'` (988) กัน trap stack ค้าง (เช่น doReverse เด้งไป view ใบใหม่)
- **คืน focus หลัง render:** ไม่มี `preserveRenderState/withRenderPreservation` (extractor: "คืน focus หลัง render : ไม่มี") — แต่มี workaround เฉพาะ search: `onSearchInput` (651) re-focus `#ss-list-search` + `setSelectionRange` หลัง re-render (เพราะ list วาดใหม่ทั้งก้อน)

### 7.3 Positioning (portal)
- combobox/row-menu ใช้ `position:fixed` + คำนวณจาก `getBoundingClientRect()` แล้ว portal ไป `#ss-overlay-root` — **เหตุผล:** ต้องลอยเหนือ drawer/modal โดยไม่ติด stacking context ของ panel (DSP-02)
- flip ขึ้นเมื่อพื้นที่ล่างไม่พอ: combo `<280` · row-menu `<240`
- resize → `closeAllPops()` (1143) กัน popup ค้างผิดตำแหน่ง

### 7.4 Keyboard combobox (`comboKey` 969)
ArrowDown/Up เลื่อน `COMBO.hi` (ข้าม disabled ตอน Enter) · Enter เลือกตัว highlight · Escape ปิด

### 7.5 กันกดรัว (race)
- `actBusy()` (593) คืน true ถ้ากำลังทำงาน (reset 500ms) · `modalShell` เคลียร์ `state._busy=false` ทุกครั้งเปิด modal ใหม่ (FIX-07)
- ปุ่มส่ง/บันทึกร่าง disable ตัวเองระหว่างทำงาน (`#ss-btn-submit`/`#ss-btn-draft`)

### 7.6 Click-through guards
- แถวตาราง clickable แต่ cell ปุ่ม ⋮ ห่อ `onclick="event.stopPropagation()"` (709) · ปุ่มลบไฟล์/แนบเพิ่ม ใน upload zone ใช้ `event.stopPropagation()` กันเด้ง file picker

---

## §8 · State-Driven UI Matrix

### 8.1 สถานะเอกสาร → pill + ปุ่ม (row menu `openRowMenu` 724 · header `headerActions` 997)
| status | pill label/class | ปุ่มที่โผล่ (เงื่อนไข) |
|---|---|---|
| `draft` | ร่าง · `.pill.draft` | ดูรายละเอียด · **แก้ไข** (`edit/:id`) · **ส่งอนุมัติ** (`submitStart`) · **ยกเลิก** (`openCancel`) |
| `pending` | รออนุมัติ · `.pill.pending` | (ถ้า `canActStep`) **อนุมัติ**(`openApprove`) · **ตีกลับ**(`openReject`) · **ยกเลิก** |
| `approved` | อนุมัติแล้ว · `.pill.approved` | **ผ่านรายการ** (`postStart`) — ยกเลิกไม่ได้แล้ว (FIX-02) |
| `posted` | ผ่านรายการ · `.pill.posted` | **กลับรายการ** (`openReverse`) เฉพาะถ้ายังไม่ถูกกลับ/ไม่ใช่ใบกลับ |
| `cancelled` | ยกเลิก · `.pill.cancelled` | — (ดูอย่างเดียว) |
| `reversed` | กลับรายการแล้ว · `.pill.reversed` | — (ดูอย่างเดียว) |

- `canActStep(d)` (630): มีขั้น pending + ผู้ใช้ไม่ใช่ผู้ส่ง + (assignee ตรง ME หรือ role ตรง)
- ล็อกหลังอนุมัติ: `['approved','posted','reversed']` แสดง 🔒 "ล็อกหลังอนุมัติ" ใน foot (1017)

### 8.2 ประเภทการปรับ → ชนิด bin ที่เลือกได้ (BR-12 · `ADJ_TYPES` 377)
| ประเภท | binTypes | บังคับแนบ |
|---|---|---|
| ปรับยอดทั่วไป (`general`) | storage, staging | ไม่ |
| ตัดจำหน่ายของเสีย (`damage`) | damage | **ใช่ (BR-23)** |
| ปรับยอดกักกัน (`quarantine`) | quarantine | ไม่ |
- เปลี่ยนประเภทเมื่อมี bin ไม่เข้าประเภทใหม่ → `confirmModal` "จะล้าง bin ที่ไม่เข้าประเภทใหม่ n บรรทัด" (onChangeAdjType 797)

### 8.3 เหตุผล → ทิศ (dir) + ต้องอธิบาย (`REASONS` 420 · combo กรองตามผลต่าง)
- `plus` (RS-01,02) แสดงเฉพาะบรรทัดผลต่าง + · `minus` (RS-03,04,05,06) เฉพาะ − · `both` (RS-07,99) ได้ทั้งคู่
- `needNote:true` (RS-03,06,07,99) → คำอธิบายเพิ่มบังคับ (BR-06)

### 8.4 โหมดกรอก (line editor · `setGridMode` 839)
- `correct` "ระบุยอดที่ถูกต้อง" → correctQty · `delta` "ระบุจำนวนที่ปรับ (+/−)" → deltaQty · `lineDiff` (548) คำนวณผลต่างตามโหมด · สลับโหมดแปลงค่าให้อัตโนมัติ

### 8.5 DOA tier ตาม Σ|มูลค่า| (`doaTiers` 558)
| ฐาน (abs) | ชั้น | roles |
|---|---|---|
| < 20,000 | 1 | WH_LEAD |
| ≥ 20,000 | 2 | + WH_MGR |
| ≥ 200,000 | 3 | + FIN_MGR |
| ≥ 1,000,000 | 4 | + DIR |
> เป็น mock display เท่านั้น — feature ส่ง `Σ|มูลค่า|` ให้ DOA กลาง (F-DLG-001 · API-16) ตัดสินชั้นจริง

---

## §9 · Microcopy (verbatim · R2)

### 9.1 ปุ่ม (18 · `<span>…</span></button>`)
`กลับ` · `กลับรายการ` · `คิดจากยอดล่าสุด` · `ดาวน์โหลด` · `ตีกลับ` · `ตีกลับไปแก้` · `บันทึกร่าง` · `ผ่านรายการ` · `พิมพ์` · `ยกเลิก` · `ล้างตัวกรอง` · `สร้างใบปรับยอด` · `ส่งอนุมัติ` · `อนุมัติ` · `เปลี่ยน` · `เพิ่มบรรทัด` · `แก้ไข` · `แนบเพิ่ม`
(+ inline: `ถัดไป` · `เติมทุกบรรทัดที่ว่าง` · `ยืนยันยกเลิก` · `ยืนยันกลับรายการ` · `ล้างและเปลี่ยน`)

### 9.2 Toast — สตริงดิบทุกตัว (47 · `showToast(...)`) — **verbatim ห้าม paraphrase**
| variant | สตริงดิบ (verbatim จากโค้ด) |
|---|---|
| warning | `" ต้องพิมพ์คำอธิบายเพิ่ม (BR-06)` |
| warning | `กรุณากรอกข้อมูลให้ครบถ้วน` |
| warning | `กรุณาระบุเหตุผล` |
| warning | `กรุณาเพิ่มรายการปรับยอดอย่างน้อย 1 บรรทัด` |
| warning | `กลับรายการซ้ำไม่ได้ (BR-18)` |
| info | `การแจ้งเตือน (mock)` |
| info | `คัดลอกแล้ว` |
| warning | `คู่ (bin, สินค้า) ซ้ำ:` |
| success | `ดาวน์โหลด PDF (mock)` |
| info | `ตีกลับ` |
| warning | `ต้องอนุมัติครบทุกขั้นก่อนผ่านรายการ` |
| error | `บรรทัด` |
| warning | `บรรทัด` |
| info | `บันทึกร่างแล้ว` |
| warning | `ประเภทตัดจำหน่ายของเสีย ต้องแนบหลักฐานอย่างน้อย 1 ไฟล์ (BR-23)` |
| warning | `ผลต่าง = 0 — ให้ลบบรรทัดหรือแก้ยอด (BR-02)` |
| success | `ผ่านรายการ` |
| warning | `ผ่านรายการได้เฉพาะสถานะ "อนุมัติแล้ว" (BR-08)` |
| warning | `มีบรรทัดที่เลือก bin หรือสินค้าไม่ครบ` |
| success | `ยกเลิก` |
| warning | `ยกเลิกได้เฉพาะใบร่าง/รออนุมัติเท่านั้น` |
| error | `ยอดหลังปรับติดลบ — คงเหลือ` |
| warning | `ยังไม่เลือกเหตุผล (BR-06)` |
| info | `ร่างยังไม่มีเลขที่` |
| success | `สร้างใบกลับรายการ` |
| success | `ส่ง` |
| success | `อนุมัติขั้น` |
| success | `อนุมัติครบทุกขั้น — สถานะ "อนุมัติแล้ว" · กด "ผ่านรายการ" เพื่อโพสต์` |
| info | `อ้างอิงใบนับ ${esc(d.ref_count_doc)} — แสดงผล ไม่เปิดหน้าใบนับ` |
| info | `เติมเหตุผลให้บรรทัดที่ยังว่างแล้ว` |
| info | `เปิด ${esc(it.label)} (mock)` |
| success | `เพื่ออนุมัติแล้ว` |
| info | `เพื่อแก้ไข` |
| warning | `เลือกผู้อนุมัติให้ครบทุกขั้น (BR-10)` |
| warning | `เลือกใบนับต้นเรื่อง (F084/F086) ก่อน (BR-26)` |
| warning | `เหตุผล` |
| warning | `เหตุผล "` |
| warning | `แก้ไขได้เฉพาะฉบับร่าง` |
| success | `แล้ว` |
| success | `แล้ว — ส่งต่อ` |
| warning | `ใบนี้ผ่านรายการแล้ว — ใช้ "กลับรายการ" แทน` |
| warning | `ไม่ตรงทิศผลต่าง (BR-07)` |
| warning | `ไม่พบเอกสาร` |
| warning | `ไม่ใช่ผู้มีสิทธิ์` |
| warning | `ไม่ใช่ผู้มีสิทธิ์ในขั้นปัจจุบัน` |
| success | `— movement เกิดแล้ว · JE รอลงบัญชี` |
| success | `— รออนุมัติตามมูลค่าก่อนผ่านรายการ` |

> ประโยค toast จริงหลายตัวประกอบจากตัวแปร เช่น `ส่ง '+d.code+' เพื่ออนุมัติแล้ว` · `อนุมัติขั้น '+(idx+1)+' แล้ว — ส่งต่อ '+next.assignee` · `บรรทัด '+l.bin+' ยอดหลังปรับติดลบ — คงเหลือ '+... (BR-03)` · `ผ่านรายการ '+d.code+' — movement เกิดแล้ว · JE รอลงบัญชี` — dev ต้องประกอบข้อความให้ตรงตัวอักษรต้นทาง

### 9.3 Empty state (verbatim)
| ที่ | title | desc |
|---|---|---|
| list (มีตัวกรอง · `emptyHtml` 712) | `ไม่พบรายการที่ค้นหา` | `ลองปรับคำค้นหรือล้างตัวกรอง` |
| list (ว่างเปล่า) | `ยังไม่มีใบปรับยอด` | `เริ่มต้นด้วยการสร้างใบปรับยอดใบแรก` |
| เอกสารแนบ landing | — | `ยังไม่มีเอกสารแนบ` |
| combobox bin | — | `ไม่พบ bin ที่ตรงประเภท/คลัง` |
| combobox อื่น | — | `ไม่พบรายการ` |
| bin combo — พิมพ์ "ย้าย" | head warn | `การย้ายของระหว่าง bin/คลัง ไม่อยู่ในใบปรับยอด — ใช้ "โอนย้ายสต๊อก" (Stock Transfer)` |
| bin combo — พิมพ์ "TR-" | head mute | `bin ระหว่างทาง (in-transit · TR-*) สงวนให้โอนย้ายสต๊อก — ไม่แสดงในใบปรับยอด` |

### 9.4 Validation microcopy สำคัญ (wizardNext 897 · เชิงลบ FN-40 กลุ่ม)
- BR-01 คู่ซ้ำ · BR-02 ผลต่าง=0 · BR-03 ยอดหลังปรับติดลบ · BR-06 เหตุผล/คำอธิบาย · BR-07 ทิศไม่ตรง · BR-10 ผู้อนุมัติไม่ครบ · BR-23 แนบหลักฐาน · BR-26 ต้องเลือกใบนับ · BR-08 post เฉพาะ approved · BR-15 balance re-check · BR-18 กลับรายการซ้ำไม่ได้

---

## §10 · Data Binding & BACKEND anchors

Mock data ในไฟล์ (แปลงเป็น API จริง):
| mock (ในโค้ด) | ↔ FRD API | หน้าที่ |
|---|---|---|
| `DOCS[]` (461) · `filteredDocs` (632) | F082-API-01 GET /stock-adjustments | list + filter + KPI |
| `findDoc(id)` | F082-API-02 GET /:id | view drawer detail |
| `saveDraft`/`buildDoc` (909) | F082-API-03 POST · API-04 PUT | สร้าง/บันทึกร่าง/แก้ร่าง |
| `submitForApproval`/`confirmSubmit` (916/1082) | F082-API-05 POST /submit | ส่ง → `nextCode()` ออกเลข ADJ-YYYY-NNNN |
| `confirmApprove` (1095) | F082-API-06 POST /approve | อนุมัติราย slot |
| `openReject` (1109) | F082-API-07 POST /reject | ตีกลับเป็นร่าง |
| `openCancel` (1110) | F082-API-08 POST /cancel | ยกเลิก (draft/pending) |
| `doPost` (1131) | F082-API-09 POST /post | ผ่านรายการ + movement (BR-15) |
| `doReverse` (1112) | F082-API-10 POST /reverse | กลับรายการ → ใบใหม่ |
| `historyTab` movements | F082-API-11 GET /:id/movements | movement + คู่ reversal |
| `onAttachPick` (863) · `#ss-attach-input` | F082-API-12 POST /:id/attachments | แนบหลักฐาน (real file input) |
| `BINS`/`binCombo` filter | F082-API-13 GET /bins | bin picker (filter type+wh, กรอง in-transit FN-32) |
| `ITEMS`/`itemCombo` | F082-API-14 GET /items | item picker (soft-ref) |
| `sysMock(bin,item)` (742) | F082-API-15 GET /bins/:binId/stock-balance | ยอดระบบ snapshot (FN-04 · `snapAt`) |
| `doaTiers(abs)` (558) | F082-API-16 GET /doa/resolve · **X-module F-DLG-001** | resolve สาย DOA |
| `REASONS`/`REASON_BY` | F082-API-17 GET /adjustment-reasons | reason master |
| `COUNT_DOCS` (459) | F082-API-18 GET /count-documents · **X-module F084/F086 display-only** | count-doc picker |
| `pdfTab` (1040) | F082-API-19 GET /:id/pdf | PDF A4 model/render |
| `attachmentsSection` (716) | F082-API-20 GET /stock-adjustment-attachments | landing aggregate |

**FWD-WIRE (ยังไม่ผูก · demo-only chip):** valuation engine (ต้นทุน W5) · DOA engine (ชั้นจริง) · JE posting · ENG-DOC-NUM (เลขรัน) / ENG-DOC-STORE (สำเนา PDF · DOCCFG_BRIEF_F082) — ห้าม feature รันเลข/ลงบัญชีเอง.
**Append-only:** movement เกิดตอน post เท่านั้น (`mkMovement` 533) · ไม่มีปุ่มลบ/แก้ · แก้ผิดใช้ "กลับรายการ".

---

## §11 · Traceability + Drift Log

### 11.1 Brief ↔ FRD ↔ HTML
| Brief § | FRD | HTML anchor |
|---|---|---|
| §4.1 list | P-01 · API-01,20 | `renderListPage` 655 · `attachmentsSection` 716 |
| §4.2 wizard 5 step | P-02 · API-03,04,05 | `openCreateDrawer` 744 · `renderStep1..5` 783–890 |
| §4.3 view 4 tab | P-03 · API-02,11,19 | `renderViewDrawer` 1004 · `detailTab/pdfTab/signTab/historyTab` |
| §6 submit modal | P-04 · API-05 | `openSubmitModal` 1072 · `confirmSubmit` 1082 |
| §6 approve/reject | P-05 · API-06,07 | `openApprove` 1090 · `openReject` 1109 |
| §6/§8 post+drift | P-06 · API-09 · BR-15 | `postStart`/`doPost` 1125/1131 |
| §6 cancel/reverse | P-07 · API-08,10 | `openCancel` 1110 · `openReverse`/`doReverse` 1111/1112 |
| §8.5 DOA tier | API-16 (F-DLG-001) | `doaTiers` 558 |
| §5 combobox bin (in-transit filter) | API-13 · FN-32 | `comboItemsFor` line-bin 945 |

### 11.2 ⚠️ Drift Log
1. **[label drift · cosmetic]** จุดหยุด/บรีฟงานเรียกแท็บ "ลายเซ็น·อนุมัติ" แต่ค่าจริงในโค้ด (1015) = **"ลายเซ็น / อนุมัติ"** — ยึดตามโค้ด (source of truth). ไม่บล็อก.
2. **[HTML-only · demo]** `.fwd-badge.demo-only` (chip FWD-WIRE + อ้าง BR-xx ที่ผู้ใช้เห็น) เป็น demo — FRD ไม่ได้ระบุให้ render จริง → production ต้อง inject `.demo-only{display:none}`. เป็นไปตามคอมเมนต์ในโค้ด (110, 291) ไม่ใช่ drift ธุรกิจ.
3. **[extractor undercount]** ตัวสกัด route จับได้แค่ `create`/`list` (regex จับ literal `#/xxx`) — จริงมี `edit/:id`, `view/:id` ผ่าน `navigate('view/'+id)` / `navigate('edit/'+id)` (compose string). Brief §2 บันทึกครบทั้ง 4. ไม่ใช่ drift ของระบบ.
4. **[OQ ค้าง — ยกให้ BA]** โค้ดคอมเมนต์อ้าง OQ ยังไม่เคาะ: `OQ-ADJ-01` (ใบกลับรายการ fast-track ต้องมีมติ · doReverse 1115) · `OQ-ADJ-02` (ท่อ CSQ ตอน post · doPost 1133). **ห้าม AI เลือกข้าง** — ยกเป็น OQ.

---

## §12 · Diff จากเวอร์ชันก่อน
— ไม่มี HTML เวอร์ชันก่อนให้ diff ในรอบนี้ (single version).

---

## §13 · 💡 ข้อเสนอ (ไม่ใช่ AS-BUILT)
> ที่เดียวที่อนุญาตให้คิดเอง (R1) — **ยังไม่มีในโค้ด · ห้าม dev ทำจนกว่าจะเคาะ**
1. combobox popup ยังไม่ตามตำแหน่ง trigger เมื่อ scroll ภายใน drawer (ปิดตอน resize เท่านั้น) — เสนอเพิ่ม reposition ตอน scroll ของ panel.
2. focus-restore ทั่วไปหลัง re-render มีเฉพาะช่องค้นหา (`onSearchInput`) — เสนอ pattern กลาง (`preserveRenderState`) ถ้าจะขยายให้ทุก input ใน list.

*(ข้อเสนอเหล่านี้อยู่นอก AS-BUILT — บันทึกไว้ให้ BA/dev พิจารณา ไม่ใช่สเปคที่ต้องสร้าง)*
