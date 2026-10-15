# 03_LOGIC — F-PUR-PO · ใบสั่งซื้อ

> **Audience:** BE dev (business logic layer)
> **Scope:** ตรรกะที่ไม่ใช่ HTTP — pure function · state transition · การคำนวณ · validation · integration
> **⚠️ รหัส `FN-xx` ในไฟล์นี้เป็นฟังก์ชัน*ชั้นโค้ด* — คนละชุดกับ `FN-01..FN-95` ใน `FUNCTION_CHECKLIST` (ฟังก์ชัน*เชิงธุรกิจ*)** ดู `00_OVERVIEW §0.12.4`

---

## §3.1 Functions (Scope-Local)

### F-PUR-PO-FN-01 · `createPurchaseOrder`
- **Purpose:** สร้างใบสั่งซื้อใหม่สถานะร่าง
- **Input:** `{ source_type, refs, header_fields, lines[] }`
- **Output:** `PoHeader | ValidationError[]`
- **Invoked by:** API-02
- **Calls:** FN-05, FN-20
- **Side effects:** INSERT `t_po_header` + `t_po_line` · `pushAudit('สร้างใบ')`
- **หมายเหตุ:** **ไม่ออกเลขเอกสาร** — ร่างยังไม่มี `po_no` (R11 · LOCK-03)

### F-PUR-PO-FN-02 · `hydrateFromPurchaseRequest`
- **Purpose:** ดึงหัวและรายการจากใบขอซื้อมาตั้งต้น
- **Input:** `{ pr_ref }` · **Output:** `{ header_defaults, lines[], pr_remaining }`
- **Invoked by:** API-02 (เมื่อ `source_type = from_pr`)
- **หมายเหตุ:** `[ASSUMED contract]` — สัญญาข้อมูลกับ F072 ยังไม่ยืนยัน (`00_OVERVIEW §0.4`)

### F-PUR-PO-FN-03 · `hydrateFromCompareResult`
- **Purpose:** ตั้งต้นผู้ขายผู้ชนะ + ราคาที่ชนะรายรายการ
- **Input:** `{ compare_ref }` · **Output:** `{ vendor_ref, line_prices[] }`
- **Invoked by:** API-02 (`source_type = from_compare`) · **soft-ref** — ไม่มีก็กรอกเองได้

### F-PUR-PO-FN-04 · `checkSourceDocumentStatus`
- **Purpose:** ตรวจว่าเอกสารต้นทางยังใช้ได้ → **เตือน ไม่บล็อก**
- **Output:** `Warning[]` (`pr_cancelled` · `compare_superseded`)
- **Invoked by:** API-02 · API-04 · API-05
- **Trace:** E01 · VR15 · R04 — **ห้ามเปลี่ยนเป็น block** (Q6 ยังไม่เคาะ)

### F-PUR-PO-FN-05 · `validatePoDraft`
- **Purpose:** ตรวจช่องบังคับและความถูกต้องของบรรทัดก่อนบันทึก/ส่ง
- **Output:** `ValidationError[]` (VR01–VR11)
- **Invoked by:** API-02 · API-04 · API-05

### F-PUR-PO-FN-06 · `checkPrRemaining`
- **Purpose:** เทียบยอดสุทธิกับยอดคงเหลือของใบขอซื้อ
- **Output:** `{ exceeded: boolean, remaining, delta }`
- **Invoked by:** API-05
- **★ hard control (L-09 · E02 · VR12):** `exceeded = true` → **บล็อกการส่งอนุมัติ** (`EXCEEDS_PR_REMAINING`) แต่ **บันทึกร่างได้**

### F-PUR-PO-FN-07 · `checkBudgetAvailability`
- **Purpose:** ตรวจวงเงินงบคงเหลือ — **แสดงผลอย่างเดียว**
- **Output:** `{ over_budget: boolean, limit, used, remaining }`
- **Invoked by:** API-05 · API-15
- **★ soft (L-09 · R17 · E03 · Q2 เคาะแล้ว):** **ห้ามใช้ผลลัพธ์นี้บล็อกอะไรทั้งสิ้น**
- **สถานะ:** ข้อมูลจำลอง — ตัวจริงมาจาก F117 (W7) ดู `02_API §2.7.2`

