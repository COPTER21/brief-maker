# 03_LOGIC — F-PUR-RTV · RTV คืนผู้ขาย

> Audience: BE dev (business logic layer) · **ไม่มีศัพท์ HTTP ในส่วน Engine**
> ★ `F-PUR-RTV-FN-xx` ในไฟล์นี้ = **ฟังก์ชันชั้นโค้ด** — คนละชุดกับ `FN-01..FN-94` ของ `FUNCTION_CHECKLIST` (ฟังก์ชันเชิงธุรกิจ) · ดู `00_OVERVIEW §0.12.1`
> ทุกหัวข้ออ้าง **ชื่อฟังก์ชันจริงในต้นแบบ** ที่บรรทัดนั้นสกัดมา — dev ใช้เป็นจุดเทียบได้ตรง ๆ

## §3.1 Functions (scope-local)

### `F-PUR-RTV-FN-01` · `listRtv`
- **Purpose:** ประกอบผลหน้ารายการ + ตัวชี้วัด 5 ตัว ตามตัวกรองและขอบเขตสิทธิ์ของผู้ใช้
- **Input:** `{ filters: { q, status, main_reason, vendor_ref, include_archived }, sort, page, userScope }` · **Output:** `{ rows[], kpi: { month_count, returned_value, pending_count, quarantine_qty, wait_credit_value }, total }`
- **Logic:** ซ่อน `cancelled`/`reversed` เว้นแต่ `include_archived = true` (**กลไก soft archive** · BR-22) · `q` ค้นใน `rtv_no · grn_ref · po_ref · ชื่อผู้ขาย · rma_no · note` · `quarantine_qty` เรียก `ENG-RTV-01` ไล่ทุกใบรับของที่บันทึกรับเข้าแล้ว
- **Invoked by:** `API-01` · **Calls:** `ENG-RTV-01` · `ENG-RTV-02` · **Side effects:** —
- **สกัดจาก:** `rtvFiltered()` · `kpis()` · `sortBy()` · `setFilter()`
- **Implements:** `FN-90(chk)` · `IS-11`

### `F-PUR-RTV-FN-02` · `getSelectableGrns`
- **Purpose:** คัดใบรับของที่คืนได้ **พร้อมส่งเหตุผลรายใบของใบที่เลือกไม่ได้กลับไปด้วย**
- **Input:** `{ q?, userScope }` · **Output:** `[{ grn_ref, grn_date, vendor_ref, po_ref, returnable_qty, selectable, block_reason }]`
- **Logic:** เลือกได้เมื่อ `สถานะใบรับของ = บันทึกรับเข้าแล้ว` **และ** `Σ ยอดคืนได้ทุกบรรทัด > 0` · มิฉะนั้นคืน `block_reason` 1 ใน 3 ข้อความ (ร่าง / ถูกกลับรายการ / คืนครบแล้ว) — **ห้ามกรองทิ้ง** (BR-01 · `EC-03`)
- **Invoked by:** `API-03` · **Calls:** `ENG-RTV-01`
- **สกัดจาก:** `grnRowsList()` · `grnBlockReason()` · `grnReturnable()`
- **Implements:** `BR-01` · `FN-01(chk)` · `FN-04(chk)` · `IS-01`

### `F-PUR-RTV-FN-03` · `buildDraftFromGrn`
- **Purpose:** สร้างร่างจากใบรับของ — ดึงทุกบรรทัดพร้อมยอดคืนได้ · ราคา/ส่วนลด/ภาษี · เหตุผลและที่อยู่ต้นทางที่เดามาให้
- **Input:** `{ grn_ref, main_reason?, doc_date?, actor }` · **Output:** `RtvDraft`
- **Logic:**
  1. ปฏิเสธถ้า `FN-02` บอกว่าเลือกไม่ได้
  2. คัดลอกหัวเอกสารจากใบรับของ: ผู้ขาย · ใบสั่งซื้อ · คลัง · ที่อยู่ส่งคืนจากทะเบียนผู้ขาย
  3. เดาเหตุผลคืนหลัก: มีบรรทัดที่ QC ไม่ผ่าน → `qc` มิฉะนั้น → `over`
  4. ต่อบรรทัด: เหตุผลตั้งต้น = `over` ถ้ามีจำนวนรับเกิน · มิฉะนั้นเหตุผล QC เดิมจากใบรับของ (ไม่มี → `damaged`) · มิฉะนั้น `offspec`
  5. `source_location_ref` ตั้งต้น = **พื้นที่กักกัน** เมื่อเหตุผลไม่ใช่ `over` · **ตำแหน่งจัดเก็บปกติ** เมื่อเป็น `over` (BR-07)
  6. `qty_return` ตั้งต้น = ยอดคืนได้ของบรรทัดนั้น (**0 ถ้าของถูกใช้ต่อแล้ว**)
  7. ราคา · ส่วนลด · โหมดภาษี · หน่วย · ชื่อสินค้า = **อ่านอย่างเดียว คัดลอกมาเป็น snapshot** (BR-02)
- **Invoked by:** `API-04` · **Calls:** `ENG-RTV-01` · `ENG-RTV-02` · **Side effects:** INSERT header + lines · audit `สร้างร่าง`
- **สกัดจาก:** `pickGrn()` · `commitWizard('draft')` · `blankData()`
- **Implements:** `BR-01` · `BR-02` · `BR-07` · `FN-02(chk)` · `FN-03(chk)` · `FN-13(chk)` · `IS-01`

### `F-PUR-RTV-FN-04` · `updateDraft`
- **Purpose:** บันทึกการแก้ร่าง (หัวเอกสาร + จำนวนคืน + เหตุผล + ที่อยู่ต้นทาง + หมายเหตุ + โหมดภาษี)
- **Input:** `{ rtv_id, row_version, header, lines[], actor }` · **Output:** `{ draft, blockers[] } | ValidationError[]`
- **Logic:** ปฏิเสธถ้า `สถานะ ≠ ร่าง` (BR-15) · ตรวจ `row_version` (`BR-28`) · ถ้า `main_reason` เปลี่ยน → เรียก `FN-07` ก่อน · แล้วเรียก `FN-05` · เขียน audit ค่าก่อน-หลัง
- **Invoked by:** `API-05` · **Calls:** `FN-05` · `FN-07` · `ENG-RTV-01` · `ENG-RTV-02`
- **สกัดจาก:** `updateLine()` · `commitWizard()` · `saveDraft()`
- **Implements:** `BR-02`..`BR-08` · `BR-15` · `FN-20(chk)` · `FN-21(chk)`

