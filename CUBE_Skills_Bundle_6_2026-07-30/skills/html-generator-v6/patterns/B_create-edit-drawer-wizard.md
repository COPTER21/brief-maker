# Pattern B — Create / Edit Drawer (CUBE Admin CI v2 — Wizard)

> **⭐ AUTHORITATIVE STANDARD (locked to `pr.html`).** The create + edit drawer in this
> pattern MUST render **100% identical** to the reference. This supersedes any older
> `.drawer` / `.drawer-backdrop` / `.field-row` markup.
>
> **Verbatim source of truth (copy from here — do not improvise):**
> - `references/drawer-standard/_SOURCE_pr-reference.html` — full working reference
> - `references/drawer-standard/drawer.css.html` — required CSS (tokens + classes)
> - `references/drawer-standard/create-edit-drawer.js.txt` — full create/edit wizard JS
> - `references/drawer-standard/shared-helpers.js.txt` — formatMoney / renderPill / showToast / formatThaiDate
>
> **Rule:** When you generate a create/edit drawer, reproduce the structure, class names,
> inline styles, spacing, and animation below **exactly**. Adapt only the field set, labels,
> entity names, and mock data to the target feature — never the shell, the stepper, the
> footer contract, the toggle, or the CSS tokens.

---

## 🧩 v6.1 — Skeleton ships the Pattern B chrome

`templates/file-skeleton.template.html` มี CSS ของ header/stepper/footer ตาม pr.html ให้แล้ว
— ไม่ต้อง copy จาก `drawer.css.html` อีกสำหรับ 3 ส่วนนี้:

| ส่วน | Class ใน skeleton | สเปค |
|---|---|---|
| Header | `.dw-head > .dw-head-row` → `.dw-eyebrow` (uppercase 11px + icon) + `.dw-title` (20px/700 navy) + `.dw-sub` + ปุ่มปิด `.top-icon-btn` | ห้ามใช้ `.drawer-header` + avatar วงกลมกับ create/edit |
| Stepper | `.d-stepper > .stepper-item(.active/.done) > .stepper-circle + .stepper-label` | วงกลม 32px · active = primary ทึบ + ring 4px · connector `::after` เปลี่ยนสีตาม done · อยู่ **ใน** `.dw-head` (margin-top 18px) ไม่ใช่ band แยก |
| Footer | `.dw-footer` = space-between → ซ้าย: `ย้อนกลับ` (secondary, step>1) · ขวา `.dw-footer-right`: `ยกเลิก` (ghost) + `[บันทึกแบบร่าง]` + primary | ตาม contract ของ reference (supersede layout เดิมที่ ghost อยู่ซ้ายสุด) |

ที่เหลือ (form-grp, combobox, line table, toggle ฯลฯ) ยังต้องอ่าน reference ตามเดิม.

---

## 🎯 When to Use

✅ Create a new record (form drawer, single OR multi-step wizard)
✅ Edit an existing record (same drawer, pre-filled)
✅ Line-item documents (PR/PO/SO/Quotation) with totals, VAT, WHT, discount
✅ Multi-step capture (info → lines → attachments → review)

❌ Simple confirm/delete → Pattern D (modal — see `confirmCancel()` in reference)
❌ Read-only detail → Pattern C (view drawer)

---

## 🧱 Drawer Shell — EXACT (overlay-wrap → backdrop + drawer-panel)

Do **NOT** use `.drawer` / `.drawer-backdrop`. The standard shell is:

```
#overlay-root                         ← persistent empty div in <body>
└─ .overlay-wrap (position:fixed; inset:0; z-index:50)
   ├─ .backdrop (rgba(0,0,0,.45), click = close)
   └─ .drawer-panel.drawer-enter      ← max-width 920px (wide). Add .standard for 680px.
      └─ #create-drawer-content (flex column, height:100%)
         ├─ Header  (padding 18px 24px 16px; border-bottom; flex-shrink:0)
         │   ├─ eyebrow (uppercase 11px + icon) + <h2 20px/700 navy>
         │   ├─ close .top-icon-btn (transparent, x icon)
         │   └─ .stepper (4 items)  ← only for wizard
         ├─ Body    (flex:1; overflow-y:auto; padding 22px 24px)
         └─ Footer  (padding 14px 24px; border-top; bg off-white; flex-shrink:0;
                     space-between → [back] left · [cancel ghost + primary] right)
```

