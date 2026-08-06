# 05_RULES — F-BNK Bank Master

> **Audience:** Backend developer + QA
> **Purpose:** Business Rules + Validation + State Machine + Edge Cases + Errors + Security (D-CLASS)
> **Principle:** Declarative — readable without code. Source: BRD §8/§9/§10 + HTML source of truth.
> Change-Likelihood tags: **FIXED** (invariant/contract) · **CONFIGURABLE 🤖** (may change — [AI-DEFAULT]).

---

## §5.1 Business Rules (BR)

### BR-BNK-01: Account number unique per company — **FIXED**
- **Statement:** `(tenant_id, company_id, acc_no)` unique.
- **Enforced by:** F-BNK-FN-03 (app) + DB UNIQUE constraint (04_DB).
- **Error / UI:** `BR_ACCNO_DUPLICATE` (422) → "เลขบัญชีนี้มีอยู่แล้วในบริษัทนี้".

### BR-BNK-02: Default pay / receive = 1 each per company — **FIXED**
- **Statement:** ≤1 `default_pay` and ≤1 `default_receive` true per company; setting one clears the previous.
- **Enforced by:** F-BNK-FN-06 + partial-unique indexes (04_DB). Account must be `active`.
- **Error / UI:** setting on non-active → toast "บัญชีต้องอยู่สถานะใช้งานก่อนตั้งเป็นค่าเริ่มต้น".

### BR-BNK-03: Account number = numeric 10–15 digits — **CONFIGURABLE 🤖** `[AI-DEFAULT]`
- **Statement:** `^[0-9]{10,15}$`; input strips non-digits. **Range read from config `accNo_length_range` (default 10–15) — NOT hardcoded** (S-04).
- **Enforced by:** F-BNK-FN-03 + DB CHECK (backstop).
- **Error / UI:** `BR_ACCNO_FORMAT` (422) → "เลขบัญชีต้องเป็นตัวเลข 10-15 หลัก". Empty → "กรุณากรอกเลขที่บัญชี".
- **Owner/freq:** Admin (rare) · Admin Panel (Phase 2). No per-bank format table (OOS-6).

### BR-BNK-04: SWIFT = 8 or 11 alnum — **FIXED**
- **Statement:** `^[A-Z0-9]{8}$|^[A-Z0-9]{11}$` (international standard). Input uppercases + strips non-alnum.
- **Enforced by:** ENG-BNK-02 (F-BNK-FN-08/09).
- **Error / UI:** `BR_SWIFT_FORMAT` (422) → "SWIFT ต้องมี 8 หรือ 11 หลัก". Empty → "กรุณากรอกรหัส SWIFT". Duplicate → "รหัส SWIFT นี้มีอยู่แล้ว".

### BR-BNK-05: Inactive/archived → hidden from new-doc picker; existing docs unchanged — **FIXED** (Contract #6)
- **Statement:** picker (API-16) returns `status='active'` only. Consumer documents snapshot values; master changes never rewrite issued docs.
- **Enforced by:** F-BNK-FN-11.

### BR-BNK-06: Used-in-doc account → no hard delete → soft archive + audit — **FIXED** (Contract #7)
- **Statement:** accounts are never hard-deleted; `used_in_doc=true` → archive only. No DELETE endpoint on accounts.
- **Enforced by:** F-BNK-FN-07 (no delete path); UI archive modal.
- **UI:** "บัญชีนี้ถูกใช้ในเอกสารและรายการกระทบยอดธนาคารแล้ว จึงลบถาวรไม่ได้ — ระบบจะเก็บถาวร (soft archive) เท่านั้น…".

### BR-BNK-07: Every action → append-only audit — **FIXED** (Contract #7)
- **Statement:** create/edit/reveal/set-default/deactivate/activate/archive/bank-added/bank-edited/bank-removed each write an append-only entry (2 streams). No UPDATE/DELETE on audit.
- **Enforced by:** F-BNK-FN-12; T_bank_audit_log REVOKE UPDATE/DELETE.

