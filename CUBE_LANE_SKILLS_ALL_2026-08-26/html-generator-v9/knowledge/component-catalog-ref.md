# Component Catalog — Canonical Names + Props

> Source of truth for component names. Use these names verbatim in HTML class names.
> Total: 41 components. (v3.13: เพิ่ม stepper, tile, timeline)

---

## 🏗️ Group 1: App Shell (4 components)

### 1. `sidebar`
Fixed left navigation. 232px wide, gradient navy bg.
**Sub-components:** `sb-brand`, `sb-logo`, `sb-name`, `sb-sub`, `sb-nav`, `sb-module`, `sb-module-header` (`mod-icon`/`mod-label`/`mod-chevron`), `sb-features`, `sb-item`, `sb-badge`, `sb-footer`, `pulse-dot`
**⚠️ BANNED (Iron Rule #27):** `sb-section`, `sb-section-title` — legacy flat pattern ห้ามใช้
**States:** `.is-active`, `.is-disabled`, `:hover`

### 2. `shell-bar`
Top header. 52px tall, white bg, sticky.
**Sub-components:** `breadcrumb`, `breadcrumb-current`, `icon-btn`, `notif-dot`, `user-chip`, `user-text`, `user-name`, `user-role`, `avatar`

### 3. `breadcrumb`
Trail of navigation. In shell-bar, left side.
**Sub-components:** `sep` (chevron-right icon class)

### 4. `main` / `content`
Right-of-sidebar wrapper + inner content padding (22px).

---

## 📄 Group 2: Page Header (1 component)

### 5. `ph` (Page Header)
Top of every content page. Contains title, subtitle, count, actions.
**Sub-components:** `ph-title-row`, `ph-title`, `ph-count`, `ph-sub`, `ph-actions`

---

## 📊 Group 3: KPI / Stats (1 component)

### 6. `stats` + `stat`
KPI cards row.
**Sub-components:** `stat-label`, `stat-value`, `stat-meta`
**Variants:** `stat-meta.is-up`, `stat-meta.is-down`

---

## 🔘 Group 4: Buttons (1 component, 4 variants)

### 7. `btn`
**Variants:** `btn-primary`, `btn-secondary`, `btn-ghost`, `btn-danger`, `btn-link`
**Sizes:** `btn-sm` (30px), default (36px)
**Icon support:** `<i data-lucide="..." class="w-4 h-4"></i>` ใน button

---

## 📦 Group 5: Card + Filter + Table (8 components)

### 8. `card`
White container with border + radius. Standard wrapper for table/form.

### 9. `filter-bar`
In card, top section. Contains search + selects + reset button.
**Padding:** 14px 18px
**Border-bottom:** `var(--c-line-2)`

### 10. `input` / `select`
Form inputs. Border `var(--c-line)`, focus border `var(--c-primary)`.

### 11. `input-search`
Wrapper with leading search icon.
**Sub-component:** `lead-icon`

### 12. `table`
Data table.
**Sub-classes:** `table-scroll`, `table th`, `table td`, `table tbody tr.is-selected`
**Header states:** `is-sortable`, `is-sorted`, `sort-arrow`
**Column types:** `col-check` (40px), regular, action (60px)

### 13. `cb` (Checkbox)
Custom checkbox.
**States:** `.is-checked`, `.is-partial`

### 14. `table-footer`
Footer of table card with pagination + count.
**Sub-component:** `pagination`, `pg-btn` (with `.is-active`, `.is-disabled`)

### 15. `row-actions` + `ra-btn`
Inline action buttons in table row.
**Variants:** `ra-btn`, `ra-btn.is-danger`, `ra-btn.is-success`

---

## 🏷️ Group 6: Pills + Dots + Status (3 components)

### 16. `pill`
Status badge.
**Variants:** `pill-registered`, `pill-active`, `pill-converted`, `pill-suspended`, `pill-archived` (extend as needed)

### 17. `dot`
Status indicator dot (4px).
**Variants:** `.is-active`, `.is-converted`, `.is-suspended`, `.is-archived`

### 18. `bulk-bar`
Sticky bar at top of card when rows selected. Navy bg.

---

## 👤 Group 7: User / Avatar Components (3 components)

### 19. `user-cell`
Cell with avatar + name + email (in table).
**Sub-components:** `uc-avatar`, `uc-name`, `uc-email`

### 20. `user-chip`
In shell-bar, top right. Contains user-text + avatar.

### 21. `avatar`
Circle with initials, gradient bg.
**Sizes:** Default 30px (shell-bar), 44px (drawer-avatar), 32px (uc-avatar)

---

## 🪟 Group 8: Drawer + Modal + Form (7 components)

### 22. `drawer-backdrop` + `drawer`
Slide-in panel from right. 920px wide (v2), `.standard` = 680px.
**Sub-components:**
- `drawer-header` — avatar + title + subtitle + close
- `drawer-avatar` — 44px circle
- `drawer-title`, `drawer-subtitle`
- `drawer-tabs`, `drawer-tab` (with `.is-active`)
- `drawer-body` — scroll area
- `drawer-section`, `drawer-section-title`
- `drawer-fields` — grid label/value
- `drawer-footer` — sticky bottom

### 23. `modal-backdrop` + `modal`
Centered confirmation card. 440px wide.
**Sub-components:**
- `modal-header` — icon + title + subtitle + close
- `modal-header-icon` (with `.is-danger`, `.is-warning`)
- `modal-title`, `modal-subtitle`
- `modal-body`
- `modal-footer`

### 24. `field` (Form field)
Wrapper for input + label + help + error.
**Sub-components:** `field-label`, `field-label .req`, `field-input`, `field-help`, `field-error`

### 25. `notes-area`
Textarea for notes/comments.

### 26. `toast`
Bottom-right notification.
**Variants:** `.is-success`, `.is-info`, `.is-warning`, `.is-error`

### 27. `tenant-link`
Mini-link with arrow icon (for converted prospect → linked customer).

### 28. `empty`
Empty state.
**Sub-components:** `empty-icon`, `empty-title`, `empty-desc`

---

## 🕒 Group 9: Timeline + Activity (1 component)

### 29. `timeline` + `tl-item`
Vertical timeline (activity log).
**Sub-components:** `tl-dot` (with `.is-success`, `.is-warning`), `tl-title`, `tl-meta`

---

## 📌 Group 10: Misc (3 components)

### 30. `bm-card` (Bookmark Card)
Card with icon + label (for related links in drawer).
**Sub-components:** `bm-icon`

### 31. `notif-wrap` + `notif-panel`
Notification dropdown (anchored to bell icon in shell-bar).
**Sub-components:** `notif-header`, `notif-list`, `notif-item` (with `.is-unread`), `notif-icon-box` (with semantic variants), `notif-title`, `notif-meta`, `notif-empty`, `notif-footer`, `notif-mark-read`

### 32. `user-menu`
Dropdown from user-chip.
**Sub-components:** `user-menu-item` (with `.is-danger`), `user-menu-divider`

---

## 🎯 Component Selection Rules

### When to use Drawer vs Modal?

| Use Case | Component | Width |
|---|---|---|
| Create new record | **Drawer** (slide-in) | 920px (.standard 680) |
| Edit existing record | **Drawer** (slide-in) | 920px (.standard 680) |
| View detail with tabs | **Drawer** | 540-680px |
| Confirm action (delete, archive) | **Modal** | 440px |
| Simple 1-3 field form (rare) | **Modal** | 440px |
| Multi-step wizard | **Drawer** (full body) or full page | 920px / full |
| Print preview (PDF) | **Drawer** (PO-style) | 680px |

### When to use `ph-count` badge?

- ✅ List pages (e.g., "29 รายการ")
- ❌ Detail pages, create/edit pages, dashboards

### When to use `bulk-bar`?

- ✅ Table with multi-select (checkbox column)
- ❌ Single-record actions, detail views

---

## 📋 Iron Rule Cross-Reference

| Component | Related Iron Rules |
|---|---|
| sidebar | #3, #5 (icons), #21 (icon classes) |
| shell-bar | #4, #7 (breadcrumb) |
| ph | #6 (page header pattern) |
| stats | #8 |
| filter-bar | #9 (in card) |
| table | #16 (≤8 cols), #21 (icon classes) |
| drawer | #11 (width), #12 (animation), #13 (4 zones), #15 (close methods) |
| modal | #11 (width), #14 (confirmation only) |
| field | #18 (structure), #19 (no number spinner) |
| toggle | #20 (div onclick) |
| all icons | #21 (w-{N} h-{N} required) |
| wizard | #22 (full-height flex) |
| everywhere | #23 (no emoji), #24 (no dev-tool), #25 (createIcons) |


---

## 🆕 Group v3.13 additions (3 components)

### 39. `stepper`
Wizard step indicator กลาง (Iron Rule #47).
**Sub-components:** `step`, `step-dot`, `step-label`, `step-connector`, `drawer-stepper-band`
**States:** `.is-done`, `.is-current`

### 40. `tile`
Landing feature tile (Pattern M / Rule #48).
**Sub-components:** `tile-icon`, `tile-text`, `tile-title`, `tile-desc`, `tile-chev`, `hero`, `hero-inner`, `hero-title`, `hero-sub`, `hero-actions`

### 41. `timeline`
Activity log แนวตั้ง (Pattern L3).
**Sub-components:** `tl-item`, `tl-dot`, `tl-body`, `tl-title`, `tl-meta`
**States:** `tl-dot.is-success`, `tl-dot.is-danger`
