# 00_OVERVIEW — F-AGM-001 Farmer Member Management (จัดการสมาชิกเกษตรกร)

> **Audience:** All roles (PM, BA, FE, BE, QA, DBA)
> **Purpose:** Document Control + Scope + Roles + Dependencies + Scope Lock + Coverage Manifest

---

## §0.1 Document Control

| Field | Value |
|---|---|
| **Feature ID** | F-AGM-001 |
| **Feature Name** | Farmer Member Management (จัดการสมาชิกเกษตรกร) |
| **Feature Code** | AGM-FARMER-MEMBER |
| **Module** | AGM (Agriculture Management) / Farmer |
| **Client** | WKN (วังขนาย Sugar Group) |
| **Variant** | STANDARD (7 files) |
| **Status** | DRAFT (generated — รอ review) |
| **FRD Version** | 1.0 (2026-07-20) |
| **Generator** | frd-generator-v6 (Design Authority Edition) |
| **Source Brief** | — (WF-01 Refactor Wave — ไม่มี Brief; variant จาก handover + fallback ตรงกัน) |
| **Source BRD** | BRD_F-AGM-001_Farmer_Member.md (status: APPROVED, 2026-07-20) |
| **Constraint** | invariants.md LOCKED 🔒 (ผ่าน LOCK-01..08 ใน BRD §3.4) |
| **Legacy source** | farmer-management.zip (Next.js/v0 prototype — cross-check microcopy/testid/API names) |
| **Author** | 2BSimple BA (Strike) — generated via Cowork |
| **Reviewers** | Strike (BA), 2BSimple Dev/QA |

**Variant decision log:** STANDARD — handover LOCK ค่าไว้; fallback check จาก BRD ยืนยันตรงกัน (pages=2+5 overlays, states=4 [Pending/Approved/Rejected/Deleted], approval=Yes [R-02 verify], money=No → STANDARD)

---

## §0.2 Revision History

| Version | Date | Author | Changes |
|---|---|---|---|
| 1.0 | 2026-07-20 | frd-generator-v6 | Initial FRD Pack จาก BRD v1.0 APPROVED |
| 1.1 | 2026-07-22 | Refactor-Wave recheck | อัปเดตตาม authoritative spec: CSV address, email required, quota no_quota, NFR SER/VAL/CRE-UPT, CSV idempotency, FN 99–114 mapping |

---

## §0.3 Scope

### In Scope (ตาม BRD §3.1)
- ทะเบียนสมาชิกชาวไร่: สร้าง / แก้ไข / ลบ (soft) / ดูรายการ + รายละเอียด + ประวัติ
- ตรวจสอบยืนยัน (Verify) รายคนและทั้งกลุ่ม พร้อมเหตุผลบังคับเมื่อปฏิเสธ
- ส่งใหม่หลังถูกปฏิเสธ — Rejected → แก้ไข+บันทึก → กลับ Pending Approval อัตโนมัติ (LOCK-06)
- นำเข้า CSV จำนวนมาก + template download + error report (LOCK-04)
- แสดงสถานะโควตาของสมาชิก (read-only จาก module Quota)
- Governance: User Access ENC + DOA placeholder + Data Classification (LOCK-05)

### Out of Scope (ตาม BRD §3.2)
- สร้าง/จัดการโควตา — module Quota (feature ถัดไป)
- ผูกแปลงไร่ / สัญญาส่งอ้อย / การเงินชาวไร่
- Mobile app / self-service portal ของชาวไร่
- Notification ภายนอก (SMS/email)
- Data migration จากระบบเดิม

---

## §0.4 Roles & Responsibilities (COSO)

