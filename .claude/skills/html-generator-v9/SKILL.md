---
name: html-generator-v9
description: >
  สร้าง Production-Ready HTML Prototype มาตรฐาน 2BSimple จาก input อะไรก็ได้ (FRD Pack / Brief / BRD /
  PREBRIEF / screenshot / ข้อความ) — CI CUBE Warm Light, Satoshi + Noto Sans Thai, vanilla JS single-file SPA.
  ★ v9 แทน v8/v7/v6: Pattern Q Transaction Document Archetype ล็อกทุกเอกสาร PR/PO/QT/SO/GRN/INV/CN
  (list + wizard 5 steps + view tabs รายละเอียด›PDF›ลายเซ็น›ประวัติ + เอกสารแนบใน landing) · B2 v2 Line Editor
  re-locked กับ SO (grid compact, VAT segmented, ส่วนลด, totals) · Pattern P Planner/Scheduler ·
  Iron Rules #98–#105 (doc archetype, combobox anatomy คน/สินค้า, lean list ไม่ซ้อนคอลัมน์, layout นิ่ง, ★ v9.1 compact form/placeholder/lean cell + z-index registry).
  ใช้เมื่อ user พูดถึง "สร้าง HTML", "HTML prototype/mockup", "html-generator", "html-generator-v9/v8/v7",
  "line editor", "รายการสินค้า", "เอกสารธุรกรรม PR PO SO", "search dropdown", "sidebar shell", "planner".
---

# HTML Generator v9.0 — CUBE Warm Light · Document Archetype Edition

> **v9.0 (2026-08-25) = v8 ทั้งหมด + ล็อก "แบบประกอบ" ของเอกสารธุรกรรม + Planner pattern (จากไฟล์ที่ user craft/vibe แล้ว)**
> - **Pattern Q — Transaction Document Archetype ⭐ (BREAKING):** ทุก feature ที่ออกเอกสาร (PR/PO/QT/SO/GRN/INV/CN/DN/RTV)
>   ต้องใช้โครงเดียวกันเป๊ะ — list (สถานะเอกสาร + ลายเซ็น n/N) · create wizard **5 steps ชื่อล็อก** · view drawer
>   **tabs ล็อก** รายละเอียด › [domain] › PDF Preview › ลายเซ็น/อนุมัติ › ประวัติ · **เอกสารแนบ = section ใน landing tab** ·
>   DOA submit = slot picker เลือกคน (มติ 2026-08-17) — canonical `references/document-archetype/_SOURCE_so-reference.html`
> - **B2 v2 — Line Editor re-locked (BREAKING):** canonical ย้ายจาก PR reference → SO reference: grid compact `.line-tbl`
>   (26/—/64/92/92/78/72/104/54) · lean 1-line advanced row (VAT segmented ไม่คิด/บวกเพิ่ม/NET · % · หมายเหตุ · ราคาระบบ/ใช้ราคาระบบ) ·
>   free-row ของแถม · discount engine (บรรทัด %/฿ + ท้ายบิล segmented ฿/% + คูปอง) · totals 8 บรรทัด · `updateLine` focus-preserve —
>   **การกรอก item · ส่วนลด · VAT เหมือนกันทุกเอกสารในอนาคต**
> - **Pattern P — Day Planner / Team Scheduler:** ปฏิทินเดือน + day Gantt/log + build page (pool DnD → plan · capacity · AI plan) +
>   ชั้นทีม (`.wk-table` คน×7วัน · `.mbar`) — reference `references/planner/`
> - **Iron Rules #98–#101** (ดู `knowledge/iron-rules.md` Group 20) + audit.sh ตรวจ doc-archetype
> - ชื่อ CSS var / kit / rules #1-#97 คงเดิมจาก v8 ทั้งหมด (backward-compat)

> **v6.0 (2026-07-09) = v4 base ทั้งหมด + CUBE CI Rebrand + Pattern N Sidebar Shell รวมเป็นตัวเดียว**
> - **CI ใหม่ (CUBE Design System — Warm Light):** Ivory `#FAF8F5` ground · White cards · Charcoal `#111111` text/sidebar (flat, ไม่มี gradient) · **Red `#FF3B30` = action/priority** · **Orange `#FF9A1F` = connection** · Satoshi + Noto Sans Thai (Fontshare + Google Fonts) — ชื่อ CSS var คงเดิมจาก v4 (`--c-navy`=Charcoal, `--c-primary`=Red, `--c-teal`=Orange) เพื่อ backward-compat
> - **Pattern N — Sidebar Navigation Shell:** เมนู 3 ระดับ (Module›Group›Feature) · 2 โหมด (กางเต็ม 244px / icon rail 58px + slide panel) · Red สงวนให้ active เท่านั้น · ผ่าน Playwright 35 เคส · reference: `references/sidebar-shell/core-shell-ultimate.html`
> - **Iron Rule #49 — Minimal Scrollbar:** 5px มุมมน track โปร่งใส · ขาวโปร่งบนพื้นเข้ม / charcoal จางบนพื้นสว่าง · audit = FAIL ถ้าใช้ default
> - Base เดิมจาก v4.0: 48 rules + Unified Drawer v2 (920/680) + Fixed Tokens + microcopy.md + patterns A-M ครบ

