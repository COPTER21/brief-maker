# 02_API — F-TAX Tax Code (รหัสภาษี)

> **Audience:** Backend developer (HTTP layer)
> **Purpose:** API contracts — CUBIC API Entity format
> **🚨 Iron Rule:** ห้าม business logic >5 lines ที่นี่ — ย้ายไป 03_LOGIC §3.1/§3.2
> **🚨 R8:** ทุก mutation API ระบุ "Calls (Logic)" → trace ใน 03_LOGIC §3.3
> **Headers ทุก request:** `X-Company-Id` (required, RLS/LOCK-02) · `Authorization: Bearer` · mutation เพิ่ม `Idempotency-Key` (`[AI-DEFAULT]` PR-7/OQ-8) · edit/deactivate เพิ่ม `If-Match` (optimistic lock `[AI-DEFAULT]` PR-1/OQ-9)

---

## §2.1 API Overview

| ID | Method | Path | Summary | Auth (role) |
|---|---|---|---|---|
| F-TAX-API-01 | GET | /api/v1/tax-codes | List (filter family/status) | `tax_code.view` |
| F-TAX-API-02 | GET | /api/v1/tax-codes/:id | Detail + lineage | `tax_code.view` |
| F-TAX-API-03 | POST | /api/v1/tax-codes | Create (draft หรือ create+activate) | `tax_code.create` (+`activate` ถ้า active) |
| F-TAX-API-04 | PUT | /api/v1/tax-codes/:id | Update (edit; rate lock ถ้า used>0) | `tax_code.update` |
| F-TAX-API-05 | POST | /api/v1/tax-codes/:id/activate | Activate (full validate) | `tax_code.activate` |
| F-TAX-API-06 | POST | /api/v1/tax-codes/:id/deactivate | Deactivate (active→inactive) | `tax_code.deactivate` |
| F-TAX-API-07 | POST | /api/v1/tax-codes/:id/archive | Archive draft (draft→archived) | `tax_code.deactivate` |
| F-TAX-API-08 | POST | /api/v1/tax-codes/:id/replacement | สร้างรหัสแทน + lineage | `tax_code.create` (+`activate` ยืนยัน) |
| F-TAX-API-09 | GET | /api/v1/tax-codes/pickable | Consumer resolve ตาม context+date | `tax_code.view` (+ external contract) |
| F-TAX-API-10 | GET | /api/v1/tax-codes/:id/audit | Audit timeline | `tax_code.view_audit` |
| F-TAX-API-11 | GET | /api/v1/gl-accounts | GL lookup (filter tax_role+company+active+posting) — reads CoA | `tax_code.view` |
| F-TAX-API-12 | GET | /api/v1/income-types | Income_Type reference (WHT) | `tax_code.view` |

> **Mutation APIs:** 03, 04, 05, 06, 07, 08 → ต้องมี ≥1 Function/Engine ใน trace (R8, §2.4).

---

## §2.2 Per-API Contract

### F-TAX-API-01: GET /api/v1/tax-codes
| Field | Value |
|---|---|
| **id** | F-TAX-API-01 · **method** GET · **path** /api/v1/tax-codes |
| **summary** | List tax codes บริษัทปัจจุบัน แยก family + filter status |
| **auth** | required · **roles** any `tax_code.view` |

**Request:** Query: `family` (VAT\|WHT, default VAT) · `status` (all\|active\|attention\|inactive…) · `q` (search) · `limit`/`offset`. Header `X-Company-Id`.
**Response 200:** `{ "data":[ { "id","code","name","rate","direction","income_type","eff_start","eff_end","status","used" } ], "total":N }`
**Errors:** 401 ERR_NOT_AUTHENTICATED · 403 ERR_INSUFFICIENT_ROLE
**Preconditions:** — · **Side effects:** — (read-only)
**Calls (Logic):** F-TAX-FN-01 buildTaxCodeListQuery → 03_LOGIC §3.1

---

### F-TAX-API-02: GET /api/v1/tax-codes/:id
| Field | Value |
|---|---|
| **summary** | รายละเอียด + lineage (replaces/replacedBy) + used |
| **auth** | required · `tax_code.view` |