### `F-PUR-RTV-FN-05` · `validateRtv`
- **Purpose:** ตรวจทั้งใบตาม `VR01`–`VR21` ก่อนบันทึกร่าง / ส่งอนุมัติ / บันทึกส่งคืน — **คืนรายการปัญหาทั้งหมดในครั้งเดียว ไม่หยุดที่ข้อแรก**
- **Input:** `RtvDraft` · **Output:** `{ blockers: [{ scope:'header'|'line', line_no?, code, message }] }`
- **Logic (ลำดับเดียวกับที่จอแสดง):**
  1. หัวเอกสาร: ยังไม่เลือกใบรับของ / ยังไม่เลือกเหตุผลคืนหลัก / ยังไม่ระบุวันที่เอกสาร / **ยังไม่ระบุผู้ขอคืน (ต้องเป็นคนจริง)** / ยังไม่ระบุคลังที่ของออก
  2. ทั้งใบ: ต้องมีอย่างน้อย 1 บรรทัดที่จำนวนคืน > 0 (BR-03)
  3. ต่อบรรทัด เรียก `ENG-RTV-01.lineBlockReason()` — ของถูกใช้ต่อแล้ว / เกินยอดคืนได้ (พร้อมบอกเพดาน) / ติดลบ / ไม่มีเหตุผลคืน / เหตุผล "อื่น ๆ" ไม่มีคำอธิบาย / ไม่มีที่อยู่ต้นทาง
- **Invoked by:** `FN-04` · `FN-10` · `FN-12` · **Calls:** `ENG-RTV-01`
- **สกัดจาก:** `wizardBlockers()` · `lineBlocked()`
- **Implements:** `VR01`..`VR12` · `FN-11(chk)` · `FN-92(chk)`

### `F-PUR-RTV-FN-06` · `refreshFromGrn`
- **Purpose:** ดึงข้อมูลจากใบรับของใหม่ เมื่อยอดคืนได้ขยับเพราะใบคืนใบอื่นตัดไปก่อน หรือใบรับของถูกแก้
- **Input:** `{ rtv_id, actor }` · **Output:** `RtvDraft`
- **Logic:** อัปเดต `qty_received · qty_qc_failed · qty_over · unit_price · discount_pct · vat_mode` และยอดคืนได้ใหม่ · **clamp `qty_return` ลงมาไม่ให้เกินยอดคืนได้ใหม่** · แล้ว re-validate
- **Invoked by:** `API-06` · **Calls:** `ENG-RTV-01` · `FN-05`
- **สกัดจาก:** `reloadFromGrn()` — ต้นแบบดึงใหม่ทั้งชุด (`lines = []` แล้ว `pickGrn()`) · **ของจริงต้องรักษาค่าที่ผู้ใช้กรอกไว้เท่าที่ยังใช้ได้**
- **Implements:** `EC-13` · `EC-21` · `FN-09(chk)`

### `F-PUR-RTV-FN-07` · `applyMainReason`
- **Purpose:** เปลี่ยนเหตุผลคืนหลักแล้วเขียนค่าตั้งต้นลงทุกบรรทัด — **เพราะเหตุผลเปลี่ยนแล้วฐานคืนได้และที่อยู่ต้นทางเปลี่ยนตาม**
- **Input:** `{ draft, main_reason }` · **Output:** `RtvDraft`
- **Logic:** ต่อบรรทัด — `over` → เหตุผล `over` + ที่อยู่ปกติ · `qc` → เหตุผล QC เดิมจากใบรับของ (ไม่มี → `damaged`) + **พื้นที่กักกัน** · `offspec` → เหตุผล `offspec` + พื้นที่กักกันถ้าใบรับของมีของไม่ผ่าน มิฉะนั้นที่อยู่ปกติ · `other` → เหตุผล `other` (ที่อยู่คงเดิม) · **ปิดท้ายด้วยการ clamp จำนวนคืนลงมาไม่ให้เกินยอดคืนได้ใหม่**
- **Invoked by:** `FN-04` · **Calls:** `ENG-RTV-01`
- **สกัดจาก:** `applyMainReason()` · `updateLine(id,'reason',…)`
- **Implements:** `BR-07` · `FN-12(chk)` · `FN-13(chk)` · `FN-34(chk)` · `IS-04`

### `F-PUR-RTV-FN-08` · `fillAllReturnable`
- **Purpose:** ปุ่มลัด "คืนทั้งหมดที่คืนได้" — ตั้ง `qty_return = ยอดคืนได้` ทุกบรรทัดในคลิกเดียว
- **Input:** `RtvDraft` · **Output:** `RtvDraft`
- **Logic:** ต่อบรรทัด `qty_return = ENG-RTV-01.returnableQty(line)` · บรรทัดที่ของถูกใช้ต่อแล้วได้ 0 โดยอัตโนมัติ (ฐานคืนได้เป็น 0)
- **Invoked by:** `FN-04` (ผ่าน `API-05`) · **สกัดจาก:** `fillAllReturnable()`
- **Implements:** `FN-05(chk)` · `AC-01`

