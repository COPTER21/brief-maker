# _UX_CHECK_REPORT — F-MKT-CONSENT · ความยินยอม PDPA (F058)

> WF-01 **step 3** · skill `qc-ux-html-checker` — ตรวจ "ทำ**ถูก**มั้ย" (form / iron-rules / CI / UX heuristics)
> ไฟล์: `outputs/F-MKT-CONSENT/consent-pdpa.html`
> วันที่ตรวจ: 2026-09-11 · **รอบ 7 (loop mode)** — re-run หลัง **2 fixes**: (1) `.up-zone` เพิ่ม `display:block` (label เดิม inline ทำให้กล่อง dropzone เพี้ยน) · (2) "อ่านเอกสาร" เปลี่ยนจากปุ่มเป็นลิงก์ `.doc-link` (สีหลัก + file icon + ชื่อไฟล์ + underline on hover) 3 จุด

---

## VERDICT: ✅ PASS with 4 warnings (BLOCK = 0)

**BLOCK = 0 · WARN = 4 (residual เดิมทั้งหมด — 2 fixes ไม่สร้างอันใหม่) · INFO = 3**
`audit.sh` (ด่านชี้ขาด) = **FAIL=0 · WARN=5** — ตรง 5 residual ที่จดไว้ทุกตัว ไม่มี blocker ใหม่

**2 fixes — ยืนยันด้วยภาพสด (1280 + 1024) + วัด DOM จริง ทุกจุดผ่าน:**
- **Fix 1 · Upload dropzone** ✅ — `.up-zone` (เดิมเป็น `<label>` ที่ไม่มี display) วัด `display=block` แล้วทั้ง 1280+1024 · กล่อง dashed กึ่งกลางจริง (622×129, `border-style:dashed`, `text-align:center`) · icon upload-cloud + "อัปโหลดเอกสาร PDPA" + hint ครบ · หลัง mock upload → `.up-file` chip สะอาด (teal file icon + ชื่อไฟล์ + type·size + ปุ่ม "เปลี่ยนไฟล์") · ครบทั้ง สร้างวัตถุประสงค์ + modal "ออกเวอร์ชันใหม่"
- **Fix 2 · Read-document เป็นลิงก์** ✅ — `.doc-link` render เป็นสีหลัก (`rgb(255,59,48)`) · `background:transparent` · `border:none` · มี file icon + ชื่อไฟล์ · underline on hover — อ่านเป็นลิงก์ ไม่ใช่ปุ่ม · ครบทั้ง 3 จุด (create-request rows · req-view "เนื้อหาที่ให้เซ็น" · purpose-view version list) · คลิก → เปิด document viewer modal ลอย**เหนือ** drawer (z=60 > 55, DSP-01) · **create-request row ไม่ toggle checkbox** (row `is-on` = false ทั้งก่อน/หลังคลิก → stopPropagation ทำงาน)

---

## Sync Read (Phase 0)
- Generator: **html-generator-v9** (`.claude/skills/html-generator-v9`) — iron-rules ติดตั้งจริง **#1–#103**
- อ่าน: `iron-rules.md` · `layout-integrity.md` · `component-contracts.md` · `page-anatomy.md` · `ci-tokens.md` · `microcopy.md` + scripts `audit.sh`/`self_audit.py`
- กฎ **#104–#106** ที่ SKILL.md ของ qc-ux อ้าง **ไม่มีในตัว generator v9 ที่ติดตั้ง (#1–#103)** → **NOT-APPLICABLE**

## Archetype
- `doc_archetype.is_document = false` → ไม่ใช่เอกสารธุรกรรม (Q) → **Pass D ไม่ทริกเกอร์** ✅
- master/list + resolver + recipient surface · single-screen create (ไม่มี wizard stepper) → สอดคล้อง LOCK-07 (ห้าม Pattern Q)

---

## ⭐ จุดโฟกัสรอบนี้ — ยืนยัน 2 fixes (RENDER + measure)

หลักฐานภาพ: `scratchpad/_shots/` — render สด 1280×900 และ 1024×768 + วัด getComputedStyle / class / z-index ด้วย DOM eval

