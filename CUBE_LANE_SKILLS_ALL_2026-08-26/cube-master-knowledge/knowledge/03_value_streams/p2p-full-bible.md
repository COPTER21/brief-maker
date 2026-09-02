---
file_id: KB-03-01
title: P2P (Procure-to-Pay) — Full Value Stream Bible
version: 1.0.0
last_updated: 2026-05-27
status: stable
sources:
  - P2P_Payment_CheatSheet.pdf v1.0 (เมษายน 2568, 2BSimple)
  - chat consolidation 2026-05-27
---

# P2P — Procure-to-Pay Full Bible

## Quick Reference (TL;DR)

- **VS**: P2P
- **Trigger**: ความต้องการสินค้า/บริการ (PR หรือ direct invoice)
- **Outcome**: เสร็จสิ้น — ชำระเงิน vendor + ปิด PO + บันทึก GL
- **VCs**: 7 ตัว (6 จาก cheat sheet + Direct Payment)
- **Invariants**: 3-way match บังคับ (ยกเว้น Direct Payment), Close-Balance trigger ที่ GRN เท่านั้น

---

## §1. VC Catalog (7 Value Chains)

| VC | name | trigger event | GRN trigger | 3-way match |
|---|---|---|---|---|
| **VC1** | Full Postpay | PR/PO → GRN → Inv → PV | ทันที | YES (PO eff = GRN = Inv net) |
| **VC2** | Full Prepay | PR/PO → AP Inv → PV → GRN | หลัง PV confirm | YES |
| **VC3** | Deposit | PR/PO → Inv มัดจำ → PV มัดจำ → GRN → Inv balance → PV balance | หลัง PV มัดจำ | YES (ที่ Inv balance) |
| **VC4** | Installment | PR/PO → GRN → AP Inv → PV งวด 1..N | ทันที | YES (หลัง GRN ครั้งเดียว) |
| **VC5** | Partial Delivery | PR/PO → GRN round 1 → Inv qty จริง → PV → ... → GRN round N | ทันที | YES (ต่อ round) |
| **VC6** | Credit N วัน | PR/PO → GRN → Inv (due = วันออก + N) → PV ก่อน due | ทันที | YES |
| **VC7** | Direct Payment | AP Inv โดยตรง → PV (bypass PR/PO/GRN) | N/A | **NO** (bypass) |

### VC Decision (ที่ไหน + ใคร)
- **เลือกที่**: PO Wizard Step 2 (D01)
- **ใคร**: Procurement Officer (+ HOD ถ้า amount > threshold)
- **เปลี่ยนได้ไหมหลัง PO approve**: **ไม่ได้** (D05) — ต้อง cancel + สร้าง PO ใหม่
- **ข้อยกเว้น**: Subcontract Unit Conversion → lock VC1 Full Postpay อัตโนมัติ (D12)

### Direct Payment (VC7) Special Notes
- ใช้กับ: ค่าไฟ, ค่าน้ำ, ค่าบริการ subscription, ค่าใช้จ่ายที่ไม่มี PR/PO/GRN
- เข้าระบบที่ AP Invoice ตรง
- **ข้าม** 3-way match ทั้งหมด
- ต้อง approval พิเศษ (ขึ้นกับ DOA)
- ออกเป็น PV type=payment ปกติ

---

## §2. Path Catalog (per VC)

### Receiving Rules (Master — ใช้ทุก VC ยกเว้น VC7)

| สถานการณ์ | Rule | Action | ผลกับ AP Invoice |
|---|---|---|---|
| รับครบ + QC ผ่านหมด | **Happy Path** | Putaway ทั้งหมด → AP Invoice เต็ม | Invoice = PO qty, 3-Way pass ทันที |
| รับครบ + QC fail บางส่วน | **Partial QC** | Putaway qty ดี / qty fail → HOLD location → สร้าง RTV | Invoice เต็ม → Hold → รอ CN → จ่าย net |
| รับครบ + QC fail ทั้งหมด | **Full Reject** | ทุก qty เข้า HOLD → RTV ทั้งล็อต | CN เต็มจำนวน → Refund หรือส่งใหม่ |
| รับไม่ครบ (qty < PO) | **Partial always** | Decision ที่ GRN: รอ round 2 / Close PO balance + Putaway qty จริง | Invoice = qty รับจริง, PO eff = closed qty |
| รับไม่ครบ + QC fail บางส่วน | **Hyper Case** | Close PO balance qty ขาด → HOLD qty fail → RTV → Putaway qty ผ่าน | Invoice = qty รับ, CN = qty ขาด+fail, PV = Putaway qty |

### Iron rule: รับไม่ครบ = Partial เสมอ (D03)
- ไม่มี exception
- ไม่มี "รับเต็ม" ถ้า qty ไม่ครบ
- Decision อยู่ที่ GRN screen เท่านั้น

---

## §3. Anchors / Invariants (cross-VC)

### D06: 3-Way Match (บังคับทุก VC ยกเว้น VC7)
สูตร: **`PO effective qty = GRN qty รับจริง = AP Invoice net qty`**