### BR-BNK-08 ⭐: Custom bank hard-delete only when `used=0`; preset never — **FIXED (explicit exception to Contract #7)**
- **Statement:** A **custom** bank (`is_custom=true`) MAY be hard-deleted **only when `used_count=0`** (no account references its `bank_code`). If `used_count>0` → blocked (button disabled + warning). **Preset ธปท. banks are never deletable/editable** (R-12). Deletion is audited (`bank-removed`).
- **Rationale (W1 RESOLVED, DECISION_LOG 2026-08-05):** An unused custom lookup entry has no soft-ref to break; deleting it cannot corrupt any document. This is the ONLY sanctioned exception to the global no-hard-delete rule, and it is scoped, guarded, and audited.
- **Enforced by:** F-BNK-FN-10 (guard order: preset→403; used>0→422; else delete).
- **Error / UI:** `BR_BANK_IN_USE` (422) → toast "ลบไม่ได้ — มี {N} บัญชีอ้างอิงธนาคารนี้อยู่ (ย้าย/ปิดบัญชีก่อน)"; disabled button tooltip "มี {N} บัญชีอ้างอิงธนาคารนี้ — ลบไม่ได้". Preset edit/delete → `ERR_PRESET_READONLY` / toast "ธนาคารมาตรฐาน ธปท. แก้ไขไม่ได้".

### BR-BNK-09 ⭐: Mask to last-4 default; full reveal requires `canRevealFull` + audit — **CONFIGURABLE 🤖** (tier) / mechanism **FIXED**
- **Statement:** Account number masked to last-4 everywhere (lists, detail, picker, export). Full reveal ONLY via API-05 with permission `canRevealFull`, and **every reveal writes an append-only `revealed` audit (audit-first — if audit fails, reveal fails)**. Denied attempt keeps the number masked. **Backend-enforced (not button-hide) — OQ-BNK-04.**
- **Enforced by:** F-BNK-FN-05 + ENG-BNK-01.
- **Owner/freq:** Policy/Security owns which tier gets `canRevealFull` (OQ-BNK-01 — mechanism fixed, tier TBD; do NOT hardcode `true`).
- **Error / UI:** `ERR_REVEAL_FORBIDDEN` (403) → toast "คุณไม่มีสิทธิ์ดูเลขบัญชีเต็ม". Success → "บันทึกการเข้าถึงเลขบัญชีเต็มแล้ว". `ERR_REVEAL_RATE_LIMITED` (429) when >50/user/day (BRD §17.4).

### BR-BNK-10: Currency = THB only (readonly) — **CONFIGURABLE 🤖** (roadmap toggle) `[AI-DEFAULT]`
- **Statement:** `currency='THB'` forced + readonly this phase. `currency` column exists → multi-currency opens later via **feature toggle, not schema change** (OQ-BNK-02).
- **UI:** info-tip "เฟสนี้รองรับ THB เท่านั้น — สกุลเงินอื่นจะเปิดใช้พร้อม multi-currency (OQ-2)".

### BR-BNK-11: GL account required before use/posting — **FIXED**
- **Statement:** `gl_code` required on create/edit (soft-ref to CoA).
- **Enforced by:** F-BNK-FN-03.
- **Error / UI:** `BR_GL_REQUIRED` (422) → "กรุณาเลือกบัญชี GL".

### BR-BNK-12: Preset ธปท. banks read-only — **FIXED**
- **Statement:** the 22 preset banks cannot be edited or deleted; only custom banks are mutable.
- **Enforced by:** F-BNK-FN-09/FN-10 (`is_custom` guard).
- **UI:** manage cell "มาตรฐาน"; edit blocked toast "ธนาคารมาตรฐาน ธปท. แก้ไขไม่ได้".

### §5.1.9 Flexibility Summary
| Rule | Level | Owner | Note |
|---|---|---|---|
| BR-BNK-01,02,04,05,06,07,08,11,12 | **FIXED** | — | invariant / Global Contract / W1 stakeholder decision |
| BR-BNK-03 (accNo range) | **CONFIGURABLE — Admin Panel** 🤖 | Admin | `[AI-DEFAULT]` S-04 |
| BR-BNK-09 (canRevealFull tier) | **CONFIGURABLE — Permission/Policy** 🤖 | Policy | mechanism fixed; tier → OQ-BNK-01 |
| BR-BNK-10 (multi-currency toggle) | **CONFIGURABLE — roadmap toggle** 🤖 | Strike | OQ-BNK-02; not schema change |

