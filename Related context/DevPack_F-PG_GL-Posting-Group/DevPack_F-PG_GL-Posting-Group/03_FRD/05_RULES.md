# 05_RULES — F-PG GL Posting Group

> **Audience:** Backend developer + QA
> **🚨 Critical:** IR-PG-01 and R05 are **two separate rules**, checked independently, never merged into one guard. See BR-03 and BR-05 below — do not conflate.

---

## §5.1 Business Rules (BR)

### BR-01: Account type & postability match (R01/R02)
- **Statement:** Every account field (in either entity) must be a COA account that is **leaf**, **postable**, **active**, and whose **type** matches the field's required control-account type:
  - vendor.account_1 (AP) = `liability` · vendor.account_2 (input VAT) = `asset`
  - inventory.account_1 = `asset` · inventory.account_2 (Interim GR/IR) = `asset` ∨ `liability`
  - bank.account_1 = `asset`
  - customer.account_1 (AR) = `asset` · customer.account_2 (output VAT) = `liability`
  - setup.sales_account = `income` · setup.purchase_account = `expense` ∨ `asset` · setup.cogs_account = `expense`
- **Enforced by:** F-PG-FN-03/F-PG-FN-09 (`03_LOGIC.md`) via `ENG-PG-01 coa-account-resolver`
- **Error:** `BR_ACCOUNT_TYPE_MISMATCH` / `BR_ACCOUNT_NOT_LEAF_OR_INACTIVE` → HTTP 422
- **Tag:** FIXED — accounting standard, no policy override. Validated on both the form path and the CSV import path.
- **Note (dual-type fields):** interim/purchase allowing 2 account types is an as-built HTML nuance not literally spelled out in BRD's plain-English R02 summary — see `02_API.md` §2.5 for the full reconciliation. Not a contradiction, not blocking.

### BR-02: Uniqueness (R03/R04)
- **Statement:** `code` (tab 1) must be unique. `(bus_group, prod_group)` combination (tab 2) must be unique.
- **Enforced by:** F-PG-FN-03/F-PG-FN-09 + DB unique index (`04_DB.md` §4.2)
- **Error:** `BR_CODE_DUPLICATE` / `BR_COMBINATION_DUPLICATE` → HTTP 422
- **Tag:** FIXED — core business key constraint.

### BR-03: `kind` locked always (R05)
- **Statement:** `kind` is **read-only in edit mode unconditionally** — this lock does **not** depend on `used`. There is no path, ever, to change `kind` after create.
- **Enforced by:** F-PG-FN-02 (`03_LOGIC.md` guard — checked *before and separately from* the IR-PG-01 check in BR-05)
- **Error:** `BR_KIND_LOCKED` → HTTP 422
- **Tag:** FIXED — decided, no exceptions (BRD LOCK-02).
- **⚠️ Do not merge with BR-05.** These are two independently-triggered guards on two different fields, with two different trigger conditions (`kind`: always vs `code`/`combination`: only when `used>0`). A single combined "if used>0 then lock kind+code" implementation would be **wrong** — `kind` must lock even at `used=0`.

### BR-03b: Clear accounts on kind change pre-submit (R07)
- **Statement:** When `kind` is changed **during create** (before first submit), all previously-entered account field values are cleared.
- **Enforced by:** Client-side (`onKindChange` in HTML); server only needs to validate that submitted accounts match the submitted `kind`'s expected type (already covered by BR-01) — there is no separate server-side "clear" action since the client never submits stale values for the old kind.
- **Tag:** FIXED, UI-behavior rule.

### BR-04: No delete when used>0 (R06)
- **Statement:** Records with `used>0` cannot be deleted, individually or in bulk. Bulk-delete silently skips them and reports the skipped count. There is no single-row delete button anywhere in this feature (FN-40/BRD out-of-scope).
- **Enforced by:** F-PG-FN-06/F-PG-FN-12
- **Error:** N/A (never a hard failure — skip + report, per `02_API.md` F-PG-API-06/15 response shape)
- **Tag:** FIXED — guard against destructive data loss on referenced mappings.