| VC | PO qty ที่ใช้ | GRN qty | Invoice qty | เมื่อไหร่ |
|---|---|---|---|---|
| VC1 Full Postpay | PO effective | รับจริง | Invoice net | หลัง GRN confirm |
| VC2 Full Prepay | PO original | รับจริง (ถ้าขาด = PO eff) | Invoice net (หลัง CN) | หลัง GRN confirm |
| VC3 Deposit | PO effective | รับจริง | Invoice เหลือ net | หลัง GRN, ที่ Invoice ส่วนที่เหลือ |
| VC4 Installment | PO effective | รับจริง | Invoice net | หลัง GRN (ครั้งเดียว) |
| VC5 Partial Del. | PO eff per round | GRN qty/round | Invoice qty/round | ต่อ GRN round |
| VC6 Credit N | PO effective | รับจริง | Invoice net | หลัง GRN confirm |
| VC7 Direct Pay | — | — | — | bypass — ไม่มี 3-way |

- **PO effective qty** = PO original qty หลัง Close PO Balance
- **Invoice net** = Invoice − CN
- ต้องตรงกันทั้ง 3 ก่อนสร้าง PV ได้ (ยกเว้น VC7)

### D07: Close PO Balance — trigger ที่ GRN เท่านั้น
- ห้าม trigger จาก Invoice หรือ PV
- กด 'ไม่รอ' ที่ GRN เท่านั้น
- บันทึก audit log ทุกครั้ง

### D04: Auto-close PO เมื่อ GRN cumulative = PO qty
- ปิดอัตโนมัติ
- Manual close = กด 'ไม่รอ' ที่ GRN เท่านั้น

---

## §4. Edge Cases (Business-Level — อยู่ใน Bible)

| Edge | Trigger | การจัดการ |
|---|---|---|
| **RTV** | QC fail → ของอยู่ใน HOLD | สร้าง RTV (จาก GRN) → vendor รับคืน → vendor ออก CN → CN link Invoice → Invoice net ลด → 3-Way ใหม่ → PV จ่าย net |
| **CN (Credit Note)** | vendor ออก CN | บันทึก CN + แนบไฟล์ CN จาก vendor → CN link Invoice → Invoice net = Invoice − CN → 3-Way ใช้ net → PV จ่าย net |
| **Refund (Full Prepay)** | จ่ายครบแล้ว, CN มา | เลือก: (1) รับเงินสดคืน → PV type=refund link CN+PV เดิม / (2) Offset รอบถัดไป → CN ค้างไว้หัก PO/Invoice ใหม่ |
| **Close PO Balance** | qty < PO + user ไม่รอ | user กด 'ไม่รอ' ที่ GRN → auto Close PO balance + audit log → PO eff = GRN qty → 3-Way ใช้ PO eff |
| **Cancel PO** | ต้องการยกเลิก | ก่อน GRN: cancel ได้; จ่ายมัดจำแล้ว: Refund ก่อน; Full Prepay จ่ายแล้ว: CN + Refund Voucher; เปลี่ยน VC: cancel + สร้างใหม่ |
| **Overdue (Credit)** | due_date < วันนี้ ยังไม่จ่าย | badge แดง 'เกินกำหนด' ที่ Invoice + PO landing → **ไม่ block** PO ใหม่ / GRN / payment |
| **Auto Close (Partial Del.)** | GRN cum = PO qty | ระบบ auto detect → 'รับครบ' → ปิด PO อัตโนมัติ (ตราบใด cum < PO = partial เสมอ) |
| **Installment + QC fail** | จ่ายตามงวด, QC fail | จ่ายตามงวดปกติ → QC fail → vendor ส่งของเพิ่ม (ไม่ยกเลิกงวด, ไม่ proportional CN) → CN offset เก่า, PV งวดถัดไปจ่ายปกติ |
| **Deposit + QC fail** | มัดจำจ่ายแล้ว, ของมา QC fail | จ่าย remaining ปกติตาม Invoice → vendor ส่งของเพิ่มให้ครบก่อน (ไม่ลด remaining) → CN ออกหลัง RTV เสร็จ |

---

## §5. Payment Voucher — 2 voucher_types ใน 1 document (D13)

| voucher_type | ใช้เมื่อ | Link กับ | GL Direction |
|---|---|---|---|
| `payment` (จ่ายออก) | ทุก VC ปกติ | AP Invoice | DR AP Payable / CR Bank |
| `refund` (รับเงินคืน) | VC2 + CN, Cancel PO หลังจ่าย, VC3 + QC fail total | CN + PV เดิม | DR Bank / CR AP Payable |

**Key**: ใช้เอกสารเดียวกัน แยกด้วย `voucher_type` field — **ไม่สร้าง Refund Voucher แยก**

---

## §6. Locked Decisions (15 ข้อ)

