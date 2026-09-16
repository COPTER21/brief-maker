# 02_API — F082 F-WH-STKADJ ใบปรับยอดสต๊อก (Stock Adjustment)

> **Audience:** Backend developer (HTTP layer)
> **Purpose:** API contracts — CUBIC API Entity format
> **🚨 Iron Rule:** ห้ามมี business logic >5 บรรทัดที่นี่ — ย้ายไป 03_LOGIC §3.1/§3.2
> **🚨 R8:** ทุก mutation API ระบุ "Calls (Logic)" → trace ใน 03_LOGIC §3.3
> **Resource:** `/api/v1/stock-adjustments` · ปี ค.ศ. ทุก timestamp

---

## §2.1 API Overview

| ID | Method | Path | Summary | Auth (role) | Mutation |
|---|---|---|---|---|---|
| F082-API-01 | GET | /api/v1/stock-adjustments | List + filter + KPI (FN-26,90) | required | — |
| F082-API-02 | GET | /api/v1/stock-adjustments/:id | Detail (view drawer 4 tabs) | required | — |
| F082-API-03 | POST | /api/v1/stock-adjustments | สร้าง/บันทึกร่าง (FN-19) | จนท./หน.คลัง | ✅ |
| F082-API-04 | PUT | /api/v1/stock-adjustments/:id | แก้ร่าง (lines/header · FN-04..13,41,52) | จนท./หน.คลัง | ✅ |
| F082-API-05 | POST | /api/v1/stock-adjustments/:id/submit | ส่งอนุมัติ → ออกเลขที่ (FN-20) | จนท./หน.คลัง | ✅ |
| F082-API-06 | POST | /api/v1/stock-adjustments/:id/approve | อนุมัติ slot (FN-21) | approver (slot) | ✅ |
| F082-API-07 | POST | /api/v1/stock-adjustments/:id/reject | ตีกลับ (FN-22) | approver | ✅ |
| F082-API-08 | POST | /api/v1/stock-adjustments/:id/cancel | ยกเลิก (ร่าง/รออนุมัติ · FN-24) | maker/หน.คลัง | ✅ |
| F082-API-09 | POST | /api/v1/stock-adjustments/:id/post | ผ่านรายการ (FN-23,27,30) | หน.คลัง | ✅ |
| F082-API-10 | POST | /api/v1/stock-adjustments/:id/reverse | กลับรายการ → สร้างใบใหม่ (FN-25,44) | หน.คลัง | ✅ |
| F082-API-11 | GET | /api/v1/stock-adjustments/:id/movements | ประวัติ movement + คู่ reversal (FN-29,45) | required | — |
| F082-API-12 | POST | /api/v1/stock-adjustments/:id/attachments | แนบหลักฐาน (FN-33,51) | maker | ✅ |
| F082-API-13 | GET | /api/v1/bins | Bin picker (filter type+warehouse · FN-01,02,03,32,46) | required | — |
| F082-API-14 | GET | /api/v1/items | Item picker (soft-ref) | required | — |
| F082-API-15 | GET | /api/v1/bins/:binId/stock-balance | ยอดระบบ snapshot (FN-04) | required | — |
| F082-API-16 | GET | /api/v1/doa/resolve | resolve สาย DOA จาก abs value (FN-14,15,16) · **X-module F-DLG-001** | required | — |
| F082-API-17 | GET | /api/v1/adjustment-reasons | Reason master (FN-37,41) | required | — |
| F082-API-18 | GET | /api/v1/count-documents | Count-doc picker (FN-52) · **X-module F084/F086 · display-only** | required | — |
| F082-API-19 | GET | /api/v1/stock-adjustments/:id/pdf | PDF A4 model/render (FN-34) | required | — |
| F082-API-20 | GET | /api/v1/stock-adjustment-attachments | Landing "เอกสารแนบ" aggregate (FN-33) | required | — |

> **Common headers (ทุก endpoint):** `Authorization: Bearer <jwt>` · `X-Tenant-Id: <uuid>`
> **Mutation headers:** `Idempotency-Key: <uuid>` (EC-02) · `If-Match: <version>` สำหรับ approve/post/reverse (EC-01 optimistic lock)

---

## §2.2 Per-API Contract (สำคัญ — mutation + key reads)

