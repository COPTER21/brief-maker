# 00_OVERVIEW — F-VENDOR ทะเบียนคู่ค้า

> **Audience:** PM, BA, FE, BE, QA, DBA, Security  
> **Purpose:** ขอบเขต แหล่งอ้างอิง การอนุมัติ และ Coverage Manifest ของ Vendor Master

---

## §0.1 Document Control

| Field | Value |
|---|---|
| **Feature ID** | F-VENDOR |
| **Feature Name** | Vendor Master / ทะเบียนคู่ค้า |
| **Feature Code** | VEN / F-VENDOR-MASTER-001 |
| **Module** | Purchase |
| **Variant** | FULL — มี 7 lifecycle states, KYC, multi-step approval, PII/financial data และ cross-module contracts |
| **Status** | IN-REVIEW |
| **FRD Version** | 1.1 (2026-07-31 · HTML↔FRD sync) |
| **Generator** | frd-generator-v6 |
| **Source BRD** | `Related context/vendor/Vendor/BRD_vendor_master.md` v1.1 — APPROVED โดยผู้ใช้ในบทสนทนา 2026-07-31 |
| **UI Source of Truth** | `outputs/F-VENDOR/vendor.html` — APPROVED โดยผู้ใช้ + sync revision 2026-07-31 |
| **Business/Dependency Source** | `CUBE_4.0_AI_CONTEXT_PACK.md` + ทุกไฟล์ใน `Central Plan/` |
| **Historical references** | ทุกไฟล์ใน `Related context/vendor/Vendor/` |
| **Author** | Codex + frd-generator-v6 |

### Source precedence

1. ข้อยืนยันผู้ใช้ในบทสนทนาและ Scope Lock
2. Central Plan สำหรับ dependency, Golden Rule และ cross-module contract
3. HTML ที่อนุมัติแล้วสำหรับ route, layout, action, state ที่มองเห็น และ microcopy
4. BRD v1.1 สำหรับ business intent
5. เอกสาร/HTML/ZIP เดิมเป็น historical reference เท่านั้น

เมื่อ BRD เดิมขัดกับ HTML ที่อนุมัติแล้ว ให้ใช้ HTML และบันทึกเหตุผลใน `07_LOCKED_DECISIONS.md`

## §0.2 Revision History

| Version | Date | Author | Changes |
|---|---|---|---|
| 1.0 | 2026-07-31 | Codex | Initial FULL FRD Pack จาก BRD v1.1 และ HTML ที่อนุมัติ |
| 1.1 | 2026-07-31 | Codex | Sync KYC non-sanctions result, Policy approval/fallback, unblock gates, bank-deactivate reason และ UI microcopy กับ HTML |

## §0.3 Feature Overview

F-VENDOR เป็น master data กลางสำหรับสร้าง ตรวจสอบ อนุมัติ และควบคุมสถานะคู่ค้า ตั้งแต่ร่างจนพร้อมใช้ในธุรกรรม ระบบเก็บข้อมูลนิติบุคคล ภาษี ที่อยู่ ผู้ติดต่อ บัญชีธนาคาร เอกสาร และประวัติการตัดสินใจ โดยแยกหน้าที่ Procurement, Compliance, Finance และ Approver ตาม SoD

คู่ค้าจะใช้กับธุรกรรมใหม่ได้เมื่อสถานะ `active` และ KYC ผ่าน ส่วนความพร้อมสำหรับ Payment ต้องมีบัญชีธนาคารที่ Finance ยืนยันแล้วสำหรับคู่ค้าที่ไม่ใช่ One-time การเลือกสายอนุมัติเป็นหน้าที่ Policy Center; Vendor ไม่มี threshold หรือ auto-approval ภายใน feature

### In Scope

- รายการคู่ค้า ค้นหา กรอง เรียง และแบ่งหน้า ที่ route `#/vendors`
- Create/Edit แบบ drawer wizard 3 ขั้น และบันทึกร่าง
- ประเภทคู่ค้า 11 ประเภท: RM, TR, SV, MN, CT, LG, SP, UT, GV, EM, OT
- ข้อมูลภาษี สถานประกอบการ ที่อยู่ ผู้ติดต่อ บัญชีธนาคาร เงื่อนไขชำระ วงเงินเครดิต และไฟล์แนบ
- KYC review, sanctions-hit control และการบันทึกแหล่งข้อมูล/เหตุผล
- สายอนุมัติจาก Policy Center, multi-step approval, reject/resubmit และ SoD
- Bank verification โดย Finance; verified account เป็น read-only และใช้การปิดใช้งานแทนการลบ
- Block, unblock, inactive และ blacklist พร้อม audit
- Masking ตาม role, tenant isolation, optimistic locking และ idempotency
- Read-only Vendor Price List summary และ transaction-eligibility contract ให้ PO/PV

