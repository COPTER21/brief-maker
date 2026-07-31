# 03_LOGIC — F-PRODUCT-MASTER-001 Product Master

> **Audience:** BE dev (business logic layer) · R8: mutation API → ≥1 Function/Engine ใน §3.3
> Reverse Mode: logic สกัดจาก JS จริงใน `product-master.html` — ชื่อ function ตรง prototype เพื่อ trace ง่าย

---

## §3.1 Functions (Scope-Local)

### F-PDM-FN-01: `buildProductQuery`
- **Purpose:** ประกอบ query list — search 7 fields (case-insensitive substring) + filter type/cat_l1/status + sort + paginate
- **Input:** `{ search?, type?, cat_l1?, status?, sort:{col,dir}, limit, offset, tenant_id }`
- **Output:** `{ rows: ProductListItem[], total, stats:{total,active,inactive,draft} }` — inactive = obsolete+discontinued
- **Invoked by:** API-01 · **Calls:** — · **Side effects:** — (read)
- **Iron rule check:** ✅ no HTTP terms

### F-PDM-FN-02: `createProductRecord`
- **Purpose:** สร้าง record ใหม่ (draft/active) จาก payload ที่ผ่าน validation แล้ว
- **Input:** `{ payload, activate:boolean, actor_id }`
- **Output:** `Product | ValidationError[]`
- **Invoked by:** API-03, FN-12 · **Calls:** FN-09 (code), FN-10 (defaults), FN-07, FN-08, FN-06 (เมื่อ activate)
- **Side effects:** INSERT T_product + children · audit `สร้างรายการ (v1)` (+`เปิดใช้งาน` success เมื่อ active)
- **Errors:** BR_CODE_DUPLICATE, BR_MINMAX_INVALID, BR_UOM_*, BR_NOT_READY

### F-PDM-FN-03: `amendProduct` (BR-S07)
- **Purpose:** แก้ record ตรง — version+1, ห้ามแตะ code (IR-01) / uom เมื่อ has_txn (IR-02)
- **Input:** `{ id, payload, expected_version, actor_id, activate?:boolean }`
- **Output:** `Product | Error`
- **Invoked by:** API-04 · **Calls:** FN-07, FN-08, FN-06 (draft+activate)
- **Side effects:** UPDATE + version+1 + modified_at · audit `แก้ไข (vN)`
- **Errors:** ERR_STALE_DATA (version mismatch), BR_CODE_IMMUTABLE, BR_UOM_LOCKED, BR_INVALID_STATE

### F-PDM-FN-04: `activateProduct`
- **Purpose:** draft → active หลังผ่าน gates (แทน submit+approve เดิม — [DOA-ENGINE placeholder])
- **Input:** `{ id, actor_id }` · **Output:** `{status:'active'} | Error`
- **Invoked by:** API-05 · **Calls:** FN-07, FN-06
- **Side effects:** status=active · audit `เปิดใช้งาน` (success)
- **Errors:** BR_INVALID_STATE (ไม่ใช่ draft), BR_MINMAX_INVALID, BR_NOT_READY

### F-PDM-FN-05: `transitionStatus` (FN-07 เดิมบนจอ — state machine)
- **Purpose:** เปลี่ยนสถานะตามตาราง transition (05 §5.2) พร้อม guard
- **Input:** `{ id, to: 'obsolete'|'discontinued'|'archived'|'active', actor_id }`
- **Output:** `{status} | Error`
- **Invoked by:** API-06 · **Calls:** FN-06 (เมื่อ to=active)
- **Side effects:** UPDATE status + modified_at · audit kind=status label ตามจอ (`เลิกผลิต (obsolete) — ขายสต็อกคงเหลือได้ งดซื้อ/ผลิตเพิ่ม` ฯลฯ) · to=archived + has_txn → append note `— มี transaction อ้างอิง`
- **Errors:** BR_INVALID_STATE, BR_NOT_READY

### F-PDM-FN-06: `validateActivationReady` (FN-10 เดิม)
- **Purpose:** gate ก่อน active — คืนรายชื่อ field ที่ขาด
- **Rules:** `standard_cost > 0` เว้น type EX/NS · `sellable → list_price > 0` · `stocked → prod_posting_group` required
- **Input:** `Product` · **Output:** `missing: string[]` (ว่าง = ผ่าน)
- **Invoked by:** FN-02/03/04/05 · **Errors → caller:** BR_NOT_READY `{missing}`

