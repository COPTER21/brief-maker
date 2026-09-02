# Example: STANDARD Variant Walkthrough — F-02 Product Catalog Management

> **Purpose:** Concrete STANDARD example — แสดงจุดที่ต่างจาก LEAN (มี 05_RULES + ≤ 2 Engines) และจุดที่ต่างจาก FULL (ไม่มี 07_LOCKED + INDEX, ไม่มี state machine)
> **Scenario:** Product CRUD พร้อม category hierarchy + auto-calc selling price จาก cost + margin
> **Why STANDARD (not LEAN):** มี business rules > 5 ข้อ + 1 engine (price calculator) + Edge cases หลายตัว
> **Why STANDARD (not FULL):** ไม่มี state machine, ไม่มี multi-step approval, engines ≤ 2

---

## Input Summary

**Brief §3.4 Generator Hints:**
- complexity: **Medium**
- has-state: **No** (status เป็น flag ธรรมดา active/inactive ไม่ใช่ state machine)
- has-entity: **Yes** (Product, Category)
- has-approval: **No**
- multi-tenant: **Yes**
- PII: **No**
- financial: **Partial** (price/cost — sensitivity audit required)

**BRD §14.6 Screen Inventory (หยาบ — v2.1):**
- 3 pages (List, Detail/Edit, Category Tree side-panel)
- ERP feature: YES (Sidebar context: Inventory > Products)
- ประเภทหยาบ: หน้ารายการ / รายละเอียด+แก้ไข / side tree — **pattern ตัดสินที่ Phase 1.5** → A / C / L (Layout Decision Log ใน 01_UI §1.0)

**Phase 0 decision tree:**
```
Q1 complexity=Critical? → NO
Q2 has-state=Yes?       → NO
Q3 multi-engine (≥3)?   → NO (estimate: 1 engine)
Q4 multi-step approval? → NO
Q5 Low + has-entity=No? → NO (has-entity=Yes)
→ STANDARD (7 files)
```

---

## Generated Pack Structure

```
FRD_F-02_Product_Catalog_Pack/
├── 00_OVERVIEW.md          75 lines
├── 01_UI.md                180 lines (3 pages)
├── 02_API.md               220 lines (5 endpoints)
├── 03_LOGIC.md ⭐          165 lines (6 functions + 1 engine)
├── 04_DB.md                95 lines (3 tables)
├── 05_RULES.md ⭐ NEW vs LEAN  140 lines (8 rules + 6 edge cases)
└── 06_TESTS.md             110 lines (12 ACs)

ไม่มี: 07_LOCKED_DECISIONS, INDEX  (STANDARD ใส่ใน 00_OVERVIEW §Open Decisions แทน)
```

---

## Phase 2.5 — Edge Case Probes Activated

จาก `references/edge-case-probes.md` STANDARD ปกติเปิด 3-5 probes:

| Probe | Why activated | Outcome |
|---|---|---|
| **PR-2** Duplicate handling | has-entity=Yes + Product SKU | → BR-03 unique SKU per tenant |
| **PR-3** Soft-delete | has-entity=Yes + ไม่ระบุ hard-delete | → Soft delete + archive flag |
| **PR-4** Bulk operations | inventory feature ปกติมี bulk | → Out of scope — flag ใน 00_OVERVIEW OQ-02 |
| **PR-7** Concurrent edit | multi-tenant + ของแชร์ | → BR-07 optimistic lock (version field) |

---

## File Highlights

### 03_LOGIC.md — Heart of STANDARD (functions + 1 engine)

