# 05_RULES — F-CP-001 เปรียบเทียบราคา (Price Comparison)

> **Audience:** Backend developer + QA
> **Purpose:** Business Rules + Validation + Edge Cases + Errors + Security
> **Principle:** Declarative — อ่านแล้วเข้าใจโดยไม่ต้องดูโค้ด

---

## §5.1 Business Rules (BR)

### BR-CP-01: CP ต้องอ้างใบขอซื้ออย่างน้อย 1 ใบ
- **Statement:** 1 CP ต้องมี pr_refs ≥ 1 (PR ต้อง status=approved + route=cp)
- **Enforced by:** F-CP-001-API-03 precondition + FN-01 createComparison
- **Error:** `BR_CP_PR_REQUIRED` → 422
- **Rationale:** CP เกิดจากความต้องการซื้อที่อนุมัติแล้วเท่านั้น

### BR-CP-02: ต้องเทียบผู้ขายอย่างน้อย 2 ราย
- **Statement:** `CP_MIN_VENDORS = 2`, `CP_MAX_VENDORS = 3` (PURCHASE_CONFIG)
- **Enforced by:** FN-05 validateComparisonForSubmit (ตอน submit/award), UI step 2
- **Error:** `BR_CP_MIN_VENDORS` → 422
- **Configurable:** YES — Purchase Config (audit logged)

### BR-CP-03: ต้องเลือกผู้ชนะครบทุกรายการก่อนส่งเซ็น/ออก PO
- **Statement:** ทุก line ต้องมี winner_vendor_id + winner_price > 0
- **Enforced by:** FN-05, F-CP-001-API-05/08 precondition
- **Error:** `BR_CP_WINNER_INCOMPLETE` → 422

### BR-CP-04: ราคา preset ดึงจาก Vendor Price List (แก้ไขได้)
- **Statement:** ตอนเข้าขั้นเทียบราคา / เพิ่มผู้ขาย → เติมราคาจาก price list **เฉพาะช่องว่าง** (is_preset=true) · ผู้ใช้แก้ทับได้ (is_preset→false)
- **Used by:** ENG-03 vendor-price-list-resolver, FN-01/FN-02
- **Rationale:** ลดงานกรอก + ใช้ราคามาตรฐาน แต่คง flexibility

### BR-CP-05: ผู้ชนะ default = ราคาต่ำสุดต่อรายการ (override ได้)
- **Statement:** autoWinners เลือก lowest unit_price per line · buyer override เป็นผู้ขายอื่นได้
- **Used by:** ENG-01 price-comparison-winner-engine
- **Note:** override (ไม่ใช่ต่ำสุด) → ENG-01 เก็บ flag · (OQ-04: บันทึกเหตุผลหรือไม่)

### BR-CP-06: PO Split = จัดกลุ่มตามผู้ขายที่ชนะ (1 ผู้ขาย = 1 PO)
- **Statement:** lines ที่ชนะโดย vendor เดียวกัน → รวมเป็น 1 PO
- **Used by:** ENG-02 po-split-engine

### BR-CP-07: เลขที่ PO ออกโดยระบบใบสั่งซื้อ (PO) เท่านั้น
- **Statement:** po_id ไม่ได้กำหนดใน CP — มาจาก F-PO-001 ตอน award
- **Enforced by:** FN-09 awardComparison (เรียก F-PO-001)

### BR-CP-08: สายอนุมัติมาจาก DOA (ห้าม hardcode)
- **Statement:** ผู้ตรวจสอบ/ผู้อนุมัติ + ลำดับ resolve จาก `doa-approval-resolver` ด้วย {feature_id:F-CP-001, cost_center, amount=winner_total}
- **Used by:** ENG-04, FN-06/FN-07
- **Rationale:** Approval Pattern standard — TODO placeholder รอ DOA wire, ไม่ hardcode rule

### BR-CP-09: VAT 7% (เอกสาร)
- **Statement:** เอกสาร CP แสดง winner_total (ก่อน VAT) + VAT 7% + grand_total
- **Computed by:** FN-11 buildComparisonDocument
- **Configurable:** อัตรา VAT = Finance config · (OQ-02: คำนวณใน CP หรือผลักไป PO)

### BR-CP-10: PR ที่ถูกใช้แล้วอ้างซ้ำไม่ได้
- **Statement:** PR ที่ถูก CP อื่นอ้าง หรือออก PO ตรงแล้ว → อ้างใน CP ใหม่ไม่ได้
- **Enforced by:** FN-01 precondition
- **Error:** `BR_CP_PR_ALREADY_USED` → 422

### BR-CP-11: แก้ไขได้เฉพาะสถานะ draft
- **Statement:** PUT (lines/quotes/winners) ทำได้เฉพาะ status=draft
- **Enforced by:** F-CP-001-API-04 precondition
- **Error:** `BR_CP_NOT_EDITABLE` → 422

---

## §5.2 State Machine

