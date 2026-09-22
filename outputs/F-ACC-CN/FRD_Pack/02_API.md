# 02_API — F-ACC-CN ใบลดหนี้ลูกค้า (Credit Note)

> **Audience:** Backend developer (HTTP layer)
> **Purpose:** API contracts — CUBIC API Entity format (HTTP layer only)
> **🚨 Iron Rule:** ห้าม business logic >5 บรรทัดที่นี่ — ย้ายไป 03_LOGIC §3.1/§3.2
> **🚨 R8:** ทุก mutation API ต้องระบุ "Calls (Logic)" → trace ใน 03_LOGIC §3.3
> **Convention:** เลข CN, DOA resolve, VAT calc, JE, notification, PDF store = เรียก engine กลาง — **ห้าม feature generate เอง**

---

## §2.1 API Overview

| ID | Method | Path | Summary | Auth (role) |
|---|---|---|---|---|
| F-ACC-CN-API-01 | GET | /api/v1/credit-notes | List + filter + sort | any (view scope) |
| F-ACC-CN-API-02 | GET | /api/v1/credit-notes/:id | Get detail (+chain/audit) | any |
| F-ACC-CN-API-03 | POST | /api/v1/credit-notes | Create draft | officer-ar |
| F-ACC-CN-API-04 | PUT | /api/v1/credit-notes/:id | Update draft | officer-ar (owner) |
| F-ACC-CN-API-05 | POST | /api/v1/credit-notes/:id/submit | Submit (draft→pending, freeze DOA) | officer-ar (owner) |
| F-ACC-CN-API-06 | POST | /api/v1/credit-notes/:id/approve | Approve step (last→issue CN) | approver (current step) |
| F-ACC-CN-API-07 | POST | /api/v1/credit-notes/:id/reject | Reject (pending→draft + history) | approver (current step) |
| F-ACC-CN-API-08 | POST | /api/v1/credit-notes/:id/cancel | Cancel (draft/pending→cancelled) | officer-ar (owner) |
| F-ACC-CN-API-09 | POST | /api/v1/credit-notes/:id/send | Send to customer (approved→sent · resend) | officer-ar |
| F-ACC-CN-API-10 | GET | /api/v1/credit-notes/export | CSV export | any (view scope) |
| F-ACC-CN-API-11 | GET | /api/v1/ar-invoices/open | Open-item picker (outstanding>0) | officer-ar |
| F-ACC-CN-API-12 | GET | /api/v1/sales-returns?invoice=:no | SR picker (mock F090) | officer-ar |
| F-ACC-CN-API-13 | GET | /api/v1/credit-notes/:id/pdf | Render/fetch PDF copy (ENG-DOC-STORE) | any |
| F-ACC-CN-API-14 | POST | /api/v1/credit-notes/:id/revise-doc | Mark "ออกเอกสารแก้ไข" (display-only) | officer-ar |
| F-ACC-CN-API-15 | GET | /api/v1/config/cn-reasons | Reason master (config) | any |

---

## §2.2 Per-API Contract (key mutations)

### F-ACC-CN-API-01: GET /api/v1/credit-notes
**auth:** required · **roles:** all (view scope = company/branch)
**Query:** `status` (all|draft|pending_approval|approved|sent|cancelled) · `reason` (all|RET|DISC|PRICE|QTY) · `customer` (partner code) · `stat` (pending|month|draft|vat) · `q` (search: code/customer/inv/sr/reasonText/item) · `sort` (code|date|total) · `limit`/`offset`
**Response 200:** `{ data:[{ id, code, cn_date, customer_code, customer_name, ref_invoice, reason, status, approval_progress, grand_total, net_vat }], total, stats:{pending,month,draft,vat} }`
**Side effects:** — (read-only) · **Calls (Logic):** F-ACC-CN-FN-01 buildCnListQuery

---