| Role | Person/Team | Responsibilities |
|---|---|---|
| **Maker** | R-01 เจ้าหน้าที่ทะเบียนชาวไร่ (Farmer Registrar) | สร้าง / แก้ไข / ลบ (Pending) / CSV import / แก้ไข-ส่งใหม่หลัง Rejected |
| **Checker** | R-02 หัวหน้างานทะเบียน (Registrar Supervisor) | Verify เดี่ยว/กลุ่ม (Approve/Reject + เหตุผล) เฉพาะ Pending |
| **Approver** | (DOA placeholder — รอ OQ-01) | approval chain จริงรอ WKN — Phase 4 wire DOA ENC |
| **Owner** | แผนกทะเบียนชาวไร่ WKN | Monitor dashboard + anomaly report |

> SoD: Maker (R-01) ≠ Checker (R-02) ต้องเป็นคนละบัญชี — self-verify block ดู 05_RULES EC-15 (รอ OQ-02, dev เตรียม logic หลัง flag)

---

## §0.5 Dependencies

### Upstream
| Dependency | Type | Source |
|---|---|---|
| M-01 Thai Address Hierarchy master | Data / Lookup API | CUBE core master (existing ✅) |
| Document Numbering config (prefix FM, %06d) | Config | CUBE Admin → System Config (existing ✅ — seed ค่า FM) |
| Central Import Framework | Engine | CUBE core (existing ⚠️ — เพิ่ม config ต่อ entity farmer_member) |
| User Access ENC | Policy | Policy Center — register matrix จาก BRD §4 |

### Downstream (BRD §12.1)
| Consumer | What it uses |
|---|---|
| Module Quota | member_id + verify_status (ผูก quota ได้เฉพาะ Approved) — ดู 02_API §2.X |
| สัญญาส่งอ้อย / ส่งเสริม | ข้อมูลติดต่อ + ที่อยู่ (lookup สด ไม่ snapshot) |
| การเงินชาวไร่ | citizen_id (ยืนยันตัวตนรับเงิน) — แก้หลัง Approved → Immutable Log + Anomaly Report |
| รายงานทะเบียนชาวไร่ | ทุก field (soft-deleted ไม่นับ active) |

### External
— ไม่มี (ไม่มี 3rd party integration ใน Phase 1)

---

## §0.6 Stack & Architecture

| Layer | Technology |
|---|---|
| Frontend | ตาม CUBE NATIVE standard (prototype = HTML SPA จาก html-generator-v6) |
| API | CUBE platform API layer |
| Database | PostgreSQL + RLS (multi-tenant: 1 tenant = 1 โรงงาน) |
| Engine layer | CUBIC Registry (reuse: import framework, address master) |
| Auth | CUBE platform JWT + ENC role-based |

---

## §0.7 Multi-Tenant & Security Context

- [x] Multi-tenant feature: YES (1 tenant = 1 โรงงาน, RLS)
- [x] PII data involved: YES (citizen_id, phone, email, address — ดู 04_DB §4.2/§4.6)
- [ ] Financial data: NO (แต่ citizen_id เป็น input การจ่ายเงิน downstream)
- [x] Audit log required: YES — Immutable Master Data Log (S01-07) ทุก mutation

**Security Preset:** P3 Master Data (10 controls — BRD §16.3) → mapping ใน 05_RULES §5.7

### §0.7.1 Data Classification Summary

Highest classification ที่ feature นี้แตะ: **Restricted** (citizen_id)
- [x] Has Restricted fields: `citizen_id` (mask บน list — S02-04)
- [x] Has Confidential fields: `phone`, `email`, `address_line`
- [x] Internal: ชื่อ-นามสกุล, สถานะ, audit fields

**Linkage:** `citizen_id` ต้อง register ที่ Policy Center → Restricted Resources (ดู OQ-F02)

---

## §0.8 Open Questions

