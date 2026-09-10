# 03_LOGIC — F-HR-EXPENSE · Expense Claim (เบิกค่าใช้จ่าย)

> **Audience:** BE dev (business logic layer)
> **Scope:** non-HTTP logic — state transitions, guards, VAT/totals, DOA resolve, hooks, masking
> **Iron Rule R8:** ทุก mutation API ต้อง trace ไป ≥1 Function/Engine ใน §3.3
> Naming: Functions = camelCase · Engines = kebab-case

---

## §3.1 Functions (Scope-Local)

### F-HR-EXPENSE-FN-01: `createExpenseClaim`
- **Purpose:** สร้างใบเบิกใหม่ (draft) พร้อม header + lines + snapshot ผู้เบิก/cc (FN-01/02/06)
- **Input:** `{ emp_id, date, pay, lines:[{date,cat,desc,unit_price,vat_mode,over_reason?}] }`
- **Output:** `ExpenseClaim | ValidationError[]`
- **Invoked by:** API-02
- **Calls:** FN-15 resolveMovementSnapshot · FN-13 checkOverCap · ENG-EXP-01 (VAT/totals) · FN-21 appendAudit
- **Side effects:** INSERT T_expense_claim (doc_no=null · status='draft') + T_expense_line + emp_snapshot · audit
- **Error cases:** ERR_VALIDATION_FAILED · BR_LINE_AMOUNT_REQUIRED (unit_price>0 · BR-01)
- **Iron rule check:** ✅ no HTTP terms

### F-HR-EXPENSE-FN-02: `updateExpenseClaim`
- **Purpose:** แก้ไข header/lines ของใบร่าง · re-compute totals (FN-11 groundwork)
- **Input:** `{ id, ...fields, lines? }` · **Output:** `ExpenseClaim | ValidationError[]`
- **Invoked by:** API-04 · **Calls:** ENG-EXP-01, FN-13, FN-21 · **Side effects:** UPDATE + audit (guard status ∈ {draft})
- **Iron rule check:** ✅

### F-HR-EXPENSE-FN-03: `computeLineVat` (calcLineVat)
- **Purpose:** คำนวณ VAT ต่อบรรทัด (none/add/included) → {netAmount, vatAmount, lineTotal} (FN-03)
- **Input:** `{ line{unit_price,qty,vat_mode,vat_pct} }` · **Output:** `{ netAmount, vatAmount, lineTotal }`
- **Invoked by:** ENG-EXP-01 (wrapper), FN-01/02, view/list render · **Calls:** — (pure)
- **Iron rule check:** ✅ pure — ตรรกะจริงอยู่ ENG-EXP-01

### F-HR-EXPENSE-FN-04: `computeTotals` (totals)
- **Purpose:** รวมยอดทั้งใบ (before/vat/grand · single source) — VAT included แยกฐาน (FN-03)
- **Input:** `{ doc{lines[]} }` · **Output:** `{ before, vat, after, grand, n }`
- **Invoked by:** ทุกจุดที่แสดงยอด (list/wizard/view/submit) · **Calls:** FN-03/ENG-EXP-01
- **Iron rule check:** ✅ pure

### F-HR-EXPENSE-FN-05: `resolveApprovalChain` (resolveDoa)
- **Purpose:** resolve สายอนุมัติจากยอดรวม (ตามวงเงิน · FN-08) — เรียกซ้ำได้ → re-resolve เมื่อยอดข้ามช่วง (BR-05/FN-11)
- **Input:** `{ amount }` · **Output:** `{ steps:[{slot_role}], range_label, mock:true }`
- **Invoked by:** API-05, API-12, ใช้ภายใน FN-06 · **External:** DOA engine (F-DLG-001) resolve chain
- **Logic:** เรียก GET /doa/resolve (ของจริง) · **DOA_RANGES ใน HTML = mock** — ช่วงวงเงิน FREE ตั้งค่าที่ DOA กลาง · **ห้าม hardcode สาย/3-tier ในโค้ด**
- **⚠️ OQ-01:** role-id ปลายทาง + CL-0013 แขวน — เดาผิดมีคนตั้งค่าจริง
- **Iron rule check:** ✅

