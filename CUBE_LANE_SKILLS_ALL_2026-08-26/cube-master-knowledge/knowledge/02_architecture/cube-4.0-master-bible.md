---
file_id: KB-02-01
title: CUBE 4.0 Master Bible
version: 1.0.0
last_updated: 2026-05-27
status: stable
source: CUBE_4_0_MASTER_BIBLE.md (original, 2026-05-22)
superseded_note: |
  ★ 2026-08-25 — §2–§3 (7 domain แยก site) ล้าสมัย: HR/Agent/Report/Policy ยุบเข้า Core ERP เดียวแล้ว
  โครงปัจจุบัน + baseline + มติ → cube-4.0-current-state.md · catalog → 05_features v2.0
  ยังใช้ได้: §4 Architecture Patterns · §5 Dev Process · §8 Glossary
---

# CUBE 4.0 — Master Bible

**Version**: 1.0
**Status**: Architecture Finalized
**Last Updated**: 2026-05-22
**Owner**: 2BSimple Co., Ltd.

---

## 1. ภาพรวม (Overview)

CUBE 4.0 คือ **AI-native operating platform** ของ 2BSimple — ขยายจาก CUBE NATIVE (SaaS ERP) ไปเป็น **ระบบนิเวศแบบ Universe** ที่รวม Core ERP + Knowledge Hub + AI Agent + Policy Governance + HR ไว้ในจักรวาลเดียวกัน

### หลักการออกแบบ (Design Principles)

1. **Domain-Module-Feature Hierarchy** — โครงสร้าง 3 ชั้น (Domain → Module → Feature)
2. **Federated Multi-Tenant** — แต่ละ company = ERP แยก (data silo จริง) เชื่อมผ่าน Identity Hub
3. **Master กลาง + Config ต่อ Module** — Master Data อยู่กับ module เจ้าของ, แต่ละ module มี config ของตัวเอง
4. **Governance-as-Layer** — Policy / DOA / Audit เป็น cross-cutting layer (ไม่ฝังในแต่ละ module)
5. **AI-First** — ทุก module ออกแบบให้ AI Agent เรียกใช้ได้ผ่าน API + Skill BRD/FRD/HTML

### Color Code (จาก Diagram)

| Color | ความหมาย |
|---|---|
| **สีดำ (กรอบใหญ่)** | Domain |
| **สีดำ (กรอบกลาง)** | Module |
| **สีฟ้า** | Feature |
| **สีส้ม** | External Integration |

---

## 2. โครงสร้างระดับ Domain

CUBE 4.0 ประกอบด้วย **7 Domains** + **1 External Integration**:

```
┌───────────────────────────────────────────────────────────────┐
│                         CUBE 4.0                              │
├───────────────┬───────────────────────────────┬───────────────┤
│   Cubic       │      Claude Automation (Ext)  │               │
├───────────────┼───────────────────────────────┴───────────────┤
│   Knowledge   │   Core Cube   │   Agent   │  Policy Center    │
│   (+ CMS)     │               │           │                   │
├───────────────┼───────────────┼───────────┼───────────────────┤
│               │    Report     │     HR    │                   │
└───────────────┴───────────────┴───────────┴───────────────────┘
```

### สรุป Domain ทั้งหมด

| # | Domain | บทบาท | ผู้ใช้หลัก |
|---|---|---|---|
| 1 | **Cubic** | System backbone — registry + notification + sandbox + onboarding | Platform Admin |
| 2 | **Knowledge** + **Knowledge CMS** | Content Hub สาธารณะ + admin หลังบ้าน | End User (public) + Internal Editor |
| 3 | **Core Cube** | ERP Core (12 modules) — เป็นหัวใจของระบบ | Tenant User |
| 4 | **Agent** | AI Agent orchestration + launcher | All Users |
| 5 | **Policy Center** | Governance — Policy / User / Data / Security / Compliance | Compliance Officer + Admin |
| 6 | **HR** | Human Resources — Lifecycle / Performance / Payroll / Time | HR Team |
| 7 | **Report** | Company Report — Overview + People analytics | Executive + Manager |
| Ext | **Claude Automation** | External skill engine (Skill BRD/FRD/HTML pipeline) | BA / Dev |

---

## 3. รายละเอียดแต่ละ Domain

### 3.1 Cubic Domain

