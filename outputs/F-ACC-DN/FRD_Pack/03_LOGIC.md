# 03_LOGIC — F-ACC-DN ใบลดหนี้ผู้ขาย (Debit Note)

> **Audience:** BE dev (business logic layer)
> **Scope:** non-HTTP logic — functions, calculations, state transitions, validations, integrations
> **CUBIC:** §3.1 Functions = scope-local · §3.2 Engines = CUBIC Registry candidate
> **Iron Rule R8:** ทุก mutation API → ≥1 Function/Engine ใน §3.3
> **HTML anchor:** logic ทั้งหมด derive จากจอจริง (`totals`, `dnRoom`, `dnSplit`, `invOutstanding`, `resolveDoa`, `approveGuard`, `confirm*` handlers) — dev ต้องได้พฤติกรรมเดียวกัน

---

## §3.1 Functions (Scope-Local · camelCase)

### F-ACC-DN-FN-01: `buildDnListQuery`
- **Purpose:** สร้าง query/filter/sort + stats 4 tile สำหรับหน้ารายการ (FN-90)
- **Input:** `{ status, reason, partner, stat, q, sort, limit, offset }`
- **Output:** `{ rows: DebitNote[], total, stats:{pending,month,draft,vat} }`
- **Invoked by:** API-01 · **Calls:** ENG dn-totals (grand/netVat per row for stats/sort)
- **Side effects:** — (read) · **Iron check:** ✅ no HTTP terms

### F-ACC-DN-FN-02: `createDebitNoteDraft`
- **Purpose:** สร้างร่างใบลดหนี้ผู้ขายจาก payload (buildRecord) — status draft, code null (ออกเลขตอนอนุมัติ) (FN-01/03/05/10)
- **Input:** `{ inv, dn_date, reason, rtv, reason_text, sales_rep, bill_to, vendor_cn?, vendor_cn_date?, note, lines[], endbill, attachments[] }`
- **Output:** `DebitNote | ValidationError[]`
- **Invoked by:** API-03 · **Calls:** FN-04 buildLinesFromInvoice, FN-05 validateDebitNote, ENG dn-totals, ENG ap-open-item
- **Side effects:** INSERT T_debit_note (+_line +_attachment) · T_dn_audit "สร้างใบลดหนี้ผู้ขาย อ้าง {inv}"
- **Error cases:** BR_VALIDATION_* (ดู 05_RULES) · **Iron check:** ✅

### F-ACC-DN-FN-03: `updateDebitNoteDraft`
- **Purpose:** แก้ร่าง (prefillEdit → recompute per-line `max` จาก lineRoom + RTV cap) (FN-06/07/08)
- **Input:** `{ id, …payload, version }` · **Output:** `DebitNote | ValidationError[]`
- **Invoked by:** API-04 · **Calls:** FN-04, FN-05, ENG dn-totals, ENG ap-open-item
- **Side effects:** UPDATE (draft only guard) + T_dn_audit · **Error:** BR_EDIT_DRAFT_ONLY, ERR_STALE_DATA · **Iron check:** ✅

### F-ACC-DN-FN-04: `buildLinesFromInvoice`
- **Purpose:** ล็อกบรรทัดจากใบเดิมตาม reason.mode — qty: qty=qtyLeft, ล็อกราคาเดิม · price: qty ล็อก, unit_price=0 (ให้กรอกราคาที่ลด ≤ ราคาเดิม). ตั้ง `max` = qtyLeft (หรือ RTV qty ถ้า RTV) (FN-03/05/06/07)
- **Input:** `{ invoice_no, reason, rtv?, selected_line_idx[]? }`
- **Output:** `DebitNoteLine[]` (item locked, src_line, origQty, origPrice, max, _room)
- **Invoked by:** FN-02, FN-03 (`pickInv`/`setReason`/`pickRTV`/readdLine) · **Calls:** FN-14 computeInvoiceRoom
- **Side effects:** — (in-memory build) · **Iron check:** ✅

