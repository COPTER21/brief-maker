# 05_RULES — F-VENDOR ทะเบียนคู่ค้า

> **Audience:** Backend developer, QA, Security  
> **Purpose:** Declarative source of truth สำหรับ business rules, state, permissions, edge cases และ errors

---

## §5.1 Business Rules

### Identity and aggregate

| ID | Rule | Enforcement |
|---|---|---|
| BR-VEN-01 | TH `tax_id` ต้องเป็นเลข 13 หลักและ checksum ถูกต้อง | FN-05 + DB normalized hash |
| BR-VEN-02 | non-null tax identity unique ต่อ `(tenant,country)` | ENG-02 + partial unique DB |
| BR-VEN-03 | OT อาจไม่มี tax ID; ประเภทอื่นต้องมีเมื่อ submit KYC | FN-05 |
| BR-VEN-04 | code สร้างโดย server รูปแบบ `V-{CC}-{TT}-{NNNNN}` และไม่ reuse | FN-03 + unique DB |
| BR-VEN-05 | `legal_name` required, trimmed, 1..255 chars | FN-05 |
| BR-VEN-06 | bank account เป็นเลข 10..15 หลัก; verified identity เปลี่ยนไม่ได้ | FN-05/FN-11 |
| BR-VEN-07 | non-OT ต้องมี active verified bank ก่อน submit approval และก่อน payment | FN-08 + ENG-01 |
| BR-VEN-08 | ก่อน submit approval ต้องมี active contact อย่างน้อย 1 รายที่ email+phone valid | FN-08 |
| BR-VEN-09 | credit limit ≥ 0; WHT อยู่ใน 0..30 | FN-05 + DB check |
| BR-VEN-10 | ต้อง `kyc_status=passed` ก่อน submit/approve | FN-08/FN-09 |
| BR-VEN-11 | sanctions hit ห้าม pass KYC และทำให้ vendor `blocked` | FN-07 |
| BR-VEN-12 | tax ID immutable หลัง KYC passed | FN-04 + UI disabled |
| BR-VEN-13 | KYC decision ทำได้เฉพาะ Compliance/Admin | API role + FN-07 |
| BR-VEN-14 | KYC review ครอบคลุมเอกสาร, tax identity และ sanctions; provider policy อยู่ OQ-01 | FN-07 |
| BR-VEN-15 | approver ห้ามเป็น maker ของ vendor รอบนั้น (SoD) | FN-09 |
| BR-VEN-16 | ผู้อนุมัติต้องมี role ตรง current step ที่ snapshot จาก Policy Center | FN-09 |
| BR-VEN-17 | Policy Center resolve chain สำหรับทุก vendor type รวม OT; Vendor ไม่มี threshold/auto-approve | FN-08 |
| BR-VEN-18 | tax/credit = Confidential; bank account = Restricted; mask/exclude ตาม field policy | FN-01 + API serialization |
| BR-VEN-19 | reject ต้องมี reason, close current round, กลับ `pending_kyc`; submit ใหม่ resolve chain ใหม่ | FN-09 |
| BR-VEN-20 | `blacklisted` เป็น terminal; ไม่มี transition ออก | FN-10 + state matrix |
| BR-VEN-21 | aggregate edit ได้เฉพาะ `draft`, `pending_kyc`, `active`; active ยังติด immutable/verified-child rules | FN-04 |
| BR-VEN-22 | block, unblock, deactivate, blacklist และ reject ต้องมี reason | FN-09/FN-10/FN-12 |
| BR-VEN-23 | vendor/child ที่ persist หรือถูกอ้างอิงใช้ soft-disable; ห้าม hard delete/cascade | FN-04/10/12/14 + DB |
| BR-VEN-24 | active address ต้องมี exactly one billing และ one primary shipping; address เดียวรับสอง role ได้ | FN-05 + DB partial unique |
| BR-VEN-25 | ลบ/ปิดใช้ designated address ต้อง clear role และบังคับเลือก replacement อย่าง explicit ก่อน save | FN-04/FN-05 |
| BR-VEN-26 | verified bank เป็น read-only; การเปลี่ยนต้องเพิ่มบัญชีใหม่และปิดใช้บัญชีเดิม | FN-11/FN-12 |
| BR-VEN-27 | active vendor + KYC passed เท่านั้นที่ PO ใช้ทำรายการใหม่ได้ (GR-VEN-01) | ENG-01 |
| BR-VEN-28 | block/blacklist/inactive ห้าม transaction ใหม่ แต่ historical/in-flight recordsไม่ถูกลบ | ENG-01 + consumer contract |
| BR-VEN-29 | ทุก mutation, sensitive view และ decision ต้องมี tenant-scoped audit | middleware + functions |
| BR-VEN-30 | audit write failure ทำให้ mutation rollback `[AI-DEFAULT]` | transaction boundary |

