# 02_API — F-PG GL Posting Group

> **Audience:** Backend developer (HTTP layer)
> **🚨 Iron Rule:** No business logic > 5 lines here — see `03_LOGIC.md` §3.1/§3.2 (R8 traceability)
> **⭐ §2.5 of this file resolves OQ-PG-02** (per BRD §15 explicit instruction — COA dropdown sync contract, written directly here instead of a separate meeting)

---

## §2.1 API Overview

| ID | Method | Path | Summary | Auth |
|---|---|---|---|---|
| F-PG-API-01 | GET | /api/v1/gl/posting-groups | List specific posting groups (filter/search) | required |
| F-PG-API-02 | POST | /api/v1/gl/posting-groups | Create specific posting group | required (Finance Lead) |
| F-PG-API-03 | GET | /api/v1/gl/posting-groups/:id | Get one posting group | required |
| F-PG-API-04 | PUT | /api/v1/gl/posting-groups/:id | Update posting group | required (Finance Lead) |
| F-PG-API-05 | POST | /api/v1/gl/posting-groups/:id/status | Change status (free, no approval) | required (Finance Lead) |
| F-PG-API-06 | POST | /api/v1/gl/posting-groups/bulk-delete | Bulk soft-delete (skip used>0) | required (Finance Lead) |
| F-PG-API-07 | POST | /api/v1/gl/posting-groups/import/preview | Validate CSV rows (no write) | required (Finance Lead) |
| F-PG-API-08 | POST | /api/v1/gl/posting-groups/import/commit | Commit valid rows, merge-only | required (Finance Lead) |
| F-PG-API-09 | GET | /api/v1/gl/posting-groups/export | Export filtered rows as CSV | required (Finance Lead, Auditor) |
| F-PG-API-10 | GET | /api/v1/gl/posting-setups | List general posting setups | required |
| F-PG-API-11 | POST | /api/v1/gl/posting-setups | Create posting setup | required (Finance Lead) |
| F-PG-API-12 | GET | /api/v1/gl/posting-setups/:id | Get one posting setup | required |
| F-PG-API-13 | PUT | /api/v1/gl/posting-setups/:id | Update posting setup | required (Finance Lead) |
| F-PG-API-14 | POST | /api/v1/gl/posting-setups/:id/status | Change status | required (Finance Lead) |
| F-PG-API-15 | POST | /api/v1/gl/posting-setups/bulk-delete | Bulk soft-delete (skip used>0) | required (Finance Lead) |
| F-PG-API-16 | POST | /api/v1/gl/posting-setups/import/preview | Validate CSV rows | required (Finance Lead) |
| F-PG-API-17 | POST | /api/v1/gl/posting-setups/import/commit | Commit valid rows, merge-only | required (Finance Lead) |
| F-PG-API-18 | GET | /api/v1/gl/posting-setups/export | Export filtered rows as CSV | required (Finance Lead, Auditor) |
| F-PG-API-19 | GET | /api/v1/gl/posting-groups?type=product | **Served to Item Master (F-PDM)** — product posting group values | required (service-to-service) |
| F-PG-API-20 | GET | /api/v1/gl/vat-groups | **Served to Item Master (F-PDM)** — VAT group values (**stub, blocked OQ-PG-01**) | required (service-to-service) |

> **Not in this list:** `GET /api/v1/coa/accounts` — this feature **consumes** it (does not serve it); see §2.5.

---

## §2.2 Per-API Contract — Tab 1 (Specific Posting Groups)

### F-PG-API-01: GET /api/v1/gl/posting-groups

| Field | Value |
|---|---|
| **id** | F-PG-API-01 |
| **method** | GET |
| **path** | /api/v1/gl/posting-groups |
| **summary** | List posting groups with filters (matches P-01 tab1 filter bar) |
| **auth** | required |
| **roles** | Finance Lead, Auditor |
| **rate-limit** | default |

**Request — Query params:**
- `kind` (optional): `vendor` \| `inventory` \| `bank` \| `customer` \| `all` (default `all`)
- `status` (optional): `draft` \| `active` \| `inactive` \| `all` (default `all`)
- `search` (optional): matches `code`, `name_th`, `name_en` (case-insensitive substring)
- `limit` / `offset` (optional, default 20/0, max 100)