### Fix 1 · `.up-zone{display:block}` — dropzone อัปโหลดเอกสาร ✅
- CSS บรรทัด 1373: `.up-zone{ display:block; border:1.5px dashed …; text-align:center; … }` · markup = `<label class="up-zone" for="…">` (บรรทัด 2848) — label default `inline` จึงต้อง `display:block` ให้กล่อง dashed + เนื้อห ากึ่งกลางเรนเดอร์ถูก
- **วัด DOM (ทั้ง 1280 + 1024):** `upzone_display=block` · `upzone_tag=label` · box `622×129` · `border-style=dashed` · `text-align=center` · `up-t="อัปโหลดเอกสาร PDPA"` · `up-s="รองรับ .pdf .doc .docx .txt — คลิกเพื่อเลือกไฟล์ (ต้นแบบ)"` · icon present
- **หลัง mock upload → `.up-file` chip:** `upfile_present=true` · name แสดง · meta = `type·size` · ปุ่ม "เปลี่ยนไฟล์" present
- **modal "ออกเวอร์ชันใหม่":** `nv_upzone=true` · `nv_upzone_display=block` · หลัง upload → `.up-file` present + warn-banner "ความยินยอม N รายการจะไม่ครอบคลุมเวอร์ชันใหม่"
- **ภาพ:** `d1280_01_create_dropzone.png` (dashed box กึ่งกลาง สะอาด) · `d1280_02_create_upfile_chip.png` (chip teal + "เปลี่ยนไฟล์") · `d1280_04_newversion_upfile.png` (modal ออกเวอร์ชัน v3) · `d1024_01_create_dropzone.png` (drawer พอดี viewport 1024, sidebar → hamburger)

### Fix 2 · read-document เป็นลิงก์ `.doc-link` ✅
- CSS บรรทัด 1389–1391: `.doc-link{ display:inline-flex; …; background:none; border:0; padding:0; color:var(--c-primary); font-weight:600; cursor:pointer; }` + `:hover{ text-decoration:underline }` + icon 14px
- **วัด DOM:** `tag=button` (semantic ปุ่ม แต่ **style เป็นลิงก์**) · `color=rgb(255,59,48)` (primary) · `background=rgba(0,0,0,0)` · `border=none` · มี file icon + ชื่อไฟล์ · underline เฉพาะ hover
- **3 จุด — ยืนยัน render:**
  - (a) **create-request purpose rows** (บรรทัด 2652, `onclick="event.stopPropagation(); viewPolicy(...)"`) → ลิงก์ "นโยบาย-PUR-0x-vN.pdf" ใต้ชื่อวัตถุประสงค์ + checkbox แยกซ้าย · **ภาพ** `d1280_05_createreq_doclink.png`
  - (b) **req-view "เนื้อหาที่ให้เซ็น (BR-06)"** (บรรทัด 2686) → ลิงก์ 2 อัน + "— เอกสารที่เจ้าของข้อมูลเห็นตอนเซ็น" · **ภาพ** `dbg_reqview.png`
  - (c) **purpose-view version list** (บรรทัด 2882) → ลิงก์ต่อเวอร์ชัน (v2 ปัจจุบัน / v1 เก่า) · **ภาพ** `dbg_purview.png`
- **คลิก → เปิด document viewer modal:** เปิดสำเร็จทั้ง 3 จุด (`policy_modal_open_from_createreq/reqview/purview = true`) · modal = header ชื่อวัตถุประสงค์ + version·date·docName → info-banner BR-06 → `.doc-meta` → `.doc-frame` (body) · **ภาพ** `d1280_06_policy_over_createreq.png`
- **DSP-01 (modal เหนือ drawer):** วัด `z_modal=60` (`--z-portal`) > drawer 55 · backdrop dim drawer · modal อยู่กลาง ไม่ถูก drawer บัง
- **stopPropagation ที่ create-request row:** row class `is-on` = **false ทั้งก่อนและหลังคลิกลิงก์** → คลิกชื่อเอกสาร **ไม่ toggle checkbox** ✅ (row มี `onclick="toggleReqPurpose(...)"` บรรทัด 2649 — ลิงก์กัน bubble สำเร็จ)
- **Esc chain:** Esc ปิด modal ก่อน · drawer ยังเปิด (`drawer_still_open_after_esc=true`) — ลำดับถูก

---

## Phase 1 — Mechanical Scan

### audit.sh (ด่านชี้ขาด) → FAIL=0 · WARN=5 — residual เดิมทั้งหมด (ไม่ re-flag ตามข้อกำกับ)
| # | WARN | สถานะ |
|---|---|---|
| Rule #21 | `<i data-lucide>` บางตัวไม่มี class `w-/h-` (brand 1675 + combobox/empty helpers) | documented residual |
| Rule #40 | `.uc-email` sub-line ในเซลล์ (บรรทัด 696) | documented residual |
| Token | hardcoded font-size บรรทัด 82/129/130/145/168 (BASE-KIT) | documented residual |
| Rule #44 | submit ไม่มี loader-2 (mock submit synchronous) | documented residual |
| Rule #103/#40 | บรรทัด 2530 = pill 2 ตัว | **false-positive** — ternary เลือก pill เดียว (ใช้งาน/ปิดแล้ว) · เดิมอยู่บรรทัด 2527 เลื่อนเพราะ CSS `.doc-link` แทรก |