| # | Decision | Detail |
|---|---|---|
| D01 | Payment term เลือกที่ PO เท่านั้น | PR/Comparison ไม่มี payment term; เริ่มที่ PO Wizard Step 2 |
| D02 | GRN trigger ตาม VC | VC2/VC3 = รอ PV ก่อน; อื่นๆ = ทันที |
| D03 | รับไม่ครบ = Partial เสมอ | ไม่มี exception; GRN qty < PO = partial ทุกกรณี |
| D04 | Auto-close PO เมื่อ GRN cum = PO qty | manual close = กด 'ไม่รอ' ที่ GRN |
| D05 | เปลี่ยน payment type ไม่ได้หลัง PO approve | ต้อง cancel + สร้างใหม่ |
| D06 | 3-Way Match บังคับทุกกรณี | PO eff = GRN = Invoice net; ไม่มี bypass (ยกเว้น VC7) |
| D07 | Close PO Balance trigger ที่ GRN เท่านั้น | ห้าม trigger จาก Invoice/PV |
| D08 | Deposit: inherit % + ปรับได้ที่ PO | remaining จ่ายหลัง GRN confirm ทันที |
| D09 | Installment: inherit + ปรับ % และ due_date | ต่องวดได้ที่ PO |
| D10 | Partial Delivery: GRN กำหนดยอดจ่าย | GRN qty = Invoice qty = PV amount ต่อ round |
| D11 | Credit overdue: แสดงเตือน ไม่ block | badge แดง; ไม่ block อะไรเลย |
| D12 | Unit Conversion (Subcontract) = Full Postpay | lock อัตโนมัติ ไม่ให้ user เปลี่ยน |
| D13 | Payment Voucher 2 types ใน document เดียว | voucher_type = payment / refund |
| D14 | CN ต้องมาจาก vendor เท่านั้น | ออก CN เองไม่ได้ ต้องแนบไฟล์ vendor CN |
| D15 | Installment ≠ Partial Delivery | Installment = ส่งรอบเดียว แบ่งจ่าย N งวด; Partial = ส่งหลายรอบ จ่ายตาม GRN |

---

## §7. Feature Catalog (P2P-specific)

### ✓ Done (existing)
- F-PURCHASE-CONFIG-001 (Purchase Configuration — Payment Term)
- F-INV-STOCK-001 (Inventory — Stock by Product & Location)

### ○ To do (backlog from cheat sheet §8)
| feature_id | name | scope notes |
|---|---|---|
| F-PO-001 | Purchase Order Enhancement | + payment type field + dynamic section, 3-lane status, payment summary, qty tracking per line |
| F-GRN-001 | GRN — Receiving + QC inline | qty check, QC pass/fail, Close PO balance trigger, HOLD location assign, RTV trigger |
| F-PUTAWAY-001 | Putaway | เก็บของผ่าน QC → PICK_FACE / RESERVE |
| F-RTV-001 | Return to Vendor | trigger จาก GRN, ดึงของจาก HOLD, link กับ CN |
| F-INV-001 | AP Invoice + 3-Way Match | PO-based + Direct Payment mode, Hold status, 3-Way per VC, CN offset |
| F-PV-001 | Payment Voucher Enhancement | voucher_type = payment/refund, refund mode link CN |
| F-CN-001 | Credit Note | link AP Invoice, vendor CN ref + file attach, offset/refund trigger, many-to-one CN → Invoice |
| F-DIRECT-PAY-001 | Direct Payment Flow | bypass PR/PO/GRN, AP Invoice direct, ไม่มี 3-Way, approval พิเศษ |

### Required specs (! — ยังต้องระบุ flow)
- Credit Note link AP Invoice flow (many-to-one)
- Deposit / Installment / Partial Delivery / Credit flow diagrams
- Direct Payment flow

---

## §8. Inventory Locations (จาก receiving rules)

| location | usage |
|---|---|
| `HOLD` | QC fail items (waiting for decision) |
| `QC` | items in inspection |
| `DAMAGED` | confirmed damaged items (sub of HOLD) |
| `PICK_FACE` | items ready for picking (post-Putaway) |
| `RESERVE` | reserve stock |

**Rule**: HOLD location ไม่นับเป็น available stock

---

## §9. Glossary (P2P-specific terms)

- **RTV**: Return to Vendor — คืนของให้ vendor (link CN)
- **CN**: Credit Note — vendor ออกเอกสารลด/ยกเลิกบางส่วน
- **GRN**: Goods Receipt Note — ใบรับของ
- **PV**: Payment Voucher — ใบจ่ายเงิน (มี voucher_type)
- **3-Way Match**: จับคู่ PO + GRN + Invoice qty (ทั้ง 3 ต้องตรง)
- **PO effective qty**: PO original qty หลัง Close Balance (เป็น qty ที่ใช้ในการ match)
- **Invoice net**: Invoice amount − CN
- **HOLD location**: location สำหรับของ QC fail (ไม่ count เป็น available)
- **Subcontract Unit Conversion**: case พิเศษที่ lock VC = Full Postpay อัตโนมัติ
- **Direct Payment**: ค่าไฟ/ค่าบริการ — bypass PR/PO/GRN ขึ้นที่ AP Invoice ตรง

---

## Change Log

- **1.0.0** (2026-05-27): Initial — full cheat sheet absorbed + Direct Payment (VC7) added + structure aligned to VS/VC/Path hierarchy