```markdown
# 03_LOGIC — F-02 Product Catalog Management

## §3.1 Functions (Scope-Local) — 6 functions

### F-02-FN-01: createProduct
- **Purpose:** สร้าง product ใหม่ + validate uniqueness + auto-calc price ถ้ามี cost+margin
- **Input:** `{ sku, name, category_id, cost, margin_pct?, manual_price?, tenant_id }`
- **Output:** `Product | ValidationError[]`
- **Invoked by:** F-02-API-02 POST /products
- **Calls:** F-02-FN-04 (validate), ENG-011 (calculate price if manual_price null)
- **Side effects:** INSERT T_product, INSERT T_audit_log
- **Error cases:** BR_DUPLICATE_SKU, BR_INVALID_CATEGORY, BR_MARGIN_OUT_OF_RANGE
- **Iron rule check:** ✅ no HTTP terms

### F-02-FN-02: updateProduct
- **Purpose:** แก้ไข product (optimistic lock + audit)
- **Input:** `{ id, version, ...fields, tenant_id }`
- **Output:** `Product | ConflictError | ValidationError[]`
- **Invoked by:** F-02-API-03 PUT /products/:id
- **Calls:** F-02-FN-04, ENG-011 (if cost/margin changed)
- **Side effects:** UPDATE T_product (WHERE version = ?), INSERT T_audit_log
- **Error cases:** ERR_VERSION_CONFLICT (BR-07), BR_INVALID_CATEGORY

### F-02-FN-03: softDeleteProduct
- **Purpose:** Soft delete (set archived=true, archived_at)
- **Input:** `{ id, tenant_id, reason? }`
- **Output:** `void | NotFoundError`
- **Invoked by:** F-02-API-05 DELETE /products/:id
- **Side effects:** UPDATE T_product SET archived=true, audit log

### F-02-FN-04: validateProductData
- **Purpose:** ตรวจ SKU format + category exists + margin range + duplicate
- **Input:** `{ sku, category_id, margin_pct?, tenant_id, exclude_product_id? }`
- **Output:** `ValidationResult`
- **Invoked by:** F-02-FN-01, F-02-FN-02
- **Side effects:** — (pure read, no mutation)
- **Error cases:** BR_INVALID_SKU_FORMAT, BR_DUPLICATE_SKU, BR_INVALID_CATEGORY, BR_MARGIN_OUT_OF_RANGE

### F-02-FN-05: buildProductListQuery
- **Purpose:** Build filter+sort+paginate query สำหรับ list page
- **Input:** `{ filters: {category?, search?, archived?}, sort, page, page_size }`
- **Output:** SQL query object
- **Invoked by:** F-02-API-01 GET /products

### F-02-FN-06: getCategoryTree
- **Purpose:** ดึง category tree (parent-child) สำหรับ side panel + dropdown
- **Input:** `{ tenant_id }`
- **Output:** `CategoryNode[]` (hierarchical)
- **Invoked by:** F-02-API-04 GET /categories/tree
- **Side effects:** — (pure read)

---

## §3.2 Engines (Reusable) — 1 engine

### ENG-011: product-pricing-engine [NEW]

| Field | Value |
|---|---|
| code | `product-pricing-engine` |
| name | Product Pricing Engine |
| category | financial-calculation |
| status | DRAFT |
| owner | F-02 |

**Input Schema:**
```json
{
  "cost": "number",
  "margin_pct": "number (0-1000)",
  "rounding_rule": "string (nearest_5 | nearest_10 | exact)"
}
```

**Output Schema:**
```json
{
  "selling_price": "number",
  "calculated_margin_thb": "number",
  "rounding_applied": "boolean"
}
```

**Logic Outline:**
1. `gross = cost × (1 + margin_pct/100)`
2. Apply rounding rule (default: nearest_5)
3. Calculate actual margin in THB after rounding
4. Return breakdown

**Used by features:**
- F-02 (current — Product Catalog)
- F-07 (planned — Bundle Pricing, Q3 backlog)

**Iron rule check:**
- [x] ✅ Pure — input/output ชัด, no I/O
- [x] ✅ Reusable — F-07 จะใช้ + อาจ reuse ใน promotion calc
- [x] ✅ Substantial — มี rounding algorithm + breakdown logic

**CUBIC Registration note:**
- DRAFT → register ตอน F-02 deploy → F-07 reuse engine id

---

## §3.3 API ↔ Logic Trace Table (R8 Anchor)

| API ID | Method | Path | Calls Functions | Calls Engines |
|---|---|---|---|---|
| F-02-API-01 | GET | /products | F-02-FN-05 | — |
| F-02-API-02 | POST | /products | F-02-FN-01, F-02-FN-04 | ENG-011 |
| F-02-API-03 | PUT | /products/:id | F-02-FN-02, F-02-FN-04 | ENG-011 |
| F-02-API-04 | GET | /categories/tree | F-02-FN-06 | — |
| F-02-API-05 | DELETE | /products/:id | F-02-FN-03 | — |

### Trace Verification
- [x] All mutation APIs (POST/PUT/DELETE) have ≥ 1 Function ✅
- [x] No orphan Function — FN-01 to FN-06 ทุกตัวอยู่ใน trace ✅
- [x] ENG-011 traced via FN-01, FN-02 ✅
- [x] No hidden logic in 02_API ✅
```

### Why Pricing Got an Engine (Not Just a Function)

**Function vs Engine tie-breaker check:**

| Criteria | Result |
|---|---|
| Pure (no I/O, no HTTP)? | ✅ YES (cost, margin → price) |
| Reusable 2+ features? | ✅ YES (F-02 now + F-07 planned) |
| Substantial (> 20 lines / named algorithm)? | ✅ YES (rounding rule algorithm) |
| **Score:** | **3/3 → Engine** |

