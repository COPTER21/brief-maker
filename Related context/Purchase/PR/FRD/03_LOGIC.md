# 03_LOGIC — F-PR-001 ใบขอซื้อ (Purchase Requisition)

> **Audience:** BE dev (business logic layer)
> **Scope:** All non-HTTP business logic — pure functions, calculations, validations, integrations
> **CUBIC alignment:** §3.1 Functions = scope-local · §3.2 Engines = CUBIC candidate/existing
> **Iron Rule R8:** ทุก mutation API ต้อง trace ไปที่ ≥ 1 Function/Engine ใน §3.3

---

## §3.1 Functions (Scope-Local) — camelCase

### F-PR-FN-01: `createPurchaseRequisition`
- **Purpose:** สร้าง PR draft จาก input (header + lines) + gen pr_no + คำนวณยอด
- **Input:** `{ header: PrHeaderInput, lines: PrLineInput[] }`
- **Output:** `PrHeader | ValidationError[]`
- **Invoked by:** F-PR-API-02
- **Calls:** F-PR-FN-03 (validate), ENG-DOC-AMT (totals)
- **Side effects:** gen pr_no (Document Numbering) · INSERT T_pr_header + T_pr_line · audit
- **Error cases:** ERR_VALIDATION_FAILED, BR_RELEASE_REF_REQUIRED
- **Iron rule check:** ✅ no HTTP terms

### F-PR-FN-02: `updatePurchaseRequisition`
- **Purpose:** แก้ PR draft/rejected (replace lines + recalc)
- **Input:** `{ id, patch: Partial<PrHeader>, lines?: PrLineInput[] }`
- **Output:** `PrHeader | ValidationError[]`
- **Invoked by:** F-PR-API-04
- **Calls:** F-PR-FN-03, ENG-DOC-AMT
- **Side effects:** UPDATE T_pr_header · DELETE+INSERT T_pr_line · audit (diff)
- **Error cases:** BR_PR_NOT_EDITABLE, ERR_STALE_DATA
- **Iron rule check:** ✅

### F-PR-FN-03: `validatePurchaseRequisition`
- **Purpose:** ตรวจข้าม field — branch/requester required, lines ≥1, qty/price >0, discount 0–100, **release_ref gating** ตาม Purchase Config.require_unlock_ref
- **Input:** `{ header, lines, config: { require_unlock_ref } }`
- **Output:** `ValidationError[] (empty = pass)`
- **Invoked by:** F-PR-FN-01, F-PR-FN-02, F-PR-FN-06
- **Calls:** —
- **Side effects:** none (pure validation)
- **Error cases:** BR_RELEASE_REF_REQUIRED, BR_EMPTY_LINES, BR_INVALID_QTY_PRICE
- **Iron rule check:** ✅

### F-PR-FN-04: `buildPrListQuery` / `hydratePr`
- **Purpose:** สร้าง query (filter: status/type/branch/release_ref/q + RLS + role scope) · hydrate detail (join branch/budget/lines)
- **Input:** `{ filters, role, tenantId }`
- **Output:** `QuerySpec` / `PrDetail`
- **Invoked by:** F-PR-API-01, F-PR-API-03
- **Calls:** —
- **Side effects:** none (read)
- **Iron rule check:** ✅

### F-PR-FN-06: `submitPurchaseRequisition`
- **Purpose:** orchestrate การส่งอนุมัติ — validate → hard control งบ → SoD check → resolve DOA chain → set pending
- **Input:** `{ id, actorId }`
- **Output:** `{ status, approval_chain } | BusinessError`
- **Invoked by:** F-PR-API-05
- **Calls:** F-PR-FN-03 (validate), ENG-BUDGET (availability check), ENG-DOA (resolve chain)
- **Side effects:** UPDATE status=pending, submitted_at, approval_chain · notify · audit
- **Error cases:** BR_OVER_BUDGET, BR_SOD_VIOLATION, BR_RELEASE_REF_REQUIRED
- **Iron rule check:** ✅

### F-PR-FN-07: `approvePurchaseRequisition`
- **Purpose:** อนุมัติชั้นปัจจุบัน → advance chain → ถ้าครบ set approved + commit งบ + emit event
- **Input:** `{ id, approverId, comment? }`
- **Output:** `{ status, current_step, chain_complete }`
- **Invoked by:** F-PR-API-06
- **Calls:** ENG-BUDGET (commit when complete)
- **Side effects:** advance approval_chain · ถ้าครบ → status=approved + **emit `procurement.pr_linked`** · notify · audit
- **Error cases:** ERR_NOT_CURRENT_APPROVER, BR_INVALID_STATE
- **Iron rule check:** ✅

