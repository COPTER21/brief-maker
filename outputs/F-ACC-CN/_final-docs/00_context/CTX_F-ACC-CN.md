# CTX — F-ACC-CN (F096): ใบลดหนี้ลูกค้า (Credit Note)

> **derived from:** FRD_F-ACC-CN v1.0 (2026-09-22) · **generated:** 2026-09-22
> **module:** Accounting / Accounts Receivable (AR) · Wave W5 Phase A (LITE) · dep=""
> **status:** active (FRD v1.0 = DRAFT, pending BA gate)
> ⚠ Derived artifact — source of truth คือ FRD Pack · ถ้า FRD revise ต้อง regen CTX (R9)

---

## 1. Summary
ออก **ใบลดหนี้ลูกค้า (Credit Note)** ที่ **อ้างใบแจ้งหนี้ AR เสมอ** (ห้าม "ลดลอย") — เจ้าหน้าที่ลูกหนี้สร้าง/แก้ร่าง/ส่งอนุมัติ, ผู้อนุมัติ (ผจก.ขาย/บัญชี/CFO) อนุมัติตามสาย DOA 3-tier ตามมูลค่า, แล้วส่งใบให้ลูกค้า.
Trigger: มีใบแจ้งหนี้คงค้าง (outstanding>0) ที่ต้องลดหนี้ (รับคืน/ส่วนลดภายหลัง/ผิดราคา/คิดจำนวนเกิน).
ผลลัพธ์เมื่ออนุมัติครบสาย: ออกเลข `CN-YYYY-NNNN`, ลด outstanding ของใบเดิม (`cn_applied`), กลับภาษีขายเดือน cnDate (ภ.พ.30), JE (mock), PDF A4 ตาม ม.86/10.
รองรับ **ส่วนลดท้ายบิล (end-bill)** ที่ลดฐานภาษี → คำนวณ VAT ใหม่ตามสัดส่วน (FN-19). ประวัติ append-only, ไม่มี hard delete.
Pattern Q document + B2 v2 line editor (LOCK-01). Security Preset **P4 Financial**.

## 2. Data Contract

### Entities
| Entity | PK | Key Fields (ที่ feature อื่น join/อ่าน) | หมายเหตุ |
|---|---|---|---|
| `T_credit_note` (header) | `id` (uuid) | `code`, `ref_invoice`, `sales_return_ref`, `customer_code`, `cn_date`, `reason`, `status`, `endbill`(jsonb), `doa_entry_ref`, `approval_chain`(jsonb), `approval_history`(jsonb) | owner F-ACC-CN · RLS scope company · `code` NULL จนอนุมัติครบ · UNIQUE(tenant_id, code) WHERE code NOT NULL (no-gap) |
| `T_credit_note_line` | `id` (uuid) | `cn_id`(FK), `src_line` (soft-ref "INV\|idx"), `item_code`, `qty`, `unit_price`, `orig_qty`, `orig_price`, `vat_mode`, `vat_pct` | ล็อกสินค้าจากใบเดิม · CASCADE จาก header |
| `T_cn_attachment` | `id` (uuid) | `cn_id`(FK), `name`, `size`, `url` | jpg/png/pdf ≤10MB `[AI-DEFAULT]` |
| `T_cn_audit` | `id` (uuid) | `cn_id`(FK), `act`, `by`, `at`, `note` | **append-only — NO UPDATE / NO DELETE** (trigger) · retention 7 ปี |
| `T_cn_reason_master` (config) | `code` | `name`, `mode`(qty\|price), `need_sr`, `legal_basis`, `trade_discount_warn` | Admin Phase 2 · seed 4 rows [ASSUMED, รอ Finance OQ-CN-01] |
| `ar_invoice` / `ar_invoice_line` | — | contract `ar_open_item` (invGrand/paid/cn_applied/outstanding) | **external F094 — soft-ref, [ASSUMED contract]** |
| `sales_return` | — | SR no + lines (RET) | **external F090 — soft-ref, mock [ASSUMED]** |

