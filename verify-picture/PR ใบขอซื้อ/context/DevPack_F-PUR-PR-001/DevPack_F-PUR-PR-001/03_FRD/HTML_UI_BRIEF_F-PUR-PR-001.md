# HTML_UI_BRIEF — F-PUR-PR · PR ใบขอซื้อ

> **EXTRACTION-BASED** — ทุกบรรทัดในไฟล์นี้ trace กลับหา selector / ฟังก์ชัน / ข้อความจริงใน
> `01_HTML/F-PUR-PR.html` ได้ · **ไม่มีบรรทัดไหนที่แต่งสเปคขึ้นเอง**
> source of truth = HTML · คู่กับ `01_UI.md` (Layout Decision Log) · CI/iron rules อ้างสดจาก `html-generator-v9`

## §1 Design Tokens (verbatim จาก `:root`)

### สี
| token | ค่า | ใช้ที่ |
|---|---|---|
| `--c-primary` | `#FF3B30` | CTA หลัก · ยอดสุทธิ · stepper active |
| `--c-primary-hover` | `#E62E24` | hover ของ CTA |
| `--c-teal` | `#FF9A1F` | accent (orange) |
| `--c-teal-light` | `#FFB763` | accent อ่อน |
| `--c-navy` / `--c-navy-2` | `#111111` | sidebar **flat ไม่ gradient** |
| `--c-ink` | `#111111` | ตัวอักษรหลัก |
| `--c-mute` / `-2` / `-3` | `#54565C` / `#73757B` / `#9A9CA2` | ตัวอักษรรอง 3 ระดับ |
| `--c-line` / `-2` / `-3` | `#DEDAD4` / `#E9E5E0` / `#F1EEEA` | เส้นขอบ 3 ระดับ |
| `--c-bg-off` | `#FAF8F5` | พื้นหลัง Ivory |
| `--c-success` | `#1F9D55` | สถานะอนุมัติแล้ว |
| `--c-warning` | `#E8870F` | แถบเตือนงบ |
| `--c-danger` | `#E62E24` | ไม่อนุมัติ · ยกเลิก |
| `--c-primary-08` / `-12` | `rgba(255,59,48,.08)` / `.14` | พื้นอ่อนของ primary |
| `--c-teal-08` | `rgba(255,154,31,.10)` | พื้นอ่อนของ accent |

### ขนาดและระยะ
| token | ค่า |
|---|---|
| `--sidebar-w` | `232px` |
| `--shell-h` | `52px` |
| `--fs-h1` … `--fs-cap` | `22 / 17 / 15 / 14 / 13 / 12 / 11 px` (h1·h2·h3·body·sub·meta·cap) · `--fs-kpi` `28px` |
| `--sp-xs` … `--sp-xl` | `4 / 8 / 12 / 20 / 28 px` |
| `--r-xs` … `--r-full` | `4 / 6 / 8 / 12 / 999 px` |

### Typography
`'Satoshi','Noto Sans Thai',system-ui,-apple-system,sans-serif` · mono = `ui-monospace,monospace`
โหลดจาก fontshare + `fonts.googleapis.com` (Noto Sans Thai 400–800)

### Icon
**Lucide เท่านั้น** — `data-lucide` **95 จุด** · class `.lu` · เรียกผ่าน `renderIcons()` · **ไม่มี emoji สี** (พบเฉพาะ `★` 1 ตัวในข้อความ)

## §2 Z-index Map (ค่าจริง + ยืนยันด้วย `getComputedStyle`)

| ชั้น | selector | z-index | ยืนยันบนจอ |
|---|---|---|---|
| sticky header ของตาราง | `thead th` | 19 / 20 | — |
| backdrop | `.backdrop` | **50** | ✅ `50` |
| drawer | `.drawer-panel` | **51** | ✅ `51` |
| modal | `.modal` | 60 | — |
| combobox popup | `.combo-pop` | 70 | — |
| (สำรอง) | — | 80 | — |
| toast | `.toast-wrap` | **90** | ✅ `90` |

> **ไฟล์นี้ไม่ใช้ `var(--z-*)`** — ประกาศเลขตรง (`grep -cE '\-\-z-[a-z]+\s*:'` = 0 และการใช้ = 0)
> จึง **ไม่ติดบั๊ก `z-index:auto`** ที่เคยพบใน F-SEC-TRANS / F-SEC-LOCKOUT · ดู `07_LOCKED` D-03

## §3 Route Map

