# 05_RULES — F-VENDOR-PRICELIST-001 Vendor Price List

> **Audience:** Backend developer + QA  
> **Principle:** กฎในไฟล์นี้เป็น declarative source of truth; constants ที่เป็น config ห้าม hardcode

---

## §5.1 Business Rules

| ID | Statement | Enforcement / Error |
|---|---|---|
| BR-VPL-01 | Header unique ตาม tenant/company/site/vendor/product/UOM/currency; null site นับเป็น scope เดียวกัน | DB unique + FN-04 · `BR_VPL_DUPLICATE_HEADER` |
| BR-VPL-02 | สร้าง/submit/import/resolve/compare ได้เฉพาะ F-VENDOR UUID ใน tenant เดียวกันและ `status=active` | FN-04/FN-18/FN-19 · `BR_VENDOR_NOT_ACTIVE` |
| BR-VPL-03 | Product UUID ต้อง `status=active && purchasable=true` | FN-04/FN-18/FN-19 · `BR_PRODUCT_NOT_PURCHASABLE` |
| BR-VPL-04 | `price > 0`, `price_per > 0`; landed cost ต้องไม่ติดลบ | DB + ENG-01 |
| BR-VPL-05 | สกุลเงินเริ่มต้นมาจาก `F-VENDOR.currency_code`; ผู้ใช้เปลี่ยนก่อนสร้างได้ | UI default + server validation |
| BR-VPL-06 | `buy_uom` ต้องเป็น base UOM หรือ Product UOM ที่ `can_buy=true` | FN-04 · `BR_UOM_NOT_PURCHASABLE` |
| BR-VPL-07 | `tax_code` default จาก `product.vat_prod_group`; GL mapping เป็นของ Finance Posting Setup | FN-04/FN-15 |
| BR-VPL-08 | Tier เรียง min ขึ้น, ไม่ซ้อน, max>min, มี max=null ได้เฉพาะแถวสุดท้าย; flat มีหนึ่งแถว | DB + FN-04 · `BR_TIER_OVERLAP` |
| BR-VPL-09 | Landed ex-tax = `(price ÷ price_per) × (1 − discount_pct/100) + freight_per_unit` | ENG-01; formula version in trace |
| BR-VPL-10 | `effective_from` required; `effective_to=null` แสดง “เป็นต้นไป”; end ≥ start | DB + FN-04 |
| BR-VPL-11 | ราคาใหม่และทุก version ต้อง approval; `abs(change_pct) >= configured threshold` เลือก elevated DOA tier | FN-05/FN-12; default config 10%, never local constant |
| BR-VPL-12 | Approver ต้องไม่เท่ากับ requester/maker ทุก tier รวม admin | FN-06 + DB guard · `BR_SOD_VIOLATION` |
| BR-VPL-13 | ราคา/discount/freight/landed/FX/change% เป็น Confidential; unauthorized role ไม่ได้รับ raw value | server projection + audit |
| BR-VPL-14 | Vendor non-active ถูกตัดจาก new/submit/import/resolve/compare; price history remains | event/cache invalidation + live recheck |
| BR-VPL-15 | Compare ใช้ qty/date/target currency เดียวกันและ dated fresh FX; sort landed target ascending | ENG-02 |
| BR-VPL-16 | Resolve รับ explicit vendor และคืนคำตอบเดียว; compare เท่านั้นที่จัดอันดับหลาย vendor | ENG-02 · ambiguity/no-price errors |
| BR-VPL-17 | ทุก price/status/approval change append WORM history with before/after/by/at/reason/correlation | FN mutation + DB WORM |
| BR-VPL-18 | Approval SLA เริ่มต้น 1 วันทำการ; overdue escalates through DOA | policy snapshot + scheduler/monitor |
| BR-VPL-19 | Active validity/tier under same resolution key must not yield multiple answers | FN-04/FN-06 + ENG-02 |
| BR-VPL-20 | PR/RFQ/PO persist `price_version_id` + calculation snapshot/trace; later changes never recalculate old transaction | API-14 contract |
| BR-VPL-21 | Source precedence: approved Contract > approved VPL > authorized manual override | ENG-02; contract UI remains out of scope |

## §5.2 State Machines

### Version workflow

```text
draft --submit--> pending_approval --approve--> active --new approved version--> superseded
  ^                         |
  └---------reject----------┘  (rejection event retained; editable state shown as draft)
```