**บทบาท**: System backbone — เป็น **registry กลาง** ของทุก artifact ในระบบ + notification engine + onboarding workflow

**ขอบเขต**: เห็นเฉพาะ Platform Admin (2BSimple staff) — Tenant User เข้าไม่ได้

#### Modules:

##### 3.1.1 System Development
ทะเบียนกลางของทุกองค์ประกอบทาง technical ในระบบ (CUBIC Registry concept)

| Feature | คำอธิบาย |
|---|---|
| Platform | ทะเบียน platform (cube.com, reportcube.com, ...) |
| Module | ทะเบียน module ทั้งหมดในระบบ (Sales, Purchase, ...) |
| Feature | ทะเบียน feature ทุกตัว (Quotation, SO, PO, ...) — ใช้ทำ index/discovery |
| AIR Schema | Architecture Index Registry — schema ของ artifact ทุกประเภท |
| Engine | ทะเบียน engine 18 ตัว (EN-001..EN-018) — Function Numbers (FN-[PREFIX]-[NNN]) |
| API | ทะเบียน API endpoint ทั้งหมด |

##### 3.1.2 Notification Management
| Feature | คำอธิบาย |
|---|---|
| Notification | ส่ง notification ข้ามระบบ (in-app, email, LINE, SMS) |
| Notification Logs | log + audit ของทุก notification ที่ส่ง |

##### 3.1.3 Sandbox
| Feature | คำอธิบาย |
|---|---|
| Onboarding Sandbox | sandbox สำหรับ tenant ใหม่ลองเล่น 22 features × scenarios |

##### 3.1.4 Onboarding
| Feature | คำอธิบาย |
|---|---|
| Onboarding 30 Days Hypercare | Workflow รับ tenant ใหม่ 30 วันแรก (training, support, monitoring) |

---

### 3.2 Knowledge Domain (Public-Facing)

**บทบาท**: Content Hub สาธารณะ — magazine SPA สำหรับ acquire prospect → convert เป็น tenant

**ขอบเขต**: Public (3 tiers: Free / Registered / Paid)

#### Module: Knowledge Site

| Feature | คำอธิบาย |
|---|---|
| Home | Landing page — Hero + filterable article grid |
| Register | Sign-up เป็น Registered user (free tier ขยับขึ้น) |
| Pillar | 5 pillars: จัดซื้อ / ขาย / สต็อก / การเงิน / AI |
| Article | 19 articles แบ่งตาม pillar + tier (Free/Registered/Paid) |
| My Profile | Profile + Settings + tier upgrade |

---

### 3.3 Knowledge CMS Domain (Internal Editor)

**บทบาท**: หลังบ้านของ Knowledge Hub — สร้าง/แก้ไข content + author management

**ขอบเขต**: 2BSimple Internal Editor

#### Module: Article Management

| Feature | คำอธิบาย |
|---|---|
| Pillar CMS | จัดการ pillar (สร้าง/แก้ไข/จัดลำดับ) |
| Article CMS | จัดการ article (CRUD + publish workflow + tier setting) |
| Author | ทะเบียน author + bio + profile + access control |
| Scraping Pool | external content scraping queue (sourcing pipeline) |

---

### 3.4 Core Cube Domain ⭐ (หัวใจของระบบ)

**บทบาท**: ERP Core — ทุก transactional operation ของ tenant อยู่ที่นี่

**ขอบเขต**: Tenant User (per-company data silo via PostgreSQL RLS)

**ประกอบด้วย 12 Modules**:

#### 3.4.1 Home Module
หน้าแรกของ tenant — landing เข้าระบบ

| Feature | คำอธิบาย |
|---|---|
| Home | Dashboard ภาพรวม + KPI + Notification panel + My Tasks |
| My Profile | Profile ส่วนตัว + e-Signature upload + preferences |

#### 3.4.2 Operation Process Module
ระบบจัดการกระบวนการทำงาน CL/SOP/SOW (เป็น signature ของ 2BSimple)

| Feature | คำอธิบาย |
|---|---|
| Operation Process | จัดการ CL instance (work order) — track งานจริง |
| Template Management | ทะเบียน CL/SOP/SOW Template (master) |

#### 3.4.3 Sales Module
Order-to-Cash (O2C) workflow

