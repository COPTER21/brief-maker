# HTML UI Brief — F-WH-GRN · GRN รับของ

> **EXTRACTION-BASED** — ทุกบรรทัดสกัดจาก `01_HTML/F-WH-GRN.html` (หลัง 7R re-gate · 3,400 บรรทัด · 227,823 bytes)
> HTML = source of truth · ไฟล์นี้ไม่แต่งสเปคเพิ่ม · ใช้คู่ `03_FRD/01_UI.md` (Layout Decision Log)

## §1 Design tokens (verbatim จาก 2 บล็อก `:root`)

### §1.1 BASE-KIT v6.4 tokens

| Token | ค่า | Token | ค่า |
|---|---|---|---|
| `--c-navy` · `--c-ink` | `#111111` | `--c-primary` | `#FF3B30` |
| `--c-primary-hover` · `--c-danger` | `#E62E24` | `--c-teal` | `#FF9A1F` |
| `--c-teal-light` | `#FFB763` | `--c-mute` | `#54565C` |
| `--c-mute-2` | `#73757B` | `--c-mute-3` | `#9A9CA2` |
| `--c-line` | `#DEDAD4` | `--c-line-2` | `#E9E5E0` |
| `--c-line-3` | `#F1EEEA` | `--c-bg-off` | `#FAF8F5` |
| `--c-success` | `#1F9D55` | `--c-warning` | `#E8870F` |
| `--sidebar-w` | `232px` | `--shell-h` | `52px` |

**Type scale (ค่าตายตัว ห้ามเพิ่มขนาดใหม่):** `--fs-h1 22` · `--fs-h2 17` · `--fs-h3 15` · `--fs-body 14` · `--fs-sub 13` · `--fs-meta 12` · `--fs-cap 11` · `--fs-kpi 28`
**Spacing:** `--sp-xs 4` · `--sp-sm 8` · `--sp-md 12` · `--sp-lg 20` · `--sp-xl 28`
**Radius:** `--r-xs 4` · `--r-sm 6` · `--r-md 8` · `--r-lg 12` · `--r-full 999`

### §1.2 Page tokens (CUBE Warm Light · ชั้นที่ 2)

`--c-ivory #FAF8F5` · `--c-charcoal #111111` · `--c-red #FF3B30` · `--c-orange #FF9A1F` · `--c-blue #0B5CFF` · `--c-tealx #00A88E`
alias: `--c-text #111111` · `--c-text-soft #54565C` · `--c-text-mute #73757B` · `--c-border #DEDAD4` · `--c-border-soft #E9E5E0`
โปร่งแสง: `--c-primary-08` · `--c-primary-12` · `--c-teal-08` · `--c-warning-08` · `--c-danger-08`
`--r 8px` · เงา `--sh-md` / `--sh-lg` / `--sh-xl`

> ⚠️ `--c-purple` ถูก map เป็น `#FF9A1F` (ส้ม) — ใช้กับตัวเลข VAT · **ไม่ใช่สีม่วงจริง** อย่าไปแก้ชื่อ

### §1.3 Fonts
`'Satoshi', 'Noto Sans Thai', system-ui, sans-serif` (หลัก) · `'Noto Sans Thai', sans-serif` · `ui-monospace, SFMono-Regular, Menlo, monospace` (`.tbl-mono` — เลขเอกสาร/รหัส)
โหลดจาก `fonts.googleapis.com` (Noto Sans Thai 400–800) + `api.fontshare.com` (Satoshi 300–900)

## §2 z-index map (สกัดจาก computed style จริง)

| ชั้น | selector | z-index | position |
|---|---|---|---|
| sticky header ตาราง | `thead th` | `var(--z-sticky)` = **20** | sticky |
| shell / sidebar | `.sidebar` | `var(--z-shell)` = **30** | fixed |
| dropdown | `.menu-fixed` · combobox | `var(--z-dropdown)` = **40** | fixed |
| backdrop (BASE-KIT) | `.drawer-backdrop` · `.modal-backdrop` | `var(--z-backdrop)` = **50** | fixed |
| drawer (BASE-KIT · ไม่ได้ใช้) | `.drawer` | `var(--z-drawer)` = **51** | fixed |
| **overlay portal (ที่ใช้จริง)** | `#overlay-root` · `.overlay-wrap` | **70** | relative / fixed |
| **เมนูแถว** | `#row-menu` | **80** | fixed |
| **toast** | `#toast` | `var(--z-toast)` = **90** | fixed |

