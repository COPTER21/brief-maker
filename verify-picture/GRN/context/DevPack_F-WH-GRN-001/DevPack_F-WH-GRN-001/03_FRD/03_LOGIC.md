# 03_LOGIC — F-WH-GRN · GRN รับของ

> Audience: BE dev (business logic layer) · ไม่มีศัพท์ HTTP ในส่วน Engine
> ★ `FN-xx` ในไฟล์นี้ = **ฟังก์ชันชั้นโค้ด** — คนละชุดกับ `FN-01..FN-94` ของ `FUNCTION_CHECKLIST` (ฟังก์ชันเชิงธุรกิจ) · ดู `00_OVERVIEW §0.12.5`

## §3.1 Functions (scope-local)

### `F-WH-GRN-FN-01` · `listGrn`
- **Purpose:** ประกอบคิวรีรายการ + KPI ตามตัวกรอง 5 ตัว + ขอบเขตสิทธิ์ของผู้ใช้
- **Input:** `{ filters, userScope }` · **Output:** `{ rows[], kpi{} }`
- **Invoked by:** `API-01` · **Side effects:** —

### `F-WH-GRN-FN-02` · `getSelectablePos`
- **Purpose:** คัดใบสั่งซื้อที่รับของได้ + ให้เหตุผลรายใบสำหรับใบที่เลือกไม่ได้
- **Input:** `{ userScope }` · **Output:** `[{ po_ref, selectable, block_reason, open_qty }]`
- **Logic:** เลือกได้เมื่อ `status ∈ {sent, partially received}` **และ** มีบรรทัดที่ `qty_ordered − received > 0` **และ** ไม่ `shortClosed` (R02)
- **Invoked by:** `API-03` · **Implements:** BR-01 · BR-02

### `F-WH-GRN-FN-03` · `buildDraftFromPo`
- **Purpose:** สร้างฉบับร่างจากใบสั่งซื้อ — ดึงเฉพาะบรรทัดที่ยังค้างรับ
- **Input:** `{ po_ref, actor }` · **Output:** `GrnDraft`
- **Logic:** คัดบรรทัด `qty_open > 0` → คัดลอก `item/uom/unit_price/discount_pct/vat_mode/vat_pct/tolerance_pct/want_date` แบบ **อ่านอย่างเดียว** · ตั้ง `quarantine_ref` จากคอนฟิกของคลัง (CF-04) · `dest_location_ref` = คลังของใบสั่งซื้อ
- **Invoked by:** `API-04` · **Side effects:** INSERT header+lines · audit `created`
- **Implements:** BR-01 · BR-03

### `F-WH-GRN-FN-04` · `updateDraft`
- **Purpose:** บันทึกการแก้ฉบับร่าง (ข้อมูลหลัก + จำนวนรับ + ผลตรวจ)
- **Input:** `{ grn_id, header, lines[], actor }` · **Output:** `GrnDraft | ValidationError[]`
- **Logic:** ปฏิเสธถ้า `status ≠ draft` (R14) · เรียก `FN-05` · เขียน audit ค่าก่อน-หลัง
- **Invoked by:** `API-05` · **Calls:** FN-05 · ENG-GRN-01 · ENG-GRN-02

### `F-WH-GRN-FN-05` · `validateGrn`
- **Purpose:** ตรวจทั้งใบตาม VR01–VR16 ก่อนบันทึกร่าง/บันทึกรับเข้า
- **Input:** `GrnDraft` · **Output:** `ValidationError[]`
- **Logic:** เรียก `ENG-GRN-02` (เพดานรับ) + `ENG-GRN-01` (ผลตรวจ) แล้วรวมผล + ตรวจ field บังคับของหัวเอกสาร
- **Invoked by:** FN-04 · FN-11

### `F-WH-GRN-FN-06` · `refreshFromPo`
- **Purpose:** ดึงข้อมูลจากใบสั่งซื้อใหม่เมื่อต้นทางถูกแก้แล้วอนุมัติใหม่
- **Input:** `{ grn_id }` · **Output:** `GrnDraft`
- **Logic:** อัปเดต `qty_ordered · qty_received_before · unit_price · tolerance_pct · want_date` · **คงค่าที่ผู้ใช้กรอกไว้** (`qty_received_now` · ผลตรวจ · หมายเหตุ) แล้ว re-validate
- **Invoked by:** `API-06` · **Implements:** E-07

