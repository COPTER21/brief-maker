# 02_API — F-BNK Bank Master

> **Audience:** Backend developer (HTTP layer)
> **Purpose:** API contracts — CUBIC API Entity format
> **🚨 Iron Rule:** no business logic >5 lines here — moved to 03_LOGIC §3.1/§3.2
> **🚨 R8:** every mutation API lists "Calls (Logic)" → traced in 03_LOGIC §3.3
> **Convention:** `/api/v1/...`, plural nouns, `X-Tenant-Id` on all, `Idempotency-Key` on mutations, `If-Match` on account edit

---

## §2.1 API Overview

| ID | Method | Path | Summary | Auth (role) |
|---|---|---|---|---|
| F-BNK-API-01 | GET | /api/v1/bank-accounts | List company bank accounts (masked) | required |
| F-BNK-API-02 | POST | /api/v1/bank-accounts | Create bank account | finance_admin |
| F-BNK-API-03 | GET | /api/v1/bank-accounts/:id | Get account detail (masked) | required |
| F-BNK-API-04 | PUT | /api/v1/bank-accounts/:id | Edit account | finance_admin |
| F-BNK-API-05 | POST | /api/v1/bank-accounts/:id/reveal | **Reveal full account number (ACL-gated + audited)** ⭐ | requires `canRevealFull` |
| F-BNK-API-06 | POST | /api/v1/bank-accounts/:id/deactivate | Deactivate (active→inactive) | finance_admin |
| F-BNK-API-07 | POST | /api/v1/bank-accounts/:id/activate | Activate (inactive→active) | finance_admin |
| F-BNK-API-08 | POST | /api/v1/bank-accounts/:id/archive | Soft archive (→archived, terminal) | finance_admin |
| F-BNK-API-09 | POST | /api/v1/bank-accounts/:id/set-default | Set default pay/receive (1/company) | finance_admin |
| F-BNK-API-10 | GET | /api/v1/banks | List banks (preset + custom) | required |
| F-BNK-API-11 | POST | /api/v1/banks | Create custom bank | finance_admin |
| F-BNK-API-12 | PUT | /api/v1/banks/:id | Edit custom bank | finance_admin |
| F-BNK-API-13 | DELETE | /api/v1/banks/:id | Delete custom bank (**used=0 guard; preset never**) ⭐ | finance_admin |
| F-BNK-API-14 | GET | /api/v1/bank-accounts/:id/audit | Account audit stream | required |
| F-BNK-API-15 | GET | /api/v1/banks/:id/audit | Bank audit stream | required |
| F-BNK-API-16 | GET | /api/v1/bank-accounts/pickable | **Cross-module picker** (active only, masked) ⭐ | required (consumer feature) |

