# 03_LOGIC — F-VENDOR-PRICELIST-001 Vendor Price List

> **Audience:** Backend developer / Architect  
> **Boundary:** no HTTP request/response concepts in Functions or Engines

---

## §3.1 Functions (Scope-Local)

### FN-01 `buildPriceListQuery`

- Input: tenant/company scope, permission context, filters/sort/pagination.
- Output: permission-safe list rows + totals.
- Reads Header/current Version/Tier; applies Confidential projection and allowed-action flags.
- Invoked by API-01; errors invalid filter/sort.

### FN-02 `getPriceListDetail`

- Input: scope, `header_id`, permission context.
- Output: Header + current/pending/version timeline + approval/audit summary.
- Reads all four owned tables; applies pricing gate. Invoked by API-02.

### FN-03 `createPriceDraft`

- Input: authenticated scope/actor + draft DTO.
- Calls FN-04 and ENG-01; inserts Header, v1 draft, tiers and WORM event atomically.
- Output: draft aggregate. Invoked by API-03.
- Errors: duplicate header, invalid master/UOM/price/tier/date.

### FN-04 `validatePriceDraft`

- Input: scope + vendor/product/UOM/currency + effective range + tiers.
- Re-fetches F-VENDOR and Product Master by UUID; validates active/purchasable/UOM, uniqueness, tier shape, price/date and overlap.
- Calls ENG-01 for calculation trace and normalized landed cost.
- Output: normalized snapshots, tiers, trace or structured field errors.
- Invoked by APIs 03/04/05/07/09.

### FN-05 `submitPriceForApproval`

- Input: mutable version, actor, final reason, idempotency context.
- Calls FN-04, FN-12 and ENG-01; derives absolute landed-cost change, requests DOA route, sets pending, appends history/outbox.
- Every create/version becomes pending regardless of threshold; threshold only selects DOA tier.
- Invoked by APIs 05/07/10. Errors one-pending, no route, stale state, invalid master/overlap.

### FN-06 `decidePriceApproval`

- Input: pending version, decision actor, approve/reject, reason, current policy decision reference.
- Rechecks role, current step, SoD, state/version and master eligibility.
- Approve: calls ENG-01, prevents overlap, activates version/supersedes prior applicable version, updates Header, appends history/outbox.
- Reject: records decision/history and returns editable UI state as draft without erasing rejection audit.
- Invoked by API-06.

### FN-07 `createPriceVersion`

- Input: Active Header identity, price/effective/tier content, reason, optional submit.
- Rejects identity changes and existing pending version; allocates sequential `version_no` under lock.
- Calls FN-04 and optional FN-05. Invoked by API-07.

### FN-08 `validateBatchRows`

- Input: batch/import rows + mode + scope.
- Ignores fully blank rows; assigns stable row IDs; calls FN-04 per started row; classifies duplicate/external-ID outcome.
- Output: normalized preview + signed/short-lived validation token; no price mutation.
- Invoked by APIs 09/11.

### FN-09 `commitBatchRows`

- Input: unexpired validation token + accepted rows + actor.
- Revalidates master/config versions captured in token; atomically creates drafts and calls FN-05 for each.
- Any changed-invalid row aborts whole commit with row errors; idempotency prevents duplicates.
- Invoked by APIs 10/12.

### FN-10 `previewPriceImport`

- Input: CSV bytes, declared mode, actor permission.
- Validates encoding/header/version/size, parses cells without spreadsheet formula execution, normalizes external IDs and calls FN-08.
- Output: preview token, counts and visible rows. Invoked by API-11.

### FN-11 `commitPriceImport`

- Input: preview token.
- Applies mode semantics: merge creates/version-matches; replace-unused only draft/pending; identical fingerprint skips.
- Calls FN-09; output counts + IDs. Invoked by API-12.

### FN-12 `resolveApprovalRoute`

- Input: scope, landed cost before/after, change percentage, requester, effective date, current DOA config.
- Output: route/tier, threshold/config version, SLA/escalation snapshot or `BR_DOA_ROUTE_NOT_FOUND`.
- Does not auto-approve any version. Invoked by FN-05/FN-06.

### FN-13 `changeHeaderAvailability`

- Input: Header, activate/deactivate, actor, reason.
- Deactivate changes availability only. Activate re-fetches Vendor/Product, validates UOM and no active ambiguity, then updates version/History/event.
- Invoked by API-08.

### FN-14 `buildVendorPriceSummary`

- Input: tenant/company, `vendor_id`, permission scope.
- Output: VPL-owned counts/product summary for Vendor façade; no duplicated Vendor-side persistence.
- Invoked by API-15.

### FN-15 `getPriceListRefs`

- Input: scope, current date, permission.
- Reads policy/tax/currency reference services; returns ETag/config version. Invoked by API-16.

### FN-16 `buildImportTemplate`

- Input: current import schema version and locale.
- Output: UTF-8 CSV template bytes + filename metadata. Invoked by API-17.

### FN-17 `updatePriceDraft`

- Input: draft aggregate, replacement DTO, expected version, actor.
- Calls FN-04; replaces mutable Header/version/tier fields, increments optimistic version and appends diff history.
- Cannot update Active content. Invoked by API-04.

### FN-18 `comparePriceLists`

- Input: scope, product, qty, date, target currency, permission.
- Loads eligible candidate versions + dated FX; calls ENG-02; excludes candidates with explicit ineligibility reasons.
- Output sorted ascending with rank/best marker and trace. Invoked by API-13.

### FN-19 `resolveVendorPrice`

