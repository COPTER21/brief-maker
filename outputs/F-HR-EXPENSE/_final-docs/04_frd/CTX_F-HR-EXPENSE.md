# CTX — F-HR-EXPENSE: เบิกค่าใช้จ่าย (Expense Claim · F101)

> **derived from:** FRD_F-HR-EXPENSE v1.0 · **generated:** 2026-09-10
> **module:** HR (Human Capital → Expense & Reimbursement) · **wave:** W5 · **status:** active
> ⚠ Derived artifact — source of truth = FRD · ถ้า FRD revise ต้อง regen CTX

---

## 1. Summary

ใบเบิกค่าใช้จ่ายพนักงาน (archetype Q-document · เลขรัน `EXP-<พ.ศ.>-NNNN` + PDF + line editor). ผู้เบิก/ธุรการสร้างใบผ่าน wizard (หัวเอกสาร + รายการค่าใช้จ่าย + VAT + แนบใบเสร็จ) แล้วส่งอนุมัติตามสาย DOA ที่ resolve **ตามยอดรวม** (มีวงเงิน). อนุมัติครบสาย → ออกเลขเอกสาร + เก็บสำเนา PDF + ยิง 7C **FC (commit งบ) + EC (มูลค่า) — ไม่มี AC**. การจ่ายจริง (payroll/transfer/PV/petty), การหักลบเงินทดรอง (F103), การตรวจงบ (F117) และสิทธิ์สวัสดิการ (F102) เป็น **hook display-only** — F101 ไม่จ่าย/ไม่ post บัญชี/ไม่ปรับ ledger ปลายทาง.

---

## 2. Data Contract

### Entities

| Entity | PK | Key Fields (cross-boundary) | หมายเหตุ |
|---|---|---|---|
| `T_expense_claim` | `id` (uuid) | `doc_no` (EXP-พ.ศ.-NNNN · null ก่อนอนุมัติ) · `emp_id` (FK T_employee) · `emp_snapshot` (jsonb · PII) · `status` · `pay` · `grand` (Restricted) · `advance_offset` (Restricted · display-only) · `date` · `version` (optimistic lock) | header · UNIQUE(tenant_id, doc_no) WHERE doc_no NOT NULL |
| `T_expense_line` | `id` (uuid) | `claim_id` (FK) · `line_no` · `cat` · `unit_price` (Restricted) · `qty` · `vat_mode` · `vat_pct` · `line_total` (Restricted) · `over_reason` | 1 claim : N line (grid B2 v2) · UNIQUE(claim_id, line_no) |
| `T_expense_approval_step` | `id` (uuid) | `claim_id` (FK) · `step_order` · `slot_role` (role ref จาก DOA · ไม่ hardcode คน) · `approver_id` (FK T_employee · PII) · `result` · `acted_at` | สาย DOA embedded เมื่อยื่น · UNIQUE(claim_id, step_order) |
| `T_expense_audit_log` | `id` (bigserial) | `entity_type` · `entity_id` · `action` · `kind` · `actor` (PII) · `at` | append-only · **NO UPDATE / NO DELETE** |
| `T_employee` (F011) | — | อ่าน: ผู้เบิก/ผู้อนุมัติ | existing master (read) |

### Enums / States

