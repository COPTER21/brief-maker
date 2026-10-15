# HTML UI Brief — F-PUR-RTV · RTV คืนผู้ขาย

> **EXTRACTION-BASED** — ทุกบรรทัดสกัดจาก `01_HTML/F-PUR-RTV.html` (หลัง 7R re-gate · **2,555 บรรทัด** · md5 `5b285dd17f6be90e82891875642bac9e`)
> HTML = source of truth · ไฟล์นี้ไม่แต่งสเปคเพิ่ม (R1) · ใช้คู่กับ `03_FRD/01_UI.md` (Layout Decision Log) และ `03_FRD/07_LOCKED_DECISIONS.md`
> Pairing: FRD Pack **มี** (`03_FRD/*`) → §11 ทำ traceability 3 ทาง + Drift Log ตาม R6

## §0 Document Control

| หัวข้อ | ค่า |
|---|---|
| Feature | F-PUR-RTV · RTV คืนผู้ขาย (Return to Vendor) · `F080` |
| Archetype | Pattern Q เต็ม (transaction-document) + B2 v2 line editor + DOA |
| HTML | `01_HTML/F-PUR-RTV.html` · 2,555 บรรทัด |
| FRD ที่ pair | `03_FRD/00_OVERVIEW.md` · `01_UI.md` · `02_API.md` · `03_LOGIC.md` · `05_RULES.md` · `06_TESTS.md` · `07_LOCKED_DECISIONS.md` |
| สถานะ drift | **มี 3 จุดที่ HTML "สอบตก" เทียบสเปค** (ดู §11 Drift Log) — ตั้งใจบันทึกไว้ ไม่ใช่ตกหล่น |

## §1 Design Tokens AS-BUILT

### §1.1 `:root` block ที่ 1 — BASE-KIT v6.4 (บรรทัด 13–58)

| Token | ค่า | Token | ค่า |
|---|---|---|---|
| `--c-navy` / `--c-navy-2` / `--c-ink` | `#111111` | `--c-primary` | `#FF3B30` |
| `--c-primary-hover` | `#E62E24` | `--c-teal` | `#FF9A1F` |
| `--c-teal-light` | `#FFB763` | `--c-mute` | `#54565C` |
| `--c-mute-2` | `#73757B` | `--c-mute-3` | `#9A9CA2` |
| `--c-line` | `#DEDAD4` | `--c-line-2` | `#E9E5E0` |
| `--c-line-3` | `#F1EEEA` | `--c-bg-off` | `#FAF8F5` |
| `--c-success` | `#1F9D55` | `--c-warning` | `#E8870F` |
| `--c-danger` | `#E62E24` | `--sidebar-w` / `--shell-h` | `232px` / `52px` |

**Type scale:** `--fs-h1 22` · `--fs-h2 17` · `--fs-h3 15` · `--fs-body 14` · `--fs-sub 13` · `--fs-meta 12` · `--fs-cap 11` · `--fs-kpi 28`
**Spacing:** `--sp-xs 4` · `--sp-sm 8` · `--sp-md 12` · `--sp-lg 20` · `--sp-xl 28`
**Radius:** `--r-xs 4` · `--r-sm 6` · `--r-md 8` · `--r-lg 12` · `--r-full 999`

### §1.2 z-index scale — **§2 มีรายละเอียดเต็ม (นี่คือค่าดิบใน `:root` บรรทัด 38)**

`--z-sticky: 19; --z-shell: 20; --z-dropdown: 65; --z-backdrop: 50; --z-drawer: 51; --z-modal: 61; --z-toast: 70;`

### §1.3 `:root` block ที่ 2 — archetype aliases (Pattern Q / B2 v2 · บรรทัด 39–57)

`--c-white #FFFFFF` · `--c-text #111111` · `--c-text-mute #54565C` · `--c-text-soft #9A9CA2` · `--c-slate #73757B` · `--c-border #DEDAD4` · `--c-border-soft #E9E5E0` · `--c-off-white #FAF8F5`
โปร่งแสง: `--c-primary-08` `rgba(255,59,48,.08)` · `--c-primary-12` · `--c-teal-08` `rgba(31,157,85,.10)` · `--c-warning-08` · `--c-danger-08`
`--r: 8px` · เงา `--sh-md` `0 2px 8px rgba(17,17,17,.05)` / `--sh-lg` `0 12px 32px rgba(17,17,17,.12)` / `--sh-xl` `-16px 0 40px rgba(17,17,17,.18)`

> ⚠️ **`--c-purple: #FF9A1F`** (ส้ม จริง ๆ) — ใช้กับตัวเลข VAT ในบางที่ (ตระกูลเดียวกับข้อสังเกตของ GRN brief) **ไม่ใช่สีม่วง** อย่าไปแก้ชื่อ token

### §1.4 Fonts / Icons

`'Satoshi', 'Noto Sans Thai', system-ui, sans-serif` (หลัก) — โหลดจาก `fonts.googleapis.com` (Noto Sans Thai 400–800) + `api.fontshare.com` (Satoshi 300–900) · ไอคอน Lucide (`data-lucide`, `renderIcons()`, boot รอ `lucide:ready` หรือ timeout 5s ที่บรรทัดท้ายไฟล์)

## §2 z-index map (สกัดจากค่าจริงใน `:root` + การใช้งานจริงในซีเลกเตอร์)

| ชั้น | selector ที่ใช้ | token | ค่า |
|---|---|---|---|
| sticky header ตาราง | `thead th` | `--z-sticky` | **19** |
| shell / sidebar | `.sidebar` | `--z-shell` | **20** |
| backdrop ลิ้นชัก | `.drawer-backdrop` | `--z-backdrop` | **50** |
| ลิ้นชัก | `.drawer-host` | `--z-drawer` | **51** |
| กล่องโต้ตอบ (modal) | `.modal-backdrop` | `--z-modal` | **61** |
| **dropdown / เมนูแถว / ป๊อปอัปคอมโบ** | `.menu-fixed` · `.combo-pop` (บรรทัด 145, 172, 381, 420, 456) | `--z-dropdown` | **65** |
| toast | `.toast#toast` | `--z-toast` | **70** |

**ลำดับจริง (ต่ำ → สูง):** `sticky 19 < shell 20 < backdrop 50 < drawer 51 < modal 61 < dropdown 65 < toast 70`