- Input: explicit vendor/product/UOM/currency/qty/date/scope and transaction context.
- Revalidates Vendor/Product state, loads applicable candidates and calls ENG-02 in single-vendor mode.
- Requires exactly one answer and returns immutable calculation snapshot. Invoked by API-14.

All full IDs are `F-VENDOR-PRICELIST-001-FN-NN`.

## §3.2 Engines (CUBIC Candidates)

### F-VENDOR-PRICELIST-001-ENG-01: `landed-unit-cost-engine` [NEW]

| Field | Value |
|---|---|
| Category | financial-calculation |
| Status | DRAFT; register at dev handoff |
| Owner | F-VENDOR-PRICELIST-001 / candidate shared |
| Stateless / pure / deterministic | true / true / true |

**Input schema:**

```json
{
  "price": 184.5,
  "price_per": 1,
  "discount_pct": 2,
  "freight_per_unit": 1.2,
  "source_currency": "THB",
  "target_currency": "THB",
  "fx_rate": 1,
  "formula_version": "v1"
}
```

**Output schema:**

```json
{
  "base_unit_price": 184.5,
  "discount_amount": 3.69,
  "landed_unit_cost_ex_tax_source": 182.01,
  "landed_unit_cost_target": 182.01,
  "trace": {"formula_version":"v1","rounding_stage":"final"}
}
```

**Algorithm:** validate positive price/price_per and bounded discount/freight → calculate `(price/price_per)*(1-discount/100)+freight` → reject negative result → apply supplied dated FX → round only at configured final precision → return full trace. Tax is excluded from landed result.

**Errors:** `ENG_ERR_INVALID_INPUT`, `ENG_ERR_NEGATIVE_NET_COST`, `ENG_ERR_FX_REQUIRED`. No DB/HTTP/file I/O.

**Reuse:** threshold calculation, compare, resolve and downstream PR/RFQ/PO verification.

### F-VENDOR-PRICELIST-001-ENG-02: `vendor-price-resolution-engine` [NEW]

| Field | Value |
|---|---|
| Category | matcher |
| Status | DRAFT; register at dev handoff |
| Owner | F-VENDOR-PRICELIST-001 / candidate shared |
| Stateless / pure / deterministic | true / true / true |

**Input:** resolution scope, explicit optional vendor, product/UOM/currency, qty/date, candidates with Header/Version/Tiers/vendor/product eligibility, dated FX records, source-precedence records and formula/config versions.

**Output:** eligible results sorted by landed target cost, excluded candidates with reason codes, selected result for explicit-vendor mode, and complete trace.

**Algorithm:**

1. Filter exact tenant/company and site precedence; match product/UOM/currency and optional explicit vendor.
2. Exclude non-active Vendor/Product/Header/Version and out-of-date versions.
3. Select exactly one tier whose range contains qty; ambiguity is an error.
4. Apply source precedence Contract > VPL > authorized override when such external candidates are supplied.
5. Call ENG-01 per eligible candidate with dated/fresh FX.
6. Sort compare output ascending; deterministic tie-breaker is vendor code then version ID.
7. Single-vendor resolve requires exactly one winner and returns its snapshot; never selects a vendor on behalf of PO.

**Errors:** `ENG_ERR_AMBIGUOUS_PRICE`, `ENG_ERR_NO_APPLICABLE_PRICE`, `ENG_ERR_FX_REQUIRED`, `ENG_ERR_INVALID_TIER`. No direct I/O.

**Reuse:** VPL compare/resolve, PR/RFQ/PO pricing and future purchase planning.

## §3.3 API ↔ Logic Trace (R8 Anchor)

| API | Method | Functions | Engines |
|---|---|---|---|
| API-01 | GET | FN-01 | — |
| API-02 | GET | FN-02 | — |
| API-03 | POST | FN-03 → FN-04 | ENG-01 |
| API-04 | PATCH | FN-17 → FN-04 | ENG-01 |
| API-05 | POST | FN-05 → FN-04,FN-12 | ENG-01 |
| API-06 | POST | FN-06 → FN-12 | ENG-01 |
| API-07 | POST | FN-07 → FN-04,(FN-05) | ENG-01 |
| API-08 | POST | FN-13 | — |
| API-09 | POST | FN-08 → FN-04 | ENG-01 |
| API-10 | POST | FN-09 → FN-05 | ENG-01 |
| API-11 | POST | FN-10 → FN-08 | ENG-01 |
| API-12 | POST | FN-11 → FN-09 | ENG-01 |
| API-13 | POST | FN-18 | ENG-02 → ENG-01 |
| API-14 | POST | FN-19 | ENG-02 → ENG-01 |
| API-15 | GET | FN-14 | — |
| API-16 | GET | FN-15 | — |
| API-17 | GET | FN-16 | — |

**Verification:** 10/10 mutation APIs have Function trace; FN-01..19 are all invoked; ENG-01/02 are traced; no business logic is hidden in API contracts.

## §3.4 External Dependencies

- F-VENDOR read service and lifecycle event; canonical source is `outputs/F-VENDOR/_final-docs`.
- Product Master read service and status/UOM data; canonical source is `Related context/Item Master`.
- Policy Center DOA route/config/SLA service.
- FX Master dated-rate service and Finance Posting Setup tax references.
- Central audit/outbox/idempotency services.

## §3.5 Logic Decisions

- LD-02: every new/version needs approval; threshold only changes route.
- LD-05: Active identity is immutable; UOM/currency change creates a new Header.
- LD-08: compare/resolve share ENG-02 and calculation trace; UI never duplicates formula authority.
- Engine global UUIDs remain OQ-01 until CUBIC registration.
