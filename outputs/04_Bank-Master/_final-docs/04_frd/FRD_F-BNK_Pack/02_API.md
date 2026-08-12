# 02_API — F-BNK Bank Master (บัญชีธนาคาร)

> **Audience:** Backend developer (HTTP layer)
> **Purpose:** API contracts (CUBIC API Entity) + Cross-Module Contract (GL Posting Group consume / Receipt-PV serve)
> **🚨 Iron Rule:** ห้ามมี business logic >5 lines ที่นี่ — ย้ายไป 03_LOGIC §3.1
> **🚨 R8:** ทุก mutation API ต้องระบุ "Calls (Logic)" → trace ใน 03_LOGIC §3.3
> **Note:** HTML prototype = mock synchronous (client-side). API ด้านล่าง = production design (server-side mirror ของ `saveBank()`/`bulkValidateRow()` — Control C4).

---

## §2.1 API Overview

| ID | Method | Path | Summary | Auth |
|---|---|---|---|---|
| F-BNK-API-01 | GET | /api/v1/bank-accounts | List + filter (search/bank/status) + stat counts | required |
| F-BNK-API-02 | POST | /api/v1/bank-accounts | Create bank account | required (Finance Admin) |
| F-BNK-API-03 | GET | /api/v1/bank-accounts/:id | Get detail (view drawer) | required |
| F-BNK-API-04 | PUT | /api/v1/bank-accounts/:id | Update (IR-BNK-01: lock bank+account_no ถ้า used>0) | required (Finance Admin) |
| F-BNK-API-05 | POST | /api/v1/bank-accounts/:id/status | เปลี่ยนสถานะเดี่ยว (view menu) | required (Finance Admin) |
| F-BNK-API-06 | POST | /api/v1/bank-accounts/bulk-status | Bulk set status | required (Finance Admin) |
| F-BNK-API-07 | POST | /api/v1/bank-accounts/bulk-delete | Bulk delete (guard used>0 → skip) | required (Finance Admin) |
| F-BNK-API-08 | POST | /api/v1/bank-accounts/import/preview | Validate CSV rows (no write) | required (Finance Admin) |
| F-BNK-API-09 | POST | /api/v1/bank-accounts/import/commit | Commit valid rows, **merge-only** | required (Finance Admin) |
| F-BNK-API-10 | GET | /api/v1/bank-accounts/export | Export filtered rows as CSV (BOM, roundtrip) | required (Finance Admin, Auditor) |
| F-BNK-API-11 | GET | /api/v1/bank-accounts/active | Downstream picker (Receipt/PV — active + ฝั่งตรง) | required (any consumer) |

> **Consumed (external, ไม่ได้เป็นเจ้าของ):** `GET /api/v1/gl/posting-groups?kind=bank&status=active` = **generic F-PG-API-01** (ดู §2.6). **ไม่มี endpoint เฉพาะ Bank Master ฝั่ง F-PG** (Bank Master = downstream consumer ที่ประกาศแล้วแต่ยังไม่ implement ฝั่ง F-PG — F-PG 00_OVERVIEW §0.4/§0.5).
> **ไม่มี** endpoint: single-delete (POST bulk-delete เท่านั้น), CSV import mode=replace, approve/submit (DOA null), เส้นไป Payment Method (OQ-BNK-01=NO). ดู 05_RULES + §7 SCOPE_LOCK.

---

## §2.2 Per-API Contract

### F-BNK-API-01: GET /api/v1/bank-accounts
| Field | Value |
|---|---|
| **id** | F-BNK-API-01 · **method** GET · **auth** required · **roles** Finance Admin, Finance Viewer |

**Request — Query params:** `search` (code/bank label/branch/account_no/account_name, optional) · `bank` (9 enum | all) · `status` (draft/active/inactive | all) · `sort` (col+dir) · `limit` (default 8, max 100) · `offset`. **Headers:** `X-Tenant-Id`.