---

## §5.2 State Machine (CompanyBankAccount)

```
             create
               │
               ▼
   ┌────────┐  deactivate  ┌──────────┐
   │ active │─────────────▶│ inactive │
   │        │◀─────────────│          │
   └───┬────┘   activate   └────┬─────┘
       │ archive                │ archive
       ▼                        ▼
   ┌──────────────────────────────────┐
   │        archived (TERMINAL)        │  ← no reactivate path
   └──────────────────────────────────┘
```

| From | To | Action (API) | Allowed role | Conditions / side effects |
|---|---|---|---|---|
| (none) | active | create (API-02) | finance_admin | validation pass (BR-01/03/04/11); currency=THB |
| active | inactive | deactivate (API-06) | finance_admin | clear default flags + confirm modal shows default-loss warning if was default (EC-14 — RESOLVED: warn+clear); gone from new-doc picker |
| inactive | active | activate (API-07) | finance_admin | reversible |
| active/inactive | archived | archive (API-08) | finance_admin | **terminal**; used-in-doc allowed (soft archive); clear defaults; audit |
| archived | — | — | — | **no transition out** (EC-09) |

- **Bank (E1):** preset = static (read-only); custom = create → editable → deletable only if `used=0`. No status machine.

---

## §5.3 Permission Matrix

| Role | View list/detail | Reveal full accNo | Create/Edit account | Deactivate/Activate/Archive | Set default | Manage custom bank |
|---|:--:|:--:|:--:|:--:|:--:|:--:|
| **finance_admin** | ✅ (masked) | ✅ if `canRevealFull` (OQ-1) | ✅ | ✅ | ✅ | ✅ (create/edit/delete used=0) |
| **finance_user** | ✅ (masked only) | ❌ | ❌ | ❌ | ❌ | ❌ |
| **accounting** | ✅ (ref) | per permission | ❌ | ❌ | ❌ | ❌ |
| **system** | — | enforce+audit | validate | audit transitions | enforce unique | audit bank changes |

> No tier / package entitlement — plain RBAC (Shared-Foundation master, LOCK-01). `canRevealFull` is a permission, not a tier.

---

## §5.4 Field Validation Rules

| Field | Rule | Error code | UI message (verbatim) |
|---|---|---|---|
| bank_code | required | BR_BANK_REQUIRED | กรุณาเลือกธนาคาร |
| acc_no | required | — | กรุณากรอกเลขที่บัญชี |
| acc_no | `^[0-9]{10,15}$` (config range) | BR_ACCNO_FORMAT | เลขบัญชีต้องเป็นตัวเลข 10-15 หลัก |
| acc_no | unique per company | BR_ACCNO_DUPLICATE | เลขบัญชีนี้มีอยู่แล้วในบริษัทนี้ |
| acc_name | required | — | กรุณากรอกชื่อบัญชี |
| gl_code | required | BR_GL_REQUIRED | กรุณาเลือกบัญชี GL |
| currency | server-forced THB | — | (readonly; info-tip) |
| swift | `^[A-Z0-9]{8}$|^[A-Z0-9]{11}$` | BR_SWIFT_FORMAT | SWIFT ต้องมี 8 หรือ 11 หลัก |
| swift | required (bank form) | — | กรุณากรอกรหัส SWIFT |
| swift | unique | BR_SWIFT_DUPLICATE | รหัส SWIFT นี้มีอยู่แล้ว |
| name_th | required (bank form) | — | กรุณากรอกชื่อธนาคาร |
| abbr | required (bank form) | — | กรุณากรอกชื่อย่อ |
| code (BOT) | `^[0-9]{3}$` if present | BR_BOTCODE_FORMAT | รหัส ธปท. ต้องเป็นตัวเลข 3 หลัก |

**Cross-field / server:** default flag change → clear siblings (BR-BNK-02); reveal → permission + audit (BR-BNK-09); currency immutable after create.

---

## §5.5 Edge Cases

> ☑ = BRD-confirmed. ☐→ = BRD AI-pattern edge resolved in Lane Mode with conservative default `[AI-DEFAULT]` (see 00_OVERVIEW §0.13) + Open Question.

