# 07_LOCKED_DECISIONS — F-BNK Bank Master

> **Audience:** All roles.
> **Purpose:** Immutable Scope Lock + resolved decisions — do not re-open.

---

## §7.0 Scope Lock (Imported from BRD §3.4) ⭐ IMMUTABLE

> Client-signed constraints — never override across pack or downstream chain (HTML/Test/Dev). If any spec conflicts with a LOCK, the LOCK wins.

| LOCK-ID | ข้อยืนยัน | อ้างเอกสาร | สถานะใน FRD |
|---|---|---|---|
| **LOCK-01** | Feature = Shared-Foundation **MASTER · NO tier / no Lite-Full linkage** — no invented tier behavior | PREBRIEF · Central Plan · task | ✅ สอดคล้อง — RBAC only, no tier, no 🔗/✋ (05_RULES §5.3) |
| **LOCK-02** | **2 levels only:** Bank list (preset ธปท. 22) + CompanyBankAccount (per company) | OB-1 · DECISION_LOG | ✅ — E1/E2 (04_DB), P-01/P-02 (01_UI) |
| **LOCK-03** | **Downstream (config/soft-ref picker) = Payment Voucher · Receipt Voucher · Bank Reconciliation · Payroll** (Payroll named — W2 closed) · **Inbound = Chart of Accounts (GL)** | OB-2 · Central Plan Finance box · task | ✅ — 02_API §2.X + API-16 + 06_TESTS XT-01..04 (Payroll = XT-04) |
| **LOCK-04** | **OUT this phase:** bank API / auto statement import (S-06) · multi-currency (THB only) | PREBRIEF S-06 · OQ-2 | ✅ — 00_OVERVIEW §0.3 OOS-1/2; currency THB-locked (BR-BNK-10); no statement/import endpoint |
| **LOCK-05** | D1: `BankMaster.html` = source of truth screen (gated) — no invented/missing screen | DECISION_LOG D1 | ✅ — 01_UI Mode A observed; Section M §1.9 |
| **LOCK-06** | D3: coverage baseline = PREBRIEF + Central Plan edges (no workflow_graph) · no scope beyond FN-01..06+90 / BR-01..05 / edges | DECISION_LOG D3 | ✅ — Coverage Manifest 00 §0.12; scope creep 0 |
| **LOCK-07** | W1: custom bank hard-delete allowed **only `used=0`** — explicit exception to Global Contract #7 | DECISION_LOG W1 RESOLVED | ✅ — BR-BNK-08 · FN-10 · API-13 · AC-12/AC-13 |

- **Scope Lock Ref:** PREBRIEF F-BNK + `00_CONTEXT/DECISION_LOG.md` (D1–D5, W1 RESOLVED 2026-08-05) — immutable.
- **Drift found while writing FRD (layer 3):** **none of scope.** Two *naming* drifts vs BRD (audit action `set-default` not `default-changed`; tab label "บัญชีบริษัท" not "บัญชีธนาคาร") — resolved by following HTML source of truth (R14). Documented in 01_UI §1.9 + 04_DB §4.2. Neither expands scope.
- **No spec in this pack conflicts with any LOCK.**

---

## §7.1 Locked Decisions (LD)

### LD-01: Reveal is a backend-gated, audit-first server action (not client unmask)
- **Date:** 2026-08-06
- **Context:** `acc_no` is Restricted (R10); the prototype unmasks client-side with a mock `canRevealFull=true`.
- **Decision:** Production reveal = dedicated endpoint **API-05** — permission checked at the endpoint (OQ-BNK-04), audit `revealed` written **before** returning the number (audit-first; if audit fails, reveal fails).
- **Rationale:** Hiding the button is not a control; the number must never leave the server without a permission check + non-repudiable audit.
- **Implications:** 02_API-05, 03_LOGIC FN-05 + ENG-BNK-01, 05_RULES BR-BNK-09, 06_TESTS TC-07/08/09/16 (P0).
- **Reversibility:** LOW — security invariant.

### LD-02: ENG-BNK-01 / ENG-BNK-02 built scope-local now, register with CUBIC at hand-off
- **Decision:** `sensitive-field-masker` + `swift-bic-validator` are DRAFT engines this sprint; register in CUBIC Registry at dev hand-off once a second consumer (Payment Voucher / Payroll) confirms reuse.
- **Rationale:** Avoid premature abstraction; masker especially is a strong shared candidate.
- **Implications:** 03_LOGIC §3.2 status DRAFT; global engine IDs assigned at registration.
- **Reversibility:** EASY.

