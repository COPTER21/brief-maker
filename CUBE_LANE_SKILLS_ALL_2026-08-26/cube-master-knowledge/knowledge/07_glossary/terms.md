---
file_id: KB-07-01
title: CUBE Glossary
version: 1.0.0
last_updated: 2026-05-27
status: stable
---

# CUBE Glossary

## Quick Reference (TL;DR)

Term dictionary สำหรับ CUBE concept — เรียงตามหมวด

---

## 🏗 Hierarchy & Process Terms

| Term | Definition |
|---|---|
| **VS** | Value Stream — ระบบ business 1 ตัว end-to-end (เช่น P2P, O2C) |
| **VC** | Value Chain — happy path หลัก, decide ก่อน start (เช่น Prepay/Postpay) |
| **Path** | Process Path — event ระหว่างทาง (เจอแล้วถึงรู้, เช่น รับไม่ครบ) |
| **CL** | Chain Link — งานข้ามแผนก (cross-department phase) |
| **SOP** | Standard Operating Procedure — งานภายในแผนก (single dept phase) |
| **SOW** | Statement of Work — task 1 คน 1 deliverable (A→B→C zigzag) |
| **Scenario** | (QA term) — test scenario; ≠ Path (business term) |
| **Channel** | (legacy term) = VC; ใช้ใน skill ตัวเก่า |

---

## 🏛 Architecture Terms

| Term | Definition |
|---|---|
| **CUBE 4.0** | AI-native operating platform ของ 2BSimple — universe ที่รวม ERP + KM + AI + Governance |
| **CUBE NATIVE** | brand name + CI ของ CUBE 4.0 (Navy/Blue/Teal) |
| **Domain** | ระดับสูงสุดของ CUBE architecture (7 ตัว: Cubic, Knowledge, Core Cube, Agent, Policy, HR, Report) |
| **Module** | ระดับกลาง — group ของ features ภายใต้ Domain (เช่น Sales, Purchase ใน Core Cube) |
| **Feature** | ระดับล่าง — feature เดี่ยวที่ทำงาน 1 อย่าง (เช่น Quotation, PR) |
| **Tenant** | 1 company ที่ใช้ระบบ (1 subdomain — federated multi-tenant) |
| **Identity Hub** | layer เหนือ Core Cube — global user + tenant switcher + SSO |
| **RLS** | Row-Level Security (PostgreSQL) — บังคับ tenant data isolation |
| **AIR Schema** | Architecture Index Registry — schema กลางของ artifact ทุกประเภท |
| **CUBIC Registry** | ทะเบียนกลางใน Cubic Domain — Platform/Module/Feature/API/Engine/AIR |

---

## 🔐 Governance Terms

| Term | Definition |
|---|---|
| **DOA** | Delegation of Authority — ศูนย์กลาง approval rules (flat / sequential / threshold) |
| **RBAC** | Role-Based Access Control |
| **User Access** | RBAC matrix ใน Policy Center → ทุก feature ต้องมี entry |
| **ENC** | Enhancement — การเพิ่ม feature เข้า governance registry |
| **Feature-DOA Pairing** | iron rule: ทุก feature ต้องมี DOA + User Access entry ก่อน deploy |
| **PDPA** | Personal Data Protection Act (Thailand) — consent + DSR |
| **Data Classification** | 4-level: Public / Internal / Confidential / Restricted |
| **Restricted Resources** | resource ที่จำกัดสิทธิ์เข้าถึง (Policy Center) |

---

## 💰 P2P Terms

