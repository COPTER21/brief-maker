# 02_API — F-VENDOR-PRICELIST-001 Vendor Price List

> **Audience:** Backend developer (HTTP layer)  
> **Iron rule:** business logic lives in `03_LOGIC.md`; every mutation traces to at least one Function/Engine.

---

## §2.1 API Overview

| ID | Method | Path | Summary |
|---|---|---|---|
| API-01 | GET | `/api/v1/vendor-price-lists` | list/filter/sort/paginate |
| API-02 | GET | `/api/v1/vendor-price-lists/:header_id` | header + versions + approval/audit detail |
| API-03 | POST | `/api/v1/vendor-price-lists` | create draft header/version |
| API-04 | PATCH | `/api/v1/vendor-price-lists/:header_id/draft` | amend draft identity/price |
| API-05 | POST | `/api/v1/vendor-price-lists/:header_id/submit` | submit draft for approval |
| API-06 | POST | `/api/v1/vendor-price-lists/:header_id/approval-decisions` | approve or reject pending version |
| API-07 | POST | `/api/v1/vendor-price-lists/:header_id/versions` | create draft/new pending version from Active header |
| API-08 | POST | `/api/v1/vendor-price-lists/:header_id/availability-actions` | deactivate/reactivate header |
| API-09 | POST | `/api/v1/vendor-price-lists/batch/validate` | validate batch rows |
| API-10 | POST | `/api/v1/vendor-price-lists/batch/commit` | commit validated batch as pending |
| API-11 | POST | `/api/v1/vendor-price-lists/imports/preview` | parse + validate CSV preview |
| API-12 | POST | `/api/v1/vendor-price-lists/imports/commit` | commit preview token |
| API-13 | POST | `/api/v1/vendor-price-lists/compare` | compare active vendor prices |
| API-14 | POST | `/api/v1/vendor-price-lists/resolve` | resolve specified vendor price for transaction |
| API-15 | GET | `/api/v1/vendor-price-lists/vendor-summary/:vendor_id` | VPL-owned summary for F-VENDOR API-20 |
| API-16 | GET | `/api/v1/vendor-price-lists/refs` | policy/tax/currency UI references |
| API-17 | GET | `/api/v1/vendor-price-lists/imports/template` | current CSV template |

Full IDs use `F-VENDOR-PRICELIST-001-API-NN`; short `API-NN` below is pack-local notation.

## §2.2 Common Contract

- Auth: `Authorization: Bearer`; `X-Tenant-Id` required by platform. `company_id` and optional `site_id` derive from authorized session context, not request authority.
- Mutations require `Idempotency-Key`; updates/state decisions also require `If-Match` with current entity version.
- Same idempotency key + same canonical body returns stored outcome; same key + different body returns 409.
- Pricing response fields require `canSeePricing`; unauthorized calls receive a permission-safe shape with values omitted/masked and never raw values in logs.
- Standard envelope: `{data, meta, correlation_id}`; errors: `{error:{code,message_key,field?,details?},correlation_id}`.
- Role is rechecked at mutation time. Tenant/company RLS applies to all queries.

## §2.3 Read Contracts

### F-VENDOR-PRICELIST-001-API-01: GET /api/v1/vendor-price-lists

| Field | Contract |
|---|---|
| Roles | authenticated; pricing gated |
| Query | `search`, `status`, `view=flat|vendor`, `vendor_id`, `product_id`, `sort_by`, `sort_dir`, `page`, `page_size` |
| Response | list rows include header/version IDs, full vendor/product snapshot codes/names, UOM, currency, effective range, version number, state and allowed actions |
| Errors | 400 invalid query; 401; 403 |
| Calls | FN-01 `buildPriceListQuery` |

### F-VENDOR-PRICELIST-001-API-02: GET /api/v1/vendor-price-lists/:header_id

Returns header, current/pending version, immutable version timeline, tiers, calculation trace, requester/approver audit and server-derived capabilities. Confidential fields follow pricing gate. 404 `ERR_VPL_NOT_FOUND`. Calls FN-02 `getPriceListDetail`.

### F-VENDOR-PRICELIST-001-API-15: GET /api/v1/vendor-price-lists/vendor-summary/:vendor_id

Internal/read-only contract used by F-VENDOR API-20. Returns `{vendor_id,total_headers,active_count,pending_count,inactive_count,products:[{product_id,product_code_snapshot,buy_uom,currency_code,status}]}` with price values omitted unless caller has pricing scope. No data returns empty counts, not fabricated rows. Calls FN-14 `buildVendorPriceSummary`.