| Feature | คำอธิบาย |
|---|---|
| Quotation | ใบเสนอราคา |
| Sales Order | คำสั่งขาย |
| Promotion | promotion campaign + discount rule |
| Customer | ลูกค้า (Master Data — สังกัด Sales module) |
| Customer Segment | จำแนกประเภทลูกค้า (VIP/Standard/...) |
| Price List | รายการราคาขาย (per segment / per item) |
| Invoice / Tax Invoice | ใบกำกับภาษี/ใบแจ้งหนี้ |
| Credit Note / Debit Note | ใบลด/เพิ่มหนี้ |
| Sales Return | คืนสินค้าจากลูกค้า (RMA) — link กับ Credit Note |
| Sales Configuration | Config ของ Sales module (default term, approval rule, allowed item type) |

#### 3.4.4 Marketing Module
Lead generation + campaign

| Feature | คำอธิบาย |
|---|---|
| Prospect | Lead capture + scoring + assignment |
| Campaign Management | จัดการ campaign (plan/budget/timeline/ROI) |
| Email/Communication Marketing | Email/SMS/LINE OA broadcast + tracking |

#### 3.4.5 Inventory Module
Warehouse + Stock + Item Master

| Feature | คำอธิบาย |
|---|---|
| Warehouse Location | คลังสินค้า + location hierarchy |
| Inventory | Stock balance + valuation |
| Goods Receipt News | รับสินค้าเข้าคลัง (จาก PO / Return) |
| Put Away | จัดเก็บเข้า location |
| Pick | เบิกของจาก location |
| Pack | บรรจุพร้อมส่ง |
| Delivery Note | ใบส่งของ |
| Stocktake | นับสต็อก (cycle count / annual count) |
| Stock Adjustment | ปรับสต็อก (write-off / write-on) |
| Stock Transfer | โอนสต็อกระหว่าง warehouse |
| **Item / Product** ⭐ | Master Data — ถังเดียว แยกด้วย `item_type` (raw_material/finished_good/consumable/service/asset/packaging) — เก็บได้หลายรหัส (internal/material/product/barcode/vendor code) |
| Product Category | หมวดหมู่สินค้า |
| Unit of Measure (UoM) | หน่วยวัด (cross-module shared) |
| Bills of Materials (BOM) | สูตรการผลิต — header + lines (version, effective date, approval) |
| Inventory Configuration | Config ของ Inventory (valuation method: FIFO/Avg/Standard, sellable/purchasable rules) |

**หมายเหตุ**: BOM อยู่ใน Inventory ตอน Phase 1 — ย้ายไป Manufacturing module ตอนเปิด scope จริง

#### 3.4.6 Purchase Module
Procure-to-Pay (P2P) workflow

| Feature | คำอธิบาย |
|---|---|
| Purchase Requisition | ใบขอซื้อ (PR) |
| Comparison Form | เปรียบเทียบราคา 3 vendor |
| Purchase Order | ใบสั่งซื้อ (PO) |
| Supplier / Vendor | ทะเบียนผู้ขาย (Master Data — สังกัด Purchase) |
| Vendor Category | จำแนกประเภท vendor |
| Purchase Return | คืนของให้ vendor (RTV) — link กับ Debit Note |
| Purchase Configuration | Config ของ Purchase (vendor payment term, 3-way match rule, approval) |

**หมายเหตุ**: 3-way Match (PO+GR+Invoice) ทำที่ AP Invoice ใน Accounting module

#### 3.4.7 Budget Module
Budget planning + execution

| Feature | คำอธิบาย |
|---|---|
| Fiscal Year & Master Management | ปีงบประมาณ + master setup |
| Budget Preparation | จัดทำงบประมาณประจำปี |
| Budget Request | ขอใช้งบ (in-year request + transfer) |
| Budget Configuration | Config ของ Budget (approval threshold, control level) |

#### 3.4.8 IT Support Module
Internal IT helpdesk

| Feature | คำอธิบาย |
|---|---|
| Ticket | IT ticket system |

#### 3.4.9 Accounting Module
General ledger + statutory reporting

