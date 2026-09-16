# 03_LOGIC — F082 F-WH-STKADJ ใบปรับยอดสต๊อก (Stock Adjustment)

> **Audience:** BE dev (business logic layer)
> **Scope:** All non-HTTP business logic — functions, calculations, validations, state transitions, integrations
> **CUBIC:** §3.1 Functions = scope-local · §3.2 Engines = candidate CUBIC Registry
> **Iron Rule R8:** ทุก mutation API trace ไป ≥1 Function/Engine ใน §3.3
> **Naming:** Function = camelCase · Engine = kebab-case

---

## §3.1 Functions (Scope-Local)

### F082-FN-01: `buildAdjustmentListQuery`
- **Purpose:** ประกอบ query list + filter + KPI aggregate (รออนุมัติ/เกินอายุ NC/มูลค่าสะสมเดือน/กลับรายการ)
- **Input:** `{ tenant_id, user_scope, filters:{ status, warehouse_ref, adjustment_type, date_from, date_to, created_by, reason_code, q, kpi }, paging }`
- **Output:** `{ rows[], kpi, total }`
- **Invoked by:** F082-API-01 · **Calls:** — · **Side effects:** — (read)
- **Iron rule check:** ✅ no HTTP terms · FN: FN-26, FN-90

### F082-FN-02: `createDraftAdjustment`
- **Purpose:** สร้างใบร่างใหม่ + บันทึกร่าง (status=draft, **ยังไม่ออกเลขที่** BR-21)
- **Input:** `{ header, lines? }`
- **Output:** `StockAdjustment(draft) | ValidationError[]`
- **Invoked by:** F082-API-03 · **Calls:** F082-FN-04 · **Side effects:** INSERT T_stock_adjustment(+lines), T_audit_log
- **Error cases:** ERR_WAREHOUSE_REQUIRED, ERR_INVALID_ADJ_TYPE · **Iron rule check:** ✅ · FN: FN-19

### F082-FN-03: `updateAdjustmentLines`
- **Purpose:** แก้ line editor (B2 v2) — เพิ่ม/ลบ/แก้บรรทัด, สลับ input_mode (correct↔delta, migrateLine), dup check, กรอง reason ตามทิศ, เปลี่ยนคลัง=ล้างบรรทัด (BR-04)
- **Input:** `{ adjustment_id, header, lines[] }`
- **Output:** `StockAdjustment | ValidationError[]`
- **Invoked by:** F082-API-04 · **Calls:** F082-FN-04 (re-snapshot), F082-FN-07, F082-ENG-01 (recompute)
- **Side effects:** UPDATE T_stock_adjustment_line, T_audit_log
- **Error cases:** ERR_DUPLICATE_BIN_ITEM(BR-01), ERR_ZERO_DELTA(BR-02), ERR_NEGATIVE_STOCK(BR-03), ERR_REASON_DIRECTION_MISMATCH(BR-07)
- **Iron rule check:** ✅ · FN: FN-04..09, FN-11, FN-12, FN-37

### F082-FN-04: `snapshotSystemQty`
- **Purpose:** ดึงยอดคงเหลือราย bin (Σ movement in−out ต่อ (bin,item)) + เก็บ snap_at + ต้นทุนอ้างอิง mock
- **Input:** `{ bin_ref, item_ref }`
- **Output:** `{ system_qty, snap_at, uom, unit_cost_ref }`
- **Invoked by:** F082-API-15, F082-FN-02, F082-FN-03 · **Calls:** — · **Side effects:** — (read ledger)
- **Iron rule check:** ✅ · FN: FN-04 · gap G-01 (cost mock)

### F082-FN-05: `filterBinPicker`
- **Purpose:** กรอง bin ให้ picker — ตาม adjustment_type→allowed location_types (BR-12), **exclude in-transit เสมอ** (BR-13), mark ล็อก/โซนปิด disabled+reason (BR-14)
- **Input:** `{ warehouse_ref, adjustment_type, q }`
- **Output:** `Bin[] (with disabled, locked_reason)`
- **Invoked by:** F082-API-13 · **Calls:** — · **Side effects:** —
- **Iron rule check:** ✅ · FN: FN-01, FN-02, FN-03, FN-32(neg), FN-46

