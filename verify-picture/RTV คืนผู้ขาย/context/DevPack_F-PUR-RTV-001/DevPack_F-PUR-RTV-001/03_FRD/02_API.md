# 02_API — F-PUR-RTV · RTV คืนผู้ขาย

> Audience: BE dev (**HTTP layer เท่านั้น**) · business logic อยู่ที่ `03_LOGIC.md` · กติกาอยู่ที่ `05_RULES.md`
> Base path: `/api/v1/purchase/rtv`

## §2.1 Endpoint list

| ID | Method · Path | สาระ | Mutation | มาจากอะไรบนจอ |
|---|---|---|:--:|---|
| `F-PUR-RTV-API-01` | `GET /rtv` | หน้ารายการ + ตัวกรอง 4 แกน + สวิตช์รวมที่ยกเลิก + ตัวชี้วัด 5 ตัว | — | `renderPage()` · `rtvFiltered()` · `kpis()` |
| `F-PUR-RTV-API-02` | `GET /rtv/{id}` | รายละเอียดใบเดียว (ครบทั้ง 5 แท็บ) | — | `renderViewDrawer()` |
| `F-PUR-RTV-API-03` | `GET /rtv/selectable-grns` | ใบรับของที่คืนได้ + **เหตุผลรายใบของใบที่เลือกไม่ได้** + ยอดคืนได้ | — | `renderGrnRowsHtml()` · `grnReturnable()` · `grnBlockReason()` |
| `F-PUR-RTV-API-04` | `POST /rtv` | สร้างร่างจากใบรับของ (ดึงบรรทัด + ยอดคืนได้ + ราคา/ภาษี/location) | ✅ | `pickGrn()` → `commitWizard('draft')` |
| `F-PUR-RTV-API-05` | `PUT /rtv/{id}` | แก้ร่าง (ข้อมูลหลัก + จำนวนคืน + เหตุผล + location + หมายเหตุ) | ✅ | `updateLine()` · `applyMainReason()` · `saveDraft()` |
| `F-PUR-RTV-API-06` | `POST /rtv/{id}/refresh-from-grn` | ดึงข้อมูลจากใบรับของใหม่ | ✅ | `reloadFromGrn()` |
| `F-PUR-RTV-API-07` | `POST /rtv/{id}/submit` ★ | **ส่งอนุมัติ** — ออกเลขเอกสาร + freeze สาย + snapshot คนจริงต่อขั้น | ✅ | `openSubmitModal()` · `doSubmit()` |
| `F-PUR-RTV-API-08` | `POST /rtv/{id}/approve` | อนุมัติขั้นปัจจุบัน (ครบสาย → `อนุมัติแล้ว`) | ✅ | `doApprove()` · `currentSlot()` |
| `F-PUR-RTV-API-09` | `POST /rtv/{id}/sendback` | ส่งกลับแก้ (กลับเป็นร่าง **เลขเดิม**) | ✅ | `doSendback()` |
| `F-PUR-RTV-API-10` | `POST /rtv/{id}/reject` | ไม่อนุมัติ (→ `ยกเลิก`) | ✅ | `doReject()` |
| `F-PUR-RTV-API-11` | `POST /rtv/{id}/ship` ★ | **บันทึกส่งคืน** — ตัดสต๊อก + เขียนยอดคืนสะสมกลับ GRN + ล็อก GRN | ✅ | `doShip()` |
| `F-PUR-RTV-API-12` | `POST /rtv/{id}/credit` | บันทึกเครดิต · ปิดใบ | ✅ | `doCredit()` |
| `F-PUR-RTV-API-13` | `POST /rtv/{id}/reverse` ★ | กลับรายการทั้งใบ (movement ตรงข้าม + หักยอดคืนสะสม) | ✅ | `doReverse()` |
| `F-PUR-RTV-API-14` | `POST /rtv/{id}/cancel` | ยกเลิกก่อนของออก (รวมเส้นทาง "ทิ้งร่าง") | ✅ | `doCancel()` · `openModal('cancel')` |
| `F-PUR-RTV-API-15` | `POST /rtv/{id}/attachments` · `DELETE /rtv/{id}/attachments/{fileId}` | เอกสารแนบ | ✅ | `addMockFile()` · `removeFile()` |
| `F-PUR-RTV-API-16` | `GET /rtv/{id}/print` | ข้อมูลเอกสารพิมพ์ A4 + สถานะลายน้ำ | — | `renderPdfTab()` · `pdfSign()` |
| `F-PUR-RTV-API-17` | `GET /rtv/export` | ส่งออก CSV ตามตัวกรองปัจจุบัน | — | `exportCsv()` |
| `F-PUR-RTV-API-18` | `GET /rtv/doa-preview?amount=` | preview สายอนุมัติจากมูลค่า (ใช้ที่ขั้น 5 และตอนเปิดหน้าต่างส่งอนุมัติ) | — | `resolveDoa()` ใน `renderStep5()` |

**Mutation API = 12 ตัว** (04·05·06·07·08·09·10·11·12·13·14·15) — ทุกตัวมี Function/Engine ใน `03_LOGIC §3.3` (R8)

