# _UX_CHECK_REPORT — F-HR-RECRUIT · สรรหา (Recruit)

> Step 3 · WF-01 — ตรวจ "ทำถูกมั้ย" (form / iron rules / UX / CI)
> Skill: `qc-ux-html-checker` (check mode · re-run หลังแก้ FIX-01..07 จากใบสั่ง BA) · Generator (Sync Read): **html-generator-v9** (BASE-KIT v6.4)
> Target: `outputs/F-HR-RECRUIT/สรรหา.html` (2870 บรรทัด · เดิม 2837 · +33 จาก 7 fix)
> archetype: **master + kanban** (ไม่ใช่ Pattern Q เอกสารธุรกรรม) → Pass D = N/A
> วันที่ตรวจ: 2026-09-03 (รอบ re-run หลัง FIX-01..07) · env: Windows (python + PYTHONIOENCODING=utf-8)

---

## VERDICT: 🟢 PASS with 4 warnings — 0 blocker · 4 WARN · 2 INFO  (ดีขึ้น: WARN ลด 1 · ไม่ถอยจากเดิม)

| ระดับ | จำนวน | สรุป |
|:--:|:--:|---|
| **BLOCK** | **0** | — (ไม่มี blocker · 7 fix ไม่สร้าง blocker ใหม่) |
| WARN | 4 | token purity residual (demo-strip grays) · off-scale font/spacing · inline layout |
| INFO | 2 | stage color hardcode ใน JS · lucide missing w/h class |

**เทียบรอบก่อน:** เดิม PASS · 5 WARN documented → **รอบนี้ PASS · 4 WARN** — verdict ไม่ถอย + **WARN หายไป 1 (UX-06 submit loader) เพราะ FIX-07** · ไม่มี WARN/INFO ใหม่จาก 7 fix