### F082-FN-06: `validateAdjustmentDocument`
- **Purpose:** ตรวจ pre-submit ครบทุก BR — ผลต่าง≠0, non-negative, เหตุผลครบ+ตรงทิศ+note, ทุก slot คนจริง, หลักฐานครบ (damage), ref_count_doc ครบ (source=count), SoD
- **Input:** `{ adjustment_id }` (โหลด header+lines+approval+attachments)
- **Output:** `{ ok:true } | ValidationError[]`
- **Invoked by:** F082-API-05 (submit), บางส่วนใน F082-API-04 · **Calls:** — · **Side effects:** —
- **Error cases:** ERR_ZERO_DELTA, ERR_NEGATIVE_STOCK, ERR_REASON_REQUIRED, ERR_REASON_DIRECTION_MISMATCH, ERR_REASON_NOTE_REQUIRED, ERR_APPROVER_SLOT_EMPTY, ERR_EVIDENCE_REQUIRED, **ERR_COUNT_DOC_REQUIRED (BR-26)**, ERR_SOD_SELF_APPROVAL, ERR_DUPLICATE_BIN_ITEM
- **Iron rule check:** ✅ · FN: FN-10, FN-11, FN-12, FN-17, FN-18, FN-40, FN-42, FN-51, FN-52

### F082-FN-07: `fillLineReasonsFromHeader`
- **Purpose:** เติมเหตุผลรวมของใบให้ทุกบรรทัดที่ยังว่าง (แก้รายบรรทัดต่อได้)
- **Input:** `{ adjustment_id, header_reason_code }` · **Output:** `Line[]`
- **Invoked by:** F082-API-04 · **Side effects:** UPDATE lines · **Iron rule check:** ✅ · FN: FN-41

### F082-FN-08: `submitForApproval` (orchestrate)
- **Purpose:** ส่งอนุมัติ — validate (FN-06) → คำนวณ abs base (ENG-01) → resolve สาย DOA → snapshot approval slots → **ออกเลขที่ (ENG-DOC-NUM)** → transition draft→pending → emit doa_pending + NTF slot1
- **Input:** `{ adjustment_id, approval_slots[] }`
- **Output:** `{ adj_no, status:"pending", approval[] }`
- **Invoked by:** F082-API-05 · **Calls:** F082-FN-06, F082-ENG-01, ENG-DOC-NUM(F-DOCCFG), DOA resolve(F-DLG-001)
- **Side effects:** UPDATE status+adj_no, INSERT approval, emit events, T_audit_log
- **Iron rule check:** ✅ · FN: FN-20 · BR-21

### F082-FN-09: `approveSlot`
- **Purpose:** อนุมัติ slot ปัจจุบัน — SoD check (ไม่ใช่ผู้จัดทำ), บันทึกผล+เวลา, ไป slot ถัดไป/ครบ→approved
- **Input:** `{ adjustment_id, actor, note? }` · **Output:** `{ status, current_step, sign_progress }`
- **Invoked by:** F082-API-06 · **Calls:** — · **Side effects:** UPDATE approval row, emit doa_result+NTF
- **Error cases:** ERR_SOD_SELF_APPROVAL, ERR_INVALID_STATE_TRANSITION, ERR_STALE_DATA
- **Iron rule check:** ✅ · FN: FN-21

### F082-FN-10: `rejectDocument`
- **Purpose:** ตีกลับ — เหตุผลบังคับ → กลับ draft, เก็บ approval_history (returned:true)
- **Input:** `{ adjustment_id, actor, reason }` · **Output:** `{ status:"draft", returned:true }`
- **Invoked by:** F082-API-07 · **Side effects:** UPDATE status+approval, T_audit_log
- **Error cases:** ERR_REJECT_REASON_REQUIRED · **Iron rule check:** ✅ · FN: FN-22 · BR-11

### F082-FN-11: `cancelDocument`
- **Purpose:** ยกเลิก — **guard status ∈ {draft,pending}** (BR-27/FIX-02), เหตุผลบังคับ, ไม่มี movement, ใบยังอยู่
- **Input:** `{ adjustment_id, actor, reason }` · **Output:** `{ status:"cancelled" }`
- **Invoked by:** F082-API-08 · **Side effects:** UPDATE status, emit adj_cancelled(NTF)+CSQ no-effect, T_audit_log
- **Error cases:** ERR_CANCEL_NOT_ALLOWED (status=approved/posted), ERR_ACTION_REASON_REQUIRED
- **Iron rule check:** ✅ · FN: FN-24 · **BR-27**