| Feature | คำอธิบาย |
|---|---|
| GL / Journal Entry | บัญชีแยกประเภท + เดบิต/เครดิต manual entry |
| AR (Account Receivable) | ลูกหนี้การค้า |
| AP (Account Payable) | เจ้าหนี้การค้า + 3-way match |
| Bank Reconciliation | กระทบยอดธนาคาร |
| Chart of Accounts | ผังบัญชี (per company) |
| Cost Center / Profit Center | ศูนย์ต้นทุน / ศูนย์กำไร |
| Tax Code | รหัสภาษี (VAT 7%, WHT 1%, 3%, 5%, ...) |
| Currency & Exchange Rate | สกุลเงิน + อัตราแลกเปลี่ยน |

#### 3.4.10 Finance Module
Cash + payment + treasury

| Feature | คำอธิบาย |
|---|---|
| Bank Master | ทะเบียนบัญชีธนาคาร |
| Payment Method | วิธีจ่าย (โอน, เช็ค, สด, บัตรเครดิต) |
| Payment Term | เงื่อนไขชำระ (NET30, NET60, COD, ...) — master ของกลาง |
| Receipt Voucher | ใบรับเงิน |
| Payment Voucher | ใบจ่ายเงิน (`voucher_type`: payment / refund) — รองรับ Full Prepay Refund flow |
| Cash Flow | กระแสเงินสด (forecast + actual) |
| Petty Cash | เงินสดย่อย |

#### 3.4.11 Asset Management Module
Fixed asset lifecycle

| Feature | คำอธิบาย |
|---|---|
| Asset Master | ทะเบียนทรัพย์สิน |
| Depreciation | คำนวณค่าเสื่อม (straight-line / declining) |
| Maintenance Schedule | ตารางบำรุงรักษา (PM / CM) |

#### 3.4.12 Organization Module ⭐
โครงสร้างองค์กร (per-tenant — ของบริษัทตัวเอง)

| Feature | คำอธิบาย |
|---|---|
| Company Master | ข้อมูลบริษัทตัวเอง (ไม่มี hierarchy ข้าม tenant) |
| Branch / Location | สาขา/สำนักงาน (ภายใน company) |
| Department | แผนก |
| Position & Tier | ตำแหน่ง + ระดับ — ตาม WKN model: **บริหาร (M1-M7) / วิชาการ (S1-S6) / ปฏิบัติการ (E8-E9)** + career path rule (M5 ↔ S1 สลับสายได้) |

---

### 3.5 Agent Domain

**บทบาท**: AI Agent orchestration — ทุก feature ใน Core Cube จะมี AI Agent ช่วยทำงาน

**ขอบเขต**: All Users (per role)

#### Module: Agent

| Feature | คำอธิบาย |
|---|---|
| Agent Management | จัดการ agent (skill, prompt, data access) |
| Frontend Launcher | UI launcher ของ agent (chat bubble, command palette) |
| Agent Management (CMS) | หลังบ้านจัดการ agent (training data, skill registry) |

---

### 3.6 Policy Center Domain ⭐ (Governance Layer)

**บทบาท**: ระบบ Governance กลาง — **ทุก feature ที่มี approval ต้อง wire ไปที่ DOA ที่นี่** (ห้าม hardcode approval rule ในแต่ละ module)

**ขอบเขต**: Compliance Officer + System Admin (per-tenant)

#### Modules:

##### 3.6.1 Policy Management
| Feature | คำอธิบาย |
|---|---|
| Policy Document | นโยบาย/SOP/Document ระดับองค์กร (multi-version, audit trail) |

##### 3.6.2 User Management
| Feature | คำอธิบาย |
|---|---|
| System User | ทะเบียน user (Identity ระดับ tenant) |
| User Roles Access | RBAC matrix |

##### 3.6.3 Data Governance
| Feature | คำอธิบาย |
|---|---|
| PDPA | PDPA consent + DSR (Data Subject Request) |
| Data Classification | จัดประเภทข้อมูล (Public / Internal / Confidential / Restricted) |
| Restricted Resources | ทะเบียน resource ที่จำกัดสิทธิ์เข้าถึง |
| DOA | **Delegation of Authority** — ศูนย์กลางของทุก approval rule ในระบบ (flat / sequential / threshold by amount) |

##### 3.6.4 Security & Risk
| Feature | คำอธิบาย |
|---|---|
| Security Control | 78 security controls (รวมใน framework) |
| Risk | Risk register + assessment |

##### 3.6.5 Monitoring & Compliance
| Feature | คำอธิบาย |
|---|---|
| Reports | Compliance report (cross-module) |
| Audit | Audit log ทั้งระบบ |