### F-PUR-PO-FN-08 · `checkVendorStatus`
- **Purpose:** เตือนเมื่อผู้ขายถูกระงับ — **เลือกได้อยู่** (soft-ref · LOCK-01 · VR14 · E04)

### F-PUR-PO-FN-09 · `findSimilarPurchaseOrders`
- **Purpose:** หาใบที่ผู้ขาย + รายการ + ช่วงเวลาใกล้เคียง → **เตือนอย่างเดียว**
- **Invoked by:** API-14 · API-05
- **Trace:** R20 · VR16 · E09 · S-14 — **เกณฑ์อยู่ในกฎกลาง ห้าม hardcode ใน feature** (LOCK-05 · Q4 รอเคาะ)

### F-PUR-PO-FN-10 · `resolveDoaChain`
- **Purpose:** ถามทะเบียน DOA ว่ายอดนี้ต้องผ่านกี่ขั้น ตำแหน่งอะไรบ้าง
- **Input:** `{ payable_total, cost_center_ref }` · **Output:** `{ doa_entry_ref, steps: [{step_no, position_ref}] }`
- **Invoked by:** API-05 · API-15
- **★ ห้าม hardcode สายอนุมัติหรือจุดตัดวงเงินใน feature** (LOCK-02 · R07) — ค่าอยู่ที่ทะเบียน DOA กลาง
- **Trace:** `DOA_BRIEF §3`

### F-PUR-PO-FN-11 · `snapshotApprovalChain`
- **Purpose:** บันทึกสายอนุมัติ + **คนจริงที่ถูกเลือก** เป็นภาพนิ่ง ณ เวลาส่ง
- **Side effects:** INSERT `t_po_approval`
- **★ `[AI-DEFAULT]` PR-9:** แก้ทะเบียน DOA ทีหลัง **ไม่กระทบ** ใบที่ส่งไปแล้ว
- **Trace:** LOCK-02 · R08 · S-04

### F-PUR-PO-FN-12 · `approveStep`
- **Purpose:** บันทึกการอนุมัติ 1 ขั้น แล้วเลื่อนไปขั้นถัดไป
- **Guard:** ผู้กดต้องเป็น `person_ref` ของขั้นปัจจุบัน และไม่ใช่ `submitted_by` (R09)

### F-PUR-PO-FN-13 · `rejectApproval`
- **Purpose:** ไม่อนุมัติ/ส่งกลับแก้ — **บังคับเหตุผล** → ใบกลับเป็นร่าง
- **Side effects:** เก็บสายอนุมัติรอบเดิมเข้าประวัติ · `pushAudit` · แจ้งเตือนผู้ส่ง
- **Trace:** S-06 · VR10

### F-PUR-PO-FN-14 · `issueDocumentNumber`
- **Purpose:** ขอเลขเอกสารจากทะเบียนกลาง **ตอนอนุมัติครบสายเท่านั้น**
- **Calls:** `ENG-DOC-NUM.next('PO')` → `PO-YYYY-NNNN` (ค.ศ.)
- **★ ห้ามสร้างเลขเอง ห้ามเปลี่ยนเลขหลังออกแล้ว** (LOCK-03 · R22)

### F-PUR-PO-FN-15 · `sendToVendor`
- **Purpose:** บันทึกการส่งเอกสารให้ผู้ขาย (ช่องทาง · เวลา · ผู้ส่ง) → สถานะ `sent`
- **Side effects:** เก็บสำเนาเอกสารที่ส่งออก · แจ้งเตือน · `pushAudit` — **Trace:** S-07

### F-PUR-PO-FN-16 · `applyTransitionGuard`
- **Purpose:** ดักการแก้ใบที่ `approved`/`sent` — บังคับยืนยัน + เหตุผล
- **Trace:** BR-10 · R12 · S-11 · E06

### F-PUR-PO-FN-17 · `revertToDraft`
- **Purpose:** ล้างผลอนุมัติ เก็บเข้าประวัติ แล้วตั้งสถานะกลับเป็นร่าง
- **หมายเหตุ:** **`po_no` ที่ออกแล้วคงอยู่เสมอ** ไม่ถูกล้าง (LOCK-03)

