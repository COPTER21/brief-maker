---
name: qc-ux-html-checker
description: "Quality Gate หลัง html-generator-v9 (รองรับ v6–v8) — ตรวจ HTML prototype ว่า 'ทำถูกมั้ย' เชิง form: iron rules #1–#103 Sync Read จาก html-generator เวอร์ชันสูงสุด (ไม่ copy กฎมาเก็บเอง), CI Warm Light, component consistency, UX heuristics (empty/loading/error, Esc chain, destructive confirm, microcopy), Pass D Document Archetype (Pattern Q/B2 v2 #98–#101), combobox anatomy #102, lean list/stable screen #103, Render Gate + golden compare → ออก _UX_CHECK_REPORT.md fix list ระบุตำแหน่ง+วิธีแก้ · loop mode diff · fix mode surgical ใช้เมื่อ user พูดถึง 'qc-ux-html-checker', 'ตรวจ UX', 'เช็ค HTML', 'ตรวจ iron rules', 'ux gate', 'ตรวจก่อนส่ง', 'review HTML', 'fix list', 'vibe check' — ใช้ทุกครั้งหลัง gen/vibe HTML ก่อนขั้นเอกสาร Output: _UX_CHECK_REPORT.md + verdict PASS/WARN/BLOCK ห้ามใช้ตรวจ business scope — นั่นคือ qc-coverage-checker"

## ⛔ Lane-mode BLOCK list เพิ่ม (2026-09-10 — Sync Read กับ html-generator-v9 #104–#106)

4 ข้อนี้ใน lane/automate mode ให้ verdict = **BLOCK เสมอ (ห้ามลดเป็น WARN)**:
| # | ตรวจ | วิธีตรวจ |
|---|---|---|
| #67.1 | hint/info-banner/ⓘ โผล่โดย FRD/PREBRIEF ไม่ได้ระบุ explicit | grep banner/callout/hint + เทียบ PREBRIEF — เจอโดยไม่มีแหล่ง = BLOCK |
| #104 | สลับ sub-view ด้วยปุ่มขวาบน page header / dropdown แทน tab row มาตรฐาน | มี ≥2 view แต่ไม่มี `.tabs` ใต้ page-head = BLOCK |
| #105 | persona/role switcher ไม่ติด `data-demo="persona-switch"` + badge DEMO | มีตัวสลับบทบาทเปลือย = BLOCK · และเช็คต่อใน FRD gate: ไม่มี section "Demo-only elements" = BLOCK ที่ S6.5 |
| #106 | toolbar filter ไม่ใช่ block มาตรฐาน (`.toolbar > .search-box` + select 160–240px แถวเดียว) | พบ class filter-row/filter-bar/input-search หรือ search เต็มแถวเดี่ยว = BLOCK |

รายงานใน _UX_CHECK_REPORT.md ต้องระบุ: จุดที่เจอ (selector/บรรทัด) + วิธีแก้ (ชี้ block/กฎ) — ตาม format เดิม
---

# QC: UX HTML Checker

## Purpose

ด่านตรวจ "ทำ**ถูก**มั้ย" (form) ของ HTML prototype — จับ violation เชิง CI/iron rules/
UX แล้วแปลงเป็น **fix list ที่ชี้ตำแหน่ง + บอกวิธีแก้** เพื่อให้การ vibe มีเป้าชัด
จบเร็ว ไม่วนตามความรู้สึก

ไม่ตรวจความครบของ business scope (edges, golden rules, exception paths) —
นั่นคืองานของ `qc-coverage-checker` สองตัวนี้แยกกันเพื่อให้ ux loop วนเร็วโดยไม่ต้องแบก graph

## หลักการสำคัญ: Single Source of Truth

**ห้ามเก็บ iron rules ไว้ใน skill นี้** — ตัวกฎอยู่ที่ **`html-generator-v9`** (เวอร์ชันสูงสุดที่ติดตั้ง) เท่านั้น
skill นี้เก็บแค่ "วิธีตรวจ" ทุก run ต้อง Sync Read — **หา `GEN=$(ls -d /mnt/skills/user/html-generator-v* | sort -V | tail -1)` ก่อนเสมอ** แล้วจด version ลง report:

