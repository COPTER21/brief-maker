# _UX_CHECK_REPORT — F-WH-STKTRF · Stock Transfer

> Stage **S3a** · `qc-ux-html-checker` (Sync Read iron rules #1–#103 จาก `html-generator-v9`) · 2026-09-10
> ไฟล์ที่ตรวจ: `1_HTML/F-WH-STKTRF.html` (2,290 บรรทัด · 205 KB · single-file SPA)
> เครื่องมือ: `scripts/static_scan.py` + `html-generator-v9/scripts/audit.sh` + `self_audit.py` + Render Gate (Chromium 1440 / 1024)

---

## VERDICT: **PASS** (BLOCK = 0 · FAIL = 0)

| ด่าน | ผล |
|---|---|
| `audit.sh` (hard gate ของเลน) | **FAIL = 0** · WARN = 1 |
| `node --check` (JS syntax) | **ผ่าน** |
| Render Gate 1440px / 1024px | **ผ่าน** · console error (นอกเหนือ CDN offline) = **0** · body h-scroll ที่ 1024 = **false** |
| Pass D — Document Archetype (#98–#101) | **ครบทุกข้อ** |
| #102 combobox anatomy · #103 lean list | **ผ่าน** |

---

## 1. Pass A — CI / Brand (#1–#5)

| # | ตรวจ | ผล | หลักฐาน |
|---|---|---|---|
| #1 | CI CUBE Warm Light tokens | ✅ | `:root` มี Ivory `#FAF8F5` · Charcoal `#111111` · Red `#FF3B30` · Orange `#FF9A1F` · Teal `#00A88E` ครบ |
| #2 | Satoshi + Noto Sans Thai | ✅ | `font-family:'Satoshi','Noto Sans Thai',system-ui` · โหลดจาก Google Fonts + Fontshare |
| #3 | Sidebar 232px charcoal flat | ✅ | `--sidebar-w:232px` · `background:#111111` (ไม่มี gradient) |
| #4 | Shell bar 52px ขาว | ✅ | `--shell-h:52px` · `.shell-bar{background:#fff}` · ไม่มี title ซ้ำใน shell bar |
| #5 | Lucide เท่านั้น · ไม่มี color emoji | ✅ | `lucide_icon_count = 142` · `fontawesome=false` · emoji scan = 0 (ลบ `★` ในคอมเมนต์ออกแล้ว) |

## 2. Pass B — Layout / Component (#6–#49)

| # | ตรวจ | ผล | หลักฐาน / การแก้ |
|---|---|---|---|
| #6 | `.ph` + h1 + sub + actions | ✅ | `renderList()` — ปุ่มสร้างอยู่ `.ph-actions` ขวาสุด |
| #7 | Breadcrumb ใน shell bar + `chevron-right` | ✅ | `คลังสินค้า › ย้ายสินค้า` · ไม่มี `›` เป็นตัวอักษร |
| #8 | KPI ≤6 การ์ด | ✅ | 4 การ์ด (`statCard`) · คลิกแล้ว filter จริง |
| #9 | Filter bar อยู่ใน card | ✅ | `.filter-bar` อยู่ใน `.card.list-card` |
| #10 | Table footer = count + pagination | ✅ | `renderFootHtml()` |
| #11 | Drawer width | ✅ | view `.drawer-panel` 920 · create `.drawer-panel.wide` **1290** (ข้อยกเว้นเดียวของ B2) · **ไม่มี 540px** |
| #12 | Slide 280ms + backdrop `rgba(17,17,17,.40)` | ✅ | `.drawer-panel{transition:transform 280ms cubic-bezier(.4,0,.2,1)}` |
| #14 | Create/Edit = drawer ไม่ใช่ modal | ✅ | `openCreateDrawer()` |
| #15 | ปิดได้ 3 ทาง | ✅ | backdrop click · ปุ่ม X · Esc (มี Esc chain: combo → row-menu → modal → drawer) |
| #16 | คอลัมน์ list | 🟡 **9 คอลัมน์ + ⋮** | เกิน 8 โดยเจตนา — Pattern Q กำหนดชุดคอลัมน์ของเอกสารไว้เอง (เลขที่/วันที่/ต้นทาง/ปลายทาง/โหมด/สถานะ/ระหว่างทาง/ลายเซ็น/มูลค่า) · **#103 บังคับให้แต่ละแกนแยกคอลัมน์ ห้ามยุบรวม** → รับเป็น rare exception ตาม #16 |
| #18 | โครง field (label/input/help/error) | ✅ | `.field > .lbl + .input + .field-help + .field-error` |
| #19 | ซ่อน spinner number input | ✅ | มีใน BASE-KIT |
| #21 | ทุก `<i data-lucide>` มี `w-N h-N` | ✅ | แก้ไอคอน empty state ที่ขาดแล้ว → audit ไม่พบเหลือ |
| #23 | ไม่มี color emoji | ✅ | แก้ `★` ในคอมเมนต์ → 0 |
| #24 | ไม่มี dev bar / console.log / **TODO** | ✅ | `audit.sh` ผ่าน · ใช้ marker **`FWD-WIRE:`** แทน TODO ตาม convention เลน (`_RUNNER_BRIEF §2.11`) — พบ 27 จุด |
| #25 | `renderIcons()` ไม่เรียก `lucide.createIcons()` ตรง | ✅ | helper เดียว `renderIcons()` ที่ห่อ `window.lucide.createIcons()` |
| #27 | Sidebar `.sb-module` + `data-module`/`data-feature` | ✅ | 2 module (จัดซื้อ · คลังสินค้า) · header เป็น `<button onclick="toggleModule(this)">` · ไม่มี `sb-section` |
| #28 | Slim top bar | ✅ | Breadcrumb + Notification + User chip เท่านั้น |
| #29 | Render preservation | ✅ | `preserveRenderState()/restoreRenderState()` ใน `render()` + `updateLine()` คืน focus/caret เอง |
| #30 | `.content` ไม่มี max-width | ✅ | `audit.sh` ตรวจแล้วผ่าน |
| #31 | Drawer button contract | ✅ | create footer: `ย้อนกลับ`(secondary ซ้าย) → `ยกเลิก`(ghost) → primary ขวาสุด · view footer มีแค่ `ปิด` (secondary) · header actions เรียง secondary→primary→danger→divider→X |
| #34/#94 | Search-select แทน `<select>` ยาว | ✅ | 18 combobox (สินค้า · bin ต้นทาง/ปลายทาง/ที่ลงจริง · ผู้อนุมัติ) · `<select>` ที่เหลือเป็น enum สั้น (≤7) ทั้งหมด — `select_big = 0` |
| #35 | Layout stability | ✅ | `scrollbar-gutter:stable` · `.combo-pop{position:fixed}` (ลอยทับ ไม่ดันเนื้อหา) · `.line-wrap{overflow-x:auto}` |
| #36 | Button symmetry + Thai optical center | ✅ | `.btn{padding:2px 16px 0; white-space:nowrap; justify-content:center}` · **ไม่มี `line-height:1` / `overflow:hidden` บนปุ่ม** |
| #38 | Thai vertical rhythm | ✅ (ค่า) / 🟡 (ตรวจตา) | `.btn 2px…0` · `.pill 3px 9px 2px` · `.table td 13px 14px 11px` — ตรงชุดค่าที่ verify แล้ว · **การเทียบเส้นกึ่งกลางด้วยฟอนต์ไทยจริง = NOT-CHECKED (offline)** ดู §5 |
| #39 | Empty state | ✅ | 2 เคสแยกกัน: "ยังไม่มีใบย้ายสินค้า" (ปุ่มสร้าง) vs "ไม่พบรายการที่ค้นหา" (ปุ่มล้างตัวกรอง) |
| #40/#103 | 1 ข้อมูล = 1 คอลัมน์ | ✅ | `td_multi_pill = 0` · สถานะเอกสาร / ระหว่างทาง / ลายเซ็น แยกคอลัมน์ · บรรทัดรองมีเฉพาะ meta ของค่าเดียวกัน (รหัสสินค้าใต้ชื่อสินค้า) |
| #41 | คลิกแถว = เปิด view · ไม่มี eye | ✅ | `<tr class="is-clickable" onclick="navigate('view/…')">` · `data-lucide="eye"` = 0 |
| #42 | Sticky header + Thai-safe truncate | ✅ | `.table-wrap thead th{position:sticky;top:0;background:var(--c-bg-off);z-index:3}` (พื้นทึบที่ `th` จริง) + `.cell-truncate` + `title` |
| #43 | tabular-nums + format กลาง | ✅ | `.num/.tbl-num` · `formatMoney/fdate/fdt` ตัวเดียวทั้งไฟล์ · **ปี ค.ศ. ล้วน** (`fdate` ใช้ `getFullYear()`) |
| #44 | Loading/submitting | ✅ | `confirmSubmit / confirmApprove / confirmReceive / confirmShortage` → disabled + `loader-2 spin` + "กำลังบันทึก…/กำลังอนุมัติ…" + toast หลังปิด |
| #45 | Disabled/read-only + form section | ✅ | `.input:disabled` style ตาม token · ช่องต้นทุน/ส่วนลด/เลขที่ = readonly พร้อม `field-help` อธิบาย |
| #46 | Placement contract | ✅ | ปุ่มสร้าง `.ph-actions` ขวาสุด · drawer primary ล่างขวา · pill เดียวระดับ header · ทุก destructive ผ่าน confirm |
| #47/#47.1 | Stepper กลาง geometry | ✅ | `.stepper-item{flex:1 1 0}` · connector `top:15px` (กึ่งกลาง dot 32px) · dot ขนาดเดียวทุก state · CSS ลอกจาก `doc-archetype.css` |
| #49 | Minimal scrollbar 5px | ✅ | `::-webkit-scrollbar{width:5px}` + `scrollbar-width:thin` + track โปร่งใส |
| #95 | Overlay portal | ✅ | `.combo-pop` เป็น `position:fixed` คำนวณจาก `getBoundingClientRect()` + flip-up เมื่อชนขอบล่าง · `#row-menu` ใช้ `.menu-fixed` |
| #96 | List full-height | ✅ | `.page-fill` + `.table-wrap{flex:1;overflow:auto}` + `.table-foot` ติดล่าง |
| #97 | Responsive desktop-base | ✅ | `body{min-width:768px}` · media 1180: drawer `min(กว้างเดิม,100vw)` · sidebar off-canvas + `.nav-toggle` · **Render Gate 1024: ไม่มี body h-scroll** |

## 3. Pass D — Document Archetype (#98–#101) ★

| # | ตรวจ | ผล | หลักฐาน (จาก `static_scan.json → doc_archetype`) |
|---|---|---|---|
| #98 | list มี `docPill` + `renderSignProgress` (n/N + bar 46px) | ✅ | `has_docPill:true` · `has_signProgress:true` |
| #98 | view header: code mono primary + pill + summary + action group ตามสถานะ + divider + copy/printer/download/X | ✅ | ดู `_shots/02_view_detail.png` · action group เปลี่ยนครบ 6 สถานะ |
| #98 | PDF `.a4` + ช่องเซ็น | ✅ | `a4:true` · **4 ช่อง** (ผู้จัดทำ · ผู้อนุมัติ · ผู้ส่งของ · **ผู้รับปลายทาง**) เมื่อโหมดข้ามคลัง · 3 ช่องเมื่อภายในคลัง |
| #98 | submit modal = DOA slot picker เลือกคน | ✅ | `slot_row:true` · `_shots/06_doa_slot_picker.png` — avatar + ตำแหน่ง + ชื่อ · **ไม่มี role ID บนจอ** |
| #98 | create drawer = `.drawer-panel.wide` | ✅ | `1290px` × 2 จุด |
| #99 | `.line-tbl` + grid contract v2 | ✅ | `line_tbl_widths = 26 / (auto) / 64 / 92 / 92 / 78 / 72 / 104 / 54` — **ตรง contract เป๊ะ** |
| #99 | `calcLineVat` / `migrateLine` / `totals` / `taxBadgeV` / `renderLineSummary` | ✅ | ครบ 5 ตัว · **ไม่มีการคำนวณมูลค่านอก `totals()`** |
| #99 | แถวขยาย lean 1 บรรทัด + selector 3 ตัว | ✅ | `line-expand-panel-anchor` / `line-expand-panel-inner` / `line-collapse-panel` ครบ · VAT segmented 3 โหมด (`vat_segmented_3:true`) + หมายเหตุ + chevron-up — **ไม่มีแถวที่ 2** |
| #99 | `updateLine` คืน focus + caret | ✅ | จับ `oninput` + `selectionStart` แล้วคืนหลัง render |
| #100 | wizard 5 steps ชื่อล็อก | ✅ | `เลือกแหล่งที่มา › ข้อมูลหลักใบย้าย › รายการสินค้า › เอกสารแนบ › ตรวจสอบและยืนยัน` |
| #100 | ทุก step เปิดด้วย `STEPH()` · step 4 มี `.upload-zone` · step 5 review read-only | ✅ | ครบ |
| #100 | footer contract + `wizardNext()` validate ต่อ step | ✅ | step 5 = `บันทึกแบบร่าง` (secondary) → `บันทึกและส่งอนุมัติ` (primary · disabled เมื่อ hard control) |
| #101 | view tabs ล็อกลำดับ | ✅ | `รายละเอียด › ระหว่างทางและการรับ (domain 1 tab) › PDF Preview › ลายเซ็น / อนุมัติ › ประวัติ` |
| #101 | เอกสารแนบเป็น **section ใน tab รายละเอียด** | ✅ | `attach_in_detail:true` · **ไม่มี tab เอกสารแนบแยก** |
| #101 | landing section order | ✅ | banners → ข้อมูลเอกสาร → สถานะ → **เส้นทางของสินค้า** → ผู้เกี่ยวข้อง → สรุปมูลค่า → รายการสินค้า → เอกสารแนบ → ข้อมูลระบบ |

## 4. Pass E — #102 Combobox anatomy · #103 Lean & Stable

| ตรวจ | ผล | หลักฐาน |
|---|---|---|
| **คน** = avatar/initials → ชื่อ → ตำแหน่ง · แผนก · รหัส | ✅ | `combo_person_option = 6` · `paintCombo()` สาขา `it.av` |
| **สินค้า** = `package` icon → `code · หมวด` (mono) → ชื่อ → ราคา/หน่วย (ขวา) | ✅ | `kind==='item'` สลับลำดับให้ code อยู่บนชื่อตาม contract |
| **สถานที่/bin** = `map-pin` → รหัส bin → ชื่อโซน (+ เหตุผลล็อก) | ✅ | bin ที่ `ล็อก` = option `disabled` + จาง + บอกเหตุผล |
| keyboard ↑↓/Enter/Esc + focus เปิดทันที + "ไม่พบรายการ" | ✅ | `comboKey()` · `comboOpen()` · Esc ปิด list ก่อน drawer (Esc chain) |
| หน้าจอนิ่ง — overlay ลอยทับ ไม่ดันเนื้อหา | ✅ | Render Gate: เปิด combobox ในตาราง line editor แล้ว layout ไม่ขยับ |
| `renderTableOnly()` ตอนเปลี่ยน filter/sort/page | ✅ | `render_table_only:true` — ไม่ re-render ทั้งหน้า |
| ข้อมูล lean · ไม่มี hint เปลือย | ✅ | `naked_hints = 0` (self_audit) |

## 5. รายการที่ตรวจไม่ได้ในรอบนี้ (offline)

| เรื่อง | สถานะ | เหตุผล |
|---|---|---|
| Rule #38 Thai rhythm — เทียบเส้นกึ่งกลางด้วย **ฟอนต์ไทยจริง** | **NOT-CHECKED (offline)** | sandbox บล็อก CDN (`ERR_TUNNEL_CONNECTION_FAILED`) → Noto Sans Thai/Satoshi ไม่โหลด · ค่าที่ใช้เป็นชุดที่ verify แล้วใน BASE-KIT (`_RUNNER_BRIEF §2.12`) |
| Rule #5/#21 icon geometry จริง | **NOT-CHECKED (offline)** | Lucide CDN ถูกบล็อก — โครงสร้าง class ตรวจแบบ static ผ่านแล้ว |

## 6. Iron Rule Overrides Applied (Rule #98 silent override — log ตามข้อบังคับ)

| # | เรื่อง | ทำอะไร | เหตุผล |
|---|---|---|---|
| 1 | **ชื่อ step 3** | PREBRIEF เรียก "รายการที่ย้าย" → ใช้ชื่อที่ล็อก **"รายการสินค้า"** | Rule #100 ล็อกชื่อ step · เนื้อหา business ยังตาม PREBRIEF |
| 2 | **คอลัมน์ 5–8 ของ line grid** | เปลี่ยน *label* เป็น `ต้นทุน/หน่วย · ส่วนลด % · ภาษี · มูลค่าที่ย้าย` (จำนวน/ลำดับ/ความกว้าง **ไม่เปลี่ยน**) | B2 อนุญาตให้ปรับ label ตาม business · ย้ายสินค้าไม่ใช่รายการค้า |
| 3 | **ส่วนลด % + ภาษี** | คงคอลัมน์ไว้ตาม contract แต่ **`disabled` + ทุกบรรทัด `vat_mode='none'`** พร้อม tooltip อธิบาย | PREBRIEF §3.6 "ไม่มี VAT/ส่วนลด" vs Rule #99 ล็อก 9 คอลัมน์ → คงโครง ปิดการใช้งานเชิงธุรกิจ |
| 4 | **bin ต้นทาง → bin ปลายทาง** | วางเป็นแถวย่อย (`.binrow`) **ภายในคอลัมน์ "สินค้า"** (คอลัมน์ auto-width) | Rule #99 ห้ามเพิ่มคอลัมน์ใน grid · bin เป็นข้อมูลของบรรทัดเดียวกัน (ไม่ใช่ list view จึงไม่ชน #40) |
| 5 | **ส่วนลดท้ายบิล (block ที่ 4 ของ B2)** | **ตัดออก** (คง `endbill` ใน data model + `totals()`) | PREBRIEF §3.6 · B2 อนุญาตตัด optional block ที่ business ไม่มี — block ที่เหลือคงลำดับเดิม |
| 6 | **step 1 "เลือกแหล่งที่มา"** | ไม่มีเอกสารต้นทางข้ามระบบ → 2 tile = `สร้างใหม่` / `ทำสำเนาจากใบย้ายเดิม` | Rule #100: ไม่มีต้นทาง ให้คง step ไว้ ห้ามสลับลำดับ |
| 7 | **domain tab** | เพิ่ม 1 tab **"ระหว่างทางและการรับ"** ระหว่าง รายละเอียด กับ PDF | Rule #101 อนุญาต domain tab ≤2 แทรกหลังรายละเอียด — เป็นแกนที่ feature นี้ขาดไม่ได้ (2 ขา) |
| 8 | **คอลัมน์ list 9 ตัว** | เกิน 8 ของ #16 | Pattern Q spec เองระบุชุดคอลัมน์ 9 + ⋮ · #103 ห้ามยุบแกนสถานะรวมกัน |

## 7. `self_audit.py` — รายการที่ยอมรับพร้อมเหตุผล (ไม่ใช่ BLOCK)

`self_audit.py` เข้มกว่า `audit.sh` (ซึ่งเป็น hard gate ของเลน) — รายการที่เหลือทั้งหมด **มาจากการลอก reference verbatim ตาม Rule #98/#99 ซึ่งห้ามแก้โครง**:

| รายการ | เหตุผลที่ยอมรับ |
|---|---|
| `inline_layout = 250` | `doc-view-drawer.js` / `line-editor-v2.js` / `doc-approval-modals.js` เป็น inline-style ทั้งชุดโดยการออกแบบ — แก้ = ผิด #98/#99 |
| `font_count = 12` · `font_off (10.5/11.5/12.8/9.5)` | ค่าจาก `doc-archetype.css` (`.emp-r 10.5` · `.emp-n 12.8` · `.pill 11` · `.emp-chip.sm 9.5`) |
| `custom_tabs (.tabs/.tab/.tabbar)` | `.tabs/.tab` เป็น class ของ archetype เอง (ไม่ใช่ `.drawer-tab` ของ kit) |
| `hex_off (#00A88E #4FD1BC #8A5200 #D1D5DB #F3F4F6 #FDFBF8)` | #00A88E/#4FD1BC = CI Teal ที่ประกาศเป็น token ใน `:root` · ที่เหลืออยู่ใน `.a4` (งานพิมพ์) + `.upload-zone` ตาม reference |
| `td_pad_fat` | ค่า `13px 14px 11px` คือค่าที่ Rule #38 ระบุว่า verified แล้ว — เช็คตัวนี้ขัดกับ #38 (ทั้ง 12 และ 13 ถูก flag) |
| `stopprop_blanket = 6` | ทุกจุดเป็น `event.stopPropagation()` ที่จำเป็นตาม #41 (checkbox/action cell ในแถวที่คลิกได้) |
| `long_banners` | เป็น `.note`/`.hard-warn` ของ **action จริง** (ค้างระหว่างทาง · ยกเลิก · ตัดส่วนต่าง) ไม่ใช่ hint — ข้อยกเว้นที่ #33 อนุญาตไว้ชัดเจน |

## 8. Fix list ที่แก้ไปแล้วในรอบนี้ (auto-fix loop รอบ 1 — ไม่มีรอบ 2)

| # | ปัญหา | ตำแหน่ง | แก้เป็น |
|---|---|---|---|
| F1 | JS SyntaxError — ternary ขึ้นบรรทัดใหม่ด้วย `+ :` | `renderCreateDrawer()` footer | ย้าย `+` ให้อยู่หลัง string |
| F2 | `<i data-lucide>` ของ empty state ไม่มี `w-N h-N` (#21) | `renderTableHtml()` | เพิ่ม `class="w-5 h-5"` |
| F3 | `★` ในคอมเมนต์ (#23) | หัวบล็อก line engine | เปลี่ยนเป็น `*` |
| F4 | ไม่มี hash route ใน href (refresh-safe evidence) | sidebar + breadcrumb | เปลี่ยนเป็น `href="#/list"` |
| F5 | ปุ่มไอคอนล้วนไม่มี `aria-label` | shell bar · row menu · drawer header | เพิ่ม `aria-label` 8 จุด |
| F6 | ไม่มี PREFLIGHT stamp (#60) | ท้ายไฟล์ | เพิ่มตราพร้อมตัวเลขจริงจาก `self_audit.py` |
| F7 | `.tabbar/.tabs` ไม่มี `align-items` · `.emp-av/.slot-no` grid ไม่มี `gap` | BASE-KIT + archetype CSS | เพิ่มครบ |
| F8 | `.table td` padding ไม่ตรงค่า verified ของ #38 | BASE-KIT | `12/10` → **`13px 14px 11px`** |
| F9 | **บั๊กจริง**: `transitBinFor()` จับคู่ in-transit bin ด้วยการค้นชื่อคลังในชื่อ bin → หาไม่เจอ ทำให้ทุกใบข้ามคลังขึ้น "ยังไม่มีจุดพักระหว่างทาง" | `transitBinFor()` | เพิ่ม field `from`/`to` ที่ bin `TR-*` แล้วจับคู่ด้วยรหัสคลังตรง ๆ |
| F10 | ช่องค้นหาใน filter bar แคบเกินอ่านไม่ออก | `.input-search` | `flex:1 1 240px; min-width:240px` |

## 9. หลักฐานภาพ (`1_HTML/_shots/`)

`01_list.png` · `02_view_detail.png` · `03_view_transit.png` · `03_view_pdf.png` · `03_view_sign.png` · `04a_wizard_step2.png` · `04_wizard_step3.png` · `04b_wizard_step5.png` · `05_receive_modal.png` · `05b_receive_shortage.png` · `06_doa_slot_picker.png` · `07_list_1024.png`
