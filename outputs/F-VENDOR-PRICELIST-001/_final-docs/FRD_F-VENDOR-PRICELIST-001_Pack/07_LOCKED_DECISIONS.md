# 07_LOCKED_DECISIONS — F-VENDOR-PRICELIST-001 Vendor Price List

> **Audience:** All roles  
> **Rule:** ถ้า specification ใดขัดกับ Scope Lock ตารางนี้ ให้ Scope Lock ชนะ

---

## §7.0 Scope Lock — Imported from APPROVED BRD v2.4

| LOCK-ID | Confirmation | Status in FRD |
|---|---|---|
| LOCK-VPL-01 | Buy-side Vendor Price List only | applied |
| LOCK-VPL-02 | old HTML/FRD/tests are coverage reference, not authority | applied |
| LOCK-VPL-03 | new price/every Price Version require approval; requester cannot self-approve | applied |
| LOCK-VPL-04 | threshold default 10% is audited config; basis is absolute landed ex-tax change | applied; no production hardcode |
| LOCK-VPL-05 | approval SLA 1 business day; reuse central DOA | applied |
| LOCK-VPL-06 | pricing is Confidential; mask UI/export/log | applied |
| LOCK-VPL-07 | Header key includes tenant/company/site(optional)/vendor/product/UOM/currency; versions immutable | applied |
| LOCK-VPL-08 | Active validity/tier may not resolve to multiple answers | applied |
| LOCK-VPL-09 | PR/RFQ/PO store version + calculation snapshot/trace | applied |
| LOCK-VPL-10 | Compare full page; create/edit drawer; view tabbed drawer; confirm modal | applied |
| LOCK-VPL-11 | Batch/CSV preview, validate, duplicate check, confirm; stable external ID | applied |
| LOCK-VPL-12 | no AVL/contract editor/lead/MOQ/preferred/attachment/OCR/AI recommendation | applied |
| LOCK-VPL-13 | no business A4/PDF document | applied; PDF skill skipped |
| LOCK-VPL-14 | Vendor source = `outputs/F-VENDOR/_final-docs`; old Related context Vendor is historical | applied |
| LOCK-VPL-15 | canonical ID `F-VENDOR-PRICELIST-001`; legacy alias has no separate ownership/schema | applied |
| LOCK-VPL-16 | VPL owns summary/data; Vendor API-20 is read-only façade | applied |
| LOCK-VPL-17 | Product source = `Related context/Item Master`; UUID primary; active+purchasable + purchase UOM | applied |

Scope Lock ref: `../BRD_VendorPriceList_v2.4.md` §1.1, APPROVED.

## §7.1 Locked Decisions

### LD-01: Current HTML is UI source of truth

- **Decision:** `../vendor-price-list-v6.html` governs route, surface, visible label and interaction behavior.
- **Implication:** older `vendor-pricelist/vendor-pricelist.html` is historical comparison only; downstream UI Brief/tests extract from current HTML.

### LD-02: Every create/version is pending approval

- **Context:** BRD S-04 AC1 text said a change not exceeding threshold could apply immediately, while LOCK-VPL-03 and R11 say every version requires approval.
- **Decision:** Scope Lock wins. Below/equal/above threshold all become pending; threshold only resolves normal/elevated DOA tier.
- **Implication:** tests include boundary values and forbid auto-activation.

### LD-03: Company and Site are context, not form fields in this UI

- **Decision:** `company_id` comes from authenticated company context; `site_id=null` is the UI-v1 default.
- **Rationale:** current approved HTML deliberately removed Company/Site inputs while preserving the domain key.
- **Implication:** API ignores client authority for tenant/company; future site selection is an enhancement requiring UI review.

### LD-04: Draft identity editable; Active identity immutable

- Draft edit may change vendor, product, UOM and currency subject to revalidation.
- New version from Active locks all identity fields and shows an explanation.
- UOM/currency change from Active uses `สร้างรายการใหม่จากรายการนี้`, creating a new Header rather than mutating history.

