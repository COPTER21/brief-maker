# 02_API — F-PAY Payment Term (เงื่อนไขการชำระเงิน)

> **Audience:** Backend developer (HTTP layer)
> **Purpose:** API contracts (CUBIC API Entity) + Cross-Module Contract
> **🚨 Iron Rule:** ห้ามมี business logic >5 lines ที่นี่ — ย้ายไป 03_LOGIC §3.1
> **🚨 R8:** ทุก mutation API ต้องระบุ "Calls (Logic)" → trace ใน 03_LOGIC §3.3
> **Note:** HTML prototype = mock synchronous (client-side). API ด้านล่าง = production design (server-side mirror ของ `submitTerm()` validations — Control C4).

---

## §2.1 API Overview

| ID | Method | Path | Summary | Auth |
|---|---|---|---|---|
| F-PAY-API-01 | GET | /api/v1/payment-terms | List + filter (search/type/status) | required |
| F-PAY-API-02 | POST | /api/v1/payment-terms | Create term | required (Finance Admin) |
| F-PAY-API-03 | GET | /api/v1/payment-terms/:id | Get detail | required |
| F-PAY-API-04 | PUT | /api/v1/payment-terms/:id | Update (แม้ used>0) | required (Finance Admin) |
| F-PAY-API-05 | PATCH | /api/v1/payment-terms/:id/status | เปลี่ยนสถานะเดี่ยว (view menu) | required (Finance Admin) |
| F-PAY-API-06 | POST | /api/v1/payment-terms/bulk-status | Bulk set status | required (Finance Admin) |
| F-PAY-API-07 | POST | /api/v1/payment-terms/bulk-delete | Bulk delete (guard used>0 → skip) | required (Finance Admin) |
| F-PAY-API-08 | GET | /api/v1/payment-terms/active | Downstream picker (active only) | required (any consumer) |

> **ไม่มี** endpoint: single-delete, CSV import/export, approve/submit (DOA null), archive/reactivate (dead path). ดู 05_RULES BR-09 + §7 SCOPE_LOCK.

---

## §2.2 Per-API Contract

### F-PAY-API-01: GET /api/v1/payment-terms
| Field | Value |
|---|---|
| **id** | F-PAY-API-01 |
| **method** | GET |
| **summary** | List payment terms with filters |
| **auth** | required · roles: Finance Admin, Finance Viewer |

**Request — Query params:** `search` (code/name/name_en, optional) · `type` (7 enum | all) · `status` (draft/active/inactive | all) · `limit` (default 20, max 100) · `offset`. **Headers:** `X-Tenant-Id`.

**Response 200:**
```json
{
  "data": [
    { "id":"uuid","code":"NET30","name":"เครดิต 30 วัน","name_en":"Net 30",
      "type":"credit","trigger":"immediate","due_basis":"invoice_date",
      "net_days":30,"is_default":true,"status":"active","used":186,
      "summary":"ครบกำหนด 30 วัน" }
  ],
  "counts": { "all": 12, "active": 9, "inactive": 1, "draft": 2 },
  "total": 12, "limit": 20, "offset": 0
}
```
**Errors:** 400 ERR_INVALID_QUERY_PARAMS · 401 ERR_NOT_AUTHENTICATED · 403 ERR_INSUFFICIENT_ROLE
**Side effects:** — (read-only) · **Calls (Logic):** F-PAY-FN-04 buildTermListQuery, F-PAY-FN-10 buildTermSummary (per row)

---

### F-PAY-API-02: POST /api/v1/payment-terms
| Field | Value |
|---|---|
| **id** | F-PAY-API-02 |
| **method** | POST |
| **summary** | Create new payment term |
| **auth** | required · roles: Finance Admin · Idempotency-Key required (AD-04) |

**Request — Body:**
```json
{
  "code":"NET30","name":"เครดิต 30 วัน","name_en":"Net 30",
  "type":"credit","trigger":"immediate","due_basis":"invoice_date",
  "net_days":30,"discount_pct":2,"discount_days":10,
  "deposit_method":null,"deposit_value":null,"remaining_timing":null,
  "expense_category":null,
  "installments":[],
  "use_in":["po","ap_invoice"],
  "is_default":false,"status":"active"
}
```
**Validation (field-level, ≤5 lines — complex → 03_LOGIC F-PAY-FN-03):**
- `code`: required, uppercase, unique/tenant
- `name`: required
- `type`: required, ∈ 7 enum
- `use_in`: required, array len ≥ 1, ทุกค่า ∈ 7 enum (ไม่มี 'pr')
- **Per-type + cross-field validation → F-PAY-FN-03 validatePaymentTerm** (BR-02..07)

**Response 201:** `{ "id":"uuid","status":"active","used":0, ...full record..., "approver_role":null,"approved_by":null,"approved_at":null,"approval_chain":null }`

