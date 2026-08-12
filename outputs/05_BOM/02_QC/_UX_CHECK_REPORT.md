# UX Check Report — BOM (F-BOM-001) · f-bom.html

- วันที่: 2026-08-11 · Iteration: 2 (fix-mode — surgical, ไม่ regenerate)
- Generator spec: **html-generator-v8** (iron-rules.md Sync Read จาก `.claude/skills/html-generator-v8/knowledge/`)
- Authoritative gate: `audit.sh` → **FAIL=0 · WARN=2** (residuals ที่รับไว้แล้ว — ดูท้าย report)
- ไฟล์ที่ตรวจ: `outputs/05_BOM/01_HTML/f-bom.html`
- หลักฐานภาพ (หลังแก้): `02_QC/_shots/route_bom.png`, `route_bom__overlay_btn-primary.png` (playwright)

## Verdict: 🟢 PASS (with 2 accepted warnings · 0 BLOCK)

| BLOCK | WARN | INFO | NOT-CHECKED |
|---|---|---|---|
| 0 | 2 (accepted residuals #21 + font-size) | 2 | 1 |

**Loop diff (iteration 2):**

| สถานะ | รายการ |
|---|---|
| ✓ แก้แล้ว | **UX-01** (BLOCK→fixed), **UX-02** (warn→fixed), **UX-03** (warn→fixed) |
| ⚪ คงเหลือ (accepted) | Rule #21 icon inline-size · token font-size px (audit.sh WARN=2 — รับไว้แต่เดิม) |

> Iteration 1 เป็น BLOCK เพราะ icon ที่ถูกอ้างแต่ไม่มีนิยามใน `ICONS` (audit.sh มองไม่เห็น).
> Iteration 2 fix-mode แก้ครบ 3 จุดแล้ว ยืนยันด้วยภาพ render จริง.

---

## ✅ Fix verification (iteration 2)

- **UX-01 — FIXED & visually verified.** เติม 3 path เข้า `ICONS` (บรรทัด ~266): `chevron-down`, `x-circle`, `file-edit` (ใช้ official lucide inner paths). `renderIcons()` วาดได้แล้ว:
  - `route_bom.png` (หลังแก้) — stat card **"ไม่ใช้งาน" มี x-circle**, **"ร่าง" มี file-edit** (เดิมว่างเปล่า)
  - `route_bom__overlay_btn-primary.png` (หลังแก้) — FG combobox **มี chevron-down ขวามือแล้ว** (affordance dropdown กลับมา)
  - status menu (`STATUS_ICON` draft=file-edit / inactive=x-circle) และ toast error (x-circle) ใช้ map เดียวกัน → วาดได้ตามกลไกที่ยืนยันแล้ว
- **UX-02 — FIXED.** ลบ `.pill-inactive` ตัวแดง (`#FEE2E2/#B91C1C`) ที่บรรทัด ~116 ออก เหลือชุดอำพัน (`#FFF1DD/#B8690B`) ที่บรรทัด 83 เดียว. grep `pill-inactive{` = **1**. "ไม่ใช้งาน" ไม่อ่านเป็น danger อีก.
- **UX-03 — FIXED.** เพิ่ม `reflowSuggest()` + `window.addEventListener('scroll',…,true)` (capture) และ `'resize'` → portal เรียก `placeSuggest()` ให้ติดกับ input เมื่อ scroll drawer-body/table หรือ resize. ปิด Rule #95 ครบ.
- Gate หลังแก้: `audit.sh` = **FAIL=0 · WARN=2** (เท่าเดิม — ไม่เกิด regression).

---

## 🔴 BLOCK — ต้องแก้ก่อนผ่าน gate

### UX-01 · Rule #21 (icon render) · หลายจุด · ICONS map บรรทัด 266
- **พบ:** มี `data-lucide` 3 ชื่อที่ถูกอ้างในโค้ด แต่ **ไม่มีนิยามใน object `ICONS`** →
  `renderIcons()` เจอ `if(!inner)return;` แล้วปล่อย `<i>` ไว้เฉย ๆ → **ไม่มี icon แสดง (ช่องว่าง)**
  - `x-circle` — stat card "ไม่ใช้งาน" (บรรทัด 386), bulk bar ปุ่ม "ไม่ใช้งาน" (398), `STATUS_ICON.inactive` (334) ในเมนูเปลี่ยนสถานะ, toast error icon (362)
  - `file-edit` — stat card "ร่าง" (บรรทัด 387), bulk bar ปุ่ม "ร่าง" (399), `STATUS_ICON.draft` (334)
  - `chevron-down` — **cbx-chev ของ combobox FG (585) และ combobox วัตถุดิบ (604)** → หายทั้งคู่ = ผู้ใช้ไม่เห็นสัญญาณว่าเป็น dropdown
- **หลักฐานภาพ:** `route_bom.png` — stat "สูตรทั้งหมด"/"ใช้งาน" มี icon แต่ "ไม่ใช้งาน"/"ร่าง" **ว่างเปล่า** ·
  `route_bom__overlay_btn-primary.png` — ช่องค้นหา FG มีแต่แว่นขยายซ้าย **ไม่มี chevron ขวา**
- **แก้:** เติม 3 path เข้า `ICONS` (ค่าจาก lucide):
  ```js
  "chevron-down": "<path d=\"m6 9 6 6 6-6\" />",
  "x-circle": "<circle cx=\"12\" cy=\"12\" r=\"10\" /><path d=\"m15 9-6 6\" /><path d=\"m9 9 6 6\" />",
  "file-edit": "<path d=\"M12 22h6a2 2 0 0 0 2-2V7l-5-5H6a2 2 0 0 0-2 2v10\" /><path d=\"M14 2v4a2 2 0 0 0 2 2h4\" /><path d=\"M10.4 12.6a2 2 0 1 1 3 3L8 21l-4 1 1-4Z\" />"
  ```
  (หรือใช้ icon ที่มีอยู่แล้วแทน — เช่น `x` / `pencil` — แต่ chevron-down ควรเติมจริงเพื่อ affordance dropdown)

---

## 🟡 WARN

### UX-02 · H-Consistency + off-palette · `.pill-inactive` นิยามซ้ำ 2 ที่ (บรรทัด 83 และ 116)
- **พบ:** `.pill-inactive` ถูกประกาศ 2 ครั้ง:
  - บรรทัด 83: `background:#FFF1DD;color:#B8690B` (อำพัน — เข้าชุด muted/inactive)
  - บรรทัด 116: `background:#FEE2E2;color:#B91C1C` (แดง — โทน danger)
  ตัวหลังชนะ → badge "ไม่ใช้งาน" ออกเป็น **แดง** ซึ่งสื่อความหมาย error/อันตราย ผิดเจตนา status "ไม่ใช้งาน" (ควร neutral/อำพัน). ทั้ง 4 hex ยังหลุด palette (self_audit `hex_off`).
- **แก้:** ลบ rule ซ้ำที่บรรทัด 116 ให้เหลือชุดอำพันที่บรรทัด 83 (หรือแมปเป็น `var(--c-warning)`/token) — เลือกแบบเดียว.

### UX-03 · Rule #95 (Overlay Portal) — บางส่วน · combobox suggest portal
- **พบ:** portal (`#suggest-portal`, `.cbx-suggest{position:fixed}`) วางตำแหน่งครั้งเดียวตอนเปิดผ่าน `placeSuggest()` แต่ **ไม่มี listener `scroll`/`resize`** (ยืนยันด้วย grep — ไม่พบเลย). เมื่อ dropdown เปิดค้างแล้ว scroll `.drawer-body` หรือ resize หน้าต่าง → dropdown ตัว fixed **ลอยค้างที่เดิม หลุดจาก input**.
- **ที่ทำถูกแล้ว:** portal อยู่นอก drawer (กัน transform), z-index 200 ลอยเหนือ table/drawer, flip-up เมื่อพื้นที่ล่าง<200px, ปิดเมื่อ select และ mousedown นอกกล่อง.
- **แก้:** ผูก reposition ตอน portal เปิด:
  ```js
  // เรียกใน fgSuggestOnly/lineSuggestOnly หลังเปิด
  const reflow=()=>placeSuggest(sgEl,inputEl);
  window.addEventListener('scroll',reflow,true); window.addEventListener('resize',reflow);
  // ถอดเมื่อปิด
  ```

---

## ℹ️ INFO (ไม่บังคับ)

- **UX-04** · `.drawer-panel` ใส่ class `drawer-enter` (บรรทัด 616, 660) แต่ **ไม่มี CSS `.drawer-enter`** — dead class, ลบได้.
- **UX-05** · rule ซ้ำแบบ additive: `.stat` (49 + 84), `.line-row .input,.line-row .select` (169 height:38px แล้ว 172 height:34px). ตัวหลังชนะ ไม่กระทบ visual แต่ควร merge ให้อ่านง่าย.

---

## ⬜ NOT-CHECKED

- **Render matrix ไม่ครบ** · `render_shots.py` auto-capture ได้ 2 ใบ (list + create-drawer step1). **View drawer / status menu เปิด / line-editor combobox เปิด / bulk-delete modal** ไม่ถูกจับภาพอัตโนมัติ — ตรวจจากโค้ดแทน (ผลด้านล่าง) แต่ยังไม่มีภาพยืนยัน bottom-edge flip ของ combobox วัตถุดิบแถวล่างสุด. แนะนำ capture เพิ่มก่อนปิด gate.

---

## 🎯 Latent-bug blind spots (ตรวจชัดตามที่สั่ง)

**1. Drawer re-render หลัง status change / edit (#29 keepScroll) — ✅ YES ถูกต้อง**
`setStatus()` → `closeMenus()` → `render()` = `_keepScroll(_renderNow)`. `renderView()` อ่าน `b` สดจาก RAW ทุกครั้ง → pill/badge/แท็บประวัติ refresh, ไม่มี stale DOM (overlay innerHTML สร้างใหม่ทั้งก้อน), `state.drawer.open/tab` คงเดิม drawer ไม่ปิด, และ `_keepScroll` เก็บ-คืน scrollTop ของ `.content`/`.table-scroll`/`.drawer-body` ใน rAF → scroll ไม่หลุด. ผ่าน #29.

**2. In-drawer modal/menu z-index + Esc chain — ✅ YES ถูกต้อง**
overlay/menu ที่เปิดจากใน drawer = `statusMenu` (`.pop-menu` z-index 80) อยู่ใน overlay-root (z-index 100) วางเหนือเนื้อ drawer ได้. `#modal-root` z-index 120 > drawer 100 (ถ้ามี modal เปิดจากใน drawer จะอยู่เหนือจริง — แต่ modal เดียวในฟีเจอร์นี้คือ bulk-delete ซึ่งเป็น list-level ไม่ใช่ in-drawer). Esc chain (บรรทัด 725-731) เรียงถูก: **modal > statusMenu > drawer**. ผ่าน.

**3. Combobox suggestion portal ลอยเหนือ table / reposition / ปิดเมื่อ select — ⚠️ PARTIAL**
✅ ลอยเหนือ line-editor table ไม่โดน clip (portal นอก drawer, fixed z200) · ✅ flip ขึ้นเมื่อพื้นที่ล่างไม่พอ · ✅ ปิดเมื่อ select และเมื่อ mousedown นอกกล่อง · ❌ **ไม่ reposition เมื่อ scroll/resize** (ไม่มี listener) → ดู UX-03. เป็นช่องเดียวที่ยังไม่ครบ #95.

---

## Known / accepted residuals (ไม่ re-litigate)

จาก v8 self-audit เดิม (audit.sh WARN=2) — รับไว้แล้ว ไม่นับเป็น block ใหม่:
1. Rule #21 — `<i data-lucide>` ใน JS template ปรับขนาดผ่าน inline style/scoped CSS แทน class `w-{N}/h-{N}` (page-h, stat, fsec-title, form icons).
2. Token — `font-size` เป็น px literal หลายจุด (แทน `var(--fs-*)`).

> หมายเหตุแยกจากข้างบน: `self_audit.py` (นับเข้ม non-gate) รายงาน counter อื่น ๆ ไม่ศูนย์ (spacing_off, font_off, z_adhoc, hex_off ฯลฯ) ซึ่งเป็นลักษณะที่แม้ gold reference ก็ตก — gate จริงคือ audit.sh (FAIL=0). ไม่ยกเป็น block ยกเว้น UX-02 ที่เป็น "ความไม่สม่ำเสมอจริง" (pill ซ้ำ) ไม่ใช่แค่ off-scale.
