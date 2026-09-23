# CTX — F-ACC-DN (F097): ใบลดหนี้ผู้ขาย (Debit Note)

> **derived from:** FRD_F-ACC-DN v1.0 (2026-09-23) · **generated:** 2026-09-23
> **module:** Accounting / Accounts Payable (AP) · Wave W5 Phase A (LITE) · dep=""
> **status:** active (FRD v1.0 = DRAFT, pending BA gate)
> ⚠ Derived artifact — source of truth คือ FRD Pack · ถ้า FRD revise ต้อง regen CTX (R9)
> **Mirror ของ F-ACC-CN (AR)** re-domain → **AP/ผู้ขาย**: ภาษีซื้อ (input VAT) ค่าลบ · prefix DN · RTV · JE F093 · ค.ศ.

---

## 1. Summary
ออก **ใบลดหนี้ผู้ขาย (Debit Note · ฝั่ง AP/ซื้อ)** ที่ **อ้างใบตั้งหนี้ AP เสมอ** (ห้าม "ลดลอย") — เจ้าหน้าที่เจ้าหนี้ (officer-ap) สร้าง/แก้ร่าง/ส่งอนุมัติ, ผู้อนุมัติ (ผจก.จัดซื้อ/ผจก.บัญชี/CFO) อนุมัติตามสาย DOA 3-tier ตามมูลค่า, แล้วส่งใบให้ผู้ขาย.
Trigger: มีใบตั้งหนี้ approved/posted ที่ **dnRoom>0** (คืนสินค้า RTV / ผู้ขายคิดราคาเกิน / ของขาด-ไม่ครบ).
ผลลัพธ์เมื่ออนุมัติครบสาย: ออกเลข `DN-YYYY-NNNN`, แยกยอด `dnSplit` (applyToAp หักหนี้ค้าง + vendorCredit ส่วนเกินคงค้าง), ลด outstanding ของใบเดิม (`dn_applied += applyToAp`), JE (mock F093), **กลับภาษีซื้อ (input VAT ค่าลบ)** — แต่ลง ภ.พ.30 เมื่อกรอก vendorCn ภายหลังเท่านั้น (ม.82/10).
รองรับ **ส่วนลดท้ายบิล (end-bill)** ที่ลดฐานภาษี → คำนวณ input VAT ใหม่ตามสัดส่วน (FN-19). ประวัติ append-only, ไม่มี hard delete.
Pattern Q document + B2 v2 line editor (LOCK-01). Security Preset **P4 Financial**.

## 2. Data Contract

### Entities
| Entity | PK | Key Fields (ที่ feature อื่น join/อ่าน) | หมายเหตุ |
|---|---|---|---|
| `T_debit_note` (header) | `id` (uuid) | `code`, `inv`(ref_ap_invoice), `vinv`(เลขใบกำกับเดิมผู้ขาย), `rtv`, `partner`(vendor_code), `dn_date`, `reason`, `status`, `endbill`(jsonb), `vendor_cn`/`vendor_cn_date`, `apply_to_ap`, `vendor_credit`, `input_vat_applied`/`input_vat_month`, `doa_entry_ref`, `approval_chain`(jsonb), `approval_history`(jsonb) | owner F-ACC-DN · RLS scope company · `code` NULL จนอนุมัติครบ · UNIQUE(tenant_id, code) WHERE code NOT NULL (no-gap) · CHECK (input_vat_applied=false OR vendor_cn NOT NULL) |
| `T_debit_note_line` | `id` (uuid) | `dn_id`(FK), `src_line` (soft-ref "INV\|idx"), `item_code`, `qty`, `unit_price`, `orig_qty`, `orig_price`, `vat_mode`, `vat_pct` | ล็อกสินค้าจากใบตั้งหนี้เดิม · CASCADE จาก header |
| `T_dn_attachment` | `id` (uuid) | `dn_id`(FK), `name`, `size`, `mime`, `url` | jpg/png/pdf ≤10MB `[AI-DEFAULT]` OQ-FU-01 |
| `T_dn_audit` | `id` (uuid) | `dn_id`(FK), `act`, `by`, `at`, `note` | **append-only — NO UPDATE / NO DELETE** (trigger · `pushAudit` unshift-only) · retention 7 ปี |
| `T_dn_reason_master` (config) | `code` | `name`, `mode`(qty\|price), `need_rtv`, `legal_basis` | Admin Phase 2 · seed 3 rows [ASSUMED, รอ Finance OQ-DN-01/05] |
| `V_vendor_credit_ledger` (view) | — | `partner`, `vendor_name`, SUM `credit_balance`, `dn_count` | display-only (FN-20) · DN approved/sent ที่ vendor_credit>0.005 · flow ใช้/ตัดยอด = OQ-DN-06 |
| `ap_invoice` / `ap_invoice_line` | — | contract `ap_open_item` (invGrand/paid/dn_applied/input_vat_line) | **external F-ACC-APINV — soft-ref, [ASSUMED contract]** |
| `rtv_return` | — | RTV no + lines | **external W3-LITE — soft-ref, mock [ASSUMED]** |

