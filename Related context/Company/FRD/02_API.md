# 02_API — F-ORG-001 Organization Management

> Audience: BE (HTTP layer only). business logic อยู่ 03_LOGIC. ทุก mutation มี "Calls (Logic)" (R8). `{entity}` ∈ branch|division|department|position. company = singleton (GET/PUT เท่านั้น).

## API Summary
| ID | Method Path | Summary | Calls (Logic) |
|---|---|---|---|
| F-ORG-API-01 | GET /api/v1/org/{entity} | list + search/filter | FN-08 buildListQuery |
| F-ORG-API-02 | GET /api/v1/org/{entity}/:id | detail + related | FN-09 loadDetailWithRelated |
| F-ORG-API-03 | POST /api/v1/org/{entity} | create | FN-01 createRecord, FN-05 validateRecord, FN-07 reseqSiblings |
| F-ORG-API-04 | PUT /api/v1/org/{entity}/:id | update | FN-02 updateRecord, FN-05 validateRecord, FN-07 reseqSiblings |
| F-ORG-API-05 | PATCH /api/v1/org/{entity}/:id/status | toggle active | FN-03 toggleStatus |
| F-ORG-API-06 | DELETE /api/v1/org/{entity}/:id | delete + cascade | FN-04 deleteRecord, **ENG-ORG-03 cascade-resolver** |
| F-ORG-API-07 | POST /api/v1/org/{entity}/import/validate | validate CSV (no write) | FN-10 parseCsv, **ENG-ORG-02 csv-import-validator** |
| F-ORG-API-08 | POST /api/v1/org/{entity}/import/apply | apply import (Replace/Merge) | FN-11 applyImport, ENG-ORG-02, FN-07 |
| F-ORG-API-09 | GET /api/v1/org/{entity}/chart | org chart tree | **ENG-ORG-01 org-tree-builder** |
| F-ORG-API-10 | GET /api/v1/org/{entity}/export | export CSV (BOM) | FN-12 buildCsv |
| F-ORG-API-11 | GET /api/v1/org/company | company detail | FN-09 |
| F-ORG-API-12 | PUT /api/v1/org/company | update company | FN-02, FN-05 |
| F-ORG-API-13 | PUT /api/v1/org/company/logo | อัปโหลด/แทนที่โลโก้บริษัท | FN-13 saveCompanyLogo |
| F-ORG-API-14 | DELETE /api/v1/org/company/logo | ลบโลโก้บริษัท | FN-14 removeCompanyLogo |

## Representative Contracts

### F-ORG-API-03: POST /api/v1/org/{entity}
| Field | Value |
|---|---|
| auth | required | roles | org_admin, senior_admin, admin_manager |
**Request Body:** entity fields (ดู 04_DB §4.2). **Validation:** name_th required; code unique ถ้าระบุ; FK valid; parent ≠ self/descendant; tier ∈ track (≤5 lines else→05_RULES).
**Response 201:** `{ "id":"uuid", "code":"...", "status":"created" }`
**Errors:** 400 ERR_VALIDATION_FAILED · 409 ERR_DUPLICATE_CODE · 422 ERR_CYCLE_DETECTED · 422 ERR_TIER_TRACK_MISMATCH · 403 ERR_INSUFFICIENT_ROLE
**Preconditions:** FK records exist. **Side effects:** INSERT T_{entity}; reseq siblings; Immutable audit log (S01-07).
**Calls (Logic):** FN-01 createRecord → FN-05 validateRecord; FN-07 reseqSiblings (dept/position)

### F-ORG-API-06: DELETE /api/v1/org/{entity}/:id
| Field | Value |
|---|---|
| auth | required | roles | senior_admin, admin_manager (SoD: ≠ creator) |
**Response 200:** `{ "deleted":true, "cascade": {...} }`
**Side effects:** division → set null department.division_id + position.division_id; dept/position → reparent children to parent_id; DELETE row; audit before/after.
**Calls (Logic):** FN-04 deleteRecord → **ENG-ORG-03 cascade-resolver**

### F-ORG-API-07: POST /api/v1/org/{entity}/import/validate
**Request:** multipart CSV + `?mode=replace|merge`. **Response 200:** `{ "ok":N,"fail":M,"total":T,"rows":[{row,code,ok,errs[]}] }` (no write).
**Calls (Logic):** FN-10 parseCsv → **ENG-ORG-02 csv-import-validator**

### F-ORG-API-08: POST /api/v1/org/{entity}/import/apply
**Request:** validated payload + mode. **Response 200:** `{ "imported":N,"mode":"replace|merge" }`.
**Preconditions:** validate ผ่าน ok≥1. **Side effects:** Replace=rebuild entity (เฉพาะ entity นี้) / Merge=upsert by code; reseq; audit. **Calls:** FN-11 applyImport → ENG-ORG-02 (resolve refs) → FN-07

### F-ORG-API-09: GET /api/v1/org/{entity}/chart
**Response 200:** `{ "tree": {...} }` (department: Company→Division→Dept tree; position: reports-to tree). **Calls:** **ENG-ORG-01 org-tree-builder** (coverage-safe, cycle/orphan guard)

### F-ORG-API-13: PUT /api/v1/org/company/logo
| Field | Value |
|---|---|
| auth | required | roles | org_admin, senior_admin, admin_manager |
**Request:** multipart `logo` (image) — PNG/JPG/SVG. **Response 200:** `{ "logo_url": "<ref>" }`
**Preconditions:** mime ∈ config `logo.allowed_mime`; size ≤ config `logo.max_size` (2MB) — BR-14.
**Errors:** 400 `ERR_LOGO_TYPE` (ชนิดไม่รองรับ), 400 `ERR_LOGO_SIZE` (ใหญ่เกิน). **Side effects:** เก็บไฟล์ (Object Storage) → set `company.logo_url`; audit before/after. **Calls (Logic):** FN-13 saveCompanyLogo

### F-ORG-API-14: DELETE /api/v1/org/company/logo
| Field | Value |
|---|---|
| auth | required | roles | org_admin, senior_admin, admin_manager |
**Response 200:** `{ "deleted": true }`
**Side effects:** set `company.logo_url=NULL` (hero กลับเป็นไอคอนเริ่มต้น); ไม่กระทบเอกสาร/รายงานที่ออกไปแล้ว; audit. **Calls (Logic):** FN-14 removeCompanyLogo

> Iron Rules: ไม่มี business logic >5 บรรทัด/calculation/threshold ใน API; cascade/tree/validate = engine; create/update/reseq = function.
