# ERP Design Guide — Sidebar / Shell-Bar / Breadcrumb / Page Header

> Read this **before** building any ERP feature. General/Web features → skip to `general-shell.template.html`.

---

## 🏗️ ERP App Shell — Overview

Every ERP page = **3 fixed zones + 1 scrollable content zone**

```
┌──────────┬────────────────────────────────────────────┐
│          │  Shell Bar (52px, sticky)                  │
│ Sidebar  ├────────────────────────────────────────────┤
│ (232px,  │                                            │
│  fixed)  │  Content (scroll, padding 22px)            │
│          │   ├─ Page Header (.ph)                     │
│          │   ├─ KPI Stats (optional)                  │
│          │   └─ Card (filter + table OR form OR ...)  │
└──────────┴────────────────────────────────────────────┘
```

---

## 🎨 Zone 1: Sidebar

### Specs

| Property | Value |
|---|---|
| Width | `232px` (CSS var `--sidebar-w`) |
| Height | full (`top: 0; bottom: 0`) |
| Position | `fixed` left edge |
| Background | `linear-gradient(180deg, #111111 0%, #111111 50%, #111111 100%)` |
| Border-right | `1px solid rgba(255,255,255,0.06)` |
| z-index | 20 |
| Color (text) | `#E9E5E0` (light gray on navy) |

### Structure (Iron Rule #27 — Module / Feature pattern)

Sidebar nav = **2-level hierarchy**: Module (collapsible group) → Feature (clickable item).

- **Module header** = group title; click = **toggle expand/collapse** only (NOT navigable). Use a `<button>` element, never `<a>`.
- **Feature item** = clickable navigation target (uses `<a>` with `data-feature`).
- **`data-module` + `data-feature`** = required identity attributes for future Menu Management + permission gating.

```html
<aside class="sidebar">
  <!-- 1. Brand block (top) -->
  <div class="sb-brand">
    <div class="sb-logo"><i data-lucide="box" class="w-4 h-4"></i></div>
    <div>
      <div class="sb-name">CUBE NATIVE</div>
      <div class="sb-sub">Core ERP</div>
    </div>
  </div>

  <!-- 2. Nav (middle, scrollable) — Module → Feature -->
  <nav class="sb-nav" id="sb-nav">

    <!-- Module = collapsible group -->
    <div class="sb-module" data-module="marketing" data-expanded="true">
      <button class="sb-module-header" type="button" onclick="toggleModule(this)">
        <i data-lucide="megaphone" class="mod-icon w-3.5 h-3.5"></i>
        <span class="mod-label">Marketing</span>
        <i data-lucide="chevron-down" class="mod-chevron w-3 h-3"></i>
      </button>
      <div class="sb-features">
        <a class="sb-item is-active" data-feature="prospects">
          <i data-lucide="users-round" class="w-4 h-4"></i>
          <span>Prospects</span>
          <span class="sb-badge">12</span>
        </a>
        <a class="sb-item" data-feature="campaigns">
          <i data-lucide="briefcase" class="w-4 h-4"></i>
          <span>Campaigns</span>
        </a>
      </div>
    </div>

    <div class="sb-module" data-module="sales" data-expanded="true">
      <button class="sb-module-header" type="button" onclick="toggleModule(this)">
        <i data-lucide="trending-up" class="mod-icon w-3.5 h-3.5"></i>
        <span class="mod-label">Sales</span>
        <i data-lucide="chevron-down" class="mod-chevron w-3 h-3"></i>
      </button>
      <div class="sb-features">
        <!-- more features... -->
      </div>
    </div>
  </nav>

  <!-- 3. Footer (bottom — env indicator, version, etc.) -->
  <div class="sb-footer">
    <div class="pulse-dot"></div>
    <span>UAT · v1.0.0</span>
  </div>
</aside>
```

**Required JS** (already in `file-skeleton.template.html`):
```javascript
function toggleModule(headerEl) {
  const mod = headerEl.closest('.sb-module');
  if (!mod) return;
  const isExpanded = mod.getAttribute('data-expanded') !== 'false';
  mod.setAttribute('data-expanded', isExpanded ? 'false' : 'true');
}
```

