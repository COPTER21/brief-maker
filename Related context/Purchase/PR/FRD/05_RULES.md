# 05_RULES — F-PR-001 ใบขอซื้อ (Purchase Requisition)

> **Audience:** Backend developer + QA
> **Purpose:** Business Rules + Validation + Edge Cases + Errors + Security
> **Principle:** Declarative — อ่านแล้วเข้าใจโดยไม่ต้องดูโค้ด

---

## §5.1 Business Rules (BR)

### BR-PR-01: สถานะเริ่มต้น
- **Statement:** PR ใหม่ status = `draft`
- **Enforced by:** F-PR-FN-01 · **Tag:** FIXED

### BR-PR-02: วันที่ต้องการ default
- **Statement:** `need_date` default = `pr_date` + 7 วัน (แก้ได้)
- **Enforced by:** UI default + F-PR-FN-03 · **Tag:** CONFIGURABLE (Admin Panel)

### BR-PR-03: VAT ต่อบรรทัด
- **Statement:** default `vat_mode=add`, `vat_pct=7` (จาก product.vat_group, แก้ได้)
- **Used by:** ENG-DOC-AMT · **Tag:** CONFIGURABLE (Tax config)

### BR-PR-04: บังคับอ้างอิงใบปลดอายัด
- **Statement:** ถ้า Purchase Config.`require_unlock_ref`=true → `release_ref` required
- **Enforced by:** F-PR-FN-03 · **Error:** `BR_RELEASE_REF_REQUIRED` 422 · **Tag:** CONFIGURABLE (Purchase Config)

### BR-PR-05: Hard Control เพดานงบ ⭐
- **Statement:** Σ(grand_total ของ PR active ที่อ้าง release_ref เดียวกัน) + ใบปัจจุบัน ≤ งบคงเหลือของ release นั้น
- **Enforced by:** F-PR-FN-06 → ENG-BUDGET (check) · **Error:** `BR_OVER_BUDGET` 422 · **Tag:** FIXED (guard — ห้ามปิด)

### BR-PR-06: ความสัมพันธ์ใบปลดอายัด
- **Statement:** 1 ใบปลดอายัด : หลาย PR (1:M) — ตัดยอดสะสม
- **Tag:** FIXED

### BR-PR-07: Route lock
- **Statement:** route=`po_direct` → ล็อก PR (CP อ้างไม่ได้); เปลี่ยน route หลัง lock ไม่ได้
- **Enforced by:** F-PR-FN-10 · **Error:** `BR_ROUTE_LOCKED` 422 · **Tag:** FIXED

### BR-PR-08: สายอนุมัติจาก DOA
- **Statement:** จำนวนชั้น/ผู้อนุมัติ = ผลจาก `doa-resolver({feature_id, cost_center, amount})` — **ไม่ hardcode**
- **Used by:** F-PR-FN-06 → ENG-DOA · **Tag:** DYNAMIC (DOA Engine)

### BR-PR-09: SoD
- **Statement:** ผู้ขอ (Maker) ≠ ผู้อนุมัติ (Approver)
- **Enforced by:** F-PR-FN-06 (block ถ้า resolver คืนผู้อนุมัติ = ผู้ขอ) · **Error:** `BR_SOD_VIOLATION` 422 · **Tag:** FIXED (COSO)

### BR-PR-10: Reject ต้องมีเหตุผล
- **Statement:** ตีกลับต้องระบุ `reason`
- **Enforced by:** F-PR-FN-08 · **Error:** `BR_REJECT_REASON_REQUIRED` 422 · **Tag:** FIXED

### BR-PR-11: Vendor optional
- **Statement:** `vendor_id` เว้นได้ที่ PR (เลือกขั้น CP/PO) · **Tag:** FIXED

### BR-PR-12: emit event เมื่อ approved
- **Statement:** PR ครบสายอนุมัติ → emit `procurement.pr_linked {releaseRef, docNo, amount, source}` → Budget 3-stage committed
- **Enforced by:** F-PR-FN-07 → ENG-BUDGET (commit) · **Tag:** FIXED (integration) · contract = OQ-02

### BR-PR-13: ไม่มี Payment Term ที่ PR
- **Statement:** PR ไม่มี payment term — เลือกที่ PO เท่านั้น (P2P D01)
- **Tag:** FIXED (LD-02)

### BR-PR-14: เลขที่ PR
- **Statement:** `pr_no` = PR-YYMM-NNNNN จาก Document Numbering (Purchase Config)
- **Tag:** CONFIGURABLE (Admin Panel)

---

## §5.2 State Machine

