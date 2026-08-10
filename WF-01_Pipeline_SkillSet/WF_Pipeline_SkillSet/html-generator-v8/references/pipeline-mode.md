# Pipeline Mode — Input from FRD Pack (v4-v6)

> **Source:** v25 lines 186-285 "Reference Mode" — refactored for v3.
> **Activated when:** User provides an FRD Pack (v4-v6) (folder with 01_UI.md, 02_API.md, 03_LOGIC.md, etc.) along with Brief + BRD.

---

## 🎯 When Pipeline Mode Activates

Pipeline Mode kicks in when user input includes **at least one of**:

1. **FRD Pack (v4-v6) folder** with files like `01_UI.md`, `02_API.md`, `03_LOGIC.md`, `04_DB.md`, `05_RULES.md`, `06_TESTS.md`
2. **Brief + BRD pair** referencing finalized FRD spec
3. **Explicit user request:** "ใช้ pipeline mode" / "generate HTML จาก FRD Pack" / "follow FRD v4 spec"

If none of these are present → use **Standalone Mode** (see `standalone-mode.md`).

---

## 📥 Input Priority

When multiple sources are available, **resolve conflicts in this priority order**:

```
1. FRD Pack (v4-v6) / 01_UI.md    ← HIGHEST PRIORITY (authoritative UI spec)
2. BRD §14.6 (Functions Cut)  ← Scope lock — what's IN/OUT
3. Brief §3.4 (Generator Hints) ← Generator-specific config
4. RIF (Requirement Intake Form) ← Original business intent
5. Chat context / user override ← Lowest priority
```

**Rule:** If FRD 01_UI.md says "show X field", but Brief says "hide X" → **FRD wins**.

---

## 🔍 Step-by-Step Pipeline Flow

### Step 1: Scan input files

```
INPUT FOLDER LAYOUT (expected):
  FRD_F-XX_Pack/
    ├─ 00_INDEX.md            (table of contents)
    ├─ 01_UI.md               ⭐ PRIMARY — UI screens, components, interactions
    ├─ 02_API.md              (API endpoints — informational only)
    ├─ 03_LOGIC.md            (Functions + Engines — informational)
    ├─ 04_DB.md               (Tables — schema reference)
    ├─ 05_RULES.md            (Business rules — embed as validations)
    └─ 06_TESTS.md            (Test cases — verify coverage)

OPTIONAL companion files:
  ├─ BRD_F-XX.md              (business context)
  ├─ Brief_F-XX.md            (decision log)
  └─ RIF_F-XX.md              (original requirement)
```

### Step 2: Parse 01_UI.md (primary spec)

Extract:
- **Screens/pages** — title, route, layout (Pattern A/B/C/D/E/F/G/H/I)
- **Components** — which components per screen (table, drawer, modal, fields)
- **Interactions** — onClick handlers, state changes, navigation
- **Data shape** — sample records, field types, validation rules
- **Routes** — `#/route` hash routes for SPA navigation

### Step 3: Parse 05_RULES.md (validations)

Extract:
- **Required fields** — embed in form validation
- **Cross-field rules** — implement in `validate()` functions
- **State transitions** — encode in status-conditional rendering
- **Permissions/visibility** — apply to UI elements

### Step 4: Cross-reference Brief + BRD

