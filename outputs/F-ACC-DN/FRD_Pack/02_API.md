# 02_API — F-ACC-DN ใบลดหนี้ผู้ขาย (Debit Note)

> **Audience:** Backend developer (HTTP layer)
> **Purpose:** API contracts — CUBIC API Entity format (HTTP layer only)
> **🚨 Iron Rule:** ห้าม business logic >5 บรรทัดที่นี่ — ย้ายไป 03_LOGIC §3.1/§3.2
> **🚨 R8:** ทุก mutation API ต้องระบุ "Calls (Logic)" → trace ใน 03_LOGIC §3.3
> **Convention:** เลข DN, DOA resolve, VAT calc, JE, notification, PDF store = เรียก engine กลาง — **ห้าม feature generate เอง**

---

## §2.1 API Overview

| ID | Method | Path | Summary | Auth (role) |
|---|---|---|---|---|
| F-ACC-DN-API-01 | GET | /api/v1/debit-notes | List + filter + sort | any (view scope) |
| F-ACC-DN-API-02 | GET | /api/v1/debit-notes/:id | Get detail (+chain/audit) | any |
| F-ACC-DN-API-03 | POST | /api/v1/debit-notes | Create draft | officer-ap |
| F-ACC-DN-API-04 | PUT | /api/v1/debit-notes/:id | Update draft | officer-ap (owner) |
| F-ACC-DN-API-05 | POST | /api/v1/debit-notes/:id/submit | Submit (draft→pending, freeze DOA) | officer-ap (owner) |
| F-ACC-DN-API-06 | POST | /api/v1/debit-notes/:id/approve | Approve step (last→issue DN) | approver (current step) |
| F-ACC-DN-API-07 | POST | /api/v1/debit-notes/:id/reject | Reject (pending→draft + history) | approver (current step) |
| F-ACC-DN-API-08 | POST | /api/v1/debit-notes/:id/cancel | Cancel (draft/pending→cancelled) | officer-ap (owner) |
| F-ACC-DN-API-09 | POST | /api/v1/debit-notes/:id/send | Send to vendor (approved→sent · resend) | officer-ap |
| F-ACC-DN-API-10 | GET | /api/v1/debit-notes/export | CSV export | any (view scope) |
| F-ACC-DN-API-11 | GET | /api/v1/ap-invoices/open | Open-item picker (dnRoom>0) | officer-ap |
| F-ACC-DN-API-12 | GET | /api/v1/rtv-returns?invoice=:no | RTV picker (mock W3-LITE) | officer-ap |
| F-ACC-DN-API-13 | GET | /api/v1/debit-notes/:id/pdf | Render/fetch PDF copy (ENG-DOC-STORE) | any |
| F-ACC-DN-API-14 | POST | /api/v1/debit-notes/:id/revise-doc | Mark "ออกเอกสารแก้ไข" (display-only) | officer-ap |
| F-ACC-DN-API-15 | GET | /api/v1/config/dn-reasons | Reason master (config) | any |
| **F-ACC-DN-API-16** ⭐ | POST | /api/v1/debit-notes/:id/vendor-cn | Record vendorCn → input-VAT reversal (BR-14) | officer-ap / mgr-acc |
| **F-ACC-DN-API-17** ⭐ | GET | /api/v1/vendor-credits | Vendor credit ledger (display-only, FN-20) | any (view scope) |

---

## §2.2 Per-API Contract (key mutations)

### F-ACC-DN-API-01: GET /api/v1/debit-notes
**auth:** required · **roles:** all (view scope = company/branch)
**Query:** `status` (all|draft|pending_approval|approved|sent|cancelled) · `reason` (all|RTV|OVERPRICE|SHORT) · `partner` (vendor code) · `stat` (pending|month|draft|vat) · `q` (search: code/partner/inv/rtv/vendorCn/vinv/reasonText/item) · `sort` (code|date|total) · `limit`/`offset`
**Response 200:** `{ data:[{ id, code, dn_date, partner, vendor_name, inv, reason, status, approval_progress, grand_total, net_vat, apply_to_ap, vendor_credit }], total, stats:{pending,month,draft,vat} }`
**Side effects:** — (read-only) · **Calls (Logic):** F-ACC-DN-FN-01 buildDnListQuery