> **Computed (ไม่ใช่ column — ENG cn-totals / ar-open-item):** `grand` = max(0, after − ebAmt − coupon) (ยอดลดหนี้สุทธิ, ฐาน DOA tier) · `net_before` = before − ebBase · `net_vat` = vat − ebVat · `outstanding` = invGrand − paid − cn_applied(approved/sent) · `available` = outstanding − cn_held(draft/pending).

### Enums / States (ครบทุกค่า — R6)
| Field | Values | Transition owner |
|---|---|---|
| `status` | `draft` → `pending_approval` → `approved` → `sent` · `cancelled` (จาก draft/pending) | feature นี้ (state machine §5.2) |
| `approval_status` (mirror, DOA contract) | `draft` \| `pending_approval` \| `approved` \| `rejected` \| `cancelled` | feature (mirror จาก DOA engine) |
| `reason` | `RET` (รับคืน, mode qty, need_sr) · `DISC` (ส่วนลดภายหลัง, mode price, warn) · `PRICE` (ผิดราคา, mode price) · `QTY` (คิดจำนวนเกิน, mode qty) | config master |
| reason `mode` | `qty` \| `price` | config master |
| `vat_mode` (line) | `add` \| `included` \| `none` | feature |

**State transitions (§5.2):**
| From | To | Action (API) | Roles | Guard |
|---|---|---|---|---|
| — | draft | create/save (API-03) | officer-ar | — |
| draft | pending_approval | submit (API-05) | officer-ar owner | !ebOver · grand ≤ available · reason_text≥10 · slot ครบ |
| pending_approval | approved | approve ครบสาย (API-06 last) | approver ขั้นสุดท้าย | re-check grand ≤ outstanding → ออกเลข CN |
| pending_approval | draft | reject (API-07) | approver current step | reason required · append history |
| draft / pending_approval | cancelled | cancel (API-08) | officer-ar owner | reason required · คืน held |
| approved | sent | send (API-09) | officer-ar | sent→resend ไม่เปลี่ยน state |
| approved / sent | (คงเดิม) | ออกเอกสารแก้ไข (API-14) | officer-ar | display-only · ไม่ถอนยอด (OQ-CN-02) |

### Relationships
- `ar_invoice` (F094) 1—N (soft, `ref_invoice`) `T_credit_note` 1—N `T_credit_note_line` —(soft `src_line`)→ `ar_invoice_line`
- `sales_return` (F090 mock) —(referenced เมื่อ RET, `sales_return_ref`)→ `T_credit_note`
- `T_cn_reason_master` 1—N `T_credit_note` (`reason`)
- `T_credit_note` 1—N `T_cn_attachment` · `T_cn_audit`
- `approval_chain` / `approval_history` = jsonb snapshot บน header (freeze ณ ส่ง — LD-01)
- อ้าง master/external (อ่าน): `ar_open_item` (F094, อ่าน+เขียน cn_applied ตอนอนุมัติ) · Employee (rep, อ่าน) · DOA entry `DOA-ACC-CN` (resolve)

## 3. API Surface
| Method | Endpoint | ทำอะไร | Payload หลัก / Auth |
|---|---|---|---|
| GET | /api/v1/credit-notes | List + filter (status/reason/customer/stat/q) + sort | query params · any (view scope) |
| GET | /api/v1/credit-notes/:id | Get detail (+chain/audit) | any |
| POST | /api/v1/credit-notes | Create draft | { ref_invoice, cn_date, reason, sales_return_ref?, reason_text, sales_rep, bill_to, lines[], endbill } · officer-ar |
| PUT | /api/v1/credit-notes/:id | Update draft (draft only) | เหมือน create · `If-Match: version` · officer-ar owner |
| POST | /api/v1/credit-notes/:id/submit | draft→pending, freeze DOA chain | { slots:[{step, assignee_id}] } · officer-ar owner |
| POST | /api/v1/credit-notes/:id/approve | Approve step (last→issue CN) | { note } · approver current step |
| POST | /api/v1/credit-notes/:id/reject | pending→draft + history | { reason } (required) · approver |
| POST | /api/v1/credit-notes/:id/cancel | draft/pending→cancelled + คืน held | { reason } (required) · officer-ar owner |
| POST | /api/v1/credit-notes/:id/send | approved→sent (resend) + เก็บ PDF | officer-ar |
| GET | /api/v1/credit-notes/export | CSV export | any (view scope) |
| GET | /api/v1/ar-invoices/open | Open-item picker (outstanding>0) | officer-ar · **[ASSUMED contract F094]** |
| GET | /api/v1/sales-returns?invoice=:no | SR picker (mock F090) | officer-ar · **mock [ASSUMED]** |
| GET | /api/v1/credit-notes/:id/pdf | Render/fetch PDF (ENG-DOC-STORE) | any |
| POST | /api/v1/credit-notes/:id/revise-doc | Mark "ออกเอกสารแก้ไข" (display-only) | officer-ar |
| GET | /api/v1/config/cn-reasons | Reason master (config) | any |