### F082-API-01: GET /api/v1/stock-adjustments
- **roles:** ทุก role (scope: เจ้าหน้าที่เห็นใบตัวเอง/คลังตัวเอง · §5.3)
- **Query:** `status` · `warehouse_ref` · `adjustment_type` · `date_from`/`date_to` (ค.ศ.) · `created_by` · `reason_code` · `q` (เลขที่) · `kpi` (pending|aging|reversed) · `limit`/`offset`
- **Response 200:** `{ data:[{ id, adj_no|null, warehouse_ref, adjustment_type, abs_adjustment_amount, status, sign_progress:"n/N", effective_date, created_by }], kpi:{ pending_count, aging_count, month_abs_total, reversed_count }, total, limit, offset }`
- **Errors:** 400 ERR_VALIDATION_FAILED · 401 · 403
- **Side effects:** — (read) · **Calls:** F082-FN-01 buildAdjustmentListQuery

### F082-API-02: GET /api/v1/stock-adjustments/:id
- **Response 200:** header + lines[] + approval[] + attachments[] + movements[] (สำหรับ 4 tabs) + `reversal_of`/`reversed_by_doc` + `je_status`
- **Errors:** 401 · 403 · 404 ERR_NOT_FOUND · **Calls:** — (assemble; PDF model แยกที่ API-19)

### F082-API-03: POST /api/v1/stock-adjustments  (สร้าง/บันทึกร่าง)
- **roles:** เจ้าหน้าที่คลัง, หัวหน้าคลัง
- **Headers:** `Idempotency-Key` (required)
- **Body:** `{ warehouse_ref, effective_date, adjustment_type, adj_source, ref_count_doc?, cost_center_ref?, header_reason_code?, note?, lines?[] }`
- **Validation (field ≤5 บรรทัด):** warehouse_ref required (VR-01) · effective_date ≤ today (VR-02) · adjustment_type enum (VR-03) · adj_source enum (VR-04) · **complex → 03_LOGIC F082-FN-06**
- **Response 201:** `{ id, status:"draft", adj_no:null }` — ร่างยังไม่มีเลขที่ (BR-21)
- **Errors:** 400 · 403 · 409 ERR_DUPLICATE_IDEMPOTENCY_KEY · 422 (VR)
- **Side effects:** INSERT T_stock_adjustment(+lines) · T_audit_log · **Calls:** F082-FN-02 createDraftAdjustment, F082-FN-04 snapshotSystemQty

### F082-API-04: PUT /api/v1/stock-adjustments/:id  (แก้ร่าง)
- **Precondition:** status = `draft` (แก้ได้เฉพาะร่าง — HTML toast "แก้ไขได้เฉพาะฉบับร่าง")
- **Body:** header + lines[] เต็มชุด (bin, item, input_mode, correct_qty|adjust_qty, reason_code, reason_note, attachment_ref)
- **Validation:** BR-01 dup (VR-15) · BR-02 delta≠0 (VR-06) · BR-03 non-negative (VR-07) · BR-07 reason direction · **complex → F082-FN-03/FN-06**
- **Response 200:** updated doc + computed (delta, line_amount, abs_total, net_total)
- **Errors:** 409 ERR_STALE_DATA (If-Match) · 422 (VR-05..09) · **Calls:** F082-FN-03 updateAdjustmentLines, F082-FN-07 fillLineReasonsFromHeader, F082-FN-04, ENG F082-ENG-01

### F082-API-05: POST /api/v1/stock-adjustments/:id/submit  (ส่งอนุมัติ)
- **Precondition:** status = `draft`
- **Body:** `{ approval_slots:[{ step_no, role_slot, approver_person_id }] }` (คนจริงทุก slot)
- **Validation (pre-submit — all BR):** BR-02/03/06/07/10/12/13/23/26 (VR-05..12) · SoD (slot ≠ ผู้จัดทำ)
- **Response 200:** `{ id, adj_no:"ADJ-YYYY-NNNN", status:"pending", approval:[...] }` — **ออกเลขที่ตอนนี้** (BR-21 · ENG-DOC-NUM)
- **Errors:** 422 ERR_APPROVER_SLOT_EMPTY / ERR_REASON_REQUIRED / ERR_EVIDENCE_REQUIRED / ERR_COUNT_DOC_REQUIRED / ERR_SOD_SELF_APPROVAL
- **Side effects:** UPDATE status · INSERT approval snapshot · **ENG-DOC-NUM.next('ADJ')** · emit `doa_pending` (DOA engine) + NTF slot1 · T_audit_log
- **Calls:** F082-FN-06 validateAdjustmentDocument, F082-FN-08 submitForApproval, F082-ENG-01 (abs base), **ENG-DOC-NUM (F-DOCCFG)**, **DOA resolve (F-DLG-001)**