---

### F-ACC-DN-API-03: POST /api/v1/debit-notes  (create draft)
**roles:** officer-ap · **Headers:** `X-Tenant-Id`, `Idempotency-Key`
**Body:**
```json
{
  "inv": "API-2026-0041",
  "dn_date": "2026-09-20",
  "reason": "RTV",
  "rtv": "RTV-2026-0007",
  "reason_text": "คืนไส้กรอง 2 กล่อง ...",
  "sales_rep": "…",
  "bill_to": "…",
  "vendor_cn": "",
  "vendor_cn_date": "",
  "note": "",
  "lines": [ { "src_line": "API-2026-0041|0", "qty": 2, "unit_price": 5040, "vat_mode": "add", "vat_pct": 7 } ],
  "endbill": { "enabled": false, "mode": "percent", "value": 0 },
  "attachments": []
}
```
**Validation (field-level ≤5 บรรทัด):** inv required · dn_date required · reason ∈ master. **Complex → 03_LOGIC FN-05 validateDebitNote** (reason_text≥10, RTV→needRTV, line qty≤room, price≤orig, net≤netLeft, endbill≤cap, grand≤dnRoom).
**Response 201:** `{ id, status:"draft", code:null, grand_total, net_before, net_vat }`
**Errors:** 400 ERR_VALIDATION_FAILED · 403 ERR_INSUFFICIENT_ROLE · 409 ERR_DUPLICATE_IDEMPOTENCY_KEY · 422 BR_DN_EXCEEDS_ROOM / BR_LINE_QTY_EXCEEDED / BR_ENDBILL_EXCEEDS_CAP / BR_REASON_TEXT_TOO_SHORT / BR_RTV_NEEDS_RTV
**Preconditions:** invoice approved/posted & dnRoom>0 (BR-01) · reason exists
**Side effects:** INSERT T_debit_note (status draft, code null) + T_debit_note_line + T_dn_attachment + T_dn_audit ("สร้างใบลดหนี้ผู้ขาย อ้าง {inv}")
**Calls (Logic):** FN-02 createDebitNoteDraft, FN-04 buildLinesFromInvoice, FN-05 validateDebitNote · ENG dn-totals-engine, ENG ap-open-item-resolver

> **NOTE:** draft ที่ยอดเกิน dnRoom **บันทึกได้** (blockReason อนุญาต save ร่าง: "ยอดลดหนี้เกินมูลค่าที่ลดได้ (บันทึกร่างได้)") แต่ **ส่งอนุมัติไม่ได้** (submitGuard block). ยึดตาม HTML.

---

### F-ACC-DN-API-04: PUT /api/v1/debit-notes/:id  (update draft)
**roles:** officer-ap (owner) · **Headers:** `If-Match` (version — optimistic lock PR-2)
**Precondition:** `status === 'draft'` (มิฉะนั้น 422 BR_EDIT_DRAFT_ONLY → toast "แก้ไขได้เฉพาะฉบับร่าง")
**Body:** เหมือน API-03 · **Response 200:** updated · **Errors:** +409 ERR_STALE_DATA
**Side effects:** UPDATE T_debit_note/_line + T_dn_audit · **Calls:** FN-03 updateDebitNoteDraft, FN-04, FN-05 · ENG dn-totals, ENG ap-open-item

---

### F-ACC-DN-API-05: POST /api/v1/debit-notes/:id/submit  (draft → pending_approval)
**roles:** officer-ap (owner)
**Body:** `{ "slots": [ { "step": 1, "assignee_id": "emp-…" }, ... ] }` (คนต่อขั้นตาม resolveDoa)
**Precondition (submitGuard):** status=draft · !ebOver · grand ≤ **dnRoom** · reason_text≥10 · ทุก slot มี assignee
**Response 200:** `{ status:"pending_approval", doa_entry_ref:"DOA-ACC-DN", tier, approval_chain:[…snapshot…] }`
**Errors:** 422 BR_SUBMIT_DRAFT_ONLY / BR_DN_EXCEEDS_ROOM / BR_ENDBILL_EXCEEDS_CAP / BR_SLOT_INCOMPLETE
**Side effects:** UPDATE status + `approval_chain` (jsonb snapshot, freeze) + `doa_entry_ref` + `submitted_by/at` · T_dn_audit · emit DOA `doa_pending` (DOA engine) — feature **ไม่** ยิงเอง
**Calls (Logic):** FN-06 submitForApproval · **ENG-DOA (external)** resolveDoa+freeze (tier = totals.grand หลัง end-bill — LD-05)