> ⚠️ **`--z-dropdown` ต้องอยู่สูงกว่า `--z-modal` เสมอ** — `.combo-pop` (ป๊อปอัปค้นหาทะเบียน: ผู้ขอคืน · คลัง · ศูนย์ต้นทุน · location ต้นทางรายบรรทัด · **ผู้อนุมัติต่อขั้น** · location รับของกลับ) ถูก portal เข้า `#overlay-root` และใช้ร่วมกันทั้งใน **ลิ้นชัก** (z 51) และ **กล่องโต้ตอบส่งอนุมัติ** (z 61) — ถ้า `--z-dropdown` ต่ำกว่าตัวใดตัวหนึ่งใน 2 ค่านี้ ป๊อปอัปจะถูกบังจนมองไม่เห็นและกดด้วยเมาส์ไม่ได้ (เส้นทางคีย์บอร์ด ↓+Enter ยังใช้ได้เพราะไม่พึ่งการมองเห็น)
> **นี่คือ `07_LOCKED_DECISIONS.md LD-16`** — ค่าเดิมก่อนแก้คือ `40` (ต่ำกว่าทั้งลิ้นชักและ modal) ซึ่งบล็อกการเลือกผู้อนุมัติ (`BR-10`/`LOCK-03`) ทั้งไฟล์ · แก้แล้วเป็น `65` ในเลนนี้ (อนุมัติ 2026-09-15) **ห้ามลดค่านี้ลงต่ำกว่า 61 อีก** — จะทำให้บั๊กเดิมกลับมา

## §3 Route map (`getRoute()` บรรทัด 1151–1160)

```js
function getRoute() {
  var h = (location.hash || '').replace(/^#\/?/, '');
  if (!h) return { name:'list' };
  var p = h.split('/');
  if (p[0] === 'view')   return { name:'view', id:p[1] };
  if (p[0] === 'edit')   return { name:'edit', id:p[1] };
  if (p[0] === 'create') return { name:'create', from:p[1] || '' };
  return { name:'list' };
}
function navigate(to) { location.hash = '#/' + to; }
```

