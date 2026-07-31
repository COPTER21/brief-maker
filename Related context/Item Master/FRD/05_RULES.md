# 05_RULES — F-PRODUCT-MASTER-001 Product Master

> **Audience:** Backend developer + QA · Declarative — อ่านแล้วเข้าใจโดยไม่ต้องดูโค้ด
> `[AI-DEFAULT]` = ตัดสินโดย probe default (Lane Mode) — รอ BA confirm (OQ-07)

---

## §5.1 Business Rules (BR)

### BR-PDM-01: รหัสสินค้าไม่ซ้ำ (BR-S01)
- **Statement:** `code` unique ต่อ tenant — ตรวจตอนสร้าง/import
- **Enforced by:** DB UNIQUE + FN-02/FN-11 · **Error:** `BR_CODE_DUPLICATE` → 422 · จอ: toast `รหัสสินค้าซ้ำ (CODE_DUPLICATE)`

### BR-PDM-02: รหัส immutable (IR-01)
- **Statement:** `code` แก้ไม่ได้หลังสร้าง — gen จากประเภท + เลขรัน (ฐาน 1001) server-side
- **Enforced by:** field readonly บนจอ + FN-03 reject · **Error:** `BR_CODE_IMMUTABLE` → 422

### BR-PDM-03: Multi-UOM (VR-03 / VR-04)
- **Statement:** หน่วยฐาน = หน่วยเล็กสุด · หน่วยแปลง factor ≥ 1 · ห้ามซ้ำ base · ห้ามข้ามหมวด (นับจำนวน/น้ำหนัก/ปริมาตร) · หน่วยเริ่มต้นเดี่ยว
- **Enforced by:** FN-08 + DB CHECK/UNIQUE · **Errors:** `BR_UOM_FACTOR` / `BR_UOM_DUP_BASE` / `BR_UOM_CROSS_CATEGORY` → 422
- **จอ:** step 2 toast เช่น "หน่วย X (…) คนละหมวดกับหน่วยฐาน …" / "จำนวนหน่วยฐานต้อง ≥ 1"

### BR-PDM-04: UOM lock เมื่อมี transaction (IR-02)
- **Statement:** `has_txn = true` → ห้ามแก้ base_uom + สูตรแปลงทั้งชุด (กันสต็อก/ต้นทุนเพี้ยน)
- **Enforced by:** FN-08 + UI disabled + `conv-locked-note` · **Error:** `BR_UOM_LOCKED` → 422

### BR-PDM-05: Activation gate
- **Statement:** เปิดใช้งานได้เมื่อ — `standard_cost > 0` (เว้น EX/NS) ∧ (`sellable → list_price > 0`) ∧ (`stocked → prod_posting_group`)
- **Enforced by:** FN-06 · **Error:** `BR_NOT_READY {missing}` → 422 · จอ: `ข้อมูลไม่พร้อมใช้งาน: <รายการ> (NOT_READY)` + เด้ง step 3

### BR-PDM-06: Min/Max stock (VR-MM · ENH-MINMAX)
- **Statement:** เฉพาะ stocked · min ≥ 0 · max ≥ 0 · max ≥ min · null = ไม่เตือนด้านนั้น · หน่วย = หน่วยฐาน
- **Enforced by:** FN-07 + DB CHECK · **Error:** `BR_MINMAX_INVALID` → 422 · จอ: `สต็อกสูงสุด (Max) ต้องไม่ต่ำกว่าขั้นต่ำ (Min) — MINMAX_INVALID` + เด้ง step 3
- **Downstream:** contract `PRODUCT_STOCK_THRESHOLD v1` (02 §2.X)

### BR-PDM-07: Amend = version+1 (BR-S07)
- **Statement:** แก้ได้เฉพาะ status draft/active/obsolete → UPDATE ตรง + `version+1` + audit — **ไม่มี re-approval** (ชั้นอนุมัติถอดออก)
- **Enforced by:** FN-03 + API-04 precondition · **Error:** `BR_INVALID_STATE` → 422

### BR-PDM-08: Soft delete เท่านั้น (BR-S06 / BR-002)
- **Statement:** ห้าม hard delete — archive = status change · `product_id` เป็น match key ของ transaction downstream · `has_txn` → บันทึกหมายเหตุใน audit
- **Enforced by:** ไม่มี DELETE endpoint + FN-05

### BR-PDM-09: Behavior defaults จากประเภท
- **Statement:** TYPEMETA กำหนด stocked/sell/buy ต่อประเภท (FG ✓✓✗ · RM ✓✗✓ · PM ✓✗✓ · CN ✓✓✓ · SV ✗✓✗ · TR ✓✓✓ · EX ✗✗✓ · NS ✗ sell:configurable buy:✓) — override รายตัวได้
- **Enforced by:** FN-10 (set ตอน create/เปลี่ยน type — ไม่ re-apply ตอน amend field อื่น)