| route | ฟังก์ชันที่ render | หมายเหตุ |
|---|---|---|
| `#/list` | `renderList()` · `goList()` | หน้าเริ่มต้น |
| `#/create` | `renderCreateDrawer()` · `goCreate()` | wizard 5 ขั้น |
| `#/edit/:id` | `renderCreateDrawer()` · `goEdit()` | **guard:** ใบที่ไม่ใช่ร่าง → เด้งกลับ `#/view/:id` |
| `#/view/:id` | `renderViewDrawer()` · `goView()` | drawer 4 แท็บ |

listener: `hashchange` · ปิด drawer = `closeDrawer()` (ล้าง `createWizard` + `VIEW.open` แล้ว `goList()`)

## §4 Anatomy รายหน้า

### 4.1 Shell (ทุกหน้า)
```
.shell
├── .sidebar (232px · พื้น #111 flat)
│   ├── .sb-brand > .sb-logo + .sb-name       "CUBE 4.0"
│   └── .sb-group × 3 > .sb-item              จัดซื้อ / ข้อมูลหลัก / นโยบาย
│                                              active = ใบขอซื้อ (PR)
└── .content
    ├── .shell-bar (52px · พื้นขาว) > .crumb + .shell-right > .icon-btn × n
    └── (page body)
```

### 4.2 P-01 · หน้ารายการ — `renderList()`
```
.pg
├── .ph > .eyebrow + h1 + .ph-sub · .ph-right > .btn.btn-primary "สร้างใบขอซื้อ"
├── .card (ตัวกรอง) > .field × 4 + ปุ่มล้างตัวกรอง (resetF)
├── .card > table.tbl
│   ├── thead > th × 10   (มี .sortable 4 ช่อง + sortIc())
│   └── tbody > tr        (คลิกทั้งแถว → goView)
│       └── td: .emp-chip · .pill (docPill) · .sign-prog (renderSignProgress) · .tabular
├── .state / .state.err / .skel        empty · error · loading
└── .card "เอกสารแนบล่าสุด" > .file-card × n     ← Pattern Q #98 (รวมไฟล์ข้ามใบ)
```
**คอลัมน์:** `เลขที่` · `วันที่เอกสาร` · `ผู้ขอซื้อ` · `หน่วยงาน` · `ต้องการใช้` · `สถานะ` · `ประเภท` · `ลายเซ็น` · `ยอดสุทธิ` · (actions 40px)

### 4.3 P-02 · Wizard — `renderCreateDrawer()`
```
.backdrop (z50)
.drawer-panel.wide.on (1290px · z51)
├── .dw-head > .dw-title + ปุ่มปิด
├── .stepper > .step-i × 5 (+ .step-line × 4)      stepItem()
│   └── .no + .tx     .done คลิกย้อนได้ · .active/อนาคต คลิกไม่ได้
├── .dw-body
│   ├── .steph > .ic + h3 + .hint                  หัวขั้น (STEPH)
│   └── (เนื้อหาตามขั้น)
└── .dw-foot > "ย้อนกลับ" · "ยกเลิก" · "ถัดไป"
```

| ขั้น | เนื้อหา (selector หลัก) |
|---|---|
| 1 เลือกแหล่งที่มา | `.tile-row > .tile × 2` (สร้างใหม่ / จากใบขอซื้อเดิม) |
| 2 ข้อมูลหลักใบขอซื้อ | `.form-grid` 2 คอลัมน์ · `.field > .lbl + input/.select` · `.req` · `.field-help` · `.err` เมื่อ `markErr()` |
| 3 **รายการสินค้า** | `.line-wrap > table.line-tbl` (ดู §4.4) |
| 4 เอกสารแนบ | `.upload-zone` · `.file-card × n` |
| 5 ตรวจสอบและยืนยัน | `.card` สรุป read-only · `.hard-warn` (งบ) · `.slot-row × n` (สายอนุมัติ) |