### F082-FN-12: `recheckQtyBeforePost`
- **Purpose:** BR-15 — เทียบ system_qty_snapshot vs ยอดล่าสุด ต่อบรรทัด · ต่าง → คืน drift[] (บังคับผู้ใช้เลือก latest/return)
- **Input:** `{ adjustment_id }` · **Output:** `{ drift:[{ bin, item, old, latest, new_delta }] | [] }`
- **Invoked by:** F082-API-09 (precondition ของ FN-13) · **Calls:** F082-FN-04 · **Side effects:** — (read)
- **Iron rule check:** ✅ · FN: FN-27 · BR-15

### F082-FN-13: `postDocument` (orchestrate)
- **Purpose:** ผ่านรายการ — guard status=approved (BR-08), หลัง recheck → generate movements (ENG-02) + je_status=รอลงบัญชี + store PDF (approved_final) + emit adj_posted/writeoff/drift(NTF) + CSQ EC · ถ้า posted doc = reversal → set ต้นฉบับ=reversed (BR-17.1)
- **Input:** `{ adjustment_id, actor, recheck_choice }` · **Output:** `{ status:"posted", movements[], je_status }`
- **Invoked by:** F082-API-09 · **Calls:** F082-FN-12, F082-ENG-02, ENG-DOC-STORE, ENG-CSQ
- **Side effects:** INSERT T_inventory_movement (append-only), UPDATE status, emit events, T_audit_log
- **Error cases:** ERR_INVALID_STATE_TRANSITION, ERR_STALE_DATA · **Iron rule check:** ✅ · FN: FN-23, FN-29, FN-30

### F082-FN-14: `reverseDocument`
- **Purpose:** กลับรายการ (FIX-03) — guard status=posted & ยังไม่กลับ (BR-18), เหตุผลบังคับ → **สร้างใบกลับรายการใหม่** (is_reversal_doc, delta ตรงข้าม) → resolve DOA ตาม abs ของใบนั้น → status pending (ไม่ auto-post) → ผูก 2 ทาง
- **Input:** `{ adjustment_id, actor, reason }` · **Output:** `{ reversal_doc:{ id, adj_no, status:"pending" } }`
- **Invoked by:** F082-API-10 · **Calls:** F082-ENG-01, ENG-DOC-NUM, DOA resolve
- **Side effects:** INSERT ใบกลับรายการ(+approval), UPDATE links, T_audit_log
- **Error cases:** ERR_ALREADY_REVERSED, ERR_ACTION_REASON_REQUIRED · **Iron rule check:** ✅ · FN: FN-25, FN-44 · **BR-17/18**

### F082-FN-15: `attachEvidence`
- **Purpose:** แนบไฟล์หลักฐาน → Document Center + ผูกใบ (โผล่ landing)
- **Input:** `{ adjustment_id, file }` · **Output:** `Attachment`
- **Invoked by:** F082-API-12 · **Side effects:** INSERT T_stock_adjustment_attachment · **Iron rule check:** ✅ · FN: FN-33, FN-51

### F082-FN-16: `getMovementHistory`
- **Purpose:** ดึง movement ของใบ + คู่ reversal ผูก 2 ทาง (append-only, ไม่มีปุ่มลบ)
- **Input:** `{ adjustment_id }` · **Output:** `Movement[]`
- **Invoked by:** F082-API-11 · **Side effects:** — · **Iron rule check:** ✅ · FN: FN-29, FN-45(neg)

### F082-FN-17: `buildAdjustmentPdfModel`
- **Purpose:** ประกอบ data PDF A4 — header meta + 10-col line table + totals (headline Σ|มูลค่า|) + 3 signature slots ตามสาย DOA + watermark ตามสถานะ · ปี ค.ศ.
- **Input:** `{ adjustment_id }` · **Output:** `PdfModel`
- **Invoked by:** F082-API-19 · **Calls:** F082-ENG-01 (totals) · **Side effects:** — · **Iron rule check:** ✅ · FN: FN-28, FN-34, FN-38