### Out of Scope

- การตั้ง threshold/สายอนุมัติใน Vendor — เป็นความรับผิดชอบของ Policy Center
- การแก้ไข Price List — อยู่ใน F-VENDOR-PRICE-LIST
- การสร้าง PO/PV หรือการชำระเงินจริง
- การออกเอกสารธุรกรรม/จดหมาย PDF A4 — ไม่มีเอกสารชนิดนี้ใน feature จึงไม่ใช้ `thai-doc-pdf-generator`
- Bulk import/export, duplicate merge และ vendor self-service portal
- การ implement codebase — deliverable รอบนี้เป็นเอกสารสำหรับส่งต่อ AI Coding Agent

## §0.4 Roles & Responsibilities (COSO)

| Role | Responsibility |
|---|---|
| `procurement_officer` | สร้าง/แก้ไข บันทึกร่าง ส่ง KYC และส่งอนุมัติ |
| `procurement_manager` | ดูแลข้อมูลและอนุมัติตามขั้นที่ Policy Center คืนมา |
| `procurement_director` | อนุมัติขั้น Director และ blacklist |
| `compliance_officer` | ตรวจ KYC, sanctions และบันทึกผล |
| `finance_officer` | ดูข้อมูลการเงินเต็มรูปแบบ ส่งตรวจ/ยืนยัน/ปิดใช้บัญชีธนาคาร |
| `admin` | ทำ action ได้ทุกกลุ่มโดยยังต้องผ่าน state rule, SoD และ audit |
| `viewer` | อ่านข้อมูลที่ได้รับอนุญาต โดย Confidential/Restricted ถูก mask |

## §0.5 Dependencies

### Upstream

| Dependency | Type | Purpose |
|---|---|---|
| Policy Center | API | resolve approval chain และ runtime policy |
| Sanctions screening provider | External integration | ตรวจรายชื่อเฝ้าระวัง; provider จริงยังเป็น OQ-01 |
| F-PAYMENT-TERM | Master data | ค่าเงื่อนไขการชำระเงินเริ่มต้น |
| Auth/Tenant/Role service | Platform | JWT, tenant context, role และ SoD |
| Object storage + malware scan | Platform | จัดเก็บและตรวจไฟล์แนบ |
| Thai address reference | Reference data | จังหวัด อำเภอ ตำบล รหัสไปรษณีย์ |

### Downstream

| Consumer | Contract used |
|---|---|
| F-VENDOR-PRICE-LIST | `vendor_id`, `status`; ผูก Price List กับคู่ค้าและแสดง summary แบบ read-only |
| F-PO | `vendor_id`, `status`, `default_payment_term`; เลือกได้เฉพาะคู่ค้า `active` |
| Payment/PV | transaction eligibility + verified bank; non-OT ต้องมีบัญชียืนยันแล้ว |

## §0.6 Architecture Context

- UI: single-page HTML contract ที่ `#/vendors`; list เป็นหน้าหลัก ส่วน view/create/edit เป็น drawer และ action confirmation เป็น modal
- API: versioned REST `/api/v1`, multi-tenant, JWT/RBAC, idempotency สำหรับ mutation
- Logic: scope-local orchestration + reusable pure engines ตาม CUBIC 3-layer
- DB: PostgreSQL + RLS; master recordsใช้ soft archive/soft disable; audit append-only
- Integrations: Policy Center, sanctions provider, object storage และ downstream consumers
- Stack จริงยังไม่ถูกล็อก เพราะไม่มี codebase; contract นี้ไม่บังคับ framework

## §0.7 Multi-Tenant & Security

| Concern | Applies | Control |
|---|---|---|
| Multi-tenant | YES | `tenant_id`, PostgreSQL RLS, tenant from trusted token context |
| PII | YES | field-level classification, encryption, masking, view audit |
| Financial data | YES | bank account/credit limit access control and audit |
| Audit | YES | append-only/WORM 7 ปี; mutation ล้มเหลวถ้าเขียน audit ไม่สำเร็จ |
| SoD | YES | maker ห้ามอนุมัติรายการที่ตนสร้าง |

