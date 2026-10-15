# 03_LOGIC — F-PUR-PR · PR ใบขอซื้อ

> Audience: BE dev (business logic layer)
> Scope: logic ที่ไม่ใช่ HTTP — pure function · state transition · การคำนวณ · validation · integration
> วางตำแหน่งตาม `logic-placement-matrix.md`

## §3.1 Functions (Scope-Local)

### F-PUR-PR-FN-01 · `buildPrListQuery`
- **Purpose:** ประกอบเงื่อนไขค้นหา/กรอง/เรียง + **ขอบเขตการมองเห็นตาม role**
- **Input:** `{ q?, status?, department?, requester_id?, sort, dir, page, size, actor }`
- **Output:** `QuerySpec`
- **Invoked by:** API-01
- **Side effects:** — (อ่านอย่างเดียว)
- **หมายเหตุ:** ขอบเขตการมองเห็นมาจาก BRD §4.2 — ผู้ขอเห็นเฉพาะใบตน/หน่วยงานตน · หัวหน้าเห็นใบที่ตนอยู่ในสาย

### F-PUR-PR-FN-02 · `getPrDetail`
- **Purpose:** ประกอบเอกสารเต็มใบ + คำนวณ flag `can_*` ให้ UI
- **Input:** `{ pr_id, actor }` · **Output:** `PrDetail` · **Invoked by:** API-02 · **Calls:** FN-11
- **หมายเหตุ:** UI **ห้ามคำนวณสิทธิ์เอง** — ใช้ `can_approve/can_edit/can_recall/can_cancel` จาก function นี้

### F-PUR-PR-FN-03 · `createPrDraft`
- **Purpose:** สร้างใบร่างใหม่ · **ไม่ออกเลขที่**
- **Input:** `PrDraftInput` · **Output:** `{ pr_id }` · **Invoked by:** API-03
- **Calls:** FN-04 · FN-05 · ENG-PR-CALC
- **Side effects:** INSERT `t_pr_header` `t_pr_line` `t_pr_vendor_suggest` + `t_pr_history('create')`

### F-PUR-PR-FN-04 · `validatePrHeader`
- **Purpose:** ตรวจหัวเอกสาร (V-01 · V-02)
- **Input:** `PrHeaderInput` · **Output:** `ValidationError[]` · **Invoked by:** FN-03 · FN-06
- **กติกา:** หน่วยงาน · วันที่เอกสาร · วันที่ต้องการใช้ · ประเภท · เหตุผล = บังคับ · `required_date >= doc_date`

### F-PUR-PR-FN-05 · `validatePrLines`
- **Purpose:** ตรวจรายการ (V-03 · V-04 · V-05)
- **Input:** `PrLineInput[]` · **Output:** `ValidationError[]` · **Invoked by:** FN-03 · FN-06 · FN-08
- **กติกา 3 ด่าน:** (1) ≥1 รายการที่มีชื่อ + `qty>0` + `unit_price_est>0` (2) ไม่มีแถวว่าง (3) ไม่ซ้ำ `item + uom`
- **หมายเหตุ:** รายการ `is_free` ไม่นับเป็นรายการที่ใช้ได้และแก้/ลบไม่ได้

### F-PUR-PR-FN-06 · `updatePrDraft`
- **Purpose:** แก้ใบร่าง + optimistic lock
- **Input:** `PrDraftInput + version` · **Output:** `{ version }` · **Invoked by:** API-04
- **Calls:** FN-04 · FN-05 · ENG-PR-CALC
- **Side effects:** UPDATE + `t_pr_history('update', before, after)`
- **กติกา:** สถานะต้องเป็น `draft` เท่านั้น (BR-04) · `version` ไม่ตรง → `PR_VERSION_CONFLICT` `[AI-DEFAULT]`

### F-PUR-PR-FN-07 · `checkBudgetMock` ★ forward-wire
- **Purpose:** ตรวจงบประมาณ — **จำลองล้วนในรอบนี้**
- **Input:** `{ cost_center_id, amount }` · **Output:** `{ ok, remaining, budget_code, mock: true }`
- **Invoked by:** FN-08 · API-02 (แสดงผลซ้ำให้ผู้อนุมัติเห็น)
- **★ LOCK-FW:** ห้าม implement logic งบจริง · ผล "ไม่พอ" เป็น **คำเตือนเท่านั้น ไม่ block** (BR-07)
- **TODO:** `ENG-BUDGET.check({cost_center, amount, period})` เมื่อ F117 (W7) พร้อม — สัญญา `[ASSUMED]` A-01
- **กติกา:** ไม่ได้เลือกศูนย์ต้นทุน → คืน `{ok:true, remaining:null}` **ข้ามการตรวจ ไม่ถือเป็นข้อผิดพลาด** (EC-02 · AC-12)