> **Common:** ทุก mutation รับ `Idempotency-Key` (cache 24h, PR-7) · PUT/approve/reject ใช้ `If-Match: version` → 409 ERR_STALE_DATA (optimistic lock PR-2) · ทุก endpoint `X-Tenant-Id` → RLS scope company · ทุก mutation → T_cn_audit append-only.

### Error Contract (code · HTTP · cause — 05_RULES §5.6, no microcopy)
| Code | HTTP | Cause |
|---|---|---|
| ERR_VALIDATION_FAILED | 400 | field-level generic |
| ERR_INSUFFICIENT_ROLE | 403 | role mismatch |
| ERR_NOT_CURRENT_APPROVER | 403 | SoD / step (BR-07) |
| ERR_DUPLICATE_IDEMPOTENCY_KEY | 409 | same key diff body |
| ERR_STALE_DATA | 409 | version mismatch (EC-CC-01) |
| BR_CN_EXCEEDS_OUTSTANDING | 422 | grand > available at submit (BR-02) |
| BR_APPROVE_EXCEEDS_OUTSTANDING | 422 | grand > outstanding at last-step approve (BR-02) |
| BR_ENDBILL_EXCEEDS_CAP | 422 | ebOver — net < 0 (BR-11) |
| BR_LINE_QTY_EXCEEDED / BR_LINE_NET_EXCEEDED | 422 | qty/net เกินเพดานบรรทัด (BR-03) |
| BR_PRICE_EXCEEDS_ORIG | 422 | unit_price > orig_price (BR-04) |
| BR_REASON_TEXT_TOO_SHORT | 422 | reason_text < 10 (BR-05) |
| BR_RET_NEEDS_SR | 422 | RET ไม่มี SR ของใบเดียวกัน (BR-06) |
| BR_SUBMIT_DRAFT_ONLY / BR_EDIT_DRAFT_ONLY / BR_CANCEL_STATE_INVALID / BR_SEND_STATE_INVALID | 422 | state guard (§5.2) |
| BR_SLOT_INCOMPLETE | 422 | เลือกผู้อนุมัติไม่ครบทุกขั้น (BR-07) |

### Events emitted
| Event | ชื่อลัด | Trigger point | Payload key |
|---|---|---|---|
| `ar_cn_approved_applied` (NTF) + `ar_cn.approved` (CSQ→AC) | cn.issued | approve ครบสาย (FN-11, ออกเลข CN) | cn_id, cn_no, inv_no, customer, grand, net_vat, net_before, outstanding, reason_code, cn_date |
| `ar_cn_sent` (NTF) | cn.sent | approved→sent (FN-10) | cn_id, cn_no, inv_no, customer, grand, pdf_ref |
| `ar_cn_cancelled` (NTF) | cn.cancelled | draft/pending→cancelled (FN-09) | cn_id, cn_no‖'ร่าง', reason, actor |
| `ar_cn.approved` (CSQ→EC, kind=actual) | cn.issued | approve ครบสาย เมื่อ reason ∈ {DISC, PRICE} | reason_code, base_amount · `[ASSUMED — CSQ-OQ-CN-1]` |

> **ไม่ประกาศ (มาจาก DOA engine — ห้ามซ้ำ):** `doa_pending` / `doa_result` / `doa_escalate` (NTF) · CSQ ท่อ DC (decision ระดับเอกสาร). CSQ ท่อ OC/SC/SecC/FC = ไม่ประกาศ (FC = OQ-CN-03, default ไม่ยิง).