> **Computed (ไม่ใช่ column — ENG dn-totals / ap-open-item):** `grand` = max(0, after − ebAmt − couponAmt) (ยอดลดหนี้สุทธิ, ฐาน DOA tier) · `netBefore` = before − ebBase · `netVat` = vat − ebVat (input VAT ที่ลดจริง, ม.86/10) · `outstanding` = max(0, invGrand − paid − dn_applied(approved/sent)) · **`dnRoom` = max(0, invGrand − dn_applied − dn_held(draft/pending)) — ⭐ไม่หัก paid (BR-13)** · `dnSplit(grand)`: `applyToAp` = min(grand, outstanding) · `vendorCredit` = max(0, grand − applyToAp).

### Enums / States (ครบทุกค่า — R6)
| Field | Values | Transition owner |
|---|---|---|
| `status` | `draft` → `pending_approval` → `approved` → `sent` · `cancelled` (จาก draft/pending) | feature นี้ (state machine §5.2) |
| `approval_status` (mirror, DOA contract) | `draft` \| `pending_approval` \| `approved` \| `rejected` \| `cancelled` | feature (mirror จาก DOA engine) |
| `reason` | `RTV` (คืนสินค้า, mode qty, need_rtv) · `OVERPRICE` (ผู้ขายคิดราคาเกิน, mode price) · `SHORT` (ของขาด/ไม่ครบ, mode qty) | config master |
| reason `mode` | `qty` \| `price` | config master |
| `vat_mode` (line) | `add` \| `included` \| `none` (VAT7 ภาษีซื้อ) | feature |
| `input_vat_applied` | `false` (รอเอกสาร) → `true` (มี vendorCn ครบ → ลง ภ.พ.30) | feature (FN-16) |

**State transitions (§5.2):**
| From | To | Action (API) | Roles | Guard |
|---|---|---|---|---|
| — | draft | create/save (API-03) | officer-ap | — (draft เกิน dnRoom บันทึกได้ แต่ส่งไม่ได้) |
| draft | pending_approval | submit (API-05) | officer-ap owner | !ebOver · grand ≤ dnRoom · reason_text≥10 · slot ครบ |
| pending_approval | approved | approve ครบสาย (API-06 last) | approver ขั้นสุดท้าย | **re-check grand ≤ dnRoom** (ไม่ใช่ outstanding) → ออกเลข DN + dnSplit |
| pending_approval | draft | reject (API-07) | approver current step | reason required · append history |
| draft / pending_approval | cancelled | cancel (API-08) | officer-ap owner | reason required · คืน held |
| approved | sent | send (API-09) | officer-ap | sent→resend ไม่เปลี่ยน state |
| approved / sent | (คงเดิม) | บันทึก vendorCn (API-16) | officer-ap / mgr-acc | กลับภาษีซื้อเดือน vendorCnDate (BR-14) |
| approved / sent | (คงเดิม) | ~~ออกเอกสารแก้ไข~~ (API-14) | officer-ap | ⚠️ **forward — ไม่มีใน prototype v1** · display-only · ไม่ถอนยอด (OQ-DN-04 · D-3) |

