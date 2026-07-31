# 07_LOCKED_DECISIONS — F-PRODUCT-MASTER-001 Product Master

> **Audience:** All roles · ห้ามเปิดอภิปรายซ้ำ — เปลี่ยนได้ต้องมี decision ใหม่ + bump FRD

---

## §7.0 Scope Lock (R11)

**Scope Lock Ref:** **N/A — standalone** (งานไม่ผ่าน sign-off chain; ไม่มีใบเซ็น NF-SO/ENH-SO)
Session decisions ที่มีผลเทียบเท่า LOCK บันทึกเป็น LD-01/LD-04 ด้านล่าง
**Drift ระหว่างเขียน FRD:** ไม่มี — Reverse Mode สกัดจากจอ 1:1 (Phase 3.5 M)

---

## §7.1 Locked Decisions

### LD-01: ถอดชั้นอนุมัติ / DOA ออกทั้งหมด
- **Date:** 2026-07-27 · **Context:** คำสั่ง user ("เอาส่วนพวกการอนุมัติ, DOA ออกก่อน")
- **Decision:** ตัด pending status, approve/reject, DOA tier/chain, SoD, RE_APPROVAL ทั้งชุด — flow = validate แล้ว active ตรง
- **Implications:** state machine 5 สถานะ (05 §5.2) · API submit/approve/reject ถูกลบ · seed audit เดิม rewrite เป็น "เปิดใช้งาน"
- **Reversibility:** MEDIUM — โครง placeholder พร้อม (LD-02) แต่ UI/logic ต้อง build ใหม่ตอนเสียบ DOA engine (OQ-01, owner Strike)

### LD-02: DOA pre-placeholder fields คงไว้ (กติกาเหล็ก #3)
- **Decision:** `approver_role / approved_by / approved_at` = null คงใน schema + payload — comment `[DOA-ENGINE placeholder]` (เลี่ยงคำ "TODO" เพราะ audit v6 Rule #24 ห้าม)
- **Implications:** เสียบ Policy Center DOA engine ภายหลังโดย**ไม่ต้อง migrate schema** · ห้าม dev ลบ columns เหล่านี้
- **Reversibility:** EASY

### LD-03: ENG-STOCK-ALERT owner = Inventory Monitoring (consumer side)
- **Context:** ENH-MINMAX — ใครเป็นเจ้าของ engine เตือนสต็อก
- **Decision:** F-PDM เป็น **contract provider เท่านั้น** (`PRODUCT_STOCK_THRESHOLD v1` + `product_threshold_changed_event`) — engine ประเมิน on-hand เทียบ threshold อยู่ฝั่ง Inventory Monitoring
- **Implications:** 03 §3.2 ไม่มี engine owned · Architect register ตอน Inventory Monitoring build (OQ-03)
- **Reversibility:** EASY

### LD-04: ตัด ENH-4CODE (Item/SKU composer) ออกจาก scope
- **Date:** 2026-07-26 (session ก่อน) · **Decision:** Product Master = single-code (`code` เดียว) — ไม่มี item/sku 4-Code
- **Implications:** ไม่มี composer/sdd/code-chip บนจอ · migration drop columns 4CODE · เอกสาร v3.5 ที่อ้าง 4CODE = stale
- **Reversibility:** HARD (ต้อง redesign + migration ถ้ากลับมา)

### LD-05: Wizard 4 ขั้นตามจอจริง (R14)
- **Context:** Rule #47 แนะขั้นสุดท้าย "ตรวจสอบและยืนยัน" แต่จอจริงจบที่ "รูปภาพ & เอกสาร"
- **Decision:** FRD ยึดจอ (Reverse Mode ห้ามสวนจอ) — ต่างจาก standard → OQ-06 ให้ Chin เคาะ; ถ้าเพิ่มขั้น 5 ต้องแก้ HTML ก่อนแล้ว sync FRD (html-to-frd-sync)
- **Reversibility:** EASY

### LD-06: Soft reference สำหรับ master pickers (สืบทอด LD-4C-02 นโยบายทีม)
- **Decision:** หมวด/กลุ่ม/uom = picker soft reference — format soft, uniqueness blocking เฉพาะ `code`, ไม่มี FK enforcement/existence validation
- **Implications:** 04_DB ระบุ FK(soft) · ห้าม dev เพิ่ม hard FK โดยพลการ

---

## §7.2 Convention Deviations

### CD-01: Feature ID ยาว (`F-PRODUCT-MASTER-001` แทน `F-XX` 2 หลัก)
- **Reason:** ตาม FEATURE_REGISTRY ของทีม (ID ยาวทั้ง universe) — scope-local IDs ใช้ prefix ย่อ `F-PDM-API-NN / F-PDM-FN-NN` ให้อ่านง่าย
- **Impact:** ไม่มี — mapping 1:1

### CD-02: API-02 (GET detail) ไม่มี Function ใน trace
- **Reason:** pure read + middleware gate — ไม่มี business logic (Matrix #1) · R8 บังคับเฉพาะ mutation ✅ compliant

---

## §7.3 Promoted from OQ — ยังไม่มี (OQ-01..07 เปิดอยู่ ดู 00 §0.8)
