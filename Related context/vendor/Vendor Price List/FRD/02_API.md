# 02_API — F-VENDOR-PRICELIST-001 Vendor Price List

> Audience: BE (HTTP layer). 🚨 ห้าม business logic >5 บรรทัด — ย้าย 03_LOGIC. 🚨 R8: mutation ทุกตัวมี "Calls (Logic)". Auth: required + role-gated. Multi-tenant: `X-Tenant-Id`. Mutations: `Idempotency-Key`; updates: `If-Match` (version).

## §2.1 API Overview
| ID | Method | Path | Summary | Auth (roles) |
|---|---|---|---|---|
| F-VPL-API-01 | GET | /api/v1/vendor-prices | List (flat, product-centric) + filters | required |
| F-VPL-API-02 | GET | /api/v1/vendor-prices/vendors | Vendor summaries (vendor-first list) | required |
| F-VPL-API-03 | GET | /api/v1/vendor-prices/vendors/:vendorId | Vendor detail + items | required |
| F-VPL-API-04 | GET | /api/v1/vendor-prices/:id | Item detail + tiers + history | required |
| F-VPL-API-05 | POST | /api/v1/vendor-prices | Create single item (+tiers) | proc_officer+ |
| F-VPL-API-06 | PUT | /api/v1/vendor-prices/:id | Edit code/uom/currency | proc_officer+ |
| F-VPL-API-07 | POST | /api/v1/vendor-prices/bulk | Batch create | proc_officer+ |
| F-VPL-API-08 | POST | /api/v1/vendor-prices/bulk/csv | CSV import | proc_officer+ |
| F-VPL-API-09 | POST | /api/v1/vendor-prices/:id/price-change | Request price change (apply/pending) | proc_officer+ |
| F-VPL-API-10 | POST | /api/v1/vendor-prices/:id/approve | Approve pending price change | proc_manager+ |
| F-VPL-API-11 | POST | /api/v1/vendor-prices/:id/status | Toggle active/inactive | proc_officer+ |
| F-VPL-API-12 | GET | /api/v1/vendor-prices/compare | Compare across vendors (FX-normalized) | proc/finance |
| F-VPL-API-13 | GET | /api/v1/vendor-prices/get-price | Resolve price (product+vendor+qty) — feeds PR/PO | required (service) |

## §2.2 Per-API Contract (key)

### F-VPL-API-05: POST /api/v1/vendor-prices
| Field | Value |
|---|---|
| auth | required (proc_officer, proc_manager, proc_director, admin) |
| body | `{ vendor_id, product_id, vendor_item_code?, buy_uom, currency, price_type, tiers:[{min_qty,max_qty?,price,price_per,discount_pct,freight,tax_code,incl_vat,valid_from,valid_until?}] }` |
**Validation (thin):** required vendor_id/product_id/buy_uom/price_type/tiers; deep rules → 05_RULES (UNIQUE, active vendor, purchasable, uom, tier overlap, price>0, valid_from).
**Response 201:** `{ id, status:"active", version:1 }`
**Errors:** 400 ERR_VALIDATION_FAILED · 403 ERR_INSUFFICIENT_ROLE · 409 ERR_DUPLICATE_VENDOR_PRODUCT · 422 ERR_TIER_OVERLAP
**Preconditions:** vendor.status=active · product.purchasable=true · UNIQUE(vendor,product)
**Side effects:** INSERT item + tiers · audit
**Calls (Logic):** createVendorPriceItem → validateVendorPriceLink, validateTiers, landed-price-engine

### F-VPL-API-06: PUT /api/v1/vendor-prices/:id
| auth | proc_officer+ · If-Match: version |
**Body:** `{ vendor_item_code?, buy_uom?, currency? }` (ราคาเปลี่ยนผ่าน API-09 เท่านั้น)
**Response 200:** `{ id, version }` · **Errors:** 404 · 409 ERR_VERSION_CONFLICT
**Calls (Logic):** updateVendorPriceItem