| ID | Question | Blocking? | Owner |
|---|---|---|---|
| OQ-01 | DOA approval chain จริงของการ verify (WKN กี่ระดับ) — Phase 4 wire | NO (placeholder ไปก่อน) | WKN + Policy team |
| OQ-02 | บังคับ SoD "ผู้สร้างห้าม verify ตัวเอง" (EC-15) — เปิดเลยหรือรอ confirm | NO (dev เตรียม logic หลัง feature flag) | Strike/WKN |
| OQ-03 | ตำแหน่ง VC ใน VS Bible AGM (ยังไม่มี Bible) | NO | BA |
| OQ-F01 | Retention period ของ farmer_member_history (เสนอ default 10 ปี ตาม master data) | NO | WKN Compliance |
| OQ-F02 | Wire `citizen_id` เข้า Restricted Resources registry ที่ Policy Center — ทำตอน ENC register | NO | Policy team |

---

## §0.9 Glossary

| Term | Definition |
|---|---|
| AGM | Agriculture Management — ระบบบริหารจัดการไร่อ้อย |
| Verify | การตรวจสอบยืนยันสมาชิกโดยหัวหน้างาน (Approve/Reject) |
| Re-submit | Rejected → แก้ไข+บันทึก → กลับ Pending Approval อัตโนมัติ (LOCK-06) |
| Soft delete | ซ่อนจากระบบแต่คงใน DB (`is_deleted` flag) |
| SoD | Segregation of Duties — ผู้สร้างห้ามตรวจสอบรายการตัวเอง |
| Partial success | CSV import แถวดีถูกสร้าง แถวเสียรายงาน — ไม่ล้มทั้งไฟล์ |
| Optimistic lock | กันแก้ทับกันด้วย `expected_updated_at` |

---

## §0.10 Pack Navigation

| File | Audience | Purpose |
|---|---|---|
| 00_OVERVIEW.md | All | Meta + scope + Scope Lock + Coverage Manifest |
| 01_UI.md | FE dev + html-generator-v6 | Layout Decision Log + Pages + Journey |
| 02_API.md | BE dev (HTTP) | API contracts + legacy name mapping + Cross-Module Contract |
| 03_LOGIC.md | BE dev (logic) | Functions + Engines + Trace |
| 04_DB.md | DBA / BE | Tables + Field Dictionary + Classification |
| 05_RULES.md | BE + QA | Business Rules + State Machine + Edge Cases + Errors |
| 06_TESTS.md | QA + ai-testcase-md-generator | Acceptance + XT cross-module + DoD |

---

## §0.11 Scope Lock (STANDARD variant) ⭐

> Scope Lock Ref: `invariants.md` LOCKED 🔒 (Refactor Wave — invariants ทำหน้าที่ scope constraint แทนใบเซ็น)
> **Immutable ตลอด pack — spec ใดขัด LOCK → LOCK ชนะ**

| LOCK-ID | ข้อความยืนยัน | อ้าง | สถานะใน pack |
|---|---|---|---|
| LOCK-01 | ขอบเขต regen = ความสามารถ legacy 100% ห้ามตัด | invariants §1–§6 | ✅ ทุก capability legacy มีใน Coverage Manifest — layout เปลี่ยนเป็น standard ได้ (capability preserved) |
| LOCK-02 | State machine: Pending Approval → Approved / Rejected + soft delete | invariants §4 | ✅ 05_RULES §5.2 |
| LOCK-03 | Optimistic lock (expected_updated_at) + idempotency key `{FN}:{id}:{user}` ทุก mutation | invariants BR-05/06 | ✅ 02_API §2.3 + ทุก mutation contract |
| LOCK-04 | CSV contract 10 คอลัมน์ + partial success + error report download | invariants BR-07 | ✅ 02_API API-08 + 05_RULES BR-AGM-07/08 |
| LOCK-05 | เพิ่ม governance (ENC + DOA placeholder) ได้ ไม่ถือว่า scope drift | CUBE 4.0 standard | ✅ 04_DB approver placeholder + 05_RULES §5.3/§5.7 |
| LOCK-06 | Rejected → แก้ไข+บันทึก → กลับ Pending อัตโนมัติ (verified_note เดิมย้ายเข้า history) | Strike Q-01 | ✅ 03_LOGIC FN-02 + 05_RULES §5.2 |
| LOCK-07 | Approved แก้ได้ทุก field สถานะคงเดิม — Immutable Log + Anomaly Report | Strike Q-02 | ✅ 03_LOGIC FN-02 + 05_RULES BR-AGM-12 |
| LOCK-08 | email = optional ⚠️ **superseded** (authoritative) → email = REQUIRED | Strike Q-03 | ⚠️ 04_DB §4.2 (NOT NULL) + 05_RULES VR-03/04 — ดู note ใต้ตาราง |

