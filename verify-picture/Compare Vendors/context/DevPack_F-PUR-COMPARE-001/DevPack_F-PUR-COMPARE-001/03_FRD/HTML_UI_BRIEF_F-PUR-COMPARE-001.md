# HTML UI Brief — F-PUR-COMPARE-001 · เทียบราคาผู้ขาย

**source of truth:** `01_HTML/CompareVendors.html` (1,167 บรรทัด · single-file SPA)
**กติกาของเอกสารนี้:** EXTRACTION-BASED — ทุกบรรทัดต้อง trace กลับหา selector / ชื่อฟังก์ชัน / ข้อความจริงในไฟล์ได้ **ห้ามแต่งสเปคเพิ่ม**
**ใช้คู่กับ:** `03_FRD/01_UI.md` (เจตนา) · ไฟล์นี้ (ของจริง)

---

## §1 Design tokens (`:root` — verbatim)

| token | ค่า | ใช้ที่ |
| --- | --- | --- |
| `--c-primary` | `#FF3B30` | แบรนด์ · ปุ่มหลัก · แท็บ active |
| `--c-primary-hover` / `--c-danger` | `#E62E24` | hover · การกระทำอันตราย |
| `--c-primary-08` / `--c-primary-12` | `rgba(255,59,48,.08)` / `.14` | พื้นอ่อน |
| `--c-teal` / `--c-teal-light` / `--c-teal-08` | `#FF9A1F` / `#FFB763` / `rgba(255,154,31,.10)` | เตือน · หมดอายุ |
| `--c-success` | `#1F9D55` | ค่าดีที่สุด · สำเร็จ |
| `--c-warning` | `#E8870F` | กล่องเตือน |
| `--c-ink` / `--c-navy` / `--c-navy-2` | `#111111` | ตัวอักษรหลัก · sidebar |
| `--c-mute` / `-2` / `-3` | `#54565C` / `#73757B` / `#9A9CA2` | ตัวอักษรรอง 3 ระดับ |
| `--c-line` / `-2` / `-3` | `#DEDAD4` / `#E9E5E0` / `#F1EEEA` | เส้น 3 ระดับ |
| `--c-bg-off` | `#FAF8F5` | พื้นหลังหน้า (Ivory) |
| `--fs-h1 … --fs-cap` | `22 · 17 · 15 · 14 · 13 · 12 · 11 px` · `--fs-kpi:28px` | ระดับตัวอักษร |
| `--sp-xs … --sp-xl` | `4 · 8 · 12 · 20 · 28 px` | ระยะห่าง |
| `--r-xs … --r-full` | `4 · 6 · 8 · 12 · 999 px` | มุมโค้ง |
| `--sidebar-w` / `--shell-h` | `232px` / `52px` | โครง shell |