**Errors:** 400 ERR_VALIDATION_FAILED · 403 ERR_INSUFFICIENT_ROLE · 409 ERR_DUPLICATE_CODE (BR-01) · 409 ERR_DUPLICATE_IDEMPOTENCY_KEY · 422 ERR_* (per validation — ดู 05_RULES §5.6)
**Preconditions:** type enum valid; ถ้า is_default=true → status ต้อง active (BR-07)
**Side effects:** INSERT T_payment_term (+ T_payment_term_installment ถ้า installment) · INSERT T_audit_log · **ไม่ emit event** (NOTIF off) · ถ้า is_default → unset default เดิม (same type)
**Calls (Logic):** F-PAY-FN-01 createPaymentTerm · F-PAY-FN-03 validatePaymentTerm · F-PAY-FN-08 enforceDefaultUniqueness · **ENG-PT-01 installment-validator** (ถ้า type=installment)

---

### F-PAY-API-03: GET /api/v1/payment-terms/:id
| Field | Value |
|---|---|
| **method** | GET · summary: Get detail (view drawer) · auth: required (Admin/Viewer) |

**Response 200:** full record + `installments[]` + `summary` (termSummary). **Errors:** 404 ERR_NOT_FOUND · 403.
**Side effects:** — · **Calls (Logic):** F-PAY-FN-10 buildTermSummary

---

### F-PAY-API-04: PUT /api/v1/payment-terms/:id
| Field | Value |
|---|---|
| **method** | PUT · summary: Update term (**allowed even used>0** — AD-01) · auth: Finance Admin · `If-Match` required (optimistic lock, AD-04) |

**Request:** same body as API-02 (full replace) · **Headers:** `If-Match: <version>`.
**Response 200:** updated record.
**Errors:** 400/403/404 · 409 ERR_STALE_DATA (version mismatch) · 409 ERR_DUPLICATE_CODE · 422 ERR_* (per validation)
**Business note:** **แก้ได้แม้ used>0** — เอกสารเก่า snapshot ไม่เปลี่ยน (BR-08 / AD-01). **ไม่มี** lock used>0 แบบ Tax Code (ตั้งใจ — OQ-PAY-05).
**Side effects:** UPDATE T_payment_term (+ replace installments) · INSERT T_audit_log (diff) · ถ้า is_default → unset default เดิม
**Calls (Logic):** F-PAY-FN-02 updatePaymentTerm · F-PAY-FN-03 validatePaymentTerm · F-PAY-FN-08 enforceDefaultUniqueness · ENG-PT-01 (ถ้า installment)

---

### F-PAY-API-05: PATCH /api/v1/payment-terms/:id/status
| Field | Value |
|---|---|
| **method** | PATCH · summary: เปลี่ยนสถานะเดี่ยว (view menu, `setStatusFromMenu`) · auth: Finance Admin |

**Request Body:** `{ "status":"active|inactive|draft" }` · **Headers:** `If-Match`.
**Response 200:** `{ "id":"uuid","status":"inactive" }`.
**Errors:** 400 (invalid status) · 403 · 404 · 409 ERR_STALE_DATA
**Business note:** 3 ค่าอิสระ ทุกทิศ ทันที (no approval, VD-PDM-02). ถ้าเปลี่ยนเป็น non-active + is_default=true → auto unset is_default (guard BR-07).
**Side effects:** UPDATE status · INSERT T_audit_log · **Calls (Logic):** F-PAY-FN-05 setTermStatus

---

### F-PAY-API-06: POST /api/v1/payment-terms/bulk-status
| Field | Value |
|---|---|
| **method** | POST · summary: Bulk set status (bulk bar) · auth: Finance Admin |

**Request Body:** `{ "ids":["uuid",...], "status":"active|inactive|draft" }` · Idempotency-Key.
**Response 200:** `{ "updated": 5, "status":"inactive" }`.
**Errors:** 400 · 403 · 422 (บาง id ไม่พบ → partial report)
**Side effects:** UPDATE many · INSERT T_audit_log (per id) · **Calls (Logic):** F-PAY-FN-06 bulkSetStatus

---

### F-PAY-API-07: POST /api/v1/payment-terms/bulk-delete
| Field | Value |
|---|---|
| **method** | POST · summary: Bulk delete with used>0 guard (skip) · auth: Finance Admin |

**Request Body:** `{ "ids":["uuid",...] }` · Idempotency-Key.
**Response 200:**
```json
{ "deleted": 3, "skipped": 2, "skipped_ids": ["uuid","uuid"], "reason":"used>0" }
```
**Errors:** 400 · 403
**Business note:** ตัวที่ `used>0` **ถูกข้าม** ไม่ลบ (BR-08) · ไม่มี hard delete ถ้า used>0 (Central Plan) · ถ้าไม่มีตัวลบได้ → deleted=0 (UI ปุ่ม disabled).
**Side effects:** DELETE (used=0 only) T_payment_term + CASCADE installments · INSERT T_audit_log · **Calls (Logic):** F-PAY-FN-07 bulkDeleteTerms

---

### F-PAY-API-08: GET /api/v1/payment-terms/active
| Field | Value |
|---|---|
| **method** | GET · summary: Downstream active-terms picker · auth: any consumer · SLA <500ms (BRD §17.1) |

