# 02_API — F-PRODUCT-MASTER-001 Product Master

> **Audience:** Backend developer (HTTP layer)
> **🚨 Iron Rule:** business logic > 5 บรรทัด → 03_LOGIC · **R8:** ทุก mutation ระบุ Calls (Logic)
> Common headers ทุก endpoint: `Authorization: Bearer` + `X-Tenant-Id`

---

## §2.1 API Overview

| ID | Method | Path | Summary | Roles |
|---|---|---|---|---|
| F-PDM-API-01 | GET | /api/v1/products | List + filter + sort + paginate | authenticated (pricing masked ตาม role) |
| F-PDM-API-02 | GET | /api/v1/products/:id | รายละเอียด (view 5 แท็บ) | authenticated |
| F-PDM-API-03 | POST | /api/v1/products | สร้าง (draft หรือ activate=true → active) | canManage |
| F-PDM-API-04 | PUT | /api/v1/products/:id | amend (version+1) | canManage · status ∈ draft/active/obsolete |
| F-PDM-API-05 | POST | /api/v1/products/:id/activate | draft → active | canManage |
| F-PDM-API-06 | POST | /api/v1/products/:id/status | transition: obsolete / discontinued / archived / active(reactivate) | canManage |
| F-PDM-API-07 | POST | /api/v1/products/bulk-import | นำเข้า CSV — per-row validate, partial commit | canManage |

> **Removed จาก v3.5:** submit-for-approval / approve / reject — ชั้นอนุมัติถอดออก (00 §0.3) · [DOA-ENGINE placeholder]

---

## §2.2 Per-API Contract

### F-PDM-API-01: GET /api/v1/products
**Query:** `search` (7 fields: code, old_code, name_th, name_en, gtin, description, cat/group) · `type` (enum 8) · `cat_l1` · `status` (5 ค่า) · `sort` (code|name_th|old_code|type|status|list_price ±) · `limit` (default 20) · `offset`
**Response 200:** `{ data:[ProductListItem], total, limit, offset, stats:{total,active,inactive,draft} }`
— `ProductListItem` รวม `conversions_count`, `cover_url` · **pricing fields ตัดออกจาก payload เมื่อ role ไม่ผ่าน `canSeePricing`** (mask ที่ server ไม่ใช่ UI)
**Errors:** 400 ERR_INVALID_QUERY_PARAMS · 401 · 403
**Calls (Logic):** F-PDM-FN-01 buildProductQuery

### F-PDM-API-02: GET /api/v1/products/:id
**Response 200:** full record + `uoms[]` + `images[]` + `attachments[]` + `audit[]` (desc) — pricing gate เดียวกับ API-01
**Errors:** 404 ERR_NOT_FOUND
**Calls:** — (read + gate ที่ middleware)

### F-PDM-API-03: POST /api/v1/products
**Headers:** `Idempotency-Key` (required — EC-02 [AI-DEFAULT])
**Body:** ทุก field ตาม 04_DB §4.2 (ยกเว้น computed/immutable) + `"activate": true|false`
- `code`: **server generate เสมอ** (F-PDM-FN-09) — client ส่งมาเพื่อ echo เท่านั้น ห้ามเชื่อ
**Validation (field-level):** name_th required · type enum · cat_l1 required · ตัวเลข ≥ 0 — complex → FN-06/07/08
**Response 201:** record ใหม่ (status = draft | active ตาม activate + gates)
**Errors:** 400 · 409 ERR_DUPLICATE_IDEMPOTENCY_KEY · 422 BR_CODE_DUPLICATE / BR_MINMAX_INVALID / BR_UOM_* / BR_NOT_READY (เมื่อ activate=true)
**Side effects:** INSERT T_product (+uoms/images/attachments) + audit `สร้างรายการ (v1)` (+ `เปิดใช้งาน` ถ้า active)
**Calls:** FN-02 createProductRecord · FN-09 generateProductCode · FN-10 applyTypeBehaviorDefaults · FN-07 validateMinMax · FN-08 validateUomConversions · FN-06 validateActivationReady (เมื่อ activate)

### F-PDM-API-04: PUT /api/v1/products/:id
**Headers:** `If-Match: <version>` (optimistic lock — EC-01 [AI-DEFAULT])
**Preconditions:** status ∈ {draft, active, obsolete} → อื่น 422 BR_INVALID_STATE · `has_txn` → ห้ามแตะ base_uom/uoms (422 BR_UOM_LOCKED)
**Body:** fields แก้ได้ (code immutable — ส่งมาต้องตรงเดิม ไม่งั้น 422 BR_CODE_IMMUTABLE)
**Response 200:** record (version+1)
**Errors:** 409 ERR_STALE_DATA · 422 BR_*
**Side effects:** UPDATE + version+1 + audit `แก้ไข (vN)` (+ `เปิดใช้งาน` ถ้า draft และ body.activate=true)
**Calls:** FN-03 amendProduct · FN-07 · FN-08 · FN-06 (เมื่อ activate)

### F-PDM-API-05: POST /api/v1/products/:id/activate
**Preconditions:** status = draft เท่านั้น → 422 BR_INVALID_STATE
**Gates:** FN-07 VR-MM → 422 BR_MINMAX_INVALID · FN-06 → 422 BR_NOT_READY `{missing:[...]}`
**Response 200:** `{ id, status:'active' }` · audit `เปิดใช้งาน` (success)
**Calls:** FN-04 activateProduct → FN-06, FN-07

