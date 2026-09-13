# Pattern C — View Drawer with Tabs (CUBE Admin CI v2)

> **⭐ AUTHORITATIVE STANDARD (locked to `pr.html`).** The view drawer MUST render
> **100% identical** to the reference. This supersedes any older `.drawer`/`.drawer-tabs` markup.
>
> **Verbatim source of truth:**
> - `references/drawer-standard/_SOURCE_pr-reference.html` — full working reference
> - `references/drawer-standard/drawer.css.html` — required CSS (same tokens/classes as Pattern B)
> - `references/drawer-standard/view-drawer.js.txt` — full view drawer JS (3 tabs)
> - `references/drawer-standard/shared-helpers.js.txt` — renderPill / formatMoney / formatThaiDate / showToast
>
> **Rule:** Reproduce structure, class names, inline styles, tabs, and action contract **exactly**.
> Adapt only the fields/labels/entity for the target feature.

---

## 🎯 When to Use

✅ Read view of one document/record (PR, PO, SO, Invoice, Quotation, Receipt, etc.)
✅ Multiple tabs: รายละเอียด (Detail) · PDF Preview · ลายเซ็น (Signatures)
✅ Status-conditional header actions (submit / approve / reject / edit / create-next)
✅ Documents with budget control, line items, attachments, signature chain

❌ Create/edit → Pattern B
❌ Confirm/delete → Pattern D (`confirmCancel()` modal in reference)

---

## 🧱 Drawer Shell — EXACT (same v2 shell as Pattern B)

```
#overlay-root
└─ .overlay-wrap
   ├─ .backdrop (click = closeViewDrawer)
   └─ .drawer-panel.drawer-enter         ← wide 920px (this view = PO-style wide)
      └─ #view-drawer-content (flex column, height:100%)
         ├─ Header (padding 18px 24px 12px; border-bottom; flex-shrink:0)
         │   ├─ eyebrow + <h2 mono primary>${doc_no}</h2> + status pill + sub (requester · dept)
         │   ├─ action cluster (status-conditional) + divider + print/download/close .top-icon-btn ×3
         │   └─ .tabs (detail / pdf / signatures)
         ├─ Body (flex:1; overflow-y:auto; padding 20px 24px) → renders active tab
         └─ Footer (padding 12px 24px; border-top; bg off-white) → "แก้ไขล่าสุด …"
```

Open/close/animation = identical to Pattern B (`drawer-enter` → `drawer-active` 250ms; close after 200ms).

> Use the same required shell hooks (`#overlay-root`, `#toast-root`) and the same
> `drawer.css.html` token/class set as Pattern B.

---

## 📋 Header — EXACT markup

```html
<div style="padding: 18px 24px 12px; border-bottom: 1px solid var(--c-border-soft); flex-shrink: 0;">
  <div style="display: flex; align-items: flex-start; justify-content: space-between; gap: 16px;">
    <div>
      <div style="font-size: 11px; text-transform: uppercase; letter-spacing: 0.06em; color: var(--c-text-mute); margin-bottom: 4px;">ใบขอซื้อ (Purchase Requisition)</div>
      <div style="display: flex; align-items: center; gap: 10px;">
        <h2 style="font-size: 20px; font-weight: 700; color: var(--c-primary);" class="tbl-mono">${r.pr_no}</h2>
        ${renderPill(r.status)}
      </div>
      <div style="font-size: 13px; margin-top: 4px; color: var(--c-text-mute);">${r.requester} · ${r.dept}</div>
    </div>
    <div style="display: flex; align-items: center; gap: 6px;">
      <!-- STATUS-CONDITIONAL ACTIONS (see contract below) + divider -->
      <button class="top-icon-btn" title="พิมพ์"><i data-lucide="printer" class="w-4 h-4"></i></button>
      <button class="top-icon-btn" title="ดาวน์โหลด PDF"><i data-lucide="download" class="w-4 h-4"></i></button>
      <button onclick="closeViewDrawer()" class="top-icon-btn"><i data-lucide="x" class="w-4 h-4"></i></button>
    </div>
  </div>

  <div class="tabs" style="margin-top: 14px; margin-bottom: 0;">
    ${tabBtn('detail', 'รายละเอียด', 'file-text')}
    ${tabBtn('pdf', 'PDF Preview', 'file')}
    ${tabBtn('signatures', 'ลายเซ็น', 'pen-tool')}
  </div>
</div>
```

`tabBtn(key,label,icon)` → `.tab` (+`.on` when active) with lucide icon. Verbatim in reference.

### Header action contract (status-conditional, before the divider)
| Status | Actions (left→right) |
|---|---|
| `draft` | `ยกเลิก` (btn-link danger) · `แก้ไข` (btn-secondary, pencil) · `ส่งอนุมัติ` (btn-primary, send) |
| `pending` | `ปฏิเสธ` (btn-link danger) · `ส่งคืนแก้ไข` (btn-secondary) · `อนุมัติ` (btn-success, check) |
| `approved` & ordered<100% | `สร้าง CP` (btn-primary, scale) |
| any | always: divider `1px×22px` → `พิมพ์` · `ดาวน์โหลด PDF` · `ปิด(x)` as `.top-icon-btn` |

---

## 📑 Tab 1 — รายละเอียด (`renderDetailTab`)