**Response 200:**
```json
{
  "data": [
    { "id": "g1", "code": "LOCAL", "kind": "vendor", "name_th": "เจ้าหนี้ในประเทศ", "name_en": "Domestic Vendors",
      "account_1": "2-1-10-01", "account_2": "1-1-40", "status": "active", "used": 82,
      "created_by": "uuid", "created_date": "2026-01-10T09:00:00Z", "modified_by": "uuid", "modified_date": "2026-01-10T09:00:00Z" }
  ],
  "total": 7, "limit": 20, "offset": 0
}
```

**Error Responses:** 400 `ERR_INVALID_QUERY_PARAMS` · 401 `ERR_NOT_AUTHENTICATED` · 403 `ERR_INSUFFICIENT_ROLE`
**Preconditions:** — **Side effects:** — (read-only)
**Calls (Logic):** F-PG-FN-04 `buildPostingGroupListQuery` — see `03_LOGIC.md` §3.1

---

### F-PG-API-02: POST /api/v1/gl/posting-groups

| Field | Value |
|---|---|
| **id** | F-PG-API-02 |
| **method** | POST |
| **path** | /api/v1/gl/posting-groups |
| **summary** | Create a new specific posting group |
| **auth** | required |
| **roles** | Finance Lead |
| **rate-limit** | default |

**Request — Body:**
```json
{
  "code": "LOCAL",
  "kind": "vendor",
  "name_th": "เจ้าหนี้ในประเทศ",
  "name_en": "Domestic Vendors",
  "account_1": "2-1-10-01",
  "account_2": "1-1-40",
  "status": "active"
}
```
- **Headers:** `Idempotency-Key` (required — PR-7, double-submit guard for the double-click-submit scenario)
- **Validation (field-level ≤5 lines):** `code` required non-empty; `kind` required, one of 4 enum values; `name_th` required non-empty
- **Complex validation → 03_LOGIC.md F-PG-FN-03 `validatePostingGroupData`** (unique code, required account per kind, account type-match via ENG-PG-01)

**Response 201:**
```json
{ "id": "g8", "code": "LOCAL", "kind": "vendor", "status": "active", "used": 0,
  "doa_field_1": null, "doa_field_2": null, "doa_field_3": null, "doa_field_4": null,
  "created_by": "uuid", "created_date": "2026-08-10T10:00:00Z" }
```

**Error Responses:**
- 400 `ERR_VALIDATION_FAILED` (required fields missing)
- 403 `ERR_INSUFFICIENT_ROLE`
- 409 `ERR_DUPLICATE_IDEMPOTENCY_KEY`
- 422 `BR_CODE_DUPLICATE` — 05_RULES BR-02
- 422 `BR_ACCOUNT_TYPE_MISMATCH` — 05_RULES BR-01
- 422 `BR_ACCOUNT_NOT_LEAF_OR_INACTIVE` — 05_RULES BR-01

**Preconditions:** `kind` is one of the 4 defined values
**Side effects:** INSERT `T_gl_posting_group` (with `used=0`, DOA placeholders ×4 `null`), INSERT `T_audit_log`
**Calls (Logic):** F-PG-FN-01 `createPostingGroup`, F-PG-FN-03 `validatePostingGroupData`, ENG-PG-01 `coa-account-resolver` — see `03_LOGIC.md` §3.1/§3.2

---

### F-PG-API-03: GET /api/v1/gl/posting-groups/:id

| Field | Value |
|---|---|
| **id** | F-PG-API-03 · **method** GET · **path** /api/v1/gl/posting-groups/:id · **auth** required · **roles** Finance Lead, Auditor |

**Response 200:** same shape as one item in F-PG-API-01's `data[]`.
**Error:** 404 `ERR_NOT_FOUND`
**Calls (Logic):** F-PG-FN-04 (single-record variant)

---

### F-PG-API-04: PUT /api/v1/gl/posting-groups/:id

| Field | Value |
|---|---|
| **id** | F-PG-API-04 · **method** PUT · **path** /api/v1/gl/posting-groups/:id · **auth** required · **roles** Finance Lead |

**Request — Body:** same shape as F-PG-API-02, plus optimistic concurrency header `If-Match` (see §2.3 note — **not implemented in current HTML mock**, recommended for real backend).

