# Iron Rules — 48 ข้อบังคับใช้ในทุก HTML output (v3.13)

> Source: v2.6.7 (v25) consolidated + reference patterns from `core-marketing-prospect.html`
> **ทุก HTML ที่ generate ต้องผ่านทั้ง 49 rules — no exception**
> Rules #27-#28 (v3.3) · #29 (v3.4) · #30 (v3.5) · #31 (v3.7) · #32 (v3.8) · #33 (v3.9)
> #34-#37 (v3.11 Search-Select · Layout Stability · Button Symmetry · Requirement Coverage)
> **#38-#43 (v3.12 Thai Rhythm · Empty State · List Cell Atomicity · List Row=view · Long-list UX · Validation+Format)**
> **#44-#48 (v3.13 Loading/Submitting · Disabled+Form Section · Placement Contract · Stepper Standard · Landing Standard)**

---

## Group 1: Brand & CI (Rules 1-5)

### Rule #1 — CI Tokens Locked
ใช้ CSS variables จาก `knowledge/ci-tokens.md` เท่านั้น — Navy `#111111`, Primary `#FF3B30`, Teal `#FF9A1F`. **ห้าม:** Crimson `#b02049`, Pink `#ffc0cb`, hardcoded hex.

### Rule #2 — Font Stack
ใช้ `'Satoshi', 'Noto Sans Thai', system-ui` เท่านั้น. Load จาก Google Fonts CDN. ห้าม font-family อื่น.

### Rule #3 — Sidebar Standard
Width = 232px (CSS var `--sidebar-w`). Background = navy gradient. Border-right = `rgba(255,255,255,0.06)`. Fixed position, full height. z-index 20.

### Rule #4 — Shell Bar (Header) Standard
Height = 52px (CSS var `--shell-h`). Background = white (not navy — modern look). Border-bottom = `var(--c-line-2)`. Sticky top. **ห้าม:** title ซ้ำใน shell bar กับ page header.

### Rule #5 — Lucide Icons Only
ทุก icon ใช้ `<i data-lucide="...">` จาก lucide.dev. ห้าม emoji color, Heroicons, FontAwesome.

---

## Group 2: Layout Structure (Rules 6-10)

### Rule #6 — Page Header (`.ph`) Pattern
ทุก content page ต้องมี Page Header section:
```html
<div class="ph">
  <div class="ph-title-row">
    <h1 class="ph-title">Title</h1>
    <span class="ph-count">29 รายการ</span>  <!-- if list page -->
  </div>
  <p class="ph-sub">Subtitle / description</p>
  <div class="ph-actions">
    <!-- buttons -->
  </div>
</div>
```
**ห้าม:** ใส่ title ใน shell-bar.

### Rule #7 — Breadcrumb in Shell Bar
Breadcrumb อยู่ใน shell-bar (left side) — items: Module → Submodule → Current. Separator = `<i data-lucide="chevron-right">`. Current page = bold + color `--c-ink`.

### Rule #8 — Stats/KPI Row (Optional)
ถ้าหน้ามี KPI: ใช้ `.stats` grid (auto-fit minmax(200px, 1fr)). แต่ละ stat = label + value + meta (with trend icon). ห้ามเกิน 6 cards ใน row.

### Rule #9 — Filter Bar in Card
Filter bar (search + selects + reset) อยู่ **ใน card** (border-top + bg off-white) — ไม่ลอยอยู่บน table โดยตรง.

### Rule #10 — Table Footer = pagination + count
Table footer (border-top + bg off-white) มี: pagination buttons (left) + record count "X – Y จาก Z" (right).

---

## Group 3: Drawer & Modal (Rules 11-15)

### Rule #11 — Drawer Width Standard (v2 — unified v3.13)
- **Create / Edit / View drawer:** `920px` (v2 standard, `max-width: 96vw`) — locked to `references/drawer-standard/` (pr.html)
- **`.drawer.standard`:** `680px` — simple form (≤6 fields) / short view / PO-style
- **Modal (confirmation):** `440px` max-width 92vw
- ❌ **540px = legacy — ห้ามใช้แล้วทุกกรณี** (ถ้าเจอใน HTML เก่า → migrate เป็น 920/680)

### Rule #12 — Drawer Slide Animation
```css
.drawer {
  transform: translateX(100%);
  transition: transform 280ms cubic-bezier(0.4, 0, 0.2, 1);
}
.drawer.is-open { transform: translateX(0); }
```
Backdrop: `rgba(17,17,17,0.40)`, opacity transition 220ms.

### Rule #13 — Drawer Structure
4 zones: `header` (avatar + title + meta + close) → `tabs` (optional) → `body` (scroll) → `footer` (sticky bottom, bg off-white).

### Rule #14 — Create/Edit = Drawer Slide-in (Modal for Confirmation Only)
**Create/Edit ทุกแบบ (single-step OR multi-step wizard) → ใช้ drawer slide-in (v2, 920px / .standard 680px)** เท่านั้น.
**Modal** = **confirmation, delete, archive, logout, simple form (1-3 fields)** เท่านั้น.
**ห้าม:** ใช้ modal สำหรับ multi-step create/edit (ใช้ drawer slide-in แทน).
**Override behavior:** ถ้า FRD spec บอกใช้ modal สำหรับ create → **silent override** เป็น drawer + log ใน "Iron Rule Overrides Applied".

### Rule #15 — Close behaviors
Drawer/Modal ต้องปิดได้ 3 ทาง:
1. Click backdrop
2. Click `<button class="icon-btn"><i data-lucide="x"></i></button>` ที่มุมบนขวา
3. กด Esc key

---

## Group 4: Table & Forms (Rules 16-20)

### Rule #16 — Table List ≤ 8 Columns
ตาราง list page ใช้ **≤ 8 columns** เท่านั้น (rare exception: 9 if needed). คอลัมน์ที่จำเป็น:
- Checkbox (40px) + ข้อมูลหลัก 5-6 cols + Row actions (60px)
- Signature column = `✓ ครบ` (teal) หรือ `-` (gray) — ห้ามแสดง "X/Y" ratio
- Action column = `⋮ more-vertical` button หรือ inline icon buttons (max 3)

### Rule #17 — Responsive Form Grid
**ห้ามใช้** `grid-cols-2` หรือ `grid-cols-3` ตรงๆ. ใช้:
- **Pattern A:** `grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));`
- **Pattern B:** `grid grid-cols-1 sm:grid-cols-2 gap-4` (utility classes defined in `file-skeleton.template.html` CSS — no Tailwind CDN required)

### Rule #18 — Form Field Structure
```html
<div class="field">
  <label class="field-label">Label <span class="req">*</span></label>
  <input class="input field-input" type="text" placeholder="...">
  <div class="field-help">Helper text (optional)</div>
  <div class="field-error">Error message (when invalid)</div>
</div>
```

### Rule #19 — Number Input — Hide Spinner Globally
```css
input[type="number"]::-webkit-inner-spin-button,
input[type="number"]::-webkit-outer-spin-button { -webkit-appearance: none; margin: 0; }
input[type="number"] { -moz-appearance: textfield; }
```
ต้องมีใน CSS ทุก HTML.

### Rule #20 — Toggle Pattern (Bulletproof)
ใช้ `<div onclick="toggle(); render();">` (full row clickable) + visual track เป็น `<div>` (transform translateX). **ห้าม:** `<label class="toggle"><input>` (browser inconsistency).

---

## Group 5: Code Quality (Rules 21-26)

### Rule #21 — Icon Class Audit (BREAKING)
ทุก `<i data-lucide="...">` element **ต้องมี** `w-{N}` + `h-{N}` utility class (e.g. `w-3.5 h-3.5`, `w-4 h-4`) — utility classes ถูก define ใน `file-skeleton.template.html` CSS แล้ว (no Tailwind CDN required).
- **เหตุผล:** Lucide default render เป็น 24×24px จะใหญ่ overflow ใน table row.
- **Audit:** หลัง generate ต้อง grep `<i data-lucide` ทุกตัว → ตรวจว่ามี `w-{N} h-{N}` ครบ.

### Rule #22 — Wizard Full-Height Layout
Wizard ใน main page (ไม่ใช่ drawer) ใช้ flex column 4 zones:
```
.wizard-shell (flex column, min-height 100%)
  ├─ .wizard-stepper-band (flex 0 0 auto)
  ├─ .wizard-body (flex 1, scroll)
  │   └─ .wizard-card (max-width 960px, margin auto)
  └─ .wizard-footer (sticky bottom 0, in flex parent)
```
**ห้าม:** `max-w-3xl` + `sticky bottom-0` ตรงๆ (ลอยใน whitespace).

### Rule #23 — No Color Emoji (BREAKING)
**ห้ามใช้:** 🔒 🔓 🔑 ⚡ ✅ ❌ ⚠️ 📊 📋 📄 📁 💳 💰 💾 🖨️ 🛒 📞 ✉️ 🔔 ⚙️ 🏠 👤 👥 📅 🕐 ⭐ 🎯 🚀 💡 📌 🏷️ ทุก emoji color.
**Acceptable abstract marks:** `•` `·` `→` `—` `✓` (plain, สำหรับ signature) `−` `-`.

### Rule #24 — No Dev-tool Bar in Production
HTML ที่ deliver **ห้ามมี:** dev-tool bar, page selector dropdown, debug panel, `console.log` calls, TODO comments.

### Rule #25 — renderIcons() After Every Render
ทุกครั้งที่ `render()` re-paint DOM (innerHTML replace) ต้องเรียก `renderIcons()` ทันทีหลัง assignment — ไม่งั้น icon ใหม่จะไม่ render.

