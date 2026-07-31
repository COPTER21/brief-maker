# Example: FULL Variant Walkthrough — F-04 Payroll Cycle

> **Purpose:** Concrete FULL example — แสดง 9 files + INDEX + cross-references
> **Scenario:** Payroll Cycle — 4 pages, 7 APIs, 8 functions, 2 engines, multi-step approval

---

## Input Summary

**Brief §3.4:**
- complexity: Critical
- has-state: Yes (draft → submitted → approved → paid)
- has-entity: Yes (Payroll)
- has-approval: Yes (manager → finance approver → admin)
- multi-tenant: Yes
- PII: Yes (employee data)
- financial: Yes

**BRD §14.6 Screen Inventory (หยาบ):**
- 4 pages
- ERP feature with sidebar
- Layouts: A (List+Drawer), B (Detail), C (Wizard), H (Approver Inbox tab)

**Phase 0 decision:** **FULL** (9 + INDEX)
**Trigger:** complexity=Critical AND has-state=Yes AND multi-engine

---

## Generated Pack Structure

```
FRD_F-04_Pack/
├── 00_OVERVIEW.md          (~150 lines)
├── 01_UI.md                (~400 lines)
├── 02_API.md               (~500 lines, 7 endpoints)
├── 03_LOGIC.md             (~450 lines, 8 FN + 2 ENG + trace)
├── 04_DB.md                (~300 lines, 3 tables + relations)
├── 05_RULES.md             (~350 lines, 4 BR + 4 EC + 12 errors + 6 D-domains)
├── 06_TESTS.md             (~400 lines, 10 AC + DoD + WebSocket)
├── 07_LOCKED_DECISIONS.md  (~150 lines, 3 LD + 0 CD + 2 AT)
└── INDEX.md                (~250 lines, all cross-refs)
```

---

## Phase 2.5 — Edge Case Probes Activated

ตาม trigger pattern:
- **PR-1 Concurrency** ← "approval"
- **PR-3 Permission Mid-flight** ← "approval"
- **PR-7 Idempotency** ← "submit/create"
- **PR-9 Race Condition** ← "financial"

→ User asked 4 questions, all answered, integrated into:
- 05_RULES.md §5.5 (4 edge cases EC-01 to EC-04)
- 03_LOGIC.md §3.1 (FN-06 submitOrder, FN-07 approveOrder with concurrency logic)
- 02_API.md §2.3 (Idempotency-Key + If-Match patterns)
- 07_LOCKED_DECISIONS.md §7.1 (LD-01 optimistic locking)

---

## File Highlights

### 03_LOGIC.md — Heart of FULL Pack

```markdown
## §3.1 Functions (Scope-Local) — 8 functions

F-04-FN-01: createPayrollRecord
F-04-FN-02: updatePayrollRecord
F-04-FN-03: validatePayrollData
F-04-FN-04: buildPayrollListQuery
F-04-FN-05: deletePayrollRecord (soft-delete)
F-04-FN-06: submitOrder (state transition + notification orchestration)
F-04-FN-07: approveOrder (concurrent-safe with version check)
F-04-FN-08: exportPayrollCSV

## §3.2 Engines (Reusable) — 2 engines

ENG-005: payroll-calculation-engine [NEW]
  - category: financial-calculation
  - status: DRAFT (register Phase 2 — see LD-02)
  - Used by: F-04 (this), F-XX (planned)
  - Calculates: gross_pay, net_pay, tax_amount, breakdown[]

ENG-006: tax-rule-applier [EXISTING]
  - category: financial-calculation
  - status: REGISTERED (from F-09 Tax Reporting)
  - Reused as-is — just add F-04 to "Used by" list
  - See LD-03

## §3.3 API ↔ Logic Trace Table

| API | Method | Functions | Engines |
|---|---|---|---|
| F-04-API-01 | GET /payrolls | F-04-FN-04 | — |
| F-04-API-02 | POST /payrolls | F-04-FN-01, F-04-FN-03 | ENG-005 (via FN-01) |
| F-04-API-03 | GET /payrolls/:id | F-04-FN-04 | — |
| F-04-API-04 | PUT /payrolls/:id | F-04-FN-02 | ENG-005 (recalc) |
| F-04-API-05 | POST /payrolls/:id/submit | F-04-FN-06 | — |
| F-04-API-06 | POST /payrolls/:id/approve | F-04-FN-07 | — |
| F-04-API-07 | GET /payrolls/export | F-04-FN-08 | — |

R8 Check: ✅ All 5 mutation APIs have ≥ 1 Function/Engine
```

---

### Why Engines Got Separated

**Without v5 (v4 behavior):**
```
02_API.md POST /payrolls:
  "...calculate gross/net pay including tax brackets, validate against
   labor law overtime limits..."
  ← business logic + calculation mixed with API spec
```

**v5 result:**
```
02_API.md POST /payrolls:
  Calls (Logic): F-04-FN-01, F-04-FN-03, ENG-005

03_LOGIC §3.1:
  F-04-FN-01 createPayrollRecord (orchestrate steps)
  F-04-FN-03 validatePayrollData (call ENG-006 for tax rules)

03_LOGIC §3.2:
  ENG-005 payroll-calculation-engine (pure math)
  ENG-006 tax-rule-applier (REUSED from F-09)
```

