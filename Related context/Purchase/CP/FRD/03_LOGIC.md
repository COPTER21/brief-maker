# 03_LOGIC — F-CP-001 เปรียบเทียบราคา (Price Comparison)

> **Audience:** BE dev (business logic layer)
> **Scope:** All non-HTTP logic — functions, comparison/split/price/DOA engines
> **CUBIC alignment:** §3.1 Functions = scope-local · §3.2 Engines = CUBIC candidates
> **Iron Rule R8:** ทุก mutation API ต้อง trace ≥ 1 Function/Engine ใน §3.3

---

## §3.1 Functions (Scope-Local)

> Naming: camelCase · scope-local

---

### F-CP-001-FN-01: `createComparison`
- **Purpose:** สร้าง CP record ใหม่จาก pr_refs + vendors + lines + quotes (draft)
- **Input:** `{ cp_date, buyer_id, pr_refs[], vendors[], lines[], quotes[], save_mode }`
- **Output:** `Comparison | ValidationError[]`
- **Invoked by:** F-CP-001-API-03
- **Calls:** FN-03 pullLinesFromPR, ENG-01 winner-selection, ENG-02 po-split, ENG-03 price-list-resolver
- **Side effects:** gen `cp_no` (CP-YYMM-NNNNN), INSERT T_comparison(+pr_ref+line+quote), audit log
- **Error cases:** BR_CP_PR_REQUIRED, BR_CP_PR_ALREADY_USED
- **Iron rule check:** ✅ no HTTP terms

### F-CP-001-FN-02: `updateComparison`
- **Purpose:** แก้ไข CP ที่ยัง draft (lines/quotes/winners/vendors) + recompute ยอด
- **Input:** `{ comparison_id, lines[], quotes[], vendors[], expected_version }`
- **Output:** `Comparison | ValidationError[]`
- **Invoked by:** F-CP-001-API-04
- **Calls:** ENG-01 winner-selection, ENG-02 po-split, ENG-03 price-list-resolver
- **Side effects:** UPSERT lines/quotes, recompute winner_total/po_count, audit, version++
- **Error cases:** BR_CP_NOT_EDITABLE, ERR_STALE_DATA
- **Iron rule check:** ✅

### F-CP-001-FN-03: `pullLinesFromPR`
- **Purpose:** รวมรายการสินค้าจาก PR ที่อ้าง → comparison lines (dedupe ตาม item_code, รวม qty)
- **Input:** `{ pr_refs[] }`
- **Output:** `ComparisonLine[]`
- **Invoked by:** FN-01, P-02 step1→2 transition (preview)
- **Calls:** — (อ่าน T_purchase_requisition ผ่าน upstream)
- **Side effects:** — (pure read)
- **Iron rule check:** ✅

### F-CP-001-FN-04: `buildComparisonQuery`
- **Purpose:** สร้าง query filter/sort/paginate สำหรับ list + assemble detail (header+lines+quotes+splits)
- **Input:** `{ search?, status?, sort?, limit, offset } | { comparison_id }`
- **Output:** `{ data[], total } | ComparisonDetail`
- **Invoked by:** F-CP-001-API-01, F-CP-001-API-02
- **Calls:** — · **Side effects:** — (read) · **Iron rule check:** ✅

### F-CP-001-FN-05: `validateComparisonForSubmit`
- **Purpose:** ตรวจความครบก่อน submit/award — ผู้ขาย ≥ 2, ทุก line มีผู้ชนะ, ราคาผู้ชนะ > 0
- **Input:** `{ comparison_id }`
- **Output:** `true | ValidationError[]`
- **Invoked by:** FN-06, FN-09, F-CP-001-API-03 (save_mode=pending)
- **Calls:** — · **Error cases:** BR_CP_MIN_VENDORS, BR_CP_WINNER_INCOMPLETE · **Iron rule check:** ✅