```
   ┌───────┐  submit   ┌─────────┐  approve  ┌──────────┐  award   ┌─────────┐
   │ draft │──────────►│ pending │──────────►│ approved │─────────►│ awarded │
   └───┬───┘           └────┬────┘           └──────────┘          └─────────┘
       │                    │ reject (+reason)
       │ cancel             ▼
       ▼               ┌───────┐
  ┌──────────┐         │ draft │ (กลับไปแก้)
  │cancelled │         └───────┘
  └──────────┘
```

| From | To | Action | Allowed roles | Conditions |
|---|---|---|---|---|
| draft | pending | submit | buyer | vendors ≥ 2 + ทุก line มีผู้ชนะ (BR-CP-02,03) |
| draft | cancelled | cancel | buyer, admin | — |
| pending | approved | approve | approver (ตาม DOA) | actor อยู่ในชั้น DOA |
| pending | draft | reject | approver | reject_reason required |
| approved | awarded | award | proc_manager | po_splits resolved + PO created |

> Transitions enforced by FN-06 submit, FN-07 approve, FN-08 reject, FN-09 award (03_LOGIC §3.1)

---

## §5.3 Permission Matrix

| Role | View | Create | Edit(draft) | Submit | Approve | Reject | Award | Export |
|---|---|---|---|---|---|---|---|---|
| buyer | all | ✅ | own | ✅ | — | — | — | ✅ |
| proc_manager | all | — | — | — | — | — | ✅ | ✅ |
| approver | all | — | — | — | ✅ | ✅ | — | ✅ |
| finance | all | — | — | — | — | — | — | ✅ |
| admin | all | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

---

## §5.4 Field Validation Rules

| Field | Rule | Error code |
|---|---|---|
| `cp_date` | required, date | `BR_CP_INVALID_DATE` |
| `pr_refs` | required, array ≥ 1, each approved+route=cp+unused | `BR_CP_PR_REQUIRED` / `BR_CP_PR_ALREADY_USED` |
| `vendors` | ≥ 2, ≤ 3 (submit) | `BR_CP_MIN_VENDORS` |
| `quote.unit_price` | ≥ 0 (null = ไม่เสนอ) | `BR_CP_NEGATIVE_PRICE` |
| `line.winner_vendor_id` | required ก่อน submit, ต้องเป็น vendor ที่มี quote | `BR_CP_WINNER_INCOMPLETE` |
| `reject_reason` | required ตอน reject | `ERR_REASON_REQUIRED` |

### Cross-field
- `winner_total` = Σ(line.qty × winner_price) → enforced by ENG-01
- `grand_total` = winner_total + vat_amount → FN-11
- `po_count` = distinct winner_vendor_id → ENG-02
- `approved_at` ≥ `submitted_at` → state machine + DB check

---

## §5.5 Edge Cases (from Phase 2.5 Probing)

### EC-01: Concurrent approve (PR-1)
- **Scenario:** 2 approver กดอนุมัติพร้อมกัน
- **Resolution:** optimistic lock (`version` + If-Match) — คนแรกชนะ, คนสองได้ 409
- **Error:** `ERR_STALE_DATA` · **Test:** TC-CC-01

### EC-02: Idempotent submit/create (PR-7)
- **Scenario:** double-click ส่งเซ็น/สร้าง
- **Resolution:** Idempotency-Key → คืน cached response (ไม่ INSERT ซ้ำ) · **Test:** TC-ID-01

### EC-03: PR ถูกใช้/ยกเลิกหลังเลือก (PR-3)
- **Scenario:** เลือก PR ใน step1 แล้ว PR ถูก CP อื่นอ้าง/ออก PO ตรงก่อน save
- **Resolution:** re-check ตอน save (FN-01) → 422 BR_CP_PR_ALREADY_USED · **Test:** TC-PR-01

### EC-04: ราคาถูกล้างแล้วเข้าขั้นใหม่ (PR-5)
- **Scenario:** ผู้ใช้ลบราคาในเซลล์ แล้วกลับเข้า step3
- **Resolution:** applyPriceList เติม **เฉพาะช่องว่าง** จาก price list (ไม่ทับค่าที่แก้) · **Test:** TC-PL-01

### EC-05: เพิ่ม/ลบผู้ขายกลางคัน (PR-5)
- **Scenario:** เพิ่ม vendor หลังกรอกราคาบางส่วน / ลบ vendor ที่เป็นผู้ชนะ
- **Resolution:** เพิ่ม → เติม column preset · ลบ vendor ที่ชนะ → clear winner ของ line นั้น (ต้องเลือกใหม่) · **Test:** TC-VN-01

### EC-06: Idempotent award (PR-7)
- **Scenario:** กดออกใบสั่งซื้อซ้ำ / retry หลัง timeout
- **Resolution:** Idempotency-Key + ตรวจ status=awarded แล้ว → คืน po_splits เดิม (ไม่สร้าง PO ซ้ำ) · **Test:** TC-AW-01