**Drift check:** ไม่พบ scope ใหม่เกิน LOCK ระหว่างเขียน FRD — governance additions ทั้งหมดอยู่ใต้ LOCK-05

> ⚠️ **Recheck reconciliation (2026-07-22 — vs authoritative FRD FN-AT/SEQ-AGM 99–114):**
> - **LOCK-08 superseded:** email = **REQUIRED** (authoritative FRD + as-built create form) — LOCK-08 "optional" ถูกแทนที่ทั้ง pack (04_DB, 05_RULES, testcases). blank → "กรุณากรอกอีเมล".
> - **LOCK-06/07 additive:** re-submit ผ่าน edit (rejected→pending อัตโนมัติ / approved แก้ได้คงสถานะ) เป็นพฤติกรรม **เกิน authoritative FRD** ซึ่งระบุ verify_status เปลี่ยน **ผ่าน Verify Modal (single/bulk) เท่านั้น** — **คงไว้** (ภายใต้ LOCK-06/07) แต่ **ต้องขอ owner sign-off** ก่อนถือเป็น final scope.
> - **LOCK-05 governance additive:** citizen_id masking บน list, History timeline (API-10), ENC/SoD, Anomaly Report, DOA placeholder เป็นส่วนเสริม **เกิน authoritative FRD** (richer, ไม่ใช่ capability หาย) — **คงไว้** ภายใต้ LOCK-05 แต่ **ต้องขอ owner sign-off** ก่อนถือเป็น final scope.

---

## §0.12 Coverage Manifest ⭐ (กัน requirement หล่น BRD→FRD)

### Stories (BRD §7)
| BRD Ref | Requirement (ย่อ) | อยู่ที่ใน Pack |
|---|---|---|
| §7 US-01 | สร้างสมาชิกใหม่ | 01_UI OV-01 · 02_API API-02 · 03_LOGIC FN-01/FN-03 · 06 AC-01/AC-02 |
| §7 US-02 | นำเข้า CSV | 01_UI OV-03 · 02_API API-08/09 · 03_LOGIC FN-08 · 06 AC-08..AC-11 |
| §7 US-03 | ค้นหาสมาชิก | 01_UI P-01 · 02_API API-01 · 03_LOGIC FN-04 · 06 AC-12/AC-13 |
| §7 US-04 | Verify รายคน | 01_UI OV-04 · 02_API API-05 · 03_LOGIC FN-05 · 06 AC-14..AC-16 |
| §7 US-05 | Verify ทั้งกลุ่ม | 01_UI OV-04 (bulk) · 02_API API-06 · 03_LOGIC FN-06 · 06 AC-17/AC-18 |
| §7 US-06 | แก้ Rejected ส่งใหม่ / แก้ Approved | 01_UI OV-02 · 02_API API-04 · 03_LOGIC FN-02 · 06 AC-19/AC-20 |
| §7 US-07 | ลบสมาชิก Pending | 01_UI OV-05 · 02_API API-07 · 03_LOGIC FN-07 · 06 AC-21/AC-22 |
| §7 US-08 | ดูรายละเอียด + ประวัติ | 01_UI P-02 · 02_API API-03/API-10 · 06 AC-23/AC-24 |

