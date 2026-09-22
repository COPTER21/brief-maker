# 03_LOGIC — F-ACC-CN ใบลดหนี้ลูกค้า (Credit Note)

> **Audience:** BE dev (business logic layer)
> **Scope:** non-HTTP logic — functions, calculations, state transitions, validations, integrations
> **CUBIC:** §3.1 Functions = scope-local · §3.2 Engines = CUBIC Registry candidate
> **Iron Rule R8:** ทุก mutation API → ≥1 Function/Engine ใน §3.3
> **HTML anchor:** logic ทั้งหมด derive จากจอจริง (`totals`, `resolveDoa`, `lineRoom`, `invOutstanding`, `confirm*` handlers) — dev ต้องได้พฤติกรรมเดียวกัน

---

## §3.1 Functions (Scope-Local · camelCase)

### F-ACC-CN-FN-01: `buildCnListQuery`
- **Purpose:** สร้าง query/filter/sort + stats 4 tile สำหรับหน้ารายการ (FN-90)
- **Input:** `{ status, reason, customer, stat, q, sort, limit, offset }`
- **Output:** `{ rows: CreditNote[], total, stats:{pending,month,draft,vat} }`
- **Invoked by:** API-01 · **Calls:** ENG cn-totals (grand/netVat per row for stats/sort)
- **Side effects:** — (read) · **Iron check:** ✅ no HTTP terms

### F-ACC-CN-FN-02: `createCreditNoteDraft`
- **Purpose:** สร้างร่างใบลดหนี้จาก payload (buildRecord) — status draft, code null (ออกเลขตอนอนุมัติ) (FN-01/03/05/10)
- **Input:** `{ ref_invoice, cn_date, reason, sales_return_ref, reason_text, sales_rep, bill_to, note, lines[], endbill, attachments[] }`
- **Output:** `CreditNote | ValidationError[]`
- **Invoked by:** API-03 · **Calls:** FN-04 buildLinesFromInvoice, FN-05 validateCreditNote, ENG cn-totals, ENG ar-open-item
- **Side effects:** INSERT T_credit_note (+_line +_attachment) · T_cn_audit "สร้างใบลดหนี้ อ้าง {inv}"
- **Error cases:** BR_VALIDATION_* (ดู 05_RULES) · **Iron check:** ✅

### F-ACC-CN-FN-03: `updateCreditNoteDraft`
- **Purpose:** แก้ร่าง (prefillEdit → recompute per-line `max` จาก lineRoom + SR cap) (FN-06/07/08)
- **Input:** `{ id, …payload, version }` · **Output:** `CreditNote | ValidationError[]`
- **Invoked by:** API-04 · **Calls:** FN-04, FN-05, ENG cn-totals, ENG ar-open-item
- **Side effects:** UPDATE (draft only guard) + T_cn_audit · **Error:** BR_EDIT_DRAFT_ONLY, ERR_STALE_DATA · **Iron check:** ✅

### F-ACC-CN-FN-04: `buildLinesFromInvoice`
- **Purpose:** ล็อกบรรทัดจากใบเดิมตาม reason.mode — qty: qty=qtyLeft, price ล็อกราคาเดิม · price: qty ล็อก, unit_price=0 (ให้กรอกราคาที่ลด ≤ ราคาเดิม). ตั้ง `max` = qtyLeft (หรือ SR qty ถ้า RET) (FN-03/05/06/07)
- **Input:** `{ invoice_no, reason, sales_return_ref?, selected_line_idx[]? }`
- **Output:** `CreditNoteLine[]` (item locked, src_line, origQty, origPrice, max, _room)
- **Invoked by:** FN-02, FN-03 (pickInvoice/setReason/pickSR/readdLine) · **Calls:** FN-14 computeInvoiceRoom
- **Side effects:** — (in-memory build) · **Iron check:** ✅

### F-ACC-CN-FN-05: `validateCreditNote`
- **Purpose:** รวมศูนย์ validation (blockReason + submitGuard + step + line) — reused across create/update/submit (FN-06/07/09/10)
- **Input:** `CreditNoteDraft` · **Output:** `{ ok:boolean, block?:string, fieldErrors?:{} }`
- **Rules enforced:** reason_text ≥10 (BR-05) · RET→needSR (BR-06) · line qty ≤ (origQty−credited) (BR-03) · price mode ≤ origPrice (BR-04) · line net ≤ netLeft (BR-03) · endbill ≤ ebCap i.e. !ebOver (BR-11) · grand ≤ available at submit (BR-02) · cn_date ≥ inv_date
- **Invoked by:** FN-02, FN-03, FN-06 · **Calls:** ENG cn-totals (ebOver/grand), ENG ar-open-item (available)
- **Error cases:** BR_REASON_TEXT_TOO_SHORT, BR_RET_NEEDS_SR, BR_LINE_QTY_EXCEEDED, BR_PRICE_EXCEEDS_ORIG, BR_LINE_NET_EXCEEDED, BR_ENDBILL_EXCEEDS_CAP, BR_CN_EXCEEDS_OUTSTANDING · **Iron check:** ✅