## §5.2 State Machines

### Vendor lifecycle

```text
draft ──submit KYC──> pending_kyc ──submit approval──> pending_approval
  ▲                         │                               │
  │                         │ sanctions hit                 ├─ final approve → active
  │                         ▼                               └─ reject → pending_kyc
  │                      blocked <──── block ───────────── active
  │                         └──── valid unblock ──────────> active
  └─ save draft

non-terminal ──deactivate──> inactive
allowed non-terminal ──blacklist──> blacklisted (terminal)
```

| From | To | Action | Roles | Conditions |
|---|---|---|---|---|
| draft | draft | save draft | procurement_officer/admin | legal name present |
| draft | pending_kyc | submit KYC | procurement_officer/admin | minimum KYC dataset |
| pending_kyc | pending_kyc | amend/resubmit KYC | procurement_officer/admin | editable rules |
| pending_kyc | pending_approval | submit approval | procurement_officer/admin | KYC passed + readiness + Policy response |
| pending_approval | pending_approval | approve intermediate step | current approver/admin | SoD, current version |
| pending_approval | active | approve final step | current approver/admin | all prior steps approved |
| pending_approval | pending_kyc | reject | current approver/admin | reason required |
| draft/pending_kyc | blocked | sanctions hit | compliance/admin | source + note + decision evidence |
| active | blocked | block | authorized procurement/admin | reason required |
| blocked | active | unblock | authorized procurement/admin | KYC/policy still valid |
| permitted non-terminal | inactive | deactivate | authorized procurement/admin | reason required |
| permitted non-terminal | blacklisted | blacklist | director/admin | reason required |
| blacklisted | any | — | — | forbidden |

`inactive → active` reactivation ไม่อยู่ใน approved HTML/BRD; หากต้องการให้เปิดเป็น enhancement ใหม่

### KYC

| From | To | Conditions |
|---|---|---|
| pending | passed | reviewer Compliance/Admin, no sanctions hit |
| pending | failed | reason required; without sanctions vendor remains/returns `pending_kyc` |
| any reviewable | failed | sanctions hit + source + note; vendor blocked |
| passed | expired | only when OQ-02 policy exists |
| failed/expired | pending | explicit resubmit after correction |

### Bank verification

| From | To | Action |
|---|---|---|
| unverified | pending_verification | Finance `ส่งตรวจ` |
| pending_verification | verified | Finance `ยืนยันผล` |
| pending_verification | unverified | reject with reason |
| verified | disabled | Finance `ปิดใช้บัญชี` with reason |
| disabled | any | forbidden; add new bank |

## §5.3 Permission Matrix