<details>
<summary>รายละเอียด base v4.0 (Iron Rules #44-#48)</summary>

> - **Unified Drawer v2** — 920px/.standard 680 เป็นค่าเดียวทั้ง skill (ลบ 540px legacy ออกจาก ci-tokens + skeleton + rules)
> - **Fixed Tokens** — type scale / spacing / radius เป็นค่าตายตัว + CSS vars (`--fs-* --sp-* --r-*`) ใน :root — ห้ามใช้ช่วง/ตัวเลขลอย
> - **#44 Loading/Submitting** — ปุ่ม submit disabled+loader+label "กำลัง…" กัน double-submit
> - **#45 Disabled/Read-only + Form Section Grouping** — ฟอร์ม >6 fields แบ่งกลุ่มหัว caption
> - **#46 Placement Contract ⭐** — ปุ่มสร้าง=`.ph-actions` ขวาสุด · drawer primary=ล่างขวาชิด · badge หลังชื่อ 8px · แก้ไข→ลบ ลำดับตายตัว · ลบผ่าน confirm เสมอ
> - **#47 Stepper Standard** — `.stepper` component กลางจาก skeleton (2-5 steps) ห้ามออกแบบเอง
> - **#48 Landing Standard** — M1 Hero+Tiles / M2 Workspace / M3 KPI Home เท่านั้น
> - **microcopy.md** — คำมาตรฐานปุ่ม/toast/confirm/empty + Status Pill Vocabulary กลาง (สถานะเดียว=สีเดียวทุกไฟล์)
> - **Patterns:** J Dashboard (KPI+SVG chart) · K Report/Print · L Card-grid/Kanban/Timeline · M Landing (G ยุบเป็น alias ของ C)

</details>


### Version History (สรุป — รายละเอียดเต็มอยู่ใน git/README)
| Ver | สาระสำคัญ |
|---|---|
| **v9.1** | ⭐ **Compact Form + Lean Cell + Kit fixes** (จาก Tenant Master / Plan & Package vibe 2026-09-16) — **#104** compact form spacing · ไม่จอง error · placeholder `--c-placeholder` · `label.chk` · ⓘ ชิดซ้าย/is-below · combobox blur ก่อน render · **#105** 1 เซลล์ = 1 บรรทัด (`.nw`) · **kit: Z-Index Registry #62 ประกาศจริงใน `:root` (เดิมหาย)** · `.ph` wrap fix — ดู `CHANGELOG-v9.1.md` |
| **v9.0** | ⭐⭐ **Document Archetype release — แทน html-generator-v8** (จาก f-sales-order.html + op-action-plan.html + team-plan.html ที่ user craft แล้ว, 2026-08-25) — **Pattern Q** โครงเอกสารธุรกรรมล็อก 4 surface (list / wizard 5 steps / view tabs / PDF+sign+modals) · **B2 v2** line editor re-locked กับ SO (grid compact + lean advanced row + discount engine + totals order) · **Pattern P** planner/scheduler · **#98 Document Archetype Lock · #99 Line Editor v2 Lock · #100 Wizard Step Contract · #101 View Tab Contract** · audit `doc_archetype` checks — ดู `CHANGELOG-v9.0.md` |
| **v8.0** | ⭐⭐ **Consolidated release — แทน html-generator-v7** (รวม field feedback 2026-08-09 เป็น major) — **#95 Overlay Portal (BREAKING)** root cause "dropdown จม" = ancestor overflow clip ไม่ใช่ z-index → เมนูใน scroll container (.table-wrap/drawer body/B2 grid) ต้อง `portalMenu()` ไป `#overlay-root` position:fixed (util + `.menu-fixed` ใน skeleton BASE-KIT) · **#94.1 Cascade Clear** clear combobox → field autofill ตามต้องเคลียร์ครบ + confirm ก่อนล้าง line items · **#96 List Full-Height** `.page-fill` + `.table-wrap` flex:1 scroll ภายใน + thead sticky + `.table-foot` ติดล่าง — ตารางชิดขอบล่าง viewport เสมอ · **#97 Responsive Desktop-Base (BREAKING — แทน doctrine desktop-only)** ≥1180 เต็ม · 768–1180 adaptive (sidebar off-canvas/rail + `.nav-toggle`, drawer `min(กว้างเดิม,100vw)`, content padding 16) · <768 ไม่ guarantee · `body min-width:768` · Render Gate เพิ่ม viewport 1024 · **#67.1 Hint Opt-in** default ไม่ gen hint/ⓘ เลย — มีได้เฉพาะ FRD ระบุ explicit · **#47.1 Stepper Geometry Lock** `flex:1 1 0` เท่ากันเป๊ะ + connector กึ่งกลาง dot + dot ขนาดเดียว + CSS จาก kit verbatim + Render Gate วัดจริง · self-check #20–24 · doctrine sync (erp-design-guide, Rule #30, Checklist F) — ดู `CHANGELOG-v8.0.md` |
| **v7.0** | ⭐⭐ **Consolidated release — แทน html-generator-v6.** Pattern B2 — Document Line Editor (สกัด verbatim จาก F-PR-001, CI Warm Light): grid 8 คอลัมน์ locked · VAT engine 3 โหมด (`calcLineVat`+`migrateLine`) · multi-UoM cascade (`units[]`+`setLineUnit`) · totals 6 บรรทัด (ฐาน WHT = ก่อน VAT) · hard control hook (disable ปุ่มจริง) · `.drawer-panel.wide` 1290px = ข้อยกเว้นเดียวของ Rule #11 · เพิ่ม keyboard nav + drop-up ให้ item combobox (ปิด gap OQ-B2-01) + **Iron Rule #94 Master-Backed Field = Search Combobox เสมอ** (canonical: `master-combobox.js.txt`) + QC Rules #83–#92 ใน component-contracts |
| **v6.1** | ⭐ Field fixes จาก build จริง (Checklist Test Run) — (1) skeleton: เพิ่ม `.hidden{display:none!important}` (root cause: search-select list เปิดค้าง + ปุ่ม X โผล่ เพราะ JS toggle class ที่ CSS ไม่มี) · (2) `hashchange` เป็น late-binding `function(){render()}` (เดิม capture placeholder ทำให้ render ของ feature ไม่ถูกเรียกตอนเปลี่ยน route) · (3) skeleton ships Pattern B drawer chrome (`.dw-head/.dw-eyebrow/.dw-title/.d-stepper/.stepper-item 32px/.dw-footer/.top-icon-btn`) — create/edit ใช้ชุดนี้แทน `.drawer-header`+avatar และ `.drawer-stepper-band` · (4) Pattern O ใหม่ — Split-Pane Runner (navigator ซ้าย 300px sticky + execution ขวา + step checklist มีหัวตาราง grid ตรงกัน) · (5) reword comment ที่ audit จับ Rule #25 false-positive |
| **v6.0** | ⭐ Consolidated release — v4 base + CUBE CI Rebrand (Warm Light: Ivory/Charcoal/Red/Orange, Satoshi) + Pattern N Sidebar Shell + Rule #49 Minimal Scrollbar รวมเป็น skill เดียว แทนที่ html-generator-v4 |
| **v4.2** | ⭐ Pattern N — Sidebar Navigation Shell (3-level accordion Module›Group›Feature + icon rail 58px + slide panel + ⌘K, จาก core-shell-ultimate ที่ผ่าน Playwright 35 เคส) rebrand เป็น CI ใหม่ + Iron Rule #49 Minimal Scrollbar (5px, track โปร่งใส, ขาวโปร่งบนพื้นเข้ม/charcoal จางบนพื้นสว่าง — ห้าม default scrollbar, audit FAIL) |
| v4.1 | ⭐ CUBE CI Rebrand — Warm Light theme: Ivory bg + Charcoal text + Red #FF3B30 (action) + Orange #FF9A1F (connection), Satoshi replaces Inter, sidebar flat charcoal (no gradient), status tints ใหม่ทั้งชุด — ชื่อ CSS var คงเดิม (--c-navy=Charcoal, --c-primary=Red, --c-teal=Orange) |
| v4.0 | Rebrand + One-Shot Policy (ไม่หยุดถาม, audit hard gate, Placement Cheat Sheet) |
| v3.13 | Rules #44-48: Loading · Disabled+FormSection · Placement Contract · Stepper · Landing + Unified Drawer v2 (920/680) + Fixed Tokens + microcopy.md + Patterns J/K/L/M |
| v3.12 | Rules #38-43: Thai Rhythm · Empty State · List Cell Atomicity · List Row=view · Long-list UX · Validation+Format · audit.sh |
| v3.11 | Rules #34-37: Search-Select · Layout Stability · Button Symmetry · Requirement Coverage |
| v3.10 | Create/Edit/View drawer = v2 shell, locked 100% to `references/drawer-standard/` (pr.html verbatim, 920px) |
| v3.9 | Rule #33 Hint = hover tooltip (ไม่ใช่ info-banner) |
| v3.8 | Rule #32 CSV Import convention (modal + template-in-modal + validate/confirm + Replace/Merge) |
| v3.7 | Rule #31 Drawer Button Contract (footer/header order + color=role + draft rule) |
| v3.6 | `references/design-system.html` living visual reference |
| v3.5 | Rule #30 Fluid Content (no max-width cap on `.content`) |
| v3.4 | Rule #29 Render Preservation (scroll + focus restore) |
| v3.3 | Rules #27-28 Module-Feature sidebar + Slim Top Bar |
| v3.2 | Lucide multi-CDN robustness, pinned 0.469.0 |
| v3.1 | Modular files + reference-driven CSS, drawer override, no Tailwind CDN |

---

## ⭐ DRAWER STANDARD v2 — READ FIRST (create / edit / view)

When generating **any** create, edit, or view drawer:
1. **Load** `references/drawer-standard/drawer.css.html` and include its tokens + classes.
2. **Follow** `patterns/B_create-edit-drawer-wizard.md` (create/edit) and
   `patterns/C_view-drawer-tabbed.md` (view) — reproduce structure/classes/inline-styles **exactly**.
3. **Copy** the JS verbatim from `create-edit-drawer.js.txt` / `view-drawer.js.txt` /
   `shared-helpers.js.txt`, adapting only fields, labels, entity names, and mock data.
4. **Place** the shell hooks `#overlay-root` + `#toast-root` before `</body>`.
5. The `_SOURCE_pr-reference.html` is the canonical, working example — diff against it.

v3.13: skeleton + ci-tokens + Rule #11 ถูก unify เป็น 920/.standard 680 แล้ว — ไม่มี 540px เหลือในระบบ (audit.sh จะ FAIL ถ้าเจอ)

---

## 🎯 Quick Decision Tree

```
User สั่ง "สร้าง HTML..."
    │
    ▼
[Phase 0] รับ Input
    │
    ├─ มี FRD Pack folder? (00_INDEX + 01_UI + ...)
    │     ├─ Yes → Pipeline Mode ⭐ (อ่าน references/pipeline-mode.md)
    │     │
    │     ├─ มี BRD + Brief (ไม่มี FRD)?  → Pipeline Mode partial
    │     │
    │     └─ No → Standalone Mode (อ่าน references/standalone-mode.md)
    │
    ▼
[Phase 1] Plan
    - Read knowledge/iron-rules.md` + `knowledge/layout-integrity.md (มาตรฐาน 43 ข้อ)
    - Read knowledge/ci-tokens.md (สี/font/spacing)
    - 🆕 Read knowledge/design-system-reference.md (route map ของ variants)
    - 🆕 View references/design-system.html (visual reference — ดู variant ที่จะใช้)
    - Decide: ERP shell vs General shell
    - ⭐ v9: เอกสารธุรกรรม? → Pattern Q ทั้งชุด (Rule #98) · มี line items → B2 v2
    - Map pages → patterns (A-Q) + matched variants from design system
    │
    ▼
[Phase 2] Build Skeleton (templates/file-skeleton.template.html + shell)
    │
    ▼
[Phase 3] Implement Pages (lazy-load patterns/{X}.md ที่ใช้)
    - 🆕 Copy structure จาก design-system.html variants ที่ matched
    - ไม่ต้อง "ออกแบบใหม่" — reference เป็น source of truth visual
    │
    ▼
[Phase 4] Implement Behavior (JS — state, routing, drawer, toast)
    │
    ▼
[Phase 5] Mechanical Verification (9 checks A-I — ตาม knowledge/iron-rules.md)
    │
    ▼
[Phase 6] Deliver (present_files + summary)
```

---

## 📌 Placement Cheat Sheet (Rule #46 ย่อ — แปะไว้กันหลุดตอน generate)

| ของ | ตำแหน่งตายตัว |
|---|---|
| ปุ่มสร้าง | `.ph-actions` ขวาสุด (primary เดียว) — secondary เรียงซ้าย |
| ปุ่ม primary ใน drawer | footer ล่างขวาสุดชิดขวา (sticky) — ยกเลิก ghost ซ้ายสุด |
| Status pill | หลังชื่อ ห่าง 8px (list = คอลัมน์ตัวเอง / card = มุมขวาบน) — pill เดียวระดับ header |
| แก้ไข/ลบ ใน list row | คอลัมน์ขวาสุด: pencil → trash-2 (>3 actions = ⋮) |
| แก้ไข/ลบ ใน drawer | view header: secondary→primary→danger→\|→X · edit ไม่มีปุ่มลบ · ลบ = confirm modal เสมอ |
| Search / Reset filter | ซ้ายสุด / ขวาสุด ของ filter bar (filter อยู่ใน card) |
| Toast | ขวาล่าง auto-dismiss 3.5s — หลังปิด drawer เท่านั้น |
| Stepper | drawer = `.drawer-stepper-band` ใต้ header / page = `.wizard-stepper-band` |
| Pagination / count | ซ้าย / ขวา ของ table footer |

---

## 📌 Always-On Reminders (v9 — จาก feedback user 2026-08-25 · ทุกไฟล์ ทุก pattern)

| หลัก | สิ่งที่ต้องทำ | กฎ |
|---|---|---|
| **Search dropdown ทุกที่ที่เป็นไปได้** | field ใดอ้างข้อมูลที่มีรายการ (คน/สินค้า/ลูกค้า/คู่ค้า/แผนก/คลัง/โครงการ/เอกสารต้นทาง…) = **search combobox** ไม่ใช่ `<select>` — เว้นแต่ enum ตายตัว ≤7 ค่า | #94, #102 |
| **Option anatomy เหมือนกันทุก dropdown** | **คน** = avatar/`user` icon → ชื่อ (บรรทัด 1) → ตำแหน่ง · แผนก (บรรทัด 2) · **สินค้า** = `package` icon → code · หมวด (บรรทัด 1 mono) → ชื่อ (บรรทัด 2) → ราคา/หน่วย + สต๊อก (ขวา) · **องค์กร/อื่น** = icon ประเภท → ชื่อ → code · meta · ลำดับห้ามสลับ | #102 |
| **หน้าจอนิ่ง ไม่เบี้ยว** | dropdown/popover ลอยทับ (portal) ไม่ดันเนื้อหา · `scrollbar-gutter:stable` · ตารางกว้าง scroll ใน wrap · render แล้วคืน scroll/focus · ความสูงแถว/ปุ่มคงที่ | #29, #35, #36, #95 |
| **ข้อมูล lean** | แสดงเฉพาะที่ตัดสินใจได้ · ข้อมูลรองไป `title`/บรรทัดรอง/drawer · ไม่มี hint เปลือย · ไม่มีศัพท์ภายใน | #67.1, #81, #103 |
| **List view ห้ามซ้อนข้อมูล** | **1 ข้อมูล = 1 คอลัมน์** — คนละตัว (สถานะเอกสาร / จัดส่ง / การจ่าย / ลายเซ็น / ยอด) แยกคอลัมน์ ห้ามยัดรวมใน cell เดียว · ★ v9.1: **1 เซลล์ = 1 บรรทัด** — ไม่มี user-cell avatar+ชื่อ+code ใน list (แยกคอลัมน์ รหัส · ชื่อ) · td ชื่อ/รหัส/วันที่ ใส่ `.nw` | #40, #103, #105 |
| **ฟอร์ม compact** | section ห่าง 16 · field ห่าง 12 · ไม่จองพื้นที่ error (โผล่เฉพาะ invalid) · placeholder `#B4B6BC` · ตัวเลือกที่ต้องอธิบาย = การ์ดเลือก (`.track-card`) · เลือกแล้วมีการ์ดสรุป · รายการย่อยเป็นตารางมีหัว · checkbox+ข้อความ = `label.chk` | #104 |

## 📥 Input Modes

### Mode 1: Pipeline Mode ⭐ (Recommended)

**Input:** FRD Pack folder + BRD + Brief
**Read priority:**
| Source | Used for | Priority |
|---|---|---|
| **FRD Pack `01_UI.md`** | Pages, layout patterns, journeys, components | 🥇 PRIMARY |
| **FRD Pack `02_API.md`** | API calls in actions, mock data shape | 🥈 |
| **FRD Pack `05_RULES.md`** | Validation rules, status transitions | 🥈 |
| **FRD Pack `06_TESTS.md`** | Scenarios for behavior | 🥉 |
| **BRD `§14.6` Functions Cut** | Scope lock (IN/OUT for this iteration) | 🛡️ |
| **Brief `§3.4` Generator Hints** | complexity, has-state hints | reference |
| **Iron Rules** (knowledge/iron-rules.md) | Always overrides above sources | 🔒 SUPREME |

→ Detail flow: see `references/pipeline-mode.md`
→ Conflict procedure: see `references/conflict-resolution.md`

### Mode 2: Standalone Mode (Fallback)

**Input:** Any text, idea, screenshot, partial spec
**Behavior:** Infer best-practice ERP feature pattern + fill gaps with defaults
→ Detail flow: see `references/standalone-mode.md`
→ Gap handling: see `references/gap-detection.md`

### Mode 3: Legacy Pipeline (RIF + BRD + FRD v2.8)

**Input:** RIF + old-format FRD + BRD
**Use when:** Project still on v2.8 FRD format (not yet migrated to v4 Pack)
→ Behavior: same as Pipeline Mode but reads RIF instead of Brief

---

## 📋 Phase 0 — Detect Input + Auto-Configure

### Step 0.1 — Identify ERP vs General

**Auto-detect from input:**
- BRD §14.6 mentions "Sidebar Menu Entry" → **ERP**
- FRD 01_UI.md mentions Module/Breadcrumb context → **ERP**
- Standalone input with "internal tool", "admin panel", "module" → **ERP**
- Otherwise → **General** (single-page feature, marketing, public-facing)

**If unclear → ONE-SHOT default = ERP** (บริบทงาน CUBE ส่วนใหญ่เป็น ERP shell) — เลือก ERP ไปเลย
แล้ว log ใน summary: `Assumption: ERP shell (input ไม่ระบุ)` — ถามเฉพาะกรณี input ชี้ชัดว่าเป็น
public/marketing page แต่ขัดกับบริบทอื่น (rare)

### Step 0.2 — Identify Pack Input

**Auto-detect:**
- มี folder ชื่อ `FRD_F-XX_Pack/` → Pipeline Mode (v4 Pack)
- มีไฟล์ `FRD_*.md` (single file) → Pipeline Mode (legacy v2.8)
- มีไฟล์ Brief `F-XX_*.md` → Pipeline Mode (partial — Brief only)
- ไม่มีไฟล์ใดๆ → Standalone Mode

### Step 0.3 — Mandatory Knowledge Read

ก่อนเข้า Phase 1 ทุกครั้ง — `view`:
```
1. knowledge/iron-rules.md       (49 rules — บังคับใช้ทั้งหมด)
2. knowledge/ci-tokens.md        (token ตายตัว: สี, type scale, spacing, radius, icon size)
3. knowledge/component-catalog-ref.md  (canonical component names)
4. knowledge/microcopy.md        (คำมาตรฐานปุ่ม/toast/confirm/empty + status pill mapping)
```

**ถ้า ERP** → เพิ่ม:
```
5. knowledge/erp-design-guide.md  (Sidebar 232px / Shell-bar 52px white / Breadcrumb / .ph)
```

---

## 📋 Phase 1 — Plan

### Step 1.0 — Requirement Coverage Map (Iron Rule #37) ⭐

อ่าน input **ทั้งหมด** ให้ละเอียดก่อน (FRD Pack 01_UI/02_API/05_RULES + Brief + screenshot + ข้อความ) แล้วสกัดเป็น checklist เดียวที่จะใช้ verify ตอนจบ — **ห้ามข้ามขั้นนี้** เพราะเป็นที่มาของ "ตกหล่น requirement":

```markdown
## Coverage Map — [feature]
| ประเภท | รายการที่ FRD/req ระบุ | จะทำ? | หมายเหตุ |
|---|---|---|---|
| Field | [field + type + required + validation] | ✅ | |
| Action | [create/edit/view/delete/approve/export/import/...] | ✅ | wire จริง |
| Status | [draft→submitted→approved...] | ✅ | |
| Validation | [rule จาก 05_RULES] | ✅ | |
| Route | [#/route จาก 01_UI] | ✅ | refresh-safe |
| Column | [คอลัมน์ใน list] | ✅ | ≤8 |
| CUT | [อยู่ใน BRD §14.6 Functions Cut] | ❌ | ไม่ทำ (log) |
```

ทุกแถวต้องลงเอยเป็น ✅ (ทำ) หรือ ❌ + เหตุผล (CUT / defer). **ไม่มีแถวที่เงียบหาย.** ใช้ map นี้ซ้ำใน Phase 5 Check I.

### Step 1.1 — Extract Page Inventory

**Pipeline Mode:**
- Read FRD Pack `01_UI.md` → Routes table → list pages
- Read BRD `§14.6` → confirm Functions Cut (drop features in CUT list)

**Standalone Mode:**
- Infer pages from input (typical ERP: list → drawer create → drawer view → modal delete)

### Step 1.2 — Map Page → Pattern (A-O)

| Page Type | Pattern | File |
|---|---|---|
| List/table with filter | A | `patterns/A_list-view.md` |
| **Create/Edit (single OR multi-step)** | **B (v2 drawer wizard — locked to pr.html)** | `patterns/B_create-edit-drawer-wizard.md` |
| **⭐ เอกสารธุรกรรม (มีเลขที่+สถานะ+อนุมัติ+PDF: PR/PO/QT/SO/GRN/INV/CN/DN/RTV/RV)** | **Q (แบบประกอบ — locked to SO reference) — อ่านก่อน B/B2/C/H/I** | `patterns/Q_transaction-document-archetype.md` |
| **รายการสินค้า/บริการ + ยอดรวม (step 3 ของ Q)** | **B2 v2 (locked to line-editor-v2)** | `patterns/B2_document-line-editor.md` |
| Detail/document view with tabs | **C (v2 view drawer — locked to pr.html)** | `patterns/C_view-drawer-tabbed.md` |
| **Confirmation dialog (delete/archive/logout)** | **D (modal only)** | `patterns/D_modal-confirmation.md` |
| Compact table with expandable row | E | `patterns/E_compact-table-expandable.md` |
| Toggle + sub-config section | F | `patterns/F_configurable-modifier.md` |
| PO-style view drawer (with PDF) — **alias of C** | G | `patterns/G_po-style-view-drawer.md` |
| A4 PDF preview | H | `patterns/H_a4-paper-pdf-preview.md` |
| Signature card list | I | `patterns/I_signature-card-list.md` |
| **Dashboard (KPI + chart)** | **J** | `patterns/J_dashboard-kpi-chart.md` |
| **Informative report (screen+print)** | **K** | `patterns/K_report-print.md` |
| Card grid / Kanban / Timeline | L | `patterns/L_collection-views.md` |
| **Landing / Home page** | **M** | `patterns/M_landing-home.md` |
| **Sidebar nav 3 ระดับ (Module›Group›Feature) / icon rail / เมนูย่อได้** | **N** | `patterns/N_sidebar-nav-shell.md` |
| **Runner / checklist execution (list ซ้าย + ทำงานขวา, ติ๊กผลรายขั้น)** | **O** | `patterns/O_split-pane-runner.md` |
| **Planner / Scheduler (คลังงาน → วางลงวัน · ปฏิทินเดือน · Gantt วัน · โควตา · ทีม)** | **P** | `patterns/P_day-planner-scheduler.md` |

**Lazy-load:** อ่านเฉพาะ pattern ที่ feature ใช้จริง (ไม่ใช่ทั้ง 17)

### ⭐ Document Archetype Override (v9 — CRITICAL)

**Iron Rule #98:** feature ที่เข้าข่าย "เอกสารธุรกรรม" (มีเลขที่เอกสาร + สถานะ + ลายเซ็น/อนุมัติ + PDF) → **ใช้ Pattern Q ทั้งชุด** ไม่ว่า FRD/PREBRIEF จะวาดโครงอย่างไร — ถ้า FRD ระบุ tab/step ต่างออกไป → silent override + log ใน `Iron Rule Overrides Applied` (เนื้อหา business ยังตาม FRD · **โครง/ลำดับ/ชื่อ** ตาม Q)

ลำดับอ่านสำหรับ feature เอกสาร: `Q` → `B2` → `references/document-archetype/*.js.txt` (ลอก verbatim) → `doc-archetype.css.html`

### ⚠️ Pattern B Override (CRITICAL)

**Iron Rule #14 enforces:** Create/Edit always uses **drawer slide-in (920px v2)**, NEVER modal.

ถ้า FRD spec บอกใช้ modal สำหรับ create → **silent override** เป็น drawer + log:
```markdown
## Iron Rule Overrides Applied
- Iron Rule #14: FRD specified modal for Create; applied drawer slide-in (Pattern B) per CI policy.
```

**ถ้า feature มี line items → ต้องอ่าน `patterns/B2_document-line-editor.md` (v2) ต่อทันที** ห้ามออกแบบตารางกรอกรายการเอง — canonical = `references/document-archetype/line-editor-v2.js.txt` (ไม่ใช่ `drawer-standard/line-editor.js.txt` ของ v8 อีกต่อไป)

**Rule #94 (BREAKING):** ทุก field ที่อ้าง master (product/customer/vendor/employee/dept/branch/BR/project/GL...) ต้องเป็น **search combobox pattern เดียวกันเสมอ** — verbatim source: `references/drawer-standard/master-combobox.js.txt` (ดู iron-rules Group 18)

Modal (Pattern D) ใช้เฉพาะ:
- Delete confirmation
- Archive confirmation
- Logout confirmation
- Simple 1-3 field form (rare case — invite by email, send simple message)

### Step 1.3 — Plan Summary (show to user before Phase 2)

```markdown
📋 Plan Summary

**Mode:** Pipeline (FRD Pack) / Standalone
**Shell:** ERP (Sidebar 232px + Shell-bar 52px white)
**Pages (N):**
| Route | Title | Pattern | Width |
|---|---|---|---|
| #/list | [Title] | A list-view | full |
| #/list (create) | [Title] | B v2 drawer wizard | 920px (.standard=680) |
| #/list (view) | [Title] | C v2 view drawer | 920px |
| #/list (delete) | [Title] | D modal | 440px |

**Patterns to load:** A, B, C, D
**Iron rules applied:** 48 (all mandatory)
**CI Tokens:** CUBE Charcoal/Red/Orange (Warm Light theme — v2.0 rebrand)
**Functions Cut (BRD §14.6):** [list — NOT implemented]
```

**ONE-SHOT POLICY ⭐ — แสดง Plan Summary แล้ว "ดำเนินการต่อทันที" ไม่ต้องรอ user ตอบ**
- หยุดถามได้กรณีเดียว: requirement ขัดแย้งกันเองร้ายแรงจน generate ไม่ได้ (เช่น 2 เอกสารสั่ง flow ตรงข้าม)
- ทุกความไม่ชัด → ตัดสินด้วย default ตาม gap-detection.md + log ใน `Gaps Filled / Assumptions` ท้าย summary
- เป้าหมาย: user เปิดไฟล์แล้วใช้ได้เลย — ไม่ต้องตอบคำถามกลางทาง ไม่ต้องนั่งไล่แก้

---

## 📋 Phase 2 — Build HTML Structure

### Step 2.1 — File Skeleton

`view templates/file-skeleton.template.html` → use as base. Contains:
- Google Fonts (Satoshi + Noto Sans Thai)
- Lucide CDN
- CUBE `:root` CSS variables (v2.0 rebrand values)
- Full CSS for all components (sidebar / shell-bar / drawer / modal / table / etc.)
- Self-contained utility classes (`.w-3 .h-3 .w-4 .h-4 .w-5 .h-5` etc. — no Tailwind CDN needed)
- Number input spinner hide (Iron Rule #19)
- Line-expand animation (Pattern E)
- Wizard layout (Iron Rule #22)
- State + router + drawer/modal/toast handlers skeleton

### Step 2.2 — App Shell

| Mode | Template |
|---|---|
| ERP | `view templates/erp-shell.template.html` (sidebar + breadcrumb + shell-bar) |
| General | `view templates/general-shell.template.html` (no sidebar — for marketing/public) |

---

## 📋 Phase 3 — Implement Pages

**Per page:**
1. `view patterns/{X}.md` for the pattern needed
2. Copy zone-by-zone HTML structure
3. Bind data from FRD Pack (or mock data for Standalone)
4. Wire actions to JS functions (from Phase 4)

**Iron Rules to enforce during Phase 3:**
- #5 Lucide icons only (no color emoji)
- #14 **Create/Edit = drawer slide-in (NOT modal)** ⭐
- #16 List tables ≤ 8 columns
- #18 Form field structure (label / input / help / error)
- #21 Icon class audit (every `<i data-lucide>` has `w-{N} h-{N}`)
- #22 Full-height wizard layout (when applicable)

→ Full rules: `knowledge/iron-rules.md`

---

## 📋 Phase 4 — Implement Behavior (JavaScript)

### Step 4.1 — State + Mock Data

**Pipeline Mode:** generate mock data from FRD 04_DB.md schema (fields + types + statuses)
**Standalone Mode:** generate plausible Thai mock (15-25 records, 3-4 statuses)

```javascript
const state = {
  currentRoute: 'home',
  drawer: { open: false, mode: null, recordId: null, step: 1, tab: 'overview' },
  modal: { open: false, type: null, data: null },
  toast: { visible: false, message: '', variant: 'info' },
  filters: { search: '', status: 'all' },
  pagination: { page: 1, pageSize: 20 },
  sort: { col: null, dir: 'asc' },
  selectedIds: new Set(),
  records: [],
};
```

### Step 4.2 — Hash Routing (refresh-safe SPA)

```javascript
function getRoute() {
  const hash = location.hash;
  if (!hash || hash === '#' || hash === '#/') return 'home';
  return hash.replace(/^#\//, '');
}
function navigate(route) { location.hash = '#/' + route; }
window.addEventListener('hashchange', render);
window.addEventListener('DOMContentLoaded', render);
```

### Step 4.3 — Drawer/Modal Toggle (per pattern)

→ See JS helpers in each pattern file:
- Drawer open/close + slide animation: `patterns/B_create-edit-drawer-wizard.md`
- Modal open/close + scale animation: `patterns/D_modal-confirmation.md`
- Esc key handler: included in `templates/file-skeleton.template.html`

### Step 4.4 — Toast / Filter / Pagination / Sort

Standard helpers (copy from `patterns/A_list-view.md` JS Helpers section):
- `getFilteredRecords()`, `getPaginated()`, `sortBy()`, `toggleSelect()`, `goToPage()`, `resetFilters()`
- `initials()`, `formatDate()`, `formatDateTime()`, `showToast()`, `statusLabel()`

---

## 📋 Phase 5 — Mechanical Verification

**Run all 9 checks before deliver — write report in chat (not in HTML):**

> **⚙️ HARD GATE (v4): `bash scripts/audit.sh <file.html>` ต้อง exit 0 (FAIL=0) ก่อน deliver เท่านั้น — เจอ FAIL → แก้แล้วรันซ้ำจนผ่าน ห้ามส่งงานพร้อม FAIL.** WARN ให้ไล่เก็บถ้าแก้ได้ในไฟล์เดียว. จับ banned patterns อัตโนมัติ (line-height:1 บนปุ่ม, eye icon, .content max-width, createIcons ตรง ๆ, ฯลฯ). **สำหรับ visual rules (Thai rhythm #38 / button #36 / empty #39 / sticky #42)** — `python3 scripts/render-check.py <file.html>` แล้ว**ดูภาพจริง** (บทเรียน: อ่าน CSS แล้วเดาไม่พอ — ไทยลอยสูง/ปุ่มเบี้ยวเห็นเฉพาะตอน render ด้วยฟอนต์ไทย).

```markdown
## 🔍 Phase 5 Verification — [feature_name].html

### A. Production-Ready Check
- [ ] No dev-tool bar / page selector / debug panel ✅/❌
- [ ] No console.log ✅/❌
- [ ] No TODO comments ✅/❌
- [ ] Single file (HTML+CSS+JS inline) ✅/❌
- [ ] CDN imports working (Google Fonts + Lucide) ✅/❌

### B. Routing Check
- [ ] Hash routing (#/route) ✅/❌
- [ ] Refresh-safe ✅/❌
- [ ] hashchange + DOMContentLoaded listeners ✅/❌

### C. ERP Compliance (if ERP)
- [ ] Sidebar 232px + gradient navy ✅/❌
- [ ] Shell-bar 52px WHITE (not navy) ✅/❌
- [ ] Breadcrumb in shell-bar (chevron-right separator, NEVER `›` text) ✅/❌
- [ ] Satoshi + Noto Sans Thai loaded ✅/❌
- [ ] CSS variables used (Charcoal #111111, Red #FF3B30, Orange #FF9A1F) ✅/❌
- [ ] Page Header (.ph) with h1 + subtitle + actions ✅/❌
- [ ] **Sidebar uses Module/Feature pattern** — `.sb-module` + `.sb-module-header` button + `.sb-features`, NO `.sb-section`/`.sb-section-title` ✅/❌
- [ ] **Every module has `data-module="<id>"`; every feature has `data-feature="<id>"`** ✅/❌
- [ ] **Module header is non-navigable** — `<button onclick="toggleModule(this)">`, NOT `<a>` ✅/❌
- [ ] **Slim Top Bar** — only Breadcrumb + Notification + User Chip; NO Help button, NO Search button, NO extras ✅/❌
- [ ] **Fluid Content** — `.content` ไม่มี `max-width` cap (stretch เต็ม viewport on wide monitors) ✅/❌

### D. Component Compliance
- [ ] Create/edit/view drawer = v2 shell (overlay-wrap → backdrop + drawer-panel), 920px wide (.standard=680) — locked to pr.html ✅/❌
- [ ] Modal 440px max-width ✅/❌
- [ ] Drawer slide animation 280ms cubic-bezier ✅/❌
- [ ] Backdrop opacity rgba(17,17,17,0.40) + click-to-close ✅/❌
- [ ] Esc key closes drawer/modal ✅/❌
- [ ] **Drawer Button Contract (Iron Rule #31):** Create/Edit footer order = `ยกเลิก (ghost)` left → spacer → `[บันทึกร่าง]` → `primary` right ✅/❌
- [ ] **View drawer footer = `ปิด` (btn-secondary) ONLY** — NOT btn-danger, NOT btn-primary ✅/❌
- [ ] **View drawer header actions** = secondary→primary→danger → `.drawer-header-divider` → icon-btn X (far right) ✅/❌
- [ ] **Button color = role** — ปุ่มปิด/กลับ ไม่เป็นสีแดง; danger เฉพาะ destructive; ไม่มี primary ซ้ำ 2 ปุ่ม ✅/❌
- [ ] **บันทึกร่าง present only if entity has draft state (Rule #31.5)** — consistent across all entities in file ✅/❌
- [ ] **Search-Select (Iron Rule #34):** dropdown ที่ options เยอะ/lookup master ใช้ `searchSelectHTML`+`initSearchSelect` (พิมพ์กรอง+ไฮไลต์+คีย์บอร์ด) — ไม่ใช่ `<select>` ยาว ✅/❌
- [ ] **Button Symmetry (Iron Rule #36):** ปุ่มแถวเดียวสูงเท่ากัน · label ไม่ตัดบรรทัด · icon ไม่ถูกบีบ · ปุ่มคู่สมมาตร (`.btn-eq` ถ้าจำเป็น) ✅/❌

### E. Behavior Check
- [ ] Search/filter/sort/pagination works ✅/❌
- [ ] Create drawer: full flow works (Iron Rule #14 — drawer not modal) ✅/❌
- [ ] Edit drawer: pre-populates fields ✅/❌
- [ ] renderIcons() called after every render() (NOT lucide.createIcons() directly) ✅/❌
- [ ] Toast appears + auto-dismisses ✅/❌
- [ ] **Render preservation (Iron Rule #29):** กดปุ่ม / toggle ใน drawer ที่ scroll ลงไปแล้ว → drawer **ไม่** เด้งกลับบน ✅/❌
- [ ] **Render preservation:** พิมพ์ใน input → click toggle อื่น → input ที่พิมพ์อยู่ **ยังคง** focus + cursor ตำแหน่งเดิม ✅/❌

### F. Responsive & Layout Stability Check
- [ ] Body has min-width: 768px (v7.1 desktop-base — Rule #97) ✅/❌
- [ ] Viewport 1024px: drawer = `min(กว้างเดิม,100vw)` ไม่ล้นจอ · sidebar off-canvas/rail · ไม่มี body h-scroll (#97) ✅/❌
- [ ] หน้า list ใช้ `.page-fill` — ตารางยืดชิดขอบล่าง viewport, scroll ใน `.table-wrap`, `.table-foot` ติดล่าง (#96) ✅/❌
- [ ] Drawer/modal scale properly on smaller widths ✅/❌
- [ ] **Layout Stability (Iron Rule #35):** เปิด dropdown/search-select → list **ลอยทับ** ไม่ดันเนื้อหาใต้มัน ✅/❌
- [ ] **Layout Stability:** เปิด modal/drawer หรือ content โต → หน้า **ไม่ขยับซ้าย-ขวา** (`scrollbar-gutter:stable`) ✅/❌
- [ ] **Layout Stability:** ตารางกว้างเกิน viewport อยู่ใน wrapper `overflow-x:auto` — ไม่ดันทั้งหน้าเบี้ยว ✅/❌

### G. Iron Rules #1-43 Compliance (from knowledge/iron-rules.md)
- [ ] #1-5 Brand/CI (tokens, fonts, sidebar, shell-bar, Lucide) ✅/❌
- [ ] #6-10 Layout (page header, breadcrumb, stats, filter-in-card, footer) ✅/❌
- [ ] #11-15 Drawer/Modal (widths, animation, structure, **create=drawer**, close methods) ✅/❌
- [ ] #16-20 Table/Forms (≤8 cols, grid, field structure, no spinner, toggle) ✅/❌
- [ ] #21-26 Code Quality (icon classes, wizard, no emoji, no dev-tool, createIcons, lean catalog) ✅/❌
- [ ] **#27 Sidebar = Module/Feature pattern (`.sb-module` collapsible + `data-module`/`data-feature`)** ✅/❌
- [ ] **#28 Slim Top Bar (Breadcrumb + Notif + User Chip only — no Help/Search/extras)** ✅/❌
- [ ] **#29 Render Preservation (`preserveRenderState()` + `restoreRenderState()` used in render(), OR render wrapped with `withRenderPreservation()`)** ✅/❌
- [ ] **#30 Fluid Content (`.content` ไม่มี `max-width` cap — content stretch เต็ม viewport)** ✅/❌
- [ ] **#31 Drawer Button Contract (footer order + role-color + view footer=ปิด secondary only + header actions order + draft rule 31.5)** ✅/❌
- [ ] **#34 Search-Select (options เยอะ/lookup master → searchable dropdown ผ่าน helper กลาง)** ✅/❌
- [ ] **#35 Layout Stability (scrollbar-gutter:stable + popover overlay + table overflow-x — ไม่เบี้ยว/ดัน/เด้ง)** ✅/❌
- [ ] **#36 Button Symmetry (justify-center + nowrap + icon flex-shrink:0 + ปุ่มแถวสูงเท่ากัน + `.btn-eq`)** ✅/❌
- [ ] **#37 Requirement Coverage (Coverage Map ครบ — field/action/status/validation/route; ของขาด/เติม log แล้ว)** ✅/❌
- [ ] **#44 Loading/Submitting (ปุ่ม submit → disabled+loader-2+"กำลัง…" + กัน double-submit + toast หลังปิด)** ✅/❌
- [ ] **#45 Disabled/Read-only style + Form Section (>6 fields แบ่งกลุ่มหัว caption)** ✅/❌
- [ ] **#46 Placement Contract (สร้าง=`.ph-actions` ขวาสุด · drawer primary ล่างขวา · badge หลังชื่อ 8px pill เดียว · แก้ไข→ลบลำดับตายตัว · ลบผ่าน modal)** ✅/❌
- [ ] **#47 Stepper กลาง (.stepper จาก skeleton, 2-5 steps, สุดท้าย="ตรวจสอบและยืนยัน")** ✅/❌
- [ ] **#48 Landing = M1/M2/M3 เท่านั้น (ถ้ามีหน้า home)** ✅/❌
- [ ] **Microcopy (คำปุ่ม/toast/confirm ตรง knowledge/microcopy.md — สถานะใช้ pill vocabulary กลาง)** ✅/❌
- [ ] **Fixed Tokens (font-size/spacing/radius ใช้ var --fs-*/--sp-*/--r-* — audit ไม่เจอค่าลอย)** ✅/❌

### G2. Document Archetype Check (if Pattern Q — Iron Rules #98–#101)
- [ ] wizard 5 steps ชื่อล็อก: เลือกแหล่งที่มา › ข้อมูลหลัก[เอกสาร] › รายการสินค้า › เอกสารแนบ › ตรวจสอบและยืนยัน (#100) ✅/❌
- [ ] step 3 = B2 v2 verbatim: `.line-tbl` + widths 26/—/64/92/92/78/72/104/54 + lean 1-line advanced row + ส่วนลดท้ายบิล segmented ฿/% + `renderLineSummary` order (#99) ✅/❌
- [ ] `calcLineVat` / `migrateLine` / `totals` / `taxBadgeV` / `updateLine` ลอกตรงจาก line-editor-v2 (#99) ✅/❌
- [ ] view tabs ล็อก: รายละเอียด › [domain ≤2] › PDF Preview › ลายเซ็น / อนุมัติ › ประวัติ · เอกสารแนบเป็น section ใน รายละเอียด (#101) ✅/❌
- [ ] view header: code `.tbl-mono` primary + `docPill` + summary line + action group ตามสถานะ + divider + copy/printer/download/X (#98) ✅/❌
- [ ] list มีคอลัมน์ สถานะเอกสาร (`docPill`) + ลายเซ็น (`renderSignProgress` n/N) (#98) ✅/❌
- [ ] PDF tab = toolbar + `.a4` + 3 ช่องเซ็น (#98) ✅/❌
- [ ] submit modal = DOA slot picker เลือกคน (avatar+position+name) ไม่มี hardcoded chain (#98 + มติ 2026-08-17) ✅/❌
- [ ] `bash scripts/audit.sh` ส่วน `doc_archetype` = 0 ✅/❌

### H. Pipeline Mode Specific Check (if Pipeline)
- [ ] All routes from FRD 01_UI.md exist ✅/❌
- [ ] All actions in 01_UI.md mapped to JS functions ✅/❌
- [ ] Validations from 05_RULES.md enforced ✅/❌
- [ ] Functions Cut (BRD §14.6) NOT implemented ✅/❌
- [ ] Conflicts logged (if any) in output summary ✅/❌

### I. Requirement Coverage Check (Iron Rule #37) — เทียบกับ Coverage Map (Step 1.0)
- [ ] ทุก **field** ใน map → มีในฟอร์ม (type/required/validation ตรง) ✅/❌
- [ ] ทุก **action/ปุ่ม** → wire เป็น JS จริง (ไม่มีปุ่มหลอก) ✅/❌
- [ ] ทุก **status** → แสดง + transition ได้ ✅/❌
- [ ] ทุก **route + column** → ครบ ✅/❌
- [ ] ของที่ **ขาด/เติม default** → log ใน summary (Gaps Filled / Functions Cut) — ไม่มีแถวเงียบหาย ✅/❌

### Verdict
✅ All checks pass → deliver
❌ Found N issues at [section] → fix before deliver
```

---

## 📋 Phase 6 — Deliver

### Step 6.1 — Save

```
/mnt/user-data/outputs/[feature_name].html
```
`feature_name` = kebab-case English (e.g., `customer-management.html`, `f-01-prospect.html`)

### Step 6.2 — present_files

```python
present_files(["/mnt/user-data/outputs/[feature_name].html"])
```

### Step 6.3 — Summary Message

```markdown
✅ HTML Prototype พร้อมแล้ว — [feature_name].html

📋 Pages: [list with routes]
🧩 Patterns used: [A, B, C, D etc.]
🛡️ Iron Rules: 48/48 enforced ✅
⚠️ Iron Rule Overrides: [list — typically Rule #14 if FRD said modal for create]
🕳️ Gaps Filled (defaults applied): [list — e.g., "Activity log schema inferred"]

▶️ วิธีใช้:
1. ดับเบิลคลิกไฟล์ → เปิดใน browser
2. ทุก action เล่นได้จริง ด้วย mock data
3. Refresh → ยังอยู่หน้าเดิม (hash routing)

🔧 Dev handoff:
- Replace mock data ใน state.records ด้วย API call ตาม FRD 02_API.md
- Replace setTimeout() ใน submit ด้วย fetch() ตาม API contracts
```

---

## 🚨 Hard Rules (override-resistant)

1. **Iron Rules #1-48 ALWAYS apply** — ใน `knowledge/iron-rules.md` (override anything else including FRD)
2. **CI tokens locked** — Charcoal #111111, Red #FF3B30 (action), Orange #FF9A1F (connection), Ivory bg #FAF8F5, Satoshi + Noto Sans Thai (no exceptions)
3. **Patterns A-O = source of truth** — copy HTML structure verbatim from pattern files
4. **No fabrication** — ถ้า FRD Pack ไม่มีข้อมูล → ใช้ best practice + log in `Gaps Filled` section
5. **Create/Edit = Drawer slide-in (Iron Rule #14)** — silently override FRD if it says modal
6. **Drawer Button Contract (Iron Rule #31)** — footer/header button order + color=role locked; ปุ่มปิด/กลับ ห้ามแดง; view footer = `ปิด` secondary only; บันทึกร่าง ตามกฎ 31.5
7. **No Tailwind CDN** — utility classes อยู่ใน file-skeleton แล้ว (self-contained)
8. **No color emoji** (Iron Rule #23) — Lucide icons only
9. **Search-Select (Iron Rule #34)** — options เยอะ/lookup master → `searchSelectHTML`+`initSearchSelect` ไม่ใช่ `<select>` ยาว
10. **Layout Stability (Iron Rule #35)** — ไม่เบี้ยว/ดัน/เด้ง: scrollbar-gutter stable + popover overlay + table overflow-x
11. **Requirement Coverage (Iron Rule #37)** — ทำ Coverage Map (Step 1.0) ก่อน + verify (Check I); ของขาด/เติม ต้อง log เสมอ
12. **Thai Rhythm (Iron Rule #38/#36)** — ข้อความไทยใน element fix-height ต้องเข้ากึ่งกลาง (padding-top nudge) — **render จริงด้วยฟอนต์ไทยก่อน claim** ห้าม `line-height:1`/`overflow` บนปุ่ม
13. **List Contract (Iron Rule #40/#41)** — 1 ข้อมูล=1 คอลัมน์ (ห้ามซ้อน) · กดแถว=เปิด view (ไม่มีไอคอนดวงตา)
14. **Self-audit (workflow)** — รัน `scripts/audit.sh` + `render-check.py` ใน Phase 5 ก่อน deliver
15. **Placement Contract (Iron Rule #46)** — ปุ่มสร้างอยู่ `.ph-actions` ขวาสุดเท่านั้น · drawer primary ล่างขวาชิดขวาเสมอ · status badge หลังชื่อห่าง 8px (pill เดียวระดับ header) · edit→delete ลำดับตายตัว · ลบผ่าน confirm modal เสมอ
16. **Microcopy กลาง (knowledge/microcopy.md)** — คำปุ่ม/toast/confirm/empty ตามตาราง ห้ามแต่งเอง · status pill vocabulary สถานะเดียว=สีเดียวทุกไฟล์
17. **Stepper กลาง (Iron Rule #47)** — `.stepper` จาก skeleton เท่านั้น ห้ามออกแบบใหม่
18. **Landing = 3 variants (Iron Rule #48)** — M1/M2/M3 ห้าม carousel/banner
19. **Fixed tokens** — font-size/spacing/radius ผ่าน `var(--fs-*/--sp-*/--r-*)` เท่านั้น
20. **Document Archetype (Iron Rule #98)** — เอกสารธุรกรรมทุกใบ = Pattern Q ทั้ง 4 surface · ห้ามคิดโครงใหม่ · FRD ขัด = silent override + log
21. **Line Editor v2 (Iron Rule #99)** — การกรอก item / ส่วนลด / VAT / totals ต้องเหมือน SO reference เป๊ะ ทุกเอกสาร (PR/PO/GRN/INV/CN…) — ลอก `line-editor-v2.js.txt` verbatim
22. **Wizard Step Contract (Iron Rule #100)** — 5 steps ชื่อ+ลำดับล็อก (ตัด step 3 ได้ถ้าไม่มี line items) · `STEPH` header ทุก step
24. **Combobox Option Anatomy (Iron Rule #102)** — คน = avatar → ชื่อ → ตำแหน่ง·แผนก · สินค้า = package → code·หมวด → ชื่อ → ราคา/สต๊อก — ทุก dropdown ในไฟล์หน้าตาเดียวกัน · อะไร search ได้ต้องเป็น search dropdown
25. **Lean List (Iron Rule #103)** — 1 ข้อมูล = 1 คอลัมน์ ห้ามซ้อน · ข้อมูลรองไป title/drawer · หน้าจอนิ่ง (#35/#95)
23. **View Tab Contract (Iron Rule #101)** — landing = รายละเอียด (รวมเอกสารแนบ) · PDF Preview · ลายเซ็น/อนุมัติ · ประวัติ — domain tabs แทรกหลัง รายละเอียด ไม่เกิน 2

---

## 📚 Files in this Skill

| File | Purpose |
|---|---|
| `SKILL.md` | This file — workflow + decisions |
| `references/pipeline-mode.md` | Pipeline Mode detail (FRD Pack input) |
| `references/standalone-mode.md` | Standalone Mode detail (no Pack) |
| `references/conflict-resolution.md` | Priority order when sources conflict |
| `references/gap-detection.md` | Detect dropped requirements through chain |
| `references/design-system.html` | 🆕 **Living visual reference** — เปิด browser ดู 21 features × 66 variants พร้อม Iron Rules 30/30 |
| `patterns/A_list-view.md` | List page with filter + table |
| `patterns/B_create-edit-drawer-wizard.md` | **Drawer slide-in for Create/Edit (override)** |
| `patterns/Q_transaction-document-archetype.md` | ⭐ **v9 — แบบประกอบเอกสารธุรกรรม (list / wizard 5 steps / view tabs / PDF / sign / DOA modals) — locked to SO reference** |
| `patterns/B2_document-line-editor.md` | ⭐ **v9 = v2 — Line editor re-locked กับ SO: grid compact `.line-tbl` + lean advanced row + VAT 3 โหมด + discount engine + ส่วนลดท้ายบิล ฿/% + totals — บังคับทุกเอกสารธุรกรรม** |
| `patterns/P_day-planner-scheduler.md` | ⭐ **v9 — Planner/Scheduler (ปฏิทินเดือน · day Gantt · build pool DnD · capacity · team week)** |
| `references/document-archetype/_SOURCE_so-reference.html` | ⭐ **canonical ของ Q + B2 v2** — F-SALES-SO v2 (user craft) เปิด browser ดูเป้าหมาย 100% |
| `references/document-archetype/line-editor-v2.js.txt` | JS line editor v2 (25 defs) — ลอก verbatim |
| `references/document-archetype/doc-create-wizard.js.txt` | JS create drawer + 5 steps + wizardNext/Back + combo |
| `references/document-archetype/doc-view-drawer.js.txt` | JS view drawer + tabs + SEC/KV/SECWRAP + PDF + Sign + History |
| `references/document-archetype/doc-approval-modals.js.txt` | JS submit/approve/reject/cancel/hold + DOA slot picker |
| `references/document-archetype/doc-archetype.css.html` | CSS fragments ที่ Q/B2 ต้องมีเพิ่มจาก kit |
| `references/planner/_SOURCE_op-action-plan.html` / `_SOURCE_team-plan.html` | canonical ของ Pattern P |
| `references/drawer-standard/_SOURCE_line-editor-reference.html` | (legacy v8 PR reference — เทียบเท่านั้น ห้ามใช้ gen) |
| `references/drawer-standard/master-combobox.js.txt` | **Master combobox canonical (Rule #94)** — search dropdown สำหรับทุก field ที่อ้าง master (SO ใช้ `combo()` เวอร์ชันย่อใน doc-create-wizard.js.txt — contract เดียวกัน) |
| `patterns/C_view-drawer-tabbed.md` | View detail with tabs |
| `patterns/D_modal-confirmation.md` | **Modal — confirmation only** |
| `patterns/E_compact-table-expandable.md` | Compact table with expandable row |
| `patterns/F_configurable-modifier.md` | Toggle + sub-config card |
| `patterns/G_po-style-view-drawer.md` | PO-style view (alias of C — v2 wide drawer + PDF) |
| `patterns/H_a4-paper-pdf-preview.md` | A4 paper PDF preview tab |
| `patterns/I_signature-card-list.md` | Signature card list |
| `patterns/J_dashboard-kpi-chart.md` | 🆕 Dashboard KPI + SVG chart (J1/J2/J3) |
| `patterns/K_report-print.md` | 🆕 Informative report — screen + print CSS |
| `patterns/L_collection-views.md` | 🆕 Card grid / Kanban / Timeline |
| `patterns/M_landing-home.md` | 🆕 Landing/Home — M1 Hero+Tiles / M2 Workspace / M3 KPI Home |
| `patterns/N_sidebar-nav-shell.md` | 🆕 Sidebar Navigation Shell 3 ระดับ + icon rail + slide panel (reference: `references/sidebar-shell/core-shell-ultimate.html`) |
| `patterns/O_split-pane-runner.md` | 🆕 v6.1 Split-Pane Runner — checklist/execution page (navigator ซ้าย + step checklist) |
| `knowledge/ci-tokens.md` | CUBE Design System colors (Charcoal/Red/Orange, Warm Light), fonts, spacing tokens |
| `knowledge/iron-rules.md` | Iron Rules consolidated (#1–#49 + #94–#103) |
| `knowledge/microcopy.md` | 🆕 คำมาตรฐานกลาง + status pill vocabulary |
| `knowledge/erp-design-guide.md` | ERP Sidebar 232px / Shell-bar 52px white / Breadcrumb / Page Header |
| `scripts/audit.sh` | 🆕 Self-audit lint — grep banned patterns (Phase 5) |
| `scripts/render-check.py` | 🆕 Screenshot HTML (playwright) — verify visual Thai-rhythm/empty/sticky |
| `knowledge/component-catalog-ref.md` | Canonical component names (38 components in 10 groups) |
| `knowledge/design-system-reference.md` | 🆕 Route map → variants ใน design-system.html (when to consult + how) |
| `templates/file-skeleton.template.html` | HTML skeleton with full CSS + utility classes |
| `templates/erp-shell.template.html` | ERP App Shell (Sidebar + Shell-bar + content wrapper) |
| `templates/general-shell.template.html` | General feature shell (no sidebar) |
| `examples/pipeline-mode-walkthrough.md` | F-01 Prospect example (Pack → HTML) |

---

## 🎓 Quick Start

```
User: "สร้าง HTML จาก FRD Pack นี้"
       + แนบ FRD_F-04_Pack/ + BRD_F-04.md

Skill:
  Phase 0: Detect Pipeline Mode (Pack exists)
    - Read knowledge/iron-rules.md + ci-tokens.md + erp-design-guide.md + component-catalog-ref.md
    - Read knowledge/design-system-reference.md (route map)
    - Read references/pipeline-mode.md + references/conflict-resolution.md
  Phase 1: Plan
    - Read FRD Pack 01_UI.md → N pages, patterns A+B+C+D needed
    - 🆕 View references/design-system.html — match each page → variant ใน design system
      (e.g. F-04 list page → #/list "Table View", F-04 create → #/create "Single-Step Drawer")
    - Read patterns/A_list-view.md, B_*.md, C_*.md, D_*.md (lazy-load)
    - Apply Iron Rule #14 override if FRD says modal for create → use drawer
    - Show plan summary to user (with Functions Cut list from BRD §14.6)
  Phase 2: Build skeleton + ERP shell
    - templates/file-skeleton.template.html (full CSS)
    - templates/erp-shell.template.html (sidebar 232px + shell-bar 52px white)
  Phase 3: Implement N pages (using loaded patterns)
    - 🆕 Copy structure จาก matched variants ใน design system
  Phase 4: Implement behavior (state/router/drawer/toast)
  Phase 5: Mechanical Verification (9 checks A-I, Iron Rules 48/48)
    - 🆕 Visual sanity check vs design-system.html (variant ที่ใช้ดูคล้ายไหม)
  Phase 6: Deliver with summary + Iron Rule overrides log + Gaps filled
```


---

## ⭐ v6.2 (2026-07-26) — Layout Integrity + Pre-flight
- เพิ่มหมวดกฎ **#50-#60** ใน `knowledge/layout-integrity.md` — คุมเรขาคณิต (spacing scale, form grid,
  row consistency, table align, vertical rhythm, overflow discipline) เกิดจาก defect จริง F-PRODUCT:
  ไฟล์ผ่านกฎ 49 ข้อแต่เบี้ยว เพราะไม่มีกฎคุมเรขาคณิตเลย
- **Rule #60 Pre-flight บังคับ:** ก่อนส่งไฟล์ ต้อง self-check ตาม checklist แล้วประทับ
  `<!-- PREFLIGHT: ... -->` ท้ายไฟล์ — ไม่มี = checker นับ NOT-CHECKED = BLOCK
- อ่าน layout-integrity.md **ทุกครั้ง** ที่ gen เท่ากับ iron-rules.md — สองไฟล์นี้ศักดิ์เท่ากัน
- **v6.3 (2026-07-26) Component Contracts #63-#68** — `knowledge/component-contracts.md`
  จาก defect จริงเทียบระบบ production: #63 List Density (row 44/td pad 8·12/font 12.5) ·
  #64 Breathing Room (ระยะขั้นต่ำระหว่าง component) · #65 Search Dropdown Contract
  (avatar+ชื่อ+บรรทัดรอง+meta, max-height 320+scroll) · #66 Position Awareness (flip-up เมื่อจอล่างไม่พอ
  — ใช้ positionMenu util) · #67 Hint→Tooltip (ห้าม hint เปลือย >60 ตัวอักษร — เข้า ⓘ hover) ·
  #68 Overlay Discipline (global outside-click ตัวเดียว, ห้าม stopPropagation เหมา, เปิดทีละตัว)
  — อ่านไฟล์นี้ทุกครั้งที่ gen ศักดิ์เท่า iron-rules
- **v6.4 (2026-07-26) Kit Integrity #69 + Checkpoint Protocol** — วินิจฉัยจากข้อมูลจริง:
  CSS เบี้ยวเพราะ**สืบทอดจาก skeleton ที่ป่วยเอง** (แก้แล้ว: skeleton ผ่าน self_audit = 0 ทุกตัวนับ,
  เพิ่ม tooltip/drop-up CSS + utils positionMenu/openOverlay/global-click + `#page-late` escape) ·
  inline ท้ายไฟล์เพราะย้อนแก้ CSS ไม่ได้ → มี `<style id="page-late">` ให้แล้ว inline = ผิด 100% ·
  audit ตรวจเป็น **checkpoint ทุก Phase** ไม่ใช่ครั้งเดียวท้ายไฟล์ (ดู layout-integrity.md)
- **v6.10 (2026-07-28) One-Shot Hardening** — #82 Behavior-from-Kit (JS ใน reference ถูก strip — ลอกได้แค่ markup/CSS) + audit v7 จับ undefined_handlers/missing_ids (tab ตาย = จับได้ static) + Render Gate เดิน interaction ครบ
- **v6.9.1 (2026-07-28)** — #81 ห้ามศัพท์ภายในรั่วขึ้นจอ (E-xxx/hook/bucket) · #68.1 overlay ระบบเดียว (แก้เด้ง) · #73.1 ทุก tab มีชีวิต + audit jargon_leak
- **v6.9 (2026-07-28)** — reference ครบ 4 archetype (drawer/fullpage/console/general-standard จากไฟล์
  vibe ที่ user อนุมัติ — heal แล้วทั้งหมด) + #78.7 filter=dropdown เท่านั้น · #78.8 chip ใน td ·
  #62.2 เมนูลอยต้องทึบ+var(--z-dropdown) + audit menu_no_bg_z
- **v6.8 (2026-07-27) Reference-First** — `templates/reference/product-master.reference.html`
  (ไฟล์ vibe ที่ user อนุมัติ, CSS heal เข้า scale แล้ว) = Golden Reference: feature type ตรง →
  **mirror ทั้งโครงทุกหน้า** bind data ใหม่เท่านั้น (inline ใน ref ต้องแปลงเป็น class ตอน gen)
- **v6.7 (2026-07-27) Block-First + Reference Blocks** — `templates/blocks/` snippet จริงที่กลั่นจาก
  ไฟล์ vibe ที่ผ่านตา user: toolbar-filter · uom-editor (progressive + สมการ + role chips สี) ·
  avatar-cell (initial แทนรูปแตก) — เคสที่มี block **ลอกแล้ว bind ห้ามออกแบบเอง** + กฎ #78-#80
- **v6.6 (2026-07-27) — จาก visual review รอบ 2 ของ user:**
  #74 Drawer Tab Contract (ใช้ class kit เท่านั้น — เส้นเดียว ห้ามซ้อน) · #75 Form Composition
  (grid 2 คอลัมน์, ห้าม orphan/ช่องโหว่ง >24px, สถานะอยู่ header) · #76 No Horizontal Overflow
  (drawer ห้ามมี scrollbar ล่าง) · #77 Mock Completeness + Compound Widget (ทุก section มีข้อมูลจริง,
  conversion แสดงสมการ+ตัวอย่าง+role chips) — ดู component-contracts.md
  **+ Phase 0.5 ERP UX Reference:** อ่าน `knowledge/erp-ux-patterns.md` ทุกครั้ง (offline layer) ·
  มี network → search UI จริง (Odoo/Fiori/D365) ของ feature type สั้น ๆ หยิบเฉพาะโครงการวาง
  แล้ว log ว่าหยิบอะไร · ลำดับศักดิ์: กฎเรา > ไฟล์ pattern > search สด
- **v6.5 (2026-07-26) Page Anatomy #70-#73** — `knowledge/page-anatomy.md` — บทเรียนจากเทียบ
  ไฟล์เลน (audit ศูนย์แต่จืด) กับไฟล์ vibe ที่ user ชอบกว่า: ความถูก ≠ ความรวย — กฎชุดนี้สั่งขั้นต่ำ
  ของ composition: #70 List (stat row ≥4 คลิกได้ + chip counts + sortable + เซลล์ 2 บรรทัด) ·
  #71 Form/Wizard (section cards + summary ก่อน submit) · #72 Drawer (identity header + tab counts +
  definition grid) · #73 Interaction (sort จริง/filter จริง/ตัวเลข sync data) — ความรวยมาจาก element
  ไม่ใช่ขยายขนาด (density ยึด #63 เดิม) — อ่านทุกครั้ง ศักดิ์เท่า iron-rules
- **Self-Review Protocol 2 รอบ (บังคับ):** รอบ 1 Mechanical — รัน `scripts/self_audit.py <file>`
  แก้จนทุกตัวนับ = 0 · รอบ 2 Role Sweep — เปลี่ยนหมวกเป็น reviewer ไล่ checklist เชิงบทบาท
  (pattern/ปุ่มตามบทบาท/state ครบ/flow เดินจบ/microcopy/hook) พร้อมหลักฐานทุกข้อ
  แล้วประทับ `<!-- PREFLIGHT v6.2 -->` **แบบมีตัวเลข** — ตราเปล่า/ไม่มีตรา = checker BLOCK
  (env ไม่มี python → ไล่นับมือตาม logic เดียวกัน — ตัวเลขต้องมาจากการนับจริงเท่านั้น)