| Term | Definition |
|---|---|
| **PR** | Purchase Requisition — ใบขอซื้อ |
| **PO** | Purchase Order — ใบสั่งซื้อ |
| **GRN / GR** | Goods Receipt (Note) — ใบรับของ |
| **AP** | Account Payable — เจ้าหนี้การค้า |
| **AP Invoice** | ใบแจ้งหนี้จาก vendor |
| **PV** | Payment Voucher — ใบจ่ายเงิน (2 voucher_types: payment / refund) |
| **CN** | Credit Note — เอกสารลดหนี้จาก vendor |
| **RTV** | Return to Vendor — คืนของให้ vendor |
| **3-Way Match** | จับคู่ PO + GRN + AP Invoice (qty ทั้ง 3 ต้องตรง) — บังคับยกเว้น Direct Payment |
| **PO Effective Qty** | PO original qty หลัง Close Balance |
| **Invoice Net** | Invoice − CN |
| **Close PO Balance** | ปิด PO ที่ qty รับจริง (trigger ที่ GRN เท่านั้น — D07) |
| **Direct Payment** | bypass PR/PO/GRN, ไป AP Invoice ตรง (เช่น ค่าไฟ) |
| **HOLD location** | location สำหรับ QC fail items (ไม่ count เป็น available stock) |

---

## 🛒 O2C Terms

| Term | Definition |
|---|---|
| **Quotation** | ใบเสนอราคา |
| **SO** | Sales Order — คำสั่งขาย |
| **RMA** | Return Merchandise Authorization — รับคืนจากลูกค้า |
| **Tax Invoice** | ใบกำกับภาษี |

---

## 📊 Reporting Terms

| Term | Definition |
|---|---|
| **CL/PF/OP/TX** | 4-group Report Framework v2 — Closing / Performance / Operation / Transaction |
| **Closing reports** | end-of-period (P&L, ภ.พ.30) |
| **Performance reports** | KPI / trend (Sales Performance, Vendor Score) |
| **Operation reports** | status / SLA / backlog real-time |
| **Transaction reports** | รายการที่แผนกสร้าง (Quotation List) |

---

## 👥 Organization Terms (per WKN model)

| Term | Definition |
|---|---|
| **Tier M** | บริหาร — M1 ถึง M7 |
| **Tier S** | วิชาการ — S1 ถึง S6 |
| **Tier E** | ปฏิบัติการ — E8, E9 |
| **Career path** | M5 ↔ S1 สลับสายได้ |

---

## 🏭 Inventory / Manufacturing Terms

| Term | Definition |
|---|---|
| **BOM** | Bills of Materials — สูตรการผลิต |
| **UoM** | Unit of Measure — หน่วยวัด |
| **FIFO/Avg/Standard** | Inventory valuation methods |
| **Item Master** | ถังเดียวแยก type — raw/finished/consumable/service/asset/packaging |
| **Item Type** | classifier ของ item (1 item อาจมีหลาย type ในต่าง warehouse) |

---

## 📝 BA Pipeline Terms

| Term | Definition |
|---|---|
| **REQ-PHILO** | Requirement Philosophy 5-pillar (Flow/Brain/Guardrails/Health/Monitoring) |
| **PSAP/OSAP/POSAP** | Pre-Brief framework — Problem/Opportunity/Hybrid - Solution-Action-Plan |
| **RIF** | Requirement Intake Format — output ของ requirement-intake-formatter |
| **Brief Pack** | Feature handover pack (4-7 files per feature) |
| **Iron Rule** | non-negotiable rule ใน skill (เช่น R10 ของ frd-generator-v6: Data Classification) |
| **Pack Mode** | FRD format ที่แยกไฟล์ตาม layer (UI/API/LOGIC/DB/RULES/TESTS) |
| **Zigzag Pattern** | SOW format A→B→C chain |

---

## 🧪 QA Terms

| Term | Definition |
|---|---|
| **TC** | Test Case |
| **SCN** | Test Scenario document |
| **WORM** | Write Once Read Many — compliance log pattern (audit immutable) |
| **3 Layers Synthesis** | Findings format: Facts / Tensions / Gaps |

---

## 📁 Document Types

| Term | Definition |
|---|---|
| **BRD** | Business Requirements Document |
| **FRD** | Functional Requirements Document |
| **VS Bible** | Master document of a Value Stream |
| **Charter** | High-level scope document (Stage A) |
| **Handover Pack** | Multi-file feature spec for downstream skill |

---

## Change Log

- **1.0.0** (2026-05-27): Initial glossary — 8 categories