### BR-05: IR-PG-01 — partial lock on `code`/`combination` only, when `used>0`
- **Statement:** When `used>0`: **tab 1** — only `code` is locked; **tab 2** — only the `(bus_group, prod_group)` pair is locked (as a unit — you cannot change one half without the other, but this pair-lock is still a *separate mechanism from* BR-03's `kind` lock). In **both** tabs, `name`/`account(s)`/`status` remain editable regardless of `used`. Intent: the destination account can still be redirected going forward without breaking historical soft-references.
- **Enforced by:** F-PG-FN-02 (tab1 guard) / F-PG-FN-08 (tab2 guard) — see exact pseudo-logic in `03_LOGIC.md`
- **Error:** `BR_CODE_LOCKED_USED` (tab1) / `BR_COMBINATION_LOCKED_USED` (tab2) → HTTP 422
- **Tag:** FIXED — **confirmed via มติ 2026-08-09, not AI-inferred.** BRD explicitly flags that the *only* part of this area still AI-DRAFT is the `used` counter's real-sync mechanism (OQ-PG-03), not this partial-lock rule itself, which is settled.
- **⚠️ Do not merge with BR-03.** IR-PG-01's trigger is `used>0`; R05/BR-03's trigger is unconditional. They happen to both live on "edit mode" but are independent guards on independent fields with independent conditions.

### BR-06: Free 3-state transitions, no approval
- **Statement:** `status` ∈ {`draft`,`active`,`inactive`} may transition in any direction, any time, via menu or bulk bar, with no approval step. Only `active`-status records are visible to entity pickers / GL resolve.
- **Enforced by:** F-PG-FN-05/F-PG-FN-11
- **Tag:** FIXED — lane decision (OB-6), no state-machine restriction table needed since all 3×3 transitions are allowed.

### BR-07: Import = merge-only, blank status = draft
- **Statement:** CSV import only ever **adds** new rows; it never updates or overwrites existing registry rows (LOCK-03 — no Replace mode exists or should exist). A blank `status` cell in the import file defaults the new row to `draft`.
- **Enforced by:** F-PG-FN-14 `commitImportRows`
- **Tag:** FIXED — มติ 2026-08-09, "ห้ามมีเด็ดขาด" on any replace/merge-overwrite mode.

### BR-08: This feature does not post to GL
- **Statement:** `GL_Posting_Group` and `GL_Posting_Setup` are a mapping/translation layer only. The GL/Journal Engine (a separate, out-of-scope module) resolves `code`/`combination` into actual journal lines at document-posting time.
- **Enforced by:** Architectural boundary — no posting logic exists anywhere in this FRD's Functions/Engines (`03_LOGIC.md` §3.1/§3.2 contains zero GL-posting logic by design)
- **Tag:** FIXED — architectural decision (BRD LOCK-05).

### R09: Business/Product group value set — DYNAMIC (not FIXED)
- **Statement:** The current `bus_group` (`DOMESTIC`/`FOREIGN`) and `prod_group` (`GOODS`/`SERVICE`) value sets are as-built placeholders. An Admin Panel to manage these values, and a sync with Item Master's 6-value product-group set, is planned but **not built in this FRD** (Phase 2, per BRD §13).
- **Tag:** **DYNAMIC** — Admin Panel category (lookup value management, not a Rule Engine — no complex condition logic, just a value list). Do not build the Admin Panel in this pass; do design the DB schema as a lookup table, not a hardcoded enum (see `04_DB.md` §4.4).
- **Escalation:** OQ-PG-04 (see `00_OVERVIEW.md` §0.8) — target milestone has passed without a visible decision; escalated.

### Tax mapping gap — WARNING (not a rule yet)
- **Statement:** There is currently no mapping from tax code → GL account at a granularity finer than the vendor/customer group level (all tax codes on a given vendor/customer post to the same VAT account today). Whether to add a field on the Tax master, a new "VAT Posting Setup" tab 3, or leave as-is, is undecided.
- **Tag:** WARNING — scope gap, not yet a rule to implement.
- **Escalation:** OQ-PG-01 (see `00_OVERVIEW.md` §0.8) — target milestone has passed without a visible decision; escalated. **This FRD builds nothing toward tab 3** — it remains fully out of scope pending that decision.

---

## §5.2 State Machine

```
        ┌───────┐  ตั้งใช้งาน   ┌────────┐
        │ ร่าง   │─────────────►│ ใช้งาน │
        │(draft)│◄─────────────│(active)│
        └───┬───┘  กลับร่าง     └───┬────┘
            │                      │
   ตั้งไม่ใช้งาน│                      │ตั้งไม่ใช้งาน
            ▼                      ▼
        ┌──────────────┐
        │  ไม่ใช้งาน    │◄── (จาก active ก็เข้าตรงนี้ได้)
        │ (inactive)   │
        └──────┬───────┘
               │ กลับร่าง / ตั้งใช้งาน (ทั้ง 2 ทาง กลับไปได้ทุก state)
               ▼
        (ร่าง หรือ ใช้งาน)
```

| From | To | Action | Allowed roles | Conditions |
|---|---|---|---|---|
| any of 3 | any of the other 2 | change status (menu/bulk) | Finance Lead | **none** — no approval, no restriction, all 6 directed edges allowed (BR-06) |
| (none) | draft/active/inactive | create (form) | Finance Lead | no forced default at form (BRD §6.2 note) |
| (none) | per file / draft | import | Finance Lead | blank → draft (BR-07) |
| any (used=0) | (deleted) | bulk-delete | Finance Lead | skipped automatically if used>0 (BR-04) |

> No approval step exists at any transition (BR-06) — this table intentionally has no "Approver" column because BRD §5 confirms N/A throughout (OB-5).

---

## §5.3 Permission Matrix

| Role | View | Create | Edit (name/acct/status) | Edit (code/combination, used=0) | Edit (code/combination, used>0) | Change kind | Bulk delete | Import | Export |
|---|---|---|---|---|---|---|---|---|---|
| Finance Lead | ✅ | ✅ | ✅ | ✅ | ❌ (block+toast, IR-PG-01) | ❌ (locked always, R05) | ✅ (auto-skip used>0) | ✅ | ✅ |
| Auditor (Watcher) | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| System | — | — | — | — | Block + Toast | Block | Skip + report | Validate per-row | — |

---

## §5.4 Field Validation Rules

| Field | Rule | Error code |
|---|---|---|
| `code` (tab1) | required, unique (R03), uppercased | `BR_FIELD_REQUIRED` / `BR_CODE_DUPLICATE` |
| `kind` | required on create; read-only on edit (R05) | `BR_FIELD_REQUIRED` / `BR_KIND_LOCKED` |
| `name_th` | required | `BR_FIELD_REQUIRED` |
| `account_1` | required always; type-match per kind (R01/R02) | `BR_FIELD_REQUIRED` / `BR_ACCOUNT_TYPE_MISMATCH` |
| `account_2` | required for vendor/inventory/customer; N/A for bank | `BR_FIELD_REQUIRED` / `BR_ACCOUNT_TYPE_MISMATCH` |
| `bus_group`/`prod_group` (tab2) | required, combination unique (R04) | `BR_FIELD_REQUIRED` / `BR_COMBINATION_DUPLICATE` |
| `sales_account`/`purchase_account`/`cogs_account` | required, type-match | `BR_FIELD_REQUIRED` / `BR_ACCOUNT_TYPE_MISMATCH` |
| CSV row (either tab) | REQUIRED / BAD_KIND / CODE_DUPLICATE (or combination-dup) / account-not-in-COA / BAD_STATUS | (skip row, no hard error to caller) |

### Cross-field rules
- `account_2` MUST be NULL when `kind='bank'` (DB CHECK, `04_DB.md`)
- `(bus_group, prod_group)` MUST be unique among non-deleted rows (R04, DB unique index)

---

## §5.5 Edge Cases

### From BRD §10.1 (BA-confirmed, ☑)

| ID | Scenario | Resolution |
|---|---|---|
| EC-01 (E01) | `code` blank/duplicate | Block + inline error + toast (S-05) |
| EC-02 (E02) | `name_th` blank | Block (S-05) |
| EC-03 (E03) | required primary account blank | Block (S-05) |
| EC-04 (E04) | `(bus_group,prod_group)` duplicate | Block both fields + toast (R04) |
| EC-05 (E05) | `used>0`, attempt to change `code`/combination | Block + toast (IR-PG-01) |
| EC-06 (E06) | `kind` changed before submit | Clear all account fields (R07) |
| EC-07 (E07) | bulk-delete includes `used>0` rows | Skip + report count (R06) |
| EC-08 (E08) | import row invalid | Skip row, show reason on hover |
| EC-09 (E09) | import row blank status | Default `draft` (BR-07) |
| EC-10 (E10) | tab switch | Clear bulk selection + status filter (OB-6) |

### From BRD §10.2 (AI-pattern, unconfirmed ☐ — Lane Mode handling)

> Per Lane Mode (no-ask): where BRD/PREBRIEF gave no answer, a **conservative default** is applied and tagged `[AI-DEFAULT]`, with an Open Question logged in `00_OVERVIEW.md` §0.8 (OQ-FRD-07) for BA confirmation at SOW3.7. Where a probe has no safe default without more product input, it stays unconfirmed and undecided (no code should special-case it).

| ID | Scenario | Lane Mode disposition |
|---|---|---|
| DI-01 | COA account referenced by this feature gets deactivated at COA while still referenced | `[AI-DEFAULT]`: no automatic warning banner built this pass (would require a COA→PG reverse-lookup job, out of scope); the existing dropdown-filter behavior (inactive accounts simply stop appearing as *new* choices) is the only mitigation. **Not resolved — flagged as a UX follow-up, not blocking.** |
| DI-02 | COA account deleted while referenced | `[AI-DEFAULT]`: recommend COA restrict deletion of any account referenced by this feature — but that restriction lives in **F-COA-001**, not here. This feature's own mitigation: `account_1`/`account_2` are stored as plain `varchar` codes (soft-ref), so a COA delete never cascades or corrupts this feature's data; it would just make the code unresolvable at GL-resolve time (BR-08's existing failure mode). |
| DI-03 | COA account renamed (same code) | `[AI-DEFAULT]`: live-lookup, not snapshot — `acctName()`/`acctLabel()` pattern in the as-built HTML always resolves the *current* COA name for display. Carried forward as the default; no snapshot column added. |
| DI-04 | Search dropdown finds nothing because account filtered out by type | `[AI-DEFAULT]`: **not implemented this pass** — the as-built `sdd-empty` state just shows "ไม่พบรายการ" generically, no reason-for-filter message. Left as a UX enhancement opportunity, not a blocker. |
| CA-01 | 2 sessions edit same record concurrently | `[AI-DEFAULT]`: optimistic locking added (`version` column + `If-Match` header, see `04_DB.md`/`02_API.md` §2.3) — conservative default per PR-2 probe guidance, since BRD doesn't confirm behavior but concurrent edit on financial-control mapping is a real risk (BRD §16.4 R-03). |
| CA-07 | 2 sessions create same `code` simultaneously (race before unique constraint fires) | `[AI-DEFAULT]`: DB-level UNIQUE constraint (not just app-level check) is mandatory — see `04_DB.md` §4.2. This is a correctness requirement regardless of BA confirmation, so it is treated as settled, not left open. |
| ST-02 | Revert active→draft on high-`used` record | **Left unconfirmed** — no default applied; BR-06 already allows this transition unconditionally, and no additional audit-reason-prompt is built this pass. If BA wants a soft-warning, that's a UI addition for a future pass. |
| ST-04 | Set inactive on high-`used` record without extra warning | **Left unconfirmed** — same as ST-02, BR-06 already permits it; no soft-warning built. |
| PM-03 | Non-Finance role calls API directly | `[AI-DEFAULT]`: server-side role re-check on every mutation endpoint (see `02_API.md` §2.3) — this is baseline security practice, applied regardless of explicit BA confirmation. |
| PM-04 | Multi-company/branch scoping | **Left unconfirmed** — BRD confirms as-built has no company/branch scoping; nothing added this pass beyond the existing tenant-level RLS assumption (§0.7). |
| FU-01 | CSV file too large | `[AI-DEFAULT]`: recommend a conservative cap (e.g. 5MB / 5,000 rows) at the API layer — no number confirmed by BRD, so this default should be treated as a placeholder pending BA/infra confirmation, not a hard product requirement. |
| FU-02 | Wrong file type uploaded (renamed .xlsx) | `[AI-DEFAULT]`: validate actual content, not just extension (parse-and-fail gracefully with a clear error) — baseline defensive practice. |

---

## §5.6 Error Catalog

| Code | HTTP | Cause |
|---|---|---|
| `BR_FIELD_REQUIRED` | 400/422 | Required field missing |
| `BR_CODE_DUPLICATE` | 422 | R03 — code not unique |
| `BR_COMBINATION_DUPLICATE` | 422 | R04 — bus×prod not unique |
| `BR_KIND_LOCKED` | 422 | R05 — attempted kind change |
| `BR_CODE_LOCKED_USED` | 422 | IR-PG-01 (tab1) — code change attempted on used>0 |
| `BR_COMBINATION_LOCKED_USED` | 422 | IR-PG-01 (tab2) — combination change attempted on used>0 |
| `BR_ACCOUNT_TYPE_MISMATCH` | 422 | R01/R02 — account type doesn't match field |
| `BR_ACCOUNT_NOT_LEAF_OR_INACTIVE` | 422 | R01 — account not leaf/postable/active |
| `BR_USED_GT_ZERO` | 200 (skip, not error) | R06 — bulk-delete skip reason |
| `ERR_NOT_AUTHENTICATED` | 401 | No/invalid token |
| `ERR_INSUFFICIENT_ROLE` | 403 | Role mismatch (PM-03 default) |
| `ERR_NOT_FOUND` | 404 | Resource missing |
| `ERR_DUPLICATE_IDEMPOTENCY_KEY` | 409 | PR-7 default |
| `ERR_STALE_DATA` | 409 | PR-2/CA-01 default (optimistic lock) |

---

## §5.7 Security Bible Application

> Domains triggered: **D2, D5, D9, D15, D17** (per BRD §16.2/§16.3 — Security Preset **P4 Financial/Payment, 16 controls**, 1 marked N/A: S01-05 3-Way Matching, since this is not an invoice-matching feature)

### D2: Authentication & Session
- All endpoints require JWT; standard TTL per platform convention

### D5: Financial Transactions (control-account mapping)
- Every mutation (create/edit/status/delete/import) → mandatory before/after audit log (S01-07 Must)
- No amount-based approval threshold applies (no monetary amounts in this feature's data — the "financial" risk is *classification* risk, not transaction-amount risk)

### D9: Audit Logging
- `T_audit_log` entry per mutation; retention 7 years, append-only (S06-03)

### D15: Admin Actions
- Status transitions logged with actor identity (no "reason required" field exists in as-built HTML — BRD §16.3 S11-02 *recommends* ticket/reason enforcement but does not mandate it; not built this pass, flagged as recommendation only)

### D17: Multi-Tenant Isolation
- RLS on both tables; `X-Tenant-Id` middleware validation

### D-CLASS: Data Classification
- All fields Internal, no Confidential/Restricted fields — see `04_DB.md` §4.6 for full detail. No masking/hiding UI behavior needed.

### Security Control Checklist reference (BRD §16.3, P4)
| Control | Must/Optional | This feature's status |
|---|---|---|
| S01-04 SoD Conflict Matrix | Must | Finance Lead role kept separate from GL-posting role (out of scope, BR-08) |
| S01-07 Immutable Master Data Log | Must | Implemented — every mutation audited |
| S02-02 MFA Enforcer | Must (recommended) | Infra-dependent — not implementable in this FRD's scope, flagged for platform team |
| S04-06 SLA & Escalation | Must | See BRD §17.1 — operational, not a code requirement here |
| S06-01 ABAC | Must | Role check on every endpoint (Finance Lead only for mutations) |
| S06-03 Standardized Audit Content | Must | Who/What/When/Result on every mutation |
| S11-01 UAR Scheduler | Must | Operational (90-day review) — not a code requirement here |
| S11-02 Ticket Enforcement | Must (recommended) | Not built this pass — see D15 note above |
| S01-05 3-Way Matching | N/A | Correctly excluded — not an invoice-matching feature |

---

## §5.8 Compliance & Audit Requirements

| Requirement | Implementation |
|---|---|
| Internal audit trail on all mapping changes | `T_audit_log`, 7-year retention |
| No PII / PDPA scope | Confirmed N/A — no fields carry personal data |
| GL misstatement risk mitigation | BR-01 (type-match validation) + S01-07 (immutable log) are the primary controls, since there is no approval workflow to catch errors (BRD §16.4 R-01) |
