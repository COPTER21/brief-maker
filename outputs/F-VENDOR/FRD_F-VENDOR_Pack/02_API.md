# 02_API — F-VENDOR ทะเบียนคู่ค้า

> **Audience:** Backend developer  
> **Scope:** HTTP contracts only; business logicอยู่ใน `03_LOGIC.md`, declarative rulesอยู่ใน `05_RULES.md`

---

## §2.1 API Overview

| ID | Method | Path | Summary | Roles |
|---|---|---|---|---|
| F-VENDOR-API-01 | GET | `/api/v1/vendors` | list/search/filter vendors | authenticated |
| F-VENDOR-API-02 | GET | `/api/v1/vendors/refs` | form reference data | authenticated |
| F-VENDOR-API-03 | GET | `/api/v1/vendors/:vendor_id` | vendor detail aggregate | authenticated |
| F-VENDOR-API-04 | POST | `/api/v1/vendors` | create draft or create-and-submit-KYC | procurement_officer, admin |
| F-VENDOR-API-05 | PATCH | `/api/v1/vendors/:vendor_id` | amend aggregate | procurement_officer, admin |
| F-VENDOR-API-06 | POST | `/api/v1/vendors/:vendor_id/submit-kyc` | submit existing draft to KYC | procurement_officer, admin |
| F-VENDOR-API-07 | POST | `/api/v1/vendors/:vendor_id/kyc-decisions` | record KYC result | compliance_officer, admin |
| F-VENDOR-API-08 | POST | `/api/v1/vendors/:vendor_id/submit-approval` | resolve chain and submit | procurement_officer, admin |
| F-VENDOR-API-09 | POST | `/api/v1/vendors/:vendor_id/approval-decisions` | approve current step or reject | current approver role, admin |
| F-VENDOR-API-10 | POST | `/api/v1/vendors/:vendor_id/block` | risk/operational block | procurement roles, admin |
| F-VENDOR-API-11 | POST | `/api/v1/vendors/:vendor_id/unblock` | restore blocked vendor | procurement roles, admin |
| F-VENDOR-API-12 | POST | `/api/v1/vendors/:vendor_id/deactivate` | normal offboarding | procurement roles, admin |
| F-VENDOR-API-13 | POST | `/api/v1/vendors/:vendor_id/blacklist` | terminal blacklist | procurement_director, admin |
| F-VENDOR-API-14 | POST | `/api/v1/vendors/:vendor_id/bank-accounts/:bank_id/submit-verification` | send bank account for checking | finance_officer, admin |
| F-VENDOR-API-15 | POST | `/api/v1/vendors/:vendor_id/bank-accounts/:bank_id/verification-decisions` | verify/reject bank | finance_officer, admin |
| F-VENDOR-API-16 | POST | `/api/v1/vendors/:vendor_id/bank-accounts/:bank_id/deactivate` | soft-disable verified bank | finance_officer, admin |
| F-VENDOR-API-17 | POST | `/api/v1/vendors/:vendor_id/attachments` | attach scanned file metadata | procurement_officer, admin |
| F-VENDOR-API-18 | DELETE | `/api/v1/vendors/:vendor_id/attachments/:attachment_id` | soft-remove attachment | procurement_officer, admin |
| F-VENDOR-API-19 | GET | `/api/v1/vendors/:vendor_id/transaction-eligibility` | PO/PV readiness | authenticated service/user |
| F-VENDOR-API-20 | GET | `/api/v1/vendors/:vendor_id/price-list-summary` | read-only Price List summary | authenticated |

## §2.2 Common Contract

### Authentication and tenant

- `Authorization: Bearer <token>` required
- tenant is derived from trusted token context; `X-Tenant-Id` may be supplied but must match
- RLS is applied to every DB access
- roles are re-checked at mutation time

### Mutation headers

- `Idempotency-Key: <uuid>` required for every POST/PATCH/DELETE
- `If-Match: "<version>"` required for update/state mutation of an existing vendor
- same idempotency key + same canonical body within 24h returns the original result
- same key + different body → `409 ERR_IDEMPOTENCY_CONFLICT`
- version mismatch → `409 ERR_STALE_DATA`

