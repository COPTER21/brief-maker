# Pattern E — Compact Table with Expandable Row

> **Use for:** Tables with 10+ attributes per record where some attributes are detail-level.
> **Pattern:** Click row → expand below row to show full detail (no drawer/modal).
> **Examples:** Pricing tiers, feature matrix, complex inventory items.
> **Source:** v25 lines 1314-1673 (refactored).

---

## 🎯 When to Use

✅ Table where 10+ attributes per record (too wide for ≤ 8 columns)
✅ Detail info is **secondary** — not always needed
✅ Multi-record comparison + occasional drill-in
✅ Want to keep user "in context" (no drawer / modal switch)

❌ Simple records (< 8 attributes — use Pattern A)
❌ Heavy detail with multiple tabs (use Pattern C drawer)
❌ Edit-heavy workflow (use Pattern B drawer)

---

## 🏗️ Structure

```
.card
  └─ .table-scroll
      └─ .table
          ├─ thead — column headers (compact, ≤ 6 visible cols)
          └─ tbody
              ├─ tr (regular row, clickable)
              ├─ tr.line-expanded (expanded detail row, one-shot animation)
              ├─ tr (regular)
              ├─ ... (only ONE expanded at a time)
```

---

## 📋 HTML Skeleton

```html
<div class="card">
  <div class="filter-bar">
    <div class="input-search">
      <i data-lucide="search" class="lead-icon"></i>
      <input class="input" type="text" placeholder="ค้นหา...">
    </div>
  </div>

  <div class="table-scroll">
    <table class="table">
      <thead>
        <tr>
          <th style="width: 32px;"></th>  <!-- expand toggle column -->
          <th>ชื่อ</th>
          <th>หมวด</th>
          <th>ราคา/เดือน</th>
          <th>สถานะ</th>
          <th style="text-align: right;">แก้ไขล่าสุด</th>
        </tr>
      </thead>
      <tbody>
        ${records.map(r => `
          <tr onclick="toggleExpand('${r.id}')" 
              style="cursor: pointer;">
            <td style="text-align: center; color: var(--c-mute-2);">
              <i data-lucide="${state.expandedId === r.id ? 'chevron-down' : 'chevron-right'}" 
                 class="w-3.5 h-3.5"></i>
            </td>
            <td>
              <div style="font-weight: 600;">${r.name}</div>
              <div style="font-size: 12px; color: var(--c-mute-2);">${r.code}</div>
            </td>
            <td>${r.category}</td>
            <td style="font-weight: 600;">฿${r.price.toLocaleString()}</td>
            <td>
              <span class="pill pill-${r.status}">
                <span class="dot is-${r.status}"></span>
                ${statusLabel(r.status)}
              </span>
            </td>
            <td style="text-align: right; font-size: 12.5px; color: var(--c-mute);">
              ${formatDate(r.updatedAt)}
            </td>
          </tr>
          
          ${state.expandedId === r.id ? `
            <tr class="line-expanded" data-id="${r.id}">
              <td colspan="6" style="padding: 0; background: var(--c-bg-off);">
                <div style="padding: 18px 22px; border-top: 1px solid var(--c-line-2);">
                  ${renderExpandedDetail(r)}
                </div>
              </td>
            </tr>
          ` : ''}
        `).join('')}
      </tbody>
    </table>
  </div>

  <div class="table-footer">
    <!-- pagination + count (per Pattern A) -->
  </div>
</div>
```

---

## 🎨 Expanded Detail Content