```
   ┌───────┐  submit   ┌─────────┐  approve(ครบสาย)  ┌──────────┐
   │ draft │──────────►│ pending │──────────────────►│ approved │──► (route → CP/PO)
   └───┬───┘           └────┬────┘                   └────┬─────┘
       │ cancel             │ reject(reason)              │ cancel(reverse committed)
       ▼                    ▼                             ▼
  ┌──────────┐        ┌──────────┐                  ┌──────────┐
  │cancelled │        │ rejected │──revise──► draft │cancelled │
  └──────────┘        └──────────┘                  └──────────┘
```

| From | To | Action | Allowed roles | Conditions |
|---|---|---|---|---|
| draft | pending | submit | requester | valid + hard control + DOA resolve |
| draft | cancelled | cancel | requester | — |
| pending | approved | approve | approver (current step) | chain ครบ |
| pending | rejected | reject | approver | reason required |
| pending | cancelled | cancel | requester | — |
| rejected | draft | revise | requester | — |
| approved | cancelled | cancel | approver | reverse committed budget |

> Enforced by F-PR-FN-06/07/08/09/10 (ดู 03_LOGIC §3.1)

---

## §5.3 Permission Matrix

| Role | View | Create | Edit | Submit | Approve | Reject | Cancel | Set Route |
|---|---|---|---|---|---|---|---|---|
| ผู้ขอซื้อ (requester) | own/all* | ✅ | own (draft/rejected) | ✅ | — | — | ✅ (ก่อนอนุมัติ) | — |
| checker | all | — | — | — | (ชั้น checker) | — | — | — |
| approver | all | — | — | — | ✅ | ✅ | ✅ (หลังอนุมัติ) | — |
| buyer | all | — | — | — | — | — | — | ✅ |
| admin | all | — | — | — | — | — | — | — |

*scope ตาม User Access ENC

---

## §5.4 Field Validation Rules

| Field | Rule | Error code |
|---|---|---|
| `branch_id` | required, active | `BR_BRANCH_REQUIRED` |
| `requester_id` | required, active | `BR_REQUESTER_REQUIRED` |
| `need_date` | ≥ pr_date | `BR_NEED_DATE_INVALID` |
| `lines` | ≥ 1 valid | `BR_EMPTY_LINES` |
| `qty` / `unit_price` | > 0 | `BR_INVALID_QTY_PRICE` |
| `discount_pct` | 0–100 | `BR_DISCOUNT_RANGE` |
| `release_ref` | required เมื่อ require_unlock_ref=true | `BR_RELEASE_REF_REQUIRED` |
| `subtotal/vat/grand` | computed (not user input) | — |

**Cross-field:** `grand_total` = subtotal − endbill_discount + vat_total (ENG-DOC-AMT) · `approved_at ≥ submitted_at ≥ created_at` (DB constraint + state machine)

---

## §5.5 Edge Cases (Phase 2.5 Probing)

### EC-01: Over-budget (PR-9 budget guard)
- **Scenario:** Σ PR + ใบนี้ > งบคงเหลือ
- **Resolution:** F-PR-FN-06 → ENG-BUDGET check → block submit
- **Error:** `BR_OVER_BUDGET` · **Test:** TC-BG-01

### EC-02: Config ปิด require_unlock_ref
- **Scenario:** Purchase Config.require_unlock_ref=false
- **Resolution:** ซ่อน section ใบปลดอายัด + ไม่บังคับ release_ref · **Test:** TC-CFG-01

### EC-03: po_direct lock (PR-5 state)
- **Scenario:** route=po_direct แล้วพยายามอ้างใน CP / เปลี่ยน route
- **Resolution:** F-PR-FN-10 block · **Error:** `BR_ROUTE_LOCKED` · **Test:** TC-RT-01

### EC-04: Concurrent edit / approve (PR-1)
- **Scenario:** 2 users แก้/อนุมัติ PR เดียวกัน
- **Resolution:** optimistic lock `version` + `If-Match` → first wins, second 409 · **Error:** `ERR_STALE_DATA` · **Test:** TC-CC-01

### EC-05: Concurrent budget commit (PR-1 + PR-9) ⭐
- **Scenario:** 2 PR ผูก release เดียวกัน submit/approve พร้อมกัน → อาจ over-commit
- **Resolution:** ENG-BUDGET atomic decrement (lock/serializable) — **strategy = OQ-01**
- **Test:** TC-BG-02

### EC-06: Idempotency (PR-7)
- **Scenario:** double-click ส่ง/บันทึก
- **Resolution:** Idempotency-Key → cached (24h) · **Error:** `ERR_DUPLICATE_IDEMPOTENCY_KEY` (ถ้า body ต่าง) · **Test:** TC-ID-01

### EC-07: Master ถูก deactivate หลังเลือก (PR-3 data integrity)
- **Scenario:** branch/release/product/vendor ถูกปิดหลังเลือก
- **Resolution:** re-validate ตอน submit → เตือน + บังคับเลือกใหม่ · **Error:** `BR_REFERENCE_INACTIVE` · **Test:** TC-DI-01