### F-VPL-API-07: POST /api/v1/vendor-prices/bulk
**Body:** `{ vendor_id?, valid_from, rows:[{vendor_id?,product_id,vendor_item_code?,buy_uom,price}] }` (vendor_id ระดับ body = locked mode; ไม่งั้น per-row)
**Response 200:** `{ created:N, skipped:M, errors:[{row,reason}] }`
**Side effects:** INSERT N items (flat, default conditions) · audit
**Calls (Logic):** bulkCreateVendorPrices → validateVendorPriceLink (ต่อ row), createVendorPriceItem

### F-VPL-API-08: POST /api/v1/vendor-prices/bulk/csv
**Body:** multipart `file` (header: vendor_code,product_code,vendor_item_code,uom,price,price_per,discount_pct,freight,currency,tax_code,valid_from,valid_until)
**Response 200:** `{ created, unmatched:[{row,code}], errors:[] }`
**Calls (Logic):** parseCsvImport → bulkCreateVendorPrices

### F-VPL-API-09: POST /api/v1/vendor-prices/:id/price-change
**Body:** `{ tier_id?, new_price, reason }` (reason required)
**Response 200:** `{ id, applied:true }` หรือ `{ id, status:"pending_approval", pct }`
**Errors:** 400 ERR_REASON_REQUIRED · 409 ERR_PENDING_EXISTS (มีคำขอค้าง — E12)
**Side effects:** ≤threshold → UPDATE price + INSERT history(applied) · >threshold → SET pending + status=pending_approval
**Calls (Logic):** requestPriceChange → doa-threshold-evaluator, landed-price-engine

### F-VPL-API-10: POST /api/v1/vendor-prices/:id/approve
**Body:** `{ decision:"approve"|"reject" }`
**Response 200:** `{ id, status:"active" }`
**Errors:** 403 ERR_SOD_SELF_APPROVAL (approver = ผู้ขอ) · 409 ERR_NO_PENDING
**Side effects:** approve → UPDATE price + INSERT history(approved) + clear pending · reject → INSERT history(rejected) + clear pending (คงราคาเดิม)
**Calls (Logic):** approvePriceChange (SoD check)

### F-VPL-API-11: POST /api/v1/vendor-prices/:id/status
**Body:** `{ status:"active"|"inactive" }` → **Calls (Logic):** toggleItemStatus

### F-VPL-API-12: GET /api/v1/vendor-prices/compare
**Query:** `product_id` (req), `qty` (default 1)
**Response 200:** `{ rows:[{vendor_id, net_unit_thb, currency, net_unit_native}], cheapest_vendor_id }` — เรียง net_unit_thb ↑; ตัด vendor blocked/blacklisted; **mask ถ้า role ∉ pricing**
**Calls (Logic):** price-select-engine, landed-price-engine, fx-normalize-engine, maskPricingForRole

### F-VPL-API-13: GET /api/v1/vendor-prices/get-price (core contract — PR/PO autofill)
**Query:** `product_id` (req), `vendor_id` (req), `qty` (default 1), `as_of` (default today)
**Response 200:** `{ item_id, tier_id, currency, price, net_unit, net_unit_thb, tax_code, incl_vat }` หรือ 404 ERR_NO_ACTIVE_PRICE (E14)
**Preconditions:** item.status=active · tier ภายใน validity ที่ qty
**Calls (Logic):** price-select-engine → landed-price-engine, fx-normalize-engine

### F-VPL-API-01 / 02 / 03 / 04 (reads)
- API-01 list flat: query `search,product_id,vendor_id,status,limit,offset` → `buildFlatList` + maskPricingForRole
- API-02 vendor summaries: `buildVendorSummaries` (active vendors ∪ items, active-first)
- API-03 vendor detail: items ของ vendor + current price ต่อ item
- API-04 item detail: item + tiers + history (mask ตาม role)
**Calls (Logic):** API-01→buildFlatList, API-02→buildVendorSummaries; ทั้งหมด→maskPricingForRole

## §2.3 Common Errors
ERR_VALIDATION_FAILED(400) · ERR_INSUFFICIENT_ROLE(403) · ERR_SOD_SELF_APPROVAL(403) · ERR_NOT_FOUND(404) · ERR_NO_ACTIVE_PRICE(404) · ERR_DUPLICATE_VENDOR_PRODUCT(409) · ERR_VERSION_CONFLICT(409) · ERR_PENDING_EXISTS(409) · ERR_TIER_OVERLAP(422) · ERR_INTERNAL(500)