### `F-WH-GRN-FN-07` · `checkDuplicateDeliveryNote`
- **Purpose:** ตรวจเลขใบส่งของซ้ำของผู้ขายรายเดียวกัน
- **Input:** `{ vendor_ref, delivery_note_no, exclude_grn_id? }` · **Output:** `{ duplicate, existing[] }`
- **Logic:** เทียบเฉพาะใบที่ `status ≠ draft` · **เตือนอย่างเดียว ไม่บล็อก** · เกณฑ์จากกติกากลาง (CF-06)
- **Invoked by:** `API-12` · **Implements:** BR-18 · VR03 · E-08

### `F-WH-GRN-FN-08` · `computeLineAmounts`
- **Purpose:** คำนวณยอดต่อบรรทัดและยอดรวมทั้งใบ
- **Input:** `GrnLine[]` · **Output:** `{ lines[], totals: { before, vat, after, grand } }`
- **Logic:** `line_amount = qty_received_now × (unit_price × (1 − discount_pct/100))` → VAT ตาม `vat_mode` (`none` / `add` บวกเพิ่ม / `net` รวมแล้ว)
- **Invoked by:** FN-04 · FN-11 · API-02 · API-11

### `F-WH-GRN-FN-09` · `computeReceiptSplit`
- **Purpose:** แยกยอดเข้าคลังปกติกับเข้าโซนกักของ
- **Input:** `GrnLine[]` · **Output:** `{ good_qty, reject_qty, per_line[] }`
- **Logic:** `qty_good = qty_received_now − qty_rejected` · บรรทัดบริการไม่นับทั้งสองฝั่ง
- **Invoked by:** FN-11 · ENG-GRN-03 · **Implements:** BR-12 · FN-16 (checklist)

### `F-WH-GRN-FN-10` · `isServiceLine`
- **Purpose:** ตัดบรรทัดบริการออกจากผลตรวจและความเคลื่อนไหว
- **Input:** `GrnLine` · **Output:** `bool`
- **Logic:** `line_kind === 'service'` → ไม่มี `qc_result` · ไม่สร้าง movement · **ยังปิดยอดค้างที่ใบสั่งซื้อได้**
- **Invoked by:** ENG-GRN-01 · ENG-GRN-03 · ENG-GRN-04 · **Implements:** BR-08

### `F-WH-GRN-FN-11` · `postGrn` ★
- **Purpose:** บันทึกรับเข้าคลัง — ขั้นตอนเดียวที่เปลี่ยนสต๊อกจริง
- **Input:** `{ grn_id, receiver, qc_inspector?, idempotency_key, actor }`
- **Output:** `{ grn_no, movements[], po_sync }`
- **Logic (ลำดับบังคับ ใน transaction เดียว):**
  1. ตรวจ `status = draft` · ตรวจใบสั่งซื้อยังพร้อมรับของ ณ เวลานี้ (R17)
  2. `FN-05 validateGrn` — ผิดข้อใดข้อหนึ่ง = หยุด ไม่เขียนอะไรเลย
  3. `ENG-DOC-NUM.next('GRN')` → `grn_no` (**ห้าม feature ตั้งเลขเอง** — R20/LOCK-05)
  4. `ENG-GRN-03` สร้าง movement 2 ชุด (`stock` + `quarantine`)
  5. `ENG-GRN-04` ตัดยอด + sync สถานะใบสั่งซื้อ
  6. `status = posted` · เขียน audit · ตั้งป้าย `gr_ir_status = "รอตั้ง GR/IR"` · `gr_ir_amount = totals.before`
  7. `ENG-NOTIFY.emit` + `ENG-CSQ.emit` (**นอก transaction** — ล้มเหลวต้องไม่ย้อนการรับของ)
- **Side effects:** UPDATE header · INSERT movement · UPDATE PO.received · INSERT audit
- **Implements:** BR-04..BR-09 · BR-12 · BR-20 · BR-23

### `F-WH-GRN-FN-12` · `discardDraft`
- **Purpose:** ทิ้งฉบับร่างแบบ soft archive
- **Logic:** บังคับเหตุผล (VR15) · **ไม่กระทบสต๊อก/ใบสั่งซื้อ** · ยังค้นเจอผ่านตัวกรอง "รวมที่ยกเลิก/กลับรายการ"
- **Invoked by:** `API-09` · **Implements:** BR-21

### `F-WH-GRN-FN-13` · `reverseGrn` ★
- **Purpose:** กลับรายการทั้งใบ
- **Input:** `{ grn_id, reason, idempotency_key, actor }`
- **Logic:**
  1. ตรวจ `status = posted` · ผู้ใช้เป็นหัวหน้าคลัง · **ของยังไม่ถูกใช้ต่อ** (R16 — ยังไม่คืนผู้ขาย/ยังไม่ถูกย้ายออก)
  2. บังคับเหตุผล (VR15)
  3. `ENG-GRN-03` สร้าง movement **ตรงข้าม** ทุกแถว พร้อม `reversal_of` — **ห้ามลบแถวเดิม** (LOCK-02)
  4. `ENG-GRN-04` หักยอดรับสะสมคืนที่ใบสั่งซื้อ + ถอยสถานะ
  5. `status = reversed` (สถานะปลายทาง อ่านอย่างเดียว) · audit