Slide animation = `.drawer-enter { translateX(100%) }` → add `.drawer-active { translateX(0); transition: transform 250ms ease-out }` on next frame. Close = remove `.drawer-active`, add `.drawer-enter`, then clear `#overlay-root` after 200ms.

### Required shell hooks (place once, before `</body>`)
```html
<div id="overlay-root"></div>
<div id="toast-root" style="position: fixed; top: 16px; right: 16px; z-index: 100; display: flex; flex-direction: column; gap: 8px;"></div>
```

---

## 🎨 Required CSS — copy verbatim from `references/drawer-standard/drawer.css.html`

The drawer depends on these tokens/classes (all present in the reference CSS). **Include them all** — missing any one breaks the 100% match:

`:root` tokens → `--c-navy #111111`, `--c-navy-d #06122A`, `--c-primary #FF3B30`, `--c-primary-h #0a4ed1`, `--c-teal #FF9A1F`, `--c-slate #73757B`, `--c-off-white #FAF8F5`, `--c-border #E9E5E0`, `--c-border-soft #EEF2F7`, `--c-text #111111`, `--c-text-mute #73757B`, `--c-text-soft #9A9CA2`, `--c-warning #F59E0B`, `--c-danger #EF4444`, **`--c-purple #7C3AED`**, `--c-primary-08/12/18`, `--c-teal-08`, `--c-warning-08`, `--c-danger-08`, radii `--r-sm 6px / --r 10px / --r-lg 14px`, shadows `--sh-sm/md/lg/xl`.

Classes the drawer uses: `.top-icon-btn` · `.btn` (+ `.btn-primary/.btn-secondary/.btn-ghost/.btn-success/.btn-danger/.btn-link`, sizes `.sm/.lg`) · `.pill` (+ status mods) · `.card` (`.card-head/.card-title/.card-body`) · `.input/.select` (+ `label.required`) · `.tabs/.tab` · `.tbl` (+ `.tbl-mono/.tbl-num/.tbl-name/.tbl-meta`) · `.progress-bar` · **`.stepper/.stepper-item/.stepper-circle/.stepper-label`** · `.overlay-wrap/.backdrop/.drawer-panel(.standard)/.modal-overlay/.hidden/.drawer-enter/.drawer-active` · `.animate-slide-in` · `.line-expand-panel/.line-collapse-panel` · `.upload-zone(.has-files)` · **`.form-grp/.form-field`** · **`.toggle/.toggle-slider`** · `.section-row/.section-label` · `mark` · `.num`.

> ⚠️ Number-spinner reset + scrollbar styling are also in the reference CSS — keep them.

---

## 📋 Header — EXACT markup (wizard)

```html
<!-- Drawer Header -->
<div style="padding: 18px 24px 16px; border-bottom: 1px solid var(--c-border-soft); flex-shrink: 0;">
  <div style="display: flex; align-items: flex-start; justify-content: space-between; gap: 16px;">
    <div>
      <div style="display: flex; align-items: center; gap: 6px; font-size: 11px; text-transform: uppercase; letter-spacing: 0.06em; color: var(--c-text-mute); margin-bottom: 4px;">
        <i data-lucide="file-plus" class="w-3.5 h-3.5"></i> สร้างเอกสารใหม่
      </div>
      <h2 style="font-size: 20px; font-weight: 700; color: var(--c-navy);">สร้างคำร้องขอซื้อใหม่</h2>
    </div>
    <button onclick="closeCreateDrawer()" class="top-icon-btn" style="background: transparent; border: none; width: 32px; height: 32px;">
      <i data-lucide="x" class="w-5 h-5"></i>
    </button>
  </div>

  <div class="stepper" style="margin-top: 18px;">
    ${renderStepperItem(1, 'ข้อมูลคำร้องขอซื้อ')}
    ${renderStepperItem(2, 'รายการสินค้า')}
    ${renderStepperItem(3, 'เอกสารแนบ')}
    ${renderStepperItem(4, 'ตรวจสอบและยืนยัน')}
  </div>
</div>
```

`renderStepperItem(n,label)` → `.stepper-item.active` (current) / `.done` (past) / none (future); circle shows the number; label below. (Verbatim in reference JS.)

---

## 📋 Footer — EXACT markup + Button Contract