**Response 200:** full TaxCode object (04_DB §4.2) + `{ "replaces":{...}, "replaced_by":{...} }`. **Audit ไม่รวมที่นี่** (แยก API-10, gated).
**Errors:** 403 · 404 ERR_NOT_FOUND
**Side effects:** — · **Calls (Logic):** — (single-row read, trivial)

---

### F-TAX-API-03: POST /api/v1/tax-codes
| Field | Value |
|---|---|
| **summary** | สร้างรหัสภาษี — `mode=draft` (saveDraft) หรือ `mode=activate` (create+activate) |
| **auth** | required · `tax_code.create` (+`tax_code.activate` เมื่อ mode=activate) |

**Request headers:** `X-Company-Id`, `Idempotency-Key` (required — OQ-8).
**Body:**
```json
{ "mode":"draft|activate", "code":"WHT3", "name":"...", "family":"VAT|WHT",
  "vat_kind":"standard|zero|exempt", "rate":7, "direction":"sale|purchase|both|pay",
  "gl_sale":"uuid", "gl_purchase":"uuid", "gl_wht":"uuid",
  "income_type":"ค่าบริการ / รับจ้างทำของ", "eff_start":"YYYY-MM-DD", "eff_end":null }
```
**Validation (field-level ≤5 lines):** `code` required · `name` required · `rate` 0–100. **Complex validation (uniqueness, GL role, WHT income, effStart, mode=activate completeness) → 03_LOGIC F-TAX-FN-04 validateTaxCodeForm.**
**Response 201:** `{ "id","code","status":"draft|active", ... }`
**Errors:** 400 ERR_VALIDATION_FAILED · 403 ERR_INSUFFICIENT_ROLE · 409 ERR_DUPLICATE_IDEMPOTENCY_KEY · 422 BR_TAX_CODE_DUPLICATE / BR_TAX_GL_REQUIRED / BR_TAX_WHT_INCOME_REQUIRED (ดู 05_RULES §5.6)
**Preconditions:** company context set (LOCK-02); mode=activate ต้องผ่าน validate เต็ม (R04)
**Side effects:** INSERT T_tax_code · INSERT T_tax_code_audit (`บันทึกร่าง — รอผูกบัญชี GL` / `สร้างและเปิดใช้งานรหัสภาษี`) · (mode=activate) mark snapshot-ready
**Calls (Logic):** F-TAX-FN-02 createTaxCodeRecord, F-TAX-FN-04 validateTaxCodeForm, F-TAX-FN-14 resolveVatReportCategory, F-TAX-FN-12 deriveIncomeCategoryCode, F-TAX-FN-13 appendAudit · (mode=activate) F-TAX-FN-05 activateTaxCode, ENG-03 gl-role-validator

---

### F-TAX-API-04: PUT /api/v1/tax-codes/:id
| Field | Value |
|---|---|
| **summary** | แก้ไข (edit draft / edit active metadata) — **rate/family/vat_kind/direction/code lock เมื่อ used>0 (R02)** |
| **auth** | required · `tax_code.update` |

**Request headers:** `X-Company-Id`, `Idempotency-Key`, `If-Match: <version>` (optimistic lock — OQ-9).
**Body:** editable fields (server ปฏิเสธ lock fields ถ้า used>0). **ห้ามแก้อัตราของ used>0 → ต้อง replacement (API-08).**
**Response 200:** updated object.
**Errors:** 400 · 403 · 404 · 409 ERR_STALE_DATA (version mismatch) · 422 BR_TAX_RATE_LOCKED / BR_TAX_CODE_DUPLICATE
**Preconditions:** record exists; ถ้า used>0 → lock fields immutable (R02/E02)
**Side effects:** UPDATE T_tax_code (version++) · INSERT audit
**Calls (Logic):** F-TAX-FN-03 updateTaxCodeRecord, F-TAX-FN-04 validateTaxCodeForm, F-TAX-FN-13 appendAudit

---

### F-TAX-API-05: POST /api/v1/tax-codes/:id/activate
| Field | Value |
|---|---|
| **summary** | เปิดใช้งาน (draft/inactive → active) — validate เต็ม (Approver, SoD) |
| **auth** | required · `tax_code.activate` (Maker ที่ไม่มี activate → 403, E16) |