### `F-PUR-RTV-FN-09` · `computeDocumentTotals`
- **Purpose:** ผูกยอดรายบรรทัดและยอดทั้งใบเข้าด้วยกันสำหรับทุกหน้าจอ/เอกสาร/ฐานวงเงิน
- **Input:** `RtvDoc` · **Output:** `{ lines: [{ line_net_amount, line_vat_amount, line_total }], totals: { before, vat, after, grand } }`
- **Logic:** ห่อ `ENG-RTV-02` — **เป็นทางเดียวที่ชั้นบนได้ตัวเลขยอด** (B2 v2 lock: ห้ามคำนวณยอดที่อื่น)
- **Invoked by:** `FN-01` · `FN-04` · `FN-10` · `FN-12` · `FN-16` · `FN-18` · `API-02`
- **สกัดจาก:** `totals()` · `calcLineVat()` · `linesTableView()` tfoot
- **Implements:** `BR-02` · `IS-02`

### `F-PUR-RTV-FN-10` · `submitForApproval` ★
- **Purpose:** ส่งอนุมัติ — ออกเลขเอกสาร · resolve สายใหม่ตามมูลค่าปัจจุบัน · freeze ภาพนิ่งสายพร้อมคนจริง
- **Input:** `{ rtv_id, approvers: [{ slot_no, person_id }], idempotency_key, actor }`
- **Output:** `{ rtv_no, doa_entry_ref, approval_base_amount, chain[] }`
- **Logic (ลำดับบังคับ · transaction เดียว):**
  1. ตรวจ `สถานะ = ร่าง` (`BR-DOA-01`)
  2. `FN-05 validateRtv` — ผิดข้อใดข้อหนึ่ง = หยุด **ไม่เขียนอะไรเลย ไม่ออกเลข**
  3. `FN-09` → `total_grand` → เรียก **ทะเบียน DOA `resolve()`** (`FW-03` · **ห้าม hardcode สายในฟีเจอร์** · LOCK-03)
  4. เทียบ `approvers` ที่ส่งมากับสายที่เพิ่ง resolve — ไม่ครบ → `APPROVER_INCOMPLETE` (BR-10) · จำนวนขั้น/ตำแหน่งไม่ตรง → `APPROVER_CHAIN_MISMATCH` (**เกิดได้จริงเมื่อมูลค่าข้ามจุดตัดระหว่างที่หน้าต่างเปิดค้าง** · BR-11)
  5. ตรวจ `ผู้ขอคืน ∉ รายชื่อผู้อนุมัติ` → มิฉะนั้น `SELF_APPROVAL_FORBIDDEN` (`BR-26` · `C-02`)
  6. **ถ้ายังไม่มีเลขเอกสาร** → `ENG-DOC-NUM.next('RTV')` (`FW-04`) · **ถ้ามีแล้ว (เคยถูกส่งกลับแก้) ใช้เลขเดิม** (`DR-08` · BR-21)
  7. freeze `approval_base_amount = total_grand` · เขียน `T_rtv_approval` **round ใหม่** (สายเดิมยังอยู่ · `BR-DOA-05`)
  8. `สถานะ = รออนุมัติ` · audit `ส่งอนุมัติ` พร้อมเลขที่ · มูลค่า · จำนวนขั้น
  9. `doa_pending` ยิงโดย **ทะเบียน DOA เอง** — **ฟีเจอร์ห้ามยิงซ้ำ** (`NTF_BRIEF §2`)
- **Side effects:** UPDATE header · INSERT approval · INSERT audit
- **สกัดจาก:** `openSubmitModal()` · `doSubmit()` · `commitWizard('pending', doa)` · `resolveDoa()` · `nextDocNo()`
- **Implements:** `BR-09`·`BR-10`·`BR-11`·`BR-21` · `BR-DOA-01/02/04/05` · `FN-14(chk)`·`FN-15(chk)`·`FN-16(chk)`·`FN-22(chk)`·`FN-23(chk)` · `IS-05`

### `F-PUR-RTV-FN-11` · `decideApproval`
- **Purpose:** บันทึกการตัดสินใจของขั้นปัจจุบัน (อนุมัติ / ส่งกลับแก้ / ไม่อนุมัติ)
- **Input:** `{ rtv_id, action: 'approve'|'sendback'|'reject', reason?, comment?, idempotency_key, actor }`
- **Output:** `{ status, current_slot, chain[] }`
- **Logic:**
  1. ตรวจ `สถานะ = รออนุมัติ`
  2. หาขั้นปัจจุบัน = ขั้นแรกที่ยังไม่ `อนุมัติแล้ว` (`currentSlot()`)
  3. **ตรวจว่า `actor` คือคนที่ถูกเลือกไว้ในขั้นนั้นจริง** → มิฉะนั้น `NOT_CURRENT_APPROVER` (`BR-26` — **จุดที่ต้นแบบยังไม่ทำ** ดู `07_LOCKED LD-13`)
  4. `approve` → ตั้งผลขั้นเป็น `อนุมัติแล้ว` + เวลา + ความเห็น · **ถ้าไม่มีขั้นที่ยังค้างเหลือ → `สถานะ = อนุมัติแล้ว`** + audit `อนุมัติครบสาย` · **สต๊อกยังไม่ขยับ** (BR-13)
  5. `sendback` → **บังคับเหตุผล** (BR-12) · ตั้งผลขั้นเป็น `ส่งกลับแก้` · `สถานะ = ร่าง` · **เลขเอกสารคงเดิม**
  6. `reject` → **บังคับเหตุผล** · ตั้งผลขั้นเป็น `ไม่อนุมัติ` · `สถานะ = ยกเลิก` · `cancel_reason = reason` · **สต๊อกไม่ขยับ**
  7. audit ทุกกรณี · `doa_result` ยิงโดยทะเบียน DOA เอง (**ไม่ประกาศซ้ำ**)
- **สกัดจาก:** `doApprove()` · `doSendback()` · `doReject()` · `currentSlot()`
- **Implements:** `BR-09`·`BR-12`·`BR-26` · `BR-DOA-03` · `FN-17(chk)`·`FN-18(chk)`·`FN-19(chk)` · `AC-08`·`AC-09`

