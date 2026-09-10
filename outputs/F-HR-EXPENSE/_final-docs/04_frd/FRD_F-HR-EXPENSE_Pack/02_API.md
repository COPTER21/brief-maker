# 02_API — F-HR-EXPENSE · Expense Claim (เบิกค่าใช้จ่าย)

> **Audience:** Backend developer (HTTP layer)
> **🚨 Iron Rule:** ห้าม business logic > 5 บรรทัดที่นี่ — ย้ายไป 03_LOGIC §3.1
> **🚨 R8:** ทุก mutation API ต้องระบุ "Calls (Logic)" → trace ใน 03_LOGIC §3.3
> Base path: `/api/v1/expense` · Headers: `X-Tenant-Id` (required) · mutation: `Idempotency-Key` (required · FN-92)

---

## §2.1 API Overview

| ID | Method | Path | Summary | Auth (role) |
|---|---|---|---|---|
| API-01 | GET | /expenses | List ใบเบิก (scope self/all · filter สถานะ/ค้นหา) | any (scope-filtered) |
| API-02 | POST | /expenses | สร้างใบเบิก (draft · header + lines) | maker (ผู้เบิก/ธุรการ) |
| API-03 | GET | /expenses/:id | รายละเอียดใบเบิก + lines + steps + audit | any (scope + mask) |
| API-04 | PUT | /expenses/:id | แก้ไขใบเบิก (draft · lines/header) | maker |
| API-05 | POST | /expenses/:id/submit | ส่งอนุมัติ (resolve DOA + slot picks → pending_approval) | maker |
| API-06 | POST | /expenses/:id/approve | อนุมัติ 1 ขั้น (ครบ → เลข+PDF+7C) | approver (canApprove) |
| API-07 | POST | /expenses/:id/reject | ตีกลับ (เหตุผลบังคับ) | approver (canApprove) |
| API-08 | POST | /expenses/:id/cancel | ยกเลิก (soft archive · เฉพาะ draft) | maker |
| API-09 | POST | /expenses/:id/reopen | แก้ไขและยื่นใหม่ (rejected → draft) | maker |
| API-10 | POST | /expenses/:id/pay-channel | เลือก/ส่งช่องทางจ่าย (hook display-only) | เจ้าหน้าที่/maker |
| API-11 | GET | /expenses/:id/pay-status | สถานะจ่าย (hook อ่านกลับ display-only) | any |
| API-12 | GET | /doa/resolve?amount= | (ext DOA F-DLG-001) resolve สายตามวงเงิน | any |
| API-13 | GET | /hr-config/expense-categories | (ref F164 #107) หมวด/เพดาน (A-EXP-04 mock) | any |
| API-14 | GET | /employees?status=active&q= | (ref F011) ผู้เบิก/ผู้อนุมัติ combobox | any |
| API-15 | GET | /movement/resolve?emp_id=&as_of= | (ref F-HR-MOVE) ตำแหน่ง/cc snapshot | any |
| API-16 | GET | /advances/outstanding?emp_id= | (hook F103) เงินทดรองค้าง — display-only (FN-18) | any (mask) |
| API-17 | GET | /budget/check?amount= | (hook F117) ตรวจงบ — display-only mock (OQ-EXP-04) | any |
| API-18 | GET | /welfare/remaining?emp_id=&cat= | (hook F102) สิทธิ์สวัสดิการ — display-only mock (OQ-EXP-04) | any |
| API-20 | GET | /expenses/:id/pdf | สำเนา PDF (a4 · snapshot ตอนอนุมัติ) | any (mask) |

> **Mutation APIs (ต้อง trace §2.4/R8):** API-02, 04, 05, 06, 07, 08, 09, 10

---

## §2.2 Per-API Contract (key endpoints)

### API-02: POST /expenses
| Field | Value |
|---|---|
| roles | maker (ผู้เบิก/ธุรการ) |
| headers | X-Tenant-Id, Idempotency-Key (required) |

**Body:**
```json
{ "emp_id":"uuid", "date":"2569-08-31", "pay":"payroll",
  "lines":[{ "date":"2569-08-28","cat":"travel","desc":"ค่าแท็กซี่","unit_price":450,"vat_mode":"add","over_reason":null }] }
```
**Validation (field-level ≤5 lines):** emp_id required · date required · pay ∈ {payroll,transfer,pv,petty} · แต่ละ line: cat ∈ HR Config · unit_price > 0 (BR-01) · **complex → 03_LOGIC FN-01 createExpenseClaim**
**Response 201:** `{ "id":"uuid","status":"draft","doc_no":null }` (doc_no ออกตอนอนุมัติ)
**Errors:** 400 ERR_VALIDATION_FAILED · 403 ERR_INSUFFICIENT_ROLE · 409 ERR_DUPLICATE_IDEMPOTENCY_KEY · 422 BR_LINE_AMOUNT_REQUIRED (BR-01)
**Preconditions:** cat exists in HR Config (#107) · emp_id resolvable (Movement snapshot · FN-06)
**Side effects:** INSERT T_expense_claim + T_expense_line + emp_snapshot (Movement resolve as_of=date) · INSERT audit
**Calls (Logic):** FN-01 createExpenseClaim · FN-15 resolveMovementSnapshot · FN-03/FN-04 (ENG-EXP-01 VAT/totals) · FN-13 checkOverCap · FN-21 appendAudit

---

### API-04: PUT /expenses/:id
**Body:** `{ ...header?, lines?:[...] }` · **Preconditions:** status ∈ {draft, rejected→draft ผ่าน reopen} · optimistic lock (version)
**Behavior:** แก้ header/lines · re-compute totals · **ยอดเปลี่ยนข้ามช่วง → re-resolve DOA ตอน submit** (FN-11 · resolve เกิดตอน submit ไม่ freeze จน submit)
**Side effects:** UPDATE claim/lines · audit · **Errors:** 409 ERR_STALE_DATA
**Calls (Logic):** FN-02 updateExpenseClaim · FN-03/FN-04 · FN-13 · FN-21

---

### API-05: POST /expenses/:id/submit (ส่งอนุมัติ · DOA)
**Body:**
```json
{ "steps":[ {"order":1,"slot_role":"หัวหน้าสายงาน","approver_id":"A1"},
            {"order":2,"slot_role":"ผู้จัดการแผนก","approver_id":"A2"} ] }
```
**Preconditions:**
- status='draft' · grand > 0 · line count > 0 (**FN-05** · canSubmit)
- over-cap ทุกรายการมี over_reason ครบ (**FN-04** · overCapReasonsOk)
- ใบเสร็จหมวดบังคับครบ (**FN-12** · receiptRequired)
- resolve สายจากยอดรวม (**GET /doa/resolve** · API-12) · เลือกผู้อนุมัติครบทุก slot (**FN-08** · ไม่ hardcode สาย · จาก DOA กลาง)
**Response 200:** `{ "id","status":"pending_approval","doa_range_label":"...","steps":[...] }`
**Errors:** 422 BR_SUBMIT_NO_LINES (FN-05) · 422 BR_OVERCAP_REASON_REQUIRED (FN-04) · 422 BR_RECEIPT_REQUIRED (FN-12) · 422 BR_DOA_SLOTS_INCOMPLETE (FN-08)
**Side effects:** resolve DOA (API-12) → INSERT T_expense_approval_step (N ขั้น · result='pending') · UPDATE status='pending_approval', doa_range_label, doc code='(รออนุมัติ)' · audit · **emit NTF `exp.submitted`** (+ `exp.overcap` ถ้ามี over-cap) · (DOA engine emit `doa_pending` อัตโนมัติ — ไม่ประกาศเอง)
**Calls (Logic):** FN-05 resolveApprovalChain · FN-06 submitClaim · FN-13 checkOverCap · FN-14 checkReceiptRequired · FN-21

> **FN-11 re-resolve:** ยอดที่ resolve = ยอด ณ ตอน submit · ถ้าแก้ยอดแล้ว submit ใหม่ → resolve ใหม่ตามช่วง (BR-05)

---

### API-06: POST /expenses/:id/approve
**Preconditions:** caller `canApprove` (**re-check ที่ mutation** · EC-02/BR-13) · status='pending_approval' · มีขั้น pending · optimistic lock (version · EC-01)
**Behavior (→ FN-07):**
1. หา step pending ตัวถัดไป → result='approved', acted_at=nowStamp; approval_current++
2. **ยังมีขั้นถัดไป** → คง status='pending_approval' (ยังไม่ side-effect) · toast "อนุมัติขั้น N แล้ว — รอขั้นถัดไป"
3. **ครบทุกขั้น** → status='approved' + **ออกเลข doc_no `EXP-<พ.ศ.>-NNNN`** (ENG-DOC-NUM · ตัวนับ global · FN-11) + **สำเนา PDF** (ENG-DOC-STORE · FN-23) + **emit 7C `FC (commit งบ) + EC (มูลค่า)` — ไม่มี AC** (FN-22/FN-19) + **emit NTF `exp.approved`** + set pay_hook (ส่งสถานะจ่ายปลายทาง)
**Response 200:** `{ "id","status":"pending_approval|approved","doc_no?","approval_current":n }`
**Errors:** 403 ERR_NOT_APPROVER (BR-13) · 409 ERR_STALE_DATA (EC-01) · 422 BR_NOT_PENDING_APPROVAL · 422 BR_NO_PENDING_STEP
**Side effects:** UPDATE approval_step + claim · audit · (final) doc_no + PDF snapshot + 7C event + NTF
**Calls (Logic):** FN-07 approveClaimStep · FN-11 issueDocNumber · FN-22 emitCostStructure · FN-23 snapshotPdf · FN-21

---

### API-07: POST /expenses/:id/reject
**Body:** `{ "reason":"..." }` (required · BR-18/D15)
**Preconditions:** canApprove · status='pending_approval'
**Side effects:** UPDATE status='rejected' · reject_reason · audit(kind=bad) · **emit NTF `exp.rejected`**
**Errors:** 403 ERR_NOT_APPROVER · 400 ERR_REASON_REQUIRED
**Calls (Logic):** FN-08 rejectClaim · FN-21

### API-08: POST /expenses/:id/cancel
**Body:** `{}` (confirm ที่ UI · Pattern D) · **Preconditions (FN-14 · guard):** status='draft' เท่านั้น (paid/approved/rejected/pending = no-op)
**Side effects:** UPDATE status='cancelled' (soft archive · ไม่มี hard delete) · audit(kind=warn)
**Errors:** 422 BR_CANCEL_ONLY_DRAFT
**⚠️ OQ-05:** path "ยกเลิกหลังอนุมัติ" **ไม่มีในระบบปัจจุบัน** (cancel เฉพาะ draft) — ถ้า BA ต้องการเปิด → ต้องนิยาม compensating **reverse EC / release FC** (ดู 05_RULES EC-05)
**Calls (Logic):** FN-09 cancelClaim · FN-21

### API-09: POST /expenses/:id/reopen
**Body:** `{}` · **Preconditions (FN-13 · guard · FIX-04):** status='rejected' เท่านั้น (กันเลขที่ออกแล้วหาย)
**Side effects:** UPDATE status='draft' · doc code='(ร่าง)' · reset chain steps → pending · audit
**Errors:** 422 BR_REOPEN_ONLY_REJECTED
**Calls (Logic):** FN-10 reopenClaim · FN-21

### API-10: POST /expenses/:id/pay-channel (hook display-only)
**Body:** `{ "pay":"payroll|transfer|pv|petty" }` · **Preconditions:** status='approved' (หรือ sent_to_pay)
**Behavior:** เลือก/ยืนยันช่องทางจ่าย → ส่งจ่าย **hook display-only** (payDownstream) · **ไม่จ่าย/ไม่ post** · optional หักลบทดรอง F103 (advance_offset · display-only · FN-18) → status='sent_to_pay'
**Side effects:** UPDATE pay + status='sent_to_pay' + advance_offset (จาก API-16) · audit · **ส่งค่าหักลบให้ F103 (ไม่ปรับ ledger เอง)**
**Calls (Logic):** FN-12 selectPayChannel · FN-16 computeAdvanceOffset (ENG-EXP-02) · FN-21

### API-11: GET /expenses/:id/pay-status (hook read)
Read-only · อ่านสถานะจ่ายจากปลายทาง (Payroll/Finance · display-only) → pay_hook · status paid เมื่อปลายทางจ่ายจริง (**FN-16**)
**Calls (Logic):** FN-12 (read path)

---

### API-12: GET /doa/resolve?amount= (ext · DOA F-DLG-001)
**สถานะ:** สายอนุมัติ resolve **ตามวงเงิน** — ช่วงวงเงิน **FREE ตั้งค่าอิสระที่ DOA กลาง** · `DOA_RANGES` ใน HTML = **mock/ตัวอย่าง** (ห้าม hardcode 3-tier ในระบบจริง · OQ-01 · CL-0013 แขวน)
**Response 200:** `{ "range_label":"฿5,000.00 – ฿50,000.00","steps":[{"order":1,"slot_role":"หัวหน้าสายงาน"},...] }`

### API-13: GET /hr-config/expense-categories (ref F164 #107)
Read-only · หมวด + เพดาน + receiptRequired · **group เพดานยังไม่มีใน HR Config → mock resolve** (A-EXP-04 · OQ-02) · ห้าม hardcode ตัวเลขเพดาน

### API-16: GET /advances/outstanding?emp_id= (hook F103 · display-only)
Read-only · เงินทดรองค้างของผู้เบิก · **F101 ไม่ปรับ ledger F103** — ใช้คำนวณ advance_offset (display-only · FN-18)

### API-17/18: GET /budget/check · /welfare/remaining (hook F117/F102 · display-only mock)
Read-only · **display-only mock** (F117 W7 ยังไม่ dev · F102 ctl) · render สถานะ + note ที่มา · **ห้าม hardcode ตัวเลขจริง** (OQ-EXP-04)

### API-20: GET /expenses/:id/pdf
สำเนา PDF a4 (immutable snapshot ตอนอนุมัติ · ENG-DOC-STORE) · mask ตาม role

---

## §2.3 Common Concerns

### Idempotency (PR-7 · FN-92)
ทุก mutation รับ `Idempotency-Key` · cache 24 ชม. · key เดิม+body เดิม → คืน cached (ไม่ INSERT ซ้ำ) · key เดิม+body ต่าง → 409 · **UI กัน double-submit ด้วย `state._busy`** (ทุก action ที่เปลี่ยนสถานะ · L2428/2440/2474/2480)

### Optimistic Locking (PR-1/EC-01)
approve/update ใช้ `version` (หรือ `If-Match: updated_at`) · mismatch → 409 ERR_STALE_DATA (กัน 2 approver ชนกันขั้นเดียว)

### Permission re-check (PR-3/EC-02)
role/canApprove ตรวจที่ **mutation time** ไม่ใช่แค่ GET → 403 ERR_NOT_APPROVER / ERR_PERMISSION_REVOKED (`doApprove`/`doReject` guard L2442/2476)

### Scope guard (FN-20)
GET list/detail กรองตาม role.scope: `self` → เฉพาะ emp_id=self · `all` → ทุกใบ (visibleDocs L2173) · enforce ที่ API (ไม่พึ่ง client เท่านั้น)

### Multi-Tenant
ทุก endpoint บังคับ X-Tenant-Id · DB filter ผ่าน RLS

### Audit Log (FN-93)
ทุก mutation เขียน T_expense_audit_log (append-only) ผ่าน FN-21 · เก็บ actor/action/detail/kind/at

### Masking (FN-94)
field Restricted (grand/unit_price/line_total/advance_offset/FC·EC) → API คืน `฿ •••••` หรือ excluded เมื่อ role ไม่ unmask ใบคนอื่น · **export/PDF ก็ mask ตาม role** (§10.2 PM edge)

---

## §2.4 API → Logic Trace (Anchor for R8)

> **Authoritative:** 03_LOGIC §3.3 · ที่นี่ summary

| API | Calls Functions | Calls Engines |
|---|---|---|
| API-01 GET list | FN-19 visibleDocsByScope, FN-18 mask | — |
| API-02 POST create | FN-01, FN-15, FN-13, FN-21 | ENG-EXP-01 |
| API-03 GET detail | FN-18, FN-16 | ENG-EXP-01, ENG-EXP-02 |
| API-04 PUT update | FN-02, FN-13, FN-21 | ENG-EXP-01 |
| API-05 submit | FN-05, FN-06, FN-13, FN-14, FN-21 | — |
| API-06 approve | FN-07, FN-11, FN-22, FN-23, FN-21 | — |
| API-07 reject | FN-08, FN-21 | — |
| API-08 cancel | FN-09, FN-21 | — |
| API-09 reopen | FN-10, FN-21 | — |
| API-10 pay-channel | FN-12, FN-16, FN-21 | ENG-EXP-02 |
| API-11 pay-status | FN-12 | — |
| API-16 advances | FN-16 | ENG-EXP-02 |
| API-17/18 budget/welfare | FN-17 | — |
| API-20 pdf | FN-23, FN-18 | — |

> **R8 Check:** ทุก mutation row (API-02,04,05,06,07,08,09,10) มี ≥1 Function ✅ (FN-21 appendAudit ทุก mutation)

---

## §2.X Cross-Module Contract (จาก BRD §12.1 Downstream Impact Map)

| Downstream | รูปแบบ | Contract | Trigger | Payload หลัก |
|---|---|---|---|---|
| 7C / โครงสร้างต้นทุน (CSQ) | Event | `exp.approved` → **FC (commit งบ) + EC (มูลค่า)** · **ไม่มี AC** (FN-19) | อนุมัติครบสาย (API-06 final) | `{ ref:claim_id, doc_no, cost_center, amount, currency:'THB', kinds:['FC','EC'] }` (CSQ_BRIEF) |
| Payroll (HK-1)/Finance/F091/F109 | Event/hook (display-only) | `exp.pay_hook` | เลือกช่องทางจ่าย (API-10) | `{ claim_id, doc_no, pay, net_pay, currency:'THB' }` — **ไม่ auto-post/ไม่ auto-จ่าย** |
| F103 เงินทดรอง | hook (display-only) | `exp.advance_offset` | หน้ารายละเอียด/จ่าย (API-10/16) | `{ emp_id, offset }` — **F101 ไม่ปรับ ledger F103** ส่งค่าหักลบให้ F103 (FN-18) |
| F117 Budget Control | hook (ctl · display-only mock) | GET /budget/check (API-17) | render ก่อนอนุมัติ | **display-only จน F117 W7 พร้อม (OQ-EXP-04)** |
| F102 Welfare | hook (ctl · display-only mock) | GET /welfare/remaining (API-18) | render หมวดสวัสดิการ | **display-only (OQ-EXP-04)** |
| DOA กลาง (F-DLG-001) | Engine (external) | resolve chain ตามวงเงิน | ส่งอนุมัติ (API-05/12) | slots ตามตำแหน่ง (ไม่ hardcode · CL-0013 แขวน) |
| ENG-NOTIFY | Event | submitted/approved/rejected/paid/overcap | state transition | ดู NTF_BRIEF / 01_UI §1.5 |
| ENG-DOC-NUM / ENG-DOC-STORE | Engine (external) | เลข EXP + สำเนา PDF | อนุมัติครบ (API-06 final) | doc_type EXP (DOCCFG_BRIEF · ห้าม feature รันเลขเอง) |

- **compensating (ยกเลิก/แก้หลังอนุมัติ):** path **ไม่มีในระบบปัจจุบัน** (cancel เฉพาะ draft · reopen เฉพาะ rejected) → ถ้าเปิด = ต้องนิยาม **reverse EC / release FC** (OQ-05 · policy pending) → trace 06_TESTS XT-04
- ทุกแถวที่มี data ไหล → trace 06_TESTS §6.9 (XT-01..04) อย่างน้อย 1 case