### F082-FN-18: `buildAttachmentLandingQuery`
- **Purpose:** รวมไฟล์แนบล่าสุดทุกใบ + กรองตามใบ (Document Center section ที่ landing)
- **Input:** `{ tenant_id, user_scope, filter }` · **Output:** `Attachment[]`
- **Invoked by:** F082-API-20 · **Side effects:** — · **Iron rule check:** ✅ · FN: FN-33

> **หมายเหตุ negative FN** (FN-35 no cycle-count, FN-36 no location move, FN-47/48 no config screen, FN-49 no VAT column) = พิสูจน์ว่า "ไม่มี" — ไม่มี function/endpoint รองรับ (ดู 06_TESTS §6.7 negatives · 00 §0.12)

---

## §3.2 Engines (Reusable / CUBIC-Registered)

### F082-ENG-01: `adjustment-valuation-engine` [NEW]

| Field | Value |
|---|---|
| **id** | (assigned at CUBIC registration) |
| **code** | `adjustment-valuation-engine` |
| **name** | Adjustment Valuation Engine |
| **category** | financial-calculation |
| **status** | DRAFT (this FRD) |
| **owner** | F082 (shared → Stock Transfer F083 · OB-16) |

**Input Schema:** `{ lines:[{ delta_qty, unit_cost_ref }] }`
**Output Schema:** `{ per_line:[{ line_amount }], abs_total, net_total, plus_count, minus_count }`
**Logic Outline:**
1. per line `line_amount = delta_qty × unit_cost_ref` (มีเครื่องหมาย)
2. `abs_total = Σ |line_amount|` ← **ฐาน DOA (BR-09) — ค่าสัมบูรณ์ ไม่ใช่ net**
3. `net_total = Σ line_amount` (แสดงอย่างเดียว)
4. นับ plus/minus lines

**Used by features:** F082 (this) · F083 Stock Transfer (planned · reuse ค่าสัมบูรณ์)
**Iron rule check:** ✅ Pure (no I/O direct) · ✅ Reusable (2+) · ✅ Substantial (financial base ที่ทั้ง DOA/JE/PDF ใช้)
**CUBIC Registration:** DRAFT → register ตอน dev hand-off (ดู 07 §7.1 LD-02)
**Note:** `unit_cost_ref` = mock (Item Master) รอบนี้ · `FWD-WIRE: valuation engine (W5)` — engine รับ input ต้นทุน ไม่ได้ตัดสินต้นทุนเอง (gap G-01)

### F082-ENG-02: `inventory-movement-engine` [NEW]

| Field | Value |
|---|---|
| **code** | `inventory-movement-engine` |
| **name** | Inventory Movement Engine (append-only) |
| **category** | generation |
| **status** | DRAFT (this FRD) |
| **owner** | Warehouse lane (shared — F082 + F083 Stock Transfer · OB-16) |

**Input Schema:** `{ ref_doc, lines:[{ bin_ref, item_ref, delta_qty, uom, unit_cost, reason_code, reason_note }], mode:"post"|"reverse", origin_movement_ids? }`
**Output Schema:** `{ movements:[{ movement_no, movement_type, qty(+), bin_ref, amount, je_status:"รอลงบัญชี", reversed_movement_id?, reversal_movement_id? }] }`
**Logic Outline:**
1. mode=post → movement_type = ปรับเพิ่ม (delta>0) / ปรับลด (delta<0) · qty = |delta|
2. mode=reverse → movement_type = กลับรายการปรับเพิ่ม/ปรับลด (ทิศตรงข้ามของต้นฉบับ) · ผูก `reversed_movement_id`↔`reversal_movement_id` 2 ทาง (BR-18)
3. **append-only** — INSERT เท่านั้น, ไม่ UPDATE/DELETE (BR-16)
4. single bin — ไม่มี from→to (LOCK-03)
5. set je_status=`รอลงบัญชี` (mock BR-19) — **ไม่ post JE จริง**

**Used by features:** F082 (this) · F083 Stock Transfer (planned)
**Iron rule check:** ✅ Reusable (2+) · ✅ Substantial (ledger + reversal linking algorithm) · Pure? มี DB write (insert-only) — ผ่านเกณฑ์ ≥2/3 (Reusable+Substantial)
**CUBIC Registration:** DRAFT → register ตอน dev hand-off (LD-03)