> **สำคัญ:** ไฟล์มี drawer 2 ระบบ — BASE-KIT (`#drawer`/`#drawerBackdrop`, **ไม่ถูกใช้**) และ overlay portal ของ Pattern Q (**ที่ใช้จริง**)
> ลิ้นชักทุกตัวถูก inject ผ่าน `document.getElementById('overlay-root').innerHTML = ...`
> เมื่อมี overlay เปิด: `body:has(#overlay-root .overlay-wrap) .toast { bottom: 96px; }` เพื่อไม่ทับปุ่มใน footer

## §3 Route map

| Route | เปิดอะไร | ฟังก์ชัน |
|---|---|---|
| `#/list` (default) | หน้ารายการ | `renderListPage()` |
| `#/create` | ลิ้นชักตัวช่วยสร้าง (เริ่มขั้น 1) | `openCreateDrawer()` |
| `#/edit/:id` | ลิ้นชักแก้ฉบับร่าง (**เริ่มขั้น 2**) | `openCreateDrawer(editId)` |
| `#/view/:id` | ลิ้นชักดูเอกสาร (เริ่มแท็บรายละเอียด) | `openViewDrawer(id)` |

`hashchange` listener = ✅ · route แบบ refresh-safe (ลิ้นชักตั้ง `location.hash` เอง) · ปิดลิ้นชักแล้ว `navigate('list')`

## §4 Overlay registry + dismiss rules

| Overlay | id / selector | เปิดด้วย | ปิดด้วย | ความกว้าง |
|---|---|---|---|---|
| ลิ้นชักตัวช่วยสร้าง | `#create-drawer` `.drawer-panel.wide` | `openCreateDrawer()` | `closeCreateDrawer()` · คลิก `.backdrop` · Esc | **1290** (`max-width`) |
| ลิ้นชักดูเอกสาร | `#view-drawer` `.drawer-panel` | `openViewDrawer(id)` | `closeViewDrawer()` · คลิก `.backdrop` · Esc | **920** |
| หน้าต่างยืนยันรับเข้า | `#post-modal` | `openPostModal()` | ปุ่มยกเลิก · Esc | modal |
| หน้าต่างเหตุผล | `#reason-modal` | `openReasonModal(id, 'reverse'\|'discard')` | ปุ่มยกเลิก · Esc | modal |
| เมนูแถว | `#row-menu` | `openRowMenu(id, e)` | คลิกที่ใดก็ได้ (global listener) · เลือกเมนู | `min-width:200px` |
| combobox | `[data-overlay]` | `openOverlay(menu, trigger)` | คลิกนอก · เลือกค่า | ตาม trigger |
| toast | `#toast` | `showToast(msg, variant, ms)` | หมดเวลาเอง | มุมขวาล่าง |

**Esc chain (ลำดับจริงในโค้ด):** modal → ลิ้นชักตัวช่วยสร้าง → ลิ้นชักดูเอกสาร — ปิดทีละชั้นจากบนลงล่าง
**Animation:** `.drawer-panel` `transform: translateX()` 280ms `cubic-bezier(.4,0,.2,1)` · `.drawer-enter` → `.drawer-active`

## §5 Anatomy รายหน้า

### §5.1 หน้ารายการ (`#/list`)

- **Shell:** sidebar 232px (มี watermark `Prototype · W3P` — **ต้องถอดก่อน production**) + shell-bar 52px
- **KPI 5 ใบ** · **ตัวกรอง 5 ตัว** (`setFilt()`) + สวิตช์ "มีของในโซนกักของ"
- **ตาราง 8 คอลัมน์:** เลขที่ใบรับ (`.tbl-mono`) · วันที่รับจริง · ผู้ขาย · อ้างอิง PO · สถานะเอกสาร · ผลตรวจคุณภาพ · ลายเซ็น (กว้าง 70px กลาง) · มูลค่ารับ (ชิดขวา) + คอลัมน์เมนู 44px
- คอลัมน์ที่เรียงได้ใช้ `th(label, key)` · แถวคลิกได้ → `#/view/:id`
- **สถานะว่างเปล่า** 8 จุดในไฟล์

### §5.2 ตัวช่วยสร้าง — โครงร่วม

`.stepper` 5 ขั้น (`renderStepperItem(n, label)`) — ขั้นที่ผ่านแล้ว (`.done`) **คลิกย้อนกลับได้**
ทุกขั้นเปิดด้วย `STEPH(icon, title, hint)`
footer: ซ้าย [ย้อนกลับ] (ขั้น > 1) · ขวา [ยกเลิก] → [ถัดไป] / ขั้นสุดท้าย [บันทึกแบบร่าง] → [รับเข้าคลัง]

