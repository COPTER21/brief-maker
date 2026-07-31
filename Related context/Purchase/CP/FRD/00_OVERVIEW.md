# 00_OVERVIEW — F-CP-001 เปรียบเทียบราคา (Price Comparison)

> **Audience:** All roles (PM, BA, FE, BE, QA, DBA)
> **Purpose:** Document Control + Scope + Roles + Dependencies + Open Questions

---

## §0.1 Document Control

| Field | Value |
|---|---|
| **Feature ID** | F-CP-001 |
| **Feature Name** | เปรียบเทียบราคา (Price Comparison) |
| **Feature Code** | PROC-CP |
| **Module** | Procurement — Procure-to-Pay (P2P) |
| **Variant** | FULL (9 files + INDEX) |
| **Status** | DRAFT |
| **FRD Version** | 1.0 (2026-06-06) |
| **Generator** | frd-generator-v5 (v5.1) |
| **Source Brief** | — (ไม่มี Brief — reverse จาก HTML prototype) |
| **Source BRD** | — (ไม่มี BRD — spec source = HTML prototype `CP_F-CP-001.html` ที่ผ่าน design review/lock) |
| **Author** | 2BSimple BA (Tadswan C.) |
| **Reviewers** | Bird (Dev Mgr), Strike (Dev), Chin (UI) |

> ⚠️ **Input note:** FRD นี้สร้างแบบ reverse/standalone — feature พัฒนา HTML ก่อน (ไม่ผ่าน brd-generator-full)
> spec source คือ HTML prototype ที่ lock แล้ว + PDF document (thai-doc-pdf-generator) + การ design review หลายรอบ
> Layout Template ID อ้างจาก html-generator-v3 (Pattern A/B/C) แทน BRD §14.6
> หาก feature เข้าสู่ pipeline เต็ม ภายหลังควร back-fill BRD เพื่อ traceability

---

## §0.2 Revision History

| Version | Date | Author | Changes |
|---|---|---|---|
| 1.0 | 2026-06-06 | 2BSimple BA | Initial FRD (reverse จาก HTML prototype + PDF) |

---

## §0.3 Scope

### In Scope
- รายการ CP (list) — ค้นหา / กรองสถานะ / sort / pagination / ส่งออก CSV
- สร้าง CP wizard 4 ขั้น: ข้อมูลทั่วไป (อ้าง PR + ผู้จัดทำ) → เลือกผู้ขายที่เทียบ → เปรียบเทียบราคา (matrix + เลือกผู้ชนะ) → สรุป + แยก PO
- ดึงราคา preset จาก Vendor Price List มาเติมในตารางเทียบ (แก้ไขได้)
- เลือกผู้ชนะรายรายการ (line-by-line) — default ราคาต่ำสุด, override ได้
- แยกใบสั่งซื้อ (PO Split) ตามผู้ขายที่ชนะ (1 ผู้ขาย = 1 PO)
- View drawer 4 แท็บ: รายละเอียด / แยก PO (พร้อมรายการสินค้า+ราคา+สถานะสร้าง PO+po_id) / PDF Preview (เอกสาร A4) / ลายเซ็น (DOA chain)
- สายอนุมัติ: ส่งเซ็น (DOA) → อนุมัติ / ตีกลับ → ออกใบสั่งซื้อ (award → po_id จากระบบ PO)
- เอกสาร PDF ใบเปรียบเทียบราคา (A4 · Sarabun · CI CUBE NATIVE)

### Out of Scope
- การสร้าง/บันทึก PO จริง — เป็นหน้าที่ของ F-PO-001 (CP เพียงสั่ง award + รับ po_id กลับ)
- การจัดการ Vendor master + Vendor Price List master — เป็น Master Data feature (CP อ่านอย่างเดียว)
- การอนุมัติงบประมาณ / budget release — มาจาก PR/Budget (CP สืบทอด)
- e-bidding / RFQ ส่งคำขอราคาออนไลน์ไปผู้ขาย — เฟสถัดไป

### Out of Scope (mark from Phase 2.5 skipped probes)
- การเทียบผู้ขาย > 3 ราย (ตาราง A4 จะกว้างเกิน) — flag OQ-03

---

## §0.4 Roles & Responsibilities (COSO)

| Role | Person/Team | Responsibilities |
|---|---|---|
| **Maker** | ผู้จัดทำ (จัดซื้อ / Buyer) | สร้าง CP, เลือกผู้ขาย, กรอก/แก้ราคา, เลือกผู้ชนะ, ส่งเซ็น |
| **Checker** | ผู้ตรวจสอบ (ผู้จัดการฝ่ายจัดซื้อ) | ตรวจสอบผลเปรียบเทียบ + ลงนาม |
| **Approver** | ผู้อนุมัติ (ตาม DOA — cost center + มูลค่า) | อนุมัติผล / ตีกลับ + ลงนาม |
| **Owner** | ฝ่ายจัดซื้อ (Procurement) | ดูแลกระบวนการ + ออกใบสั่งซื้อหลังอนุมัติ |

> รายละเอียดต่อ workflow → ดู `01_UI.md §1.3 Journey` + `05_RULES.md §5.2 State Machine`

---

## §0.5 Dependencies