⚠️ **ห้ามเรียก `lucide.createIcons()` ตรง ๆ** — ใช้ `renderIcons()` helper เท่านั้น (defined ใน `file-skeleton.template.html` INIT block).
- เหตุผล: `renderIcons()` เป็น safe wrapper ที่กัน `TypeError: lucide is undefined` เมื่อ Lucide CDN ทุกตัว fail หรือยัง load ไม่เสร็จ.
- Multi-CDN loader (unpkg → jsdelivr → cdnjs, pinned `@0.469.0`) อยู่ใน template แล้ว — feature code ไม่ต้องจัดการ load Lucide เอง.

### Rule #26 — Lean Catalog Principle (Registry UI)
สำหรับ Registry/Catalog UI (features, APIs, engines, schemas): **ห้าม** เก็บ implementation detail (params/schema/code) ใน UI. เก็บแค่ discovery field (code, name, location, tags, docs[]) + link ไป source-of-truth.

---

## Group 6: Global Shell Navigation (Rules 27-28)

### Rule #27 — Sidebar Module-Feature Pattern (BREAKING)
Sidebar nav = **2-level hierarchy**: Module (collapsible group) → Feature (clickable item).

**Required structure:**
```html
<div class="sb-module" data-module="<id>" data-expanded="true">
  <button class="sb-module-header" type="button" onclick="toggleModule(this)">
    <i data-lucide="<icon>" class="mod-icon w-3.5 h-3.5"></i>
    <span class="mod-label">Module Name</span>
    <i data-lucide="chevron-down" class="mod-chevron w-3 h-3"></i>
  </button>
  <div class="sb-features">
    <a class="sb-item" data-feature="<id>">…</a>
  </div>
</div>
```

**Hard requirements:**
- Module header = `<button>` (NOT `<a>`) — click toggles `data-expanded`, never navigates
- Module header has `mod-icon` + `mod-label` + `mod-chevron` (chevron rotates -90° when collapsed)
- Features wrapped in `.sb-features` (display:none when module collapsed)
- Every module has `data-module="<id>"`; every feature has `data-feature="<id>"` — required for future Menu Management + permission gating
- `toggleModule()` helper is already in `file-skeleton.template.html` — don't redefine
- If active feature is inside a module → that module starts `data-expanded="true"` (auto-rule)

**Banned:**
- `<div class="sb-section-title">` (the old flat label pattern) — replaced by `.sb-module-header`
- Making module header navigable (linking to a page)
- Mixing patterns — every sidebar item must live inside a `.sb-module`

### Rule #28 — Slim Top Bar (BREAKING)
Shell bar (top bar) = **Breadcrumb (left) + Notification + User Chip (right)**. Nothing else by default.

**Banned in top bar:**
- ❌ Help button (`?`) — if help is needed, put it inside the User Chip dropdown or as contextual per-feature
- ❌ Global Search button — search belongs inside pages (filter bar)
- ❌ Theme toggle / language switcher / any extra icon-btn — belongs in User Chip dropdown

**Breadcrumb required pattern:**
- `[Module] › [Feature]` minimum (2 levels). Use `data-lucide="chevron-right"` for separator — never `›` text.
- Level-1 (module name) = `<a>`, clickable, hover primary blue
- Last level = `<span class="breadcrumb-current">`, NOT clickable
- Optional `data-breadcrumb-module="<id>"` on level-1 to link back to sidebar

**User Chip required structure:**
- 2-line text: `user-name` + `user-role` (role line includes tenant, e.g. `"Marketing Lead · CUBE NATIVE"`)
- Avatar circle 30px gradient Primary→Teal, 2-char initials
- Click opens dropdown (My Profile / Preferences / Sign out)

---

## Group 7: Render Behavior (Rule 29)

### Rule #29 — Render Preservation (BREAKING)
ทุกครั้งที่ `render()` ทำ `innerHTML = ...` (full DOM rebuild pattern) ต้อง **save + restore** state ที่ user มองเห็น/รู้สึก ไม่งั้น user จะรู้สึก "เด้งกลับบน" หรือ "ช่อง input หาย focus" ทุกครั้งที่ toggle/click.

**Required preservation (4 axes):**
1. **Scroll position ของ `.drawer-body`** — drawer แบบ scrollable form ที่ user เลื่อนลงไปกรอกข้อมูล
2. **Scroll position ของ `.modal-body`** — modal ที่มี content ยาว
3. **Scroll position ของ `window` / page** — ตอนกดปุ่มใน list view
4. **Focus + cursor position ของ input/textarea ที่ active** — user กำลังพิมพ์อยู่ ไม่ควรหายไป

**Why innerHTML breaks these:**
เมื่อ `el.innerHTML = newHTML` browser ทิ้ง DOM node เดิมทั้งหมด แล้วสร้างใหม่ — scroll position, focus, selection ทั้งหมดหายเพราะ DOM ที่ถือ state เหล่านี้ "ไม่มีแล้ว"

**Solution — wrap render() with preservation:**
```js
function render() {
  // 1. SAVE before innerHTML rebuild
  const drawerScroll = document.querySelector('.drawer-body')?.scrollTop || 0;
  const modalScroll = document.querySelector('.modal-body')?.scrollTop || 0;
  const pageScroll = window.scrollY;
  const activeEl = document.activeElement;
  const focusKey = (activeEl?.tagName === 'INPUT' || activeEl?.tagName === 'TEXTAREA')
    ? { placeholder: activeEl.placeholder, type: activeEl.type,
        selStart: activeEl.selectionStart, selEnd: activeEl.selectionEnd }
    : null;

  // 2. ... innerHTML rebuilds here ...

  // 3. RESTORE after rebuild (in next frame)
  requestAnimationFrame(() => {
    const dBody = document.querySelector('.drawer-body');
    if (dBody && drawerScroll > 0) dBody.scrollTop = drawerScroll;
    const mBody = document.querySelector('.modal-body');
    if (mBody && modalScroll > 0) mBody.scrollTop = modalScroll;
    if (pageScroll > 0) window.scrollTo(0, pageScroll);

    if (focusKey) {
      const candidates = document.querySelectorAll('input, textarea');
      for (const c of candidates) {
        if (c.placeholder === focusKey.placeholder && c.type === focusKey.type) {
          c.focus();
          if (focusKey.selStart != null && c.setSelectionRange) {
            try { c.setSelectionRange(focusKey.selStart, focusKey.selEnd); } catch(e) {}
          }
          break;
        }
      }
    }
  });
}
```

**Helper provided by template:**
`file-skeleton.template.html` ใส่ helper `withRenderPreservation(renderFn)` ให้แล้ว — wrap render function ของ feature ด้วยตัวนี้ได้เลย ไม่ต้องเขียน save/restore เอง.

**Banned:**
- เรียก `el.innerHTML = ...` หลายครั้งโดยไม่ save/restore — โดยเฉพาะใน feature ที่มี drawer/modal ยาว, input ที่ user พิมพ์อยู่, หรือ list view ที่ scroll ยาว
- ใช้ `window.scrollTo(0, 0)` ตอนต้น render ทุกครั้ง (forced reset)
- ไม่ใส่ guard `if (scrollPos > 0)` — เพราะถ้า scroll เป็น 0 อยู่แล้ว ก็ไม่ต้อง restore

**When NOT required:**
- หน้าที่ไม่มี drawer/modal และ list view สั้น (เห็นทั้งหมดใน 1 viewport) — เหตุการณ์ "เด้งกลับบน" ไม่เกิดเพราะไม่มี scroll อยู่แล้ว
- แต่ default ใช้ helper ก็ "ไม่มี cost" เพราะ guard ภายในจัดการเอง

---

## Group 8: Page Layout (Rule 30)

### Rule #30 — Fluid Content Width (BREAKING)
`.content` (page wrapper ของ ERP shell admin tool) ต้อง **fluid full-width** — ห้ามใส่ `max-width` cap ใด ๆ ทั้งสิ้น.

**Scope:** Rule นี้บังคับใช้กับ **ERP shell** (`erp-shell.template.html`, ใช้ `.content` class) ที่เป็น admin tool เท่านั้น. **ไม่ใช้** กับ `general-shell.template.html` (marketing/public pages, ใช้ `.content-general` class) ซึ่งเป็น landing page convention ที่ content จัดกลางหน้าได้ปกติ (`max-width: 1200px; margin: auto`).

**เหตุผล:** Admin tool ของ CUBE NATIVE ออกแบบสำหรับ desktop-only (`body { min-width: 1180px }`) — บนจอกว้าง (1920px / 2560px / 4K) ต้องใช้พื้นที่ horizontal ให้คุ้ม. ถ้าใส่ `max-width: 1640px` (หรือค่าใด ๆ) ตรง `.content` → บนจอกว้าง content จะหยุดที่ค่านั้นแล้วเหลือ whitespace ขวา ทำให้ user รู้สึก "ไม่ stretch เต็ม" + Table list/Dashboard เสีย real estate ที่ใช้แสดงข้อมูลได้.

**Required pattern:**
```css
.content {
  padding: 22px;
  /* fluid — no max-width */
}
```

**Component-level constraints ยังคงอยู่ (ไม่กระทบ):**
- `.modal` — `width: 440px; max-width: 92vw` ✅ คงไว้
- `.toast` — `max-width: 380px` ✅ คงไว้
- `.wizard-card` — `max-width: 960px; margin: auto` ✅ คงไว้
- `.stepper-row` — `max-width: 640px; margin: auto` ✅ คงไว้
- A4 paper / Invoice preview — `max-width: 820px; margin: auto` ✅ คงไว้
- Text paragraph (`home-hero-sub` ฯลฯ) — `max-width: 640px` (optional, readability) ✅ คงไว้

