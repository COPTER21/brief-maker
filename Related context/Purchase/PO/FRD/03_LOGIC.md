# 03_LOGIC — F-PO-001 ใบสั่งซื้อ (Purchase Order)

> **Audience:** BE dev (business logic layer)
> **Scope:** Non-HTTP logic — functions, state transitions, calculations, validations

---

## §3.1 Functions (Scope-Local)

### F-PO-001-FN-01: createPurchaseOrder
- **Purpose:** สร้าง PO draft จาก input (source + vendor + lines)
- **Input:** `{ source_type, source_pr_no?, source_cp_no?, vendor_id, buyer, po_date, expected_date, payment_term, lines[], endbill_discount_*, wht_* }`
- **Output:** `PurchaseOrder | ValidationError[]`
- **Invoked by:** API-03
- **Calls:** FN-03 (ถ้ามี source), FN-05 (validate), ENG po-amount-engine (totals)
- **Side effects:** INSERT po_header + po_line + audit
- **Iron check:** ✅ no HTTP terms

### F-PO-001-FN-02: updatePurchaseOrder
- **Purpose:** แก้ไข PO draft + recompute totals
- **Input:** `{ id, patch }` · **Output:** `PurchaseOrder | Error`
- **Invoked by:** API-04 · **Calls:** FN-05, ENG po-amount-engine
- **Side effects:** UPDATE po_header/po_line (draft only), modified_by/at

### F-PO-001-FN-03: buildLinesFromSource
- **Purpose:** สร้างรายการเริ่มต้นจากแหล่งที่มา — CP awarded (line_count/total ของผู้ชนะ) หรือ PR (pr.total)
- **Input:** `{ source_type, cp_no?|pr_no?, vendor_id? }` · **Output:** `PoLine[]`
- **Invoked by:** FN-01, UI step2 selectVendor
- **Side effects:** none (pure builder)

### F-PO-001-FN-04: resolveSourceVendor
- **Purpose:** ตัดสินวิธีได้ผู้ขาย — CP → ล็อกผู้ชนะ (won) ; PR/direct → ต้องเลือกจาก Vendor Master
- **Input:** `{ source_type, cp_no? }` · **Output:** `{ mode:"locked"|"selectable", vendor? }`
- **Invoked by:** UI step1/step2, FN-01, FN-05
- **Side effects:** none

### F-PO-001-FN-05: validatePurchaseOrder
- **Purpose:** ตรวจรวมศูนย์ (vendor required, date order, ≥1 line, discount cap, DoA ceiling, source mode ตาม config)
- **Input:** `PurchaseOrder` · **Output:** `ValidationError[]`
- **Invoked by:** FN-01, FN-02, API-05 · **Calls:** FN-04
- **Side effects:** none · maps VR01–VR08

### F-PO-001-FN-06: applyStatusTransition
- **Purpose:** เปลี่ยน status_doc ตาม state machine + SoD + reason guard
- **Input:** `{ id, action:submit|approve|reject|return|cancel, actor, reason? }` · **Output:** `{ status_doc, revision_no } | Error`
- **Invoked by:** API-05/-06/-07/-08/-09 · **Calls:** ENG doa-resolver-engine (submit/approve)
- **Side effects:** UPDATE status_doc, revision_no, po_approval log; SoD block (Maker≠Approver)
- **Trigger rules:** ดู 05_RULES §5.4 state table

### F-PO-001-FN-07: generatePoNumber
- **Purpose:** ขอเลข running `PO-YYYY-NNNNN` ตอน approved
- **Input:** `{ year }` · **Output:** `po_no` · **Invoked by:** FN-06 (approve)
- **Calls:** Document Numbering service · **Side effects:** reserve sequence

### F-PO-001-FN-08: buildPoPdfModel
- **Purpose:** map PO → PDF model + เลือกรูปแบบภาษี (VAT/NoVAT/Discount/WHT) ตามข้อมูล
- **Input:** `PurchaseOrder` · **Output:** `PoPdfModel { variant, header, lines, totals, baht_text }`
- **Invoked by:** API-10 · **Calls:** ENG po-amount-engine (totals), ENG baht-text-engine
- **Side effects:** none

