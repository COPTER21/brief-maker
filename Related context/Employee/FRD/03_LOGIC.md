# 03_LOGIC — F-EMP-001 Employee Master

> **Audience:** BE dev (business logic layer)
> **Scope:** non-HTTP logic — functions, state transitions, calculations, validations, integrations
> **CUBIC:** §3.1 Functions = scope-local · §3.2 Engines = CUBIC Registry candidate
> **Iron Rule R8:** ทุก mutation API trace ไป ≥1 Function/Engine ใน §3.3 · Function=camelCase · Engine=kebab-case

---

## §3.1 Functions (Scope-Local)

### F-EMP-FN-01: `createEmployeeRecord`
- **Purpose:** สร้าง employee record + sub-lists จาก payload
- **Input:** `{ ...employeeFields, education[], experience[], dependents[], documents[], portfolio[] }`
- **Output:** `{ id, code } | ValidationError[]`
- **Invoked by:** F-EMP-API-03, F-EMP-API-08 (per row)
- **Calls:** F-EMP-FN-03 validateEmployeeData, F-EMP-FN-04 generateEmployeeCode, F-EMP-FN-05 copyAddressIfSame, F-EMP-FN-09 applyPositionDefaults, ENG thai-national-id-validator, ENG address-cascade-resolver
- **Side effects:** INSERT T_employee (+5 sub-tables), status='onboarding', org_snapshot, audit log
- **Error cases:** ERR_VALIDATION, ERR_DUPLICATE_NATIONAL_ID, ERR_CODE_RACE
- **Iron rule check:** ✅ no HTTP terms

### F-EMP-FN-02: `updateEmployee`
- **Purpose:** อัปเดต employee + sub-lists ด้วย optimistic lock
- **Input:** `{ id, version, changedFields, sublistsDiff }`
- **Output:** `EmployeeRecord | ConflictError | ValidationError[]`
- **Invoked by:** F-EMP-API-04
- **Calls:** F-EMP-FN-03, F-EMP-FN-07 detectSensitiveChange, F-EMP-FN-08 checkSupervisorCycle, F-EMP-FN-05, ENG supervisor-cycle-detector, ENG address-cascade-resolver
- **Side effects:** UPDATE T_employee, before/after audit, bump version
- **Error cases:** ERR_VERSION_CONFLICT, ERR_SENSITIVE_CHANGE_NEEDS_APPROVAL, ERR_VALIDATION, ERR_DUPLICATE_NATIONAL_ID
- **Iron rule check:** ✅

### F-EMP-FN-03: `validateEmployeeData`
- **Purpose:** ตรวจ required + format (รวมศูนย์ ใช้ทั้ง create/update/import)
- **Input:** `employeePayload`
- **Output:** `ValidationError[]` (empty = valid)
- **Invoked by:** FN-01, FN-02, FN-14
- **Calls:** ENG thai-national-id-validator (ถ้ามี national_id)
- **Side effects:** none (pure validation)
- **Error cases:** rolls up VR01-VR10
- **Iron rule check:** ✅

### F-EMP-FN-04: `generateEmployeeCode`
- **Purpose:** ออกรหัส `EMP-NNNN` running 4-digit (DB sequence/transaction กัน race)
- **Input:** `{ tenantId }`
- **Output:** `string` (e.g. `EMP-0009`)
- **Invoked by:** FN-01
- **Calls:** — (อ่าน sequence)
- **Side effects:** advance sequence
- **Error cases:** ERR_CODE_RACE (retry on unique violation)
- **Iron rule check:** ✅

### F-EMP-FN-05: `copyAddressIfSame`
- **Purpose:** ถ้า same_addr=true → คัดลอก cur_addr ไป reg_addr (R05)
- **Input:** `{ cur_addr, reg_addr, same_addr }`
- **Output:** `{ cur_addr, reg_addr }`
- **Invoked by:** FN-01, FN-02
- **Side effects:** none (pure transform)
- **Iron rule check:** ✅

### F-EMP-FN-06: `buildEmployeeListQuery`
- **Purpose:** ประกอบ query list จาก filter (q/division/status) + pagination + RLS
- **Input:** `{ tenantId, q?, division_id?, status?, limit, offset }`
- **Output:** `{ sql, params }` / ORM query
- **Invoked by:** F-EMP-API-01, F-EMP-API-09
- **Side effects:** none
- **Iron rule check:** ✅

### F-EMP-FN-07: `detectSensitiveChange`
- **Purpose:** ตรวจว่ามีการแก้ field Restricted (salary/grade/bank/national_id) → ต้อง approval flow
- **Input:** `{ before, after }`
- **Output:** `{ isSensitive:bool, fields:[] }`
- **Invoked by:** FN-02
- **Side effects:** none
- **Iron rule check:** ✅