### F-PUR-PR-FN-08 · `submitPr` ★ หัวใจ
- **Purpose:** ร่าง → รออนุมัติ · ออกเลขที่ · แช่แข็งสายอนุมัติ
- **Input:** `{ pr_id, slots[], actor, idempotency_key }` · **Output:** `{ pr_no, slots[] }` · **Invoked by:** API-05
- **Calls:** FN-05 · FN-07 · **ENG-PR-CALC** · **ENG-DOA-RESOLVE** · `ENG-DOC-NUM` · `ENG-NOTIFY`
- **Side effects:** UPDATE header · INSERT slot (snapshot) · `t_pr_history('submit')` · emit `pr_submitted` (+ `pr_budget_warning` ถ้างบไม่พอ)
- **ลำดับบังคับ:** ตรวจสถานะ → **คำนวณยอดใหม่ฝั่งเซิร์ฟเวอร์** → resolve ชั้น DOA จากยอดนั้น → ตรวจ slot ครบ + ไม่ใช่ตัวเอง → ขอเลขที่ → เขียน snapshot → emit
- **★ BR-02:** ชั้นอนุมัติเลือกจากยอด **ณ เวลาที่กดส่ง** แล้วแช่แข็ง — แก้ทะเบียน DOA ภายหลังไม่กระทบใบที่ส่งแล้ว
- **★ BR-03:** ผู้ขออยู่ใน `slots` → `PR_SELF_APPROVAL_FORBIDDEN`

### F-PUR-PR-FN-09 · `approvePrSlot`
- **Purpose:** บันทึกการอนุมัติของขั้นหนึ่ง · ถ้าครบทุกขั้น → `approved`
- **Input:** `{ pr_id, slot_seq, actor, note? }` · **Output:** `{ status, slots[] }` · **Invoked by:** API-06
- **Calls:** FN-11 · `ENG-NOTIFY` · `ENG-CSQ` · `ENG-DOC-STORE`
- **Side effects:** UPDATE slot · UPDATE header (ถ้าขั้นสุดท้าย) · `t_pr_history('approve')`
- **ขั้นสุดท้ายเท่านั้น:** emit `pr_approved` + `ENG-CSQ doc.approved` (EC · `estimated`) + `ENG-DOC-STORE.store(pdf,'PR',id,'approved_final')`
- **CA-01 `[AI-DEFAULT]`:** slot ถูกตัดสินไปแล้ว → `PR_SLOT_ALREADY_DECIDED` (คนแรกชนะ)

### F-PUR-PR-FN-10 · `recallPr`
- **Purpose:** รออนุมัติ → ร่าง (ผู้ขอเท่านั้น)
- **Input:** `{ pr_id, actor }` · **Output:** `{ status: 'draft' }` · **Invoked by:** API-08 · **Calls:** `ENG-NOTIFY`
- **★ EC-03:** slot ทุกขั้น → `decision='void'` **ไม่ลบแถว** — ยังเห็นในประวัติ (AC-10)
- **Side effects:** `t_pr_history('recall')` · emit `pr_recalled` ให้ผู้อนุมัติที่ค้าง
- **หมายเหตุ:** ส่งใหม่ต้องเลือกสายใหม่ตามยอดใหม่ (BR-04)

### F-PUR-PR-FN-11 · `resolveCurrentActor`
- **Purpose:** หาว่าผู้เรียกอยู่ในขั้นปัจจุบันหรือไม่
- **Input:** `{ pr, actor }` · **Output:** `slot_seq | -1`
- **Invoked by:** FN-02 · FN-09 · FN-13
- **★ SC-10 / AC-06:** คืน `-1` → **ไม่แสดงปุ่มอนุมัติ** (จอจริงใช้ `canActStep()` ที่เทียบ `ACT_AS` กับ `assignee` ของ slot ที่ `pending`)

### F-PUR-PR-FN-12 · `duplicatePr`
- **Purpose:** ทำสำเนาเป็นใบร่างใหม่
- **Input:** `{ source_pr_id, actor }` · **Output:** `{ pr_id }` · **Invoked by:** API-10
- **★ AC-13:** คัดลอกหัว + รายการ · **ไม่คัดลอก** `pr_no` · slot · history · attachment

