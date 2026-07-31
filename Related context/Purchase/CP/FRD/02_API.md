# 02_API — F-CP-001 เปรียบเทียบราคา (Price Comparison)

> **Audience:** Backend developer (HTTP layer)
> **Purpose:** API contracts — CUBIC API Entity format
> **🚨 Iron Rule:** ห้าม business logic >5 บรรทัดที่นี่ — ย้ายไป 03_LOGIC §3.1
> **🚨 R8:** ทุก mutation API ต้องระบุ "Calls (Logic)" → trace ใน 03_LOGIC §3.3

---

## §2.1 API Overview

| ID | Method | Path | Summary | Auth |
|---|---|---|---|---|
| F-CP-001-API-01 | GET | /api/v1/comparisons | List CP + filters | required |
| F-CP-001-API-02 | GET | /api/v1/comparisons/:id | Get detail (header+lines+quotes+splits) | required |
| F-CP-001-API-03 | POST | /api/v1/comparisons | Create CP (draft/pending) | required (buyer) |
| F-CP-001-API-04 | PUT | /api/v1/comparisons/:id | Update draft (lines/quotes/winners) | required (buyer) |
| F-CP-001-API-05 | POST | /api/v1/comparisons/:id/submit | ส่งเซ็น draft→pending | required (buyer) |
| F-CP-001-API-06 | POST | /api/v1/comparisons/:id/approve | อนุมัติ pending→approved | required (approver) |
| F-CP-001-API-07 | POST | /api/v1/comparisons/:id/reject | ตีกลับ pending→draft | required (approver) |
| F-CP-001-API-08 | POST | /api/v1/comparisons/:id/award | ออกใบสั่งซื้อ approved→awarded (+po_id) | required (proc_manager) |
| F-CP-001-API-09 | GET | /api/v1/comparisons/export | Export CSV | required |
| F-CP-001-API-10 | GET | /api/v1/comparisons/:id/document | PDF เอกสารใบเปรียบเทียบราคา | required |

> **Upstream lookups (อ้าง feature อื่น — ไม่ owned โดย CP):**
> - GET /api/v1/purchase-requisitions?route=cp&status=approved (F-PR-001) — refable PR list
> - GET /api/v1/vendors (Master) — vendor selection
> - GET /api/v1/vendor-prices?vendor_id=&item_code= (Master) — preset price (ดู ENG-03)

---

## §2.2 Per-API Contract

### F-CP-001-API-01: GET /api/v1/comparisons

| Field | Value |
|---|---|
| id | F-CP-001-API-01 |
| method | GET |
| path | /api/v1/comparisons |
| summary | List CP พร้อม filter/sort/pagination |
| auth | required |
| roles | buyer, proc_manager, approver, finance |

**Request — Query params:**
- `search` (optional): match cp_no / buyer / pr_no
- `status` (optional): draft|pending|approved|awarded|cancelled|all
- `sort` (optional): cp_date|cp_no|winner_total (+dir)
- `limit` (default 20, max 100), `offset` (default 0)
- **Headers:** `X-Tenant-Id` (required)

**Response 200:**
```json
{ "data": [ { "id":"uuid","cp_no":"CP-2605-00003","cp_date":"2026-05-27","buyer":"Tadswan Chanyarakskul","item_count":3,"vendor_count":3,"po_count":2,"status":"approved","winner_total":13700.00 } ], "total": 4, "limit": 20, "offset": 0 }
```
**Errors:** 400 ERR_INVALID_QUERY_PARAMS · 401 ERR_NOT_AUTHENTICATED · 403 ERR_INSUFFICIENT_ROLE
**Side effects:** — (read-only)
**Calls (Logic):** F-CP-001-FN-04 buildComparisonListQuery → 03_LOGIC §3.1

---

### F-CP-001-API-02: GET /api/v1/comparisons/:id

| Field | Value |
|---|---|
| id | F-CP-001-API-02 |
| method | GET · path /api/v1/comparisons/:id · auth required |
| roles | buyer, proc_manager, approver, finance |

**Response 200:** header + `lines[]` + `quotes[]` (matrix) + `po_splits[]` (พร้อม po_id) + `pr_refs[]`
**Confidential fields** (unit_price, winner_total, subtotal) → mask ถ้า role ไม่ผ่าน (ดู 05_RULES §5.7 D-CLASS)
**Errors:** 401 · 403 · 404 ERR_NOT_FOUND
**Side effects:** — (read-only; ถ้า Restricted ในอนาคต → audit view)
**Calls (Logic):** F-CP-001-FN-04 (assemble detail)

---

### F-CP-001-API-03: POST /api/v1/comparisons

| Field | Value |
|---|---|
| id | F-CP-001-API-03 · method POST · path /api/v1/comparisons |
| auth | required · roles: buyer |