### F082-API-06: POST /api/v1/stock-adjustments/:id/approve  (อนุมัติ slot)
- **Precondition:** status = `pending` · caller = ผู้อนุมัติ slot ปัจจุบัน · caller ≠ ผู้จัดทำ (SoD)
- **Headers:** `If-Match: <version>` (EC-01)
- **Body:** `{ note? }`
- **Response 200:** `{ status:"pending"|"approved", current_step, sign_progress }` — ไป slot ถัดไป หรือ `approved` เมื่อครบ
- **Errors:** 403 ERR_SOD_SELF_APPROVAL / ERR_INSUFFICIENT_ROLE · 409 ERR_STALE_DATA · 422 ERR_INVALID_STATE_TRANSITION
- **Side effects:** UPDATE approval row (result=approved) · emit `doa_result` (DOA engine) + NTF · **Calls:** F082-FN-09 approveSlot

### F082-API-07: POST /api/v1/stock-adjustments/:id/reject  (ตีกลับ)
- **Precondition:** status = `pending` · caller = ผู้อนุมัติ slot ปัจจุบัน
- **Body:** `{ reason }` (required · BR-11 · VR-12)
- **Response 200:** `{ status:"draft", returned:true }`
- **Errors:** 422 ERR_REJECT_REASON_REQUIRED · **Calls:** F082-FN-10 rejectDocument

### F082-API-08: POST /api/v1/stock-adjustments/:id/cancel  (ยกเลิก)
- **Precondition:** ★ status ∈ {`draft`,`pending`} เท่านั้น — **`approved` ยกเลิกไม่ได้** (BR-27 · VR-16 · FIX-02)
- **Body:** `{ reason }` (required · VR-14)
- **Response 200:** `{ status:"cancelled" }` — ไม่มี movement · ใบยังอยู่
- **Errors:** 422 ERR_CANCEL_NOT_ALLOWED (ถ้า status=approved/posted) / ERR_ACTION_REASON_REQUIRED
- **Side effects:** UPDATE status · emit `adj_cancelled` (NTF) · **Calls:** F082-FN-11 cancelDocument

### F082-API-09: POST /api/v1/stock-adjustments/:id/post  (ผ่านรายการ)
- **Precondition:** status = `approved` (BR-08 · VR-13) · role = หัวหน้าคลัง · `If-Match`
- **Body:** `{ recheck_choice?: "latest"|"return" }` — เมื่อ BR-15 พบ drift (S-15)
- **Behaviour:** (1) F082-FN-12 recheckQtyBeforePost เทียบ snapshot vs ยอดล่าสุด — ต่าง → 200 `{ warn:"WARN_QTY_CHANGED", drift:[{bin,item,old,latest,new_delta}] }` (บังคับเลือก) · (2) เลือกแล้ว → generate movement append-only + je_status=รอลงบัญชี
- **Response 200:** `{ status:"posted", movements:[...], je_status:"รอลงบัญชี" }`
- **Errors:** 422 ERR_INVALID_STATE_TRANSITION · 409 ERR_STALE_DATA
- **Side effects:** INSERT T_inventory_movement (append-only) · ยอดคงเหลือ bin ขยับ · **`FWD-WIRE: JE posting`** (mock BR-19) · emit `adj_posted`/`adj_writeoff_posted`/`adj_qty_drift_on_post` (NTF) + CSQ EC (`adj_posted_increase`/`_decrease`/`_writeoff_posted`) · ถ้า posted doc = reversal → set ต้นฉบับ `reversed` (BR-17.1)
- **Calls:** F082-FN-12, F082-FN-13 postDocument, F082-ENG-02 inventory-movement-engine, **ENG-DOC-STORE (approved_final)**, **ENG-CSQ (F-CSQ-01)**

### F082-API-10: POST /api/v1/stock-adjustments/:id/reverse  (กลับรายการ → สร้างใบใหม่)
- **Precondition:** status = `posted` · ยังไม่เคยกลับรายการ (`reversed_by_doc` is null · BR-18 · VR-14)
- **Body:** `{ reason }` (required · VR-14)
- **Behaviour (FIX-03):** สร้าง **ใบกลับรายการใหม่** (`is_reversal_doc=true`, delta ตรงข้าม, reason auto RS-05/RS-02) → resolve DOA ตาม abs ของใบกลับรายการ → status `pending` (ไม่ auto-post) · ผูก `reversal_of`/`reversed_by_doc` 2 ทาง
- **Response 200:** `{ reversal_doc:{ id, adj_no, status:"pending" } }`
- **Errors:** 422 ERR_ALREADY_REVERSED / ERR_ACTION_REASON_REQUIRED
- **Side effects:** INSERT ใบกลับรายการ (+ approval snapshot) · **ENG-DOC-NUM.next('ADJ')** ใหม่ · emit `adj_reversed` เมื่อใบกลับรายการ post (ไม่ใช่ตอนริเริ่ม) · **Calls:** F082-FN-14 reverseDocument, F082-ENG-01, DOA resolve

