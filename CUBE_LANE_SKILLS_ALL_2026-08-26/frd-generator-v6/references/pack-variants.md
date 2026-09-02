# Pack Variants — frd-generator-v6

> **Purpose:** ตัดสินใจ LEAN / STANDARD / FULL จาก Brief §3.4 Generator Hints
> **Used by:** Phase 0 (Auto-Detect), Phase 3.5 Section A (verify)

---

## 🎯 Decision Tree

```
Brief §3.4 Generator Hints:
  ├─ complexity: Low | Medium | Critical
  ├─ has-state: Yes | No
  ├─ has-entity: Yes | No
  ├─ has-approval: Yes | No
  └─ multi-tenant / PII / financial flags

START
  │
  ▼
[Q1] complexity == "Critical"?
  YES → FULL ──────────────────────────────────────┐
  NO  → continue                                    │
  │                                                 │
  ▼                                                 │
[Q2] has-state == "Yes" (state machine present)?    │
  YES → FULL ──────────────────────────────────────┤
  NO  → continue                                    │
  │                                                 │
  ▼                                                 │
[Q3] Multi-engine? (estimate ≥ 3 engines)           │
  YES → FULL ──────────────────────────────────────┤
  NO  → continue                                    │
  │                                                 │
  ▼                                                 │
[Q4] has-approval == "Yes" + multi-step approval?   │
  YES → FULL ──────────────────────────────────────┤
  NO  → continue                                    │
  │                                                 │
  ▼                                                 │
[Q5] complexity == "Low" AND has-entity == "No"?    │
  YES → LEAN                                        │
  NO  → STANDARD                                    │
                                                    │
                                                    ▼
                                              FULL = 9 + INDEX
```

---

## 📋 Variant Matrix

| Variant | File count | Trigger pattern | Estimated dev time |
|---|---|---|---|
| **LEAN** | 6 | Simple view / search / single-page feature | 1-3 days |
| **STANDARD** | 7 | CRUD + simple workflow, ≤ 3 APIs, ≤ 3 pages | 1-2 weeks |
| **FULL** | 9 + INDEX | Critical OR state-machine OR multi-engine OR multi-step approval | 2-6 weeks |

---

## 📂 File Lists per Variant

### LEAN (6)
```
00_OVERVIEW.md
01_UI.md
02_API.md
03_LOGIC.md      ⭐ mandatory (Functions only — Engines section says "N/A")
04_DB.md
06_TESTS.md
```
**ไม่มี:** 05_RULES, 07_LOCKED_DECISIONS, INDEX
**เหตุผล:** rules embed ใน 02_API/03_LOGIC ได้ — feature เล็ก ไม่มี LD complex

### STANDARD (7)
```
00_OVERVIEW.md
01_UI.md
02_API.md
03_LOGIC.md      Functions + ≤ 2 Engines OK
04_DB.md
05_RULES.md
06_TESTS.md
```
**ไม่มี:** 07_LOCKED_DECISIONS, INDEX
**เหตุผล:** LD ใส่ใน 00_OVERVIEW §Open Decisions ได้

### FULL (9 + INDEX)
```
00_OVERVIEW.md
01_UI.md
02_API.md
03_LOGIC.md      Functions + 3+ Engines (CUBIC candidate)
04_DB.md
05_RULES.md
06_TESTS.md
07_LOCKED_DECISIONS.md
INDEX.md
```

---

## 🎯 Examples

### Example A: Dashboard with KPI cards (LEAN)
- complexity: Low
- has-state: No
- has-entity: No (read-only)
- pages: 1
- APIs: 1-2 (GET)
- Functions: 1-2 (query builder, formatter)
- Engines: none

→ **LEAN** (6 files)

### Example B: Customer Quick-Add (LEAN)
- complexity: Low
- has-state: No
- has-entity: Yes (create only, no edit/delete)
- pages: 1
- APIs: 1 (POST)
- Functions: 2 (create, validate Thai ID)

→ **LEAN** — borderline แต่ APIs น้อย + ไม่มี state

### Example C: Product CRUD with categories (STANDARD)
- complexity: Medium
- has-state: No
- has-entity: Yes
- pages: 3 (list, detail, edit)
- APIs: 5 (GET list, GET detail, POST, PUT, DELETE)
- Functions: 6
- Engines: 1 (price-calculator)

→ **STANDARD** (7 files)

### Example D: Order with discount + approval (STANDARD/FULL borderline)
- complexity: Medium
- has-state: Yes (draft → submitted → approved)
- has-entity: Yes
- APIs: 6
- Engines: 2 (pricing, discount-applier)

→ **FULL** (มี state-machine → Q2 = YES)

### Example E: Payroll Cycle (FULL)
- complexity: Critical
- has-state: Yes
- has-entity: Yes
- has-approval: Yes (multi-step)
- APIs: 8+
- Engines: 3+ (calculation, tax-rule, payslip-gen)

→ **FULL** (9 + INDEX)

---

## ⚠️ Common Mistakes

### M-1: ใช้ LEAN กับ feature ที่มี state machine
**Wrong:** "Approval feature แค่ 2 หน้า → LEAN"
**Right:** has-state=Yes → FULL (เพราะ state transition rules + audit สำคัญ)

### M-2: ใช้ FULL กับ simple display
**Wrong:** "Dashboard ใหญ่ 10 cards → FULL"
**Right:** ถ้า logic แค่ aggregate query → LEAN

### M-3: ผสม variant กลางทาง
**Wrong:** "ใช้ LEAN แต่เพิ่ม 05_RULES เพราะมี rule เยอะ"
**Right:** ถ้ามี rule เยอะ → upgrade เป็น STANDARD (R5: variant discipline)

---

## 🔄 Upgrade Triggers

ตอนเขียน FRD ถ้าเจอสัญญาณเหล่านี้ → consider upgrade variant:

| Signal | LEAN → STANDARD | STANDARD → FULL |
|---|---|---|
| Functions count | > 5 | > 10 |
| Engines count | ≥ 1 | ≥ 3 |
| APIs count | > 3 | > 6 |
| Business rules | > 5 | > 15 |
| Edge cases | > 3 | > 8 |
| Locked decisions | > 0 | > 3 |
| State transitions | ใดๆ | multi-step |

ถ้า upgrade — กลับ Phase 0 → revise variant → restart Phase 2

---

## Variant Fallback (v6 — ไม่มี Brief §3.4)

งาน WF-01 ปกติไม่มี Brief → ตัดสินจาก BRD เอง (ไม่ถาม user):
- pages = จำนวนหน้าใน §14.6 · states = §8 · approval = §5 COSO · money = §9
- pages ≤2 AND states ≤2 AND ไม่มี approval → **LEAN**
- states ≥4 OR (approval AND money) OR §9.5 มี Engine Management → **FULL**
- อื่น ๆ → **STANDARD**
- Log เหตุผลใน 00_OVERVIEW เสมอ