---

### F-ACC-DN-API-06: POST /api/v1/debit-notes/:id/approve  (approve step)
**roles:** approver = ผู้มีสิทธิ์ขั้นปัจจุบัน (assignee หรือ role ตรง) · **SoD:** submitted_by ≠ actor (BR-07)
**Body:** `{ "note": "" }`
**Precondition:** canActStep · **ถ้าขั้นสุดท้าย (approveGuard):** grand ≤ **dnRoom** re-check (FN-17) — ไม่พอ → block "อนุมัติไม่ได้ — มูลค่าที่ลดได้ของ {inv} เหลือ ฿Y น้อยกว่ายอดลดหนี้ (มีใบลดหนี้อื่นได้รับอนุมัติเพิ่มระหว่างรออนุมัติ) · ให้ไม่อนุมัติกลับไปแก้"
**Response 200:** non-last → `{ status:"pending_approval", current_step:n+1 }` · last → `{ status:"approved", code:"DN-2026-0012", apply_to_ap, vendor_credit, net_vat, je:[…] }`
**Errors:** 403 ERR_NOT_CURRENT_APPROVER · 422 BR_APPROVE_EXCEEDS_ROOM
**Side effects (last step → issueDebitNote):** `code = ENG-DOC-NUM.next('DN')` · status=approved · **dnSplit:** `apply_to_ap = min(grand, outstanding)` · `vendor_credit = max(0, grand − applyToAp)` · UPDATE ap_open_item.dn_applied += applyToAp (F-ACC-APINV) · JE mock (F093) · **input_vat_line รอ vendorCn** (ยังไม่ลง ภ.พ.30 — BR-14) · **emit CSQ `dn.issued`→AC(+EC)** · **NTF `dn.issued`** · T_dn_audit (append)
**Calls (Logic):** FN-07 approveStep → (last) FN-11 issueDebitNote · ENG-DOC-NUM, ENG-CSQ, ENG-NOTIFY, ENG ap-open-item (dnSplit) (external + feature)

---

### F-ACC-DN-API-07: POST /api/v1/debit-notes/:id/reject  (pending → draft)
**roles:** approver (current step) · **Body:** `{ "reason": "…" }` (required)
**Response 200:** `{ status:"draft", rejected_rounds:n }`
**Side effects:** append `approval_history[]` (snapshot chain + result:rejected, **append-only**) · status=draft · clear chain/submitted_by · T_dn_audit · badge "ถูกตีกลับ N ครั้ง" · **Calls:** FN-08 rejectToDraft

### F-ACC-DN-API-08: POST /api/v1/debit-notes/:id/cancel  (draft/pending → cancelled)
**roles:** officer-ap (owner) · **Body:** `{ "reason":"…" }` (required)
**Precondition:** status ∈ {draft, pending_approval} (double-guard `openCancelDN`) (มิฉะนั้น "ใบลดหนี้ที่ออกเลขแล้วยกเลิกไม่ได้ — ใช้ \"ออกเอกสารแก้ไข\"")
**Side effects:** status=cancelled · pending chain steps→cancelled · `cancel_info{by,at,reason}` · **คืนยอด held** (dnRoom เพิ่มกลับ) · T_dn_audit · NTF `dn.cancelled` · **Calls:** FN-09 cancelDebitNote

### F-ACC-DN-API-09: POST /api/v1/debit-notes/:id/send  (approved → sent · resend)
**roles:** officer-ap · **Precondition:** status ∈ {approved, sent}
**Behavior:** approved→sent (`sent_at/by`, เก็บสำเนา PDF ผ่าน ENG-DOC-STORE, audit `sent_external`) · sent→**resend** (ไม่เปลี่ยนสถานะ/วันที่ส่งเดิม · audit "ส่งสำเนาซ้ำ") · NTF `dn.sent` · **Calls:** FN-10 sendToVendor