### F-PUR-PO-FN-18 · `cancelPurchaseOrder`
- **Purpose:** ยกเลิกใบ — **บังคับเหตุผล**
- **Guard:** ทำได้เฉพาะ `draft` · `approved` · `sent` และ **ต้องยังไม่มีการรับของ** (R13 · E08 · VR17)
- **Side effects:** ปลดภาระผูกพัน → event ไประบบควบคุมงบ + 7C

### F-PUR-PO-FN-19 · `shortClosePurchaseOrder`
- **Purpose:** ปิดใบก่อนรับครบ — **บังคับเหตุผล** · ยกเลิกยอดค้างรับ
- **Guard:** เฉพาะสถานะ `partially_received` (R14 · BR-12)
- **Side effects:** `line_status → short_closed` · สถานะใบ → `closed` · ปลดภาระผูกพันส่วนที่เหลือ
- **★ หลังปิดแล้วเปิดรับของต่อไม่ได้** — สถานะ `closed` เข้าเงื่อนไข read-only

### F-PUR-PO-FN-20 · `calcPoTotals`
- **Purpose:** คำนวณยอดทั้งใบ — **เรียก ENG-PO-CALC**
- **Invoked by:** API-02 · API-04 · API-05

### F-PUR-PO-FN-21 · `computeLineReceiptStatus`
- **Purpose:** คำนวณ `qty_open` และ `line_status` จากยอดรับสะสม
- **★ อ่านอย่างเดียวสำหรับ feature นี้** — `qty_received` เขียนโดยใบรับของเท่านั้น (R15 · BR-13)
- **Trace:** S-09

### F-PUR-PO-FN-22 · `syncHeaderStatusFromLines`
- **Purpose:** เลื่อนสถานะใบตามยอดรับรวม — รับบางส่วน / รับครบ → ปิดแล้ว
- **Invoked by:** callback จากใบรับของ (F079)

### F-PUR-PO-FN-23 · `buildReceiptContract`
- **Purpose:** ประกอบชุดข้อมูลให้ใบรับของ (รวม `over_receipt_tolerance_pct`)
- **Invoked by:** `GET /purchase-orders/receivable` (§2.7.1)
- **★ ส่งค่าเพดานให้ ไม่บังคับเอง** (BR-08 · R10 · HANDOFF §7)

### F-PUR-PO-FN-24 · `pushAudit`
- **Purpose:** ต่อท้ายประวัติ 1 รายการ (พร้อมค่าก่อน/หลัง)
- **★ APPEND-ONLY — ไม่มีฟังก์ชันลบหรือแก้ประวัติในระบบ** (LOCK-04 · R18 · L-06)
- **Trace:** S-13

### F-PUR-PO-FN-25 · `calcOpenCommitment`
- **Purpose:** รวมมูลค่าภาระผูกพันคงค้าง = Σ(`qty_open` × ราคาสุทธิต่อหน่วย) ของใบที่อนุมัติแล้วและยังไม่ปิด
- **Invoked by:** API-01 (แถบสรุป) — **Trace:** S-12

### F-PUR-PO-FN-26 · `emitPoEvents`
- **Purpose:** ยิงเหตุการณ์ไป 7C · ศูนย์แจ้งเตือน · ระบบควบคุมงบ
- **★ feature ประกาศ event เท่านั้น ห้าม hardcode ช่องทาง/ผู้รับ/เงื่อนไข** (LOCK-05)
- **★ ห้ามประกาศ `doa_pending`/`doa_result` ซ้ำ** — DOA engine ยิงเอง (`NTF_BRIEF`)

---

## §3.2 Engines (Reusable / CUBIC-Registered)

### ENG-PO-CALC · `purchase-order-calculation-engine`

| | |
|---|---|
| **code** | `purchase-order-calculation-engine` |
| **category** | financial-calculation |
| **input** | `{ lines: [{qty, unit_price, discount_mode, discount_value, vat_mode, vat_pct}], header_discount, wht }` |
| **output** | `{ amount_before_vat, vat_amount, grand_total, wht_amount, payable_total, lines: [{line_amount, vat_base, line_vat}] }` |

