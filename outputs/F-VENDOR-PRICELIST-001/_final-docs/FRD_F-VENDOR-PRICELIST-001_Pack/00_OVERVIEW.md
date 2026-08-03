# 00_OVERVIEW — F-VENDOR-PRICELIST-001 Vendor Price List

> **Audience:** PM, BA, FE, BE, QA, DBA และ Architect  
> **Purpose:** ขอบเขต ภาพรวมสถาปัตยกรรม dependency และจุดเริ่มอ่าน FRD Pack

---

## §0.1 Document Control

| Field | Value |
|---|---|
| **Feature ID** | `F-VENDOR-PRICELIST-001` |
| **Legacy alias** | `F-VENDOR-PRICE-LIST` — ใช้ค้นหา/redirect เท่านั้น |
| **Feature Name** | Vendor Price List / รายการราคาคู่ค้า |
| **Module** | Purchase |
| **Variant** | FULL |
| **Status** | IN-REVIEW |
| **FRD Version** | 1.0 — 2026-08-03 |
| **Generator** | frd-generator-v6 |
| **Source BRD** | `../BRD_VendorPriceList_v2.4.md` — APPROVED |
| **Source HTML** | `../vendor-price-list-v6.html` — current UI source of truth |
| **Author** | AI-assisted BA handoff |
| **Reviewers** | PM, Tech Lead, QA Lead, Security/Policy owner |

## §0.2 Revision History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-08-03 | Initial FULL Pack จาก BRD v2.4 + HTML v6 ที่ผ่านการปรับร่วมกับผู้ใช้ |

## §0.3 Outcome และ Scope

Feature นี้เป็นแหล่งข้อมูลราคาซื้อจากคู่ค้าแบบมีเวอร์ชันและการอนุมัติ เพื่อให้ PR/RFQ/PO ใช้ราคาเดิมได้อย่างตรวจสอบย้อนหลัง แม้ภายหลังจะมีการเปลี่ยนราคาใหม่

### In Scope

- Price Header ตาม tenant/company/site(optional)/vendor/product/purchase UOM/currency
- ราคาแบบ flat และ tier พร้อม validity, price-per, discount, freight และ tax code
- สร้างร่าง ส่งอนุมัติ อนุมัติ ปฏิเสธ เปิด/ปิดใช้งาน และสร้าง Price Version ใหม่
- Single entry, Batch Entry และ CSV import แบบ preview/validate/duplicate-check/confirm
- ค้นหาและเลือกคู่ค้าจาก `F-VENDOR` เฉพาะ `status=active`
- ค้นหาและเลือกสินค้าจาก Product Master เฉพาะ `status=active && purchasable=true` พร้อม Purchase UOM
- เปรียบเทียบ landed unit cost ก่อนภาษีด้วย qty/date/FX เดียวกัน เรียงต่ำไปสูง
- Resolve ราคาให้ downstream พร้อม `price_version_id` และ calculation snapshot/trace
- DOA tier, SoD, SLA 1 วันทำการ, Confidential masking และ WORM history

### Out of Scope

- Sales Price List
- AVL, preferred vendor, contract editor/lock, lead time, MOQ/MPQ
- Attachment, OCR และ AI price recommendation
- เอกสารธุรกรรม A4/PDF ของ feature นี้
- Company/Site picker บนฟอร์ม: `company_id` มาจาก session context และ `site_id=null` ใน UI รุ่นนี้
- การสร้างหรือแก้ Vendor/Product/UOM/FX/DOA master จากหน้านี้
- การแก้ identity ของ Header ที่ Active แล้ว; เปลี่ยน Purchase UOM/สกุลเงินต้องสร้าง Header ใหม่จากรายการเดิม

## §0.4 Roles & COSO