> WARN ทั้ง 5 ตัวเป็น residual ประเภทเดิมทุกรอบ (round 1–6) — 2 fixes ไม่เพิ่ม/ไม่ทำให้แย่ลง

---

## Fix list (WARN — ไม่บล็อก gate · ยกมาจากรอบก่อน · **อยู่นอกขอบเขต 2 fixes** · ไม่แย่ลง)

| id | severity | rule ref | ตำแหน่ง | พบอะไร | วิธีแก้ (concrete) |
|---|---|---|---|---|---|
| **UX-04** | WARN (คงเดิม) | H-overlay / #66 | `.demo-strip` vs `.dw-footer-left` ที่ viewport ≤1024 | demo-strip (z=90) ทับปุ่มซ้ายสุดของ footer ~30px ในบาง drawer — ไม่เกี่ยวกับ 2 fixes | ซ่อน/ย่อ demo-strip เมื่อ drawer เปิด (`body.drawer-open .demo-strip{display:none}`) |
| UX-01 | WARN | H-CI (token drift) | `.rz-json`/`.http-chip` (code viewer) | code-viewer ใช้ hex นอก whitelist | ยอมรับได้ในฐานะ code block — ถ้าเก็บ ย้ายเป็น `--code-*` |
| UX-02 | WARN | H-CI (token drift) | `.warn-banner` | banner ใช้สีใกล้ family แต่ไม่ตรง token | ปรับ text→`var(--c-warning)` |
| UX-03 | WARN | Pass G (numeric align) | tab วัตถุประสงค์ คอลัมน์ "อายุ (เดือน)" + "% ครอบคลุม" | ตัวเลขไม่ชิดขวา/ไม่มี tabular-nums | ใส่ `text-align:right; font-variant-numeric:tabular-nums;` |

## INFO (ไม่ต้องแก้)
- policy modal + info-banner ใช้สี info-blue inline (family เดียวกัน consistent) — ไม่ใช่ token drift ใหม่
- `.doc-link` semantic เป็น `<button>` (ถูกต้องเพื่อ a11y/keyboard) แต่ style เป็นลิงก์ — ตรงตามเจตนา fix
- **PREFLIGHT stamp เปล่า** (บรรทัด ~2098 ยังเป็น template `_`) · gate ชี้ขาด = audit.sh (ไม่ตรวจ stamp) → ไม่บล็อก · แจ้งไว้ให้ผู้เขียน HTML กรอกตัวเลขจาก self_audit.py หากต้องการปิดช่องนี้

## NOT-CHECKED
- iron-rules #104–#106 — ไม่มีใน generator v9 ที่ติดตั้ง → ไม่นำมาตัดสิน

---

## สรุปสำหรับ WF-01
- **ผ่าน step 3** (BLOCK=0) — 2 fixes ยืนยันครบด้วยภาพสด 1280+1024 + วัด DOM:
  - **Fix 1 · Upload dropzone** ✅ `.up-zone` วัด `display=block` · กล่อง dashed กึ่งกลาง (icon + "อัปโหลดเอกสาร PDPA" + hint) · หลัง upload → `.up-file` chip สะอาด · ครบทั้งสร้างวัตถุประสงค์ + modal ออกเวอร์ชันใหม่
  - **Fix 2 · Read-document เป็นลิงก์** ✅ `.doc-link` primary color + file icon + ชื่อไฟล์ · 3 จุด (create-request · req-view · purpose-view version list) · คลิก → เปิด viewer modal เหนือ drawer (z60>55, DSP-01) · create-request row **ไม่ toggle checkbox** (stopPropagation ทำงาน)
- **ไม่พบ issue ใหม่** — z-tier ถูกลำดับ · ไม่มี layout shift · Esc chain ถูก
- **ไม่พบ regression** — audit.sh FAIL=0 · WARN 5 residual เดิม · ไม่มี WARN ใหม่
- WARN 4 ตัว (UX-01/02/03 cosmetic + UX-04 overlap 1024) เป็นของเดิม non-blocking นอกขอบเขต 2 fixes — ให้ผู้ใช้ตัดสินว่าจะเก็บก่อนส่ง dev หรือปล่อย
