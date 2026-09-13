# Design System Reference — 2BSimple CUBE NATIVE

> **Living HTML reference** ของทุก component / layout / pattern ที่ Skill นี้ generate.
> เปิดไฟล์ในเบราว์เซอร์เพื่อดูตัวอย่างจริง (กดเล่นได้) — ดีกว่าอ่าน spec เป็นข้อความ

---

## 📍 Where

**Path:** `references/design-system.html`
**Open:** เปิดในเบราว์เซอร์ → SPA hash routing — sidebar ซ้ายมี 6 modules
**Coverage:** 6 modules × 21 features × 60+ variants — ครบทุก pattern ที่ skill นี้รองรับ

---

## 🎯 When to consult this reference

Skill (Claude) ควรเปิดดู `references/design-system.html` ก่อน generate ใน 3 สถานการณ์:

### 1. ก่อน Phase 2 (Build Skeleton)
ตรวจ shell + sidebar + shell-bar pattern — ดูตัวอย่างจริง `#/home` หรือ `#/landing`

### 2. ระหว่าง Phase 3 (Implement Pages)
ดูตัวอย่าง **variant ที่ตรงกับ feature** เพื่อ copy structure:

| ถ้า feature ต้องการ... | เปิด route |
|---|---|
| List page (table + filter) | `#/list` variant "Table View" |
| Card-grid view (browse entities) | `#/list` variant "Card Grid" |
| Kanban workflow | `#/list` variant "Kanban Board" |
| Timeline / activity log | `#/list` variant "Timeline" |
| Detail page with tabs | `#/detail` variant "Header + Tabs" |
| Detail page two-column | `#/detail` variant "Two-Column" |
| Document/Invoice style | `#/detail` variant "Document Style" |
| Dashboard (KPI heavy) | `#/dashboard` variant "KPI Heavy" |
| Dashboard (chart heavy) | `#/dashboard` variant "Chart Heavy" |
| Dashboard (mixed compact) | `#/dashboard` variant "Mixed Compact" |
| Landing/Home page | `#/landing` variant "Hero + Tiles" or "Workspace Grid" |
| Create — single step | `#/create` variant "Single-Step Drawer" |
| Create — multi-step wizard | `#/create` variant "Multi-Step Wizard" |
| Create — quick form (1-3 fields) | `#/create` variant "Quick Add Modal" |
| Edit existing record | `#/edit` variant "Edit Drawer" / "Inline Edit" |
| Field examples (input/select/toggle/textarea) | `#/fields` (4 variants) |
| Modal — Confirm | `#/modals` variant "Confirm (Info)" |
| Modal — Danger Delete | `#/modals` variant "Danger Delete" |
| Modal — Warning | `#/modals` variant "Warning" |
| Modal — Success | `#/modals` variant "Success" |
| Drawer — Create | `#/drawers` variant "Create Drawer" |
| Drawer — View + Tabs | `#/drawers` variant "View Drawer + Tabs" |
| Drawer — PO-style (680px) | `#/drawers` variant "PO-Style View" |
| Toast notifications | `#/toasts` (4 variants) |
| Empty state | `#/empty` (3 variants) |
| KPI report | `#/kpi` (3 variants) |
| Chart report (bar/line/pie/area) | `#/chart` (4 variants) |
| Table report (standard/grouped/pivot) | `#/table-rpt` (3 variants) |
| Mixed report (exec/ops) | `#/mixed` (2 variants) |
| Wizard (linear/branching) | `#/wizard` (2 variants) |
| Tab bars (underline/pill) | `#/tabs` (2 variants) |
| Auth pages (signin/signup/forgot) | `#/login` (3 variants) |
| Color tokens | `#/colors` (4 variants) |
| Typography scale | `#/typography` (3 variants) |
| Iconography (Lucide grid) | `#/iconography` (4 variants) |

### 3. ระหว่าง Phase 5 (Verification)
- ตรวจว่า component ใน HTML ที่ generate ดูเหมือน reference ไหม
- ถ้ามี variant ใน reference ตรงกับสิ่งที่ generate → mimic เลย ลด freelance design

---

## 🛠️ How Skill Should Use It

```
[Phase 1 — Plan]
  - Read knowledge/iron-rules.md
  - Read knowledge/ci-tokens.md
  - ✨ NEW: Open references/design-system.html (ดู structure ของ variant ที่จะใช้)
  - Decide patterns A-I

[Phase 3 — Implement]
  - copy structure จาก variant ที่ matched ใน design system
  - ไม่ต้อง "ออกแบบ" ใหม่ — reference เป็น source of truth

[Phase 5 — Verify]
  - เทียบกับ design system reference variant ที่ใช้
  - ✅ ดูเหมือน reference → pass
  - ❌ deviate จาก reference โดยไม่จำเป็น → fix
```

---

## 📋 Module / Feature Map

| Module | Features (sidebar items) | Total Variants |
|---|---|---|
| **Foundations** | Overview · Colors · Typography · Iconography | 11 |
| **Page Layouts** | List · Detail · Dashboard · Landing | 12 |
| **Forms & Inputs** | Create · Edit · Fields | 10 |
| **Feedback** | Modals · Drawers · Toasts · Empty | 14 |
| **Reports & Charts** | KPI · Chart · Table · Mixed | 12 |
| **Navigation** | Wizards · Tabs · Auth Pages | 7 |

**Grand total:** 21 features, 66 variants

---

## 🔒 Relationship with Iron Rules

Design System reference เป็น **visual implementation** ของ Iron Rules 30 ข้อ — ทุก variant ใน reference **ผ่าน 30/30 rules**.

**Hierarchy:**
1. `knowledge/iron-rules.md` — **rule definitions** (SUPREME, override anything)
2. `references/design-system.html` — **visual examples** of rules in action
3. `patterns/A-I.md` — **structure guides** per page type

ถ้ามี conflict → iron-rules ชนะเสมอ. Design system เป็น guide ที่ตอบโจทย์ rules ครบแล้ว ดังนั้น copy structure จาก reference = ผ่าน rules โดยอัตโนมัติ.

---

## 🚀 Future Extensions (planned)

- **Code view** — กดดู HTML/CSS snippet ของแต่ละ variant + copy button
- **Storybook-style site** — deploy เป็น `design.cube.com` (standalone)
- **CUBIC Registry integration** — link component → API → Engine → Feature
- **A11y panel** — แสดง contrast ratio, ARIA roles per component
- **Token editor** — แก้ CSS variable แล้ว preview รวม (rebrand simulation)

---

## 📝 Maintenance Notes

- **Update เมื่อมี:** new Iron Rule (#31, #32, ...), new pattern (J/K/...), new component variant
- **Versioning:** ใส่ version note ใน `<title>` ของ design-system.html (e.g. "v1.0 · 30 rules")
- **Validation:** ทุกครั้งที่อัพเดต design system HTML ต้องรัน Phase 5 audit (30/30 rules)
