# Pattern A — List View

> **Use for:** List/index pages with search + filter + table + row actions.
> **Examples:** Prospects list, Customers list, Orders list, Users list.
> **Reference:** `core-marketing-prospect.html`

---

## 🎯 When to Use

✅ Display many records in tabular form
✅ Filter by status / category
✅ Search by name/keyword
✅ Bulk actions (multi-select)
✅ Per-row actions (edit, delete) — **view = กดทั้งแถว (Rule #41), ไม่มีไอคอนดวงตา**
✅ Pagination

❌ Single-record display (use Pattern C — View Drawer)
❌ Multi-step form (use Pattern B — Create/Edit Drawer)
❌ Confirmation (use Pattern D — Modal)

---

## 🏗️ Structure

```
.ph (Page Header) — title + count + subtitle + actions
↓
.stats (optional KPI row)
↓
.card
  ├─ .filter-bar (search + selects + reset)
  ├─ .bulk-bar (sticky, when rows selected — optional)
  ├─ .table-scroll
  │   └─ .table (≤ 8 columns)
  │       ├─ thead — column headers (sortable)
  │       └─ tbody — rows with cells + row-actions
  └─ .table-footer (pagination + count)
```

---

## 📋 Full HTML Skeleton

```html
<div class="card">
  <!-- 1. FILTER BAR -->
  <div class="filter-bar">
    <div class="input-search">
      <i data-lucide="search" class="lead-icon"></i>
      <input class="input" type="text" placeholder="ค้นหา..." 
             value="${state.filters.search}" 
             oninput="state.filters.search = this.value; state.pagination.page = 1; render();">
    </div>
    <select class="select" style="max-width: 180px;" 
            onchange="state.filters.status = this.value; state.pagination.page = 1; render();">
      <option value="all">ทุกสถานะ</option>
      <option value="active">Active</option>
      <option value="converted">Converted</option>
      <option value="suspended">Suspended</option>
      <option value="archived">Archived</option>
    </select>
    <button class="btn btn-ghost btn-sm" onclick="resetFilters()">
      <i data-lucide="rotate-ccw" class="w-3.5 h-3.5"></i>
      <span>รีเซ็ต</span>
    </button>
  </div>

  <!-- 2. BULK BAR (optional — show when state.selectedIds.size > 0) -->
  ${state.selectedIds.size > 0 ? `
    <div class="bulk-bar">
      <i data-lucide="check-square" class="w-4 h-4"></i>
      <span>เลือก ${state.selectedIds.size} รายการ</span>
      <div style="margin-left: auto; display: flex; gap: 8px;">
        <button class="btn btn-secondary"><i data-lucide="download" class="w-3.5 h-3.5"></i>Export</button>
        <button class="btn btn-secondary"><i data-lucide="archive" class="w-3.5 h-3.5"></i>Archive</button>
      </div>
    </div>
  ` : ''}

  <!-- 3. TABLE -->
  <div class="table-scroll is-sticky">
    <table class="table">
      <thead>
        <tr>
          <th class="col-check">
            <div class="cb ${allSelected ? 'is-checked' : ''} ${someSelected ? 'is-partial' : ''}" 
                 onclick="toggleSelectAll()"></div>
          </th>
          <th class="is-sortable ${state.sort.col === 'name' ? 'is-sorted' : ''}" 
              onclick="sortBy('name')">
            ชื่อ <span class="sort-arrow">↕</span>
          </th>
          <th>บริษัท</th>      <!-- Rule #40 — แยกคอลัมน์ ไม่ซ้อนใต้ชื่อ -->
          <th>อีเมล</th>
          <th>สถานะ</th>
          <th>แหล่งที่มา</th>
          <th>สร้างเมื่อ</th>
          <th style="width: 88px; text-align: right;"></th>
        </tr>
      </thead>
      <tbody>
        ${filteredRecords.map(r => `
          <tr class="is-clickable ${state.selectedIds.has(r.id) ? 'is-selected' : ''}" 
              onclick="openDrawer('view', '${r.id}')">
            <td onclick="event.stopPropagation()">
              <div class="cb ${state.selectedIds.has(r.id) ? 'is-checked' : ''}" 
                   onclick="toggleSelect('${r.id}')"></div>
            </td>
            <td>
              <div class="user-cell">
                <div class="uc-avatar">${initials(r.name)}</div>
                <div class="uc-name">${r.name}</div>   <!-- Rule #40 — บรรทัดเดียว ไม่ซ้อน sub-line -->
              </div>
            </td>
            <td><span class="cell-truncate" title="${r.company || ''}">${r.company || '—'}</span></td>
            <td><span class="cell-truncate" title="${r.email}">${r.email}</span></td>
            <td>
              <span class="pill pill-${r.status}">
                <span class="dot is-${r.status}"></span>
                ${statusLabel(r.status)}
              </span>
            </td>
            <td>${r.source}</td>
            <td>${fmtDate(r.createdAt)}</td>
            <td onclick="event.stopPropagation()" style="text-align: right;">
              <!-- Rule #41 — ไม่มีไอคอนดวงตา (กดแถว = เปิด view แล้ว). เหลือเฉพาะ edit + delete -->
              <div class="row-actions">
                <button class="ra-btn" onclick="openDrawer('edit', '${r.id}')" title="แก้ไข">
                  <i data-lucide="pencil" class="w-4 h-4"></i>
                </button>
                <button class="ra-btn is-danger" onclick="openModal('delete', '${r.id}')" title="ลบ">
                  <i data-lucide="trash-2" class="w-4 h-4"></i>
                </button>
              </div>
            </td>
          </tr>
        `).join('')}
      </tbody>
    </table>
    ${filteredRecords.length === 0 ? emptyStateHTML({
      icon: 'search-x', title: 'ไม่พบรายการที่ตรงกับเงื่อนไข',
      desc: 'ลองปรับคำค้นหรือตัวกรอง หรือล้างตัวกรองเพื่อดูทั้งหมด',
      actionLabel: 'ล้างตัวกรอง', actionIcon: 'rotate-ccw', onAction: 'resetFilters()'
    }) : ''}
  </div>

  <!-- 4. TABLE FOOTER -->
  <div class="table-footer">
    <div>
      <select class="select" style="height: 30px; font-size: 12.5px; padding: 0 28px 0 10px;"
              onchange="state.pagination.pageSize = +this.value; state.pagination.page = 1; render();">
        <option value="10">10 / หน้า</option>
        <option value="20" selected>20 / หน้า</option>
        <option value="50">50 / หน้า</option>
        <option value="100">100 / หน้า</option>
      </select>
    </div>
    <div style="display: flex; align-items: center; gap: 16px;">
      <span>${start} – ${end} จาก ${total} รายการ</span>
      <div class="pagination">
        <button class="pg-btn ${page === 1 ? 'is-disabled' : ''}" 
                onclick="goToPage(${page - 1})">
          <i data-lucide="chevron-left" class="w-3 h-3"></i>
        </button>
        ${pageNumbers.map(n => `
          <button class="pg-btn ${n === page ? 'is-active' : ''}" 
                  onclick="goToPage(${n})">${n}</button>
        `).join('')}
        <button class="pg-btn ${page === totalPages ? 'is-disabled' : ''}" 
                onclick="goToPage(${page + 1})">
          <i data-lucide="chevron-right" class="w-3 h-3"></i>
        </button>
      </div>
    </div>
  </div>
</div>
```

---

## 🎨 Column Conventions

| Column Type | Width | Alignment | Notes |
|---|---|---|---|
| Checkbox | 40px | center | First column, no padding-right |
| Primary entity (name + avatar) | flex | left | `.user-cell` — **avatar + ชื่อ บรรทัดเดียว** (Rule #40: ห้ามซ้อน sub-line) |
| Secondary data (company, email, ID) | flex | left | **คอลัมน์แยกของตัวเอง** + `.cell-truncate` + `title` (Rule #40) |
| Status pill | auto | left | `.pill` + `.dot` |
| Category/Source | auto | left | Plain text or tag |
| Date | 110px | left | `fmtDate()` helper (Rule #43) |
| Number/amount | 100px | **right** | `td class="col-num"` + `.num` (tabular, Rule #43) |
| Row actions | 88px | **right** | `.row-actions` — **edit + delete เท่านั้น (ไม่มี eye, Rule #41)** |

**Total columns: ≤ 8** (Iron Rule #16) — ถ้าข้อมูลที่จะแยกคอลัมน์ทำให้เกิน 8 → **ตัดตัวที่สำคัญน้อยลง drawer แทนการซ้อนบรรทัด** (Rule #40)

---

## 🛡️ Iron Rules to Enforce

- **#16** Table ≤ 8 columns ✓
- **#40** **1 ข้อมูล = 1 คอลัมน์ — ห้ามซ้อน sub-line ใต้ค่าหลัก** (ตัดลง drawer ถ้าจะเกิน 8) ✓
- **#41** **กดแถว = เปิด view; ไม่มีไอคอนดวงตา; checkbox/action ต้อง `stopPropagation()`** ✓
- **#42** Sticky header (`.table-scroll.is-sticky`) + `.cell-truncate` (Thai-safe) สำหรับ list ยาว ✓
- **#43** ตัวเลข `.num` tabular ชิดขวา · วันที่ `fmtDate()` ✓
- **#9** Filter bar in card · **#10** Table footer · **#21** icon `w/h` · **#25** `renderIcons()` ✓

---

## ⚠️ Common Mistakes

1. **❌** ซ้อนข้อมูล 2 บรรทัดในเซลล์เดียว (name + company ใต้กัน) → **แยกคอลัมน์** (Rule #40)
2. **❌** ใส่ไอคอนดวงตา (eye) เพื่อเปิด view → **กดแถวเปิดเอง** (Rule #41)
3. **❌** Table with 10+ columns (use Pattern E expandable instead)
4. **❌** Action column with 4+ icon buttons (max 3 → ใช้ `more-vertical` menu)
5. **❌** Filter bar outside card (must be inside, with border-bottom)
6. **❌** No pagination / no empty state on long lists
7. **❌** Hover style on whole row but click does nothing — wire row click to view + `.is-clickable`
8. **❌** Clickable cells (checkbox, action buttons) ไม่ `event.stopPropagation()` → trigger row click

---

## 🔧 Required JS Helpers

```javascript
// Filter + Search + Sort + Paginate (composable)
function getFilteredRecords() {
  let arr = state.records;
  // Filter by status
  if (state.filters.status !== 'all') {
    arr = arr.filter(r => r.status === state.filters.status);
  }
  // Search
  if (state.filters.search) {
    const q = state.filters.search.toLowerCase();
    arr = arr.filter(r => 
      r.name?.toLowerCase().includes(q) || 
      r.email?.toLowerCase().includes(q) ||
      r.company?.toLowerCase().includes(q)
    );
  }
  // Sort
  if (state.sort.col) {
    arr = [...arr].sort((a, b) => {
      const va = a[state.sort.col] ?? '';
      const vb = b[state.sort.col] ?? '';
      const cmp = String(va).localeCompare(String(vb));
      return state.sort.dir === 'asc' ? cmp : -cmp;
    });
  }
  return arr;
}

function getPaginated() {
  const all = getFilteredRecords();
  const { page, pageSize } = state.pagination;
  const start = (page - 1) * pageSize;
  return {
    records: all.slice(start, start + pageSize),
    total: all.length,
    page,
    totalPages: Math.max(1, Math.ceil(all.length / pageSize)),
    start: all.length === 0 ? 0 : start + 1,
    end: Math.min(start + pageSize, all.length),
  };
}

// Sort handler
function sortBy(col) {
  if (state.sort.col === col) {
    state.sort.dir = state.sort.dir === 'asc' ? 'desc' : 'asc';
  } else {
    state.sort.col = col;
    state.sort.dir = 'asc';
  }
  render();
}

// Selection
function toggleSelect(id) {
  if (state.selectedIds.has(id)) state.selectedIds.delete(id);
  else state.selectedIds.add(id);
  render();
}
function toggleSelectAll() {
  const visible = getPaginated().records;
  const allSelected = visible.every(r => state.selectedIds.has(r.id));
  if (allSelected) visible.forEach(r => state.selectedIds.delete(r.id));
  else visible.forEach(r => state.selectedIds.add(r.id));
  render();
}

// Pagination
function goToPage(n) {
  const { totalPages } = getPaginated();
  if (n < 1 || n > totalPages) return;
  state.pagination.page = n;
  render();
}

// Reset filters
function resetFilters() {
  state.filters = { search: '', status: 'all' };
  state.pagination.page = 1;
  state.selectedIds.clear();
  render();
}

// Helper: get initials from name
function initials(name) {
  return (name || '?').split(' ').map(s => s[0]).join('').slice(0, 2).toUpperCase();
}

// Helper: format date (Thai)
function formatDate(iso) {
  if (!iso) return '—';
  return new Date(iso).toLocaleDateString('th-TH', { year: 'numeric', month: 'short', day: 'numeric' });
}
```

---

## 🎯 Variant: Card Grid (for non-tabular data)

If records don't fit table well (e.g., visual data like pillars, products with images):

```html
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px; padding: 18px;">
  ${records.map(r => `
    <div class="bm-card" onclick="openDrawer('view', '${r.id}')">
      <div class="bm-icon"><i data-lucide="${r.icon}" class="w-4 h-4"></i></div>
      <div>
        <div style="font-weight: 600;">${r.name}</div>
        <div style="font-size: 12px; color: var(--c-mute);">${r.description}</div>
      </div>
    </div>
  `).join('')}
</div>
```

Still wrap in `.card` + include filter bar + footer.

---

## ⭐ v9 — Column Atomicity ย้ำ (Rule #103)
1 ข้อมูล = 1 คอลัมน์: สถานะเอกสาร / จัดส่ง / การจ่าย / ลายเซ็น / ยอด / วันที่ / ผู้รับผิดชอบ แยกคอลัมน์ ห้าม pill ≥2 ใน cell เดียว ·
บรรทัดรองใน cell = meta ของข้อมูลเดียวกันเท่านั้น (code ใต้ชื่อ) · เกิน 8 คอลัมน์ → ย้ายไป drawer/⋮ ไม่ยุบรวม ·
filter/sort/page → `renderTableOnly()` เฉพาะ `#table-body` (หน้าไม่กระโดด)