### BR-PDM-10: Pricing Confidential
- **Statement:** `standard_cost/avg_cost/last_cost/purchase_price/list_price` = Confidential — role `canSeePricing` = product_manager/director/admin/finance เท่านั้น · enforcement ที่ server (payload exclusion)
- **Enforced by:** API middleware + UI `•••` · ดู §5.7 D-CLASS

---

## §5.2 State Machine (5 สถานะ — ไม่มี pending)

```
 ┌───────┐ activate  ┌────────┐ obsolete   ┌──────────┐ discontinue ┌──────────────┐
 │ draft │──────────►│ active │───────────►│ obsolete │────────────►│ discontinued │
 └───────┘ (gate)    └───┬────┘◄───────────└────┬─────┘             └──────┬───────┘
                         │      reactivate      │                          │
                         │      (gate FN-06)    │                          │ archive
                         │ archive              └──────────────────────────┤
                         ▼                                                 ▼
                     ┌──────────┐  ◄────────────────────────────── (soft delete)
                     │ archived │
                     └──────────┘
```

| From | To | Action (จอ) | Roles | Conditions |
|---|---|---|---|---|
| draft | active | เปิดใช้งาน / บันทึกและเปิดใช้งาน | canManage | FN-06 + FN-07 ผ่าน |
| active | obsolete | เลิกผลิต (modal) | canManage | — |
| obsolete | active | ใช้งานอีกครั้ง (direct) | canManage | FN-06 ผ่าน |
| obsolete | discontinued | ยกเลิกถาวร (modal) | canManage | — |
| active | archived | จัดเก็บ (modal) | canManage | soft delete |
| discontinued | archived | จัดเก็บ (modal) | canManage | soft delete |

- ทุก transition อื่น = `BR_INVALID_STATE` (รวมยิงซ้ำสถานะเดิม) — จอ: toast `… (INVALID_STATE)` + ปิด modal กลับ context
- archived = terminal (ไม่มีขากลับใน scope นี้)
- Enforced by FN-05 — **ห้าม set status ตรงข้าม state machine**

---

## §5.3 Permission Matrix

| Role | View list/detail | See pricing | Create/Edit/Import | Activate | Status transitions |
|---|---|---|---|---|---|
| `master_data_clerk` | ✅ | — (`•••`) | ✅ | ✅ | ✅ |
| `product_manager` | ✅ | ✅ | ✅ | ✅ | ✅ |
| `finance` | ✅ | ✅ | — | — | — |
| `director` | ✅ | ✅ | — | — | — |
| `admin` | ✅ | ✅ | ✅ | ✅ | ✅ |
| อื่น (authenticated) | ✅ | — | — | — | — |

> `canManage = [master_data_clerk, product_manager, admin]` · `canSeePricing = [product_manager, director, admin, finance]` (ตามจอจริง)

---

## §5.4 Field Validation Rules

| Field | Rule | Error |
|---|---|---|
| `name_th` | required, ≤200 | BR_REQUIRED |
| `type` | required, enum 8 | BR_BAD_TYPE |
| `cat_l1` | required (picker — soft ref) | BR_REQUIRED |
| `base_uom` | required, อยู่ใน uom_master active | BR_REQUIRED |
| `standard_cost/…/list_price` | ≥ 0 numeric | ERR_VALIDATION_FAILED |
| `min_stock/max_stock` | ดู BR-PDM-06 | BR_MINMAX_INVALID |
| `conversions[].factor` | ≥ 1 | BR_UOM_FACTOR |
| `gtin/hs_code/old_code` | free — format soft, ไม่บังคับ unique (soft reference policy) | — |

**Cross-field:** stocked → posting group required ตอน activate (ไม่บังคับตอน draft) · is_default เดี่ยวต่อ product

---

## §5.5 Edge Cases

### EC-01: Concurrent amend (PR-1/PR-2) `[AI-DEFAULT]`
2 คนแก้ record เดียวกัน → optimistic lock `version` + `If-Match` — คนแรก commit, คนหลัง 409 `ERR_STALE_DATA` · Test TC-CC-01