### Standard error envelope

```json
{
  "error": {
    "code": "ERR_STALE_DATA",
    "message_key": "error.concurrency.stale",
    "field_errors": [],
    "correlation_id": "uuid"
  }
}
```

Common status: 400 validation, 401 unauthenticated, 403 forbidden, 404 not found, 409 conflict, 422 business rule, 500 internal.

## §2.3 Read Contracts

### F-VENDOR-API-01: GET /api/v1/vendors

| Field | Value |
|---|---|
| **auth** | required |
| **query** | `search`, `vendor_type`, `status`, `sort_by`, `sort_dir`, `page`, `page_size` |
| **validation** | enum values per `05_RULES`; `page_size` allowlist by platform config |
| **response** | 200 list envelope |
| **side effects** | Confidential/Restricted view audit when unmasked fields requested |
| **Calls (Logic)** | F-VENDOR-FN-01 |

```json
{
  "data": [{
    "id": "uuid",
    "vendor_code": "V-TH-TR-00001",
    "legal_name": "บริษัท ตัวอย่าง จำกัด",
    "vendor_type": "TR",
    "tax_id_masked": "0105•••••••01",
    "status": "active",
    "kyc_status": "passed",
    "version": 4
  }],
  "pagination": {"page": 1, "page_size": 20, "total": 1}
}
```

### F-VENDOR-API-02: GET /api/v1/vendors/refs

| Field | Value |
|---|---|
| **auth** | required |
| **response** | 200 with vendor types, status labels, countries, currencies, banks, bank purposes, payment terms and Thai address refs/version |
| **cache** | ETag allowed; reference changes must invalidate |
| **side effects** | none |
| **Calls (Logic)** | F-VENDOR-FN-02 |

### F-VENDOR-API-03: GET /api/v1/vendors/:vendor_id

| Field | Value |
|---|---|
| **auth** | required |
| **path** | `vendor_id` UUID |
| **response** | 200 aggregate with active/archived child records, KYC/approval/audit summaries |
| **field policy** | tax, credit, bank and risk fields masked/excluded by role |
| **errors** | 404 `ERR_VENDOR_NOT_FOUND` |
| **Calls (Logic)** | F-VENDOR-FN-01 |

Response includes `version`, `updated_at`, action capability flags derived server-side, and never exposes raw object keys or secrets.

### F-VENDOR-API-19: GET /api/v1/vendors/:vendor_id/transaction-eligibility

| Field | Value |
|---|---|
| **auth** | required; service-to-service permitted |
| **response** | 200 eligibility contract |
| **errors** | 404 `ERR_VENDOR_NOT_FOUND` |
| **Calls (Logic)** | F-VENDOR-FN-15 → F-VENDOR-ENG-01 |

```json
{
  "vendor_id": "uuid",
  "vendor_code": "V-TH-TR-00001",
  "status": "active",
  "kyc_status": "passed",
  "eligible_for_po": true,
  "eligible_for_payment": true,
  "default_payment_term_id": "uuid",
  "reason_codes": [],
  "version": 4
}
```

### F-VENDOR-API-20: GET /api/v1/vendors/:vendor_id/price-list-summary

| Field | Value |
|---|---|
| **auth** | required |
| **response** | 200 read-only totals/items/status summary |
| **fallback** | 200 empty summary if no list; downstream unavailable → 503, do not fabricate data |
| **Calls (Logic)** | F-VENDOR-FN-16 |

## §2.4 Vendor Aggregate Mutations

### Aggregate body