### F-ACC-DN-FN-05: `validateDebitNote`
- **Purpose:** รวมศูนย์ validation (blockReason + submitGuard + step + line) — reused across create/update/submit (FN-06/07/09/10)
- **Input:** `DebitNoteDraft` · **Output:** `{ ok:boolean, block?:string, fieldErrors?:{} }`
- **Rules enforced:** reason_text ≥10 (BR-05) · RTV→needRTV (BR-06) · line qty ≤ (origQty−credited) (BR-03) · price mode ≤ origPrice (BR-04) · line net ≤ netLeft (BR-03) · endbill ≤ ebCap i.e. !ebOver (BR-11) · grand ≤ **dnRoom** at submit (BR-02/BR-13 · `dnOver`) · dn_date ≥ vdate
- **Invoked by:** FN-02, FN-03, FN-06 · **Calls:** ENG dn-totals (ebOver/grand), ENG ap-open-item (dnRoom)
- **Error cases:** BR_REASON_TEXT_TOO_SHORT, BR_RTV_NEEDS_RTV, BR_LINE_QTY_EXCEEDED, BR_PRICE_EXCEEDS_ORIG, BR_LINE_NET_EXCEEDED, BR_ENDBILL_EXCEEDS_CAP, BR_DN_EXCEEDS_ROOM · **Iron check:** ✅

### F-ACC-DN-FN-06: `submitForApproval`
- **Purpose:** draft→pending_approval — resolveDoa (tier by grand หลัง end-bill), bind คนต่อขั้น (slots), freeze `approval_chain` snapshot (FN-11)
- **Input:** `{ id, slots:[{step, assignee_id}] }` · **Output:** `{ status, doa_entry_ref, tier, approval_chain[] }`
- **Invoked by:** API-05 · **Calls:** FN-05 (submitGuard), **ENG-DOA (external)** resolveDoa
- **Side effects:** UPDATE status/chain/doa_entry_ref/submitted_by/at · T_dn_audit · emit DOA `doa_pending` (via DOA engine — **ไม่ยิงเอง**)
- **Error:** BR_SUBMIT_DRAFT_ONLY, BR_SLOT_INCOMPLETE, BR_DN_EXCEEDS_ROOM · **Iron check:** ✅

### F-ACC-DN-FN-07: `approveStep`
- **Purpose:** อนุมัติขั้นปัจจุบัน — SoD check (submitted_by≠actor) + canActStep. ถ้าขั้นสุดท้าย → approveGuard (re-check grand≤dnRoom, FN-17) แล้วเรียก FN-11 (FN-12/14/17)
- **Input:** `{ id, actor, note }` · **Output:** `{ status, current_step | issued:{code,…} }`
- **Invoked by:** API-06 · **Calls:** FN-11 issueDebitNote (last step only), ENG ap-open-item (re-check)
- **Side effects:** UPDATE chain step (approved/by/at/note) · non-last: advance approver_role · toast "อนุมัติขั้น {n} แล้ว — ส่งต่อ {assignee}" · T_dn_audit
- **Error:** ERR_NOT_CURRENT_APPROVER, BR_APPROVE_EXCEEDS_ROOM · **Iron check:** ✅

### F-ACC-DN-FN-08: `rejectToDraft`
- **Purpose:** ไม่อนุมัติ → pending→draft + append `approval_history` (snapshot, append-only) + clear chain/submitted_by (FN-13)
- **Input:** `{ id, actor, reason }` · **Output:** `{ status:"draft", rejected_rounds }`
- **Invoked by:** API-07 · **Side effects:** append approval_history · T_dn_audit · **Error:** ERR_NOT_CURRENT_APPROVER, BR_REASON_REQUIRED · **Iron check:** ✅

### F-ACC-DN-FN-09: `cancelDebitNote`
- **Purpose:** draft/pending→cancelled + คืนยอด held + cancel_info (FN-15)
- **Input:** `{ id, actor, reason }` · **Output:** `{ status:"cancelled" }`
- **Invoked by:** API-08 · **Calls:** ENG ap-open-item (held recompute)
- **Side effects:** status/cancel_info · pending chain→cancelled · T_dn_audit · NTF dn.cancelled · **Error:** BR_CANCEL_STATE_INVALID, BR_REASON_REQUIRED · **Iron check:** ✅