### F-HR-EXPENSE-FN-06: `submitClaim` (doSubmit)
- **Purpose:** ส่งอนุมัติ · resolve DOA + ผูก slot picks → pending_approval (FN-07)
- **Input:** `{ claim_id, steps:[{order,slot_role,approver_id}] }` · **Output:** `ExpenseClaim | BusinessError`
- **Invoked by:** API-05 · **Calls:** FN-05, FN-13 checkOverCap, FN-14 checkReceiptRequired, FN-21
- **Logic:**
  1. guard status='draft' · **canSubmit:** grand>0 && line count>0 (FN-05)
  2. over-cap ทุกรายการมี over_reason (FN-04 · overCapReasonsOk) — ไม่ครบ → BR_OVERCAP_REASON_REQUIRED
  3. ใบเสร็จหมวดบังคับครบ (FN-12) — ไม่ครบ → BR_RECEIPT_REQUIRED
  4. resolve สาย (FN-05) · เลือกผู้อนุมัติครบทุก slot (FN-08 · submitReady) — ไม่ครบ → BR_DOA_SLOTS_INCOMPLETE
  5. INSERT approval_step (N ขั้น · pending) · UPDATE status='pending_approval', doa_range_label · **emit NTF `exp.submitted`** (+ `exp.overcap` ถ้ามี)
- **Side effects:** INSERT T_expense_approval_step + UPDATE claim + audit + NTF · (DOA engine emit doa_pending อัตโนมัติ — ไม่ประกาศเอง)
- **Iron rule check:** ✅

### F-HR-EXPENSE-FN-07: `approveClaimStep` (doApprove)
- **Purpose:** อนุมัติ 1 ขั้น · ครบ → side-effect ทั้งชุด (เลข+PDF+7C · FN-09)
- **Input:** `{ claim_id, actor }` · **Output:** `ExpenseClaim | ConcurrencyError`
- **Invoked by:** API-06 · **Calls:** FN-11 issueDocNumber, FN-22 emitCostStructure, FN-23 snapshotPdf, FN-21 · **External:** ENG-NOTIFY, ENG-DOC-NUM/STORE, CSQ emitter
- **Logic:**
  1. **re-check** actor.canApprove (EC-02) — ไม่ผ่าน → ERR_NOT_APPROVER (FN-20)
  2. guard status='pending_approval' (rejected/cancelled/draft/approved/paid = no-op)
  3. optimistic lock (version · EC-01) — mismatch → ERR_STALE_DATA
  4. หา step pending ตัวถัดไป → result='approved', acted_at=nowStamp; approval_current++
  5. **ยังมีขั้นถัดไป** → คง pending_approval (ไม่ side-effect) · toast "อนุมัติขั้น N แล้ว — รอขั้นถัดไป"
  6. **ครบทุกขั้น** → status='approved' + FN-11 (doc_no) + FN-23 (PDF) + FN-22 (7C FC/EC) + set pay_hook + **emit NTF `exp.approved`** (side-effect "ครั้งเดียว" ตอนจบ chain)
- **Side effects:** UPDATE approval_step + claim · audit · (final) doc_no + PDF + 7C event + NTF
- **Iron rule check:** ✅

### F-HR-EXPENSE-FN-08: `rejectClaim` (doReject)
- **Purpose:** ตีกลับ (เหตุผลบังคับ) → rejected (FN-13)
- **Input:** `{ claim_id, reason, actor }` · **Output:** `ExpenseClaim`
- **Invoked by:** API-07 · **Calls:** FN-21
- **Logic:** re-check canApprove (FN-20) · reason required (ปุ่ม disabled จนกรอก · UX-06) · UPDATE status='rejected', reject_reason · audit(kind=bad) · **emit NTF `exp.rejected`**
- **Error cases:** ERR_NOT_APPROVER · ERR_REASON_REQUIRED

