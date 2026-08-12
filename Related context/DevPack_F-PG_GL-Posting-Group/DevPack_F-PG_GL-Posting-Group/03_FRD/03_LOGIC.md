# 03_LOGIC — F-PG GL Posting Group

> **Audience:** BE dev (business logic layer)
> **Scope:** All non-HTTP logic for both entities (`GL_Posting_Group`, `GL_Posting_Setup`)
> **CUBIC alignment:** §3.1 Functions = scope-local · §3.2 Engine = candidate for CUBIC Registry (1 engine, resolves OQ-PG-02)

---

## §3.1 Functions (Scope-Local)

### F-PG-FN-01: `createPostingGroup`
- **Purpose:** Create a new `GL_Posting_Group` row after validation passes.
- **Input:** `{ code: string, kind: 'vendor'|'inventory'|'bank'|'customer', name_th: string, name_en?: string, account_1: string, account_2?: string, status?: 'draft'|'active'|'inactive' }`
- **Output:** `GL_Posting_Group | ValidationError[]`
- **Invoked by:** F-PG-API-02
- **Calls:** F-PG-FN-03 `validatePostingGroupData`
- **Side effects:** INSERT `T_gl_posting_group` (`used=0`, `doa_field_1..4=null`); INSERT `T_audit_log`
- **Error cases:** `BR_CODE_DUPLICATE`, `BR_ACCOUNT_TYPE_MISMATCH`, `BR_ACCOUNT_NOT_LEAF_OR_INACTIVE`, `BR_FIELD_REQUIRED`
- **Iron rule check:** ✅ no HTTP terms

