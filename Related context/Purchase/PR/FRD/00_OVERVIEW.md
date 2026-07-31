# 00_OVERVIEW — F-PR-001 ใบขอซื้อ (Purchase Requisition)

> **Audience:** All roles (PM, BA, FE, BE, QA, DBA)
> **Purpose:** Document Control + Scope + Roles + Dependencies + Open Questions

---

## §0.1 Document Control

| Field | Value |
|---|---|
| **Feature ID** | F-PR-001 |
| **Feature Name** | ใบขอซื้อ (Purchase Requisition) |
| **Feature Code** | F-PR-001 (scope-local prefix: `F-PR`) |
| **Module** | Procurement (Value Stream: P2P) |
| **Variant** | FULL (9 files + INDEX) |
| **Status** | DRAFT |
| **FRD Version** | 1.0 (2026-06-06) |
| **Generator** | frd-generator-v5 (v5.1) |
| **Source Brief** | — (ไม่มี Brief แยก — สังเคราะห์จาก HTML prototype + FRD packs context) |
| **Source BRD** | BRD_purchase_requisition.md (BRD-PR-001, status: AI Reviewed/APPROVED, 2026-06-06) |
| **Author** | Tadswan C. (BA) |
| **Reviewers** | Bird (Tech Lead/BE), Strike (Dev), Chin (UI) |

---

## §0.2 Revision History

| Version | Date | Author | Changes |
|---|---|---|---|
| 1.0 | 2026-06-06 | Tadswan C. | Initial FRD generation (FULL) จาก BRD-PR-001 |

---

## §0.3 Scope

### In Scope
- สร้าง/แก้/ดู/ยกเลิก ใบขอซื้อ (Header + Lines + Attachment)
- ผูกใบปลดอายัดงบ (release_ref) + Hard Control เพดานงบสะสม (1 ใบปลดอายัด : หลาย PR)
- ดึงสินค้าจาก Product Master (รหัสสั้น, หลายหน่วย/หลายราคา, autofill ราคา + VAT group)
- ผู้ขอ (Employee), สาขาปลายทาง (Branch จาก Organization, บังคับ), ผู้ขาย (optional)
- คำนวณยอด: VAT ต่อบรรทัด (none/add/included) + WHT + ส่วนลดท้ายบิล
- เส้นทางจัดซื้อ (route): PR→CP หรือ PR→PO ตรง (po_direct ล็อก PR)
- ส่งสายอนุมัติผ่าน DOA engine (จำนวนชั้น/ผู้อนุมัติ = ผลจาก chain)
- เอกสาร PDF ใบขอซื้อ (A4) + preview

### Out of Scope
- Payment Term — เลือกที่ PO เท่านั้น (LD-02 / BR-PR-13) — reason: P2P design D01
- CP / PO / GRN — feature แยกในสาย P2P
- การจัดการ master (Product/Budget/Organization/DOA) — PR แค่อ้างอิง
- Direct Payment (bypass PR/PO)

---

## §0.4 Roles & Responsibilities (COSO)

| Role | Person/Team | Responsibilities |
|---|---|---|
| **Maker** | ผู้ขอซื้อ (Requester) | สร้าง draft / submit |
| **Checker** | หัวหน้าแผนก (ถ้า DOA chain มีชั้น checker) | ตรวจก่อนอนุมัติ |
| **Approver** | ผู้อนุมัติตามสาย DOA (N ชั้น) | อนุมัติ / ตีกลับ |
| **Owner** | แผนกจัดซื้อ (Buyer) | รับ PR อนุมัติแล้ว เลือก route → CP/PO |

> รายละเอียดต่อ workflow → ดู `01_UI.md §1.3 Journey` + `05_RULES.md §5.2 State Machine`

---

## §0.5 Dependencies

### Upstream (this feature depends on)
| Dependency | Type | Source |
|---|---|---|
| Product Master | Data/API | F-PRODUCT-MASTER-001 (item_code, units[], purchase_price, vat_group) |
| Employee Master | Data/API | HR module (requester lookup) |
| Organization → Branch | Data/API | F-ORG-001 (branch_id, ship-to address) |
| Budget Release | Data/API/Engine | F-BGT-REQ-001 (release_ref, งบคงเหลือ, hard control + commit) |
| DOA Engine | Engine | F-PC-DOA-01 (`doa-resolver` — approval chain) |
| Purchase Config | Config | F-PURCH-CFG-001 (`require_unlock_ref`, doc numbering) |
| Document Numbering | Service | Purchase Config (เลขที่ PR) |

