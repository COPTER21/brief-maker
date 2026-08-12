# 05_RULES — F-BOM-001 สูตรการผลิต (Bill of Materials)

> **Audience:** Backend + QA  
> Declarative source for business rules, lifecycle, validation, edges, errors, permissions and security.

---

## §5.1 Business Rules

| ID | Statement | Enforcement | Error/Result |
|---|---|---|---|
| BR-01 | one FG may have many versions; `(tenant,parent,version normalized)` is unique | FN-05 + DB unique | `BR_BOM_VERSION_DUPLICATE` |
| BR-02 | one FG has at most one default and a default must be active | FN-08 + DB checks/index | clear old default or reject conflict |
| BR-03 | parent must be current active Item type FG at mutation | FN-05 | `BR_BOM_PARENT_INVALID` |
| BR-04 | component must be current active Item type RM/PM/TR at mutation | FN-05 | `BR_BOM_COMPONENT_INVALID` |
| BR-05 | BOM is single-level; component cannot equal parent or be FG | FN-05 | `BR_BOM_SELF_COMPONENT`, `BR_BOM_COMPONENT_INVALID` |
| BR-06 | line UoM must be active and in component base-UoM category | FN-05 | `BR_BOM_UOM_INVALID` |
| BR-07 | cost = Σ(`standard_cost×qty×(1+scrap_pct/100)`), decimal only | ENG-01 | `ENG_BOM_COST_INVALID_INPUT` |
| BR-08 | no approval; `draft/active/inactive` transition in every direction | FN-06 | success if authorized/current |
| BR-09 | standard/derived cost is read-only Confidential Item data | policy + ENG-01 | masked/default deny |
| BR-10 | exactly three statuses: `draft`, `active`, `inactive` | FN-05/FN-06 + DB | `BR_BOM_STATUS_INVALID` |
| BR-11 | `[AI-DEFAULT]` BOM with current MO reference cannot be deleted; bulk skips it | FN-07 | `BR_BOM_IN_USE` |
| BR-12 | `[AI-DEFAULT]` referenced BOM may be amended; old MO snapshot remains unchanged | FN-04 + MO contract | no retroactive update |
| BR-13 | import/export CSV is not supported | route/scope guard | no endpoint/control |
| BR-14 | `[AI-DEFAULT]` `scrap_pct` 0..100 inclusive; 100 doubles effective qty | FN-05 + DB | `BR_BOM_NUMERIC_RANGE` |
| BR-15 | `[AI-DEFAULT]` deactivated master remains readable; a new save must revalidate and rejects inactive selection | FN-05 | `BR_BOM_MASTER_INACTIVE` |

## §5.2 State Machine

```text
create ──บันทึกร่าง────────────> draft
create ──บันทึก + เปิดใช้งาน──> active
draft <───────────────────────> active
draft <───────────────────────> inactive
active <──────────────────────> inactive
```

| From | To | Role | Side effect |
|---|---|---|---|
| create | draft | Planner | force `is_default=false` |
| create | active | Planner | set/retain requested default atomically |
| draft | active/inactive | Planner | default false unless explicitly setting active default |
| active | draft/inactive | Planner | force `is_default=false` |
| inactive | draft/active | Planner | default false unless explicitly setting active default |

No submit/approve/reject state exists. `eff_from` does not trigger an automatic transition.

## §5.3 Permission Matrix

| Role | List/detail | Create/edit | Status/default | Delete | Cost | Audit history |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| Planner | ✓ | ✓ | ✓ | eligible only | policy grant | ✓ |
| Production | active via API-07 | — | — | — | — | — |
| Costing | ✓ | — | — | — | ✓ | optional policy grant |
| Auditor | ✓ | — | — | — | masked by default | ✓ |

Exact platform role identifiers are not found in the conversation; implementation maps these capability names through centralized authorization. Permission is rechecked at mutation time and per bulk record.

## §5.4 Validation Rules