| Capability | Officer | Manager | Director | Compliance | Finance | Admin | Viewer |
|---|---:|---:|---:|---:|---:|---:|---:|
| View list/detail | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Create/edit/submit KYC | ✅ | — | — | — | — | ✅ | — |
| KYC decision | — | — | — | ✅ | — | ✅ | — |
| Submit approval | ✅ | — | — | — | — | ✅ | — |
| Approve current step | policy role | policy role | policy role | — | — | policy override | — |
| Block/unblock/deactivate | ✅ | ✅ | ✅ | — | — | ✅ | — |
| Blacklist | — | — | ✅ | — | — | ✅ | — |
| Bank verification/full account | — | — | — | — | ✅ | ✅ | — |
| Full tax identity | — | — | — | ✅ | ✅ | ✅ | — |
| Full credit data | — | — | — | — | ✅ | ✅ | — |

Role naming must map to organization IAM roles; aliasesห้ามทำให้ permission กว้างขึ้น

Prototype alias mapping is explicit: HTML `finance` → IAM `finance_officer`; HTML `compliance` → IAM `compliance_officer`. The aliases grant exactly the mapped role capabilities and no override.

## §5.4 Validation Rules

| Field/aggregate | Rule | Error |
|---|---|---|
| `legal_name` | required, max 255 | `BR_VENDOR_NAME_REQUIRED` |
| `vendor_type` | one of 11 fixed codes | `BR_VENDOR_TYPE_INVALID` |
| `country_code` | valid reference | `BR_COUNTRY_INVALID` |
| `tax_id` | required except OT at submit; TH checksum | `BR_TAX_ID_INVALID` |
| `tax_id` uniqueness | tenant+country unique | `BR_DUPLICATE_TAX_ID` |
| `branch_code` | required for branch; valid reference format | `BR_BRANCH_INVALID` |
| `default_payment_term_id` | active reference | `BR_PAYMENT_TERM_INVALID` |
| `credit_limit` | numeric ≥0 | `BR_CREDIT_LIMIT_INVALID` |
| `withholding_tax_rate` | 0..30 | `BR_WHT_INVALID` |
| contact | submit approval needs ≥1 active with valid email+phone | `BR_CONTACT_REQUIRED` |
| address | submit/save active needs exactly one billing and shipping | `BR_ADDRESS_ROLE_REQUIRED` |
| bank | account number 10..15 digits; bank/currency/account name required | `BR_BANK_INVALID` |
| attachment | allowlist type/size + malware clean | `ERR_FILE_REJECTED` |
| reason | non-blank, trimmed for negative/status actions | `BR_REASON_REQUIRED` |

User input is normalized but original evidence remains in audit where legally allowed. All output is escaped; filenames are sanitized.

## §5.5 Edge Cases

### BRD-confirmed

| ID | Scenario | Resolution |
|---|---|---|
| EC-VEN-01 | duplicate tax ID in same tenant/country | block create/update with `BR_DUPLICATE_TAX_ID` |
| EC-VEN-02 | OT without tax ID | allowed; display `ยกเว้น (One-time)` |
| EC-VEN-03 | submit approval before KYC pass | 422 `BR_KYC_NOT_PASSED` |
| EC-VEN-04 | submit approval without valid contact | 422 `BR_CONTACT_REQUIRED` |
| EC-VEN-05 | non-OT submit approval without verified bank | 422 `BR_VERIFIED_BANK_REQUIRED` |
| EC-VEN-06 | maker approves own vendor | 422 `BR_SOD_VIOLATION` |
| EC-VEN-07 | wrong role approves current step | 422 `BR_WRONG_APPROVER` |
| EC-VEN-08 | sanctions hit | pass disabled; source+note required; failed+blocked |
| EC-VEN-09 | amend tax ID after KYC pass | UI read-only and server returns `BR_TAX_ID_IMMUTABLE` |
| EC-VEN-10 | reject after one or more approved steps | close round, `pending_kyc`, submit again resolves new chain |
| EC-VEN-11 | block vendor with transaction history | soft-block; vendor ID/history remain |
| EC-VEN-12 | try to leave blacklist | no UI action; server returns `BR_BLACKLIST_TERMINAL` |
| EC-VEN-13 | deactivate last verified bank of active vendor | vendor stays active; payment eligibility false + event |

