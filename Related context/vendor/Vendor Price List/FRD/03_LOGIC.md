# 03_LOGIC — F-VENDOR-PRICELIST-001 Vendor Price List

> Audience: BE (business logic). Functions = scope-local (camelCase). Engines = reusable/CUBIC (kebab-case, pure, no HTTP). 🚨 R8: ทุก mutation API trace ใน §3.3.

## §3.1 Functions (Scope-Local)

### F-VPL-FN-01: createVendorPriceItem
- **Purpose:** สร้าง item + tiers ใหม่
- **Input:** `{ vendor_id, product_id, vendor_item_code?, buy_uom, currency, price_type, tiers[] }`
- **Output:** `VendorPriceItem | ValidationError[]`
- **Invoked by:** F-VPL-API-05, (ผ่าน bulk) F-VPL-FN-05
- **Calls:** F-VPL-FN-03 (validateVendorPriceLink), F-VPL-FN-04 (validateTiers), ENG-VPL-02 (landed-price)
- **Side effects:** INSERT T_vendor_price_item + T_vendor_price_tier · audit
- **Iron rule:** ✅ no HTTP

### F-VPL-FN-02: updateVendorPriceItem
- **Purpose:** แก้ code/uom/currency (ไม่แตะราคา)
- **Input:** `{ id, version, patch:{vendor_item_code?,buy_uom?,currency?} }`
- **Output:** `VendorPriceItem | VersionConflict`
- **Invoked by:** F-VPL-API-06 · **Side effects:** UPDATE item (version++) · audit

### F-VPL-FN-03: validateVendorPriceLink
- **Purpose:** ตรวจ UNIQUE(vendor,product) + vendor.active + product.purchasable + buy_uom ∈ product buy uoms
- **Input:** `{ vendor_id, product_id, buy_uom, tenant_id }`
- **Output:** `{ ok } | ValidationError` (DUPLICATE / VENDOR_INACTIVE / NOT_PURCHASABLE / UOM_INVALID)
- **Invoked by:** FN-01, FN-05 · **Side effects:** none (read masters)

### F-VPL-FN-04: validateTiers
- **Purpose:** ตรวจ tier: price>0, เรียง min↑, ห้าม overlap, เฉพาะ tier สุดท้าย max=∞, valid_from required
- **Input:** `tiers[]`
- **Output:** `{ ok, sorted_tiers } | ValidationError(TIER_OVERLAP / PRICE_NONPOSITIVE / VALID_FROM_REQUIRED)`
- **Invoked by:** FN-01 · **Side effects:** none

### F-VPL-FN-05: bulkCreateVendorPrices
- **Purpose:** สร้างหลาย item (flat, default conditions: price_per=1, disc=0, freight=0, tax=product vat, from=page date)
- **Input:** `{ vendor_id?, valid_from, rows[] }`
- **Output:** `{ created, skipped, errors[] }`
- **Invoked by:** F-VPL-API-07, (ผ่าน CSV) FN-06
- **Calls:** FN-03 (ต่อ row), FN-01 · **Side effects:** INSERT N items+tiers · audit

### F-VPL-FN-06: parseCsvImport
- **Purpose:** parse CSV → map vendor_code/product_code → id, นับ unmatched, ข้ามแถวว่าง
- **Input:** `csvText`
- **Output:** `{ rows[], unmatched[] }`
- **Invoked by:** F-VPL-API-08 · **Calls:** FN-05 · **Side effects:** none (resolve masters)

### F-VPL-FN-07: requestPriceChange
- **Purpose:** คำนวณ %เปลี่ยน → ถ้า ≤ threshold apply ทันที + history; > threshold set pending_approval
- **Input:** `{ id, tier_id?, new_price, reason, actor }`
- **Output:** `{ applied } | { status:"pending_approval", pct }`
- **Invoked by:** F-VPL-API-09
- **Calls:** ENG-VPL-04 (doa-threshold-evaluator), ENG-VPL-02 (landed-price)
- **Side effects:** UPDATE price + INSERT history(applied) | SET pending + status; block ถ้ามี pending ค้าง (E12)
- **Guard:** reason required (E07)

### F-VPL-FN-08: approvePriceChange
- **Purpose:** อนุมัติ/ปฏิเสธคำขอ — **SoD: approver ≠ pending.by**
- **Input:** `{ id, decision, approver }`
- **Output:** `{ status:"active" } | SoDError`
- **Invoked by:** F-VPL-API-10
- **Side effects:** approve → UPDATE price + INSERT history(approved) + clear pending; reject → INSERT history(rejected) + clear pending
- **Guard:** approver ≠ requester (E08/R12) → else ERR_SOD_SELF_APPROVAL

### F-VPL-FN-09: toggleItemStatus
- **Purpose:** soft active ↔ inactive
- **Input:** `{ id, status }` · **Output:** `VendorPriceItem`
- **Invoked by:** F-VPL-API-11 · **Side effects:** UPDATE status · audit · (inactive → ถูกตัดจาก get-price/compare, E13)

### F-VPL-FN-10: buildVendorSummaries
- **Purpose:** รายชื่อคู่ค้า = active vendors ∪ vendors ที่มี item (active-first) + count items
- **Input:** `{ tenant_id, filters }` · **Output:** `VendorSummary[]`
- **Invoked by:** F-VPL-API-02 · **Side effects:** none