> **No DELETE on accounts** — soft archive only (Contract #7). `acc_no` is never returned in full by any endpoint except API-05 (reveal).

---

## §2.2 Per-API Contract

### F-BNK-API-01: GET /api/v1/bank-accounts

| Field | Value |
|---|---|
| **method** | GET · **path** /api/v1/bank-accounts · **auth** required · **roles** finance_admin, finance_user, accounting |
| **summary** | List accounts for a company, masked account numbers |

**Request — Query params:** `company_id` (required, uuid) · `status` (optional: active/inactive/archived/all) · `q` (optional: search bank/acc_name/last-4) · `limit` (default 50) · `offset`
**Headers:** `X-Tenant-Id` (required)

**Response 200:**
```json
{
  "data": [
    { "id": "BA-001", "company_id": "C1", "bank_code": "004", "bank_name_th": "ธนาคารกสิกรไทย",
      "acc_no_masked": "••••••5678", "acc_name": "บริษัท ทูบี ซิมเปิล จำกัด", "acct_type": "current",
      "branch": "สยามพารากอน", "gl_code": "1010-02", "currency": "THB", "status": "active",
      "default_pay": true, "default_receive": false, "used_in_doc": true }
  ],
  "total": 4, "limit": 50, "offset": 0
}
```
> `acc_no_masked` uses `acc_no_last4` — full number NEVER in list payload (R10/BR-BNK-09).

**Errors:** 400 ERR_INVALID_QUERY_PARAMS · 401 ERR_NOT_AUTHENTICATED · 403 ERR_INSUFFICIENT_ROLE
**Side effects:** — (read-only)
**Calls (Logic):** F-BNK-FN-04 buildAccountListQuery

---

### F-BNK-API-02: POST /api/v1/bank-accounts

| Field | Value |
|---|---|
| **method** | POST · **path** /api/v1/bank-accounts · **auth** required · **roles** finance_admin |

**Request — Headers:** `X-Tenant-Id`, `Idempotency-Key` (PR-7). **Body:**
```json
{ "company_id": "C1", "bank_code": "004", "acc_no": "0012345678", "acc_name": "…",
  "acct_type": "savings", "branch": "…", "gl_code": "1010-03",
  "default_pay": false, "default_receive": false }
```
**Field validation (≤5 lines):** `company_id` required uuid · `acc_no` required · `bank_code` required · `acc_name` required · `gl_code` required · `currency` server-forced `THB` (ignored if sent). **Complex validation → 03_LOGIC F-BNK-FN-03.**

**Response 201:** `{ "id": "BA-006", "status": "active", "acc_no_masked": "••••••5678", ... }`

**Errors:** 400 ERR_VALIDATION_FAILED · 403 ERR_INSUFFICIENT_ROLE · 409 ERR_DUPLICATE_IDEMPOTENCY_KEY · 422 `BR_ACCNO_DUPLICATE` (BR-BNK-01) · 422 `BR_ACCNO_FORMAT` (BR-BNK-03) · 422 `BR_GL_REQUIRED` (BR-BNK-11)
**Preconditions:** company exists; bank exists; gl_code exists in CoA.
**Side effects:** encrypt + INSERT T_company_bank_account (currency='THB', status='active') · set `acc_no_last4` · if default set → clear siblings (FN-06) · INSERT T_bank_audit_log (`created`) · increment T_bank.used_count.
**Calls (Logic):** F-BNK-FN-01 createBankAccount · F-BNK-FN-03 validateAccountForm · F-BNK-FN-06 enforceDefaultUnique · F-BNK-FN-12 appendAudit

---

### F-BNK-API-03: GET /api/v1/bank-accounts/:id
**Response 200:** full record with `acc_no_masked` (last-4 only). **Never** returns full `acc_no`.
**Errors:** 403 ERR_INSUFFICIENT_ROLE · 404 ERR_NOT_FOUND
**Calls (Logic):** F-BNK-FN-04 (single-fetch variant) — trivial read.

---

### F-BNK-API-04: PUT /api/v1/bank-accounts/:id

| Field | Value |
|---|---|
| **method** | PUT · **auth** finance_admin · **Headers** `X-Tenant-Id`, `If-Match` (version — PR-2) |

**Body:** editable subset (bank_code, acc_no, acc_name, acct_type, branch, gl_code). `currency` immutable (THB). `status` NOT edited here (use lifecycle endpoints).
**Response 200:** updated masked record.
**Errors:** 403 ERR_INSUFFICIENT_ROLE · 403 `ERR_PERMISSION_REVOKED` (re-check at mutation — EC-13) · 404 · 409 `ERR_STALE_DATA` (If-Match mismatch) · 422 BR_ACCNO_DUPLICATE / BR_ACCNO_FORMAT / BR_GL_REQUIRED
**Side effects:** re-encrypt `acc_no` if changed + refresh `acc_no_last4` · adjust T_bank.used_count if bank changed · INSERT audit (`edited`) · bump `version`.
**Calls (Logic):** F-BNK-FN-02 updateBankAccount · F-BNK-FN-03 validateAccountForm · F-BNK-FN-12 appendAudit

---

### F-BNK-API-05: POST /api/v1/bank-accounts/:id/reveal ⭐ (security spine)

| Field | Value |
|---|---|
| **method** | POST · **auth** required + **permission `canRevealFull`** · **Headers** `X-Tenant-Id` |
| **summary** | Return the full (unmasked) account number. **Backend-enforced permission (OQ-BNK-04) + mandatory append-only audit.** |

**Request:** no body (reason optional: `{ "reason": "verify before payment" }`).
**Response 200:** `{ "id": "BA-001", "acc_no": "0012345678", "revealed_at": "…", "audit_id": "…" }`
**Response 403 (no permission — EC-05):** `ERR_REVEAL_FORBIDDEN` — body stays masked; **UI shows toast "คุณไม่มีสิทธิ์ดูเลขบัญชีเต็ม"**. Attempt itself MAY be logged (`revealed` with denied flag) — see 05_RULES BR-BNK-09.
**Errors:** 401 · 403 ERR_REVEAL_FORBIDDEN · 404 · 429 `ERR_REVEAL_RATE_LIMITED` (threshold >50/user/day — BRD §17.4)
**Preconditions:** caller has `canRevealFull` (checked at THIS endpoint, not at GET).
**Side effects (MANDATORY, atomic with response):** decrypt `acc_no` · **INSERT T_bank_audit_log (`revealed`, actor, timestamp, account_id)** — if audit write fails, reveal MUST fail (audit-first; BRD §17.4 "audit write fail → block reveal").
**Calls (Logic):** F-BNK-FN-05 revealAccountNumber · **ENG-BNK-01 sensitive-field-masker** (reveal-gate) · F-BNK-FN-12 appendAudit

> **UI text (verbatim):** success toast "บันทึกการเข้าถึงเลขบัญชีเต็มแล้ว" (info) · denied toast "คุณไม่มีสิทธิ์ดูเลขบัญชีเต็ม" (warning) · button "ดูเต็ม" / "ซ่อน" · row tooltip "ต้องมีสิทธิ์ · ระบบจะบันทึกการเข้าถึง".

---

### F-BNK-API-06 / 07 / 08: Lifecycle transitions

| API | Path | From → To | Guard | Audit action | UI confirm |
|---|---|---|---|---|---|
| API-06 deactivate | POST …/:id/deactivate | active → inactive | must be active | `deactivated` | modal "ปิดใช้งานบัญชีนี้?" |
| API-07 activate | POST …/:id/activate | inactive → active | must be inactive (archived has NO path) | `activated` | button "เปิดใช้งาน" |
| API-08 archive | POST …/:id/archive | active/inactive → archived | terminal; used-in-doc allowed (soft archive) | `archived` | modal "เก็บถาวรบัญชีนี้?" |

**Common:** Headers `X-Tenant-Id`, `Idempotency-Key`. On deactivate/archive → **clear both default flags** + confirm modal shows a default-loss warning if it was a default (EC-14 / OQ-BNK-05 — RESOLVED 2026-08-06: warn + clear). Response 200 updated record. Errors: 403 · 404 · 422 `BR_INVALID_TRANSITION` (e.g. activate an archived account). Side effects: status update + INSERT audit + bump version. **No hard delete anywhere** (BR-BNK-06 / Contract #7).
**Calls (Logic):** F-BNK-FN-07 transitionAccountStatus · F-BNK-FN-12 appendAudit

---

### F-BNK-API-09: POST /api/v1/bank-accounts/:id/set-default

**Body:** `{ "field": "pay" | "receive", "value": true | false }`
**Guard:** account must be `active` (else 422 `BR_DEFAULT_REQUIRES_ACTIVE` — UI toast "บัญชีต้องอยู่สถานะใช้งานก่อนตั้งเป็นค่าเริ่มต้น"). Setting true clears same flag on all sibling accounts of the company (BR-BNK-02).
**Response 200:** updated record (+ any sibling whose flag was cleared).
**Side effects:** partial-unique index enforces 1/company; INSERT audit (`set-default`); concurrent writers → last-write-wins + audit both (EC-12).
**Calls (Logic):** F-BNK-FN-06 enforceDefaultUnique · F-BNK-FN-12 appendAudit

---

### F-BNK-API-10: GET /api/v1/banks
**Query:** `q` (name/SWIFT/code), `type` (local/foreign/all). **Response 200:** array of `{ id, code, name_th, abbr, swift, type, is_custom, used_count }`. Read-only.
**Calls (Logic):** F-BNK-FN-04 (bank list variant) — trivial.

---

### F-BNK-API-11: POST /api/v1/banks (create custom bank)
**Body:** `{ "name_th": "…", "abbr": "HSBC", "code": "070"|null, "swift": "HSBCTHBK", "type": "foreign" }`
**Response 201.** **Errors:** 422 `BR_SWIFT_FORMAT` (BR-BNK-04) · 422 `BR_SWIFT_DUPLICATE` (UI "รหัส SWIFT นี้มีอยู่แล้ว") · 422 `BR_BOTCODE_FORMAT` (3 digits if present).
**Side effects:** INSERT T_bank (is_custom=true) · INSERT bank audit (`bank-added`).
**Calls (Logic):** F-BNK-FN-08 createCustomBank · **ENG-BNK-02 swift-bic-validator** · F-BNK-FN-12 appendAudit

---

### F-BNK-API-12: PUT /api/v1/banks/:id (edit custom bank)
**Guard:** `is_custom=true` only — preset → 403 `ERR_PRESET_READONLY` (UI toast "ธนาคารมาตรฐาน ธปท. แก้ไขไม่ได้"). `code` read-only in edit.
**Errors:** 403 ERR_PRESET_READONLY · 422 BR_SWIFT_FORMAT / BR_SWIFT_DUPLICATE.
**Side effects:** UPDATE T_bank · INSERT bank audit (`bank-edited`).
**Calls (Logic):** F-BNK-FN-09 updateCustomBank · ENG-BNK-02 swift-bic-validator · F-BNK-FN-12 appendAudit

---

### F-BNK-API-13: DELETE /api/v1/banks/:id ⭐ (W1 — R-08 exception to Contract #7)

| Field | Value |
|---|---|
| **method** | DELETE · **auth** finance_admin |
| **summary** | Hard-delete a **custom** bank **only when `used_count = 0`**. Preset banks are never deletable. Explicit, audited exception to Global Contract #7 (no-hard-delete). |

**Guard order:** (1) not custom → 403 `ERR_PRESET_READONLY`; (2) `used_count > 0` → 422 `BR_BANK_IN_USE` (UI toast "ลบไม่ได้ — มี {N} บัญชีอ้างอิงธนาคารนี้อยู่ (ย้าย/ปิดบัญชีก่อน)"; delete button disabled with tooltip "มี {N} บัญชีอ้างอิงธนาคารนี้ — ลบไม่ได้"); (3) else delete.
**Response 200:** `{ "deleted": true, "id": "…" }`
**Side effects:** DELETE row from T_bank · INSERT bank audit (`bank-removed`) — audit survives the deletion (append-only stream keyed by bank_code stays).
**Calls (Logic):** F-BNK-FN-10 deleteCustomBank · F-BNK-FN-12 appendAudit

---

### F-BNK-API-14 / 15: Audit streams (read)
- **API-14** GET …/bank-accounts/:id/audit → account stream (`account_id = :id`), newest-first. Detail masked (never full acc_no in detail).
- **API-15** GET …/banks/:id/audit → bank stream (`bank_code`), newest-first.
**Response 200:** `[{ action, detail, actor_name, created_at }]`. Read-only.
**Calls (Logic):** — (trivial read; ORDER BY created_at DESC)

---

### F-BNK-API-16: GET /api/v1/bank-accounts/pickable ⭐ (cross-module picker)
| Field | Value |
|---|---|
| **summary** | Returns **active-only, masked** accounts for a company for consumer documents to snapshot. Powers PV / RV / Bank Recon / Payroll pickers (soft-reference). |

**Query:** `company_id` (required) · `purpose` (optional: `pay`/`receive` → hints default). **Response 200:** `[{ id, bank_name_th, acc_no_masked, acc_name, gl_code, currency, is_default_pay, is_default_receive }]` — **inactive/archived excluded** (BR-BNK-05).
**Consumer contract:** consumer must **snapshot** returned values into its own document (no live lookup) — Contract #6.
**Calls (Logic):** F-BNK-FN-11 buildPickableAccounts

---

## §2.3 Common Concerns

**Idempotency (PR-7):** all POST create endpoints require `Idempotency-Key`; 24h cache; same key+body → cached; same key+diff body → 409.
**Optimistic Locking (PR-2):** PUT account (API-04) requires `If-Match: <version>`; mismatch → 409 `ERR_STALE_DATA`.
**Multi-Tenant:** `X-Tenant-Id` on all; PostgreSQL RLS.
**Permission re-check (EC-13 / OQ-BNK-04):** role + `canRevealFull` re-evaluated at mutation/reveal time, never trusted from GET — hiding the button is NOT the control.
**Audit:** every mutation + every reveal → T_bank_audit_log via FN-12 (append-only). Detail strings never contain full account number (last-4 only).
**Sensitive response hygiene:** `acc_no` full value appears ONLY in API-05 response. Logs/errors/audit detail carry last-4 only.

---

## §2.4 API → Logic Trace (anchor for R8) — authoritative in 03_LOGIC §3.3

| API | Calls Functions | Calls Engines |
|---|---|---|
| API-01 GET /bank-accounts | FN-04 | — |
| API-02 POST /bank-accounts | FN-01, FN-03, FN-06, FN-12 | — |
| API-03 GET /bank-accounts/:id | FN-04 | — |
| API-04 PUT /bank-accounts/:id | FN-02, FN-03, FN-12 | — |
| API-05 POST …/reveal | FN-05, FN-12 | ENG-BNK-01 |
| API-06 POST …/deactivate | FN-07, FN-12 | — |
| API-07 POST …/activate | FN-07, FN-12 | — |
| API-08 POST …/archive | FN-07, FN-12 | — |
| API-09 POST …/set-default | FN-06, FN-12 | — |
| API-10 GET /banks | FN-04 | — |
| API-11 POST /banks | FN-08, FN-12 | ENG-BNK-02 |
| API-12 PUT /banks/:id | FN-09, FN-12 | ENG-BNK-02 |
| API-13 DELETE /banks/:id | FN-10, FN-12 | — |
| API-14 GET …/audit (acct) | — | — |
| API-15 GET …/audit (bank) | — | — |
| API-16 GET /bank-accounts/pickable | FN-11 | — |

> **R8 check:** every mutation row has ≥1 Function/Engine. ✅

---

## §2.X Cross-Module Contract ⭐ (R12 — from BRD §12.1 Downstream Impact Map)

> Every downstream with data flow has a contract. Pattern = `config master → doc` = **PULL on create + snapshot** (Central Plan §Global Contract #6). Bank Master exposes API-16 + emits soft events; consumers snapshot.

| Downstream | รูปแบบ | Contract | Trigger | Payload หลัก | ถ้าบัญชีถูกปิด/เก็บถาวร/แก้ |
|---|---|---|---|---|---|
| **Payment Voucher** | Endpoint (consumer pulls) | GET /bank-accounts/pickable?company&purpose=pay | on PV create (pick pay-from) | account_id, bank_name, acc_no_masked, gl_code | inactive → absent from picker; existing PV keeps snapshot (soft-ref) |
| **Receipt Voucher** | Endpoint | GET /bank-accounts/pickable?company&purpose=receive | on RV create | + is_default_receive (pre-select) | same; default-receive pre-selects |
| **Bank Reconciliation** | Endpoint | GET /bank-accounts/pickable?company + GET /:id | on recon period setup | account_id, gl_code, acc_no_masked | archived keeps recon history (no cascade) |
| **Payroll** ⭐ | Endpoint | GET /bank-accounts/pickable?company&purpose=pay | on payroll run (pick disbursement account) | account_id, gl_code (1010-06), acc_no_masked | payroll disbursement acct inactive → new run can't pick; existing run keeps snapshot |
| **Chart of Accounts (inbound)** | Endpoint (this pulls) | GET /chart-of-accounts (CoA) | on account create/edit (GL combobox) | gl_code, name | GL disabled in CoA → account keeps code; warn at posting (EC-11) |

- **Compensating behavior:** archive/deactivate does NOT cascade to consumer docs — soft-ref snapshot preserved. No `pr.cancelled`-style release needed (master change never rewrites issued docs).
- Every downstream row traced to 06_TESTS §6.9 (XT-01..XT-04).
