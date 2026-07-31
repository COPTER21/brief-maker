# 06_TESTS — F-PR-001 ใบขอซื้อ (Purchase Requisition)

> **Audience:** QA engineer
> **Purpose:** Acceptance Criteria + Definition of Done + WebSocket events
> **Coverage source:** 02_API contracts + 03_LOGIC functions + 05_RULES edge cases

---

## §6.1 Acceptance Criteria (AC)

### AC-01: List PR + filters
**Given** role = ผู้ขอซื้อ, tenant มี 5 PR (mix สถานะ/สาขา)
**When** GET /purchase-requisitions?status=draft&branch_id=HQ
**Then** 200 + เฉพาะ draft ของสาขา HQ **And** response < 500ms

### AC-02: Create PR — happy path
**Given** สาขา + ผู้ขอ + รายการ valid (+ ใบปลดอายัดถ้า config บังคับ)
**When** POST /purchase-requisitions (+ Idempotency-Key)
**Then** 201, status=draft **And** gen pr_no PR-YYMM-NNNNN **And** subtotal/vat/grand คำนวณถูกโดย ENG-DOC-AMT **And** audit log created

### AC-03: Create — ไม่เลือกสาขา
**When** POST ไม่มี branch_id
**Then** 422 `BR_BRANCH_REQUIRED`

### AC-04: Create — config บังคับใบปลดอายัด แต่ไม่ใส่
**Given** Purchase Config.require_unlock_ref=true
**When** POST ไม่มี release_ref
**Then** 422 `BR_RELEASE_REF_REQUIRED`

### AC-05: Submit — over-budget (EC-01)
**Given** Σ PR + ใบนี้ > งบคงเหลือ
**When** POST /:id/submit
**Then** 422 `BR_OVER_BUDGET` **And** status ยังเป็น draft

### AC-06: Submit — happy path + DOA resolve
**Given** draft valid, งบพอ
**When** POST /:id/submit
**Then** 200 status=pending **And** approval_chain ถูก resolve จาก doa-resolver **And** ผู้อนุมัติชั้นแรกได้ notification

### AC-07: Submit — SoD violation (BR-PR-09)
**Given** resolver คืนผู้อนุมัติ = ผู้ขอเดียวกัน
**When** submit
**Then** 422 `BR_SOD_VIOLATION`

### AC-08: Approve — ครบสาย → committed + event
**Given** PR pending, ผู้อนุมัติชั้นสุดท้าย
**When** POST /:id/approve
**Then** status=approved **And** emit `procurement.pr_linked` **And** Budget committed (3-stage) **And** approved_at/by set

### AC-09: Approve — ไม่ใช่ชั้นปัจจุบัน
**When** approve โดย user ที่ไม่ใช่ current step
**Then** 403 `ERR_NOT_CURRENT_APPROVER`

### AC-10: Reject — ไม่มีเหตุผล
**When** POST /:id/reject body ว่าง
**Then** 422 `BR_REJECT_REASON_REQUIRED`

### AC-11: Set route po_direct → lock (EC-03)
**Given** PR approved
**When** POST /:id/route {route: po_direct} แล้วพยายามเปลี่ยน/อ้าง CP
**Then** route=po_direct **And** ครั้งที่ 2 → 422 `BR_ROUTE_LOCKED`

### AC-12: Concurrent edit (EC-04)
**Given** 2 users PUT PR เดียวกัน (If-Match เก่า)
**When** ส่งพร้อมกัน
**Then** first 200, second 409 `ERR_STALE_DATA`

### AC-13: Idempotency (EC-06)
**Given** Idempotency-Key X + body Y, cached
**When** ส่ง X+Y ซ้ำใน 24h
**Then** response เดิม (ไม่ INSERT ซ้ำ ไม่มี audit ซ้ำ)

### AC-14: VAT included rounding (EC-08)
**Given** line vat_mode=included, vat_pct=7
**When** คำนวณ
**Then** VAT back-calc = line_net − line_net/1.07 (ROUND_HALF_UP) **And** grand_total ถูกต้อง

### AC-15: Cancel หลัง approved → reverse (EC-09)
**Given** PR approved (งบ committed)
**When** POST /:id/cancel (approver)
**Then** status=cancelled **And** Budget committed ถูก reverse

### AC-16: PDF render
**Given** PR ใด ๆ + role ผ่าน ACL
**When** GET /:id/pdf
**Then** application/pdf A4 **And** signature slots = N ชั้นจาก approval_chain **And** branch ship-to + org/logo ถูกต้อง **And** audit export (Restricted)