| From | Action | To | Actor / Guards |
|---|---|---|---|
| none | create/save draft | draft | canManage; valid master identity |
| draft | submit | pending_approval | Maker; all rules + DOA route |
| pending_approval | approve | active | current DOA approver; SoD; no overlap |
| pending_approval | reject | draft | current approver; reason required |
| active | create new version | draft or pending_approval | Maker; identity locked |
| active | later version becomes effective | superseded | system transaction after approval/effective gate |

Only draft is price-content mutable. Pending may only receive workflow metadata. Active/superseded price/tier data is immutable.

### Header availability

| From | Action | To | Guard |
|---|---|---|---|
| inactive | first version approved / activate | active | Vendor/Product eligible; one applicable Active version; no ambiguity |
| active | deactivate | inactive | soft action; history retained |
| inactive | reactivate | active | live master + UOM + overlap revalidation |

Header inactive excludes all its versions from resolve/compare without deleting them.

## §5.3 Permission Matrix

| Role | View | See price | Create/Edit/Import | Submit | Approve/Reject | Activate/Deactivate |
|---|---:|---:|---:|---:|---:|---:|
| procurement_officer | ✓ | ✓ | ✓ | ✓ | — | ✓ |
| procurement_manager | ✓ | ✓ | ✓ | ✓ | DOA + SoD | ✓ |
| procurement_director | ✓ | ✓ | ✓ | ✓ | DOA + SoD | ✓ |
| finance_viewer | ✓ | ✓ | — | — | — | — |
| admin | ✓ | ✓ | ✓ | ✓ | DOA + SoD | ✓ |
| other authenticated | ✓ | masked | — | — | — | — |
| downstream service | scoped | scoped | — | — | — | — |

## §5.4 Field & Cross-Field Validation

| Field/action | Rule | UI message anchor / code |
|---|---|---|
| identity | unique header key | `มีรายการราคาสำหรับขอบเขตนี้แล้ว` |
| vendor_id | same tenant, live active | `คู่ค้านี้ไม่พร้อมใช้งานสำหรับรายการราคาใหม่` |
| product_id | live active+purchasable | `สินค้าไม่อยู่ในสถานะใช้งานหรือซื้อไม่ได้` |
| buy_uom | current purchase UOM | `Purchase UOM ไม่ตรงกับ Product Master` |
| price | >0 | `ราคาต้อง > 0` |
| price_per | >0 | `BR_PRICE_PER_INVALID` |
| discount_pct | 0..100 and result non-negative | `BR_DISCOUNT_INVALID` |
| freight | >=0 | `BR_FREIGHT_INVALID` |
| effective range | from required; to null or >=from | `กรุณาระบุวันเริ่มราคา` / `BR_DATE_RANGE_INVALID` |
| tiers | sorted, contiguous policy, no overlap | `ช่วงปริมาณ (tier) ซ้อนทับกัน` |
| change submit | reason required | `กรุณาระบุเหตุผล` |
| approval | current route + maker≠approver | `ไม่พบสายอนุมัติที่ใช้ได้` / `ไม่สามารถอนุมัติรายการที่ตนเองสร้างได้` |
| Active overlap | exactly one answer | `ช่วงวันที่หรือปริมาณซ้อนกับราคาที่ใช้งานอยู่` |
| batch row | blank ignored; started row complete | `กรุณากรอกข้อมูลให้ครบถ้วน` |

## §5.5 Edge Cases

| ID | Scenario | Resolution |
|---|---|---|
| EC-01 | duplicate vendor/product/UOM/currency scope | block by BR-VPL-01; clone must actually change identity |
| EC-02 | vendor becomes non-active after picker opened | recheck on mutation; block; history untouched |
| EC-03 | tier qty ranges overlap | reject preview/submit with row/tier anchors |
| EC-04 | price ≤0 or net cost negative | ENG-01/DB reject |
| EC-05 | batch blank and incomplete rows | ignore fully blank; highlight/block any started invalid row |
| EC-06 | CSV vendor/product code unmatched | row invalid; preview counts it; commit cannot silently skip without reported result |
| EC-07 | missing change reason | block submit/price change |
| EC-08 | requester attempts own approval | 403/422 SoD; no state/history success event |
| EC-09 | discount >100 or invalid freight | reject; no clamp or silent correction |
| EC-10 | FX missing/stale | exclude with reason or fail compare/resolve; never assume rate |
| EC-11 | two users edit/approve concurrently | first valid commit wins; second 409 `ERR_STALE_DATA`/already decided |
| EC-12 | another pending version already exists | block with `BR_PENDING_VERSION_EXISTS` |
| EC-13 | inactive Header | excluded from resolve/compare |
| EC-14 | no effective tier/version | `NO_APPLICABLE_PRICE` with reason |
| EC-15 | unauthorized export/log/print | raw pricing omitted; attempt audited |
| EC-16 | service snapshot vs UI mask | service gets only granted scope; UI receives masked contract; snapshot remains immutable |