**Banned:**
- ❌ `.content { max-width: 1640px }` — เก่า, ผิด rule
- ❌ `.content { max-width: <ค่าใด ๆ> }` — block fluid layout
- ❌ ใส่ `max-width` cap บน wrapper element ใด ๆ ที่ห่อทั้งหน้า (`.main`, `.page`, `.page-content-host`)

**If a specific page genuinely needs internal cap:**
ใช้ **child element** ภายใน `.content` เป็น constraint แทน — wrapper `.content` ยัง fluid:
```html
<main class="content">
  <div class="page-header">...</div>             <!-- fluid -->
  <div style="max-width: 1640px; margin: auto;"> <!-- specific page cap -->
    <table>...</table>
  </div>
</main>
```
แต่กรณีนี้ rare มาก — table list/dashboard/detail ทั่วไป **ไม่ต้องการ** cap.

**Pre-existing HTML migration:** ถ้าเจอ HTML ที่ generate จาก v3.0-v3.4 มี `.content { max-width: 1640px }` ให้ลบบรรทัด max-width ทิ้งเลย — ไม่กระทบอย่างอื่น.

---

## Group 9: Drawer Button Contract (Rule 31)

### Rule #31 — Drawer Button Contract (BREAKING)
ปุ่มทั้งหมดใน drawer (header actions + footer) ต้องเป็นไปตาม **contract ตายตัวด้านล่าง** — ห้ามตีความใหม่ต่อ feature. แก้ปัญหาคลาสสิก: drawer จาก skill เดียวกันแต่ footer/ปุ่มไม่ตรงกัน (ลำดับสลับ, สีปุ่มมั่ว, ปุ่มปิดเป็นสีแดง, ปุ่มร่างมีบ้างไม่มีบ้าง).

> **กฎสำคัญสุด:** สีปุ่ม = หน้าที่ของปุ่ม (role) ไม่ใช่ความสวยงาม. `btn-danger` (แดง) สงวนไว้ **เฉพาะ destructive action** (ลบ / ปิดใช้งาน / reject) เท่านั้น — **ปุ่ม "ปิด" หรือ "ย้อนกลับ" ห้ามเป็นสีแดงเด็ดขาด**.

---

#### 31.1 — Button Color = Role (ตายตัว)

| Role / ความหมายของปุ่ม | Class | สี | ตัวอย่าง label |
|---|---|---|---|
| **Primary action** (action หลักของ drawer) | `btn-primary` | น้ำเงินทึบ | ถัดไป, ยืนยันสร้าง, บันทึกการแก้ไข, Approve, Convert |
| **Secondary action** (action รอง / กลับ / ปิด) | `btn-secondary` | ขาว+เส้นขอบ | กลับ, บันทึกร่าง, แก้ไข, ปิด |
| **Cancel** (ยกเลิกการกรอก ฟอร์ม) | `btn-ghost` | โปร่ง ไม่มีขอบ | ยกเลิก |
| **Destructive** (ทำลาย/ถอน) | `btn-danger` | แดง | ลบ, ปิดใช้งาน, Reject, Archive |
| **Inline link** (navigate ออก) | `btn-link` | น้ำเงิน text | ดูลูกค้า, เปิดเอกสาร |

**Banned (สีผิด role):**
- ❌ ปุ่ม "ปิด" / "ย้อนกลับ" / "ตีกลับ" / "Close" เป็น `btn-danger` (แดง) — ต้องเป็น `btn-secondary` เสมอ
- ❌ ปุ่ม "ยกเลิก" เป็น `btn-secondary` หรือ `btn-danger` — ต้องเป็น `btn-ghost`
- ❌ มีปุ่ม `btn-primary` มากกว่า 1 ปุ่มใน footer/header เดียวกัน (primary มีได้ปุ่มเดียว = action หลัก)

---

#### 31.2 — Create/Edit Footer (single-step) — ลำดับตายตัว

```html
<div class="drawer-footer">
  <button class="btn btn-ghost" onclick="closeDrawer()">ยกเลิก</button>
  <div class="footer-spacer"></div>
  <!-- [optional] ปุ่มร่าง — เฉพาะ entity ที่มี draft state จริง (ดู 31.5) -->
  <button class="btn btn-secondary" onclick="saveDraft()">
    <i data-lucide="save" class="w-4 h-4"></i><span>บันทึกร่าง</span>
  </button>
  <button class="btn btn-primary" onclick="submitCreate()">
    <i data-lucide="check" class="w-4 h-4"></i><span>ยืนยันสร้าง</span>
  </button>
</div>
```
**ลำดับ (ซ้าย→ขวา) บังคับ:** `ยกเลิก (ghost)` → spacer → `[บันทึกร่าง (secondary)]` → `ปุ่มหลัก (primary)`.
- **Label ปุ่ม primary ตายตัวตามโหมด (ดู `knowledge/microcopy.md`):** Create = `ยืนยันสร้าง` · Edit = `บันทึกการแก้ไข` · Wizard step สุดท้าย = `ยืนยันสร้าง` — ห้ามแต่งคำใหม่ต่อ feature
- ปุ่ม primary อยู่ **ขวาสุดเสมอ**
- ปุ่ม ghost "ยกเลิก" อยู่ **ซ้ายสุดเสมอ**
- ใช้ `.footer-spacer` (defined ใน skeleton) ดันปุ่มหลักไปขวา — **ห้าม** inline `<div style="flex:1">` (ใช้ class แทนเพื่อ consistency)

---

#### 31.3 — Create/Edit Footer (multi-step wizard) — ลำดับตายตัว

```html
<div class="drawer-footer">
  <!-- ซ้าย: step 1 = ยกเลิก (ghost) / step >1 = กลับ (secondary) -->
  ${step > 1
    ? `<button class="btn btn-secondary" onclick="goToStep(${step-1})"><i data-lucide="arrow-left" class="w-4 h-4"></i><span>กลับ</span></button>`
    : `<button class="btn btn-ghost" onclick="closeDrawer()">ยกเลิก</button>`}
  <div class="footer-spacer"></div>
  <!-- [optional] บันทึกร่าง — เฉพาะ entity ที่มี draft state จริง -->
  <!-- ขวา: step < last = ถัดไป (primary) / step = last = ยืนยัน (primary) -->
  ${step < lastStep
    ? `<button class="btn btn-primary" onclick="goToStep(${step+1})"><span>ถัดไป</span><i data-lucide="arrow-right" class="w-4 h-4"></i></button>`
    : `<button class="btn btn-primary" onclick="submitWizard()"><i data-lucide="check" class="w-4 h-4"></i><span>ยืนยันสร้าง</span></button>`}
</div>
```
**บังคับ:**
- ปุ่ม "ถัดไป": ลำดับ icon = ข้อความ **ก่อน** icon (`<span>ถัดไป</span>` แล้ว `arrow-right`) — ทิศทาง icon ตรงกับการเดินหน้า
- ปุ่ม "กลับ": icon **ก่อน** ข้อความ (`arrow-left` แล้ว `<span>กลับ</span>`)
- ปุ่มร่างใน wizard: ถ้ามี ให้วางก่อน primary เหมือน single-step (ไม่บังคับให้มี — entity ส่วนใหญ่ของ wizard ไม่ต้องมีร่างก็ได้)

---

#### 31.4 — View Drawer — Footer + Header Actions

**Footer ของ view drawer (read-only detail):**
```html
<div class="drawer-footer">
  <div class="drawer-footer-meta">version 1 · อัปเดตล่าสุด ${formatDateTime(r.updatedAt)}</div>
  <div class="footer-spacer"></div>
  <button class="btn btn-secondary" onclick="closeDrawer()">ปิด</button>
</div>
```
**บังคับ:**
- ปุ่มขวาสุด = `ปิด` เป็น `btn-secondary` **เท่านั้น** — ❌ ห้าม `btn-danger`, ❌ ห้าม `btn-primary`
- ซ้าย = metadata (timestamp/version) สี mute — เป็น text ไม่ใช่ปุ่ม
- View drawer footer **ห้ามมี** action ปุ่มอื่น (edit/approve/delete) — action พวกนี้อยู่ที่ **header-right** เท่านั้น (ดูด้านล่าง)

**Header actions ของ view drawer (อยู่ header-right เสมอ):**
```html
<div class="drawer-header-actions">
  <!-- action buttons ตาม status — สีตาม role (31.1) -->
  <button class="btn btn-sm btn-secondary" onclick="openDrawer('edit','${r.id}')">
    <i data-lucide="pencil" class="w-3.5 h-3.5"></i><span>แก้ไข</span></button>
  <button class="btn btn-sm btn-danger" onclick="confirmDeactivate('${r.id}')">
    <i data-lucide="power-off" class="w-3.5 h-3.5"></i><span>ปิดใช้งาน</span></button>
  <span class="drawer-header-divider"></span>
  <button class="icon-btn" onclick="closeDrawer()"><i data-lucide="x" class="w-4 h-4"></i></button>
</div>
```
**ลำดับ (ซ้าย→ขวา) บังคับ:** `action buttons (เรียงจากเบาไปหนัก: secondary → primary → danger)` → `divider` → `icon-btn ปิด (X)`.
- icon-btn ปิด (X) อยู่ **ขวาสุดเสมอ** มี divider คั่นก่อนหน้า
- action ปุ่มสีตาม role: Edit=secondary, Approve/Convert=primary, Reject/ปิดใช้งาน/ลบ=danger
- ถ้า status เป็น read-only ล้วน (เช่น รออนุมัติ, archived ที่ไม่มี action) → header มีแค่ icon-btn ปิด (X) อย่างเดียวก็ได้ แต่ถ้ามี action ต้องเรียงตาม contract นี้

