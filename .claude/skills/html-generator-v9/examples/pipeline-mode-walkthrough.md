# Pipeline Mode Walkthrough — F-01 Prospect List

> **Purpose:** Concrete example showing how Pipeline Mode parses FRD Pack and generates HTML.
> **Scenario:** Building a Prospect list page from a complete FRD v4 Pack.

---

## 📥 Input: Files Provided to Generator

```
INPUT FILES:
  ├─ Brief_F-01.md
  ├─ BRD_F-01.md
  ├─ RIF_F-01.md
  └─ FRD_F-01_PROSPECT_Pack/
      ├─ 00_INDEX.md
      ├─ 01_UI.md            ⭐ Primary
      ├─ 02_API.md
      ├─ 03_LOGIC.md
      ├─ 04_DB.md
      ├─ 05_RULES.md
      └─ 06_TESTS.md
```

---

## 📄 Sample 01_UI.md (excerpt)

```markdown
# F-01 Prospect — UI Spec

## Screens

### Screen 1: Prospect List (`#/prospects`)
- Pattern: List view
- Components: filter-bar + table + pagination
- Columns: Name (with avatar), Email, Status, Source, CreatedAt, Actions
- Actions: View, Edit, Delete (per row), Add Prospect (page-header)
- Filters: search by name/email, status dropdown (all/active/converted/archived)
- Pagination: 20 per page

### Screen 2: Create Prospect (`#/prospects/new`)
- Pattern: Drawer slide-in (920px v2)
- Steps: 1 (single step)
- Fields:
  - firstName (required)
  - lastName (required)
  - email (required, format-valid)
  - company (optional)
  - phone (optional)
  - source (required, select: web/event/referral/cold-call)
  - notes (optional, textarea)

### Screen 3: View Prospect (`#/prospects/:id`)
- Pattern: Drawer 920px with 3 tabs
- Tabs: Overview / Activity / Notes
- Header actions (status-conditional):
  - status=active: Edit, Convert, Archive
  - status=converted: Link to Customer
  - status=archived: Restore
```

---

## 📄 Sample 05_RULES.md (excerpt)

```markdown
# F-01 Prospect — Business Rules

## Validation Rules

### R1: Email format
- Email must match valid format
- Error: "อีเมลไม่ถูกต้อง"

### R2: Duplicate email
- Cannot create prospect with email already in system
- Error: "อีเมลนี้มีในระบบแล้ว"

### R3: Required fields on Create
- firstName, lastName, email, source must be filled

### R4: Status transitions
- active → converted (manual via Convert action)
- active → archived (manual via Archive action)
- archived → active (manual via Restore action)
- converted → ARCHIVED ONLY (no manual revert)
```

---

## 📄 Sample BRD §14.6 (excerpt)

```markdown
## §14.6 Functions Cut for v1

The following features are CUT from v1 and deferred to v2:
- Bulk Convert (multi-select → convert all)
- Auto-assign by territory
- Email integration (send from prospect detail)
- Lead scoring algorithm
```

---

## 🤖 Generator's Workflow

### Step 1: Activate Pipeline Mode

```
✅ Pipeline Mode activated.
Detected FRD v4 Pack with 7 files in FRD_F-01_PROSPECT_Pack/
```

### Step 2: Read priority files

```
📖 Reading 00_INDEX.md (overview)... 2KB
📖 Reading 01_UI.md (primary UI spec)... 8KB
📖 Reading 05_RULES.md (validations)... 3KB
📖 Reading BRD_F-01.md §14.6 (functions cut)... 1KB (excerpt)
📖 Skim 02_API.md, 04_DB.md (informational)... 6KB
```

### Step 3: Plan generation

```
📋 Plan:

Screens: 3
- Screen 1 (Prospect List) → Pattern A
- Screen 2 (Create Prospect) → Pattern B (drawer slide-in (920px v2))
- Screen 3 (View Prospect) → Pattern C (drawer with 3 tabs)

