# 07_LOCKED_DECISIONS — F-CP-001 เปรียบเทียบราคา (Price Comparison)

> **Audience:** All roles
> **Purpose:** บันทึกการตัดสินใจที่ถกแล้ว — ห้ามเปิดอภิปรายซ้ำ

---

## §7.1 Locked Decisions (LD)

### LD-01: FRD สร้างแบบ reverse จาก HTML prototype (ไม่มี BRD)
- **Date:** 2026-06-06
- **Context:** CP พัฒนา HTML ตรง (html-generator-v3) ก่อน ไม่ผ่าน brd-generator-full
- **Options:** A) บังคับทำ BRD ก่อน B) reverse FRD จาก HTML ที่ lock แล้ว + PDF
- **Decision:** B — ใช้ HTML prototype (ผ่าน design review หลายรอบ) + PDF เป็น spec source
- **Rationale:** HTML lock แล้ว = design authority de-facto · ส่งมอบ dev ได้เร็ว
- **Implications:** Layout อ้าง html-generator-v3 Pattern A/B/C แทน BRD §14.6 · ควร back-fill BRD ภายหลังเพื่อ full traceability
- **Reversibility:** EASY (back-fill BRD ได้)

### LD-02: ENG-01 + ENG-02 register CUBIC ตอน dev hand-off (ไม่ใช่ sprint นี้)
- **Date:** 2026-06-06
- **Context:** price-comparison-winner + po-split มีศักยภาพ reuse (RFQ, PO)
- **Decision:** scope-local ก่อน (status=DRAFT) → register Phase 2 เมื่อ feature ที่ 2 ยืนยัน reuse
- **Rationale:** เลี่ยง premature abstraction
- **Implications:** 03_LOGIC §3.2 = DRAFT · DoD: register ก่อน mark done
- **Owner:** Architect · **Reversibility:** EASY

### LD-03: ใช้ ENG-03 (vendor-price-list-resolver) + ENG-04 (doa-approval-resolver) ที่มีอยู่ (shared)
- **Date:** 2026-06-06
- **Context:** ราคา preset + สายอนุมัติ
- **Decision:** reuse engine ที่ register แล้ว (ใช้ร่วมกับ F-PR-001) ไม่สร้างใหม่
- **Rationale:** single source — price list + DOA ต้องตรงกันทั้ง P2P
- **Implications:** 03_LOGIC §3.2 = EXISTING · เพิ่ม F-CP-001 ใน "used by" · **DOA ห้าม hardcode**
- **Reversibility:** EASY

### LD-04: po_id ออกโดย F-PO-001 เท่านั้น (CP ไม่กำหนดเอง)
- **Date:** 2026-06-06
- **Context:** เลขที่ PO
- **Decision:** award (FN-09) เรียก F-PO-001 createPurchaseOrder → รับ po_id กลับ
- **Rationale:** เลข running PO เป็นของ PO module · กัน id ชนกัน
- **Implications:** T_comparison_po_split.po_id = nullable จนกว่า award · BR-CP-07
- **Reversibility:** MEDIUM

### LD-05: ราคา preset เติมเฉพาะช่องว่าง (ไม่ทับค่าที่แก้เอง)
- **Date:** 2026-06-06
- **Context:** UX ดึงราคา vs แก้เอง
- **Decision:** applyPriceList เติมเฉพาะ cell ว่าง (is_preset) · แก้แล้วไม่ทับ · มีปุ่ม "เติมราคา price list" ดึงซ้ำเฉพาะช่องว่าง
- **Rationale:** ลดงานกรอก + คง manual override (BR-CP-04, EC-04)
- **Reversibility:** EASY

### LD-06: award แบบ all-or-nothing (transaction)
- **Date:** 2026-06-06
- **Context:** EC-07 PO สร้าง fail บางใบ (OQ-01)
- **Decision (proposed):** all-or-nothing — ถ้าใบใด fail → rollback ทั้ง CP, status คง approved, 502
- **Rationale:** กัน CP awarded ครึ่ง ๆ (po_id บางใบว่าง) · ง่ายต่อ reconcile
- **Status:** ⚠️ pending confirm (OQ-01 — Bird) · ถ้าต้อง partial → เปลี่ยนเป็น mark fail + retry
- **Reversibility:** MEDIUM

---

## §7.2 Convention Deviations

### CD-01: Feature ID = F-CP-001 (3-digit) ไม่ใช่ F-XX (2-digit)
- **Convention default:** `F-XX` (2-digit) ใน conventions.md
- **Deviation:** ใช้ `F-CP-001` (domain + 3-digit) ตามมาตรฐานโครงการ CUBE 4.0
- **Reason:** house standard ปัจจุบัน (สอดคล้อง F-PR-001, F-PO-001) — 3-digit feature ID convention
- **Approved by:** Dev Mgr (Bird) · **Apply to:** ทุก ID ใน feature นี้ (API/FN/ENG ใช้ prefix F-CP-001)

### CD-02: Engine ID = F-CP-001-ENG-NN (scope-local) จนกว่าจะ register
- **Convention default:** ENG-NNN (global) หลัง register
- **Deviation:** ใช้ F-CP-001-ENG-01/02 ใน FRD draft (ENG-03/04 อ้าง global ที่ register แล้ว)
- **Reason:** ตาม conventions §Engine scope-local rule (DRAFT) · global id assign ตอน CUBIC register

---

## §7.3 Open Questions Promoted from 00_OVERVIEW
[ยังไม่มีที่ resolved — OQ-01..05 ยัง open ใน 00_OVERVIEW §0.8]

---

## §7.4 Architecture Tradeoffs Acknowledged

### AT-01: PostgreSQL RLS over app-level filtering
- **Tradeoff:** perf ~5% vs security guarantee · **Accepted:** YES (CUBE ERP standard)

### AT-02: Synchronous award (เรียก F-PO-001 sync)
- **Tradeoff:** latency (~1.5s รวมสร้าง PO) vs complexity (async queue)
- **Accepted:** sync สำหรับ V1 · **Re-evaluate:** ถ้า splits เยอะ/latency > 3s → async + job tracking

### AT-03: Matrix เก็บเป็น T_comparison_quote (row per cell)
- **Tradeoff:** row count (lines × vendors) vs flexibility (เพิ่ม/ลบ vendor ง่าย, query winner ตรง)
- **Accepted:** YES — line × vendor สูงสุด ~3×N rows, จัดการได้

---

## §7.5 Decisions Deferred to Implementation

| Item | Owner | Deadline |
|---|---|---|
| validation lib (zod/yup) | Tech Lead | sprint planning |
| Idempotency cache store (Redis TTL) | DevOps | pre-deploy |
| winner override ต้องบันทึกเหตุผลไหม (OQ-04) | Procurement | pre-dev |
| VAT คำนวณใน CP vs PO (OQ-02) | Finance | pre-dev |

---

## §7.6 References
- **Spec source:** `CP_F-CP-001.html` (locked) + `CP_template.html` + `CP_print-spec.md`
- **Convention:** `knowledge/conventions.md`
- **Related FRD:** F-PR-001 (ใบขอซื้อ — แชร์ pattern + ENG-03/04), F-PO-001 (ใบสั่งซื้อ — consume award)