### Activated proactive probes

- PR-1 concurrency: optimistic version/If-Match; concurrent decision test.
- PR-3 permission mid-flight: role rechecked on each mutation.
- PR-4/PR-7 network/idempotency: retry same key returns same result.
- PR-5 bulk atomicity: preview then atomic accepted-set commit; no partial silent write.
- PR-6 wizard: explicit `บันทึกร่าง`; unsaved browser-local fields are not promised after close.
- PR-9 financial race: unique/pending/activation checks occur inside transactions.

## §5.6 Error Catalog

| Code | HTTP | Meaning |
|---|---:|---|
| `ERR_VALIDATION_FAILED` | 400 | malformed/field validation |
| `ERR_NOT_AUTHENTICATED` | 401 | no valid auth |
| `ERR_INSUFFICIENT_ROLE` | 403 | capability denied |
| `ERR_PERMISSION_REVOKED` | 403 | role changed before mutation |
| `ERR_VPL_NOT_FOUND` | 404 | header/version absent in scope |
| `ERR_STALE_DATA` | 409 | If-Match/version mismatch |
| `ERR_IDEMPOTENCY_CONFLICT` | 409 | same key, different body |
| `ERR_ALREADY_DECIDED` | 409 | approval no longer pending |
| `BR_VPL_DUPLICATE_HEADER` | 422 | identity exists |
| `BR_VENDOR_NOT_ACTIVE` | 422 | vendor non-active/wrong tenant |
| `BR_PRODUCT_NOT_PURCHASABLE` | 422 | product non-active/non-purchasable |
| `BR_UOM_NOT_PURCHASABLE` | 422 | invalid purchase UOM |
| `BR_PRICE_INVALID` | 422 | price/price_per invalid |
| `BR_DISCOUNT_INVALID` | 422 | discount/result invalid |
| `BR_FREIGHT_INVALID` | 422 | freight negative |
| `BR_DATE_RANGE_INVALID` | 422 | effective date invalid |
| `BR_TIER_OVERLAP` | 422 | tier ambiguity |
| `BR_ACTIVE_PRICE_OVERLAP` | 422 | active effective ambiguity |
| `BR_REASON_REQUIRED` | 422 | missing reason |
| `BR_PENDING_VERSION_EXISTS` | 422 | one pending already exists |
| `BR_DOA_ROUTE_NOT_FOUND` | 422 | no current route |
| `BR_SOD_VIOLATION` | 422 | approver=requester |
| `NO_APPLICABLE_PRICE` | 422 | no valid active price |
| `BR_PRICE_AMBIGUOUS` | 422 | more than one result |
| `ERR_FX_UNAVAILABLE` | 422/503 | missing/stale FX or service down |
| `ERR_PREVIEW_EXPIRED` | 410 | batch/import token expired |
| `ERR_UPSTREAM_UNAVAILABLE` | 503 | vendor/product/policy dependency unavailable |

## §5.7 Security & Compliance Application

Security baseline is BRD v2.4 P2 Approval/Workflow plus CUBE context.

- Authentication/session: all APIs authenticated; service-to-service uses scoped identity.
- Authorization: RBAC + current DOA participant + pricing scope; mutation-time recheck.
- Financial/Confidential: BEFORE/AFTER audit; masking/omission at server; logs use IDs and safe metadata.
- SoD/DOA: requester never approves; threshold/config snapshots are auditable.
- Audit: owned WORM history plus central `T_audit_log`; correlation ID joins them.
- Multi-tenant: DB RLS + authenticated company context; no body-controlled tenant/company.
- Import: CSV size/schema/encoding validation, formula execution disabled, filename untrusted, preview token signed and expiring.
- Integrity: Active price/tier immutability, transaction snapshot and no hard delete.

## §5.8 Compliance & Monitoring

| Requirement | Evidence |
|---|---|
| ISO-style access/audit | RLS, RBAC, WORM, central audit |
| SOX-style control | maker-checker, DOA, immutable financial change history |
| Confidential pricing | per-field classification + server projection |
| SLA | pending timestamp, DOA owner, 1-business-day escalation |
| Anomaly | negative/invalid cost blocked; threshold/rapid approval events reportable |