| ไฟล์ (ใน `$GEN`) | ใช้ตรวจ |
|---|---|
| `knowledge/iron-rules.md` | กฎทั้งหมด #1–#49 · #94–#103 (Group 18–21) — อ่านจำนวนจริงจากไฟล์ |
| `knowledge/layout-integrity.md` | #50–#62 เรขาคณิต · Pre-flight #60 |
| `knowledge/component-contracts.md` | #63–#68 · #74–#80 · B2 QC #83–#92 (re-scoped v9) |
| `knowledge/page-anatomy.md` | #70–#73 ความรวยของหน้า |
| `knowledge/ci-tokens.md` | hex whitelist, CSS vars, fonts, spacing (Warm Light) |
| `knowledge/microcopy.md` | ถ้อยคำมาตรฐาน ปุ่ม/empty/error/status pill |
| `knowledge/component-catalog-ref.md` | component pattern ที่ต้อง consistent |
| `patterns/Q_transaction-document-archetype.md` + `patterns/B2_document-line-editor.md` | **Pass D** — เอกสารธุรกรรม (list/wizard/view/PDF/line editor) |
| `patterns/P_day-planner-scheduler.md` | feature ประเภท planner |
| `references/document-archetype/_SOURCE_so-reference.html` · `references/planner/*.html` · `templates/reference/*.html` | golden reference ต่อ archetype — ใช้ใน Render Gate เทียบภาพ |
| `references/drawer-standard/README.md` | spec drawer 920/680 + `.wide` 1290 + combobox anatomy #102 |
| `scripts/audit.sh` · `scripts/self_audit.py` | เครื่องนับหลัก (audit.sh มีส่วน `doc_archetype` + `#102/#103`) |

ถ้าไม่มี v9 → ใช้เวอร์ชันสูงสุดที่มี และระบุใน report ว่ากฎ #98–#103 = NOT-CHECKED (generator เก่ากว่า v9)
ถ้าไม่มีเลย → แจ้ง user และตรวจได้เฉพาะหมวด UX heuristics (ระบุใน report ชัดว่า
iron rules = NOT-CHECKED)

## Input

| Input | จำเป็น | หมายเหตุ |
|---|---|---|
| ไฟล์ .html | ✅ | output จาก html-generator-v9 (หรือ v6–v8) หรือไฟล์ที่ vibe แก้แล้ว |
| archetype hint | optional | Q-document / master / planner / dashboard — ถ้าไม่ให้ checker เดาจากไฟล์ (มี `vat_mode`/`renderSignTab` = Q · `.cal-grid`/`.pool-card` = P) |
| `_UX_CHECK_REPORT.md` รอบก่อน | loop mode | ให้ diff fixed/remaining/new |
| NODE_BRIEF | optional | ใช้แค่รู้ชื่อ feature/route — ไม่ใช้ตรวจ scope |

---

## Workflow

### Phase 0 — Sync Read

อ่านไฟล์ authoritative ตามตารางข้างบน + สร้าง checklist สดจาก iron-rules.md
(จำนวนกฎ/เลขกฎ ยึดตามไฟล์ ไม่ยึดตามความจำ) — จด version ของ generator ที่อ่านลง report

### Phase 1 — Mechanical Scan (script)

