# CHANGELOG v4.2 — Pattern N Sidebar Shell + Minimal Scrollbar (2026-07-09)

ต่อยอดจาก v4.1 (CUBE CI Rebrand) — เพิ่ม 2 อย่างตาม Menu_Layout_v2 package

## 1. 🆕 Pattern N — Sidebar Navigation Shell

Register เมนู "core-shell-ultimate" เข้าเป็น pattern มาตรฐาน (ตาม OQ-05 ของ brief ต้นทาง)

- **`patterns/N_sidebar-nav-shell.md`** — pattern doc: menu model 3 ระดับ (Module›Group›Feature,
  หัวโมดูล/กลุ่ม toggle-only ห้าม navigate), 2 โหมด (กางเต็ม 244px default / icon rail 58px + slide panel 216px),
  visual hierarchy ด้วย inset well + เส้นราง + เยื้อง (ไม่ใช้สีบอกชั้น — Red สงวนให้ active เท่านั้น),
  behavior contracts (revealActive 3 จังหวะ, พับ active ได้, z-index scrim 30 < panel 34 < sidebar 35,
  anim เฉพาะเปิด panel, Esc คืน focus, ↑↓ Enter, tooltip 240ms, ⌘K), a11y contract ครบ (WCAG 1.4.13/2.4.3/2.4.7/3.2.1)
- **`references/sidebar-shell/core-shell-ultimate.html`** — reference ต้นแบบ (ผ่าน Playwright 35 เคส)
  **rebrand เป็น CI ใหม่แล้ว:** sidebar+panel flat Charcoal `#111111`, active item Red `#FF3B30`,
  ไอคอนโมดูลที่มี active = Orange Light `#FFB763`, caption/muted บนพื้นเข้มเป็น warm gray
  (`#6F86A3→#85878D`, `#7C93B2→#9A9CA2`), Satoshi + Noto Sans Thai, scrollbar ตาม Rule #49
- **`references/sidebar-shell/UI_REVISION_BRIEF_core-shell-sidebar.md`** — brief ต้นฉบับเก็บเป็น
  design rationale (มี note ชี้ว่าให้ยึด Pattern N + reference ที่ rebrand แล้ว)
- SKILL.md: pattern range A-M → **A-N** (decision tree, mapping table, file table, override note)

## 2. 🆕 Iron Rule #49 — Minimal Scrollbar (รวมเป็น 49 rules)

ห้ามใช้ default scrollbar ของ browser ในทุกไฟล์ที่ generate:

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

- บาง **5px** มุมมน · track/corner โปร่งใส · **พื้นเข้ม (sidebar/panel) = ขาวโปร่ง** · พื้นสว่าง = charcoal จาง
- Firefox: `scrollbar-width: thin` + `scrollbar-color` บังคับคู่กัน
- ❌ ห้าม `overflow: overlay` และห้ามซ่อน scrollbar ทั้งหมด
- ฝังใน: `templates/file-skeleton.template.html` (§SCROLLBAR), `knowledge/ci-tokens.md`,
  `knowledge/iron-rules.md` (Group 17), reference ทั้งสองไฟล์
- **audit.sh:** ไม่มี `::-webkit-scrollbar` = **FAIL** · ไม่มี `scrollbar-width` = WARN

## Verification
- `bash -n scripts/audit.sh` ✅ syntax OK
- `audit.sh references/sidebar-shell/core-shell-ultimate.html` → **FAIL=0** (WARN 2 = ของเดิมใน source, minor)
- ไม่เหลือ hex CI เก่าในไฟล์ใหม่ทั้งหมด