### F-VENDOR-PRICELIST-001-API-16: GET /api/v1/vendor-price-lists/refs

Returns allowed currencies/tax codes, current approval threshold display, SLA display and config version. Vendor/Product picker records are read from their owning APIs, not duplicated in this payload. Calls FN-15 `getPriceListRefs`.

### F-VENDOR-PRICELIST-001-API-17: GET /api/v1/vendor-price-lists/imports/template

Returns UTF-8 CSV with versioned column header contract and content-disposition filename. No price data is included. Calls FN-16 `buildImportTemplate`.

## §2.4 Single Entry / Version Contracts

### F-VENDOR-PRICELIST-001-API-03: POST /api/v1/vendor-price-lists

**Roles:** canManage. **Body:**

```json
{
  "vendor_id": "uuid",
  "product_id": "uuid",
  "buy_uom": "KG",
  "currency_code": "THB",
  "vendor_item_code": null,
  "external_id": null,
  "price_type": "flat",
  "effective_from": "2026-08-01",
  "effective_to": null,
  "reason": "ราคาเสนอฉบับใหม่",
  "tiers": [{"min_qty":0,"max_qty":null,"price":184.5,"price_per":1,"discount_pct":2,"freight_per_unit":1.2,"tax_code":"VAT7","incl_vat":false}]
}
```

Creates Header inactive + Version v1 draft. Server ignores tenant/company sent by client, re-fetches Vendor/Product and stores snapshots. Response 201. Errors: `BR_VPL_DUPLICATE_HEADER`, `BR_VENDOR_NOT_ACTIVE`, `BR_PRODUCT_NOT_PURCHASABLE`, `BR_UOM_NOT_PURCHASABLE`, validation errors. Calls FN-03 `createPriceDraft` → FN-04 and ENG-01.

### F-VENDOR-PRICELIST-001-API-04: PATCH /api/v1/vendor-price-lists/:header_id/draft

Updates a draft only. Body may change vendor/product/UOM/currency and price fields; all master references are revalidated. Requires `If-Match`. Response 200 with incremented version. Errors: 409 `ERR_STALE_DATA`, 422 invalid state/rules. Calls FN-04 `validatePriceDraft`, FN-17 `updatePriceDraft`, ENG-01.

### F-VENDOR-PRICELIST-001-API-05: POST /api/v1/vendor-price-lists/:header_id/submit

Body `{ "reason":"..." }` (reason may already exist but final value is required). Revalidates master state, uniqueness, tier/date overlap and current policy; resolves DOA and changes draft → pending_approval. Response 200 includes approval request/tier/SLA snapshot. Calls FN-05 `submitPriceForApproval` → FN-04, FN-12, ENG-01.

### F-VENDOR-PRICELIST-001-API-06: POST /api/v1/vendor-price-lists/:header_id/approval-decisions

Body `{ "decision":"approve|reject", "reason":"required-on-reject", "approval_request_id":"uuid" }`. Only current DOA actor may decide; requester cannot approve. Approve activates the version/effective schedule and supersedes prior applicable version transactionally. Reject returns version to draft in the UI contract while preserving rejection event/history. Errors include 403 SoD/route mismatch, 409 already decided/stale, 422 overlap or master invalid. Calls FN-06 `decidePriceApproval` → FN-12, ENG-01.

### F-VENDOR-PRICELIST-001-API-07: POST /api/v1/vendor-price-lists/:header_id/versions

Creates a new version for an Active header. Body contains price/effective/reason/tiers only; vendor/product/UOM/currency are immutable on this path. `submit=true` may create and submit atomically. If UOM/currency changes, client must call API-03 to create a new Header, optionally carrying `source_header_id` for trace. One pending version per Header. Calls FN-07 `createPriceVersion` → FN-04, FN-05 when submit, ENG-01.

### F-VENDOR-PRICELIST-001-API-08: POST /api/v1/vendor-price-lists/:header_id/availability-actions

Body `{ "action":"deactivate|activate", "reason":"optional-by-current-UI" }`. Deactivate excludes Header from resolve/compare without deleting history. Activate revalidates vendor/product/UOM and overlap. Response 200 `{header_id,status,version}`. Calls FN-13 `changeHeaderAvailability`.

## §2.5 Batch & Import

### API-09: POST /api/v1/vendor-price-lists/batch/validate

Body `{rows:[SingleEntryShape...]}`. Returns normalized rows with `row_id`, master UUID/snapshots, field errors, duplicate classification and `validation_token`. No DB price mutation. Blank rows are returned as ignored. Calls FN-08 `validateBatchRows` → FN-04, ENG-01.

### API-10: POST /api/v1/vendor-price-lists/batch/commit