### F-HR-EXPENSE-FN-09: `cancelClaim` (doCancel)
- **Purpose:** ยกเลิกใบเบิก soft archive (FN-14/FN-91)
- **Input:** `{ claim_id }` · **Output:** `ExpenseClaim`
- **Invoked by:** API-08 · **Calls:** FN-21
- **Logic:** **guard status='draft' เท่านั้น** (FIX-05 · paid/approved/rejected/pending = no-op → warn) · UPDATE status='cancelled' (soft archive · ไม่มี hard delete) · audit(kind=warn)
- **⚠️ OQ-05:** ยกเลิกหลังอนุมัติ (ออกเลข+FC/EC แล้ว) **ไม่มี path** — ถ้าเปิด ต้องนิยาม reverse EC/release FC (EC-05)

### F-HR-EXPENSE-FN-10: `reopenClaim` (doReopen)
- **Purpose:** แก้ไขและยื่นใหม่ (rejected → draft · FN-13)
- **Input:** `{ claim_id }` · **Output:** `ExpenseClaim`
- **Invoked by:** API-09 · **Calls:** FN-21
- **Logic:** **guard status='rejected' เท่านั้น** (FIX-04 · กันเลขที่ออกแล้วหาย) · UPDATE status='draft', doc code='(ร่าง)' · reset chain steps → pending · audit
- **Error cases:** BR_REOPEN_ONLY_REJECTED

### F-HR-EXPENSE-FN-11: `issueDocNumber`
- **Purpose:** ออกเลข EXP-<พ.ศ.>-NNNN ตอนอนุมัติครบ (immutable · FN-09)
- **Input:** `{ claim_id }` · **Output:** `{ doc_no }`
- **Invoked by:** FN-07 (ตอน chain ครบ) · **External:** ENG-DOC-NUM.next() (DOCCFG · doc_type EXP)
- **Logic:** **ตัวนับ global เดินหน้าอย่างเดียว (ไม่อิง count สถานะ → ไม่ซ้ำ)** + pad 4 หลัก · **ห้าม feature รันเลขเอง / ห้าม hardcode รูปแบบ** (จาก DOCCFG_BRIEF_F101)
- **Iron rule check:** ✅

### F-HR-EXPENSE-FN-12: `selectPayChannel` / pay-status (payDownstream)
- **Purpose:** เลือก/ส่งช่องทางจ่าย (hook display-only) + อ่านสถานะจ่ายกลับ (FN-10/16)
- **Input:** `{ claim_id, pay }` · **Output:** `ExpenseClaim`
- **Invoked by:** API-10 (write), API-11 (read) · **Calls:** FN-16 computeAdvanceOffset, FN-21 · **External:** Payroll/Finance/F091/F109 hook
- **Logic:** map pay → payDownstream (payroll/transfer/pv/petty) · **hook display-only — ไม่จ่าย/ไม่ post** · status='sent_to_pay' · status='paid' อ่านจากปลายทาง (pay_hook)
- **Iron rule check:** ✅

### F-HR-EXPENSE-FN-13: `checkOverCap` (overCapLines/overCapReasonsOk)
- **Purpose:** ตรวจรายการเกินเพดานหมวด → เตือน + บังคับเหตุผล (FN-04 · LOCK-08)
- **Input:** `{ doc{lines[]} }` · **Output:** `{ over_lines:[{line,cap}], reasons_ok:bool }`
- **Invoked by:** FN-01/02/06, UI render · **Calls:** — (อ่านเพดานจาก HR Config mock)
- **Logic:** cap != null && unit_price > cap → over · ทุก over ต้องมี over_reason.trim() · **ยังส่งได้ (ไม่ hard block · A-EXP-05)**
- **Iron rule check:** ✅ pure