**ข้อยกเว้น — Approval flow (Reject/Return/Approve):**
ใน drawer ที่เป็น approval (เช่น PO/Invoice รออนุมัติ) ลำดับเชิง UX ที่ยอมรับได้คือ **negative ก่อน positive**: `Reject (danger)` → `Return/ส่งกลับ (secondary)` → `Approve (primary)` → divider → icon-btns. กรณีนี้ danger อยู่ซ้ายสุดได้ (เพราะเป็น flow ที่ user ต้องเลือกระหว่าง 3 ทาง) — แต่ยังบังคับ: Reject = `btn-danger` (ไม่ใช่ `btn-link` แดง), Approve = `btn-primary`, ปุ่มปิด X ขวาสุด.

---

#### 31.5 — เมื่อไรมี "บันทึกร่าง" (กฎตัดสิน ไม่ใช่แล้วแต่ feature)

ปุ่ม "บันทึกร่าง" (`saveDraft`) ใส่ได้ **ก็ต่อเมื่อ entity มี draft state จริง** — ตรวจจาก:
- FRD `05_RULES.md` หรือ BRD มี status `draft` / `ฉบับร่าง` ใน lifecycle ของ entity นั้น **หรือ**
- entity มี DOA approval flow (สร้างแล้วต้องรออนุมัติ → ร่างไว้ก่อน submit ได้)

**ถ้า entity ไม่มี draft state** (เช่น UOM Master — สร้างแล้ว active ทันที ไม่มีร่าง) → ❌ **ห้ามใส่** ปุ่มบันทึกร่าง. Footer มีแค่ `ยกเลิก` + `ปุ่มหลัก`.

**Consistency requirement:** ภายในไฟล์ HTML เดียว — entity ที่มี draft state ต้องใส่ปุ่มร่าง **ทุกตัว**, entity ที่ไม่มี draft state ต้อง **ไม่ใส่ทุกตัว**. ห้ามมีบ้างไม่มีบ้างในระดับเดียวกัน.

---

## Group 10: Bulk Data Import (Rule 32)

### Rule #32 — CSV Import Convention (BREAKING)
ทุก feature ที่เป็น **master/registry list** (Chart of Accounts, Vendor, Product, Posting Group, Payment Term, ฯลฯ) ที่ต้องรองรับการนำเข้าข้อมูลจำนวนมาก ให้ใช้ **CSV Import แบบมาตรฐานเดียวกันนี้เสมอ** — ห้ามออกแบบ flow import ใหม่ต่อ feature.

> **กฎสำคัญสุด:** import ต้อง **preview + ยืนยันก่อนเขียนข้อมูลเสมอ** — ห้าม apply ทันทีหลังเลือกไฟล์. ผู้ใช้ต้องเห็นผลตรวจสอบ (ผ่าน/ไม่ผ่านกี่แถว + แถวไหนพัง) แล้วกดยืนยันถึงจะเขียนจริง.

---

#### 32.1 — Import = Modal (ไม่ใช่ Drawer)
CSV Import ใช้ **modal ลอยกลางจอ** ขนาดใหญ่ (`.modal.is-lg` ~680px) — ไม่ใช่ drawer. นี่เป็น **ข้อยกเว้นที่ตั้งใจของ Rule #14** (ปกติ form = drawer) เพราะ import เป็น action+confirm ในตัว ไม่ใช่ entity form. Modal body scroll ได้ (preview ยาว).

#### 32.2 — Template Download อยู่ใน Modal
ปุ่ม **"ดาวน์โหลด Template"** ต้องอยู่**ใน modal upload เสมอ** (ไม่แยกไปอยู่ page header) — ผู้ใช้ที่ยังไม่มีไฟล์กดโหลด template ได้จากจุดเดียวกับที่อัปโหลด. Template เป็น `.csv` มี **UTF-8 BOM** (`\uFEFF`) นำหน้าเพื่อให้ Excel เปิดภาษาไทยไม่เพี้ยน + header row + ตัวอย่างข้อมูลจริงหลายแถว.

#### 32.3 — Validate + Result ก่อน Apply (บังคับ)
หลังเลือกไฟล์ → parse → validate ทันที → แสดง:
- **สรุปจำนวน:** "สำเร็จ X แถว · ไม่ผ่าน Y แถว" (chip เขียว/แดง)
- **รายการแถวที่ไม่ผ่าน:** บอก**รหัส + เหตุผล**รายแถว (เช่น "1-2 — ประเภทไม่ถูกต้อง", "9-9-9 — ไม่พบบัญชีแม่") ใน scrollable list
- **preview table:** ตัวอย่างข้อมูลที่จะนำเข้า (แถวเสีย highlight)
- ปุ่มยืนยัน **disabled** ถ้า valid = 0

#### 32.4 — Confirm = Apply, Cancel = ยกเลิก
- กด **ยืนยันนำเข้า** = เขียนข้อมูล (เฉพาะแถวที่ผ่าน — แถวเสียถูกข้าม + รายงานใน toast ว่าข้าม Y แถว)
- กด **ยกเลิก** = ปิด modal ไม่เขียนอะไร
- Replace mode (destructive) ใช้ **inline warning** ใน modal (ไม่ nest modal ซ้อน modal)

#### 32.5 — 2 โหมดเสมอ: Replace (default) + Merge
- **Replace** — ลบ master เดิมทั้งหมด แล้วโหลดใหม่ (default — เหมาะตั้งค่าครั้งแรก/sandbox)
- **Merge by code** — upsert: รหัสซ้ำ=อัปเดต / ใหม่=เพิ่ม / ที่เหลือคงไว้ (ปลอดภัยเมื่อมีข้อมูล/transaction แล้ว)
- ห้ามมีแค่ replace อย่างเดียว — master ที่มี GL movement/transaction การ replace ล้วนเสี่ยง orphan

#### 32.6 — Consistency (hierarchy master)
สำหรับ master ที่เป็นลำดับชั้น (parent-child): ถ้าแถวแม่ "ไม่ผ่าน" → แถวลูกต้องถูก flag ไม่ผ่านด้วย (กัน orphan) วน flag จนนิ่งก่อน import.

**Implementation note:** ใช้ `FileReader.readAsText(file,'UTF-8')` + `Blob`+`URL.createObjectURL` สำหรับ download. **ห้าม** ใช้ localStorage/sessionStorage. CSV parser ต้องรองรับ quoted field + comma ใน quote.

**Banned:**
- ❌ import เป็น drawer (ต้องเป็น modal)
- ❌ apply ทันทีหลังเลือกไฟล์ (ต้อง preview+confirm)
- ❌ ปุ่ม template download นอก modal
- ❌ replace อย่างเดียวไม่มี merge
- ❌ ไม่บอกว่าแถวไหนไม่ผ่าน

---

## Group 11: Hint & Help Text (Rule 33)

### Rule #33 — Hint = Hover Tooltip, Never a Banner (BREAKING)
คำอธิบาย/คำแนะนำการใช้งานที่ "อ่านครั้งเดียวก็พอ" (เช่น feature นี้คืออะไร, section นี้ทำงานยังไง, ตารางนี้หมายถึงอะไร) **ห้ามทำเป็นแผง info-banner ลอยเหนือเนื้อหา** — ให้ทำเป็น **icon `i` เล็ก ๆ ที่ hover แล้วแสดง tooltip** เท่านั้น

> **เหตุผล:** banner กินพื้นที่แนวตั้งถาวร, ดึงสายตาจากเนื้อหาจริง (ตาราง/ฟอร์ม), และผู้ใช้ที่รู้แล้วต้องเลื่อนผ่านทุกครั้ง. hint ที่ดีต้อง "อยู่เงียบ ๆ จนกว่าจะถาม" — discoverable แต่ไม่รบกวน.

#### 33.1 — รูปแบบมาตรฐาน
- icon = `<i data-lucide="info">` (หรือ `help-circle`) ขนาด w-3.5 สีเทา (`--c-mute-3`), hover เป็นสี primary
- วางต่อท้าย **title ของ section/card/field** ที่มันอธิบาย
- tooltip แสดงตอน hover เท่านั้น (pure CSS `:hover::after`) — พื้น navy (`--c-navy`), ตัวขาว, max-width ~340px, มี arrow ชี้, z-index สูง
- `cursor:help`

#### 33.2 — เมื่อไหร่ใช้อะไร
| ความต้องการ | ใช้ |
|---|---|
| อธิบาย feature/section คืออะไร (อ่านครั้งเดียวพอ) | **hint icon + tooltip** (Rule นี้) |
| คำเตือน/ผลลัพธ์ของ action ที่กำลังจะเกิด (destructive, irreversible) | `.note.is-warn` inline (คงไว้ได้ — นี่ไม่ใช่ hint) |
| สถานะ/ผลลัพธ์ที่ระบบต้องรายงาน (เช่น import result) | summary block ปกติ (ไม่ใช่ hint) |
| help ของ field เดี่ยวในฟอร์ม | `.field-help` ใต้ field (คงไว้) |

#### 33.3 — Banned
- ❌ info-banner / callout box ลอยเหนือ list/table เพื่ออธิบายว่า feature คืออะไร
- ❌ กล่องสีฟ้า/เหลืองถาวรที่เป็นแค่ "คำแนะนำการใช้งาน" (ไม่ใช่ warning ของ action)
- ❌ ย่อหน้าอธิบายยาว ๆ คั่นระหว่าง header กับเนื้อหา

