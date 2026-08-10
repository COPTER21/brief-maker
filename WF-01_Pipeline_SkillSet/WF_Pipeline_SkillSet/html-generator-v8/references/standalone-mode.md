# Standalone Mode — Flexible Input

> **Source:** v25 lines 156-185 — refactored for v3.
> **Activated when:** User provides ad-hoc input (idea, screenshot, brief, bullets, mixed) — NOT a structured FRD Pack.

---

## 🎯 When Standalone Mode Activates

Standalone Mode is the **default fallback**. It kicks in when input is:

- **Text description** of feature ("I want a list of customers with...")
- **Screenshot** of UI to replicate
- **Existing Feature Brief** (Markdown)
- **BRD** without paired FRD
- **Bullet points** of requirements
- **Mixed input** — text + screenshot + reference link
- **Idea/sketch** — even just "ทำหน้า login เถอะ"

If user gives **FRD v4 Pack** → switch to `pipeline-mode.md` instead.

---

## 📥 Acceptable Input Formats

### Format 1: Text Description (most common)

```
สร้างหน้า Customer list มี:
- search by name
- filter by status (active / inactive)
- table แสดงชื่อ อีเมล วันที่สร้าง
- click row → ดู detail
- เพิ่ม customer ใหม่ผ่าน drawer
```

→ Generator infers: Pattern A (list) + Pattern B (create drawer) + Pattern C (view drawer)

### Format 2: Screenshot

User attaches PNG/JPG of existing UI:
- Generator analyzes layout
- Maps elements to component catalog
- Recreates in CUBE NATIVE CI

→ Reply with: "เห็น dashboard with 4 KPI cards + table. กำลังสร้าง Pattern A + KPI stats..."

### Format 3: Feature Brief (.md)

Pre-existing Brief from `feature-brief-generator`:
- Read sections: §3 (UI), §4 (Data), §5 (Validation), §10 (Acceptance)
- Generate HTML per Brief spec

### Format 4: Bullets

```
- หน้าราคา membership
- 3 tiers: Free, Pro, Enterprise
- มี toggle monthly/yearly
- CTA button per tier
```

→ Recognize as marketing/landing page → use `general-shell.template.html` + custom card grid

### Format 5: Mixed

```
[screenshot]
"แบบนี้แต่ใส่ filter เพิ่ม"
```

→ Combine: base layout from screenshot + filter addition

---

## 🔍 Step-by-Step Standalone Flow

### Step 1: Classify input type

Quickly identify what user gave:
- **ERP feature** (admin, has sidebar + breadcrumb)? → `erp-shell.template.html`
- **Marketing/landing/public** (no sidebar)? → `general-shell.template.html`
- **Single component/widget**? → Skip shell, just build the component

### Step 2: Ask once if critical info missing

**Ask once** if these are unclear:
- Module/section name (for sidebar context)
- Primary entity (customer? product? order?)
- Primary action (create? approve? view?)