### F-ACC-DN-FN-10: `sendToVendor`
- **Purpose:** approved→sent (เก็บสำเนา PDF) · sent→resend (ไม่เปลี่ยนสถานะ) (FN-16)
- **Input:** `{ id, actor }` · **Output:** `{ status:"sent" | "resent" }`
- **Invoked by:** API-09 · **Calls:** ENG-DOC-STORE (PDF copy), ENG-NOTIFY (dn.sent)
- **Side effects:** sent_at/by · audit `sent_external` · **Error:** BR_SEND_STATE_INVALID · **Iron check:** ✅

### F-ACC-DN-FN-11: `issueDebitNote`  (called by FN-07 on final approve)
- **Purpose:** ออกเลข + แยกยอด + ลงผลข้ามระบบเมื่ออนุมัติครบสาย (FN-12/18/20 · BR-08/09/13)
- **Input:** `DebitNote (approved chain complete)` · **Output:** `{ code, apply_to_ap, vendor_credit, net_vat, je[] }`
- **Steps (verbatim `onFinalApprove`):** 1) `code = ENG-DOC-NUM.next('DN', ctx)` (DN-YYYY-NNNN no-gap — **ห้าม format เอง**) · 2) status=approved · 3) `g = totals(s).grand` · **`sp = dnSplit(inv, g)`** → `apply_to_ap = sp.applyToAp` (min(g, outstanding)) · `vendor_credit = sp.vendorCredit` (max(0, g − applyToAp)) · 4) ap_open_item.dn_applied += applyToAp (F-ACC-APINV) · 5) JE mock (F093): Dr 2110 เจ้าหนี้ = applyToAp · Cr 5xxx รับคืน/ส่วนลด = netBefore · Cr 1150 ภาษีซื้อ = netVat · 6) **input_vat_line รอ vendorCn** (BR-14 — ยังไม่ลง ภ.พ.30) · 7) emit CSQ `dn.issued`→AC(+EC) · 8) NTF `dn.issued`
- **Audit (verbatim):** "ออกเลข {code} · ลดหนี้ {inv} ฿{g} (หักหนี้ค้าง ฿{applyToAp}[ · เครดิตคงเหลือกับผู้ขาย ฿{vendorCredit}]) · ภาษีซื้อ ฿{netVat} (กลับเมื่อได้รับใบลดหนี้ผู้ขาย) · บันทึกเข้า 7C ตาม CSQ_BRIEF_F097 (จำลอง)"
- **Calls:** ENG-DOC-NUM, ENG dn-totals, ENG ap-open-item (dnSplit), ENG-CSQ, ENG-NOTIFY (external) · **Side effects:** UPDATE + T_dn_audit (append) · **Iron check:** ✅

### F-ACC-DN-FN-12: `buildCsvExport`
- **Purpose:** CSV (dn_no,dn_date,partner,inv,reason,base,vat,apply_to_ap,vendor_credit,grand_total,status) → toast "ส่งออก CSV {n} รายการ" (FN-90 · §18.6)
- **Invoked by:** API-10 · **Calls:** ENG dn-totals · **Iron check:** ✅

### F-ACC-DN-FN-13: `markReviseDoc`  (⚠️ FORWARD — ไม่มีใน prototype v1)
- **สถานะ:** ไม่มีใน HTML prototype v1 — forward ภายใต้ **OQ-DN-04** (D-3) · FRD-internal fn เลข 13 (ไม่ผูก checklist FN-13=reject)
- **Purpose:** ทำเครื่องหมาย "ออกเอกสารแก้ไข" — **display-only** ไม่เปลี่ยนสถานะ/ยอด (OQ-DN-04)
- **Invoked by:** API-14 · **Side effects:** T_dn_audit "ขอออกเอกสารแก้ไข" · set revise_marked · **Iron check:** ✅