**Request:**
- **Headers:** `X-Tenant-Id`, `Idempotency-Key` (required)
- **Body:**
  ```json
  { "cp_date":"2026-05-27","buyer_id":"uuid","pr_refs":["PR-2605-00012"],
    "vendors":["V-001","V-003","V-005"],
    "lines":[{"item_code":"PPR-A4","item_name":"กระดาษ A4 80g","qty":50,"unit":"รีม","source_pr_no":"PR-2605-00012"}],
    "quotes":[{"line_no":1,"vendor_id":"V-001","unit_price":125,"is_preset":true,"is_winner":true}],
    "save_mode":"draft" }
  ```
- **Validation (≤5 บรรทัด):** cp_date required date · pr_refs required array ≥1 · vendors array · save_mode ∈ {draft,pending}
  - **Complex validation → 03_LOGIC F-CP-001-FN-05 validateComparisonForSubmit** (เฉพาะ save_mode=pending)

**Response 201:** `{ "id":"uuid","cp_no":"CP-2605-00004","status":"draft","winner_total":0 }`
**Errors:** 400 ERR_VALIDATION_FAILED · 403 · 409 ERR_DUPLICATE_IDEMPOTENCY_KEY · 422 BR_CP_PR_REQUIRED / BR_CP_MIN_VENDORS / BR_CP_WINNER_INCOMPLETE
**Preconditions:** PR ที่อ้าง = approved + route=cp + ยังไม่ถูกใช้ (BR-CP-01, BR-CP-10)
**Side effects:** INSERT T_comparison(+pr_ref+line+quote) · gen cp_no · INSERT T_audit_log · ถ้า pending → emit `cp_submitted_event`
**Calls (Logic):** F-CP-001-FN-01 createComparison · F-CP-001-FN-03 pullLinesFromPR · ENG-01 winner-selection · ENG-02 po-split (preview) · (pending) F-CP-001-FN-06 submitComparison

---

### F-CP-001-API-04: PUT /api/v1/comparisons/:id

| Field | Value |
|---|---|
| id | F-CP-001-API-04 · method PUT · path /api/v1/comparisons/:id |
| auth | required · roles: buyer (own draft) |

**Request:** Headers `If-Match` (updated_at, optimistic lock) · Body = lines/quotes/winners/vendors เหมือน API-03
**Preconditions:** status = draft เท่านั้น (BR-CP-11)
**Response 200:** updated header
**Errors:** 403 · 404 · 409 ERR_STALE_DATA · 422 BR_CP_NOT_EDITABLE (status ≠ draft)
**Side effects:** UPDATE/UPSERT lines+quotes · recompute winner_total/po_count · T_audit_log · version++
**Calls (Logic):** F-CP-001-FN-02 updateComparison · ENG-01 winner-selection · ENG-02 po-split (preview)

---

### F-CP-001-API-05: POST /api/v1/comparisons/:id/submit

| Field | Value |
|---|---|
| id | F-CP-001-API-05 · method POST · path /.../submit |
| auth | required · roles: buyer |

**Preconditions:** status=draft · vendors ≥ 2 · ทุก line มีผู้ชนะ (BR-CP-02, BR-CP-03)
**Response 200:** `{ "id":"uuid","status":"pending","approval_chain":[...] }`
**Errors:** 403 · 409 ERR_STALE_DATA · 422 BR_CP_MIN_VENDORS / BR_CP_WINNER_INCOMPLETE
**Side effects:** status→pending · submitted_at · resolve DOA chain · emit `cp_submitted_event` (notify approver) · T_audit_log
**Calls (Logic):** F-CP-001-FN-05 validateComparisonForSubmit · F-CP-001-FN-06 submitComparison · ENG-04 doa-approval-resolver

---

### F-CP-001-API-06: POST /api/v1/comparisons/:id/approve

| Field | Value |
|---|---|
| id | F-CP-001-API-06 · method POST · path /.../approve |
| auth | required · roles: approver (ตาม DOA) |

**Request:** Headers `If-Match` · Body `{}`
**Preconditions:** status=pending · ผู้เรียกอยู่ในชั้น DOA ปัจจุบัน
**Response 200:** `{ "status":"approved","approved_at":"...","approved_by":"uuid" }`
**Errors:** 403 ERR_INSUFFICIENT_ROLE · 409 ERR_STALE_DATA (EC-01 concurrent) · 422 BR_CP_NOT_PENDING
**Side effects:** status→approved · approved_at/by · emit `cp_approved_event` (notify maker) · T_audit_log
**Calls (Logic):** F-CP-001-FN-07 approveComparison

---

### F-CP-001-API-07: POST /api/v1/comparisons/:id/reject

