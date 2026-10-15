# _UX_CHECK_REPORT — F-PUR-COMPARE · เทียบราคาผู้ขาย

**ขั้น:** WF-01 §7R re-gate (Phase B entry) · `qc-ux-html-checker`
**target:** `01_HTML/CompareVendors.html` (97 KB single-file · 1,167 บรรทัด)
**ต้นทาง:** `input/09132026-compare-vendors/1_HTML/F-PUR-COMPARE.html` (ไม่แก้ไขเนื้อไฟล์)
**วันที่:** 2026-09-13 · Sync Read iron rules จาก `html-generator-v9`

## Verdict: **PASS** · 0 BLOCK · **8 WARN** (ใหม่ 6 · ยกมาจาก S3a 2)

> รายงานนี้ **ไม่ใช่** การคัดลอก `_UX_CHECK_REPORT.md` ของ Phase A — รันใหม่ทั้งหมดบนไฟล์ที่อยู่ใน pack นี้
> ทุกข้อมีหลักฐานเป็นค่าที่วัดได้จริง (Playwright / static scan) + ภาพใน `_shots/`

---

## 1. Render gate — ผ่าน

| เช็ค | วิธี | ผล |
| --- | --- | --- |
| runtime error | Playwright headless 1600×950 · `pageerror` + `console.error` | ✅ **0 / 0** |
| interaction walk | 42 step (คิวงาน → 3 แท็บ → ฟอร์มใบเสนอราคา → ตารางเทียบ → ผลการเลือก → ยืนยัน → ล็อก → เปิดรอบใหม่ → ยกเลิกรอบ → responsive) | ✅ **42/42** · `_shots/01`–`_shots/42` |
| Esc chain | เปิดฟอร์มใบเสนอราคา → `Escape` → `!document.querySelector('.mbd')` | ✅ `true` |
| modal ไม่ล้นจอ | `getBoundingClientRect()` ของ modal = 940×823 · viewport 1600×950 | ✅ `overflowX:false · overflowY:false` |
| toast ไม่ทับปุ่ม modal | rect ของ `.toast` เทียบปุ่มทั้ง 5 ตัวใน modal footer | ✅ **overlapped: []** · `_shots/39_toast_over_modal.png` |
| ข้อความถูกตัดกลางคัน | `scrollWidth > clientWidth+1` บน `td * · .chip · .pill · .vn · .nm` | ✅ **0 จุด** |
| z-index stack | `getComputedStyle().zIndex` จริง | ✅ sidebar 20 · shell-bar 19 · toast 90 · `.mx thead th` 2 |

**หมายเหตุ `--z-*`:** ไฟล์นี้ **ไม่ได้ใช้ `var(--z-*)` ของ BASE-KIT เลย** — ประกาศ z-index เป็นตัวเลขตรงทั้ง 9 จุด
(`sidebar 20 · shell-bar 19 · backdrop 50 · drawer-panel 51 · mbd 60 · combo-pop 70 · row-menu 80 · toast-wrap 90 · mx thead 2`)
จึง **ไม่เจอบั๊ก `--z-*` ไม่ประกาศค่า** ที่เจอใน F-SEC-TRANS / F-SEC-LOCKOUT · ลำดับชั้นถูกต้อง: modal (60) > drawer (51) > backdrop (50) > sidebar (20)

---

## 2. CI / typography / tokens — ผ่าน

| เช็ค | ผล |
| --- | --- |
| `:root` CUBE Warm Light · 40 CSS custom properties | ✅ |
| font stack `'Satoshi','Noto Sans Thai',system-ui,…` + Noto Sans Thai จาก Google Fonts | ✅ |
| ไอคอน Lucide เท่านั้น (52 ตัว) · ไม่มี FontAwesome · emoji 1 ตัว (`★` ใน label) | ✅ |
| scrollbar block #49 (`::-webkit-scrollbar` 5px) | ✅ |
| sidebar 232 · shell-bar 52 · drawer 920 — ตรง watchlist | ✅ |
| **ปี ค.ศ. ล้วน** — `fmtDate` ใช้ `getFullYear()` · ไม่พบ `+543` | ✅ ยืนยันบนจอ: "15 ก.ย. 2026" |
| script ภายนอก | ✅ 0 (Lucide loader มี CDN fallback 3 ชั้น + `window.__lucideFailed`) |

