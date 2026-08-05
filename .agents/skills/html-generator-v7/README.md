# html-generator-v7 — Auxiliary Files Pack

> Auxiliary files for `html-generator-v7` — consolidated release (2026-08-03):
> v6 base ทั้งหมด + **Pattern B2 Document Line Editor** (locked reference จาก F-PR-001,
> CI Warm Light, multi-UoM + VAT 3 โหมด + WHT/ส่วนลดท้ายบิล + hard control) +
> **Iron Rule #94 Master-Backed Field = Search Combobox** (canonical: master-combobox.js.txt)
> + QC Rules #83–#92 (component-contracts) + Rule #11 exception `.drawer-panel.wide` 1290px.
> Lineage: html-generator-25 → v3.x → v4.x → v6 → **v7**.
> Reference: `core-marketing-prospect.html` (CSS skeleton + design tokens).

---

## 📁 Folder Structure

```
html-generator-v7/
├─ knowledge/                      # 4 files — Design system foundations
│  ├─ ci-tokens.md                  # CI colors, fonts, layout tokens
│  ├─ iron-rules.md                 # 49 inviolable rules (v6.0)
│  ├─ erp-design-guide.md           # Sidebar / shell-bar / breadcrumb / page-header
│  └─ component-catalog-ref.md      # 38 components in 10 groups
│
├─ templates/                       # 3 files — Copy-paste HTML templates
│  ├─ file-skeleton.template.html   # Base HTML skeleton (~1,200 lines full CSS)
│  ├─ erp-shell.template.html       # ERP sidebar + shell-bar + content wrapper
│  └─ general-shell.template.html   # Public/marketing (no sidebar)
│
├─ patterns/                        # 13 files — UI patterns A through M (v3.13: +J dashboard, +K report, +L collection, +M landing)
│  ├─ A_list-view.md                # Filter + table + pagination
│  ├─ B_create-edit-drawer-wizard.md # ⭐ Drawer slide-in for Create/Edit (override)
│  ├─ C_view-drawer-tabbed.md       # View detail with tabs
│  ├─ D_modal-confirmation.md       # Confirmation modal (440px)
│  ├─ E_compact-table-expandable.md # Compact table with expandable rows
│  ├─ F_configurable-modifier.md    # Toggle + sub-config card
│  ├─ G_po-style-view-drawer.md     # Wide drawer (680px) with PDF preview
│  ├─ H_a4-paper-pdf-preview.md     # A4 print-ready layout
│  └─ I_signature-card-list.md      # Approval signatures
│
├─ references/                      # 4 files — Mode logic
│  ├─ pipeline-mode.md              # Input from FRD Pack
│  ├─ standalone-mode.md            # Flexible input (text/screenshot/Brief)
│  ├─ conflict-resolution.md        # Priority order when sources disagree
│  └─ gap-detection.md              # Defaults vs ask-user protocol
│
└─ examples/                        # 1 file — Walkthrough
   └─ pipeline-mode-walkthrough.md  # F-01 Prospect generation example
```

**Total:** 20 files (excl. README) · 6,495 lines · 276 KB

---

## 🎯 Key Design Decisions

### 1. Reference HTML drives the CSS skeleton

`core-marketing-prospect.html` is **cleaner and more modern** than v25's embedded CSS. We use:
- **White shell-bar** (not navy — modern look)
- Sidebar 232px (not 256px)
- Drawer 920px v2 standard (.standard 680px)
- Modal 440px max-width
- Full `:root` CSS variables block

### 2. Create/Edit = Drawer Slide-in (override)

Reference HTML uses modal for Create — **but per user requirement**, Pattern B uses **drawer slide-in** instead:
- Wider editing surface (920px v2)
- Consistent with Edit (also drawer)
- Modal reserved for confirmations only (Pattern D)

This override is enforced as **Iron Rule #14**.

### 3. Modular vs Monolithic

v25 = monolith (one 144KB SKILL.md, all content embedded).
v3 = modular (20 files, each focused on one concern).

Trade-offs:
| Aspect | v25 (monolith) | v3 (modular) |
|---|---|---|
| Self-contained | ✅ Single file | ❌ Needs file system |
| Easy to grep/find | ❌ One huge file | ✅ Locate by folder |
| Easy to update one part | ❌ Risk breaking other parts | ✅ Edit only relevant file |
| Context window | ❌ Large load | ✅ Selective load |
| SKILL.md size | ❌ 144KB | ✅ ~20KB orchestrator only |

---

## 🛠️ How to Use This Pack

### As html-generator-v7 skill author:

1. Place these files alongside `SKILL.md` in `/mnt/skills/user/html-generator-v7/`:
   ```
   /mnt/skills/user/html-generator-v7/
   ├─ SKILL.md           ← orchestrator (~424 lines, exists)
   ├─ knowledge/         ← from this pack
   ├─ patterns/          ← from this pack
   ├─ references/        ← from this pack
   ├─ templates/         ← from this pack
   └─ examples/          ← from this pack
   ```