ถ้าเป็นแค่ `gross = cost × (1+margin)` ตรงๆ ไม่มี rounding → จะเป็น Function ใน §3.1 แทน

---

### 05_RULES.md — STANDARD-only file (LEAN ไม่มี)

นี่คือ **ความแตกต่างหลักจาก LEAN** — STANDARD แยก rules ออกมาเป็นไฟล์เพราะ:
- มี business rules > 5 ข้อ ที่ QA ต้องใช้แยก test
- มี edge cases ที่ต้อง audit ตรวจสอบเป็นรายการ

```markdown
# 05_RULES — F-02 Product Catalog Management

## §5.1 Business Rules

### BR-01: SKU Format
- Pattern: `^[A-Z]{2,4}-\d{4,6}$` (e.g. `ELEC-12345`)
- ใช้ใน: F-02-FN-04 validateProductData

### BR-02: SKU Uniqueness
- Unique per tenant (not global)
- DB constraint: UNIQUE (tenant_id, sku)
- Error: ERR_DUPLICATE_SKU (409)

### BR-03: Category must exist + active
- category_id must reference T_category WHERE archived = false
- Error: BR_INVALID_CATEGORY

### BR-04: Margin Range
- margin_pct ∈ [0, 1000] (เปอร์เซ็นต์, รองรับขายแพง 10x)
- ถ้านอกช่วง → BR_MARGIN_OUT_OF_RANGE

### BR-05: Manual Price Override
- ถ้า manual_price ระบุมา → ไม่เรียก ENG-011 (skip auto-calc)
- ถ้า manual_price = null AND cost + margin มี → เรียก ENG-011

### BR-06: Rounding Default
- Default rounding_rule = "nearest_5" (ลงท้าย 5 หรือ 0)
- Configurable per tenant ใน settings (out of scope this feature)

### BR-07: Optimistic Lock (PR-7 outcome)
- PUT /products/:id ต้องส่ง version field
- ถ้า version ไม่ตรง DB → 409 ERR_VERSION_CONFLICT

### BR-08: Soft Delete Behavior
- DELETE /products/:id = soft delete (archived=true)
- GET /products?archived=true ถึงจะเห็น
- ไม่มี hard delete ใน feature นี้

---

## §5.2 Edge Cases (Probe Outcomes)

### EC-01: Create with cost=0 + margin > 0
- Behavior: ENG-011 returns selling_price = 0 (cost × anything = 0)
- Decision: allow (Free sample SKU pattern)

### EC-02: Update only category (no price change)
- ไม่เรียก ENG-011 (price ไม่เปลี่ยน)
- Optimization: skip engine call if cost+margin ไม่อยู่ใน update fields

### EC-03: Concurrent update of same product
- PR-7 outcome: optimistic lock via version field
- User retry ด้วย version ใหม่

### EC-04: Delete product ที่อยู่ใน open Sales Order
- Out of scope this feature
- Flag ใน 00_OVERVIEW OQ-03 (cross-feature check at F-05 SO)

### EC-05: Category being archived while product still references it
- Out of scope this feature (handled in F-08 Category Management)
- ปัจจุบัน BR-03 check archived=false ตอนสร้าง/แก้ product เท่านั้น

### EC-06: Bulk import / export
- Out of scope (PR-4 ปิดไว้)
- OQ-02 ใน 00_OVERVIEW

---

## §5.3 Error Catalog

| Code | HTTP | Source | Message |
|---|---|---|---|
| ERR_VALIDATION_FAILED | 400 | API layer | Generic field validation |
| BR_INVALID_SKU_FORMAT | 422 | FN-04 | SKU format invalid (see BR-01) |
| BR_DUPLICATE_SKU | 409 | FN-04 + DB | SKU exists for this tenant |
| BR_INVALID_CATEGORY | 422 | FN-04 | Category not found or archived |
| BR_MARGIN_OUT_OF_RANGE | 422 | FN-04 | Margin must be 0-1000% |
| ERR_VERSION_CONFLICT | 409 | FN-02 | Product was modified by another user |
| ERR_NOT_FOUND | 404 | FN-03 | Product not found |
```

---

## Phase 3.5 Verification Report (sample output)