**ลำดับการคำนวณ (ล็อก · L-02 · R23):**
1. ยอดบรรทัด = `จำนวน × ราคา − ส่วนลดบรรทัด`
2. ภาษีต่อบรรทัด 3 โหมด — `ไม่คิด` / `บวกเพิ่ม` / `รวมแล้ว (NET)` (โหมด `included` ถอด VAT ออกจากยอด)
3. รวมยอดก่อนภาษี → รวม VAT → ยอดหลังภาษี
4. หัก ณ ที่จ่าย (ถ้าเปิด) — **ฐาน = ยอดก่อนภาษี**
5. ส่วนลดท้ายบิล
6. **ยอดสุทธิ**

> **ต้องตรงกับ `calcLineVat` / `migrateLine` / `totals` / `renderLineSummary` ในต้นแบบทุกตัวอักษร** — เป็นสูตรกลางของทุกเอกสารธุรกรรม (Iron Rule #99) **ห้ามเขียนเวอร์ชันของ PO เอง**

**Used by:** F-PUR-PO · (คาดว่า) F079 GRN · F095 AP Invoice · เอกสารธุรกรรมอื่นในตระกูล B2
**Iron rule check:** ✅ pure · ไม่มี HTTP · ไม่มี I/O ตรง

### ENG-DOC-NUM · `document-number-engine` *(ของกลาง — ไม่ใช่ของ feature นี้)*
`next('PO')` → `PO-YYYY-NNNN` · อ่าน config จาก F-DOCCFG เท่านั้น (LOCK-03)

### ENG-DOC-STORE · `document-store-engine` *(ของกลาง)*
`store(doc_type, po_id, rendered)` · นโยบายเก็บสำเนาอ่านจาก F-DOCCFG

### ENG-DOA · `delegation-of-authority-engine` *(ของกลาง — F-DLG-001)*
`resolve({amount, cost_center})` → ขั้น + ตำแหน่ง · **feature เป็นผู้ถาม ไม่ใช่เจ้าของสาย** (LOCK-02)

### ENG-NOTIFY / ENG-CSQ *(ของกลาง)*
รับ event ตาม `NTF_BRIEF` / `CSQ_BRIEF`

---

## §3.3 API ↔ Logic Trace Table (R8 Anchor)

| API | Functions | Engines |
|---|---|---|
| API-01 `GET /purchase-orders` | FN-25 | — |
| API-02 `POST /purchase-orders` | FN-01, FN-02, FN-03, FN-04, FN-05, FN-08, FN-20, FN-24 | ENG-PO-CALC |
| API-03 `GET /:id` | FN-21 | — |
| API-04 `PUT /:id` | FN-05, FN-16, FN-17, FN-20, FN-24, FN-26 | ENG-PO-CALC |
| API-05 `POST /:id/submit` | FN-04, FN-05, FN-06, FN-07, FN-08, FN-09, FN-10, FN-11, FN-24, FN-26 | ENG-DOA |
| API-06 `POST /:id/approve` | FN-12, FN-14, FN-24, FN-26 | ENG-DOC-NUM, ENG-DOC-STORE, ENG-CSQ, ENG-NOTIFY |
| API-07 `POST /:id/reject` | FN-13, FN-24, FN-26 | ENG-NOTIFY |
| API-08 `POST /:id/send` | FN-15, FN-24, FN-26 | ENG-DOC-STORE, ENG-NOTIFY |
| API-09 `POST /:id/cancel` | FN-18, FN-24, FN-26 | ENG-CSQ, ENG-NOTIFY |
| API-10 `POST /:id/short-close` | FN-19, FN-21, FN-24, FN-26 | ENG-CSQ, ENG-NOTIFY |
| API-11 `GET /:id/document` | — | ENG-DOC-STORE |
| API-12 `GET /:id/audit` | — | — |
| API-13 `POST /:id/attachments` | FN-24 | — |
| API-14 `GET /duplicate-check` | FN-09 | — |
| API-15 `GET /:id/doa-preview` | FN-07, FN-10 | ENG-DOA |
| *(callback จากใบรับของ)* | FN-21, FN-22, FN-24, FN-26 | ENG-CSQ |
| *(contract ให้ใบรับของ)* | FN-23 | — |

### R8 verification
- ✅ ทุก mutation API (02·04·05·06·07·08·09·10·13) มี Function ≥ 1
- ✅ ทุก Function ใน §3.1 (FN-01..FN-26) ถูก trace อย่างน้อย 1 จุด — **ไม่มี orphan**
- ✅ ทุก Engine ถูกเรียกผ่าน Function หรือ API โดยตรง