### `F-PUR-RTV-FN-12` · `shipReturn` ★ — จุดเดียวที่สต๊อกขยับ
- **Purpose:** บันทึกส่งคืน — ของออกจากคลังจริง
- **Input:** `{ rtv_id, return_date, shipper, vehicle_no?, vendor_receiver?, idempotency_key, actor }`
- **Output:** `{ movements[], grn_sync }`
- **Logic (ลำดับบังคับ · transaction เดียว · `DR-03`):**
  1. ตรวจ `สถานะ = อนุมัติแล้ว` — **ไม่มีทางลัด** (BR-09 · `C-05`)
  2. บังคับ `return_date` (ไม่เป็นอนาคต · ≥ วันที่รับของในใบรับของ) และ `shipper` (`VR17`/`VR18`)
  3. **lock บรรทัดใบรับของ** แล้ว `FN-05 validateRtv` ซ้ำอีกครั้งด้วยยอดคืนได้ ณ วินาทีนี้ — ใบอื่นอาจตัดไปก่อน → `QTY_OVER_RETURNABLE` (`EC-21`)
  4. `ENG-RTV-03` (mode `out`) — สร้างความเคลื่อนไหวออกจาก `source_location_ref` ของแต่ละบรรทัดที่ `qty_return > 0` · bucket = พื้นที่กักกัน/ปกติ ตามชนิดของตำแหน่ง (BR-14)
  5. `ENG-RTV-04` (mode `apply`) — บวกยอดคืนสะสมกลับใบรับของรายบรรทัด **+ ตั้งล็อกกลับรายการที่ใบรับของ** (BR-20 · `DR-05` · `IS-12`)
  6. `สถานะ = ส่งคืนแล้ว` · เก็บข้อมูลขนส่ง · audit `บันทึกส่งคืน` พร้อมรายการความเคลื่อนไหวที่เกิด
  7. **นอก transaction:** `ENG-NOTIFY.emit('rtv_returned')` + `ENG-CSQ.emit('rtv_returned')` และ `ENG-CSQ.emit('rtv_credit_expected')` (`FW-05` · `FW-06`)
  8. **ห้ามลงบัญชีใด ๆ** — ป้าย "รอเครดิตจากผู้ขาย" เป็นผลของสถานะ ไม่ใช่รายการบัญชี (`FW-01` · `OS-01`)
- **Side effects:** UPDATE header · INSERT movement · **เขียนกลับใบรับของ** · INSERT audit
- **สกัดจาก:** `doShip()` · `shipDraft`
- **Implements:** `BR-08`·`BR-09`·`BR-13`·`BR-14`·`BR-20` · `FN-24(chk)`·`FN-25(chk)`·`FN-32(chk)`·`FN-37(chk)` · `IS-06`·`IS-12` · `AC-11`

### `F-PUR-RTV-FN-13` · `recordCredit`
- **Purpose:** บันทึกเอกสารเครดิตจากผู้ขายแล้วปิดใบ
- **Input:** `{ rtv_id, credit_doc_no, credit_date?, credit_amount_actual?, idempotency_key, actor }`
- **Logic:** ตรวจ `สถานะ = ส่งคืนแล้ว` · **บังคับ `credit_doc_no`** (BR-18 · `VR19`) · `credit_amount_actual` ว่าง → ใช้มูลค่าที่คืนรวม · `สถานะ = ปิดใบ` · audit
  5. **ไม่ post รายการบัญชีใด ๆ** — `FW-01` (W5) · ส่วนต่างระหว่างเครดิตที่ได้จริงกับมูลค่าที่คืนบันทึกเป็นหมายเหตุในรอบนี้ (`OQ-RTV-06` · `EC-16`)
  6. **นอก transaction:** `ENG-NOTIFY.emit('rtv_credited')` + `ENG-CSQ.emit('rtv_credited')`
- **สกัดจาก:** `doCredit()` · `creditDraft` · `creditPill()`
- **Implements:** `BR-18` · `FN-30(chk)`·`FN-31(chk)`·`FN-38(chk)` · `IS-08` · `AC-13`

### `F-PUR-RTV-FN-14` · `reverseRtv` ★
- **Purpose:** กลับรายการทั้งใบหลังของออกไปแล้ว
- **Input:** `{ rtv_id, reason, reverse_location_ref, idempotency_key, actor }`
- **Logic:**
  1. ตรวจ `สถานะ = ส่งคืนแล้ว` · ผู้เรียกเป็นหัวหน้าคลัง (`OQ-RTV-05`)
  2. **บังคับเหตุผล + ตำแหน่งที่รับของกลับ** (BR-12 · `VR20`)
  3. `ENG-RTV-03` (mode `reverse`) — สร้างความเคลื่อนไหวทิศตรงข้ามทุกแถว ชี้ `reversal_of` · **ห้ามลบแถวเดิม** (LOCK-02 · `DR-04`)
  4. `ENG-RTV-04` (mode `revert`) — **หักยอดคืนสะสมคืนที่ใบรับของ** → ของกลับไปนับเป็น "คืนได้" ตามเดิม
  5. `สถานะ = กลับรายการ` (**สถานะปลายทาง อ่านอย่างเดียว**) · audit พร้อมตำแหน่งที่รับของกลับ
  6. **การปลดล็อกกลับรายการของใบรับของยังไม่เปิดในรอบนี้** (`OQ-RTV-07` · `EC-18`)
  7. **นอก transaction:** `ENG-NOTIFY.emit('rtv_reversed')` (**ปิดไม่ได้**) + `ENG-CSQ.emit('rtv_reversed')` แบบ `avoided`
- **สกัดจาก:** `doReverse()` · `reverseDraft`
- **Implements:** `BR-12`·`BR-15`·`BR-16` · `FN-26(chk)`·`FN-27(chk)` · `IS-09` · `AC-12`