## §2.2 Contract blocks

### `F-PUR-RTV-API-03` · `GET /rtv/selectable-grns?q=`
- **Response 200:** `[{ grn_ref, grn_date, vendor_ref, vendor_name, po_ref, returnable_qty, selectable: bool, block_reason }]`
- **`block_reason` ต้องส่งข้อความที่ผู้ใช้อ่านรู้เรื่องมาเลย** (จอแสดงตรง ๆ ไม่แปลงเพิ่ม): `"ใบรับของยังเป็นร่าง — ยังไม่มีของเข้าคลัง"` · `"ใบรับของถูกกลับรายการแล้ว"` · `"คืนครบแล้ว — ไม่มีของคงเหลือให้คืน"`
- **Logic:** → `FN-02 getSelectableGrns` · `ENG-RTV-01`
- **หมายเหตุ:** ใบที่เลือกไม่ได้ **ต้องส่งมาด้วย ไม่ใช่กรองทิ้ง** — จอแสดงเป็นแถวจางพร้อมเหตุผล (BR-01 · `EC-03`)

### `F-PUR-RTV-API-04` · `POST /rtv`
- **Request:** `{ grn_ref, main_reason?, doc_date? }`
- **Request validation (HTTP layer, trivial):** `grn_ref` required · `doc_date` ISO date
- **Response 201:** `RtvDetail` (บรรทัดถูกดึงมาครบพร้อม `qty_returnable` · `qty_return` ตั้งต้น = ยอดคืนได้ · `return_reason`/`source_location_ref` เดามาให้)
- **Logic:** → `FN-03 buildDraftFromGrn` · `ENG-RTV-01` · `ENG-RTV-02`
- **Errors:** `GRN_NOT_SELECTABLE` (409) · `GRN_NOT_FOUND` (404)

### `F-PUR-RTV-API-05` · `PUT /rtv/{id}`
- **Request:** `{ row_version, header: { main_reason, doc_date, return_date, rma_no, requester, warehouse_ref, cost_center_ref, return_address, note }, lines: [{ line_id, qty_return, return_reason, reason_note, source_location_ref, line_note, vat_mode }] }`
- **Precondition:** `status = draft` เท่านั้น
- **Response 200:** `RtvDetail` + `blockers[]` (รายการปัญหาที่ยังค้าง — จอเอาไปแสดงในกล่อง `ยังส่งอนุมัติไม่ได้`)
- **Logic:** → `FN-04 updateDraft` · `FN-05 validateRtv` · `FN-07 applyMainReason` (เมื่อ `main_reason` เปลี่ยน) · `ENG-RTV-01` · `ENG-RTV-02`
- **Concurrency:** optimistic lock ด้วย `row_version` (`BR-28 [AI-DEFAULT]`) — ไม่ตรง → `409 CONFLICT_STALE_RECORD` พร้อมข้อมูลล่าสุด
- **Errors:** `RTV_NOT_DRAFT` (409) · `QTY_OVER_RETURNABLE` (422) · `QTY_NEGATIVE` (422) · `REASON_REQUIRED` (422) · `REASON_NOTE_REQUIRED` (422) · `SOURCE_LOCATION_REQUIRED` (422) · `LINE_CONSUMED` (409)

### `F-PUR-RTV-API-07` · `POST /rtv/{id}/submit` ★ หัวใจที่หนึ่ง
- **Request:** `{ approvers: [{ slot_no, person_id }], idempotency_key }`
- **Precondition:** `status = draft` · ผ่าน `FN-05 validateRtv` ทั้งหมด · `approvers` ครบทุกขั้นที่ทะเบียน DOA คืนมา
- **Response 200:** `{ rtv_no, status: 'pending', doa_entry_ref, approval_base_amount, chain: [{ slot_no, role_label, person_id, person_name, person_position, decision }] }`
- **Logic:** → `FN-10 submitForApproval` → **DOA engine `resolve()`** (`FW-03`) · **`ENG-DOC-NUM.next('RTV')`** (`FW-04`)
- **ลำดับบังคับ (transaction เดียว):** ตรวจสถานะ → validate → **resolve สายใหม่ตามมูลค่าปัจจุบัน** (BR-11) → ตรวจว่า `approvers` ที่ส่งมาตรงกับสายที่ resolve ได้ทุกขั้น (BR-10) → ออกเลข **ถ้ายังไม่มี** (ส่งกลับแก้แล้วส่งใหม่ใช้เลขเดิม · `DR-08`) → freeze `approval_base_amount` → เขียน `T_rtv_approval` round ใหม่ → `status = pending` → audit
- **Idempotency:** `idempotency_key` **required** — กดซ้ำคืนผลเดิม ไม่ออกเลขซ้ำ (`BR-27 [AI-DEFAULT]` · `DR-10`)
- **Errors:** `RTV_NOT_DRAFT` (409) · `NO_LINE_WITH_QTY` (422) · `APPROVER_INCOMPLETE` (422) · `APPROVER_CHAIN_MISMATCH` (409 — สาย resolve ใหม่ไม่ตรงกับที่จอเลือกไว้ เช่นมูลค่าข้ามจุดตัดระหว่างทาง) · `SELF_APPROVAL_FORBIDDEN` (422) · `DOC_NUMBER_UNAVAILABLE` (503) · `DOA_ENTRY_NOT_CONFIGURED` (503)

