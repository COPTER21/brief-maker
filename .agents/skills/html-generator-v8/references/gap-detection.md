# Gap Detection

> **Purpose:** Identify when input is missing critical information needed for HTML generation, and decide whether to fill with defaults, ask user, or stop.

---

## 🎯 What Counts as a Gap

A **gap** is missing information that prevents generating correct output. Types:

### Type 1: Cosmetic Gap (auto-fill with default)
Missing details that don't affect functionality. Safe to fill silently.

| Gap | Default |
|---|---|
| Icon for action button | Lucide default (edit=pencil, view=eye, delete=trash-2) |
| Empty state copy | "ยังไม่มี <entity>" |
| Sample record count | 10-15 records |
| Avatar gradient | Primary→Teal |
| Status color | Map to nearest semantic (in-progress=blue, done=green) |
| Date format | Thai locale: "18 พ.ค. 2026" |
| Number format | Comma-separated, 2 decimal for currency |

### Type 2: Structural Gap (auto-fill with sensible default + log)
Missing structural details. Fill with default + log in output.

| Gap | Default | Log Required |
|---|---|---|
| Route name | `#/feature-slug` | Yes |
| Validation rules for required field | `required + type-check` | Yes |
| Pagination size | 20 records/page | Yes |
| Module name in breadcrumb | "Module" | Yes |
| Owner of record | "— Unassigned —" | Yes |

### Type 3: Business Logic Gap (must ask or stop)
Missing decisions that affect feature behavior. Cannot guess.

| Gap | Required Info | Action |
|---|---|---|
| What entity is this list? | Entity name (Customer? Prospect?) | **Ask** |
| What statuses exist? | Status list + transitions | **Ask** or default to "active/archived" |
| Who approves? | Approver role/department | **Ask** for approval workflow |
| What columns to show? | Field list | **Ask** if too vague |
| Single or multi-step create? | Step count | Default to single, mention in log |

---

## 🚨 Gap Action Protocol

When gap found:

```
1. Classify gap (Cosmetic / Structural / Business Logic)
2. Apply protocol:
   - Cosmetic → silent default
   - Structural → default + log in output
   - Business Logic → STOP and ask, OR default + log clearly

3. Continue generation
```

---

## 🛑 STOP and Ask — When to Pause

**Pause generation** only when:

1. **Critical business logic gap** that would create wrong feature (e.g., "approval system" but no approvers defined)
2. **Multiple equally-likely interpretations** with very different outputs (e.g., "create" could be 1-step OR 5-step wizard)
3. **Input contradicts itself** (e.g., Brief says "no edit" but FRD shows edit form)

Pause format:
```
🛑 ต้องการข้อมูลเพิ่มก่อนสร้าง:

1. หน้า list นี้แสดง entity อะไร? (Customer / Prospect / Order / Other?)
2. มีกี่ status — แค่ active/inactive หรือมี suspended/archived ด้วย?

(ตอบมาแล้วผมจะทำต่อทันที)
```

**Don't pause** for:
- Single missing detail with obvious default (icon, color)
- Optional features (could add or omit)
- Phrasing/wording (use sensible Thai/English)

---

## 🤖 Action: Default with Loud Log

For **Structural Gaps** that get filled with defaults, **log loudly in output**:

```markdown
## 🕳️ Gaps Filled (Defaults Used — Verify)

| Gap | Default Applied | How to Override |
|---|---|---|
| Module name | "Marketing" | Replace `{{MODULE_NAME}}` in HTML |
| Approver role | "Manager" | Change in `submitDoc()` function |
| Pagination size | 20 records/page | Change `state.pagination.pageSize` initial value |
| Empty state copy | "ยังไม่มี Prospect" | Search/replace in HTML |
```

This way user can quickly fix if defaults don't match intent.

---

## 🔍 Gap Detection Heuristics

### Check 1: Required Fields for Pattern

Each pattern needs minimum info:

| Pattern | Minimum Required Info |
|---|---|
| A (List) | Entity name, ≥3 fields to show, ≥1 status type |
| B (Create/Edit drawer) | Entity name, field list, validation rules |
| C (View drawer) | Entity name, sections to show (Overview at minimum) |
| D (Modal) | Action verb (delete/archive), destructive vs reversible |
| E (Compact + expand) | Visible cols (≤6), expand cols, expand layout |
| F (Toggle modifier) | Toggle name, sub-config fields when ON |
| G (PO-style drawer) | Doc type, line item shape, signers list |
| H (A4 paper) | Doc metadata (no/date/party), line items, totals |
| I (Signature list) | Signer roles, sign order (sequential/parallel) |

### Check 2: Cross-Reference with Patterns

After picking pattern(s), scan whether user provided enough info for each.

### Check 3: Iron Rule Coverage

Are there gaps that would violate Iron Rules?
- No icon specified for action → use Lucide default (Iron Rule #21 satisfied if size class added)
- Color emoji in input → silently swap to Lucide (Iron Rule #23)
- "Create modal" mentioned → silently use drawer (Iron Rule #14)

---

## 📋 Gap Report Template

End every generation with a gap report:

```markdown
## 🕳️ Gap Report

### Cosmetic Gaps (silently filled — no review needed)
- Icon for Edit button: used `pencil`
- Empty state copy: "ยังไม่มี Prospect"
- Pagination size: 20/page

### Structural Gaps (defaults applied — please review)
- Module name: "Marketing" (override: replace `Marketing` in shell)
- Sample record: 12 generated (override: edit `state.records` array)

### Business Logic Gaps Filled (DEFAULTS — verify carefully!)
- Status options: active / inactive / suspended / archived (no other status mentioned)
- Owner field: random assigned (real implementation should auto-assign by login)

### Critical Gaps That Need Confirmation
(none — or list here if any unresolved)
```

---

## 🛠️ Recovery from Wrong Defaults

If user later says "ผิดแล้ว status ผิด" → easy to recover because gaps are logged:

```
User: "Status ควรเป็น new / qualified / converted ไม่ใช่ active/inactive"

Generator: "เห็นแล้ว — เปลี่ยน status enum. รอแป๊บ..."
[Read existing HTML → Find pill mappings → Update CSS classes + sample data → Re-render]
```

Without logs, user has to dig through HTML to find what was used. **Always log.**

---

## ⚠️ Common Gap Mistakes

1. **❌** Silently using "Lorem Ipsum" sample data instead of plausible Thai data
2. **❌** Pausing for every small gap (annoying user) — fill aggressively, log clearly
3. **❌** Choosing 1 of 5 equally-likely interpretations without telling user
4. **❌** Forgetting to log defaults applied (user has to guess what was assumed)
5. **❌** Asking the same question multiple times in different chat turns

---

## 🎯 Priority Order for Gap Resolution

When multiple gaps found:

1. **Critical first:** What entity is this? What's the primary action?
2. **Structural next:** Routes, fields, validation, columns
3. **Cosmetic last:** Icons, colors, sample data, empty copy

If asking user, **ask all critical gaps in one batch** — don't drip-feed questions:

```
🛑 ต้องการข้อมูลเพิ่ม 3 ข้อก่อนสร้าง:

1. Entity name (Customer? Prospect? Order?)
2. Status list (ใช้ active/inactive หรือมีอีก?)
3. Pattern แบบไหน (table list + drawer แบบมาตรฐาน?)

ตอบมาแล้วทำให้เลย
```

Better than 3 separate turns asking each question.