```html
<div style="padding: 14px 24px; border-top: 1px solid var(--c-border-soft); background: var(--c-off-white); flex-shrink: 0; display: flex; align-items: center; justify-content: space-between;">
  <div>
    ${step > 1 ? `
      <button onclick="wizardBack()" class="btn btn-secondary">
        <i data-lucide="chevron-left" class="w-4 h-4"></i><span>ย้อนกลับ</span>
      </button>` : ''}
  </div>
  <div style="display: flex; align-items: center; gap: 8px;">
    <button onclick="closeCreateDrawer()" class="btn btn-ghost">ยกเลิก</button>
    ${step < LAST ? `
      <button onclick="wizardNext()" class="btn btn-primary"><span>ถัดไป</span><i data-lucide="chevron-right" class="w-4 h-4"></i></button>` : `
      <button onclick="saveDraft()" class="btn btn-secondary"><i data-lucide="save" class="w-4 h-4"></i><span>บันทึกแบบร่าง</span></button>
      <button onclick="submitForApproval()" class="btn btn-primary"><i data-lucide="send" class="w-4 h-4"></i><span>บันทึกและส่งอนุมัติ</span></button>`}
  </div>
</div>
```

**Contract:** back (secondary) left · cancel (ghost) + next/save (primary) right. `บันทึกแบบร่าง` only when the entity has a real draft state.

---

## 📋 Step bodies — reproduce from reference