| ID | Scenario | Resolution | Rule/OQ | Test |
|---|---|---|---|---|
| EC-01 ☑ | accNo dup in same company | block on submit | BR-BNK-01 | AC-02b |
| EC-02 ☑ | accNo not 10–15 / has letters | strip non-digits + block | BR-BNK-03 | AC-02 |
| EC-03 ☑ | set 2nd default pay | auto-move (clear previous) | BR-BNK-02 | AC-04 |
| EC-04 ☑ | account inactive | absent from new-doc picker; existing docs show | BR-BNK-05 | AC-05b |
| EC-05 ☑ | reveal w/o permission | denied, masked stays, toast | BR-BNK-09 | AC-08 |
| EC-06 ☑ | delete used account | impossible (no delete path) → archive | BR-BNK-06 | AC-06 |
| EC-07 ☑ | SWIFT not 8/11 | block | BR-BNK-04 | AC-11 |
| EC-08 ☑ | delete custom bank used>0 | blocked, button disabled | BR-BNK-08 | AC-12 |
| EC-09 ☑ | archived → reactivate | no path (terminal) | §5.2 | AC-06b |
| EC-10 ☐→ | bank archived/deleted after account created | account keeps snapshot (soft-ref, no cascade); custom bank with used>0 can't be deleted anyway | `[AI-DEFAULT]` (Contract #6) | XT note |
| EC-11 ☐→ | GL disabled in CoA after binding | account keeps `gl_code`; warn at posting time (downstream) | `[AI-DEFAULT]` → OQ (posting owned by consumer) | — |
| EC-12 ☐→ | 2 users set different default pay concurrently | last-write-wins + audit both; partial-unique index keeps ≤1 | `[AI-DEFAULT]` (PR-1/PR-9) | AC-04b |
| EC-13 ☐→ | direct URL/drawer w/o edit permission | **backend re-check at mutation** → 403 ERR_PERMISSION_REVOKED (not button-hide) | **OQ-BNK-04** | AC-16 |
| EC-14 ☑ | default account deactivated/archived (was a default) | **warn + clear flag** — clear `defaultPay`/`defaultReceive` + confirm modal shows default-loss warning note | **RESOLVED 2026-08-06** (ex-OQ-BNK-05; see 07_LOCKED_DECISIONS LD-06) | AC-05c |
| EC-15 ☐→ | export/print account list | **mask always** unless permitted + audit | `[AI-DEFAULT]` → OQ-BNK-03 | AC-09 |
| EC-16 (probe) | double-click create (network retry) | Idempotency-Key → single record | `[AI-DEFAULT]` (PR-4/PR-7) | AC-17 |
| EC-17 (probe) | stale edit (2 users) | If-Match version → 409 ERR_STALE_DATA | `[AI-DEFAULT]` (PR-2) | AC-18 |

---

## §5.6 Error Catalog