### 4.4 P-02.3 · B2 v2 Line Editor
```
.line-wrap
└── table.line-tbl (font-size 12.5px)
    ├── thead th × 9   width 26 / auto / 64 / 92 / 92 / 78 / 72 / 104 / 54
    └── tbody
        ├── tr (แถวปกติ)
        │   └── .item-combo > input + .combo-pop > .combo-opt / .combo-empty
        │       (.hi = ไฮไลต์ · <mark> ตรงคำค้น)
        ├── tr.expanded + .line-expand-panel-anchor > .line-expand-panel-inner
        │   └── .seg (VAT segmented 3 โหมด) · .vat-c · หมายเหตุ · ศูนย์ต้นทุนรายบรรทัด
        └── tr.free-row  (ของแถม — แก้/ลบไม่ได้)
.section-row  ส่วนลดท้ายบิล   > .toggle > .toggle-slider + .seg
.section-row  หักภาษี ณ ที่จ่าย > .toggle
#line-summary-wrap > .sum-tbl > .tot (+ .grand = ยอดสุทธิ 16px/700 primary)
```
**ลำดับ totals (ล็อก):** `ราคาก่อน VAT` → `ภาษีมูลค่าเพิ่ม (VAT)` *(ม่วง)* → `ยอดรวมหลัง VAT` → `ส่วนลดท้ายบิล` → **`ยอดสุทธิทั้งหมด`** → บรรทัดธุรกิจ
ฟังก์ชัน: `addLine()` · `removeLine()` · `applyItemToLine()` · `useFreeText()` · `setLineUnit()` · `renderLineExpand()` · `renderLineSummary()` · `taxBadgeV()`

### 4.5 P-03 · View drawer — `renderViewDrawer()`
```
.drawer-panel.on (920px · z51)
├── .dw-head > .dw-title + .pill (สถานะ) + .top-icon-btn × n (copy/print/download/X)
├── .tabs > .tab × 4          setTab('detail'|'pdf'|'sign'|'history')
├── .dw-body
│   ├── detail  : .sec × n (KV · ตารางอ่านอย่างเดียว · .dw-sum · เอกสารแนบ · การส่งต่อเอกสาร)
│   ├── pdf     : .pdf-tool + .pdf-stage > .a4 (max 720) · .sig × n · bahtText()
│   ├── sign    : .sec > การ์ดต่อ slot (.emp-chip + สถานะ + วันเวลา + เหตุผล)
│   └── history : .tl > .tl-i × n   (append-only)
└── .dw-actions  ปุ่มตามสถานะ (canActStep)
```

### 4.6 Overlays
| overlay | selector | ฟังก์ชัน |
|---|---|---|
| ส่งอนุมัติ | `.modal > .modal-h/.modal-b/.modal-f` + `.slot-row` | `renderSubmitModal()` |
| เหตุผล | `.modal` + `.preset-chips` | `renderReasonModal()` |
| ยืนยัน | `.modal` (440px) | `renderModal()` |
| toast | `.toast-wrap > .toast` (+ `.bad`) | `toast()` |

## §5 Component States

| component | states |
|---|---|
| `.btn` | `.btn-primary` · `.btn-secondary` · `.btn-ghost` · `.btn-link` · `.btn-success` · `.sm` · `:disabled` |
| `.pill` | `.ok` · `.warn` · `.bad` · `.info` · `.teal` · `.mute` (+ `.dot`) |
| `.step-i` | `.done` (คลิกได้) · `.active` · ปกติ (คลิกไม่ได้) |
| `.field` | ปกติ · `.err` (จาก `markErr()`) · `.req` (มีดอกจัน) · `.field-help` |
| `.tab` | ปกติ · `.active` |
| `.state` | empty · `.err` (error + ปุ่มลองใหม่) · `.skel` (loading) |
| `.toggle` | เปิด/ปิด (`.toggle-slider`) |
| `.tile` | ปกติ · `.active` |
| `.line-tbl tr` | ปกติ · `.expanded` · `.free-row` (แก้/ลบไม่ได้) |

## §6 Overlay Registry + Dismiss Rules

| overlay | z | Esc ปิดได้ | คลิก backdrop | หมายเหตุ |
|---|---|:--:|:--:|---|
| `.combo-pop` | 70 | ✓ | ✓ | `scheduleCloseCombo()` + `focusCombo()` กัน focus หลุด |
| submit modal | 60 | ✓ | ✓ | ปุ่มส่งถูกปิดจนเลือกครบทุกขั้น |
| reason modal (reject) | 60 | **✗** | ✗ | **บังคับตัดสินใจ** — ปิดไม่ได้ |
| reason modal (cancel) | 60 | ✓ | ✓ | |
| confirm modal | 60 | ✓ | ✓ | 440px |
| wizard drawer | 51 | ✓ | ✓ | `tryCloseWizard()` → ถาม destructive confirm ถ้ามีข้อมูลค้าง |
| view drawer | 51 | ✓ | ✓ | `closeDrawer()` |

**Esc chain (ในลำดับนี้):** combobox → submit modal → reason modal → confirm modal → wizard → view drawer

## §7 BACKEND anchors ↔ FRD API

