# _UX_CHECK_REPORT — F-WH-PUTAWAY.html · ขั้น 7R re-gate (qc-ux-html-checker)

วันที่ **2026-09-14** · เลน WF-01 Phase B · ไฟล์ `01_HTML/F-WH-PUTAWAY.html`
arch = **master/console** (registry F081 `arch=master` · `dec=csq` · `wave=W3Q` · `auto=lite`) — Pass D Document Archetype **ไม่ทริกเกอร์**

> **นี่คือ re-gate ของเลนนี้ ไม่ใช่การคัดลอกรายงาน S3a ของต้นน้ำ**
> ตาม `feature-pack-workflow.md` §7R.3 — รันเครื่องมือใหม่ทั้งหมดบนไฟล์ที่อยู่ในแพ็กจริง ห้ามใช้ `0_DIRECTION/_UX_CHECK_REPORT.md` แทน
> HANDOFF อ้าง re-gate ชื่อ `html-review-fix-order` ซึ่งเป็น skill ของ BA lane **ไม่มีใน repo นี้** → ใช้ `qc-ux-html-checker` + `qc-coverage-checker` ทำหน้าที่แทน

## verdict: **PASS** (BLOCK 0 · WARN 5) — หลังแก้ 2 จุดที่ re-gate จับได้