### Relationships
- `ap_invoice` (F-ACC-APINV) 1—N (soft, `inv`) `T_debit_note` 1—N `T_debit_note_line` —(soft `src_line`)→ `ap_invoice_line`
- `rtv_return` (W3-LITE mock) —(referenced เมื่อ RTV, `rtv`)→ `T_debit_note`
- `T_dn_reason_master` 1—N `T_debit_note` (`reason`)
- `T_debit_note` 1—N `T_dn_attachment` · `T_dn_audit`
- `T_debit_note` —(effect on approve)→ `ap_open_item`(dn_applied+=applyToAp) · `V_vendor_credit_ledger`(vendorCredit) · `input_vat_line`(negative, gated vendorCn) · journal_entry(mock)
- `approval_chain` / `approval_history` = jsonb snapshot บน header (freeze ณ ส่ง — LD-01)
- อ้าง master/external (อ่าน): `ap_open_item` (F-ACC-APINV, อ่าน+เขียน dn_applied ตอนอนุมัติ) · Employee (rep, อ่าน) · DOA entry `DOA-ACC-DN` (resolve)

## 3. API Surface
| Method | Endpoint | ทำอะไร | Payload หลัก / Auth |
|---|---|---|---|
| GET | /api/v1/debit-notes | List + filter (status/reason/partner/stat/q) + sort | query params · any (view scope) |
| GET | /api/v1/debit-notes/:id | Get detail (+chain/audit) | any |
| POST | /api/v1/debit-notes | Create draft | { inv, dn_date, reason, rtv?, reason_text, sales_rep, bill_to, vendor_cn?, vendor_cn_date?, lines[], endbill } · officer-ap |
| PUT | /api/v1/debit-notes/:id | Update draft (draft only) | เหมือน create · `If-Match: version` · officer-ap owner |
| POST | /api/v1/debit-notes/:id/submit | draft→pending, freeze DOA chain | { slots:[{step, assignee_id}] } · officer-ap owner |
| POST | /api/v1/debit-notes/:id/approve | Approve step (last→issue DN + dnSplit) | { note } · approver current step |
| POST | /api/v1/debit-notes/:id/reject | pending→draft + history | { reason } (required) · approver |
| POST | /api/v1/debit-notes/:id/cancel | draft/pending→cancelled + คืน held | { reason } (required) · officer-ap owner |
| POST | /api/v1/debit-notes/:id/send | approved→sent (resend) + เก็บ PDF | officer-ap |
| GET | /api/v1/debit-notes/export | CSV export | any (view scope) |
| GET | /api/v1/ap-invoices/open | Open-item picker (dnRoom>0) | officer-ap · **[ASSUMED contract F-ACC-APINV]** |
| GET | /api/v1/rtv-returns?invoice=:no | RTV picker (mock W3-LITE) | officer-ap · **mock [ASSUMED]** |
| GET | /api/v1/debit-notes/:id/pdf | Render/fetch PDF (ENG-DOC-STORE) | any |
| POST | /api/v1/debit-notes/:id/revise-doc | ⚠️ **FORWARD — ไม่มีใน prototype v1** · mark "ออกเอกสารแก้ไข" (display-only) | officer-ap · **OQ-DN-04 · dev อย่า implement จน BA เคาะ (D-3)** |
| GET | /api/v1/config/dn-reasons | Reason master (config) | any |
| **POST** | **/api/v1/debit-notes/:id/vendor-cn** ⭐ | บันทึก vendorCn → input-VAT reversal (BR-14/FN-21) | { vendor_cn, vendor_cn_date } · officer-ap / mgr-acc · status ∈ {approved, sent} |
| **GET** | **/api/v1/vendor-credits** ⭐ | Vendor credit ledger (display-only, FN-20) | partner? · any (view scope) |

