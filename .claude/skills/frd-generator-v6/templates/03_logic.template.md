# 03_LOGIC — F-XX [Feature Name]

> **Audience:** BE dev (business logic layer)
> **Scope:** All non-HTTP business logic — pure functions, calculations, validations, integrations
> **CUBIC alignment:** §3.1 Functions = scope-local · §3.2 Engines = candidate for CUBIC Registry
> **Iron Rule R8:** ทุก mutation API ต้อง trace ไปที่ ≥ 1 Function/Engine ใน §3.3

---

## §3.1 Functions (Scope-Local)

> Logic ที่ใช้ใน feature นี้เท่านั้น
> Pattern: createX, updateX, validateX (complex), formatX, orchestrateX
> Naming: camelCase

---

### F-XX-FN-01: `<functionName>`

- **Purpose:** [ทำอะไร, ใช้ทำไม — 1-2 ประโยค]
- **Input:**
  ```
  {
    <field>: <type>,
    ...
  }
  ```
- **Output:** `<type | union>` — เช่น `PayrollRecord | ValidationError[]`
- **Invoked by:** [API ID, page action, หรือ function อื่น]
- **Calls:** [F-XX-FN-NN list, ENG-NNN list, หรือ "—"]
- **Side effects:**
  - INSERT/UPDATE/DELETE table T_xxx
  - Emit event xxx_event
  - Audit log entry
- **Error cases:** [ERR_CODE list ที่จะ throw — ดู 05_RULES §x]
- **Iron rule check:** ✅ no HTTP terms (req/res/header/status)

---

### F-XX-FN-02: `<functionName>`

[Repeat structure]

---

## §3.2 Engines (Reusable / CUBIC-Registered)

> Logic ที่ pure / reusable / substantial — candidate สำหรับ CUBIC Registry
> Naming: kebab-case
> Format: CUBIC Engine Entity schema

> **Note (LEAN variant):** ถ้า feature ไม่มี engine → เขียน:
> ```
> > ไม่มี engine ใน feature นี้ — logic ทั้งหมดเป็น scope-local Functions ใน §3.1
> ```

---

### ENG-NNN: `<engine-code>` [NEW | EXISTING]

| Field | Value |
|---|---|
| **id** | (assigned at CUBIC registration) |
| **code** | `<engine-code>` |
| **name** | [Human-readable name] |
| **category** | financial-calculation / validation / integration / generation / matcher |
| **status** | DRAFT (in this FRD) / REGISTERED (already in CUBIC) |
| **owner** | F-XX (this feature) / shared |

**Input Schema:**
```json
{
  "field": "type",
  ...
}
```

**Output Schema:**
```json
{
  "field": "type",
  ...
}
```

**Logic Outline:**
1. Step 1: ...
2. Step 2: ...
3. Step 3: ...

**Used by features:**
- F-XX (current — this FRD)
- F-YY (planned / existing)

**Iron rule check:**
- [ ] ✅ Pure — no I/O direct, no HTTP terms
- [ ] ✅ Reusable — 2+ features (current + planned)
- [ ] ✅ Substantial — logic > 20 lines OR named algorithm

**CUBIC Registration note:**
- [ ] DRAFT → ต้อง register ผ่าน CUBIC Registry ตอน dev hand-off
- [ ] EXISTING → reuse engine ID ที่มีอยู่: `<engine-uuid>`

---

### ENG-NNN+1: ...

[Repeat structure]

---

## §3.3 API ↔ Logic Trace Table (R8 Anchor)

> **MANDATORY** — Phase 3.5 Section C จะตรวจตารางนี้
> ทุก mutation API (POST/PUT/PATCH/DELETE) ต้องมีอย่างน้อย 1 Function/Engine
> GET ที่ trivial (single table read) อาจไม่มี logic — mark `—`

| API ID | Method | Path | Calls Functions | Calls Engines |
|---|---|---|---|---|
| F-XX-API-01 | GET | /payrolls | F-XX-FN-04 (filter) | — |
| F-XX-API-02 | POST | /payrolls | F-XX-FN-01 (create), F-XX-FN-03 (validate) | ENG-005 (calculate) |
| F-XX-API-03 | PUT | /payrolls/:id | F-XX-FN-05 (update) | ENG-005 (recalculate) |
| F-XX-API-04 | POST | /payrolls/:id/submit | F-XX-FN-06 (orchestrate) | — |
| F-XX-API-05 | DELETE | /payrolls/:id | F-XX-FN-07 (soft-delete) | — |

### Trace Verification (Self-Check)

- [ ] **Every mutation API** has ≥ 1 Function/Engine in trace
- [ ] **No orphan Function** — every FN-NN in §3.1 appears in trace
- [ ] **No orphan Engine** — every ENG-NNN in §3.2 appears in trace (directly or via Function)
- [ ] **No "hidden logic" in 02_API** — all business logic traced here

---

## §3.4 Dependencies (Optional — for complex features)

> ถ้า feature มี logic เรียก feature/module อื่น → list ที่นี่

### External Function/Engine called
- `f-yy-fn-12 lookupCustomer` from F-YY (Customer Master)
- `ENG-002 thai-id-validator` from CUBIC Registry (existing)

### External Function/Engine that calls into this feature
- F-ZZ uses `ENG-005 payroll-calculation-engine` (if registered)

---

## §3.5 Open Questions / Locked Decisions Referenced

ระบุ LD ใน 07_LOCKED_DECISIONS.md ที่เกี่ยวกับ logic:

- LD-03: Engine ENG-005 จะ register CUBIC ใน Phase 2 ของ dev (not this sprint)
- LD-07: validateXxx เลือก scope-local ไม่ใช่ shared (เพราะ business rule ต่างจาก F-YY)

---

## Audience Cheat-Sheet

| Reader | Read sections |
|---|---|
| BE dev | §3.1 + §3.2 + §3.3 (all) |
| BE dev (HTTP layer) | §3.3 + relevant §3.1/§3.2 entries |
| QA | §3.3 + §3.1 Side effects + §3.2 Input/Output |
| DBA | §3.1 Side effects (DB ops only) |
| Architect / CUBIC owner | §3.2 + §3.4 + §3.5 |
| PM | §3.3 (table only) — coverage view |
