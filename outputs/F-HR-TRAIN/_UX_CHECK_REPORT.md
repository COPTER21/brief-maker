# UX Check Report — F-HR-TRAIN (อบรม / Training) · **รอบ re-gate #2 (หลังแก้ BUG-03 + BUG-04)**

- วันที่: 2026-09-03 · Iteration: 3 (re-gate #2) · ทับรายงานรอบก่อน (PASS)
- Generator spec: **html-generator-v9** (iron-rules #1–#49 · #94–#105 · Pattern Q/B2 v2/P) — Sync Read สำเร็จจาก `.claude/skills/html-generator-v9`
- Passes run: `audit.sh` · `static_scan.py` · `self_audit.py` · **Pass G** (geometry/stamp integrity) · **Pass R** (render จริง — จอเจาะจุด BUG-03/BUG-04 + regression BUG-01) · component consistency
- Pass D (Document Archetype Q/B2): **N/A** — `doc_archetype.is_document=false` · ไม่มี `vat_mode`/`renderSignTab`/`line-tbl` → archetype = master → ไม่ทริกเกอร์ (ถูกต้อง)
- ไฟล์ที่ตรวจ: `outputs/F-HR-TRAIN/อบรม.html`

## Verdict: 🟢 PASS (with 3 warnings)

| BLOCK | WARN | INFO | NOT-CHECKED |
|---|---|---|---|
| 0 | 3 | 3 | 0 |

**Gate = `audit.sh` FAIL=0** ✅ · render 3 จอเจาะจุด **0 pageerror / 0 console error·warning** · `bodyScrollX=false` ทุกจอ · **BUG-03 + BUG-04 ยืนยันแก้จริงด้วยหลักฐานภาพ+กลไก** · **ไม่มี regression** (BUG-01 ยังไม่ซ้อน)
ประเมินเวลาแก้: 0 นาที (WARN ทั้ง 3 เป็น judgment/re-stamp ไม่ใช่บล็อก)

---

## ✅ จุดที่เพิ่งแก้รอบนี้ — ยืนยันผล (หลักฐาน = ภาพใน `_shots/` + DOM probe)

### 🐛 BUG-03 · ปุ่ม "บันทึกผล" disabled ครอบ `<span class="tt-wrap" title=…>` เพื่อให้ tooltip โผล่ — FIXED ✓ · จอไม่เพี้ยน
- **โค้ด:** บรรทัด 2445–2446 (แถวผู้เรียน) + 2714/2718 (ตารางผล) — ปุ่มยัง `class="is-disabled" disabled`, span wrapper มี `title` (hover เห็น) + ปุ่มก็มี `title` เดิม
- **หลักฐานภาพ:** `_shots/REGATE2_learner_ttwrap.png` — ปุ่ม "บันทึกผล" (สถานะ disabled) อยู่แถวเดียวกับปุ่ม `X ยกเลิก` ของ สุนิสา แก้วมณี · ไม่ล้น ไม่เบี้ยว
- **DOM probe (geometry):** `wrapH=30 = btnH=30` → span wrapper **ไม่เพิ่มความสูง** · แถว `.lrn-act` ที่มี 2 ปุ่ม → children ทั้งคู่ `height=30` และ `top=368` เท่ากัน → **เรียงแถวเดียว ไม่ skew** · `btnDisabled=true` · tooltip title ครบทั้ง span + button
- **สรุป:** span wrapper ไม่ทำ layout ในแถวปุ่มเพี้ยน ✓

### 🐛 BUG-04 · modal ลงทะเบียน combobox **ไม่เด้งเปิด dropdown เอง** — FIXED ✓
- **โค้ด:** `tcOpenModal()` บรรทัด 2893 — หลัง `trapFocus` auto-focus ช่องแรก ถ้าเป็น `.ss-input` จะ `s.open=false` + เพิ่ม `.hidden` ให้ `ss-list-<key>` + `blur()` → กัน dropdown เด้งเอง (ไม่แตะ base-kit)
- **DOM probe (เปิด modal SE1):** `listOpen=false · listVisibleArea=0` → **dropdown ปิดอยู่ตอนเปิด modal** ✓ · `avatarsInOpts=7` · `svgIcons=10` (icon เรนเดอร์ครบ ไม่มีกล่องว่าง — FIX-06 ยังอยู่)
- **DOM probe (คลิก combobox เอง):** `open=true · opts=7 · avatars=7 · emptyAvatars=0` → เปิดได้ปกติเมื่อผู้ใช้คลิก · ทุก option มี avatar (ไม่ว่าง)
- **หลักฐานภาพ:** `_shots/REGATE2_enroll_modal_open.png` — เปิด modal มา ช่อง "ค้นหาพนักงาน…" เป็น placeholder เฉย ๆ ไม่มี list ร่วง · การ์ด gap ด้านบนมี avatar ธนกฤต ครบ · `_shots/REGATE2_enroll_combo_manual_open.png` = เปิด list ด้วยการคลิก

### 🐛 BUG-01 (regression check) · การ์ดอนุมัติ **ยังไม่ซ้อนกัน** — OK ✓
- **DOM probe (persona manager · SE1 · แท็บ approval):** 3 การ์ด `.secwrap` · tops/bottoms เรียงต่อเนื่อง (398<412 · 694<708) · `overlap=false`
- **หลักฐานภาพ:** `_shots/REGATE2_approval_cards.png` — 3 กล่องแยกอิสระ ช่องไฟสม่ำเสมอ ไม่ nest/ไม่ทับ

---

## 🟡 WARN

### UX-03 · Pass G · PREFLIGHT stamp drift — `missing_ids` (0 → 1) · false-positive · **แนะนำ re-stamp**
- **พบ:** stamp (บรรทัด 3019) ระบุ `missing_ids=0` แต่ `self_audit.py` รันสดได้ `missing_ids=1 → ['ss-list-']`
- **ต้นเหตุ:** การแก้ **BUG-04** บรรทัด 2893 เพิ่ม `document.getElementById('ss-list-'+key)` — regex ของ scanner จับ prefix สแตติก `ss-list-` เป็น "id ที่ต้องการ" แต่ element จริงใช้ id แบบต่อสตริง (`id="ss-list-'+key+'"` บรรทัด 1812) → **element มีจริง** = scanner false-positive
- **ทำไมไม่ BLOCK:** (1) `audit.sh` = **FAIL=0** (gate ทางการผ่าน) · (2) counter อีก 8 ตัวใน stamp **ตรงเป๊ะทุกตัว** (spacing 28 · font 3/11 · flex 2 · inline 36 · hex 5 · stopprop 3 · long_banners 15 · custom_tabs 3) → ตราไม่ได้ปลอมทั้งไฟล์ · (3) ตรวจสดยืนยัน element `ss-list-<key>` ถูกสร้างจริง (บรรทัด 1812) → ไม่มี dead ref จริง
- **วิธีปิด:** อัปเดต stamp เป็น `missing_ids=1` พร้อมโน้ต FP (`ss-list-` = getElementById ต่อสตริง element มีจริง) — เป็น doc drift 1 บรรทัด ไม่ใช่บั๊กโค้ด

### UX-01 · Pass R Geometry (#40/#103) · tab `หลักสูตร` แถวชื่อหลักสูตรยาว *(ยกจากรอบก่อน · ยังคง)*
- ชื่อ "ความปลอดภัยในการทำงาน (จป. ระดับหัวหน้างาน)" wrap 2 บรรทัด + sub-line รหัส → แถวสูง ~82px (>64) · แถวอื่นปกติ
- **ของจริงแต่เบา:** โครงเซลล์ถูกตาม #103 (บรรทัดรอง = meta ของหลักสูตรเดียวกัน) · สูงเพราะเนื้อหา ไม่ใช่โครงผิด → ไม่ BLOCK · BA เคาะว่ายอมให้ wrap ได้ไหม (ทางแก้: `-webkit-line-clamp:1` + `title`)

### UX-02 · H-Microcopy / #81 tension · แท็บรายงาน + drawer อนุมัติ + result modal *(ยกจากรอบก่อน · ยังคง)*
- ศัพท์เชื่อมระบบภายในบนจอ: `hook`, `EC`, `CSQ`, `[OB-1]/[OB-2]`, `(NTF)`, `display-only`, `soft ref`
- **WARN ไม่ใช่ BLOCK:** `jargon_leak=0` (regex #81 ไม่จับ) · คำมาจากมติที่ล็อกไว้ = annotation ตั้งใจให้ BA/dev เห็นสัญญาข้ามโมดูล → BA เคาะว่า UI จริง persona `ผู้ชมทั่วไป` ตัดออกหรือคงไว้

---

## ℹ️ INFO (เอกสารรับรู้แล้ว · ไม่แตะ)

- **audit.sh WARN=3** — base-kit inherited: #21 (`<i data-lucide>` มี CSS sizing) · #40 (`.uc-email` sub-line = user-cell meta) · Token (font-size sidebar hardcode ใน BASE-KIT) — ห้ามแก้ base-kit (#69)
- **off-whitelist hex 2 ค่า:** `#B4B6BB` / `#C7C9CE` ที่ `.demo-strip` (persona control บน charcoal sidebar) = prototype scaffolding · business hex บนพื้นจอ = 0 · `#103/#104/#105` = false-positive (เลขกฎในคอมเมนต์)
- **self_audit.py = FAIL** เป็นปกติของ base-kit นี้ (มติ "self_audit ไม่ zero-tolerance · gate = audit.sh") — residual declare ใน stamp · counter 8 ตัวตรง stamp (missing_ids drift = UX-03)

---

## Pass G — Stamp Integrity

รัน `self_audit.py` เทียบ PREFLIGHT stamp (บรรทัด 3016–3026):

| counter | stamp | self_audit จริง | ตรง? |
|---|---|---|---|
| spacing_off | 28 | 28 | ✓ |
| font_off / font_count | 3 / 11 | 3 / 11 | ✓ |
| flex_noalign | 2 | 2 | ✓ |
| inline_layout | 36 | 36 | ✓ |
| hex_off | 5 | 5 | ✓ |
| stopprop_blanket | 3 | 3 | ✓ |
| long_banners | 15 | 15 | ✓ |
| custom_tabs | 3 | 3 | ✓ |
| **missing_ids** | **0** | **1** (`ss-list-` = FP จาก BUG-04) | ✗ → **UX-03 (WARN, re-stamp)** |

→ 8/9 counter ตรง · ตัวที่เพี้ยนเป็น false-positive ที่พิสูจน์แล้ว → ตราไม่ปลอมทั้งไฟล์ → **ไม่ BLOCK**

---

## Render Gate — screenshots (`outputs/F-HR-TRAIN/_shots/`)

จอ re-gate #2 (0 error): `REGATE2_learner_ttwrap` (BUG-03 · ปุ่ม disabled ใน span) · `REGATE2_enroll_modal_open` (BUG-04 · dropdown ปิดตอนเปิด) · `REGATE2_enroll_combo_manual_open` (คลิกเปิดเอง avatar ครบ) · `REGATE2_approval_cards` (BUG-01 · ไม่ซ้อน)
Runtime: **0 pageerror · 0 console error/warning** · `bodyScrollX=false` ทุกจอ

## เครื่องนับ (อ้างอิง)
- `audit.sh`: **FAIL=0 · WARN=3** (base-kit inherited) → GATE PASS
- `self_audit.py`: FAIL (natural base-kit) · 8/9 ตรง stamp · missing_ids=1 (FP → UX-03)
- `static_scan.py`: `doc_archetype.is_document=false` · `portal_menu=true` · `overlay_root=true` · `select_big=0` · `td_multi_pill=0` · 540px legacy=0

## ⬜ NOT-CHECKED
- ไม่มี — ทุกหมวดที่บังคับ (mechanical + Pass G + Pass R) รันครบพร้อมหลักฐานภาพ
