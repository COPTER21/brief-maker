# 00_OVERVIEW — F-PURCH-CFG-001 ตั้งค่าการจัดซื้อ (Purchase Configuration)

> **Audience:** All roles · **Purpose:** Document Control + Scope + Roles + Dependencies + Open Questions

---

## §0.1 Document Control
| Field | Value |
|---|---|
| **Feature ID** | F-PURCH-CFG-001 (scope prefix `PCFG`) |
| **Feature Name** | ตั้งค่าการจัดซื้อ (Purchase Configuration) |
| **Module** | จัดซื้อ (Purchase / P2P) — Configuration Layer |
| **Variant** | FULL (9 files + INDEX) |
| **Status** | APPROVED |
| **FRD Version** | 1.0 (2026-06-05) |
| **Source BRD** | BRD-PURCH-CFG-001 (APPROVED) |
| **Prototype** | purchase-config.html (final-check PASS · 2 tabs) |

## §0.2 Scope
**In-scope (6 config groups + numbering):**
- Comparison (enable/required/min-quotes/threshold/award) · Flow gating (require_pr_before_po)
- Payment Types (เปิดใช้ + default + deposit%/installment/credit — ดึงจาก Payment Term · inherit→PO)
- PR document (mandatory item/qty/need_by + quote attachment) · Vendor sourcing (approved-only + pricelist autofill)
- Document Numbering (PR/CP/PO: prefix/digits/reset/next + preview) · Boundary/Locked reference views

**Out-of-scope (อ่าน/อ้างอิงเท่านั้น):** Payment Term master→Finance · release_require_unlock_ref→Budget Config(#4) · approval tiers→DOA · GRN/QC/Putaway→Inventory Config · **Direct Payment→Finance/Accounting (เปิดที่ AP Invoice)** · Vendor master/Price List data→Master

## §0.3 Roles & Permissions
| Role | สิทธิ์ | ขอบเขต |
|---|---|---|
| Purchasing Admin | ดู + แก้ + บันทึก config/numbering | ทั้ง tenant · ทุกการบันทึก→audit |
| Purchasing Manager | ดู + แก้ + บันทึก (อาจผ่าน DOA — Q1) | |
| ผู้ใช้จัดซื้อทั่วไป | อ่านอย่างเดียว | |
| PR/PO/Comparison engine | อ่าน effective config (system) | API-06 |

## §0.4 Dependencies
- **Upstream:** Finance Payment Term (รายการ payment types) ✓ · Budget Config #4 (release flag) · DOA ✓Test · Vendor Master + Price List ✓
- **Downstream (consumer):** PR (F-PR-001) · Comparison (F-CMP-001) · PO (F-PO-001) — อ่าน config ไป gate flow
- **Engine NEW reusable:** ENG-DOCNUM-01 (doc-number-generator)

## §0.5 Open Questions
| Q | คำถาม | กระทบ |
|---|---|---|
| Q1 | config change สำคัญ ต้องผ่าน **DOA approval** มั้ย? | §0.3 / 05_RULES |
| Q2 | default delivery/warehouse location บน PO → Purchase Config หรือ Inventory/PO? | scope |
| Q3 | Tax/VAT default → Finance หรือที่นี่? | scope |
| Q4 | multi-currency future? (ตอนนี้ THB only) | 04_DB |
| Q5 | numbering แยกตามแผนก/สาขา หรือรวม tenant? | 04_DB T_doc_numbering |

## §0.6 Functional Requirements
| FR | ชื่อ | Scenario |
|---|---|---|
| FR-01 | อ่าน/แสดง config ปัจจุบัน | S-01 |
| FR-02 | แก้+บันทึก config (validate + audit) | S-02 |
| FR-03 | Comparison dependency gating (ปิด enable → disable ลูก) | S-03 |
| FR-04 | Payment Types จาก Payment Term + inherit→PO | S-04 |
| FR-05 | PR mandatory (ไม่มี cost center/รหัสงบ) | S-05 |
| FR-06 | Vendor sourcing rules | S-06 |
| FR-07 | Numbering: prefix/digits/reset/next + preview | S-07 |
| FR-08 | Numbering engine: issue + reset cycle (ไม่ซ้ำ) | S-08 |
| FR-09 | effective config สำหรับ consumer (PR/PO) | S-09 |
| FR-10 | Audit log ทุกการเปลี่ยน config | S-10 |
| FR-11 | Boundary/Locked reference views | S-11 |

## §0.7 Governance
- ✅ **User Access ENC** — เฉพาะ Purchasing Admin/Manager แก้ได้ (FN-09 checkAdminAccess); อื่นอ่าน
- ✅ **DOA ENC** — (optional Q1) config change สำคัญอาจเข้าสายอนุมัติ DOA · feature นี้ไม่ hardcode approval

### §0.7.1 Data Classification (highest)
- **Internal** ทั้งหมด — config keys/numbering/audit ไม่มีจำนวนเงิน Confidential, ไม่มี PII. รายละเอียด 04_DB §4.6