> **External Engines referenced (ไม่ owned ที่นี่):** `ENG-DOC-NUM` / `ENG-DOC-STORE` (F-DOCCFG) · DOA chain resolver (F-DLG-001) · `ENG-NOTIFY` (F-NOTIFY) · `ENG-CSQ` (F-CSQ-01). Feature **ประกาศ** ผ่าน declaration briefs — ไม่ implement engine เอง.

---

## §3.3 API ↔ Logic Trace Table (R8 Anchor)

| API ID | Method | Path | Calls Functions | Calls Engines |
|---|---|---|---|---|
| F082-API-01 | GET | /stock-adjustments | F082-FN-01 | — |
| F082-API-02 | GET | /:id | — (assemble) | — |
| F082-API-03 | POST | /stock-adjustments | F082-FN-02, F082-FN-04 | — |
| F082-API-04 | PUT | /:id | F082-FN-03, F082-FN-07, F082-FN-04 | F082-ENG-01 |
| F082-API-05 | POST | /:id/submit | F082-FN-06, F082-FN-08 | F082-ENG-01, ENG-DOC-NUM*, DOA* |
| F082-API-06 | POST | /:id/approve | F082-FN-09 | — |
| F082-API-07 | POST | /:id/reject | F082-FN-10 | — |
| F082-API-08 | POST | /:id/cancel | F082-FN-11 | — |
| F082-API-09 | POST | /:id/post | F082-FN-12, F082-FN-13 | F082-ENG-02, ENG-DOC-STORE*, ENG-CSQ* |
| F082-API-10 | POST | /:id/reverse | F082-FN-14 | F082-ENG-01, ENG-DOC-NUM*, DOA* |
| F082-API-11 | GET | /:id/movements | F082-FN-16 | — |
| F082-API-12 | POST | /:id/attachments | F082-FN-15 | — |
| F082-API-13 | GET | /bins | F082-FN-05 | — |
| F082-API-15 | GET | /bins/:id/stock-balance | F082-FN-04 | — |
| F082-API-19 | GET | /:id/pdf | F082-FN-17 | F082-ENG-01 |
| F082-API-20 | GET | /stock-adjustment-attachments | F082-FN-18 | — |

`*` external engine (F-DOCCFG / F-DLG-001 / F-CSQ-01)

### Trace Verification (Self-Check)
- [x] **ทุก mutation API** (03,04,05,06,07,08,09,10,12) มี ≥1 Function/Engine
- [x] **No orphan Function** — FN-01..18 ปรากฏใน trace (FN-05,FN-06 fold บาง read/mutation; FN-04 ใน API-03/04/15; FN-16/17/18 ใน read APIs)
- [x] **No orphan Engine** — ENG-01 (API-04/05/10/19), ENG-02 (API-09) trace ครบ
- [x] **No hidden logic ใน 02_API** — business logic ทั้งหมด trace ที่นี่

---

## §3.4 Dependencies

### External Function/Engine called
- `ENG-DOC-NUM.next('ADJ', ctx)` / `ENG-DOC-STORE.store(...)` — F-DOCCFG (existing)
- DOA `resolve(abs_value)` → steps[] — F-DLG-001 (existing, wire pending)
- `ENG-NOTIFY.emit(event)` — F-NOTIFY · `ENG-CSQ.emit(event)` — F-CSQ-01
- ยอดคงเหลือราย bin (Σ movement) — Putaway §3.4 ledger (shared T_inventory_movement)

### External that calls into this feature
- F083 Stock Transfer — reuse F082-ENG-01, F082-ENG-02 (ถ้า register)

---

## §3.5 Locked Decisions Referenced (ดู 07_LOCKED)
- LD-02: F082-ENG-01 register CUBIC ตอน dev hand-off (scope-local ก่อน)
- LD-03: F082-ENG-02 shared กับ Stock Transfer — register ตอน F083 ยืนยัน reuse
- LD-05 (FIX-03): reversal = ใบใหม่ผ่าน DOA ตาม abs ของตัวเอง — ไม่ auto-post
- LD-06 (FIX-04): ref_count_doc = soft-ref display-only (F084/F086) — ไม่เปิดหน้าใบนับ

---

## Audience Cheat-Sheet
| Reader | Read |
|---|---|
| BE dev | §3.1 + §3.2 + §3.3 |
| QA | §3.3 + §3.1 Side effects + §3.2 I/O |
| Architect / CUBIC owner | §3.2 (ENG-01/02 candidates) + §3.4 |
| PM | §3.3 (coverage view) |