### EC-08: VAT included rounding (PR calc)
- **Scenario:** vat_mode=included → back-calc VAT
- **Resolution:** ENG-DOC-AMT ใช้ ROUND_HALF_UP (ยืนยัน OQ-04) · **Test:** TC-VAT-01

### EC-09: Cancel หลัง approved
- **Scenario:** ยกเลิก PR ที่ approved แล้ว
- **Resolution:** F-PR-FN-09 → ENG-BUDGET reverse committed (compensating) · **Test:** TC-CN-01

---

## §5.6 Error Catalog

| Code | HTTP | Message (i18n key) | Cause |
|---|---|---|---|
| `ERR_VALIDATION_FAILED` | 400 | error.validation.failed | generic |
| `ERR_NOT_AUTHENTICATED` | 401 | error.auth.unauth | no/invalid token |
| `ERR_INSUFFICIENT_ROLE` | 403 | error.auth.role | role mismatch |
| `ERR_NOT_CURRENT_APPROVER` | 403 | error.approve.notcurrent | ไม่ใช่ชั้นปัจจุบัน |
| `ERR_NOT_FOUND` | 404 | error.notfound | resource missing |
| `ERR_DUPLICATE_IDEMPOTENCY_KEY` | 409 | error.idempotency.dup | same key diff body |
| `ERR_STALE_DATA` | 409 | error.concurrency.stale | version mismatch |
| `BR_BRANCH_REQUIRED` | 422 | br.branch.required | BR validation |
| `BR_REQUESTER_REQUIRED` | 422 | br.requester.required | — |
| `BR_EMPTY_LINES` | 422 | br.lines.empty | — |
| `BR_INVALID_QTY_PRICE` | 422 | br.qtyprice.invalid | — |
| `BR_DISCOUNT_RANGE` | 422 | br.discount.range | — |
| `BR_RELEASE_REF_REQUIRED` | 422 | br.release.required | BR-PR-04 |
| `BR_OVER_BUDGET` | 422 | br.budget.over | BR-PR-05 |
| `BR_SOD_VIOLATION` | 422 | br.sod | BR-PR-09 |
| `BR_ROUTE_LOCKED` | 422 | br.route.locked | BR-PR-07 |
| `BR_REJECT_REASON_REQUIRED` | 422 | br.reject.reason | BR-PR-10 |
| `BR_CANCEL_NOT_ALLOWED` | 422 | br.cancel.notallowed | state |
| `BR_REFERENCE_INACTIVE` | 422 | br.ref.inactive | EC-07 |
| `ENG_ERR_CALCULATION_FAILED` | 500 | error.engine.calc | ENG-DOC-AMT |

---

## §5.7 Security Bible Application

> Domains triggered: **D2, D5, D7, D9, D15, D17**

### D2: Authentication & Session
- ทุก endpoint require JWT · token TTL 1h · refresh 7d · ผ่าน User Access ENC

### D5: Financial Transactions
- ทุก amount change → audit log (before/after) · approval workflow ผ่าน DOA · Hard Control งบ (BR-PR-05)

### D7: PII Protection
- `requester`/`requester_id` = PII → mask ตาม role · logs ใช้ ID reference · PDPA scope

### D-CLASS: Data Classification ⭐ (v5.1)
> Per-field รายละเอียดที่ 04_DB §4.2 + §4.6

**Enforcement summary:**
| Layer | Confidential (requester/release/vendor) | Restricted (ราคา/ยอด) |
|---|---|---|
| API response | mask if no permission | excluded ถ้าไม่ผ่าน ACL |
| UI display | `***` | hidden + audit access |
| Export/PDF | excluded ถ้า role ไม่ผ่าน | require Restricted Resources approval (F-PR-API-10) |
| Audit | view + mutation | view + mutation + export |

**Wire points:** Policy Center → Data Classification · Restricted Resources · DOA (downgrade approval)

### D9: Audit Logging
- ทุก mutation + state transition → T_audit_log (append-only, 7 ปี)

### D15: Admin Actions
- ทุก state transition logged · approver identity recorded · reason required (reject/cancel)

### D17: Multi-Tenant Isolation
- PostgreSQL RLS · middleware validate X-Tenant-Id · ห้าม cross-tenant

---

## §5.8 Compliance & Audit
| Requirement | Implementation |
|---|---|
| คุมงบประมาณ (over-budget) | BR-PR-05 Hard Control |
| SoD / อำนาจอนุมัติ | BR-PR-09 + DOA |
| Audit trail | D9 + T_audit_log |
| PDPA (ผู้ขอ) | D7 mask + retention |
| Governance | User Access ENC + DOA ENC ก่อน deploy |