### `F-PUR-RTV-API-08` · `POST /rtv/{id}/approve`
- **Request:** `{ comment?, idempotency_key }`
- **Precondition:** `status = pending` **และผู้เรียกคือคนที่ถูกเลือกไว้ในขั้นปัจจุบัน** (`BR-26` — ต้นแบบยังไม่ตรวจข้อนี้ ดู `07_LOCKED LD-13`)
- **Response 200:** `{ status, current_slot, chain[] }`
- **Logic:** → `FN-11 decideApproval(action='approve')`
- **ผลเมื่ออนุมัติขั้นสุดท้าย:** `status = approved` + audit `อนุมัติครบสาย` · **สต๊อกยังไม่ขยับ** (BR-13)
- **Errors:** `RTV_NOT_PENDING` (409) · `NOT_CURRENT_APPROVER` (403) · `SELF_APPROVAL_FORBIDDEN` (403)

### `F-PUR-RTV-API-09` / `API-10` · `sendback` / `reject`
- **Request:** `{ reason, idempotency_key }` — **`reason` required ทั้งคู่** (BR-12 · VR14/VR15)
- **`sendback`:** `status → draft` · **เลขเอกสารคงเดิม** (`DR-08`) · บันทึกผลขั้นเป็น `sendback` พร้อมเหตุผล
- **`reject`:** `status → cancelled` · `cancel_reason = reason` · **สต๊อกไม่ขยับ**
- **Logic:** → `FN-11 decideApproval(action='sendback'|'reject')`
- **Errors:** `RTV_NOT_PENDING` (409) · `REASON_REQUIRED` (422) · `NOT_CURRENT_APPROVER` (403)

### `F-PUR-RTV-API-11` · `POST /rtv/{id}/ship` ★ หัวใจที่สอง — จุดเดียวที่สต๊อกขยับ
- **Request:** `{ return_date, shipper, vehicle_no?, vendor_receiver?, idempotency_key }`
- **Precondition:** `status = approved` เท่านั้น (BR-09 · **ไม่มีทางลัด**) · `return_date` ไม่เป็นอนาคตและ ≥ วันที่รับของใน GRN
- **Response 200:** `{ status: 'returned', movements: [{ movement_id, line_id, item_ref, location_ref, qty, direction:'out', bucket }], grn_sync: { grn_ref, lines: [{ grn_line_no, returned_after, returnable_after }], reversal_locked: true } }`
- **Logic:** → `FN-12 shipReturn` → `ENG-RTV-03` (movement) · `ENG-RTV-04` (เขียนยอดคืนสะสม + ตั้งล็อกที่ GRN) → `ENG-NOTIFY.emit('rtv_returned')` + `ENG-CSQ.emit('rtv_returned','rtv_credit_expected')` (`FW-05` · `FW-06`) **นอก transaction**
- **Transaction:** ตัดสต๊อก + เขียนกลับ GRN + ตั้งล็อก อยู่ใน transaction เดียว (`DR-03`) · ต้อง **lock บรรทัดใบรับของ** กัน 2 ใบคืนตัดของก้อนเดียวกันพร้อมกัน
- **Idempotency:** `idempotency_key` **required** — กดรัว ๆ ต้องได้ movement ชุดเดียว (`DR-10` · `VR21`)
- **Errors:** `RTV_NOT_APPROVED` (409) · `RETURN_DATE_REQUIRED` (422) · `RETURN_DATE_FUTURE` (422) · `SHIPPER_REQUIRED` (422) · `QTY_OVER_RETURNABLE` (409 — ยอดคืนได้เปลี่ยนไปแล้วเพราะใบอื่นตัดก่อน) · `SOURCE_LOCATION_REQUIRED` (422) · `FORBIDDEN_ROLE` (403)

### `F-PUR-RTV-API-12` · `POST /rtv/{id}/credit`
- **Request:** `{ credit_doc_no, credit_date?, credit_amount_actual?, idempotency_key }`
- **Precondition:** `status = returned` · **`credit_doc_no` required** (BR-18 · VR19)
- **Response 200:** `{ status: 'closed', credit_doc_no, credit_amount_actual, credit_date }`
- **Logic:** → `FN-13 recordCredit` → `ENG-NOTIFY.emit('rtv_credited')` + `ENG-CSQ.emit('rtv_credited')`
- **★ ห้ามลงบัญชีจริงในรอบนี้** — `FW-01` (W5) · ระบบเก็บเลขอ้างอิงเท่านั้น (`OS-01`)
- **Errors:** `RTV_NOT_RETURNED` (409) · `CREDIT_DOC_REQUIRED` (422)