### F-PR-FN-08: `rejectPurchaseRequisition`
- **Purpose:** ตีกลับ (require reason) → status=rejected
- **Input:** `{ id, approverId, reason }`
- **Output:** `{ status }`
- **Invoked by:** F-PR-API-07
- **Calls:** —
- **Side effects:** UPDATE status=rejected, reject_reason · notify requester · audit
- **Error cases:** BR_REJECT_REASON_REQUIRED
- **Iron rule check:** ✅

### F-PR-FN-09: `cancelPurchaseRequisition`
- **Purpose:** ยกเลิก PR · ถ้า status=approved → reverse budget committed (compensating)
- **Input:** `{ id, actorId, reason }`
- **Output:** `{ status }`
- **Invoked by:** F-PR-API-08
- **Calls:** ENG-BUDGET (reverse ถ้า approved)
- **Side effects:** UPDATE status=cancelled · reverse committed · audit
- **Error cases:** BR_CANCEL_NOT_ALLOWED
- **Iron rule check:** ✅

### F-PR-FN-10: `setRoute`
- **Purpose:** กำหนดเส้นทาง (cp/po_direct) · po_direct → lock PR
- **Input:** `{ id, route }`
- **Output:** `{ route }`
- **Invoked by:** F-PR-API-09
- **Calls:** —
- **Side effects:** UPDATE route · set lock flag · audit
- **Error cases:** BR_ROUTE_LOCKED
- **Iron rule check:** ✅

### F-PR-FN-11: `buildPrDocumentModel`
- **Purpose:** ประกอบ data model สำหรับ PDF — org+logo (Organization), branch ship-to (address), lines, totals, baht text, signature slots = N ชั้นจาก approval_chain
- **Input:** `{ id }`
- **Output:** `PrDocModel`
- **Invoked by:** F-PR-API-10
- **Calls:** —
- **Side effects:** audit (export Restricted — D-CLASS)
- **Iron rule check:** ✅

---

## §3.2 Engines (Reusable / CUBIC-Registered) — kebab-case

### ENG-DOC-AMT: `doc-amount-engine` [NEW]
| Field | Value |
|---|---|
| id | (assigned at CUBIC registration) |
| code | `doc-amount-engine` |
| name | Document Amount Engine (line + doc-level totals) |
| category | financial-calculation |
| status | DRAFT (this FRD) |
| owner | shared (P2P/O2C documents) |

**Input Schema:**
```json
{
  "lines": [{ "qty": 0, "unit_price": 0, "discount_pct": 0, "vat_mode": "none|add|included", "vat_pct": 7 }],
  "endbill_discount": { "mode": "amount|percent", "value": 0 },
  "wht": { "enabled": false, "pct": 3 }
}
```
**Output Schema:** `{ subtotal, discount_total, vat_total, wht_total, grand_total, lines: [{ line_amount }] }`
**Logic Outline:**
1. ต่อบรรทัด: base = qty × unit_price; หัก discount_pct → line_net
2. VAT ต่อบรรทัด: none = 0 · add = line_net × vat_pct% · included = line_net − (line_net / (1+vat_pct%)) [back-calc, ROUND_HALF_UP — OQ-04]
3. subtotal = Σ line_net · vat_total = Σ line_vat
4. หัก end-bill discount (amount หรือ percent ของ subtotal)
5. wht_total = (subtotal − endbill_discount) × wht_pct% (ถ้า enabled)
6. grand_total = subtotal − endbill_discount + vat_total
**Used by features:** F-PR-001 (current), F-PO/F-CP/F-QT (planned reuse)
**Iron rule check:** ✅ pure · ✅ reusable 2+ · ✅ substantial (algorithm ชัด)
**CUBIC Registration:** DRAFT → register ที่ dev hand-off (ดู LD-05)

---

### ENG-DOA: `doa-resolver` [EXISTING]
| Field | Value |
|---|---|
| code | `doa-resolver` · category validation/workflow · status REGISTERED (F-PC-DOA-01) · owner DOA module |