### LD-05: Vendor and Product are searchable master dropdowns

- Vendor search is from canonical F-VENDOR active records.
- Product search is from Product Master active+purchasable records.
- UOM is a dependent dropdown from Product base/default + `can_buy=true`; free-text master identity is forbidden.

### LD-06: Batch/import success always enters approval

- Valid accepted rows are pending_approval, return to the main list and are visible immediately.
- Preview is not a commit; commit is idempotent and atomic for the accepted request.

### LD-07: Header deactivate/reactivate is reversible

- Deactivate is soft and excludes resolve/compare.
- Reactivate revalidates Vendor/Product/UOM/overlap and preserves all history.

### LD-08: Shared calculation and resolution engines

- Landed calculation and candidate resolution are pure Engines; compare and resolve cannot implement separate formulas.
- Compare sorts low→high and marks the first result as best; resolve receives explicit vendor and never chooses one silently.

### LD-09: Price Version and calculation trace use human-facing labels

- UI shows `ราคาฉบับที่ N`, `รหัสอ้างอิง`, and plain-language explanation rather than internal terms such as `Price Version vN · Calculation Trace`.
- Technical IDs remain in API/DB for traceability.

### LD-10: Optimistic concurrency + idempotent mutation

- `If-Match` protects draft/state decisions; platform idempotency protects create/submit/batch/import retry.
- First valid concurrent approval wins; later attempt receives conflict, never duplicate history.

### LD-11: VPL summary ownership stays in VPL

- Vendor API-20 may call VPL summary contract but does not persist/cache a second business source without an explicitly versioned read cache.

### LD-12: No feature PDF artifact

- `thai-doc-pdf-generator` is skipped. A QA result PDF produced by UAT tooling is not a Vendor Price List business document.

## §7.2 Drift Resolution

| Drift | Resolution |
|---|---|
| BRD S-04 immediate apply below threshold vs locks | LD-02; always pending |
| BRD entity includes company/site labels but current HTML does not | LD-03; context + null site |
| Old reference lacks current F-VENDOR/Product contracts | use LOCK-VPL-14/17 canonical sources |
| Old UI allowed master-like free text | LD-05 search dropdowns |
| Old behavior implied Active UOM/currency mutation | LD-04 new Header via clone |
| Prototype timer simulates requests | production waits for API state; timer is not contract |

## §7.3 Convention Deviations

### CD-01: Long canonical feature ID

Standard examples use `F-XX`; this approved feature uses `F-VENDOR-PRICELIST-001`. API/Function IDs retain the full canonical prefix to avoid a second alias namespace.

### CD-02: Custom state actions use POST

Approval, submit and availability actions use POST custom-action endpoints instead of generic PATCH because they create workflow/audit side effects and require idempotency.

### CD-03: Cross-module references are soft UUID references

No DB FK crosses Vendor/Product service ownership. UUID is authoritative; code/name snapshots exist for display/audit only.

## §7.4 Architecture Tradeoffs

| Tradeoff | Accepted decision | Revisit trigger |
|---|---|---|
| Context-only company/site vs visible selectors | context-only for current UI | multi-site users must set a non-default site |
| Atomic batch vs partial commit | atomic accepted-set after preview | confirmed business need for very large async jobs |
| Synchronous compare | synchronous within benchmark | sustained latency above SLO |
| Two new CUBIC engines vs feature-local duplicate logic | CUBIC candidates | Architect registration review |
| Soft master refs vs cross-service FK | soft refs + live validation + snapshots | ownership architecture changes |

## §7.5 Deferred Implementation Decisions

| Item | Owner | Deadline |
|---|---|---|
| CUBIC global Engine IDs/versions | Architect | before merge |
| Internal transport for Vendor API-20 façade | Backend Lead | API design review |
| Platform config: page/batch/file limits, preview/idempotency TTL | Platform Owner | staging |
| FX freshness window and monitoring thresholds | Finance/Policy Owner | staging |

None of these may change the locked business behavior without BRD/FRD revision.
