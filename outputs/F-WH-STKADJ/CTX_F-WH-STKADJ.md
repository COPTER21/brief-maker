# CTX — F-WH-STKADJ (F082): ใบปรับยอดสต๊อก (Stock Adjustment)

> **derived from:** FRD_F-WH-STKADJ v1.0 (2026-09-16) · **generated:** 2026-09-16
> **module:** Warehouse · Wave W3Q · arch Q-document (Pattern Q + B2 v2) · **status:** active
> ⚠ Derived artifact — source of truth คือ FRD Pack · ถ้า FRD revise ต้อง regen CTX

---

## 1. Summary
ออกใบปรับยอดสต๊อก (+/−) ราย (bin, สินค้า) พร้อมผลต่าง + มูลค่า + เหตุผลบังคับทุกบรรทัด · เจ้าหน้าที่คลังสร้าง → ส่งเข้าสายอนุมัติ DOA ตาม **ค่าสัมบูรณ์ของมูลค่า** (slot คนจริง) → หัวหน้าคลังผ่านรายการ (post) → เกิด `inventory_movement` แบบ append-only · แก้ผิดได้ด้วย **กลับรายการ** (สร้างใบใหม่ เข้าสาย DOA ของตัวเอง ไม่ auto-post) · ปรับได้ทั้งแบบตรงและอ้างอิงใบนับ (display-only) · location อ่านอย่างเดียวจาก Putaway (ไม่ย้าย/โอน = คนละ feature กับ Stock Transfer F083)

## 2. Data Contract
### Entities
| Entity (T_*) | PK | Key Fields (ที่ feature อื่นน่าจะอ่าน/join) | หมายเหตุ |
|---|---|---|---|
| `T_stock_adjustment` | id | adj_no · warehouse_ref · adj_source · ref_count_doc · adjustment_type · status · abs_adjustment_amount · net_adjustment_amount · is_reversal_doc · reversal_of · reversed_by_doc · doa_entry_ref · je_status | หัวใบ · owner F082 · RLS multi-tenant · `adj_no` = `ADJ-YYYY-NNNN` (ค.ศ.) null จนส่งอนุมัติ |
| `T_stock_adjustment_line` | id | adjustment_id(FK) · bin_ref · item_ref · delta_qty · line_amount · reason_code | UNIQUE (adjustment_id, bin_ref, item_ref) = BR-01 |
| `T_stock_adjustment_approval` | id | adjustment_id(FK) · step_no · role_slot · approver_person_id · result | **append-only** · SoD: approver ≠ created_by/submitted_by |
| `T_stock_adjustment_attachment` | id | adjustment_id(FK) · file_ref · file_name | Document Center · damage ต้องมี ≥1 (BR-23) |
| `T_inventory_movement` | id | movement_no · movement_type · item_ref · bin_ref · qty · amount · ref_doc · reversed_movement_id · reversal_movement_id | **shared ledger ของ Warehouse lane** · append-only (no UPDATE/DELETE) · StockAdj เขียนได้เฉพาะ type ปรับยอด/กลับรายการ |
| `T_adj_reason` | reason_code | reason_name · direction · require_note | config · **read-only** ที่ feature นี้ (seed 8 row RS-01..07/RS-99) |
| `T_adj_type_bin_map` | adjustment_type | allowed_location_types[] · require_attachment | config · map ประเภทการปรับ → location_type |

### Enums / States (ครบทุกค่า)
| Field | Values | Transition owner |
|---|---|---|
| `status` | `draft` → `pending` → `approved` → `posted` · `draft`/`pending` → `cancelled` · `posted` → `reversed` | F082 · **ยกเลิกได้เฉพาะ draft/pending** (BR-27/FIX-02) · **ไม่มี approved→cancelled** |
| `approval_status` | draft / pending_approval / approved / rejected / cancelled | map กับ status |
| `adj_source` | `direct` (ปรับตรง) / `count` (จากใบนับ) | required ref_count_doc เมื่อ = count (BR-26/VR-17) |
| `adjustment_type` | `general` / `damage` / `quarantine` | คุมประเภท bin (BR-12) · damage ต้องแนบหลักฐาน |
| `input_mode` (line) | `correct` (ระบุยอดที่ถูก) / `delta` (ระบุจำนวนปรับ) | delta_qty ≠ 0 · system+delta ≥ 0 |
| `movement_type` | ปรับเพิ่ม / ปรับลด / กลับรายการปรับเพิ่ม / กลับรายการปรับลด | qty บวกเสมอ · ทิศอยู่ที่ type |
| `je_status` | `รอลงบัญชี` (คงที่รอบนี้ · mock BR-19) | W5 owns จริง |

