# INDEX — FRD F-XX [Feature Name]

> **Variant:** FULL only — STANDARD/LEAN ไม่มี INDEX
> **Audience:** All roles (entry point for navigation)
> **Purpose:** Cross-reference + Function Trace + Quick Nav

---

## 📂 Pack Contents

| # | File | Audience | Size hint |
|---|---|---|---|
| 00 | OVERVIEW.md | All | Meta + Scope + Roles |
| 01 | UI.md | FE dev | Pages + Components |
| 02 | API.md | BE dev (HTTP) | API contracts |
| 03 | LOGIC.md | BE dev (logic) | Functions + Engines |
| 04 | DB.md | DBA / BE | Tables + Fields |
| 05 | RULES.md | BE + QA | Rules + Edge Cases + Errors |
| 06 | TESTS.md | QA | AC + DoD |
| 07 | LOCKED_DECISIONS.md | All | LDs + Convention deviations |

---

## 🔍 Quick Nav by Question

### "ผม FE dev — เริ่มอ่านที่ไหน?"
→ 01_UI.md
→ For action triggers → 01_UI §1.2 (each page action shows API ID)
→ For data shape → 02_API.md response schemas

### "ผม BE dev — สร้าง endpoint ใหม่ — เริ่มที่ไหน?"
→ 02_API.md §2.2 (contract for the endpoint)
→ 03_LOGIC.md §3.3 (which Functions/Engines to call)
→ 04_DB.md (which tables affected)
→ 05_RULES.md (validation + business rules)

### "ผม DBA — schema มีอะไร?"
→ 04_DB.md
→ For RLS/indexes → 04_DB §4.2 per-table
→ For migration → 04_DB §4.4

### "ผม QA — test อะไรบ้าง?"
→ 06_TESTS.md §6.1 (Acceptance Criteria)
→ 05_RULES.md §5.5 (Edge Cases)
→ 06_TESTS.md §6.4 (Definition of Done)

### "ผม PM — มี risk อะไร / Open ที่ยังไม่ปิด?"
→ 00_OVERVIEW.md §0.8 (Open Questions)
→ 07_LOCKED_DECISIONS.md §7.3 (Promoted to LD)

### "ผม Architect — Engine ตัวไหนเป็น CUBIC candidate?"
→ 03_LOGIC.md §3.2 (Engines with status: DRAFT)
→ 07_LOCKED_DECISIONS.md §7.1 (registration timing decisions)

---

## 🔗 Cross-Reference Tables

### Page → API (from 01_UI §1.2)

| Page | Actions | Calls |
|---|---|---|
| P-01 List | row click | F-XX-API-03 |
| P-01 List | filter | F-XX-API-01 |
| P-01 List | export | F-XX-API-07 |
| P-02 Detail | edit | F-XX-API-04 |
| P-02 Detail | submit | F-XX-API-05 |
| P-03 Create | save | F-XX-API-02 |
| P-04 Inbox | approve | F-XX-API-06 |

### API → Logic (from 02_API §2.4 / 03_LOGIC §3.3)

| API | Functions | Engines |
|---|---|---|
| F-XX-API-01 GET /payrolls | F-XX-FN-04 | — |
| F-XX-API-02 POST /payrolls | F-XX-FN-01, F-XX-FN-03 | ENG-005 |
| F-XX-API-03 GET /payrolls/:id | F-XX-FN-04 | — |
| F-XX-API-04 PUT /payrolls/:id | F-XX-FN-05 | ENG-005 |
| F-XX-API-05 POST /payrolls/:id/submit | F-XX-FN-06 | — |
| F-XX-API-06 POST /payrolls/:id/approve | F-XX-FN-07 | — |
| F-XX-API-07 GET /payrolls/export | F-XX-FN-08 | — |

### API → DB (from 02_API §2.2 Side effects)

| API | Reads | Writes |
|---|---|---|
| F-XX-API-01 | T_payroll | — |
| F-XX-API-02 | T_payroll_period, T_employee | T_payroll, T_audit_log |
| F-XX-API-04 | T_payroll | T_payroll, T_audit_log |
| F-XX-API-05 | T_payroll | T_payroll (status update), T_audit_log |
| F-XX-API-06 | T_payroll | T_payroll (status + approver), T_audit_log |

### Engine ↔ Feature (from 03_LOGIC §3.2)

| Engine | Used by | Status |
|---|---|---|
| ENG-005 payroll-calculation-engine | F-04 (this), F-XX (planned) | DRAFT |
| ENG-006 tax-rule-applier | F-04 (this), F-09 (existing) | EXISTING |

---

## 🚨 R8 Verification Matrix

> Phase 3.5 Section C anchor

**Rule:** ทุก mutation API ต้องมี ≥ 1 Function/Engine

| API (mutation) | Functions count | Engines count | ✅/❌ |
|---|---|---|---|
| POST /payrolls | 2 | 1 | ✅ |
| PUT /payrolls/:id | 1 | 1 | ✅ |
| POST /payrolls/:id/submit | 1 | 0 | ✅ |
| POST /payrolls/:id/approve | 1 | 0 | ✅ |

**Rule:** No orphan Function/Engine (declared แต่ไม่ถูก trace)

| Function/Engine | Traced in §3.3? |
|---|---|
| F-XX-FN-01 | ✅ (API-02) |
| F-XX-FN-03 | ✅ (API-02) |
| F-XX-FN-04 | ✅ (API-01, API-03) |
| F-XX-FN-05 | ✅ (API-04) |
| F-XX-FN-06 | ✅ (API-05) |
| F-XX-FN-07 | ✅ (API-06) |
| F-XX-FN-08 | ✅ (API-07) |
| ENG-005 | ✅ (API-02, API-04) |
| ENG-006 | ✅ (via ENG-005 internal) |

---

## 📊 Pack Statistics

| Metric | Count |
|---|---|
| Pages | 4 |
| APIs | 7 |
| Functions | 8 |
| Engines | 2 |
| DB Tables | 3 |
| Business Rules | 4 |
| Edge Cases | 4 |
| Error codes | 12 |
| Locked Decisions | 3 |

---

## 🎯 Reading Order Recommendation

### First-time reader (any role)
1. 00_OVERVIEW → understand scope + roles
2. 01_UI §1.3 Journey → understand user flow
3. Drill down to relevant file based on role

### Onboarding new dev
1. 00_OVERVIEW
2. INDEX (this file)
3. 01_UI (FE) OR 02_API + 03_LOGIC (BE) OR 04_DB (DBA)
4. 05_RULES (constraints)
5. 06_TESTS (acceptance bar)

### Architect review
1. 03_LOGIC §3.2 (Engines — CUBIC candidates)
2. 04_DB (data model)
3. 07_LOCKED_DECISIONS (tradeoffs)
4. INDEX cross-reference matrices

---

## Coverage Manifest Pointer ⭐ v6
- ดู `00_OVERVIEW §0.12` — ทุก BRD requirement → ที่อยู่ใน pack (Phase 3.5 Section K verify)
- Scope Lock: `07_LOCKED §7.0`