**font stack:** `'Satoshi','Noto Sans Thai',system-ui,-apple-system,sans-serif` · monospace: `ui-monospace,monospace` (`.tbl-mono`)
**ไอคอน:** Lucide เท่านั้น (52 ตัว) · โหลดผ่าน CDN 3 ชั้น + `window.__lucideFailed` · เรียกซ้ำด้วย `renderIcons()`
**scrollbar:** `::-webkit-scrollbar` กว้าง `5px` (Iron Rule #49)

> ⚠️ ไฟล์นี้ **ไม่ได้ใช้ `var(--z-*)`** — ประกาศ z-index เป็นตัวเลขตรง ดู §2

---

## §2 z-index map (ค่าจริงจาก `getComputedStyle`)

| ชั้น | selector | z-index | หมายเหตุ |
| --- | --- | --- | --- |
| toast | `.toast-wrap` | **90** | สูงสุด · มุมขวาล่าง 20px |
| เมนูลอย | `.row-menu` | 80 | *(CSS ค้าง ไม่ได้ใช้ — ดู §8)* |
| combobox | `.combo-pop` | 70 | *(CSS ค้าง ไม่ได้ใช้ — ดู §8)* |
| modal | `.mbd` | **60** | `position:fixed; inset:0; display:grid; place-items:center` |
| drawer | `.drawer-panel` | 51 | *(CSS ค้าง ไม่ได้ใช้)* |
| ฉากหลัง drawer | `.backdrop` | 50 | *(CSS ค้าง ไม่ได้ใช้)* |
| sidebar | `.sidebar` | **20** | `position:fixed; inset:0 auto 0 0` |
| shell-bar | `.shell-bar` | **19** | `position:sticky; top:0` |
| หัวตารางเทียบ | `.mx thead th` | **2** | `position:sticky; top:0` |

**ลำดับที่ยืนยันแล้ว:** toast (90) > modal (60) > sidebar (20) > shell-bar (19) > หัวตาราง (2) ✅
**ตรวจการทับซ้อน:** `.toast` rect เทียบปุ่มทั้ง 5 ใน modal footer → **ไม่ทับ** (`overlapped: []`)

---

## §3 Route map

| route | ที่ไป |
| --- | --- |
| `#/queue` | หน้าเดียวของฟีเจอร์ — คอนโซลทั้งหมด |

**ไม่มี `hashchange` listener** — sidebar ทุกลิงก์ชี้ `#/queue` แล้วเรียก `toast()` บอกว่าอยู่นอกขอบเขต (ดู §7 WARN)
สถานะภายในเก็บใน global ไม่ใช่ใน URL: `SEL` (รอบที่เลือก) · `TAB` (แท็บ) · `QUEUE` (ตัวกรอง) · `AWARD` · `editQuote` · `reasonState` · `modalState`
→ **รีเฟรชแล้วสถานะหาย** · ไม่มี `localStorage` (ยืนยัน: `localStorage_or_session = false`)

---

## §4 สถาปัตยกรรมการ render

**แบบ full re-render — ไม่มี `classList` ไม่มี virtual DOM ไม่มีการต่อชื่อคลาสแบบไดนามิก**

```
render()                     ← เรียกทุกครั้งที่ state เปลี่ยน
 ├─ renderQueue()      L631  ← ใช้ queueRows() L616
 ├─ renderMain()       L935  ← หัวรอบ + แท็บ + body
 │   ├─ renderQuotesTab()  L700
 │   ├─ renderMatrixTab()  L741   ★ แกนหลัก
 │   └─ renderAwardTab()   L828  →  renderAwarded() เมื่อ status='awarded'
 ├─ renderHistory()    L918
 ├─ renderModal()            ← modalState / editQuote / reasonState
 └─ renderIcons()            ← Lucide ซ้ำหลัง render
```

**การรักษา focus ขณะพิมพ์** (สำคัญมากกับสถาปัตยกรรม full re-render):
- `renderKeep()` L676 — เก็บ/คืน `selectionRange` ของช่องค้นหาคิวงาน
- `renderQuoteKeep()` — ใช้ `data-f` ระบุช่องที่กำลังโฟกัสในฟอร์มใบเสนอราคา
- `qf(field,val)` L1076 · `qfl(lineNo,field,val)` L1077 — ตัวเขียนค่าลงฟอร์ม

> **FE ที่จะทำใหม่:** ถ้าย้ายไป React/Vue ให้ใช้ controlled input ปกติ — กลไก `data-f` มีไว้แก้ปัญหาของ full re-render เท่านั้น ไม่ใช่ข้อกำหนดทางธุรกิจ

---

## §5 Anatomy รายส่วน (selector จริง)

### 5.1 Shell
```
.sidebar (232px, #111)
  .sb-brand > .sb-logo + .sb-name        "CUBE 4.0"
  .sb-group                              "จัดซื้อ" · "ข้อมูลหลัก" · "นโยบาย"
  .sb-item (×8, .active = เทียบราคาผู้ขาย)
.shell
  .shell-bar (sticky, 52px) > .crumb + .shell-right > .icon-btn + .emp-chip
  .content
    .ph > .ph-sub + .ph-right
```

### 5.2 คิวงาน
```
.console
  .queue (sticky, 328px)
    .queue-head > .queue-title + .cnt + .input + select ×2 + ปุ่มล้าง
    .queue-body
      .q-item[.on]  →  .q-top > .q-no + .pill
                        .q-meta   หน่วยงาน · N รายการ · ต้องการใช้ …
                        .q-foot > .chip (N ใบเสนอราคา) + .age
      .state / .state.err / .skel          ว่าง · ผิดพลาด · กำลังโหลด
```

### 5.3 พื้นที่หลัก
```
.round-head > .round-title (+ .tbl-mono เลขที่ใบขอซื้อ) + .pill ×2 + .round-actions
.round-sub                    ⚠️ 127 ตัวอักษร (เกิน 120)
.ctabs > .ctab[.on] ×3        ใบเสนอราคา · ตารางเทียบ · ผลการเลือก
```

**แท็บ ① ใบเสนอราคา** — `.qc` (การ์ดต่อผู้ขาย) > `.vend > .vn` + `.pill` + ปุ่มแก้/ลบ · ตารางราคา · แถบยอด (`.val` · `.vat-c` · ยอดสุทธิ)
**แท็บ ② ตารางเทียบ** — `.mx-wrap > table.mx` · `thead th` sticky · `td.best` ไฮไลต์ · `.na` = "ไม่เสนอ" · `tfoot` 6 แถว (`.grand` · `.delta` · `.zero`)
**แท็บ ③ ผลการเลือก** — `.mode-seg > button[.on]` ×2 · `.select` ต่อบรรทัด · `.note-box.warn` (BR-04) · `textarea.input` + `.preset-chips` · ปุ่ม `.btn.btn-primary[disabled]`
**ประวัติ** — `.tl > .tl-i` (`.t` เหตุการณ์ · `.m` ผู้ทำ · `.n` หมายเหตุ)

### 5.4 Overlay
```
.mbd (z-60, grid place-items:center, padding 20px)
  > div  max-width: min(92vw, 1100px)
    .modal-b   overflow-x:hidden   ← กันตารางราคาดันความกว้างจนล้นจอ
.toast-wrap (z-90) > .toast[.ok|.bad]
```

---

## §6 Component states

| component | สถานะที่มี | ตัวกระตุ้น |
| --- | --- | --- |
| `.q-item` | ปกติ · `.on` (เลือกอยู่) · hover | `selectRow()` L681 |
| `.pill` สถานะรอบ | `mute` เปิดรอบ · `info` กำลังเทียบ · success ตัดสินแล้ว · danger ยกเลิก | `R_STATUS` L552 |
| `.ctab` | ปกติ · `.on` | `setTab()` L933 |
| `td` ในตารางเทียบ | ปกติ · `.best` · `.na` ("ไม่เสนอ") | `bestUnit()` · `available` |
| `.qc` การ์ดใบเสนอราคา | ปกติ · ขอบส้มเมื่อหมดอายุ | `isExpired()` L611 |
| ปุ่มยืนยันผล | เปิด · `disabled` | `awardCalc().ok && (!needReason \|\| reason≥3)` L865 |
| ปุ่มแก้/ลบใบเสนอราคา | แสดง · **ไม่ render เลย** เมื่อ `locked` | `r.status==='awarded'\|\|'cancelled'` L940 |

---

## §7 Microcopy verbatim (คัดที่สำคัญ — ใช้เป็น anchor ของ test case)

| จุด | ข้อความ |
| --- | --- |
| ว่าง · ยังไม่เลือกงาน | `เลือกงานจากคิวทางซ้าย` / `เลือกใบขอซื้อที่อนุมัติแล้วเพื่อเปิดรอบเทียบราคา หรือดูรอบที่ทำค้างไว้` |
| ว่าง · คิวว่าง | `ไม่มีงานรอเทียบราคา` / `ใบขอซื้อที่อนุมัติแล้วจะเข้าคิวที่นี่โดยอัตโนมัติ` |
| ว่าง · กรองไม่เจอ | `ไม่พบงานที่ตรงกับเงื่อนไข` / `ลองล้างตัวกรองแล้วดูอีกครั้ง` |
| ผิดพลาด | `โหลดคิวงานไม่สำเร็จ` / `ไม่สามารถติดต่อระบบได้ในขณะนี้` |
| ว่าง · ยังไม่มีใบเสนอราคา | `ยังไม่มีใบเสนอราคา` / `บันทึกราคาที่ได้รับจากผู้ขายอย่างน้อย 1 ราย จึงจะเทียบและตัดสินได้` |
| ว่าง · ยังตัดสินไม่ได้ | `ยังตัดสินไม่ได้` / `ต้องมีใบเสนอราคาอย่างน้อย 1 รายก่อนจึงจะเลือกผู้ชนะได้` |
| ตารางเทียบ (คำโปรย) | `ค่าที่ดีที่สุดของแต่ละแถวถูกไฮไลต์ · ราคาต่อหน่วย (ยอดรวมรายการในวงเล็บ)` |
| **BR-04 · ไม่ใช่ต่ำสุด** | `ต้องระบุเหตุผล` / `ผลที่เลือกไม่ใช่ราคาต่ำสุด — ส่วนต่าง ฿<n> จึงต้องอธิบายเหตุผลให้ตรวจสอบย้อนหลังได้` |
| **BR-04 · รายเดียว** | `มีผู้เสนอราคาเพียงรายเดียว` |
| ก่อนยืนยันผล | `ยืนยันแล้วรอบนี้จะถูกล็อก — ต้องการเปลี่ยนต้องเปิดรอบใหม่` |
| หลังยืนยันผล | `ยืนยันผลการเลือกแล้ว — รอบนี้ถูกล็อก` · `ข้อมูลถูกล็อก แก้ไม่ได้` |
| ลบใบเสนอราคา | `ใบเสนอราคาของ <ผู้ขาย> จะถูกลบออกจากรอบนี้ การกระทำนี้ย้อนกลับไม่ได้ (การลบจะถูกบันทึกในประวัติ)` |
| ยกเลิกรอบ | `การยกเลิกย้อนกลับไม่ได้ — ใบขอซื้อจะกลับเข้าคิวให้เปิดรอบใหม่ และเหตุผลจะถูกบันทึกถาวรในประวัติ` |
| เปิดรอบใหม่ | `รอบเดิมจะยังอ่านได้และตรวจย้อนหลังได้ · รอบใหม่จะคัดลอกใบเสนอราคาเดิมมาเป็นค่าตั้งต้นให้แก้ต่อ` |
| ประวัติ (หัวข้อ) | `ประวัติ (บันทึกเพิ่มอย่างเดียว · แก้ไข/ลบไม่ได้)` |
| เลือกผู้ขาย (โหมดทั้งใบ) | `เลือกได้เฉพาะรายที่เสนอครบทุกรายการ` · `(ไม่ครบทุกรายการ)` |
| หมดอายุ | `หมดอายุแล้ว` · `ใบเสนอราคาหมดอายุเมื่อ <วันที่> — ยืนยันผลได้ แต่ควรขอราคายืนยันจากผู้ขายอีกครั้ง` |
| ผู้เสนอรายเดียว (คำแนะนำ) | `ควรขอราคาเพิ่มอย่างน้อย 2 ราย — หากยืนยันผลด้วยรายเดียว ระบบจะบังคับให้ระบุเหตุผล` |
| จุดเชื่อม PO | `ปุ่มออกใบสั่งซื้อเป็นจุดเชื่อมไปยังฟีเจอร์ปลายทาง — ยังไม่เปิดใช้งานในรอบนี้` |
| preset เหตุผลเลือก | `ส่งมอบเร็วกว่า` · `คุณภาพ/สเปกตรงกว่า` · `เงื่อนไขชำระเงินดีกว่า` · `มีการรับประกันครอบคลุมกว่า` |
| preset เหตุผลยกเลิก | `ใบขอซื้อถูกยกเลิก` · `ราคาที่ได้ยังไม่เหมาะสม ขอเทียบใหม่` · `ผู้ขายถอนข้อเสนอ` · `เปลี่ยนสเปกสินค้า` |

### ⚠️ ข้อความที่ **ต้องเปลี่ยนก่อนต่อระบบจริง** (Iron Rule #81 · LD-12)

| ที่ | ปัจจุบัน | ปัญหา |
| --- | --- | --- |
| chip ใต้หัวข้อหน้า | `คอนโซลปฏิบัติงาน — ไม่ใช่เอกสารธุรกรรม` | ศัพท์ archetype ของทีมสร้าง |
| **ปุ่มออกใบสั่งซื้อ** | `ใบสั่งซื้อ (W3) — อยู่นอกขอบเขตรอบนี้` | รหัส wave + คำว่า "รอบ" ชนกับ *รอบเทียบราคา* |
| toast เมนูข้าง ×7 | `… — soft-reference` · `chip = csq เท่านั้น` · `F007/F009/F012/F019` · `อยู่นอกขอบเขต feature นี้ (W3)` · `คนละไฟล์ต้นแบบ` | ศัพท์ภายในทั้งหมด |
| ปุ่มมุมขวาบนคิวงาน | `สาธิตสถานะโหลดผิดพลาด` | ของทดสอบ · ถอดก่อน production (LD-11) |

---

## §8 CSS ที่ **มีแต่ไม่ได้ใช้** (50 คลาส — ห้ามหยิบไปใช้ · LD-01)

ตรวจแล้วเชื่อถือได้ (ไฟล์ไม่มี `classList.*` และไม่มีการต่อชื่อคลาสแบบไดนามิก):

```
แบบพิมพ์/ลายเซ็น : a4  pdf-stage  pdf-tool  sig  sign-bar  sign-prog
line editor v2   : line-tbl  line-wrap  free-row  slot-row  sum-tbl  tbl-foot
                   line-collapse-panel  line-expand-panel-anchor  line-expand-panel-inner
drawer เอกสาร     : drawer-panel  backdrop  wide  dw-head  dw-body  dw-title  dw-sum
                   dw-actions  dw-foot-note
combobox/อัปโหลด  : combo-pop  combo-opt  combo-empty  item-combo  upload-zone  file-card  row-menu
เบ็ดเตล็ด         : btn-success  hard-warn  divider-s  divider-v  eyebrow  expanded  sortable
                   section-row  secwrap  sep  kbd  top-icon-btn  hd  pg  pgl  sn  sz  c3  c4
```

> **คำเตือนถึง FE:** คลาสกลุ่มบนคือแผงหน้าของ **Pattern Q (เอกสารธุรกรรม)** ที่ติดมากับชุดสไตล์ — **LD-01 ห้ามใช้ในฟีเจอร์นี้**
> ควรลบทิ้งตอนย้ายเข้าโปรเจกต์จริง (TD-03) · เป็นเหตุให้เครื่องตรวจรายงาน `is_document=true` ผิด

---

## §9 Traceability 3 ทาง

| Brief §  | ↔ FRD | ↔ HTML |
| --- | --- | --- |
| §1 tokens | `01_UI §1` | `:root` 40 ตัว |
| §2 z-index | `01_UI §4` | 9 จุด · ยืนยันด้วย `getComputedStyle` |
| §4 render | `03_LOGIC §1–4` | `render()` chain |
| §5.3 ตารางเทียบ | `01_UI §3.4` · `02_API §4` | `renderMatrixTab()` L741 |
| §5.3 ผลการเลือก | `01_UI §3.5` · `03_LOGIC §4` · `05_RULES` BR-04 | `awardCalc()` L808 · `renderAwardTab()` L828 |
| §7 microcopy | `06_TESTS` (anchor ของทุกเคส) | ข้อความจริงในไฟล์ |
| §8 dead CSS | `07_LOCKED` TD-03 | `<style>` 4 บล็อก |

## §10 Drift log

| # | ต่างจาก FRD/BRD ตรงไหน | ท่าที |
| --- | --- | --- |
| D-1 | BRD §4 มีเมทริกซ์สิทธิ์ 4 บทบาท — **HTML ไม่มีเลย** | ทำใน Phase B ตาม C-09 (TD-01) |
| D-2 | BRD §10 บอก SC-15 "มีจุดเชื่อมในโค้ด" — จริง ๆ มีแค่ `const prCancelled=false` ที่ไม่มีใครอ่าน | ทำใน Phase B (TD-02) |
| D-3 | `01_UI §6` ระบุรองรับ 768 — **จริงมี h-scroll ที่ 768** | แก้ sidebar เป็น rail/off-canvas (TD-04) |
| D-4 | ไฟล์แนบใน BRD §6.3 เป็นฟิลด์จริง — HTML เป็น mock | ต่อ `02_API §5` (TD-05) |