### Rules (BRD §9)
| BRD Ref | Rule (ย่อ) | อยู่ที่ใน Pack |
|---|---|---|
| §9 R01 | Member ID `FM-%06d` (CONFIGURABLE) | 05_RULES BR-AGM-01 · 03_LOGIC FN-01 · 06 AC-02 |
| §9 R02 | เริ่ม Pending เสมอ | 05_RULES BR-AGM-02/§5.2 · 06 AC-02/AC-09 |
| §9 R03 | Verify เฉพาะ Pending | 05_RULES BR-AGM-03 · 06 AC-16 |
| §9 R04 | Reject ต้องมีเหตุผล | 05_RULES BR-AGM-04/VR-07 · 06 AC-15 |
| §9 R05 | ลบเฉพาะ Pending + soft only | 05_RULES BR-AGM-05 · 06 AC-21/AC-22 |
| §9 R06 | Optimistic lock + idempotency | 02_API §2.3 · 05_RULES BR-AGM-06 · 06 AC-25/AC-26 |
| §9 R07 | CSV .csv ≤5MB header 10 คอลัมน์ (CONFIGURABLE) | 05_RULES BR-AGM-07 · 06 AC-10 |
| §9 R08 | CSV partial success + error report | 05_RULES BR-AGM-08 · 06 AC-08/AC-11 |
| §9 R09 | postal_code auto + server validate | 05_RULES BR-AGM-09/VR-09 · 06 AC-05 |
| §9 R10 | citizen_id unique ต่อ tenant | 05_RULES BR-AGM-10/VR-05 · 06 AC-06/AC-07 |
| §9 R11 | Re-submit อัตโนมัติ (LOCK-06) | 05_RULES BR-AGM-11 · 03_LOGIC FN-02 · 06 AC-19 |
| §9 R12 | Approved แก้ได้ + Immutable Log (LOCK-07) | 05_RULES BR-AGM-12 · 06 AC-20 · XT-02 |
| §9 R13 | quota_status read-only | 05_RULES BR-AGM-13 · 06 XT-03 |
| §9 R14 | DOA placeholder (WARNING) | 04_DB §4.2 placeholder fields · 05_RULES BR-AGM-14 · OQ-01 |
| §9 VR-01..11 | Validation ทั้งชุด | 05_RULES §5.4 (map 1:1) · 06 AC-03..AC-07 |

### Edge Cases (BRD §10)
| BRD Ref | Edge (ย่อ) | อยู่ที่ใน Pack |
|---|---|---|
| §10 EC-01 ☑ | Verify/Edit ชนกัน | 05_RULES EC-01 · 06 AC-25 |
| §10 EC-02 ☑ | ลบรายการยืนยันแล้ว | 05_RULES EC-02 · 06 AC-22 |
| §10 EC-03 ☑ | Reject ไม่ใส่เหตุผล | 05_RULES EC-03 · 06 AC-15 |
| §10 EC-04 ☑ | CSV บางแถวพัง | 05_RULES EC-04 · 06 AC-08 |
| §10 EC-05 ☑ | ค้นหาไม่เจอ | 05_RULES EC-05 · 06 AC-13 |
| §10 EC-06 ☑ | เลือกทั้งหมด = เฉพาะ Pending | 05_RULES EC-06 · 06 AC-17 |
| §10 EC-07 ☑ | citizen_id ซ้ำ (form+CSV) | 05_RULES EC-07 · 06 AC-06/AC-07 |
| §10 EC-08 ☑ | เปลี่ยนจังหวัด reset ลูกโซ่ | 05_RULES EC-08 · 06 AC-04 |
| §10 EC-09..16 ☐ | Recommended (BA confirm SOW3.7) | 05_RULES §5.5.2 · 06 §6.11 recommended cases |

**สรุป:** Stories 8/8 ✅ · Rules 14/14 + VR 11/11 ✅ · Edges confirmed 8/8 ✅ + recommended 8/8 (marked) · ไม่มีที่ลง → ไม่มี (OQ ใหม่: OQ-F01, OQ-F02 เป็น governance detail ไม่ใช่ requirement หล่น)
