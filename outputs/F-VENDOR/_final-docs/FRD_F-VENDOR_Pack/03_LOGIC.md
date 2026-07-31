# 03_LOGIC — F-VENDOR ทะเบียนคู่ค้า

> **Audience:** Backend developer, Architect  
> **Iron rule:** UI → API → Function → Engine/Integration; functionsไม่มี HTTP context

---

## §3.1 Scope-Local Functions

### F-VENDOR-FN-01: `queryVendorAggregate`

- **Purpose:** สร้าง tenant-scoped list/detail query, apply filter/sort/page และ field masking policy
- **Input:** `{tenant_id, actor, vendor_id?, filters?, pagination?}`
- **Output:** `VendorList | VendorDetail`
- **Invoked by:** API-01, API-03
- **Calls:** Policy Center field policy
- **Side effects:** audit unmasked Confidential/Restricted views
- **Errors:** `ERR_VENDOR_NOT_FOUND`, `ERR_FIELD_ACCESS_DENIED`

### F-VENDOR-FN-02: `loadVendorReferences`

- **Purpose:** รวม reference data สำหรับ form พร้อม version/ETag
- **Input:** `{tenant_id, locale}`
- **Output:** `VendorReferenceBundle`
- **Invoked by:** API-02
- **Calls:** payment terms, bank, country/currency, Thai address repositories
- **Side effects:** none
- **Errors:** `ERR_REFERENCE_DATA_UNAVAILABLE`

### F-VENDOR-FN-03: `createVendorAggregate`

- **Purpose:** สร้าง vendor code และ aggregate ใน transaction เดียว
- **Input:** `{tenant_id, actor, aggregate, save_action, idempotency_context}`
- **Output:** `{vendor_id,vendor_code,status,version}`
- **Invoked by:** API-04
- **Calls:** FN-05, ENG-02
- **Side effects:** insert vendor/children, audit, optional KYC-submitted event
- **Errors:** validation/duplicate/idempotency codesใน `05_RULES.md`

### F-VENDOR-FN-04: `updateVendorAggregate`

- **Purpose:** amend allowed fields, upsert children และ soft-disable removed persisted children
- **Input:** `{vendor_id,actor,patch,expected_version}`
- **Output:** `{vendor_id,status,version,updated_at}`
- **Invoked by:** API-05
- **Calls:** FN-05, ENG-02
- **Side effects:** atomic updates, audit, possible eligibility-changed event
- **Errors:** `ERR_STALE_DATA`, `BR_VENDOR_NOT_EDITABLE`, `BR_TAX_ID_IMMUTABLE`

Address role removal is explicit: clear billing/shipping flags after confirmation and reject final save until replacements are selected.

### F-VENDOR-FN-05: `validateVendorAggregate`

- **Purpose:** รวม validation ที่ create/update/submit ใช้ร่วมกัน
- **Input:** `{aggregate, mode:draft|submit_kyc|submit_approval, current_record?}`
- **Output:** `{valid,errors[],normalized}`
- **Invoked by:** API-04, API-05, API-06; FN-03/04/06/08
- **Calls:** ENG-02
- **Side effects:** none
- **Errors:** field/business errorsใน §5.4/§5.6

### F-VENDOR-FN-06: `submitVendorForKyc`

- **Purpose:** ตรวจ minimum KYC dataset และ transition เป็น `pending_kyc`
- **Input:** `{vendor_id,actor,expected_version}`
- **Output:** `{status,kyc_status,version}`
- **Invoked by:** API-06; optionally FN-03
- **Calls:** FN-05
- **Side effects:** update vendor, append audit, emit event
- **Errors:** `BR_INVALID_STATE_TRANSITION`, `ERR_VALIDATION_FAILED`

### F-VENDOR-FN-07: `recordVendorKycDecision`