### F082-API-11: GET /:id/movements
- **Response 200:** movements[] (append-only) + คู่ reversal (reversed/reversal ผูก 2 ทาง) · **Calls:** F082-FN-16 getMovementHistory · **ไม่มี** DELETE/PUT movement (BR-16)

### F082-API-12: POST /:id/attachments
- **Body:** multipart file · **Response 201:** attachment record · **Side effects:** INSERT T_stock_adjustment_attachment + Document Center · **Calls:** F082-FN-15 attachEvidence

### F082-API-13: GET /api/v1/bins  (Bin picker)
- **Query:** `warehouse_ref` (required) · `type` (จาก adjustment_type → allowed location_types) · `q`
- **Behaviour:** ★ **exclude `in-transit` เสมอ (server-side · BR-13/FN-32)** · bin `ล็อก`/โซนปิด → คืน `disabled:true` + `locked_reason` (BR-14/FN-03)
- **Response 200:** `{ data:[{ bin_code, zone, location_type, disabled, locked_reason? }] }` · **Calls:** F082-FN-05 filterBinPicker

### F082-API-15: GET /api/v1/bins/:binId/stock-balance
- **Query:** `item_ref` · **Response 200:** `{ system_qty, snap_at, uom, unit_cost_ref (mock · FWD-WIRE valuation) }` · **Calls:** F082-FN-04 snapshotSystemQty

### F082-API-16: GET /api/v1/doa/resolve  (X-module)
- **Query:** `abs_value` · `module=WH-STKADJ` · **Response 200:** `{ doa_entry_ref:"DOA-WH-ADJ-01", steps:[{ step_no, role_slot }] }` — ชั้นตัดสินโดย DOA กลาง (F-DLG-001) · feature แค่ส่ง abs (BR-09) · **ไม่ owned** ที่นี่

### F082-API-18: GET /api/v1/count-documents  (X-module · display-only)
- **Query:** `q` · **Response 200:** `{ data:[{ count_doc_no, type:"F084|F086", label }] }` — **display-only ไม่เปิด/สร้างหน้าใบนับ** (FN-52 · BR-26)

### F082-API-19: GET /:id/pdf
- **Response:** PDF A4 portrait (Sarabun) — header + 10-col line table + totals (headline = Σ|มูลค่า| ค่าสัมบูรณ์) + 3 signature slots (ผู้จัดทำ / ผู้อนุมัติ / ผู้ผ่านรายการ) · watermark ตามสถานะ · **Calls:** F082-FN-17 buildAdjustmentPdfModel · print-spec = `5_DECLARATIONS/print-spec-adj.md`

---

## §2.3 Common Concerns

### Idempotency (EC-02 · FN-92)
ทุก mutation รับ `Idempotency-Key` — key เดิม+body เดิม → คืน cached response (ไม่สร้าง/post ซ้ำ) · cache 24hr · key เดิม+body ต่าง → 409.

### Optimistic Locking (EC-01)
approve/post/reverse ต้องมี `If-Match: <version>` — mismatch → 409 ERR_STALE_DATA. เพิ่ม serialize post ที่ (bin,item) กัน race (BRD §14.3).

### Multi-Tenant / Permission
ทุก endpoint `X-Tenant-Id` (RLS) + row scope ตามคลังที่ผู้ใช้สังกัด · **re-check role ตอน mutation** (EC-03).

### Audit
ทุก mutation → T_audit_log (actor, action, resource, diff, ค.ศ. timestamp · BR-25 · FN-39).

### Append-only
**ไม่มี** endpoint DELETE/PUT สำหรับ movement (BR-16/FN-45) หรือ hard delete ใบใด ๆ (ยกเลิก/กลับรายการ = สถานะ ไม่ลบ).

---

## §2.4 API → Logic Trace (Anchor for R8)

> Authoritative: `03_LOGIC §3.3`. ที่นี่ summary.