### F-PO-001-FN-09: buildPoListQuery
- **Purpose:** ประกอบ query list + filter 3 แกน
- **Input:** `{ filters }` · **Output:** `QuerySpec` · **Invoked by:** API-01 · **Side effects:** none

---

## §3.2 Engines (Reusable / CUBIC-Registered)

### ENG: po-amount-engine (NEW)
- **code:** `po-amount-engine` · **category:** financial-calculation
- **input schema:** `{ lines:[{ qty, unit_price, discount_mode, discount_pct, discount_amt, vat_mode, vat_pct }], endbill_discount_mode, endbill_discount_value, wht_enabled, wht_pct }`
- **output schema:** `{ subtotal, total_discount, after_discount, vat_amount, total_incl_vat, wht_amount, net_payable, line_breakdown[] }`
- **logic outline:**
  1. per line: `line_subtotal = qty×unit_price` ; `line_discount = amount? min(discount_amt, line_subtotal) : line_subtotal×discount_pct/100` ; `line_net = subtotal − discount`
  2. VAT per line: none=0 · add=`net×vat%` · included=`net×vat/(100+vat)` (ถอนย้อน)
  3. `subtotal = Σ line_net`
  4. `endbill_discount = amount? value : subtotal×value/100` → `after_discount`
  5. `vat_amount = round(after_discount×vat%, 2)` (ROUND_HALF_UP; ยกเว้น VAT → 0)
  6. `total_incl_vat = after_discount + vat_amount`
  7. `wht_amount = wht_enabled ? round(after_discount×wht%,2) : 0` ; `net_payable = total_incl_vat − wht_amount`
- **Used by:** F-PO-001 (planned: SO/INV reuse) · **Iron check:** ✅ pure, no HTTP/DB

### ENG: doa-resolver-engine (EXISTING — CUBIC, F-PC-DOA-01)
- **code:** `doa-resolver-engine` · **category:** governance
- **input schema:** `{ feature_id, cost_center, amount }`
- **output schema:** `{ tier, approver_role, within_limit:boolean, chain[] }`
- **logic outline:** resolve tier จาก DoA matrix (≤100K→Manager · ≤500K→Director · >500K→CEO) — placeholder pattern, ไม่ hardcode ใน PO
- **Used by:** ทุก feature ที่มี approval · **Iron check:** ✅ reusable governance engine

### ENG: baht-text-engine (EXISTING — reusable)
- **code:** `baht-text-engine` · **category:** formatting
- **input:** `{ amount }` · **output:** `{ thai_text }` (เอ็ด/ยี่สิบ/ล้าน/สตางค์/ถ้วน)
- **Used by:** PO/SO/INV/RC PDF · **Iron check:** ✅ pure

---

## §3.3 API ↔ Logic Trace Table (Phase 3.5 Anchor)
| API | Calls Functions | Calls Engines |
|---|---|---|
| API-01 GET list | FN-09 | — |
| API-02 GET detail | — (read) | — |
| API-03 POST create | FN-01, FN-03, FN-05 | po-amount-engine |
| API-04 PUT update | FN-02, FN-05 | po-amount-engine |
| API-05 POST submit | FN-05, FN-06 | doa-resolver-engine |
| API-06 POST approve | FN-06, FN-07 | doa-resolver-engine |
| API-07 POST reject | FN-06 | — |
| API-08 POST return | FN-06 | — |
| API-09 POST cancel | FN-06 | — |
| API-10 GET pdf | FN-08 | po-amount-engine, baht-text-engine |
| API-11 GET awarded | — (read CP) | — |
| API-12 GET vendors | — (read master) | — |
| API-13 POST attach | — (storage) | — |

> **R8 check:** ทุก mutation API (03–09,13) มี ≥1 Function ✅ · ไม่มี orphan function/engine ✅
