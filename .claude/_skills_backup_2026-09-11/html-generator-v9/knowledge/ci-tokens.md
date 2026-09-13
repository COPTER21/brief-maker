# CUBE — CI Tokens (v2.0 CUBE Rebrand / v3.13 fixed values)

> Source of truth for all colors, fonts, and spacing tokens used in HTML output.
> ห้าม override ค่าใน skill หรือใน HTML output — ใช้ตามนี้เท่านั้น
>
> **⭐ v2.0 (2026-07-09) — CUBE Design System Rebrand:** เปลี่ยนจากธีม Navy/Blue/Teal (CUBE NATIVE)
> เป็น **Warm Light theme** ของ CUBE Design System ใหม่ — Ivory ground `#FAF8F5`, White cards,
> Charcoal text `#111111`, **Red `#FF3B30` = action/priority**, **Orange `#FF9A1F` = connection**,
> ฟอนต์ **Satoshi (Latin) + Noto Sans Thai** แทน Inter
> **ชื่อ CSS var คงเดิมทั้งหมดเพื่อ backward-compat** — เปลี่ยนเฉพาะค่า:
> `--c-navy` = Charcoal · `--c-primary` = Red · `--c-teal` = Orange (อ่านตารางด้านล่างเป็นความหมายจริง)

---

## 🎨 Color Palette

### Brand Core (5 หลัก)

| Token | Hex | CSS var | ใช้กับ |
|---|---|---|---|
| Charcoal | `#111111` | `--c-navy` | Sidebar bg (flat), headings, primary text |
| Charcoal (alias) | `#111111` | `--c-navy-2` | เท่ากับ `--c-navy` — sidebar เป็นสีพื้นเดียว ไม่ใช่ gradient แล้ว |
| Red (Action) | `#FF3B30` | `--c-primary` | CTA buttons, links, focus ring, active menu item, priority |
| Red Hover | `#E62E24` | `--c-primary-hover` | Button hover state |
| Orange (Connection) | `#FF9A1F` | `--c-teal` | Secondary accent — connection/link-module semantics, logo gradient end |
| Orange Light | `#FFB763` | `--c-teal-light` | Orange hover/highlight บนพื้นเข้ม |

### Neutrals (Text + Borders + Bg)

| Token | Hex | CSS var | ใช้กับ |
|---|---|---|---|
| Ink | `#111111` | `--c-ink` | Primary text on white bg |
| Mute | `#54565C` | `--c-mute` | Secondary text |
| Mute 2 | `#73757B` | `--c-mute-2` | Tertiary text, labels |
| Mute 3 | `#9A9CA2` | `--c-mute-3` | Disabled text, placeholders, sidebar inactive |
| Line | `#DEDAD4` | `--c-line` | Input borders, table borders |
| Line 2 | `#E9E5E0` | `--c-line-2` | Card borders, dividers |
| Line 3 | `#F1EEEA` | `--c-line-3` | Subtle hover bg |
| Bg Off | `#FAF8F5` | `--c-bg-off` | App background |
| White | `#FFFFFF` | — | Card bg, modal bg, drawer bg |

### Semantic

| Token | Hex | CSS var | ใช้กับ |
|---|---|---|---|
| Success | `#1F9D55` | `--c-success` | Success state, positive trend |
| Warning | `#E8870F` | `--c-warning` | Warning state, attention needed |
| Danger | `#E62E24` | `--c-danger` | Error state, destructive action |

### Pill Background Variants (status badges)

| Status | Bg | Text | Use |
|---|---|---|---|
| Registered/Active/Info | `#E6F0FF` | `#1A5FCC` | New, in-progress |
| Converted/Success | `#E4F4EB` | `#157A41` | Completed, approved |
| Suspended/Warning | `#FFF1DD` | `#B8690B` | On-hold, needs attention |
| Archived/Inactive | `#F1EEEA` | `#73757B` | Inactive, archived |
| Danger | `#FFE9E7` | `#E62E24` | Rejected, failed |

---

## 🔤 Typography

### Font Stack

```css
font-family: 'Satoshi', 'Noto Sans Thai', system-ui, -apple-system, sans-serif;
```