---

### 3.7 HR Domain

**บทบาท**: HR ครบ lifecycle ตั้งแต่ Recruit → Performance → Payroll → Time

**ขอบเขต**: HR Team (per-tenant)

#### Modules:

##### 3.7.1 Insights & Overview
| Feature | คำอธิบาย |
|---|---|
| Analytics | HR analytics |
| Dashboard | HR dashboard |

##### 3.7.2 Employee Lifecycle
| Feature | คำอธิบาย |
|---|---|
| Candidate Pool | ฐานข้อมูลผู้สมัคร |
| Recruit | จัดการการรับสมัคร (job posting → interview → offer) |
| Onboard | กระบวนการ onboard พนักงานใหม่ |
| Employee Portfolio | แฟ้มประวัติพนักงาน |
| Offboard | กระบวนการลาออก/พ้นสภาพ |

##### 3.7.3 Performance & Development
| Feature | คำอธิบาย |
|---|---|
| Discipline | บันทึกวินัย |
| Performance | ประเมินผลงาน (per cycle) |

##### 3.7.4 Payroll & Time
| Feature | คำอธิบาย |
|---|---|
| Payroll | บัญชีเงินเดือน |
| Salary | โครงสร้างเงินเดือน (ผูก Tier Master จาก Organization module) |
| Leave Day | การลา |
| OT / Shift Management | OT + กะการทำงาน |
| Attendance / Time Tracking | บันทึกเวลาเข้า-ออก |

##### 3.7.5 Configuration
| Feature | คำอธิบาย |
|---|---|
| Company Information | ข้อมูลบริษัทในมุม HR (working hour, leave policy, holidays) |

---

### 3.8 Report Domain

**บทบาท**: Cross-module reporting + executive dashboard

**ขอบเขต**: Executive + Manager (per-tenant)

#### Module: Company Report

| Feature | คำอธิบาย |
|---|---|
| Overview | Executive overview (อิง 4-group framework: CL/PF/OP/TX) |
| People | People analytics (cross HR + Organization) |

---

### 3.9 External: Claude Automation

**บทบาท**: Skill-based document generation pipeline — สำหรับ BA/Dev สร้างเอกสาร mass

| Feature | คำอธิบาย |
|---|---|
| Skill BRD | Generate BRD จาก RIF |
| Skill FRD | Generate FRD จาก BRD |
| Skill HTML | Generate HTML Prototype จาก FRD |

**Integration point**: เชื่อมกับ Cubic → System Development (artifact registry)

---

## 4. Architecture Patterns

### 4.1 Multi-Tenant Federated

แต่ละ company = **ERP แยก instance** (ไม่ share data ไม่มี intercompany)

```
Identity Hub (Layer เหนือ Core Cube)
├─ Global User Account (1 user → access N tenants)
├─ Tenant Registry (wkn-main / wkn-uthong / slick-auto / coe / credence / ...)
├─ User-Tenant Access Matrix
├─ Tenant Switcher (UI redirect ข้าม subdomain)
└─ SSO (login ครั้งเดียว → access ทุก tenant ที่มีสิทธิ์)

แต่ละ Tenant = ERP instance แยก:
└─ {tenant}.cube.com → Core Cube (12 modules) + Policy Center + HR + Report + Agent + Knowledge

Data Isolation:
- ทุก transactional table มี company_id
- PostgreSQL RLS enforce ทุก query
- ไม่มี cross-tenant query (ยกเว้น Identity Hub layer)
```

### 4.2 Master Data Strategy

**Hybrid: Operational ownership + Configuration per module**

```
Master Data ownership:
├─ Item/Product/BOM/UoM → Inventory module (เพราะ Inventory track movement จริง)
├─ Customer/Segment/Price List → Sales module
├─ Vendor/Vendor Category → Purchase module
├─ COA/Cost Center/Tax/Currency → Accounting module
├─ Bank/Payment Method/Payment Term → Finance module (master ของกลาง)
├─ Employee → HR module
└─ Position/Tier/Department/Branch/Company → Organization module

Configuration per module:
├─ Sales Configuration: default term, allowed item type, approval rule
├─ Purchase Configuration: vendor payment term, 3-way match rule
├─ Inventory Configuration: valuation method (FIFO/Avg/Standard)
└─ Budget Configuration: approval threshold
```

