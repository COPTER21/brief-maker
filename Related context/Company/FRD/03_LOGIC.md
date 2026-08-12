# 03_LOGIC — F-ORG-001 Organization Management

> Audience: BE (business logic). Functions = scope-local; Engines = reusable/CUBIC. ทุก mutation API trace ที่ §3.3 (R8).

## §3.1 Functions (Scope-Local) — camelCase

### F-ORG-FN-01: createRecord
- **Purpose:** สร้าง master record (branch/division/department/position/company) จาก validated payload
- **Input:** `{ entity, payload }` · **Output:** `Record | ValidationError[]`
- **Invoked by:** API-03, API-12 · **Calls:** FN-05, FN-06 (genCode ถ้าไม่ระบุ)
- **Side effects:** INSERT T_{entity}; audit log · **Iron:** ✅ no HTTP

### F-ORG-FN-02: updateRecord
- **Purpose:** แก้ไข record + จัดการเปลี่ยน parent (reseq) · **Input:** `{ entity, id, payload }` · **Output:** `Record | Error`
- **Invoked by:** API-04, API-12 · **Calls:** FN-05; FN-07 ถ้า parent เปลี่ยน · **Side:** UPDATE + audit before/after

### F-ORG-FN-03: toggleStatus
- **Purpose:** สลับ active/inactive · **Input:** `{ entity, id }` · **Output:** `Record` · **Invoked by:** API-05 · **Side:** UPDATE active + audit

### F-ORG-FN-04: deleteRecord
- **Purpose:** orchestrate ลบ — เรียก cascade engine แล้ว DELETE · **Input:** `{ entity, id }` · **Output:** `{ deleted, cascade }`
- **Invoked by:** API-06 · **Calls:** **ENG-ORG-03** (คำนวณ mutation) · **Side:** apply mutations + DELETE + audit (ใน transaction เดียว)

### F-ORG-FN-05: validateRecord
- **Purpose:** ตรวจ name_th required, code unique, FK valid, parent ≠ self/descendant, tier ∈ track · **Input:** `{ entity, payload }` · **Output:** `Error[]`
- **Invoked by:** FN-01, FN-02 · **Calls:** — (อ่าน 05_RULES BR-*)

### F-ORG-FN-06: genCode
- **Purpose:** สร้างรหัสอัตโนมัติ (DIV-/DEP-/POS- + running; branch zero-pad) ผ่าน Document Numbering service · **Input:** `{ entity }` · **Output:** `code` · **Invoked by:** FN-01 (R11)

### F-ORG-FN-07: reseqSiblings
- **Purpose:** จัด seq ของพี่น้องใหม่หลัง add/move/import (dept/position) · **Input:** `{ entity, parent_id }` · **Output:** `void` · **Invoked by:** FN-01, FN-02, FN-11

### F-ORG-FN-08: buildListQuery
- **Purpose:** สร้าง query list + search/filter(status) + RLS · **Input:** `{ entity, filters }` · **Output:** `Record[]` · **Invoked by:** API-01

### F-ORG-FN-09: loadDetailWithRelated
- **Purpose:** โหลด record + ตารางที่เกี่ยวข้อง (เช่น division→depts+positions) + mask Confidential/Restricted ตาม role · **Input:** `{ entity, id, role }` · **Output:** `{ record, related }` · **Invoked by:** API-02, API-11

### F-ORG-FN-10: parseCsv
- **Purpose:** parse CSV (BOM strip, quote-aware) → rows · **Input:** `csvText` · **Output:** `string[][]` · **Invoked by:** API-07

### F-ORG-FN-11: applyImport
- **Purpose:** apply ผล validate (Replace=rebuild entity / Merge=upsert by code) + resolve refs → id + reseq · **Input:** `{ entity, validatedRows, mode }` · **Output:** `{ imported }` · **Invoked by:** API-08 · **Calls:** ENG-ORG-02 (ref resolve), FN-07 · **Side:** bulk INSERT/UPDATE/DELETE (transaction) + audit

### F-ORG-FN-12: buildCsv
- **Purpose:** สร้าง CSV (UTF-8 BOM, refs เป็น code, exclude Restricted/Confidential ตาม role) · **Input:** `{ entity, role }` · **Output:** `csvText` · **Invoked by:** API-10