### F-HR-EXPENSE-FN-14: `checkReceiptRequired` (receiptRequiredCats)
- **Purpose:** หมวดที่นโยบายบังคับแนบใบเสร็จก่อนส่ง (FN-12)
- **Input:** `{ doc{lines[]} }` · **Output:** `cat[]` (ที่ receiptRequired=true)
- **Invoked by:** FN-06 (submit guard), UI step4 · **Calls:** — (mock resolve HR Config #107)
- **Iron rule check:** ✅

### F-HR-EXPENSE-FN-15: `resolveMovementSnapshot`
- **Purpose:** snapshot ตำแหน่ง/แผนก/ศูนย์ต้นทุน ณ วันเบิก (soft ref · null≠ไม่มี · FN-06/BR-08)
- **Input:** `{ emp_id, as_of:date }` · **Output:** `{ position, dept, cost_center }`
- **Invoked by:** FN-01 (สร้าง) · **External:** Movement (F-HR-MOVE) resolve(as_of)
- **Side effects:** read-only (เก็บลง emp_snapshot ตอนสร้าง)

### F-HR-EXPENSE-FN-16: `computeAdvanceOffset` (advanceClear · FN-18)
- **Purpose:** หักลบเงินทดรอง — ยอดจ่ายสุทธิ = grand − offset (display-only · soft-ref F103)
- **Input:** `{ emp_id, grand }` · **Output:** `{ adv, offset, netPay, advRemain }`
- **Invoked by:** API-03/10/16, UI view/submit · **Calls:** ENG-EXP-02 · **External:** F103 (read)
- **Logic:** offset = min(adv, grand) · netPay = max(0, grand − offset) · advRemain = max(0, adv − offset) · **F101 ไม่ปรับ ledger F103 — ส่งค่าหักลบให้ F103**
- **Side effects:** read-only (display-only)
- **Iron rule check:** ✅

### F-HR-EXPENSE-FN-17: `checkBudgetWelfareHooks` (budgetHookHTML/welfareTotal)
- **Purpose:** ตรวจงบ (F117) + เพดานสิทธิ์สวัสดิการ (F102) — display-only mock (OQ-EXP-04)
- **Input:** `{ doc{lines[],grand} }` · **Output:** `{ budget_status, welfare_status }`
- **Invoked by:** API-17/18, UI step5/view detail · **Calls:** — · **External:** F117/F102 (read · ยังไม่ dev)
- **Logic:** over = grand > งบคงเหลือ (mock) → เตือน · welfareTotal(หมวดสวัสดิการ) > สิทธิ์ (mock) → เตือน · **display-only — ห้าม hardcode ตัวเลขจริง / ห้าม mock หน้าจอ F117/F102 ใหม่**
- **Side effects:** read-only

### F-HR-EXPENSE-FN-18: `maskMoneyByRole` (maskM · FN-94)
- **Purpose:** ปิดบังตัวเงินตาม role (RESTRICTED)
- **Input:** `{ amount, doc, role }` · **Output:** `string` (`฿x,xxx.xx` | `฿ •••••`)
- **Invoked by:** ทุกจุดแสดงยอด (list/view/PDF/export · API-01/03/20) · **Calls:** FN-19 (isSelf)
- **Logic:** `role.mask && !isSelf(doc)` → mask · ใบของตน/ผู้อนุมัติ/เจ้าหน้าที่ (mask:false) เห็นเต็ม
- **Iron rule check:** ✅ pure

### F-HR-EXPENSE-FN-19: `visibleDocsByScope` (visibleDocs · FN-20)
- **Purpose:** กรองใบเบิกตามขอบเขตการมองเห็น (scope self/all · FN-20 · OQ-EXP-03)
- **Input:** `{ role, all_docs }` · **Output:** `ExpenseClaim[]`
- **Invoked by:** API-01/03 (list/detail scope guard) · **Calls:** —
- **Logic:** scope='all' → ทุกใบ (ผู้อนุมัติ, เจ้าหน้าที่ HR/Finance) · scope='self' → เฉพาะ emp_id=self (ผู้เบิก/ธุรการ)
- **Iron rule check:** ✅

### F-HR-EXPENSE-FN-20: `canApprove` (canApprove guard)
- **Purpose:** guard สิทธิ์อนุมัติ/ตีกลับ — เฉพาะ role `approver:true` (FN-20 · SoD)
- **Input:** `{ role }` · **Output:** `bool`
- **Invoked by:** FN-07/FN-08, UI footer render · **Calls:** —
- **Logic:** เจ้าหน้าที่ HR/Finance เห็นทุกใบ (scope:all) แต่ `approver:false` → กดอนุมัติไม่ได้ (OQ-EXP-03 เจตนา) · ผู้เบิก approver:false (กัน self-approve)
- **Iron rule check:** ✅ pure

### F-HR-EXPENSE-FN-21: `appendAudit`
- **Purpose:** เขียน audit log append-only (FN-93)
- **Input:** `{ entity_type, entity_id, action, detail?, kind?, actor }` · **Output:** `void`
- **Invoked by:** ทุก mutation function · **Calls:** — · **Side effects:** INSERT T_expense_audit_log (ห้าม UPDATE/DELETE)
- **Iron rule check:** ✅

### F-HR-EXPENSE-FN-22: `emitCostStructure` (7C · FN-19)
- **Purpose:** ยิงมูลค่าเข้า 7C ตอนอนุมัติครบ — **FC (commit งบ) + EC (มูลค่า) เท่านั้น · ไม่มี AC** (FN-19 · LOCK-04)
- **Input:** `{ claim_id, cost_center, amount }` · **Output:** `void`
- **Invoked by:** FN-07 (ตอน chain ครบ) · **External:** CSQ emitter · **Side effects:** emit `exp.approved` (FC/EC)
- **Logic:** **ห้ามยิง AC** (Accounting ปลายทาง post เอง) · **ไม่ hardcode ชื่อท่อ** (บันทึกเข้า 7C ตาม CSQ_BRIEF_F101)
- **Iron rule check:** ✅

### F-HR-EXPENSE-FN-23: `snapshotPdf` (a4Doc)
- **Purpose:** สร้าง/เก็บสำเนา PDF a4 (immutable ตอนอนุมัติ · FN-09/15)
- **Input:** `{ claim_id }` · **Output:** `{ pdf_ref }`
- **Invoked by:** FN-07 (final), API-20 · **External:** ENG-DOC-STORE.store()
- **Logic:** render ใบเบิก a4 (หัวบริษัท + รายการ + ยอด + ช่องลายเซ็น 3 ช่อง) · เก็บ immutable snapshot · **สำเนาผ่าน ENG-DOC-STORE (ไม่เก็บเอง)**
- **Iron rule check:** ✅

---

## §3.2 Engines (Reusable / CUBIC-Registered)

### ENG-EXP-01: `expense-vat-calculator` [NEW]

| Field | Value |
|---|---|
| id | (assigned at CUBIC registration) |
| code | `expense-vat-calculator` |
| name | Expense VAT & Totals Calculator |
| category | financial-calculation |
| status | DRAFT (this FRD) |
| owner | F-HR-EXPENSE |

**Input Schema:**
```json
{ "lines":[{"unit_price":number,"qty":number,"vat_mode":"none|add|included","vat_pct":number}] }
```
**Output Schema:**
```json
{ "per_line":[{"netAmount":number,"vatAmount":number,"lineTotal":number}],
  "totals":{"before":number,"vat":number,"grand":number,"n":number} }
```
**Logic Outline:**
1. ต่อบรรทัด: subtotal = qty × unit_price
2. `add` → vat = net × pct/100; lineTotal = net + vat
3. `included` → vat = net × pct/(100+pct); lineTotal = net (ฐาน before = net − vat)
4. `none` → vat = 0; lineTotal = net
5. รวม before/vat/grand (single source · VAT included แยกฐาน)
**Used by:** F-HR-EXPENSE (list/wizard/view/PDF) · (planned) เอกสารธุรกรรมอื่นที่มี line VAT
**Iron rule check:** ✅ pure (no I/O, no HTTP) · reusable · substantial (VAT 3-mode algorithm)
**CUBIC note:** DRAFT → register ตอน dev hand-off (LD-02)

### ENG-EXP-02: `advance-offset-calculator` [NEW]

| Field | Value |
|---|---|
| code | `advance-offset-calculator` |
| name | Advance Clearing / Net Payable Calculator |
| category | financial-calculation |
| status | DRAFT |
| owner | F-HR-EXPENSE |

**Input Schema:** `{ grand:number, advance_outstanding:number }`
**Output Schema:** `{ offset:number, net_pay:number, adv_remain:number }`
**Logic Outline:**
1. offset = min(advance_outstanding, grand)
2. net_pay = max(0, grand − offset) (กันติดลบ)
3. adv_remain = max(0, advance_outstanding − offset)
**Used by:** F-HR-EXPENSE (FN-18 หักลบทดรอง · display-only) · (planned) F103 reconcile
**Iron rule check:** ✅ pure · reusable · substantial (net payable + fallback กันติดลบ) · **display-only — F101 ไม่ปรับ ledger F103**
**CUBIC note:** DRAFT → register Phase 2 (เมื่อ F103 ledger จริงพร้อม)

> **External engines (ไม่ใช่ของ feature นี้ — reference):**
> - DOA engine (F-DLG-001) — resolve สายอนุมัติ **ตามวงเงิน** (ห้าม hardcode · CL-0013 แขวน · OQ-01)
> - ENG-NOTIFY (F-NOTIFY) — emit event ธุรกิจ (submitted/approved/rejected/paid/overcap · ไม่นับ doa_*)
> - ENG-DOC-NUM / ENG-DOC-STORE (DOCCFG) — เลข EXP + สำเนา PDF (ห้าม feature รันเลขเอง)
> - F117 Budget (W7 · **ยังไม่ dev**) / F102 Welfare — ตรวจงบ/สิทธิ์ (display-only จนพร้อม · OQ-EXP-04)
> - F103 Advance — เงินทดรองค้าง (display-only · F101 ไม่ปรับ ledger · FN-18)

---

## §3.3 API ↔ Logic Trace Table (R8 Anchor · MANDATORY)

| API ID | Method | Path | Calls Functions | Calls Engines |
|---|---|---|---|---|
| API-01 | GET | /expenses | FN-19, FN-18 | — |
| API-02 | POST | /expenses | FN-01, FN-15, FN-13, FN-21 | ENG-EXP-01 |
| API-03 | GET | /expenses/:id | FN-18, FN-16, FN-17 | ENG-EXP-01, ENG-EXP-02 |
| API-04 | PUT | /expenses/:id | FN-02, FN-13, FN-21 | ENG-EXP-01 |
| API-05 | POST | /expenses/:id/submit | FN-05, FN-06, FN-13, FN-14, FN-21 | — |
| API-06 | POST | /expenses/:id/approve | FN-07, FN-11, FN-22, FN-23, FN-21 | — |
| API-07 | POST | /expenses/:id/reject | FN-08, FN-21 | — |
| API-08 | POST | /expenses/:id/cancel | FN-09, FN-21 | — |
| API-09 | POST | /expenses/:id/reopen | FN-10, FN-21 | — |
| API-10 | POST | /expenses/:id/pay-channel | FN-12, FN-16, FN-21 | ENG-EXP-02 |
| API-11 | GET | /expenses/:id/pay-status | FN-12 | — |
| API-12 | GET | /doa/resolve | FN-05 | — |
| API-16 | GET | /advances/outstanding | FN-16 | ENG-EXP-02 |
| API-17 | GET | /budget/check | FN-17 | — |
| API-18 | GET | /welfare/remaining | FN-17 | — |
| API-20 | GET | /expenses/:id/pdf | FN-23, FN-18 | — |

### Trace Verification (Self-Check)
- [x] Every mutation API (8 ตัว: API-02/04/05/06/07/08/09/10) has ≥1 Function ✅ (ทุกตัวมี FN-21 appendAudit อย่างน้อย)
- [x] No orphan Function — FN-01..23 ปรากฏใน trace ครบ (FN-03/04 ผ่าน ENG-EXP-01 ใน API-02/03/04; FN-19 ผ่าน API-01; FN-20 ผ่าน FN-07/08 guard; FN-22 ผ่าน FN-07 final)
- [x] No orphan Engine — ENG-EXP-01 (API-02/03/04), ENG-EXP-02 (API-03/10/16) traced
- [x] No hidden logic ใน 02_API — business logic (VAT/totals/DOA/hooks/mask) อยู่ที่นี่ทั้งหมด

---

## §3.4 Dependencies

### External Function/Engine called
- DOA engine `resolve(amount, context)` from F-DLG-001 (Policy Center) — ผ่าน FN-05 (ห้าม hardcode · CL-0013 แขวน)
- `ENG-NOTIFY.emit(event, payload)` from F-NOTIFY — ผ่าน FN-06/FN-07/FN-08 (submitted/approved/rejected/paid/overcap)
- CSQ emitter `emit('exp.approved', {FC,EC})` (ไม่มี AC) — ผ่าน FN-22
- `ENG-DOC-NUM.next()` / `ENG-DOC-STORE.store()` (DOCCFG) — ผ่าน FN-11/FN-23
- Movement resolve (F-HR-MOVE) — ผ่าน FN-15
- HR Config หมวด/เพดาน (F164 #107) — ผ่าน FN-13/FN-14 (mock resolve · A-EXP-04)
- F103 advance read — ผ่าน FN-16 (display-only)
- F117/F102 read — ผ่าน FN-17 (display-only mock)

### External that calls into this feature
- 7C / CSQ รับ event FC/EC จาก FN-22 (ไม่มี AC)
- Payroll/Finance/F091/F109 รับ hook จ่ายจาก FN-12 (display-only)
- F103 รับค่าหักลบจาก FN-16 (display-only · ledger เป็นของ F103)

---

## §3.5 Locked Decisions Referenced
- LD-01: optimistic locking (version) กัน concurrent approve (EC-01) — ดู 07_LOCKED
- LD-02: ENG-EXP-01/02 register CUBIC Phase 2 (scope-local ก่อน)
- LD-03: DOA chain = ประกาศเท่านั้น · ช่วงวงเงิน FREE (ไม่ hardcode 3-tier) · CL-0013 แขวน (OQ-01)
- LD-04: จ่ายจริง/GL/ทดรอง/งบ/สวัสดิการ = hook display-only (LOCK-03/09 · OQ-03/EXP-04)
- LD-05: 7C = FC/EC เท่านั้น (ไม่มี AC · LOCK-04 · OQ-EXP-02)
- LD-06: cancel เฉพาะ draft · reopen เฉพาะ rejected — ยกเลิกหลังอนุมัติ = ไม่มี path (OQ-05 reverse EC/FC)

---

## Audience Cheat-Sheet
| Reader | Read |
|---|---|
| BE dev | §3.1 + §3.2 + §3.3 |
| QA | §3.3 + §3.1 Side effects + §3.2 I/O |
| Architect / CUBIC | §3.2 + §3.4 + §3.5 |