**Default expand state:**
- All modules start with `data-expanded="true"` on first render
- If the active feature lives inside a module → that module must be expanded (auto-rule)
- Future: persist user's collapse state per-session (localStorage) or per-user (DB)

### CSS Classes

```css
.sidebar {
  position: fixed;
  inset: 0 auto 0 0;
  width: var(--sidebar-w);
  background: linear-gradient(180deg, #111111 0%, #111111 50%, #111111 100%);
  color: #E9E5E0;
  z-index: 20;
  display: flex;
  flex-direction: column;
  border-right: 1px solid rgba(255,255,255,0.06);
}
.sb-brand {
  padding: 18px;
  display: flex;
  align-items: center;
  gap: 11px;
  border-bottom: 1px solid rgba(255,255,255,0.06);
  flex-shrink: 0;
}
.sb-logo {
  width: 34px; height: 34px;
  background: linear-gradient(135deg, #FF3B30, #FF9A1F);
  border-radius: 9px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  flex-shrink: 0;
  box-shadow: 0 4px 12px rgba(255,59,48,0.3);
}
.sb-name { font-weight: 700; font-size: 14px; color: #fff; letter-spacing: -0.01em; line-height: 1.2; }
.sb-sub { font-size: 10px; color: #9A9CA2; letter-spacing: 0.06em; font-weight: 600; text-transform: uppercase; margin-top: 2px; }
.sb-nav { flex: 1; padding: 12px 8px; overflow-y: auto; }

/* Module = collapsible group (Iron Rule #27).
   Header toggles expand/collapse only — NOT navigable. */
.sb-module { margin-bottom: 4px; }
.sb-module-header {
  display: flex; align-items: center; gap: 8px;
  width: 100%;
  padding: 8px 10px;
  border-radius: 6px;
  background: transparent; border: 0;
  color: #9A9CA2;
  font-family: inherit;
  font-size: 10.5px; font-weight: 700;
  letter-spacing: 0.08em; text-transform: uppercase;
  cursor: pointer; transition: all 120ms;
  text-align: left;
}
.sb-module-header:hover { background: rgba(255,255,255,0.04); color: #DEDAD4; }
.sb-module-header .mod-icon { flex-shrink: 0; opacity: 0.7; }
.sb-module-header .mod-label { flex: 1; }
.sb-module-header .mod-chevron { flex-shrink: 0; transition: transform 200ms; opacity: 0.7; }
.sb-module[data-expanded="false"] .mod-chevron { transform: rotate(-90deg); }
.sb-module[data-expanded="false"] .sb-features { display: none; }

.sb-features { padding: 2px 0 6px 0; }

.sb-item {
  display: flex; align-items: center; gap: 10px;
  padding: 7px 12px 7px 14px;
  border-radius: 6px;
  color: #DEDAD4;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 120ms;
  margin-bottom: 1px;
  position: relative;
  user-select: none;
}
.sb-item:hover { background: rgba(255,255,255,0.05); color: #fff; }
.sb-item.is-active {
  background: #FF3B30;
  color: #fff;
  font-weight: 600;
}
.sb-item.is-active::before {
  content: '';
  position: absolute;
  left: -10px; top: 7px; bottom: 7px;
  width: 3px;
  background: #fff;
  border-radius: 0 2px 2px 0;
}
.sb-item .icon, .sb-item [data-lucide] { width: 16px; height: 16px; opacity: 0.85; }
.sb-item.is-active .icon, .sb-item.is-active [data-lucide] { opacity: 1; }
.sb-badge {
  margin-left: auto;
  font-size: 10.5px;
  font-weight: 600;
  background: rgba(255,255,255,0.10);
  color: #9A9CA2;
  padding: 2px 7px;
  border-radius: 999px;
}
.sb-item.is-active .sb-badge { background: rgba(255,255,255,0.18); color: #fff; }
.sb-footer {
  padding: 12px 16px;
  border-top: 1px solid rgba(255,255,255,0.06);
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 11.5px;
  color: #9A9CA2;
}
.pulse-dot {
  width: 7px; height: 7px;
  background: var(--c-teal);
  border-radius: 50%;
  box-shadow: 0 0 0 3px rgba(255,154,31,0.20);
  animation: pulse 2s infinite;
}
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.6; }
}
```