| Route | เปิดอะไร | ฟังก์ชันที่จับ |
|---|---|---|
| `#/` (ไม่มี hash) และ `#/list` | หน้ารายการ | fallback ของ `getRoute()` → `{name:'list'}` |
| `#/create` | ลิ้นชักตัวช่วยสร้าง เริ่มขั้น 1 | `openCreateDrawer(null, from)` |
| `#/create/:grnCode` | ทำสำเนา — ขั้น 1 พร้อม GRN เลือกไว้แล้ว | `dupRtv()` → `navigate('create/'+r.grn)` → `pickGrn(from, true)` |
| `#/edit/:id` | ลิ้นชักแก้ร่าง **เริ่มขั้น 2** (Iron Rule #100) | `openCreateDrawer(editId)` → `createWizard.step = 2` |
| `#/view/:id` | ลิ้นชักดูเอกสาร เริ่มแท็บ `detail` | `openViewDrawer(id)` |

`hashchange` listener (บรรทัด 2534): `window.addEventListener('hashchange', function(){ state.tab = state.tab || 'detail'; render(); });` — refresh-safe เพราะ hash ถือ state ทั้งหมด (route + id) · id ที่ไม่มีจริง (`!findRtv(r.id)`) → `navigate('list')` อัตโนมัติ (บรรทัด 2508)

## §4 Layout Shell

Sidebar `232px` พื้น `#111111` + shell-bar `52px` breadcrumb `จัดซื้อ › คืนผู้ขาย (RTV)` · เมนูข้าง 2 โมดูล (จัดซื้อ 4 รายการ · คลังสินค้า 4 รายการ) · badge `#sb-count` (นับใบ `draft/pending/approved/returned`) · รายการเมนูอื่นเรียก `notWired(name)` → toast `'{name} — อยู่นอกขอบเขตต้นแบบนี้ (ดู HANDOFF)'`
Overlay hosts (ประกาศต่อกันที่ท้าย `<body>`, บรรทัด 573–577):

```html
<div class="drawer-backdrop" id="drawer-backdrop" onclick="closeTopOverlay()"></div>
<div class="drawer-host" id="drawer-host"></div>
<div id="modal-root"></div>
<div id="overlay-root"></div>
<div class="toast" id="toast"></div>
```

## §5 Route / Page Anatomy (15 surfaces — ตรงกับ `01_UI.md P-01..P-15`)

### P-01 · หน้ารายการ (`#/`, `#/list`) — `renderPage()` · `renderTableHtml()`

หัวหน้า `ใบคืนสินค้าผู้ขาย (Return to Vendor)` + ปุ่ม `ส่งออก CSV` (`exportCsv()`) · `สร้างใบคืนสินค้า` (`navigate('create')`)
**KPI 5 ใบ** (`kpis()`/`statCard()`): ใบคืนเดือนนี้ · มูลค่าที่คืนสะสม · รออนุมัติ · ของค้าง quarantine รอคืน · มูลค่ารอเครดิตจากผู้ขาย
**ตัวกรอง 4 แกน + 1 สวิตช์** (`setFilter()`): ค้นหา (placeholder `ค้นหาเลขที่ RTV / GRN / PO / ผู้ขาย / เลข RMA`) · สถานะ (7 ค่า) · เหตุผลคืนหลัก (4 ค่า) · ผู้ขาย · เช็กบ็อกซ์ `รวมที่ยกเลิก/กลับรายการ` (กลไก soft archive — `rtvFiltered()` บรรทัด 1166–1178 ซ่อน `cancelled`/`reversed` เป็นค่าตั้งต้น) · ปุ่ม `รีเซ็ต`
**ตาราง 8 คอลัมน์:** เลขที่ (`r.code` หรือ `ยังไม่ออกเลข`) · วันที่เอกสาร · ผู้ขาย · อ้างใบรับของ (`tbl-mono`) · สถานะเอกสาร (`docPill`) · ลายเซ็น (`renderSignProgress` — `n/N` + `.pgl`) · มูลค่าที่คืน (ชิดขวา) · คอลัมน์เมนู
`pageSize = 8` · คลิกแถว → `#/view/:id`
**เมนูแถว** (`openRowMenu()` บรรทัด 1320–1336, portal เข้า `#overlay-root` เป็น `.menu-fixed`): `เปิดดูใบ` (ทุกสถานะ) → `แก้ไขร่าง` (เฉพาะ `draft`) → `พิมพ์ใบคืนสินค้า` (`approved`/`returned`/`closed`, ไป `#/view/:id` แล้วตั้ง `state.tab='pdf'`) → `ยกเลิกใบ` (`draft`/`pending`/`approved`, เรียก `openModal('cancel', id)`)
**สถานะว่างเปล่า 2 แบบ** (`emptyStateHTML()`): มีตัวกรอง → `ไม่พบใบคืนสินค้าที่ตรงกับตัวกรอง` / ไม่มีตัวกรอง → `ยังไม่มีใบคืนสินค้า`

### P-02 · ขั้น 1 เลือกแหล่งที่มา (`#/create`) — `renderStep1()`

`STEPH('git-branch', 'เลือกแหล่งที่มาของใบคืนสินค้า', '...')` · tile 2 ช่อง: `.tile-btn.on` **"จากใบรับของ (GRN)"** · `.tile-btn.is-off` **"คืนของที่ไม่มีใบรับของ"** (กดแล้ว `showToast('คืนของที่ไม่มีใบรับของ — ไม่รองรับในรอบนี้ ให้ใช้ปรับปรุงสต๊อก (W3Q)','warning')`)
การ์ดตาราง GRN ที่คืนได้ (`renderGrnRowsHtml()`) — เลือกได้: แถวคลิกได้ + ปุ่ม `ใช้ใบนี้` · เลือกไม่ได้: `opacity .55` + เหตุผลจาก `grnBlockReason()`

### P-03 · ขั้น 2 ข้อมูลหลักใบคืนสินค้า (`#/create`) — `renderStep2()`

`STEPH('clipboard-list', 'ข้อมูลหลักใบคืนสินค้า')` · การ์ดอ่านอย่างเดียว "ข้อมูลจากใบรับของ" · `.form-grid` 9 ช่อง: เหตุผลคืนหลัก (`#f-reason`) · วันที่เอกสาร (`#f-docdate`, `max=TODAY_ISO`) · วันที่ส่งคืน (คาดการณ์) · เลข RMA · ผู้ขอคืน (`#f-requester`, master combobox) · คลัง/สาขาที่ของออก (`#f-wh`) · ศูนย์ต้นทุน (cascade clear เมื่อคลังถูกล้าง) · ที่อยู่ส่งคืน · หมายเหตุ

### P-04 · ขั้น 3 รายการสินค้า (`#/create`) — `renderStep3()` · `renderLineRow()`

`STEPH` icon `list` (ดูโค้ด) · ปุ่ม `คืนทั้งหมดที่คืนได้` (`fillAllReturnable()`) · `ดึงข้อมูลจากใบรับของใหม่` (`reloadFromGrn()`)
`.tbl.line-tbl` **9 คอลัมน์** กว้าง `26 / — / 64 / 92 / 92 / 78 / 72 / 104 / 54`: `#` · สินค้า · จำนวน (ช่องกรอกเดียว) · หน่วย · ราคา/หน่วย (อ่านอย่างเดียว) · ส่วนลด % (อ่านอย่างเดียว) · ภาษี (`taxBadgeV()`) · จำนวนเงิน (`calcLineVat().lineTotal`) · ปุ่มขยาย (chevron)
**แถวขยาย 1 บรรทัด** (`.line-expand-panel`): VAT segmented 3 ค่า · เหตุผลคืน select 6 ค่า · ตัดออกจาก (master combobox `line-loc-{id}`) · หมายเหตุ
ใต้ตาราง `renderLineSummary()`: กล่อง `.hard-warn` จาก `wizardBlockers()` (ถ้ามี) → ยอดรวมก่อนภาษี → VAT 7% → มูลค่าที่คืนรวม

### P-05 · ขั้น 4 เอกสารแนบ (`#/create`) — `renderStep4()`

`STEPH('paperclip', 'แนบเอกสารประกอบ (ถ้ามี)', 'รูปสภาพสินค้า · ใบส่งคืน · ...')` · `.upload-zone` — "ลากไฟล์มาวาง หรือกดเพื่อเลือกไฟล์" · "รองรับ PDF / JPG / PNG / ZIP · ไม่เกิน 20 MB ต่อไฟล์" · `addMockFile()` → toast `แนบไฟล์แล้ว (ข้อมูลจำลอง)` · `removeFile()`
> ⚠️ ขั้นนี้เข้าถึงได้เฉพาะตอนใบเป็น **ร่าง** — ดู §11 Drift Log (LD-15)

### P-06 · ขั้น 5 ตรวจสอบและยืนยัน (`#/create`) — `renderStep5()`

`STEPH('check-circle-2', 'ตรวจสอบและยืนยัน', 'ตรวจความถูกต้องก่อนส่งอนุมัติ — ...')` · ลำดับ: `.hard-warn` (ถ้ามี) → ข้อมูลใบคืนสินค้า (10 ช่อง kv) → สายอนุมัติที่ resolve จากมูลค่า → แถบเตือน **`ใบคืนนี้ไม่เปิดยอดค้างรับกลับไปที่ {PO}`** → `linesTableView()` อ่านอย่างเดียว → เอกสารแนบ (N ไฟล์)
footer: `ย้อนกลับ` · `ยกเลิก` · `บันทึกแบบร่าง` · `บันทึกและส่งอนุมัติ` (`disabled` + `title="ยังมีข้อมูลไม่ครบ"` เมื่อ `wizardBlockers().length > 0`)

### P-07 · หน้าต่างส่งอนุมัติ (modal `submit`, `.is-lg`) — `openSubmitModal()` · `renderSubmitModalBody()`

Title `ส่งอนุมัติใบคืนสินค้า` / sub `เลือกผู้อนุมัติคนจริงต่อขั้นตามทะเบียน DOA` (`modalConfig('submit')` บรรทัด 2135)
ต่อขั้น (`.slot-row`): เลขขั้น · ชื่อตำแหน่ง + `ขั้นที่ n จาก N` · master combobox → เลือกแล้วแสดง `empChip` · ยังไม่เลือก → `.is-err` + `ยังไม่ได้เลือกผู้อนุมัติ`
ปุ่ม `ส่งอนุมัติ` (`id="btn-do-submit"`) `disabled` จนครบทุกขั้น · กำลังส่ง → `กำลังส่งอนุมัติ…` (กันกดซ้ำ)

### P-08 · ลิ้นชักดูเอกสาร แท็บ `รายละเอียด` (landing, `#/view/:id`) — `renderDetailTab()`

ลำดับ section จริง (บรรทัด 2279–2331, ผ่าน `SECWRAP(SEC(icon,title)+...)`): แบนเนอร์ (ยกเลิก/กลับรายการ/ส่งกลับแก้/**ไม่เปิดยอดค้างรับกลับ PO** เสมอ) → **ข้อมูลเอกสาร** → **สถานะ** (เอกสาร · ความคืบหน้าอนุมัติ · สถานะเครดิต) → **เอกสารอ้างอิง** (GRN · PO · สถานะการล็อกใบรับของ) → **คู่ค้าและผู้รับผิดชอบ** → **เครดิตจากผู้ขาย (ยังไม่ลงบัญชี)** → **รายการสินค้าที่คืน (N)** → **เอกสารแนบ (N ไฟล์ · Document Center)** → **ข้อมูลระบบ**
ปุ่มตามสถานะ: `draft`→`ยกเลิก`·`แก้ไข`·`ส่งอนุมัติ` · `pending`→`ไม่อนุมัติ`·`ส่งกลับแก้`·`อนุมัติ` · `approved`→`ยกเลิก`·`บันทึกส่งคืน` · `returned`→`กลับรายการ`·`บันทึกเครดิต · ปิดใบ` · `closed`/`cancelled`/`reversed`→ไม่มีปุ่มกระทำ

### P-09 · แท็บ `คืนของและสต๊อก` (`stock`) — `renderStockTab()`

section 1 **ผลต่อสต๊อก**: note ยังไม่ตัด/ตัดแล้ว + ตาราง 5 คอลัมน์ (สินค้า · ตัดออกจาก · จำนวน · ประเภทที่อยู่ · สถานะ movement)
section 2 **ผลต่อเอกสารต้นทาง**: `ยอดคืนสะสมที่ {GRN}` · `การกลับรายการใบรับของ` · **`ยอดค้างรับที่ {PO}` = `ไม่เปลี่ยน` เสมอ** (คอมเมนต์ในซอร์ส "มติ OQ-RTV-01 [ASSUMED]" บรรทัด 2359) + note forward-wire ตรวจของยังอยู่จริง (`FW-02`)

### P-10 · แท็บ `PDF Preview` (`pdf`) — `renderPdfTab()` · `pdfSign()`

Toolbar: `ตัวอย่าง PDF · A4 · 1/1` (+ `· พิมพ์ได้เป็นตัวอย่างเท่านั้นจนกว่าจะอนุมัติครบ` เมื่อยังไม่ถึง `approved`) · ปุ่ม `ดาวน์โหลด` · `พิมพ์` (`window.print()`)
`.a4`: หัวบริษัท → ผู้ขาย/ที่อยู่/ภาษี/RMA คู่กับวันที่/GRN/PO/คลัง/ผู้ส่ง → ตารางรายการ 7 คอลัมน์ (**มีคอลัมน์เหตุผลคืน**) → หมายเหตุ + ยอดรวม → **ช่องลงชื่อ 3 ฝ่าย** (`pdfSign()` × 3): `ผู้จัดทำ / ผู้ขอคืน` · `ผู้อนุมัติ` (คนที่อนุมัติล่าสุด) · `ผู้รับฝั่งผู้ขาย` → ท้ายกระดาษ `{เลขที่} · {ผู้ขาย}` + `พิมพ์เมื่อ {วันที่} · หน้า 1/1`
**ลายน้ำ (บรรทัด 2380–2383):** ไม่อยู่ใน `['returned','closed','approved']` → **`ตัวอย่าง`** (สีเทาจาง หมุน -18°) · `status==='cancelled'` → **`ยกเลิก`** (สีแดงจาง) · `status==='reversed'` → **`กลับรายการ`** (สีแดงจาง) · `approved`/`returned`/`closed` → **ไม่มีลายน้ำ**

### P-11 · แท็บ `ลายเซ็น / อนุมัติ` (`sign`) — `renderSignTab()`

section 1 **สายอนุมัติ (DOA)**: kv 4 ช่อง (ทะเบียน DOA · สถานะ+ขั้น n/N · ผู้ส่งอนุมัติ · ฐานวงเงินที่ใช้ resolve) — ยังไม่ส่ง → note `ยังไม่ส่งอนุมัติ — สายอนุมัติจะถูก resolve ตามมูลค่าที่คืนตอนกดส่ง`
section 2 **ลำดับการอนุมัติ**: timeline `ส่งอนุมัติ` → ต่อขั้น (`ขั้นที่ n · {ตำแหน่ง} — {ผล}` + `empChip` + เวลา + ความเห็น) → `ผลลัพธ์`
**เงื่อนไขปุ่มตัดสินใจ inline (บรรทัด 2450):** `var canAct = r.status === 'pending' && cur;` — โผล่เฉพาะที่ขั้นปัจจุบัน (`cur === s`) **ไม่มีการเทียบผู้ใช้ที่ล็อกอิน (`state.me`) กับคนที่ถูกเลือกไว้ในขั้นนั้น** → ดู §11 Drift Log (LD-13)
section 3 **ผู้เกี่ยวข้องหน้างาน (ไม่ใช่สายอนุมัติ)**: ผู้ขอคืน · ผู้ส่งของคืน · ผู้รับฝั่งผู้ขาย

### P-12 · แท็บ `ประวัติ` (`history`) — `renderHistoryTab()`

`.tl` timeline ต่อท้ายอย่างเดียวจาก `r.audit[]` · โทนสี: แดง (ยกเลิก/ปฏิเสธ/กลับรายการ) · ส้ม (ส่งกลับ) · เขียว/ปกติ (อื่น ๆ) · **ไม่มีปุ่มแก้ไข/ลบ**

### P-13/14/15 · หน้าต่างการกระทำ — `openModal(type,id)` → `modalConfig(type,id)` → `renderModalBody()`

| type | title (verbatim) | sub (verbatim) | ปุ่มยืนยัน | ขนาด |
|---|---|---|---|---|
| `ship` | `บันทึกส่งคืน {code}` | `ของออกจากคลังจริง — สต๊อกจะถูกตัดทันทีและแก้ไม่ได้` | `บันทึกส่งคืน` (`id="btn-do-ship"`) | `.is-lg` (680) |
| `credit` | `บันทึกเครดิต · ปิดใบ {code}` | `บันทึกเลขเอกสารเครดิตจากผู้ขาย (ยังไม่ลงบัญชีจริง)` | `บันทึกและปิดใบ` | `.is-lg` (680) |
| `reverse` | `กลับรายการ {code}` | `ของกลับเข้าคลัง — สร้าง movement ตรงข้าม ไม่ลบของเดิม` | `ยืนยันกลับรายการ` (แดง) | `.is-lg` (680) |
| `cancel` | `ยกเลิกใบคืนสินค้า {code หรือ (ร่าง)}` | `ยกเลิกได้เฉพาะก่อนของออกจากคลัง` | `ยืนยันยกเลิกใบ` (แดง) | 440 |
| `sendback` | `ส่งกลับแก้ {code}` | `ระบุสิ่งที่ต้องแก้ — ใบจะกลับไปเป็นร่างโดยใช้เลขเดิม` | `ส่งกลับแก้` | 440 |
| `reject` | `ไม่อนุมัติ {code}` | `ใบจะถูกยกเลิกถาวร — ของยังอยู่ที่เดิม` | `ไม่อนุมัติ` (แดง) | 440 |
| `approve` | `อนุมัติใบคืนสินค้า {code}` | `ยืนยันว่าตรวจของและเหตุผลคืนแล้ว` | `อนุมัติ` (เขียว) | 440 |
| `submit` | `ส่งอนุมัติใบคืนสินค้า` | `เลือกผู้อนุมัติคนจริงต่อขั้นตามทะเบียน DOA` | `ส่งอนุมัติ` | `.is-lg` (680) — คือ P-07 |

`sendback`/`reject`/`cancel` มีปุ่มลัดข้อความสำเร็จรูป 3 ชุด (`presets`, บรรทัด 2162–2164) เช่น cancel: `ผู้ขายยอมลดราคาแทนการรับคืน` · `เปลี่ยนเป็นเบิกใช้ภายใน` · `ออกใบใหม่แทนใบนี้`
`ship` เพิ่ม section `สต๊อกที่จะถูกตัดออก` ไล่รายบรรทัด · `reverse` เพิ่มช่อง location รับของกลับ (บังคับคู่กับเหตุผล)

## §6 Component states

| Component | selector/function | states |
|---|---|---|
| `.tile-btn` | ขั้น 1 | `.on` (เลือกอยู่) · `.is-off` (ปิดใช้งาน + toast อธิบาย) |
| GRN picker card | `renderGrnRowsHtml()` | ปกติ (คลิกได้ + ปุ่ม `ใช้ใบนี้`) · `opacity:.55` (เลือกไม่ได้ + เหตุผลจาก `grnBlockReason()`) |
| `.stepper-item` | `renderStepperItem()` | active (ขั้นปัจจุบัน) · done (คลิกย้อนได้) · ปกติ |
| `.field` / `.is-error` | ทุกฟอร์ม | ปกติ · error (แดง + ข้อความใต้ช่อง) |
| `.slot-row` / `.is-err` | modal `submit` | ยังไม่เลือก (`.is-err` + `ยังไม่ได้เลือกผู้อนุมัติ`) · เลือกแล้ว (`empChip`) |
| `.pill` (`docPill`) | 7 สถานะ | `draft`(cls `draft`) · `pending`(`pending`) · `approved`(`sent`) · `returned`(`approved`) · `closed`(`approved`) · `cancelled`(`cancelled`) · `reversed`(`rejected`) |
| `creditPill()` | แท็บรายละเอียด | `ได้รับเครดิตแล้ว`(closed) · `รอเครดิตจากผู้ขาย`(returned) · `ยังไม่ถึงขั้นเครดิต`(อื่น ๆ) |
| `taxBadgeV()` | ตารางบรรทัด | `ไม่คิด` · `VAT n%` · `NET n%` |
| ปุ่มส่งอนุมัติ/ส่งคืน | ขั้น 5 / P-07 / modal `ship` | ปกติ · `disabled` (มี blockers ค้าง) · กำลังส่ง (`กำลังส่งอนุมัติ…`/`กำลังบันทึก…`) |
| toast (`#toast`) | `showToast()` | 4 variant: `success` · `info` · `warning` · `error` |
| line-expand-panel | ขั้น 3 | ปิด (ปกติ) · เปิด (1 บรรทัดต่อครั้ง — ไม่มี 2 บรรทัดพร้อมกัน) |

## §7 Overlay registry + dismiss rules

| Overlay | id/selector | เปิดด้วย | ปิดด้วย | ขนาด | z-index |
|---|---|---|---|---|---|
| ลิ้นชักตัวช่วยสร้าง | `#create-drawer` `.drawer-panel.wide` | `openCreateDrawer()` | ปุ่มยกเลิก/ปิด · คลิก `.drawer-backdrop` · Esc | **1290** | 51 |
| ลิ้นชักดูเอกสาร | `#view-drawer` `.drawer-panel` | `openViewDrawer(id)` | ปุ่มปิด · คลิก backdrop · Esc | **920** | 51 |
| หน้าต่างการกระทำ (7 แบบ) | `#modal-root` → `.modal` / `.modal.is-lg` | `openModal(type,id)` | ปุ่มยกเลิก/ปิด(×) · คลิก `.modal-backdrop` (`onclick="closeModal()"`) · Esc | 440 / 680 | 61 |
| เมนูแถว | `#row-menu` `.menu-fixed` | `openRowMenu(ev,id)` | คลิกที่ใดก็ได้ (`closeRowMenuOnce`, global listener) · เลือกเมนู · Esc | `min-width` ตาม `.menu-fixed` | 65 |
| combobox popup | `#combo-pop` `.combo-pop` (portal `#overlay-root`) | `comboOpenPop()`/focus | คลิกนอก (`comboOutside`) · เลือกค่า · Esc (`comboClosePop()`) | ตาม trigger | 65 |
| toast | `#toast` | `showToast(msg, variant, ms)` | หมดเวลาเอง | มุมขวาล่าง | 70 |

**.standard (680) ไม่ถูกใช้ในฟีเจอร์นี้** — โมดัลใหญ่ใช้ `.is-lg` (680) โมดัลเล็กใช้ฐาน (440); ลิ้นชัก standard (680) ก็ไม่ถูกใช้ — มีแต่ `.drawer-panel` ฐาน (920) กับ `.wide` (1290)
**"ห้ามปิด" ไม่มีในฟีเจอร์นี้** — ทุก overlay ปิดได้ด้วย Esc/backdrop เสมอ (ต่างจากบางฟีเจอร์ที่ล็อก modal ระหว่างส่งคำขอ — ที่นี่ระหว่าง "กำลังส่งอนุมัติ…"/"กำลังบันทึก…" ปุ่มยืนยันถูก disable แต่ปุ่มยกเลิก/Esc ยังกดได้ตามโค้ดที่อ่านได้)

## §8 Interaction Spec

**Esc chain (`window.addEventListener('keydown', ...)` บรรทัด 2528–2533 — ลำดับจริงในโค้ด):**
1. `#combo-pop` เปิดอยู่ → `comboClosePop()` เท่านั้น (หยุดที่นี่)
2. ไม่มีคอมโบ แต่ `#row-menu` เปิดอยู่ → `closeRowMenu()` เท่านั้น
3. ไม่มีทั้งสอง → `closeTopOverlay()`: ถ้ามี `state.modal` → `closeModal()` · ไม่งั้นถ้า route เป็น `view` → `closeViewDrawer()` · ถ้าเป็น `create`/`edit` → `closeCreateDrawer()`

ปิดลิ้นชักแล้ว `navigate()`: ลิ้นชักแก้ไข (`edit`) → กลับ `#/view/:id` (implied — เดิมมาจาก view) · ลิ้นชักสร้าง/ดูเอกสาร → `#/`
**Click-outside:** `.drawer-backdrop` และ `.modal-backdrop` เรียก `closeTopOverlay()`/`closeModal()` ตรง ๆ ใน `onclick` · เมนูแถวปิดด้วย global `click` listener (`closeRowMenuOnce`) · คอมโบปิดด้วย `comboOutside()`
**Focus/scroll:** `preserveRenderState()`/`restoreRenderState()` ทุกครั้งที่ `render()` — คืนตำแหน่งเคอร์เซอร์/สกอลล์หลังวาดใหม่ (กัน re-render ทำ focus หลุด)
**Positioning:** ลิ้นชัก/backdrop = `position:fixed` เต็มจอ · โมดัล = `.modal-backdrop{position:fixed}` + `.modal{width:440px}` กึ่งกลาง · combo/row-menu = `position:fixed` คำนวณตำแหน่งจาก trigger (`portalMenu()`) — พลิกขึ้นบนเมื่อชนขอบล่างจอ

## §9 State-driven UI Matrix

**7 สถานะ (`STATUS` object, บรรทัด 971–979):**

| status | label | pill class | ปุ่มกระทำในลิ้นชัก (ซ้าย→ขวา) |
|---|---|---|---|
| `draft` | ร่าง | `draft` | ยกเลิก(แดง) · แก้ไข · ส่งอนุมัติ |
| `pending` | รออนุมัติ | `pending` | ไม่อนุมัติ(แดง) · ส่งกลับแก้ · อนุมัติ(เขียว) |
| `approved` | อนุมัติแล้ว | `sent` | ยกเลิก(แดง) · บันทึกส่งคืน |
| `returned` | ส่งคืนแล้ว | `approved` | กลับรายการ(แดง) · บันทึกเครดิต·ปิดใบ |
| `closed` | ปิดใบ | `approved` | — (สถานะปลายทาง) |
| `cancelled` | ยกเลิก | `cancelled` | — (สถานะปลายทาง) |
| `reversed` | กลับรายการ | `rejected` | — (สถานะปลายทาง) |

ปุ่มถาวรทางขวาทุกสถานะ: `ทำสำเนา` · `พิมพ์` · `ดาวน์โหลด` · `ปิด`
เมื่อ `returned`/`closed` → เพิ่มข้อความ `ของออกจากคลังแล้ว ล็อกแก้ไข` ท้ายลิ้นชัก

## §10 Microcopy (verbatim จากโค้ด — ห้าม paraphrase)

### §10.1 Toast (`showToast(msg, variant)` — ทุกจุดเรียกในไฟล์)

| บริบท | ข้อความ | variant |
|---|---|---|
| กดช่อง "คืนของที่ไม่มีใบรับของ" | `คืนของที่ไม่มีใบรับของ — ไม่รองรับในรอบนี้ ให้ใช้ปรับปรุงสต๊อก (W3Q)` | warning |
| GRN เลือกไม่ได้ | `{รหัส GRN} — {เหตุผลจาก grnBlockReason()}` | warning |
| ดึงบรรทัดจาก GRN สำเร็จ | `ดึงรายการจาก {code} แล้ว {N} บรรทัด` | success |
| ขั้น 1 ยังไม่เลือก GRN | `กรุณาเลือกใบรับของ (GRN) ที่จะคืน` | warning |
| ขั้น 2 ช่องบังคับไม่ครบ | `กรุณากรอกข้อมูลให้ครบถ้วน` | warning |
| ขั้น 3 ทุกบรรทัด = 0 | `ต้องมีอย่างน้อย 1 บรรทัดที่จำนวนคืนมากกว่า 0` | warning |
| ขั้น 3 มีบรรทัดยังแก้ไม่ครบ | `มี {N} บรรทัดที่ยังแก้ไข่ครบ — ดูข้อความสีแดงในตาราง` (ตรวจซ้ำ: ต้นฉบับคือ "มี {N} บรรทัดที่ยังแก้ไม่ครบ — ดูข้อความสีแดงในตาราง") | warning |
| กดค้นหา GRN ไม่พบ | `พบหลายใบ — เลือกจากรายการ` / `ไม่พบใบรับของ {q}` | warning |
| กด "คืนทั้งหมดที่คืนได้" | `เติมจำนวนคืนเท่ากับยอดคืนได้ทุกบรรทัดแล้ว` | success |
| กด "ดึงข้อมูลจากใบรับของใหม่" | `ดึงข้อมูลจากใบรับของใหม่แล้ว — ตรวจจำนวนอีกครั้ง` | info |
| แนบไฟล์ (จำลอง) | `แนบไฟล์แล้ว (ข้อมูลจำลอง)` | success |
| บันทึกร่างไม่มี GRN | `กรุณาเลือกใบรับของก่อนบันทึกร่าง` | warning |
| บันทึกร่างสำเร็จ | `บันทึกร่างแล้ว — ยังไม่ออกเลขที่ และสต๊อกยังไม่ขยับ` | success |
| กดส่งอนุมัติแต่ยังมี blocker | `ยังส่งอนุมัติไม่ได้ — {blocker แรก}` | warning |
| หน้าต่าง submit เลือกผู้อนุมัติไม่ครบ | `ต้องเลือกผู้อนุมัติให้ครบทุกขั้น` | warning |
| ส่งอนุมัติสำเร็จ | `ส่งอนุมัติแล้ว · {code} — รอ {ชื่อผู้อนุมัติขั้น 1}` | success |
| อนุมัติสำเร็จ (ครบสาย) | `อนุมัติครบทุกขั้นแล้ว — กด "บันทึกส่งคืน" เมื่อของออกจากคลังจริง` | success |
| อนุมัติสำเร็จ (ยังไม่ครบ) | `อนุมัติขั้นที่ {n} แล้ว` | success |
| ส่งกลับแก้ไม่กรอกเหตุผล | `กรุณาระบุเหตุผลที่ส่งกลับแก้` | warning |
| ส่งกลับแก้สำเร็จ | `ส่งกลับให้ผู้จัดทำแก้แล้ว — เลขที่ใบยังเป็นเลขเดิม` | info |
| ไม่อนุมัติไม่กรอกเหตุผล | `กรุณาระบุเหตุผลที่ปฏิเสธ` | warning |
| ไม่อนุมัติสำเร็จ | `ปฏิเสธใบคืนแล้ว — สต๊อกไม่เปลี่ยนแปลง` | info |
| ยกเลิกไม่กรอกเหตุผล | `กรุณาระบุเหตุผลที่ยกเลิก` | warning |
| ยกเลิกสำเร็จ | `ยกเลิกใบคืนแล้ว — ของกลับไปนับเป็นของที่คืนได้ตามเดิม` | info |
| ship ไม่กรอกวันที่ | `กรุณาระบุวันที่ส่งคืนจริง` | warning |
| ship ไม่กรอกผู้ส่ง | `กรุณาระบุผู้ส่งของคืน` | warning |
| ship สำเร็จ | `บันทึกส่งคืนแล้ว — ตัดสต๊อกออกจาก location ต้นทาง และล็อก {GRN} ไม่ให้กลับรายการ` | success |
| credit ไม่กรอกเลขเอกสาร | `ต้องระบุเลขที่เอกสารเครดิตของผู้ขายก่อนปิดใบ` | warning |
| credit สำเร็จ | `ปิดใบแล้ว — บันทึกเครดิตจากผู้ขาย (ยังไม่ลงบัญชีจริง)` | success |
| reverse ไม่กรอกเหตุผล/location | `กรุณาระบุเหตุผลที่กลับรายการ` / `กรุณาระบุ location ที่รับของกลับเข้า` | warning |
| reverse สำเร็จ | `กลับรายการแล้ว — ของกลับเข้า {location} และยอดคืนสะสมที่ {GRN} ถูกหักคืน` | info |
| ทำสำเนา | `ทำสำเนาจาก {code หรือ ร่าง} — ตรวจจำนวนคืนอีกครั้ง` | info |
| ส่งออก CSV | `ส่งออก {N} รายการแล้ว` | success |
| แก้ไขใบที่ไม่ใช่ร่าง | `แก้ไขได้เฉพาะใบที่เป็นร่าง` | warning |

### §10.2 ข้อความบล็อก (`wizardBlockers()` / `lineBlocked()` — ขึ้นในกล่อง `.hard-warn`)

`ยังไม่ได้เลือกใบรับของ (GRN)` · `ยังไม่ได้เลือกเหตุผลคืนหลัก` · `ยังไม่ได้ระบุวันที่เอกสาร` · `ยังไม่ได้ระบุผู้ขอคืน (ต้องเป็นคนจริง)` · `ต้องมีอย่างน้อย 1 บรรทัดที่จำนวนคืนมากกว่า 0` · `บรรทัด {n} · {ชื่อสินค้า} — {เหตุผลจาก lineBlocked()}`
`lineBlocked()` ให้ทีละบรรทัด: `ของถูกใช้ต่อแล้ว — {เอกสารปลายทาง}` · `เกินยอดคืนได้ (สูงสุด {N} {หน่วย})` · `จำนวนคืนติดลบไม่ได้` · `ต้องระบุเหตุผลคืน` · `เลือก "อื่น ๆ" ต้องพิมพ์คำอธิบาย` · `ต้องระบุ location ต้นทางที่ตัดของออก`

### §10.3 ปุ่ม/ป้ายอื่น ๆ ที่ตรวจแล้ว

`ใช้ใบนี้` · `คืนทั้งหมดที่คืนได้` · `ดึงข้อมูลจากใบรับของใหม่` · `บันทึกแบบร่าง` · `บันทึกและส่งอนุมัติ` · `ยังไม่ได้เลือกผู้อนุมัติ` · `เลือกไม่ได้ — {เหตุผล}` (บรรทัดฝัง toast) · `เปิดดูใบ` `แก้ไขร่าง` `พิมพ์ใบคืนสินค้า` `ยกเลิกใบ` (เมนูแถว)

## §11 Data Binding & BACKEND anchors (สรุปสั้น — เต็มอยู่ที่ `02_API.md` §2.1)

| จุดบนจอ (ฟังก์ชันใน HTML) | FRD API |
|---|---|
| `renderPage()` + `rtvFiltered()` + `kpis()` | `API-01 GET /rtv` |
| `openViewDrawer(id)` → `renderViewDrawer()` | `API-02 GET /rtv/{id}` |
| `renderGrnRowsHtml()` · `grnBlockReason()` · `grnReturnable()` | `API-03 GET /rtv/selectable-grns` |
| `pickGrn()` → `commitWizard('draft')` | `API-04 POST /rtv` |
| `updateLine()` · `applyMainReason()` · `saveDraft()` | `API-05 PUT /rtv/{id}` |
| `reloadFromGrn()` | `API-06 POST /rtv/{id}/refresh-from-grn` |
| `openSubmitModal()` → `doSubmit()` → `resolveDoa()` · `nextDocNo()` | `API-07 POST /rtv/{id}/submit` (`FW-03`/`FW-04`) |
| `doApprove()` · `currentSlot()` | `API-08 POST /rtv/{id}/approve` |
| `doSendback()` / `doReject()` | `API-09`/`API-10` |
| `doShip()` | `API-11 POST /rtv/{id}/ship` (`ENG-RTV-03`/`04`) |
| `doCredit()` | `API-12 POST /rtv/{id}/credit` |
| `doReverse()` | `API-13 POST /rtv/{id}/reverse` |
| `doCancel()` / `openModal('cancel')` | `API-14 POST /rtv/{id}/cancel` |
| `addMockFile()` / `removeFile()` | `API-15 attachments` |
| `renderPdfTab()` / `pdfSign()` | `API-16 GET /rtv/{id}/print` |
| `exportCsv()` | `API-17 GET /rtv/export` |
| `resolveDoa()` (เรียกใน `renderStep5()`) | `API-18 GET /rtv/doa-preview` |

## §12 Traceability 3 ทาง

| Brief §x | FRD | HTML anchor |
|---|---|---|
| §2 z-index dropdown vs modal | `07_LOCKED LD-16` · `01_UI §1.4` · `OQ-RTV-13` | `--z-dropdown`, `.combo-pop` z-index บรรทัด 172/420/456 |
| §3 route map | `01_UI §1.0` P-01..P-15 | `getRoute()` บรรทัด 1151 |
| §5 P-02 ขั้น 1 ปิดช่อง "ไม่มี GRN" | `05_RULES BR-01` · `06_TESTS AT-01` | `.tile-btn.is-off` บรรทัด 1636 |
| §5 P-04 baseQty สูตรคืนได้ | `03_LOGIC ENG-RTV-01` · `07_LOCKED LD-14` | `baseQty()` บรรทัด 1007–1014 |
| §5 P-11 canAct ไม่เช็คตัวตน | `05_RULES BR-26` · `07_LOCKED LD-13` | `canAct = r.status==='pending' && cur` บรรทัด 2450 |
| §5 P-05 แนบเฉพาะร่าง | `02_API API-15` · `07_LOCKED LD-15` | `renderStep4()` เป็นจุดเดียวที่มี `.upload-zone` |
| §5 P-01 เมนู "ยกเลิกใบ" | `07_LOCKED LD-17` | `openModal('cancel', id)` บรรทัด 1330 (เดิมเรียก `openReasonModal` — แก้แล้ว) |
| §9 STATUS 7 ค่า | `00_OVERVIEW §0.1 states` | `STATUS` object บรรทัด 971 |
| §10 toast ทั้งชุด | `05_RULES §5.2` (ข้อความ VR) | `showToast()` ทุกจุดที่อ้างในตาราง |

## §13 Drift Log — จุดที่ HTML กับสเปคตั้งใจต่างกัน (ห้ามเงียบ — R6)

> 3 จุดนี้คือช่องว่างจริงที่พบในขั้น 7R re-gate — **ต้นแบบยังไม่ทำตามสเปค** โดยตั้งใจไม่แก้ HTML ในเลนนี้ (นอกสิทธิ์ของเลน) ดู `07_LOCKED_DECISIONS.md` ฉบับเต็ม

| # | จุด | HTML ทำอะไรจริง | สเปคต้องการอะไร | อ้างอิง |
|---|---|---|---|---|
| 1 | **สูตรฐานคืนได้ (`baseQty()`)** | รับ `reasonCode` มาแต่ใช้จริงเฉพาะ `'over'` · ถ้า `qcFail > 0` จะคืน `qcFail` **ทุกเหตุผล** (แม้เหตุผลเป็น `offspec`/`other`) จึงไม่ถึงสาขา `recv − qcFail` เลย · วัดจริง 5/7 บรรทัดใน mock ต่างจากสเปค (เช่น `GRN-2026-0007` ln1: รับ 100 ไม่ผ่าน QC 12 → ต้นแบบให้เพดาน **12** ที่ควรเป็น **88**) | **PREBRIEF §3.3**: เหตุผล `offspec`/`other` ต้องใช้ `max(0, qty_received − qty_qc_failed)` — ของที่ผ่าน QC เข้าคลังปกติแล้วพบภายหลังว่าผิดสเปค | `07_LOCKED_DECISIONS.md LD-14` · `03_LOGIC ENG-RTV-01` ข้อ 2–4 · `OQ-RTV-04` |
| 2 | **กฎตัวตนผู้อนุมัติ** | `canAct = r.status === 'pending' && cur` — ไม่เทียบ `state.me` (ผู้ใช้ล็อกอิน ค่าคงที่ `EMP-1042`) กับคนที่ถูกเลือกไว้ในขั้นปัจจุบัน → ปุ่ม อนุมัติ/ส่งกลับ/ไม่อนุมัติ โผล่ให้ทุกคนกดได้ตราบใดที่ยังมีขั้นค้าง | `05_RULES BR-26`: เฉพาะคนที่ถูกเลือกไว้ในขั้นปัจจุบันเท่านั้น + ผู้จัดทำอนุมัติใบตัวเองไม่ได้ · ฝั่ง server ต้องคืน `NOT_CURRENT_APPROVER` (403) | `07_LOCKED_DECISIONS.md LD-13` · `05_RULES BR-26`/`C-02` · `OQ-RTV-11` |
| 3 | **แนบเอกสารหลังของออก** | ช่องแนบไฟล์มีเฉพาะ `renderStep4()` (ขั้น 4 ของ wizard) ซึ่งเข้าได้เฉพาะตอนใบเป็น `draft` — ไม่มีทางแนบไฟล์เมื่อใบเป็น `returned`/`closed` | `02_API API-15`: แนบได้ทุกสถานะที่ยังไม่ปิดถาวร (รวม `returned`) เพื่อรองรับใบตอบรับผู้ขาย (S-35) และเอกสารเครดิต (S-12) | `07_LOCKED_DECISIONS.md LD-15` · `OQ-RTV-15` |
| 4 | **รหัสรอบพัฒนายังอยู่บนจอ** | 2 จุดยังมีคำว่า `(W3Q)` (ขั้น 1 + toast) และ `(ยังไม่ post JE — รอ W5)` (ประวัติของ `RTV-2026-0011`) | Iron Rule #81 ห้ามศัพท์ภายใน/รหัสรอบขึ้นจอในของจริง | `07_LOCKED_DECISIONS.md LD-18` |
| `grnBlockReason()` มี 3 สาขา (ร่าง · กลับรายการ · คืนครบแล้ว) | ไม่มีสาขาสำหรับ **"ของถูกใช้ต่อแล้ว"** ที่ระดับใบ → `GRN-2026-0003` (ของถูกจัดเก็บย้ายออก ไม่เคยถูกคืน) แสดงข้อความ **"คืนครบแล้ว"** ซึ่งบอกข้อมูลผิด · และเพราะใบนี้มีบรรทัดเดียว ทั้งใบจึงถูกบล็อกตั้งแต่ขั้นเลือก ทำให้ข้อความระดับบรรทัด `ของถูกใช้ต่อแล้ว — PUT-2026-0044…` ใน `lineBlocked()` **ไม่มีเส้นทางบนจอที่เข้าถึงได้เลย** | `07_LOCKED_DECISIONS.md LD-20` |

**ที่ตั้งใจแก้แล้วในเลนนี้ (ไม่ใช่ drift ที่ยังค้าง — บันทึกไว้กันสับสน):** z-index `--z-dropdown` 40→65 (`LD-16`) และเมนูแถว "ยกเลิกใบ" ที่เคยเรียกฟังก์ชันไม่มีจริง (`LD-17`) — ทั้งสองจุด **แก้ในไฟล์แล้ว** ไม่ใช่ของค้าง

## §14 💡 ข้อเสนอ (ไม่ใช่ AS-BUILT — R1)

- ข้อความ "มีของยังแก้ไม่ครบ" ในขั้น 3 (บรรทัด 1623) สะกด/ประโยคควรตรวจทานอีกครั้งกับ BA ก่อนขึ้นจริง — ดู §10.1 หมายเหตุ
- เมื่อ dev ปิดช่องว่าง #2 (กฎตัวตนผู้อนุมัติ) ควรเพิ่มตัวสลับ "ดูในฐานะ" (view-as) ในต้นแบบ/สภาพแวดล้อม dev เพื่อให้ QA ทดสอบ multi-approver ได้โดยไม่ต้องพึ่งหลายบัญชีจริง — ไม่บังคับ แค่ช่วยการทดสอบ