| Role | COSO | Responsibility |
|---|---|---|
| `procurement_officer` | Maker | สร้าง/แก้ร่าง, batch/import, ส่งอนุมัติ, เปิด/ปิดรายการ |
| `procurement_manager` | Checker/Approver | ตรวจ อนุมัติ หรือปฏิเสธตาม DOA; ห้ามอนุมัติคำขอตนเอง |
| `procurement_director` | Approver | อนุมัติ elevated tier ตาม DOA |
| `finance_viewer` | Viewer | ดูราคาและ calculation trace ตามสิทธิ์ |
| `admin` | Administrator | สิทธิ์ปฏิบัติการตาม role mapping แต่ยังต้องผ่าน SoD |
| other authenticated roles | Viewer | ดูโครงสร้างรายการ แต่ค่าราคา Confidential ถูก mask |

## §0.5 Dependencies

### Upstream

| Dependency | Contract ที่ใช้ | Source of truth |
|---|---|---|
| F-VENDOR | `GET /api/v1/vendors?status=active`, `GET /api/v1/vendors/:id`; UUID, code/name, status, currency | `../../F-VENDOR/_final-docs/FRD_F-VENDOR_Pack` |
| F-PRODUCT-MASTER-001 | `GET /api/v1/products?status=active`, `GET /api/v1/products/:id`; UUID, code/name, purchasable, UOM, VAT group | `../../../Related context/Item Master/FRD` |
| Company/session context | `tenant_id`, `company_id`, optional `site_id` | Identity/Organization context |
| Policy Center / DOA | approval route, threshold config, SLA/escalation | Central policy service |
| FX Master | dated FX rate + freshness policy | Finance master |
| Finance Posting Setup | tax/GL mapping | Finance module |

### Downstream

| Consumer | What it uses |
|---|---|
| PR / RFQ / PO | resolve result, `price_version_id`, calculation snapshot/trace |
| F-VENDOR API-20 | read-only price-list summary façade; data owner remains this feature |
| Monitoring/Audit | pending SLA, anomaly and immutable price-change history |

## §0.6 Architecture

- UI: single-file prototype establishes behavior; implementation must preserve route/surface contracts in `01_UI.md`.
- HTTP: `/api/v1/vendor-price-lists...`; UI never calls an Engine directly.
- Logic: scope-local orchestration plus pure pricing engines in `03_LOGIC.md`.
- DB: PostgreSQL, RLS by tenant, four owned tables in `04_DB.md`.
- Auth: JWT/session role context; role and master state rechecked on every mutation.
- Integration: vendor/product are soft UUID references with display snapshots; no duplicate master ownership.

## §0.7 Multi-Tenant & Security Context

- Multi-tenant: **YES** — `tenant_id` + PostgreSQL RLS
- Company scoped: **YES** — `company_id` from authenticated context
- PII: **NO direct business PII**; user UUIDs are audit identifiers
- Financial data: **YES — Confidential**
- Audit: **YES — WORM business history + central mutation audit**
- Security preset: BRD P2 Approval/Workflow; applicable controls are access control, data masking, SoD, DOA, optimistic concurrency and immutable audit

### Data Classification Summary

- Price, discounts, freight, calculated landed cost, FX snapshot and change percentage: **Confidential**
- Identifiers, status and timestamps: **Internal**
- No field in this feature is Public or Restricted by default
- Unauthorized responses must omit/mask numeric pricing server-side; UI masking alone is insufficient

## §0.8 Open Questions / Implementation Owners

ไม่มีคำถามที่เปลี่ยน business behavior ก่อนเริ่ม implementation. รายการต่อไปนี้เป็น implementation detail ที่เจ้าของระบบต้อง pin ใน sprint planning:

| ID | Item | Blocking? | Owner |
|---|---|---:|---|
| OQ-01 | ชื่อ/ID global ของ Engine หลังลงทะเบียน CUBIC | NO | Architect |
| OQ-02 | Path ภายในที่ Vendor Master API-20 ใช้เรียก summary service | NO | Backend Lead |
| OQ-03 | ค่า page size, batch size, import file size และ idempotency TTL จาก platform config | NO | Platform Owner |
| OQ-04 | FX freshness window และ fallback policy; ห้าม fallback เงียบ | NO | Finance/Policy Owner |

> ไม่มี Security Spec Bible แยกไฟล์ใน workspace; FRD นี้ยึด Security & Compliance §16 ของ BRD v2.4 และ CUBE context เป็น baseline โดยไม่สร้าง control ใหม่