### AC-17: Multi-unit price (UI/logic)
**Given** สินค้าหลายหน่วย (ราคาต่างกัน)
**When** เปลี่ยนหน่วยในบรรทัด
**Then** unit_price อัปเดตตามหน่วย **And** line_amount recalc

---

## §6.2 Test Case Inventory

| TC ID | Name | Type | Maps to | Priority |
|---|---|---|---|---|
| TC-01 | List + filters | API | AC-01 | P0 |
| TC-02 | Create happy | API | AC-02 | P0 |
| TC-03 | Create no branch | API neg | AC-03 | P1 |
| TC-CFG-01 | release_ref gating (on/off) | API | AC-04, EC-02 | P1 |
| TC-BG-01 | Over-budget block | API neg | AC-05 | P0 |
| TC-BG-02 | Concurrent budget commit | stress | EC-05 | P1 |
| TC-04 | Submit + DOA resolve | API | AC-06 | P0 |
| TC-SOD-01 | SoD violation | API neg | AC-07 | P1 |
| TC-AP-01 | Approve chain → committed + event | API/integration | AC-08 | P0 |
| TC-AP-02 | Approve wrong step | API neg | AC-09 | P2 |
| TC-RJ-01 | Reject no reason | API neg | AC-10 | P1 |
| TC-RT-01 | Route lock | API | AC-11, EC-03 | P1 |
| TC-CC-01 | Concurrent edit | stress | AC-12, EC-04 | P1 |
| TC-ID-01 | Idempotency | API | AC-13, EC-06 | P0 |
| TC-VAT-01 | VAT included rounding | unit (ENG-DOC-AMT) | AC-14, EC-08 | P1 |
| TC-CN-01 | Cancel reverse budget | integration | AC-15, EC-09 | P1 |
| TC-PDF-01 | PDF render + signatures | E2E | AC-16 | P1 |
| TC-DI-01 | Reference inactive | API neg | EC-07 | P2 |
| TC-UI-01 | Multi-unit price switch | UI/E2E | AC-17 | P1 |
| TC-PERF-01 | List 1000 records < 1s | perf | AC-01 | P1 |

---

## §6.3 Test Data Setup
- 3 tenants (isolated) · 3 สาขา (00000/00001/00002)
- 6 employees (active/inactive mix) · 9 products (multi-unit + vat_group)
- 2 budget releases (1 งบเหลือมาก / 1 ใกล้เต็ม) สำหรับทดสอบ over-budget
- 5 PR เริ่มต้น (mix draft/pending/approved/rejected/cancelled)
- roles: qa_requester, qa_approver (multi-step), qa_buyer, qa_finance, qa_admin

---

## §6.4 Definition of Done (DoD)

### Code
- [ ] ทุก AC implemented + unit tests pass (รวม ENG-DOC-AMT calc cases)
- [ ] Integration tests pass (API + DB + ENG-BUDGET + ENG-DOA)
- [ ] E2E happy + critical edges (over-budget, route lock, concurrent)
- [ ] Code review approved · coverage ≥ 80% logic layer
- [ ] ไม่มี critical/high security findings

### Documentation
- [ ] API docs (จาก 02_API) · changelog
- [ ] 07_LOCKED_DECISIONS สะท้อน design จริง
- [ ] CUBIC: ENG-DOC-AMT registered (จาก §3.2)

### QA
- [ ] P0 + P1 ผ่านครบ · ไม่มี P0/P1 bug ค้าง
- [ ] Performance benchmark ผ่าน
- [ ] Security checklist (D2/D5/D7/D9/D15/D17 + D-CLASS) verified

### Deployment
- [ ] Migration tested ใน staging
- [ ] **Governance: User Access ENC + DOA ENC checkpoints ผ่าน**
- [ ] Monitoring dashboards updated (PR vs Budget, PR aging)
- [ ] Rollback plan documented

---

## §6.5 WebSocket Events

### `pr_submitted`
- **Trigger:** F-PR-API-05 submit สำเร็จ
- **Channel:** `tenant:<tenant_id>:approvers`
- **Payload:** `{ event, payload: { pr_id, pr_no, submitted_by, submitted_at } }`
- **Test:** Approver inbox อัปเดตไม่ต้อง refresh

### `pr_approved`
- **Trigger:** F-PR-API-06 approve ครบสาย
- **Channel:** `tenant:<tenant_id>:requester:<id>` + `:buyers`
- **Payload:** `{ event, payload: { pr_id, pr_no, approved_at } }`

### `pr_rejected`
- **Trigger:** F-PR-API-07
- **Channel:** `tenant:<tenant_id>:requester:<id>`
- **Payload:** `{ event, payload: { pr_id, reason } }`