### Rules

- **Active item** = bold + bg `#FF3B30` + left white bar (3px wide)
- **Section title** = uppercase, 10px, letter-spacing 0.1em
- **Disabled item** = `opacity: 0.4 + cursor: not-allowed`
- **Badge** = optional, right-aligned, shows count

---

## 🎨 Zone 2: Shell Bar (Top Header)

### Specs

| Property | Value |
|---|---|
| Height | `52px` (CSS var `--shell-h`) |
| Background | `#FFFFFF` (white — modern look) |
| Border-bottom | `1px solid var(--c-line-2)` |
| Position | `sticky; top: 0` |
| z-index | 19 |
| padding | `0 22px` |

### Structure (Iron Rule #28 — Slim Top Bar)

Top Bar = **3 zones**: Breadcrumb (left) + Notification + User Chip (right).
**No Help button. No Search button.** Slim by default — extra actions belong inside pages or feature-specific toolbars.

```html
<header class="shell-bar">
  <!-- Left: Breadcrumb (Module › Feature, 2 levels minimum) -->
  <nav class="breadcrumb">
    <a data-breadcrumb-module="marketing">Marketing</a>
    <i data-lucide="chevron-right" class="w-3 h-3 sep"></i>
    <span class="breadcrumb-current">Prospects</span>
  </nav>

  <!-- Right: Notification + User (no Help, no Search) -->
  <div style="display: flex; align-items: center; gap: 6px; margin-left: auto;">
    <div class="notif-wrap" style="position: relative;">
      <button class="icon-btn" onclick="toggleNotif()" id="notifBtn" title="แจ้งเตือน">
        <i data-lucide="bell" class="w-4 h-4"></i>
        <span class="notif-dot"></span>
      </button>
      <!-- notif-panel rendered here when open (future feature) -->
    </div>
    <div class="user-chip" onclick="toggleUserMenu()">
      <div class="user-text">
        <div class="user-name">Tadswan C.</div>
        <div class="user-role">Marketing Lead · CUBE NATIVE</div>
      </div>
      <div class="avatar">TC</div>
    </div>
    <!-- user-menu rendered here when open (My Profile / Preferences / Sign out) -->
  </div>
</header>
```