### F-PG-FN-02: `updatePostingGroup`
- **Purpose:** Update an existing `GL_Posting_Group`, enforcing R05 (kind always locked) and IR-PG-01 (code locked only when `used>0`) — **two separate guards, checked independently, never merged into one condition.**
- **Input:** `{ id: string, patch: Partial<GL_Posting_Group> }`
- **Output:** `GL_Posting_Group | ValidationError[]`
- **Invoked by:** F-PG-API-04
- **Calls:** F-PG-FN-03 `validatePostingGroupData`
- **Side effects:** UPDATE `T_gl_posting_group`; INSERT `T_audit_log` (before/after diff)
- **Guard logic (pseudo, ≤10 lines — belongs here per matrix #9, not in 02_API):**
  ```
  if patch.kind is present AND patch.kind != current.kind:
      reject BR_KIND_LOCKED               // R05 — always, regardless of used
  if current.used > 0 AND patch.code is present AND patch.code != current.code:
      reject BR_CODE_LOCKED_USED          // IR-PG-01 — only when used>0
  // name_th, name_en, account_1, account_2, status: always allowed
  ```
- **Error cases:** `BR_KIND_LOCKED`, `BR_CODE_LOCKED_USED`, `BR_ACCOUNT_TYPE_MISMATCH`, `BR_CODE_DUPLICATE`
- **Iron rule check:** ✅ no HTTP terms

### F-PG-FN-03: `validatePostingGroupData`
- **Purpose:** Centralized field + business validation for both create and update (R01, R02, R03, R07).
- **Input:** `{ code, kind, name_th, account_1, account_2?, isEdit: boolean, existingId?: string }`
- **Output:** `ValidationError[]` (empty = valid)
- **Invoked by:** F-PG-FN-01, F-PG-FN-02, F-PG-FN-13 (import path)
- **Calls:** ENG-PG-01 `coa-account-resolver` (to check account exists + type-matches per kind)
- **Side effects:** none (pure validation, read-only DB check for uniqueness)
- **Validates:**
  - `code` required, non-empty, unique across `T_gl_posting_group` (excluding `existingId` on edit) — R03
  - `kind` one of 4 enum values
  - `name_th` required, non-empty
  - primary account required per kind (`account_1` always; `account_2` required for vendor/inventory/customer, N/A for bank) — R01
  - each account must resolve via ENG-PG-01 as leaf+postable+active+type-matched — R01/R02
  - **R07 note:** clearing `account_1`/`account_2` on kind-change is a **client-side, pre-submit** UI behavior (`onKindChange` in HTML) — nothing to validate server-side beyond "the submitted account must match the submitted kind's expected type," which this function already does
- **Error cases:** `BR_CODE_DUPLICATE`, `BR_ACCOUNT_TYPE_MISMATCH`, `BR_ACCOUNT_NOT_LEAF_OR_INACTIVE`, `BR_FIELD_REQUIRED`
- **Iron rule check:** ✅ no HTTP terms

### F-PG-FN-04: `buildPostingGroupListQuery`
- **Purpose:** Build the filtered/paginated query for list + detail reads.
- **Input:** `{ kind?, status?, search?, limit?, offset?, id? }`
- **Output:** `{ data: GL_Posting_Group[], total: number }`
- **Invoked by:** F-PG-API-01, F-PG-API-03
- **Calls:** —
- **Side effects:** none (read-only)
- **Iron rule check:** ✅ no HTTP terms

### F-PG-FN-05: `changePostingGroupStatus`
- **Purpose:** Free, unconditional status transition among `draft`/`active`/`inactive` (BR-06 — no approval, all 3×3 transitions allowed).
- **Input:** `{ id: string, status: 'draft'|'active'|'inactive' }`
- **Output:** `GL_Posting_Group | ValidationError[]`
- **Invoked by:** F-PG-API-05
- **Calls:** —
- **Side effects:** UPDATE `status`, `modified_by`, `modified_date`; INSERT `T_audit_log`
- **Error cases:** `BR_FIELD_REQUIRED` (invalid enum)
- **Iron rule check:** ✅ no HTTP terms

### F-PG-FN-06: `bulkDeletePostingGroups`
- **Purpose:** Soft-delete every selected row whose `used=0`; silently skip the rest (R06).
- **Input:** `{ ids: string[] }`
- **Output:** `{ deleted: string[], skipped: {id,reason}[] }`
- **Invoked by:** F-PG-API-06
- **Calls:** —
- **Side effects:** soft-delete rows (`used=0` only); INSERT `T_audit_log` per deleted row
- **Error cases:** none — this function never fails the whole batch, it partitions and reports
- **Iron rule check:** ✅ no HTTP terms

### F-PG-FN-07: `createPostingSetup`
- **Purpose:** Create a new `GL_Posting_Setup` row.
- **Input:** `{ bus_group, prod_group, sales_account, purchase_account, cogs_account, status? }`
- **Output:** `GL_Posting_Setup | ValidationError[]`
- **Invoked by:** F-PG-API-11
- **Calls:** F-PG-FN-09 `validatePostingSetupData`
- **Side effects:** INSERT `T_gl_posting_setup` (`used=0`, DOA null×4); INSERT `T_audit_log`
- **Error cases:** `BR_COMBINATION_DUPLICATE`, `BR_ACCOUNT_TYPE_MISMATCH`, `BR_FIELD_REQUIRED`
- **Iron rule check:** ✅ no HTTP terms

### F-PG-FN-08: `updatePostingSetup`
- **Purpose:** Update an existing `GL_Posting_Setup`, enforcing IR-PG-01's tab-2 variant: the **combined** `(bus_group, prod_group)` pair locks together when `used>0` — there is no R05-equivalent single-field lock on this entity.
- **Input:** `{ id: string, patch: Partial<GL_Posting_Setup> }`
- **Output:** `GL_Posting_Setup | ValidationError[]`
- **Invoked by:** F-PG-API-13
- **Calls:** F-PG-FN-09
- **Guard logic (≤10 lines):**
  ```
  if current.used > 0 AND (
       (patch.bus_group present AND patch.bus_group != current.bus_group) OR
       (patch.prod_group present AND patch.prod_group != current.prod_group)
     ):
      reject BR_COMBINATION_LOCKED_USED   // IR-PG-01 tab2 — pair locks together
  // sales_account, purchase_account, cogs_account, status: always allowed
  ```
- **Side effects:** UPDATE `T_gl_posting_setup`; INSERT `T_audit_log`
- **Error cases:** `BR_COMBINATION_LOCKED_USED`, `BR_ACCOUNT_TYPE_MISMATCH`, `BR_COMBINATION_DUPLICATE`
- **Iron rule check:** ✅ no HTTP terms

### F-PG-FN-09: `validatePostingSetupData`
- **Purpose:** Centralized validation for tab-2 create/update (R02, R04).
- **Input:** `{ bus_group, prod_group, sales_account, purchase_account, cogs_account, isEdit, existingId? }`
- **Output:** `ValidationError[]`
- **Invoked by:** F-PG-FN-07, F-PG-FN-08, F-PG-FN-13
- **Calls:** ENG-PG-01
- **Validates:** all 5 fields required; `(bus_group, prod_group)` unique (R04); each account resolves via ENG-PG-01 with correct type (`sales`=income, `purchase`=expense∨asset, `cogs`=expense)
- **Error cases:** `BR_COMBINATION_DUPLICATE`, `BR_ACCOUNT_TYPE_MISMATCH`, `BR_FIELD_REQUIRED`
- **Iron rule check:** ✅ no HTTP terms

### F-PG-FN-10: `buildPostingSetupListQuery`
- **Purpose:** Build filtered/paginated query for tab-2 list + detail.
- **Input:** `{ status?, search?, limit?, offset?, id? }`
- **Output:** `{ data: GL_Posting_Setup[], total: number }`
- **Invoked by:** F-PG-API-10, F-PG-API-12
- **Iron rule check:** ✅ no HTTP terms

### F-PG-FN-11: `changePostingSetupStatus`
- **Purpose:** Same free-transition behavior as FN-05, for tab 2.
- **Input:** `{ id, status }` · **Output:** `GL_Posting_Setup | ValidationError[]`
- **Invoked by:** F-PG-API-14
- **Iron rule check:** ✅ no HTTP terms

### F-PG-FN-12: `bulkDeletePostingSetups`
- **Purpose:** Same partition-and-skip behavior as FN-06, for tab 2.
- **Input:** `{ ids: string[] }` · **Output:** `{ deleted: string[], skipped: {id,reason}[] }`
- **Invoked by:** F-PG-API-15
- **Iron rule check:** ✅ no HTTP terms

### F-PG-FN-13: `previewImportRows`
- **Purpose:** Validate a batch of parsed CSV rows against R01-R07 without writing anything, returning per-row error lists — shared logic across both tabs via an `entityType` discriminator (`'group'` \| `'setup'`), matching the as-built HTML's shared CSV parsing/validation path.
- **Input:** `{ entityType: 'group'|'setup', rows: RawCsvRow[] }`
- **Output:** `{ rows: (RawCsvRow & { errors: string[] })[] }`
- **Invoked by:** F-PG-API-07, F-PG-API-16
- **Calls:** F-PG-FN-03 (entityType=group) or F-PG-FN-09 (entityType=setup), ENG-PG-01
- **Per-row error codes (verbatim from as-built):**
  - Group rows: `REQUIRED` (code/name_th/account_1 blank) · `BAD_KIND` (kind not in 4-value enum) · `CODE_DUPLICATE` (vs registry or within file) · account-not-in-COA · `BAD_STATUS` (status text not blank and not one of ใช้งาน/ไม่ใช้งาน/ร่าง)
  - Setup rows: `REQUIRED` · bus/prod-not-recognized (not in current value set — flag OQ-PG-04 relevance) · combination-duplicate (R04, vs registry or within file) · account-not-in-COA · `BAD_STATUS`
- **Side effects:** none (validation only, no DB write)
- **Iron rule check:** ✅ no HTTP terms

### F-PG-FN-14: `commitImportRows`
- **Purpose:** Insert only the zero-error rows from a prior preview, merge-only (LOCK-03 — never updates/overwrites existing rows).
- **Input:** `{ entityType: 'group'|'setup', rows: ValidatedRow[] }` (rows must already have `errors: []`)
- **Output:** `{ imported: number, skipped: number }`
- **Invoked by:** F-PG-API-08, F-PG-API-17
- **Calls:** —
- **Side effects:** INSERT one row per valid row (`used=0`, DOA null×4, `status` = row value or `draft` if blank — BR-07); INSERT `T_audit_log` per row
- **Iron rule check:** ✅ no HTTP terms

### F-PG-FN-15: `exportPostingRegistry`
- **Purpose:** Produce CSV bytes (UTF-8 BOM) for the currently-filtered rows of either tab, columns matching the import template (roundtrip), status rendered in Thai.
- **Input:** `{ entityType: 'group'|'setup', filters: {...} }`
- **Output:** `Buffer` (CSV bytes, `text/csv; charset=utf-8`, BOM-prefixed)
- **Invoked by:** F-PG-API-09, F-PG-API-18
- **Calls:** F-PG-FN-04 or F-PG-FN-10 (to fetch filtered rows)
- **Iron rule check:** ✅ no HTTP terms

### F-PG-FN-16: `listProductPostingGroupValues`
- **Purpose:** Serve Item Master's `GET /gl/posting-groups?type=product` contract — returns the distinct `prod_group` value set currently defined in `T_gl_posting_setup`.
- **Input:** `{}`
- **Output:** `{ value: string, label: string }[]`
- **Invoked by:** F-PG-API-19
- **Calls:** —
- **Note:** **Data gap** — returns the as-built 2-value set (`GOODS`, `SERVICE`), not Item's 6-value set. Blocked on OQ-PG-04. This function is correct as specified; the gap is a data/scope decision, not a bug.
- **Iron rule check:** ✅ no HTTP terms

### F-PG-FN-17: `listVatGroups`
- **Purpose:** Serve Item Master's `GET /gl/vat-groups` contract.
- **Input:** `{}`
- **Output:** `{ value: string, label: string }[]` (currently always `[]`)
- **Invoked by:** F-PG-API-20
- **Calls:** —
- **Note:** **Stub** — no VAT Posting Setup entity exists (blocked on OQ-PG-01). Must return an empty array plus a gap indicator in response metadata, not an error, so Item Master can degrade gracefully.
- **Iron rule check:** ✅ no HTTP terms

---

## §3.2 Engine (Reusable / CUBIC-Registered)

> 1 engine only — resolves OQ-PG-02. STANDARD variant allows ≤2 engines; this feature needs exactly 1.

### ENG-PG-01: `coa-account-resolver` [NEW]

| Field | Value |
|---|---|
| **id** | (assigned at CUBIC registration) |
| **code** | `coa-account-resolver` |
| **name** | COA Account Resolver |
| **category** | `integration` |
| **status** | DRAFT (this FRD) |
| **owner** | F-PG (this feature) — candidate for promotion to `shared` if a 2nd feature needs COA-filtered dropdowns before F-COA-001 exposes its own shared SDK |

**Input Schema:**
```json
{
  "type": "object",
  "required": ["allowed_types"],
  "properties": {
    "account_code": { "type": "string", "description": "optional — validate one specific code (import/submit path)" },
    "allowed_types": { "type": "array", "items": { "enum": ["asset","liability","equity","income","expense"] }, "description": "per §2.5 type-filter map" },
    "search": { "type": "string", "description": "optional — for dropdown-open path" }
  }
}
```

**Output Schema:**
```json
{
  "type": "object",
  "properties": {
    "options": { "type": "array", "items": { "type": "object", "properties": {
      "code": {"type":"string"}, "name": {"type":"string"}, "type": {"type":"string"} } } },
    "valid": { "type": "boolean", "description": "present only when account_code was passed — true if code exists AND is leaf AND is postable AND status=active AND type in allowed_types" }
  }
}
```

**Logic Outline:**
1. Call `GET /api/v1/coa/accounts?is_leaf=true&is_postable=true&status=active&type=<allowed_types>` (F-COA-001, see `02_API.md` §2.5)
2. If `account_code` given: check the returned set contains that code → `valid=true`, else `valid=false`
3. If `search` given: client-side substring filter over `name`+`code` (mirrors as-built `searchDropdown()` behavior)
4. Return `options` (dropdown-open path) or `{valid}` (single-code validation path, used by FN-03/FN-09/FN-13)

**Used by features:**
- F-PG (current — this FRD): FN-03, FN-09, FN-13 all call this engine instead of the current hardcoded `COA_ACCOUNTS` array
- F-PDM / others (planned): any future feature needing a "COA-filtered-by-type" dropdown can reuse this engine rather than re-implementing the filter map

**Iron rule check:**
- [x] Reusable — 2+ features (current + planned, per above)
- [x] Substantial — external integration + type-filter logic, not a 5-line helper
- [ ] Pure — **partially** (it makes an outbound HTTP call to F-COA-001; this is expected and accepted for `category: integration` engines per `cubic-schema-templates.md` Layer 3 pattern #3 "External integration," which explicitly permits this — 2-of-3 criteria still satisfied via Reusable + Substantial)

**CUBIC Registration note:**
- [ ] DRAFT → register at dev hand-off, once F-COA-001's real endpoint is confirmed live (see `02_API.md` §2.5 rollout gate)

**Test cases:**
- TC-1: `allowed_types=['liability']`, account is a leaf+postable+active liability → `valid=true`
- TC-2: same account but `status=inactive` at COA → `valid=false`
- TC-3: `allowed_types=['asset','liability']` (interim/GR-IR case), account is liability → `valid=true`
- TC-4: account not found at COA at all → `valid=false`, no exception thrown

---

## §3.3 API ↔ Logic Trace Table (R8 Anchor)

| API ID | Method | Path | Calls Functions | Calls Engines |
|---|---|---|---|---|
| F-PG-API-01 | GET | posting-groups | FN-04 | — |
| F-PG-API-02 | POST | posting-groups | FN-01, FN-03 | ENG-PG-01 |
| F-PG-API-03 | GET | posting-groups/:id | FN-04 | — |
| F-PG-API-04 | PUT | posting-groups/:id | FN-02, FN-03 | ENG-PG-01 |
| F-PG-API-05 | POST | posting-groups/:id/status | FN-05 | — |
| F-PG-API-06 | POST | posting-groups/bulk-delete | FN-06 | — |
| F-PG-API-07 | POST | posting-groups/import/preview | FN-13 | ENG-PG-01 |
| F-PG-API-08 | POST | posting-groups/import/commit | FN-14 | — |
| F-PG-API-09 | GET | posting-groups/export | FN-15 | — |
| F-PG-API-10 | GET | posting-setups | FN-10 | — |
| F-PG-API-11 | POST | posting-setups | FN-07, FN-09 | ENG-PG-01 |
| F-PG-API-12 | GET | posting-setups/:id | FN-10 | — |
| F-PG-API-13 | PUT | posting-setups/:id | FN-08, FN-09 | ENG-PG-01 |
| F-PG-API-14 | POST | posting-setups/:id/status | FN-11 | — |
| F-PG-API-15 | POST | posting-setups/bulk-delete | FN-12 | — |
| F-PG-API-16 | POST | posting-setups/import/preview | FN-13 | ENG-PG-01 |
| F-PG-API-17 | POST | posting-setups/import/commit | FN-14 | — |
| F-PG-API-18 | GET | posting-setups/export | FN-15 | — |
| F-PG-API-19 | GET | posting-groups?type=product | FN-16 | — |
| F-PG-API-20 | GET | vat-groups | FN-17 | — |

### Trace Verification (Self-Check)
- [x] Every mutation API has ≥1 Function/Engine
- [x] No orphan Function — FN-01..FN-17 all appear above
- [x] No orphan Engine — ENG-PG-01 appears via FN-03/FN-09/FN-13 (indirect) and directly on all 4 create/update/import-preview APIs
- [x] No hidden logic in `02_API.md` — all business logic traced here

---

## §3.4 Dependencies

### External Function/Engine called
- `GET /api/v1/coa/accounts` (F-COA-001) — called by ENG-PG-01

### External Function/Engine that calls into this feature
- Item Master (F-PDM) calls `F-PG-API-19`/`F-PG-API-20` (→ FN-16/FN-17) — see `02_API.md` §2.6
- GL/Journal Engine reads `T_gl_posting_group`/`T_gl_posting_setup` directly (no function call — DB-level soft-reference, see `02_API.md` §2.7)

---

## §3.5 Open Questions / Notes Referenced

- ENG-PG-01 registration timing depends on F-COA-001's real endpoint availability — not this FRD's blocker, but dev hand-off should confirm before removing the mock fallback.
- FN-16's data gap (2-value vs 6-value prod_group set) is a **data** issue tracked as OQ-PG-04, not a logic defect in FN-16 itself.