**Validation / business rules enforced server-side (see F-PG-FN-02):**
- `kind` field, if present in body, is **ignored / rejected** if it differs from current value — HTTP 422 `BR_KIND_LOCKED` (R05 — locked unconditionally, independent of `used`)
- If `used > 0` and `code` in body ≠ current `code` → HTTP 422 `BR_CODE_LOCKED_USED` (IR-PG-01 — **separate guard from R05**, only fires when `used>0`)
- All other fields (`name_th`, `name_en`, `account_1`, `account_2`, `status`) always accepted regardless of `used`

**Response 200:** updated record.
**Error Responses:** 400 `ERR_VALIDATION_FAILED` · 403 `ERR_INSUFFICIENT_ROLE` · 404 `ERR_NOT_FOUND` · 409 `ERR_STALE_DATA` (if `If-Match` implemented) · 422 `BR_KIND_LOCKED` · 422 `BR_CODE_LOCKED_USED` · 422 `BR_ACCOUNT_TYPE_MISMATCH`
**Side effects:** UPDATE `T_gl_posting_group`, INSERT `T_audit_log` (before/after diff, S01-07)
**Calls (Logic):** F-PG-FN-02 `updatePostingGroup`, F-PG-FN-03 `validatePostingGroupData`, ENG-PG-01

---

### F-PG-API-05: POST /api/v1/gl/posting-groups/:id/status

| Field | Value |
|---|---|
| **id** | F-PG-API-05 · **method** POST · **path** /api/v1/gl/posting-groups/:id/status · **auth** required · **roles** Finance Lead |

**Request — Body:** `{ "status": "active" | "draft" | "inactive" }`
**Response 200:** `{ "id": "g1", "status": "active", "modified_by": "uuid", "modified_date": "..." }`
**Error:** 400 `ERR_VALIDATION_FAILED` (invalid enum) · 404 `ERR_NOT_FOUND` · 403 `ERR_INSUFFICIENT_ROLE`
**Preconditions:** none — **all 3×3 transitions allowed, no approval step (BR-06)**
**Side effects:** UPDATE `T_gl_posting_group.status`, INSERT `T_audit_log`
**Calls (Logic):** F-PG-FN-05 `changePostingGroupStatus`

---

### F-PG-API-06: POST /api/v1/gl/posting-groups/bulk-delete

| Field | Value |
|---|---|
| **id** | F-PG-API-06 · **method** POST · **path** /api/v1/gl/posting-groups/bulk-delete · **auth** required · **roles** Finance Lead |

**Request — Body:** `{ "ids": ["g1","g2","g3"] }`
**Response 200:** `{ "deleted": ["g2"], "skipped": [{"id":"g1","reason":"BR_USED_GT_ZERO"}], "deleted_count": 1, "skipped_count": 1 }`
**Preconditions:** none — rows with `used>0` are silently skipped, never blocking the whole batch
**Side effects:** soft-delete rows where `used=0` (R06), INSERT `T_audit_log` per deleted row
**Calls (Logic):** F-PG-FN-06 `bulkDeletePostingGroups`

---

### F-PG-API-07 / F-PG-API-08: Import preview / commit

**F-PG-API-07 POST /import/preview**
- **Body:** `{ "rows": [{ "code":"IMPORT-V", "kind":"vendor", "name_th":"...", "name_en":"...", "account_1":"2-1-10-01", "account_2":"1-1-40", "status":"ใช้งาน" }, ...] }` (parsed CSV rows, one object per data row; columns per `04_DB.md` §4.1 template: `code,kind,name_th,name_en,account_1,account_2,status`)
- **Response 200:** `{ "rows": [{ ...row, "errors": ["CODE_DUPLICATE"] }, ...], "ok_count": 4, "err_count": 1 }`
- Per-row error codes (verbatim from as-built HTML validation): `REQUIRED` (code/name/required account blank) · `BAD_KIND` (kind not one of 4) · `CODE_DUPLICATE` (dup vs registry or within file) · `BAD_STATUS` (status text not ใช้งาน/ไม่ใช้งาน/ร่าง and non-blank) · account-not-in-COA (resolved via ENG-PG-01)
- **Calls (Logic):** F-PG-FN-13 `previewImportRows`