**Pattern**:
- **Master** = ตัว data จริง อยู่ที่เดียว ห้ามซ้ำ → module เจ้าของ
- **Configuration** = "module นี้ใช้ master ตัวไหน, default คืออะไร, rule ยังไง" → อยู่ใน module ที่ใช้



### 4.4 Item Master Strategy

**ถังเดียวแยก type** (เลียนแบบ SAP MARA + Odoo product.template)

```
Item Master (1 table):
├─ item_type: [raw_material | finished_good | consumable | service | asset | packaging]
├─ codes: { internal_code, material_code, product_code, barcode, vendor_code }
├─ flags: { is_sellable, is_purchasable, is_stockable }
└─ views: { sales_view, purchase_view, stock_view } — module เห็นเฉพาะที่ extend view

ตัวอย่าง (WKN sugar):
น้ำตาลทรายขาว 50kg:
├─ types: [raw_material, finished_good]  ← เป็นได้ทั้งของผลิต + ของขาย
├─ ที่โรงงาน A: finished_good (ผลิตขาย)
└─ ที่โรงงาน B: raw_material (ซื้อมาทำขนม)
```

### 4.5 Payment Term Strategy

**2 ชั้น: Master + Pattern**

```
Layer 1 (Master Payment Term) → Finance module:
- NET30, NET60, NET90, COD, 2/10 NET30, ...

Layer 2 (Settlement Pattern) → Purchase/Sales Configuration:
- จ่ายก่อนรับ (prepay 100%)
- จ่ายหลังรับ (post-pay)
- มัดจำ 30% + ส่วนที่เหลือเมื่อส่งของ
- จ่ายตามงวด (milestone)
- จ่ายเครดิต (ใช้ payment term)
```

### 4.6 e-Signature