**Request headers:** `X-Company-Id`, `Idempotency-Key`, `If-Match`.
**Response 200:** `{ "id","status":"active" }`
**Errors:** 403 ERR_INSUFFICIENT_ROLE · 409 ERR_STALE_DATA · 422 BR_TAX_GL_REQUIRED / BR_TAX_WHT_INCOME_REQUIRED / BR_TAX_EFF_START_REQUIRED
**Preconditions (R04):** GL ครบตาม direction (role ถูก, ENG-03) · WHT → income_type set (R03) · eff_start set · uniqueness ผ่าน
**Side effects:** UPDATE status=active · INSERT audit (`สร้างและเปิดใช้งานรหัสภาษี`/`บันทึกการแก้ไขและเปิดใช้งาน`)
**Calls (Logic):** F-TAX-FN-05 activateTaxCode, F-TAX-FN-04 validateTaxCodeForm, ENG-03 gl-role-validator, F-TAX-FN-13 appendAudit

---

### F-TAX-API-06: POST /api/v1/tax-codes/:id/deactivate
| Field | Value |
|---|---|
| **summary** | ปิดใช้งาน (active → inactive) — no hard delete (R05) |
| **auth** | required · `tax_code.deactivate` |

**Request headers:** `X-Company-Id`, `Idempotency-Key`, `If-Match`.
**Response 200:** `{ "id","status":"inactive","eff_end":"<today>" }`
**Errors:** 403 · 404 · 409 ERR_STALE_DATA
**Preconditions:** status=active
**Side effects:** UPDATE status=inactive, eff_end=today · INSERT audit (`ปิดใช้งาน — ไม่แสดงในเอกสารใหม่`). เอกสารเดิมยังใช้ snapshot ได้ (E01)
**Calls (Logic):** F-TAX-FN-06 deactivateTaxCode, F-TAX-FN-13 appendAudit

---

### F-TAX-API-07: POST /api/v1/tax-codes/:id/archive
| Field | Value |
|---|---|
| **summary** | เก็บร่างถาวร (draft → archived) — no hard delete (R05/S-08) |
| **auth** | required · `tax_code.deactivate` |

**Response 200:** `{ "id","status":"archived","eff_end":"<today>" }`
**Errors:** 403 · 404 · 409 · 422 (ถ้าไม่ใช่ draft)
**Preconditions:** status=draft
**Side effects:** UPDATE status=archived, eff_end=today · INSERT audit (`เก็บร่างถาวร — คงข้อมูลและประวัติไว้`)
**Calls (Logic):** F-TAX-FN-07 archiveDraft, F-TAX-FN-13 appendAudit

---

### F-TAX-API-08: POST /api/v1/tax-codes/:id/replacement
| Field | Value |
|---|---|
| **summary** | สร้างรหัสแทน (อัตราเปลี่ยน) + lineage (BR-02/S-07/LOCK-09) |
| **auth** | required · `tax_code.create` (+`tax_code.activate` เพื่อ activate รหัสแทน) |

**Request headers:** `X-Company-Id`, `Idempotency-Key`.
**Body:** `{ "new_code":"VAT7-1", "rate":9, "eff_start":"YYYY-MM-DD", ...editable }` (code+"-N" default)
**Response 201:** `{ "new":{ "id","code","replaces_tax_code_id":"<old>" }, "old":{ "id","replaced_by_tax_code_id":"<new>","eff_end":"<newStart-1d>" } }`
**Errors:** 400 · 403 · 422 (overlap/validation — E12)
**Preconditions:** old record exists (used>0 ปกติ); new eff_start > old eff_start
**Side effects:** INSERT new T_tax_code (replaces=old, status per activate) · UPDATE old (replaced_by=new, eff_end=new.eff_start−1) · INSERT audit ทั้งสอง (`สร้างรหัสแทน <code> (อัตรา N%) มีผล <date>`)
**Calls (Logic):** F-TAX-FN-08 createReplacementCode, F-TAX-FN-04 validateTaxCodeForm, F-TAX-FN-05 activateTaxCode, F-TAX-FN-13 appendAudit