## 4. Shared Rules (cross-boundary เท่านั้น — R5)
| Rule ID | Rule | กระทบใคร |
|---|---|---|
| BR-01 | เลือกได้เฉพาะใบแจ้งหนี้ issued/sent ที่ outstanding>0 (void/ชำระครบไม่โผล่) | F094 AR Invoice (contract ar_open_item) |
| BR-02 (LOCK-04) | ยอด CN สุทธิ ≤ outstanding — ตรวจ 2 จังหวะ: ส่ง (grand ≤ available) + อนุมัติขั้นสุดท้าย (grand ≤ outstanding re-check) | F094 · ผู้อนุมัติ |
| BR-06 | reason RET ต้องอ้างใบรับคืน (SR) ของใบเดียวกัน · qty ≤ min(qtyLeft, SR.qty) | F090 Sales Return (mock [ASSUMED]) |
| BR-07 (LOCK-05) | DOA resolve ตามมูลค่า ณ กดส่ง แล้ว freeze snapshot · **SoD: submitted_by ≠ actor** (ผู้ขอไม่อนุมัติเอง) | DOA engine (F-DLG-001) · Policy Center |
| LD-05 (OQ-b RESOLVED) | DOA tier คิดจาก **`grand` = ยอดสุทธิหลังหักส่วนลดท้ายบิล** (`totals().grand`) | DOA engine · tier matrix |
| BR-08 (LOCK-06) | เลข CN `CN-YYYY-NNNN` (ปี ค.ศ.) no-gap ออกเมื่ออนุมัติครบสายเท่านั้น ผ่าน `ENG-DOC-NUM.next('CN')` — feature ไม่ generate เอง | Document Configuration (F-DOCCFG) |
| BR-09 | อนุมัติครบ → `ar_open_item.cn_applied += grand` · JE (Dr 4110/4120 = net_before · Dr 2150 ภาษีขาย = net_vat · Cr 1130 ลูกหนี้ = grand) · output_vat_line ค่าลบ = net_vat เดือน cnDate | F094 · F093 JE · F105 VAT (ภ.พ.30) |
| BR-11 (FN-19) | ส่วนลดท้ายบิล (฿/%) เพดาน ebCap = max(0, after−coupon) · ยอดสุทธิ ≥0 และ ≤ outstanding | เพดาน% configurable (Admin) |
| BR-12 (FN-19, LOCK-07) | ส่วนลดท้ายบิลลดฐานภาษี → `ebVat = ebAmt × (vat/after)` · net_vat = vat − ebVat (ม.86/10). ภ.พ.30 + JE + PDF สะท้อน net_vat หลัง recompute | F105 VAT Report · F093 JE |
| BR-13 (LOCK-10) | ประวัติ append-only · ไม่มี hard delete · วันที่เก็บ ค.ศ. | ทุก consumer / audit |
| BR-14 | ลดหนี้ไม่อ้างใบ = ปิด (ต้องอ้าง ref_invoice เสมอ) | scope lock (OQ-CN-01) |
| LD-06 | เลข CN / VAT / DOA / NTF / CSQ / PDF store = engine กลาง (declare-only) — ห้าม hardcode เลขรัน/สายอนุมัติ/ช่องทาง/logic 7C (ประกาศซ้ำ = register reject 422) | engines กลางทั้งหมด |

**DOA Tier Matrix** (entry `DOA-ACC-CN` · sequential · ฐาน = grand หลัง end-bill · จุดตัด+role = [DEFAULT รอ Policy Center OQ-CN-04]):
| Tier | ช่วง (ยอดสุทธิ grand) | สายอนุมัติ |
|:--:|---|---|
| 1 | 0 – 50,000 | ผจก.ขาย (`role-mgr-sales`) |
| 2 | 50,000.01 – 300,000 | ผจก.ขาย → ผจก.บัญชี (`role-mgr-acc`) |
| 3 | > 300,000 | ผจก.ขาย → ผจก.บัญชี → CFO (`role-cfo`) |