| ขั้น | ฟังก์ชัน | องค์ประกอบ |
|---|---|---|
| ① เลือกแหล่งที่มา | `renderStep1()` | `.tile-btn` 2 ช่อง (ช่องที่ 2 `disabled`) + การ์ด `.po-pick` (`.off` = เลือกไม่ได้) |
| ② ข้อมูลหลักใบรับของ | `renderStep2()` | `.form-grid` 11 field + `.hard-warn` เมื่อใบสั่งซื้อไม่พร้อม |
| ③ รายการสินค้า | `renderStep3()` · `renderLineRow()` | `.tbl.line-tbl` + แถวขยาย + `renderLineSummary()` |
| ④ เอกสารแนบ | `renderStep4()` | `.upload-zone` + รายการไฟล์ |
| ⑤ ตรวจสอบและยืนยัน | `renderStep5()` | สรุป `<dl>` + การ์ด "ผลปลายทางเมื่อรับเข้า" + `linesTableView()` อ่านอย่างเดียว |

### §5.3 ตารางกรอกรายการ (B2 v2) — `.tbl.line-tbl` · `font-size:12.5px`

| # | หัวคอลัมน์ (verbatim) | `width` | จัดชิด |
|---|---|---|---|
| 1 | `#` | 26px | กลาง |
| 2 | `สินค้า` | — (ยืด) | ซ้าย |
| 3 | `รับครั้งนี้` | 64px | ขวา |
| 4 | `หน่วย` | 92px | ซ้าย |
| 5 | `ราคา/หน่วย` | 92px | ขวา |
| 6 | `ส่วนลด %` | 78px | ขวา |
| 7 | `ภาษี` | 72px | กลาง |
| 8 | `จำนวนเงิน` | 104px | ขวา |
| 9 | (chevron) | 54px | กลาง |

`padding-left/right: 6px` ทุกเซลล์ · แถวที่ขยายอยู่ `background: var(--c-primary-08)`
ป้ายในคอลัมน์สินค้า: `บริการ` (`.pill.draft`) · ป้ายของไม่ผ่าน · ป้ายช้ากว่ากำหนด

### §5.4 ลิ้นชักดูเอกสาร — 5 แท็บ

`tabBtn(key, label, icon)`:
`detail` **รายละเอียด** `file-text` · `qc` **ตรวจคุณภาพ** `shield-check` · `pdf` **PDF Preview** `file` · `sign` **ลายเซ็น** `pen-tool` · `history` **ประวัติ** `history`

- **รายละเอียด** (`renderDetailTab`) — `SECWRAP(SEC(icon,title) + ...)` ทุก section · แบนเนอร์ 4 แบบ: กลับรายการ (`.note.danger`) · ของไม่ผ่านตรวจ (`.note.warn`) · ใบสั่งซื้อปิดก่อนครบ (`.note.warn`) · มาช้ากว่ากำหนด (`.note`)
- **ตรวจคุณภาพ** (`renderQcTab`) — `.note.ok` เมื่อผ่านทั้งใบ / `.note.warn` เมื่อมีของไม่ผ่าน + ตาราง 5 คอลัมน์
- **PDF Preview** (`renderPdfTab`) — toolbar (`ตัวอย่าง PDF · A4 · 1/1 · แบบฟอร์มตาม print-spec-grn` + ดาวน์โหลด/พิมพ์) + `.a4` (พื้น `#fff` · `padding:36px 40px`) + 3 ช่องลงชื่อ
- **ลายเซ็น** (`renderSignTab`) — `signCount(g) = receiver + inspector` · `.tl` timeline · `empChip` · **ไม่มีปุ่มอนุมัติ**
- **ประวัติ** (`renderHistoryTab`) — timeline ต่อท้ายอย่างเดียว

## §6 Component states

| Component | states |
|---|---|
| `.po-pick` | ปกติ · `.on` (เลือกอยู่ · มี check-circle-2) · `.off` (เลือกไม่ได้ · ไอคอน lock · จาง) |
| `.tile-btn` | `.on` · ปกติ · `disabled` (+ `title` บอกเหตุผล) |
| `.stepper-item` | `.active` · `.done` (คลิกย้อนได้ · ไอคอน check) · ปกติ |
| segmented ผลตรวจ | `.seg > button` + `.on` — 3 ค่า |
| `.field` | ปกติ · `.is-error` (+ `.field-error`) |
| `.slot-row` | ปกติ · `.is-err` (เมื่อมีของไม่ผ่านแต่ยังไม่ระบุผู้ตรวจ) |
| `.pill` | ตามสถานะเอกสาร (`draft` · posted · reversed) |
| `.note` | ปกติ · `.warn` · `.danger` · `.ok` |
| toast | `.is-visible` + `.is-success` / `.is-info` / `.is-warning` / `.is-error` |
| ปุ่มบันทึกรับเข้า | ปกติ · `disabled` เมื่อ hard control · `disabled` + "กำลังบันทึก…" (`_submitting`) |