**Response 200:**
```json
{
  "data": [
    { "id":"B-001","code":"KBANK-01","bank":"KBANK","branch":"สำนักงานใหญ่ (พหลโยธิน)",
      "account_no":"012-3-45678-9","account_name":"บริษัท คิวบ์ เนทีฟ จำกัด",
      "account_type":"savings","promptpay_id":"0105561234567","posting_group":"KBANK",
      "currency":"THB","use_receive":true,"use_pay":true,
      "default_receive":true,"default_pay":false,"status":"active" }
  ],
  "counts": { "all": 8, "active": 6, "inactive": 1, "draft": 1 },
  "total": 8, "limit": 8, "offset": 0
}
```
> **`used` ไม่อยู่ใน response ของ list/detail** (S-10⑤ — ไม่โชว์บนจอ). ใช้ภายใน logic guard เท่านั้น.
**Errors:** 400 ERR_INVALID_QUERY_PARAMS · 401 ERR_NOT_AUTHENTICATED · 403 ERR_INSUFFICIENT_ROLE
**Side effects:** — (read-only) · **Calls (Logic):** F-BNK-FN-04 buildBankListQuery, F-BNK-FN-10 maskAccountNo (ถ้า render masked)

---

### F-BNK-API-02: POST /api/v1/bank-accounts
| Field | Value |
|---|---|
| **id** | F-BNK-API-02 · **method** POST · **auth** required · **roles** Finance Admin · `Idempotency-Key` required (AD-BNK-02) |

**Request — Body:**
```json
{
  "code":"", "bank":"KBANK", "account_no":"012-3-45678-9",
  "account_name":"บริษัท คิวบ์ เนทีฟ จำกัด", "branch":"สำนักงานใหญ่",
  "account_type":"savings", "promptpay_id":"",
  "posting_group":"KBANK",
  "use_receive":true, "use_pay":false,
  "default_receive":false, "default_pay":false, "status":"active"
}
```
**Validation (field-level, ≤5 lines — complex → 03_LOGIC F-BNK-FN-03):**
- `bank`: required, ∈ 9 enum
- `account_no`: required (dash-stripped 10–12 digits — detail FN-03)
- `account_name`: required non-empty
- `account_type`: ∈ 3 enum (default savings)
- `use_receive || use_pay`: ต้องมี ≥1 = true
- `currency` = THB (server enforce — ไม่รับค่าอื่น)
- **Per-field + cross-field + uniqueness → F-BNK-FN-03 validateBankAccount** (account_no dash-strip unique, code dup, promptpay 10/13, DEFAULT_GUARD)
- **code เว้น → F-BNK-FN-09 generateBankCode** (`{bank}-{seq}`)

**Response 201:**
```json
{ "id":"B-...", "code":"KBANK-03", "status":"active", "used":0,
  "approver_role":null,"approved_by":null,"approved_at":null,"approval_chain":null,
  "created_by":"uuid","created_at":"2026-08-11T10:00:00Z" }
```
**Errors:** 400 ERR_VALIDATION_FAILED · 403 ERR_INSUFFICIENT_ROLE · 409 ERR_DUPLICATE_IDEMPOTENCY_KEY · 422 `ERR_REQUIRED` · 422 `ERR_BAD_BANK` · 422 `ERR_ACCT_INVALID` · 422 `ERR_ACCT_DUPLICATE` · 422 `ERR_CODE_DUPLICATE` · 422 `ERR_PROMPTPAY_INVALID` · 422 `ERR_USE_IN_EMPTY` · 422 `ERR_DEFAULT_GUARD` (ดู 05_RULES §5.6)
**Preconditions:** bank enum valid; ถ้า default_receive/pay=true → ฝั่งนั้นเปิด + status=active (BR-03)
**Side effects:** INSERT T_bank_account (used=0, DOA null×4) · ถ้า default_receive/pay → unset ★ เดิมฝั่งเดียวกันทั้งระบบ · INSERT T_audit_log · **ไม่ emit event** (NOTIF off)
**Calls (Logic):** F-BNK-FN-01 createBankAccount · F-BNK-FN-03 validateBankAccount · F-BNK-FN-08 enforceDefaultPerSide · F-BNK-FN-09 generateBankCode (ถ้า code ว่าง)