Highest classification = **Restricted** (`bank_account_number` และไฟล์หลักฐานที่ sensitive) รายละเอียดดู `04_DB.md §4.6`

### §0.7.1 Data Classification Summary

- Restricted: bank account number/name, private object key, sanctions evidence และ protected audit snapshots
- Confidential: tax/VAT/company identifiers, contacts, addresses, credit/payment terms และ approval/KYC identity
- Internal: IDs, lifecycle status, timestamps และ non-sensitive reference codes
- Public: ไม่มี field ใด default เป็น Public
- Restricted fields ต้องลงทะเบียนกับ Policy Center Data Classification/Restricted Resources ก่อน production; ดู OQ-06

## §0.8 Open Questions

| ID | Question | Blocking? | Owner / Default |
|---|---|---|---|
| OQ-01 | Production sanctions provider และ SLA/timeout เท่าใด | ก่อน production | Security/Compliance; timeout ต้องคงสถานะรอตรวจ `[AI-DEFAULT]` |
| OQ-02 | KYC มีอายุเท่าใดและใครเป็นผู้กำหนด expiry | ก่อน production | Compliance/Policy Center; ห้าม auto-expire จนมี policy |
| OQ-03 | F-VENDOR-PRICE-LIST จะใช้ endpoint summary นี้หรือเรียก service ของตนโดยตรง | ก่อน integration | Architect |
| OQ-04 | ชนิดไฟล์ ขนาดสูงสุด จำนวนไฟล์ และ retention ของ attachment | ก่อน implementation | Security/Product; server ต้อง allowlist และ scan |
| OQ-05 | Notification channel จริงเมื่อส่ง KYC/approval/reject | ไม่ block core API | Product/Platform |
| OQ-06 | ACL/Restricted Resources registry สำหรับ bank, sanctions evidence และ protected attachments ใช้ policy ชุดใด | ก่อน production | Security/Policy Center |

## §0.9 Glossary

| Term | Meaning |
|---|---|
| KYC | การตรวจยืนยันตัวตน/เอกสารและความเสี่ยงของคู่ค้า |
| Sanctions hit | พบข้อมูลตรงกับรายชื่อเฝ้าระวัง ต้องห้าม pass KYC และ block |
| DOA | Delegation of Authority; Policy Center เป็นผู้ resolve chain |
| SoD | Segregation of Duties; แยกผู้สร้าง ผู้ตรวจ และผู้อนุมัติ |
| One-time / OT | คู่ค้าครั้งเดียว; tax ID และ verified bank อาจไม่บังคับ แต่ยังต้องผ่าน KYC/approval policy |
| Soft-disable | ปิดใช้ record ย่อยโดยรักษาประวัติและ identifier |

## §0.10 Pack Navigation

| File | Primary audience | Purpose |
|---|---|---|
| `01_UI.md` | FE | route, drawer, modal, action และ UI state |
| `02_API.md` | BE | HTTP contracts |
| `03_LOGIC.md` | BE/Architect | functions, engines และ R8 trace |
| `04_DB.md` | DBA/BE/Security | schema, classification, indexes, retention |
| `05_RULES.md` | BE/QA | state, rule, permission, edge และ errors |
| `06_TESTS.md` | QA | acceptance, trace, cross-module tests |
| `07_LOCKED_DECISIONS.md` | All | scope lock และข้อยุติ |
| `INDEX.md` | All | entry point และ cross-reference |

## §0.11 Scope Lock Pointer

ดู `07_LOCKED_DECISIONS.md §7.0`

## §0.12 Coverage Manifest

### User Stories