### F-ORG-FN-13: saveCompanyLogo
- **Purpose:** validate ชนิด/ขนาดไฟล์ (จาก config `logo.allowed_mime`/`logo.max_size`) → เก็บไฟล์ (Object Storage) → set `company.logo_url` (R14/BR-14) · **Input:** `{ file }` · **Output:** `{ logo_url }` · **Invoked by:** API-13 · **Side:** PUT object + UPDATE company.logo_url + audit before/after · **Errors:** ERR_LOGO_TYPE, ERR_LOGO_SIZE

### F-ORG-FN-14: removeCompanyLogo
- **Purpose:** ลบโลโก้ → set `company.logo_url=NULL` (ไม่กระทบเอกสาร/รายงานที่ออกไปแล้ว) · **Input:** `—` · **Output:** `{ deleted:true }` · **Invoked by:** API-14 · **Side:** UPDATE company.logo_url=NULL + audit

## §3.2 Engines (Reusable / CUBIC-Registered)

### F-ORG-ENG-01: org-tree-builder  [NEW]
| Field | Value |
|---|---|
| code | `org-tree-builder` | category | hierarchy-traversal |
| input | `{ rows[], mode: 'department'|'position', divisions?[] }` |
| output | `{ tree, coverage: {shown, total} }` |
**Logic outline:** (1) department mode: Company→Division node→top-dept(parent null)→sub-dept(recurse); dept ไม่มี division → ใต้ Company. (2) position mode: reports-to roots→recurse. (3) **coverage-pass:** node ที่ยังไม่ถูกแสดง (cycle/orphan) → promote เป็น root. (4) visited-guard กัน infinite loop.
**Used by:** F-ORG (dept+position chart); reusable feature อื่นที่มี adjacency tree · **Iron:** ✅ pure, no HTTP/DB I/O (รับ rows มาแล้ว)

### F-ORG-ENG-02: csv-import-validator  [NEW]
| Field | Value |
|---|---|
| code | `csv-import-validator` | category | data-import-validation |
| input | `{ entity, rows[], mode, masters: {division,branch,dept,position codes} }` |
| output | `{ ok, fail, total, rows:[{row,code,ok,errs[]}], resolvedRefs }` |
**Logic outline:** ตรวจ required(name_th), enum(track/tier), ref resolve (cross-entity ↔ existing; same-entity parent ↔ batch[Replace] / batch∪existing[Merge]), no self-ref, code dup ใน batch. resolve code→id map สำหรับ apply.
**Used by:** F-ORG (div/dept/pos import); reusable master-import อื่น · **Iron:** ✅ pure

### F-ORG-ENG-03: cascade-resolver  [NEW]
| Field | Value |
|---|---|
| code | `cascade-resolver` | category | referential-integrity |
| input | `{ entity, id, graph }` | output | `{ mutations:[{table,op,field,value,ids[]}] }` |
**Logic outline:** division → null department.division_id + position.division_id ที่อ้าง id; department/position → reparent children (parent_id := deleted.parent_id). คืนชุด mutation ให้ FN-04 apply ใน transaction.
**Used by:** F-ORG delete; reusable cascade อื่น · **Iron:** ✅ pure (คำนวณ mutation ไม่เขียน DB เอง)

## §3.3 API ↔ Logic Trace Table (R8 Anchor)
| API | Functions | Engines |
|---|---|---|
| API-01 GET list | FN-08 | — |
| API-02/11 GET detail/company | FN-09 | — |
| API-03 POST create | FN-01, FN-05, FN-06, FN-07 | — |
| API-04/12 PUT update | FN-02, FN-05, FN-07 | — |
| API-05 PATCH status | FN-03 | — |
| API-06 DELETE | FN-04 | **ENG-ORG-03** |
| API-07 import/validate | FN-10 | **ENG-ORG-02** |
| API-08 import/apply | FN-11, FN-07 | **ENG-ORG-02** |
| API-09 GET chart | — | **ENG-ORG-01** |
| API-10 GET export | FN-12 | — |
| API-13 PUT company/logo | FN-13 | — |
| API-14 DELETE company/logo | FN-14 | — |
> R8: ทุก mutation API (03,04,05,06,08,12,13,14) มี ≥1 Function/Engine ✅ · ไม่มี orphan (ทุก FN/ENG ถูก trace) ✅