- **Purpose:** บันทึกผล KYC/sanctions แบบ append-only และเปลี่ยน state atomically
- **Input:** `{vendor_id,actor,result,sanctions_hit,source?,note?,provider_reference?,expected_version}`
- **Output:** `{kyc_review_id,status,kyc_status,version}`
- **Invoked by:** API-07
- **Calls:** external sanctions evidence adapter when configured
- **Side effects:** append review; update vendor; audit/event
- **Errors:** `BR_SANCTIONS_HIT_CANNOT_PASS`, `BR_KYC_SOURCE_REQUIRED`, `BR_KYC_NOTE_REQUIRED`

Decision:

1. sanctions hit → source + note required, result forced failed, vendor `blocked`
2. failed without sanctions → note required, KYC `failed`, vendor remains/returns `pending_kyc` for correction and explicit resubmission
3. passed → KYC `passed`; vendor remains `pending_kyc` until explicit approval submission

### F-VENDOR-FN-08: `submitVendorForApproval`

- **Purpose:** ตรวจ readiness, ขอ Policy Center resolve chain และ snapshot decision
- **Input:** `{vendor_id,actor,expected_version}`
- **Output:** `{submission_round,policy_decision_ref,steps,status}`
- **Invoked by:** API-08
- **Calls:** FN-05, external Policy Center `resolve`
- **Side effects:** insert approval steps, update `pending_approval`, audit/event
- **Errors:** `BR_KYC_NOT_PASSED`, `BR_VENDOR_NOT_READY`, `ERR_POLICY_UNAVAILABLE`

Vendor ห้ามคำนวณ threshold หรือสร้าง fallback chain ใน production

### F-VENDOR-FN-09: `recordVendorApprovalDecision`

- **Purpose:** apply approve/reject ต่อ current step ด้วย SoD และ optimistic concurrency
- **Input:** `{vendor_id,actor,decision,reason?,expected_version}`
- **Output:** `{status,current_step,total_steps,version}`
- **Invoked by:** API-09
- **Calls:** none
- **Side effects:** update step/vendor; cancel remaining steps on reject; audit/event
- **Errors:** `ERR_STALE_DATA`, `BR_SOD_VIOLATION`, `BR_WRONG_APPROVER`, `BR_REASON_REQUIRED`

Approve final step → `active`; reject → `pending_kyc`, clear current chain by closing round, next submit resolves a new chain.

### F-VENDOR-FN-10: `changeVendorAvailability`

- **Purpose:** ใช้ state transition เดียวสำหรับ block/unblock/deactivate/blacklist
- **Input:** `{vendor_id,actor,action,reason,expected_version}`
- **Output:** `{previous_status,status,version}`
- **Invoked by:** API-10..API-13
- **Calls:** F-VENDOR-ENG-01 for post-change eligibility
- **Side effects:** update vendor, audit, status/eligibility events
- **Errors:** `BR_INVALID_STATE_TRANSITION`, `BR_BLACKLIST_TERMINAL`, `BR_REASON_REQUIRED`

### F-VENDOR-FN-11: `recordBankVerification`

- **Purpose:** submit or decide bank verification โดย Finance
- **Input:** `{vendor_id,bank_id,actor,action,evidence?,decision?,reason?,expected_version}`
- **Output:** `BankVerificationResult`
- **Invoked by:** API-14, API-15
- **Calls:** none
- **Side effects:** update bank immutable verification fields, vendor audit, eligibility event if changed
- **Errors:** `BR_BANK_STATE_INVALID`, `BR_REASON_REQUIRED`, `ERR_STALE_DATA`

### F-VENDOR-FN-12: `deactivateVerifiedBank`

- **Purpose:** soft-disable verified bank โดยรักษา identity/history
- **Input:** `{vendor_id,bank_id,actor,reason,expected_version}`
- **Output:** `{bank_status,eligibility,version}`
- **Invoked by:** API-16
- **Calls:** ENG-01
- **Side effects:** update bank, adjust primary flag, audit/event
- **Errors:** `BR_BANK_STATE_INVALID`, `BR_REASON_REQUIRED`