### F-ACC-DN-FN-14: `computeInvoiceRoom`  (dnRoom/lineRoom)
- **Purpose:** คำนวณเพดานต่อบรรทัด/ต่อใบ — origQty/origPrice/qtyLeft/netDone/netLeft + **dnRoom** (ไม่หัก paid) + outstanding (FN-04/08)
- **Input:** `{ invoice_no, line_idx, exclude_dn_id }` · **Output:** `{ origQty, origPrice, origNet, qtyLeft, netDone, netLeft, dnRoom, outstanding }`
- **Invoked by:** FN-04, API-02 display, `dnOver`, invList picker · **Calls:** ENG ap-open-item · **Iron check:** ✅

### F-ACC-DN-FN-15: `formatDebitNotePdf`
- **Purpose:** เตรียม pdfParts A4 (title/party ผู้ขาย/refHtml เลข+วันที่ใบกำกับเดิม+เดิม/ถูกต้อง/ผลต่าง/ภาษีซื้อ/เหตุผล+legal_basis/3 ช่องเซ็น) — ค.ศ. (FN-92 · pdfdoc DN_print-spec ม.86/10)
- **Invoked by:** API-13 · **Calls:** ENG dn-totals, ENG-DOC-STORE · **Iron check:** ✅

### F-ACC-DN-FN-16: `recordVendorCn` ⭐ (BR-14/FN-21)
- **Purpose:** บันทึกเลขที่+วันที่ใบลดหนี้จากผู้ขาย → เปิดการกลับภาษีซื้อ (input VAT) ในเดือน vendorCnDate (ม.82/10)
- **Input:** `{ id, vendor_cn, vendor_cn_date, actor }` · **Output:** `{ input_vat_applied:true, input_vat_month }`
- **Precondition:** status ∈ {approved, sent} · ก่อนบันทึก = "รอเอกสาร" (input_vat_line ยังไม่ลง)
- **Logic:** set vendor_cn/date/by/at · `input_vat_applied=true` · `input_vat_month = month(vendor_cn_date)` · emit `input_vat_line` (negative = netVat) เดือน input_vat_month
- **Invoked by:** API-16 · **Calls:** ENG-CSQ (`dn.vat_applied`→AC ภาษีซื้อ · OQ-DN-07)
- **Side effects:** UPDATE + T_dn_audit "บันทึกใบลดหนี้ผู้ขาย {vendor_cn} ({vendor_cn_date})" · **Edge CA-01:** vendorCn ซ้ำ/เดือนปิดงวด → flag OQ (warn) · **Iron check:** ✅

### F-ACC-DN-FN-17: `buildVendorCreditLedger` ⭐ (FN-20, display-only)
- **Purpose:** รวมเครดิตคงเหลือรายผู้ขาย (จาก DN approved/sent ที่ vendor_credit>0) สำหรับ KPI card + modal (P-01) + ref tab (P-04)
- **Input:** `{ partner? }` · **Output:** `[{ partner, vendor_name, credit_balance, dn_count, items[] }]`
- **Invoked by:** API-17, P-01 card, P-04 renderRefTab · **Calls:** ENG ap-open-item (dnSplit aggregate)
- **Side effects:** — (read-only) · **NOTE:** flow ใช้/ตัดยอด = OQ-DN-06 · **Iron check:** ✅

---

## §3.2 Engines (Reusable / CUBIC · kebab-case)

### ENG-dn-totals: `dn-totals-engine` [NEW]
| Field | Value |
|---|---|
| code | `dn-totals-engine` |
| name | Debit Note Totals & End-bill Input-VAT Engine (FN-19 core — BR-11/BR-12) |
| category | financial-calculation |
| status | DRAFT (register CUBIC ตอน hand-off — LD-03) |
| owner | F-ACC-DN (candidate reuse: AP Invoice / CN dn-totals kernel) |