```markdown
## 🔍 Phase 3.5 Verification — FRD F-02

### A. Pack Completeness
- [x] Variant = STANDARD ตรงกับ Brief §3.4 ✅
- [x] 7 files generated (00, 01, 02, 03, 04, 05, 06) ✅
- [x] 03_LOGIC.md exists (R9) ✅
- [x] No INDEX.md (STANDARD skip) ✅

### B. Function/API Coverage
- [x] 5 APIs in 02_API ✅
- [x] All Contract Blocks complete ✅

### C. R8 Logic Traceability ⭐
- [x] 3 mutation APIs (POST, PUT, DELETE) all have Function trace ✅
- [x] 2 read APIs (GET list, GET tree) have Function trace ✅
- [x] All 6 Functions in §3.1 appear in trace table ✅
- [x] ENG-011 traced via FN-01 + FN-02 ✅
- [x] No orphan ✅

### D. API ↔ DB Linkage
- [x] All APIs reference T_product / T_category from 04_DB ✅
- [x] T_audit_log mentioned in side effects ✅

### E. UI ↔ API Cross-reference
- [x] P-01 List → API-01 ✅
- [x] P-02 Detail Save → API-02 (create) / API-03 (update) ✅
- [x] P-02 Delete button → API-05 ✅
- [x] P-03 Category Tree → API-04 ✅

### F. Engine Iron Rules
- [x] ENG-011 — pure, no HTTP terms ✅
- [x] Input/output = plain objects ✅
- [x] API → Engine via Function (no direct UI→Engine bypass) ✅

### G. Logic Placement Compliance ⭐
- [x] No `createX` แอบใน 02_API → ทั้งหมดอยู่ใน 03_LOGIC §3.1 ✅
- [x] Pricing calculation อยู่ใน ENG-011 (ไม่อยู่ใน API spec) ✅
- [x] BR-04 margin range = declarative ใน 05_RULES (ไม่ปนใน API) ✅
- [x] Matrix #1-10 compliance ✅

### H. Security Bible Application
- [x] Multi-tenant trigger → tenant_id ทุก query + RLS ✅
- [x] Audit log trigger (financial-adjacent) → T_audit_log ทุก mutation ✅
- [x] PII trigger → SKIPPED (no PII in product master) ✅

### I. Convention Compliance
- API path = kebab plural (`/products`, `/categories`) ✅
- field_key = snake_case ✅
- Function code = camelCase ✅
- Engine code = kebab-case (`product-pricing-engine`) ✅
- Error code = UPPER_SNAKE (`BR_INVALID_CATEGORY`) ✅

### Verdict
✅ All checks passed → deliver Pack
```

---

## 🎯 Key Differences vs LEAN (same feature hypothetically)

If we tried to force this feature into LEAN, here's what would break:

| Concern | LEAN attempt | STANDARD correct |
|---|---|---|
| **05_RULES.md** | ❌ Rules embed ใน 02_API + 03_LOGIC FN spec | ✅ แยกชัด — QA ใช้ test ตามรายการ |
| **Edge cases** | ❌ ปนใน Open Questions | ✅ §5.2 explicit list |
| **Engine** | ❌ ENG-011 ถูกบีบไปอยู่ใน FN-01 (lose reusability) | ✅ §3.2 properly registered + F-07 reuse |
| **Error catalog** | ❌ scattered ในแต่ละ FN | ✅ §5.3 single source of truth |
| **Audit-ability** | ❌ business rule ดู spec ยาก | ✅ BR-NN listed clearly |

**Trigger ที่บอกว่าต้อง upgrade จาก LEAN → STANDARD:**
- Business rules > 5 ข้อ → BR-01 ถึง BR-08
- มี engine ≥ 1 → ENG-011
- มี optimistic lock / concurrent concern → PR-7 outcome
- Soft delete behavior ที่ต้อง audit → BR-08

---

## 🎯 Key Differences vs FULL (why not upgrade)

If we tried to bump this to FULL, here's what's NOT needed:

| FULL-only artifact | Why F-02 doesn't need it |
|---|---|
| **07_LOCKED_DECISIONS.md** | OQ-01, OQ-02, OQ-03 อยู่ใน 00_OVERVIEW ก็พอ (3 items) |
| **INDEX.md** | 7 ไฟล์ navigate ตรง folder ก็เจอ ไม่ต้อง quick nav |
| **State machine section** | status = active/inactive flag, ไม่ใช่ state machine |
| **Multi-step approval** | ไม่มี approval ใน feature นี้ |
| **3+ engines** | มี engine เดียว (ENG-011) |

**Trigger ที่จะบอกว่าต้อง upgrade STANDARD → FULL:**
- ถ้าเพิ่ม "Product Approval workflow" → has-state=Yes → FULL
- ถ้าเพิ่ม Bulk Import → engines ≥ 3 (import-parser, validator, batch-processor) → FULL
- ถ้า Locked Decisions > 3 ข้อ → FULL

---

## What This Pack Enables (Downstream)