> **Common:** ทุก mutation รับ `Idempotency-Key` (cache 24h, PR-7) · PUT/approve/reject/vendor-cn ใช้ `If-Match: version` → 409 ERR_STALE_DATA (optimistic lock PR-2) · ทุก endpoint `X-Tenant-Id` → RLS scope company · ทุก mutation → T_dn_audit append-only.

### Error Contract (code · HTTP · cause — 05_RULES §5.6, no microcopy)
| Code | HTTP | Cause |
|---|---|---|
| ERR_VALIDATION_FAILED | 400 | field-level generic |
| ERR_INSUFFICIENT_ROLE | 403 | role mismatch |
| ERR_NOT_CURRENT_APPROVER | 403 | SoD / step (BR-07) |
| ERR_DUPLICATE_IDEMPOTENCY_KEY | 409 | same key diff body |
| ERR_STALE_DATA | 409 | version mismatch (EC-CC-01) |
| BR_DN_EXCEEDS_ROOM | 422 | grand > dnRoom at submit (BR-02/BR-13) |
| BR_APPROVE_EXCEEDS_ROOM | 422 | grand > dnRoom at last-step approve re-check (BR-02, FN-17/EC-01) |
| BR_ENDBILL_EXCEEDS_CAP | 422 | ebOver — เกิน ebCap (BR-11) |
| BR_LINE_QTY_EXCEEDED / BR_LINE_NET_EXCEEDED | 422 | qty/net เกินเพดานบรรทัด (BR-03) |
| BR_PRICE_EXCEEDS_ORIG | 422 | unit_price > orig_price (BR-04) |
| BR_REASON_TEXT_TOO_SHORT | 422 | reason_text < 10 (BR-05) |
| BR_RTV_NEEDS_RTV | 422 | RTV ไม่มีใบคืนสินค้าของใบเดียวกัน (BR-06) |
| BR_SUBMIT_DRAFT_ONLY / BR_EDIT_DRAFT_ONLY / BR_CANCEL_STATE_INVALID / BR_SEND_STATE_INVALID | 422 | state guard (§5.2) |
| BR_VENDORCN_STATE_INVALID | 422 | vendorCn ต้อง approved/sent (BR-14) |
| BR_SLOT_INCOMPLETE | 422 | เลือกผู้อนุมัติไม่ครบทุกขั้น (BR-07) |
| BR_REASON_REQUIRED | 422 | reject/cancel reason ว่าง |

### Events emitted
| Event | ชื่อลัด | Trigger point | Payload key |
|---|---|---|---|
| `ap_dn_approved_applied` (NTF) + `ap_dn.approved` (CSQ→AC) | dn.issued | approve ครบสาย (FN-11/FN-12, ออกเลข DN) | dn_id, dn_no, api_no(inv), vendor, grand, net_vat, apply_to_ap, vendor_credit, outstanding, reason_code, dn_date, vendor_cn_date |
| `ap_dn_sent` (NTF) | dn.sent | approved→sent (FN-10) | dn_id, dn_no, api_no, vendor_invoice_no(vinv), vendor, grand, pdf_ref |
| `ap_dn_cancelled` (NTF) | dn.cancelled | draft/pending→cancelled (FN-09) | dn_id, dn_no‖'ร่าง', reason, actor |
| `ap_dn.approved` (CSQ→EC, kind=actual) | dn.issued | approve ครบสาย เมื่อ reason ∈ {OVERPRICE, ...DISC} หรือ no-PO expense | reason_code, base_amount (**ติดลบ**) · `[ASSUMED — CSQ-OQ-DN-1]` |
| `ap_dn.vat_applied`? (CSQ→AC ภาษีซื้อ) | — | record vendorCn (API-16/FN-16) — กลับ input VAT เดือน vendorCnDate | dn_no, vendor_cn_date, net_vat · **แยก event vs dn.issued = OQ-DN-07** |

