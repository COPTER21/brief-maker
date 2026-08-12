# UX Check Report — Warehouse & Bin (F-LOC)

- วันที่: 2026-08-12 · Iteration: 2 (FIX MODE + loop diff vs iteration 1)
- Generator spec (Sync Read, authoritative): **html-generator-v8** — `knowledge/iron-rules.md` (Rules #1–#49 + #94 Master Combobox, #94.1 Cascade Clear, #95 Overlay Portal, #96 List Full-Height, #97 Responsive) + `knowledge/ci-tokens.md` (CUBE Warm Light v2.0)
- ไฟล์ที่ตรวจ: `warehouse-bin.html` (1,329 บรรทัด, ~164 KB)
- โหมด: **FIX (surgical) — แก้เฉพาะ UX-01..UX-08 จาก report รอบก่อน** แล้วตรวจซ้ำ
- RENDER GATE: **UNAVAILABLE** (ไม่มี browser ในเลนนี้) → visual/pixel items = NOT-CHECKED (แนะนำ render pass ใน Cowork/Claude Code)

## Verdict: 🟢 PASS (0 BLOCK)

| BLOCK | WARN | INFO | NOT-CHECKED |
|---|---|---|---|
| 0 | 0 | 5 | 3 |

เกณฑ์ผ่าน gate = **BLOCK 0** → ผ่าน. INFO ทั้งหมดเป็น documented residual (optional, ไม่บังคับ). NOT-CHECKED เป็นข้อจำกัดของเลน (ไม่มี browser) ไม่ใช่ defect ในโค้ด.

Both `<script>` blocks parse (node --check ✓ ทั้ง 2 block). ไม่มี FN behavior หาย.

---

## 🔁 Loop diff (vs Iteration 1) — ทุกรายการ fix list = แก้แล้ว ✓

### UX-01 · Rule #95 Overlay Portal · Branch Master Combobox — ✅ FIXED (was 🔴 BLOCK)
- **แก้:** ถอด inline `.mb-list` ออกจาก template `branchField()` แล้ว portal ไป `document.body` เป็น `#branch-portal.mb-portal { position:fixed; z-index:500 }` — mirror pattern เดียวกับ `sm-portal-menu`.
- ฟังก์ชันใหม่ `syncBranchPortal()` (สร้าง/อัปเดต/ลบ portal ตาม state) + `positionBranchPortal()` (คำนวณจาก `getBoundingClientRect()` ของ `#f-branch-combo` + **flip-up** เมื่อ `r.bottom+h > innerHeight-8`).
- Hook `syncBranchPortal()` ต่อท้าย `render()`; reposition บน `scroll` (capture) + `resize`.
- Keyboard nav (ArrowUp/Down/Enter/Esc) คงเดิม; outside-click แก้ให้ portal นับเป็น "inside" (mousedown handler เช็คทั้ง `#f-branch-combo` และ `#branch-portal`); Esc ปิดเฉพาะ list ไม่ปิด drawer (#94.3) — `onBranchKey` ยัง `stopPropagation()`.
- บรรทัดที่แตะ: CSS `.mb-portal` (หลัง `.branch-cell`), template `branchField()`, `positionBranchPortal/syncBranchPortal/mousedown/scroll/resize` (ต่อจาก `clearBranch`), `render()` (เติม `syncBranchPortal()`).

### UX-02 · Rule #41 (ห้าม eye icon) · row-actions — ✅ FIXED (was 🟡 WARN)
- **แก้ (ทางเลือก B):** เปลี่ยน `data-lucide="eye"` → `panel-right-open` ใน `actionsCell()` (เพิ่ม glyph `panel-right-open` ใน ICONS map). ลบ eye icon ตามกฎ แต่คง view action (`openView`) ไว้ — view ยังเข้าถึงได้ทางปุ่มเดิม + row-click (location). ยืนยัน `data-lucide="eye"` เหลือ 0 จุดในไฟล์.

### UX-03 · Rule #44 (Submitting state) · submitForm/submitLoc/submitBulk/confirmStatusReason — ✅ FIXED (was 🟡 WARN)
- **แก้:** เพิ่ม helper `busySubmit(btn,after)` — set `disabled` + spinner (`loader-2 .spin`, label "กำลังบันทึก…") + guard `_submitBusy` กัน double-submit + defer commit/close ~550ms. เพิ่ม glyph `loader-2` ใน ICONS + CSS `.spin`/`@keyframes spin`. ปุ่ม submit ทั้ง 4 ส่ง `this` เข้ามา (`submitForm(this)`, `submitLoc(this)`, `submitBulk(this)`, `confirmStatusReason(this)`).

### UX-04 · Audit trail (create/edit/bulk) — ✅ FIXED (was 🟡 WARN)
- **แก้:** เพิ่ม `AUDIT[id].unshift({t,by,at,v})` (โครงเดียวกับ `applyStatus`/`quickAdd`) ใน:
  - `submitForm` — create → `'สร้างรายการ'`, edit → `'แก้ไขข้อมูล'` (ครบ 4 level: warehouse/zone/area/rack; id = `state.sel.id` ตอน create, `state.drawer.id` ตอน edit).
  - `submitLoc` — create → `'สร้างตำแหน่ง'`, edit → `'แก้ไขข้อมูล'`.
  - `submitBulk` — `'สร้างจาก bulk-gen N ตำแหน่ง'`.
- ทุก mutation ทิ้ง WORM trail แล้ว; location view แท็บ "ประวัติ" จะเห็น entry การสร้าง/แก้ไข.

### UX-05 · Rule #1 CI Tokens (backdrop/shadow drift) — ✅ FIXED (was 🟡 WARN)
- **แก้ (global token substitution ทั้งไฟล์, CSS block):** `rgba(11,29,58,*)` → `rgba(17,17,17,*)` (charcoal) และ `rgba(11,92,255,*)` → `rgba(255,59,48,*)` (red primary). ครอบคลุมทั้ง 7 จุดที่ report ระบุ (18,42,168,169,205,207,232) + จุด legacy อื่นที่เหลือ (focus ring 150, btn-primary hover 50, tree/seg selected tints, toast shadow 211 ฯลฯ). ยืนยัน legacy navy/blue เหลือ **0** จุด.

### UX-06 · Rule #2 Font Load (Noto Sans Thai หาย) — ✅ FIXED (was 🟡 WARN)
- **แก้ (per ci-tokens.md lines 70–76, verbatim CDN — v8 บังคับใช้ CDN นี้ ไม่ self-host):** เพิ่ม `<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Thai:wght@400;500;600;700;800&display=swap">` และเปลี่ยน Satoshi เป็น `satoshi@300,400,500,700,900` (เติม weight 400 ที่เป็น body base).

### UX-07 · Rule #31.1 (Cancel = btn-ghost) — ✅ FIXED (was 🟡 WARN)
- **แก้:** ปุ่มยกเลิกใน modal status-reason `btn-secondary` → `btn-ghost` (unify กับ modal ลบ/ปลดระวาง).

### UX-08 · Esc chain gap (status portal menu) — ✅ FIXED (was 🟡 WARN)
- **แก้:** global keydown เพิ่มลำดับ Esc: `sm-portal-menu` (closeStatusMenu) → branch combo list → modal → drawer. เมนูสถานะปิดด้วย Esc แล้ว (ไม่ค้าง/ไม่เผลอไปปิด drawer ข้างหลัง).

---

## ℹ️ INFO (documented residual — optional, ไม่บังคับ, ไม่แตะเพื่อกัน scope creep)

1. **Sidebar gradient** (`.sidebar` linear-gradient charcoal) vs ci-tokens v2.0 ที่เป็น flat `#111111` — cosmetic; knowledge เก่ายังพูดถึง gradient ทำให้ก้ำกึ่ง. คงไว้.
2. **Drawer base width 680px** — `.standard` สำหรับ master ฟอร์มสั้น; location wizard 2-step borderline ควรพิจารณา 920px (ดุลยพินิจ). คงไว้.
3. **font-family order** `'Noto Sans Thai','Satoshi'` (Thai-first) สลับจาก canonical — ตั้งใจเพื่อ Thai app. คงไว้.
4. **Inline layout style (Rule #56):** `warn-box`/confirm ปุ่ม disable ด้วย inline `opacity/pointer-events`, `style="flex:1"` หลายจุด (pre-existing) + busySubmit set `btn.style` ชั่วคราวขณะ submitting. Minor; คงไว้.
5. **Icons inlined** (ICONS map + shim) — ผ่าน (offline-friendly). ไม่ใช่ defect.

## ⬜ NOT-CHECKED (ต้อง render จริง — ไม่มี browser ในเลนนี้)

1. **Visual clip/flip ของ branch combobox portal** — โครงสร้างแก้แล้ว (portal→body, fixed, flip-up, reposition on scroll/resize) แต่ pixel-proof ต้อง screenshot: เปิด drawer warehouse → scroll body → เปิด combobox → ยืนยัน list ไม่ถูก drawer-body clip และ flip ขึ้นเมื่อชิดขอบล่าง.
2. **Rule #38 Thai vertical rhythm** — โดยเฉพาะหลังเพิ่ม Noto Sans Thai (UX-06) ต้อง render เทียบเส้นกึ่งกลาง pill/tag/btn/stat.
3. **Rule #42 sticky header overlap** ตอน scroll ตารางจริง.

> **แนะนำ:** รัน Render Gate (`scripts/render_shots.py`) ใน env ที่มี browser เพื่อปิด 3 ข้อ NOT-CHECKED (โดยเฉพาะ #1 = การพิสูจน์ผลของ BLOCK ที่เพิ่งแก้).

---

## Validation หลังแก้

- `node --check` ผ่านทั้ง 2 `<script>` block (icons block + main app block).
- Legacy navy/blue rgba = 0; `data-lucide="eye"` = 0; Noto link + Satoshi 400 = present; portal/busySubmit/audit ครบ.
- FN behavior คงครบ (drill/view/edit/bulk-gen/status/quick-add/validation ไม่เปลี่ยน logic — เพิ่มเฉพาะ audit push + submitting state + portal presentation).