### F-ACC-CN-API-03: POST /api/v1/credit-notes  (create draft)
**roles:** officer-ar · **Headers:** `X-Tenant-Id`, `Idempotency-Key`
**Body:**
```json
{
  "ref_invoice": "INV-2026-0140",
  "cn_date": "2026-09-20",
  "reason": "RET",
  "sales_return_ref": "SR-2026-0016",
  "reason_text": "รับคืนไส้กรอง 2 กล่อง ...",
  "sales_rep": "…",
  "bill_to": "…",
  "note": "",
  "lines": [ { "src_line": "INV-2026-0140|0", "qty": 2, "unit_price": 5040, "vat_mode": "add", "vat_pct": 7 } ],
  "endbill": { "enabled": false, "mode": "percent", "value": 0 },
  "attachments": []
}
```
**Validation (field-level ≤5 บรรทัด):** ref_invoice required · cn_date required · reason ∈ master. **Complex → 03_LOGIC FN-05 validateCreditNote** (reason_text≥10, RET→needSR, line qty≤room, price≤orig, net≤netLeft, endbill≤cap, grand≤available).
**Response 201:** `{ id, status:"draft", code:null, grand_total, net_before, net_vat }`
**Errors:** 400 ERR_VALIDATION_FAILED · 403 ERR_INSUFFICIENT_ROLE · 409 ERR_DUPLICATE_IDEMPOTENCY_KEY · 422 BR_CN_EXCEEDS_OUTSTANDING / BR_LINE_QTY_EXCEEDED / BR_ENDBILL_EXCEEDS_CAP / BR_REASON_TEXT_TOO_SHORT / BR_RET_NEEDS_SR
**Preconditions:** invoice issued/sent & outstanding>0 (BR-01) · reason exists
**Side effects:** INSERT T_credit_note (status draft, code null) + T_credit_note_line + T_cn_attachment + T_cn_audit ("สร้างใบลดหนี้ อ้าง {inv}")
**Calls (Logic):** FN-02 createCreditNoteDraft, FN-04 buildLinesFromInvoice, FN-05 validateCreditNote · ENG cn-totals-engine, ENG ar-open-item-resolver

> **NOTE:** draft ที่ยอดเกิน available **บันทึกได้** (blockReason อนุญาต save ร่าง) แต่ **ส่งอนุมัติไม่ได้** (submitGuard block). ยึดตาม HTML.

---

### F-ACC-CN-API-04: PUT /api/v1/credit-notes/:id  (update draft)
**roles:** officer-ar (owner) · **Headers:** `If-Match` (version — optimistic lock PR-2)
**Precondition:** `status === 'draft'` (มิฉะนั้น 422 BR_EDIT_DRAFT_ONLY → toast "แก้ไขได้เฉพาะฉบับร่าง")
**Body:** เหมือน API-03 · **Response 200:** updated · **Errors:** +409 ERR_STALE_DATA
**Side effects:** UPDATE T_credit_note/_line + T_cn_audit · **Calls:** FN-03 updateCreditNoteDraft, FN-04, FN-05 · ENG cn-totals, ENG ar-open-item

---

### F-ACC-CN-API-05: POST /api/v1/credit-notes/:id/submit  (draft → pending_approval)
**roles:** officer-ar (owner)
**Body:** `{ "slots": [ { "step": 1, "assignee_id": "emp-…" }, ... ] }` (คนต่อขั้นตาม resolveDoa)
**Precondition (submitGuard):** status=draft · !ebOver · grand ≤ available(outstanding−held) · reason_text≥10 · ทุก slot มี assignee
**Response 200:** `{ status:"pending_approval", doa_entry_ref:"DOA-ACC-CN", tier, approval_chain:[…snapshot…] }`
**Errors:** 422 BR_SUBMIT_DRAFT_ONLY / BR_CN_EXCEEDS_OUTSTANDING / BR_ENDBILL_EXCEEDS_CAP / BR_SLOT_INCOMPLETE
**Side effects:** UPDATE status + `approval_chain` (jsonb snapshot, freeze) + `doa_entry_ref` + `submitted_by/at` · T_cn_audit · emit DOA `doa_pending` (DOA engine) — feature **ไม่** ยิงเอง
**Calls (Logic):** FN-06 submitForApproval · **ENG-DOA (external)** resolveDoa+freeze (tier = totals.grand หลัง end-bill — LD-05)