### `F-PUR-RTV-FN-15` · `cancelRtv`
- **Purpose:** ยกเลิกก่อนของออก (ครอบเส้นทาง "ทิ้งร่าง" ด้วย)
- **Input:** `{ rtv_id, reason, idempotency_key, actor }`
- **Logic:** ตรวจ `สถานะ ∈ {ร่าง, รออนุมัติ, อนุมัติแล้ว}` (BR-17) · **บังคับเหตุผล** (`VR16`) · `สถานะ = ยกเลิก` · **ไม่แตะสต๊อก ไม่แตะใบรับของ** · **ไม่มีการลบถาวร** — ใบยังค้นเจอผ่านสวิตช์ `รวมที่ยกเลิก/กลับรายการ` (BR-22) · ของกลับไปนับเป็นคืนได้อัตโนมัติเพราะยอดคืนสะสมนับเฉพาะใบที่ของออกจริงแล้ว (`DR-02`) · audit
- **สกัดจาก:** `doCancel()` · `openModal('cancel')`
- **Implements:** `BR-12`·`BR-17`·`BR-22` · `FN-28(chk)`·`FN-33(chk)`·`FN-91(chk)` · `EC-07`

### `F-PUR-RTV-FN-16` · `buildPrintModel`
- **Purpose:** ประกอบข้อมูลเอกสารพิมพ์ A4 ตาม `print-spec-rtv.md`
- **Input:** `{ rtv_id }` · **Output:** `{ header, parties, lines[], totals, signatures[], watermark }`
- **Logic:** **ปี ค.ศ. ทุกจุด รวมในไฟล์ที่ส่งออก** (BR-23 · `DR-08`) · ตารางรายการ **ต้องมีคอลัมน์เหตุผลคืน** และบอกตำแหน่งต้นทางใน `sub` เพื่อให้ผู้ขายเห็นว่าเป็นของที่ QC ไม่ผ่าน · ช่องลงชื่อ 3 ฝ่าย (`ผู้จัดทำ / ผู้ขอคืน` · `ผู้อนุมัติ` = คนที่อนุมัติล่าสุด · `ผู้รับฝั่งผู้ขาย`) · `watermark = 'draft'` เมื่อยังไม่ถึง `อนุมัติแล้ว` (BR-25)
- **สกัดจาก:** `renderPdfTab()` · `pdfSign()`
- **Implements:** `BR-23`·`BR-25` · `FN-40(chk)`·`FN-42(chk)`·`FN-43(chk)`·`FN-94(chk)` · `IS-07` · `AC-15`

### `F-PUR-RTV-FN-17` · `appendAudit`
- **Purpose:** เขียนประวัติแบบต่อท้ายอย่างเดียวจากทุกเส้นทางที่เปลี่ยนสถานะหรือข้อมูล
- **Input:** `{ rtv_id, act, actor, note?, before?, after? }` · **Output:** `AuditRow`
- **Logic:** **INSERT อย่างเดียว — ไม่มีเส้นทาง update/delete** · ปรับ `updated_by/at` ของหัวเอกสารไปพร้อมกัน · `act` ต้องใช้ชุดคำที่ `04_DB §T_rtv_audit` ระบุไว้ (เพื่อให้ไทม์ไลน์ย้อมสีถูก)
- **Invoked by:** `FN-03`..`FN-15` ทุกตัวที่เขียนข้อมูล · **สกัดจาก:** `pushAudit()`
- **Implements:** `BR-22` · `FN-93(chk)` · `C-07`·`C-12`·`C-13` · `AC-16`

### `F-PUR-RTV-FN-18` · `exportRtvCsv`
- **Purpose:** ส่งออกรายการตามตัวกรองปัจจุบันเป็น CSV
- **Input:** `{ filters, userScope }` · **Output:** ไฟล์ CSV (UTF-8 พร้อม BOM)
- **Logic:** คอลัมน์ `เลขที่ · วันที่เอกสาร · ผู้ขาย · อ้าง GRN · PO · สถานะ · มูลค่าที่คืน` · **วันที่เป็นปี ค.ศ. ในไฟล์ด้วย ไม่ใช่แค่บนจอ** (`DR-08`) · ฟิลด์ Confidential ถูกตัดตามสิทธิ์ผู้เรียก (`05_RULES §5.7`)
- **สกัดจาก:** `exportCsv()` · **Implements:** `IS-11` · `FN-90(chk)`

## §3.2 Engines (reusable / CUBIC-registered)

### `ENG-RTV-01` · `rtv-returnable-engine` ★ หัวใจของฟีเจอร์
- **code:** `rtv-returnable-engine` · **category:** `validation-calculation`
- **input:** `{ grn_line: { qty_received, qty_qc_failed, qty_over, consumed, consumed_ref }, return_reason, returned_before, qty_return }`
- **output:** `{ base_qty, qty_returnable, qty_remaining_after, line_state, block_reason }`
- **logic outline:**
  1. **ของถูกใช้ต่อแล้ว (`consumed`) → `base_qty = 0` · `line_state = 'ของถูกใช้ต่อแล้ว'` · `block_reason = "ของถูกใช้ต่อแล้ว — {consumed_ref}"`** (ปัจจุบันมาจาก flag ของใบรับของ · **hook จริงคือ `FW-02` ฝั่ง W3Q**)
  2. `return_reason = 'over'` (รับเกิน) → `base_qty = qty_over`
  3. `return_reason = 'qc'` (QC ไม่ผ่าน) → `base_qty = qty_qc_failed`
  4. `return_reason ∈ {'offspec', 'other'}` (ผิดสเปค / อื่น ๆ) → `base_qty = max(0, qty_received − qty_qc_failed)`
     — ของที่**ผ่าน QC เข้าคลังปกติ**แล้วพบภายหลังว่าไม่ตรงสเปค (S-20) · **ไม่ใช่** `qty_qc_failed`
  5. `qty_returnable = max(0, base_qty − returned_before)` · `qty_remaining_after = max(0, qty_returnable − qty_return)`
  6. `qty_return > qty_returnable` → `block_reason = "เกินยอดคืนได้ (สูงสุด {qty_returnable} {หน่วย})"` — **ไม่มี tolerance คืนเกินเด็ดขาด** (BR-04)
  7. `qty_return < 0` → `block_reason = "จำนวนคืนติดลบไม่ได้"`
  8. `qty_returnable = 0` → `line_state = 'คืนครบแล้ว'` เลือกคืนไม่ได้ (BR-05)
  9. `line_state` หลังส่งคืน: `qty_remaining_after = 0` → `คืนครบแล้ว` · `> 0` → `คืนบางส่วนแล้ว`