### F-ACC-CN-FN-06: `submitForApproval`
- **Purpose:** draft→pending_approval — resolveDoa (tier by grand หลัง end-bill), bind คนต่อขั้น (slots), freeze `approval_chain` snapshot (FN-11)
- **Input:** `{ id, slots:[{step, assignee_id}] }` · **Output:** `{ status, doa_entry_ref, tier, approval_chain[] }`
- **Invoked by:** API-05 · **Calls:** FN-05 (submitGuard), **ENG-DOA (external)** resolveDoa
- **Side effects:** UPDATE status/chain/doa_entry_ref/submitted_by/at · T_cn_audit · emit DOA `doa_pending` (via DOA engine — **ไม่ยิงเอง**)
- **Error:** BR_SUBMIT_DRAFT_ONLY, BR_SLOT_INCOMPLETE, BR_CN_EXCEEDS_OUTSTANDING · **Iron check:** ✅

### F-ACC-CN-FN-07: `approveStep`
- **Purpose:** อนุมัติขั้นปัจจุบัน — SoD check (submitted_by≠actor) + canActStep. ถ้าขั้นสุดท้าย → approveGuard (re-check grand≤outstanding, FN-17) แล้วเรียก FN-11 (FN-12/14/17)
- **Input:** `{ id, actor, note }` · **Output:** `{ status, current_step | issued:{code,…} }`
- **Invoked by:** API-06 · **Calls:** FN-11 issueCreditNote (last step only), ENG ar-open-item (re-check)
- **Side effects:** UPDATE chain step (approved/by/at/note) · non-last: advance approver_role · T_cn_audit
- **Error:** ERR_NOT_CURRENT_APPROVER, BR_APPROVE_EXCEEDS_OUTSTANDING · **Iron check:** ✅

### F-ACC-CN-FN-08: `rejectToDraft`
- **Purpose:** ไม่อนุมัติ → pending→draft + append `approval_history` (snapshot, append-only) + clear chain/submitted_by (FN-13)
- **Input:** `{ id, actor, reason }` · **Output:** `{ status:"draft", rejected_rounds }`
- **Invoked by:** API-07 · **Side effects:** append approval_history · T_cn_audit · **Error:** ERR_NOT_CURRENT_APPROVER, BR_REASON_REQUIRED · **Iron check:** ✅

### F-ACC-CN-FN-09: `cancelCreditNote`
- **Purpose:** draft/pending→cancelled + คืนยอด held + cancel_info (FN-15)
- **Input:** `{ id, actor, reason }` · **Output:** `{ status:"cancelled" }`
- **Invoked by:** API-08 · **Calls:** ENG ar-open-item (held recompute)
- **Side effects:** status/cancel_info · pending chain→cancelled · T_cn_audit · NTF ar_cn_cancelled · **Error:** BR_CANCEL_STATE_INVALID, BR_REASON_REQUIRED · **Iron check:** ✅

### F-ACC-CN-FN-10: `sendToCustomer`
- **Purpose:** approved→sent (เก็บสำเนา PDF) · sent→resend (ไม่เปลี่ยนสถานะ) (FN-16)
- **Input:** `{ id, actor }` · **Output:** `{ status:"sent" | "resent" }`
- **Invoked by:** API-09 · **Calls:** ENG-DOC-STORE (PDF copy), ENG-NOTIFY (ar_cn_sent)
- **Side effects:** sent_at/by · T_cn_audit · **Error:** BR_SEND_STATE_INVALID · **Iron check:** ✅

### F-ACC-CN-FN-11: `issueCreditNote`  (called by FN-07 on final approve)
- **Purpose:** ออกเลข + ลงผลข้ามระบบเมื่ออนุมัติครบสาย (FN-12/18 · BR-08/09)
- **Input:** `CreditNote (approved chain complete)` · **Output:** `{ code, cn_applied, net_vat, je[] }`
- **Steps:** 1) `code = ENG-DOC-NUM.next('CN', ctx)` (CN-YYYY-NNNN no-gap — **ห้าม format เอง**) · 2) status=approved · 3) ar_open_item.cn_applied += grand (F094) · 4) output_vat_line negative = netVat, month=cnDate (F105) · 5) JE mock (F093): Dr 4110/4120 (RET/QTY vs DISC/PRICE)=netBefore, Dr 2150 ภาษีขาย=netVat, Cr 1130 ลูกหนี้=grand · 6) emit CSQ `ar_cn.approved`→AC(+EC ถ้า DISC/PRICE) · 7) NTF `ar_cn_approved_applied`
- **Calls:** ENG-DOC-NUM, ENG cn-totals, ENG-CSQ, ENG-NOTIFY (external) · **Side effects:** UPDATE + T_cn_audit (append) · **Iron check:** ✅