**Breadcrumb rules:**
- Pattern: `[Module] › [Feature]` (2 levels minimum). 3+ levels allowed when a feature has sub-pages (e.g. `Sales › Quotations › QT-2024-001`).
- Level-1 (Module) = clickable, hover turns primary blue. Optionally `data-breadcrumb-module="..."` to link back to the matching sidebar module.
- Last level (current page) = `.breadcrumb-current`, **not clickable**, color `--c-ink`, font-weight 500.
- Separator = `<i data-lucide="chevron-right" class="w-3 h-3 sep"></i>` (NEVER `›` text — Iron Rule #28).

**User Chip rules:**
- 2-line text: `user-name` (12.5px, ink) / `user-role` (10.5px, mute). Role line should include tenant: `"Marketing Lead · CUBE NATIVE"`.
- Avatar = circle 30px, gradient `Primary → Teal`, 2-character initials.
- Click = open dropdown (My Profile / Preferences / divider / Sign out). Dropdown itself is part of `templates/erp-shell.template.html`.

### CSS Classes

```css
.shell-bar {
  position: sticky;
  top: 0;
  background: #fff;
  border-bottom: 1px solid var(--c-line-2);
  height: var(--shell-h);
  display: flex;
  align-items: center;
  padding: 0 22px;
  z-index: 19;
  gap: 12px;
}
.breadcrumb {
  display: flex;
  align-items: center;
  gap: 7px;
  font-size: 13px;
  color: var(--c-mute);
}
.breadcrumb a { cursor: pointer; transition: color 120ms; }
.breadcrumb a:hover { color: var(--c-primary); }
.breadcrumb .sep { color: var(--c-mute-3); }
.breadcrumb-current { color: var(--c-ink); font-weight: 500; }
.icon-btn {
  width: 34px; height: 34px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: 0;
  color: var(--c-mute);
  border-radius: 7px;
  position: relative;
  transition: all 120ms;
}
.icon-btn:hover { background: var(--c-line-3); color: var(--c-ink); }
.notif-dot {
  position: absolute;
  top: 7px; right: 8px;
  width: 7px; height: 7px;
  background: var(--c-danger);
  border-radius: 50%;
  border: 2px solid #fff;
}
.user-chip {
  display: flex;
  align-items: center;
  gap: 9px;
  padding: 5px 10px 5px 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: background 120ms;
}
.user-chip:hover { background: var(--c-line-3); }
.user-text { line-height: 1.2; text-align: right; }
.user-name { font-size: 12.5px; font-weight: 500; color: var(--c-ink); white-space: nowrap; }
.user-role { font-size: 10.5px; color: var(--c-mute-2); white-space: nowrap; margin-top: 1px; }
.avatar {
  width: 30px; height: 30px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--c-primary), var(--c-teal));
  color: #fff;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 600;
  flex-shrink: 0;
}
```

### Rules

- **Breadcrumb** = always present, left-aligned. Items separated by `chevron-right` icon.
- **Right cluster** = icon buttons + user chip. Max 3 icon buttons before user chip.
- **User chip** = name + role + avatar (initials of real name, not "U" or "?").
- **ห้ามใส่:** search box, refresh button, settings ที่ไม่ทำงาน. ใส่ใน filter bar ถ้าจำเป็น.

---

## 🎨 Zone 3: Page Header (`.ph`)

### Purpose

แสดง **identity ของหน้าปัจจุบัน** — title, count, subtitle, primary actions.
**1 page = 1 ph block** (อยู่ในสุดบนของ content area).

### Structure

```html
<div class="ph">
  <div class="ph-title-row">
    <h1 class="ph-title">Prospects</h1>
    <span class="ph-count">29 รายการ</span>
  </div>
  <p class="ph-sub">จัดการลูกค้าเป้าหมายจากแหล่งต่างๆ และติดตามจน convert เป็น Customer</p>
  <div class="ph-actions">
    <button class="btn btn-secondary"><i data-lucide="download" class="w-4 h-4"></i>Export</button>
    <button class="btn btn-primary"><i data-lucide="plus" class="w-4 h-4"></i>Add Prospect</button>
  </div>
</div>
```

### CSS Classes

```css
.ph {
  margin-bottom: 18px;
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: flex-start;
  gap: 14px;
}
.ph > div:first-child { flex: 1 1 auto; min-width: 280px; }
.ph-title-row {
  display: flex;
  align-items: baseline;
  gap: 10px;
  margin-bottom: 5px;
}
.ph-title {
  font-family: 'Noto Sans Thai', sans-serif;
  font-size: 22px;
  font-weight: 700;
  color: var(--c-navy);
  margin: 0;
  letter-spacing: -0.01em;
}
.ph-count {
  font-size: 12.5px;
  font-weight: 600;
  color: var(--c-mute-2);
  background: var(--c-line-3);
  padding: 3px 9px;
  border-radius: 999px;
}
.ph-sub { font-size: 13px; color: var(--c-mute); margin: 0; }
.ph-actions { display: flex; gap: 8px; flex-shrink: 0; }
```

### Rules

- **Title** = h1, 22px, weight 700, color navy. **ห้าม:** title ซ้ำใน shell bar.
- **Count badge** = แสดงจำนวน records (เฉพาะ list page). Pill style.
- **Subtitle** = 1 บรรทัด, สีเทา. อธิบาย purpose ของหน้า.
- **Actions** = primary + secondary buttons. Primary action ขวาสุด.

---

## 🎨 Zone 4: Content

### Wrapper

```html
<main class="main">
  <header class="shell-bar"><!-- ... --></header>
  <div class="content">
    <!-- ph + stats + card here -->
  </div>
</main>
```

### CSS

```css
.main {
  margin-left: var(--sidebar-w);
  min-height: 100vh;
  background: var(--c-bg-off);
}
.content {
  padding: 22px;
  /* Fluid full-width — no max-width cap (Iron Rule #30).
     Admin tools need to use horizontal real estate efficiently on
     wide monitors (1920px / 2560px / 4K). Component-level constraints
     (modal/toast/wizard internal cards/document previews) keep their
     own readability bounds. */
}
```

> 📝 **Note on fluid layout (v3.5):** เดิม `.content` มี `max-width: 1640px` cap ซึ่งทำให้บน monitor 1920px+ เหลือ whitespace ขวา (ไม่ stretch เต็ม). ปัจจุบันลบ cap ออก content stretch เต็ม viewport. ดู Iron Rule #30 + section "Fluid Page Layout" ด้านล่าง

### Content Patterns

ส่วน content เลือกใช้ตาม pattern:
- **A:** List page (filter + table)
- **C:** Detail view (drawer with tabs)
- **B:** Create/Edit (drawer slide-in with form)
- **D:** Confirmation (modal)
- etc. (see `patterns/`)

---

## 📋 Complete ERP Shell Template

ดู `templates/erp-shell.template.html` สำหรับ HTML ทั้ง shell (sidebar + shell-bar + content wrapper) ที่ copy-paste ใช้ได้ทันที.

---

## 📐 Fluid Page Layout (v3.5)

### หลักการ
Admin tool ของ CUBE NATIVE ออกแบบแบบ **desktop-base + adaptive** (v7.1 Rule #97: `body min-width: 768px` · ≥1180 เต็มรูปแบบ · 768–1180 adaptive ผ่าน media query ใน skeleton — sidebar off-canvas/rail, drawer `min(กว้างเดิม,100vw)` · <768 horizontal scroll ไม่ guarantee) — บนจอกว้าง (1920px / 2560px / 4K) ต้องใช้พื้นที่ horizontal ให้คุ้ม **ไม่** capped ที่ค่าใดค่าหนึ่ง.

### Policy

| Component | Width policy | เหตุผล |
|---|---|---|
| `.content` (page wrapper) | **fluid — no max-width** | Stretch เต็ม viewport — Table list, Dashboard, Detail ใช้พื้นที่กว้างได้คุ้ม |
| `.modal` | `width: 440px; max-width: 92vw` | Modal ต้องกะทัดรัด อ่านครั้งเดียวจบ |
| `.toast` | `max-width: 380px` | Toast ต้องกะทัดรัด อยู่มุมจอ |
| `.wizard-card` | `max-width: 960px; margin: auto` | Form readability — long input row ยาวเกินไปอ่านยาก |
| `.stepper-row` | `max-width: 640px; margin: auto` | Stepper ตรงกลาง ไม่กว้างเกิน step สามารถอ่านได้ |
| A4 paper / Invoice preview | `max-width: 820px; margin: auto` | จำลอง paper proportion |
| Text paragraph (hero sub, etc.) | `max-width: 640px` (optional) | Line length 65-75 chars/line (readability) |

### ✅ Correct pattern
```css
.content {
  padding: 22px;
  /* fluid — no max-width */
}
```

### ❌ Wrong pattern
```css
.content {
  padding: 22px;
  max-width: 1640px;  /* ❌ Blocks fluid layout on wide monitors */
}
```

### When the content body needs internal constraints
ใช้ **child element** เป็น constraint ไม่ใช่ wrapper:
```html
<!-- ✅ Good: wrapper fluid, inner content has constraint -->
<main class="content">
  <div class="page-header">...</div>
  <div style="max-width: 1640px;">  <!-- if specific page needs cap -->
    ...
  </div>
</main>
```

---

## 🚨 Common Mistakes to Avoid

1. **❌** ใส่ title ใน shell-bar + page header (duplicate)
2. **❌** Sidebar กว้างเกิน 240px หรือแคบกว่า 220px (standard = 232)
3. **❌** Shell-bar background สี navy (ใช้ white ตาม reference)
4. **❌** Breadcrumb ใส่ใน content area (ต้องอยู่ใน shell-bar)
5. **❌** Avatar เป็น icon `user` (ต้องเป็น initials เช่น `TC`)
6. **❌** ใช้ emoji แทน Lucide icon (🏠 → `home`)
7. **❌** Active menu item ไม่มี white left bar (rule #3 active state)
8. **❌** Content padding เกิน 24px หรือต่ำกว่า 20px (standard = 22)
9. **❌ (v3.5)** ใส่ `max-width: 1640px` (หรือค่าอื่น) บน `.content` — block fluid layout ทำให้เหลือ whitespace ขวาบนจอกว้าง (Iron Rule #30)