- **`returned_before` คำนวณจาก:** `Σ qty_return` ของบรรทัดใบรับของเดียวกันจากใบคืน **ที่ `สถานะ ∈ {ส่งคืนแล้ว, ปิดใบ}` เท่านั้น** (ไม่นับ ร่าง/รออนุมัติ/อนุมัติแล้ว/ยกเลิก/กลับรายการ) — `DR-02`
- **Used by:** F-PUR-RTV (ใช้ซ้ำได้กับการตรวจยอดคืนของฝั่ง GRN และการจับคู่สามทางของ AP)
- **สกัดจาก:** `baseQty()` · `returnedQty()` · `returnableQty()` · `lineAvail()` · `lineBlocked()` · `grnReturnable()`
- **Implements:** `BR-03`·`BR-04`·`BR-05`·`BR-07` · `EC-01`·`EC-02`·`EC-04`·`EC-05`·`EC-13` · `DR-01`·`DR-02` · `IS-02`
- **Iron rule:** ✅ pure · ไม่มีศัพท์ HTTP · ไม่มี I/O ตรง (ผู้เรียกเป็นคนดึงยอดคืนสะสมมาให้)
- > ⚠️ **ข้อ 2–4 ข้างบนคือสูตรที่ต้อง implement (ตาม PREBRIEF §3.3) — ต้นแบบ HTML ยัง _ไม่_ ทำตามนี้**
  > `baseQty()` (บรรทัด 1007–1014) รับ `reasonCode` มาแต่ใช้จริงเฉพาะค่า `'over'` · ลำดับ `if` ทำให้เมื่อ `qty_qc_failed > 0` จะคืน `qty_qc_failed` **ทุกเหตุผล** และไปไม่ถึงสาขา `qty_received − qty_qc_failed` เลย
  > วัดจริงในชุด mock: **5 จาก 7 บรรทัดให้ค่าต่างจาก §3.3** (เช่น `GRN-2026-0007` ln1 รับ 100 · ไม่ผ่าน QC 12 → ต้นแบบให้เพดาน **12** ที่ควรเป็น **88**)
  > ผลคือ **S-20 เดินไม่ถึง** — ซึ่งเป็นสถานการณ์ที่ *รองรับ* ตาม PREBRIEF
  > **เหตุผลที่ยึด §3.3 ไม่ใช่ต้นแบบ:** HTML-first ใช้กับ *pattern ของหน้าจอ* ไม่ใช่ *เลขคณิตเชิงธุรกิจ* · PREBRIEF ประกาศตัวเองเป็น source of truth เชิง business · และคอมเมนต์เหนือ `baseQty()` เองก็เขียนว่าตั้งใจทำตาม §3.3 → เป็นความพลาดของลำดับ `if` ไม่ใช่มติที่ตั้งใจ
  > **ข้อควรระวังตอน implement:** การเปิดให้คืนของที่ผ่าน QC แล้วต้องมี **การตรวจว่าของยังอยู่จริง** (`FW-02` · W3Q) เป็นตัวคุม ไม่งั้นจะคืนของที่ถูกเบิก/ย้ายไปแล้ว — จุดนี้คือแก่นของ **`OQ-RTV-04`** ที่ต้องเคาะ**ก่อน P1**
  > ดู `07_LOCKED LD-14` · `06_TESTS` มีเคส regression กำกับข้อนี้

### `ENG-RTV-02` · `rtv-line-amount-engine` (B2 v2 · LOCKED)
- **code:** `rtv-line-amount-engine` · **category:** `financial-calculation`
- **input:** `{ lines: [{ qty_return, unit_price, discount_mode, discount_pct, discount_amt, vat_mode, vat_pct }], endbill? }`
- **output:** `{ per_line: [{ net_amount, vat_amount, line_total }], totals: { before, vat, after, eb_amount, grand } }`
- **logic outline:**
  1. `subtotal = qty_return × unit_price`
  2. `discount = discount_mode === 'amount' ? min(subtotal, discount_amt) : subtotal × discount_pct/100`
  3. `net_amount = subtotal − discount`
  4. `vat_mode = 'add'` → `vat_amount = net_amount × vat_pct/100` · `line_total = net_amount + vat_amount`
  5. `vat_mode = 'included'` → `vat_amount = net_amount × vat_pct / (100 + vat_pct)` · `line_total = net_amount` (**คำนวณย้อน**)
  6. `vat_mode = 'none'` → `vat_amount = 0` · `line_total = net_amount`
  7. ยอดทั้งใบ: `before = Σ (vat_mode === 'included' ? net − vat : net)` · `vat = Σ vat_amount` · `after = before + vat` · `grand = max(0, after − eb_amount)`
- **★ เป็นแหล่งคำนวณเดียวของทั้งฟีเจอร์** — หน้าจอ · ใบพิมพ์ · **ฐานวงเงินที่ใช้ resolve สาย DOA** · payload ของ `ENG-CSQ` ต้องใช้ผลจาก engine นี้เท่านั้น (HANDOFF §3 L2)
- **`endbill` (ปรับลดท้ายใบ) ยังอยู่ในโครงข้อมูลแต่ไม่มีหน้าจอ** — เผื่อ `OQ-RTV-06` เคาะให้บันทึกส่วนต่างเครดิต · เปิดกลับมาได้โดยไม่ต้องแก้ engine
- **Used by:** F-PUR-RTV (โครงเดียวกับ B2 v2 ของ PO/GRN/QT/SO/INV)
- **สกัดจาก:** `calcLineVat()` · `migrateLine()` · `totals()` · `taxBadgeV()`
- **Implements:** `BR-02` · `IS-02` · `FN-07(chk)`
- **Iron rule:** ✅ pure

