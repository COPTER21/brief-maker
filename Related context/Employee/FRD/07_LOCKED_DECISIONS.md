# 07_LOCKED_DECISIONS — F-EMP-001 Employee Master

> **Audience:** All roles
> **Purpose:** Locked design decisions (LD) + Convention deviations + Pre-DOA notes

---

## §7.1 Locked Decisions

| ID | Decision | Rationale | Source |
|---|---|---|---|
| LD-01 | Create/Edit = **full-page form** (ไม่ใช่ drawer) | ข้อมูลเยอะ 6 แท็บ + repeatable + upload เกินความจุ drawer | BRD §14.6 NON-STANDARD (stakeholder override, Q2 answered) |
| LD-02 | Profile = tabbed HRIS (7 tabs) | มาตรฐานสากล BambooHR/Workday/SuccessFactors | BRD §14.6 / web research |
| LD-03 | รหัส `EMP-NNNN` 4 หลัก zero-pad | อ่านง่าย, running ต่อ tenant | BRD R01 |
| LD-04 | 1 Employee : 1 User, ON DELETE RESTRICT | referential integrity people model | BRD R02/R03 (BR-IAM-07) |
| LD-05 | zip derive + locked จากตำบล | กันกรอกผิด | BRD R04 |
| LD-06 | Lifecycle = **store + Pre-DOA fields** รอบนี้ | DOA Engine ยังไม่ wire (Phase 3) | BRD §13 |
| LD-07 | org_snapshot ณ บันทึก | กันข้อมูลย้อนหลังเพี้ยนเมื่อ master เปลี่ยน | BRD R13 |
| LD-08 | Restricted: national_id/sso/tax/bank/grade/salary | PII/financial sensitive | BRD §6/§16 P6 |
| LD-09 | CI locked Navy/Primary/Teal, no override | CUBE NATIVE CI | BRD §14.6 |
| LD-10 | 5 Engines เป็น CUBIC candidate (shared) | reusable ข้าม HR/CRM/Vendor | Logic Matrix #6-7 |

## §7.2 Convention Deviations
| Item | Standard | This FRD | เหตุผล |
|---|---|---|---|
| Layout create/edit | create-drawer-wizard (B) | full-page-form ⭐ | LD-01 explicit override |
| (อื่น ๆ) | — | ตรงตาม conventions | — |

## §7.3 Engine ID Note
- Engine IDs (`thai-national-id-validator`, `address-cascade-resolver`, `supervisor-cycle-detector`, `pii-masking-engine`, `employee-status-machine`) = scope-local DRAFT (`F-EMP-ENG-01..05`)
- **Global ENG-NNN IDs to be assigned at CUBIC Registry registration** + register Smart Code (uba-taxonomy-register)

## §7.4 Governance / Pre-DOA Notes
- **Checkpoint 1 — User Access (F-IAM-02):** map Permission Matrix (BRD §4.2) → Policy Center User Roles Access
- **Checkpoint 2 — DOA (F-PC-DOA-01):** lifecycle approvals (probation/offboard/sensitive/delete) ใช้ Pre-DOA fields (`approver_role/approved_by/approval_chain` + TODO) → wire ใน Phase 3 (ห้าม hardcode rule ใน feature)
- Restricted fields → register Policy Center Restricted Resources (OQ-04)