## §7 Microcopy (verbatim — ห้ามเปลี่ยนคำตอนทำของจริงโดยไม่แจ้ง BA)

| บริบท | ข้อความ |
|---|---|
| ขั้น 1 hint | `ใบรับของทุกใบต้องอ้างใบสั่งซื้อเสมอ — เลือกได้เฉพาะ PO ที่ส่งให้ผู้ขายแล้วและยังมีบรรทัดค้างรับ` |
| tile ที่ปิด | `ไม่รองรับใน W3 — ของเข้าที่ไม่มี PO ให้ใช้ปรับยอดสต๊อก` |
| เลือก PO ไม่ได้ | `เลือกไม่ได้ — {เหตุผล}` (เช่น `ถูกปิดใบก่อนรับครบ (short-close) — เปิดรับของต่อไม่ได้`) |
| ใบสั่งซื้อไม่พร้อม | `ใบสั่งซื้อต้นทางไม่พร้อมรับของแล้ว` |
| เลขใบส่งของซ้ำ | `เลขนี้เคยใช้กับผู้ขายรายนี้แล้ว — ตรวจสอบก่อนรับเข้า (เตือนอย่างเดียว)` |
| คลังปลายทาง help | `ระดับ location เท่านั้น — การเก็บลง bin เป็นงานของ Putaway` |
| โซนกัก help | `ใช้เมื่อมีของไม่ผ่านตรวจ — ค่าตั้งต้นมาจากค่าคอนฟิกของคลัง` |
| ผู้รับของ help | `ต้องเป็นบุคคลจริง — ใช้ในช่องลงชื่อของเอกสาร` |
| ผู้ตรวจคุณภาพ help | `บังคับเมื่อมีบรรทัดที่ไม่ผ่านตรวจ` |
| วันที่รับจริง help | `ย้อนหลังได้ตามเกณฑ์กลาง (NC rules)` ⚠️ ชื่อกติกาภายใน — ควรทบทวนถ้อยคำ |
| แก้ใบที่ post แล้ว | `แก้ไขได้เฉพาะฉบับร่าง — ใบที่รับเข้าแล้วต้องกลับรายการแล้วออกใบใหม่` |
| ขั้น 4 hint | `ใบส่งของผู้ขาย · ใบชั่งน้ำหนัก · ภาพสภาพสินค้าตอนรับ — แสดงที่หน้ารายละเอียดของใบรับ` |
| ของไม่ผ่านตรวจ | `มีของไม่ผ่านตรวจ {N} หน่วย — เข้าโซนกักของ {ชื่อโซน} · ออกจากโซนกักได้ทางเดียวคือคืนผู้ขาย (RTV)` |
| QC ผ่านทั้งใบ | `ผ่านการตรวจทั้งใบ — ของทั้งหมดเข้าคลังปกติ` |
| นโยบายโซนกัก | `ของที่ไม่ผ่านถูกรับเข้าโซนกักของเสมอ (ไม่ปฏิเสธที่หน้าประตู) แล้วจึงคืนผู้ขายด้วยเอกสาร RTV` |
| GR/IR | `รอตั้ง GR/IR ฿{ยอด} — เดบิต สินค้าคงคลัง / เครดิต พักหนี้ GR-IR · ยังไม่ลงบัญชีจริงในรอบนี้` |
| ลายเซ็น | `ใบรับของไม่มีสายอนุมัติ — การรับของคือการบันทึกข้อเท็จจริง ไม่ใช่การอนุมัติ · สิ่งที่ต้องระบุคือผู้รับผิดชอบจริงต่อการรับและการตรวจ` |
| กลับรายการ | `ความเคลื่อนไหวเดิมจะไม่ถูกลบ — ระบบสร้างรายการตรงข้ามและหักยอดรับคืนที่ใบสั่งซื้อ` |
| ทิ้งร่าง | `ร่างจะถูกเก็บเป็นประวัติ (ไม่มีการลบถาวร)` |
| เลขเอกสาร (ร่าง) | `เลขออกตอนรับเข้าคลังเท่านั้น` / `(ยังไม่ออกเลข)` |
| footer ใบที่ post แล้ว | `รับเข้าแล้ว — ล็อกแก้ไข (ต้องกลับรายการ)` |

