# 02_API — F-EMP-001 Employee Master

> **Audience:** Backend developer (HTTP layer)
> **Purpose:** API contracts — CUBIC API Entity format
> **🚨 Iron Rule:** ห้ามมี business logic >5 บรรทัดที่นี่ — ย้ายไป 03_LOGIC §3.1
> **🚨 R8:** ทุก mutation API ระบุ "Calls (Logic)" → trace ใน 03_LOGIC §3.3
> Auth: JWT + `X-Tenant-Id` (RLS) ทุก endpoint. Roles บังคับผ่าน Policy Center (F-IAM-02)

---

## §2.1 API Overview

| ID | Method | Path | Summary | Auth/Roles |
|---|---|---|---|---|
| F-EMP-API-01 | GET | /api/v1/employees | List + filter + search | HR, Dept Head, IT |
| F-EMP-API-02 | GET | /api/v1/employees/:id | Get profile detail | HR, Dept Head, IT |
| F-EMP-API-03 | POST | /api/v1/employees | Create employee | HR Officer, HR Manager |
| F-EMP-API-04 | PUT | /api/v1/employees/:id | Update employee | HR Officer, HR Manager |
| F-EMP-API-05 | DELETE | /api/v1/employees/:id | Delete (guarded) | HR Manager + Dept Head + IT |
| F-EMP-API-06 | POST | /api/v1/employees/:id/probation-result | บันทึกผลทดลองงาน | HR Manager |
| F-EMP-API-07 | POST | /api/v1/employees/:id/offboard | บันทึกพ้นสภาพ | HR Officer/Manager |
| F-EMP-API-08 | POST | /api/v1/employees/import | นำเข้า CSV | HR, IT |
| F-EMP-API-09 | GET | /api/v1/employees/export | ส่งออก CSV | HR, IT (Export Limit) |
| F-EMP-API-10 | GET | /api/v1/address/cascade | geo lookup (cascade) | authenticated |
| F-EMP-API-11 | GET | /api/v1/employees/:id/user-link | ตรวจ linked user | HR, IT |

---

## §2.2 Per-API Contract

### F-EMP-API-01: GET /api/v1/employees
| Field | Value |
|---|---|
| id | F-EMP-API-01 |
| method/path | GET /api/v1/employees |
| summary | List พนักงาน + filter/search |
| roles | HR, Dept Head (own dept), IT |
**Request — Query:** `q` (รหัส/ชื่อ/ชื่อเล่น), `division_id`, `status`, `limit` (def 20, max 100), `offset`
**Response 200:** `{ data:[{id,code,first_th,last_th,nickname,photo_url,position_name,tier,dept_name,branch_name,user_linked:bool,status}], total, limit, offset }`
**Notes:** Confidential/Restricted fields ไม่ส่งใน list. **Side effects:** read-only.
**Calls (Logic):** F-EMP-FN-06 buildEmployeeListQuery, ENG pii-masking-engine (list-safe) → 03_LOGIC §3.3

### F-EMP-API-02: GET /api/v1/employees/:id
| Field | Value |
|---|---|
| id | F-EMP-API-02 |
| roles | HR, Dept Head, IT (sensitive masked by role) |
**Response 200:** full employee object + sub-lists (education/experience/dependents/documents/portfolio) + org_snapshot + user_link summary. Confidential→mask, Restricted→excluded/hidden ตาม ACL.
**Errors:** 404 ERR_EMPLOYEE_NOT_FOUND, 403 ERR_INSUFFICIENT_ROLE
**Side effects:** read; **access to Restricted fields → audit log** (§4.6.5)
**Calls (Logic):** F-EMP-FN-12 assembleEmployeeProfile, ENG pii-masking-engine

### F-EMP-API-03: POST /api/v1/employees
| Field | Value |
|---|---|
| id | F-EMP-API-03 |
| roles | HR Officer (Maker), HR Manager |
**Request body:** employee fields + sub-lists + lifecycle (recruit/onboard) — ดู 04_DB §4.2
**Response 201:** `{ id, code }` (code = EMP-NNNN)
**Errors:** 400 ERR_VALIDATION (field list), 409 ERR_DUPLICATE_NATIONAL_ID, 409 ERR_CODE_RACE
**Preconditions:** required (first_th,last_th,position_id,branch_id,hire_date,emp_type) — VR01/VR02
**Side effects:** INSERT T_employee (+sub), generate code, audit log, status='onboarding'
**Calls (Logic):** F-EMP-FN-01 createEmployeeRecord (→ FN-03 validate, FN-04 generateEmployeeCode, FN-05 copyAddressIfSame, FN-09 applyPositionDefaults, ENG thai-national-id-validator, ENG address-cascade-resolver) → 03_LOGIC §3.3