**Input Schema:** `{ feature_id: "F-PR-001", cost_center, amount }`
**Output Schema:** `{ chain: [{ step, role, approver_id?, threshold }] }`
**Logic Outline:** resolve สายอนุมัติตาม rule matrix (by cost_center + amount tiers) — **ไม่ hardcode ที่ F-PR**
**Used by features:** ทุก feature ที่มี approval (F-PR-001 included)
**Iron rule check:** ✅ pure resolver
**CUBIC Registration:** EXISTING — reuse engine ของ DOA module · F-PR ส่ง placeholder fields เท่านั้น (ดู LD-03)

---

### ENG-BUDGET: `budget-availability-engine` [EXISTING]
| Field | Value |
|---|---|
| code | `budget-availability-engine` · category financial-calculation · status REGISTERED (F-BGT-REQ-001) · owner Budget module |

**Input Schema:** `{ release_ref, amount, op: "check"|"commit"|"reverse" }`
**Output Schema:** `{ remaining, allowed: boolean, committed?: boolean }`
**Logic Outline:**
1. `check` — remaining = งบปลดอายัด − Σ(PR active ผูก release_ref เดียวกัน); allowed = (amount ≤ remaining)
2. `commit` — atomic decrement (3-stage: released→committed) เมื่อ PR approved + emit ack
3. `reverse` — คืน committed เมื่อ cancel หลัง approved
**Used by features:** F-BGT, F-PR-001, F-PO
**Iron rule check:** ✅ pure (DB ops ผ่าน owner module)
**CUBIC Registration:** EXISTING — F-PR เรียกผ่าน contract; **atomic strategy = OQ-01** · **event contract = OQ-02**

---

## §3.3 API ↔ Logic Trace Table (R8 Anchor)

| API ID | Method | Path | Calls Functions | Calls Engines |
|---|---|---|---|---|
| F-PR-API-01 | GET | /purchase-requisitions | F-PR-FN-04 | — |
| F-PR-API-02 | POST | /purchase-requisitions | F-PR-FN-01, F-PR-FN-03 | ENG-DOC-AMT |
| F-PR-API-03 | GET | /:id | F-PR-FN-04 | — |
| F-PR-API-04 | PUT | /:id | F-PR-FN-02, F-PR-FN-03 | ENG-DOC-AMT |
| F-PR-API-05 | POST | /:id/submit | F-PR-FN-06, F-PR-FN-03 | ENG-BUDGET, ENG-DOA |
| F-PR-API-06 | POST | /:id/approve | F-PR-FN-07 | ENG-BUDGET |
| F-PR-API-07 | POST | /:id/reject | F-PR-FN-08 | — |
| F-PR-API-08 | POST | /:id/cancel | F-PR-FN-09 | ENG-BUDGET |
| F-PR-API-09 | POST | /:id/route | F-PR-FN-10 | — |
| F-PR-API-10 | GET | /:id/pdf | F-PR-FN-11 | — |

### Trace Verification (Self-Check)
- [x] ทุก mutation API (02,04,05,06,07,08,09) มี ≥ 1 Function/Engine
- [x] ไม่มี orphan Function — FN-01,02,03,04,06,07,08,09,10,11 ปรากฏใน trace ครบ
- [x] ไม่มี orphan Engine — ENG-DOC-AMT (02,04), ENG-DOA (05), ENG-BUDGET (05,06,08) ครบ
- [x] ไม่มี hidden logic ใน 02_API (CRUD/calc อยู่ใน 03_LOGIC ทั้งหมด)

---

## §3.4 Dependencies
### External Function/Engine called
- `doa-resolver` from DOA module (F-PC-DOA-01) — EXISTING
- `budget-availability-engine` from Budget module (F-BGT-REQ-001) — EXISTING
- lookups: Product / Employee / Branch / Vendor masters
### External that calls into this feature
- CP / PO consume PR (approved) downstream

---

## §3.5 Open Questions / Locked Decisions Referenced
- LD-01: drawer width 1290 override (UI) — locked
- LD-02: ไม่มี payment term ที่ PR — locked
- LD-03: doa-resolver external, placeholder จนกว่า wire (Phase 3) — locked
- LD-05: doc-amount-engine register CUBIC ที่ dev hand-off
- OQ-01 atomic commit · OQ-02 event contract · OQ-04 VAT-included rounding

---

## Audience Cheat-Sheet
| Reader | Read sections |
|---|---|
| BE dev | §3.1 + §3.2 + §3.3 |
| QA | §3.3 + §3.1 Side effects + §3.2 I/O |
| Architect / CUBIC owner | §3.2 + §3.4 + §3.5 |
| PM | §3.3 (table) |