```json
{
  "legal_name": "บริษัท ตัวอย่าง จำกัด",
  "display_name": "ตัวอย่าง",
  "vendor_type": "TR",
  "country_code": "TH",
  "tax_id": "0105555555551",
  "vat_number": "0105555555551",
  "company_registration_no": "0105555555551",
  "branch_type": "head_office",
  "branch_code": "00000",
  "vat_registered": true,
  "currency_code": "THB",
  "default_payment_term_id": "uuid",
  "withholding_tax_rate": 3,
  "credit_limit": 100000,
  "contacts": [{"id": null, "contact_role": "primary", "contact_name": "สมชาย", "email": "buyer@example.com", "phone": "0812345678", "is_active": true}],
  "addresses": [{"id": null, "label": "สำนักงานใหญ่", "address_line": "99 ถนนสุขุมวิท", "province_code": "10", "district_code": "1001", "subdistrict_code": "100101", "is_billing": true, "is_primary_shipping": true, "is_active": true}],
  "bank_accounts": [{"id": null, "bank_code": "KBANK", "account_number": "0123456789", "account_name": "บริษัท ตัวอย่าง จำกัด", "purpose": "payment", "currency_code": "THB", "is_primary": true}],
  "save_action": "draft"
}
```

Server ignores client-supplied verification/approval/audit fields.

### F-VENDOR-API-04: POST /api/v1/vendors

| Field | Value |
|---|---|
| **roles** | procurement_officer, admin |
| **headers** | Idempotency-Key required |
| **body** | aggregate; `save_action=draft|submit_kyc` |
| **response** | 201 `{id,vendor_code,status,kyc_status,version}` |
| **errors** | 400 field validation; 409 duplicate/idempotency; 422 business rule |
| **side effects** | insert aggregate, audit; optional `vendor_kyc_submitted_event` |
| **Calls (Logic)** | F-VENDOR-FN-03, F-VENDOR-FN-05 → F-VENDOR-ENG-02 |

### F-VENDOR-API-05: PATCH /api/v1/vendors/:vendor_id

| Field | Value |
|---|---|
| **roles** | procurement_officer, admin |
| **headers** | Idempotency-Key + If-Match |
| **body** | partial aggregate + explicit child `id/is_active/role` state |
| **response** | 200 `{id,status,kyc_status,version,updated_at}` |
| **preconditions** | editable status; tax identity immutable after KYC pass |
| **side effects** | atomic update + child upsert/soft-disable + audit |
| **Calls (Logic)** | F-VENDOR-FN-04, F-VENDOR-FN-05 → F-VENDOR-ENG-02 |

Deleting a draft/new child absent from DB is a no-op. Persisted child records use `is_active=false`; verified bank identity cannot be changed through this endpoint.

### F-VENDOR-API-06: POST /api/v1/vendors/:vendor_id/submit-kyc

| Field | Value |
|---|---|
| **roles** | procurement_officer, admin |
| **headers** | Idempotency-Key + If-Match |
| **body** | `{}` |
| **response** | 200 `{status:"pending_kyc",kyc_status:"pending",version}` |
| **preconditions** | current status `draft` or `pending_kyc`; minimum KYC dataset valid |
| **side effects** | state/version update, audit, event |
| **Calls (Logic)** | F-VENDOR-FN-06, F-VENDOR-FN-05 |

## §2.5 KYC and Approval

### F-VENDOR-API-07: POST /api/v1/vendors/:vendor_id/kyc-decisions

| Field | Value |
|---|---|
| **roles** | compliance_officer, admin |
| **headers** | Idempotency-Key + If-Match |
| **body** | `{result:"passed|failed", sanctions_hit:boolean, sanctions_source:"OFAC|UN|EU|OTHER|null", review_note:string|null, provider_reference:string|null}` |
| **response** | 200 `{status,kyc_status,kyc_review_id,version}` |
| **preconditions** | status `draft|pending_kyc`; reviewer sees current vendor version |
| **side effects** | append KYC review, state/version update, WORM audit, event |
| **Calls (Logic)** | F-VENDOR-FN-07 |

Sanctions hit + result passed is rejected with `422 BR_SANCTIONS_HIT_CANNOT_PASS`.
Failed without sanctions returns `kyc_status:"failed"` while vendor remains/returns `status:"pending_kyc"`; only sanctions hit forces vendor `blocked`.

### F-VENDOR-API-08: POST /api/v1/vendors/:vendor_id/submit-approval