**Input:** `{ lines:[{qty, unit_price, discount_pct|amount, vat_mode(add|included|none), vat_pct}], endbill:{enabled, mode(amount|percent), value}, couponAmt? }`
**Output:** `{ before, vat, after, ebRaw, ebCap, ebOver, ebAmt, ebVat, ebBase, netBefore, netVat, grand }`
**Logic Outline (verbatim จาก HTML `calcLineVat`+`totals`):**
1. ต่อบรรทัด: subtotal = qty×price · discount (percent|amount, clamp ≤subtotal) · netAmount · vatAmount (add: net×pct% · included: net×pct/(1+pct) · none: 0) · `before += included ? netAmount−vatAmount : netAmount`
2. รวม: `after = before + vat`
3. **end-bill (BR-11/BR-12):** ebRaw = mode amount ? value : after×value% (≥0) · **ebCap = max(0, after − couponAmt)** (เพดาน — grand ไม่ติดลบ) · **ebOver = enabled && ebRaw > ebCap+0.005** (บล็อก submit) · ebAmt = min(ebRaw, ebCap)
4. **input-VAT recompute (ม.86/10):** `ebVat = after>0 ? ebAmt×(vat/after) : 0` (แบ่งตามสัดส่วน VAT — รองรับหลายอัตรา/VAT-inclusive) · `ebBase = ebAmt − ebVat` · **`netBefore = before − ebBase`** (ฐานภาษีซื้อหลังลด) · **`netVat = vat − ebVat`** (ภาษีซื้อที่ลดจริง → ภ.พ.30/JE/PDF)
5. **`grand = max(0, after − ebAmt − couponAmt)`** (ยอดลดหนี้สุทธิ = ฐานคิด DOA tier)
- ปัดเศษ money 2 ตำแหน่ง (`[AI-DEFAULT]` OQ-EB-01)
- **หมายเหตุ:** `couponAmt` = dormant (ไม่มี UI ผูก) — คงไว้ตาม kernel, ไม่นับ scope creep
**Used by:** F-ACC-DN (this) · candidate: AP Invoice, CN (kernel เดียวกัน)
**Iron check:** ✅ pure · ✅ reusable candidate · ✅ substantial (algorithm)

### ENG-ap-open-item: `ap-open-item-resolver` [NEW/shared candidate]
| Field | Value |
|---|---|
| code | `ap-open-item-resolver` |
| category | financial-calculation |
| status | DRAFT · owner F-ACC-DN (shared w/ AP family) |

**Input:** `{ invoice, exclude_dn_id }` (+ contract ap_open_item จาก F-ACC-APINV)
**Output:** `{ inv_grand, paid, dn_applied, outstanding, dn_held, dnRoom, dnSplit(grand), lineRoom(idx) }`
**Logic (verbatim จาก HTML):**
- `dnApplied` = Σ applyToAp/grand ของ DN [approved,sent] · `dnHeld` = Σ grand ของ [draft,pending]
- **`invOutstanding = max(0, invGrand − paid − dnApplied)`** (ปัด 2 ตำแหน่ง)
- **`dnRoom = max(0, invGrand − dnApplied − dnHeld)`** — ⭐ **ไม่หัก paid** (BR-13 · เพดานการออก DN)
- **`dnSplit(grand)`** → `applyToAp = round(min(grand, outstanding))` · `vendorCredit = round(max(0, grand − applyToAp))` · `outstanding`
- `lineRoom` = origQty/netLeft ต่อบรรทัด (creditedOnLine ข้ามใบ, ยกเว้น cancelled)
**Used by:** F-ACC-DN (submit/approve guard `dnOver`, line cap, dnSplit, vendor credit) · AP family
**Iron check:** ✅ pure (ยกเว้นอ่าน contract) · ✅ reusable · ✅ substantial