| API | Calls Functions | Calls Engines |
|---|---|---|
| F082-API-01 GET list | F082-FN-01 | — |
| F082-API-02 GET detail | — (assemble) | — |
| F082-API-03 POST create | F082-FN-02, F082-FN-04 | — |
| F082-API-04 PUT update | F082-FN-03, F082-FN-07, F082-FN-04 | F082-ENG-01 |
| F082-API-05 POST submit | F082-FN-06, F082-FN-08 | F082-ENG-01, ENG-DOC-NUM*, DOA* |
| F082-API-06 POST approve | F082-FN-09 | — |
| F082-API-07 POST reject | F082-FN-10 | — |
| F082-API-08 POST cancel | F082-FN-11 | — |
| F082-API-09 POST post | F082-FN-12, F082-FN-13 | F082-ENG-02, ENG-DOC-STORE*, ENG-CSQ* |
| F082-API-10 POST reverse | F082-FN-14 | F082-ENG-01, ENG-DOC-NUM*, DOA* |
| F082-API-11 GET movements | F082-FN-16 | — |
| F082-API-12 POST attachments | F082-FN-15 | — |
| F082-API-13 GET bins | F082-FN-05 | — |
| F082-API-15 GET stock-balance | F082-FN-04 | — |
| F082-API-19 GET pdf | F082-FN-17 | — |
| F082-API-20 GET attachments | F082-FN-18 | — |

`*` = engine ภายนอก (ไม่ owned) — F-DOCCFG / F-DLG-001 / F-CSQ-01
> **R8 Check:** ทุก mutation row (03,04,05,06,07,08,09,10,12) มี ≥1 entry — ✅

---

## §2.X Cross-Module Contract (จาก BRD §12.1 Downstream Impact + PREBRIEF §9)

> ทุก downstream ที่มี data ไหลออก ต้องมี contract ชัด — endpoint/event/payload · trace กับ 06_TESTS §6.9 (XT)

| Downstream | รูปแบบ | Contract | Trigger | Payload หลัก | Compensating |
|---|---|---|---|---|---|
| Inventory ledger / ยอดคงเหลือ bin | Write (internal) | INSERT T_inventory_movement | **post เท่านั้น** | { movement_type, bin_ref, item_ref, qty, amount, ref_doc } | กลับรายการ → movement ทิศตรงข้าม (append-only) |
| GL / JE (W5) | Marker (mock) | je_status=`รอลงบัญชี` + `FWD-WIRE: JE posting` | post | { adj_no, line_amount, gl_account_mock, cost_center } | ยังไม่ post จริง (BR-19) · W5 owns AC (กันนับซ้ำ) |
| ENG-NOTIFY (F-NOTIFY) | Event | `adj_posted` · `adj_reversed` · `adj_cancelled` · `adj_high_value_submitted` · `adj_writeoff_posted` · `adj_qty_drift_on_post` | ตาม transition (NTF_BRIEF §2) | { adj_no, abs_amount, warehouse, audience } | `doa_pending`/`doa_result` มาจาก DOA engine — **ไม่ประกาศซ้ำ** |
| 7C Consequence (F-CSQ-01) | Event | `adj_posted_increase`/`adj_posted_decrease`/`adj_writeoff_posted` (EC actual) · `adj_reversed` (EC avoided) · `adj_cancelled` (no-effect) | post / กลับรายการ / ยกเลิก | { abs_adjustment_amount, basis:"computed" } | กลับรายการ = avoided หักผลเดิม · **ไม่ประกาศ OC/DC/SC/SecC/AC/FC** |
| ENG-DOC-NUM / ENG-DOC-STORE (F-DOCCFG) | Endpoint (เรียกออก) | `next('ADJ', ctx)` · `store(pdf,'ADJ',id,'approved_final')` | submit / approved | { doc_type:'ADJ', year } | เลข immutable · ใบกลับรายการเรียก next() ใหม่ |
| DOA (F-DLG-001) | Endpoint (เรียกออก) | GET /doa/resolve?abs_value= (F082-API-16) | submit / reverse | { abs_value, module } → steps[] | ครอบทั้งใบปรับยอด+กลับรายการ (FIX-03) |
| Stock Transfer (F083 · ตัวถัดไป) | Reuse (schema) | movement schema §3.4 + reversal pattern + DOA slot picker | — (design handoff) | — | `in-transit` ยังว่างรอ (OB-16) |
| Count Doc (F084/F086) | Read (soft-ref) | ref_count_doc display-only (F082-API-18) | wizard step1 / view | { count_doc_no } | — (ไม่เปิดหน้าใบนับ · FIX-04) |