Conflicts: 0
Iron Rule Overrides: 0
  ✓ FRD already specifies drawer for Create (matches Iron Rule #14)

Functions Cut (per BRD §14.6) — NOT IMPLEMENTED:
- ❌ Bulk Convert (no multi-select → Convert button)
- ❌ Auto-assign (no automatic owner logic)
- ❌ Email integration (no "Send Email" button)
- ❌ Lead scoring (no score column)
```

### Step 4: Gap Detection

```
🕳️ Gap Report:

Cosmetic Gaps (silent defaults):
- Icon for "Convert" button: user-check
- Empty state for activity tab: "ยังไม่มี Activity"
- Pagination size: 20 (per FRD)

Structural Gaps (defaults logged):
- Activity log shape: assuming { at, actor, title, body, variant }
  (FRD didn't specify schema — defaulted to standard timeline shape)

Business Logic Gaps:
- (none)
```

### Step 5: Generate

```
🛠️ Generating F-01_Prospect.html...

Building shell (sidebar + breadcrumb + page header)...
Building Pattern A (list view)...
  ✓ Filter bar: search + status dropdown + reset
  ✓ Table: 7 columns (checkbox + name + email + status + source + created + actions)
  ✓ Pagination: 20/page

Building Pattern B (create drawer)...
  ✓ Drawer 920px slide-in
  ✓ Header: plus icon + "เพิ่ม Prospect ใหม่"
  ✓ Body: 2 sections (Basic Info + Source)
  ✓ Validation: R1 (email format), R3 (required fields)
  ✓ Footer: Cancel + Save Draft + Submit

Building Pattern C (view drawer)...
  ✓ Drawer 920px
  ✓ Header: dynamic avatar + name + status pill + action buttons
  ✓ Tabs: Overview / Activity / Notes
  ✓ Status-conditional buttons: active → Edit + Convert + Archive

Adding Pattern D (modals for Archive/Delete confirmations)...
  ✓ Archive modal (warning variant)
  ✓ Delete modal (danger variant)

Iron Rules audit:
  ✓ #1 CI tokens used
  ✓ #2 Noto Sans Thai loaded
  ✓ #3 Sidebar 232px gradient
  ✓ #4 Shell-bar 52px white
  ✓ #5 Lucide icons (no emoji)
  ✓ #6 Page header pattern
  ✓ #7 Breadcrumb
  ✓ #11 Drawer 920px
  ✓ #12 Slide animation
  ✓ #14 Drawer for Create (not modal)
  ✓ #16 Table 7 cols (≤8)
  ✓ #21 All icons have w-{N} h-{N}
  ✓ #23 No color emoji
  ✓ #25 renderIcons() after every render() (safe wrapper, NOT lucide.createIcons() directly)

All 26 Iron Rules pass ✓
```

### Step 6: Output

```
✅ Generated: F-01_Prospect.html (124KB)

📋 Summary:
- Single HTML file, hash routing (#/prospects, #/prospects/new, #/prospects/:id)
- 3 screens covered
- Sample data: 18 prospects across 4 statuses
- All validations from 05_RULES.md enforced
- Iron Rules audit: PASS (26/26)
- Cut features per BRD §14.6: respected (4 features excluded)

⚠️ Defaults applied (verify):
- Activity log structure (FRD didn't specify schema)
- 18 sample records (FRD didn't specify count)
- Pagination 20/page (per FRD)

Open in browser: ./F-01_Prospect.html
```

---

## 📋 Result: HTML Structure (Conceptual)

```html
<!DOCTYPE html>
<html lang="th">
<head>
  <!-- Standard CUBE NATIVE head: fonts, Lucide, full CSS from file-skeleton -->
</head>
<body>
  <!-- ERP shell from erp-shell.template.html -->
  <aside class="sidebar">...</aside>
  <main class="main">
    <header class="shell-bar">
      <nav class="breadcrumb">Core ERP > Marketing > Prospects</nav>
      ...
    </header>
    <div class="content">
      <div class="ph">
        <h1 class="ph-title">Prospects</h1>
        <span class="ph-count">18 รายการ</span>
        ...
        <button onclick="openDrawer('create')">+ Add Prospect</button>
      </div>

      <!-- Pattern A: List view -->
      <div class="card">
        <div class="filter-bar">...</div>
        <table class="table">...</table>
        <div class="table-footer">...</div>
      </div>
    </div>
  </main>

  <!-- Pattern B & C: Drawer (shared element, content swap by state) -->
  <div class="drawer-backdrop"></div>
  <div class="drawer">
    <!-- Render content per state.drawer.mode (create/view/edit) -->
  </div>

  <!-- Pattern D: Modal (shared, content swap by state) -->
  <div class="modal-backdrop">
    <div class="modal"></div>
  </div>

  <!-- Toast -->
  <div class="toast"></div>

  <script>
    // State, router, render(), event handlers
    // Sample data: 18 prospects
    // ...
  </script>
</body>
</html>
```

---

## 🎯 Key Takeaways from This Walkthrough

1. **Pipeline Mode is automatic** when FRD Pack is detected
2. **01_UI.md is the primary source** — read it first
3. **BRD §14.6 Functions Cut is respected** — drop features explicitly cut
4. **Defaults are filled for unspecified details** + logged in output
5. **Iron Rules audit always runs** before declaring "done"
6. **Output explains what was built** — not just delivers HTML silently

---

## ⚠️ When Pipeline Mode May Fail

- **FRD Pack incomplete:** Only `01_UI.md` present, no `05_RULES.md` → still generates UI, but validations are best-guess (logs which rules were inferred vs missing)
- **FRD spec inconsistent:** 01_UI.md says "show field A" but 04_DB.md doesn't have A → silent use 01_UI.md (UI wins for UI decisions), log warning
- **Brief and FRD disagree:** Apply priority (FRD wins) + log
- **Too many features in one Pack:** Ask user to scope down ("Pack มี 12 screens — focus หน้าไหนก่อน?")

---

## 📌 Quick Reference: When to Use What

| User says | Mode | Primary file to read |
|---|---|---|
| "Generate HTML from this FRD Pack" | Pipeline | `01_UI.md` |
| "Build prospect list page" (no docs) | Standalone | (chat context + defaults) |
| "Use this screenshot as reference" | Standalone | (screenshot analysis) |
| "Follow this Brief + BRD" (no FRD) | Standalone (Brief-based) | Brief.md |
| "Update existing HTML to add X" | Edit Mode | Existing HTML + delta |
