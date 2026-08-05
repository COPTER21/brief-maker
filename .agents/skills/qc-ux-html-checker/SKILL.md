---
name: qc-ux-html-checker
description: "Quality Gate หลัง html-generator-v6 — ตรวจ HTML prototype ว่า 'ทำถูกมั้ย' เชิง form: iron rules ทั้งหมดของ v6 (Sync Read จาก html-generator-v6 เป็น authoritative — ไม่ copy กฎมาเก็บเอง), CI tokens/Warm Light, component consistency, และ UX heuristics (empty/loading/error state, Esc chain, disabled, destructive confirm, microcopy) แล้วออก _UX_CHECK_REPORT.md เป็น fix list ระบุตำแหน่ง + วิธีแก้ราย item ให้ vibe แบบมีเป้า มี loop mode diff กับรอบก่อน + fix mode แก้ surgical เฉพาะรายการ ใช้เมื่อ user พูดถึง 'qc-ux-html-checker', 'ตรวจ UX', 'เช็ค HTML', 'ตรวจ iron rules', 'HTML ตรง CI มั้ย', 'ux gate', 'ตรวจก่อนส่ง', 'review HTML', 'ตรวจ component', 'fix list', 'HTML เรียบร้อยยัง', 'vibe check' — ใช้ทุกครั้งหลัง gen หรือ vibe HTML เสร็จ ก่อนไปขั้น RIF/เอกสาร แม้ user ไม่เรียกชื่อ skill ตรง ๆ Input: ไฟล์ .html (+ report รอบก่อนถ้าวน loop) Output: _UX_CHECK_REPORT.md + verdict PASS/WARN/BLOCK ห้ามใช้ตรวจความครบของ business scope — นั่นคืองาน qc-coverage-checker"
---

# QC: UX HTML Checker

## Purpose

ด่านตรวจ "ทำ**ถูก**มั้ย" (form) ของ HTML prototype — จับ violation เชิง CI/iron rules/
UX แล้วแปลงเป็น **fix list ที่ชี้ตำแหน่ง + บอกวิธีแก้** เพื่อให้การ vibe มีเป้าชัด
จบเร็ว ไม่วนตามความรู้สึก

ไม่ตรวจความครบของ business scope (edges, golden rules, exception paths) —
นั่นคืองานของ `qc-coverage-checker` สองตัวนี้แยกกันเพื่อให้ ux loop วนเร็วโดยไม่ต้องแบก graph

## หลักการสำคัญ: Single Source of Truth

**ห้ามเก็บ iron rules ไว้ใน skill นี้** — ตัวกฎอยู่ที่ `html-generator-v6` เท่านั้น
skill นี้เก็บแค่ "วิธีตรวจ" ทุก run ต้อง Sync Read:

| ไฟล์ (ใน html-generator-v6) | ใช้ตรวจ |
|---|---|
| `knowledge/iron-rules.md` | กฎทั้งหมด (48-49 ข้อ ณ v3.13 — อ่านจำนวนจริงจากไฟล์) |
| `knowledge/ci-tokens.md` | hex whitelist, CSS vars, fonts, spacing |
| `knowledge/microcopy.md` | ถ้อยคำมาตรฐาน ปุ่ม/empty/error |
| `knowledge/component-catalog-ref.md` | component pattern ที่ต้อง consistent |
| `references/drawer-standard/README.md` | spec drawer 920/680 |

ถ้า html-generator-v6 ไม่ได้ติดตั้ง → หา `html-generator-v*` เวอร์ชันสูงสุดที่มี
ถ้าไม่มีเลย → แจ้ง user และตรวจได้เฉพาะหมวด UX heuristics (ระบุใน report ชัดว่า
iron rules = NOT-CHECKED)

## Input

| Input | จำเป็น | หมายเหตุ |
|---|---|---|
| ไฟล์ .html | ✅ | output จาก html-generator-v6 หรือไฟล์ที่ vibe แก้แล้ว |
| `_UX_CHECK_REPORT.md` รอบก่อน | loop mode | ให้ diff fixed/remaining/new |
| NODE_BRIEF | optional | ใช้แค่รู้ชื่อ feature/route — ไม่ใช้ตรวจ scope |

---

## Workflow

### Phase 0 — Sync Read

อ่านไฟล์ authoritative ตามตารางข้างบน + สร้าง checklist สดจาก iron-rules.md
(จำนวนกฎ/เลขกฎ ยึดตามไฟล์ ไม่ยึดตามความจำ) — จด version ของ generator ที่อ่านลง report