→ Architect can extract ENG-005 to CUBIC Registry independently
→ Tax rule changes propagate via ENG-006 (single source)

---

## Phase 3.5 Verification Report (sample output)

```markdown
## 🔍 Phase 3.5 Verification — FRD F-04

### A. Pack Completeness
- [x] Variant = FULL match Brief §3.4 ✅
- [x] All 9 files + INDEX generated ✅
- [x] 03_LOGIC.md exists (mandatory) ✅
- [x] INDEX.md cross-references all files ✅

### B. Function/API Coverage
- [x] All 7 APIs have Contract Block complete ✅

### C. R8 Logic Traceability ⭐
- [x] All 5 mutation APIs have ≥ 1 Function/Engine in trace ✅
- [x] All 8 Functions traced to at least 1 API ✅
- [x] All 2 Engines traced (ENG-005 via FN-01, FN-02; ENG-006 via ENG-005) ✅
- [x] No orphan Function/Engine ✅

### D. API ↔ DB Linkage
- [x] T_payroll, T_payroll_period, T_payroll_deduction all referenced ✅

### E. UI ↔ API Cross-reference
- [x] All 4 pages reference valid APIs ✅

### F. Engine Iron Rules (CUBIC 3-layer)
- [x] No Engine references HTTP terms ✅
- [x] Engine I/O = pure objects ✅
- [x] No UI→Engine bypass ✅

### G. Logic Placement Compliance ⭐
- [x] No CRUD function hiding in 02_API ✅
- [x] No pure calculation in 02_API ✅
- [x] No constants/thresholds in 02_API (all in 05_RULES) ✅

### H. Security Bible Application
- [x] D2, D5, D7, D9, D15, D17 all applied in 05_RULES ✅

### I. Convention Compliance
- [x] API paths: /api/v1/payrolls ✅
- [x] Field keys snake_case ✅
- [x] Function codes camelCase ✅
- [x] Engine codes kebab-case ✅
- [x] Error codes UPPER_SNAKE ✅

### Verdict
✅ ALL CHECKS PASSED → ready to deliver Pack
```

---

## What This Pack Enables (Downstream)

### html-generator-v4
- Reads 01_UI.md → renders 4 pages with Layout IDs
- Knows all API endpoints from 02_API.md
- Doesn't need to read 03_LOGIC (logic = backend concern)

### ai-testcase-md-generator + qa-friendly-html-generator (SOW3.5)
- Reads 06_TESTS.md for AC structure
- Reads 03_LOGIC §3.1 Side effects → derive integration test scenarios
- Reads 05_RULES.md edge cases → derive negative test cases
- Reads 02_API.md → derive contract tests

### Dev hand-off
| Dev role | Primary file | Secondary |
|---|---|---|
| FE dev | 01_UI.md | 02_API (data shape) |
| BE dev (HTTP) | 02_API.md | 03_LOGIC §3.3 trace |
| BE dev (logic) | 03_LOGIC.md | 05_RULES, 04_DB |
| DBA | 04_DB.md | — |
| QA | 06_TESTS.md | 05_RULES (edge cases) |
| Architect | 03_LOGIC §3.2 + 07_LD | INDEX cross-refs |
| PM | 00_OVERVIEW + INDEX | 07_LD (tradeoffs) |

---

## 🎯 Key Differences vs v4 of same feature

| Aspect | v4 output | v5 output |
|---|---|---|
| File count | 8 + INDEX | 9 + INDEX |
| Logic location | 03_ENGINE.md (Engines only) | 03_LOGIC.md (Functions + Engines) |
| Function `createPayrollRecord` | Hidden in 02_API "Engine Logic" section | Explicit in 03_LOGIC §3.1 F-04-FN-01 |
| BE dev confusion | "Where's the create logic spec?" | Clear: 03_LOGIC §3.1 |
| Refactor to CUBIC | Hard — Functions vs Engines unclear | Easy — §3.1 stays scope-local, §3.2 = CUBIC |
| Phase 3.5 R8 check | ❌ Not present | ✅ Catches hidden logic |

---

## 🚨 Anti-Patterns Caught by v5

In drafting this Pack, the skill (v5) would have flagged these if BA tried:

1. **BA wrote in 02_API:** "Calculate net pay using tax brackets..."
   → Skill: "❌ Pure calculation → move to 03_LOGIC §3.2 ENG-005"

2. **BA wrote in 03_LOGIC §3.1:** "F-04-FN-99: calculateBonusMultiplier" (no API calls it)
   → Skill Phase 3.5 Section C: "❌ Orphan Function — no API trace"

3. **BA wrote in 02_API:** "MAX_OVERTIME_HOURS = 36"
   → Skill: "❌ Constant → move to 05_RULES BR-PAY-03"

4. **BA declared ENG-005 without status:**
   → Skill: "⚠️ Engine must specify status (DRAFT/REGISTERED) per cubic-schema-templates"
