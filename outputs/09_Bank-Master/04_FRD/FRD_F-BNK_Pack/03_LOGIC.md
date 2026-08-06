# 03_LOGIC — F-BNK Bank Master

> **Audience:** BE dev (business logic layer)
> **Scope:** all non-HTTP logic — functions, validations, state transitions, masking/reveal, integrations
> **CUBIC alignment:** §3.1 Functions = scope-local · §3.2 Engines = CUBIC candidates
> **Iron Rule R8:** every mutation API traces to ≥1 Function/Engine in §3.3
> Function code = camelCase · Engine code = kebab-case

---

## §3.1 Functions (Scope-Local)

### F-BNK-FN-01: `createBankAccount`
- **Purpose:** Create a company bank account from validated form input.
- **Input:** `{ company_id, bank_code, acc_no, acc_name, acct_type, branch, gl_code, default_pay, default_receive, actor }`
- **Output:** `CompanyBankAccount | ValidationError[]`
- **Invoked by:** F-BNK-API-02
- **Calls:** F-BNK-FN-03 (validate), F-BNK-FN-06 (default-unique if flags set), ENG-BNK-01 (compute `acc_no_last4` + encrypt), F-BNK-FN-12 (audit)
- **Side effects:** INSERT T_company_bank_account (currency forced `THB`, status `active`); increment T_bank.used_count; audit `created`.
- **Error cases:** BR_ACCNO_DUPLICATE, BR_ACCNO_FORMAT, BR_GL_REQUIRED → see 05_RULES.
- **Iron rule check:** ✅ no HTTP terms.

### F-BNK-FN-02: `updateBankAccount`
- **Purpose:** Apply edits to an existing account (identity fields; not status).
- **Input:** `{ id, patch:{ bank_code?, acc_no?, acc_name?, acct_type?, branch?, gl_code? }, expected_version, actor }`
- **Output:** `CompanyBankAccount | ValidationError[] | StaleError`
- **Invoked by:** F-BNK-API-04
- **Calls:** F-BNK-FN-03, ENG-BNK-01 (re-mask/encrypt if acc_no changed), F-BNK-FN-12
- **Side effects:** UPDATE row (bump `version`); adjust T_bank.used_count if bank changed; audit `edited`.
- **Error cases:** ERR_STALE_DATA (version mismatch), ERR_PERMISSION_REVOKED (re-check role), BR_ACCNO_*, BR_GL_REQUIRED.
- **Iron rule check:** ✅

### F-BNK-FN-03: `validateAccountForm`
- **Purpose:** Central account validation (used by create + edit).
- **Input:** `{ company_id, id?, bank_code, acc_no, acc_name, gl_code, acct_type }`
- **Output:** `ValidationError[] (empty = valid)`
- **Invoked by:** FN-01, FN-02 (and API-02/04 preconditions)
- **Calls:** —
- **Logic:**
  1. `bank_code` empty → `กรุณาเลือกธนาคาร`
  2. `acc_no` empty → `กรุณากรอกเลขที่บัญชี`; else must match `^[0-9]{R}$` where R = config `accNo_length_range` (default 10–15, BR-BNK-03) → `เลขบัญชีต้องเป็นตัวเลข 10-15 หลัก`
  3. duplicate: exists account same `company_id` + same `acc_no` + different `id` → `เลขบัญชีนี้มีอยู่แล้วในบริษัทนี้` (BR-BNK-01)
  4. `acc_name` empty → `กรุณากรอกชื่อบัญชี`
  5. `gl_code` empty → `กรุณาเลือกบัญชี GL` (BR-BNK-11)
- **Iron rule check:** ✅ (range read from config, NOT hardcoded — CONFIGURABLE R-03)

### F-BNK-FN-04: `buildAccountListQuery`
- **Purpose:** Build masked, company-scoped, status-filtered list query (also single-fetch + bank-list variants).
- **Input:** `{ tenant_id, company_id, status?, q?, limit, offset }`
- **Output:** `{ rows: MaskedAccount[], total }` — rows carry `acc_no_masked` from `acc_no_last4` (never decrypt).
- **Invoked by:** F-BNK-API-01, API-03, API-10
- **Calls:** ENG-BNK-01 (format masked string)
- **Side effects:** — (read-only)
- **Iron rule check:** ✅