### F-PDM-FN-07: `validateMinMax` (VR-MM)
- **Purpose:** ตรวจ min/max stock — เฉพาะ stocked
- **Rules:** min ≥ 0 · max ≥ 0 · (min≠null ∧ max≠null) → max ≥ min
- **Output:** `error_code | null` → BR_MINMAX_INVALID
- **Invoked by:** FN-02/03/04, FN-11

### F-PDM-FN-08: `validateUomConversions` (VR-03/VR-04 + IR-02)
- **Purpose:** ตรวจชุดหน่วยแปลง: ไม่ซ้ำ base · หมวดเดียวกับ base (count/weight/volume จาก uom_master.category) · factor ≥ 1 · default เดี่ยว · has_txn → ปฏิเสธการเปลี่ยน base_uom/rows
- **Output:** `error_code | null` → BR_UOM_DUP_BASE / BR_UOM_CROSS_CATEGORY / BR_UOM_FACTOR / BR_UOM_LOCKED
- **Invoked by:** FN-02/03

### F-PDM-FN-09: `generateProductCode` (genCode)
- **Purpose:** `{TYPE}-{running}` — running = max ของ prefix นั้น +1 (ฐาน 1001) · **server-side เท่านั้น**
- **Concurrency (EC-06 [AI-DEFAULT]):** UNIQUE(tenant,code) + retry on conflict (สูงสุด 3)
- **Invoked by:** FN-02, FN-12

### F-PDM-FN-10: `applyTypeBehaviorDefaults` (FN-05 เดิม / setType)
- **Purpose:** set stocked/sellable/purchasable จาก TYPEMETA เมื่อสร้าง/เปลี่ยนประเภท (override ภายหลังได้) · create เท่านั้น: regen code เมื่อเปลี่ยน type
- **Invoked by:** FN-02 (+FE ใช้ mirror ฝั่ง client)

### F-PDM-FN-11: `bulkValidateRow`
- **Purpose:** ตรวจ 1 แถว import — required (code*, name_th*, type*, uom*) · type ใน TYPEMETA · code ไม่ซ้ำ (รวมในไฟล์เดียวกัน) · VR-MM
- **Output:** `error_code | null` → BR_REQUIRED / BR_BAD_TYPE / BR_CODE_DUPLICATE / BR_MINMAX_INVALID
- **Invoked by:** FN-12

### F-PDM-FN-12: `bulkImportRows`
- **Purpose:** orchestrate import — validate ทุกแถว → commit เฉพาะแถวผ่านเป็น draft (partial, EC-05) → สรุป imported/skipped/errors
- **Side effects:** INSERT ×N + audit ต่อแถว `นำเข้าจากไฟล์ (bulk import)`
- **Invoked by:** API-07 · **Calls:** FN-11, FN-02, FN-09

---

## §3.2 Engines (Reusable / CUBIC)

> Feature นี้**ไม่ own engine** — logic ทั้งหมด scope-local
> **Downstream candidate (ไม่ใช่ของ feature นี้):**

### ENG-CANDIDATE: `stock-threshold-alert-engine` (ENG-STOCK-ALERT)
- **Owner:** Inventory Monitoring (consumer) — F-PDM เป็นแค่ **contract provider** (`PRODUCT_STOCK_THRESHOLD v1` — 02 §2.X)
- **Input (contract):** `{ product_id, min_stock, max_stock, uom_base }` + on-hand จากฝั่ง Inventory
- **Status:** CANDIDATE — register CUBIC โดย Architect (OQ-03) · ดู 07 LD-03

---

## §3.3 API ↔ Logic Trace Table (R8 anchor)

| API | Calls Functions | Calls Engines |
|---|---|---|
| F-PDM-API-01 GET /products | FN-01 | — |
| F-PDM-API-02 GET /products/:id | — (pure read + middleware gate) | — |
| F-PDM-API-03 POST /products | FN-02 (→ FN-09, FN-10, FN-07, FN-08, FN-06*) | — |
| F-PDM-API-04 PUT /products/:id | FN-03 (→ FN-07, FN-08, FN-06*) | — |
| F-PDM-API-05 POST /:id/activate | FN-04 (→ FN-06, FN-07) | — |
| F-PDM-API-06 POST /:id/status | FN-05 (→ FN-06 เมื่อ reactivate) | — |
| F-PDM-API-07 POST /bulk-import | FN-12 (→ FN-11, FN-02, FN-09) | — |

> **R8 check:** mutation ทุกตัว (03,04,05,06,07) มี ≥ 1 Function ✅ · orphan: ไม่มี (FN-01..12 ถูก trace ครบ; FN-10 ผ่าน FN-02)