- Upload ครั้งเดียวที่ **Core Cube → Home → My Profile**
- ทุก feature ที่ต้อง sign → ดึง signature จาก user record
- DRY (Don't Repeat Yourself) — ไม่ upload ซ้ำในแต่ละ module

### 4.7 Report Framework v2

**4 กลุ่ม ใช้เหมือนกันทุกแผนก** — Report ownership = แผนกที่รับผิดชอบงาน ไม่ใช่แผนกที่ข้อมูลเกี่ยวข้อง

| Group | คำอธิบาย | ตัวอย่าง |
|---|---|---|
| **CL** Closing | ปิดยอด end of period | P&L, ภ.พ.30, ภ.ง.ด.53 |
| **PF** Performance | KPI / trend | Sales Performance, Vendor Score |
| **OP** Operation | Status / SLA / backlog real-time | Open PO, Pending Approval |
| **TX** Transaction | รายการที่แผนกสร้าง | Quotation List, PO List |

---

## 5. Development Process Standard ⭐

**กฎเหล็กของ CUBE 4.0**: ทุก feature ที่พัฒนาต้องผ่าน 2 governance checkpoints เสมอ — **ไม่มีข้อยกเว้น**

### 5.1 หลักการกลาง

```
┌─────────────────────────────────────────────────────────┐
│  ทุก Feature ต้องบันทึกที่ 2 ที่ก่อน deploy:             │
│                                                         │
│  1. User Access (Policy Center → User Roles Access)     │
│     → ใครเข้าถึง feature นี้ได้บ้าง                       │
│                                                         │
│  2. DOA (Policy Center → Data Governance → DOA)         │
│     → ถ้า feature นั้นมี approve / sign / consent       │
│     → ทุก approval rule รวมศูนย์ที่ DOA ที่เดียว         │
└─────────────────────────────────────────────────────────┘
```

### 5.2 Feature Development Lifecycle

**Pattern: "Feature-DOA Pairing"** — สร้าง feature เป็นชุดๆ พร้อม governance ครบทุกชุด

```
┌──────────────────────────────────────────────────────┐
│  Step 1: สร้าง Feature X                              │
│  ├─ Build UI + Logic + DB                            │
│  ├─ ใส่ field placeholder:                           │
│  │   ├─ approver_role                                │
│  │   ├─ approved_by                                  │
│  │   └─ approval_chain                               │
│  └─ ใส่ TODO comment รอ DOA wire                      │
└──────────────────────────────────────────────────────┘
                       ↓
┌──────────────────────────────────────────────────────┐
│  Step 2: ENC DOA สำหรับ Feature X                     │
│  ├─ เพิ่ม Feature X เข้า DOA registry                  │
│  ├─ Set approval pattern:                            │
│  │   ├─ flat (1 approver)                            │
│  │   ├─ sequential (chain)                           │
│  │   └─ threshold (by amount/scope)                  │
│  ├─ Define scope:                                    │
│  │   ├─ เซ็นเอกสาร                                    │
│  │   ├─ อนุมัติ policy                                │
│  │   └─ อนุมัติงบตามวงเงิน                              │
│  └─ Wire กับ field placeholder ของ Feature X         │
└──────────────────────────────────────────────────────┘
                       ↓
┌──────────────────────────────────────────────────────┐
│  Step 3: ENC User Access สำหรับ Feature X             │
│  ├─ เพิ่ม Feature X เข้า User Roles Access matrix     │
│  └─ Define: ใคร / role ไหน เข้าถึงได้                 │
└──────────────────────────────────────────────────────┘
                       ↓
┌──────────────────────────────────────────────────────┐
│  Step 4: Feature X พร้อม Production                   │
│  ✓ Access control ครบ                                │
│  ✓ Approval rule ครบ                                 │
│  ✓ Audit trail ครบ                                   │
└──────────────────────────────────────────────────────┘
                       ↓
              [ทำซ้ำกับ Feature Y, Z, ...]
```

### 5.3 ENC DOA Pattern

**ENC (Enhancement) DOA** = การเพิ่ม feature ใหม่เข้าระบบ governance กลาง

```
ENC DOA Registry Structure:

DOA Master Table:
├─ feature_id              ← link กับ Feature ใน System Development module
├─ feature_name
├─ approval_required       ← true/false
├─ approval_scope          ← document_sign / policy_approve / budget_approve
├─ approval_pattern        ← flat / sequential / threshold
├─ approval_chain[]        ← list of role / position
├─ threshold_rules[]       ← ถ้า pattern = threshold
│   ├─ amount_from
│   ├─ amount_to
│   └─ required_approvers[]
├─ consent_required        ← true/false (สำหรับ PDPA / user consent)
├─ active                  ← enabled/disabled
└─ effective_date          ← เริ่มใช้เมื่อไร
```

### 5.4 User Access ENC Pattern

```
User Roles Access Registry Structure:

UserAccess Matrix:
├─ feature_id              ← link กับ Feature
├─ role_id                 ← link กับ Role
├─ permissions[]:
│   ├─ view
│   ├─ create
│   ├─ edit
│   ├─ delete
│   ├─ approve
│   ├─ export
│   └─ print
└─ scope_filter            ← optional: department / branch / project scope
```

### 5.5 Anti-Patterns ที่ห้ามทำ

❌ **Hardcode approval rule ใน feature**
- ผิด: `if user.role == "manager" && amount < 100000`
- ถูก: เรียก DOA engine → `DOA.checkApproval(feature_id, amount, user)`

❌ **Skip User Access registration**
- ทุก feature ต้องมี entry ใน User Roles Access ก่อน deploy

❌ **DOA per module** (กระจาย rule)
- ทุก approval rule ต้องอยู่ใน DOA module ที่เดียว
- Module อื่น "ถาม" DOA — ไม่ "ตัดสิน" เอง

❌ **Deploy feature โดยไม่มี DOA entry** (ถ้า feature มี approval)
- ต้อง pair: Feature created → DOA ENC → User Access ENC → Deploy

### 5.6 Pipeline ทาง Document

```
Feature Brief / BRD ของทุก feature ต้องระบุ:

Section: Governance
├─ User Access Requirements
│   ├─ ใคร / role ไหนเข้าถึงได้
│   ├─ Permissions ที่ต้องการ (view/create/edit/delete/...)
│   └─ Scope filter (ถ้ามี)
│
└─ DOA Requirements (ถ้า feature มี approval)
    ├─ ต้อง approve อะไร (document/policy/budget)
    ├─ Pattern (flat/sequential/threshold)
    ├─ Chain หรือ threshold rules
    └─ Consent required (PDPA)
```

**Skill ที่เกี่ยวข้อง**:
- `frd-generator-v6` — ต้องมี section Governance ใน FRD ทุกฉบับ
- `html-generator-v9` — ต้องสร้าง UI placeholder field (approver_role / approved_by / approval_chain)
- `brd-generator-full` — ต้องบังคับให้ระบุ User Access + DOA requirements

### 5.7 Audit Trail Standard

ทุก action ที่เกี่ยวกับ governance ต้องบันทึก:

```
Audit Log:
├─ timestamp
├─ user_id
├─ feature_id
├─ action               ← view / create / approve / reject / sign / consent
├─ before_state
├─ after_state
├─ approval_chain_state ← ถ้าเป็น approval action
├─ ip_address
└─ user_agent
```

**Storage**: Policy Center → Monitoring & Compliance → Audit

---

## 6. Roadmap & Phasing

### Phase 1 — MVP (Cube 4.0 Core)
**Core Cube 12 modules + Policy Center + HR + Agent + Knowledge Hub**

ครอบคลุมทุก feature ในเอกสารนี้ — production-ready สำหรับ SME ทั่วไป + WKN-style multi-tenant

### Phase 2 — Extensions
- **Manufacturing module** (Production Order, Work Order, Material Issue) — สำหรับ WKN sugar
- **Project module** (Project Master, Cost Tracking)
- **Master Data Governance module** (cross-tenant master sync — ถ้าจำเป็น)
- **Document Management module** (file storage + versioning)
- **Number Series Master + Print Template Master**

### Phase 3 — Enterprise Mature
- **Cross-Company Consolidation** (ถ้า requirement เปลี่ยนเป็น shared model)
- **Advanced Workflow Engine**
- **Group-level DOA** (escalation ข้าม tenant)
- **PLM-full** (Recipe, ECO, Compliance)

---

## 7. Module Count Summary

| Domain | Module Count | Feature Count |
|---|---|---|
| Cubic | 4 | ~10 |
| Knowledge | 1 | 5 |
| Knowledge CMS | 1 | 4 |
| **Core Cube** | **12** | **~75** |
| Agent | 1 | 3 |
| Policy Center | 5 | ~12 |
| HR | 5 | ~17 |
| Report | 1 | 2 |
| Claude Automation | (external) | 3 |
| **รวม** | **~30** | **~131** |

---

## 8. Glossary

| Term | คำอธิบาย |
|---|---|
| **AIR Schema** | Architecture Index Registry — schema กลางของ artifact ทุกประเภท |
| **CL** | Chain Link — ระดับสูงสุดของ Operation Process (cross-department workflow) |
| **SOP** | Standard Operating Procedure — ระดับ department |
| **SOW** | Statement of Work — task-level (1 person, 1 deliverable) |
| **DOA** | Delegation of Authority — กฎการมอบอำนาจอนุมัติ |
| **RBAC** | Role-Based Access Control |
| **RLS** | Row-Level Security (PostgreSQL) — บังคับ data isolation |
| **RTV** | Return To Vendor — คืนของให้ผู้ขาย |
| **RMA** | Return Merchandise Authorization — รับคืนจากลูกค้า |
| **3-way Match** | จับคู่ PO + GR + Invoice ก่อนตั้งหนี้ |
| **PSAP/OSAP** | Pre-Brief framework: Problem-Solution-Action-Plan / Opportunity-Solution-Action-Plan |
| **REQ-PHILO** | Requirement Philosophy 5-pillar (Flow/Brain/Guardrails/Health/Monitoring) |
| **BOM** | Bills of Materials — สูตรการผลิต |
| **COA** | Chart of Accounts — ผังบัญชี |
| **UoM** | Unit of Measure — หน่วยวัด |
| **Tenant** | 1 company ที่ใช้ระบบ (1 subdomain) |
| **Tier (WKN)** | ระดับตำแหน่ง: M (บริหาร 1-7) / S (วิชาการ 1-6) / E (ปฏิบัติการ 8-9) |

---

## 9. Visual Reference

โครงสร้างเต็มอยู่ใน:
- `StriKE_-_Cube_Universe_Feature.jpg` (visual diagram จาก draw.io)
- Memory ID #22 (CUBE 4.0 architecture summary)

---

**End of CUBE 4.0 Master Bible v1.0**

*เอกสารฉบับนี้เป็น single source of truth สำหรับการพัฒนา CUBE 4.0 ทุก session — ทีมสามารถอ้างอิงข้ามแชทได้โดยไม่ต้องเริ่มต้นใหม่*