รัน **`bash $GEN/scripts/audit.sh <file.html>`** ก่อน (FAIL ≥1 = BLOCK ทันที · ครอบ #98–#103 อัตโนมัติ) แล้ว
รัน `scripts/static_scan.py <file.html>` → ได้ JSON facts: hex ทั้งหมดที่ใช้ (พร้อมจำนวน),
font-families, px widths ที่เจอ, icon usage, hash routing, Esc handler, scrollbar css,
localStorage, emoji, ฯลฯ แล้ว**ตีความเทียบกับ tokens/rules ที่ Sync Read มา**:

- hex ที่ไม่อยู่ใน ci-tokens whitelist → BLOCK (ระบุ hex + จำนวนครั้ง + บรรทัดตัวอย่าง)
- font-family นอก stack → BLOCK
- เจอ `540px` drawer legacy → BLOCK (Rule #11) · `1290px` ใช้ได้เฉพาะ `.drawer-panel.wide` ของ B2/Q
- `select_big` (select >7 options) > 0 → WARN #102 · `overlay_root` = false ทั้งที่มี dropdown ใน scroll container → BLOCK #95 · `page_fill` = false ในหน้า list → WARN #96 · `body_minwidth_768` = false → WARN #97
- ไม่มี minimal scrollbar / hash routing / Esc handler → ตาม severity ของ rule นั้น
- script บอกได้แค่ "facts" — การตัดสินว่าผิดกฎไหนเป็นหน้าที่ Claude เทียบกับกฎสด

วิธี map fact → rule ดู `references/check-methods.md`

### Phase 2 — Heuristic Review (อ่าน HTML จริง ไล่ทีละ route/หน้า)

หมวดที่ script ตรวจไม่ได้ ต้องอ่านโค้ดเอง:

1. **States ครบชุด** — ทุก list/form มี empty state, loading/submitting, error state,
   disabled ที่ถูกจังหวะ (ตาม Rules #39, #44-45 และ microcopy มาตรฐาน)
2. **Interaction chain** — Esc ปิด overlay ตามลำดับ, focus ไปที่แรกใน drawer,
   backdrop click, destructive action มี confirmation modal (440px)
3. **Layout stability** — ไม่มี shift ตอน toggle/loading (Rule #35), button symmetry (#36)
4. **Thai rhythm + microcopy** — ถ้อยคำตรง microcopy.md, วรรคตอนไทย (#38)
5. **List/Table UX** — cell atomicity, row=view, long-list UX (#40-42) + **#103**: pill ≥2 ใน cell เดียว / ข้อมูลคนละตัวยัดคอลัมน์เดียว = BLOCK · บรรทัดรองต้องเป็น meta ของข้อมูลเดียวกัน · filter/sort ต้องเป็น `renderTableOnly` ไม่ re-render ทั้งหน้า
6. **Search dropdown (#94/#102)** — field ที่อ้าง master/รายการ >7 ค่า ต้องเป็น combobox ไม่ใช่ `<select>` · option anatomy ล็อก: คน = avatar→ชื่อ→ตำแหน่ง·แผนก · สินค้า = package→code·หมวด→ชื่อ→ราคา/ATP · ทุก dropdown ในไฟล์เรียงแบบเดียวกัน · clear = cascade (#94.1)
7. **Hint opt-in (#67.1)** — hint/ⓘ ที่ FRD ไม่ได้สั่ง = WARN · **#81** ศัพท์ภายใน (E-xxx/hook/bucket) รั่วขึ้นจอ = BLOCK · **#82** JS ต้องมาจาก kit/reference ไม่ใช่เขียนใหม่ทั้งชุด · **#47.1** stepper `flex:1 1 0` + connector กึ่งกลาง dot

### Phase 3 — Component Consistency

เทียบ**ภายในไฟล์เดียวกัน**: component ชนิดเดียวกันต้องหน้าตา/โครงเดียวกันทุกที่
(ปุ่ม, badge, drawer header, table, filter bar) — หา style ซ้ำซ้อนที่ diverge
เช่น ปุ่ม primary สองแบบ, badge สถานะเดียวกันคนละสี — พวกนี้คือสิ่งที่ทำให้ "ดูไม่เรียบร้อย"
แม้แต่ละจุดไม่ผิดกฎตรง ๆ → WARN พร้อมชี้ว่าให้ยึดแบบไหน (เลือกแบบที่ตรง catalog)

### Phase 4 — Report

สร้าง `_UX_CHECK_REPORT.md` ตาม `references/report-format.md`:

- **Verdict**: `BLOCK` (มี iron rule violation ≥1) / `WARN` (มีแต่ heuristic) / `PASS`
- ทุก finding: id (`UX-NN`), severity, rule ref (Rule #N หรือ H-หมวด), ตำแหน่ง
  (route + selector/บรรทัด), พบอะไร, **วิธีแก้ concrete** (โค้ด/ค่าที่ถูก)
- หมวดที่ตรวจไม่ได้ → ลิสต์เป็น NOT-CHECKED พร้อมเหตุผล ห้ามนับเป็นผ่านเงียบ ๆ
- สรุปหัว report: นับ BLOCK/WARN/INFO + ประเมินเวลาแก้คร่าว ๆ

### Phase 5 — Loop / Fix Mode

- **Loop mode** (มี report เก่า): diff → `แก้แล้ว ✓ / ค้าง / โผล่ใหม่` + iteration count
  — ถ้า item เดิมค้างเกิน 2 รอบ ให้ยกขึ้นบนสุดพร้อมข้อเสนอแก้ให้เลย
- **Fix mode** (user สั่ง "แก้ให้เลย"): แก้ **surgical เฉพาะรายการใน report** ห้ามแตะ
  ส่วนอื่นของไฟล์ ห้าม regenerate ทั้งหน้า → แก้เสร็จรัน Phase 1-4 ซ้ำยืนยัน
- เกณฑ์ผ่าน gate: **BLOCK = 0** — WARN เหลือได้ตามดุลยพินิจ user (ระบุใน verdict ว่า
  "PASS with N warnings")

---

## ⭐ Pass เพิ่ม (2026-07-26) — ปิดตาบอดเรขาคณิต

### Pass G — Geometry Static Check (บังคับทุกครั้ง)
Sync Read `$GEN/knowledge/layout-integrity.md` (#50-#62) + `component-contracts.md` (#63-#68) + `page-anatomy.md` (#70-#73) + contracts #74-#80 + Block-First แล้วตรวจเชิงกล (audit v4: +img_placeholders) · เคสที่มี block ใน templates/blocks/ → เทียบว่าโครง markup มาจาก block จริง — ใช้ `$GEN/scripts/self_audit.py` เป็นเครื่องนับหลัก (นับอิสระ ไม่เชื่อ stamp):
| ตรวจ | วิธี | verdict ถ้าเจอ |
|---|---|---|
| px นอก spacing scale ใน padding/margin/gap | grep ค่า px ทั้งหมด เทียบ scale #50 | BLOCK (>5 จุด) / WARN (≤5) |
| inline layout style (`style="margin/padding/width`) | grep markup | BLOCK |
| `display:flex` ไม่มี `align-items` (ลูก>1) | grep คู่ property | WARN ราย selector |
| `display:grid` ไม่มี `gap` | grep คู่ property | WARN |
| ปุ่มร่วมแถวใช้ class ต่างระบบ / height ต่าง | ไล่ action rows | BLOCK |
| td ตัวเลขไม่ชิดขวา/ไม่มี tabular-nums | ไล่คอลัมน์เลข | WARN |
| card/drawer/modal padding หลายค่า | grep padding ของ container class | WARN |
| **ไม่มี `<!-- PREFLIGHT` stamp / stamp ไม่มีตัวเลข** | grep | **NOT-CHECKED = BLOCK** (v6.2 Rule #60) |
| **BASE-KIT ถูกแก้** (#69) | ตัด CSS ระหว่าง BASE-KIT markers เทียบ diff กับ `$GEN/templates/file-skeleton.template.html` | **BLOCK** — kit ต้อง verbatim |
| inline layout ทั้งที่มี `#page-late` | grep | **BLOCK** (#69 ปิดข้ออ้าง "จำเป็น" แล้ว) |
| Pattern A ไม่มี stat row ≥4 / chip counts / sortable headers (#70,#73) | grep class stat/chip/is-sortable + นับ | WARN (ขาด 1) / BLOCK (ขาด ≥2 ชั้น) |
| wizard ไม่มี summary ก่อน submit · drawer header ไม่เป็น identity block (#71,#72) | ไล่ markup | WARN |
| **ตัวเลขใน stamp ไม่ตรงกับการนับจริง** | รัน `$GEN/scripts/self_audit.py` ซ้ำ เทียบกับ stamp | **BLOCK** — stamp ปลอม/นับผิด = ไว้ใจ pre-flight ไม่ได้ทั้งไฟล์ |

### Pass D — Document Archetype (v9 Rules #98–#101 — บังคับเมื่อไฟล์เป็นเอกสารธุรกรรม)
ทริกเกอร์: ไฟล์มี `vat_mode` / `renderSignTab` / `line-tbl` หรือ archetype hint = Q · เกณฑ์ = `patterns/Q_*.md` + `patterns/B2_*.md` ใน `$GEN` (Sync Read — อย่าจำ)
| ตรวจ | วิธี | verdict |
|---|---|---|
| audit.sh ส่วน `doc_archetype` | รัน `$GEN/scripts/audit.sh` — FAIL ใด ๆ | BLOCK (คัดลอกบรรทัดลง report) |
| wizard 5 steps ชื่อ+ลำดับ (#100) | grep `renderStepperItem(` ทั้ง 5 ชื่อ: เลือกแหล่งที่มา › ข้อมูลหลัก › รายการสินค้า › เอกสารแนบ › ตรวจสอบและยืนยัน | สลับ/เปลี่ยนชื่อ = BLOCK · ตัด step 3 ได้เฉพาะไม่มี line items (ต้องมี log) |
| grid B2 v2 (#99) | th widths ใน `.line-tbl` = 26/—/64/92/92/78/72/104/54 · ไม่มีคอลัมน์เพิ่ม | BLOCK |
| แถวขยาย lean 1-line (#99) | `.line-expand-panel-inner` มี VAT segmented 3 ปุ่ม + % + หมายเหตุ · ไม่มี flex-wrap เป็นแถว 2 จริงในภาพ | BLOCK |
| VAT/discount engine | `calcLineVat/migrateLine/totals` ตรง `line-editor-v2.js.txt` (diff ตัว function) | ต่าง = BLOCK |
| totals order (#99) | renderLineSummary: ก่อน VAT → VAT → หลัง VAT → [WHT] → [ท้ายบิล] → [คูปอง] → สุทธิ | BLOCK |
| view tabs (#101) | `tabBtn` ลำดับ detail › [domain ≤2] › pdf › sign › history · ไม่มี tab attachments | BLOCK |
| เอกสารแนบใน landing | `SEC('paperclip', \`เอกสารแนบ` ใน renderDetailTab | BLOCK |
| header actions ตามสถานะ + divider + copy/printer/download/X (#98) | grep renderViewDrawer | WARN |
| list: docPill + renderSignProgress (#98) | grep | BLOCK |
| PDF `.a4` + 3 ช่องเซ็น · Sign `.tl` + `empChip` · submit modal `.slot-row` เลือกคน | grep + ภาพจาก Pass R | BLOCK |
| DOA hardcoded chain นอก mock | grep `approval_chain` ที่ไม่ใช่ seed | BLOCK |

### Pass R — Render Gate (บังคับเมื่อรันในเลน / env มี browser)
static analysis มองไม่เห็นความเบี้ยว — ต้องดูของจริง **หลักฐานเป็นไฟล์ภาพเท่านั้น**:
1. รัน `scripts/render_shots.py <file.html> <outdir>` (playwright) — จับทุก route + drawer/modal ที่เปิดได้
2. **ไม่มีไฟล์ภาพใน `_shots/` = NOT-CHECKED = BLOCK** — ห้ามสรุปจาก code แทนภาพเด็ดขาด
   (บทเรียน F-PRODUCT: AI ที่ถูกขอให้หาจุดเบี้ยวโดยไม่บังคับหลักฐาน จะถอยไป static analysis เสมอ)
3. ดูภาพทีละใบตาม Visual Checklist: แนวตรงมั้ย · ช่องไฟสม่ำเสมอ · กล่องล้น/หด ·
   ปุ่มร่วมแถวสูงเท่า · ฟอร์มคอลัมน์ตรง grid · ข้อความชนขอบ · จังหวะแนวตั้งคงที่ ·
   **density เทียบมาตรฐาน #63** (แถว list ~44px ไม่บวม) · **component ไม่ขอบชนกัน (#64)** ·
   **ความรวยตาม #70-73**: หน้า list เปิดมาต้องเห็น stat row + chips มีเลขนับ ไม่ใช่ตารางโล่ง ·
   **#74**: tab bar เส้นเดียว ไม่มีเส้นซ้อน/ไม่กระจุก · **#75**: ฟอร์มไม่มีช่องโหว่ง >24px /
   สถานะไม่ลอยท้ายฟอร์ม · **#76**: ขอบล่าง drawer ต้องไม่มี scrollbar แนวนอน (ซูมดูมุมล่างทุก drawer) ·
   **#77**: ทุก section มีข้อมูลตัวอย่างจริง ไม่มีช่องว่าง/placeholder เปล่า
3.1 **Bottom-Edge Test (#66 — บังคับ):** scroll ไปแถวล่างสุดของ list แล้วเปิด dropdown/เมนูที่อยู่ต่ำสุด
   → screenshot — เมนูต้อง flip ขึ้นบนหรือหดพร้อม scroll ห้ามจมใต้จอ · ทำซ้ำกับ select ใน drawer footer
3.14 **All-Tabs Test (#73.1):** คลิกทุก tab ทุก drawer → screenshot ทุก pane — tab เงียบ = BLOCK
3.15 **Sticky-vs-Overlay Test (#62.1):** scroll ตารางให้ sticky header ทำงาน → เปิด drawer/modal
   → screenshot — หัวตาราง/แถบ sticky ใด ๆ ต้อง**ไม่ทะลุ** overlay (เห็นพาดผ่าน = BLOCK)
3.2 **Dropdown Anatomy Test (#65 + #102):** เปิด**ทุก** search dropdown ในไฟล์ → screenshot — item 2 บรรทัด compact:
   คน = avatar → ชื่อ → ตำแหน่ง·แผนก · สินค้า = package icon → code·หมวด → ชื่อ → ราคา/ATP ขวา · ลำดับสลับ = BLOCK ·
   ทุก dropdown หน้าตาเดียวกัน (ต่างกัน = BLOCK) · เมนูลอยทับไม่ดันเนื้อหา (#95) · คลิกนอกเมนู → ต้องปิด (screenshot ก่อน/หลัง)
3.3 **Stable Screen Test (#35/#103):** เปิด/ปิด dropdown · toggle section · เปลี่ยน filter · เปิด drawer → screenshot ก่อน/หลัง
   ทับกัน — เนื้อหาใต้ overlay ต้องไม่ขยับ · ปุ่มด้านล่างไม่กระโดด · ไม่มี body h-scroll · scrollbar-gutter stable
3.4 **Viewport 1024 Test (#97):** screenshot ที่ 1024px — drawer `min(กว้าง,100vw)` ไม่ล้น · sidebar off-canvas/rail · B2 grid scroll ใน wrap ไม่ยุบคอลัมน์
3.5 **List Full-Height (#96):** หน้า list ที่ 1440×900 — ตารางชิดขอบล่าง viewport · scroll ใน `.table-wrap` · `.table-foot` ติดล่าง
3.6 **Golden Compare (Taste):** วาง screenshot คู่กับ golden reference ของ archetype (`$GEN/references/document-archetype/_SOURCE_so-reference.html` / `references/planner/` / `templates/reference/`) render ที่ viewport เดียวกัน — ความต่างเชิงโครง (ตำแหน่ง block, ลำดับ, density) = BLOCK · ต่างแค่ data = ผ่าน · ถ้ามี `TASTE_LOG.md` ในโฟลเดอร์งาน → ไล่ทุก item
4. ทุก finding ต้องอ้างชื่อไฟล์ภาพ + จุดในภาพ + บรรทัด CSS ที่เป็นเหตุ — ไม่มีภาพอ้าง = ไม่นับ
5. env ไม่มี browser จริง ๆ → mark `RENDER: UNAVAILABLE` ใน report — เลนถือเป็น BLOCK
   (ให้ไปรันใน Cowork/Claude Code ที่มี — ห้ามปล่อยผ่านเงียบ)

## Quality Gates ของตัว checker เอง

- [ ] Sync Read จาก html-generator เวอร์ชันสูงสุด (v9) สำเร็จ + จด version ลง report ทุกครั้ง · รัน `$GEN/scripts/audit.sh` ก่อนทุกอย่าง
- [ ] Pass D รันเสมอเมื่อไฟล์เป็นเอกสารธุรกรรม — ข้าม = NOT-CHECKED = BLOCK
- [ ] ทุก finding มีตำแหน่ง + วิธีแก้ concrete — ห้ามมี "ปรับให้สวยขึ้น/เรียบร้อยขึ้น" ลอย ๆ
- [ ] ไม่ report กฎที่ไม่ได้ตรวจจริงว่าผ่าน (unverified = NOT-CHECKED)
- [ ] Mechanical facts มาจาก script ไม่ใช่กะด้วยตา (กันตกหล่น hex/px ที่ซ่อนอยู่)
- [ ] Fix mode ต้อง diff เฉพาะจุด — ตรวจซ้ำหลังแก้เสมอ

## References

- `references/check-methods.md` — ตาราง map: fact จาก script → rule + severity + วิธีตัดสิน
- `references/report-format.md` — โครง _UX_CHECK_REPORT.md + ตัวอย่าง finding ที่ดี/แย่
- `scripts/static_scan.py` — mechanical scanner (รันได้เดี่ยว ๆ, output JSON)