### F-VENDOR-FN-13: `attachVendorDocument`

- **Purpose:** ผูกไฟล์ที่ upload/scan ผ่านแล้วกับ vendor
- **Input:** `{vendor_id,actor,file_token,metadata}`
- **Output:** `AttachmentSummary`
- **Invoked by:** API-17
- **Calls:** external object storage/malware scanner
- **Side effects:** insert attachment metadata, audit
- **Errors:** `ERR_FILE_TYPE_NOT_ALLOWED`, `ERR_FILE_REJECTED`, `ERR_DUPLICATE_ATTACHMENT`

### F-VENDOR-FN-14: `removeVendorAttachment`

- **Purpose:** soft-remove attachment metadata ตาม retention policy
- **Input:** `{vendor_id,attachment_id,actor}`
- **Output:** `void`
- **Invoked by:** API-18
- **Calls:** none
- **Side effects:** set inactive, audit, schedule object retention action
- **Errors:** `ERR_ATTACHMENT_NOT_FOUND`, `BR_ATTACHMENT_LOCKED`

### F-VENDOR-FN-15: `getVendorTransactionEligibility`

- **Purpose:** สร้าง readiness snapshot สำหรับ PO/PV
- **Input:** `{vendor_id,tenant_id}`
- **Output:** `TransactionEligibility`
- **Invoked by:** API-19; FN-10/11/12
- **Calls:** ENG-01
- **Side effects:** none
- **Errors:** `ERR_VENDOR_NOT_FOUND`

### F-VENDOR-FN-16: `getVendorPriceListSummary`

- **Purpose:** อ่าน summary จาก F-VENDOR-PRICE-LIST โดยไม่ให้ Vendor แก้ข้อมูลนั้น
- **Input:** `{vendor_id,tenant_id,actor}`
- **Output:** `PriceListSummary`
- **Invoked by:** API-20
- **Calls:** external F-VENDOR-PRICE-LIST
- **Side effects:** none
- **Errors:** `ERR_PRICE_LIST_UNAVAILABLE`

## §3.2 Engines

### F-VENDOR-ENG-01: `vendor-transaction-eligibility-engine` [NEW CANDIDATE]

| Field | Value |
|---|---|
| **code** | `vendor-transaction-eligibility-engine` |
| **category** | validation |
| **version/status** | 1.0.0 / DRAFT |
| **owner** | shared Purchase platform |
| **stateless** | true |

**Input schema**

```json
{
  "type": "object",
  "required": ["vendor_type", "status", "kyc_status", "has_verified_bank"],
  "properties": {
    "vendor_type": {"type": "string"},
    "status": {"type": "string"},
    "kyc_status": {"type": "string"},
    "has_verified_bank": {"type": "boolean"}
  }
}
```

**Output schema**

```json
{
  "type": "object",
  "required": ["eligible_for_po", "eligible_for_payment", "reason_codes"],
  "properties": {
    "eligible_for_po": {"type": "boolean"},
    "eligible_for_payment": {"type": "boolean"},
    "verified_bank_required": {"type": "boolean"},
    "reason_codes": {"type": "array", "items": {"type": "string"}}
  }
}
```

**Logic outline**

1. PO eligible only if `status=active` and `kyc_status=passed`
2. Payment begins with the same gate
3. non-OT additionally requires `has_verified_bank=true`; OT does not
4. return all blocking reason codes deterministically

**Errors:** `ENG_ERR_INVALID_INPUT`

**Used by:** F-VENDOR, F-PO, Payment/PV

**Iron rules:** stateless ✅ · pure ✅ · deterministic ✅ · reusable 3 consumers ✅ · substantial decision matrix ✅

### F-VENDOR-ENG-02: `vendor-duplicate-match-engine` [NEW CANDIDATE]

| Field | Value |
|---|---|
| **code** | `vendor-duplicate-match-engine` |
| **category** | matcher |
| **version/status** | 1.0.0 / DRAFT |
| **owner** | Master Data platform |
| **stateless** | true |