| Field | Value |
|---|---|
| **roles** | procurement_officer, admin |
| **headers** | Idempotency-Key + If-Match |
| **body** | `{}`; client cannot send threshold/chain |
| **response** | 200 `{status:"pending_approval",submission_round,policy_decision_ref,steps:[...]}` |
| **preconditions** | KYC passed + readiness rules |
| **side effects** | call Policy Center, snapshot steps, state update, audit/event |
| **Calls (Logic)** | F-VENDOR-FN-08 → external Policy Center |

### F-VENDOR-API-09: POST /api/v1/vendors/:vendor_id/approval-decisions

| Field | Value |
|---|---|
| **roles** | current `required_role`, procurement_director/admin override only if Policy Center permits |
| **headers** | Idempotency-Key + If-Match |
| **body** | `{decision:"approved|rejected", reason:string|null}` |
| **response** | 200 `{status,current_step,total_steps,version}` |
| **preconditions** | `pending_approval`, current pending step, maker ≠ approver |
| **side effects** | step decision, possible next step/activation/reject reset, audit/event |
| **Calls (Logic)** | F-VENDOR-FN-09 |

`reason` is required for rejected. Concurrent second decision receives 409.

## §2.6 Availability Mutations

All require Idempotency-Key + If-Match, body `{reason:"..."}`, update state/version atomically and append audit.

### F-VENDOR-API-10: POST /api/v1/vendors/:vendor_id/block

| Field | Value |
|---|---|
| **roles** | procurement_officer, procurement_manager, procurement_director, admin |
| **preconditions** | current status `active`; reason required |
| **response** | 200 `{previous_status:"active",status:"blocked",version}` |
| **side effects** | vendor/audit update + status/eligibility events |
| **Calls (Logic)** | F-VENDOR-FN-10 |

### F-VENDOR-API-11: POST /api/v1/vendors/:vendor_id/unblock

| Field | Value |
|---|---|
| **roles** | procurement_officer, procurement_manager, procurement_director, admin |
| **preconditions** | current status `blocked`; reason; KYC/policy still valid |
| **response** | 200 `{previous_status:"blocked",status:"active",version}` |
| **side effects** | vendor/audit update + status/eligibility events |
| **Calls (Logic)** | F-VENDOR-FN-10 |

### F-VENDOR-API-12: POST /api/v1/vendors/:vendor_id/deactivate

| Field | Value |
|---|---|
| **roles** | procurement_officer, procurement_manager, procurement_director, admin |
| **preconditions** | non-terminal allowed state; reason required |
| **response** | 200 `{previous_status,status:"inactive",version}` |
| **side effects** | vendor/audit update + status/eligibility events; historical references remain |
| **Calls (Logic)** | F-VENDOR-FN-10 |

### F-VENDOR-API-13: POST /api/v1/vendors/:vendor_id/blacklist

| Field | Value |
|---|---|
| **roles** | procurement_director, admin |
| **preconditions** | not already blacklisted; reason required |
| **response** | 200 `{previous_status,status:"blacklisted",version}` |
| **side effects** | terminal state/audit update + status/eligibility events |
| **Calls (Logic)** | F-VENDOR-FN-10 |

Errors: `BR_REASON_REQUIRED`, `BR_INVALID_STATE_TRANSITION`, `BR_BLACKLIST_TERMINAL`, `BR_VENDOR_NOT_READY`.

## §2.7 Bank Verification

### F-VENDOR-API-14: POST /api/v1/vendors/:vendor_id/bank-accounts/:bank_id/submit-verification

| Field | Value |
|---|---|
| **roles** | finance_officer, admin |
| **body** | `{evidence_attachment_id:"uuid|null"}` |
| **response** | 200 `{verification_status:"pending_verification",version}` |
| **preconditions** | active bank row in `unverified` state |
| **Calls (Logic)** | F-VENDOR-FN-11 |

### F-VENDOR-API-15: POST /api/v1/vendors/:vendor_id/bank-accounts/:bank_id/verification-decisions