Body `{validation_token,accepted_row_ids}`. Revalidates changed masters/config since preview; accepted request commits atomically as pending_approval versions and creates DOA requests. Returns counts + created IDs. Any row invalid at commit returns 422 row errors and commits none. Calls FN-09 `commitBatchRows` → FN-05.

### API-11: POST /api/v1/vendor-price-lists/imports/preview

Multipart CSV + `mode=merge|replace-unused`. Validates UTF-8/schema/size, stable `external_id`, Vendor/Product/UOM, duplicates and current state. Returns `preview_token`, summary and rows; price values require pricing permission. No price mutation. Calls FN-10 `previewPriceImport` → FN-08.

### API-12: POST /api/v1/vendor-price-lists/imports/commit

Body `{preview_token}`. `merge` creates or versions matching external ID; `replace-unused` can replace only draft/pending rows and skips records already used/active. Revalidation failure rejects the commit. All created/updated rows finish `pending_approval`; identical external ID + fingerprint is a safe skip. Calls FN-11 `commitPriceImport` → FN-09.

## §2.6 Calculation Contracts

### API-13: POST /api/v1/vendor-price-lists/compare

Body `{product_id,qty,price_date,target_currency:"THB",company_id?}`; company comes from context. Returns eligible vendors sorted `landed_unit_cost_target ASC`, `rank`, `is_best`, tier, dated FX, version and calculation trace. Non-active vendors/products/VPL or missing/stale FX are excluded with explicit reason metadata. Calls FN-18 `comparePriceLists` → ENG-02.

### API-14: POST /api/v1/vendor-price-lists/resolve

Service/user roles with pricing scope. Body `{vendor_id,product_id,buy_uom,currency_code,qty,price_date,transaction_type,transaction_id?}`. Returns exactly one applicable price or 422 `NO_APPLICABLE_PRICE` / `BR_PRICE_AMBIGUOUS`. Success includes `header_id`, `price_version_id`, chosen tier, landed ex-tax, currency/FX, policy/formula version and immutable `calculation_snapshot`. It does not choose a vendor. Calls FN-19 `resolveVendorPrice` → ENG-02.

## §2.7 API → Logic Trace

| API | Functions | Engines |
|---|---|---|
| 01 | FN-01 | — |
| 02 | FN-02 | — |
| 03 | FN-03, FN-04 | ENG-01 |
| 04 | FN-17, FN-04 | ENG-01 |
| 05 | FN-05, FN-04, FN-12 | ENG-01 |
| 06 | FN-06, FN-12 | ENG-01 |
| 07 | FN-07, FN-04, optional FN-05 | ENG-01 |
| 08 | FN-13 | — |
| 09 | FN-08, FN-04 | ENG-01 |
| 10 | FN-09, FN-05 | ENG-01 |
| 11 | FN-10, FN-08 | ENG-01 |
| 12 | FN-11, FN-09 | ENG-01 |
| 13 | FN-18 | ENG-02 |
| 14 | FN-19 | ENG-02 |
| 15 | FN-14 | — |
| 16 | FN-15 | — |
| 17 | FN-16 | — |

## §2.8 Cross-Module Contracts

| Module | Direction | Contract | Rule |
|---|---|---|---|
| F-VENDOR | VPL reads | API-01/03 of Vendor + status event | accept only same-tenant active vendor |
| F-VENDOR API-20 | Vendor reads VPL | VPL API-15 | façade only; Vendor stores no price copy |
| Product Master | VPL reads | Products API-01/02 | UUID primary; active+purchasable; buy UOM |
| Policy/DOA | bidirectional | resolve/create/decide approval request | threshold chooses tier; every version still needs approval |
| FX Master | VPL reads | dated/fresh FX | no silent fallback |
| PR/RFQ/PO | consumers call | VPL API-14 | persist returned version + snapshot/trace |

### Events emitted

- `vendor_price_submitted_event {header_id,version_id,approval_request_id,requested_by,requested_at}`
- `vendor_price_approved_event {header_id,version_id,effective_from,approved_by,approved_at}`
- `vendor_price_rejected_event {header_id,version_id,requested_by,rejection_reason}`
- `vendor_price_availability_changed_event {header_id,status,changed_at}`

### Events consumed

- `vendor_status_changed_event`: invalidate cache/picker; non-active vendor is immediately excluded from new submit/import/resolve/compare, while history remains.
- `product_status_changed_event` or equivalent: invalidate product eligibility; non-active/non-purchasable product is excluded from future mutation/resolve/compare.

Each downstream contract has coverage in `06_TESTS.md` §6.9.