### F-VPL-FN-11: buildFlatList
- **Purpose:** product-centric list + current price ต่อ item (ผ่าน price-select)
- **Input:** `{ filters, paging }` · **Output:** `FlatRow[]`
- **Invoked by:** F-VPL-API-01 · **Calls:** ENG-VPL-01 · **Side effects:** none

### F-VPL-FN-12: maskPricingForRole
- **Purpose:** บังคับ Confidential — ถ้า role ∉ {proc, finance, admin} → ราคา/ส่วนลด/ค่าขนส่ง/net = `•••`
- **Input:** `{ payload, role }` · **Output:** masked payload
- **Invoked by:** API-01/03/04/12 (response), export, log · **Side effects:** none

## §3.2 Engines (Reusable / CUBIC)

### ENG-VPL-01: price-select-engine [NEW]
| Field | Value |
|---|---|
| code | `price-select-engine` |
| name | Vendor Price Select (get-price) |
| category | matcher |
| version | 1.0.0 · status DRAFT · owner F-VPL · stateless true |

**Input:** `{ tiers[], qty, asOf, currency }`
**Output:** `{ tier, price, net_unit }` หรือ `null` (ไม่มี active ที่ qty/validity)
**Logic Outline:**
1. filter tiers: status=active ∧ valid_from ≤ asOf ∧ (valid_until null ∨ ≥ asOf)
2. filter: min_qty ≤ qty ∧ (max_qty null ∨ qty ≤ max_qty)
3. ต่อ tier → net_unit จาก ENG-VPL-02
4. คืน tier ที่ net_unit ต่ำสุด (R16)
**Error:** ENG_ERR_NO_ACTIVE_PRICE
**Dependencies:** ENG-VPL-02
**Used by features:** F-VPL (compare, flat list, get-price), **PR, PO** (autofill)
**Iron rules:** ✅ stateless ✅ pure ✅ deterministic ✅ no HTTP ✅ reusable

### ENG-VPL-02: landed-price-engine [NEW]
| code | `landed-price-engine` · category financial-calculation · v1.0.0 · stateless true |
**Input:** `{ price, price_per, discount_pct, freight }`
**Output:** `{ net_unit }` — `net_unit = (price / price_per) * (1 - discount_pct/100) + freight` (ex-VAT, R09)
**Logic Outline:** 1) base=price/price_per 2) afterDisc=base*(1-disc/100) 3) +freight 4) คืน
**Error:** ENG_ERR_INVALID_INPUT (price≤0 / per≤0)
**Used by:** F-VPL, PR, PO, Compare
**Iron rules:** ✅ pure ✅ deterministic ✅ no HTTP

### ENG-VPL-03: fx-normalize-engine [NEW]
| code | `fx-normalize-engine` · category financial-calculation · v1.0.0 · stateless true |
**Input:** `{ amount, fromCurrency, toCurrency:"THB", fxRates }`
**Output:** `{ amount_thb }` (R15)
**Logic Outline:** lookup rate(from→to) จาก fxRates → multiply → คืน
**Error:** ENG_ERR_FX_RATE_MISSING (fallback rule → E10)
**Used by:** F-VPL (compare), PR, PO
**Iron rules:** ✅ pure ✅ no HTTP

### ENG-VPL-04: doa-threshold-evaluator [NEW — placeholder]
| code | `doa-threshold-evaluator` · category validation · v0.1.0 · status DRAFT · stateless true |
**Input:** `{ oldPrice, newPrice, thresholdPct, requester }`
**Output:** `{ requires_approval:boolean, pct }`
**Logic Outline:** 1) pct=|new-old|/old*100 2) requires_approval = pct > thresholdPct (R11)
**Note:** ⚠️ **placeholder** — Phase 2 จะ delegate ไป Policy Center DOA engine (Feature-DOA pairing); SoD บังคับใน FN-08 (approver≠requester). thresholdPct จาก config (OQ1).
**Used by:** F-VPL (price-change); future: ทุก feature ที่มี DoA
**Iron rules:** ✅ pure ✅ no HTTP

## §3.3 API ↔ Logic Trace Table (R8 anchor)
| API | Calls Functions | Calls Engines |
|---|---|---|
| API-01 GET list (flat) | FN-11 buildFlatList, FN-12 mask | ENG-VPL-01, -02 |
| API-02 GET vendors | FN-10 buildVendorSummaries | — |
| API-03 GET vendor detail | FN-12 mask | ENG-VPL-01, -02 |
| API-04 GET item detail | FN-12 mask | ENG-VPL-02 |
| API-05 POST create | FN-01, FN-03, FN-04 | ENG-VPL-02 |
| API-06 PUT edit | FN-02 | — |
| API-07 POST bulk | FN-05, FN-03, FN-01 | ENG-VPL-02 |
| API-08 POST csv | FN-06, FN-05 | ENG-VPL-02 |
| API-09 POST price-change | FN-07 | ENG-VPL-04, -02 |
| API-10 POST approve | FN-08 | — |
| API-11 POST status | FN-09 | — |
| API-12 GET compare | FN-12 mask | ENG-VPL-01, -02, -03 |
| API-13 GET get-price | — | ENG-VPL-01, -02, -03 |

> R8: ทุก mutation API (05–11) มี ≥1 Function ✅. ไม่มี orphan: FN-01..12 ทุกตัวถูก trace; ENG-01..04 ถูกเรียกผ่าน Function/API ✅.