- **Implements:** BR-14 · BR-15 · BR-16 · E-11

### `F-WH-GRN-FN-14` · `lateDays`
- **Purpose:** คำนวณจำนวนวันที่ของมาถึงช้ากว่ากำหนดในใบสั่งซื้อ
- **Logic:** `max(0, receive_date − want_date)` ต่อบรรทัด → เอาค่ามากสุดเป็นของทั้งใบ · ป้อน KPI
- **Implements:** E-09 · FN-13 (checklist)

### `F-WH-GRN-FN-15` · `buildPrintModel`
- **Purpose:** ประกอบข้อมูลเอกสารพิมพ์ A4 ตาม `print-spec-grn.md`
- **Logic:** **ปี ค.ศ. ทุกจุด** (R19) · 3 ช่องลงชื่อ (ผู้ส่งของ · ผู้รับของ · ผู้ตรวจคุณภาพ)
- **Invoked by:** `API-11`

## §3.2 Engines (reusable / CUBIC-registered)

### `ENG-GRN-01` · `grn-qc-engine`
- **code:** `grn-qc-engine` · **category:** `quality-control`
- **input:** `{ lines: [{ line_kind, qty_received_now, qc_result, qty_rejected, reject_reason, quarantine_ref }], header_quarantine_ref }`
- **output:** `{ valid: bool, errors: [{ line_no, code }], split: [{ line_no, qty_good, qty_quarantine }] }`
- **logic outline:**
  1. บรรทัดบริการ → ข้าม (ไม่มีผลตรวจ)
  2. `qc_result = pass` → `qty_rejected = 0` · `qty_good = qty_received_now`
  3. `qc_result = partial` → บังคับ `0 < qty_rejected < qty_received_now` + เหตุผล + โซนกัก + ผู้ตรวจ
  4. `qc_result = fail` → `qty_rejected = qty_received_now` · **`qty_good = 0`** (เข้าโซนกักทั้งจำนวน)
  5. มีของไม่ผ่าน → `quarantine_ref` บังคับ และ **ต้องต่างจากคลังปลายทาง**
- **Used by:** F-WH-GRN (F080 RTV จะใช้ผลตรวจนี้เป็นต้นทาง)
- **Implements:** BR-09 · BR-10 · VR10..VR13 · E-04 · E-05
- **Iron rule:** ✅ pure · ไม่มีศัพท์ HTTP

### `ENG-GRN-02` · `receipt-tolerance-engine`
- **code:** `receipt-tolerance-engine` · **category:** `validation-calculation`
- **input:** `{ lines: [{ qty_ordered, qty_received_before, tolerance_pct, qty_received_now, line_note }] }`
- **output:** `{ valid, errors[], per_line: [{ qty_open, qty_cap, qty_open_after, over: bool }] }`
- **logic outline:**
  1. `qty_open = max(0, qty_ordered − qty_received_before)`
  2. `qty_cap = qty_open × (1 + tolerance_pct/100)` — `tolerance_pct` ตั้งต้น **0%** (CF-01 · `[ASSUMED OQ-PO-01]`)
  3. `qty_received_now > qty_cap` → **บล็อก** `QTY_OVER_CAP` พร้อมบอกเพดาน (VR08)
  4. `qty_open < qty_received_now ≤ qty_cap` → ผ่านแต่ **บังคับ `line_note`** (R07 · VR09)
  5. ทุกบรรทัด `qty_received_now = 0` → `NO_LINE_WITH_QTY` (R04)
  6. `qty_received_now < 0` → ปฏิเสธ (R05)
- **Used by:** F-WH-GRN (ใช้ซ้ำได้กับ RTV/AP 3-way matching)
- **Implements:** BR-04..BR-07 · E-01 · E-02 · E-03
- **Iron rule:** ✅ pure