### F-BNK-FN-05: `revealAccountNumber` ⭐
- **Purpose:** Return the full account number IF and ONLY IF the caller has `canRevealFull`, writing a mandatory audit entry (audit-first).
- **Input:** `{ id, actor, actor_can_reveal_full: boolean, reason? }`
- **Output:** `{ acc_no_full } | RevealForbiddenError`
- **Invoked by:** F-BNK-API-05
- **Calls:** ENG-BNK-01 (reveal-gate + decrypt), F-BNK-FN-12 (audit)
- **Logic:**
  1. if `!actor_can_reveal_full` → write audit `revealed` (denied flag, optional) → throw `ERR_REVEAL_FORBIDDEN` (UI toast "คุณไม่มีสิทธิ์ดูเลขบัญชีเต็ม"); number stays masked.
  2. rate check: reveals by actor today > threshold (config, default 50) → `ERR_REVEAL_RATE_LIMITED` (BRD §17.4).
  3. **write audit `revealed` FIRST** (append-only). If audit write fails → abort reveal (`ERR_AUDIT_WRITE_FAILED`, block — BRD §17.4).
  4. decrypt + return full number.
- **Error cases:** ERR_REVEAL_FORBIDDEN, ERR_REVEAL_RATE_LIMITED, ERR_AUDIT_WRITE_FAILED.
- **Iron rule check:** ✅ permission is a passed-in boolean resolved from RBAC — no hardcoded `true` (mock only in prototype; OQ-BNK-01/04).

### F-BNK-FN-06: `enforceDefaultUnique`
- **Purpose:** Ensure ≤1 default_pay and ≤1 default_receive per company; auto-clear the previous holder.
- **Input:** `{ tenant_id, company_id, account_id, field: 'pay'|'receive', value }`
- **Output:** `{ updated: account_id, cleared: account_id|null }`
- **Invoked by:** F-BNK-API-09, FN-01 (on create with flag), FN-07 (clear on deactivate/archive)
- **Calls:** F-BNK-FN-12
- **Logic:** account must be `active` (else BR_DEFAULT_REQUIRES_ACTIVE — toast "บัญชีต้องอยู่สถานะใช้งานก่อนตั้งเป็นค่าเริ่มต้น"); set flag true → clear same flag on all siblings in company (partial-unique index backs this); audit `set-default` (on) / clear (off). Concurrent writers → last-write-wins + audit both (EC-12).
- **Iron rule check:** ✅