> **ไม่ประกาศ (มาจาก DOA engine — ห้ามซ้ำ):** `doa_pending` / `doa_result` / `doa_escalate` (NTF) · CSQ ท่อ DC (decision ระดับเอกสาร). CSQ ท่อ OC/SC = ไม่ประกาศ · SecC = no-effect (ไม่มี Restricted) · FC = **OQ-DN-03/06, default ไม่ยิง** [ASSUMED].

## 4. Shared Rules (cross-boundary เท่านั้น — R5)
| Rule ID | Rule | กระทบใคร |
|---|---|---|
| BR-01 | เลือกได้เฉพาะใบตั้งหนี้ approved/posted ที่ **dnRoom>0** (ลดเต็มแล้วไม่โผล่ · **ใบจ่ายครบยังโผล่** ถ้า dnRoom>0) | F-ACC-APINV (contract ap_open_item) |
| BR-02 (LOCK-04) | ยอด DN สุทธิ ≤ **dnRoom** — ตรวจ 2 จังหวะ: ส่ง (grand ≤ dnRoom) + อนุมัติขั้นสุดท้าย (grand ≤ dnRoom re-check) | F-ACC-APINV · ผู้อนุมัติ |
| BR-06 | reason RTV ต้องอ้างใบคืนสินค้า (RTV) ของใบเดียวกัน · qty ≤ min(qtyLeft, RTV.qty) | W3-LITE RTV (mock [ASSUMED]) |
| BR-07 (LOCK-05) | DOA resolve ตามมูลค่า `grand` ณ กดส่ง แล้ว freeze snapshot · **SoD: submitted_by ≠ actor** (ผู้ขอไม่อนุมัติเอง) | DOA engine (F-DLG-001) · Policy Center |
| LD-05 | DOA tier คิดจาก **`grand` = ยอดสุทธิหลังหักส่วนลดท้ายบิล** (`totals().grand`) | DOA engine · tier matrix |
| BR-08 (LOCK-06) | เลข DN `DN-YYYY-NNNN` (ปี ค.ศ.) no-gap ออกเมื่ออนุมัติครบสายเท่านั้น ผ่าน `ENG-DOC-NUM.next('DN')` — feature ไม่ generate เอง | Document Configuration (F-DOCCFG) |
| BR-09 | อนุมัติครบ → `ap_open_item.dn_applied += applyToAp` · JE (**Dr 2110 เจ้าหนี้ = applyToAp · Cr 5xxx รับคืน/ส่วนลด = netBefore · Cr 1150 ภาษีซื้อ = netVat**) · input_vat_line ค่าลบ = netVat (⚠️ ลง ภ.พ.30 เมื่อมี vendorCn — BR-14) | F-ACC-APINV · F093 JE · VAT ภ.พ.30 |
| ⭐ BR-11 (FN-19) | ส่วนลดท้ายบิล (฿/%) เพดาน ebCap = max(0, after−couponAmt) · ebOver → บล็อก submit · grand ≥0 และ net ≤ dnRoom | เพดาน% configurable (Admin) |
| ⭐ BR-12 (FN-19, LOCK-07) | ส่วนลดท้ายบิลลดฐานภาษี → `ebVat = ebAmt × (vat/after)` · netVat = vat − ebVat (ม.86/10). ภ.พ.30 + JE + PDF สะท้อน netVat หลัง recompute · **legal basis ฝั่งซื้อ [ASSUMED — OQ-DN-05]** | VAT Report ภ.พ.30 · F093 JE |
| ⭐ BR-13 (LOCK-04, FIX-01) | เพดาน = **`dnRoom` = invGrand − dn_applied − dn_held (ไม่หัก paid)** → ใบจ่ายครบยังออก DN ได้ · `dnSplit`: applyToAp = min(grand, outstanding) · vendorCredit = max(0, grand − applyToAp) = **display-only** (OQ-DN-06) | F-ACC-APINV · Vendor Credit Ledger (F097) |
| ⭐ BR-14 (LOCK-07, FIX-02) | กลับภาษีซื้อ ภ.พ.30 **gated by vendorCn** — input_vat_line ค่าลบ ลงได้เมื่อมีเลข+วันที่ใบลดหนี้จากผู้ขาย · **เดือนภาษี = vendorCnDate** (ม.82/10) · ไม่มี → "รอเอกสาร" · ปุ่มบันทึกภายหลังบน approved/sent · **[ASSUMED — OQ-DN-05]** | VAT Report ภ.พ.30 · F093 JE |
| BR-15 (LOCK-10) | ประวัติ append-only · ไม่มี hard delete · วันที่เก็บ ค.ศ. | ทุก consumer / audit |
| BR-16 | ลดหนี้ไม่อ้างใบ = ปิด (tile "ปิดไว้" · ต้องอ้าง inv เสมอ) | scope lock (OQ-DN-01) |
| BR-17 | เหตุผลแต่ละตัวพก `legal_basis` (ม.86/10 ฝั่งซื้อ) พิมพ์ลง PDF · **[ASSUMED mirror CN — OQ-DN-05]** | pdfdoc / Finance |
| LD-06 | เลข DN / VAT / DOA / NTF / CSQ / PDF store = engine กลาง (declare-only) — ห้าม hardcode เลขรัน/สายอนุมัติ/ช่องทาง/logic 7C (ประกาศซ้ำ = register reject 422) | engines กลางทั้งหมด |