### F-EMP-FN-08: `checkSupervisorCycle`
- **Purpose:** กัน supervisor = self / circular (R12, E09)
- **Input:** `{ employeeId, supervisorId }`
- **Output:** `boolean (valid)`
- **Invoked by:** FN-02, FN-01
- **Calls:** ENG supervisor-cycle-detector
- **Side effects:** none
- **Iron rule check:** ✅

### F-EMP-FN-09: `applyPositionDefaults`
- **Purpose:** เมื่อเลือก position → เสนอ division/dept อัตโนมัติ (R/E04) + snapshot tier
- **Input:** `{ position_id }`
- **Output:** `{ division_id, dept_id, tier, org_snapshot }`
- **Invoked by:** FN-01, FN-02
- **Side effects:** none (read org masters)
- **Iron rule check:** ✅

### F-EMP-FN-10: `deleteEmployeeGuarded`
- **Purpose:** ลบแบบ soft-delete พร้อม guard linked user (E01)
- **Input:** `{ id }`
- **Output:** `{ deleted:true } | LinkedUserError`
- **Invoked by:** F-EMP-API-05
- **Calls:** F-EMP-FN-11 checkUserLinkage
- **Side effects:** set deleted_at+active=false, audit
- **Error cases:** ERR_EMPLOYEE_HAS_LINKED_USER
- **Iron rule check:** ✅

### F-EMP-FN-11: `checkUserLinkage`
- **Purpose:** ตรวจว่ามี T_user.employee_id ผูกอยู่ไหม
- **Input:** `{ employeeId }`
- **Output:** `{ linked:bool, user? }`
- **Invoked by:** FN-10, F-EMP-API-11, FN-14 (import replace)
- **Side effects:** none
- **Iron rule check:** ✅

### F-EMP-FN-12: `assembleEmployeeProfile`
- **Purpose:** ประกอบ profile object (header + 5 sub-lists + org_snapshot + user_link) + apply masking
- **Input:** `{ employeeId, requesterRole }`
- **Output:** `EmployeeProfile (masked)`
- **Invoked by:** F-EMP-API-02
- **Calls:** ENG pii-masking-engine
- **Side effects:** audit access ถ้าแตะ Restricted (§4.6.5)
- **Iron rule check:** ✅

### F-EMP-FN-13: `captureLifecycleTransition`
- **Purpose:** บันทึก lifecycle (probation result / offboard) + เปลี่ยน status ตาม state machine + set Pre-DOA fields
- **Input:** `{ employeeId, action, payload }`
- **Output:** `{ newStatus } | InvalidTransitionError`
- **Invoked by:** F-EMP-API-06, F-EMP-API-07
- **Calls:** ENG employee-status-machine
- **Side effects:** UPDATE lifecycle+status, audit, approval_chain (Pre-DOA)
- **Error cases:** ERR_INVALID_STATE_TRANSITION, ERR_REASON_REQUIRED
- **Iron rule check:** ✅

### F-EMP-FN-14: `parseEmployeeCsv`
- **Purpose:** parse + validate CSV ทีละแถว, resolve position_code/branch_code → id, รายงานผ่าน/ไม่ผ่าน
- **Input:** `{ csvBuffer, mode }`
- **Output:** `{ rows:[{valid, data|error}], summary }`
- **Invoked by:** F-EMP-API-08
- **Calls:** F-EMP-FN-03, F-EMP-FN-11 (replace mode คง linked-user)
- **Side effects:** none (parse phase)
- **Error cases:** ERR_CSV_FORMAT, ERR_CSV_VALIDATION
- **Iron rule check:** ✅

### F-EMP-FN-15: `buildEmployeeCsvRow`
- **Purpose:** map employee → CSV row (Restricted excluded ถ้าไม่ผ่าน ACL)
- **Input:** `{ employee, requesterRole }`
- **Output:** `string[] (csv cells)`
- **Invoked by:** F-EMP-API-09
- **Calls:** ENG pii-masking-engine
- **Side effects:** none
- **Iron rule check:** ✅

---

## §3.2 Engines (Reusable / CUBIC-Registered)