### F-PUR-PR-FN-13 · `rejectPr`
- **Purpose:** ไม่อนุมัติ + เหตุผลบังคับ
- **Input:** `{ pr_id, slot_seq, reason, actor }` · **Invoked by:** API-07 · **Calls:** FN-11 · `ENG-NOTIFY`
- **กติกา:** `reason` ≥ 3 ตัวอักษร (V-07) · ขั้นที่เหลือ **ไม่ต้องพิจารณา** · emit `pr_rejected` (**ปิดไม่ได้**)

### F-PUR-PR-FN-14 · `cancelPr`
- **Purpose:** ยกเลิกใบ (จากร่าง หรือจากอนุมัติแล้ว)
- **Input:** `{ pr_id, reason, actor }` · **Invoked by:** API-09 · **Calls:** `ENG-NOTIFY` · `ENG-CSQ`
- **กติกา:** เหตุผลบังคับ · ต้องยังไม่มี PO อ้าง (`PR_HAS_PO_REFERENCE` — ตรวจจริงเมื่อ W3 พร้อม)
- **★ ยิง `ENG-CSQ doc.cancelled` (EC · `avoided`) เฉพาะใบที่เคยอนุมัติแล้ว** — ยกเลิกจากร่างไม่ยิง

### F-PUR-PR-FN-15 · `validateAttachment`
- **Purpose:** ตรวจชนิดและขนาดไฟล์ **ฝั่งเซิร์ฟเวอร์**
- **Input:** `{ file_name, mime_type, file_size }` · **Output:** `ValidationError[]` · **Invoked by:** API-11
- **กติกา:** PDF · JPG · PNG · XLSX · ≤ 10 MB `[ASSUMED]` A-02 · **ไฟล์เดียวไม่ผ่านต้องไม่ล้มทั้งชุด** (EC-05)

### F-PUR-PR-FN-16 · `formatPrDocNo`
- **Purpose:** แปลง `pr_no` เป็นข้อความแสดงผล · ร่างที่ยังไม่มีเลข → ข้อความ "ออกอัตโนมัติเมื่อส่งอนุมัติ"
- **Input:** `{ pr_no, status }` · **Output:** `string` · **Invoked by:** FN-01 · FN-02
- **★ ห้าม generate เลขเอง** — function นี้ format อย่างเดียว

---

## §3.2 Engines (Reusable / CUBIC-Registered)

### ENG-PR-CALC · `pr-amount-calculation-engine` (NEW)
| key | value |
|---|---|
| **code** | `pr-amount-calculation-engine` |
| **category** | financial-calculation |
| **input** | `{ lines: [{qty, unit_price_est, discount_mode, discount_pct, discount_amt, vat_mode, vat_pct}], endbill: {enabled, mode, value}, wht: {enabled, pct} }` |
| **output** | `{ subtotal, discount_total, vat_base, vat_amount, grand_total, wht_amount, line_totals[] }` |
| **used by** | F-PUR-PR (+ ทุกเอกสารธุรกรรมที่ใช้ B2 v2: PO · QT · SO · GRN · INV) |

**logic outline:**
1. ต่อบรรทัด: `base = qty × unit_price_est` → หักส่วนลดรายบรรทัด (`pct` หรือ `amt`)
2. แยกตาม `vat_mode` — **3 โหมดใช้ร่วมกันไม่ได้**:
   - `none` → ไม่คิดภาษี
   - `add` → ราคายังไม่รวมภาษี · `vat = base × vat_pct/100`
   - `included` → ราคารวมภาษีแล้ว · **ถอดภาษีย้อน** `base = amount × 100/(100+vat_pct)` (CL-01)
3. รวม `subtotal` · `vat_base` · `vat_amount`
4. หัก **ส่วนลดท้ายบิล** (หลัง VAT) — ไม่เกินยอดหลังภาษี (V-09)
5. `wht_amount` = ประมาณการ **ไม่หักออกจาก `grand_total`** (ไม่ใช่การตั้งหนี้)
6. ปัดเศษสตางค์ **ครึ่งขึ้น** (CL-02)

**Iron rule check:** ✅ pure · ไม่มี HTTP term · ไม่แตะ DB โดยตรง
**★ ต้องรันฝั่งเซิร์ฟเวอร์เสมอตอน create/update/submit** — ห้ามเชื่อยอดจากหน้าจอ (BRD §14.3 · S-06)