### F-ACC-DN-API-16: POST /api/v1/debit-notes/:id/vendor-cn ⭐ (record vendorCn — BR-14/FN-21)
**roles:** officer-ap / mgr-acc · **Precondition:** status ∈ {approved, sent}
**Body:** `{ "vendor_cn": "TFS-6650", "vendor_cn_date": "2026-10-05" }`
**Behavior:** set vendor_cn + vendor_cn_date + vendor_cn_by/at · **input_vat_applied = true** · **input_vat_month = month(vendor_cn_date)** → `input_vat_line` (negative) ลง ภ.พ.30 เดือน vendorCnDate (ม.82/10) · ก่อนบันทึก = "รอเอกสาร" (ยังไม่ลด input VAT) · **[ASSUMED legal basis OQ-DN-05]** · T_dn_audit "บันทึกใบลดหนี้ผู้ขาย {vendor_cn} ({vendor_cn_date}) · กลับภาษีซื้อเดือน MM/YYYY"
**Errors:** 422 BR_VENDORCN_STATE_INVALID (ต้อง approved/sent) · CA-01 vendorCn ซ้ำ / เดือนภาษีปิดงวด → **ยก OQ** (flag warn, ไม่ block ในรอบนี้)
**Calls (Logic):** FN-16 recordVendorCn · ENG-CSQ (`dn.vat_applied`→AC ภาษีซื้อ · OQ-DN-07)

### F-ACC-DN-API-17: GET /api/v1/vendor-credits ⭐ (vendor credit ledger — FN-20, display-only)
**roles:** any (view scope) · **Query:** `partner?`
**Response:** `[{ partner, vendor_name, credit_balance, dn_count, items:[{ dn_code, dn_date, vendor_credit }] }]` (จาก V_vendor_credit_ledger — DN approved/sent ที่ vendor_credit>0)
**Side effects:** — (read-only) · **NOTE:** flow ใช้/ตัดยอด = OQ-DN-06 (นอก scope) · **Calls:** FN-17 buildVendorCreditLedger

### F-ACC-DN-API-14: POST /api/v1/debit-notes/:id/revise-doc  (⚠️ FORWARD — ไม่มีใน prototype v1)
**สถานะ:** **ไม่มีใน HTML prototype v1** (grep `revise`/`ออกเอกสารแก้ไข` = 0) — spec นี้ mirror มาจาก CN sibling (display-only) เป็น **forward ภายใต้ OQ-DN-04** · dev **อย่า implement จนกว่า BA เคาะ OQ-DN-04** (drift D-3)
**roles:** officer-ap · **Behavior (OQ-DN-04, ถ้าอนุมัติให้ทำ):** ทำเครื่องหมายรอเอกสารทดแทน — **ไม่เปลี่ยนสถานะ · ไม่ถอนยอด · ไม่ลบใบ** · T_dn_audit "ขอออกเอกสารแก้ไข" · **Calls:** FN-13 markReviseDoc (FRD-internal fn, ไม่ผูก checklist FN)

### F-ACC-DN-API-11: GET /api/v1/ap-invoices/open  (upstream contract F-ACC-APINV)
**Response:** `[{ no, vinv, vendor, date, inv_grand, paid, dn_applied, dn_held, outstanding, dn_room }]` — เฉพาะ **approved/posted ที่ dnRoom>0** (ใบที่ลดเต็มแล้ว excluded · **ใบจ่ายครบยังโผล่** ถ้า dnRoom>0, BR-01/BR-13) · **[ASSUMED contract]** · **Calls:** ENG ap-open-item-resolver

### F-ACC-DN-API-12: GET /api/v1/rtv-returns?invoice=:no  (mock W3-LITE)
**Response:** `[{ rtv_no, lines:[{ src_line, qty }] }]` — RTV ของใบเดียวกัน · **[ASSUMED contract mock]** · **Calls:** FN-04 (cap qty≤RTV)

### F-ACC-DN-API-13: GET /api/v1/debit-notes/:id/pdf
**Response:** PDF (A4 ตาม DN_print-spec — ม.86/10 ฝั่งซื้อ) · เก็บสำเนา ENG-DOC-STORE ตอน approved_final + sent_external · **Calls:** FN-15 formatDebitNotePdf

---