| Step | Function | Key pieces (all verbatim in `create-edit-drawer.js.txt`) |
|---|---|---|
| 1 General | `renderStep1()` | Section eyebrows (icon + 13px/600 navy title); `.form-grp` 2-col grid; `label.required`; **searchable combobox** (`brCombobox`/`ucpCombobox`: search icon left, chevron/clear right, absolute suggest list, `<mark>` highlight, keyboard nav); selected-summary card with `linear-gradient(135deg, rgba(255,59,48,.04), white)`; textareas via `.input` with `height:auto`. |
| 2 Lines | `renderStep2()` + `renderLineRow()` + `renderLineSummary()` | Compact 9-col `.tbl` (#, item, qty, unit, unit_price, discount%, tax-badge, amount, actions); inline item combobox popover (`item-suggest-popover`); **expandable advanced row** (`.line-expand-panel`, 3-mode VAT radio cards none/add/included, VAT% chips 0/7/10 + custom, computed VAT, note); WHT card with `.toggle` + 1/2/3/5% chips + custom; End-bill discount card with `.toggle` + amount/percent segmented + value input; live `#line-summary-wrap` summary card with `BY_LINE` pill. |
| 3 Attach | `renderStep3()` + `mockUpload()` | `.upload-zone` (empty vs `.has-files`), file rows with file icon chip + size + remove. |
| 4 Review | `renderStep4()` | General-info card (`<dl>` 2-col), lines card with per-line rows + totals table (ราคาก่อน VAT / VAT / หลัง VAT / WHT / ส่วนลดท้ายบิล / ยอดสุทธิ), attachments card. |

VAT math (`calcLineVat`, `migrateLine`) and number formatting (`formatMoney`, `formatThaiDate`) are **verbatim** — copy as-is.

---

## ✏️ EDIT mode — same drawer, pre-filled

Edit reuses the **exact same wizard**. Only differences:
1. Eyebrow icon `pencil` + text `แก้ไขเอกสาร`; `<h2>` = `แก้ไข[เลขที่]`.
2. `openEditDrawer(id)` clones the record into `createWizard.data` (instead of blanks) and may jump to step 1.
3. Footer right-side primary = `<i data-lucide="save">` + `บันทึกการแก้ไข`; keep `ยกเลิก` ghost. Drop `บันทึกแบบร่าง` unless still a draft.
4. Reuse every `renderStep*`, `renderLineRow`, combobox, toggle, and summary unchanged.

```js
function openEditDrawer(id){
  const r = state.records.find(x => x.id === id); if(!r) return;
  createWizard.step = 1;
  createWizard.data = JSON.parse(JSON.stringify(r));        // pre-fill
  if(!createWizard.data.lines || !createWizard.data.lines.length)
    createWizard.data.lines = [createBlankLine()];
  // …open overlay exactly like openCreateDrawer(), id="create-drawer", isEdit flag for header/footer text
}
```

---

## 🔧 Open / Close — EXACT

```js
function openCreateDrawer() {
  createWizard.step = 1; createWizard.expandedLineId = null;
  createWizard.data = { /* blank defaults — see reference */ lines:[createBlankLine()] };
  const overlay = document.getElementById('overlay-root');
  overlay.innerHTML = `
    <div class="overlay-wrap">
      <div class="backdrop" onclick="closeCreateDrawer()"></div>
      <div id="create-drawer" class="drawer-panel drawer-enter">
        <div id="create-drawer-content" style="display: flex; flex-direction: column; height: 100%;"></div>
      </div>
    </div>`;
  const drawer = document.getElementById('create-drawer');
  requestAnimationFrame(() => drawer.classList.add('drawer-active'));
  renderCreateDrawer();
}
function closeCreateDrawer() {
  const drawer = document.getElementById('create-drawer');
  if (drawer) { drawer.classList.remove('drawer-active'); drawer.classList.add('drawer-enter'); }
  setTimeout(() => { document.getElementById('overlay-root').innerHTML = '';
    if (getRoute().name === 'create') navigate('list'); }, 200);
}
```

`renderCreateDrawer()` rebuilds `#create-drawer-content` (header + stepper + body-by-step + footer), then calls `renderIcons()` and re-opens any open combobox lists. **Copy verbatim** from `create-edit-drawer.js.txt`.

---

## 🛡️ Iron Rules to Enforce (drawer scope)

- Shell = `overlay-wrap → backdrop + drawer-panel` (NOT `.drawer/.drawer-backdrop`).
- Panel width = 920px default (`.drawer-panel`), 680px via `.standard`.
- Slide = translateX 250ms ease-out via `.drawer-enter/.drawer-active`; close after 200ms.
- 3 close methods: backdrop click · X `.top-icon-btn` · (optional) Esc.
- Footer contract: back(secondary) left · cancel(ghost)+primary right; one primary only.
- **Master/registry lookup field (ลูกค้า/สินค้า/ผู้ขาย/บัญชี/เลขอ้างอิง ฯลฯ) = search-select (Iron Rule #34)** — ใช้ `searchSelectHTML()`+`initSearchSelect()` (helper กลางใน skeleton) หรือ combobox แบบ `brCombobox` verbatim; **ห้าม** `<select>` ยาว. enum สั้น (สถานะ/ประเภท ≤8) ใช้ `<select>` ได้.
- **Buttons (Iron Rule #36):** ปุ่ม footer สูงเท่ากัน · label ไม่ตัดบรรทัด · icon มี `flex-shrink:0` (อยู่ใน `.btn` แล้ว); ปุ่มคู่ที่ควรสมมาตรใช้ `.btn-eq`.
- All `<i data-lucide>` carry `w-{n} h-{n}`; call `renderIcons()` after every drawer render.
- VAT modes mutually exclusive (none/add/included); summary recomputes live.
- Use `var(--c-*)` tokens everywhere — never hardcode hex inside the drawer (except the PDF paper preview in Pattern C/G which intentionally uses print-black tokens).

---

## ⚠️ Common Mistakes

1. ❌ Falling back to old `.drawer`/`.field-row` markup — must use the v2 shell above.
2. ❌ Forgetting `#overlay-root` / `#toast-root` hooks → drawer never mounts.
3. ❌ Dropping `--c-purple` or `*-08/12` token aliases → tax badges & gradients break.
4. ❌ Re-styling the stepper / toggle / combobox instead of copying verbatim.
5. ❌ Two primary buttons in footer, or wrong order.
6. ❌ Not calling `renderIcons()` after re-render → blank icons.
7. ❌ Hardcoding hex inside drawer body instead of CSS tokens.

---

## 🎯 Pre-deploy Audit

- [ ] Shell = overlay-wrap → backdrop + drawer-panel(.standard?) ✓
- [ ] Drawer slides translateX 250ms; closes after 200ms ✓
- [ ] Header eyebrow + 20px navy title + `.top-icon-btn` close ✓
- [ ] `.stepper` 4 items with active/done states (wizard) ✓
- [ ] `.form-grp` 2-col grid + `label.required` ✓
- [ ] Combobox: search-left, chevron/clear-right, `<mark>` highlight, keyboard nav ✓
- [ ] Line table: 3-mode VAT, WHT toggle, end-bill toggle, live summary ✓
- [ ] Footer contract correct; one primary ✓
- [ ] Edit mode pre-fills + `บันทึกการแก้ไข` ✓
- [ ] All tokens from `drawer.css.html` included ✓