### Phase 1 — Mechanical Scan (script)

รัน `scripts/static_scan.py <file.html>` → ได้ JSON facts: hex ทั้งหมดที่ใช้ (พร้อมจำนวน),
font-families, px widths ที่เจอ, icon usage, hash routing, Esc handler, scrollbar css,
localStorage, emoji, ฯลฯ แล้ว**ตีความเทียบกับ tokens/rules ที่ Sync Read มา**:

- hex ที่ไม่อยู่ใน ci-tokens whitelist → BLOCK (ระบุ hex + จำนวนครั้ง + บรรทัดตัวอย่าง)
- font-family นอก stack → BLOCK
- เจอ `540px` drawer legacy → BLOCK (Rule #11)
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
5. **List/Table UX** — cell atomicity, row=view, long-list UX (#40-42)

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
Sync Read `html-generator-v6/knowledge/layout-integrity.md` (#50-#62) + `component-contracts.md` (#63-#68) + `page-anatomy.md` (#70-#73) + contracts #74-#80 + Block-First แล้วตรวจเชิงกล (audit v4: +img_placeholders) · เคสที่มี block ใน templates/blocks/ → เทียบว่าโครง markup มาจาก block จริง — ใช้ `html-generator-v6/scripts/self_audit.py` เป็นเครื่องนับหลัก (นับอิสระ ไม่เชื่อ stamp):
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
| **BASE-KIT ถูกแก้** (#69) | ตัด CSS ระหว่าง BASE-KIT markers เทียบ diff กับ `html-generator-v6/templates/file-skeleton.template.html` | **BLOCK** — kit ต้อง verbatim |
| inline layout ทั้งที่มี `#page-late` | grep | **BLOCK** (#69 ปิดข้ออ้าง "จำเป็น" แล้ว) |
| Pattern A ไม่มี stat row ≥4 / chip counts / sortable headers (#70,#73) | grep class stat/chip/is-sortable + นับ | WARN (ขาด 1) / BLOCK (ขาด ≥2 ชั้น) |
| wizard ไม่มี summary ก่อน submit · drawer header ไม่เป็น identity block (#71,#72) | ไล่ markup | WARN |
| **ตัวเลขใน stamp ไม่ตรงกับการนับจริง** | รัน `html-generator-v6/scripts/self_audit.py` ซ้ำ เทียบกับ stamp | **BLOCK** — stamp ปลอม/นับผิด = ไว้ใจ pre-flight ไม่ได้ทั้งไฟล์ |

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
3.2 **Dropdown Anatomy Test (#65):** เปิด search dropdown → screenshot — item ต้อง 2 บรรทัด compact
   (avatar+ชื่อ+รอง+meta) ไม่อ้วน · คลิกนอกเมนู → ต้องปิด (screenshot ก่อน/หลัง)
4. ทุก finding ต้องอ้างชื่อไฟล์ภาพ + จุดในภาพ + บรรทัด CSS ที่เป็นเหตุ — ไม่มีภาพอ้าง = ไม่นับ
5. env ไม่มี browser จริง ๆ → mark `RENDER: UNAVAILABLE` ใน report — เลนถือเป็น BLOCK
   (ให้ไปรันใน Cowork/Claude Code ที่มี — ห้ามปล่อยผ่านเงียบ)

## Quality Gates ของตัว checker เอง

- [ ] Sync Read สำเร็จ + จด generator version ลง report ทุกครั้ง
- [ ] ทุก finding มีตำแหน่ง + วิธีแก้ concrete — ห้ามมี "ปรับให้สวยขึ้น/เรียบร้อยขึ้น" ลอย ๆ
- [ ] ไม่ report กฎที่ไม่ได้ตรวจจริงว่าผ่าน (unverified = NOT-CHECKED)
- [ ] Mechanical facts มาจาก script ไม่ใช่กะด้วยตา (กันตกหล่น hex/px ที่ซ่อนอยู่)
- [ ] Fix mode ต้อง diff เฉพาะจุด — ตรวจซ้ำหลังแก้เสมอ

## References

- `references/check-methods.md` — ตาราง map: fact จาก script → rule + severity + วิธีตัดสิน
- `references/report-format.md` — โครง _UX_CHECK_REPORT.md + ตัวอย่าง finding ที่ดี/แย่
- `scripts/static_scan.py` — mechanical scanner (รันได้เดี่ยว ๆ, output JSON)