---

### F-ACC-CN-API-06: POST /api/v1/credit-notes/:id/approve  (approve step)
**roles:** approver = ผู้มีสิทธิ์ขั้นปัจจุบัน (assignee หรือ role ตรง) · **SoD:** submitted_by ≠ actor (BR-07)
**Body:** `{ "note": "" }`
**Precondition:** canActStep · **ถ้าขั้นสุดท้าย (approveGuard):** grand ≤ outstanding re-check (FN-17) — ไม่พอ → block "อนุมัติไม่ได้ — ยอดคงค้าง {inv} เหลือ ฿X น้อยกว่ายอดลดหนี้ ... ให้ไม่อนุมัติกลับไปแก้"
**Response 200:** non-last → `{ status:"pending_approval", current_step:n+1 }` · last → `{ status:"approved", code:"CN-2026-0024", cn_applied, net_vat, je:[…] }`
**Errors:** 403 ERR_NOT_CURRENT_APPROVER · 422 BR_APPROVE_EXCEEDS_OUTSTANDING
**Side effects (last step → issueCreditNote):** `code = ENG-DOC-NUM.next('CN')` · status=approved · UPDATE ar_open_item.cn_applied (F094) · output_vat_line negative = netVat เดือน cnDate (F105) · JE mock (F093) · **emit CSQ `ar_cn.approved`→AC(+EC)** · **NTF `ar_cn_approved_applied`** · T_cn_audit (append)
**Calls (Logic):** FN-07 approveStep → (last) FN-11 issueCreditNote · ENG-DOC-NUM, ENG-CSQ, ENG-NOTIFY (external)

---

### F-ACC-CN-API-07: POST /api/v1/credit-notes/:id/reject  (pending → draft)
**roles:** approver (current step) · **Body:** `{ "reason": "…" }` (required)
**Response 200:** `{ status:"draft", rejected_rounds:n }`
**Side effects:** append `approval_history[]` (snapshot chain + result:rejected, **append-only**) · status=draft · clear chain/submitted_by · T_cn_audit · badge "ถูกตีกลับ N ครั้ง" · **Calls:** FN-08 rejectToDraft

### F-ACC-CN-API-08: POST /api/v1/credit-notes/:id/cancel  (draft/pending → cancelled)
**roles:** officer-ar (owner) · **Body:** `{ "reason":"…" }` (required)
**Precondition:** status ∈ {draft, pending_approval} (มิฉะนั้น "ใบลดหนี้ที่ออกเลขแล้วยกเลิกไม่ได้ — ใช้ \"ออกเอกสารแก้ไข\"")
**Side effects:** status=cancelled · pending chain steps→cancelled · `cancel_info{by,at,reason}` · **คืนยอด held** (available เพิ่มกลับ) · T_cn_audit · NTF `ar_cn_cancelled` · **Calls:** FN-09 cancelCreditNote

### F-ACC-CN-API-09: POST /api/v1/credit-notes/:id/send  (approved → sent · resend)
**roles:** officer-ar · **Precondition:** status ∈ {approved, sent}
**Behavior:** approved→sent (`sent_at/by`, เก็บสำเนา PDF ผ่าน ENG-DOC-STORE) · sent→**resend** (ไม่เปลี่ยนสถานะ/วันที่ส่งเดิม · audit "ส่งสำเนาซ้ำ") · NTF `ar_cn_sent` · **Calls:** FN-10 sendToCustomer

### F-ACC-CN-API-14: POST /api/v1/credit-notes/:id/revise-doc  (display-only)
**roles:** officer-ar · **Behavior (OQ-CN-02):** ทำเครื่องหมายรอเอกสารทดแทน — **ไม่เปลี่ยนสถานะ · ไม่ถอนยอด · ไม่ลบใบ** · T_cn_audit "ขอออกเอกสารแก้ไข" · **Calls:** FN-13 markReviseDoc

