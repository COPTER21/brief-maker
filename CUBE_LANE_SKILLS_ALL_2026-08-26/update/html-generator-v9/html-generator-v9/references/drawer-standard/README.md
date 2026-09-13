# Drawer Standard v2 — Source of Truth (locked to `pr.html`)

These files define the **exact** create / edit / view drawer that `html-generator-v8` must
reproduce. They were extracted **verbatim** from the approved reference (`pr.html`). Do not
paraphrase — copy and adapt only field set, labels, entity names, and mock data.

| File | What it is | Used by |
|---|---|---|
| `_SOURCE_pr-reference.html` | The complete, working reference page (list + create + edit + view + modal). Open in a browser to see the target 100%. Diff your output against this. | Patterns B, C, G |
| `drawer.css.html` | All CSS the drawers depend on — `:root` tokens (incl. `--c-purple #7C3AED` + `*-08/12/18` aliases) and every component class (`.drawer-panel`, `.overlay-wrap`, `.backdrop`, `.stepper*`, `.toggle*`, `.form-grp`, `.tabs/.tab`, `.btn*`, `.input`, `.card*`, `.tbl*`, `.pill`, `.progress-bar`, `.upload-zone`, `.section-row`, `.line-expand-*`, `.top-icon-btn`, `mark`, `.num`). Paste inside `<style>`. | B, C, G |
| `create-edit-drawer.js.txt` | Full create/edit **wizard** JS — `createWizard`, `openCreateDrawer`/`closeCreateDrawer`, `renderCreateDrawer`, `renderStepperItem`, `renderStep1..4`, comboboxes (BR/UCP/item), `renderLineRow`/`renderLineSummary`, `calcLineVat`/`migrateLine`, WHT + end-bill toggles, attachments, review, `wizardNext/Back`, `saveDraft`/`submitForApproval`/`createNewRecord`. | B |
| `view-drawer.js.txt` | Full view drawer JS — `viewState`, `openViewDrawer`/`closeViewDrawer`, `renderViewDrawer`, `tabBtn`, `renderDetailTab`, `renderPdfTab`, `renderSignaturesTab`, `approveAction`. | C, G |
| `shared-helpers.js.txt` | `confirmCancel` (delete modal), `closeAllOverlays`, `renderPill`, `formatMoney`, `formatThaiDate`, `showToast`. | B, C, G, D |
| `_SOURCE_line-editor-reference.html` | 🆕 v7 — reference เต็มของ **Pattern B2** (line editor: multi-UoM, VAT 3 โหมด, WHT/end-bill, budget hard control, item combobox keyboard nav ครบ). Diff step 2 ของคุณกับไฟล์นี้ | B2 |
| `line-editor.css.html` | 🆕 v7 — CSS ที่ B2 ต้องมี (btn/card/input/tbl/expand-anim/toggle/section-row + `.drawer-panel.wide`) | B2 |
| `line-editor.js.txt` | 🆕 v7 — JS line editor 23 defs (item combobox + UoM cascade + `calcLineVat`/`migrateLine` + expand + totals + WHT/end-bill + hard control hook) | B2 |
| `master-combobox.js.txt` | 🆕 v7 — canonical master combobox (**Iron Rule #94**) — ตัวอย่าง verbatim = combobox "ผู้ขอ" | ทุก pattern ที่มี field อ้าง master |

## Drawer shell (the locked structure)

```
#overlay-root
└─ .overlay-wrap (fixed; inset:0; z-index:50)
   ├─ .backdrop (rgba(0,0,0,.45); click = close)
   └─ .drawer-panel.drawer-enter           ← 920px wide (documents). Add .standard for 680px.
      └─ #{create|view}-drawer-content (flex column; height:100%)
         ├─ Header (flex-shrink:0; border-bottom)
         ├─ Body   (flex:1; overflow-y:auto)
         └─ Footer (flex-shrink:0; border-top; bg off-white)
```

Animation: add `.drawer-active` (translateX(0); 250ms ease-out) on next frame to open;
remove `.drawer-active` + add `.drawer-enter`, then clear `#overlay-root` after 200ms to close.

Required hooks before `</body>`:
```html
<div id="overlay-root"></div>
<div id="toast-root" style="position:fixed; top:16px; right:16px; z-index:100; display:flex; flex-direction:column; gap:8px;"></div>
```

> The only place literal hex (not `var(--c-*)`) is allowed is the **A4 PDF sheet** inside the
> view drawer's PDF tab — it intentionally simulates printed paper.

## v9 — Rule #102 Option Anatomy
คน = `.emp-av` initials → ชื่อ → ตำแหน่ง · แผนก | สินค้า = `package` → code · หมวด → ชื่อ → ฿ราคา/หน่วย + ATP |
องค์กร = `building-2` → ชื่อ → code · กลุ่ม | เอกสาร = `file-text` → เลขที่ → คู่ค้า · วันที่ · ยอด — ดู `comboItems/paintCombo/paintItemPop` ใน `references/document-archetype/`
