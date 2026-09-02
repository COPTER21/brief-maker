# Conflict Resolution

> **Purpose:** When multiple input sources disagree on the same UI/behavior decision, this document defines the priority order and procedure.
> **Used in:** Pipeline Mode (primarily), also Standalone Mode when multi-source.

---

## 🎯 Priority Order (Highest → Lowest)

```
1. ⭐ FRD v4 Pack / 01_UI.md         — Authoritative UI spec
2. ⭐ User explicit override          — "Use drawer not modal" in chat
3. ⭐ Iron Rules (knowledge/iron-rules.md) — Inviolable, override anything else
4.    BRD §14.6 Functions Cut         — Scope lock (IN/OUT)
5.    Brief §3.4 Generator Hints      — Pattern preference, sizing
6.    RIF (Requirement Intake Form)   — Original business intent
7.    BRD/Brief general body          — Context
8.    Inference from screenshot       — Visual reference
9.    Inference from chat history     — Implicit context
10.   Default conventions             — CI defaults, naming, etc.
```

**Rule of thumb:** Higher number = lower priority = override-able by anything above.

---

## ⚠️ Important Exceptions

### Exception A: Iron Rules ALWAYS win

Iron Rules (knowledge/iron-rules.md) **cannot be overridden** by any input — including FRD.

If FRD says "create as modal" but Iron Rule #14 says drawer → use drawer.

**Document the override in output:**
```markdown
## Iron Rule Overrides Applied
- Iron Rule #14: FRD specified modal for Create; applied drawer slide-in instead (CI policy).
```

### Exception B: User chat override is supreme (per session)

If user types in chat "ใช้ drawer แทน modal" → that overrides FRD for the rest of the session.

If user later contradicts themselves, ask:
> "เห็น user เคยบอกใช้ drawer แต่ตอนนี้ขอ modal — ใช้ modal เลยใช่มั้ย?"

### Exception C: Safety-critical sometimes overrides

If FRD spec would create a UX hazard (e.g., delete without confirmation), apply safety:
- Add confirmation modal anyway
- Log: "Added confirmation modal (FRD didn't specify — safety default)"

---

## 🔍 Common Conflict Scenarios

### Conflict 1: Pattern Choice

**Brief says:** "Create modal for new customer"
**FRD 01_UI.md says:** "Create drawer slide-in"
**Iron Rule #14:** "Create/Edit must use drawer slide-in"

**Resolution:**
- FRD aligns with Iron Rule #14 → use drawer ✓
- Brief is overridden (lower priority + conflicts with Iron Rule)
- Log: "Brief mentioned modal; followed FRD + Iron Rule #14 → drawer slide-in"

### Conflict 2: Column Count

**FRD spec:** Table with 10 columns
**Iron Rule #16:** Max 8 columns

**Resolution:**
- Iron Rule wins → use 7 columns visible + Pattern E expandable for hidden 3
- Log: "Iron Rule #16 override: 10 cols → 7 visible + Pattern E (3 cols in expand)"

### Conflict 3: Drawer Width

**Brief §3.4:** "Drawer 640px"
**FRD 01_UI.md:** "Drawer 800px"

**Resolution:**
- Iron Rule #11 wins (SUPREME) → 920px v2 standard — drawer width ไม่ตาม FRD (log override)
- Note: Brief is 1 step lower in priority than FRD
- Log: "FRD said 800px — overridden to 920px per Iron Rule #11 (v2 standard)"

### Conflict 4: Status Names

**FRD:** Status = "active / inactive / suspended / archived"
**Screenshot:** Shows "Open / Closed / On-hold / Done"

**Resolution:**
- FRD wins (higher priority) → use FRD's status names
- If user objects, they can override in chat

### Conflict 5: Visibility of Action Button

**FRD spec:** Edit button visible for all rows
**BRD §14.6:** "Edit is OUT for v1 (read-only)"

**Resolution:**
- BRD §14.6 = scope lock — but BRD is **lower priority than FRD**
- However, "Functions Cut" is a special directive → treat as **scope override** (sibling priority to FRD)
- **Best practice:** Ask user — "FRD shows Edit button, BRD says Edit is cut for v1 — confirm cut?"

---

## 🚨 Conflict Logging Template

In every output, include a section if conflicts were resolved:

```markdown
## ⚠️ Conflicts Resolved

### Conflict 1: Pattern for Create
- **FRD 01_UI.md:** Modal
- **Iron Rule #14:** Drawer slide-in
- **Resolution:** Drawer slide-in (Iron Rule wins)

### Conflict 2: Column count in table
- **FRD 01_UI.md:** 10 columns
- **Iron Rule #16:** Max 8 visible
- **Resolution:** 7 visible + Pattern E (3 in expand)
```

If no conflicts, omit the section.

---

## 🔧 Decision Procedure (when in doubt)

```
1. Identify the disputed item (e.g., "Create pattern")
2. List each source's claim
3. Apply priority order
4. Check Iron Rules — if any rule applies, it wins
5. Generate accordingly
6. Document in output
```

---

## ❌ Don't Do

1. **Don't silently override.** Always document conflicts and resolutions.
2. **Don't fail if conflict found** — pick highest-priority interpretation and continue.
3. **Don't ask user for every conflict** — only ask for genuinely ambiguous ones (e.g., scope conflicts).
4. **Don't apply 50/50 mixes** — pick ONE source per disputed item, not "use modal width but drawer animation".
5. **Don't let Brief override FRD on UI** — Brief is for high-level decisions, FRD is the implementation contract.

---

## 🎯 Special Case: Multi-File FRD Pack Internal Conflicts

If 01_UI.md and 05_RULES.md disagree:
- 01_UI.md wins for **UI/visual decisions**
- 05_RULES.md wins for **validation/behavior decisions**

Example:
- 01_UI.md: Show "Quick Save" button always
- 05_RULES.md: Validation forbids save with empty required fields
- **Resolution:** Show button always (UI), but disable + tooltip when invalid (behavior from rules)

---

## 🛡️ Hard Limits (Never Override)

These cannot be overridden by **any** source:

- **CI colors** — always use CSS variables from `ci-tokens.md`
- **Font** — always Satoshi + Noto Sans Thai
- **Lucide icons** — never replace with emoji
- **Iron Rule #14** — Create/Edit always drawer (not modal)
- **Iron Rule #21** — All icons have w-{N} h-{N}
- **Iron Rule #23** — No color emoji ever
- **Iron Rule #16** — Tables ≤ 8 columns visible

If FRD spec violates these, **silently override** + log + continue.