### LD-03: `canRevealFull` tier + `accNo_length_range` are configuration, not hardcode
- **Decision:** `canRevealFull` resolved from RBAC (mock `true` only in prototype — OQ-BNK-01); account-number length range read from config `accNo_length_range` (default 10–15 — BR-BNK-03/S-04). Dev must NOT hardcode `true` or `{10,15}`.
- **Reversibility:** EASY (config).

### LD-04: `set-default` + `bank-edited` audit action names follow HTML (not BRD wording)
- **Decision:** audit enum uses the HTML strings (`set-default`, `bank-edited`) rather than the BRD's `default-changed`. Source-of-truth wins (R14).
- **Reversibility:** EASY (naming).

### LD-05: Currency lock is a value-lock, not a schema omission
- **Decision:** `currency` column stays in schema (default `THB`, CHECK=THB this phase). Multi-currency opens later via feature toggle (OQ-BNK-02), removing the CHECK — **not** a schema migration of the column.
- **Reversibility:** EASY.

### LD-06: Default account deactivated/archived → WARN + CLEAR the default flag (resolves EC-14 / OQ-BNK-05)
- **Date:** 2026-08-06
- **Context:** EC-14 / OQ-BNK-05 — a company account currently set as default-pay and/or default-receive is deactivated or archived. The earlier FRD `[AI-DEFAULT]` said "warn + keep flag"; the HTML always cleared the flag. This FRD↔HTML divergence is now **RESOLVED — they agree**.
- **Decision:** **WARN + CLEAR.** `confirmDeactivate`/`confirmArchive` clear `defaultPay`/`defaultReceive`, AND the confirm modal shows an explicit default-loss warning when the target account holds a default flag: `บัญชีนี้เป็นบัญชีจ่าย/รับเริ่มต้น — ค่าเริ่มต้นนี้จะถูกยกเลิก บริษัทจะไม่มีค่าเริ่มต้นดังกล่าว กรุณาตั้งบัญชีอื่นแทนภายหลัง`.
- **Rationale:** clearing prevents a dangling default pointing at an account that is now hidden from new-document pickers; the warning tells the admin to reassign a replacement default.
- **Implications:** 03_LOGIC FN-06/FN-07, 05_RULES §5.2 + EC-14, 06_TESTS AC-05c / TC-05c, 01_UI M-01/M-02, 02_API API-06/API-08.
- **Reversibility:** LOW — confirmed rule (no longer `[AI-DEFAULT]`).

---

## §7.2 Convention Deviations

### CD-01: Custom lifecycle-action endpoints (POST …/reveal, /deactivate, /activate, /archive, /set-default)
- **Convention default:** PATCH for state change.
- **Deviation:** POST custom actions.
- **Reason:** Each is a distinct audited action with side effects (esp. reveal), not a property patch — matches HTML function boundaries.
- **Approved by:** (pending Tech Lead review). Applies to API-05/06/07/08/09.

### CD-02: DELETE endpoint exists for banks but NOT for accounts
- **Reason:** accounts are no-hard-delete (Contract #7 → soft archive); custom banks have the W1 exception (used=0). Intentional asymmetry.

---

## §7.3 Open Questions Promoted from 00_OVERVIEW
**OQ-BNK-05 → RESOLVED 2026-08-06 as LD-06** (default account deactivated/archived = warn + clear the default flag). Remaining OQ-BNK-01/02/03/04/06 stay open (policy/roadmap). Dev must not implement `canRevealFull` tier binding (OQ-BNK-01) or multi-currency toggle (OQ-BNK-02) until resolved.

---

## §7.4 Architecture Tradeoffs Acknowledged
- **AT-01:** Encrypt `acc_no` at rest + denormalized `acc_no_last4` for masked reads — extra write cost vs. never decrypting for lists. Accepted (security > micro-perf).
- **AT-02:** Audit-first reveal (audit before response) adds latency to reveal but guarantees non-repudiation. Accepted (SLA reveal <1s still met).

## §7.5 Decisions Deferred to Implementation
| Item | Owner | Deadline |
|---|---|---|
| `canRevealFull` tier definition (OQ-BNK-01) | Policy/Strike | before Phase 3 |
| Restricted Resources registration of `acc_no` (OQ-BNK-06) | Tech Lead | dev hand-off |
| Encryption library / KMS for `acc_no` | DevOps | pre-deploy |
| Legacy account migration + gl backfill (OQ-BNK-06) | PM/BA | pre-launch |

## §7.6 References
- Convention: `knowledge/conventions.md` · Central Plan §2 Global Contracts #6/#7 · BRD §3.4/§16 · DECISION_LOG (W1)