| ID | Condition | Visible microcopy / API code |
|---|---|---|
| VR-01 | `parent_code` empty | `เลือกสินค้าผลผลิตก่อน` / `BR_BOM_PARENT_REQUIRED` |
| VR-02a | version empty after trim | `ระบุเวอร์ชันสูตร (เช่น v1)` / `BR_BOM_VERSION_REQUIRED` |
| VR-02b | normalized parent+version exists excluding current ID | `เวอร์ชัน ${f.ver} ของสินค้านี้มีอยู่แล้ว` / `BR_BOM_VERSION_DUPLICATE` |
| VR-03 | name empty after trim | `ระบุชื่อสูตร` / `BR_BOM_NAME_REQUIRED` |
| VR-04 | no component line | `ต้องมีส่วนประกอบอย่างน้อย 1 รายการ` / `BR_BOM_LINE_REQUIRED` |
| VR-05 | qty ≤0 or exceeds numeric range | `ปริมาณของ ${l.item} ต้องมากกว่า 0` / `BR_BOM_NUMERIC_RANGE` |
| VR-06 | duplicate component code | `วัตถุดิบ ${l.item} ซ้ำ — รวมเป็นรายการเดียว` / `BR_BOM_COMPONENT_DUPLICATE` |
| VR-07 | component equals parent | `ส่วนประกอบห้ามเป็นตัวสินค้าเอง (${l.item}) — กัน BOM วน` / `BR_BOM_SELF_COMPONENT` |
| VR-08 | UoM inactive/wrong category | UI must not offer it / `BR_BOM_UOM_INVALID` |

Additional server validation: `out_qty>0`, scrap 0..100, maximum 500 lines `[AI-DEFAULT]`, maximum safe decimal bounds, valid date, unique line number, no client-supplied cost/code/audit/usage.

## §5.5 Edge Cases

| ID | Scenario | Resolution | Test |
|---|---|---|---|
| EC-01 | set a new default for same FG | one transaction clears old then sets new; unique partial index settles race | TC-EC-01 |
| EC-02 | version differs only by case/normalization | block as duplicate | TC-EC-02 |
| EC-03 | component repeats in separate lines | block; do not silently merge | TC-EC-03 |
| EC-04 | component equals parent | block | TC-EC-04 |
| EC-05 | component changed | clear/reselect UoM within new category | TC-EC-05 |
| EC-06 | active default leaves active | clear default in same transaction | TC-EC-06 |
| EC-07 | bulk delete mixes used/unused | delete eligible, skip used, return ledger | TC-EC-07 |
| EC-08 | standard cost null/zero | provisional zero contribution + `has_missing_cost`; cost never editable | TC-EC-08 |
| EC-09 | scrap=100 | allow and calculate effective quantity ×2 | TC-EC-09 |
| EC-10 | Item/UoM deactivated after activation | detail readable; next save rejects inactive master under provisional rule | TC-EC-10 |
| EC-AI-01 | two planners edit same BOM | optimistic lock; second gets `ERR_STALE_DATA` | TC-CC-01 |
| EC-AI-02 | concurrent bulk status/edit | transaction per record + version ledger | TC-CC-02 |
| EC-AI-03 | Item display changes | show current name/image but persist stable code | TC-DI-01 |
| EC-AI-04 | UoM deactivated | exclude from new picker; existing line flagged until corrected on save | TC-DI-02 |
| EC-AI-05 | numeric overflow | reject meaningful range error | TC-NUM-01 |
| EC-AI-06 | rounding drift | decimal scale/mode from ENG-01 everywhere | TC-NUM-02 |
| EC-AI-07 | client sends draft+default | persist draft+false | TC-STATE-01 |
| EC-AI-08 | caller lacks cost permission | mask across list/detail/form and exclude MO contract | TC-SEC-01 |
| EC-AI-09 | mixed bulk authorization | skip forbidden record, audit result, process permitted records | TC-SEC-02 |

## §5.6 Error Catalog