### F-EMP-ENG-01: `thai-national-id-validator` [NEW]
| Field | Value |
|---|---|
| code | `thai-national-id-validator` |
| name | Thai National ID Validator |
| category | validation |
| status | DRAFT (CUBIC candidate) |
| owner | shared (HR/CRM/Vendor) |
**Input:** `{ nationalId: string }`
**Output:** `{ valid: bool, reason? }`
**Logic Outline:** 1) ตรวจ 13 หลัก 2) คำนวณ checksum หลักที่ 13 (mod 11) 3) return valid
**Used by:** F-EMP-001, (future) Vendor/Customer KYC
**Iron rule check:** ✅ pure, no HTTP, reusable

### F-EMP-ENG-02: `address-cascade-resolver` [NEW]
| Field | Value |
|---|---|
| code | `address-cascade-resolver` |
| name | Thai Address Cascade Resolver |
| category | lookup/derivation |
| status | DRAFT |
| owner | shared |
**Input:** `{ level, parent?, q?, subdistrict? }`
**Output:** `{ options[], zip? }`
**Logic Outline:** 1) คืน list ตาม level (province/district/subdistrict) กรองด้วย parent+q 2) ถ้า subdistrict → derive zip 3) คืน zip (locked)
**Used by:** F-EMP-001, (future) any address feature
**Iron rule check:** ✅ pure (data lookup), reusable

### F-EMP-ENG-03: `supervisor-cycle-detector` [NEW]
| Field | Value |
|---|---|
| code | `supervisor-cycle-detector` |
| name | Supervisor Cycle Detector |
| category | validation/graph |
| status | DRAFT |
| owner | shared (org/hierarchy) |
**Input:** `{ employeeId, supervisorId, edges[] }`
**Output:** `{ hasCycle: bool }`
**Logic Outline:** 1) self check 2) traverse supervisor chain 3) detect revisit → cycle
**Used by:** F-EMP-001, F-ORG-001 (reporting line)
**Iron rule check:** ✅ pure graph

### F-EMP-ENG-04: `pii-masking-engine` [NEW]
| Field | Value |
|---|---|
| code | `pii-masking-engine` |
| name | PII Masking Engine |
| category | security/transform |
| status | DRAFT |
| owner | shared (all PII features) |
**Input:** `{ record, fieldClassificationMap, requesterRole/attributes }`
**Output:** `{ maskedRecord }` (Confidential→`***`/partial, Restricted→excluded/hidden)
**Logic Outline:** 1) อ่าน classification per field 2) เทียบ ABAC (role/attr) 3) mask/exclude 4) flag Restricted access → audit
**Used by:** F-EMP-001, Payroll, CRM
**Iron rule check:** ✅ pure transform (audit side via caller)

### F-EMP-ENG-05: `employee-status-machine` [NEW]
| Field | Value |
|---|---|
| code | `employee-status-machine` |
| name | Employee Lifecycle State Machine |
| category | state-machine |
| status | DRAFT |
| owner | F-EMP-001 (HR shared) |
**Input:** `{ currentStatus, action, payload }`
**Output:** `{ allowed: bool, nextStatus?, reason? }`
**Logic Outline:** validate transition ตามตาราง (§05_RULES §5.6): onboarding→probation→active→leave/suspended→resigned/terminated; block illegal jumps (E14)
**Used by:** F-EMP-001, (future) Onboarding/Offboarding modules
**Iron rule check:** ✅ pure

---

## §3.3 API ↔ Logic Trace Table (Phase 3.5 Anchor)

| API | Calls Functions | Calls Engines |
|---|---|---|
| F-EMP-API-01 GET /employees | FN-06 | ENG-04 (list-safe) |
| F-EMP-API-02 GET /employees/:id | FN-12 | ENG-04 |
| F-EMP-API-03 POST /employees | FN-01, FN-03, FN-04, FN-05, FN-09 | ENG-01, ENG-02 |
| F-EMP-API-04 PUT /employees/:id | FN-02, FN-03, FN-05, FN-07, FN-08 | ENG-01, ENG-02, ENG-03 |
| F-EMP-API-05 DELETE /employees/:id | FN-10, FN-11 | — |
| F-EMP-API-06 POST /:id/probation-result | FN-13 | ENG-05 |
| F-EMP-API-07 POST /:id/offboard | FN-13 | ENG-05 |
| F-EMP-API-08 POST /employees/import | FN-14, FN-01, FN-03, FN-11 | ENG-01, ENG-02 |
| F-EMP-API-09 GET /employees/export | FN-06, FN-15 | ENG-04 |
| F-EMP-API-10 GET /address/cascade | — | ENG-02 |
| F-EMP-API-11 GET /:id/user-link | FN-11 | — |

> **R8 check:** ทุก mutation API (03,04,05,06,07,08) มี ≥1 Function/Engine ✅ · ไม่มี orphan (FN-01..15, ENG-01..05 ถูก trace ครบ) ✅