### EC-07: PO สร้างไม่สำเร็จบางใบตอน award (PR-8)
- **Scenario:** F-PO-001 สร้าง PO ใบที่ 2 ล้มเหลว (ใบที่ 1 สำเร็จ)
- **Resolution (OQ-01):** เลือก 1 ใน — (a) all-or-nothing rollback ทั้ง CP, (b) partial + mark split ที่ fail ไว้ retry
- **Default ที่เสนอ:** all-or-nothing (transaction) → status คง approved + `ERR_PO_CREATE_FAILED` · **Test:** TC-AW-02

### EC-08: submit ทั้งที่ winner ไม่ครบ (PR-9)
- **Scenario:** บาง line ยังไม่เลือกผู้ชนะ
- **Resolution:** FN-05 block → 422 BR_CP_WINNER_INCOMPLETE · **Test:** TC-SB-01

---

## §5.6 Error Catalog

| Code | HTTP | Message (i18n key) | Cause |
|---|---|---|---|
| `ERR_VALIDATION_FAILED` | 400 | error.validation.failed | generic |
| `ERR_REASON_REQUIRED` | 400 | error.reason.required | reject ไม่มีเหตุผล |
| `ERR_NOT_AUTHENTICATED` | 401 | error.auth.unauth | no token |
| `ERR_INSUFFICIENT_ROLE` | 403 | error.auth.role | role/DOA ไม่ผ่าน |
| `ERR_NOT_FOUND` | 404 | error.notfound | CP ไม่พบ |
| `ERR_DUPLICATE_IDEMPOTENCY_KEY` | 409 | error.idempotency.dup | key เดิม body ต่าง |
| `ERR_STALE_DATA` | 409 | error.concurrency.stale | version mismatch (EC-01) |
| `ERR_PO_CREATE_FAILED` | 502 | error.po.create | F-PO-001 fail (EC-07) |
| `BR_CP_PR_REQUIRED` | 422 | br.cp.pr.required | BR-CP-01 |
| `BR_CP_PR_ALREADY_USED` | 422 | br.cp.pr.used | BR-CP-10 |
| `BR_CP_MIN_VENDORS` | 422 | br.cp.vendors.min | BR-CP-02 |
| `BR_CP_WINNER_INCOMPLETE` | 422 | br.cp.winner.incomplete | BR-CP-03 |
| `BR_CP_NOT_EDITABLE` | 422 | br.cp.not.editable | BR-CP-11 |
| `BR_CP_NOT_PENDING` | 422 | br.cp.not.pending | approve/reject ผิดสถานะ |
| `BR_CP_NOT_APPROVED` | 422 | br.cp.not.approved | award ผิดสถานะ |
| `BR_CP_NEGATIVE_PRICE` | 422 | br.cp.price.negative | ราคา < 0 |
| `ENG_ERR_WINNER_NO_QUOTE` | 500 | error.engine.winner | override vendor ไม่มี quote |

---

## §5.7 Security Bible Application

> Domains triggered: **D2, D5, D9, D15, D17, D-CLASS** (+ D7 minimal)

### D2: Authentication & Session
- ทุก endpoint require JWT · token TTL 1 ชม. · refresh 7 วัน

### D5: Financial Transactions
- ทุกการเปลี่ยนราคา/ยอด → audit log (before+after)
- approval workflow ตาม DOA (มูลค่า winner_total)

### D7: PII Protection
- `buyer` (ชื่อพนักงาน) → PDPA scope · log ใช้ ID reference ไม่ใช่ชื่อเต็ม

### D-CLASS: Data Classification ⭐ (v5.1)
Per-field รายละเอียดที่ 04_DB §4.2 + §4.6

**Enforcement summary:**
| Layer | Confidential fields (ราคา/ยอด) |
|---|---|
| API response | mask `***` ถ้า role ไม่ใช่ procurement/finance |
| UI display | matrix ราคา + winner_total แสดงเฉพาะ role ที่ผ่าน |
| Export/Print | ตัดคอลัมน์ราคาถ้า role ไม่ผ่าน |
| Audit | log view + mutation + export ของ pricing |

**Wire points:** Policy Center → Data Classification (ราคา/ยอด = Confidential)

### D9: Audit Logging
- ทุก mutation + state transition + award → T_audit_log · retention 7 ปี · append-only

### D15: Admin Actions
- state transitions (submit/approve/reject/award) → log actor + timestamp · reject ต้องมีเหตุผล

### D17: Multi-Tenant Isolation
- PostgreSQL RLS · middleware validate X-Tenant-Id · cross-tenant ห้าม

---

## §5.8 Compliance & Audit Requirements

| Requirement | Implementation |
|---|---|
| จัดซื้อโปร่งใส (เทียบ ≥ 2 ราย) | BR-CP-02 |
| Audit trail การเลือกผู้ชนะ | D9 + ENG-01 flag (override) |
| DOA governance | BR-CP-08 + ENG-04 (ไม่ hardcode) |
| PDPA (ชื่อผู้จัดทำ) | D7 |
| User Access ENC + DOA ENC checkpoints | ก่อน deploy (CUBE 4.0 standard) |