---

## 3. Archetype guard ★ (ข้อสำคัญที่สุดของฟีเจอร์นี้ — HANDOFF §3 #1)

| เช็ค | หลักฐาน | ผล |
| --- | --- | --- |
| ไม่มี wizard 5 ขั้น | `static_scan.doc_archetype.wizard_steps = []` | ✅ |
| ไม่มี view drawer 4 แท็บ | `view_tabs = []` | ✅ |
| ไม่มีเลขที่เอกสาร / docPill | `has_docPill = false` | ✅ |
| ไม่มีแท็บแบบพิมพ์ / ลายเซ็น | `has_signProgress = false` · `a4 = false` | ✅ |
| ไม่มี line editor v2 ของเอกสาร | `line_tbl = false` · `has_calcLineVat = false` · `has_totals = false` | ✅ |
| ไม่มี DOA / สายอนุมัติในตรรกะ | grep `role|perm|approve` ในตรรกะ = **0** (มีแค่ label เมนู "สายอนุมัติ (DOA)" ของ module map) | ✅ |
| ใช้ Pattern A (คิวงาน) + card + modal (D) | `.q-item` · `.card` · `.mbd` | ✅ |

> ⚠️ `static_scan.py` รายงาน `doc_archetype.is_document = true` — **เป็น false positive**
> heuristic ติดจาก `vat_mode` (VAT 3 โหมดในฟอร์มใบเสนอราคา) เท่านั้น · ตัวชี้วัดจริงของ Pattern Q (`line_tbl` · `wizard_steps` · `view_tabs` · `docPill` · `signProgress`) **เป็น false/ว่างทั้งหมด**
> แต่ดู **WARN-5** — CSS ของ Pattern Q ยังค้างอยู่ในไฟล์ และนั่นคือสิ่งที่ทำให้ heuristic สับสน

**DIVERGENCE check เทียบ registry (`Cube_Feature_List.html` F073 · `arch: master` · `dec: ["csq"]`):** **ไม่พบ**
ไม่มี DOA · ไม่มีเลขรัน · ไม่มีแบบพิมพ์ · ไม่มี event แจ้งเตือน — ตรงกับชิปที่ประกาศ

---

## 4. UX heuristics — ผ่าน

