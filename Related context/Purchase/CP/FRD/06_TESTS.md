# 06_TESTS — F-CP-001 เปรียบเทียบราคา (Price Comparison)

> **Audience:** QA engineer
> **Purpose:** Acceptance Criteria + Definition of Done + WebSocket events
> **Coverage source:** 02_API + 03_LOGIC + 05_RULES edge cases

---

## §6.1 Acceptance Criteria (AC)

### AC-01: List CP + filter
**Given** role=buyer, tenant มี 4 CP
**When** GET /comparisons?status=approved
**Then** 200, คืนเฉพาะ status=approved · response < 500ms

### AC-02: สร้าง CP (happy)
**Given** PR approved+route=cp + ผู้ขาย 3 ราย + ราคาครบ + เลือกผู้ชนะครบ
**When** POST /comparisons (save_mode=draft) + Idempotency-Key
**Then** 201, status=draft, gen cp_no, winner_total = Σ winner (ENG-01), po_count = distinct winner vendor (ENG-02), audit log created

### AC-03: สร้าง CP — ไม่มี PR
**Given** pr_refs = []
**When** POST /comparisons
**Then** 422 BR_CP_PR_REQUIRED

### AC-04: เติมราคา preset จาก price list (BR-CP-04)
**Given** เข้าขั้นเทียบราคา, ผู้ขายมีราคาใน Vendor Price List
**When** applyPriceList (ENG-03)
**Then** เซลล์ว่างถูกเติม is_preset=true · เซลล์ที่แก้เองไม่ถูกทับ

### AC-05: เลือกผู้ชนะอัตโนมัติ = ราคาต่ำสุด (BR-CP-05)
**Given** 3 ผู้ขายเสนอราคาต่างกันต่อ line
**When** autoWinners (ENG-01)
**Then** winner = lowest unit_price ต่อ line · ป้าย "ต่ำสุด" ตรง · winner_total ถูกต้อง

### AC-06: PO Split ตามผู้ชนะ (BR-CP-06)
**Given** 3 lines: line1,3 ชนะ V-001, line2 ชนะ V-003
**When** ENG-02 po-split
**Then** 2 splits — V-001 (2 รายการ, subtotal=9,050), V-003 (1 รายการ, subtotal=4,650), po_count=2

### AC-07: ส่งเซ็น (submit) — happy
**Given** CP draft, ผู้ขาย ≥ 2, ผู้ชนะครบ
**When** POST /:id/submit
**Then** status=pending, submitted_at set, DOA chain resolved (ENG-04), approver ได้ notification

### AC-08: ส่งเซ็น — ผู้ชนะไม่ครบ (EC-08)
**Given** บาง line ไม่มีผู้ชนะ
**When** POST /:id/submit
**Then** 422 BR_CP_WINNER_INCOMPLETE

### AC-09: อนุมัติ — concurrent (EC-01)
**Given** 2 approver กดอนุมัติพร้อมกัน
**When** ทั้งคู่ถึง API ภายใน 100ms
**Then** คนแรก 200, คนสอง 409 ERR_STALE_DATA

### AC-10: ตีกลับ (reject)
**Given** CP pending
**When** POST /:id/reject {reject_reason}
**Then** status=draft, reject_reason บันทึก, maker ได้ notification + เหตุผล · ถ้าไม่มีเหตุผล → 400 ERR_REASON_REQUIRED

### AC-11: ออกใบสั่งซื้อ (award) — happy (BR-CP-07)
**Given** CP approved, 2 splits
**When** POST /:id/award + Idempotency-Key
**Then** status=awarded, F-PO-001 สร้าง PO 2 ใบ, po_id เติมครบใน po_split, "สร้าง PO แล้ว 2/2"

### AC-12: award — idempotent (EC-06)
**Given** CP awarded แล้ว
**When** POST /:id/award ซ้ำ (key เดิม)
**Then** คืน po_splits เดิม, ไม่สร้าง PO ซ้ำ

### AC-13: award — PO fail บางใบ (EC-07)
**Given** F-PO-001 สร้างใบที่ 2 fail
**When** POST /:id/award
**Then** rollback (all-or-nothing), status คง approved, 502 ERR_PO_CREATE_FAILED

### AC-14: PDF เอกสาร (API-10)
**Given** CP ใด ๆ
**When** GET /:id/document
**Then** 200 application/pdf, A4, แสดงตารางเทียบ + ผู้ชนะ + winner_total + VAT + grand_total + baht text + ลายเซ็น 3 ช่อง

### AC-15: Data Classification masking (D-CLASS)
**Given** role ไม่ใช่ procurement/finance
**When** GET /comparisons/:id
**Then** ราคา/หน่วย + winner_total ถูก mask (`***`) · export ตัดคอลัมน์ราคา

---

## §6.2 Test Case Inventory