**DOA Tier Matrix** (entry `DOA-ACC-DN` · sequential · ฐาน = grand หลัง end-bill · จุดตัด+role = [DEFAULT รอ Policy Center OQ-DN-02]):
| Tier | ช่วง (ยอดสุทธิ grand) | สายอนุมัติ |
|:--:|---|---|
| 1 | 0 – 50,000 | ผจก.จัดซื้อ (`role-mgr-pur`) |
| 2 | 50,000.01 – 300,000 | ผจก.จัดซื้อ → ผจก.บัญชี (`role-mgr-acc`) |
| 3 | > 300,000 | ผจก.จัดซื้อ → ผจก.บัญชี → CFO (`role-cfo`) |

> role-ids ทั้งชุด **[ASSUMED]** (OQ-AP-06) — `role-mgr-pur`/`role-mgr-acc`/`role-cfo` ยังไม่ยืนยันใน master, รอ Policy Center. จุดตัด 50k/300k = **[ASSUMED mirror CN]**.

## 5. Integration
- **Depends on (upstream):**
  - **F-ACC-APINV (AP Invoice)** — contract `ap_open_item` (invGrand/paid/dn_applied/input_vat_line → outstanding + **dnRoom ไม่หัก paid**) ผ่าน GET /ap-invoices/open · ✅ ba-done · **[ASSUMED contract]**
  - **RTV คืนสินค้า (W3-LITE)** — RTV ของใบเดียวกัน + จำนวนคืน (reason RTV) · **mock [ASSUMED]** (forward-wire)
  - **DOA engine (F-DLG-001)** — resolve tier by grand + freeze · entry `DOA-ACC-DN` ต้องตั้งค่า (mock)
  - **ENG-DOC-NUM / ENG-DOC-STORE (F-DOCCFG)** · **ENG-NOTIFY (F-NOTIFY)** · **ENG-CSQ (F-CSQ-01)** · **ENG dn-totals / ap-open-item-resolver** (feature-owned, register CUBIC ตอน hand-off — LD-03)