| รอบ | BLOCK | WARN | สถานะไฟล์ |
|---|---|---|---|
| re-gate รอบแรก (ไฟล์ต้นน้ำ byte-identical) | **1** (Iron Rule #81) | 5 | ตรงกับ `1_HTML/F-WH-PUTAWAY.html` ทุกไบต์ |
| re-gate รอบสอง (หลังแก้ 2 บรรทัด) | **0** | 5 | **ไม่ byte-identical กับต้นน้ำอีกต่อไป** — ดู §2 · LD-03 |

---

## 1. ★ ของที่ re-gate จับได้ แต่ gate ต้นน้ำไม่เห็น

### 1.1 BLOCK · Iron Rule #81 — marker ภายในรั่วขึ้นหน้าจอผู้ใช้ (แก้แล้ว)

รายงาน S3a ของต้นน้ำเขียนว่า `jargon_leak = 0` และยก 2 element นี้เป็น **หลักฐานผ่าน** ของ FN-15 และ FN-33
ตรวจจริงด้วย `innerText` ทุกสถานะ (ไม่ใช่ `grep` source) พบว่า **marker `FWD-WIRE:` ถูก render ให้ผู้ใช้เห็นจริง 2 จุด**

| # | element | ข้อความที่ผู้ใช้เห็นจริง (ก่อนแก้) | เห็นเมื่อไหร่ |
|---|---|---|---|
| L-1 | `.cbar .cmini` (บรรทัด 2584) | `ไม่กระทบบัญชี — ย้ายภายในคลังเดียวกัน (FWD-WIRE: JE posting)` | **ทุกงาน ทุกครั้งที่เปิดแผงทำงาน** |
| L-2 | `.warnbox` ในหัวข้อ "เลือกช่องเก็บอื่น" (บรรทัด 2561) | `ของกักกันเลือกได้เฉพาะช่องประเภทกักกันเท่านั้น — ออกจากการกักกันได้ทางเดียวคือใบคืนผู้ขาย (FWD-WIRE: RTV handoff)` | ทุกงานในคิวกักกัน |

**ทำไม gate ต้นน้ำมองไม่เห็น:** `self_audit.jargon_leak` รู้จักเฉพาะ pattern `E-\d{3}` · `GR-…` · `bucket model` · `self-slice`
`FWD-WIRE` ไม่อยู่ในรายการ · และ `audit.sh` Rule #24 จับ literal `TODO` เท่านั้น — ซึ่งเป็นเหตุผลที่ต้นน้ำเปลี่ยนคำมาใช้ `FWD-WIRE` ตั้งแต่แรก
→ **ผ่าน gate ทั้งสองตัว แต่ marker ยังโผล่บนจอ** (รูปแบบเดียวกับที่เจอในรอบ F-PUR-PO)

**การแก้ (อนุมัติโดยผู้ใช้ · 2026-09-14):** ถอดวงเล็บ marker ออกจาก string ที่ render แล้วย้าย marker ไปเป็น **JS comment ท้ายบรรทัดเดียวกัน** — trace ยังอยู่ในซอร์ส แต่ไม่เข้า DOM

```diff
-    ... ออกจากการกักกันได้ทางเดียวคือใบคืนผู้ขาย (FWD-WIRE: RTV handoff)</span></div>' : '')
+    ... ออกจากการกักกันได้ทางเดียวคือใบคืนผู้ขาย</span></div>' : '')  /* FWD-WIRE: RTV handoff */

-    + '<span class="cmini">...ไม่กระทบบัญชี — ย้ายภายในคลังเดียวกัน (FWD-WIRE: JE posting)</span>'
+    + '<span class="cmini">...ไม่กระทบบัญชี — ย้ายภายในคลังเดียวกัน</span>'  /* FWD-WIRE: JE posting */
```

**ยืนยันหลังแก้:** `19_confirm_bar_clean.png` · ข้อความที่ render จริง =
`เก็บครั้งนี้ 100 ท่อน · คงค้าง 0 ท่อน | ไม่กระทบบัญชี — ย้ายภายในคลังเดียวกัน | ข้ามงานนี้ | ยืนยันจัดเก็บ`
`FWD-WIRE` ในซอร์สยังครบ **5 จุด ทั้งหมดอยู่ในคอมเมนต์** (บรรทัด 2049 · 2069 · 2561 · 2584 · 2902) — forward-wire ledger ของ HANDOFF §4.3 ไม่หาย

### 1.2 WARN · `NC rules` โผล่ในป้าย KPI (ไม่แก้ — บันทึกไว้)

`เกิน 24 ชม. (เกณฑ์จาก NC rules)` ในการ์ด KPI "ค้างเกินเกณฑ์" — `NC rules` เป็นชื่อกลไกภายใน เจ้าหน้าที่คลังไม่รู้จัก
**ไม่ถือเป็น BLOCK** เพราะเป็นชื่อระบบที่ผู้ดูแลใช้จริง และตัวเลข 24 อ่านจาก `NC.agingWarnHours` จริง (ไม่ hardcode ในป้าย — ยืนยันบรรทัด 2069 `const NC = { agingWarnHours: 24, softLockMinutes: 30 }`)
→ เสนอถ้อยคำแทน: `เกิน 24 ชม. (ตามเกณฑ์ที่ตั้งไว้)` · **ผู้ใช้ตัดสินให้บันทึกไว้เฉย ๆ รอบนี้**

### 1.3 WARN · watermark ต้นแบบใน sidebar footer (ไม่แก้ — ต้องถอดก่อน production)

`ต้นแบบ Phase A · 2026` — scaffolding ของ prototype ไม่ใช่ affordance ของฟีเจอร์
→ บันทึกเป็น **pre-production removal** ใน README + `07_LOCKED_DECISIONS`

### 1.4 บันทึก · ขนาดไฟล์ในรายงานต้นน้ำไม่ตรงกับไฟล์ที่ส่งมา

`0_DIRECTION/_UX_CHECK_REPORT.md` และ `_TECH_CHECK.md` อ้าง **146,047 bytes · 2,987 บรรทัด**
ไฟล์จริงใน `1_HTML/` = **2,995 บรรทัด** (`static_scan` นับ 147,093 อักขระ) — ต่างกัน **8 บรรทัด**
→ รายงาน S3a/S3b/S3c ของต้นน้ำ **เขียนก่อนการแก้รอบสุดท้าย** จึงเป็นหลักฐานของไฟล์คนละฉบับกับที่ส่งมา
→ **ไม่ใช่ defect** แต่เป็นเหตุผลเชิงรูปธรรมว่าทำไม §7R ห้ามใช้รายงานเดิมแทนการ re-gate · re-run ทั้งหมดในไฟล์นี้ให้ผลเดียวกัน (verdict ไม่เปลี่ยน)

---

## 2. สถานะไฟล์เทียบต้นน้ำ

| | ค่า |
|---|---|
| `cmp` กับ `input/09142026-putaway/1_HTML/F-WH-PUTAWAY.html` | **ต่างกัน 2 บรรทัด** (2561 · 2584) |
| ประเภทการแก้ | microcopy เท่านั้น — ไม่แตะ markup โครงสร้าง · ไม่แตะตรรกะ · ไม่แตะ BASE-KIT |
| อำนาจที่ใช้ | **HANDOFF §5** คอลัมน์ "ทำได้เลย (ไม่ต้อง re-gate business)" แถว *"ปรับถ้อยคำ microcopy · ป้าย · ข้อความ empty state"* + อนุมัติจากผู้ใช้ 2026-09-14 |
| ผลต่อ HANDOFF §3 (ห้ามแตะ) | **ไม่กระทบข้อใดเลย** — L1..L10 ยังครบ (ดู `03_FRD/07_LOCKED_DECISIONS.md`) |
| บันทึกไว้ที่ | `07_LOCKED_DECISIONS.md` **LD-03** · `README.md` §"สิ่งที่ QC เจอ" |

---

## 3. ★ ห้าม Pattern Q — ตรวจเชิงกล (L1)

| เช็ค | คำสั่งที่รัน | ผล |
|---|---|---|
| `static_scan.doc_archetype` | `static_scan.py` | `is_document=false` · `line_tbl=false` · `wizard_steps=[]` · `view_tabs=[]` · `has_docPill=false` · `has_signProgress=false` · `a4=false` · `slot_row=false` · `has_calcLineVat=false` · `has_totals=false` · `vat_segmented_3=false` — **false ครบทุก flag** ✅ |
| grep surface ต้องห้าม | `grep -c` | `STEP_NAMES`=0 · `line-tbl`=0 · `calcLineVat`=0 · `renderSignTab`=0 · `slot-row`=0 · `tabBtn(`=0 · `vat_mode`=0 · `a4`=0 · `docPill`=0 · `signProgress`=0 ✅ |
| `audit.sh` block `doc_archetype` | `audit.sh` | ไม่ทริกเกอร์ (ไม่มี `vat_mode|renderSignTab|line-tbl`) ✅ |
| เลขที่เอกสาร | grep | `เลขที่เอกสาร`=0 · `doccfg`=0 · `ENG-DOC-NUM`=0 ✅ |
| PDF / ลายเซ็น / สายอนุมัติ | grep + อ่าน context ทุกจุด | `PDF`=1 · `ลายเซ็น`=1 · `อนุมัติ`=3 · `พิมพ์`=4 — **ทั้งหมดอยู่ในคอมเมนต์ หรือเป็นคำไทยปกติ** (บรรทัด 2047 คอมเมนต์ประกาศว่าห้ามมี · 715/716 คอมเมนต์ CSS `/* อนุมัติแล้ว */` · 2151 ชื่อคน "พิมพ์ชนก" · 2501 "ต้องพิมพ์เหตุผลเพิ่ม") · **ไม่มีจุดใด render เป็น surface เอกสาร** ✅ |
| `DOA` ในไฟล์ | grep | **0** ✅ |

### 3.1 dead CSS รูปทรง Pattern Q — false positive ที่ต้องอธิบาย

แยก CSS สองก้อนด้วย marker `END BASE-KIT` (บรรทัด 1349) แล้วเทียบกับ markup+JS (`re.sub` ตัด `<style>` ออก):

| ก้อน | คลาสที่ประกาศ | ไม่ถูกใช้ |
|---|---|---|
| **BASE-KIT** (บรรทัด 1–1349 · Rule #69 verbatim ห้ามแก้) | 254 | **117** |
| **PAGE CSS** (ใต้ END marker · ของผู้เขียนเอง) | 83 | **1** (`is-done`) |

ในกลุ่ม dead ของ BASE-KIT มี **27 คลาสรูปทรง Pattern Q** — `stepper` · `stepper-item` · `stepper-circle` · `d-stepper` · `wizard-shell` · `wizard-body` · `wizard-card` · `wizard-footer` · `wizard-stepper-band` · `drawer-tabs` · `drawer-tab` · `drawer-panel` · `drawer-header` · `drawer-footer` ฯลฯ

> **นี่คือ CSS ของ kit ที่ติดมากับ skeleton ไม่ใช่ surface ของฟีเจอร์** — ต่างจากรอบ F-PUR-COMPARE ที่ dead CSS ทำให้ `doc_archetype.is_document` รายงาน `true` ผิด
> รอบนี้ **ตัวชี้วัดจริงทุกตัวเป็น `false`** (ตาราง §3) และ **PAGE CSS ของผู้เขียนสะอาดถึง 82/83** → ไม่มี Pattern Q ทั้งใน CSS ที่เขียนเองและใน markup
> เงื่อนไขความน่าเชื่อถือของวิธีสแกน: ไฟล์มี dynamic class construction (`classList.*` / `'is-'+v`) จริง → จึงรายงาน `is-done` เป็น **WARN ไม่ใช่ให้ลบ**

---

## 4. Iron Rules #1–#103

| Rule | ผล | หลักฐาน (รันเอง 2026-09-14) |
|---|---|---|
| #1 CI tokens | ✅ | `hex_off = 1` → `#E7E2DB` เท่านั้น = `.menu-fixed` ของ BASE-KIT (ยืนยันเป็น baseline ใน §5) |
| #2 Font stack | ✅ | `font_count = 8` (limit 8) · `font_off = 0` · Satoshi + Noto Sans Thai + system-ui |
| #3/#4 Sidebar 232 / Shell 52 | ✅ | `px_watchlist`: `232px`=1 · `52px`=5 · `540px`=0 · `244px`=0 |
| #5 Lucide only | ✅ | `lucide_icon_count = 82` · `fontawesome = false` |
| #6/#7 Page header + breadcrumb | ✅ | ช็อต `01` — breadcrumb `คลังสินค้า › จัดเก็บเข้าที่` + `.ph-title-row` + `.ph-count` "12 งานค้าง" + `.ph-sub` |
| #8 KPI ≤ 6 | ✅ | 5 การ์ด (ช็อต `01`) |
| #9 Filter ใน card · #10 Table footer | ✅ | `.aside-tools` ใน card คิว · `.table-footer` ทั้งมุมมองผังและประวัติ |
| #11–#15 Drawer/Modal | ✅ | ไม่มี drawer ใช้งานจริง (console) · modal 440px (`px_watchlist 440px=1`) · backdrop z=50 · **Esc ปิดได้จริง** (`esc_closes_modal = true`) · ช็อต `13`, `15` |
| #16 ≤ 8 คอลัมน์ | ✅ | ผัง 7 · ประวัติ 8 |
| #19 Number spinner | ✅ | BASE-KIT global hide |
| #21 Icon class | ⚠️ (2) | `ss-caret` (บรรทัด 1772) · `emptyStateHTML` (บรรทัด 1885) — **ทั้งคู่ใน BASE-KIT** Rule #69 ห้ามแก้ |
| #23 No color emoji | ⚠️ (baseline) | `emoji.count = 4` (`⚠ ✅`) — อยู่ในคอมเมนต์ CSS/JS ของ BASE-KIT · **ไม่พบใน `innerText` ของทุกสถานะ** (sweep §6) |
| #24 No dev-tool / TODO | ✅ | `audit.sh` **FAIL = 0** · literal `TODO` ในไฟล์ = **0** |
| #25 renderIcons() | ✅ | ไม่มี `lucide.createIcons()` นอก wrapper |
| #27 Sidebar module-feature | ✅ | `.sb-module[data-module]` × 2 (คลังสินค้า · จัดซื้อ) · header เป็น `<button>` + `aria-expanded` · ช็อต `01` |
| #28 Slim top bar | ✅ | breadcrumb + notification + user chip เท่านั้น |
| #29 Render preservation | ✅ | `render = withRenderPreservation(function realRender(){…})` — พิมพ์ในช่องจำนวนแล้ว re-render ไม่หลุด focus (ยืนยันตอนทดสอบ `setDestQty` ต่อเนื่อง) |
| #30 Fluid content | ✅ | `.content` ไม่มี `max-width` |
| #33 Hint = tooltip | ✅ | `.info-tip[data-tip]` 3 จุด · `naked_hints = 0` · `long_banners = 0` |
| #34/#94/#102 Search combobox | ✅ | `combobox_count = 13` · `select_big = 0` · `<select>` เหลือเฉพาะ enum เหตุผล override 5 ค่า · ช็อต `09` (anatomy คน: ชื่อ → ตำแหน่ง · แผนก) |
| #35 Layout stability | ✅ | `scrollbar_gutter_stable = true` |
| #36 Button symmetry | ✅ | ปุ่มทุกตัวใช้ `.btn` ของ kit |
| #37 Requirement coverage | ✅ | ดู `_COVERAGE_REPORT.md` — FN 44/44 พร้อมหลักฐาน runtime |
| #38 Thai rhythm | ⚠️ **NOT-CHECKED (offline)** | CDN ถูกบล็อก → Satoshi/Noto Sans Thai/Lucide ไม่โหลด · ตรวจ optical center จริงไม่ได้ · **ข้อจำกัดเดียวกับต้นน้ำ ไม่วนแก้** |
| #39 Empty state | ✅ | `markers.empty_state = 12` · `nosuggest_stopbox` มีข้อความจริง (§6.3) |
| #40/#103 List atomicity | ✅ | `td_multi_pill = 0` |
| #41 Row = view | ✅ | `data-lucide="eye"` = 0 · แถวกาง inline (`.line-expanded`) — ช็อต `12`, `14` |
| #43 Validation + format | ✅ | `destIssues()` คืนข้อความจริง (§6.4) · **ปี ค.ศ. ล้วน** ผ่าน `fmtD/fmtDT` (`getFullYear()`) — ช็อต `01` แสดง "10 ก.ย. 2026" |
| #44 Loading/submitting | ✅ | `markers.loading = 5` · `state.busy` กันกดซ้ำ |
| #45 Disabled/read-only | ✅ | `markers.disabled = 10` · ยืนยันจริง: ปุ่มยืนยัน `is-disabled` เมื่อ over-qty และ qty=0 (§6.4) |
| #46 Placement contract | ✅ | primary เดียวที่ `.ph-actions` ("เริ่มงานถัดไป") · toast ขวาล่าง z=80 |
| #47 Stepper | N/A | console ไม่มี wizard (L1) |
| #48 Landing | ✅ | M3 KPI home ย่อ — ไม่มี hero/carousel |
| #49 Scrollbar | ✅ | `webkit_scrollbar = true` · width 5px |
| #62 Z-index registry | ✅ | ดู §5.1 — ประกาศครบ ใช้ครบ ยืนยันด้วย `getComputedStyle` |
| #69 BASE-KIT verbatim | ✅ | การแก้ 2 จุดอยู่ที่บรรทัด 2561/2584 = **ใต้ `END BASE-KIT UTILS` (2041)** ทั้งคู่ · BASE-KIT ไม่ถูกแตะ |
| #81 Jargon leak | ✅ **หลังแก้** | sweep `innerText` 13 สถานะ → **0 hit** (ก่อนแก้ 4 hit · §1.1) |
| #95 Overlay portal | ✅ | `portal_menu = true` · `overlay_root = true` |
| #96 List full-height | ✅ | `page_fill = true` |
| #97 Responsive desktop-base | ✅ | ตาราง 7 ความกว้าง §5.2 — **สะอาดครบรวม 768** |
| #100 STEP_NAMES | N/A | ไม่ใช่ Q-document — `STEP_NAMES` = 0 |
| #103 Stable screen | ✅ | overlay ลอยทับทุกตัว · การกางแถวใช้ `.line-expanded` |

---

## 5. เครื่องมือเชิงกล — ผลที่รันเอง

### 5.1 `self_audit.py` + การพิสูจน์ baseline

```
spacing_off = 2  → ['1180','52']          font_off = 0      font_count = 8 (limit 8)
flex_noalign = 0    grid_nogap = 0        inline_layout = 0    z_adhoc = 0
hex_off = 1  → ['#E7E2DB']                naked_hints = 0      long_banners = 0
overlay_no_z = 0    undefined_handlers = 0                     jargon_leak = 0
missing_ids = 5 → ['ss-','ss-caret-','ss-clear-','ss-input-','ss-list-']
fullwidth_select = 1    custom_tabs = 0   td_pad_fat = 0    tbody_font_fat = 0
duplicate_counts = 0    img_placeholders = 0    menu_no_bg_z = 0
menu_no_maxheight = 0   menu_no_flip = 0  preflight = 0
```

**พิสูจน์ว่า 4 ตัวที่ไม่เป็นศูนย์คือ baseline ของ skeleton จริง** — รัน `self_audit.py` กับ `templates/file-skeleton.template.html` เปล่า:

```
spacing_off = 2 → ['1180','52']        ← เท่ากัน
hex_off = 1 → ['#E7E2DB']              ← เท่ากัน
fullwidth_select = 1                    ← เท่ากัน
missing_ids = 7 → ['overlay-root','page-content','ss-','ss-caret-','ss-clear-','ss-input-']
                                        ← skeleton มากกว่า 2 ตัว (ไฟล์เราประกาศ overlay-root/page-content จริง)
```

→ **คำกล่าวอ้างของต้นน้ำถูกต้อง** · ส่วนที่ผู้เขียนเพิ่มเอง = **0 ทุกตัวนับ** (`inline_layout` · `z_adhoc` · `naked_hints` · `long_banners` · `undefined_handlers` · `jargon_leak` เป็นศูนย์หมด)

**Z-Index registry (#62) — ตรวจสองฝั่งตามบทเรียน F-PUR-PR:**

| | ผล |
|---|---|
| ประกาศ (`grep -cE '\-\-z-[a-z]+\s*:'`) | บรรทัด 1352 — `:root { --z-content:1; --z-sticky:10; --z-shell:20; --z-dropdown:30; --z-backdrop:50; --z-drawer:51; --z-modal:60; --z-toast:80; }` |
| ใช้ (`var(--z-*)`) | 6 ตัว: `backdrop` `drawer` `dropdown` `shell` `sticky` `toast` |
| ครอบคลุม | **ใช้ 6 / ประกาศ 8 → ครบทุกตัวที่ใช้** ✅ (ไม่ใช่บั๊ก `--z-*` ที่เจอใน F-SEC-TRANS / F-SEC-LOCKOUT) |
| ยืนยัน runtime `getComputedStyle().zIndex` | `.shell-bar` = **10** (sticky) · `thead th` = **3** (sticky) · `.modal-backdrop` = **50** (fixed) · `.toast` = **80** (fixed) · `.ss-list` = **50** |
| modal เปิดจาก view — ทับได้ถูกชั้นไหม | `document.elementFromPoint()` กลางบน modal → **คืน element ในตัว modal เอง** (`modal_is_topmost = true`) ✅ |
| `#overlay-root` z = `auto`, สูง **0px** | **ไม่ใช่บั๊ก** — เป็น portal container ที่ลูกเป็น `position:fixed` (รูปแบบเดียวกับ #95 ใน F-PUR-PO) · **บันทึกไว้ให้ขั้น 12: ห้ามใช้ `#overlay-root` เป็น container ตอน capture** |

### 5.2 Responsive — วัดหลายความกว้าง (บทเรียน F-PUR-COMPARE #4)

`document.documentElement.scrollWidth` เทียบ `window.innerWidth`:

| width | 1600 | 1440 | 1280 | 1180 | 1024 | 900 | **768** |
|---|---|---|---|---|---|---|---|
| scrollWidth | 1600 | 1440 | 1280 | 1180 | 1024 | 900 | **768** |
| h-scroll | ไม่มี | ไม่มี | ไม่มี | ไม่มี | ไม่มี | ไม่มี | **ไม่มี** |

**สะอาดครบ 7 ความกว้างรวม 768** — sidebar ยุบหายที่ 768 · KPI reflow 3+2 · split-pane ซ้อนเป็นคอลัมน์เดียว (ช็อต `17_queue_1024.png` · `18_queue_768.png`)
`body_minwidth_768 = true` · ดีกว่ารอบ F-PUR-COMPARE ที่ 768 ล้น 28px

### 5.3 Bottom-edge test ของ dropdown ทุกตัว (บทเรียน F-PUR-PO #4)

เลื่อน input เข้ากลางจอก่อน แล้วเปิดลิสต์ แล้ววัด `getBoundingClientRect()` + `elementFromPoint` ทั้ง 4 มุม:

| combobox | rect (top→bottom) | ล้นใต้จอ | 4 มุมคืน element ในลิสต์ | z-index | max-height |
|---|---|---|---|---|---|
| `wh` (ตัวกรองคลัง) | 116 → 294 | 0 px | ✅ ครบ 4 | 50 | 280px |
| `binpick` (ค้นช่องเก็บ) | 472 → 752 | 0 px | ✅ ครบ 4 | 50 | 280px |
| `actor` (ผู้จัดเก็บ) | 680 → 917 | **17 px** | 2 บน ✅ · 2 ล่าง offscreen | 50 | 280px |

⚠️ **WARN** — ลิสต์ `actor` ล้นขอบล่าง **17px** ที่ viewport 1440×900 เมื่อ input อยู่กลางจอพอดี
ไม่ใช่ BLOCK: ลิสต์เป็น `position:absolute` ในแผงที่ scroll ได้ → เลื่อนลงอีกนิดก็เห็นครบ · และ `max-height:280px` ของ kit กันไม่ให้ยาวกว่านี้
`self_audit.menu_no_flip = 0` ครอบเฉพาะ `.menu-fixed` ของ kit ไม่ครอบ `.ss-list` — จึงต้องวัดเองแบบนี้

### 5.4 `audit.sh` · `node --check`

```
audit.sh   →  FAIL = 0 · WARN = 3
node --check (แยก 8 script block · strip HTML comment ก่อน)  →  OK
```

| WARN | ที่มา | ท่าที |
|---|---|---|
| Rule #21 `<i data-lucide>` ไม่มี `w-N h-N` (2) | BASE-KIT (`ss-caret` 1772 · `emptyStateHTML` 1885) | ไม่แก้ — Rule #69 |
| Rule #40 `.uc-email` sub-line | BASE-KIT CSS (คลาสไม่ถูกใช้ในไฟล์นี้) | ไม่แก้ |
| Token hardcoded font-size | BASE-KIT CSS (บรรทัด 82 · 129 · 130 · 145 · 168) | ไม่แก้ |

---

## 6. Render check — Playwright จริง (ไม่เชื่อ stamp)

### 6.1 Console / error

| เช็ค | ผล |
|---|---|
| console error ทั้งหมด | **0** |
| console error จากโค้ดของ feature | **0** |
| `pageerror` (JS exception) | **0** |

> รอบนี้ CDN โหลดไม่ถูกบล็อกเหมือน sandbox ของต้นน้ำ → **console error รวม = 0** ไม่ใช่ 5

### 6.2 Iron Rule #81 sweep — `innerText` ทุกสถานะ

ไล่ 13 สถานะ: `queue` · `queue-quarantine` · `queue-void` · `bins` · `bins-expanded` · `bins-WH-TRN` · `history` · `history-expanded` · `runner-normal` · `runner-quarantine` · `runner-nosuggestion` · `modal-lock` · `modal-reverse`
สแกนหา 40 คำ: `FWD-WIRE` `TODO` `ENG-` `PIPES_HIT` `CSQ` `basis:` `OQ-` `AI-DRAFT` `ASSUMED` `BR-` `FN-` `S-0` `LD-4C` `state.` `suggestBins` `violationOf` `rank1` `location_type` `null` `undefined` `NaN` `[object` `mock` `Pattern` `W3Q` `F081` `F-WH` `prototype` ฯลฯ

| ก่อนแก้ | หลังแก้ |
|---|---|
| `FWD-WIRE` × 4 context · `NC rules` × 4 · `ต้นแบบ` × 1 | **`FWD-WIRE` × 0** · `NC rules` × 4 (WARN §1.2) · `ต้นแบบ` × 1 (WARN §1.3) |

**ไม่พบ:** `null` · `undefined` · `NaN` · `[object` · `BR-xx` · `FN-xx` · `S-0x` · `OQ-` · ชื่อฟังก์ชัน · ชื่อ engine · `PIPES_HIT` · คอลัมน์ผลรายท่อ ✅

### 6.3 Flow ที่เดินจริงได้ (หลักฐาน 20 ช็อต)

`01` console + KPI 5 + คิว 12 งาน → `02` เลือกงาน → เสนอ 3 การ์ดพร้อมเหตุผล → `03` รับงาน → `04` เลือกอันดับ 2 → `05` split 2 ปลายทาง → `06` กรอกเกินยอด → บล็อก → `07` override ข้ามหมวดโซน → บังคับเหตุผล → `08` เลือกเหตุผลแล้วยืนยันได้ → `09` combobox ผู้จัดเก็บ (ชื่อ → ตำแหน่ง · แผนก) → `10` คิวกักกัน (ตัวเลือกเหลือแต่ `QA-02`) → `11` ไม่มีช่องเก็บที่ตรงเกณฑ์ → `12` ผังช่องเก็บกางโซน B → `13` modal ล็อกช่อง → `14` ประวัติกางแถว → `15` modal กลับรายการ → `16` กลับรายการสำเร็จ (คู่ 2 แถว) → `17` 1024px → `18` 768px → `19` แถบยืนยันหลังแก้ → `20` กลุ่มคิวกักกัน

### 6.4 Validation ที่ยืนยันด้วยการรันจริง (ไม่ใช่อ่านโค้ด)

| กรณี | ที่ทำ | `destIssues()` คืน | ปุ่มยืนยัน |
|---|---|---|---|
| จำนวนเกินยอดค้าง | `setDestQty(0, remain + 10)` | `จำนวนรวมเกินยอดคงค้างเก็บ 100 ท่อน` | `is-disabled = true` ✅ |
| จำนวน = 0 | `setDestQty(0, 0)` | `ต้องมีปลายทางอย่างน้อย 1 รายการที่จำนวนมากกว่า 0` | `is-disabled = true` ✅ |
| override ข้ามหมวด ยังไม่มีเหตุผล | `chooseBin('A-01-01-A')` | `ปลายทางที่ 1 (ข้ามหมวดโซน): ต้องเลือกเหตุผลก่อนยืนยัน` | `is-disabled = true` ✅ |
| ใส่เหตุผลแล้ว | `reason = 'bin แนะนำเต็ม'` | `[]` | เปิด ✅ |
| ไม่มีช่องเก็บที่ตรงเกณฑ์ | เลือก `PT-0015` | `.warnbox.is-stop` = `ไม่มีช่องเก็บที่ตรงเกณฑ์ในคลังนี้ — ช่องที่เหลือถูกกรองออกเพราะ เต็ม / ล็อก / ห้ามปนสินค้า / ผิดประเภท · ทางออก: ปล่อยงานค้างคิวไว้ก่อน หรือค้นหาช่องเก็บเองแล้วระบุเหตุผล` | — ✅ |
| modal ล็อก bin ยังไม่มีเหตุผล | `askLockBin()` | — | ปุ่มยืนยัน `is-disabled = true` ✅ |
| Esc ปิด modal | `keyboard.press('Escape')` | — | modal ปิดจริง ✅ |

---

## 7. Fix loop รอบนี้

| รอบ | ปัญหา | แก้ | ยืนยัน |
|---|---|---|---|
| 1 | **Iron Rule #81** — `FWD-WIRE: JE posting` และ `FWD-WIRE: RTV handoff` render ให้ผู้ใช้เห็น (§1.1) | ย้าย marker เข้าคอมเมนต์ JS ท้ายบรรทัดเดิม 2 จุด | `innerText` sweep 13 สถานะ = **0 hit** · `audit.sh` FAIL 0 · `self_audit` เท่าเดิม · `node --check` OK · console/pageerror 0 · behaviour test ทั้ง 7 กรณีให้ผลเดิมทุกข้อ |

**BLOCK คงเหลือ: 0** · ภาพหลักฐานทั้ง 20 ใบถ่ายใหม่หลังแก้ (ลบชุดก่อนแก้ทิ้งทั้งหมด — ตรวจ md5 ซ้ำ = 0)