### `F-PUR-RTV-API-13` · `POST /rtv/{id}/reverse` ★ หัวใจที่สาม
- **Request:** `{ reason, reverse_location_ref, idempotency_key }` — **required ทั้งคู่** (BR-12 · VR20)
- **Precondition:** `status = returned` · ผู้เรียกเป็นหัวหน้าคลัง (`OQ-RTV-05` — รอบนี้ไม่จำกัดจำนวนวัน)
- **Response 200:** `{ status: 'reversed', counter_movements: [{ movement_id, reversal_of, direction:'in', location_ref }], grn_sync: { returned_after } }`
- **Logic:** → `FN-14 reverseRtv` → `ENG-RTV-03` (mode `reverse` — สร้างแถวตรงข้ามชี้ `reversal_of` · **ห้ามลบแถวเดิม** `DR-04`) · `ENG-RTV-04` (mode `revert` — หักยอดคืนสะสมคืน) → `ENG-NOTIFY.emit('rtv_reversed')` + `ENG-CSQ.emit('rtv_reversed')`
- **กลับรายการทำได้ทั้งใบเท่านั้น** (BR-16) — ไม่มีพารามิเตอร์เลือกบรรทัด
- **การปลดล็อกกลับรายการของ GRN ยังไม่เปิดในรอบนี้** (`OQ-RTV-07` · `EC-18`) — `grn_sync` ส่ง `reversal_locked` กลับตามสภาพจริงหลังหักยอด แต่ฝั่ง GRN ยังคงบล็อกไว้
- **Errors:** `RTV_NOT_RETURNED` (409) · `REASON_REQUIRED` (422) · `REVERSE_LOCATION_REQUIRED` (422) · `FORBIDDEN_ROLE` (403)

### `F-PUR-RTV-API-14` · `POST /rtv/{id}/cancel`
- **Request:** `{ reason, idempotency_key }` — **`reason` required** (BR-12 · VR16)
- **Precondition:** `status ∈ {draft, pending, approved}` — **ก่อนของออกเท่านั้น** (BR-17)
- **Response 200:** `{ status: 'cancelled', cancel_reason }` · **สต๊อกไม่ขยับ · ของกลับไปนับเป็นของที่คืนได้ตามเดิมโดยอัตโนมัติ** (เพราะยอดคืนสะสมนับเฉพาะ `returned`/`closed` · `DR-02`)
- **เส้นทาง "ทิ้งร่าง" (S-16) ใช้ endpoint เดียวกัน** — ใบที่ยกเลิกเป็น soft archive ค้นเจอผ่านสวิตช์ `รวมที่ยกเลิก/กลับรายการ` (`LD-12` · `OQ-RTV-12`)
- **Errors:** `RTV_ALREADY_SHIPPED` (409) · `REASON_REQUIRED` (422)

### `F-PUR-RTV-API-15` · เอกสารแนบ
- **`POST`:** multipart · ผ่าน Document Center · คืน `{ file_id, file_name, size, doc_center_ref }`
- **`DELETE`:** ตั้ง `is_removed = true` — **ไม่ลบแถว** (BR-22)
- **Precondition (สัญญาของ FRD):** แนบได้ทุกสถานะที่ยังไม่ใช่สถานะปลายทาง **รวม `returned`** เพื่อรองรับใบตอบรับผู้ขาย (S-35) และเอกสารเครดิต (S-12)
  > ⚠️ ต้นแบบยังแนบได้เฉพาะตอนเป็นร่าง — ช่องว่างที่ dev ต้องปิด ดู `07_LOCKED LD-15` · `OQ-RTV-15`

### `F-PUR-RTV-API-16` · `GET /rtv/{id}/print`
- **Response 200:** `{ header, parties, lines[], totals, signatures: [{ role, name, date }], watermark: 'none'|'draft'|'cancelled'|'reversed' }`
- **`watermark`:** `draft` (= ป้าย "ตัวอย่าง") เมื่อ `status ∉ {approved, returned, closed}` (BR-25) · `cancelled` · `reversed` ตามสถานะ
- **ปี ค.ศ. ทุกจุด รวมในไฟล์ที่ส่งออก** (BR-23 · `DR-08`)
- **Logic:** → `FN-16 buildPrintModel` · `ENG-RTV-02`

### `F-PUR-RTV-API-18` · `GET /rtv/doa-preview?amount=`
- **Response 200:** `{ doa_entry_ref, step_count, steps: [{ slot_no, role_label, candidates: [{ person_id, person_name, person_position }] }] }`
- **อ่านอย่างเดียว ไม่ freeze อะไร** — ใช้แสดงที่ขั้น 5 และเติมตัวเลือกให้ combobox ของหน้าต่างส่งอนุมัติ
- **`candidates` มาจากทะเบียน DOA/ทะเบียนพนักงาน** — จอแสดงเฉพาะ **ชื่อ + ตำแหน่ง + รูป** ห้ามแสดงรหัส role (LOCK-03)

## §2.3 Request validation ที่อยู่ชั้น HTTP (trivial เท่านั้น)