### `ENG-RTV-03` · `rtv-movement-engine`
- **code:** `rtv-movement-engine` · **category:** `inventory`
- **input:** `{ rtv_ref, lines: [{ line_ref, item_ref, qty_return, source_location_ref }], mode: 'out' | 'reverse', reverse_location_ref?, origin_movements? }`
- **output:** `{ movements: [{ line_ref, item_ref, location_ref, qty, direction, bucket, reversal_of? }] }`
- **logic outline:**
  1. `mode = 'out'` → ต่อบรรทัดที่ `qty_return > 0` สร้าง **1 แถว** ทิศ `out` จาก `source_location_ref` · `bucket` = `quarantine` ถ้าตำแหน่งนั้นเป็นพื้นที่กักกัน มิฉะนั้น `stock`
  2. `mode = 'reverse'` → อ่าน `origin_movements` แล้วสร้างแถว **ทิศตรงข้าม** ทุกแถว ตั้ง `reversal_of = origin.movement_id` · ตำแหน่งปลายทาง = `reverse_location_ref` ที่ผู้ใช้ระบุ (อาจต่างจากตำแหน่งเดิม เช่นรับกลับเข้าพื้นที่กักกันแทน)
  3. บรรทัดที่ `qty_return = 0` → **ไม่สร้างแถวใด ๆ**
  4. **ต่อท้ายอย่างเดียว** — engine นี้ไม่มีเส้นทาง update/delete (LOCK-02 · BR-15 · `DR-04`)
- **Used by:** F-PUR-RTV · โครงเดียวกับ `stock-movement-engine` ของ F-WH-GRN (ควรรวมเป็น engine กลางตอนขึ้น CUBIC Registry — ดู `07_LOCKED LD-08`)
- **สกัดจาก:** `doShip()` (สร้างรายการ movement ลง audit) · `doReverse()` · `renderStockTab()`
- **Implements:** `BR-13`·`BR-14`·`BR-15`·`BR-16` · `EC-08` · `IS-06`
- **Iron rule:** ✅ pure

### `ENG-RTV-04` · `grn-return-sync-engine` ★ ทางเดียวที่เขียนกลับใบรับของ
- **code:** `grn-return-sync-engine` · **category:** `document-sync`
- **input:** `{ grn_ref, lines: [{ grn_line_no, qty_return }], mode: 'apply' | 'revert', rtv_no }`
- **output:** `{ lines: [{ grn_line_no, returned_after, returnable_after, line_badge }], reversal_locked: bool }`
- **logic outline:**
  1. `mode = 'apply'` → `returned += qty_return` ต่อบรรทัด · `line_badge` = `คืนบางส่วนแล้ว` หรือ `คืนครบแล้ว`
  2. `mode = 'revert'` → `returned −= qty_return` (ไม่ต่ำกว่า 0)
  3. **ตั้ง `reversal_locked = true` ที่ใบรับของทันทีที่มีใบคืนใบใดใบหนึ่งอยู่ในสถานะ ส่งคืนแล้ว/ปิดใบ** — ฝั่งใบรับของต้องปิดปุ่มกลับรายการพร้อมเหตุผลที่ชี้มาที่เลขใบคืน (BR-20 · LOCK-08 · `DR-05`)
  4. **การปลดล็อกเมื่อใบคืนถูกกลับรายการหมดแล้ว ยังไม่เปิดในรอบนี้** — `reversal_locked` คงเป็น `true` (`OQ-RTV-07` · `EC-18`)
  5. **★ ห้ามแตะใบสั่งซื้อทุกกรณี** — ยอดรับสะสม/ยอดค้างรับของใบสั่งซื้อไม่ใช่ขอบเขตของ engine นี้ (LOCK-05 · BR-19 · `DR-06`)
- **Used by:** F-PUR-RTV — **เป็นทางเดียวที่ยอดคืนสะสมของใบรับของถูกเขียน** ห้ามมีเส้นทางแก้ด้วยมือ
- **สกัดจาก:** `returnedQty()` (ฝั่งอ่าน) · `grnLockedByRtv()` (ฝั่งล็อก) · `renderStockTab()` section "ผลต่อเอกสารต้นทาง"
- **Implements:** `BR-19`·`BR-20` · `EC-18` · `DR-05`·`DR-06` · `IS-12` · `OS-02`
- **Iron rule:** ✅ pure (ผู้เรียกเป็นคนยิงคำสั่งเขียนไปยังฝั่งใบรับของ)

### Engine กลางที่ **เรียกใช้** (ไม่ได้เป็นเจ้าของ — ประกาศผ่านใบใน `03_FRD/`)

| Engine | ใบประกาศ | สัญญา | forward-wire |
|---|---|---|---|
| **ทะเบียน DOA (F-DLG-001)** | `DOA_BRIEF_F-PUR-RTV.md` | `resolve({feature, amount})` → สาย + ตัวเลือกคนจริงต่อขั้น · เรียกตอนกดส่งอนุมัติ **ทุกครั้ง** (BR-11) แล้ว freeze | **`FW-03`** |
| **`ENG-DOC-NUM` (F-DOCCFG)** | `DOCCFG_BRIEF_F-PUR-RTV.md` | `next('RTV', company_ctx)` → `RTV-YYYY-NNNN` ปี ค.ศ. · เรียก **ครั้งเดียวต่อใบ** ตอนส่งอนุมัติ · **ห้าม format เอง ห้าม +1 เอง** | **`FW-04`** |
| **`ENG-NOTIFY` (F-NOTIFY)** | `NTF_BRIEF_F-PUR-RTV.md` | 5 เหตุการณ์ธุรกิจ · **ไม่ประกาศซ้ำ `doa_pending`/`doa_result`/`doa_escalate`** · ห้ามเช็คช่องทาง/preference เองในฟีเจอร์ | **`FW-05`** |
| **`ENG-CSQ` (F-CSQ-01)** | `CSQ_BRIEF_F-PUR-RTV.md` | 5 เหตุการณ์ → ท่อ EC/FC · **ไม่ประกาศ OC/DC/SC/SecC/AC** · ฟีเจอร์ห้ามตีมูลค่าเอง | **`FW-06`** |
| `ENG-DOC-STORE` (F-DOCCFG) | `DOCCFG_BRIEF §3` | เก็บสำเนา PDF ตอน `approved_final` และ `sent_external` | (ผ่าน FW-04) |
| Document Center | — | เอกสารแนบ | — |