- **Brief §3.4 Generator Hints** — pattern preference, drawer width, special components
- **BRD §14.6 Functions Cut** — final scope (what's IN/OUT for this iteration)

### Step 5: Generate HTML

Use patterns from `patterns/` folder:
- Map screens → patterns (e.g., "Prospect List" → Pattern A, "Create Prospect" → Pattern B drawer)
- Use components from `knowledge/component-catalog-ref.md`
- Apply CI tokens from `knowledge/ci-tokens.md`
- Enforce all 26 Iron Rules

### Step 6: Self-validate output

Check against:
- 01_UI.md screen list — every screen present?
- 05_RULES.md validations — every rule enforced?
- Iron Rules audit — all 48 rules pass?

---

## 🚨 Conflict Resolution Procedure

When sources disagree:

```
SITUATION: Brief says "hide Status column", FRD 01_UI.md says "show Status column with filter"

STEP 1: Apply priority — FRD wins → include Status column
STEP 2: Log conflict in chat output:
  "⚠️ Conflict detected: Brief and FRD disagree on Status column.
   Applied FRD spec (higher priority) — including Status column with filter.
   To override: explicit user instruction needed."
STEP 3: Continue generation with FRD spec
```

---

## 🕳️ Gap Detection

Sometimes FRD doesn't cover everything. Common gaps:

| Gap Type | Detection | Default Action |
|---|---|---|
| Missing route definition | FRD references page but no route | Generate `#/feature/page` |
| Missing field validation | RIF requires X, but 05_RULES.md silent | Add basic `required` validation |
| Missing empty state copy | Table specified, no empty message | Use generic "ไม่พบข้อมูล" |
| Missing icon for action | "Edit" button defined, no icon | Use Lucide `pencil` |
| Missing color for status | New status "review", no color | Default to `pill-registered` (blue) |

**For ANY gap:** Log in output:
```markdown
## Gaps Filled
- ❓ FRD didn't specify validation for `email` — added `required + format`.
- ❓ FRD missing icon for "Convert" button — used `user-check`.
- ❓ BRD §14.6 unclear on "Archive" scope — included as soft archive (Pattern D modal).
```

---

## 📋 Context Window Management

FRD Pack (v4-v6) can be **large** (10+ files, 100KB+ total). Strategy:

### Read in order:
1. **First:** `00_INDEX.md` (small — get overview)
2. **Then:** `01_UI.md` (primary — biggest file)
3. **Selective:** `05_RULES.md`, `04_DB.md` (read only sections needed)
4. **Skim:** `02_API.md`, `03_LOGIC.md`, `06_TESTS.md` (informational — don't deep-read unless asked)

### When context overflows:
- Summarize each file into 2-3 bullet points internally
- Ask user: "FRD Pack มี XX ไฟล์, focus หน้าไหนก่อน?" if too broad

---

## 🎯 Output Format

### Single feature → single HTML file

```
INPUT:  FRD_F-01_PROSPECT_Pack/
OUTPUT: F-01_Prospect.html  (single SPA, hash routing)
```

### Multi-feature in one module → single HTML or multi-page

User preference — ask if not specified:
- **Single SPA** with hash routes: `#/prospects`, `#/customers`, etc.
- **Multi-file** each feature own HTML

---

## ⚠️ Iron Rules Apply

Even in Pipeline Mode, **all 26 Iron Rules** must pass. FRD spec doesn't override Iron Rules:

- FRD says "create page in modal" → **Override: use drawer slide-in** (Iron Rule #14)
- FRD says "10 columns in table" → **Override: max 8, use Pattern E expandable** (Iron Rule #16)
- FRD says "emoji icons" → **Override: Lucide only** (Iron Rule #23)

Document overrides:
```markdown
## Iron Rule Overrides Applied
- Iron Rule #14: FRD specified modal for Create; used drawer slide-in (Pattern B) per CI policy.
- Iron Rule #16: FRD spec had 10 cols; collapsed to 7 + Pattern E expandable for cols 8-10.
```

---

## 📌 Example Pipeline Walkthrough

**Input:**
```
FRD_F-01_PROSPECT_Pack/
  ├─ 00_INDEX.md
  ├─ 01_UI.md            (lists 3 screens: List, Create, View)
  ├─ 02_API.md
  ├─ 04_DB.md            (prospect table schema)
  ├─ 05_RULES.md         (validations)
  └─ 06_TESTS.md
Brief_F-01.md           (generator hints confirmed)
BRD_F-01.md             (§14.6: cut "Bulk Convert" for v1)
```

**Generator output (chat):**
```
✅ Pipeline Mode activated. Parsing FRD_F-01_PROSPECT_Pack...

📋 Plan:
- Screen 1 (List): Pattern A — table with filter, search, pagination
- Screen 2 (Create): Pattern B — drawer slide-in (920px v2)
- Screen 3 (View): Pattern C — drawer 920px with 3 tabs (Overview/Activity/Notes)

🔍 Conflicts: None
🕳️ Gaps Filled: 2 (empty state copy, "Convert" icon)
🛡️ Iron Rule Overrides: 0 (FRD aligned with all rules)

Generating F-01_Prospect.html...
```

**Output:** `F-01_Prospect.html` (single file, ~120KB, all 3 screens via hash routing)