| Field | Value |
|---|---|
| **roles** | finance_officer, admin |
| **body** | `{decision:"verified|rejected", reason:string|null}` |
| **response** | 200 bank summary + recalculated transaction eligibility |
| **preconditions** | `pending_verification`; reject requires reason |
| **Calls (Logic)** | F-VENDOR-FN-11 |

### F-VENDOR-API-16: POST /api/v1/vendors/:vendor_id/bank-accounts/:bank_id/deactivate

| Field | Value |
|---|---|
| **roles** | finance_officer, admin |
| **body** | `{reason:"..."}` |
| **response** | 200 `{verification_status:"disabled",eligible_for_payment,...}` |
| **preconditions** | bank is verified/active |
| **Calls (Logic)** | F-VENDOR-FN-12 → F-VENDOR-ENG-01 |

Deactivating the last verified bank does not silently change vendor `active`, but returns payment eligibility false and emits an eligibility-changed event.

## §2.8 Attachments

### F-VENDOR-API-17: POST /api/v1/vendors/:vendor_id/attachments

| Field | Value |
|---|---|
| **content** | platform upload contract or multipart; file must be scanned before active metadata commit |
| **metadata** | `document_type`, `issued_at`, `valid_until` |
| **response** | 201 attachment summary without object key |
| **errors** | invalid type/size, malware, duplicate checksum |
| **Calls (Logic)** | F-VENDOR-FN-13 → external object storage/scanner |

### F-VENDOR-API-18: DELETE /api/v1/vendors/:vendor_id/attachments/:attachment_id

| Field | Value |
|---|---|
| **response** | 204 |
| **behavior** | soft-remove metadata; object retention follows OQ-04/policy |
| **Calls (Logic)** | F-VENDOR-FN-14 |

## §2.9 API → Logic Trace

| API | Functions | Engines |
|---|---|---|
| API-01 | FN-01 | — |
| API-02 | FN-02 | — |
| API-03 | FN-01 | — |
| API-04 | FN-03, FN-05 | ENG-02 |
| API-05 | FN-04, FN-05 | ENG-02 |
| API-06 | FN-06, FN-05 | — |
| API-07 | FN-07 | — |
| API-08 | FN-08 | external Policy Center |
| API-09 | FN-09 | — |
| API-10..13 | FN-10 | — |
| API-14..15 | FN-11 | — |
| API-16 | FN-12 | ENG-01 |
| API-17 | FN-13 | external scanner/storage |
| API-18 | FN-14 | — |
| API-19 | FN-15 | ENG-01 |
| API-20 | FN-16 | external F-VENDOR-PRICE-LIST |

Authoritative R8 table: `03_LOGIC.md §3.3`

## §2.10 Cross-Module Contracts

| Edge | Consumer | Contract | Trigger | Payload |
|---|---|---|---|---|
| E-002 | F-VENDOR-PRICE-LIST | API-20 + vendor status event | price list view/bind; vendor availability change | `vendor_id,status` |
| E-007 | F-PO | API-19 or service lookup | vendor picker / before PO submit | `vendor_id,status,default_payment_term_id,eligible_for_po,reason_codes,version` |
| Payment dependency | PV/Payment | API-19 | before payment submission | `eligible_for_payment,reason_codes,verified_bank_required` |

### Events

```json
{
  "event": "vendor_status_changed_event",
  "tenant_id": "uuid",
  "vendor_id": "uuid",
  "previous_status": "active",
  "status": "blocked",
  "version": 5,
  "occurred_at": "2026-07-31T10:00:00Z"
}
```

Events: `vendor_created_event`, `vendor_kyc_submitted_event`, `vendor_kyc_decided_event`, `vendor_approval_submitted_event`, `vendor_approval_decided_event`, `vendor_status_changed_event`, `vendor_payment_eligibility_changed_event`.

- At-least-once delivery; consumers deduplicate by event id/version `[AI-DEFAULT]`
- Block/blacklist/inactive prevents new PO/payment but does not delete historical references
- Existing in-flight transaction handling is consumer-owned under GR-VEN-01