**ข้อยกเว้น:** `.note.is-warn` ที่เป็น **คำเตือนของ action จริง** (เช่น "จะลบข้อมูลเดิม N รายการ" ใน import modal) ไม่ถือเป็น hint — คงไว้ได้ เพราะผูกกับการตัดสินใจ ณ ตอนนั้น ไม่ใช่คำอธิบายทั่วไป

**CSS reference (hint-i):**
```css
.hint-i { display:inline-flex; width:18px; height:18px; color:var(--c-mute-3); cursor:help; position:relative; }
.hint-i:hover { color:var(--c-primary); }
.hint-i::after { content:attr(data-tip); position:absolute; top:calc(100% + 8px); left:0;
  width:max-content; max-width:340px; padding:8px 11px; background:var(--c-navy); color:#fff;
  font-size:12px; line-height:1.5; border-radius:8px; opacity:0; visibility:hidden; transition:opacity 140ms; z-index:50; }
.hint-i:hover::after { opacity:1; visibility:visible; }
```

---

## Group 12: Input, Stability & Coverage (Rules 34-37)

### Rule #34 — Search-Select แทน Plain `<select>` เมื่อข้อมูลเยอะ/เป็น lookup (BREAKING)
`<select>` ธรรมดาใช้ได้เฉพาะ **enum สั้น ๆ คงที่** (สถานะ, ประเภท, ใช่/ไม่ใช่ — โดยทั่วไป ≤ 8 ตัวเลือก). เกินกว่านั้น หรือเป็นการ **เลือกจาก master/registry ที่อื่น** ต้องใช้ **search-select (searchable dropdown)** เสมอ — พิมพ์เพื่อกรอง + ไฮไลต์คำที่ตรง + เลือกได้ด้วยคีย์บอร์ด.

**เกณฑ์ตัดสิน (ใช้ search-select เมื่อเข้าข้อใดข้อหนึ่ง):**
- ตัวเลือก **> 8 รายการ** (หรือไม่รู้จำนวนแน่ชัด / เติบโตได้)
- เป็น **lookup จาก master อื่น** — ลูกค้า, สินค้า, ผู้ขาย, บัญชี (COA), คลัง, พนักงาน, โครงการ, เลขเอกสารอ้างอิง ฯลฯ
- ตัวเลือกมี **มากกว่า 1 มิติ** ที่ผู้ใช้ค้นได้ (รหัส + ชื่อ + รายละเอียด)

**ใช้ plain `<select>` ต่อไปได้เมื่อ:** enum ปิด/สั้น เช่น สถานะ (`active/inactive`), ประเภทเอกสาร 3-4 แบบ, ลำดับความสำคัญ (สูง/กลาง/ต่ำ). ตัวกรองใน filter-bar ที่เป็น enum สั้น ก็ยังเป็น `<select>` ได้.

**มาตรฐานการ implement (ห้ามออกแบบใหม่):**
- มี helper สำเร็จใน `file-skeleton.template.html` แล้ว — `searchSelectHTML(key, {placeholder})` + `initSearchSelect(key, {options, value, onSelect})`. option = `{ value, label, sub?, icon?, right? }`.
- โครง 1 ช่อง = search icon ซ้าย → input → (chevron-down ปกติ / ปุ่ม `x` ล้างค่าเมื่อเลือกแล้ว) ขวา → list overlay (`position:absolute`, ไม่ดันเนื้อหา).
- พิมพ์ = กรอง realtime + `<mark>` ไฮไลต์, ไม่พบ = empty text, คีย์บอร์ด ↑/↓/Enter/Esc ใช้ได้, คลิกนอก = ปิด.
- ตัวอย่างที่ทำงานจริง (verbatim source): combobox `brCombobox`/`ucpCombobox` ใน `references/drawer-standard/create-edit-drawer.js.txt` — generic helper คือ generalization ของชุดนี้.