| TC ID | Name | Type | Maps to AC | Priority |
|---|---|---|---|---|
| TC-01 | List + filter | API | AC-01 | P0 |
| TC-02 | สร้าง CP happy | API | AC-02 | P0 |
| TC-03 | สร้าง — ไม่มี PR | API neg | AC-03 | P1 |
| TC-PL-01 | เติม preset เฉพาะช่องว่าง | Logic | AC-04, EC-04 | P1 |
| TC-WN-01 | autoWinners ต่ำสุด | Logic | AC-05 | P0 |
| TC-SP-01 | PO split group by winner | Logic | AC-06 | P0 |
| TC-04 | submit happy | API | AC-07 | P0 |
| TC-SB-01 | submit winner ไม่ครบ | API neg | AC-08, EC-08 | P1 |
| TC-CC-01 | concurrent approve | API stress | AC-09, EC-01 | P1 |
| TC-RJ-01 | reject + reason | API | AC-10 | P1 |
| TC-AW-01 | award happy + po_id | API | AC-11 | P0 |
| TC-ID-01 | idempotent create/submit | API | EC-02 | P0 |
| TC-AW-02 | award idempotent / partial fail | API | AC-12,13, EC-06,07 | P1 |
| TC-PR-01 | PR used หลังเลือก | API neg | EC-03 | P2 |
| TC-VN-01 | เพิ่ม/ลบ vendor กลางคัน | Logic/UI | EC-05 | P2 |
| TC-DOC-01 | PDF render ครบ | E2E | AC-14 | P1 |
| TC-DC-01 | classification masking | API/UI | AC-15 | P1 |
| TC-UI-01 | wizard 4 ขั้น render + footer | UI/E2E | P-02 | P1 |
| TC-PERF-01 | List 1000 CP < 1s | Perf | AC-01 | P1 |

---

## §6.3 Test Data Setup
- 3 tenants (isolated)
- PR: 4 ใบ (approved+route=cp ใช้ได้ 3, po_direct 1 ใช้ไม่ได้)
- Vendor: 5 ราย (V-001..V-005) + Vendor Price List ครอบ PPR-A4/INK-12A/OFS-001/BOX-S/FLR-25/CCO-1
- CP seed: draft / pending / approved / awarded อย่างละ 1
- Roles: qa_buyer, qa_proc_manager, qa_approver, qa_finance

---

## §6.4 Definition of Done (DoD)

### Code
- [ ] ทุก AC implement + unit tests pass
- [ ] Integration (API+DB+Engine) pass
- [ ] E2E happy + EC-01/06/07/08 pass
- [ ] Code review approved
- [ ] No critical/high security findings
- [ ] Coverage ≥ 80% logic layer

### Documentation
- [ ] API docs published (จาก 02_API)
- [ ] CUBIC Registry: ENG-01 price-comparison-winner + ENG-02 po-split registered (LD-02)
- [ ] FRD §07 reflects final design

### QA
- [ ] P0+P1 pass · no P0/P1 bug open
- [ ] Perf benchmark met
- [ ] Security checklist (D2/D5/D9/D15/D17/D-CLASS) verified

### Deployment
- [ ] Migration tested (staging) · 5 CP tables + RLS
- [ ] **User Access ENC + DOA ENC checkpoints ผ่าน** (CUBE 4.0 mandatory ก่อน deploy)
- [ ] Monitoring + rollback plan

---

## §6.5 WebSocket Events

### `cp_submitted`
- **Trigger:** API-05 submit · **Channel:** `tenant:<id>:approvers`
- **Payload:** `{ comparison_id, cp_no, submitted_by, winner_total }`
- **Test:** approver dashboard อัปเดตไม่ต้อง refresh

### `cp_approved` / `cp_rejected`
- **Trigger:** API-06 / API-07 · **Channel:** `tenant:<id>:user:<maker_id>`
- **Test:** maker เห็น toast + สถานะเปลี่ยน

### `cp_awarded`
- **Trigger:** API-08 · **Channel:** `tenant:<id>:procurement`
- **Payload:** `{ comparison_id, po_ids[] }` · **Test:** เห็น po_id ใน tab แยก PO

---

## §6.6 Performance Benchmarks

| Endpoint | P95 | Throughput |
|---|---|---|
| GET /comparisons | < 500ms | 200 req/s |
| GET /comparisons/:id (matrix) | < 400ms | 300 req/s |
| POST /comparisons | < 1000ms | 50 req/s |
| POST /:id/award | < 1500ms (รวมเรียก PO) | 30 req/s |
| GET /:id/document (PDF) | < 2500ms | 10 req/s |

---

## §6.7 Test Environment Notes
- staging tenant `tenant-test-001`
- F-PO-001 createPurchaseOrder = mock (deterministic po_id) สำหรับ award tests
- ENG-04 doa-resolver = TEST matrix (fixed chain)
- DB seed: `seed_cp_test_data.sql`

---

## §6.8 Trace: AC → Logic Coverage

| AC | API | Functions | Engines |
|---|---|---|---|
| AC-01 | API-01 | FN-04 | — |
| AC-02 | API-03 | FN-01, FN-03 | ENG-01, ENG-02, ENG-03 |
| AC-03 | API-03 | FN-01 (neg) | — |
| AC-04 | (logic) | FN-01/02 | ENG-03 |
| AC-05 | (logic) | — | ENG-01 |
| AC-06 | (logic) | — | ENG-02 |
| AC-07 | API-05 | FN-05, FN-06 | ENG-04 |
| AC-08 | API-05 | FN-05 (neg) | — |
| AC-09 | API-06 | FN-07 | — |
| AC-10 | API-07 | FN-08 | — |
| AC-11 | API-08 | FN-09 | ENG-02 |
| AC-12 | API-08 | FN-09 (idempotent) | — |
| AC-13 | API-08 | FN-09 (rollback) | ENG-02 |
| AC-14 | API-10 | FN-11 | ENG-02 |
| AC-15 | API-02/09 | FN-04, FN-10 | — |

> **Coverage check:** FN-01..11 + ENG-01..04 ถูก trace ครบ ≥ 1 AC ✅