| Code | HTTP | Cause |
|---|---:|---|
| `ERR_INVALID_QUERY_PARAMS` | 400 | unsupported/malformed query |
| `ERR_VALIDATION_FAILED` | 400 | malformed body envelope |
| `ERR_NOT_AUTHENTICATED` | 401 | no valid authenticated context |
| `ERR_INSUFFICIENT_ROLE` | 403 | capability denied or revoked |
| `ERR_BOM_NOT_FOUND` | 404 | BOM absent in tenant scope |
| `ERR_ACTIVE_BOM_NOT_FOUND` | 404 | no active BOM for requested FG |
| `ERR_IDEMPOTENCY_CONFLICT` | 409 | same key, different normalized request |
| `ERR_STALE_DATA` | 409 | optimistic version mismatch |
| `BR_BOM_VERSION_DUPLICATE` | 409 | normalized version already exists |
| `BR_BOM_PARENT_REQUIRED` | 422 | parent empty |
| `BR_BOM_PARENT_INVALID` | 422 | parent not active FG |
| `BR_BOM_VERSION_REQUIRED` | 422 | version empty |
| `BR_BOM_NAME_REQUIRED` | 422 | name empty |
| `BR_BOM_LINE_REQUIRED` | 422 | no line |
| `BR_BOM_COMPONENT_INVALID` | 422 | component type/status invalid |
| `BR_BOM_COMPONENT_DUPLICATE` | 422 | component repeats |
| `BR_BOM_SELF_COMPONENT` | 422 | component equals parent |
| `BR_BOM_UOM_INVALID` | 422 | UoM inactive/category mismatch |
| `BR_BOM_NUMERIC_RANGE` | 422 | quantity/scrap/decimal out of bounds |
| `BR_BOM_STATUS_INVALID` | 422 | unknown target status |
| `BR_BOM_IN_USE` | 422 per result | MO reference blocks delete |
| `ERR_MASTER_DATA_UNAVAILABLE` | 503 | required Item/UoM validation unavailable |
| `ENG_BOM_COST_INVALID_INPUT` | 500 | internal engine contract mismatch |

Client-facing responses use stable codes and safe messages; no raw SQL, policy internals, stack trace, secret, token, cookie, or upstream credential.

## §5.7 Security Bible — P3 Master Data

| Control | Application |
|---|---|
| S01-04 SoD Conflict Matrix | centralized capabilities separate master mutation, cost access, and audit review |
| S01-07 Immutable Master Data Log | append before/after for header, line, status, default, delete |
| S02-01 Password Policy | shared identity platform; no feature credential store |
| S02-04 Data Masking | default-deny `standard_cost`/derived costs |
| S02-05 Classification Tags | field coverage in `04_DB.md` §4.6 |
| S03-02 Policy Versioning | status/default/rule contract versioned with release |
| S04-05 Master Data Mapping | Item/UoM adapter mapping and contract tests |
| S06-03 Standardized Audit Content | Who, What, When, Where, Result + sanitized diff |
| S07-06 PII Tagging | no BOM PII; actor ID remains Confidential |
| S11-02 Ticket Enforcement | production master mutation captures `change_ref` where platform mandates |
| S14-02 Payload Schema Validation | server validates envelope and VR-01..08 |

Additional protections: tenant RLS, object-scope authorization, optimistic locking, rate limiting via shared API policy, parameterized SQL, output encoding, and audit of protected cost access.

## §5.8 Idempotency, Network Failure, and Partial Bulk

- mutation result cache TTL 24h `[AI-DEFAULT]`
- retry after lost response uses the same key and returns the same result without duplicate audit rows
- bulk uses per-record transaction and a stable ledger; request envelope failure affects all, record failure affects only that record
- repeating a completed bulk request with the same key returns the same ledger, even if later data state differs

## §5.9 AI-Default Register

| ID | Default | Change impact |
|---|---|---|
| AID-01 | allow amend when used; MO snapshot immutable | may change edit guard/API behavior |
| AID-02 | block delete when used | may change lifecycle/data retention |
| AID-03 | null cost contributes zero with visible missing-cost flag | may become warn/block policy |
| AID-04 | scrap 100 inclusive | may tighten validation |
| AID-05 | master deactivation blocks next save, not read | may require grandfathering policy |
| AID-06 | idempotency 24h, max bulk 100, max lines 500 | operational configuration |
| AID-07 | decimal response scale 6, HALF_UP | affects cost comparison/display |
| AID-08 | audit failure fails mutation closed | affects availability/control trade-off |
| AID-09 | audit retention minimum 7 years | must align central policy |
| AID-10 | internal `BOM-` sequence | may change code presentation/migration |

## §5.10 Compliance and Scope Guard

COSO, ISO/IEC 27001, NIST CSF, COBIT, CIS, NIST SP 800-53, SOC 2, ISO 22301, and OWASP API concerns are addressed through access, classification, immutable evidence, tenant isolation, schema validation, concurrency and recovery tests. No PII, AI decision, OT link, payment, approval, notification, inventory posting or accounting posting exists in this feature scope.