`required` · รูปแบบวันที่ ISO · ชนิดตัวเลข · ขนาด/ชนิดไฟล์แนบ (PDF/JPG/PNG/ZIP ≤ 20 MB) · รูปแบบ `idempotency_key`
**กติกาธุรกิจทั้งหมดอยู่ที่ `03_LOGIC` + `05_RULES`** (Logic Placement Matrix #1–2) — ห้ามมีการคำนวณยอดคืนได้หรือกฎสถานะในชั้นนี้

## §2.4 สิทธิ์ต่อ endpoint (จาก BRD §4.2)

| Endpoint | จนท.คลัง | หน.คลัง | จนท.จัดซื้อ | หน.จัดซื้อ | ผอ.สายงาน | QC | AP | ผู้ดูแล |
|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| API-01/02/03/16/17/18 (อ่าน) | ✅ คลังตัวเอง | ✅ ทุกคลัง | ✅ PO ของตน | ✅ | ✅ | ✅ (ตัดราคา) | ✅ | ✅ |
| API-04/05/06 (ร่าง) | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| API-07 (ส่งอนุมัติ) | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| API-08/09/10 (ตัดสินใจอนุมัติ) | ❌ | ✅¹ | ❌ | ✅¹ | ✅¹ | ❌ | ❌ | ❌ |
| **API-11 (บันทึกส่งคืน — ตัดสต๊อก)** | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| API-12 (บันทึกเครดิต · ปิดใบ) | ❌ | ❌ | ✅ | ✅ | ❌ | ❌ | ✅ | ❌ |
| **API-13 (กลับรายการ)** | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| API-14 (ยกเลิกก่อนของออก) | ✅² | ✅ | ✅² | ✅ | ❌ | ❌ | ❌ | ❌ |
| API-15 (เอกสารแนบ) | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ❌ | ❌ |

¹ **เฉพาะคนที่ถูกเลือกเป็นผู้อนุมัติของขั้นปัจจุบันในใบนั้น** — ไม่ใช่ทุกคนในตำแหน่ง (`BR-26` · `C-01`/`C-04`)
² เฉพาะใบที่ตัวเองสร้าง

> **Confidential field (`unit_price` · `discount_pct` · `line_total` · `total_grand` · `approval_base_amount` · `credit_amount_actual`) ต้องถูกตัดออกจาก response ของผู้ตรวจคุณภาพ** (`04_DB §4.6` · `05_RULES §5.7`)

## §2.5 Error catalog

| Code | HTTP | ข้อความบนจอ (ยึดถ้อยคำที่ต้นแบบใช้จริง) |
|---|---|---|
| `GRN_NOT_SELECTABLE` | 409 | "{เหตุผลจาก `block_reason`}" — เช่น "คืนครบแล้ว — ไม่มีของคงเหลือให้คืน" |
| `GRN_NOT_FOUND` | 404 | "ไม่พบใบรับของ {เลขที่}" |
| `RTV_NOT_DRAFT` | 409 | "แก้ไขได้เฉพาะใบที่เป็นร่าง" |
| `RTV_NOT_PENDING` | 409 | "ตัดสินใจอนุมัติได้เฉพาะใบที่รออนุมัติ" |
| `RTV_NOT_APPROVED` | 409 | "บันทึกส่งคืนได้เฉพาะใบที่อนุมัติครบแล้ว" |
| `RTV_NOT_RETURNED` | 409 | "ทำรายการนี้ได้เฉพาะใบที่ส่งคืนแล้ว" |
| `RTV_ALREADY_SHIPPED` | 409 | "ของออกจากคลังแล้ว ยกเลิกไม่ได้ — ต้องใช้กลับรายการแทน" |
| `QTY_OVER_RETURNABLE` | 422 / 409 | "เกินยอดคืนได้ (สูงสุด {N} {หน่วย})" |
| `QTY_NEGATIVE` | 422 | "จำนวนคืนติดลบไม่ได้" |
| `NO_LINE_WITH_QTY` | 422 | "ต้องมีอย่างน้อย 1 บรรทัดที่จำนวนคืนมากกว่า 0" |
| `REASON_REQUIRED` | 422 | "ต้องระบุเหตุผลคืน" / "กรุณาระบุเหตุผลที่ส่งกลับแก้" / "กรุณาระบุเหตุผลที่ปฏิเสธ" / "กรุณาระบุเหตุผลที่ยกเลิก" / "กรุณาระบุเหตุผลที่กลับรายการ" |
| `REASON_NOTE_REQUIRED` | 422 | "เลือก “อื่น ๆ” ต้องพิมพ์คำอธิบาย" |
| `SOURCE_LOCATION_REQUIRED` | 422 | "ต้องระบุ location ต้นทางที่ตัดของออก" |
| `LINE_CONSUMED` | 409 | "ของถูกใช้ต่อแล้ว — {เอกสารปลายทาง}" |
| `APPROVER_INCOMPLETE` | 422 | "ต้องเลือกผู้อนุมัติให้ครบทุกขั้น" |
| `APPROVER_CHAIN_MISMATCH` | 409 | "มูลค่าเปลี่ยนแล้ว — สายอนุมัติถูกคำนวณใหม่ กรุณาเลือกผู้อนุมัติอีกครั้ง" |
| `NOT_CURRENT_APPROVER` | 403 | "คุณไม่ใช่ผู้อนุมัติของขั้นนี้" |
| `SELF_APPROVAL_FORBIDDEN` | 403 | "ผู้จัดทำอนุมัติใบของตัวเองไม่ได้" |
| `RETURN_DATE_REQUIRED` | 422 | "กรุณาระบุวันที่ส่งคืนจริง" |
| `RETURN_DATE_FUTURE` | 422 | "วันที่ส่งคืนจริงต้องไม่เป็นอนาคต" |
| `SHIPPER_REQUIRED` | 422 | "กรุณาระบุผู้ส่งของคืน" |
| `REVERSE_LOCATION_REQUIRED` | 422 | "กรุณาระบุ location ที่รับของกลับเข้า" |
| `CREDIT_DOC_REQUIRED` | 422 | "ต้องระบุเลขที่เอกสารเครดิตของผู้ขายก่อนปิดใบ" |
| `CONFLICT_STALE_RECORD` | 409 | "มีคนแก้ใบนี้ไปก่อนหน้า — โหลดข้อมูลล่าสุดแล้วลองใหม่" |
| `DOC_NUMBER_UNAVAILABLE` | 503 | "ออกเลขเอกสารไม่สำเร็จ — ลองใหม่อีกครั้ง" |
| `DOA_ENTRY_NOT_CONFIGURED` | 503 | "ยังไม่ได้ตั้งสายอนุมัติของใบคืนสินค้า — ติดต่อผู้ดูแลระบบ" |
| `FORBIDDEN_ROLE` | 403 | "สิทธิ์ไม่พอสำหรับการกระทำนี้" |

## §2.6 Idempotency & concurrency

- **`POST` ทุกตัวที่เปลี่ยนสถานะ (07–15) ต้องส่ง `idempotency_key`** — เก็บผลลัพธ์ 24 ชม. · กดซ้ำคืนผลเดิม ไม่เกิดใบ/เลข/movement ซ้ำ (`BR-27 [AI-DEFAULT]` · `DR-10`)
- **`PUT /rtv/{id}` ใช้ optimistic lock ด้วย `row_version`** (`BR-28 [AI-DEFAULT]`) → ไม่ตรง = `409 CONFLICT_STALE_RECORD` พร้อมข้อมูลล่าสุด
- **`POST .../ship` ต้อง lock บรรทัดใบรับของ** ระหว่าง transaction — สองใบคืนที่อ้าง GRN line เดียวกันบันทึกส่งคืนพร้อมกันต้องมีใบเดียวที่ผ่าน อีกใบได้ `QTY_OVER_RETURNABLE` (`EC-21`)
- **`ENG-NOTIFY` / `ENG-CSQ` ยิงนอก transaction** — ล้มเหลวต้องไม่ย้อนการตัดสต๊อก (retry ผ่านคิวของ engine)

## §2.7 Cross-Module Contract (R12 · จาก BRD §12.1 + §3.1/§3.2)

### §2.7.1 ขาเข้า — `IS-01`..`IS-12` (BRD §3.1 · ครบทุกรหัส ไม่ย่อ)

| IS | สาระ | ที่อยู่ในแพ็กนี้ |
|---|---|---|
| **IS-01** | สร้างใบคืนโดยอ้างใบรับของ (GRN) ที่บันทึกรับเข้าแล้วและยังมีของคืนได้ | `API-03` · `API-04` · `FN-02` · `FN-03` · `BR-01` · `AT-02` |
| **IS-02** | เลือกบรรทัดและจำนวนที่จะคืน โดยระบบคุมเพดานตามของที่มีอยู่จริง (หักที่เคยคืนไปแล้ว) | `ENG-RTV-01` · `BR-04` · `DR-01`/`DR-02` · `AT-09` · `AT-12` |
| **IS-03** | ระบุเหตุผลคืนต่อบรรทัด (ชำรุด/ผิดสเปค/บรรจุภัณฑ์เสียหาย/ใกล้หมดอายุ/รับเกิน/อื่น ๆ) | `04_DB return_reason` · `BR-06` · `CF-04` · `AT-15`/`AT-18` |
| **IS-04** | ระบุที่อยู่ของของที่จะตัดออก (พื้นที่กักกัน หรือพื้นที่จัดเก็บปกติ) รายบรรทัด | `04_DB source_location_ref` · `BR-07`/`BR-08` · `FN-07` · `AT-16`/`AT-17` |
| **IS-05** | สายอนุมัติตามมูลค่าที่คืน โดยเลือก **คนจริง** ต่อขั้นตอนส่งอนุมัติ | `API-07` · `API-18` · `FN-10` · `BR-09`/`BR-10` · `DOA_BRIEF` · `AT-22`/`AT-25` |
| **IS-06** | บันทึกส่งคืน = ตัดสต๊อกออกจริง (ความเคลื่อนไหวแบบต่อท้ายอย่างเดียว) | `API-11` · `FN-12` · `ENG-RTV-03` · `BR-13`/`BR-14`/`BR-15` · `AT-33`..`AT-36` |
| **IS-07** | พิมพ์ใบคืนสินค้า A4 ให้ผู้ขายเซ็นรับ (ก่อนอนุมัติพิมพ์ได้แค่ตัวอย่าง) | `API-16` · `FN-16` · `BR-25` · `print-spec-rtv.md` · `AT-42` |
| **IS-08** | บันทึกเลขเอกสารเครดิตจากผู้ขายเพื่อปิดใบ | `API-12` · `FN-13` · `BR-18` · `AT-40`/`AT-41` |
| **IS-09** | ยกเลิกก่อนของออก และกลับรายการหลังของออก (พร้อมเหตุผลบังคับ) | `API-13` · `API-14` · `FN-14`/`FN-15` · `BR-12`/`BR-16`/`BR-17` · `AT-43`..`AT-47` |
| **IS-10** | แนบเอกสารประกอบ (รูปของเสีย · ใบส่งคืน · ใบตอบรับ · เอกสารเครดิต) | `API-15` · `AT-50` · ⚠️ ช่องว่าง `LD-15` |
| **IS-11** | หน้ารายการพร้อมตัวชี้วัด ค้นหา ตัวกรอง และส่งออก CSV | `API-01` · `API-17` · `FN-01`/`FN-18` · `AT-90` |
| **IS-12** | ล็อกใบรับของต้นทางไม่ให้กลับรายการหลังของถูกคืนไปแล้ว | `ENG-RTV-04` · `BR-20` · `DR-05` · `AT-37` · `AT-X-02` |

**สัญญาข้อมูลที่รับเข้ามาจริง**

| จาก | สัญญา | ถ้าต้นทางเปลี่ยนกลางทาง |
|---|---|---|
| **F079 GRN** | `GET /warehouse/grn/{ref}/returnable-lines` → `{ grn_line_no, item_ref, item_name, uom, qty_received, qty_qc_failed, qty_over, qc_reason, quarantine_location_ref, stock_location_ref, unit_price, discount_pct, vat_mode, vat_pct, consumed(bool), consumed_ref }` | GRN ถูกกลับรายการ/คืนครบระหว่างร่าง → `GRN_NOT_SELECTABLE` ตอนส่งอนุมัติหรือบันทึกส่งคืน (`EC-03`/`EC-04`) · ผู้ใช้กด `API-06 refresh-from-grn` เพื่อดึงใหม่ |
| **F078 PO** | `GET /purchase/po/{ref}` → header ไว้แสดงลิงก์เท่านั้น | **ไม่มีผลใด ๆ** — RTV อ่านอย่างเดียว |
| ทะเบียนกลาง | ผู้ขาย · สินค้า · หน่วย · ตำแหน่ง/คลัง · ศูนย์ต้นทุน · พนักงาน | **soft-ref** — ค่าที่หายยังแสดงข้อความ snapshot เดิม ใบเก่าไม่พัง (`EC-14`) |
| **ทะเบียน DOA (F-DLG-001)** | `resolve({ feature:'F-PUR-RTV', amount })` → `{ entry, mode:'sequential', steps:[{ slot_no, role_label, candidates[] }] }` | แก้ทะเบียนภายหลัง **ไม่กระทบใบที่ส่งไปแล้ว** (freeze ที่ `T_rtv_approval` · `BR-DOA-02` · `C-09`) |
| **ทะเบียนเอกสาร (F-DOCCFG)** | `ENG-DOC-NUM.next('RTV', company_ctx)` → `RTV-YYYY-NNNN` | ออกเลขล้มเหลว = ไม่มีใบครึ่ง ๆ (`DOC_NUMBER_UNAVAILABLE`) |
| คอนฟิกพื้นที่กักกันต่อคลัง (**CF-03**) | ค่าตั้งต้นของ `source_location_ref` เมื่อเหตุผล = QC ไม่ผ่าน | เปลี่ยนค่าภายหลังไม่กระทบใบที่บันทึกแล้ว (เก็บ snapshot ในบรรทัด) |

### §2.7.2 ขาออก — `OS-01`..`OS-09` (BRD §3.2 · ครบทุกรหัส) + เส้นที่เขียนจริง

| OS | สาระ | สถานะในรอบนี้ |
|---|---|---|
| **OS-01** | ออกใบลดหนี้ (CN) และการลงบัญชีจริง | ❌ **นอกขอบเขต — คลื่น W5** · รอบนี้เก็บเลขอ้างอิง + ป้ายสถานะเท่านั้น · hook = **`FW-01`** · ทดสอบสัญญาที่ `AT-X-06` |
| **OS-02** | เปิดยอดค้างรับกลับที่ใบสั่งซื้ออัตโนมัติ | ❌ **ตัดสินแล้วว่าไม่ทำ** — `OQ-RTV-01 [ASSUMED]` · `BR-19` · `DR-06` · **มีเคสกันไม่ให้งอกกลับที่ `AT-38` · `AT-X-03`** |
| **OS-03** | เปิดใบรับของทดแทน (replacement) อัตโนมัติ | ❌ **ไม่ทำ** — จัดซื้อเปิดใบสั่งซื้อใหม่เอง · กันไว้ที่ `AT-49` |
| **OS-04** | ค่าขนส่งคืน / ค่าธรรมเนียมคืนของ | ❌ **นอกขอบเขต** — ต้องมีต้นทุนแฝง (F069 · W4) ก่อน · กันไว้ที่ `AT-49` |
| **OS-05** | Lot / Serial / วันหมดอายุ ของที่คืน | ❌ **ไม่ทำ** — ยังไม่มีทะเบียน Lot ในเลนนี้ · กันไว้ที่ `AT-49` |
| **OS-06** | คืนของที่ไม่มีใบรับของ | ❌ **ไม่ทำ** — ใช้ปรับปรุงสต๊อก (W3Q) · ช่องบนจอเป็น `is-off` · กันไว้ที่ `AT-01` · `AT-49` |
| **OS-07** | ใบคืนใบเดียวข้ามใบรับของหลายใบ | ❌ **ไม่ทำ** — เปลี่ยนใบรับของ = ล้างบรรทัด · กันไว้ที่ `AT-49` |
| **OS-08** | ติดตามสถานะฝั่งผู้ขาย (ผู้ขายรับ/ปฏิเสธในระบบ) | ❌ **นอกขอบเขต** — เก็บเป็นเอกสารแนบ + เส้นทางกลับรายการ · `AT-50` |
| **OS-09** | การจัดเก็บลง bin และการตรวจ availability จริง | ❌ **นอกขอบเขต — คลื่น W3Q** · hook = **`FW-02`** · ทดสอบสัญญาที่ `AT-X-07` |

> ทั้ง 9 ข้อเป็น **ขอบเขตที่ตัดออกอย่างตั้งใจ ไม่ใช่งานที่ตกหล่น** — `OS-02` `OS-03` `OS-04` `OS-05` `OS-06` `OS-07` มีเคสทดสอบคอยกันไม่ให้งอกกลับเข้ามา

**สัญญาข้อมูลที่ส่งออกจริง (เส้นที่ RTV เขียนได้)**

| ไป | สัญญา | ตอนกลับรายการ |
|---|---|---|
| **F079 GRN** (ยอดคืนสะสม) | `PATCH /warehouse/grn/{ref}/returned` → `{ lines:[{ grn_line_no, qty_delta }] }` — **เขียนได้จาก RTV เท่านั้น** · บรรทัด GRN ขึ้นป้าย `คืนบางส่วนแล้ว`/`คืนครบแล้ว` + ลิงก์มาที่ใบ RTV | ส่ง `qty_delta` ติดลบ (หักคืน) — **ไม่ลบประวัติเดิม** |
| **F079 GRN** (ล็อกกลับรายการ) | `PATCH /warehouse/grn/{ref}/reversal-lock` → `{ locked: true, locked_by_rtv: rtv_no }` — ฝั่ง GRN ต้องปิดปุ่มกลับรายการพร้อมเหตุผลที่ชี้มาที่ใบคืน (`BR-20` · `LOCK-08`) | **ยังไม่ปลดล็อกในรอบนี้** (`OQ-RTV-07` · `EC-18`) |
| **F078 PO** | **ไม่มีเส้นเขียน** — `DR-06` ห้ามเขียนค่าใด ๆ กลับใบสั่งซื้อ | ไม่มีอะไรต้องย้อน |
| ยอดคงคลัง / ความเคลื่อนไหว | movement `out` จาก `source_location_ref` (bucket `quarantine` หรือ `stock`) | movement `in` ทิศตรงข้าม ชี้ `reversal_of` — **ของเดิมยังอยู่** |
| **ENG-NOTIFY** | 5 เหตุการณ์ตาม `NTF_BRIEF_F-PUR-RTV.md` (`rtv_returned` · `rtv_credited` · `rtv_reversed` · `rtv_cancelled` · `rtv_quarantine_aging`) — **ไม่ประกาศซ้ำ `doa_pending`/`doa_result`** | `rtv_reversed` (ปิดไม่ได้ — บังคับส่ง) |
| **ENG-CSQ** | 5 เหตุการณ์ตาม `CSQ_BRIEF_F-PUR-RTV.md` (`rtv_returned` EC · `rtv_credit_expected` FC · `rtv_credited` FC · `rtv_reversed` EC/FC avoided · `rtv_cancelled` no-effect) | `rtv_reversed` แบบ `avoided` — **ห้ามลบผลเดิม** |
| **AP / GL (W5)** | มูลค่าที่คืน: ยอดก่อนภาษี · ภาษี · รวม รายบรรทัดและทั้งใบ | `FW-01` — ยังไม่ต่อจริง · ห้ามให้ทั้ง RTV และ AP ยิงท่อ AC ซ้ำ (`CSQ-Q2`) |
| **Putaway / Stock (W3Q)** | ตรวจว่าของยังอยู่ที่ตำแหน่งจริงก่อนให้คืน | `FW-02` — ยังไม่ต่อจริง · รอบนี้ใช้ flag `consumed` ที่มาจาก GRN |

> **สถานะการต่อจริง:** สัญญาทั้งหมดข้างบน**ประกาศครบ** · ปลายทางที่พร้อมแล้ว (GRN · DOA · DOC-NUM · NOTIFY · CSQ) **ต้องต่อจริงใน P1–P2** · ปลายทางข้ามคลื่น (AP/GL · Putaway) **คงเป็นสัญญาเรียกใช้ ห้ามทำแทน** — ดู `00_OVERVIEW §0.15`