### F-BNK-FN-07: `transitionAccountStatus`
- **Purpose:** Guarded state machine for account lifecycle.
- **Input:** `{ id, action: 'deactivate'|'activate'|'archive', actor }`
- **Output:** `CompanyBankAccount | InvalidTransitionError`
- **Invoked by:** F-BNK-API-06/07/08
- **Calls:** F-BNK-FN-06 (clear defaults on deactivate/archive), F-BNK-FN-12
- **Logic (allowed transitions — 05_RULES §5.2):** active→inactive (deactivate); inactive→active (activate); active|inactive→archived (archive, terminal). Any other → BR_INVALID_TRANSITION. On deactivate/archive: if account was a default → **clear** `defaultPay`/`defaultReceive` flags **and the confirm modal shows an explicit default-loss warning** (EC-14 / OQ-BNK-05 — RESOLVED 2026-08-06: warn + clear). **No hard delete** (Contract #7). Audit `deactivated`/`activated`/`archived`.
- **Iron rule check:** ✅

### F-BNK-FN-08: `createCustomBank`
- **Purpose:** Create a user-defined (custom, usually foreign) bank.
- **Input:** `{ name_th, abbr, code?, swift, type, actor }`
- **Output:** `Bank | ValidationError[]`
- **Invoked by:** F-BNK-API-11
- **Calls:** ENG-BNK-02 (SWIFT validate), F-BNK-FN-12
- **Logic:** validate name/abbr required; `code` optional but if present must be `^[0-9]{3}$` (BR_BOTCODE_FORMAT); SWIFT via ENG-BNK-02; SWIFT unique (BR_SWIFT_DUPLICATE — "รหัส SWIFT นี้มีอยู่แล้ว"); set `is_custom=true`, `used_count=0`; audit `bank-added`.
- **Iron rule check:** ✅

### F-BNK-FN-09: `updateCustomBank`
- **Purpose:** Edit a custom bank (preset blocked).
- **Input:** `{ id, patch, actor }`
- **Output:** `Bank | PresetReadonlyError | ValidationError[]`
- **Invoked by:** F-BNK-API-12
- **Calls:** ENG-BNK-02, F-BNK-FN-12
- **Logic:** if `is_custom=false` → ERR_PRESET_READONLY ("ธนาคารมาตรฐาน ธปท. แก้ไขไม่ได้", R-12); `code` immutable in edit; re-validate SWIFT + uniqueness; audit `bank-edited`.
- **Iron rule check:** ✅

### F-BNK-FN-10: `deleteCustomBank` ⭐ (W1 — exception to Contract #7)
- **Purpose:** Hard-delete a custom bank only when unused.
- **Input:** `{ id, actor }`
- **Output:** `{ deleted:true } | PresetReadonlyError | BankInUseError`
- **Invoked by:** F-BNK-API-13
- **Calls:** F-BNK-FN-12
- **Logic (guard order):** (1) `is_custom=false` → ERR_PRESET_READONLY (preset never deletable, R-12); (2) `used_count > 0` → BR_BANK_IN_USE (toast "ลบไม่ได้ — มี {N} บัญชีอ้างอิงธนาคารนี้อยู่ (ย้าย/ปิดบัญชีก่อน)"; button disabled tooltip "มี {N} บัญชีอ้างอิงธนาคารนี้ — ลบไม่ได้"); (3) else DELETE + audit `bank-removed` (audit stream survives). **This is the documented, audited exception to Global Contract #7 for unused custom lookup entries (BR-BNK-08).**
- **Iron rule check:** ✅

### F-BNK-FN-11: `buildPickableAccounts` (cross-module — R12)
- **Purpose:** Return active-only, masked accounts for consumer-document pickers to snapshot.
- **Input:** `{ tenant_id, company_id, purpose?: 'pay'|'receive' }`
- **Output:** `PickableAccount[]` (masked; inactive/archived excluded)
- **Invoked by:** F-BNK-API-16 (consumed by PV/RV/Recon/Payroll)
- **Calls:** ENG-BNK-01 (mask)
- **Logic:** filter `status='active'`; include default flags for pre-select; **never** returns full acc_no (masked); consumer must snapshot (Contract #6, BR-BNK-05).
- **Iron rule check:** ✅

### F-BNK-FN-12: `appendAudit`
- **Purpose:** Append-only audit writer (both streams). Central choke point for R-07.
- **Input:** `{ account_id?|bank_code?, action, detail, actor }`
- **Output:** `AuditEntry`
- **Invoked by:** FN-01,02,05,06,07,08,09,10 (and directly by lifecycle APIs)
- **Calls:** —
- **Logic:** exactly one of account_id/bank_code set; INSERT T_bank_audit_log (never UPDATE/DELETE); `detail` MUST carry last-4 only, never full acc_no; timestamp server-set.
- **Iron rule check:** ✅

---

## §3.2 Engines (Reusable / CUBIC-Registered)

### ENG-BNK-01: `sensitive-field-masker` [NEW] ⭐ (R10 security spine)

| Field | Value |
|---|---|
| **id** | (assigned at CUBIC registration) |
| **code** | `sensitive-field-masker` |
| **name** | Sensitive Field Masker & Reveal Gate |
| **category** | validation / security-transform |
| **status** | DRAFT (this FRD) |
| **owner** | F-BNK (candidate shared across Finance features touching sensitive fields) |

**Input Schema:**
```json
{ "value": "string", "mode": "mask|reveal", "keep_last": 4,
  "actor_can_reveal_full": true, "policy": "restricted" }
```
**Output Schema:**
```json
{ "display": "••••••5678", "revealed": false, "requires_audit": true }
```
**Logic Outline:**
1. `mask` mode → replace all but last `keep_last` chars with `•` (bullet), preserving count of hidden chars (e.g. 10-digit → `••••••5678`). Never touches ciphertext beyond producing display string.
2. `reveal` mode → if `actor_can_reveal_full` false → return `{ revealed:false, forbidden:true }` (caller throws ERR_REVEAL_FORBIDDEN); if true → `{ display: full, revealed:true, requires_audit:true }` (caller MUST persist audit before returning).
3. Pure transform + policy decision — I/O (decrypt, audit persistence) handled by caller (FN-05).
**Used by features:** F-BNK (current); planned reuse: Payment Voucher, Payroll, any feature masking account numbers / national IDs.
**Iron rule check:** ✅ pure (no direct I/O/HTTP) · ✅ reusable 2+ features · ✅ substantial (masking + reveal-policy algorithm)
**CUBIC Registration note:** DRAFT → register at dev hand-off (LD-02). Ties to Policy Center → Data Classification / Restricted Resources.

### ENG-BNK-02: `swift-bic-validator` [NEW]

| Field | Value |
|---|---|
| **code** | `swift-bic-validator` · **category** validation · **status** DRAFT · **owner** F-BNK (shared candidate) |

**Input Schema:** `{ "swift": "string" }`
**Output Schema:** `{ "valid": true, "reason": null }`
**Logic Outline:**
1. Normalize: uppercase, strip non-alnum.
2. Match `^[A-Z0-9]{8}$` OR `^[A-Z0-9]{11}$` (BR-BNK-04); else `{ valid:false, reason:'SWIFT ต้องมี 8 หรือ 11 หลัก' }`.
3. (No network/registry lookup — format only; ISO 9362 structure check is a future enhancement.)
**Used by features:** F-BNK (current); planned reuse: any feature entering bank SWIFT/BIC.
**Iron rule check:** ✅ pure · ✅ reusable · ✅ standard algorithm (ISO 9362 length rule)
**CUBIC Registration note:** DRAFT.

---

## §3.3 API ↔ Logic Trace Table (R8 Anchor)

| API ID | Method | Path | Calls Functions | Calls Engines |
|---|---|---|---|---|
| API-01 | GET | /bank-accounts | FN-04 | — |
| API-02 | POST | /bank-accounts | FN-01, FN-03, FN-06, FN-12 | — (ENG-BNK-01 via FN-01 for last-4) |
| API-03 | GET | /bank-accounts/:id | FN-04 | — |
| API-04 | PUT | /bank-accounts/:id | FN-02, FN-03, FN-12 | (ENG-BNK-01 via FN-02) |
| API-05 | POST | /bank-accounts/:id/reveal | FN-05, FN-12 | **ENG-BNK-01** |
| API-06 | POST | /bank-accounts/:id/deactivate | FN-07, FN-06, FN-12 | — |
| API-07 | POST | /bank-accounts/:id/activate | FN-07, FN-12 | — |
| API-08 | POST | /bank-accounts/:id/archive | FN-07, FN-06, FN-12 | — |
| API-09 | POST | /bank-accounts/:id/set-default | FN-06, FN-12 | — |
| API-10 | GET | /banks | FN-04 | — |
| API-11 | POST | /banks | FN-08, FN-12 | **ENG-BNK-02** |
| API-12 | PUT | /banks/:id | FN-09, FN-12 | **ENG-BNK-02** |
| API-13 | DELETE | /banks/:id | FN-10, FN-12 | — |
| API-14 | GET | /bank-accounts/:id/audit | — | — |
| API-15 | GET | /banks/:id/audit | — | — |
| API-16 | GET | /bank-accounts/pickable | FN-11 | **ENG-BNK-01** |

### Trace Verification (Self-Check)
- [x] Every mutation API (API-02,04,05,06,07,08,09,11,12,13) has ≥1 Function/Engine.
- [x] No orphan Function — FN-01..12 all traced (FN-12 via nearly every mutation).
- [x] No orphan Engine — ENG-BNK-01 (API-05 direct, FN-01/02/04/11 for masking), ENG-BNK-02 (API-11/12).
- [x] No hidden logic in 02_API — masking/reveal/validation/state all here.

---

## §3.4 Dependencies

### External called by this feature
- Chart of Accounts lookup (CoA) — GL combobox options (inbound, read).
- Company Master lookup — company scope.
- Central Audit Trail store (append-only) — backs T_bank_audit_log.
- RBAC/Permission engine — resolves `canRevealFull` + edit permission (OQ-BNK-01).

### External that calls into this feature
- Payment Voucher, Receipt Voucher, Bank Reconciliation, Payroll → call API-16 (buildPickableAccounts) and snapshot.
- ENG-BNK-01 / ENG-BNK-02 are reuse candidates for the above (post-registration).

---

## §3.5 Open Questions / Locked Decisions Referenced
- **LD-02** (07_LOCKED): ENG-BNK-01 / ENG-BNK-02 register with CUBIC at dev hand-off (not this sprint).
- **OQ-BNK-01/04**: `canRevealFull` resolution is RBAC-driven; FN-05 must NOT hardcode `true` (prototype mock only).
- **R-03 config**: `accNo_length_range` read from config in FN-03 (not hardcoded).

---

## Audience Cheat-Sheet
| Reader | Sections |
|---|---|
| BE dev | §3.1 + §3.2 + §3.3 |
| QA | §3.3 + §3.1 side-effects + §3.2 I/O (esp. FN-05 / ENG-BNK-01) |
| DBA | §3.1 side-effects |
| Architect / CUBIC owner | §3.2 + §3.4 + §3.5 |