| Field | Values (ครบทุกค่า) | Transition owner |
|---|---|---|
| `claim.status` (lifecycle 8 state) | `draft` · `pending_approval` · `approved` · `sent_to_pay` · `paid` · `closed` · `rejected` · `cancelled` | F-HR-EXPENSE (`sent_to_pay`/`paid`/`closed` = state ปลายทาง hook) |
| `claim.pay` | `payroll` · `transfer` · `pv` · `petty` (PV/petty = touchpoint F091 · display-only · FN-18) | F-HR-EXPENSE |
| `line.vat_mode` | `none` · `add` · `included` | F-HR-EXPENSE |
| `line.cat` | `travel` · `lodge` · `ent` · `mat` · `other` (อ่านจาก HR Config #107 · F164) | F164 (read) |
| `approval_step.result` | `pending` · `approved` · `rejected` | F-HR-EXPENSE |
| `audit_log.entity_type` | `claim` · `line` · `approval` | F-HR-EXPENSE |
| `audit_log.kind` | `ok` · `warn` · `bad` | F-HR-EXPENSE |

**State machine (transitions):**
```
draft ──submit──▶ pending_approval ──อนุมัติครบสาย──▶ approved ──เลือกจ่าย(hook)──▶ sent_to_pay ──จ่ายจริง(hook)──▶ paid ──▶ closed
  │                     │
  │                     └──ตีกลับ(reason)──▶ rejected ──reopen──▶ draft
  └──ยกเลิก(ร่างเท่านั้น)──▶ cancelled (soft archive)
```
> ไม่มี transition `approved/paid → cancelled` ในระบบปัจจุบัน (cancel เฉพาะ draft · reopen เฉพาะ rejected) — เปิด path = ต้องนิยาม reverse EC/release FC (OQ-05).

### Relationships

- `T_expense_claim` 1—N `T_expense_line` (fk: claim_id)
- `T_expense_claim` 1—N `T_expense_approval_step` (fk: claim_id · embed เมื่อยื่น DOA)
- `T_employee` 1—N `T_expense_claim` (emp_id + emp_snapshot) · `T_employee` 1—N `T_expense_approval_step` (approver_id)
- (all) ──▶ `T_expense_audit_log` (polymorphic entity_type/entity_id · append-only)
- **Masters read (read-only hook · ไม่ FK ข้าม service):**
  - Employee (F011) ▶ `emp_id` · combobox `GET /employees`
  - Movement (F-HR-MOVE) ▶ `emp_snapshot.position/cost_center` (resolve as_of=วันเบิก · null≠ไม่มี · BR-08)
  - HR Config #107 (F164) ▶ `line.cat` + เพดานหมวด (group ยังไม่มี → mock · A-EXP-04)
  - DOA กลาง (F-DLG-001) ▶ `approval_step` (resolve ตามวงเงิน · ไม่ hardcode)
- **Soft-ref (display-only · F101 ไม่ปรับ ledger/ค่าปลายทาง):**
  - F103 (เงินทดรอง) ▶ `claim.advance_offset` (FN-18)
  - F117 (งบ) / F102 (สวัสดิการ) ▶ ตรวจก่อนอนุมัติ (display-only mock · OQ-EXP-04)
  - Payroll/Finance/F091/F109 ◀ `claim.pay`/`pay_hook` (hook จ่าย)

---

## 3. API Surface

Base: `/api/v1/expense` · Headers: `X-Tenant-Id` (required) · mutation: `Idempotency-Key` (required)

| Method | Endpoint | ทำอะไร | Payload หลัก |
|---|---|---|---|
| GET | /expenses | list (scope self/all + filter/search) | — (mask ตาม role) |
| POST | /expenses | สร้าง draft (header + lines) | `{ emp_id, date, pay, lines[] }` → `{ id, status:draft, doc_no:null }` |
| GET | /expenses/:id | รายละเอียด + lines + steps + audit | (scope + mask) |
| PUT | /expenses/:id | แก้ไข draft (re-compute totals) | `{ header?, lines? }` · optimistic lock |
| POST | /expenses/:id/submit | ส่งอนุมัติ (resolve DOA + slot picks → pending_approval) | `{ steps:[{order, slot_role, approver_id}] }` |
| POST | /expenses/:id/approve | อนุมัติ 1 ขั้น (ครบ → เลข + PDF + 7C) | → `{ status, doc_no?, approval_current }` |
| POST | /expenses/:id/reject | ตีกลับ (เหตุผลบังคับ) | `{ reason }` (required · BR-18) |
| POST | /expenses/:id/cancel | ยกเลิก (soft archive · เฉพาะ draft) | `{}` |
| POST | /expenses/:id/reopen | แก้แล้วยื่นใหม่ (rejected → draft) | `{}` |
| POST | /expenses/:id/pay-channel | เลือกช่องทางจ่าย (hook display-only → sent_to_pay) | `{ pay }` |
| GET | /expenses/:id/pay-status | สถานะจ่าย (hook อ่านกลับ → paid) | (display-only) |
| GET | /expenses/:id/pdf | สำเนา PDF a4 (snapshot ตอนอนุมัติ) | (mask ตาม role) |
| GET | /doa/resolve?amount= | (ext F-DLG-001) resolve สายตามวงเงิน (FREE ranges) | → `{ range_label, steps[] }` |
| GET | /hr-config/expense-categories | (ref F164 #107) หมวด/เพดาน (mock) | read-only |
| GET | /employees?status=active&q= | (ref F011) combobox ผู้เบิก/ผู้อนุมัติ | read-only |
| GET | /movement/resolve?emp_id=&as_of= | (ref F-HR-MOVE) ตำแหน่ง/cc snapshot | read-only |
| GET | /advances/outstanding?emp_id= | (hook F103) เงินทดรองค้าง — display-only | read-only (mask) |
| GET | /budget/check?amount= · /welfare/remaining?emp_id=&cat= | (hook F117/F102) display-only mock | read-only |

> Cross-cutting: Idempotency-Key (cache 24ชม) · optimistic lock (`version` → 409 ERR_STALE_DATA) · permission re-check ที่ mutation time (403 ERR_NOT_APPROVER) · scope guard self/all enforce ที่ API · masking Restricted field ที่ API + export/PDF.

### Events emitted

| Event | Trigger point | Payload key |
|---|---|---|
| `exp.submitted` (NTF) | `draft → pending_approval` (API-05 · FN-06) → ผู้อนุมัติขั้นแรก | `ref=claim_id` · `{code, grand, employee}` |
| `exp.overcap` (NTF) | ยื่นใบมีรายการเกินเพดาน (API-05 · BR-02) → ผู้อนุมัติ | `ref=claim_id` · `{code}` |
| `exp.approved` (NTF) | `pending_approval → approved` ครบสาย (API-06 final) → ผู้เบิก | `ref=claim_id` · `{code}` (in-app+email · lock on) |
| `exp.rejected` (NTF) | `pending_approval → rejected` (API-07 · BR-18) → ผู้เบิก | `ref=claim_id` · `{reason}` |
| `exp.paid` (NTF) | `sent_to_pay → paid` — hook อ่านกลับ (API-11 · FN-16) → ผู้เบิก | `ref=claim_id` · `{code}` |
| **7C `FC` + `EC`** (CSQ · ไม่มี AC) | อนุมัติครบสาย (API-06 final · FN-22) | `{ ref:claim_id, doc_no, cost_center, amount, currency:'THB', kinds:['FC','EC'] }` |
| `exp.pay_hook` (hook · display-only) | เลือกช่องทางจ่าย (API-10) | `{ claim_id, doc_no, pay, net_pay, currency:'THB' }` — ไม่ auto-post/จ่าย |
| `exp.advance_offset` (hook · display-only) | หน้ารายละเอียด/จ่าย (API-10/16) | `{ emp_id, offset }` — F101 ไม่ปรับ ledger F103 |

> DOA engine emit (`doa_pending`/`doa_result`/`doa_step_approved`/`doa_escalate`) มาจาก F-DLG-001 อัตโนมัติ — feature **ไม่ประกาศซ้ำ**.

---

## 4. Shared Rules (cross-boundary เท่านั้น)

| Rule ID | Rule | กระทบใคร |
|---|---|---|
| BR-06 (LOCK-02) | เลข `EXP-<พ.ศ.>-NNNN` + สำเนา PDF ออก **ครั้งเดียวตอนอนุมัติครบ** · ตัวนับ global monotonic (ไม่ reuse/renumber) · immutable · via ENG-DOC-NUM/STORE (ห้าม feature รันเลขเอง) | DOCCFG (F-DOCCFG) · ENG-DOC-NUM · ENG-DOC-STORE |
| BR-07 (LOCK-04 · FN-19) | อนุมัติครบสาย → emit 7C **FC (commit งบ) + EC (มูลค่า) เท่านั้น · ไม่มี AC** (Accounting post เอง) | 7C/CSQ · Accounting ปลายทาง |
| BR-04 (LOCK-01) | ส่งอนุมัติ = DOA resolve **ตามยอดรวม** · ช่วงวงเงิน FREE ตั้งที่ DOA กลาง (ไม่ hardcode 3-tier/สาย) · ครบทุก slot จึงส่งได้ | DOA กลาง (F-DLG-001 · CL-0013 แขวน) |
| BR-08 (LOCK-06) | ตำแหน่ง/ศูนย์ต้นทุน = snapshot Movement ณ วันเบิก (soft ref · null≠ไม่มี) | F-HR-MOVE |
| BR-09 (LOCK-03) | จ่ายจริง/post/paid = **hook display-only** — F101 ไม่จ่าย/ไม่ post บัญชี/ไม่ปรับ ledger | Payroll/Finance/F091/F109 |
| BR-11 (FN-18 · LOCK-09) | ยอดจ่ายสุทธิ = grand − offset (offset = min(adv, grand)) · **display-only** · F101 ไม่ปรับ ledger F103 (ส่งค่าหักลบให้ F103) | F103 (Advance) |
| BR-15 (OQ-EXP-04) | ตรวจงบ (F117) + สิทธิ์สวัสดิการ (F102) = hook display-only (เตือน · ไม่ block) | F117 Budget · F102 Welfare |
| BR-10 / BR-12 (LOCK-07/10) | ตัวเงิน RESTRICTED mask ตาม role (grand/unit_price/line_total/advance/FC·EC) — ใบคนอื่น mask `฿ •••••`, export/PDF ก็ mask · scope self/all · **เจ้าหน้าที่ HR/Finance เห็นทุกใบ+unmask แต่ approver:false** | Policy Center (Restricted Resources) · RBAC |
| BR-13 (SoD) | อนุมัติ/ตีกลับเฉพาะ role `approver:true` (re-check ที่ mutation) · กัน self-approve (ผู้เบิก approver:false) | RBAC/COSO |
| BR-10 (audit · no hard delete) | ทุก mutation → append-only log (≥7 ปี · immutable) · ยกเลิก = soft archive | Audit/Compliance (D9) |

---

## 5. Integration

- **Depends on:**
  - F011 Employee — `GET /employees` (combobox ผู้เบิก/ผู้อนุมัติ)
  - F-HR-MOVE Movement — `resolve(as_of=วันเบิก)` ตำแหน่ง/cost_center snapshot
  - F164 HR Config #107 — หมวด/เพดาน (read · group mock · A-EXP-04)
  - F-DLG-001 DOA (Policy Center) — resolve สายตามวงเงิน (Engine · **dep CL-0013 ผู้บริหาร แขวน 31 ส.ค.**)
  - F103 Advance — `GET /advances/outstanding` (read · display-only)
  - Engines: ENG-NOTIFY · ENG-DOC-NUM · ENG-DOC-STORE
- **Depended by (downstream · จาก BRD §12.1 + Central Plan edges):**
  - 7C/CSQ — FC + EC ตอนอนุมัติครบ (ไม่มี AC)
  - Payroll/Finance/F091/F109 — สั่งจ่าย (hook display-only) · F101 อ่าน paid กลับ (edge F101→F109/F091 flow)
  - F103 เงินทดรอง — ค่าหักลบ offset (edge F103→F101 flow "เคลียร์เงินทดรอง")
  - F117 Budget Control — ตรวจงบก่อนอนุมัติ (ctl · display-only mock · W7 ยังไม่ dev)
  - F102 Welfare — สิทธิ์สวัสดิการกำกับวงเงิน (edge F102→F101 ctl · display-only mock)
  - F059 ESS — พนักงานยื่นเบิกเอง (edge F059→F101 flow)
- **Declarations (Central Plan dec chip: doa · ntf · csq · doccfg · pdfdoc):**
  - **DOA** — yes · scope `document_sign` · 1 action `expense_claim` **มีวงเงิน** (FREE multi-range · chainMode sequential) · proposed key `DOA-EXP-CLAIM-001` `[DEFAULT — รอยืนยัน]` · role-id ทั้งหมด `[DEFAULT — รอยืนยัน]` (DOA master ไม่มีในการติดตั้ง · **CL-0013 แขวน · OQ-01**)
  - **NTF** — 5 events (`exp.submitted` · `exp.overcap` · `exp.approved` · `exp.rejected` · `exp.paid`) · เสนอกลุ่มใหม่ "ค่าใช้จ่าย (HR)" (ยังไม่มีใน registry กลาง Sales/DOA-only · OQ-NTF-01)
  - **DOCCFG** — doc_type `EXP` "ใบเบิกค่าใช้จ่าย" · format `EXP-<พ.ศ.>-NNNN` (preset `{PREFIX}-{BBBB}-{run:4}` · pad 4 · reset รายปี · no-gap · snap `approved_final`) · ⚠ module `HR` ยังไม่มีใน registry (OQ-DOCCFG-05) · scope global vs branch DIVERGENCE (OQ-DOCCFG-04)
  - **CSQ** — 7C FC/EC emit contract (ผ่าน BA input brief · อ้างใน FRD/NTF ว่าอยู่ใน CSQ_BRIEF — *ไฟล์ CSQ_BRIEF ไม่มีใน pack นี้* `[not documented]`; ตัว declaration ที่รันจริง = doccfg+doa+ntf)
  - **PDFDOC** — สำเนา PDF a4 snapshot (immutable · ENG-DOC-STORE · FN-23)
- **Engine hooks:** ENG-DOC-NUM (FN-11 issueDocNumber) · ENG-DOC-STORE (FN-23 snapshotPdf) · ENG-EXP-01 (VAT/totals · calcLineVat · FN-03/04) · ENG-EXP-02 (advance-offset · computeAdvanceOffset · FN-16) · ENG-NOTIFY (5 exp.* events) · DOA engine (F-DLG-001)

---
*trace: §2 ← FRD 04_DB · §3 ← FRD 02_API · §4 ← FRD 05_RULES · §5 ← BRD §12.1 / DOA·NTF·DOCCFG briefs / Central Plan row F101*
