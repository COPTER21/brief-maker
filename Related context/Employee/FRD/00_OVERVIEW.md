# 00_OVERVIEW — F-EMP-001 Employee Master (ทะเบียนประวัติพนักงาน)

> **Audience:** All roles (PM, BA, FE, BE, QA, DBA)
> **Purpose:** Document Control + Scope + Roles + Dependencies + Open Questions

---

## §0.1 Document Control

| Field | Value |
|---|---|
| **Feature ID** | F-EMP-001 |
| **Feature Name** | Employee Master (ทะเบียนประวัติพนักงาน) |
| **Feature Code** | HR-EMP-001 |
| **Module** | Human Resources (HR) |
| **Variant** | FULL (9 files + INDEX) |
| **Status** | APPROVED |
| **FRD Version** | 1.0 (2026-06-04) |
| **Generator** | frd-generator-v5 (v5.1) |
| **Source Brief** | — (derived from prototype; no module-decomposer Brief) |
| **Source BRD** | BRD_Employee.md (BRD-HR-001, status: APPROVED, 2026-06-04) |
| **Author** | BA Team (2B-info) |
| **Reviewers** | Tech Lead (Bird), HR Manager, QA Lead, DPO |

---

## §0.2 Revision History

| Version | Date | Author | Changes |
|---|---|---|---|
| 1.0 | 2026-06-04 | BA Team | Initial FRD generation from BRD-HR-001 (FULL variant) |

---

## §0.3 Scope

### In Scope
- Employee Master CRUD (list / profile / create / edit / delete-with-guard)
- ข้อมูลครบ: ส่วนตัว, ที่อยู่ 2 ชุด, การศึกษา/ประสบการณ์ (repeatable), ครอบครัว, ฉุกเฉิน, รูป, portfolio, เอกสาร
- รหัสพนักงานอัตโนมัติ `EMP-NNNN` (running 4 หลัก)
- Thai address cascade (จังหวัด→อำเภอ→ตำบล) + zip auto-lock
- Employment + org assignment (อ้างอิง F-ORG-001)
- Lifecycle fields (สรรหา/onboard/ทดลองงาน/พ้นสภาพ) — store + Pre-DOA approval fields
- User linkage (1:1) display + ON DELETE RESTRICT guard
- CSV import/export (merge/replace, validate)
- Data Classification 4-level per field

### Out of Scope
- Workflow approval จริงของ lifecycle — reason: ผูก DOA Engine (F-PC-DOA-01) ใน Phase 3
- โมดูล Recruitment/Onboarding/Offboarding/Payroll เต็มรูปแบบ — reason: feature แยก
- การสร้าง/แก้ไข User account — reason: อยู่ที่ F-IAM-01 (รอบนี้แค่แสดง+ผูก)
- File storage จริง — reason: Dev ต่อ storage ตอน implement

### Out of Scope (from Phase 2.5 skipped probes)
- PR-5 (rate-limit fine-tuning) — flagged OQ-07

---

## §0.4 Roles & Responsibilities (COSO)

| Role | Person/Team | Responsibilities |
|---|---|---|
| **Maker** | HR Officer | สร้าง/แก้ไขประวัติพนักงาน, บันทึกการพ้นสภาพ |
| **Checker** | HR Manager | สอบทานข้อมูล + sensitive change + ผลทดลองงาน |
| **Approver** | Department Head / HR Director | อนุมัติจ้าง/พ้นสภาพ/ลบ (Dept Head); แก้เงินเดือน (HR Director) |
| **Evaluator** | Line Manager | ประเมินผลทดลองงาน |
| **Owner** | HR Department | ดูแล/ติดตามความครบถ้วนข้อมูล |
| **System Admin** | IT | ร่วมอนุมัติลบ master data + ผูก/ถอนบัญชี (ที่ F-IAM-01) |

> รายละเอียดต่อ workflow → ดู `01_UI.md §1.5 Journey` + `05_RULES.md §5.6 State Machine`