---

### F-BNK-API-03: GET /api/v1/bank-accounts/:id
| Field | Value |
|---|---|
| **method** | GET · summary: Get detail (view drawer) · auth: required (Admin/Viewer) |

**Response 200:** full record (ไม่รวม `used`) — account_no อาจส่งแบบ masked ตาม role/OQ-BNK-08. **Errors:** 404 ERR_NOT_FOUND · 403.
**Side effects:** — (read-only, **write read-access-log** สำหรับ Confidential field — C6) · **Calls (Logic):** F-BNK-FN-10 maskAccountNo

---

### F-BNK-API-04: PUT /api/v1/bank-accounts/:id ⭐ IR-BNK-01
| Field | Value |
|---|---|
| **method** | PUT · summary: Update account · auth: Finance Admin · `If-Match` required (optimistic lock, AD-BNK-02) |

**Request:** same body as API-02 · **Headers:** `If-Match: <version>`.

**Business rules enforced server-side (F-BNK-FN-02):**
- **IR-BNK-01:** ถ้า `used > 0` → `bank` และ `account_no` ใน body ถูก **ignore** (ไม่ update field 2 ตัวนี้) — mirror HTML `if(!locked){ data.bank=bank; data.account_no=acctNo; }`. ค่าที่ client ส่งมาต่างจากเดิม **ไม่ persist** (E2E R2 #9 ยืนยัน). ไม่ error 422 — เงียบ ๆ ล็อกไว้ (จอ disabled อยู่แล้ว).
- ทุก field อื่น (`account_name`, `branch`, `account_type`, `promptpay_id`, `posting_group`, `use_*`, `default_*`, `status`) แก้ได้ปกติ ไม่ว่า used เท่าไหร่.
- Validation (name/promptpay/use/DEFAULT_GUARD/code dup) เหมือน create; **account_no dup check ข้าม** ถ้า locked (used>0) เพราะ field ไม่เปลี่ยน.

**Response 200:** updated record.
**Errors:** 400/403/404 · 409 ERR_STALE_DATA (version mismatch) · 422 ERR_* (per validation)
**Business note:** เอกสารเก่าที่ snapshot แล้วไม่กระทบ (soft-ref, no retro — EC-03). เปลี่ยน type/ฝั่ง ของ used>0 ทำได้ (ล็อกเฉพาะ ธนาคาร+เลขบัญชี).
**Side effects:** UPDATE T_bank_account (version++) · ถ้า default_receive/pay → unset ★ เดิม · INSERT T_audit_log (before/after diff)
**Calls (Logic):** F-BNK-FN-02 updateBankAccount · F-BNK-FN-03 validateBankAccount · F-BNK-FN-08 enforceDefaultPerSide

---

### F-BNK-API-05: POST /api/v1/bank-accounts/:id/status
| Field | Value |
|---|---|
| **method** | POST · summary: เปลี่ยนสถานะเดี่ยว (view menu, `setStatus`) · auth: Finance Admin |

**Request Body:** `{ "status":"active|inactive|draft" }` · **Headers:** `If-Match`.
**Response 200:** `{ "id":"B-001","status":"inactive" }`.
**Errors:** 400 (invalid enum) · 403 · 404 · 409 ERR_STALE_DATA
**Business note:** 3 ค่าอิสระ ทุกทิศ ทันที (no approval). **Side effect:** เปลี่ยนเป็น non-active → `default_receive=false` + `default_pay=false` (★ ทั้ง 2 ฝั่งหลุด — BR-03).
**Side effects:** UPDATE status (+ ★ drop) · INSERT T_audit_log · **Calls (Logic):** F-BNK-FN-05 setBankStatus

---

### F-BNK-API-06: POST /api/v1/bank-accounts/bulk-status
| Field | Value |
|---|---|
| **method** | POST · summary: Bulk set status (bulk bar) · auth: Finance Admin |

**Request Body:** `{ "ids":["B-001",...], "status":"active|inactive|draft" }` · Idempotency-Key.
**Response 200:** `{ "updated": 5, "status":"inactive" }`.
**Errors:** 400 · 403 · 422 (บาง id ไม่พบ → partial report)
**Business note:** ตัวที่ status = ค่าเดิม ถูกข้าม (n นับเฉพาะที่เปลี่ยนจริง — mirror HTML). non-active → ★ drop ต่อรายการ.
**Side effects:** UPDATE many (+ ★ drop where non-active) · INSERT T_audit_log (per id) · **Calls (Logic):** F-BNK-FN-06 bulkSetBankStatus

---

### F-BNK-API-07: POST /api/v1/bank-accounts/bulk-delete ⭐ guard used>0
| Field | Value |
|---|---|
| **method** | POST · summary: Bulk delete with used>0 guard (skip) · auth: Finance Admin |

**Request Body:** `{ "ids":["B-001",...] }` · Idempotency-Key.
**Response 200:**
```json
{ "deleted": 1, "skipped": 1, "skipped_ids": ["B-001"], "reason": "used>0" }
```
**Errors:** 400 · 403
**Business note:** ตัวที่ `used>0` **ถูกข้าม** ไม่ลบ (BR-02, no hard delete) · ถ้าไม่มีตัวลบได้ → deleted=0 (UI ปุ่ม disabled). ไม่มี single-delete endpoint.
**Side effects:** DELETE (used=0 only) T_bank_account · INSERT T_audit_log · **Calls (Logic):** F-BNK-FN-07 bulkDeleteBankAccounts

---

### F-BNK-API-08 / F-BNK-API-09: Import preview / commit (merge-only)

**F-BNK-API-08 POST /import/preview**
- **Body:** `{ "rows": [{ "code","bank","branch","account_no","account_name","account_type","use_in","status" }, ...] }` (parsed CSV rows; columns per template §04_DB — **ไม่มี** posting_group/promptpay)
- **Response 200:** `{ "rows": [{ ...row, "error": "เลขบัญชีซ้ำทะเบียน (ACCT_DUPLICATE)" | null }, ...], "ok_count": 3, "err_count": 3 }`
- **Per-row error codes (verbatim จาก HTML `bulkValidateRow` + IN_FILE check):** `REQUIRED` · `BAD_BANK` · `ACCT_INVALID` (dash-strip ≠ 10–12) · `ACCT_DUPLICATE` (ซ้ำทะเบียน) · `BAD_TYPE` · `BAD_USE` (รับ/จ่าย/ทั้งสอง) · `BAD_STATUS` (ใช้งาน/ไม่ใช้งาน/ร่าง) · `CODE_DUPLICATE` · **`IN_FILE_DUPLICATE`** (รหัส/เลขบัญชีซ้ำกันเองในไฟล์)
- **Calls (Logic):** F-BNK-FN-11 previewImportRows

**F-BNK-API-09 POST /import/commit**
- **Body:** `{ "rows": [<only rows with zero error, from prior preview>] }`
- **Response 200:** `{ "imported": 3, "skipped": 3 }`
- **Side effects:** INSERT หนึ่ง T_bank_account ต่อ valid row (Thai value map: bank/type/use_in/status; **default: ประเภท=ออมทรัพย์, ฝั่ง=ทั้งสอง, สถานะ=ร่าง**; `posting_group=''`, `promptpay_id=''`, `used=0`, DOA null×4). INSERT T_audit_log per row. **Merge-only — ไม่แตะ/ไม่ update แถวเดิม (ไม่มี Replace mode).**
- **Calls (Logic):** F-BNK-FN-12 commitImportRows

---

### F-BNK-API-10: GET /api/v1/bank-accounts/export
| Field | Value |
|---|---|
| **method** | GET · summary: Export filtered rows as CSV · auth: Finance Admin, Auditor |

**Request — Query params:** same filters as API-01 (`search`, `bank`, `status`) — export respects current filter (mirror `exportCSV()`).
**Response 200:** `text/csv; charset=utf-8` + **UTF-8 BOM**, columns `code,bank,branch,account_no,account_name,account_type,use_in,status` (roundtrips กับ import template) · bank/type/use_in/status = Thai label · filename `bank_export_YYYY-MM-DD.csv`.
> **Note:** export = Confidential data (account_no ครบ) → ต้อง access-log + จำกัดสิทธิ์ (C6/C11, OQ-BNK-08).
**Calls (Logic):** F-BNK-FN-13 exportBankRegistry

---

### F-BNK-API-11: GET /api/v1/bank-accounts/active ⭐ downstream picker
| Field | Value |
|---|---|
| **method** | GET · summary: Downstream active-accounts picker (Receipt/PV) · auth: any consumer · SLA <500ms (BRD §17.1) |

**Request — Query params:** `side` (`receive` | `pay`, required — ฝั่งเอกสาร).
**Response 200:** `{ "data":[ { "id","code","bank","account_name","account_no","posting_group","is_default" } ] }` — **เฉพาะ status=active AND (side=receive → use_receive=true / side=pay → use_pay=true)** (BR-05). `is_default` = ★ ของฝั่งนั้น (pre-select).
**Errors:** 400 (missing side) · 403
**Business note:** ★ ของฝั่ง = pre-select · ปลายทาง **snapshot** ค่าตอนบันทึก (OQ-BNK-04). ฝั่งปลายทาง (Receipt/PV) **ยังไม่ทำ** — endpoint นี้ประกาศ contract ไว้ล่วงหน้า.
**Side effects:** — (read-only, cacheable) · **Calls (Logic):** F-BNK-FN-13b getActiveAccountsForPicker

---

## §2.3 Common Concerns

### Idempotency (AD-BNK-02 / PR-7)
Mutation APIs (POST create / bulk / import commit) รับ `Idempotency-Key` — cache 24h · same key+body → cached · same key+different body → 409. **ไม่มีใน HTML mock** (client push ไม่มี network race) — เป็น **backend addition** เพราะ production networked (flagged `[AI-DEFAULT]` AD-BNK-02).

### Optimistic Locking (AD-BNK-02 / PR-1)
PUT/POST-status require `If-Match: <version>` → mismatch → 409 ERR_STALE_DATA (แก้ EC-08: 2 admin ตั้ง ★ พร้อมกัน). `[AI-DEFAULT]` — ยืนยัน OQ-BNK-CC-01. **ไม่มีใน HTML mock.**

### Multi-Tenant
ทุก endpoint require `X-Tenant-Id` → RLS by tenant_id.

### Audit Log
ทุก mutation → T_audit_log middleware: actor · action · resource (T_bank_account:<id>) · timestamp · diff. **Read access log** เพิ่มสำหรับ Confidential (account_no) — C6. **ไม่ emit NOTIF/event** (SCOPE_LOCK).

### Role enforcement (PM edge, `[AI-DEFAULT]`)
ทุก mutation endpoint re-check role server-side (ไม่ใช่แค่ซ่อนปุ่ม) → 403 ERR_INSUFFICIENT_ROLE (Viewer/Consumer เรียกตรง). Standard practice.

### DOA
**ไม่มี** endpoint อนุมัติ — approver_role/approved_by/approved_at/approval_chain = null placeholder (เตรียม Policy Center).

---

## §2.4 API → Logic Trace (Anchor for R8)
> Authoritative = 03_LOGIC §3.3.

| API | Calls Functions | Calls Engines |
|---|---|---|
| F-BNK-API-01 GET /bank-accounts | FN-04, FN-10 | — |
| F-BNK-API-02 POST /bank-accounts | FN-01, FN-03, FN-08, FN-09 | — |
| F-BNK-API-03 GET /:id | FN-10 | — |
| F-BNK-API-04 PUT /:id | FN-02, FN-03, FN-08 | — |
| F-BNK-API-05 POST /:id/status | FN-05 | — |
| F-BNK-API-06 POST /bulk-status | FN-06 | — |
| F-BNK-API-07 POST /bulk-delete | FN-07 | — |
| F-BNK-API-08 POST /import/preview | FN-11 | — |
| F-BNK-API-09 POST /import/commit | FN-12 | — |
| F-BNK-API-10 GET /export | FN-13 | — |
| F-BNK-API-11 GET /active | FN-13b | — |

> **R8 Check:** ทุก mutation row (02,04,05,06,07,09) มี ≥1 Function ✅ · **ไม่มี engine** (feature นี้ไม่มี CUBIC engine ของตัวเอง — GL resolve = external, §2.7).

---

## §2.6 Cross-Module Contract — Consumed from GL Posting Group (F-PG kind=bank) ⭐

> **DEV ต้องอ่าน:** picker "กลุ่มบัญชี GL" ในฟอร์ม (P-02/P-03) + resolve บัญชีเงินฝากตอน post = ต้องอ่านจาก **F-PG generic API-01**. Bank Master เก็บเฉพาะ `posting_group.code` (NO FK). นี่คือ **inbound reference เดียว** ของ feature.

### Consumed endpoint (owned by F-PG, called by this feature)

| Field | Value |
|---|---|
| **method** | GET |
| **path** | `/api/v1/gl/posting-groups?kind=bank&status=active` |
| **id (ฝั่ง F-PG)** | **F-PG-API-01** (generic list) — **ไม่มี endpoint เฉพาะ Bank Master** |
| **owner** | F-PG (GL Posting Group) |
| **consumer** | F-BNK (this) — via F-BNK-FN-14 buildBankPostingGroupOptions, see 03_LOGIC §3.1 |
| **auth** | service-to-service หรือ forwarded user JWT (same session) |

**Query params (mandatory):**
| Param | Value | Reason |
|---|---|---|
| `kind` | `bank` | **ใช้ `?kind=bank` (NOT `?type=bank`)** — `type=` สงวนให้ Item Master (F-PG-API-19) เท่านั้น (Drift D-1) |
| `status` | `active` | picker เห็นเฉพาะ active (F-PG BR-06) — active-only จริงคืน **KBANK เท่านั้น**, SCB=draft ถูก filter ออก (Drift D-2) |

**Response 200 (F-PG-API-01 shape):**
```json
{ "data": [
    { "id":"g?","code":"KBANK","kind":"bank","name_th":"ธนาคารกสิกรไทย","name_en":"...",
      "account_1":"1-1-XX-XX","account_2":null,"status":"active","used": 12 }
  ], "total": 1 }
```
- กลุ่ม **kind=bank** มี `account_1` = บัญชีเงินฝาก (COA type=asset), `account_2` = **NULL** (F-PG R02).

### 🚨 3 KNOWN DRIFTS (mock ใน `f-bank.html` vs f-postgrp as-built) — DEV **ห้ามลอก mock**

| # | Drift | mock ใน HTML | ของจริง (build ตามนี้) | Action |
|---|---|---|---|---|
| **D-1** | Param name | comment ระบุถูก `?kind=bank` | `?kind=bank` (NOT `?type=bank`) | ใช้ `?kind=bank` |
| **D-2** | Active-only filter | `BANK_POSTING_GROUPS=[{KBANK,active},{SCB,draft}]` seed local ทั้ง 2 แล้ว filter `status==='active'` ในจอ | `GET ?kind=bank&status=active` คืน **KBANK เท่านั้น** (SCB=draft ถูกกรองที่ server) | เรียก API active-only จริง — **แต่คงกลุ่มที่ผูกไว้เดิม (แม้ draft) กันหลุด** (ดู keep-bound ล่าง) |
| **D-3** | Endpoint | ไม่มี endpoint จริง (local array) | ใช้ **generic F-PG-API-01** — ไม่มี endpoint เฉพาะ Bank Master | consume generic API-01 (Bank Master = declared-but-not-implemented downstream ฝั่ง F-PG) |

### keep-bound-draft rule (edge SCB-01)
- picker option set = **(active groups จาก API-01) ∪ (กลุ่มที่ record นี้ผูกไว้อยู่แล้ว แม้ status≠active)** — mirror HTML `.filter(g=>g.status==='active'||g.code===r.posting_group)`. ป้องกัน binding หลุดตอนแก้ไข record ที่ผูกกลุ่ม draft (เช่น SCB-01 ผูก SCB=draft). option ของกลุ่ม draft แสดง suffix "(ร่าง)".
- Trace test: 06_TESTS AT-12 / XT-03.

---

## §2.7 Cross-Module Contract — Served to Receipt/PV + GL Engine (downstream, out of scope) ⭐

> จาก BRD §12.1 Downstream Impact Map. Master = config ต้นน้ำ; ไม่ emit event (NOTIF off). Downstream **pull** ผ่าน GET /active + **snapshot** ค่าลงเอกสารตัวเอง. ฝั่งปลายทาง (Receipt/PV, GL engine) **ยังไม่ทำ** — ประกาศ contract ให้ทีมปลายทางสร้างถูก.

| Downstream | รูปแบบ | Contract | Trigger | Payload หลัก | Trace test |
|---|---|---|---|---|---|
| **Receipt** (ฝั่งรับ · ยังไม่ทำ) | Endpoint + snapshot | GET /bank-accounts/active?side=receive | on Receipt create | snapshot {code, bank, account_no, account_name, posting_group} · ★รับ pre-select | XT-01 |
| **Payment Voucher** (ฝั่งจ่าย · ยังไม่ทำ) | Endpoint + snapshot | GET /active?side=pay | on PV create | เหมือน Receipt · ★จ่าย pre-select | XT-01 |
| **GL / Journal Engine** (external) | Read (resolve) | อ่าน `posting_group` ของบัญชี → resolve `account_1` (COA เงินฝาก) ผ่านกลุ่ม F-PG ตอน post | Receipt/PV post | บัญชีเงินฝาก COA จาก F-PG account_1 | XT-04 |
| Bank Reconciliation (future) | Read | account_no unique + bank match statement | กระทบยอด | — | — |
| ~~Payment Method (F-0.20)~~ | — | **CUT (OQ-BNK-01=NO)** — PM คง COA-direct | — | — | — |

- **Compensating behavior (แก้/ปิดกลางทาง):** แก้/ปิดบัญชี → เอกสารเก่า **snapshot คงเดิม** (no retro — soft-ref, no cascade). ปิด/inactive → ไม่โผล่ใน picker ใหม่ (status≠active). ★ หลุด → ไม่ pre-select. เปลี่ยน ธนาคาร/เลขบัญชี ของ used>0 = **บล็อกที่ master** (IR-BNK-01) → เอกสารเก่าไม่มีทางเพี้ยน.
- **GL post ไม่ได้ ถ้า:** ไม่ผูกกลุ่ม (posting_group=null) **หรือ** กลุ่ม account_1=NULL (ยังไม่ตั้ง COA ใน F-PG) — enforce ฝั่ง GL engine; view เตือนล่วงหน้า (BR-04). ดู EC-07.
- **`used` increment:** เขียนโดย GL/Journal engine ตอน post สำเร็จ (mechanism นอก scope FRD นี้ — OQ-BNK-07 นิยาม).
- ทุกแถว trace 06_TESTS §6.9.