| Code | HTTP | Message (i18n key) | Cause |
|---|---|---|---|
| ERR_NOT_AUTHENTICATED | 401 | error.auth.unauth | No/invalid token |
| ERR_INSUFFICIENT_ROLE | 403 | error.auth.role | Role mismatch |
| ERR_PERMISSION_REVOKED | 403 | error.auth.revoked | Role changed mid-flight (EC-13) |
| ERR_REVEAL_FORBIDDEN | 403 | error.reveal.forbidden | No `canRevealFull` (EC-05) — UI "คุณไม่มีสิทธิ์ดูเลขบัญชีเต็ม" |
| ERR_REVEAL_RATE_LIMITED | 429 | error.reveal.ratelimit | >50 reveals/user/day (BRD §17.4) |
| ERR_AUDIT_WRITE_FAILED | 500 | error.audit.write | Reveal blocked because audit write failed (audit-first) |
| ERR_PRESET_READONLY | 403 | error.bank.preset | Edit/delete preset bank (BR-BNK-12) |
| ERR_NOT_FOUND | 404 | error.notfound | Resource missing |
| ERR_DUPLICATE_IDEMPOTENCY_KEY | 409 | error.idempotency.dup | Same key, diff body |
| ERR_STALE_DATA | 409 | error.concurrency.stale | If-Match version mismatch (EC-17) |
| ERR_VALIDATION_FAILED | 400 | error.validation.failed | Generic — UI "กรุณากรอกข้อมูลให้ครบถ้วน" |
| BR_ACCNO_DUPLICATE | 422 | br.accno.duplicate | BR-BNK-01 |
| BR_ACCNO_FORMAT | 422 | br.accno.format | BR-BNK-03 |
| BR_GL_REQUIRED | 422 | br.gl.required | BR-BNK-11 |
| BR_SWIFT_FORMAT | 422 | br.swift.format | BR-BNK-04 |
| BR_SWIFT_DUPLICATE | 422 | br.swift.duplicate | BR-BNK-04 |
| BR_BOTCODE_FORMAT | 422 | br.botcode.format | code 3-digit |
| BR_BANK_IN_USE | 422 | br.bank.inuse | BR-BNK-08 (used>0) |
| BR_INVALID_TRANSITION | 422 | br.state.invalid | illegal status change (e.g. reactivate archived) |
| BR_DEFAULT_REQUIRES_ACTIVE | 422 | br.default.active | set default on non-active — UI "บัญชีต้องอยู่สถานะใช้งานก่อนตั้งเป็นค่าเริ่มต้น" |

---

## §5.7 Security Bible Application

> Domains triggered: **D2, D5, D7, D9, D15, D17 + field-level sensitive protection**.

### D2 — Authentication & Session
- All endpoints require JWT. Reveal + mutations re-check role at request time (not GET).

### D5 — Financial data
- `acc_no`, `gl_code` are financial identity. All mutations + all reveals audited (before+after where applicable). No money movement here (that is PV/RV — SoD).

### D7 — PII
- `acc_name` = PII (PDPA scope) → encrypt at rest (recommended), never in logs beyond necessity.

### D9 — Audit logging
- Append-only T_bank_audit_log (2 streams), 7-year retention, immutable. Reveal audit mandatory (audit-first).

### D15 — Admin actions
- Status transitions, default changes, custom-bank create/edit/delete all logged with actor + timestamp.

### D17 — Multi-tenant isolation
- PostgreSQL RLS on all tables; presets globally visible (tenant_id NULL), customs isolated.

### D-CLASS: Data Classification ⭐ (R10)
Per-field classification in 04_DB §4.2 + §4.6. Enforcement summary:

| Layer | Confidential (`acc_name`, `branch`, `gl_code`, `acc_no_last4`) | **Restricted (`acc_no` full)** |
|---|---|---|
| API response | mask/`—` if no permission | **excluded — only API-05 returns full, ACL-gated** |
| UI display | `***` / `—` if no permission | **masked last-4; reveal hidden until `canRevealFull`** |
| Export/Print | excluded column if role fails | **mask always (OQ-BNK-03) + Restricted Resources approval** |
| Audit | view + mutation | **every reveal logged (`revealed`) + mutation + export attempts** |

**Wire points (Policy Center):**
- `acc_no` → **Restricted Resources registry** + Data Classification module. ⚠️ **Registration OPEN — OQ-BNK-06.**
- `acc_name` → PDPA consent scope.
- Classification override (downgrade) → requires DOA + audit.

**Negative / permission test set (MANDATORY — the security spine):** reveal-without-permission must keep the number masked and be denied; masked value must be the only thing any list/detail/picker/export exposes to a user lacking `canRevealFull`. See 06_TESTS §6.2 Permission set (AC-08, AC-09, AC-16) — these are P0.

---

## §5.8 Compliance & Audit Requirements
| Requirement | Implementation |
|---|---|
| Sensitive financial data protection | mask + reveal-gate + reveal-audit (BR-BNK-09) + encrypt at rest (C-ENC-01) |
| Non-repudiation of reveal | audit `revealed` with actor + timestamp (append-only) |
| Data integrity of issued documents | soft-reference snapshot, no cascade (Contract #6, BR-BNK-05) |
| No silent data loss | no hard delete on accounts; custom-bank delete only used=0 + audited (BR-BNK-08) |
| PDPA | `acc_name` retention + consent scope |