| Field | Value |
|---|---|
| id | F-CP-001-API-07 · method POST · path /.../reject |
| auth | required · roles: approver |

**Request:** Body `{ "reject_reason":"..." }` (required)
**Preconditions:** status=pending
**Response 200:** `{ "status":"draft","reject_reason":"..." }`
**Errors:** 400 ERR_REASON_REQUIRED · 403 · 422 BR_CP_NOT_PENDING
**Side effects:** status→draft · reject_reason · emit `cp_rejected_event` (notify maker + reason) · T_audit_log
**Calls (Logic):** F-CP-001-FN-08 rejectComparison

---

### F-CP-001-API-08: POST /api/v1/comparisons/:id/award

| Field | Value |
|---|---|
| id | F-CP-001-API-08 · method POST · path /.../award |
| auth | required · roles: proc_manager |

**Request:** Headers `If-Match`, `Idempotency-Key` (required — EC-06) · Body `{}`
**Preconditions:** status=approved · po_splits resolved
**Response 200:**
```json
{ "status":"awarded","po_splits":[{"vendor_id":"V-002","po_id":"PO-2605-00010","subtotal":5170.00}] }
```
**Errors:** 403 · 409 ERR_STALE_DATA / ERR_DUPLICATE_IDEMPOTENCY_KEY · 422 BR_CP_NOT_APPROVED · 502 ERR_PO_CREATE_FAILED (downstream)
**Side effects:** status→awarded · awarded_at · เรียก F-PO-001 สร้าง PO ต่อ split → รับ po_id · UPDATE T_comparison_po_split.po_id · emit `cp_awarded_event` · T_audit_log
**Calls (Logic):** F-CP-001-FN-09 awardComparison · ENG-02 po-split (final payload)

---

### F-CP-001-API-09: GET /api/v1/comparisons/export

| Field | Value |
|---|---|
| id | F-CP-001-API-09 · GET · /.../export · auth required |

**Request:** query เหมือน API-01 (export ตาม filter)
**Response 200:** `text/csv` (UTF-8 BOM) — Confidential columns excluded ถ้า role ไม่ผ่าน
**Side effects:** — (read) · audit export attempt (D-CLASS)
**Calls (Logic):** F-CP-001-FN-10 exportComparisonsCsv

---

### F-CP-001-API-10: GET /api/v1/comparisons/:id/document

| Field | Value |
|---|---|
| id | F-CP-001-API-10 · GET · /.../document · auth required |

**Request:** query `format=pdf` (default)
**Response 200:** `application/pdf` (A4 · Sarabun · CI) — render จาก CP_template.html bind data
**Errors:** 403 · 404
**Side effects:** — (read) · audit (เอกสารมี Confidential pricing)
**Calls (Logic):** F-CP-001-FN-11 buildComparisonDocument

---

## §2.3 Common Concerns

### Idempotency (PR-7)
Mutation APIs (POST create/submit/award) รับ `Idempotency-Key` — cache 24 ชม. · key+body เดิม → cached response · key เดิม body ต่าง → 409

### Optimistic Locking (PR-2)
PUT/approve/reject/award require `If-Match` (updated_at/version) → mismatch = 409 ERR_STALE_DATA

### Multi-Tenant
ทุก endpoint require `X-Tenant-Id` → RLS filter ที่ DB

### Audit Log
ทุก mutation auto-write T_audit_log (actor/action/resource/diff/timestamp) — D9

---

## §2.4 API → Logic Trace (Anchor for R8)

> **Authoritative source:** `03_LOGIC.md §3.3`

| API | Calls Functions | Calls Engines |
|---|---|---|
| F-CP-001-API-01 GET /comparisons | F-CP-001-FN-04 | — |
| F-CP-001-API-02 GET /comparisons/:id | F-CP-001-FN-04 | — |
| F-CP-001-API-03 POST /comparisons | FN-01, FN-03, FN-05(if pending), FN-06(if pending) | ENG-01, ENG-02, ENG-03, ENG-04(if pending) |
| F-CP-001-API-04 PUT /comparisons/:id | FN-02 | ENG-01, ENG-02, ENG-03 |
| F-CP-001-API-05 POST /submit | FN-05, FN-06 | ENG-04 |
| F-CP-001-API-06 POST /approve | FN-07 | — |
| F-CP-001-API-07 POST /reject | FN-08 | — |
| F-CP-001-API-08 POST /award | FN-09 | ENG-02 |
| F-CP-001-API-09 GET /export | FN-10 | — |
| F-CP-001-API-10 GET /document | FN-11 | — |

> **R8 Check:** ทุก mutation row (03/04/05/06/07/08) มี ≥ 1 Function/Engine ✅