```javascript
function renderExpandedDetail(r) {
  return `
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 24px;">

      <!-- Column 1: Extended info -->
      <div>
        <h4 style="font-size: 11px; font-weight: 700; color: var(--c-mute); 
                   text-transform: uppercase; letter-spacing: 0.08em; margin: 0 0 10px;">
          รายละเอียดเพิ่มเติม
        </h4>
        <div class="drawer-fields">
          <div class="lbl">SKU</div>
          <div class="val">${r.sku}</div>
          <div class="lbl">ผู้สร้าง</div>
          <div class="val">${r.createdBy}</div>
          <div class="lbl">หมายเหตุ</div>
          <div class="val">${r.notes || '—'}</div>
        </div>
      </div>

      <!-- Column 2: Features list -->
      <div>
        <h4 style="font-size: 11px; font-weight: 700; color: var(--c-mute); 
                   text-transform: uppercase; letter-spacing: 0.08em; margin: 0 0 10px;">
          Features
        </h4>
        <ul style="list-style: none; padding: 0; margin: 0; font-size: 13px;">
          ${(r.features || []).map(f => `
            <li style="padding: 4px 0; display: flex; gap: 8px; align-items: center;">
              <i data-lucide="check" class="w-3.5 h-3.5" style="color: var(--c-success);"></i>
              <span>${f}</span>
            </li>
          `).join('')}
        </ul>
      </div>

      <!-- Column 3: Actions -->
      <div>
        <h4 style="font-size: 11px; font-weight: 700; color: var(--c-mute); 
                   text-transform: uppercase; letter-spacing: 0.08em; margin: 0 0 10px;">
          Actions
        </h4>
        <div style="display: flex; flex-direction: column; gap: 6px;">
          <!-- Rule #41 — ไม่มีปุ่ม eye 'ดูรายละเอียดเต็ม': กดแถว = expand รายละเอียดในตัวแล้ว (no drawer per pattern premise) -->
          <button class="btn btn-secondary btn-sm" style="justify-content: flex-start;" 
                  onclick="event.stopPropagation(); openDrawer('edit', '${r.id}')">
            <i data-lucide="pencil" class="w-3.5 h-3.5"></i>
            <span>แก้ไข</span>
          </button>
          <button class="btn btn-secondary btn-sm" style="justify-content: flex-start; color: var(--c-danger);" 
                  onclick="event.stopPropagation(); openModal('delete', {id: '${r.id}'})">
            <i data-lucide="trash-2" class="w-3.5 h-3.5"></i>
            <span>ลบ</span>
          </button>
        </div>
      </div>

    </div>
  `;
}
```

---

## 🔧 Required JS Helpers

```javascript
// State
// state.expandedId = null | 'r-id'

function toggleExpand(id) {
  // Mutually exclusive: only one row expanded at a time
  state.expandedId = state.expandedId === id ? null : id;
  render();
}

// CSS animation marker (used by .line-expanded class)
// The slide-down 220ms animation is one-shot — handled in CSS:
// .line-expanded { animation: lineExpand 220ms cubic-bezier(0.4, 0, 0.2, 1); }
```

---

## 🎨 Animation (CSS in file-skeleton)

```css
/* Already in file-skeleton.template.html */
.line-expanded {
  animation: lineExpand 220ms cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
}
@keyframes lineExpand {
  from { max-height: 0; opacity: 0; transform: translateY(-8px); }
  to { max-height: 600px; opacity: 1; transform: translateY(0); }
}
```

**Animation behavior:**
- **One-shot:** Plays only when row first becomes expanded
- **No reverse animation:** Collapsing just removes the row (instant) — keeps DOM simple
- **Max-height 600px:** Cap to prevent very long detail areas from animating awkwardly

---

## 🛡️ Iron Rules to Enforce

- **#16** Visible columns ≤ 6 (since detail is in expand) ✓
- **#21** All `<i data-lucide>` have `w-{N} h-{N}` ✓
- **#23** No color emoji ✓
- **Mutually exclusive expand:** Only ONE row expanded at a time ✓

---

## ⚠️ Common Mistakes

1. **❌** Multiple rows expanded simultaneously — use `state.expandedId` (single value, not Set)
2. **❌** Forgetting `event.stopPropagation()` on action buttons inside expanded area
3. **❌** Animation playing on every render — use `_justOpenedLineId` pattern if needed:
   ```javascript
   let _justOpenedLineId = null;
   function toggleExpand(id) {
     _justOpenedLineId = state.expandedId === id ? null : id;
     state.expandedId = _justOpenedLineId;
     render();
   }
   // In template: only add class if _justOpenedLineId === r.id
   ```
4. **❌** Putting too many columns in header (defeats the purpose — keep visible cols compact)
5. **❌** Heavy editing in expanded area (move to drawer instead)
6. **❌** No visual cue for expanded state (chevron-right → chevron-down)
7. **❌** Click on icon-only row toggle (whole row should be clickable for better UX)