| จุดบนจอ (ฟังก์ชัน) | FRD API | FRD Function |
|---|---|---|
| `renderList()` + `LIST.*` filters | API-01 | FN-01 |
| `goView()` → `renderViewDrawer()` | API-02 | FN-02 · FN-11 |
| `saveDraft()` (ใบใหม่) | API-03 | FN-03 |
| `saveDraft()` (ใบเดิม) | API-04 | FN-06 |
| `doSubmit()` + `nextDocNo()` | **API-05** | FN-08 |
| `doApprove()` | API-06 | FN-09 |
| `openReasonModal('reject')` | API-07 | FN-13 |
| `doRecall()` | API-08 | FN-10 |
| `openReasonModal('cancel')` | API-09 | FN-14 |
| `duplicateDoc()` | API-10 | FN-12 |
| `mockUpload()` / `mockUploadBad()` | API-11 | FN-15 |
| `budgetCheckMock()` | — (mock · XT-03) | FN-07 |
| `resolveDoa()` + `MOCK_DOA_TIERS` | — (ENG-DOA-RESOLVE) | — |

> **ทุก `MOCK_*` บนจอต้องถูกแทนด้วยบริการจริงตอนต่อระบบ:**
> `MOCK_ITEMS` `MOCK_VENDORS` `MOCK_CC` `MOCK_DEPT` `MOCK_EMP` (ทะเบียนข้อมูลหลัก · soft-ref) ·
> `MOCK_DOA_TIERS` + `SLOT_CANDIDATES` (ทะเบียน DOA) · `MOCK_BUDGET` (F117 · W7) · `MOCK_FILES` (อัปโหลดจริง)

## §8 Microcopy verbatim

ดู `01_UI.md §1.6` — ตารางข้อความจริงบนจอครบทุกบริบท (ใช้เป็น expected text ของ `06_TESTS`)

## §9 Traceability 3 ทาง

| ทิศ | สถานะ |
|---|---|
| **Brief → HTML** | ทุก selector ในไฟล์นี้มีจริงในไฟล์ HTML (ตรวจด้วย `querySelectorAll` ตอน re-gate) ✅ |
| **HTML → FRD** | ทุกหน้า/route/pattern มีแถวใน `01_UI §1.0` ✅ · ทุก action มี API ใน §7 ✅ |
| **FRD → Brief** | `01_UI` อ้าง selector ชุดเดียวกับไฟล์นี้ ✅ |

## §10 Drift Log

| # | สิ่งที่ต่าง | สถานะ |
|---|---|---|
| **DR-01** | wizard ขั้น 3 เคยชื่อ `รายการที่ขอซื้อ` ต่างจาก iron rule #100 (`รายการสินค้า`) และต่างจาก BRD §14.6 | **แก้แล้วที่ขั้น 7R** → `07_LOCKED` LD-08 |
| **DR-02** | ศัพท์ภายในรั่วขึ้นจอ 14 จุด (`ENG-NOTIFY` · `mock` · `soft-reference` · รหัสฟีเจอร์ ฯลฯ) | **แก้แล้วที่ขั้น 7R** → `07_LOCKED` LD-09 |
| **DR-03** | SC-06 ใน PREBRIEF บรรยายพฤติกรรมที่ระบบไม่ได้ทำ (เตือนเมื่อเกินวงเงินของขั้นที่เลือก) | **ยังไม่แก้** — เปิด **OQ-07** ให้ BA แก้ถ้อยคำ → `07_LOCKED` LD-10 |
| **DR-04** | CSS `.line-collapse-panel` (+ keyframes `line-collapse-slide`) **ไม่ถูกใช้ในมาร์กอัปหรือ JS เลย** — animation ตอนยุบแถวไม่ได้ถูกต่อ | **WARN** — ไม่กระทบการใช้งาน (การยุบแถวทำงานปกติ ไม่มี animation) · ให้ dev ตัดสินว่าจะต่อ animation หรือลบ CSS ทิ้ง |
| **DR-05** | ปุ่มสาธิต 2 ปุ่มยังอยู่บนจอ | **ตั้งใจเก็บไว้ให้ QA** → ต้องถอดก่อน production · `07_LOCKED` LD-11 · **OQ-09** |

> วิธีตรวจ DR-04: ถอด `<style>` ออกแล้วเทียบชื่อคลาสกับมาร์กอัป+JS · เชื่อถือได้เพราะไฟล์นี้ **ไม่มี `classList.*` เลย (0 จุด)** และไม่มีการต่อชื่อคลาสแบบ `'x-'+v` (3 จุดที่เจอเป็นการสร้าง id/ข้อความ ไม่ใช่คลาส)
