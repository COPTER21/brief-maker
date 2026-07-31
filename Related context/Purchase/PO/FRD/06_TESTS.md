# 06_TESTS — F-PO-001 ใบสั่งซื้อ (Purchase Order)

> **Audience:** QA
> **Purpose:** Acceptance per FR + DoD (ส่งต่อ frd-qa-generator-v2)

---

## §6.1 Acceptance Criteria (per Functional Requirement)

### FR-01 สร้าง PO จาก CP
- AC-01.1: เลือก source=CP → แสดงตารางผู้ชนะ (won) เท่านั้น
- AC-01.2: เลือกผู้ชนะ → step2 ผู้ขายล็อก + payment_term = ของผู้ขาย
- AC-01.3: ผู้ชนะที่ po_status=CREATED → ปุ่มเลือก disable + แสดงเลข PO เดิม (E01)

### FR-02 สร้าง PO จาก PR / อิสระ
- AC-02.1: ไม่เลือก source → กดถัดไปได้ ไม่มี pop-up ขวาง (E03)
- AC-02.2: เลือกแค่ PR → ไม่มีตารางผู้ชนะ + step2 มี vendor combobox (E02)
- AC-02.3: PO อิสระ → step3 มีแถวรายการเปล่า

### FR-03 คำนวณภาษี/ส่วนลด (ENG po-amount)
- AC-03.1: VAT add → +7% จากยอดหลังหักส่วนลด (16,959.50)
- AC-03.2: ไม่มี VAT → grand = subtotal (12,000)
- AC-03.3: ส่วนลด 5% + VAT → 72,171.50
- AC-03.4: WHT 3% → net 72,800
- AC-03.5: discount ฿ > subtotal → cap (VR05)
- AC-03.6: VAT included → ถอน VAT ย้อน (net คงเดิม)

### FR-04 สถานะ + อนุมัติ DoA
- AC-04.1: submit → status=pending + resolve tier ตามยอด
- AC-04.2: amount ≤ 100K → approver = Purchasing Manager
- AC-04.3: buyer อนุมัติเอง → block SOD_VIOLATION (R13)
- AC-04.4: ตีกลับ → status=return → revision_no+1 + ต้องมี reason (VR07)
- AC-04.5: amount เกิน tier สูงสุด → block DOA_OVER_CEILING (VR06)

### FR-05 ออก PO PDF
- AC-05.1: approved → พิมพ์ได้ + variant ตรงรูปแบบภาษี
- AC-05.2: จำนวนเงินตัวอักษรตรง net_payable
- AC-05.3: มีช่องลงนาม Maker/Checker/Approver

### FR-06 List + filter
- AC-06.1: filter status 3 แกน ทำงานถูก
- AC-06.2: Confidential field (unit_price/total) mask ใน list (D-CLASS)

### FR-07 Edit guard / concurrency
- AC-07.1: แก้ได้เฉพาะ draft (else NOT_EDITABLE)
- AC-07.2: 2 users แก้ draft → CONFLICT (E12)
- AC-07.3: approved → lock แก้ไม่ได้ (C-10)

## §6.2 Definition of Done (DoD)
- [ ] ทุก FR ผ่าน AC + edge cases E01–E16 cover
- [ ] ENG po-amount ผ่าน calc 4 รูปแบบ (ตรง PDF sample)
- [ ] SoD + DoA (ENG doa-resolver) enforce ตอน submit/approve
- [ ] State machine ครบ + reason guard
- [ ] Data Classification mask/audit (D-CLASS §5.7)
- [ ] User Access ENC + DOA ENC พร้อมก่อน deploy
- [ ] PO PDF 4 variants render ถูก (A4/Sarabun/CI)
- [ ] Audit log ทุก mutation + state transition
- [ ] No Tailwind CDN; CI palette locked; Iron Rules v3.9 compliant

## §6.3 Test Data Hooks
- Vendors: VND-2026-0007(NET30), VND-2026-1123(2-10N30), VND-2025-0010(NET60)
- CP: CP-2604-00013 (มีผู้ชนะ) · PR: PR-2604-00010 (no CP)
- Payment terms: NET30/NET60/2-10N30/POSTPAY/PREPAY/DEP50/INST3/PARTIAL