### External Engines (reference — ไม่ build ใน feature นี้)
| Engine | ใช้ | หมายเหตุ |
|---|---|---|
| ENG-DOA (F-DLG-001) | resolveDoa + freeze snapshot (tier by grand หลัง end-bill) | entry `DOA-ACC-DN` sequential 3-tier · HTML `resolveDoa` = mock ตาม matrix (0-50k / 50k.01-300k / >300k [ASSUMED]) |
| ENG-DOC-NUM (F-DOCCFG) | `next('DN')` → DN-YYYY-NNNN no-gap ตอน final approve (`nextCode()` · `DOC.prefix='DN'`) | ห้าม format เอง |
| ENG-DOC-STORE | เก็บสำเนา PDF (approved_final + sent_external) | |
| ENG-NOTIFY (F-NOTIFY) | dn.issued · dn.sent · dn.cancelled | doa_* ห้ามซ้ำ |
| ENG-CSQ (F-CSQ-01) | dn.issued → AC (ลด AP + JE) (+EC) · dn.vat_applied → AC ภาษีซื้อ (เมื่อมี vendorCn) | OC/DC/SC/FC/SecC ไม่ประกาศ · event เดียว/แยก = OQ-DN-07 |

---

## §3.3 API ↔ Logic Trace Table (R8 Anchor · Phase 3.5 Section C)

| API ID | Method | Path | Calls Functions | Calls Engines |
|---|---|---|---|---|
| API-01 | GET | /debit-notes | FN-01 | ENG dn-totals |
| API-02 | GET | /debit-notes/:id | FN-14 | ENG ap-open-item |
| API-03 | POST | /debit-notes | FN-02, FN-04, FN-05 | ENG dn-totals, ENG ap-open-item |
| API-04 | PUT | /debit-notes/:id | FN-03, FN-04, FN-05 | ENG dn-totals, ENG ap-open-item |
| API-05 | POST | /:id/submit | FN-06 (+FN-05) | ENG-DOA (ext) |
| API-06 | POST | /:id/approve | FN-07, FN-11 | ENG-DOC-NUM, ENG-CSQ, ENG-NOTIFY, ENG dn-totals, ENG ap-open-item |
| API-07 | POST | /:id/reject | FN-08 | — |
| API-08 | POST | /:id/cancel | FN-09 | ENG ap-open-item |
| API-09 | POST | /:id/send | FN-10 | ENG-DOC-STORE, ENG-NOTIFY |
| API-10 | GET | /debit-notes/export | FN-12 | ENG dn-totals |
| API-13 | GET | /:id/pdf | FN-15 | ENG dn-totals, ENG-DOC-STORE |
| API-14 | POST | /:id/revise-doc | FN-13 | — |
| API-16 | POST | /:id/vendor-cn | FN-16 | ENG-CSQ |
| API-17 | GET | /vendor-credits | FN-17 | ENG ap-open-item |

### Trace Verification (Self-Check)
- [x] ทุก mutation API มี ≥1 Function
- [x] ไม่มี orphan Function — FN-01..17 ปรากฏใน trace ครบ (FN-11 ผ่าน FN-07)
- [x] ไม่มี orphan Engine — dn-totals + ap-open-item ถูก trace; external engines ผ่าน FN
- [x] ไม่มี hidden logic ใน 02_API (calc/state/DOA/dnSplit อยู่ที่นี่ทั้งหมด)

---

## §3.5 Locked Decisions Referenced
- **LD-03:** ENG dn-totals + ap-open-item register CUBIC ตอน hand-off (scope-local ก่อน)
- **LD-05:** DOA tier คิดจาก `grand` (ยอดสุทธิหลัง end-bill) — resolveDoa ใช้ `totals(s).grand`
- **LD-06:** เลข DN / PDF copy / input VAT / DOA / NTF / CSQ = engine กลาง — feature declare เท่านั้น (ห้าม hardcode)
- **LD-07:** dnRoom = เพดานการออก DN **ไม่หัก paid** (BR-13 · FIX-01) · dnSplit แยก applyToAp/vendorCredit
- **LD-08:** input VAT gated by vendorCn (BR-14 · FIX-02) — recordVendorCn เป็น mutation แยกหลัง approve