## §0.9 Glossary

| Term | Definition |
|---|---|
| Price Header | identity คงที่ของ vendor/product/UOM/currency ภายใต้ tenant/company/site |
| Price Version | ชุดราคาและ validity ที่แก้ไม่ได้หลัง Active |
| Landed unit cost ex-tax | `(price ÷ price_per) × (1 − discount_pct/100) + freight_per_unit` |
| Resolve | คืนราคา Active สำหรับ vendor ที่ระบุและตรง date/qty/scope |
| Compare | คำนวณหลาย vendor แล้วเรียง landed cost ที่ normalize เป็นสกุลเดียวกัน |
| SoD | ผู้อนุมัติต้องไม่ใช่ผู้ขอ/ผู้สร้างคำขอ |
| WORM | ประวัติ append-only แก้หรือลบย้อนหลังไม่ได้ |

## §0.10 Pack Navigation

| File | Primary audience | Purpose |
|---|---|---|
| `01_UI.md` | FE | routes, surfaces, actions, states, microcopy anchors |
| `02_API.md` | BE | HTTP contracts and cross-module contracts |
| `03_LOGIC.md` | BE/Architect | Functions, Engines, API trace |
| `04_DB.md` | DBA/BE | tables, fields, constraints, RLS, classification |
| `05_RULES.md` | BE/QA | rules, state machines, validation, edge cases, errors |
| `06_TESTS.md` | QA | acceptance, coverage, DoD, cross-module tests |
| `07_LOCKED_DECISIONS.md` | All | immutable locks, resolved drift, tradeoffs |
| `INDEX.md` | All | quick navigation and cross-reference |

## §0.12 Coverage Manifest

### Stories

| BRD Ref | Requirement | Pack coverage |
|---|---|---|
| S-01 | Single price creation | UI P-01/P-04 · API-03/05 · FN-03/05 · AC-02/03 |
| S-02 | Batch + CSV import | UI P-03/P-09 · API-09..12 · FN-08..11 · AC-08..11 |
| S-03 | Cross-vendor compare | UI P-07 · API-13 · ENG-02 · AC-12 |
| S-04 | Controlled price change | UI P-05/P-08 · API-06/07 · FN-06/07 · AC-04..07 |
| S-05 | Detail/history/masking | UI P-06 · API-02 · BR-VPL-13/17 · AC-13/14 |

### Rules

| BRD | Pack | BRD | Pack | BRD | Pack |
|---|---|---|---|---|---|
| R01 | BR-VPL-01 | R02 | BR-VPL-02 | R03 | BR-VPL-03 |
| R04 | BR-VPL-04 | R05 | BR-VPL-05 | R06 | BR-VPL-06 |
| R07 | BR-VPL-07 | R08 | BR-VPL-08 | R09 | BR-VPL-09 |
| R10 | BR-VPL-10 | R11 | BR-VPL-11 | R12 | BR-VPL-12 |
| R13 | BR-VPL-13 | R14 | BR-VPL-14 | R15 | BR-VPL-15 |
| R16 | BR-VPL-16 | R17 | BR-VPL-17 | R18 | BR-VPL-18 |
| R19 | BR-VPL-19 | R20 | BR-VPL-20 | R21 | BR-VPL-21 |

### Edges

| BRD | Pack | BRD | Pack | BRD | Pack | BRD | Pack |
|---|---|---|---|---|---|---|---|
| E01 | EC-01 | E02 | EC-02 | E03 | EC-03 | E04 | EC-04 |
| E05 | EC-05 | E06 | EC-06 | E07 | EC-07 | E08 | EC-08 |
| E09 | EC-09 | E10 | EC-10 | E11 | EC-11 | E12 | EC-12 |
| E13 | EC-13 | E14 | EC-14 | E15 | EC-15 | E16 | EC-16 |

**Coverage result:** Stories 5/5 · Rules 21/21 · Edges 16/16 · no dropped BRD requirement. S-04 AC1 drift is resolved by Scope Lock in `07_LOCKED_DECISIONS.md` LD-02.