- **Depended by (downstream):**
  - **F-ACC-APINV / ap_open_item** — `dn_applied += applyToAp` → outstanding ลด (ปิดเมื่อ=0) เมื่อ approved/sent · cancel ก่อนอนุมัติ = คืน held · หลังอนุมัติยกเลิกไม่ได้ → revise-doc (forward)
  - **Vendor Credit Ledger (F097 owned)** — `vendorCredit = max(0, grand − applyToAp)` → เครดิตคงเหลือรายผู้ขาย (display-only) · flow ใช้/ตัดยอด = OQ-DN-06
  - **VAT Report ภ.พ.30** — `input_vat_line` (ค่าลบ) = netVat · month = **vendorCnDate** (ม.82/10 · gated by vendorCn) · forward-wire
  - **Journal Entry (F093)** — Dr 2110 เจ้าหนี้ = applyToAp · Cr 5xxx รับคืน/ส่วนลด = netBefore · Cr 1150 ภาษีซื้อ = netVat · **mock [ASSUMED]** forward-wire
  - **Payment (PV, W6)** — อ่าน outstanding หลังลด · จ่ายครบคืนของ = vendorCredit (ไม่ refund · OQ-DN-03)
- **Declarations:** (chip=detect ตรงทุกตัว · DIVERGENCE none — DECLARATION_INDEX)
  - **DOA** ✅ — `DOA-ACC-DN` sequential 3-tier by value (50k/300k [DEFAULT]), tier บนยอดสุทธิ grand หลังส่วนลด, slot picker, SoD, **approveGuard re-check grand ≤ dnRoom (ไม่ใช่ outstanding · FIX-01)** · OQ-DN-02/OQ-AP-06
  - **NTF** ✅ — feature-owned events: `ap_dn_approved_applied` (dn.issued), `ap_dn_sent` (dn.sent), `ap_dn_cancelled` · (`doa_pending`/`doa_result` จาก DOA engine — ไม่ประกาศ) · AP group id [ASSUMED]
  - **CSQ** ✅ — profile `CSQ-ACC-DN` [DEFAULT]: `ap_dn.approved`→**AC** (ลด AP + กลับภาษีซื้อ ค่าลบ, เดือน = vendorCnDate) · +**EC** (kind=actual, base ติดลบ) เมื่อ OVERPRICE/DISC/no-PO [ASSUMED] · OC/DC/SC = ไม่ประกาศ · SecC no-effect · FC = OQ-DN-03/06 (default ไม่ยิง) · event แยก late-fill vendorCn = OQ-DN-07
  - **DOCCFG** ✅ — doc_type `DN` running `DN-YYYY-NNNN` (ปี ค.ศ., reset รายปี, no-gap, scope global [DEFAULT]) · snapshot: `approved_final` + `sent_external`
  - **pdfdoc** ✅ — A4 print (ม.86/10 ฝั่งซื้อ) อ้างเลข/วันที่ใบกำกับเดิมของผู้ขาย + เดิม/ถูกต้อง/ผลต่าง + ภาษีซื้อ + เหตุผล ที่ `outputs/F-ACC-DN/_print/` (template.html + sample.pdf + print-spec.md)
- **Engine hooks:** ENG-DOC-NUM (ออกเลข final approve) · ENG-DOC-STORE (flag approved_final / sent_external) · ENG-NOTIFY (emit ที่ transition) · ENG-CSQ (POST /csq/events — dn.issued ครบสาย + dn.vat_applied เมื่อ vendorCn) · ENG-DOA (resolve+freeze by grand) · ENG dn-totals + ap-open-item-resolver (feature-owned)

---
*trace: §1 ← FRD 00_OVERVIEW §0.3/§0.9 + BRD · §2 ← FRD 04_DB + 03_LOGIC §3.2 + 05_RULES §5.2 · §3 ← FRD 02_API · §4 ← FRD 05_RULES §5.1 + 07_LOCKED_DECISIONS · §5 ← 02_API §2.X + DOA/NTF/CSQ/DOCCFG briefs*
*[not documented] markers: ไม่มี — ทุก integration ระบุใน FRD/briefs (external contracts + legal basis ฝั่งซื้อ ทำเครื่องหมาย [ASSUMED] ตามที่ FRD ระบุ · revise-doc = forward D-3 OQ-DN-04)*