**F-PG-API-08 POST /import/commit**
- **Body:** `{ "rows": [<only rows with zero errors, from a prior preview call>] }`
- **Response 200:** `{ "imported": 4, "skipped": 1 }`
- **Side effects:** INSERT one `T_gl_posting_group` row per valid row (`used=0`, DOA null×4, status = row status or `draft` if blank per BR-07), INSERT `T_audit_log` per row. **Merge-only — never touches/updates existing rows (LOCK-03).**
- **Calls (Logic):** F-PG-FN-14 `commitImportRows`

---

### F-PG-API-09: GET /api/v1/gl/posting-groups/export

| Field | Value |
|---|---|
| **id** | F-PG-API-09 · **method** GET · **path** /api/v1/gl/posting-groups/export · **auth** required · **roles** Finance Lead, Auditor |

**Request — Query params:** same filters as F-PG-API-01 (`kind`, `status`, `search`) — export respects the currently-applied filter, matching HTML `exportCSV()`.
**Response 200:** `text/csv; charset=utf-8` with UTF-8 BOM, columns `code,kind,name_th,name_en,account_1,account_2,status` (roundtrips with import template), `status` rendered in Thai (`ใช้งาน`/`ไม่ใช้งาน`/`ร่าง`).
**Calls (Logic):** F-PG-FN-15 `exportPostingRegistry`

---

## §2.2b Per-API Contract — Tab 2 (General Posting Setup)

> Mirrors §2.2 structurally; only field/rule differences are called out.

### F-PG-API-10: GET /api/v1/gl/posting-setups
**Query params:** `status` (`all`/`draft`/`active`/`inactive`), `search` (matches `bus_group`+`prod_group` concatenation, per HTML `onSetupSearch`), `limit`/`offset`.
**Response 200:** array of `{ id, bus_group, prod_group, sales_account, purchase_account, cogs_account, status, used, created_by, created_date, modified_by, modified_date }`.
**Calls (Logic):** F-PG-FN-10 `buildPostingSetupListQuery`