**DON'T ask** these (use defaults):
- Width of drawer (v2: 920px / .standard 680px — Iron Rule #11)
- Animation duration (default 280ms)
- Color of pill (default by status mapping)
- Icon for action (default by Lucide convention: edit=pencil, delete=trash-2, view=eye)

### Step 3: Pick pattern(s)

| User input keywords | Pattern |
|---|---|
| "list", "table", "search", "filter" | A |
| "create", "edit", "form", "wizard" | B (drawer slide-in) |
| "detail", "view", "tabs" | C (drawer with tabs) |
| "confirm", "delete", "archive", "logout" | D (modal) |
| "many columns", "expand", "detail per row" | E (compact + expandable) |
| "toggle", "setting", "optional feature" | F (configurable modifier) |
| "PO", "invoice", "quotation", "with PDF" | G (PO-style drawer) |
| "print preview", "A4", "PDF view" | H (A4 paper) |
| "approval", "signatures", "sign-off" | I (signature card list) |

### Step 4: Fill gaps with defaults

For any unspecified detail, use sensible defaults:

| Unspecified | Default |
|---|---|
| Module name | "Module" |
| Primary entity | "Item" |
| Page title | Use entity name plural ("Items") |
| Subtitle | "จัดการ <entity> ในระบบ" |
| Empty state copy | "ยังไม่มี <entity>" |
| Statuses | active / archived (2 simple states) |
| Sample records | Generate 5-10 plausible records |
| Avatar gradient | Primary→Teal (CUBE NATIVE standard) |
| User in shell-bar | "Tadswan C." / "Marketing Lead" / "TC" |

### Step 5: Generate

Use templates + patterns, apply CI tokens.

### Step 6: Self-document

In chat output, briefly explain what you built:

```
✅ สร้างเสร็จ: customer_list.html

📋 ใช้:
- Layout: ERP shell (sidebar + breadcrumb)
- Pattern A (list) + Pattern B (create drawer 920px) + Pattern C (view drawer 920px)
- 12 sample records, 4 statuses (active / inactive / suspended / archived)

🕳️ Defaults used (ปรับได้):
- เจ้าของในตาราง: random assign
- Module name: "Customers"
- Avatar gradient: ตาม CI default

✨ พร้อมเปิดใน browser
```

---

## 🎯 Input Quality vs. Output Quality

| Input quality | Output expectation |
|---|---|
| **Vague:** "ทำ dashboard" | Generic dashboard with 4 KPI + 1 chart placeholder + recent activity. Ask: "Dashboard นี้สำหรับ module ไหน?" |
| **Medium:** "Customer list with search + filter + bulk action" | Solid Pattern A implementation with all features mentioned, 10 sample customers |
| **Detailed:** Full Feature Brief with sections | Production-quality, accurate to Brief spec |
| **Pristine:** FRD Pack | Switch to Pipeline Mode |

---

## ⚠️ When to Push Back / Ask

**Ask user when:**
- Input is **clearly a Feature** but missing critical entity name ("ทำหน้า list" → "List ของอะไร?")
- **Mutually exclusive interpretation** ("ทำ create" → could be Modal OR Drawer → use drawer default, but note in output)
- **Suspicious gap** that would break the feature (e.g., "approval workflow" but no signers defined)

**Don't ask when:**
- Default would obviously be fine (icon color, button label phrasing)
- User said "อะไรก็ได้" or "ตามที่เห็นสมควร"

---

## 🎯 Common Standalone Scenarios

### Scenario A: "ทำ ERP feature ใหม่ใน prospect"

→ ERP shell + Pattern A list + Pattern B create drawer + Pattern C view drawer + Pattern D delete modal.

Output: ~120KB HTML, hash routing `#/prospects`.

### Scenario B: "ทำ landing page สำหรับ product แนวนี้: [screenshot of marketing page]"

→ General shell (no sidebar) + hero + features grid + pricing tiers + CTA + footer.

Output: ~80KB HTML, single page.

### Scenario C: "ทำ approval workflow มี 3 ระดับ"

→ ERP shell + Pattern A list + Pattern G PO-style drawer (3 tabs: Detail/PDF/Signatures) + Pattern I signature list.

Output: ~140KB HTML.

### Scenario D: "ปรับ HTML เดิมให้เพิ่ม XYZ" + existing HTML attached

→ Read existing HTML, identify what to keep + what to change, output diff'd version.

---

## 🛡️ Iron Rules Apply

Even with minimal input, **all 26 Iron Rules** must be enforced:

- Use CI tokens from `knowledge/ci-tokens.md` (never deviate)
- Apply Iron Rules from `knowledge/iron-rules.md` (no exception)
- For Create/Edit: **always drawer slide-in** (Iron Rule #14)
- Lucide icons only (Iron Rule #23)

---

## 📝 Self-Check at End

Before delivering, mentally check:
- [ ] Pattern(s) chosen match user intent
- [ ] CI tokens applied (no rogue colors)
- [ ] Iron Rules audit pass
- [ ] Sample data plausible (not Lorem Ipsum)
- [ ] Hash routing works (`#/route` refresh-safe)
- [ ] Single-file HTML (one `.html`, no external dependencies except CDN fonts/icons)
- [ ] Output explains what was built + what defaults applied

---

## 🎯 The "Just Make It Good" Principle

For Standalone Mode, if input is vague:
1. **Pick the most likely interpretation** (don't dither)
2. **Apply CUBE NATIVE defaults aggressively**
3. **Document choices** in output (so user can correct if wrong)
4. **Generate one cohesive output** (not 3 variants)

User wants results > clarifying questions. Better to ship something and iterate.