### F-CP-001-FN-06: `submitComparison`
- **Purpose:** เปลี่ยน draft→pending + resolve สายอนุมัติ DOA + notify
- **Input:** `{ comparison_id, actor_id, expected_version }`
- **Output:** `{ status:'pending', approval_chain[] }`
- **Invoked by:** F-CP-001-API-05, F-CP-001-API-03 (save_mode=pending)
- **Calls:** FN-05 validate, ENG-04 doa-approval-resolver
- **Side effects:** status→pending, submitted_at, emit `cp_submitted_event`, audit
- **Error cases:** BR_CP_WINNER_INCOMPLETE, ERR_STALE_DATA · **Iron rule check:** ✅

### F-CP-001-FN-07: `approveComparison`
- **Purpose:** pending→approved (ตรวจ actor อยู่ในชั้น DOA ปัจจุบัน)
- **Input:** `{ comparison_id, actor_id, expected_version }`
- **Output:** `{ status:'approved', approved_at, approved_by }`
- **Invoked by:** F-CP-001-API-06
- **Calls:** ENG-04 (verify actor ในชั้น) · **Side effects:** status→approved, emit `cp_approved_event`, audit
- **Error cases:** BR_CP_NOT_PENDING, ERR_INSUFFICIENT_ROLE, ERR_STALE_DATA (EC-01) · **Iron rule check:** ✅

### F-CP-001-FN-08: `rejectComparison`
- **Purpose:** pending→draft + บันทึกเหตุผล + notify maker
- **Input:** `{ comparison_id, actor_id, reject_reason }`
- **Output:** `{ status:'draft', reject_reason }`
- **Invoked by:** F-CP-001-API-07
- **Calls:** — · **Side effects:** status→draft, reject_reason, emit `cp_rejected_event`, audit
- **Error cases:** ERR_REASON_REQUIRED, BR_CP_NOT_PENDING · **Iron rule check:** ✅

### F-CP-001-FN-09: `awardComparison`
- **Purpose:** approved→awarded — สร้าง PO ต่อ split ผ่าน F-PO-001 + รับ po_id กลับ (idempotent)
- **Input:** `{ comparison_id, actor_id, idempotency_key, expected_version }`
- **Output:** `{ status:'awarded', po_splits:[{vendor_id, po_id, subtotal}] }`
- **Invoked by:** F-CP-001-API-08
- **Calls:** ENG-02 po-split (final payload), F-PO-001 createPurchaseOrder (external)
- **Side effects:** status→awarded, awarded_at, UPDATE po_split.po_id, emit `cp_awarded_event`, audit
- **Error cases:** BR_CP_NOT_APPROVED, ERR_PO_CREATE_FAILED (EC-07), ERR_DUPLICATE_IDEMPOTENCY_KEY (EC-06)
- **Iron rule check:** ✅ (เรียก PO ผ่าน service interface ไม่ใช่ HTTP req/res โดยตรง)

### F-CP-001-FN-10: `exportComparisonsCsv`
- **Purpose:** สร้าง CSV (UTF-8 BOM) ตาม filter — ตัดคอลัมน์ Confidential ถ้า role ไม่ผ่าน
- **Input:** `{ filter, role }`
- **Output:** `CsvBlob`
- **Invoked by:** F-CP-001-API-09 · **Calls:** FN-04 · **Side effects:** audit export · **Iron rule check:** ✅

### F-CP-001-FN-11: `buildComparisonDocument`
- **Purpose:** ประกอบข้อมูล CP → bind ลง CP_template.html → render PDF (A4)
- **Input:** `{ comparison_id }`
- **Output:** `PdfBuffer`
- **Invoked by:** F-CP-001-API-10
- **Calls:** ENG-02 (split summary), baht_text helper · **Side effects:** audit (Confidential pricing) · **Iron rule check:** ✅

---

## §3.2 Engines (Reusable / CUBIC-Registered)

> Naming: kebab-case · CUBIC Engine Entity schema

---

### F-CP-001-ENG-01: `price-comparison-winner-engine` [NEW]