| เช็ค | หลักฐาน | ผล |
| --- | --- | --- |
| empty / loading / error ครบ | `_shots/05_queue_error` · `06_queue_retry` · `07_queue_empty` · `01_console_default` (state "เลือกงานจากคิวทางซ้าย") | ✅ |
| destructive confirm | ลบใบเสนอราคา → *"การกระทำนี้ย้อนกลับไม่ได้ (การลบจะถูกบันทึกในประวัติ)"* · `_shots/18` | ✅ |
| toast หลังปิด modal | `_shots/29_after_reopen` (“เปิดรอบที่ 2 แล้ว”) | ✅ |
| microcopy ภาษาคน | *"ผลที่เลือกไม่ใช่ราคาต่ำสุด — ส่วนต่าง ฿149.80 จึงต้องอธิบายเหตุผลให้ตรวจสอบย้อนหลังได้"* | ✅ |
| focus preservation ตอนพิมพ์ | `data-f` + `renderQuoteKeep()` / `renderKeep()` | ✅ |
| ตารางเทียบกว้างได้ ไม่ยุบคอลัมน์ (#97) | `.mx-wrap` ครอบ `overflow-x` ของตัวเอง | ✅ |

---

## 5. WARN

### WARN-1 · ปุ่ม "สาธิตสถานะโหลดผิดพลาด" (ยกมาจาก S3a W1)
`simulateQueueError()` มุมขวาบนของคิวงาน — affordance สำหรับกดเข้าสถานะผิดพลาด
**มติรอบนี้: เก็บไว้ใน pack** เพราะเป็นทางเดียวที่ QA จะทดสอบ FN-03 (สถานะผิดพลาด + ปุ่มลองใหม่) ได้
→ บันทึกเป็น **LD-07** ใน `03_FRD/07_LOCKED_DECISIONS.md` ว่า **ต้องถอดก่อนขึ้น production**

### WARN-2 · ไฟล์แนบเป็น mock (ยกมาจาก S3a W2)
`addQuoteFile()` เพิ่มไฟล์ตัวอย่างในหน่วยความจำ ไม่มี upload จริง · Phase B ต้องต่อ storage — ดู `03_FRD/02_API.md`

### WARN-3 ★ ใหม่ · Iron Rule #81 — ศัพท์ภายในรั่วขึ้นจอ (11 จุด)
`self_audit` / `static_scan` จับไม่ได้ · เจอจากการอ่าน markup + ภาพจริง

| # | ข้อความบนจอ | ที่ | ประเภท |
| --- | --- | --- | --- |
| 1 | `คอนโซลปฏิบัติงาน — ไม่ใช่เอกสารธุรกรรม` | chip ใต้หัวข้อหน้า (เห็นตลอดเวลา) | ศัพท์ archetype ของทีมสร้าง |
| 2–4 | `Vendor Master (F007) — soft-reference` · `Item (F009) — soft-reference` · `Cost Center (F012) — soft-reference` | toast จากเมนูข้าง | รหัสฟีเจอร์ + ศัพท์โมเดล |
| 5 | `DOA (F019) — ฟีเจอร์นี้ไม่มีสายอนุมัติ` | toast จากเมนูข้าง | รหัสฟีเจอร์ + คำว่า "ฟีเจอร์" |
| 6 | `ศูนย์แจ้งเตือน — ฟีเจอร์นี้ไม่ประกาศ event แจ้งเตือน (chip = csq เท่านั้น)` | toast กระดิ่ง | **ศัพท์ registry (`chip`) รั่วเต็ม ๆ** |
| 7 | `ใบขอซื้อ (F-PUR-PR) — คนละไฟล์ต้นแบบ` | toast จากเมนูข้าง | คำว่า "ไฟล์ต้นแบบ" |
| 8–9 | `อยู่นอกขอบเขต feature นี้ (W3)` ×2 | toast จากเมนูข้าง | คำว่า "feature" + รหัส wave |
| 10 | **`ใบสั่งซื้อ (W3) — อยู่นอกขอบเขตรอบนี้`** | **ปุ่ม "ออกใบสั่งซื้อให้…" ในแท็บผลการเลือก (FN-18)** | ★ ไม่ใช่ scaffolding — เป็น affordance จริงของฟีเจอร์ |
| 11 | `mock flag` | คอมเมนต์ในโค้ด (ไม่ขึ้นจอ) | ไม่นับเป็น leak |

**#10 ร้ายแรงกว่าข้ออื่น** เพราะ (ก) อยู่บน affordance จริงที่ผู้ใช้กดหลังตัดสินผู้ชนะ และ (ข) คำว่า **"รอบนี้"** ในฟีเจอร์นี้แปลว่า *รอบเทียบราคา* แต่ในประโยคนี้หมายถึง *wave การส่งมอบ* → กำกวมกับผู้ใช้จริง
**ข้อความที่ควรใช้:** *"ยังออกใบสั่งซื้อจากที่นี่ไม่ได้ — ระบบใบสั่งซื้อจะเปิดใช้ภายหลัง"*
ส่วน #1–#9 เป็น scaffolding ของต้นแบบ → ถอดทั้งชุดตอนต่อระบบจริง (บันทึกเป็น **LD-08**)
หลักฐาน: `_shots/34_toast_po_hook.png` · `_shots/35_toast_nav_softref.png` · `_shots/38_w768.png` · `_shots/20_matrix_full.png` (chip #1)

### WARN-4 ★ ใหม่ · Iron Rule #97 — body h-scroll ที่ 768px
วัดด้วย `documentElement.scrollWidth` เทียบ `innerWidth` ทุกความกว้าง:

| viewport | 1600 | 1440 | 1280 | 1180 | 1024 | 900 | **768** |
| --- | --- | --- | --- | --- | --- | --- | --- |
| scrollWidth | 1600 | 1440 | 1280 | 1180 | 1024 | 900 | **796** |
| h-scroll | ✅ ไม่มี | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ **มี (+28px)** |

ตัวที่ล้น: `.queue` (right 796) → `.queue-head` → `.queue-title`
**สาเหตุ:** `.sidebar` คงที่ 232px ทุกความกว้าง (ไม่ยุบเป็น rail / off-canvas) → เหลือพื้นที่ 536px ให้คิวงานที่ min-width 328 + การ์ดใบเสนอราคา
**กติกา:** v9 Phase 5 — *"sidebar off-canvas/rail · ไม่มี body h-scroll (#97)"* · `check-methods.md` จัด `body_minwidth_768=false` เป็น **WARN #97**
ช่วง 900–1600 สะอาดหมด · หลักฐาน `_shots/36_w1180` · `37_w1024` · `38_w768`

### WARN-5 ★ ใหม่ · CSS ของ Pattern Q ค้างในไฟล์ 50 คลาส — เสี่ยงต่อ archetype guard
สแกน: สกัด selector ทั้งหมดจาก `<style>` 4 บล็อก แล้วเทียบกับ markup+JS ที่เหลือ · ไฟล์นี้ **ไม่มี `classList.*` และไม่มีการต่อชื่อคลาสแบบ `'x-'+v` เลย** (grep = 0) → ผลจึงเชื่อถือได้

**192 คลาสใน CSS · ใช้จริง 142 · ไม่ถูกอ้างที่ไหนเลย 50 คลาส** และ 50 ตัวนั้นคือ **แผงหน้าของ Pattern Q แทบทั้งชุด**:

```
a4  pdf-stage  pdf-tool  sig  sign-bar  sign-prog          ← แบบพิมพ์ + ลายเซ็น
line-tbl  line-wrap  free-row  slot-row  sum-tbl  tbl-foot ← line editor v2
line-collapse-panel  line-expand-panel-anchor  line-expand-panel-inner
drawer-panel  dw-head  dw-body  dw-title  dw-sum  dw-actions  dw-foot-note  wide  backdrop
combo-pop  combo-opt  combo-empty  item-combo  upload-zone  file-card  row-menu
btn-success  hard-warn  divider-s  divider-v  eyebrow  expanded  sortable  section-row
secwrap  sep  kbd  top-icon-btn  hd  pg  pgl  sn  sz  c3  c4
```

**ทำไมเป็นเรื่อง ไม่ใช่แค่ความสะอาด:**
1. เป็นเหตุให้ `static_scan.doc_archetype.is_document` รายงาน `true` → gate รอบหน้าอ่านผิดได้
2. HANDOFF §3 #1 บอกว่า *"ถ้าเผลอทำ = archetype ผิดทั้งฟีเจอร์"* — การมี `.line-tbl` / `.drawer-panel.wide` / `.sign-prog` พร้อมใช้อยู่ในไฟล์ คือ **คำเชิญให้คนตอนต่อระบบหยิบไปใช้** แล้วกลายเป็น DIVERGENCE เงียบ ๆ

**มติรอบนี้: รายงาน ไม่ลบ** — ไฟล์นี้ผ่าน `_TECH_CHECK` ของต้นน้ำมาแล้ว การลบ CSS 50 คลาสทำให้หลักฐานชุดนั้นใช้อ้างไม่ได้
→ ส่งต่อเป็นงาน Phase B (**LD-09**) พร้อมรายชื่อครบด้านบน

### WARN-6 ★ ใหม่ · SC-11 และ SC-15 ไม่มีการทำงานจริง — รายงาน R1 ของต้นน้ำระบุเกินจริง
`_COVERAGE_R1.md` (S3b) เขียนว่าทั้งสองเคส *"เป็นข้อกำหนดใน PREBRIEF + **hook ในโค้ด** (`prCancelled` flag)"* — ตรวจซ้ำแล้ว **ไม่ตรง**:

| เคส | สิ่งที่ตรวจ | ผลจริง |
| --- | --- | --- |
| **SC-15** ใบขอซื้อถูกยกเลิกหลังเปิดรอบ | `grep prCancelled` | พบ **ครั้งเดียว** ที่บรรทัด 939: `const prCancelled=false; /* hook: … mock flag */` — **ประกาศแล้วไม่มีที่ไหนอ่านค่าเลย** ไม่มีแถบเตือนที่หัวคอนโซล ไม่มีการปิดปุ่มยืนยัน |
| **SC-11** ผู้ไม่มีสิทธิ์เปิดดู | `grep role\|perm\|canEdit\|readonly\|viewer` (ทั้งไฟล์ + `in window`) | **0 ทุกคำ** — ไม่มีแม้แต่ตัวแปร ไม่ใช่ "hook ที่ยังไม่ผูกข้อมูล" |

เข้าแบบเดียวกับบทเรียน F-SEC-LOCKOUT: *"ฟิลด์ที่ประกาศไว้ อ้างในข้อความ แต่ไม่ถูกใช้ในตรรกะเลย"*
→ ปรับสถานะทั้งสองเคสจาก ⚠ เป็น ❌ **ยังไม่ได้ทำ** ใน `_COVERAGE_REPORT.md` และยกเป็นงานที่ต้องทำใน `03_FRD/05_RULES.md`

### WARN-7 ★ ใหม่ · ไม่มี ARIA เลย
`document.querySelectorAll('[role]').length = 0` · `[aria-label],[aria-hidden],[aria-live] = 0`
กระทบมากที่สุดที่ **toast** (ควร `aria-live="polite"`), **modal** (ควร `role="dialog"` + `aria-modal`), และ **ปุ่มไอคอนล้วน** (ควรมี `aria-label`)

### WARN-8 ★ ใหม่ · ข้อความยาวเกิน 120 ตัวอักษร 1 จุด
วัดด้วย `innerText` จริง (ไม่ใช่ regex บน source):
`.round-sub` = **127 ตัวอักษร** — *"ฝ่ายบัญชีและการเงิน · 2 รายการ · ต้องการใช้ 15 ก.ย. 2026 · อนุมัติเมื่อ 5 ก.ย. 2026 · เปิดรอบโดย สมร ตั้งใจดี 8 ก.ย. 2026 09:10"*
เกินมา 7 ตัวอักษร · อ่านออกและไม่ตัดบรรทัดผิด → **ไม่ block** · จุดอื่นทั้งหมด (`.hint` `.warn` `.info` `.q-foot` `.mute`) ผ่าน

---

## 6. สรุปสำหรับคนรีบ

ไฟล์นี้ **แข็งแรงกว่าค่าเฉลี่ยของ pack ที่ผ่านมา** — 0 runtime error · 42/42 interaction · ไม่มีบั๊ก `--z-*` · toast ไม่ทับปุ่ม · ไม่มีข้อความถูกตัด · archetype guard ผ่านสะอาด
สิ่งที่เพิ่มเข้ามารอบนี้คือ **6 ข้อที่ gate ของต้นน้ำมองไม่เห็น** เพราะเป็นหมวดที่ต้องวัดด้วย Playwright หรืออ่านภาพจริง (#81 · #97 · dead CSS · declared-but-unused)
**ไม่มีข้อไหนแตะ HANDOFF §3 "ห้ามแตะ"** — ทุกข้อเป็นงานต่อใน Phase B ไม่ต้องส่งกลับ BA