## §2.3 Common Concerns
- **Idempotency (PR-7):** ทุก mutation รับ `Idempotency-Key` (cache 24h · same key+body → cached · diff body → 409). `[AI-DEFAULT]` OQ ยืนยัน scope.
- **Optimistic Locking (PR-2):** PUT/approve/reject/vendor-cn ใช้ `If-Match: version` → mismatch 409 ERR_STALE_DATA (คุม concurrent approval EC-CC-01).
- **Multi-Tenant:** ทุก endpoint `X-Tenant-Id` → RLS (scope company).
- **Audit:** ทุก mutation → T_dn_audit append-only (actor/action/at/note · diff) — no hard delete (BR-15).
- **Re-entrancy:** commit action กัน double-submit (busyGate) — dev = idempotency key + version.

---

## §2.4 API → Logic Trace (Anchor for R8 · authoritative = 03_LOGIC §3.3)

| API | Calls Functions | Calls Engines |
|---|---|---|
| API-01 GET list | FN-01 | ENG dn-totals |
| API-02 GET detail | FN-14 (dnRoom/outstanding for display) | ENG ap-open-item |
| API-03 POST create | FN-02, FN-04, FN-05 | ENG dn-totals, ENG ap-open-item |
| API-04 PUT update | FN-03, FN-04, FN-05 | ENG dn-totals, ENG ap-open-item |
| API-05 POST submit | FN-06 | ENG-DOA (ext) |
| API-06 POST approve | FN-07, FN-11 (last) | ENG-DOC-NUM, ENG-CSQ, ENG-NOTIFY, ENG ap-open-item (dnSplit) |
| API-07 POST reject | FN-08 | — |
| API-08 POST cancel | FN-09 | ENG ap-open-item (release held) |
| API-09 POST send | FN-10 | ENG-DOC-STORE, ENG-NOTIFY (ext) |
| API-10 GET export | FN-12 | ENG dn-totals |
| API-13 GET pdf | FN-15 | ENG dn-totals, ENG-DOC-STORE |
| API-14 POST revise-doc | FN-13 | — |
| API-16 POST vendor-cn | FN-16 | ENG-CSQ (ext) |
| API-17 GET vendor-credits | FN-17 | — |

> **R8 Check:** ทุก mutation row มี ≥1 Function. ✅

---

## §2.X Cross-Module Contract ⭐ (จาก BRD §12.1 Downstream Impact Map — R12)

| Downstream | รูปแบบ | Contract | Trigger | Payload หลัก | Compensating |
|---|---|---|---|---|---|
| AP Invoice / ap_open_item (F-ACC-APINV) | Endpoint + write | `dn_applied += applyToAp` → outstanding ลด | approve last (approved/sent) | { inv_no, dn_id, apply_to_ap } | cancel ก่อนอนุมัติ = คืน held · หลังอนุมัติยกเลิกไม่ได้ → revise-doc (API-14) |
| Vendor Credit Ledger (F097) | write + read (view) | `vendor_credit = max(0, grand − applyToAp)` → เครดิตคงเหลือรายผู้ขาย | approve last (grand>outstanding) | { partner, dn_id, vendor_credit } | display-only · flow ใช้/ตัดยอด = OQ-DN-06 |
| VAT Report ภ.พ.30 | Event/contract | `input_vat_line` (negative) = netVat · month = **vendor_cn_date** | **record vendorCn (API-16)** | { dn_no, month, net_before, net_vat } | ไม่มี vendorCn = "รอเอกสาร" (ยังไม่ลง) · ม.82/10 · forward-wire |
| Journal Entry (F093) | Event (mock) | Dr 2110 เจ้าหนี้ = applyToAp · Cr 5xxx รับคืน/ส่วนลด = netBefore · Cr 1150 ภาษีซื้อ = netVat | approve last | { dn_id, entries[] } | mock [ASSUMED] |
| Payment PV (W6) | Read | อ่าน outstanding หลังลด | — | — | จ่ายครบคืนของ = vendorCredit (ไม่ refund · OQ-DN-03) |
| RTV คืนสินค้า (W3-LITE) | Read (mock) | RTV ของใบเดียวกัน + จำนวนคืน | reason=RTV | { rtv_no, lines[] } | mock [ASSUMED] |

> ทุกแถวมี test ใน 06_TESTS §6.9 (XT-01..07).