### Activated probes and conservative defaults

| Probe | Scenario | Resolution |
|---|---|---|
| PR-1 | two approvers decide same step concurrently | first valid commit wins; second 409 stale/already decided `[AI-DEFAULT]` |
| PR-2 | stale edit overwrites newer data | `If-Match`/version required; mismatch 409 `[AI-DEFAULT]` |
| PR-3 | permission revoked while drawer open | role/policy re-check at mutation time; 403 |
| PR-4 | response lost after mutation commit | retry with same Idempotency-Key returns original result |
| PR-6 | close wizard before save | unsaved browser state is not authoritative; only explicit `บันทึกร่าง` persists `[AI-DEFAULT]` |
| PR-7 | double-click create/submit | one mutation; second request replays same result |

Additional:

- Policy Center timeout: no fallback chain; vendor remains prior state
- sanctions provider timeout: never auto-pass; keep pending/manual review `[AI-DEFAULT]`
- address role removed: save fails until explicit replacement
- cross-tenant ID supplied: return 404/403 per platform anti-enumeration policy, never leak existence
- audit/outbox failure: rollback mutation
- attachment scan failure: no active metadata/object download

## §5.6 Error Catalog

| Code | HTTP | Message key | Cause |
|---|---:|---|---|
| `ERR_VALIDATION_FAILED` | 400 | `error.validation.failed` | generic fields |
| `ERR_NOT_AUTHENTICATED` | 401 | `error.auth.unauthenticated` | token missing/invalid |
| `ERR_INSUFFICIENT_ROLE` | 403 | `error.auth.role` | role denied |
| `ERR_PERMISSION_REVOKED` | 403 | `error.auth.revoked` | mid-flight change |
| `ERR_VENDOR_NOT_FOUND` | 404 | `vendor.error.not_found` | absent/outside tenant |
| `ERR_ATTACHMENT_NOT_FOUND` | 404 | `vendor.attachment.not_found` | attachment absent |
| `ERR_STALE_DATA` | 409 | `error.concurrency.stale` | version mismatch |
| `ERR_IDEMPOTENCY_CONFLICT` | 409 | `error.idempotency.conflict` | same key, different input |
| `BR_DUPLICATE_TAX_ID` | 409 | `vendor.error.duplicate_tax_id` | duplicate identity |
| `ERR_POLICY_UNAVAILABLE` | 503 | `vendor.error.policy_unavailable` | cannot resolve chain |
| `ERR_REFERENCE_DATA_UNAVAILABLE` | 503 | `vendor.error.refs_unavailable` | refs unavailable |
| `ERR_PRICE_LIST_UNAVAILABLE` | 503 | `vendor.error.price_list_unavailable` | downstream unavailable |
| `BR_VENDOR_NAME_REQUIRED` | 422 | `vendor.error.name_required` | missing name |
| `BR_VENDOR_TYPE_INVALID` | 422 | `vendor.error.type_invalid` | bad enum |
| `BR_TAX_ID_INVALID` | 422 | `vendor.error.tax_invalid` | format/checksum |
| `BR_TAX_ID_IMMUTABLE` | 422 | `vendor.error.tax_locked` | change after KYC |
| `BR_KYC_NOT_PASSED` | 422 | `vendor.error.kyc_not_passed` | approval gate |
| `BR_SANCTIONS_HIT_CANNOT_PASS` | 422 | `vendor.error.sanctions_cannot_pass` | sanctions pass attempt |
| `BR_KYC_SOURCE_REQUIRED` | 422 | `vendor.error.kyc_source_required` | sanctions source absent |
| `BR_KYC_NOTE_REQUIRED` | 422 | `vendor.error.kyc_note_required` | evidence/reason absent |
| `BR_CONTACT_REQUIRED` | 422 | `vendor.error.contact_required` | no complete contact |
| `BR_VERIFIED_BANK_REQUIRED` | 422 | `vendor.error.bank_verified_required` | non-OT readiness |
| `BR_ADDRESS_ROLE_REQUIRED` | 422 | `vendor.error.address_role_required` | billing/shipping missing |
| `BR_SOD_VIOLATION` | 422 | `vendor.error.sod` | self-approval |
| `BR_WRONG_APPROVER` | 422 | `vendor.error.wrong_approver` | role not current step |
| `BR_REASON_REQUIRED` | 422 | `vendor.error.reason_required` | negative/status action |
| `BR_INVALID_STATE_TRANSITION` | 422 | `vendor.error.state_invalid` | transition forbidden |
| `BR_BLACKLIST_TERMINAL` | 422 | `vendor.error.blacklist_terminal` | leave terminal |
| `BR_BANK_STATE_INVALID` | 422 | `vendor.error.bank_state_invalid` | bank transition |
| `ERR_FILE_TYPE_NOT_ALLOWED` | 422 | `vendor.error.file_type` | disallowed file |
| `ERR_FILE_REJECTED` | 422 | `vendor.error.file_rejected` | size/malware |
| `ERR_DUPLICATE_ATTACHMENT` | 409 | `vendor.error.file_duplicate` | duplicate checksum |
| `ENG_ERR_INVALID_INPUT` | 500 | `error.engine.input` | internal contract failure |