### เครื่องนับ (mechanical · รันจริงรอบ re-run)
- **`audit.sh` = FAIL 0 · WARN 3** ✅ (เดิม WARN 4 → **ลดเหลือ 3 · Rule #44 submit loader หายจาก FIX-07**)
  - WARN 3 คงเหลือ = #21 lucide missing w/h · #40 uc-email sub-line (person cell meta ที่ยอมรับ) · hardcoded font-size — residual เดิมทั้งหมด ไม่เกี่ยว 7 fix
  - **#44 (submit ไม่มี loading state) = หายแล้ว** — FIX-07 ใส่ `loader-2` + `spin` บนปุ่ม `submitReq`/`submitCand` ตอน `RC.busy`
- **`self_audit.py`** — 6 counter หลักตรง stamp เป๊ะ: `spacing-off=29 · font-sizes=12 · flex-noalign=3 · inline-layout=29 · z-adhoc=0 · hex-off=5` (RESULT=FAIL เป็น baseline ปกติของ archetype — gate จริงคือ `audit.sh FAIL=0`)
- **Render Gate (Pass R):** `render-check.py` + chromium หน้า list → **สะอาด ไม่มี regression** (ดู Pass R)

---

## 🎯 การแก้รอบนี้ — FIX-01..07 (จากใบสั่ง BA) · ยืนยันแล้วไม่มี issue ใหม่

ทุก fix ตรวจแล้ว: มีจริง · surgical · ไม่แตะ BASE-KIT/mock/z-index-fix เดิม · ไม่เพิ่ม hex/font/inline/z-adhoc (6 counter ตรง stamp)

| FIX | จุดแก้ | ตรวจ | ผล |
|---|---|---|---|
| **FIX-01** board guard → `candHireHandoff` | fn บรรทัด 2771 · route เดียวทั้งระบบ (2755–2758 บล็อก skip ไป hired ตรง ๆ) | เส้นทาง hire รวมเป็น 1 · ต้องตอบรับ offer ก่อน | ✅ สะอาด |
| **FIX-02** viewer read-only + ซ่อนปุ่มสร้าง | `viewerRO()` guard 15 จุด (2288) · persona `viewer` (2132) · ปุ่มสร้างมี `RC.persona!=='viewer'` guard (2325–2326) | mutation guard ครบ · ปุ่ม business ซ่อนถูกจังหวะ | ✅ สะอาด · viewer โผล่ใน demo-strip (Pass R) |
| **FIX-03** ลบ copy PDPA "ไม่มีวันหมดอายุ" + retention display-only | grep `ไม่มีวันหมดอายุ` = 0 hit (ลบแล้ว) | copy หายจริง | ✅ สะอาด |
| **FIX-04** CSS ปุ่ม ← บอร์ด | class-based (ไม่เพิ่ม inline · inline-layout=29 คงที่) | ไม่กระทบ counter | ✅ สะอาด |
| **FIX-05** validation field-level `markInvalidFields` | fn 1913 · toggle class `.is-invalid` → `border-color:var(--c-danger)` (CSS 1186–1188) · focus ตัวแรก · เรียกจาก submitReq/submitCand (2544/2629) | ใช้ CI token · ไม่มี inline · ไม่ leak jargon (jargon_leak=0) | ✅ สะอาด |
| **FIX-06** `setCandTab` fallback | 2491 — whitelist `['detail','assess','offer','history']` fallback → `detail` | กัน tab id เพี้ยน | ✅ สะอาด |
| **FIX-07** loader-2 บนปุ่ม submit | 2534/2619 — `loader-2`+`spin` เมื่อ `RC.busy` · `w-4 h-4` class ครบ | **แก้ WARN #44 หาย** · ไม่เพิ่ม #21 (มี w/h) | ✅ สะอาด · WARN ลด 1 |

**ไม่แตะ z-index fix เดิม:** `z-adhoc=0` คงที่ · การแก้ modal-เหนือ-drawer รอบก่อนยังอยู่ครบ

---

## ✅ PREFLIGHT stamp — ครบ ไม่ใช่ `_` · ตัวเลขตรงการนับจริง (บรรทัด 2857–2869)

```
round1: spacing-off=29 font-sizes=12 flex-noalign=3 inline-layout=29 z-adhoc=0 hex-off=5
round2: 7/7 checked · date: 2026-09-02 · RESIDUALS documented (accepted)
```
- ตรามีตัวเลขจริงครบทุกช่อง · **self_audit.py รอบ re-run ตรง stamp ทุกช่อง** (7 fix ไม่ขยับ counter) ✅
- `z-adhoc=0` ยังถูก (7 fix ใช้ class/token ไม่มีเลข z ดิบ) · หมายเหตุ: stamp date=2026-09-02 (จากรอบ z-index) — เนื้อ counter ไม่เปลี่ยน จึงไม่ต้อง re-stamp (checker ห้ามแก้ HTML)

---

## 🟡 WARN (residual เดิม — ยอมรับได้ · ไม่บล็อก · ไม่เกี่ยว 7 fix)

### UX-02 · Token purity — residual demo-strip
`.demo-strip .ds-lbl`(#B4B6BB) · `.ds-seg button`(#C7C9CE) — gray text บน charcoal sidebar ของ persona-switch (#105 prototype scaffolding) · ไม่ใช่ business surface → residual (documented ในตรา) · hex บน business UI = 0

### UX-03 · Off-scale font-size (residual · #61)
`.tab 13.5px` · `.kc-sub 11.5px` · `.band-seg .bl 10.5px` · demo-strip `11.5px` — compact component · Pass R สะอาด

### UX-04 · Off-scale spacing (residual · #50)
spacing_off=29 (7·9·11·13·14·15) ใน compact component — Pass R ไม่พบภาพเพี้ยน

### UX-05 · Inline layout styles (residual · #69)
inline_layout=29 (`max-width` / `margin-left:auto` ใน render fn) — ย้ายเข้า `#page-late` ได้ (low-risk) · ไม่กระทบภาพ · 7 fix ไม่เพิ่มจำนวนนี้

### ~~UX-06 · Submit ไม่มี loading state~~ — ✅ RESOLVED โดย FIX-07
เดิม `submitReq`/`submitCand` ไม่มี spinner → **FIX-07 ใส่ `loader-2`+`spin` เมื่อ `RC.busy`** · audit.sh #44 หายแล้ว

---

## 🔵 INFO
- **UX-07** — `STAGES[].color` hardcode ใน JS array (map เข้า CI token แต่ bypass var) · self_audit ไม่จับ (JS)
- **UX-08** — `<i data-lucide>` บางตัวไม่มี class w-N/h-N (ss-caret/empty-icon/note/search) · มี CSS กำหนดขนาดเอง → cosmetic

---

## ✅ PASS (ตรวจแล้วผ่าน)
- CI Warm Light · token purity (business surface hex = 0) · BASE-KIT v6.4 verbatim (#69)
- **Overlay/portal · z-scale · lockScroll · trapFocus (#29):** ✅ — z-scale เดิมคงอยู่: backdrop50 < drawer55 < modal/portal60 < toast90 · modal เหนือ drawer (7 fix ไม่แตะ)
- Esc chain (#94) modal→drawer · combobox Esc stopPropagation · Destructive confirm · Empty states (#39)
- **Validation (FIX-05):** field-level `is-invalid` + focus + `--c-danger` token ✅
- **Permission (FIX-02):** viewer read-only · mutation guard 15 จุด · ปุ่มสร้างซ่อนตาม persona ✅
- **Hire route (FIX-01):** เส้นเดียว `candHireHandoff` · ห้าม skip → hired ✅
- #102 combobox anatomy · #103 lean list / stable screen · #104 one menu · #105 persona ใน demo-strip
- Pass D (Q document archetype): N/A — master+kanban ถูกต้อง

---

## Pass R — Render Gate (รันจริง · รอบ re-run หลัง FIX)
- เครื่องมือ: `render-check.py` + chromium (playwright) · shot หน้า list หลัก (`/tmp/render-check.png`)
- ผล: **สะอาด · ไม่มี regression จาก 7 fix** — status pill สีถูก (เปิดรับ=success · อนุมัติแล้ว·รอประกาศ=info · ปิดแล้ว=muted) · chip "ไม่มีแผน" amber · จัดแนวตรง · Thai rhythm กึ่งกลาง · อัตราชิดขวา (0/2·0/1·1/1) · footer "3 รายการ" ติดล่างขวา · ไม่มี body h-scroll
- **ยืนยัน FIX-02 บนภาพ:** demo-strip ล่างซ้ายมี persona ครบ 3 (เจ้าหน้าที่สรรหา / ผู้จัดการสายงาน / **ผู้ชมทั่วไป**) · persona ปัจจุบัน = เจ้าหน้าที่สรรหา → ปุ่ม "เปิดอัตราใหม่" แสดงถูก (business action ใน page header)
- **ข้อจำกัด (Render Gate item ง):** shoot หน้า list เท่านั้น — FIX ที่อยู่ใน drawer (validation/loader/viewer guard) ยืนยันผ่าน static + logic trace (grep fn + call sites) เพราะ render-check ไม่ขับ drawer

---

## หมายเหตุกระบวนการ
- รอบนี้เป็น **re-run (check mode)** หลังแก้ FIX-01..07 จากใบสั่ง BA (ไม่ใช่ fix mode — checker ห้ามแก้ HTML)
- gate = `audit.sh FAIL=0` (ผ่าน · WARN 4→3) + PREFLIGHT counter ตรงการนับจริง + Pass R สะอาด → **PASS · WARN ลดจาก 5 เหลือ 4**
- 7 fix ทั้งหมด surgical · ไม่แตะ BASE-KIT/mock/behavior นอก scope · ไม่แตะ z-index fix เดิม · ไม่ commit