**Input schema**

```json
{
  "type": "object",
  "required": ["candidate", "existing_candidates"],
  "properties": {
    "candidate": {
      "type": "object",
      "required": ["country_code", "legal_name"],
      "properties": {
        "country_code": {"type": "string"},
        "tax_id_hash": {"type": ["string", "null"]},
        "legal_name": {"type": "string"},
        "bank_account_hashes": {"type": "array", "items": {"type": "string"}}
      }
    },
    "existing_candidates": {"type": "array"}
  }
}
```

**Output schema**

```json
{
  "type": "object",
  "required": ["hard_duplicate", "matches"],
  "properties": {
    "hard_duplicate": {"type": "boolean"},
    "matches": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "vendor_id": {"type": "string"},
          "match_reasons": {"type": "array"},
          "confidence": {"type": "number"}
        }
      }
    }
  }
}
```

**Logic outline**

1. exact normalized country + tax hash is a hard duplicate
2. bank hash/name similarity are warning candidates, not automatic merge
3. return deterministic reasons/score; never expose raw tax/bank values

**Errors:** `ENG_ERR_INVALID_INPUT`

**Used by:** F-VENDOR create/update, future vendor import/migration and shared master-data quality

**Iron rules:** stateless ✅ · pure ✅ · deterministic ✅ · reusable planned ✅ · substantial matcher ✅

## §3.3 API ↔ Logic Trace (R8 Anchor)

| API ID | Method | Calls Functions | Calls Engines / External |
|---|---|---|---|
| API-01 | GET | FN-01 | Policy field policy |
| API-02 | GET | FN-02 | reference services |
| API-03 | GET | FN-01 | Policy field policy |
| API-04 | POST | FN-03, FN-05 | ENG-02 |
| API-05 | PATCH | FN-04, FN-05 | ENG-02 |
| API-06 | POST | FN-06, FN-05 | — |
| API-07 | POST | FN-07 | sanctions evidence adapter |
| API-08 | POST | FN-08 | Policy Center |
| API-09 | POST | FN-09 | — |
| API-10 | POST | FN-10, FN-15 | ENG-01 |
| API-11 | POST | FN-10, FN-15 | ENG-01 |
| API-12 | POST | FN-10, FN-15 | ENG-01 |
| API-13 | POST | FN-10, FN-15 | ENG-01 |
| API-14 | POST | FN-11 | — |
| API-15 | POST | FN-11, FN-15 | ENG-01 |
| API-16 | POST | FN-12, FN-15 | ENG-01 |
| API-17 | POST | FN-13 | scanner/storage |
| API-18 | DELETE | FN-14 | — |
| API-19 | GET | FN-15 | ENG-01 |
| API-20 | GET | FN-16 | F-VENDOR-PRICE-LIST |

**Verification:** mutation APIs 15/15 have function trace; functions 16/16 are invoked; engines 2/2 are traced.

## §3.4 External Boundaries

| Boundary | Ownership | Failure policy |
|---|---|---|
| Policy Center approval resolve | Policy Center | timeout/error keeps vendor out of `pending_approval`; no local fallback chain |
| Sanctions provider | Security/Compliance | timeout cannot be treated as pass; remain pending/manual review `[AI-DEFAULT]` |
| Object storage/scanner | Platform | file metadata active only after clean result |
| F-VENDOR-PRICE-LIST | Purchase domain | unavailable returns explicit 503/empty only where contract allows |
| Notification service | Platform | core mutation commits via outbox; delivery retries |

## §3.5 Logic Placement Notes

- thresholds, status transitions, role permissions and validation constants: `05_RULES.md`
- request parsing/status codes: `02_API.md`
- DB constraints/classification: `04_DB.md`
- external I/O remains in adapters/functions, not pure engines
- approval decision and sanctions evidence are snapshotted so later policy/provider changes do not rewrite historical decisions