### F-ACC-CN-FN-12: `buildCsvExport`
- **Purpose:** CSV (cn_no,cn_date,customer,ref_invoice,reason,base,vat,grand_total,status) (FN-90)
- **Invoked by:** API-10 · **Calls:** ENG cn-totals · **Iron check:** ✅

### F-ACC-CN-FN-13: `markReviseDoc`
- **Purpose:** ทำเครื่องหมาย "ออกเอกสารแก้ไข" — **display-only** ไม่เปลี่ยนสถานะ/ยอด (OQ-CN-02)
- **Invoked by:** API-14 · **Side effects:** T_cn_audit "ขอออกเอกสารแก้ไข" เท่านั้น · **Iron check:** ✅

### F-ACC-CN-FN-14: `computeInvoiceRoom`
- **Purpose:** คำนวณเพดานต่อบรรทัด/ต่อใบ — origQty/origPrice/qtyLeft/netDone/netLeft + outstanding/available (FN-08)
- **Input:** `{ invoice_no, line_idx, exclude_cn_id }` · **Output:** `{ origQty, origPrice, origNet, qtyLeft, netDone, netLeft }`
- **Invoked by:** FN-04, API-02 display · **Calls:** ENG ar-open-item · **Iron check:** ✅

### F-ACC-CN-FN-15: `formatCreditNotePdf`
- **Purpose:** เตรียม pdfParts A4 (title/party/refHtml เลข+วันที่ใบเดิม+เดิม/ถูกต้อง/ผลต่าง/ภาษี/เหตุผล+legal_basis/signLabels) — ค.ศ. (FN-92 · pdfdoc CN_print-spec ม.86/10)
- **Invoked by:** API-13 · **Calls:** ENG cn-totals, ENG-DOC-STORE · **Iron check:** ✅

---

## §3.2 Engines (Reusable / CUBIC · kebab-case)

### ENG-cn-totals: `cn-totals-engine` [NEW]
| Field | Value |
|---|---|
| code | `cn-totals-engine` |
| name | Credit Note Totals & End-bill VAT Engine (FN-19 core — BR-11/BR-12) |
| category | financial-calculation |
| status | DRAFT (register CUBIC ตอน hand-off — LD-03) |
| owner | F-ACC-CN (candidate reuse: AR Invoice / DN) |

**Input:** `{ lines:[{qty, unit_price, discount_pct|amount, vat_mode(add|included|none), vat_pct}], endbill:{enabled, mode(amount|percent), value}, coupon? }`
**Output:** `{ before, vat, after, ebRaw, ebCap, ebOver, ebAmt, ebVat, ebBase, netBefore, netVat, grand }`
**Logic Outline (verbatim จาก HTML `calcLineVat`+`totals`):**
1. ต่อบรรทัด: subtotal = qty×price · discount (percent|amount, clamp ≤subtotal) · netAmount · vatAmount (add: net×pct% · included: net×pct/(1+pct) · none: 0)
2. รวม: `before` (VAT-inclusive → net−vat), `vat`, `after = before + vat`
3. **end-bill (BR-11/BR-12):** ebRaw = mode amount ? value : after×value% (≥0) · **ebCap = max(0, after − coupon)** (เพดาน — grand ไม่ติดลบ) · **ebOver = enabled && ebRaw > ebCap+0.005** (บล็อก submit) · ebAmt = min(ebRaw, ebCap)
4. **VAT recompute (ม.86/10):** `ebVat = after>0 ? ebAmt×(vat/after) : 0` (แบ่งตามสัดส่วน VAT — รองรับหลายอัตรา/VAT-inclusive) · `ebBase = ebAmt − ebVat` · **`netBefore = before − ebBase`** (ฐานภาษีหลังลด) · **`netVat = vat − ebVat`** (ภาษีขายที่ลดจริง → ภ.พ.30/JE/PDF)
5. **`grand = max(0, after − ebAmt − coupon)`** (ยอดลดหนี้สุทธิ = ฐานคิด DOA tier)
- ปัดเศษ money 2 ตำแหน่ง (`[AI-DEFAULT]` OQ-EB-01)
**Used by:** F-ACC-CN (this) · candidate: AR Invoice, Debit Note
**Iron check:** ✅ pure · ✅ reusable candidate · ✅ substantial (algorithm)