### EC-02: Double submit / retry (PR-4/PR-7) `[AI-DEFAULT]`
double-click / network retry → `Idempotency-Key` cache 24h — response เดิม ไม่ INSERT ซ้ำ (จอมี Rule #44 disabled+loader เป็นชั้นแรกแล้ว) · TC-ID-01

### EC-03: Hash-hack เข้าหน้าผิดสถานะ (observed)
`#/products/edit/<archived id>` → เด้ง view · action modal ผิดสถานะ → `BR_INVALID_STATE` + กลับ context · TC-GD-01

### EC-04: เปลี่ยนประเภทตอน create (observed)
เปลี่ยน type → regen code + reset behavior defaults (ค่า override เดิมหาย — by design จอจริง) · edit: code คงเดิม (IR-01) · TC-TY-01

### EC-05: Bulk import partial (PR-5 — observed จากจอ ไม่ใช่ default)
แถวผิดถูกข้าม ไม่ rollback แถวดี — สรุป `imported/skipped` + ตาราง error รายแถว · code ซ้ำภายในไฟล์เดียวกัน = ซ้ำด้วย · TC-BK-01/02

### EC-06: genCode race (PR-9) `[AI-DEFAULT]`
2 create พร้อมกัน type เดียว → running ชน → UNIQUE conflict → retry gen ใหม่ ≤3 ครั้ง · TC-RC-01

### EC-07: ลบรูปปก (observed)
ลบรูปที่เป็นปก → รูปแรกที่เหลือเป็นปกอัตโนมัติ · ไม่มีรูป → initials avatar

### EC-08: Reactivate ของที่ข้อมูลไม่ครบ (observed)
obsolete ที่ posting group หาย → `ใช้งานอีกครั้ง` โดน FN-06 block `BR_NOT_READY` — ต้องแก้ไขก่อน · TC-RA-01

---

## §5.6 Error Catalog

| Code | HTTP | จอ (verbatim ที่เกี่ยว) | Cause |
|---|---|---|---|
| `ERR_VALIDATION_FAILED` | 400 | — | field-level |
| `ERR_NOT_AUTHENTICATED` | 401 | — | token |
| `ERR_INSUFFICIENT_ROLE` | 403 | — | role |
| `ERR_NOT_FOUND` | 404 | — | id ไม่พบ |
| `ERR_STALE_DATA` | 409 | — | version mismatch (EC-01) |
| `ERR_DUPLICATE_IDEMPOTENCY_KEY` | 409 | — | EC-02 |
| `BR_CODE_DUPLICATE` | 422 | `รหัสสินค้าซ้ำ (CODE_DUPLICATE)` | BR-PDM-01 |
| `BR_CODE_IMMUTABLE` | 422 | (field readonly) | BR-PDM-02 |
| `BR_UOM_FACTOR` | 422 | `จำนวนหน่วยฐานต้อง ≥ 1 …` | VR-03 |
| `BR_UOM_DUP_BASE` | 422 | `หน่วยแปลงซ้ำกับหน่วยฐาน (X)` | VR-04 |
| `BR_UOM_CROSS_CATEGORY` | 422 | `หน่วย X … คนละหมวดกับหน่วยฐาน …` | VR-04 |
| `BR_UOM_LOCKED` | 422 | `สูตรหน่วยแปลงถูกล็อก — มี transaction แล้ว (IR-02)` | BR-PDM-04 |
| `BR_MINMAX_INVALID` | 422 | `สต็อกสูงสุด (Max) ต้องไม่ต่ำกว่าขั้นต่ำ (Min) — MINMAX_INVALID` | BR-PDM-06 |
| `BR_NOT_READY` | 422 | `ข้อมูลไม่พร้อมใช้งาน: <fields> (NOT_READY)` | BR-PDM-05 |
| `BR_INVALID_STATE` | 422 | `… (INVALID_STATE)` ตาม transition | §5.2 |
| `BR_REQUIRED` | 422 | bulk: `ข้อมูลบังคับไม่ครบ (REQUIRED)` | FN-11 |
| `BR_BAD_TYPE` | 422 | bulk: `ประเภทไม่ถูกต้อง (BAD_TYPE)` | FN-11 |

---

## §5.7 Security Bible Application

> Domains triggered: **D2, D5, D9, D15, D17** (D7 PII — not triggered: ไม่มี personal data)

### D2 Authentication — ทุก endpoint JWT + role check ที่ middleware
### D5 Financial — pricing/cost เปลี่ยน → audit BEFORE+AFTER · Confidential classification
### D9 Audit — ทุก mutation → T_product_audit + T_audit_log กลาง (append-only, 7 ปี)
### D15 Admin actions — status transition ทุกครั้ง log actor + label · ไม่มี reason field ใน scope (จอไม่มี) → ถ้าต้องการ = enhancement
### D17 Multi-tenant — RLS + X-Tenant-Id ทุก query

### D-CLASS (v5.1) — Enforcement summary
| Layer | Confidential (pricing 5 fields) |
|---|---|
| API | exclude/mask ตาม `canSeePricing` (server-side) |
| UI | `•••` ใน list · tab ราคา → empty "ข้อมูลจำกัด (Confidential)" |
| Export | exclude columns |
| Audit | log view + mutation |
**Wire:** Policy Center → Data Classification (override runtime) · ไม่มี Restricted → ไม่ wire Restricted Resources

---

## §5.8 Compliance & Audit
| Requirement | Implementation |
|---|---|
| Master data audit trail | T_product_audit + version ทุก amend |
| Soft delete only | BR-PDM-08 — ไม่มี DELETE endpoint |
| DOA (future) | placeholder fields + OQ-01 — ไม่มี enforcement ใน scope นี้ |