### Relationships
- `T_stock_adjustment` 1—N line / approval / attachment / movement (movement เกิดตอน **post** เท่านั้น)
- `T_stock_adjustment` 1—1(opt) `T_stock_adjustment` (`reversal_of` ↔ `reversed_by_doc` · 2 ทาง · BR-18)
- soft-ref (nullable, no FK validate): `warehouse_ref`/`bin_ref` → **F081 Putaway §3.0 (read-only)** · `item_ref`/`uom`/`cost_center_ref` → Masters · `ref_count_doc` → **F084/F086 (display-only)**

## 3. API Surface
Resource: `/api/v1/stock-adjustments` · ทุก timestamp ค.ศ. · headers: `Authorization` + `X-Tenant-Id` · mutation เพิ่ม `Idempotency-Key` + `If-Match` (approve/post/reverse)

| Method | Endpoint | ทำอะไร | Payload หลัก |
|---|---|---|---|
| GET | `/stock-adjustments` | list + filter + KPI | q · status · warehouse_ref · adjustment_type · date_from/to · kpi |
| GET | `/stock-adjustments/:id` | detail (4 tabs) | → header+lines+approval+attachments+movements |
| POST | `/stock-adjustments` | สร้าง/บันทึกร่าง | { warehouse_ref, effective_date, adjustment_type, adj_source, ref_count_doc?, lines?[] } → 201 status=draft, adj_no=null |
| PUT | `/stock-adjustments/:id` | แก้ร่าง (เฉพาะ draft) | header + lines[] เต็มชุด |
| POST | `/:id/submit` | ส่งอนุมัติ → **ออกเลขที่** | { approval_slots:[{step_no, role_slot, approver_person_id}] } → adj_no ออกตอนนี้ |
| POST | `/:id/approve` | อนุมัติ slot | { note? } · If-Match · SoD |
| POST | `/:id/reject` | ตีกลับ → draft | { reason } (required) |
| POST | `/:id/cancel` | ยกเลิก (draft/pending เท่านั้น) | { reason } · approved ยกเลิกไม่ได้ (BR-27) |
| POST | `/:id/post` | ผ่านรายการ → movement | { recheck_choice?: latest\|return } · role หน.คลัง |
| POST | `/:id/reverse` | กลับรายการ → สร้างใบใหม่ | { reason } → ใบใหม่ status=pending (เข้า DOA เอง · FIX-03) |
| GET | `/:id/movements` | ประวัติ movement + คู่ reversal | (ไม่มี DELETE/PUT · BR-16) |
| POST | `/:id/attachments` | แนบหลักฐาน | multipart file |
| GET | `/bins` | bin picker (exclude in-transit เสมอ) | warehouse_ref(req) · type · q |
| GET | `/bins/:binId/stock-balance` | ยอดระบบ snapshot | item_ref → { system_qty, unit_cost_ref(mock) } |
| GET | `/doa/resolve` | resolve สาย DOA จาก abs | **X-module F-DLG-001 · ไม่ owned** |
| GET | `/count-documents` | count-doc picker | **X-module F084/F086 · display-only** |
| GET | `/:id/pdf` | PDF A4 (headline Σ\|มูลค่า\|) | 3 signature slots |

### Events emitted
| Event | Trigger | Payload key | Channel |
|---|---|---|---|
| `adj_posted` · `adj_writeoff_posted` · `adj_qty_drift_on_post` | post | { adj_no, abs_amount, warehouse, audience } | ENG-NOTIFY (F-NOTIFY) |
| `adj_reversed` | ใบกลับรายการ post (ไม่ใช่ตอนริเริ่ม) | { adj_no } | ENG-NOTIFY |
| `adj_high_value_submitted` | submit เกิน threshold NC | { adj_no, abs_amount } | ENG-NOTIFY |
| `adj_cancelled` | cancel | { adj_no } | ENG-NOTIFY (no-effect ใน CSQ) |
| `adj_posted_increase` / `adj_posted_decrease` / `adj_writeoff_posted` | post | { abs_adjustment_amount, basis:"computed" } | 7C CSQ = EC actual |
| `adj_reversed` (CSQ) | ใบกลับรายการ post | — | 7C CSQ = EC avoided (หักผลเดิม) |
> `doa_pending`/`doa_result` มาจาก DOA engine — **ไม่ประกาศซ้ำ** · CSQ **ไม่ประกาศ** OC/DC/SC/SecC/AC/FC