Sections as `<section>` blocks (13px/700 navy heading, optional icon):
1. **ข้อมูลคำร้องขอซื้อ** — `grid-template-columns: 1fr 1fr; gap 14px 24px`; each cell = label (11px soft) + value (600). PR no in `.tbl-mono` primary; status via `renderPill`; สายเบิก uses `.progress-bar` + `.progress-bar-fill(.zero/.pending)`.
2. **ข้อมูลผู้ขอและแผนก** — 2-col, icon + value + ID sub-line.
3. **การควบคุมงบประมาณ** (if `br_no`) — `.card` with `linear-gradient(135deg, rgba(255,59,48,.04), white)`, 2-col grid; remaining (primary) + ยอดอายัด (warning).
4. **รายการสินค้า** — `.tbl` with thead + line rows + `<tfoot>` totals (ก่อน VAT / VAT purple / ยอดสุทธิ primary).
5. **เอกสารแนบ** — file cards (icon chip + name + size + download ghost).

All verbatim in `view-drawer.js.txt`.

---

## 📄 Tab 2 — PDF Preview (`renderPdfTab`)

- Toolbar row (off-white, border, radius) → "ตัวอย่าง PDF · A4 · 1/1" + ดาวน์โหลด/พิมพ์/เต็มจอ ghost buttons.
- Gray stage `background:#E5E7EB; padding:20px` → white A4 sheet `max-width:720px; min-height:900px; padding:36px 40px; font-size:11px; color:#111`.
- Sheet = company header (logo gradient + tax id) · doc meta grid · lines table (navy `#111111` header) · awarded summary band (`linear-gradient` + left primary border) · **3-column signature blocks** (border-bottom line, cursive name when signed, role + date) · footer "Generated by CUBE ERP · หน้า 1/1".
- ⚠️ The PDF sheet intentionally uses **print-black/print-gray literal hex** (`#111`, `#6B7280`, `#111111`, `#FF3B30`, `#E5E7EB`, `#F9FAFB`) — keep them; it simulates real paper. (This is the only place literal hex is allowed.)

Verbatim in reference.

---

## ✍️ Tab 3 — ลายเซ็น (`renderSignaturesTab`)

Stack of `.card` rows: status circle (teal check if signed / clock if pending) + role eyebrow + `pill approved|pending` + name + position + signed-at + a `ลงนาม` btn-primary when pending. Verbatim in reference.

---

## 🔧 Open / Close / Render — EXACT

```js
const viewState = { tab: 'detail', recordId: null };

function openViewDrawer(id) {
  viewState.tab = 'detail'; viewState.recordId = id;
  document.getElementById('overlay-root').innerHTML = `
    <div class="overlay-wrap">
      <div class="backdrop" onclick="closeViewDrawer()"></div>
      <div id="view-drawer" class="drawer-panel drawer-enter">
        <div id="view-drawer-content" style="display: flex; flex-direction: column; height: 100%;"></div>
      </div>
    </div>`;
  const drawer = document.getElementById('view-drawer');
  requestAnimationFrame(() => drawer.classList.add('drawer-active'));
  renderViewDrawer();
}
function closeViewDrawer() {
  const drawer = document.getElementById('view-drawer');
  if (drawer) { drawer.classList.remove('drawer-active'); drawer.classList.add('drawer-enter'); }
  setTimeout(() => { document.getElementById('overlay-root').innerHTML = '';
    if (getRoute().name === 'view') navigate('list'); }, 200);
}
function renderViewDrawer() { /* header + actions + tabs + active-tab body + footer → renderIcons() */ }
```

Tab switch = `viewState.tab='…'; renderViewDrawer()`. Status actions via `approveAction(id,kind)`; delete via `confirmCancel(id)` (Pattern D modal). **Copy verbatim** from `view-drawer.js.txt`.

---

## 🛡️ Iron Rules to Enforce (drawer scope)

- Shell = `overlay-wrap → backdrop + drawer-panel` (wide 920px for documents).
- Header: mono primary doc-no + `renderPill` status; status-conditional actions + divider + 3 icon buttons.
- Tabs use `.tabs/.tab(.on)`; switch re-renders whole drawer.
- PDF sheet uses literal print hex (allowed); everywhere else use `var(--c-*)`.
- Every `<i data-lucide>` has `w-{n} h-{n}`; `renderIcons()` after each render.
- Footer = single muted "แก้ไขล่าสุด …" line.

---

## ⚠️ Common Mistakes

1. ❌ Old `.drawer`/`.drawer-tabs` markup — use v2 shell + `.tabs/.tab`.
2. ❌ Missing status-conditional action contract.
3. ❌ Replacing literal PDF hex with tokens (breaks paper look) — or conversely using literal hex outside the PDF sheet.
4. ❌ Forgetting `renderPill`, `.progress-bar`, gradient budget card.
5. ❌ Not calling `renderIcons()` on tab switch → blank icons.

---

## 🎯 Pre-deploy Audit

- [ ] overlay-wrap → backdrop + drawer-panel (920px) ✓
- [ ] Header mono primary doc-no + status pill + sub ✓
- [ ] Status-conditional actions + divider + print/download/close ✓
- [ ] 3 tabs detail/pdf/signatures via `.tabs/.tab` ✓
- [ ] Detail: budget gradient card + line totals tfoot + attachments ✓
- [ ] PDF: A4 sheet with print hex + 3 signature blocks ✓
- [ ] Signatures: signed/pending states ✓
- [ ] Footer muted timestamp ✓