## §5.7 Security and Compliance

- Authentication, session and tenant isolation required on every endpoint
- Confidential/Restricted access uses Policy Center field classification and is audited
- encrypt PII/financial values at rest; TLS in transit; secrets/key material never in code or logs
- object storage private by default; signed access short-lived and authorization rechecked
- KYC/approval/audit records immutable; retentionอย่างน้อย 7 ปี
- CSV/formula injection controls apply to future export even though export out of scope
- reason/note fields are untrusted text: escape output, scan for prohibited content, no HTML rendering
- use server timestamps/actor identity; never trust client actor or status

### P2 Security Trigger Map

| Trigger/domain | Required controls |
|---|---|
| Identity & Authentication | CUBE Auth SSO/MFA, trusted actor id, session policy |
| Access Control | AC-2/AC-3/AC-6 RBAC, least privilege, re-check every mutation |
| Separation of Duties | AC-5; maker ≠ approver, Compliance/Finance actions separated |
| Audit | AU-2/AU-9/AU-11; append-only WORM and 7-year retention |
| Communication/Storage | SC-8 TLS 1.3 minimum; SC-28 strong encryption at rest |
| Input/System Integrity | SI-10 validation, output escaping, attachment allowlist/malware scan |
| Privacy/PII | PDPA inventory, minimization, masking and sensitive-view audit |
| AML/Sanctions | sanctions evidence, forced fail/block, no timeout-as-pass |
| Multi-tenant | trusted tenant context + PostgreSQL RLS |

Source preset: BRD §16 P2 — Confidential PII. Platform Security Bible file was not supplied separately; implementation must map these triggers to the then-current platform control registry without weakening them.

### D-CLASS: Data Classification

| Layer | Confidential | Restricted |
|---|---|---|
| API | role check + masked response | explicit ACL; exclude by default |
| UI | masked value and no unauthorized action | hidden/masked; never rely on UI alone |
| DB | RLS + encrypted sensitive columns | RLS + stronger key/ACL separation |
| Audit | sensitive view + mutation | view, mutation, download/export attempts |

Policy Center Data Classification and Restricted Resources registration is required before production (OQ-06).

## §5.8 Cross-Module Golden Rule

GR-VEN-01:

- F-PO may create/submit new PO only when API-19 returns `eligible_for_po=true`
- Payment/PV may proceed only when `eligible_for_payment=true`
- blacklist/block/inactive affects new transactions immediately after event/lookup
- historical references remain; consumer decides whether already-approved work may complete
