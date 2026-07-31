# 07_LOCKED_DECISIONS — F-PR-001 ใบขอซื้อ (Purchase Requisition)

> **Audience:** All roles
> **Purpose:** บันทึก decision ที่ถกแล้วสรุป — ห้ามเปิดอภิปรายซ้ำ

---

## §7.1 Locked Decisions (LD)

### LD-01: Drawer width = 1290px (override standard 920px)
- **Date:** 2026-06-06
- **Context:** ตาราง line-items (รวมคอลัมน์ ~966px) เปิดใน document drawer มาตรฐาน 920px ไม่พอ ชื่อสินค้าล้น
- **Options:** A) คง 920 (ตารางล้น/scroll) · B) ขยาย 1290 (+40%)
- **Decision:** **B — 1290px**
- **Rationale:** ความจำเป็นของตาราง multi-column; stakeholder อนุมัติ (BRD §15 Q3)
- **Implications:** 01_UI P-02 drawer 1290 · BRD §14.6 D1 logged
- **Reversibility:** EASY (CSS)

### LD-02: ไม่มี Payment Term ที่ PR
- **Date:** 2026-06-06
- **Context:** P2P design — เงื่อนไขชำระเงินอยู่ขั้น PO
- **Decision:** PR ไม่มี payment term — เลือกที่ PO เท่านั้น (D01)
- **Rationale:** PR เป็นการ "ขอซื้อ" ยังไม่ผูกผู้ขาย/เงื่อนไขชำระ
- **Implications:** 04_DB ไม่มี field payment_term · BR-PR-13 · 03_LOGIC ไม่มี logic payment
- **Reversibility:** MEDIUM

### LD-03: DOA resolver เป็น engine ภายนอก (placeholder จนกว่า wire)
- **Date:** 2026-06-06
- **Context:** สายอนุมัติต้องไม่ hardcode (Governance)
- **Options:** A) hardcode tier ที่ PR · B) เรียก doa-resolver ของ DOA module
- **Decision:** **B** — F-PR ส่ง `{feature_id, cost_center, amount}` → รับ chain กลับ
- **Rationale:** Governance DOA ENC + reuse engine กลาง
- **Implications:** 03_LOGIC ENG-DOA EXISTING · F-PR-FN-06 เรียก resolver · Phase 3 wire เต็ม (OQ-03)
- **Reversibility:** EASY

### LD-04: Hard Control งบ = blocking ที่ submit (ไม่ใช่แค่ warn)
- **Date:** 2026-06-06
- **Context:** ป้องกันซื้อเกินงบตั้งแต่ต้นทาง
- **Decision:** Σ PR > งบคงเหลือ → **block submit** (ไม่ให้ override)
- **Rationale:** กฎคุมงบ (BR-PR-05 FIXED)
- **Implications:** F-PR-FN-06 → ENG-BUDGET check ก่อน pending · `BR_OVER_BUDGET` 422
- **Reversibility:** LOW (กฎควบคุม)

### LD-05: doc-amount-engine register CUBIC ที่ dev hand-off
- **Date:** 2026-06-06
- **Context:** logic คำนวณยอด (VAT/WHT/discount) reusable ข้าม PR/PO/CP/QT
- **Decision:** สร้างเป็น engine (`doc-amount-engine`) status DRAFT → register CUBIC ตอน hand-off
- **Rationale:** หลีกเลี่ยง logic ซ้ำในหลาย doc; pure + reusable
- **Implications:** 03_LOGIC §3.2 ENG-DOC-AMT DRAFT
- **Reversibility:** EASY

### LD-06: List 9 data columns (rare-exception)
- **Date:** 2026-06-06
- **Context:** multi-branch ERP — ต้องเห็นสาขาใน list
- **Decision:** เพิ่มคอลัมน์ "สาขา" → 9 data cols (มาตรฐาน ≤8, rare-exception ≤9)
- **Rationale:** branch สำคัญต่อบริบทหลายสาขา (BRD §14.6 D2)
- **Reversibility:** EASY

---

## §7.2 Convention Deviations

| Convention | Standard | This FRD | Reason |
|---|---|---|---|
| Feature ID prefix | `F-XX` (2-digit) | `F-PR` (project ID F-PR-001) | คงรหัส project; scope-local IDs ใช้ `F-PR-API/FN-NN` |
| Engine ID | `ENG-NNN` (3-digit) | `ENG-DOC-AMT` / `ENG-DOA` / `ENG-BUDGET` (readable) | ยังไม่ register CUBIC → ใช้ readable code; assign NNN ตอน register |

---

## §7.3 Promoted to LD (from Open Questions)
- (ยังไม่มี — OQ-01/02/04/05 ยังเปิดอยู่ใน 00_OVERVIEW §0.8)
