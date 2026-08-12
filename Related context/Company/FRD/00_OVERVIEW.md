# 00_OVERVIEW — F-ORG-001 Organization Management

| Field | Value |
|---|---|
| FRD ID | FRD-F-ORG-001 |
| Feature | Organization Management (บริษัท/สาขา/สายงาน/แผนก/ตำแหน่ง) |
| Sub-features | F-COMPANY-001, F-BRANCH-001, F-DIVISION-001, F-DEPT-001, F-POS-TIER-001 |
| Source BRD | BRD-ORG-001 (status APPROVED, **v1.1**) |
| Pack Variant | **FULL** (9 files + INDEX) |
| Module | Organization (Domain: Core Cube) |
| ERP/General | ERP (Shell: sidebar 232px + shell-bar 52px) |
| Version | 1.1 | Date | 2026-06-05 (sync company logo จาก BRD v1.1) |

## §0.1 Variant Rationale
FULL — has-entity=Yes (5 tables), has-state=Yes (active/inactive + Pre-DOA), **multi-engine 3** (org-tree-builder, csv-import-validator, cascade-resolver) → trigger FULL ตาม Decision Rule.

## §0.2 Scope
**In:** CRUD 5 entity, landing detail/record, org chart (dept 3-ชั้น + position reporting), CSV export ทุก entity + import (Replace/Merge+validate) สำหรับ division/department/position, toggle active, delete+cascade.
**Out:** DOA enforcement จริง (Pre-DOA only), IAM permission runtime, Employee Master, multi-legal-entity, approval workflow ของ master (Phase 2).

## §0.3 Roles
Org Admin (Maker) · Senior Admin (Checker/Delete) · Admin Manager (Approver-Pre-DOA) · All Users (read). Runtime ผูก IAM Role (F-IAM-02).

## §0.4 Dependencies
- Downstream: F-PC-DOA-01 (DOA), F-IAM-02 (Role), Report Framework, P2P (branch/dept/cost_center)
- Reuse: Document Numbering (R11), Policy Center (Data Classification)

## §0.7 Multi-Tenant & Security Context
- Multi-tenant: YES (PostgreSQL RLS by tenant_id)
- PII data: YES (head/deputy/manager/contact names, email, phone)
- Financial data: YES (position salary band)
- Audit log required: YES (S01-07 Immutable Master Data Log)
- Security Bible domains: Master Data (P3), Admin, PII → see 05_RULES §Security

### §0.7.1 Data Classification Summary ⭐
Highest level ที่ feature แตะ:
- ☑ **Has Restricted fields** — `position.salary_min`, `position.salary_max`
- ☑ Has Confidential fields — tax_id, reg_no, head/deputy/manager/contact names, email, phone
- ☑ Internal (default) — โครงสร้างองค์กรทั้งหมด, status, audit
- ☑ Public-facing — company name_th/name_en, website
**Linkage:** Restricted fields ต้อง register Policy Center → Restricted Resources (ดู 04_DB §4.6.6) — *ดู Open Questions OQ-1*

## §0.8 Open Questions
| ID | คำถาม | Source |
|---|---|---|
| OQ-1 | position.salary_min/max = Restricted → wire กับ Restricted Resources registry หรือยัง? | R10 |
| OQ-2 | precedence ตำแหน่งที่ผูกทั้ง dept+division (BRD Q1) | BRD §15 |
| OQ-3 | branch code gen ใช้ server sequence แทน length (BRD Q2) | BRD §15 |
| OQ-4 | salary_min>max = error/warning (BRD Q3) | BRD §15 |
| OQ-5 | optimistic lock สำหรับ concurrent edit (BRD Q4) | BRD §15 |
| OQ-6 | DOA enforce ตั้งแต่ Phase 1 หรือ Pre-DOA (BRD Q5) | BRD §15 |