### html-generator-v9
อ่าน 01_UI.md → render 3 pages พร้อม:
- P-01 List with filter (BR-08 soft delete toggle)
- P-02 Detail Edit with optimistic lock indicator (BR-07)
- P-03 Category tree (FN-06)

### ai-testcase-md-generator + qa-friendly-html-generator (SOW3.5)
อ่าน 05_RULES + 06_TESTS + 02_API + 03_LOGIC → produces:
- TC pack: ≥ 12 cases (covering BR-01 ถึง BR-08 + EC-01 ถึง EC-06)
- SCN pack: 5 scenarios (happy path + 4 error paths)
- DATA pack: test fixtures พร้อมรหัส error mapping

### Dev hand-off
- FE dev: 01_UI.md only (180 lines)
- BE dev (HTTP): 02_API.md + §3.3 Trace Table (220 + 25 lines)
- BE dev (logic): 03_LOGIC.md + 05_RULES.md (165 + 140 lines)
- DBA: 04_DB.md (95 lines)
- QA: 05_RULES.md + 06_TESTS.md (140 + 110 lines)

---

## 🚨 Anti-Patterns Caught by v5 (specific to STANDARD)

### AP-1 (caught): Pricing logic แอบใน 02_API
```
❌ v4 might have written:
02_API.md F-02-API-02:
  Logic: "Calculate selling_price = cost × (1+margin/100), round to nearest 5..."

✅ v5 forces:
03_LOGIC.md §3.2 ENG-011 product-pricing-engine (full spec)
02_API.md F-02-API-02:
  Calls: F-02-FN-01 → ENG-011
```

### AP-3 (caught): Margin range constant ใน 02_API
```
❌ Wrong:
02_API.md: "validate margin between 0-1000"

✅ v5 forces:
05_RULES.md BR-04: margin_pct ∈ [0, 1000]
02_API.md: "validate against BR-04"
```

### AP-4 (avoided): Orphan function check
```
ตอนแรก FN-06 getCategoryTree เกือบเป็น orphan เพราะลืม trace
Phase 3.5 Section C จับได้ → กลับไป update §3.3 ก่อน deliver ✅
```

---

## 🎓 Lessons Learned (for BA team)

1. **STANDARD = "ของจริงในชีวิตประจำวัน"** — feature ส่วนใหญ่ใน CUBE NATIVE จะเป็น STANDARD (Product, Customer, Vendor, Invoice without approval, simple master data)

2. **อย่ารีบ upgrade เป็น FULL** — ถ้าไม่มี state machine จริง / multi-step approval / 3+ engines → ใช้ STANDARD พอ ประหยัด LD + INDEX overhead

3. **05_RULES.md เป็น artifact ที่ QA รัก** — แยกรายการ BR + EC + Error code ทำให้ test case generator ทำงานง่าย

4. **Engine แม้แค่ตัวเดียวก็คุ้ม** — ENG-011 product-pricing-engine จะ reuse ใน F-07 Bundle Pricing ทันที (CUBIC win)

5. **Optimistic lock (BR-07) เป็น STANDARD pattern** — feature ใดที่มี multi-user edit → expect to add version field

---

## File-by-File Quick Stats

| File | Lines | Sections | Key content |
|---|---|---|---|
| 00_OVERVIEW.md | 75 | 5 | 3 Open Questions, scope, roles |
| 01_UI.md | 180 | 3 pages × 5 sections | Layout Decision Log §1.0: A · C · L |
| 02_API.md | 220 | 5 endpoints | HTTP-only, refer to §3.3 for logic |
| 03_LOGIC.md | 165 | §3.1 (6 FN) + §3.2 (1 ENG) + §3.3 trace | Heart of pack |
| 04_DB.md | 95 | 3 tables (product, category, audit) | RLS + unique constraints |
| 05_RULES.md | 140 | §5.1 (8 BR) + §5.2 (6 EC) + §5.3 errors | QA's main reference |
| 06_TESTS.md | 110 | 12 AC + DoD | Maps to BR + EC |

**Total Pack:** ~985 lines · 7 files · ~35 KB

---

## ✅ Why This Example Is Useful

- **Most common variant** ที่ BA ในทีมเขียนบ่อยที่สุด (ประมาณ 60% ของ features ใน CUBE NATIVE backlog)
- **Borderline case** ทั้งทาง LEAN และ FULL — แสดงเหตุผลของ decision tree ชัดเจน
- **Real-world tradeoffs** — มี 1 engine (justify ทำไม), มี optimistic lock (มาจาก PR-7), soft delete (PR-3)
- **Convention showcase** — naming, error codes, ID conventions ครบ