---

### F-TAX-API-09: GET /api/v1/tax-codes/pickable  ⭐ (Consumer-facing contract)
| Field | Value |
|---|---|
| **summary** | รหัสที่เลือกได้ ณ วันที่เอกสาร + context (R08/R09/S-09) |
| **auth** | required · `tax_code.view` (+ External Contract — ดู §2.X) |

**Request:** Query `context` (sale\|purchase\|payment) · `document_date` (YYYY-MM-DD, **วันที่เอกสาร ไม่ใช่วันที่ระบบ**) · `family` (optional). Header `X-Company-Id`.
**Response 200:** `{ "data":[ { "id","code","rate","direction","vat_report_category","income_category_code","advisory":true|false } ] }` — `advisory=true` สำหรับ WHT ในเอกสารซื้อ (E05/LOCK-06).
**Errors:** 400 (missing document_date) · 403
**Side effects:** — (read); snapshot capture = consumer-side (POST ที่ consumer doc, ไม่ใช่ endpoint นี้)
**Calls (Logic):** F-TAX-FN-09 resolvePickableTaxCodes, ENG-02 effective-date-resolver, ENG-01 tax-snapshot-builder (สำหรับ preview/capture contract)

---

### F-TAX-API-10: GET /api/v1/tax-codes/:id/audit
| Field | Value |
|---|---|
| **summary** | Audit timeline (append-only, ล่าสุดก่อน) — S-10 |
| **auth** | required · **`tax_code.view_audit`** (ไม่มี → 403, E17) |

**Response 200:** `{ "data":[ { "ts","actor","action" } ] }` (DESC)
**Errors:** 403 ERR_INSUFFICIENT_ROLE (ไม่มี view_audit) · 404
**Side effects:** — (read; log access — D9/E17)
**Calls (Logic):** F-TAX-FN-13 appendAudit (read path buildAuditView)

---

### F-TAX-API-11: GET /api/v1/gl-accounts  (GL lookup — reads CoA)
| Field | Value |
|---|---|
| **summary** | GL combobox options — filter `tax_role` + current company + active + posting (R06/R07) |
| **auth** | required · `tax_code.view` |

**Request:** Query `tax_role` (VAT_SALE\|VAT_PURCHASE\|**WHT_PAYABLE**) · `q`. Header `X-Company-Id`.
**Response 200:** `{ "data":[ { "id","value","label","sub" } ] }` — เฉพาะ company ปัจจุบัน, `status=active`, `posting_allowed=true`, `tax_role` ตรง (**WHT → WHT_PAYABLE เท่านั้น, LOCK-12/FLAG-1**).
**Errors:** 400 (invalid tax_role) · 403
**Side effects:** — (read CoA)
**Calls (Logic):** F-TAX-FN-11 filterGlAccounts, ENG-03 gl-role-validator

---

### F-TAX-API-12: GET /api/v1/income-types  (WHT reference)
| Field | Value |
|---|---|
| **summary** | Income_Type list (value/code/recommended_rate hint) — R17 |
| **auth** | required · `tax_code.view` |

**Response 200:** `{ "data":[ { "value","code","recommended_rate","pnd_form" } ] }` (8 rows)
**Side effects:** — · **Calls (Logic):** — (reference read)

---

## §2.3 Common Concerns

### Idempotency (PR-7) `[AI-DEFAULT]` — OQ-8
Mutation APIs (03,04,05,06,07,08) accept `Idempotency-Key`. Same key+body → cached response; same key+different body → 409 ERR_DUPLICATE_IDEMPOTENCY_KEY. TTL default 24h (confirm OQ-8).

### Optimistic Locking (PR-1/PR-2/E15) `[AI-DEFAULT]` — OQ-9
Edit/deactivate/archive/activate require `If-Match: <version>`. Mismatch → 409 ERR_STALE_DATA. (BRD E15 บอกให้มี optimistic lock; contract นี้เป็น conservative default.)

### Multi-Company (LOCK-02/R15/E18)
ทุก endpoint require `X-Company-Id`; DB filter ผ่าน RLS; cross-company access → 403/404 (server-side, ไม่พึ่ง UI hide — E18).

