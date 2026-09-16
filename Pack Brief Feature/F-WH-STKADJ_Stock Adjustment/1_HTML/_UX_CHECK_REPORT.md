# _UX_CHECK_REPORT — F-WH-STKADJ.html (S3a · qc-ux-html-checker)

วันที่ 2026-09-10 · ไฟล์ `1_HTML/F-WH-STKADJ.html` (226 KB · 3,745 บรรทัด · single-file SPA)
เครื่องมือ: `scripts/static_scan.py` (→ `_static_scan.json`) + `scripts/audit.sh` + Render Gate (Playwright/Chromium 1440 และ 1024)
Sync Read กฎ: `html-generator-v9/knowledge/iron-rules.md` (#1–#103) · `layout-integrity.md` (#50–#69) · `component-contracts.md` (#63–#92) · `page-anatomy.md` (#70–#73) · `microcopy.md`

---

## 1. สรุปผล

| ด่าน | ผล |
|---|---|
| `audit.sh` | **FAIL = 0** · WARN = 3 (ทั้งหมดมาจาก BASE-KIT verbatim — §5) |
| Render Gate 1440 / 1024 | เดินครบทุก flow · **console error จากโค้ด feature = 0** · **pageerror = 0** |
| Pass D — Document Archetype (#98–#101) | ✅ ครบทุกข้อ (§3) |
| Combobox anatomy (#102) | ✅ 23 combobox · anatomy ต่อประเภทตรง contract |
| Lean list / stable screen (#103) | ✅ 8 คอลัมน์ · 1 ข้อมูล = 1 คอลัมน์ · `td_multi_pill = 0` |
| Geometry (#50–#62) | ✅ spacing/type/z-index อยู่ใน scale · PREFLIGHT stamp มีตัวเลข |

**VERDICT: PASS** (ไม่มี BLOCK · WARN ที่เหลืออธิบายครบใน §5)

---

## 2. Iron Rules #1–#49 (สุ่มตรวจพร้อมหลักฐาน)

| # | กฎ | หลักฐาน |
|---|---|---|
| 1–2 | CI token + font | `:root` = Charcoal `#111111` · Primary `#FF3B30` · Teal `#FF9A1F` + alias `--c-blue #0B5CFF` · `--c-green #00A88E` (สองสีที่เหลือของชุด Warm Light) · `'Satoshi','Noto Sans Thai'` |
| 3–4 | Sidebar 232px / Shell-bar 52px ขาว | `--sidebar-w:232px` · `--shell-h:52px` · `.shell-bar{background:#fff}` |
| 5 | Lucide only | `lucide_icon_count = 116` · ไม่มี emoji บนจอ (§5.1) |
| 6–10 | `.ph` + breadcrumb + stats + filter ใน card + table footer | `renderListPage()` ครบทั้ง 5 โซน |
| 11 | drawer width | view `.drawer-panel` 920 · create `.drawer-panel wide` 1290 · modal 440–780 · **ไม่มี 540px** |
| 12/15 | slide 280ms + ปิด 3 ทาง | `.drawer-panel{transition:transform 280ms}` · backdrop click · ปุ่ม X · Esc chain |
| 14 | create/edit = drawer ไม่ใช่ modal | `openCreateDrawer()` → drawer เท่านั้น |
| 16 | ตาราง ≤ 8 คอลัมน์ | list = 8 (เลขที่ · วันที่มีผล · คลัง · ประเภท · สถานะ · ลายเซ็น · มูลค่า · ⋮) |
| 19 | number spinner | มีใน BASE-KIT |
| 21 | icon class | `<i data-lucide>` ทุกตัวใน feature code มี `w-{N} h-{N}` (WARN 3 จุด = BASE-KIT/คอมเมนต์ §5.2) |
| 23 | ไม่มี color emoji บนจอ | emoji 4 ตัวอยู่ใน **คอมเมนต์ CSS/JS ของ BASE-KIT** เท่านั้น |
| 24 | ไม่มี dev-tool / console.log / TODO | `audit.sh` ผ่าน · ใช้ `FWD-WIRE:` แทน `TODO:` (convention เลน) |
| 25 | `renderIcons()` | เรียกทุกจุดหลัง innerHTML · ไม่มี `lucide.createIcons()` ตรง |
| 27–28 | sidebar Module/Feature + slim top bar | `.sb-module[data-module]` + `.sb-features` + `data-feature` ครบ · top bar = breadcrumb + bell + user chip เท่านั้น |
| 29 | render preservation | `render()` ใช้ `preserveRenderState()/restoreRenderState()` · `updateLine()` คืน focus+caret |
| 30 | fluid content | `.content` ไม่มี max-width |
| 31/46 | drawer button contract + placement | create footer = `กลับ(secondary) | ยกเลิก(ghost) → ถัดไป/บันทึกแบบร่าง → primary ขวาสุด` · view footer = `ปิด` secondary เดียว · header actions = link-danger → secondary → primary → divider → copy/printer/download/X · ปุ่มสร้างอยู่ `.ph-actions` ขวาสุด |
| 34/94/102 | search combobox | 23 ตัว (คลัง · ศูนย์ต้นทุน · เหตุผล · สินค้า · ช่องเก็บ · ผู้อนุมัติ) — `<select>` เหลือเฉพาะ enum ≤7 (`select_big = 0`) |
| 35/95 | layout stability + portal | `scrollbar-gutter:stable` · `.combo-pop` portal `position:fixed` `z-index:var(--z-combo)` ไม่ดันเนื้อหา · ตารางอยู่ใน `.table-wrap overflow-x:auto` |
| 36/38 | button symmetry + Thai rhythm | `.btn{padding:2px 16px 0}` จาก kit · ไม่มี `line-height:1`/`overflow:hidden` บนปุ่ม · ปุ่มร่วมแถวใช้ size class เดียว |
| 39 | empty state | 2 เคสแยกกัน — "ยังไม่มีใบปรับยอด" (ปุ่มสร้าง) vs "ไม่พบรายการที่ค้นหา" (ปุ่มล้างตัวกรอง) |
| 40/41/103 | list atomicity + row = view | ทุกคอลัมน์ = 1 ข้อมูล · กดแถวเปิด view · ไม่มีไอคอนดวงตา · `⋮` `stopPropagation()` |
| 42 | sticky header | `.table-wrap thead th{position:sticky;background:#fff}` |
| 43 | validation + format | `markErr()` inline + `.field-error` · `formatMoney/fmi/fdate` ตัวเดียวทั้งไฟล์ · `.num` tabular ทุกช่องเงิน |
| 44 | loading/submitting | `btn-draft` / `btn-submit` / `btn-confirm-submit` / `btn-post` → `disabled` + `loader-2 spin` + "กำลังบันทึก…" + toast หลังปิด |
| 45 | disabled/readonly + form section | `.input:disabled` ตาม token · ช่องเลขที่ disabled |
| 47/47.1 | stepper กลาง | `.stepper > .stepper-item{flex:1 1 0}` + `.stepper-circle` 32px จาก kit — ไม่เขียน CSS stepper เอง |
| 49 | scrollbar 5px | BASE-KIT ครบ (`webkit_scrollbar = true`, `scrollbar_width_px = 5`) |
| 96/97 | list full-height + responsive | `.page-fill` + `.table-wrap` scroll + `.table-foot` ติดล่าง · 1024px: **ไม่มี body horizontal scroll** (วัดจริง = `false` ทั้งหน้า list และ drawer) |

---

## 3. Pass D — Document Archetype (#98–#101)

| ข้อ | ผล | หลักฐาน |
|---|---|---|
| #98 list surface | ✅ | เลขที่ `.tbl-mono` primary sortable · `docPill` · `renderSignProgress` n/N + bar 46px · ยอดชิดขวา sortable · `⋮` |
| #98 create surface | ✅ | `.drawer-panel wide` (1290) · eyebrow + h2 + X · `.stepper` 5 · footer contract |
| #98 view surface | ✅ | eyebrow · code `.tbl-mono` primary · `docPill` · summary line · action group ตามสถานะ + divider + copy/printer/download/X · footer "แก้ไขล่าสุด" + 🔒 ล็อกเมื่อ posted |
| #98 PDF + sign + modals | ✅ | `.a4` + 3 ช่องเซ็น (ผู้จัดทำ · ผู้อนุมัติ · ผู้ผ่านรายการ) · `.tl` timeline + `empChip` · submit modal = `.slot-row` DOA slot picker เลือก**คนจริง** |
| #99 line editor v2 | ✅ | `table.tbl.line-tbl` widths **26/—/64/92/92/78/72/104/54** · `calcLineVat` · `migrateLine` · `totals` · `taxBadgeV` · `renderLineSummary` · `updateLine` focus-preserve · แถวขยาย `.line-expand-panel-anchor` **lean 1 บรรทัด** |
| #100 wizard step contract | ✅ | `เลือกแหล่งที่มา › ข้อมูลหลักใบปรับยอด › รายการสินค้า › เอกสารแนบ › ตรวจสอบและยืนยัน` · ทุก step เปิดด้วย `STEPH()` · step 4 = `.upload-zone` · step 5 = review read-only |
| #101 view tab contract | ✅ | `รายละเอียด › ผลต่อสต๊อก (domain 1 tab) › PDF Preview › ลายเซ็น / อนุมัติ › ประวัติ` · **เอกสารแนบเป็น section ใน "รายละเอียด"** ไม่ใช่ tab แยก |

### 3.1 Override ที่บันทึกไว้ (Iron Rule Overrides Applied)
1. **ชื่อ step ตาม #100 ทับ PREBRIEF §6.2** — PREBRIEF ตั้งชื่อ step 3 = "รายการปรับยอด" · step 1 = "ข้อมูลใบปรับยอด" → ใช้ชื่อล็อกของ Pattern Q แทน · **เนื้อหา business ครบเท่าเดิม**: step 1 กลายเป็นตัวเลือก "ประเภทการปรับ" (คุมกลุ่ม bin ตาม BR-12) · เหตุผลรายบรรทัดย้ายเข้าแถวขยายของ step "รายการสินค้า" · หลักฐานอยู่ step "เอกสารแนบ"
2. **ช่องที่ 7 ของ grid B2 v2 (เดิม "ภาษี") ใช้แสดง "เหตุผล"** — ADJ ไม่ใช่รายการภาษี · ฟังก์ชันยังชื่อ `taxBadgeV()` ตาม contract และ VAT engine (`calcLineVat` 3 โหมด + `VAT_MODES` รวม `รวมแล้ว (NET)`) คงไว้ครบ แต่ `CFG.vatEnabled=false` จึงไม่ surface (B2 §"ตัด optional block")
3. **`--c-teal` ของ fragment doc-archetype ถูก map เป็น `--c-success`** สำหรับสถานะ "อนุมัติแล้ว"/timeline ok — ให้ตรง Status Pill Vocabulary กลาง (อนุมัติแล้ว = เขียว) แทนสีส้มของ token `--c-teal` ในชุด Warm Light

---

## 4. Page Anatomy (#70–#73) + Component Contracts (#63–#68)

- **#70 list anatomy**: page header + จำนวนรวม ✅ · **stat row 4 ใบ คลิกกรองได้จริง** ✅ (ตัวเลขคำนวณจาก mock จริง — รออนุมัติ 2 · มูลค่าเดือนนี้ 5,737.50) · toolbar 1 แถว ✅ · หัวคอลัมน์ sortable + ลูกศรทิศ ✅ · footer pagination + "x – y จาก z" ✅
- **#78.5 นับที่เดียว**: ใช้ **stat row อย่างเดียว ไม่มี chip row ซ้ำ** ✅
- **#71 wizard**: step 5 = summary panel ก่อน submit ✅ · validation inline + toast ✅
- **#72 drawer**: identity header (code + pill + summary line) ✅ · tab มีตัวเลขนับ (`ผลต่อสต๊อก (N)` · `ประวัติ (N)`) ✅ · definition grid `KV()` เป็นกลุ่มมีหัวข้อ ✅ · timeline/audit ✅
- **#73 interaction**: sort จริง · filter จริง · stat คลิกกรอง · ทุก tab มีเนื้อหา (#73.1) ✅
- **#63 density**: `.tbl td padding 8px 12px` · tbody 12.5px ✅
- **#65/#66/#68**: combobox 2 บรรทัด/รายการ · `max-height:320px` + scroll · portal + flip-up ผ่าน `portalMenu` · outside-click ระบบเดียว + `isConnected` guard · Esc chain (combobox → modal → drawer) ✅
- **#67.1 hint opt-in**: ไม่มี `hint-i`/`data-tip` ที่ generator แต่งเอง — คำอธิบายที่มีทั้งหมด trace กลับ PREBRIEF/BR ได้ ✅
- **#81 ไม่มีศัพท์ภายในบนจอ**: ไม่มี edge/rule id · marker `FWD-WIRE:` ปรากฏใน 2 จุดที่เป็นสถานะระบบจริง (การลงบัญชี) — ตั้งใจให้ทีม vibe เห็นว่ายังไม่ต่อ engine

---

## 5. WARN ที่เหลือ + เหตุผล (ไม่บล็อก)

| # | WARN | เหตุผล / การจัดการ |
|---|---|---|
| 5.1 | `audit.sh` Rule #21 — `<i data-lucide>` ไม่มี `w-{N}` 3 จุด | ทั้ง 3 อยู่ใน **BASE-KIT verbatim**: คอมเมนต์อธิบาย Lucide (บรรทัด 1319) · `searchSelectHTML()` (1819) · `emptyStateHTML()` (1932) — แก้ = แตะ BASE-KIT (ชน Rule #69) · `.ss-caret`/`.empty-icon` มีขนาดตายตัวใน CSS อยู่แล้ว |
| 5.2 | Rule #40 — พบ `.uc-email` | เป็น **CSS class ที่มากับ BASE-KIT** ไม่ได้ถูกใช้ในไฟล์นี้เลย (grep ใน markup = 0) |
| 5.3 | Token — hardcoded font-size 1x px | มาจาก BASE-KIT CSS (`.sb-name` ฯลฯ) · ขนาดทั้งหมดอยู่ใน type scale #61 (11/12/12.5/13/14/16/20/26 = 8 ขนาด) |
| 5.4 | emoji 4 ตัว (⚠️ ✅) | อยู่ใน **คอมเมนต์** ของ BASE-KIT CSS/JS เท่านั้น ไม่ขึ้นจอ (Rule #23 คุม UI) |
| 5.5 | Rule #38 Thai rhythm + icon geometry | **NOT-CHECKED (offline)** — sandbox บล็อก CDN ฟอนต์ Satoshi/Noto Sans Thai + Lucide ตอน render (`_RUNNER_BRIEF` ข้อ 12) · ตรวจจากช็อตได้เฉพาะ layout/spacing (ปกติ ไม่ล้น ไม่ทับ) — **ไม่วนแก้** |

---

## 6. Fix loop ที่เกิดจริงในรอบนี้ (3 จุด · จบใน 1 รอบต่อจุด)

| # | อาการ (เจอจาก Render Gate) | สาเหตุราก | แก้ |
|---|---|---|---|
| F1 | `const state` ประกาศซ้ำกับ BASE-KIT → SPA ไม่ทำงานทั้งไฟล์ | feature script ประกาศ `const state` ทับของ kit (lexical global ชนกัน) | เปลี่ยนเป็น `Object.assign(state, {...})` — ต่อยอด state กลาง (Rule #69) |
| F2 | คลิกตัวเลือกใน combobox ที่อยู่ใน drawer ไม่ได้ (โดน `.overlay-wrap` บัง) | `.combo-pop` ใช้ `--z-dropdown (30)` < `--z-drawer (51)` | เพิ่ม `--z-combo: 70` เข้า Z-Index Registry (#62 — แก้ที่ registry ที่เดียว) แล้วอ้าง var |
| F3 | เปิด combobox ตัวที่ 2 แล้วเมนูปิดทันที | outside-click handler ของ combobox ตัวเก่ายังค้าง แล้วไปฆ่า pop ตัวใหม่ (#68.1 สองระบบชนกัน) | ใส่ guard `if (!pop.isConnected) { removeEventListener; return; }` |

---

## 7. Flow ที่เดินจริงครบใน Render Gate

`list (+stat filter, sort, pagination)` → `view drawer 5 tabs` → `submit modal + DOA slot picker (เลือกคนจริง / ปล่อยว่าง = error)` → `approve modal` → `approved (สต๊อกยังไม่ขยับ)` → `post modal (+ตรวจยอดซ้ำ)` → `movements append-only` → `reverse modal → ใบกลับรายการใบใหม่` → `create wizard 5 steps (item combo → bin combo → ยอด → แถวขยายเหตุผล)` → `hard control ยอดติดลบ (ปุ่มส่งอนุมัติ disabled)` → `ค้น bin in-transit = ไม่พบรายการ` → `viewport 1024`

**สกรีนช็อต 30 ไฟล์** ใน `1_HTML/_shots/`