| Field | Value |
|---|---|
| id | (assigned at CUBIC registration) |
| code | `price-comparison-winner-engine` |
| name | Price Comparison Winner Selection Engine |
| category | matcher / calculation |
| status | DRAFT |
| owner | F-CP-001 |

**Input Schema:**
```json
{ "lines":[{"line_no":1,"qty":50}], "quotes":[{"line_no":1,"vendor_id":"V-001","unit_price":125}], "overrides":{"1":"V-001"} }
```
**Output Schema:**
```json
{ "winners":{"1":{"vendor_id":"V-001","unit_price":125}}, "lowest":{"1":"V-001"}, "winner_total":13700.00 }
```
**Logic Outline:**
1. ต่อ line: หา lowest unit_price จาก quotes (ข้าม null)
2. ถ้ามี override → ใช้ override vendor (เก็บ flag ว่าไม่ใช่ lowest)
3. คำนวณ winner_price × qty → line winner amount
4. Σ ทุก line → winner_total
5. mark lowest per line (สำหรับป้าย "ต่ำสุด" ใน UI)

**Used by features:** F-CP-001 (current) · F-RFQ-xxx (planned e-bidding)
**Iron rule check:** ✅ pure · ✅ reusable · ✅ algorithm ชัด
**CUBIC Registration:** DRAFT → register ตอน dev hand-off (ดู LD-02)

---

### F-CP-001-ENG-02: `po-split-engine` [NEW]

| Field | Value |
|---|---|
| code | `po-split-engine` · category: generation · status: DRAFT · owner: F-CP-001 |

**Input Schema:**
```json
{ "lines":[{"line_no":1,"item_code":"PPR-A4","qty":50,"unit":"รีม","winner_vendor_id":"V-001","winner_price":125}] }
```
**Output Schema:**
```json
{ "splits":[{"vendor_id":"V-001","vendor_name":"บจก. สยามออฟฟิศ ซัพพลาย","line_count":2,"subtotal":9050.00,"lines":[...]}], "po_count":2 }
```
**Logic Outline:**
1. group lines ตาม `winner_vendor_id`
2. ต่อกลุ่ม: line_count = lines.length · subtotal = Σ(qty × winner_price)
3. คืน splits[] (1 vendor = 1 PO) + po_count
4. (final mode ตอน award) แนบ payload ให้ F-PO-001 สร้าง PO

**Used by features:** F-CP-001 (current) · F-PO-001 (consume payload)
**Iron rule check:** ✅ pure · ✅ reusable · ✅ algorithm ชัด
**CUBIC Registration:** DRAFT

---

### F-CP-001-ENG-03: `vendor-price-list-resolver` [EXISTING/SHARED]

| Field | Value |
|---|---|
| code | `vendor-price-list-resolver` · category: lookup · status: EXISTING (Master — Vendor Price List) · owner: shared |

**Input Schema:** `{ "vendor_id":"V-001", "item_code":"PPR-A4" }`
**Output Schema:** `{ "unit_price": 125 | null, "effective_date":"2026-01-01" }`
**Logic Outline:**
1. lookup T_vendor_price ตาม (tenant, vendor_id, item_code)
2. คืนราคา effective ล่าสุด หรือ null ถ้าไม่มี
3. CP ใช้เติม preset (is_preset=true) ในเซลล์ที่ว่าง — แก้ไขได้ (BR-CP-04)

**Used by features:** F-PR-001, F-CP-001, F-PO-001 (shared lookup)
**Iron rule check:** ✅ pure lookup · ✅ reusable 3+ features
**CUBIC Registration:** EXISTING (อ้าง engine id ที่ register แล้ว — ดู LD-03)

---

### F-CP-001-ENG-04: `doa-approval-resolver` [EXISTING/SHARED]

| Field | Value |
|---|---|
| code | `doa-approval-resolver` · category: governance · status: EXISTING (shared CUBIC) · owner: shared (Policy Center — DOA) |