### `ENG-GRN-03` · `stock-movement-engine`
- **code:** `stock-movement-engine` · **category:** `inventory`
- **input:** `{ grn_ref, lines: [{ line_ref, item_ref, qty_good, qty_quarantine, dest_location_ref, quarantine_ref }], mode: 'post' | 'reverse', origin_movements? }`
- **output:** `{ movements: [{ item_ref, location_ref, qty, direction, bucket, reversal_of? }] }`
- **logic outline:**
  1. `mode = post` → ต่อบรรทัด สร้างได้สูงสุด 2 แถว: `qty_good > 0` → `in · stock` · `qty_quarantine > 0` → `in · quarantine`
  2. `mode = reverse` → อ่าน `origin_movements` แล้วสร้างแถว **ทิศตรงข้าม** ทุกแถว ตั้ง `reversal_of = origin.movement_id`
  3. บรรทัดบริการ → **ไม่สร้างแถวใด ๆ**
  4. **ต่อท้ายอย่างเดียว** — engine นี้ไม่มีเส้นทาง update/delete (LOCK-02 · R14)
- **Used by:** F-WH-GRN · F081 Putaway · F080 RTV (วางแผน)
- **Implements:** BR-12 · BR-14 · E-05
- **Iron rule:** ✅ pure

### `ENG-GRN-04` · `po-receipt-sync-engine`
- **code:** `po-receipt-sync-engine` · **category:** `document-sync`
- **input:** `{ po_ref, lines: [{ po_line_no, qty_received_now }], mode: 'apply' | 'revert' }`
- **output:** `{ po_status, lines: [{ po_line_no, received_after, open_after }] }`
- **logic outline:**
  1. `mode = apply` → `received += qty_received_now` **(รวมส่วนที่ไม่ผ่านตรวจด้วย — R11)**
  2. `mode = revert` → `received −= qty_received_now` (ไม่ต่ำกว่า 0)
  3. คำนวณสถานะ: ทุกบรรทัดปิดยอด → `closed` · มีรับบางส่วน → `partially received` · ยอดรับรวม = 0 → `sent`
  4. บรรทัดบริการปิดยอดได้ตามปกติ (BR-08)
- **★ ข้อบังคับ:** engine นี้เป็น **ทางเดียว** ที่เขียน `PO.received` ได้ (R13 · LOCK) — ห้ามมีเส้นทางแก้ด้วยมือ
- **Used by:** F-WH-GRN (F080 RTV อาจใช้เมื่อ Q2 เคาะแล้ว)
- **Implements:** BR-11 · BR-13 · E-10 · E-11
- **Iron rule:** ✅ pure

### Engine กลางที่ **เรียกใช้** (ไม่ได้เป็นเจ้าของ — ประกาศผ่านใบใน `03_FRD/`)

| Engine | ใบประกาศ | สัญญา |
|---|---|---|
| `ENG-DOC-NUM` | `DOCCFG_BRIEF_F-WH-GRN.md` | `next('GRN')` → `GRN-YYYY-NNNN` ปี ค.ศ. · เรียกตอนบันทึกรับเข้าเท่านั้น |
| `ENG-NOTIFY` | `NTF_BRIEF_F-WH-GRN.md` | 7 เหตุการณ์ธุรกิจ · **ไม่มี `doa_*`** |
| `ENG-CSQ` | `CSQ_BRIEF_F-WH-GRN.md` | 3 เหตุการณ์ → ผลกระทบด้านบัญชี/ต้นทุน |

## §3.3 API ↔ Logic Trace Table (R8)

| API | Functions | Engines |
|---|---|---|
| `API-01 GET /grn` | FN-01, FN-08, FN-14 | — |
| `API-02 GET /grn/{id}` | FN-08, FN-09, FN-14 | — |
| `API-03 GET /grn/selectable-pos` | FN-02 | — |
| **`API-04 POST /grn`** | FN-03 | — |
| **`API-05 PUT /grn/{id}`** | FN-04, FN-05, FN-08, FN-10 | ENG-GRN-01, ENG-GRN-02 |
| **`API-06 POST .../refresh-from-po`** | FN-06, FN-05 | ENG-GRN-02 |
| **`API-07 POST .../post`** ★ | FN-11, FN-05, FN-08, FN-09, FN-10 | ENG-DOC-NUM, ENG-GRN-01, ENG-GRN-02, ENG-GRN-03, ENG-GRN-04, ENG-NOTIFY, ENG-CSQ |
| **`API-08 POST .../reverse`** ★ | FN-13 | ENG-GRN-03, ENG-GRN-04, ENG-NOTIFY, ENG-CSQ |
| **`API-09 POST .../discard`** | FN-12 | — |
| **`API-10 attachments`** | — (ผ่านศูนย์เอกสารกลาง) | — |
| `API-11 GET .../print` | FN-15, FN-08 | — |
| `API-12 GET /grn/check-dn` | FN-07 | — |

**R8 check:** mutation API ทั้ง 7 ตัว (04·05·06·07·08·09·10) มี Function/Engine ครบทุกตัว ✅ · ไม่มี orphan Function/Engine ✅