## §3.3 API ↔ Logic Trace Table (R8)

| API | Functions | Engines |
|---|---|---|
| `API-01 GET /rtv` | FN-01, FN-09 | ENG-RTV-01, ENG-RTV-02 |
| `API-02 GET /rtv/{id}` | FN-09, FN-16 | ENG-RTV-01, ENG-RTV-02 |
| `API-03 GET /rtv/selectable-grns` | FN-02 | ENG-RTV-01 |
| **`API-04 POST /rtv`** | FN-03, FN-05, FN-09, FN-17 | ENG-RTV-01, ENG-RTV-02 |
| **`API-05 PUT /rtv/{id}`** | FN-04, FN-05, FN-07, FN-08, FN-09, FN-17 | ENG-RTV-01, ENG-RTV-02 |
| **`API-06 POST .../refresh-from-grn`** | FN-06, FN-05, FN-17 | ENG-RTV-01, ENG-RTV-02 |
| **`API-07 POST .../submit`** ★ | FN-10, FN-05, FN-09, FN-17 | ENG-RTV-02, **ทะเบียน DOA**, **ENG-DOC-NUM** |
| **`API-08 POST .../approve`** | FN-11, FN-17 | — (`doa_result` ยิงโดยทะเบียน DOA) |
| **`API-09 POST .../sendback`** | FN-11, FN-17 | — |
| **`API-10 POST .../reject`** | FN-11, FN-17 | — |
| **`API-11 POST .../ship`** ★ | FN-12, FN-05, FN-09, FN-17 | ENG-RTV-01, ENG-RTV-02, **ENG-RTV-03**, **ENG-RTV-04**, ENG-NOTIFY, ENG-CSQ |
| **`API-12 POST .../credit`** | FN-13, FN-09, FN-17 | ENG-RTV-02, ENG-NOTIFY, ENG-CSQ |
| **`API-13 POST .../reverse`** ★ | FN-14, FN-17 | **ENG-RTV-03**, **ENG-RTV-04**, ENG-NOTIFY, ENG-CSQ |
| **`API-14 POST .../cancel`** | FN-15, FN-17 | ENG-NOTIFY, ENG-CSQ |
| **`API-15 attachments`** | FN-17 | — (ผ่าน Document Center) |
| `API-16 GET .../print` | FN-16, FN-09 | ENG-RTV-02, ENG-DOC-STORE |
| `API-17 GET /rtv/export` | FN-18, FN-01, FN-09 | ENG-RTV-02 |
| `API-18 GET /rtv/doa-preview` | — | **ทะเบียน DOA** |

**R8 check**
- mutation API ทั้ง **12 ตัว** (04·05·06·07·08·09·10·11·12·13·14·15) มี Function ครบทุกตัว ✅
- Function ทั้ง **18 ตัว** ถูก trace อย่างน้อย 1 API ✅ (`FN-17 appendAudit` ถูกเรียกจาก mutation ทุกตัว)
- Engine ที่เป็นเจ้าของทั้ง **4 ตัว** ถูก trace ผ่าน Function ✅ · Engine กลางทั้ง 5 ถูก trace ✅
- **ไม่มี orphan Function/Engine** ✅
- `API-18` เป็น read-only ที่เรียก engine กลางโดยตรง (ไม่มี business logic ของตัวเอง) — ยกเว้นที่ยอมรับได้ตาม Logic Placement Matrix #1

## §3.4 Logic Placement — ของที่ **ห้าม** ไปอยู่ผิดที่

| logic | ต้องอยู่ที่ | เหตุผล | ห้ามอยู่ที่ |
|---|---|---|---|
| คำนวณยอดคืนได้ / เพดานคืน | `ENG-RTV-01` | pure · ถูกเรียกจาก 6 จุด · เป็นตัวเลขที่ทั้งฟีเจอร์เชื่อ | ❌ ในชั้น HTTP · ❌ ในหน้าจอ |
| คำนวณยอดเงิน + VAT 3 โหมด | `ENG-RTV-02` | pure · B2 v2 lock "แหล่งคำนวณเดียว" | ❌ ที่ใดก็ตามนอก engine |
| สร้าง/หักยอดคืนสะสมที่ใบรับของ | `ENG-RTV-04` | ทางเดียวที่เขียนกลับต้นทาง | ❌ ในชั้น HTTP · ❌ ใน `FN-12` โดยตรง |
| จุดตัดวงเงิน / จำนวนขั้นอนุมัติ | **ทะเบียน DOA** | ข้อมูล ไม่ใช่โค้ด (LOCK-03) | ❌ ใน `05_RULES` · ❌ ใน `03_LOGIC` · ❌ ใน DB ของฟีเจอร์ |
| รูปแบบเลขเอกสาร / การ +1 | **ENG-DOC-NUM** | ข้อมูล ไม่ใช่โค้ด (LOCK-04) | ❌ ใน `FN-10` |
| ช่องทาง/เงื่อนไขแจ้งเตือน | **ENG-NOTIFY** | ตั้งที่ศูนย์แจ้งเตือน | ❌ ในฟีเจอร์ |
| การประทับผลกระทบ 7 ด้าน | **ENG-CSQ** | engine ประเมินเอง | ❌ ในฟีเจอร์ |
| เกณฑ์คืนช้า / จำนวนวันย้อนหลัง | **กติกากลาง (NC rules · CF-07)** | ค่าที่ธุรกิจปรับได้ | ❌ ค่าคงที่ในโค้ด |
| ตรวจ required / รูปแบบวันที่ / ขนาดไฟล์ | `02_API §2.3` | trivial · ไม่มี reuse | — |
| กฎสถานะ (A → B ได้เมื่อไร) | `05_RULES §5.3` (ประกาศ) + `FN-10`..`FN-15` (บังคับ) | กติกาต้องตรวจสอบได้ ทริกเกอร์เป็นขั้นตอน | — |