**Input Schema:** `{ "feature_id":"F-CP-001", "cost_center":"...", "amount": 13700.00 }`
**Output Schema:** `{ "chain":[{"tier":1,"role":"proc_manager"},{"tier":2,"role":"approver","person_id":"..."}] }`
**Logic Outline:**
1. resolve cost center + amount → DOA matrix
2. คืนสายอนุมัติ (ชั้น + role + ผู้อนุมัติ) — **ไม่ hardcode**
3. CP ใช้กำหนดผู้เซ็น (tab ลายเซ็น) + ตรวจสิทธิ์ตอน approve

**Used by features:** F-PR-001, F-CP-001, F-PO-001, ทุก feature ที่มี approval
**Iron rule check:** ✅ pure resolver · ✅ reusable (governance shared)
**CUBIC Registration:** EXISTING — **ห้าม hardcode approval rule** (Approval Pattern standard)

---

## §3.3 API ↔ Logic Trace Table (R8 Anchor)

| API ID | Method | Path | Calls Functions | Calls Engines |
|---|---|---|---|---|
| F-CP-001-API-01 | GET | /comparisons | FN-04 | — |
| F-CP-001-API-02 | GET | /comparisons/:id | FN-04 | — |
| F-CP-001-API-03 | POST | /comparisons | FN-01, FN-03, FN-05*, FN-06* | ENG-01, ENG-02, ENG-03, ENG-04* |
| F-CP-001-API-04 | PUT | /comparisons/:id | FN-02 | ENG-01, ENG-02, ENG-03 |
| F-CP-001-API-05 | POST | /submit | FN-05, FN-06 | ENG-04 |
| F-CP-001-API-06 | POST | /approve | FN-07 | ENG-04 (verify) |
| F-CP-001-API-07 | POST | /reject | FN-08 | — |
| F-CP-001-API-08 | POST | /award | FN-09 | ENG-02 |
| F-CP-001-API-09 | GET | /export | FN-10 | — |
| F-CP-001-API-10 | GET | /document | FN-11 | ENG-02 |

> `*` = เฉพาะเมื่อ save_mode=pending (API-03)

### Trace Verification (Self-Check)
- [x] ทุก mutation API (03/04/05/06/07/08) มี ≥ 1 Function/Engine
- [x] ไม่มี orphan Function — FN-01..FN-11 ปรากฏใน trace ครบ
- [x] ไม่มี orphan Engine — ENG-01..04 ปรากฏใน trace ครบ
- [x] ไม่มี hidden logic ใน 02_API (CRUD/calc/lookup/governance อยู่ใน 03_LOGIC ตาม matrix)

---

## §3.4 Dependencies

### External Function/Engine called
- `vendor-price-list-resolver` (ENG-03) — Master Vendor Price List (existing)
- `doa-approval-resolver` (ENG-04) — Policy Center DOA (existing)
- `createPurchaseOrder` from F-PO-001 — เรียกตอน award (FN-09)
- read T_purchase_requisition — F-PR-001 (FN-03)

### External that calls into this feature
- F-PO-001 consume `po-split-engine` payload
- Report/Dashboard อ่าน winner_total / po_count

---

## §3.5 Open Questions / Locked Decisions Referenced
- LD-02: ENG-01 + ENG-02 register CUBIC ตอน dev hand-off (scope-local ก่อน)
- LD-03: ใช้ ENG-03/ENG-04 ที่ register แล้ว (shared) ไม่สร้างใหม่
- OQ-01: award partial failure (F-PO-001 บางใบ fail) → policy ใน FN-09 (ดู 05_RULES EC-07)
- OQ-04: winner override บันทึกเหตุผลไหม → ENG-01 เก็บ flag ไว้แล้ว, ส่วน reason รอ decision

---

## Audience Cheat-Sheet
| Reader | Read |
|---|---|
| BE dev | §3.1 + §3.2 + §3.3 |
| QA | §3.3 + FN side effects + ENG I/O |
| Architect / CUBIC | §3.2 (ENG-01/02 DRAFT register) + §3.4 |
| PM | §3.3 (coverage) |