**Load (Google Fonts):**
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Thai:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link href="https://api.fontshare.com/v2/css?f[]=satoshi@300,400,500,700,900&display=swap" rel="stylesheet">
```

### Base font

- **body:** `14px` / `line-height: 1.5` / `Noto Sans Thai`
- **antialiased:** `-webkit-font-smoothing: antialiased`

### Type Scale

> **v3.13: ค่าตายตัว — ห้ามใช้ช่วง.** ใช้ CSS var เท่านั้น ห้ามพิมพ์ px ตรง ๆ ใน feature CSS.

| Element | Var | ค่า | Weight | Color |
|---|---|---|---|---|
| Page title (h1) | `--fs-h1` | `22px` | 700 | `--c-navy` |
| Section title | `--fs-h2` | `17px` | 600 | `--c-navy` |
| Card title / drawer title | `--fs-h3` | `15px` | 600 | `--c-ink` |
| Body | `--fs-body` | `14px` | 400-500 | `--c-ink` / `--c-mute` |
| Secondary body / table cell | `--fs-sub` | `13px` | 400-500 | `--c-mute` |
| Meta / label | `--fs-meta` | `12px` | 500 | `--c-mute-2` |
| Uppercase caption | `--fs-cap` | `11px` | 700 | `--c-mute` (letter-spacing 0.08em, uppercase) |
| Stat value (KPI) | `--fs-kpi` | `28px` | 700 | `--c-navy` |

---

## 📐 Layout Tokens

### Scrollbar (Iron Rule #49 — บังคับทุกไฟล์)

> ห้ามใช้ default scrollbar ของ browser — ใช้ block นี้จาก skeleton เท่านั้น

```css
* { scrollbar-width: thin; scrollbar-color: rgba(17,17,17,.16) transparent; }
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-corner { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(17,17,17,.14); border-radius: 99px; }
::-webkit-scrollbar-thumb:hover { background: rgba(17,17,17,.26); }
.sidebar, .slide { scrollbar-color: rgba(255,255,255,.28) transparent; }
.sidebar ::-webkit-scrollbar-thumb, .slide ::-webkit-scrollbar-thumb,
.sidebar::-webkit-scrollbar-thumb, .slide::-webkit-scrollbar-thumb { background: rgba(255,255,255,.28); }
.sidebar ::-webkit-scrollbar-thumb:hover, .slide ::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,.42); }
```
- บาง `5px` มุมมน track โปร่งใส · พื้นเข้ม = ขาวโปร่ง · พื้นสว่าง = charcoal จาง

### Sidebar

```css
--sidebar-w: 232px;       /* Width */
```
- **Background:** `#111111` (flat charcoal — v2.0 ยกเลิก gradient แล้ว)
- **Border-right:** `1px solid rgba(255,255,255,0.06)`
- **z-index:** 20
- **position:** fixed (full height)
- **Active menu item:** bg `rgba(255,255,255,0.08)` + แถบซ้าย 3px สี `--c-primary` (red) + icon สี red
- **Inactive menu text:** `rgba(255,255,255,0.62)` → hover เป็น `#fff`

### Shell Bar (Header)

```css
--shell-h: 52px;          /* Height */
```
- **Background:** `#FFFFFF` (flat — not charcoal)
- **Border-bottom:** `1px solid var(--c-line-2)`
- **z-index:** 19
- **position:** sticky, top: 0
- **padding:** `0 22px`

> 📝 **Note:** Reference HTML uses **white shell-bar** (cleaner, more modern). 
> **Use the reference's white shell-bar** unless user explicitly asks for charcoal header.

### Content

- **padding:** `22px` (page padding around content)
- **margin-left:** `var(--sidebar-w)` (to clear fixed sidebar)

### Drawer

> **v3.13: unified เป็น DRAWER STANDARD v2 ค่าเดียวทั้ง skill** (ยกเลิก 540px legacy ทุกที่)

```css
.drawer { width: 920px; max-width: 96vw; }   /* v2 standard — create/edit/view */
.drawer.standard { width: 680px; }            /* simple form / short view */
.drawer { transition: transform 280ms cubic-bezier(0.4, 0, 0.2, 1); }
```
- **Backdrop:** `rgba(17,17,17,0.40)` + `transition: opacity 220ms`
- **Shadow:** `-16px 0 40px rgba(17,17,17,0.18)`
- **z-index:** backdrop 50, drawer 51

### Modal (Confirmation Only)

```css
.modal { width: 440px; max-width: 92vw; }    /* Centered card */
```
- **Backdrop:** `rgba(17,17,17,0.50)`
- **Border-radius:** `12px`
- **Shadow:** `0 24px 64px rgba(17,17,17,0.28)`
- **z-index:** backdrop 60, modal 61

---

## 🔢 Spacing Tokens

> **v3.13: ค่าตายตัว + เป็น CSS var จริงใน `:root` แล้ว** — ใช้ `var(--sp-*)` เท่านั้น