### F-PDM-API-06: POST /api/v1/products/:id/status
**Body:** `{ "to": "obsolete" | "discontinued" | "archived" | "active" }`
**Transition guards (05_RULES §5.2):**
| to | จากได้เฉพาะ | เพิ่มเติม |
|---|---|---|
| obsolete | active | — |
| discontinued | obsolete | — |
| archived | active, discontinued | soft delete — `has_txn` → บันทึกหมายเหตุใน audit |
| active (reactivate) | obsolete | ต้องผ่าน FN-06 validateActivationReady |
**Errors:** 422 BR_INVALID_STATE · 422 BR_NOT_READY (reactivate)
**Side effects:** UPDATE status + modified_at + audit kind=status (label ตามจอ: `เลิกผลิต (obsolete)…` / `ยกเลิกถาวร (discontinued)…` / `จัดเก็บ (soft delete)` / `กลับมาใช้งาน (reactivate)`)
**Calls:** FN-05 transitionStatus (+FN-06 เมื่อ reactivate)

### F-PDM-API-07: POST /api/v1/products/bulk-import
**Headers:** `Idempotency-Key` required (EC-02)
**Body:** `{ rows:[{code?, name_th, type, uom, cat_l1, old_code?, name_en?, list_price?, min_stock?, max_stock?}] }` (จาก CSV parser ฝั่ง FE/BFF — คอลัมน์ตามจอ P-06)
**Behavior:** validate ต่อแถว (FN-11) — **partial commit** (EC-05, observed): แถวผ่าน → INSERT draft + audit `นำเข้าจากไฟล์ (bulk import)` · แถวผิด → รายงาน ไม่ล้มทั้งไฟล์ · `code` ว่าง → generate (FN-09)
**Response 200:** `{ imported: N, skipped: M, errors:[{row, code, name_th, error_code}] }`
**Errors ต่อแถว:** BR_REQUIRED / BR_BAD_TYPE / BR_CODE_DUPLICATE / BR_MINMAX_INVALID
**Calls:** FN-12 bulkImportRows → FN-11, FN-02, FN-09

---

## §2.3 Common Concerns
- **Idempotency (EC-02 [AI-DEFAULT]):** POST mutation ทั้งหมดรับ `Idempotency-Key` — cache 24h, same key+body → cached response, ต่าง body → 409
- **Optimistic locking (EC-01 [AI-DEFAULT]):** PUT ใช้ `If-Match: version` → mismatch 409 ERR_STALE_DATA
- **Multi-tenant:** `X-Tenant-Id` + RLS
- **Audit:** ทุก mutation → T_product_audit + T_audit_log กลาง (middleware)
- **Pricing gate:** middleware ตัด/mask Confidential fields ตาม `canSeePricing` — **enforcement ที่ server** (UI `•••` = presentation เท่านั้น)

## §2.4 API → Logic Trace (summary — authoritative ที่ 03 §3.3)

| API | Functions | Engines |
|---|---|---|
| API-01 | FN-01 | — |
| API-02 | — (read) | — |
| API-03 | FN-02, FN-09, FN-10, FN-07, FN-08, FN-06* | — |
| API-04 | FN-03, FN-07, FN-08, FN-06* | — |
| API-05 | FN-04 → FN-06, FN-07 | — |
| API-06 | FN-05 (+FN-06 reactivate) | — |
| API-07 | FN-12 → FN-11, FN-02, FN-09 | — |

> R8: mutation ทุกตัวมี ≥1 Function ✅ (* = เมื่อ activate)

## §2.X Cross-Module Contract ⭐

| Downstream | รูปแบบ | Contract | Trigger | Payload |
|---|---|---|---|---|
| **Inventory Monitoring** | Read contract + event | **`PRODUCT_STOCK_THRESHOLD v1`** | product active/amend ที่แตะ min/max → emit `product_threshold_changed_event` | `{ product_id, code, min_stock, max_stock, uom_base }` — null = ไม่เตือนด้านนั้น · เฉพาะ stocked · engine candidate `ENG-STOCK-ALERT` (owner ฝั่ง consumer — OQ-03 แจ้ง Architect) |
| BOM (F-BOM-001) | Endpoint (ปลายทางเรียก) | GET /products/:id (fields: code, standard_cost, base_uom, type, status) | on BOM line add | gate: parent=FG active, component=RM/PM/TR active |
| Inventory 4.0 | Data flag | `T_product_uom.is_stock_uom` | Multi-UOM bucket (future) | per-uom flag |
| Sales/Purchase | Endpoint | GET /products?status=active (picker) | doc line add | code/name/uom/prices (role-gated) |
| Policy Center DOA (future) | Placeholder | `approver_role/approved_by/approved_at` = null | เมื่อเสียบ engine | — (OQ-01) |

- **แก้/เลิกกลางทาง:** product → obsolete/discontinued → downstream picker ต้องกรองออก (status ≠ active) — test XT-02 · archive ไม่ลบ FK (soft) — ประวัติ doc เดิมอ้างได้ (XT-03)