### F-ACC-CN-API-11: GET /api/v1/ar-invoices/open  (upstream contract F094)
**Response:** `[{ no, customer, date, inv_grand, paid, cn_applied, outstanding }]` — เฉพาะ **issued/sent ที่ outstanding>0** (void/ชำระครบ excluded, BR-01) · **[ASSUMED contract F094]** · **Calls:** ENG ar-open-item-resolver

### F-ACC-CN-API-13: GET /api/v1/credit-notes/:id/pdf
**Response:** PDF (A4 ตาม CN_print-spec — ม.86/10) · เก็บสำเนา ENG-DOC-STORE ตอน approved_final + sent_external · **Calls:** FN-15 formatCreditNotePdf

---

## §2.3 Common Concerns
- **Idempotency (PR-7):** ทุก mutation รับ `Idempotency-Key` (cache 24h · same key+body → cached · diff body → 409). `[AI-DEFAULT]` OQ ยืนยัน scope.
- **Optimistic Locking (PR-2):** PUT/approve/reject ใช้ `If-Match: version` → mismatch 409 ERR_STALE_DATA (คุม concurrent approval EC-CC-01).
- **Multi-Tenant:** ทุก endpoint `X-Tenant-Id` → RLS (scope company).
- **Audit:** ทุก mutation → T_cn_audit append-only (actor/action/at/note · diff) — no hard delete (BR-13).
- **Re-entrancy (FIX-08):** commit action กัน double-submit (busyGate) — dev = idempotency key + version.

---

## §2.4 API → Logic Trace (Anchor for R8 · authoritative = 03_LOGIC §3.3)

| API | Calls Functions | Calls Engines |
|---|---|---|
| API-01 GET list | FN-01 | — |
| API-02 GET detail | FN-14 (room/outstanding for display) | ENG ar-open-item |
| API-03 POST create | FN-02, FN-04, FN-05 | ENG cn-totals, ENG ar-open-item |
| API-04 PUT update | FN-03, FN-04, FN-05 | ENG cn-totals, ENG ar-open-item |
| API-05 POST submit | FN-06 | ENG-DOA (ext) |
| API-06 POST approve | FN-07, FN-11 (last) | ENG-DOC-NUM, ENG-CSQ, ENG-NOTIFY (ext) |
| API-07 POST reject | FN-08 | — |
| API-08 POST cancel | FN-09 | ENG ar-open-item (release held) |
| API-09 POST send | FN-10 | ENG-DOC-STORE, ENG-NOTIFY (ext) |
| API-10 GET export | FN-12 | — |
| API-13 GET pdf | FN-15 | ENG-DOC-STORE (ext) |
| API-14 POST revise-doc | FN-13 | — |

> **R8 Check:** ทุก mutation row มี ≥1 Function. ✅

---

## §2.X Cross-Module Contract ⭐ (จาก BRD §12.1 Downstream Impact Map — R12)

| Downstream | รูปแบบ | Contract | Trigger | Payload หลัก | Compensating |
|---|---|---|---|---|---|
| AR Invoice / ar_open_item (F094) | Endpoint + write | `cn_applied += grand` → outstanding ลด | approve last (approved/sent) | { inv_no, cn_id, grand } | cancel ก่อนอนุมัติ = คืน held · หลังอนุมัติยกเลิกไม่ได้ → revise-doc (API-14) |
| VAT Report ภ.พ.30 (F105) | Event/contract | `output_vat_line` (negative) = netVat · month = cnDate | approve last | { cn_no, month, net_before, net_vat } | ม.82/10 · forward-wire |
| Journal Entry (F093) | Event (mock) | Dr 4110/4120 = netBefore · Dr 2150 = netVat · Cr 1130 = grand | approve last | { cn_id, entries[] } | mock [ASSUMED] |
| Receipt/Payment RV/PV (W6) | Read | อ่าน outstanding หลังลด | — | — | refund ชำระครบ = นอก scope (OQ-CN-03) |
| Sales Return (F090) | Read (mock) | SR ของใบเดียวกัน + จำนวนคืน | reason=RET | { sr_no, lines[] } | mock [ASSUMED] |

> ทุกแถวมี test ใน 06_TESTS §6.9 (XT-01..05).