---

## §0.5 Dependencies

### Upstream (this feature depends on)
| Dependency | Type | Source |
|---|---|---|
| Organization Master (Branch/Division/Department/Position) | Data / LOOKUP | F-ORG-001 |
| User Management (T_user.employee_id) | Data / Constraint | F-IAM-01 |
| Document Numbering | Service | shared numbering (EMP-NNNN) |
| Address Master (geo) | Data | M_address (เตรียม dataset/API) |
| User Access (Policy Center) | Governance | F-IAM-02 |
| DOA Engine | Governance / Engine | F-PC-DOA-01 (Phase 3) |

### Downstream (features that depend on this)
| Consumer | What it uses |
|---|---|
| My Profile (planned) | T_employee + linked T_user |
| Recruitment/Onboarding/Offboarding (planned) | lifecycle fields |
| Payroll (planned) | T_employee + bank/salary fields |
| ENG candidates (thai-national-id-validator, address-cascade-resolver, pii-masking-engine) | shared across HR/CRM/Vendor features |

### External
| Service | Purpose |
|---|---|
| File Storage | รูปโปรไฟล์ + เอกสารแนบ |
| Audit Log Service | immutable before/after |

---

## §0.6 Stack & Architecture

| Layer | Technology |
|---|---|
| Frontend | React / Next.js / Tailwind (CUBE NATIVE CI) |
| API | Node.js / Strapi |
| Database | PostgreSQL (RLS multi-tenant) |
| Prototype | html-generator-v3 SPA (employee-management.html) |

---

## §0.7 Multi-Tenant & Security Context

- [x] Multi-tenant feature: **YES** (RLS via tenant_id)
- [x] PII data involved: **YES** (ดู 04_DB §4.2 + §4.6)
- [x] Financial data: **YES** (salary grade / bank account)
- [x] Audit log required: **YES** (immutable, sensitive emphasis)

**Security Bible domains applied:** D2 (Auth), D7 (PII), D-CLASS (Classification), Admin/SoD — see 05_RULES.md §5.7 · **Security Preset: P6 (HR/PII, 15 controls)** จาก BRD §16

### §0.7.1 Data Classification Summary ⭐ (v5.1)

Highest classification level ที่ feature นี้แตะ:
- [x] **Has Restricted fields** — `national_id`, `sso_no`, `tax_id`, `bank_account`, `bank_name`, `grade` (salary band) (ดู 04_DB §4.2)
- [x] Has Confidential fields — `birth_date`, `religion`, `marital_status`, `blood_type`, `military_status`, `height`, `weight`, addresses, dependents, emergency, `photo`
- [x] Internal (default) — ฟิลด์ที่เหลือ
- [ ] Public-facing data — (portfolio url = Public ได้ตามที่เจ้าของตั้ง)

**Linkage:** ฟิลด์ Restricted/Confidential ต้อง register ที่ Policy Center → Data Classification + Restricted Resources (ดู 04_DB §4.6.6) — ดู Open Questions OQ-04

---

## §0.8 Open Questions

| ID | Question | Blocking? | Owner |
|---|---|---|---|
| OQ-01 | DoA thresholds ของ lifecycle (จ้าง/เงินเดือน/พ้นสภาพ/ลบ) | NO (Phase 3) | HR Director + DOA owner |
| OQ-02 | national_id / birth_date เป็น required หรือไม่ | NO | HR Manager |
| OQ-03 | ระยะเก็บข้อมูล + RTBF (PDPA) | NO (Phase 2+) | DPO |
| OQ-04 | Restricted fields wire เข้า Restricted Resources registry แล้วหรือยัง | NO | Policy Center owner |
| OQ-05 | Address master ใช้ dataset เต็มหรือ external API | NO | Dev/Architect |
| OQ-06 | Recruitment/Onboarding/Offboarding modules timeline | NO | HR roadmap |
| OQ-07 | Rate-limit เฉพาะ CSV import/export endpoints | NO | Tech Lead |