### F-EMP-API-04: PUT /api/v1/employees/:id
| Field | Value |
|---|---|
| id | F-EMP-API-04 |
| roles | HR Officer (Maker); sensitive change → HR Manager(Checker)+HR Director(Approver) |
**Request body:** changed fields + `version` (optimistic lock)
**Response 200:** updated object
**Errors:** 400 ERR_VALIDATION, 404 ERR_EMPLOYEE_NOT_FOUND, 409 ERR_VERSION_CONFLICT (E07), 409 ERR_DUPLICATE_NATIONAL_ID, 422 ERR_SENSITIVE_CHANGE_NEEDS_APPROVAL
**Side effects:** UPDATE T_employee, before/after audit (sensitive emphasis), bump version
**Calls (Logic):** F-EMP-FN-02 updateEmployee (→ FN-03 validate, FN-07 detectSensitiveChange, FN-08 checkSupervisorCycle, ENG supervisor-cycle-detector, ENG address-cascade-resolver)

### F-EMP-API-05: DELETE /api/v1/employees/:id
| Field | Value |
|---|---|
| id | F-EMP-API-05 |
| roles | HR Manager + Dept Head + IT (per DOA, Phase 3) |
**Response 200:** `{ deleted:true }` (soft-delete)
**Errors:** 409 ERR_EMPLOYEE_HAS_LINKED_USER (E01/VR08 — block), 404 ERR_EMPLOYEE_NOT_FOUND
**Preconditions:** **ตรวจ linked user ก่อน** (ON DELETE RESTRICT, BR-IAM-07)
**Side effects:** set deleted_at + active=false, audit
**Calls (Logic):** F-EMP-FN-10 deleteEmployeeGuarded (→ FN-11 checkUserLinkage)

### F-EMP-API-06: POST /api/v1/employees/:id/probation-result
| Field | Value |
|---|---|
| roles | HR Manager (Approver) + Dept Head |
**Request:** `{ result: passed|failed|extended, eval_date, evaluator_id, note, new_end_date? }`
**Response 200:** updated status
**Errors:** 422 ERR_INVALID_STATE_TRANSITION (E14), 400 ERR_REASON_REQUIRED (failed/extended — VR09)
**Side effects:** UPDATE probation_* + status (passed→active, failed→terminated, extended→probation), audit, Pre-DOA fields set
**Calls (Logic):** F-EMP-FN-13 captureLifecycleTransition, ENG employee-status-machine

### F-EMP-API-07: POST /api/v1/employees/:id/offboard
| Field | Value |
|---|---|
| roles | HR Officer (Maker) → Dept Head (Approver) |
**Request:** `{ resign_type, resign_submit_date, resign_effective_date, resign_reason, exit_interview_done, rehire_eligible, clearance_status }`
**Response 200:** updated status (resigned/terminated)
**Errors:** 422 ERR_INVALID_STATE_TRANSITION, 400 ERR_VALIDATION
**Side effects:** UPDATE resign_* + status, audit, Pre-DOA chain
**Calls (Logic):** F-EMP-FN-13 captureLifecycleTransition, ENG employee-status-machine

### F-EMP-API-08: POST /api/v1/employees/import
| Field | Value |
|---|---|
| roles | HR, IT |
**Request:** multipart CSV + `mode: merge|replace`
**Response 200:** `{ inserted, updated, skipped, errors:[{row, reason}] }` (preview-then-apply)
**Errors:** 400 ERR_CSV_FORMAT, 422 ERR_CSV_VALIDATION (per-row)
**Side effects:** bulk INSERT/UPDATE; **mode=replace คงพนักงานที่มี linked user** (VR; AC S-06)
**Calls (Logic):** F-EMP-FN-14 parseEmployeeCsv, F-EMP-FN-01 createEmployeeRecord (per row), FN-11 checkUserLinkage

### F-EMP-API-09: GET /api/v1/employees/export
| Field | Value |
|---|---|
| roles | HR, IT — **Export Limit (S02-06)** |
**Request — Query:** filters (เหมือน list)
**Response 200:** CSV stream
**Side effects:** **audit log export** (who/count/filter); Restricted columns excluded unless ACL+approval
**Calls (Logic):** F-EMP-FN-06 buildEmployeeListQuery, F-EMP-FN-15 buildEmployeeCsvRow, ENG pii-masking-engine

### F-EMP-API-10: GET /api/v1/address/cascade
| Field | Value |
|---|---|
| roles | authenticated |
**Request — Query:** `level: province|district|subdistrict`, `parent` (ชื่อระดับบน), `q` (search)
**Response 200:** `{ options:[...], zip? }` (level=subdistrict → คืน zip ด้วย)
**Side effects:** read-only (M_address)
**Calls (Logic):** ENG address-cascade-resolver

### F-EMP-API-11: GET /api/v1/employees/:id/user-link
| Field | Value |
|---|---|
| roles | HR, IT |
**Response 200:** `{ linked:bool, user:{id,username,status}? }`
**Calls (Logic):** F-EMP-FN-11 checkUserLinkage
