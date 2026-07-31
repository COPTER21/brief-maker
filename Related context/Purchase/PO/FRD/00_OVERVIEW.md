# 00_OVERVIEW — F-PO-001 ใบสั่งซื้อ (Purchase Order)

> **Audience:** All roles (PM, BA, FE, BE, QA, DBA)
> **Purpose:** Document Control + Scope + Roles + Dependencies + Data Classification + Open Questions

---

## §0.1 Document Control
| Field | Value |
|---|---|
| **Feature ID** | F-PO-001 |
| **Feature Name** | ใบสั่งซื้อ (Purchase Order) |
| **Feature Code** | PO |
| **Module** | การจัดซื้อ (Purchase) — Value Stream P2P |
| **Variant** | FULL (9 files + INDEX) |
| **Status** | DRAFT |
| **FRD Version** | 1.0 (2026-06-08) |
| **Generator** | frd-generator-v5 |
| **Source Brief** | — (ไม่มี Brief — derive จาก BRD; assume FULL จาก has-state+approval+multi-engine) |
| **Source BRD** | BRD_F-PO-001.md (status: AI Reviewed/APPROVED, 2026-06-08) |
| **Author** | Tadswan C. (BA) |
| **Reviewers** | Bird (Dev Mgr), Strike (Lead), QA |

## §0.2 Revision History
| Version | Date | Author | Changes |
|---|---|---|---|
| 1.0 | 2026-06-08 | BA | Initial FRD generation จาก BRD_F-PO-001 + po_fixed.html prototype |

## §0.3 Scope
### In Scope
- สร้าง PO ผ่าน wizard 5 ขั้น (เลือกแหล่งที่มา / ข้อมูลหลัก / รายการสินค้า / เอกสารแนบ / ตรวจสอบ)
- 3 โหมดที่มา (Purchase Config): PR→CP→PO · PR→PO · PO โดยตรง
- เลือกผู้ขายตามแหล่งที่มา (CP=ล็อกผู้ชนะ / PR-direct=เลือกจาก Vendor Master)
- คำนวณ VAT 3 mode (none/add/included) + ส่วนลดรายการ ฿/% + ส่วนลดท้ายบิล + WHT
- สถานะ 3 แกน (doc/delivery/payment) + state machine + DoA approval
- ออก PO PDF 4 รูปแบบภาษี + ช่องลงนาม Maker/Checker/Approver
- List + filter + View drawer (detail/PDF/signature)

### Out of Scope
- GRN (F-GRN-001), AP/Payment Voucher — reason: แยก feature (รับสถานะกลับเท่านั้น)
- หน้าจัดการ Vendor/Item/CP/PR/Payment Term/Purchase Config/DOA — reason: แยก feature (PO อ่านอ้างอิง)
- Rule editor สำหรับ DYNAMIC rules (R15/R16/R17) — reason: Phase 3

## §0.4 Roles & Responsibilities (COSO)
| Role | Person/Team | Responsibilities |
|---|---|---|
| **Maker** | เจ้าหน้าที่จัดซื้อ (Buyer) | สร้าง/แก้ draft + submit |
| **Checker** | หัวหน้าแผนกจัดซื้อ (optional) | ตรวจก่อนอนุมัติ |
| **Approver** | Purchasing Manager / Director / CEO (ตาม DoA tier) | อนุมัติ/ตีกลับ/ปฏิเสธ |
| **Owner** | ฝ่ายจัดซื้อ | ดูแล config + ติดตาม |
| **Downstream** | คลัง (GRN), บัญชี (AP) | ใช้ PO ต่อ + ส่งสถานะกลับ |

> SoD: Maker ≠ Approver (บังคับใน §05_RULES + 03_LOGIC applyStatusTransition)

## §0.5 Dependencies
### Upstream (depends on)
| Dependency | Type | Source |
|---|---|---|
| Vendor Master | Data/API | F-VENDOR-MASTER-001 |
| Item Master | Data/API | F-PRODUCT-MASTER-001 |
| Comparison (awarded vendors) | Data/API | F-CP-001 |
| Purchase Requisition | Data/API | F-PR-001 |
| Payment Term Master | Data | F-PAYMENT-TERM-001 (8 terms) |
| Purchase Config | Config | Purchase Config Bible v1.4 (`purchase_source_mode`) |
| DOA resolver | Engine | F-PC-DOA-01 (CUBIC) {feature_id, cost_center, amount} |
| Document Numbering | Service | running `PO-YYYY-NNNNN` |
| PO PDF | Service | thai-doc-pdf-generator (PO_print-spec.md) |

### Downstream (depends on this)
| Consumer | Uses |
|---|---|
| GRN (F-GRN-001) | po_no, lines, status_delivery contract |
| AP / Payment Voucher | po_no, payment_term, grand_total, status_payment contract |

## §0.6 Pages Summary (from BRD §14.6 — Layout Authority)
| Page | Layout Template (html-generator-v3 v3.9) | Type |
|---|---|---|
| PO List | list-view (Pattern A) | ERP page |
| PO Create | create-drawer-wizard (Pattern B, 920px) | drawer |
| PO View | view-drawer-tabbed (Pattern C) + doc/PDF/signature (G/H/I) | drawer |

## §0.7 Security Domains (Security Bible §0.1 triggers)
- **Transaction + Approval/Workflow** → Preset P2 (14 controls)
- **Financial** (amount/VAT/WHT) → input validation + audit + immutability
- **Master snapshot** (vendor/item PII) → Confidential handling
- ก่อน deploy: **User Access ENC + DOA ENC** (CUBE 4.0 governance)

### §0.7.1 Data Classification Summary
ระดับสูงสุดที่ feature แตะ = **Confidential** (ข้อมูลผู้ขาย: tax_id, ผู้ติดต่อ, ราคาต่อรอง)
- Public: —
- Internal (default): po_no, สถานะ, วันที่, qty
- Confidential: vendor tax_id/contact, unit_price, grand_total, payment_term
- Restricted: — (ไม่มี field ระดับ Restricted ในรอบนี้ → ไม่ต้อง wire Restricted Resources)

## §0.8 Open Questions
| # | Question | Status | Owner |
|---|---|:---:|---|
| Q1 | SLA เวลาอนุมัติแต่ละ DoA tier? | ⚠️ รอ | ผู้จัดการจัดซื้อ |
| Q2 | WHT table แยกตามหมวดบริการ (1/2/3/5%) อย่างไร? | ⚠️ รอ | บัญชี |
| Q3 | ยกเลิก PO ที่มี GRN บางส่วน ทำได้แค่ไหน? | ⚠️ รอ | รอ flow GRN |
| Q4 | PO อิสระต้องผ่าน DoA เหมือนกัน? | ✅ | ใช่ — resolve ตามยอด |