**Banned:**
- ❌ `<select>` ที่มี `<option>` เกิน ~8 อันจาก master (เช่น dropdown ลูกค้า 200 ราย) — ผู้ใช้หาไม่เจอ, เลื่อนยาว
- ❌ search-select ที่ list **ดันเนื้อหาด้านล่าง** (ต้องเป็น overlay — ดู Rule #35)
- ❌ ทำ combobox เองแบบ bespoke ต่อ field ทั้งที่มี helper กลางแล้ว

---

### Rule #35 — Layout Stability / No Layout Shift (BREAKING)
หน้าจอ **ห้ามขยับ เด้ง หรือเบี้ยว** เมื่อมี interaction ปกติ (เปิด dropdown, เปิด drawer/modal, แสดง error, content โต). ทุก element ที่ "โผล่มา" ต้อง **ลอยทับ (overlay)** ไม่ใช่ดันของอื่น.

**บังคับ:**
- **Scrollbar gutter คงที่** — `html { scrollbar-gutter: stable }` + `.drawer-body`/`.modal-body { scrollbar-gutter: stable }` (อยู่ใน skeleton แล้ว). กัน content กระตุกซ้าย-ขวาเมื่อ scrollbar โผล่/หายตอนเปิด overlay หรือ list ยาวขึ้น.
- **Popover / suggestion / dropdown = `position:absolute` (หรือ fixed) overlay** — ห้าม render เป็น block ใน flow ที่ดันเนื้อหาใต้มันลงไป.
- **ตารางกว้างเกิน viewport** → ใส่ wrapper `overflow-x:auto` (scroll ในกล่อง) — ห้ามให้ตารางดันทั้งหน้ากว้างจน body มี horizontal scrollbar / เบี้ยว.
- **รูป/ไอคอน/avatar** ต้องมีขนาดกำหนด (width/height หรือ aspect-ratio) — กัน reflow ตอนโหลด.
- **ปุ่มที่สลับ label ตาม state** (เช่น "บันทึก" ↔ "กำลังบันทึก...") ควรกว้างพอ/`min-width` ไม่ให้ความกว้างกระตุก.

**แนะนำ (ลด jump):** field ที่ validate แล้วโชว์ error ใต้ field — ถ้า error สำคัญและเกิดบ่อย พิจารณาจองพื้นที่ (`min-height`) ของ `.field-error` ไว้ เพื่อไม่ให้ฟอร์มกระตุกตอน error โผล่.

**Banned:**
- ❌ list/popover ที่ `display:block` ใน flow แล้วดันปุ่ม/ฟิลด์ใต้มัน
- ❌ เปิด modal แล้ว body เลื่อนซ้าย (เพราะ scrollbar หาย) — ต้อง gutter stable
- ❌ ตารางทะลุขอบจน layout พัง — ต้อง wrap overflow-x

---

### Rule #36 — Button Symmetry & Integrity (BREAKING)
ปุ่มทุกปุ่ม **ข้อความต้องอยู่กึ่งกลาง ไม่เบี้ยว ไม่ตัดบรรทัด ไอคอนไม่ถูกบีบ** และปุ่มที่วางคู่กันต้องดู **สมมาตร**.

**บังคับ (อยู่ใน `.btn` ของ skeleton แล้ว — ห้าม override ให้เสีย):**
- `display:inline-flex; align-items:center; justify-content:center` — content อยู่กึ่งกลางทั้งแนวตั้ง/นอน
- **`padding-top: 2px`** — optical centering สำหรับฟอนต์ไทย: baseline ของ Noto Sans Thai ลอยสูงเมื่อ flex-center (เพราะ font เผื่อที่สระล่าง) → นัดจ์ลง 2px ให้ตัวอักษรเข้ากึ่งกลางปุ่มจริง. `.btn-sm`/`.bulk-bar .btn` ก็ใช้ `2px 11px 0`. **✅ ค่านี้ verified ด้วยการ render จริง** (ทนทุกเบราว์เซอร์ — ต่างจาก `text-box-trim` ที่รองรับเฉพาะ Chrome/Edge 133+, Safari 18.2+, Firefox ยังไม่รองรับ)
- `white-space:nowrap` — label ห้ามตัดบรรทัด (ปุ่มสูงไม่เท่ากัน = เบี้ยว)
- `.btn [data-lucide] { flex-shrink:0 }` — icon ไม่ถูกบีบเล็กลงเมื่อ label ยาว
- `height` คงที่ (36px ปกติ / 30px `.btn-sm`) — ทุกปุ่มในแถวเดียวกันสูงเท่ากัน

> **⚠️ ข้อห้ามสำคัญ (ภาษาไทยโดยเฉพาะ):** **ห้ามใส่ `line-height:1` หรือ `overflow:hidden` กับ *ตัวปุ่ม* ที่มีข้อความไทย** — เพราะจะ **ตัดสระบน/วรรณยุกต์/สระล่าง** ทำให้ตัวอักษรไทย "เบี้ยว/ลอย/หาย". ปล่อย `line-height` ตาม body (1.5) แล้วใช้ `padding-top:2px` จัด optical center. ภาษาอังกฤษไม่แสดงอาการเพราะไม่มีสระลอย — **เทสด้วยข้อความไทยจริงเสมอ**.

**ปุ่มที่วางคู่กัน (footer / toolbar):**
- ความสูงเท่ากันเสมอ (size class เดียวกัน — ห้ามผสม `.btn` กับ `.btn-sm` ในแถวเดียว)
- ปุ่มที่มี **น้ำหนักเท่ากัน** (เช่น 2 ปุ่มเลือกทาง) → ใส่ `.btn-eq` (min-width 104px) ให้กว้างสมมาตร
- **label ยาว → ปล่อยปุ่มโตตาม label** (nowrap) + container `flex-wrap` ดีกว่า. ถ้า *ต้อง* จำกัดความกว้างจริง → ใช้ `.btn-truncate` + ห่อ label ใน `<span class="lbl">` (truncate ที่ span ด้วย `overflow:hidden;text-overflow:ellipsis` ซึ่งตัด *เฉพาะแนวนอน* line-height 1.5 ไม่ตัดสระไทย) — **ห้าม `overflow:hidden` ที่ตัวปุ่ม**
- icon + label เรียงทิศตามความหมาย (ดู Rule #31.3 — "ถัดไป" label ก่อน icon ขวา, "กลับ" icon ซ้ายก่อน label)

**Banned:**
- ❌ `line-height:1` / `overflow:hidden` บน *ตัวปุ่ม* ที่มีข้อความไทย (ตัดสระ → เบี้ยว) — บั๊กที่พบบ่อย
- ❌ ปุ่ม `max-width` แคบ + label ยาว โดยไม่ truncate ที่ span → **ข้อความทะลุขอบปุ่ม**
- ❌ ปุ่มที่ label ยาวจน **ตัด 2 บรรทัด** → ปุ่มสูงเด้งไม่เท่าปุ่มข้าง ๆ
- ❌ icon ใน button ถูกบีบ (เพราะไม่มี `flex-shrink:0`)
- ❌ ผสมความสูงปุ่มในแถวเดียว / ปุ่มคู่ที่ควรสมมาตรแต่กว้างต่างกันมาก
- ❌ ปุ่มที่มีแต่ icon โดยไม่มีขนาดชัด → ใช้ `.icon-btn` ที่ขนาดตายตัวแทน

---

### Rule #37 — Requirement Coverage (อ่าน FRD/requirement ให้ครบ)
HTML ที่ออกต้อง **ครอบคลุมทุกสิ่งที่ FRD/requirement ระบุ** — ห้ามตกหล่น field, action, สถานะ, validation, หรือ journey ใด ๆ ที่อยู่ในขอบเขต (ยกเว้นที่อยู่ใน BRD §14.6 Functions Cut).

**บังคับ — ทำ Coverage Map ก่อน implement (Phase 1) แล้ว verify (Phase 5):**
สแกน input ทั้งหมด (FRD Pack 01_UI/02_API/05_RULES + Brief + screenshot + ข้อความ) แล้วสกัดเป็นรายการตรวจสอบ:
- **ทุก field** ที่ระบุ (รวม type, required, default, validation) → มีในฟอร์ม
- **ทุก action/ปุ่ม** (create/edit/view/delete/approve/export/import/...) → wire เป็น JS จริง
- **ทุก status** ใน lifecycle → แสดง + transition ได้
- **ทุก validation rule** (05_RULES) → enforce
- **ทุก route/หน้า** (01_UI Routes) → มีจริง refresh-safe
- **ทุก column** ที่ระบุในตาราง list

**กฎสำคัญ:** ถ้า requirement ระบุแต่ skill **ตั้งใจไม่ทำ** ต้อง log เหตุผลใน output summary (เช่น อยู่ใน Functions Cut, หรือ defer). ถ้า requirement **ไม่ได้ระบุ** แล้วเติม default → log ใน "Gaps Filled". **ห้ามเงียบ ๆ ตกหล่น** — ทุกอย่างที่ขาดต้องมีคำอธิบาย.

→ ใช้คู่กับ `references/gap-detection.md` (ตรวจของหล่นข้าม chain BRD→FRD→HTML)

**Banned:**
- ❌ implement แค่ happy path แล้วข้าม field/action/status ที่ FRD ระบุโดยไม่ log
- ❌ "ปุ่มหลอก" — ปุ่มที่ FRD ต้องการให้ทำงาน แต่ใน HTML กดแล้วไม่มีอะไรเกิด (ต้อง wire จริงด้วย mock)
- ❌ ลด validation ที่ 05_RULES ระบุ โดยไม่แจ้ง

---

## Group 13: Thai Rhythm · List · States · Format (Rules 38-43)

### Rule #38 — Thai Vertical Rhythm (optical centering, render-verified) (BREAKING)
ทุก element ที่ **fix-height + flex/auto center + มีข้อความไทย** ต้องตรวจว่าตัวอักษรไม่ "ลอยสูง" — เพราะ font metric ของ Noto Sans Thai เผื่อที่สระล่าง ทำให้ baseline ลอยสูงเมื่อ center. แก้ด้วย **padding-top มากกว่า padding-bottom เล็กน้อย** (optical nudge).

**ค่าที่ verify แล้ว (อยู่ใน skeleton):**
- `.btn` → `padding: 2px 14px 0` · `.btn-sm`/`.bulk-bar .btn` → `2px 11px 0`
- `.pill` → `padding: 4px 10px 3px`
- `.table td` → `padding: 13px 14px 11px`
- input/select → ไม่ต้อง nudge (acceptable อยู่แล้ว — อย่าแตะ เสี่ยงกระทบ cursor/placeholder)

**บังคับ:** element ใหม่ที่ fix-height + ไทย (tab, chip, badge, segmented, sidebar item, stat) → **ต้อง render จริงด้วยฟอนต์ไทยแล้วเทียบเส้นกึ่งกลางก่อน claim ว่าตรง** (ใช้ `scripts/audit.sh` + render snippet). ห้าม `line-height:1`/`overflow:hidden` ตาม Rule #36.

**Banned:** อ่าน CSS แล้วเดาว่า "ตรงแล้ว" โดยไม่ render — ไทยลอยสูงมองไม่เห็นจากโค้ด.

---

### Rule #39 — Empty State (always) (BREAKING)
ทุก list / table / section ที่ **อาจว่าง** ต้องมี empty state — **ห้ามปล่อยพื้นที่โล่ง**. ใช้ helper `emptyStateHTML({icon,title,desc,actionLabel,actionIcon,onAction})` (อยู่ใน skeleton): icon + title (ทำไมว่าง) + desc + **ปุ่ม action หลัก**.

**2 เคสต่างกัน:** (1) ยังไม่มีข้อมูลเลย → ชวน "สร้างรายการแรก"; (2) filter ไม่เจอ → ชวน "ล้างตัวกรอง". ข้อความ/ปุ่มต่างกัน.

**Banned:** tbody ว่างโล่ง · "ไม่มีข้อมูล" ลอย ๆ ไม่มี icon/action.

---

### Rule #40 — List Cell Atomicity: 1 ข้อมูล = 1 คอลัมน์ (BREAKING)
ในตาราง list view **ห้ามซ้อนข้อมูลคนละชนิดเป็นหลายบรรทัดในเซลล์เดียว** (ชื่อ + บริษัท/อีเมล ใต้กัน). ตัดสินใจจะแสดงข้อมูลใด → **ต้องเป็นคอลัมน์ของตัวเอง**.
- avatar + ชื่อ บรรทัดเดียว = OK (avatar = decoration)
- ชื่อ + บริษัท + อีเมล = **3 คอลัมน์แยก**
- แยกแล้วเกิน 8 คอลัมน์ (ชน Rule #16) → **ตัดตัวสำคัญน้อยลง view drawer** แทนการซ้อนบรรทัด

**Banned:** sub-line สีเทาใต้ค่าหลักในตาราง · `<div>ชื่อ</div><div class="sub">บริษัท</div>` ใน 1 เซลล์.

---

### Rule #41 — List Row = เปิด view, ไม่มีไอคอนดวงตา (BREAKING)
คลิก **แถว** ในตาราง list = เปิด view (drawer/landing) **เสมอ** + **ห้ามมีไอคอนดวงตา (eye)** ในคอลัมน์ action (ซ้ำซ้อน).
- `<tr class="is-clickable" onclick="openDrawer('view', id)">` + cursor:pointer
- action เหลือเฉพาะ non-view (edit, delete, more)
- checkbox/action cell ต้อง `event.stopPropagation()`

**Banned:** ปุ่ม eye เปิด view · แถว hover ได้แต่กดไม่ทำอะไร · กด checkbox แล้วเปิด view ตาม.

> **Pattern E (expandable)**: กดแถว = **expand รายละเอียด inline** (ถือเป็น "ดู" รูปแบบหนึ่ง — premise คือ no drawer/modal) → ก็ไม่มี eye เช่นกัน. รายละเอียดอยู่ในแถวที่กางออก ไม่ต้องมีปุ่ม "ดูรายละเอียดเต็ม" เปิด drawer ซ้ำ.

---

### Rule #42 — Long-list UX: Sticky Header + Thai-safe Truncation
ตาราง list ยาว: `.table-scroll.is-sticky` (หัวค้างเวลา scroll) + `.cell-truncate` (ตัด … แนวนอน line-height พอ → **ไม่ตัดสระไทย**) + `title="ค่าเต็ม"`. ห้าม wrap ข้อความยาวจนแถวสูงไม่เท่ากัน.

> **⚠️ sticky header ต้องมี `background` ทึบ *ที่ตัว `th`*** (ไม่ใช่แค่ `thead`) — ไม่งั้น row เลื่อนขึ้นมา**ทะลุซ้อนหัวตาราง**. อยู่ใน skeleton แล้ว (`background: var(--c-bg-off)` + `z-index:3` + `box-shadow` ทำ border-bottom). บั๊กนี้เห็นเฉพาะตอน **scroll จริง** → ต้อง render+scroll ทดสอบ.

---

### Rule #43 — Inline Validation + Reserved Error + Format Consistency
- **(43.1)** validate ตอน **blur** ด้วย `validateField(el, validator)` (คืน '' = ผ่าน / ข้อความ = error)
- **(43.2)** `.field-error` ใช้ `visibility:hidden` + `min-height` (อยู่ใน skeleton) → error โผล่แล้ว **ฟอร์มไม่กระตุก** (ต่อ Rule #35)
- **(43.3)** format ไทยกลางเสมอ: `fmtNumber()` `fmtMoney()` `fmtDate()` `fmtDateTime()` (th-TH/พ.ศ.) · ตัวเลขในตาราง = `.num` (tabular) + `col-num` ชิดขวา

**Banned:** validate เฉพาะตอน submit · error โผล่แล้วฟอร์มเลื่อน · ตัวเลขไม่ tabular เรียงไม่ตรงหลัก · date/money format คนละแบบในไฟล์เดียว.

---

## 📋 Pre-deploy Audit Checklist

ก่อน save HTML ลง outputs ต้องผ่านทั้งหมด:

- [ ] **Rule #1-2 CI/Font:** ใช้ CSS variables + Satoshi + Noto Sans Thai ✓
- [ ] **Rule #3-4 Layout:** Sidebar 232px gradient + Shell bar 52px white ✓
- [ ] **Rule #5-6 Components:** Lucide icons only + Page header pattern ✓
- [ ] **Rule #7-10 Structure:** Breadcrumb + KPI + Filter in card + Table footer ✓
- [ ] **Rule #11-15 Drawer/Modal:** Width correct + Slide animation + 3 close methods ✓
- [ ] **Rule #16 Table:** ≤ 8 columns ✓
- [ ] **Rule #17 Grid:** Responsive (auto-fit minmax or sm:grid-cols-N) ✓
- [ ] **Rule #18 Form:** field/field-label/field-help/field-error structure ✓
- [ ] **Rule #19 Spinner:** Global hide for number input ✓
- [ ] **Rule #20 Toggle:** div onclick + transform translateX ✓
- [ ] **Rule #21 Icon audit:** ทุก `<i data-lucide>` มี w-{N} h-{N} ✓
- [ ] **Rule #22 Wizard:** Full-height flex (if applicable) ✓
- [ ] **Rule #23 No emoji:** Grep result = 0 color emoji ✓
- [ ] **Rule #24 No dev-tool:** No debug panel / console.log / TODO ✓
- [ ] **Rule #25 renderIcons:** ใช้ `renderIcons()` ไม่ใช่ `lucide.createIcons()` ตรง ๆ ✓
- [ ] **Rule #26 Lean catalog:** (if Registry UI) ✓
- [ ] **Rule #27 Module-Feature Sidebar:** `.sb-module` + `.sb-module-header` button + `.sb-features` + `data-module`/`data-feature` everywhere ✓
- [ ] **Rule #28 Slim Top Bar:** No Help / Search / extras — only Breadcrumb + Notif + User Chip ✓
- [ ] **Rule #29 Render Preservation:** `render()` save+restore scroll (drawer-body/modal-body/window) + focus+cursor on active input — use `withRenderPreservation()` helper ✓
- [ ] **Rule #30 Fluid Content:** `.content` ไม่มี `max-width` cap — content stretch เต็ม viewport ✓
- [ ] **Rule #33 Hint convention:** คำอธิบายการใช้งาน = icon `i` + hover tooltip (ไม่ใช่ info-banner ลอยเหนือเนื้อหา); `.note.is-warn` เฉพาะ warning ของ action จริง ✓
- [ ] **Rule #32 CSV Import:** (ถ้าเป็น master/registry) modal `.is-lg` + template download ใน modal + validate+result(ผ่าน/ไม่ผ่านกี่แถว+แถวไหนพัง)+confirm ก่อน apply + 2 โหมด Replace/Merge + UTF-8 BOM ✓
- [ ] **Rule #31 Drawer Button Contract:** สีปุ่ม=role (ปิด/กลับ ห้ามแดง) + ลำดับ footer ตายตัว (ยกเลิก ghost ซ้าย / primary ขวา) + view footer มีแค่ `ปิด` secondary + header actions เรียง secondary→primary→danger→divider→X + ปุ่มร่างตามกฎ 31.5 ✓
- [ ] **Rule #34 Search-Select:** dropdown ที่ options เยอะ/lookup จาก master → ใช้ `searchSelectHTML`+`initSearchSelect` (พิมพ์กรอง+ไฮไลต์+คีย์บอร์ด) ไม่ใช่ `<select>` ยาว ✓
- [ ] **Rule #35 Layout Stability:** `scrollbar-gutter:stable` + popover/list เป็น overlay (ไม่ดันเนื้อหา) + ตารางกว้างใช้ wrapper overflow-x + รูป/ไอคอนมีขนาด ✓
- [ ] **Rule #36 Button Symmetry:** `.btn` justify-center + `padding-top:2px` (Thai optical center) + nowrap + icon flex-shrink:0 + ปุ่มแถวเดียวสูงเท่ากัน + ปุ่มคู่ `.btn-eq`; **ห้าม line-height:1/overflow บนปุ่มไทย** ✓
- [ ] **Rule #37 Requirement Coverage:** ทำ Coverage Map (field/action/status/validation/route ครบ) + ของที่ขาด/เติม log ใน summary — ไม่มีปุ่มหลอก ✓
- [ ] **Rule #38 Thai Rhythm:** element fix-height + ไทย (pill `4/3`, td `13/11`, btn `2px`) เข้ากึ่งกลาง — **render จริงด้วยฟอนต์ไทยเทียบเส้นกึ่งกลาง** ก่อน claim ✓
- [ ] **Rule #39 Empty State:** ทุก list/section ที่ว่างได้ มี `emptyStateHTML()` (icon+title+desc+action) — แยกเคส "ยังไม่มีข้อมูล" vs "filter ไม่เจอ" ✓
- [ ] **Rule #40 List Cell Atomicity:** 1 ข้อมูล = 1 คอลัมน์ — ห้ามซ้อน sub-line ใต้ค่าหลัก (เกิน 8 → ตัดลง drawer) ✓
- [ ] **Rule #41 List Row:** กดแถว = เปิด view (`.is-clickable`) · ไม่มีไอคอนดวงตา · checkbox/action `stopPropagation()` ✓
- [ ] **Rule #42 Long-list UX:** `.table-scroll.is-sticky` (หัวค้าง + **bg ทึบที่ th กัน row ทะลุ** — ทดสอบด้วยการ scroll จริง) + `.cell-truncate` (Thai-safe) + `title` ค่าเต็ม ✓
- [ ] **Rule #43 Validation+Format:** validate on-blur (`validateField`) + `.field-error` จองพื้นที่ (ไม่กระตุก) + format กลาง (`fmtMoney/fmtDate`) + `.num` tabular ชิดขวา ✓


---

## Group 13: State Completeness (Rules 44-45) — v3.13

### Rule #44 — Loading / Submitting State (BREAKING)
ทุก action ที่ "ส่งข้อมูล" (submit create/edit, ยืนยัน modal, import) ต้องมี submitting state มาตรฐานเดียว:
```js
async function submitCreate(){
  const btn = document.getElementById('btn-submit');
  btn.disabled = true;
  btn.innerHTML = '<i data-lucide="loader-2" class="w-4 h-4 spin"></i><span>กำลังบันทึก…</span>';
  renderIcons();
  await new Promise(r=>setTimeout(r,600));   // mock — dev แทนด้วย fetch()
  closeDrawer(); showToast('สร้างรายการสำเร็จ','success');
}
```
- ปุ่ม primary → `disabled` + icon `loader-2` หมุน (`.spin` อยู่ใน skeleton) + label เปลี่ยนเป็น "กำลังบันทึก…/กำลังลบ…" ตาม microcopy.md
- ระหว่าง submitting: ปุ่มอื่นใน footer `disabled` ด้วย — กัน double-submit
- เสร็จแล้ว: ปิด drawer/modal → toast success (ไม่ toast ก่อนปิด)
- **ห้าม:** spinner ลอยกลางจอ, ปุ่มยังกดซ้ำได้, toast ซ้อน 2 อัน

### Rule #45 — Disabled / Read-only Field + Form Section Grouping
**Disabled/Read-only (ตายตัว):**
```css
.input:disabled, .input[readonly] {
  background: var(--c-line-3); color: var(--c-mute-2);
  cursor: not-allowed; border-color: var(--c-line-2);
}
```
- ค่าที่ระบบ generate (รหัสเอกสาร, วันที่สร้าง) = `readonly` + `field-help` อธิบาย "ระบบกำหนดให้อัตโนมัติ"
- View drawer แสดงข้อมูลเป็น text (label+value) — **ไม่ใช่** input disabled ทั้งฟอร์ม

**Form Section Grouping (ฟอร์ม >6 fields ต้องแบ่งกลุ่ม):**
```html
<div class="form-section">
  <div class="form-section-title">ข้อมูลทั่วไป</div>   <!-- --fs-cap uppercase --c-mute -->
  <div class="form-grid">…fields…</div>
</div>
```
- หัวกลุ่ม = uppercase caption (`--fs-cap`, letter-spacing 0.08em) + margin-top `--sp-xl` ระหว่างกลุ่ม
- ลำดับกลุ่มมาตรฐาน: ข้อมูลทั่วไป → รายละเอียด/รายการ → การเงิน/เงื่อนไข → หมายเหตุ/แนบไฟล์

---

## Group 14: Placement Contract (Rule 46) — v3.13 ⭐

### Rule #46 — Placement Contract (BREAKING) — "ของทุกอย่างมีที่อยู่ตายตัว"
แก้ปัญหา: ปุ่ม/badge/สถานะ อยู่คนละที่ในแต่ละไฟล์ทั้งที่เป็นของอย่างเดียวกัน

**46.1 ปุ่ม "สร้าง" (List view):**
- อยู่ที่ `.ph-actions` (page header ขวาบน — เหนือ filter/table) **ที่เดียวเท่านั้น**
- เป็น `btn-primary` + icon `plus` `w-4 h-4` + label ตาม microcopy (`สร้าง[ชื่อ entity]`)
- ปุ่ม primary ใน `.ph-actions` มีได้ปุ่มเดียว อยู่**ขวาสุด** — ปุ่มรอง (Export, Import, ตัวกรองพิเศษ) เป็น `btn-secondary` เรียงซ้ายของมัน
- ❌ ห้าม: ปุ่มสร้างใน filter bar, ลอยใน card, floating action button, ใต้ตาราง

**46.2 ปุ่ม primary ใน Drawer:** อยู่ **footer ล่างขวาสุดชิดขวา** เสมอ (ตาม Rule 31.2/31.3) — ไม่มีข้อยกเว้น ไม่ว่าฟอร์มสั้นแค่ไหน; footer เป็น sticky อยู่ล่าง drawer เสมอ (ไม่ลอยตามเนื้อหา)

**46.3 Status badge/pill — ตำแหน่งตายตัว "หลังชื่อ เว้น 8px":**
| ที่ | ตำแหน่ง |
|---|---|
| List row | คอลัมน์สถานะของตัวเอง (ไม่ปนกับคอลัมน์ชื่อ — Rule #40) |
| Drawer header (view/edit) | บรรทัดเดียวกับ title, ถัดจากชื่อ ห่าง `--sp-sm` (8px) |
| Detail page header | เหมือน drawer header — หลัง `.ph-title` ใน `.ph-title-row` |
| Card grid | มุมขวาบนของ card |
- pill เดียวต่อ 1 record ในระดับ header (สถานะหลัก) — สถานะรอง (tag, ประเภท) เป็น text meta ไม่ใช่ pill ซ้อนกันหลายเม็ด (เกิน 2 pills = ย้ายลง body)

**46.4 ปุ่ม แก้ไข / ลบ / actions ของ record:**
| ที่ | รูปแบบ |
|---|---|
| List row | คอลัมน์ actions ขวาสุด: icon-btn `pencil` → `trash-2` (ลำดับตายตัว แก้ไขก่อนลบ) หรือ `⋮ more-vertical` ถ้า >3 actions |
| View drawer | header actions ตาม Rule 31.4: secondary (`แก้ไข`) → primary (action หลักถ้ามี เช่น `อนุมัติ`) → danger (`ลบ`) → divider → X |
| Edit drawer | ไม่มีปุ่มลบใน edit — ลบทำจาก view drawer หรือ list row เท่านั้น |
- ปุ่มลบกดแล้ว → Modal confirm (Pattern D) เสมอ — ห้ามลบทันที
- ❌ ห้าม: ปุ่มแก้ไข/ลบกระจายอยู่ใน body ของ drawer, ปุ่มลบใน footer ของ view drawer (footer view = `ปิด` อย่างเดียว)

**46.5 ตำแหน่งมาตรฐานอื่น:**
- Toast: มุม**ขวาล่าง**, ซ้อนขึ้นบน, auto-dismiss 3.5s
- Search: ช่องแรกซ้ายสุดของ filter bar เสมอ + icon `search`
- ปุ่ม reset filter: ขวาสุดของ filter bar, `btn-ghost` + icon `rotate-ccw`
- Pagination: ซ้ายของ table footer / record count ขวา (ตาม Rule #10)
- Checkbox select-all: หัวคอลัมน์แรก 40px (ตาม Rule #16)

---

## Group 15: Stepper Standard (Rule 47) — v3.13

### Rule #47 — Stepper Standard กลาง (BREAKING)
Stepper ทุกที่ (drawer wizard / page wizard / onboarding) ใช้ **component เดียวจาก skeleton** — `.stepper > .step (.step-dot + .step-label) + .step-connector`:
- **States:** `.is-done` (dot ขอบ+เลข teal — ใช้ icon `check` แทนเลขได้), `.is-current` (dot พื้น primary ตัวหนังสือขาว + label ink หนา), upcoming (default เทา)
- **ตำแหน่ง:** page wizard → `.wizard-stepper-band` (Rule #22). **drawer create/edit wizard → ใช้ stepper ของ Pattern B แทน** (`.d-stepper > .stepper-item/.stepper-circle` 32px — v6.1 มีใน skeleton แล้ว, locked to `references/drawer-standard/`) — `.drawer-stepper-band` เป็น legacy สำหรับ drawer
- **จำนวน:** 2–5 steps; เกิน 5 = ต้องรวบขั้นตอน (ฟอร์มยาวใช้ form-section แทน ไม่ใช่เพิ่ม step)
- **Label:** คำนามสั้น 1–3 คำ ("ข้อมูลทั่วไป", "รายการสินค้า", "ตรวจสอบ") — step สุดท้ายของ create ชื่อ "ตรวจสอบและยืนยัน" เสมอ
- **ห้าม:** progress bar %, stepper แนวตั้ง, จุดไร้ label, ออกแบบ stepper ใหม่เองต่อ feature

---

## Group 16: Landing / Home Page Standard (Rule 48) — v3.13

### Rule #48 — Landing/Home Standard (3 variants เท่านั้น)
หน้า landing/home ของ module หรือระบบ เลือกจาก **3 variants ตายตัว** (ดู `patterns/M_landing-home.md` + design-system `#/landing`):
| Variant | ใช้เมื่อ |
|---|---|
| **M1 Hero + Tiles** | หน้าแรกของทั้งระบบ / module ใหญ่ — hero band (title+desc+CTA) + feature tiles grid |
| **M2 Workspace Grid** | หน้า workspace ของ user — การ์ดงานค้าง/shortcut/รายการล่าสุด |
| **M3 KPI Home** | หน้าแรกเชิง monitoring — stats row + chart + รายการล่าสุด |
- Hero band: bg gradient Navy→Navy-2, title ขาว, ไม่มีรูป stock/illustration ภายนอก
- Tile: icon (Lucide ใน circle) + ชื่อ + คำอธิบาย 1 บรรทัด + chevron — กดได้ทั้งการ์ด
- ❌ ห้าม: carousel, banner รูปภาพ, marketing copy เกินจริง — นี่คือ internal tool

---

## Group 17: Minimal Scrollbar (Rule 49) — v4.2

### Rule #49 — Minimal Scrollbar (ห้ามใช้ default scrollbar เด็ดขาด)
ทุกไฟล์ HTML ต้อง style scrollbar เองทั้งระบบ — default scrollbar ของ browser (แถบเทาหนา) ถือว่า FAIL:
- **ขนาด:** บางมาก `5px` (ทั้ง width/height) · thumb มุมมน `border-radius: 99px` · **track + corner โปร่งใส**
- **พื้นสว่าง (content, ตาราง, drawer ขาว):** thumb `rgba(17,17,17,.14)` → hover `.26`
- **พื้นเข้ม (sidebar `#111111`, slide panel):** thumb **ขาวโปร่ง** `rgba(255,255,255,.28)` → hover `.42`
- **Firefox:** `scrollbar-width: thin` + `scrollbar-color` คู่กันเสมอ (webkit อย่างเดียวไม่พอ)
- CSS block มาตรฐานอยู่ใน skeleton แล้ว (`templates/file-skeleton.template.html` §SCROLLBAR) — **copy ไปทั้ง block ห้ามเขียนเอง**
- scroll container ที่สร้างใหม่ (list ยาว, panel, code block) ไม่ต้องเขียนซ้ำ — global selector ครอบให้แล้ว ยกเว้นอยู่บนพื้นเข้มนอก `.sidebar/.slide` ให้เพิ่ม selector เข้า group พื้นเข้ม
- ❌ ห้าม: `overflow: overlay` (deprecated), ซ่อน scrollbar ทั้งหมด (`display:none` / `width:0`) — ผู้ใช้ต้องเห็นตำแหน่ง scroll เสมอ

- [ ] **Rule #44 Loading/Submitting:** ปุ่ม submit → disabled + loader-2 spin + label "กำลัง…" + กัน double-submit + toast หลังปิด ✓
- [ ] **Rule #45 Disabled/Read-only + Form Section:** disabled/readonly style ตาม token + ฟอร์ม >6 fields แบ่ง `.form-section` + หัวกลุ่ม caption ✓
- [ ] **Rule #46 Placement Contract:** ปุ่มสร้างอยู่ `.ph-actions` ขวาสุด · drawer primary ล่างขวาชิด · badge หลังชื่อ 8px (pill เดียวระดับ header) · แก้ไข→ลบ ลำดับตายตัว · ลบผ่าน modal confirm เสมอ ✓
- [ ] **Rule #47 Stepper:** ใช้ `.stepper` กลางจาก skeleton (2-5 steps, states is-done/is-current, step สุดท้าย "ตรวจสอบและยืนยัน") — ไม่ออกแบบเอง ✓
- [ ] **Rule #48 Landing:** (ถ้ามีหน้า home/landing) ใช้ M1/M2/M3 เท่านั้น — ไม่มี carousel/banner ✓
- [ ] **Rule #49 Scrollbar:** มี block ::-webkit-scrollbar 5px + scrollbar-width:thin + track โปร่งใส — ไม่ใช่ default scrollbar ✓