| BRD Ref | Requirement | Pack coverage |
|---|---|---|
| US-01 | Procurement เปิดคู่ค้าใหม่ | UI-02, API-04, FN-03, AC-02 |
| US-02 | ส่งคู่ค้าเข้า KYC | UI-02, API-06, FN-06, AC-06 |
| US-03 | Compliance ตรวจ KYC | UI-04, API-07, FN-07, AC-07/08 |
| US-04 | ส่งอนุมัติผ่าน DOA | UI-03, API-08, FN-08, AC-09 |
| US-05 | อนุมัติทีละขั้น | UI-05, API-09, FN-09, AC-10 |
| US-06 | ตีกลับ | UI-05, API-09, FN-09, AC-11 |
| US-07 | Finance ยืนยันบัญชี | UI-03, API-14/15/16, FN-11/12, AC-12 |
| US-08 | Block/Unblock | UI-06, API-10/11, FN-10, AC-13 |
| US-09 | Blacklist terminal | UI-06, API-13, FN-10, AC-14 |
| US-10 | Role-based masking | UI-01/03, API read contracts, BR-VEN-18, AC-15 |
| US-11 | Price List summary read-only | UI-03, API-20, FN-16, XT-01 |

### BRD Rules

| BRD Ref | Requirement | Pack coverage |
|---|---|---|
| BR-V01 | TH tax ID format/checksum | BR-VEN-01, FN-05, AC-03 |
| BR-V02 | tax ID unique per country | BR-VEN-02, DB constraint, AC-03 |
| BR-V03 | OT tax ID optional | BR-VEN-03, AC-04 |
| BR-V04 | vendor code format | BR-VEN-04, FN-03, AC-02 |
| BR-V05 | vendor name required/length | BR-VEN-05, AC-02 |
| BR-V06 | bank number validation | BR-VEN-06, AC-12 |
| BR-V07 | non-OT verified bank gate | BR-VEN-07, AC-09/12 |
| BR-V08 | valid contact gate | BR-VEN-08, AC-09 |
| BR-V09 | credit limit non-negative | BR-VEN-09, AC-02 |
| BR-K01 | KYC pass before approval | BR-VEN-10, AC-09 |
| BR-K02 | sanctions hit blocks | BR-VEN-11, AC-08 |
| BR-K03 | tax ID immutable after KYC pass | BR-VEN-12, AC-16 |
| BR-K04 | Compliance-only KYC | BR-VEN-13, permission matrix, AC-07 |
| BR-K05 | KYC review scope | BR-VEN-14, FN-07, AC-07/08 |
| BR-A01 | approver differs from maker | BR-VEN-15, AC-10 |
| BR-A02 | role must match current chain | BR-VEN-16, AC-10 |
| BR-A03 | approval chain resolution | LD-02 supersedes threshold; BR-VEN-17, AC-09 |
| BR-A04 | OT approval behavior | LD-03 supersedes auto-approve; BR-VEN-17, AC-09 |
| BR-A05 | reject resets chain | BR-VEN-19, AC-11 |
| BR-M01 | tax ID Confidential | DB classification, BR-VEN-18, AC-15 |
| BR-M02 | bank account Restricted | DB classification, BR-VEN-18, AC-15 |
| BR-M03 | masking pattern | BR-VEN-18, AC-15 |
| BR-L01 | blacklist terminal | BR-VEN-20, AC-14 |
| BR-L02 | editable statuses | BR-VEN-21; `draft/pending_kyc/active`, AC-05/16 |
| BR-L03 | reason required | BR-VEN-22, AC-11/13/14 |
| BR-L04 | referenced vendor soft-only | BR-VEN-23, DB retention, AC-05/13/17 |

### Edge Cases

| BRD Ref | Requirement | Pack coverage |
|---|---|---|
| EC-01 | duplicate tax ID | EC-VEN-01, AC-03 |
| EC-02 | OT without tax ID | EC-VEN-02, AC-04 |
| EC-03 | approval before KYC pass | EC-VEN-03, AC-09 |
| EC-04 | approval without valid contact | EC-VEN-04, AC-09 |
| EC-05 | approval without verified bank | EC-VEN-05, AC-09 |
| EC-06 | maker self-approves | EC-VEN-06, AC-10 |
| EC-07 | wrong approval role | EC-VEN-07, AC-10 |
| EC-08 | sanctions hit | EC-VEN-08, AC-08 |
| EC-09 | edit tax after KYC pass | EC-VEN-09, AC-16 |
| EC-10 | reject after partial approval | EC-VEN-10, AC-11 |
| EC-11 | block referenced vendor | EC-VEN-11, AC-13 |
| EC-12 | reactivate blacklisted vendor | EC-VEN-12, AC-14 |
| EC-13 | deactivate last verified bank | EC-VEN-13, XT-03 |

**Coverage result:** Stories 11/11 · BRD rules 26/26 · BRD edges 13/13 · unresolved implementation inputs are OQ-01..OQ-06.