## §8 BACKEND anchors ↔ FRD API

| จุดบนจอ (ฟังก์ชันใน HTML) | FRD API |
|---|---|
| `renderListPage()` + `setFilt()` | `API-01 GET /grn` |
| `openViewDrawer(id)` → `renderViewDrawer()` | `API-02 GET /grn/{id}` |
| `poSelectable()` · `poBlockReason()` | `API-03 GET /grn/selectable-pos` |
| `pickPo(code)` → `lineFromPoLine()` | `API-04 POST /grn` |
| `setLineQc()` · `fillAllOpen()` · แก้ field | `API-05 PUT /grn/{id}` |
| `refreshFromPo()` | `API-06 POST /grn/{id}/refresh-from-po` |
| `openPostModal()` → ยืนยัน → `nextDocNo()` | **`API-07 POST /grn/{id}/post`** |
| `openReasonModal(id,'reverse')` | **`API-08 POST /grn/{id}/reverse`** |
| `openReasonModal(id,'discard')` | `API-09 POST /grn/{id}/discard` |
| `.upload-zone` | `API-10 attachments` |
| `renderPdfTab()` | `API-11 GET /grn/{id}/print` |
| `dupDn` check ในขั้น 2 | `API-12 GET /grn/check-dn` |

## §9 Traceability 3 ทาง

| Brief (FN ธุรกิจ) | FRD | HTML (ฟังก์ชันจริง) |
|---|---|---|
| FN-02 เลือก PO ได้เฉพาะที่ค้างรับ | `05_RULES BR-02` · `03_LOGIC FN-02` | `poSelectable()` · `.po-pick.off` |
| FN-08/09 เพดานรับเกิน | `05_RULES BR-06` · `ENG-GRN-02` | `lineCap()` · `_overCap` |
| FN-14..17 ผลตรวจ | `05_RULES BR-09/10` · `ENG-GRN-01` | `setLineQc()` · `lineGood()` · `qcAxis()` |
| FN-21 เลขเอกสาร | `05_RULES BR-20` · `ENG-DOC-NUM` | `nextDocNo()` |
| FN-24/25 กลับรายการ | `05_RULES BR-15` · `03_LOGIC FN-13` | `openReasonModal(id,'reverse')` · `reversal_of` |
| FN-27..30 sync ใบสั่งซื้อ | `ENG-GRN-04` | จุดเขียน `.received` **1 จุด** |
| FN-33 เอกสารพิมพ์ | `03_LOGIC FN-15` | `renderPdfTab()` · `.a4` |
| FN-94 ปี ค.ศ. | `05_RULES BR-19` | `formatCEDate()` |

## §10 Drift Log — ที่ต่างจาก `input/09142026-grn/1_HTML/`

ไฟล์นี้ **ไม่ byte-identical** กับต้นน้ำ — เลน 7R แก้ 4 จุด (ผู้ใช้อนุมัติ) · รายละเอียดเต็มที่ `07_LOCKED_DECISIONS.md §LD-03`

| # | จุด | ผลต่อ UI |
|---|---|---|
| 1 | ปิด `@keyframes` 2 บล็อกที่ขาดปีกกา | **คืนชีพ CSS 64 selector** — `.a4` · `.tl` · `.note*` · `.field-error` · `.combo-pop` · `.upload-zone` · `.emp-*` · `.slot-*` · `.drawer-panel.wide` · `.line-expand-panel` |
| 2 | ถอด `FWD-WIRE:` ออกจาก microcopy 7 บรรทัด | ข้อความบนจอสั้นลง ไม่มีศัพท์ภายใน |
| 3 | ประกาศ `--z-*` 6 ตัว + ยก toast เมื่อมี overlay | toast มองเห็นได้เมื่อลิ้นชักเปิด |
| 4 | flip เมนูแถวเมื่อชนขอบล่าง | เมนูแถวสุดท้ายกดครบทุกรายการ |

> **อย่ารันการเทียบไฟล์กับ `input/` แล้วสรุปว่าแพ็กผิด** — ความต่างทั้ง 4 จุดเป็นการแก้ข้อบกพร่องที่มีหลักฐานใน `01_HTML/_UX_CHECK_REPORT.md`