| Token | Var | Px | Use |
|---|---|---|---|
| xs | `--sp-xs` | 4 | Tight gap, icon margin |
| sm | `--sp-sm` | 8 | Button gap, inline gap |
| md | `--sp-md` | 12 | Card padding inner, input padding |
| lg | `--sp-lg` | 20 | Card padding outer, drawer padding |
| xl | `--sp-xl` | 28 | Section gap (page padding = 22px ตาม layout) |

---

## 🔘 Border Radius

> **v3.13: ค่าตายตัว + CSS var ใน `:root`** — ใช้ `var(--r-*)` เท่านั้น

| Token | Var | Px | Use |
|---|---|---|---|
| xs | `--r-xs` | 4 | Dot, tag เล็ก |
| sm | `--r-sm` | 6 | Button (small), icon button |
| md | `--r-md` | 8 | Button (default), input, card (inner) |
| lg | `--r-lg` | 12 | Card (outer), modal, drawer section |
| full | `--r-full` | 999 | Pill, circle avatar |

---

## ☁️ Shadows

| Use | Box-shadow |
|---|---|
| Card hover | `0 2px 8px rgba(17,17,17,0.05)` |
| Button primary hover | `0 2px 8px rgba(255,59,48,0.30)` |
| Drawer slide-in | `-16px 0 40px rgba(17,17,17,0.18)` |
| Modal | `0 24px 64px rgba(17,17,17,0.28)` |
| Notif/dropdown panel | `0 12px 32px rgba(17,17,17,0.12)` |

---

## 🎯 Icons

**Use Lucide icons only** — https://lucide.dev

⚠️ Lucide loader + `renderIcons()` helper อยู่ใน `file-skeleton.template.html` แล้ว — feature code **ห้าม** เพิ่ม `<script src="...lucide...">` เอง.

Pattern ที่ template ใช้ (multi-CDN fallback, pinned `@0.469.0`, end of body):
```html
<!-- ✅ จัดการให้ใน template แล้ว — ไม่ต้องเขียนเองใน feature -->
<!-- Multi-CDN: unpkg → jsdelivr → cdnjs, version 0.469.0 pinned -->
<!-- Loader exposes window.lucide + dispatches 'lucide:ready' event -->
```

ใน feature code ให้ใช้ helper ที่ template เตรียมไว้:
```js
// ✅ ถูก — safe wrapper, ทน race เมื่อ Lucide ยังไม่ load หรือ CDN fail ทุกตัว
renderIcons();

// ❌ ผิด — TypeError ถ้า lucide undefined
lucide.createIcons();
```

**ห้ามใช้:** color emoji (🔒✅⚠️📊 etc.), Heroicons, FontAwesome

**Icon size ต่อ context (ตายตัว — v3.13):**
| Context | Class |
|---|---|
| Chevron (sidebar/breadcrumb/expand) | `w-3 h-3` |
| ปุ่มใน drawer header / pill icon / table inline | `w-3.5 h-3.5` |
| ปุ่มทั่วไป (btn) / filter / toast | `w-4 h-4` |
| Page header action / stat trend | `w-5 h-5` |
| Empty state / modal icon ใหญ่ | `w-10 h-10` (ใน circle 56px) |

---

## 🚫 Things NEVER to use

- Crimson `#b02049` (legacy CUBE ERP — deprecated)
- Pink `#ffc0cb` (legacy)
- Color emoji of any kind (use Lucide icons)
- Random named colors (`red`, `blue`) — use CSS variables
- Inline hex codes (use CSS variables)

---

## 📋 Full `:root` Block (Copy verbatim into HTML)

```css
:root {
  --c-navy: #111111;
  --c-navy-2: #111111;
  --c-primary: #FF3B30;
  --c-primary-hover: #E62E24;
  --c-teal: #FF9A1F;
  --c-teal-light: #FFB763;
  --c-ink: #111111;
  --c-mute: #54565C;
  --c-mute-2: #73757B;
  --c-mute-3: #9A9CA2;
  --c-line: #DEDAD4;
  --c-line-2: #E9E5E0;
  --c-line-3: #F1EEEA;
  --c-bg-off: #FAF8F5;
  --c-success: #1F9D55;
  --c-warning: #E8870F;
  --c-danger: #E62E24;
  --sidebar-w: 232px;
  --shell-h: 52px;
  --fs-h1: 22px; --fs-h2: 17px; --fs-h3: 15px; --fs-body: 14px;
  --fs-sub: 13px; --fs-meta: 12px; --fs-cap: 11px; --fs-kpi: 28px;
  --sp-xs: 4px; --sp-sm: 8px; --sp-md: 12px; --sp-lg: 20px; --sp-xl: 28px;
  --r-xs: 4px; --r-sm: 6px; --r-md: 8px; --r-lg: 12px; --r-full: 999px;
}
```