### ENG-DOA-RESOLVE · `doa-chain-resolution-engine` (มีอยู่แล้ว — F019)
| key | value |
|---|---|
| **code** | `doa-chain-resolution-engine` |
| **category** | governance |
| **input** | `{ doc_type: 'PR', amount, department, company_ctx }` |
| **output** | `{ doa_entry_ref, chain_mode, steps: [{ slot_seq, role, candidates[] }] }` |
| **used by** | F-PUR-PR · ทุกเอกสารที่ต้องอนุมัติตามวงเงิน |

**★ feature ประกาศเท่านั้น — ตัวเลขวงเงินและรายชื่อผู้ถือสิทธิ์อยู่ที่ทะเบียน DOA กลาง ห้าม hardcode** (LOCK-DOA · BR-08)
ค่า default ที่ lane เสนอ (`[ASSUMED]` OQ-01): ≤50,000 → 1 ขั้น · 50,000.01–500,000 → 2 ขั้น · >500,000 → 3 ขั้น
> **หมายเหตุสำคัญ (OQ-07):** เพราะชั้นอนุมัติ **resolve จากยอดเสมอ** สภาวะ "ยอดเกินวงเงินของขั้นที่เลือก" จึงเกิดไม่ได้เชิงโครงสร้าง — ไม่มี logic เตือนเรื่องนี้และไม่ควรมี

### Engines กลางที่เรียกใช้ (ไม่ใช่ของฟีเจอร์นี้ — ห้าม implement เอง)
| Engine | ใช้ตอน | สัญญา |
|---|---|---|
| `ENG-DOC-NUM` | submit | `next('PR', company_ctx)` → `PR-YYYY-NNNN` · **ห้าม format/+1 เอง** |
| `ENG-DOC-STORE` | อนุมัติครบ | `store(pdf,'PR',pr_id,'approved_final')` |
| `ENG-NOTIFY` | ทุก transition | `emit(event_id,{ref,vars})` · **ห้ามเลือกช่องทาง/เช็ค preference เอง** |
| `ENG-CSQ` | อนุมัติครบ · ยกเลิกใบที่อนุมัติแล้ว | `doc.approved` (EC/estimated) · `doc.cancelled` (EC/avoided) · basis=`declared` · **feature ไม่คำนวณมูลค่าเอง** |
| `ENG-BUDGET` (F117 · W7) | — | **ยังไม่มี** — FN-07 เป็น mock + TODO |

---

## §3.3 ★ API ↔ Logic Trace Table (R8)

| API | Calls Functions | Calls Engines |
|---|---|---|
| API-01 `GET /` | FN-01, FN-16 | — |
| API-02 `GET /:id` | FN-02, FN-11, FN-07, FN-16 | — |
| **API-03** `POST /` | FN-03, FN-04, FN-05 | ENG-PR-CALC |
| **API-04** `PUT /:id` | FN-06, FN-04, FN-05 | ENG-PR-CALC |
| **API-05** `POST /:id/submit` | FN-08, FN-05, FN-07 | ENG-PR-CALC, ENG-DOA-RESOLVE, ENG-DOC-NUM, ENG-NOTIFY |
| **API-06** `POST /:id/approve` | FN-09, FN-11 | ENG-NOTIFY, ENG-CSQ, ENG-DOC-STORE |
| **API-07** `POST /:id/reject` | FN-13, FN-11 | ENG-NOTIFY |
| **API-08** `POST /:id/recall` | FN-10 | ENG-NOTIFY |
| **API-09** `POST /:id/cancel` | FN-14 | ENG-NOTIFY, ENG-CSQ |
| **API-10** `POST /:id/duplicate` | FN-12, FN-03 | ENG-PR-CALC |
| **API-11** `POST /:id/attachments` | FN-15 | ENG-NOTIFY |
| **API-12** `DELETE /:id/attachments/:aid` | FN-15 | — |

### R8 verification
- **mutation API ทั้ง 10 ตัว (API-03..API-12) มี ≥1 Function/Engine** ✅
- **Function ทั้ง 16 ตัวถูก trace อย่างน้อย 1 API** ✅ (FN-01,02,03,04,05,06,07,08,09,10,11,12,13,14,15,16)
- **Engine ทั้ง 2 ตัวของฟีเจอร์ถูก trace** ✅ (ENG-PR-CALC ผ่าน API-03/04/05/10 · ENG-DOA-RESOLVE ผ่าน API-05)
- **ไม่มี orphan Function/Engine** ✅
