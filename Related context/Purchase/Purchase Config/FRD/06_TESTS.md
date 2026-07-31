# 06_TESTS — F-PURCH-CFG-001 ตั้งค่าการจัดซื้อ (Purchase Configuration)

> **Audience:** QA

---

## §6.1 Acceptance Criteria (per FR)

### FR-01 อ่าน/แสดง config (S-01)
- เปิดหน้า → แสดงค่าปัจจุบันครบทุกกลุ่ม · badge "บันทึกแล้ว"

### FR-02 แก้+บันทึก config (S-02)
- แก้ค่า → badge "ยังไม่บันทึก" + ปุ่มบันทึก/คืนค่าเปิด · กดบันทึก → toast + audit + badge กลับ "บันทึกแล้ว"
- คืนค่า → กลับค่าที่บันทึกล่าสุด

### FR-03 Comparison dependency gating (S-03)
- ปิด enable_comparison → comparison_required/min/threshold/award **disabled** (VAL-01)

### FR-04 Payment Types จาก Payment Term + inherit (S-04)
- checklist ดึงจาก Payment Term · เลือกเปิด/ปิด · default ต้อง ∈ ที่เปิด (VAL-02) · ปิดทุกอัน → block (VAL-05)
- deposit%/installment/credit param disable เมื่อ type ปิด · inherit ไป PO เป็นค่าเริ่มต้น (D08/D09)

### FR-05 PR mandatory (S-05)
- toggle item/qty/need_by/quote attachment · **ยืนยันไม่มี cost_center/budget_account** (โน้ต: มากับ UNLK)

### FR-06 Vendor sourcing (S-06)
- require_approved_vendor_only + vendor_pricelist_autofill (จาก Vendor Price List) บันทึกได้

### FR-07 Numbering config + preview (S-07)
- ตั้ง prefix/digits/reset/next ต่อชนิด → **ตัวอย่างเลขสด** (เช่น PR-2569-0232) · prefix ว่าง/digits 0 → block (VAL-03)

### FR-08 Numbering engine: issue + reset (S-08) ⭐
- issue → format `{prefix}-{พ.ศ.}-{next:0{digits}}` + increment · reset_cycle=yearly ขึ้นปีใหม่ → next=1 ครั้งเดียว (last_reset_period)
- **concurrent issue → ไม่ซ้ำ** (atomic FOR UPDATE)

### FR-09 effective config สำหรับ consumer (S-09)
- API-06 ส่ง config keys ครบ + resolve release flag (Budget Config) + payment term list · read-only · real-time

### FR-10 Audit log (S-10)
- ทุกการเปลี่ยน config/numbering → 1 แถวใน T_purchase_config_log (field, old→new, ใคร, เมื่อ)

### FR-11 Boundary/Locked views (S-11)
- การ์ดอ้างอิงแสดง Budget/DOA/Finance/Inventory/Direct-Payment · การ์ด locked แสดง D-series (read-only ปรับไม่ได้)

---

## §6.2 Edge Case Tests
ครอบ EC-01–EC-06 (05_RULES §5.5): forward-only, CP ค้าง, reset cycle ครั้งเดียว, default invalidate, optimistic lock, concurrent atomic issue

## §6.3 Definition of Done
- [ ] 3 ตาราง (T_purchase_config + T_doc_numbering + T_purchase_config_log) + constraints + indexes
- [ ] **ENG-DOCNUM-01** (issue atomic FOR UPDATE + reset guard + peek) + unit test (ไม่ซ้ำ concurrent, reset ครั้งเดียว)
- [ ] 8 APIs (6 read + 2 PUT mutation) · mutation → validate → persist → audit
- [ ] config-driven: effective config (API-06) ให้ PR/PO/CP อ่าน · **ไม่มี hardcode rule**
- [ ] payment types ดึงจาก Payment Term (FN-10) + inherit→PO (default/%/งวด/วัน)
- [ ] **ไม่มี cost_center/budget_account ใน PR mandatory** (มากับ UNLK · บังคับอ่านจาก Budget Config)
- [ ] approval→DOA (ไม่ตั้ง tier) · Direct Payment ไม่อยู่ feature นี้
- [ ] validation VAL-01–06 · comparison dependency cascade · ≥1 payment type
- [ ] audit ทุกการเปลี่ยน (diff old→new) · forward-only
- [ ] role gate (Admin/Manager edit · viewer read) · Data Classification Internal
- [ ] UI ตรง prototype (2 tabs, Flow Preview สด, checklist, num-preview, boundary/locked cards, hint hover)

## §6.4 Real-time / Integration
- consumer (PR/PO/CP) อ่าน effective config สด · numbering issue ภายใน transaction ของ doc create
- (optional Q1) config change → DOA approval hook