2. SKILL.md will reference these files via paths in its instructions.

3. When skill activates, it reads relevant files on demand based on input type (Pipeline vs Standalone).

### As HTML generator (Claude using this skill):

1. **First:** Read `SKILL.md` for orchestration logic
2. **Then:** Read needed knowledge files (always start with `knowledge/iron-rules.md` + `knowledge/ci-tokens.md`)
3. **Pick pattern(s)** based on user input → read those pattern files
4. **Pick template** (erp-shell vs general-shell)
5. **Generate HTML** = template + patterns + CI tokens + iron rules
6. **Audit:** Verify all 26 Iron Rules pass before saving

---

## 📋 File Reading Strategy

Don't read all 20 files for every generation. Selectively read based on input:

| Input | Required Files |
|---|---|
| **Any generation** | `knowledge/ci-tokens.md` + `knowledge/iron-rules.md` + `templates/file-skeleton.template.html` |
| **ERP feature** | + `knowledge/erp-design-guide.md` + `templates/erp-shell.template.html` |
| **Public/marketing** | + `templates/general-shell.template.html` |
| **List page** | + `patterns/A_list-view.md` |
| **Create/Edit** | + `patterns/B_create-edit-drawer-wizard.md` |
| **View detail** | + `patterns/C_view-drawer-tabbed.md` |
| **Delete/Archive confirm** | + `patterns/D_modal-confirmation.md` |
| **PO/Invoice document** | + `patterns/G` + `patterns/H` + `patterns/I` |
| **FRD Pack input** | + `references/pipeline-mode.md` + `references/conflict-resolution.md` |
| **Ad-hoc input** | + `references/standalone-mode.md` + `references/gap-detection.md` |

Look-up `knowledge/component-catalog-ref.md` when unsure of canonical component name.

---

## 🛡️ Iron Rules (Most Critical)

Even with all the modular files, **these 48 rules ALWAYS apply** (no exception):

1. CI tokens locked (use CSS variables)
2. Satoshi + Noto Sans Thai fonts
3. Sidebar 232px gradient navy
4. Shell-bar 52px white background
5. Lucide icons only
6. Page header pattern (.ph)
7. Breadcrumb in shell-bar
8. Stats/KPI optional
9. Filter bar in card
10. Table footer with pagination
11. Drawer width standards (540/680px, modal 440px)
12. Drawer slide animation 280ms
13. Drawer 4 zones
14. **Modal for confirmation ONLY** — drawer for create/edit
15. 3 close methods (backdrop/X/Esc)
16. Table ≤ 8 columns visible
17. Responsive form grid
18. Form field structure
19. Hide number input spinner
20. Toggle: div onclick + transform
21. **Icon class audit:** All `<i data-lucide>` have `w-{N} h-{N}`
22. Wizard full-height flex
23. **No color emoji** anywhere
24. No dev-tool bar in production
25. `renderIcons()` after every render (NOT `lucide.createIcons()` directly — see Iron Rule #25)
26. Lean catalog principle for registry UI

Full details: `knowledge/iron-rules.md`

---

## 🎯 Quick Start: Generate Simple List Page

```javascript
// 1. Read base files
const ciTokens = readFile('knowledge/ci-tokens.md');
const ironRules = readFile('knowledge/iron-rules.md');
const erpGuide = readFile('knowledge/erp-design-guide.md');

// 2. Read template
const skeleton = readFile('templates/file-skeleton.template.html');
const erpShell = readFile('templates/erp-shell.template.html');

// 3. Read pattern
const patternA = readFile('patterns/A_list-view.md');

// 4. Combine: skeleton + erp-shell + Pattern A content
// 5. Replace {{PLACEHOLDERS}} per feature
// 6. Audit Iron Rules
// 7. Save to outputs/
```

For full walkthrough: `examples/pipeline-mode-walkthrough.md`

---

## 📊 Source Attribution

| Source | Used For |
|---|---|
| `html-generator-25/SKILL.md` (v25) | Patterns E, F, G, H, I content; Iron Rules; structure logic |
| `core-marketing-prospect.html` (reference) | CSS skeleton; design tokens; sidebar/shell-bar/drawer/modal patterns; Pattern A & C |
| **NEW** (this refactor) | Modular split; Pattern B drawer-slide-in override; conflict/gap protocols |

---

## ✅ Next Steps

1. Review files (especially Pattern B drawer-slide-in approach)
2. Update `SKILL.md` to reference these new file paths
3. Test with sample input (use F-01 Prospect from `examples/pipeline-mode-walkthrough.md`)
4. Verify Iron Rules audit on output

---

**Total:** 20 files · 6,495 lines · 276 KB
**Status:** ✅ Ready for review and integration into `/mnt/skills/user/html-generator-v7/`