### Downstream (features that depend on this)
| Consumer | What it uses |
|---|---|
| CP (Compare Price) | อ้าง PR ที่ approved + route=cp |
| PO (Purchase Order) | สร้างจาก PR (cp หรือ po_direct) |
| Budget 3-stage tracking | event `procurement.pr_linked` → committed |

### External
| Service | Purpose |
|---|---|
| Notification service | แจ้งสายอนุมัติ |
| PDF render (Chromium/Gotenberg + Sarabun) | เอกสาร PDF A4 (thai-doc-pdf-generator) |
| Audit Log service | audit trail |

---

## §0.6 Stack & Architecture

| Layer | Technology |
|---|---|
| Frontend | single-file SPA prototype → React/Next + Tailwind (dev) |
| API | Node.js / Strapi (CUbe) |
| Database | PostgreSQL (RLS multi-tenant) |
| Engine layer | CUBIC Registry (doc-amount-engine NEW; doa-resolver + budget-availability-engine EXISTING) |
| Auth | JWT + role-based (User Access ENC) |

---

## §0.7 Multi-Tenant & Security Context

- [x] Multi-tenant feature: YES (RLS by tenant)
- [x] PII data involved: YES (requester = employee data)
- [x] Financial data: YES (amounts, budget, prices)
- [x] Audit log required: YES

**Security Bible domains applied:** D2 (Auth), D5 (Financial), D7 (PII), D9 (Audit), D15 (Admin Actions), D17 (Multi-Tenant) — see 05_RULES §5.7

### §0.7.1 Data Classification Summary (v5.1)

Highest classification level ที่ feature นี้แตะ:
- [x] **Has Restricted fields** — `unit_price`, `subtotal`, `vat_total`, `grand_total`, `line_amount` (purchase price / amounts)
- [x] Has Confidential fields — `requester`, `release_ref`/`budget_code` (งบ), `vendor_id`
- [x] Internal (default) — ส่วนใหญ่
- [ ] Public-facing data

**Linkage:** Restricted fields ต้อง register ที่ Policy Center → Restricted Resources (ดู 04_DB §4.6.6) — ดู OQ-05

---

## §0.8 Open Questions

| ID | Question | Blocking? | Owner |
|---|---|---|---|
| OQ-01 | Atomic budget commit strategy (กัน race เมื่อหลาย PR ผูก release เดียวกัน — EC-05) | YES | Bird/Strike |
| OQ-02 | Contract ของ event `procurement.pr_linked` ↔ budget 3-stage ตรงกับฝั่ง Budget? | YES | ทีม Budget |
| OQ-03 | DOA chain ของ PR — by_department หรือ by_amount tiers? (รอ DOA wire Phase 3) | NO | Admin/ผู้บริหาร |
| OQ-04 | VAT included → back-calc ปัดเศษแบบไหน (ROUND_HALF_UP?) | NO | Finance |
| OQ-05 | Restricted fields (ราคา/ยอด) wire กับ Restricted Resources registry แล้วหรือยัง | NO | Policy Center owner |

> Resolved → move to 07_LOCKED_DECISIONS as LD-NN

---

## §0.9 Glossary

| Term | Definition |
|---|---|
| PR | Purchase Requisition (ใบขอซื้อ) — entry ของ P2P |
| ใบปลดอายัด / release_ref | Budget Release — ปลดวงเงินงบมาใช้ซื้อ (1:M กับ PR) |
| Hard Control | กฎ block ไม่ให้ PR สะสมเกินงบคงเหลือ |
| DOA | Delegation of Authority (สายอำนาจอนุมัติ) |
| route (cp/po_direct) | เส้นทางจัดซื้อหลัง PR |
| Branch | สาขาในองค์กร (ปลายทางรับสินค้า) |

---

## §0.10 Pack Navigation

| File | Audience | Purpose |
|---|---|---|
| 00_OVERVIEW.md | All | meta + scope |
| 01_UI.md | FE dev | Pages + Components + Journey |
| 02_API.md | BE dev (HTTP) | API contracts |
| 03_LOGIC.md | BE dev (logic) | Functions + Engines + Trace |
| 04_DB.md | DBA / BE | Tables + Fields + Classification |
| 05_RULES.md | BE + QA | Rules + Edge Cases + Errors |
| 06_TESTS.md | QA | Acceptance + DoD |
| 07_LOCKED_DECISIONS.md | All | LDs + Convention deviations |
| INDEX.md | All | Cross-reference quick nav |