### Upstream (this feature depends on)
| Dependency | Type | Source |
|---|---|---|
| ใบขอซื้อ (PR) ที่ approved + route=cp | Data / API | F-PR-001 |
| Vendor master (รายชื่อผู้ขาย + เครดิต + เลขภาษี) | Data | Master Data — Vendor |
| Vendor Price List (ราคาต้นทางต่อผู้ขาย × สินค้า) | Data / Engine | Master Data — Vendor Price List |
| DOA approval chain resolver | Engine | CUBIC `doa-approval-resolver` (shared, ใช้กับ F-PR-001 ด้วย) |

### Downstream (features that depend on this)
| Consumer | What it uses |
|---|---|
| F-PO-001 (ใบสั่งซื้อ) | รับ PO split payload (vendor + lines) จาก award → สร้าง PO + ส่ง po_id กลับ |
| Report / Dashboard | winner_total, จำนวน CP, อัตราการแยก PO |

### External
| Service | Purpose |
|---|---|
| thai-doc-pdf-generator (build-time) | สร้างเอกสาร PDF ใบเปรียบเทียบราคา (template + render) |

---

## §0.6 Stack & Architecture

| Layer | Technology |
|---|---|
| Frontend | HTML/JS prototype (Pattern A/B/C, hash routing) → React/Next plug ต่อ |
| API | Node.js / Strapi (CUbe) |
| Database | PostgreSQL (RLS multi-tenant) |
| Engine layer | CUBIC Registry (winner-selection, po-split, price-list-resolver, doa-resolver) |
| Auth | JWT + role-based |
| Document | Chromium render + Sarabun (CI CUBE NATIVE) |

---

## §0.7 Multi-Tenant & Security Context

- [x] Multi-tenant feature: YES (RLS by tenant_id)
- [x] PII data involved: YES (ชื่อผู้จัดทำ / ผู้ติดต่อผู้ขาย — minimal)
- [x] Financial data: YES (ราคา/หน่วย, winner_total)
- [x] Audit log required: YES (ทุก mutation + state transition + award)

**Security Bible domains applied:** D2, D5, D9, D15, D17, D-CLASS (+ D7 minimal) — see 05_RULES.md §5.7

### §0.7.1 Data Classification Summary ⭐ (v5.1)

Highest classification level ที่ feature นี้แตะ:
- [ ] Has Restricted fields
- [x] Has Confidential fields — ราคา/หน่วยผู้ขาย, winner_total, เลขภาษีผู้ขาย (vendor pricing = ข้อมูลการค้า)
- [x] Internal (default) — สถานะ, วันที่, เลขที่ CP, audit timestamps
- [ ] Public-facing data

**Linkage:** ฟิลด์ Confidential (ราคา/ยอดรวม) → register ที่ Policy Center → Data Classification (ดู 04_DB §4.6)

---

## §0.8 Open Questions

| ID | Question | Blocking? | Owner |
|---|---|---|---|
| OQ-01 | award แล้วถ้า F-PO-001 สร้าง PO ไม่สำเร็จบางใบ — rollback ทั้ง CP หรือ partial? (ดู EC-07) | YES | Bird |
| OQ-02 | VAT 7% คำนวณในเอกสาร CP หรือผลักไป PO อย่างเดียว? (ปัจจุบันเอกสารแสดง VAT) | NO | Finance |
| OQ-03 | รองรับเทียบผู้ขาย > 3 ราย หรือไม่ (กระทบ layout เอกสาร A4) | NO | Chin |
| OQ-04 | winner override (เลือกไม่ใช่ราคาต่ำสุด) ต้องบันทึกเหตุผลไหม (audit/compliance) | NO | Procurement |
| OQ-05 | ราคา/หน่วย ควรเป็น Confidential หรือ Restricted (จำกัด person)? ปัจจุบัน Confidential | NO | Policy Center |

> Resolved questions → move to 07_LOCKED_DECISIONS as LD-NN

---

## §0.9 Glossary

| Term | Definition |
|---|---|
| CP | Comparison / ใบเปรียบเทียบราคา — เอกสารเทียบราคาหลายผู้ขายสำหรับสินค้าชุดเดียวกัน |
| PR | Purchase Requisition / ใบขอซื้อ — ต้นทางของ CP |
| PO | Purchase Order / ใบสั่งซื้อ — ปลายทางหลัง award |
| PO Split | การแยก CP เป็นหลาย PO ตามผู้ขายที่ชนะ (1 ผู้ขาย = 1 ใบ) |
| Winner | ผู้ขายที่ถูกเลือกสำหรับ 1 รายการ (line) |
| Price List | ราคาต้นทางต่อผู้ขาย × สินค้า ที่ดึงมาเป็นค่าเริ่มต้น (แก้ไขได้) |
| DOA | Delegation of Authority — กำหนดสายอนุมัติตาม cost center + มูลค่า |
| winner_total | ผลรวมราคาผู้ชนะทุก line (ก่อน VAT) |

---

## §0.10 Pack Navigation

| File | Audience | Purpose |
|---|---|---|
| 00_OVERVIEW.md | All | This file — meta + scope |
| 01_UI.md | FE dev | Pages + Components + Journey |
| 02_API.md | BE dev (HTTP) | API contracts |
| 03_LOGIC.md | BE dev (logic) | Functions + Engines + Trace |
| 04_DB.md | DBA / BE | Tables + Fields + Relationships |
| 05_RULES.md | BE + QA | Business Rules + Edge Cases + Errors |
| 06_TESTS.md | QA | Acceptance + DoD |
| 07_LOCKED_DECISIONS.md | All | LDs + Convention deviations |
| INDEX.md | All | Cross-reference quick nav |