**Request — Query params:** `use_in` (doc-type filter เช่น po/so/ap_invoice, optional) · `type` (optional).
**Response 200:** `{ "data": [ { "id","code","name","type","summary","is_default", ...snapshot fields } ] }` — **เฉพาะ status=active** (BR-10). Direct payment ที่ปิด po/quotation/so จะไม่โผล่ถ้า use_in filter = po/quotation/so.
**Errors:** 400 · 403
**Side effects:** — (read-only, cacheable) · **Calls (Logic):** F-PAY-FN-11 getActiveTermsForPicker

---

## §2.3 Common Concerns

### Idempotency (AD-04 / PR-7)
Mutation APIs (POST create/bulk) รับ `Idempotency-Key` — cache 24h · same key+body → cached response · same key+different body → 409.

### Optimistic Locking (AD-04 / PR-1)
PUT/PATCH require `If-Match: <version>` — mismatch → 409 ERR_STALE_DATA (แก้ EC-01 concurrent default). `[AI-DEFAULT]` — ยืนยัน OQ-PAY-CC-01.

### Multi-Tenant
ทุก endpoint require `X-Tenant-Id` → RLS by tenant_id.

### Audit Log
ทุก mutation → T_audit_log middleware: actor · action · resource (T_payment_term:<id>) · timestamp · diff. **ไม่ emit NOTIF/event** (SCOPE_LOCK).

### DOA
**ไม่มี** endpoint อนุมัติ — approver_role/approved_by/approved_at/approval_chain = null placeholder (เตรียม Policy Center).

---

## §2.4 API → Logic Trace (Anchor for R8)
> Authoritative = 03_LOGIC §3.3.

| API | Calls Functions | Calls Engines |
|---|---|---|
| F-PAY-API-01 GET /payment-terms | F-PAY-FN-04, F-PAY-FN-10 | — |
| F-PAY-API-02 POST /payment-terms | F-PAY-FN-01, F-PAY-FN-03, F-PAY-FN-08 | ENG-PT-01 (if installment) |
| F-PAY-API-03 GET /:id | F-PAY-FN-10 | — |
| F-PAY-API-04 PUT /:id | F-PAY-FN-02, F-PAY-FN-03, F-PAY-FN-08 | ENG-PT-01 (if installment) |
| F-PAY-API-05 PATCH /:id/status | F-PAY-FN-05 | — |
| F-PAY-API-06 POST /bulk-status | F-PAY-FN-06 | — |
| F-PAY-API-07 POST /bulk-delete | F-PAY-FN-07 | — |
| F-PAY-API-08 GET /active | F-PAY-FN-11 | — |

> **R8 Check:** ทุก mutation row (02, 04, 05, 06, 07) มี ≥1 Function ✅

---

## §2.X Cross-Module Contract ⭐ (จาก BRD §12.1 Downstream Impact Map)

> Master = config ต้นน้ำ; ไม่ emit event (NOTIF off). Downstream **pull** ผ่าน GET /active + **snapshot** ค่าลงเอกสารตัวเอง. Trigger/GL แปลผลด้วย engines.

| Downstream | รูปแบบ | Contract | Trigger | Payload หลัก | Trace test |
|---|---|---|---|---|---|
| PO / SO / Quotation | Endpoint (ปลายทางเรียก) | GET /payment-terms/active?use_in=po\|so\|quotation | on doc create (เลือก term) | snapshot {code, type, net_days, due_basis, discount, deposit, installments[], trigger} | XT-01 |
| AP / AR Invoice | Endpoint + snapshot | GET /active?use_in=ap_invoice\|ar_invoice | on invoice | due_basis + net_days + discount → downstream คำนวณ due date | XT-03 |
| Payment Voucher / Receipt | Endpoint + snapshot | GET /active?use_in=payment_voucher\|receipt | on pay/receipt | เงื่อนไข/งวด/ส่วนลด | XT-01 |
| Warehouse / GRN / Ship | Engine (downstream) | **ENG-PT-02 payment-trigger-resolver** (03_LOGIC §3.2) | PO/SO confirm หรือชำระ | {type, trigger, side:P2P\|S2C} → unlock point | XT-05 |
| Accounting / GL | Engine + Hook | **ENG-PT-01** installment split · Hook-2 deposit VAT (Tax Code) · Hook-3 cash-discount | posting | งวด/มัดจำ/ส่วนลด → journal | XT-03, XT-04 |
| Vendor/Customer master (future) | — | payment_term default override (OQ-PAY-03) | — | — | (out of scope) |

**Compensating behavior (แก้/ปิดกลางทาง):** master เปลี่ยน/ปิด → เอกสารเก่า **snapshot คงเดิม** (no retro), ปิด master → ไม่โผล่ใน picker ใหม่ (status≠active). ไม่มี compensating event เพราะ soft-ref (no cascade). ทุกแถว trace 06_TESTS §6.9.