## 4. Shared Rules (cross-boundary เท่านั้น)
| Rule | Rule | กระทบใคร |
|---|---|---|
| **BR-09** | ฐาน DOA = `abs_adjustment_amount` = Σ\|line_amount\| (ค่าสัมบูรณ์) **ห้ามใช้ net** | F-DLG-001 · ทุก consumer ที่คิดวงเงิน/JE/PDF/NTF/CSQ |
| **BR-21** | เลขเอกสาร `ADJ-YYYY-NNNN` (ค.ศ.) ออกตอน **submit** ผ่าน ENG-DOC-NUM · immutable · null ตอนร่าง | F-DOCCFG · ใบกลับรายการเรียก next() ใหม่ |
| **BR-16** | `T_inventory_movement` append-only — **ห้าม UPDATE/DELETE** (no endpoint, no DB grant) | ทุก feature ที่อ่าน/เขียน shared ledger (F083, valuation, รายงาน) |
| **BR-18** | กลับรายการผูก movement + doc 2 ทาง (`reversed_*`/`reversal_*`) · ใบเดิม → status `reversed` | consumer ledger/รายงาน |
| **BR-26 / VR-17** | adj_source='count' → `ref_count_doc` required (DB CHECK) · ใบนับ display-only ห้ามเปิด/สร้างหน้า | F084/F086 |
| **BR-13** | **ห้ามเขียน/แสดง bin `in-transit`** (server-side exclude) — จองให้ Stock Transfer | F083 |
| **BR-19** | JE = mock (`je_status=รอลงบัญชี` + `FWD-WIRE: JE posting`) — **W5 owns AC จริง** (กันนับซ้ำ) | GL/W5 |
| **LOCK-03** | movement มี location เดียว (`bin_ref`) — **ไม่มี "จาก→ไป"** (ไม่ใช่ transfer) | F083 (ห้าม reuse ผิด) |
| **SoD** | approver_person_id ≠ ผู้จัดทำ/ผู้ส่ง · slot เก็บ **คนจริง** ห้ามเก็บ role ID แทนคนบนจอ | Policy Center / audit |
| **BR-27 / VR-16** | ยกเลิกได้เฉพาะ draft/pending · **approved/posted ยกเลิกไม่ได้** (ต้องกลับรายการ) | consumer state machine |

## 5. Integration
- **Depends on (upstream):** F081 Putaway §3.0 (location/bin + ยอดคงเหลือ · read-only soft-ref) · Masters (Item/UOM/Cost Center) · F084/F086 (ref_count_doc display-only) · **F-DLG-001** (DOA resolve) · **F-DOCCFG** (ENG-DOC-NUM/STORE) · **W5** (ต้นทุน/valuation · mock ตอนนี้)
- **Depended by (downstream):** **F083 Stock Transfer** (reuse F082-ENG-01/02 + movement schema + reversal pattern + DOA slot picker · in-transit ยังว่างรอ OB-16) · GL/JE W5 · ENG-NOTIFY/7C CSQ · รายงาน inventory accuracy
- **Declarations:** DOA **yes** (scope: วงเงินตาม abs · `DOA-WH-ADJ-01` · ครอบใบปรับยอด+ใบกลับรายการ) · NTF **6 events** (feature-owned; DOA events excluded) · CSQ **5 EC events** (OC/DC/SC ไม่ประกาศ) · DOCCFG **doc_type `ADJ`** (ADJ-YYYY-NNNN ค.ศ. · snapshot approved_final)
- **Engine hooks:** owned F082-ENG-01 (abs base valuation · pure) · F082-ENG-02 (inventory-movement · append-only ledger) · external (ประกาศ ไม่ implement): ENG-DOC-NUM/STORE (F-DOCCFG) · DOA resolve (F-DLG-001) · ENG-NOTIFY (F-NOTIFY) · ENG-CSQ (F-CSQ-01)
- **Data class:** highest = **Confidential** (มูลค่า/ต้นทุน = financial D5 · ชื่อ/ตำแหน่งผู้ปฏิบัติงาน = Confidential+PII PDPA) · **ไม่มี Restricted fields**

---
*trace: §2 ← FRD 04_DB · §3 ← FRD 02_API (+§2.X X-module) · §4 ← FRD 05_RULES/DB constraints · §5 ← 00_OVERVIEW §0.5 + declaration briefs*