### F-PG-API-11: POST /api/v1/gl/posting-setups
**Body:** `{ bus_group, prod_group, sales_account, purchase_account, cogs_account, status }` + `Idempotency-Key` header.
**Validation:** all 5 fields required; combination `(bus_group, prod_group)` must be unique (R04) → 422 `BR_COMBINATION_DUPLICATE`; each account type-matched via ENG-PG-01 (sales=`income`, purchase=`expense`\|`asset`, cogs=`expense` — see §2.5 note on purchase's dual-type allowance).
**Side effects:** INSERT `T_gl_posting_setup` (`used=0`, DOA null×4), INSERT `T_audit_log`.
**Calls (Logic):** F-PG-FN-07 `createPostingSetup`, F-PG-FN-09 `validatePostingSetupData`, ENG-PG-01

### F-PG-API-12: GET /api/v1/gl/posting-setups/:id
Single record fetch. **Calls (Logic):** F-PG-FN-10 (single-record variant)

### F-PG-API-13: PUT /api/v1/gl/posting-setups/:id
**Business rules enforced (F-PG-FN-08):**
- If `used > 0` and (`bus_group` ≠ current OR `prod_group` ≠ current) → 422 `BR_COMBINATION_LOCKED_USED` (IR-PG-01 tab2 variant — **the pair locks together**, not per-field independently)
- There is **no R05-equivalent** for tab2 (no single always-locked field like `kind`) — the only lock is the combined `bus_group+prod_group` pair, and only when `used>0`
- All 3 accounts + status always editable regardless of `used`
**Calls (Logic):** F-PG-FN-08 `updatePostingSetup`, F-PG-FN-09, ENG-PG-01

### F-PG-API-14: POST /api/v1/gl/posting-setups/:id/status
Same shape/behavior as F-PG-API-05. **Calls (Logic):** F-PG-FN-11 `changePostingSetupStatus`

### F-PG-API-15: POST /api/v1/gl/posting-setups/bulk-delete
Same shape/behavior as F-PG-API-06. **Calls (Logic):** F-PG-FN-12 `bulkDeletePostingSetups`

### F-PG-API-16 / F-PG-API-17: Import preview / commit
Columns: `bus_group,prod_group,sales_account,purchase_account,cogs_account,status`. Error codes: `REQUIRED`, combination-not-recognized (`bus_group`/`prod_group` not in the current value set — see §0.9/OQ-PG-04), combination-duplicate (R04), account-not-in-COA, `BAD_STATUS`. **Calls (Logic):** F-PG-FN-13, F-PG-FN-14 (shared, `entityType` param — see 03_LOGIC.md)

### F-PG-API-18: GET /api/v1/gl/posting-setups/export
Columns match import template. **Calls (Logic):** F-PG-FN-15 (shared, `entityType` param)

---

## §2.3 Common Concerns

### Idempotency (PR-7)
All create endpoints (`POST /gl/posting-groups`, `POST /gl/posting-setups`, `.../import/commit`) accept `Idempotency-Key`. Server caches result 24h; same key+body → cached response; same key+different body → 409. **Not present in current HTML mock** (client-side array push has no network race) — this is a **backend addition** required because the real API is networked; flagged as `[AI-DEFAULT]` per Lane Mode Phase 2.5 (PR-7 is mandatory for LEAN/STANDARD with mutation per `edge-case-probes.md`).

### Optimistic Locking (PR-2) — `[AI-DEFAULT]`
BRD §10.2 CA-01 ("2 Finance Lead sessions edit the same record simultaneously") is listed as ☐ unconfirmed. Lane Mode default: add `updated_at`/`version` to both tables (see `04_DB.md`) and accept `If-Match` on PUT endpoints, returning 409 `ERR_STALE_DATA` on mismatch. **This is a conservative default, not a BA-confirmed requirement — flagged as Open Question OQ-FRD-07 in `00_OVERVIEW.md`.**

### Multi-Tenant
All endpoints assume `X-Tenant-Id` header per CUBE ERP convention (BRD does not discuss tenancy explicitly; carried as house convention, not contradicted).

### Audit Log
All mutation APIs write to `T_audit_log` (S01-07 Immutable Master Data Log — BRD §16.3 Must-control): actor, action, resource (`T_gl_posting_group:<id>` or `T_gl_posting_setup:<id>`), timestamp, before/after diff.

### Role enforcement (PM-03, `[AI-DEFAULT]`)
BRD §10.2 PM-03 ("non-Finance role calls API directly") is ☐ unconfirmed but is a baseline security requirement regardless — every mutation endpoint above must re-check role server-side (not just hide the button client-side), returning 403 `ERR_INSUFFICIENT_ROLE`. Applied as default because it is standard practice, not a feature-specific judgment call — logged for completeness.

---

## §2.4 API → Logic Trace (Anchor for R8)

> Authoritative source: `03_LOGIC.md` §3.3. Summary only here.

| API | Calls Functions | Calls Engines |
|---|---|---|
| F-PG-API-01 GET posting-groups | FN-04 | — |
| F-PG-API-02 POST posting-groups | FN-01, FN-03 | ENG-PG-01 |
| F-PG-API-03 GET posting-groups/:id | FN-04 | — |
| F-PG-API-04 PUT posting-groups/:id | FN-02, FN-03 | ENG-PG-01 |
| F-PG-API-05 POST posting-groups/:id/status | FN-05 | — |
| F-PG-API-06 POST posting-groups/bulk-delete | FN-06 | — |
| F-PG-API-07 POST posting-groups/import/preview | FN-13 | ENG-PG-01 |
| F-PG-API-08 POST posting-groups/import/commit | FN-14 | — |
| F-PG-API-09 GET posting-groups/export | FN-15 | — |
| F-PG-API-10 GET posting-setups | FN-10 | — |
| F-PG-API-11 POST posting-setups | FN-07, FN-09 | ENG-PG-01 |
| F-PG-API-12 GET posting-setups/:id | FN-10 | — |
| F-PG-API-13 PUT posting-setups/:id | FN-08, FN-09 | ENG-PG-01 |
| F-PG-API-14 POST posting-setups/:id/status | FN-11 | — |
| F-PG-API-15 POST posting-setups/bulk-delete | FN-12 | — |
| F-PG-API-16 POST posting-setups/import/preview | FN-13 | ENG-PG-01 |
| F-PG-API-17 POST posting-setups/import/commit | FN-14 | — |
| F-PG-API-18 GET posting-setups/export | FN-15 | — |
| F-PG-API-19 GET posting-groups?type=product | FN-16 | — |
| F-PG-API-20 GET vat-groups | FN-17 | — |

> **R8 check:** every mutation row has ≥1 Function/Engine. ✅

---

## §2.5 COA Account Sync Contract ⭐ RESOLVES OQ-PG-02

> **This section is this FRD's explicit resolution of BRD §15 OQ-PG-02** ("COA dropdown hardcode 16 accounts — must sync from F-COA-001, filtered leaf+postable+active + type per R02"). Per BRD instruction, this is resolved by writing the real contract here, not by a separate meeting.

### Consumed endpoint (owned by F-COA-001, called by this feature)

| Field | Value |
|---|---|
| **method** | GET |
| **path** | `/api/v1/coa/accounts` |
| **owner** | F-COA-001 (Chart of Accounts) |
| **consumer** | F-PG (this feature) — via `ENG-PG-01 coa-account-resolver`, see `03_LOGIC.md` §3.2 |
| **auth** | service-to-service or forwarded user JWT (same session) |

**Query params (mandatory filter set, per R01/R02):**
| Param | Value | Reason |
|---|---|---|
| `is_leaf` | `true` | R01 — only leaf accounts are postable candidates |
| `is_postable` | `true` | R01 — parent/header accounts excluded even if leaf |
| `status` | `active` | R01 — inactive COA accounts excluded from all dropdowns |
| `type` | one or more of `asset`\|`liability`\|`equity`\|`income`\|`expense` | R02 — see type-filter map below |

**Response 200:**
```json
{
  "data": [
    { "code": "2-1-10-01", "name": "เจ้าหนี้การค้า", "type": "liability", "is_leaf": true, "is_postable": true, "status": "active" }
  ]
}
```

### Account-type filter map (R02 — per field, resolved from BRD assumption §3.3 + confirmed by HTML as-built filter sets)

| Entity.field | kind/context | `type` filter sent to COA | Source |
|---|---|---|---|
| `GL_Posting_Group.account_1` | kind=`vendor` (AP control) | `liability` | BRD R02: AP=liability |
| `GL_Posting_Group.account_2` | kind=`vendor` (Input VAT) | `asset` | BRD R02: input-VAT=asset |
| `GL_Posting_Group.account_1` | kind=`inventory` | `asset` | BRD R02: inventory=asset |
| `GL_Posting_Group.account_2` | kind=`inventory` (Interim GR/IR) | `asset, liability` | **As-built HTML observation** (`acctSelect('interim_acct', ..., ['asset','liability'])`) — broader than the BRD's single-type assumption because a GR/IR clearing account can sit on either side depending on org convention. Per Mode A (HTML is de facto), this dual-type filter is kept; **not a contradiction of R02**, just an accounting nuance R02's plain-English summary didn't spell out. Not blocking — noted for BA awareness. |
| `GL_Posting_Group.account_1` | kind=`bank` | `asset` | BRD R02: bank=asset |
| `GL_Posting_Group.account_1` | kind=`customer` (AR control) | `asset` | BRD R02: AR=asset |
| `GL_Posting_Group.account_2` | kind=`customer` (Output VAT) | `liability` | BRD R02: output-VAT=liability |
| `GL_Posting_Setup.sales_account` | — | `income` | BRD R02: sales=revenue |
| `GL_Posting_Setup.purchase_account` | — | `expense, asset` | **As-built HTML observation** (`acctSelect('purchase_acct', ..., ['expense','asset'])`) — broader than BRD's single-type "purchase=expense" assumption, allowing a purchase to post to an asset account (e.g. capitalized purchase). Kept per Mode A; flagged for BA awareness, not blocking. |
| `GL_Posting_Setup.cogs_account` | — | `expense` | BRD R02: COGS=expense |

### Migration path (mock → real)
1. **Current (as-built HTML):** hardcoded `COA_ACCOUNTS` array of 16 mock accounts, client-side filter by `type`.
2. **This FRD's target:** `ENG-PG-01` calls the real `GET /api/v1/coa/accounts` contract above at dropdown-open time (create/edit forms) and at import-validation time (row-level account check), server-side.
3. **Backward-compat requirement:** response shape (`code`, `name`, `type`) matches the mock's `{code, name, type}` shape 1:1 so the frontend dropdown rendering (`acctSelect()`/`searchDropdown()`) needs **no UI change** — only the data source swaps.
4. **Rollout gate:** this feature must not go to production with the mock still wired — OQ-PG-03's launch-blocker note in `00_OVERVIEW.md` applies to `used` sync, but this contract (§2.5) is the concrete deliverable that unblocks OQ-PG-02 specifically; dev must confirm F-COA-001's endpoint is live before cutover.

---

## §2.6 Cross-Module Contract — Served to Item Master (F-PDM)

> From BRD §12.1 Downstream Impact Map — these are contracts **this feature serves**, not consumes.

| Downstream | Endpoint | Contract | Trigger | Payload | Status |
|---|---|---|---|---|---|
| Item Master (F-PDM) | `GET /api/v1/gl/posting-groups?type=product` (F-PG-API-19) | Returns the current `prod_group` value set from `T_gl_posting_setup` (distinct `prod_group` values + their status) | Item create/edit screen loads product-posting-group dropdown | `{ "data": [{"value":"GOODS","label":"GOODS"},{"value":"SERVICE","label":"SERVICE"}] }` | **Contract declared, data NOT yet synced to Item's real value set — blocked on OQ-PG-04** (Item expects 6 values: FINISHED/RAWMAT/PACKAGING/SERVICE/TRADE/EXPENSE; this feature currently only has 2: GOODS/SERVICE) |
| Item Master (F-PDM) | `GET /api/v1/gl/vat-groups` (F-PG-API-20) | Returns VAT group values for Item's tax-group dropdown | Item create/edit screen loads VAT-group dropdown | `{ "data": [] }` (empty — no VAT Posting Setup entity exists yet) | **Stub only — returns empty array + `"gap": "OQ-PG-01 not yet resolved, no VAT Posting Setup entity exists"` in response meta. Blocked on OQ-PG-01.** |

- **Compensating behavior if F-PG-API-19/20 return mismatched/empty data:** Item Master must treat both as "not yet authoritative" and not hard-fail; this is explicitly the gap BRD documents (OQ-PG-04, OQ-PG-01) — not a bug in this feature.
- Cross-module test cases: see `06_TESTS.md` §6.9 XT-01, XT-02.

---

## §2.7 Cross-Module Contract — Consumed by GL / Journal Engine (out of scope, BR-08)

> This feature does **not** post to GL. The GL/Journal Engine (a separate, out-of-scope module) resolves accounts at document-posting time by **reading** this feature's data. This section declares the contract that engine depends on, for its implementers' benefit — **no code in this FRD implements the GL/Journal Engine side.**

| Consumer | What it reads | Trigger | Resolution logic (declared, not implemented here) |
|---|---|---|---|
| GL / Journal Engine | `T_gl_posting_group` row by `code` (soft-ref from Vendor/Customer/Bank master, not built yet) | AP/AR Invoice, Payment, GRN posted | Resolve `code` → `account_1`/`account_2` per the document's line type. If `code` not found or `status != 'active'` → posting fails at GL (by design — BR-06). |
| GL / Journal Engine | `T_gl_posting_setup` row by `(bus_group, prod_group)` | Sales/Purchase document posted | Resolve combination → `sales_account`/`purchase_account`/`cogs_account`. Same failure mode as above if combination inactive/missing. |
| GL / Journal Engine | `used` counter (**currently mock, OQ-PG-03**) | Every successful post through a mapping | Increments `used` on the resolved row — **this increment mechanism is itself out of scope of this FRD** (declared here so the GL Engine team knows they own writing to this column once real integration begins) |

- **Compensating event on edit:** editing `account_1`/`account_2`/accounts on a `used>0` row (allowed per IR-PG-01) takes effect only for **new** postings going forward; already-posted journal lines are never touched (no retroactive re-resolve — confirmed BRD §5.2.2).
- **Compensating event on status→inactive:** GL Engine's resolve step must exclude non-`active` rows (BR-06) — new documents referencing an inactive mapping fail at GL, by design.
- Cross-module test cases: see `06_TESTS.md` §6.9 XT-03.