> role-ids ทั้งชุด **[ASSUMED]** (OQ-AR-06) — `role-mgr-acc` ยังไม่มีใน master, รอ Policy Center ยืนยัน.

## 5. Integration
- **Depends on (upstream):**
  - **F-ACC-ARINV (F094)** — contract `ar_open_item` (invGrand/paid/cn_applied → outstanding) ผ่าน GET /ar-invoices/open · ✅ ba-done · **[ASSUMED contract]**
  - **F090 Sales Return** — SR ของใบเดียวกัน + จำนวนคืน (reason RET) · **mock [ASSUMED]** (forward-wire)
  - **DOA engine (F-DLG-001)** — resolve tier + freeze · entry `DOA-ACC-CN` ต้องตั้งค่า (mock)
  - **ENG-DOC-NUM / ENG-DOC-STORE (F-DOCCFG)** · **ENG-NOTIFY (F-NOTIFY)** · **ENG-CSQ (F-CSQ-01)** · **ENG cn-totals / ar-open-item** (feature-owned, register CUBIC ตอน hand-off — LD-03)
- **Depended by (downstream):**
  - **F094 AR Invoice / ar_open_item** — `cn_applied += grand` → outstanding ลด (ปิดเมื่อ=0) เมื่อ approved/sent · cancel ก่อนอนุมัติ = คืน held · หลังอนุมัติยกเลิกไม่ได้ → revise-doc
  - **F105 VAT Report (ภ.พ.30)** — `output_vat_line` (ค่าลบ) = net_vat · month = cnDate (ม.82/10) · forward-wire
  - **F093 Journal Entry** — Dr 4110/4120 = net_before · Dr 2150 = net_vat · Cr 1130 = grand · **mock [ASSUMED]** forward-wire
  - **RV/PV (W6)** — อ่าน outstanding หลังลด · refund กรณีชำระครบ = นอก scope (OQ-CN-03)
- **Declarations:**
  - **DOA** ✅ — `DOA-ACC-CN` sequential 3-tier by value (50k/300k), tier บนยอดสุทธิ grand หลังส่วนลด, slot picker, SoD
  - **NTF** ✅ — feature-owned events: `ar_cn_approved_applied` (cn.issued), `ar_cn_sent` (cn.sent), `ar_cn_cancelled` · (`doa_pending`/`doa_result` จาก DOA engine — ไม่ประกาศ)
  - **CSQ** ✅ — profile `CSQ-ACC-CN` [DEFAULT]: `ar_cn.approved`→**AC** (ลด AR + กลับภาษีขาย) · +**EC** (kind=actual) เมื่อ DISC/PRICE [ASSUMED] · OC/DC/SC/SecC/FC = ไม่ประกาศ (FC = OQ-CN-03)
  - **DOCCFG** ✅ — doc_type `CN` running `CN-YYYY-NNNN` (ปี ค.ศ., reset รายปี, no-gap, scope global [DEFAULT]) · snapshot: ส่งออก/อนุมัติ+เซ็น
  - **pdfdoc** ✅ — A4 print (ม.86/10) ที่ `outputs/F-ACC-CN/_print/` (template.html + sample.pdf + print-spec.md)
- **Engine hooks:** ENG-DOC-NUM (ออกเลข final approve) · ENG-DOC-STORE (flag approved_final / sent_external) · ENG-NOTIFY (emit ที่ transition) · ENG-CSQ (POST /csq/events, emit ครบสาย) · ENG-DOA (resolve+freeze) · ENG cn-totals + ar-open-item-resolver (feature-owned)

---
*trace: §1 ← FRD 00_OVERVIEW §0.3/§0.9 + BRD §2 · §2 ← FRD 04_DB + 05_RULES §5.2 · §3 ← FRD 02_API · §4 ← FRD 05_RULES §5.1 + 07_LOCKED_DECISIONS · §5 ← BRD §12.1 + DOA/NTF/CSQ/DOCCFG briefs*
*[not documented] markers: ไม่มี — ทุก integration ระบุใน FRD/BRD/briefs (external contracts ทำเครื่องหมาย [ASSUMED] ตามที่ FRD ระบุ)*