### ENG-ar-open-item: `ar-open-item-resolver` [NEW/shared candidate]
| Field | Value |
|---|---|
| code | `ar-open-item-resolver` |
| category | financial-calculation |
| status | DRAFT · owner F-ACC-CN (shared w/ AR family) |

**Input:** `{ invoice, exclude_cn_id }` (+ contract ar_open_item จาก F094)
**Output:** `{ inv_grand, paid, cn_applied, outstanding, cn_held, available, lineRoom(idx) }`
**Logic (จาก HTML):** `cn_applied` = Σ grand ของ CN [approved,sent] · `cn_held` = Σ grand ของ [draft,pending] · `outstanding = max(0, invGrand − paid − cn_applied)` · `available = max(0, outstanding − cn_held)` · `lineRoom` = origQty/netLeft ต่อบรรทัด (creditedOnLine ข้ามใบ, ยกเว้น cancelled)
**Used by:** F-ACC-CN (submit/approve guard, line cap) · AR family
**Iron check:** ✅ pure (ยกเว้นอ่าน contract) · ✅ reusable · ✅ substantial

### External Engines (reference — ไม่ build ใน feature นี้)
| Engine | ใช้ | หมายเหตุ |
|---|---|---|
| ENG-DOA (F-DLG-001) | resolveDoa + freeze snapshot (tier by grand หลัง end-bill) | entry `DOA-ACC-CN` sequential 3-tier · HTML `resolveDoa` = mock ตาม MOCK_DOA_ENTRY matrix (0-50k / 50k.01-300k / >300k) |
| ENG-DOC-NUM (F-DOCCFG) | `next('CN')` → CN-YYYY-NNNN no-gap ตอน final approve | ห้าม format เอง |
| ENG-DOC-STORE | เก็บสำเนา PDF (approved_final + sent_external) | |
| ENG-NOTIFY (F-NOTIFY) | ar_cn_approved_applied · ar_cn_sent · ar_cn_cancelled | doa_* ห้ามซ้ำ |
| ENG-CSQ (F-CSQ-01) | ar_cn.approved → AC (+EC ถ้า DISC/PRICE) | OC/DC/SC/FC/SecC ไม่ประกาศ |

---

## §3.3 API ↔ Logic Trace Table (R8 Anchor · Phase 3.5 Section C)

| API ID | Method | Path | Calls Functions | Calls Engines |
|---|---|---|---|---|
| API-01 | GET | /credit-notes | FN-01 | ENG cn-totals |
| API-02 | GET | /credit-notes/:id | FN-14 | ENG ar-open-item |
| API-03 | POST | /credit-notes | FN-02, FN-04, FN-05 | ENG cn-totals, ENG ar-open-item |
| API-04 | PUT | /credit-notes/:id | FN-03, FN-04, FN-05 | ENG cn-totals, ENG ar-open-item |
| API-05 | POST | /:id/submit | FN-06 (+FN-05) | ENG-DOA (ext) |
| API-06 | POST | /:id/approve | FN-07, FN-11 | ENG-DOC-NUM, ENG-CSQ, ENG-NOTIFY, ENG cn-totals, ENG ar-open-item |
| API-07 | POST | /:id/reject | FN-08 | — |
| API-08 | POST | /:id/cancel | FN-09 | ENG ar-open-item |
| API-09 | POST | /:id/send | FN-10 | ENG-DOC-STORE, ENG-NOTIFY |
| API-10 | GET | /credit-notes/export | FN-12 | ENG cn-totals |
| API-13 | GET | /:id/pdf | FN-15 | ENG cn-totals, ENG-DOC-STORE |
| API-14 | POST | /:id/revise-doc | FN-13 | — |

### Trace Verification (Self-Check)
- [x] ทุก mutation API มี ≥1 Function
- [x] ไม่มี orphan Function — FN-01..15 ปรากฏใน trace ครบ (FN-11 ผ่าน FN-07)
- [x] ไม่มี orphan Engine — cn-totals + ar-open-item ถูก trace; external engines ผ่าน FN
- [x] ไม่มี hidden logic ใน 02_API (calc/state/DOA อยู่ที่นี่ทั้งหมด)

---

## §3.5 Locked Decisions Referenced
- **LD-03:** ENG cn-totals + ar-open-item register CUBIC ตอน hand-off (scope-local ก่อน)
- **LD-05:** DOA tier คิดจาก `grand` (ยอดสุทธิหลัง end-bill) — resolveDoa ใช้ `totals(s).grand` (OQ-b RESOLVED)
- **LD-06:** เลข CN / PDF copy / VAT / DOA / NTF / CSQ = engine กลาง — feature declare เท่านั้น (ห้าม hardcode)