### Server-side Authorization (E16/E17/E18)
Role re-check ที่ mutation time (ไม่ใช่แค่ GET/UI hide). activate/deactivate = Approver only; Maker submit → เฉพาะ draft path (E16). view_audit gate ที่ API-10 (E17).

### Audit (D9/R05)
ทุก mutation → INSERT T_tax_code_audit (append-only; actor/action/ts). ไม่มี hard delete endpoint (R05).

---

## §2.4 API → Logic Trace (Anchor for R8)

> **Authoritative:** 03_LOGIC §3.3. ที่นี่ = summary.

| API | Calls Functions | Calls Engines |
|---|---|---|
| F-TAX-API-01 GET /tax-codes | F-TAX-FN-01 | — |
| F-TAX-API-02 GET /tax-codes/:id | — (trivial read) | — |
| F-TAX-API-03 POST /tax-codes | FN-02, FN-04, FN-14, FN-12, FN-13, (FN-05) | ENG-03 |
| F-TAX-API-04 PUT /tax-codes/:id | FN-03, FN-04, FN-13 | — |
| F-TAX-API-05 POST /:id/activate | FN-05, FN-04, FN-13 | ENG-03 |
| F-TAX-API-06 POST /:id/deactivate | FN-06, FN-13 | — |
| F-TAX-API-07 POST /:id/archive | FN-07, FN-13 | — |
| F-TAX-API-08 POST /:id/replacement | FN-08, FN-04, FN-05, FN-13 | — |
| F-TAX-API-09 GET /tax-codes/pickable | FN-09 | ENG-02, ENG-01 |
| F-TAX-API-10 GET /:id/audit | FN-13 | — |
| F-TAX-API-11 GET /gl-accounts | FN-11 | ENG-03 |
| F-TAX-API-12 GET /income-types | — (reference read) | — |

> **R8 Check:** mutation rows (03,04,05,06,07,08) มี ≥1 Function/Engine ✅

---

## §2.X Cross-Module Contract ⭐ (จาก BRD §12.1 Downstream Impact Map)

> **ทั้งหมดเป็น External Contract — downstream ยังไม่ implement** (BRD §3.3 A3 / §12.2). Feature นี้ expose contract; downstream เรียกเมื่อพร้อม.

| Downstream | รูปแบบ | Contract | Trigger | Payload หลัก | Compensating |
|---|---|---|---|---|---|
| SO / AR Invoice | Endpoint (ปลายทางเรียก) | `GET /tax-codes/pickable?context=sale&document_date=` → snapshot (ENG-01) | on doc line add | { tax_code_id, code, rate, gl_sale, vat_report_category, document_date } | รหัส inactive/หมดวันมีผล → เอกสารใหม่เลือกไม่ได้; เดิมใช้ snapshot ต่อ (E01) |
| PO / AP Invoice | Endpoint | `GET /tax-codes/pickable?context=purchase` | on doc line add | VAT ซื้อ (rate, gl_purchase) + WHT `advisory=true` | เดียวกัน; WHT ยังไม่ final |
| Payment Voucher | Endpoint | `GET /tax-codes/pickable?context=payment` — **จุดยืนยัน WHT จริง** (LOCK-06) | on payment | { tax_code_id, rate, gl_wht, income_category_code } final | report อ่านจาก payment result |
| VAT Return (ภ.พ.30) `#/accounting/reports/vat-return` | อ่าน snapshot | `vat_report_category` จาก snapshot immutable | งวดรายงาน VAT | STANDARD/ZERO_RATED/EXEMPT | snapshot immutable → รายงานคงที่ (R08) |
| WHT report (ภ.ง.ด.3/53) `#/accounting/reports/withholding-tax` | อ่าน payment result | income_category + WHT final | งวดรายงาน WHT | จาก payment ไม่ใช่ AP suggestion (LOCK-06) | — |

- **Snapshot immutability contract (R08):** consumer เก็บ snapshot object (04_DB Tax_Snapshot) — แม้ master เปลี่ยนภายหลัง snapshot ไม่เปลี่ยน. ผลิตโดย ENG-01.
- ทุกแถว trace กับ 06_TESTS §6.9 (XT-01..XT-05).
