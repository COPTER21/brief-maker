# 00_OVERVIEW — F-HR-WELFARE · Welfare (สวัสดิการ)

> **Audience:** All roles (PM, BA, FE, BE, QA, DBA)
> **Purpose:** Document Control + Scope + Roles + Dependencies + Open Questions + Coverage Manifest

---

## §0.1 Document Control

| Field | Value |
|---|---|
| **Feature ID** | F-HR-WELFARE |
| **Feature Name** | Welfare — สวัสดิการ |
| **Feature Code** | F102 (Cube_Feature_List) |
| **Module** | HR (Human Resources) · platform CUBE 4.0 |
| **Variant** | **FULL** (9 files + INDEX) |
| **Status** | DRAFT (พร้อม review) |
| **FRD Version** | 1.0 (2026-09-08) |
| **Generator** | frd-generator-v6 (v6.1 · HTML-first · Pack Mode) |
| **Source Brief** | Pack Brief Feature/F-HR-WELFARE/0_DIRECTION (PREBRIEF · FUNCTION_CHECKLIST · STANDARD_BASELINE · HANDOFF) |
| **Source BRD** | outputs/F-HR-WELFARE/BRD_welfare.md (status: **APPROVED**, 2026-09-08) |
| **Source HTML** | outputs/F-HR-WELFARE/welfare.html (gate-passed: audit FAIL=0 · qc-ux BLOCK=0 · coverage R1 FN 24/24) |
| **Decision Log** | outputs/F-HR-WELFARE/_DECISION_LOG_OQ.md (OQ-WEL-01/02/03 + A-WEL-03 · delegated PM/BA) |
| **Author** | tadswan@2bsimple.com (BA) |
| **Reviewers** | Strike · พี่เบิร์ด · Tech Lead · QA Lead |

### Variant decision (fallback from BRD)
`Variant = FULL` — pages=4 (§14.6) · **states=8** (draft/submitted/pending_approval/approved/rejected/cancelled/revoked/**reversed** ≥4 ⇒ FULL) · **approval=YES** (DOA 2-step) · **money=YES** (มูลค่าเข้า 7C·EC + reversal offset). ⇒ FULL แม้เพียง state ≥4 หรือ approval+money ก็เข้า FULL แล้ว.

---

## §0.2 Revision History

| Version | Date | Author | Changes |
|---|---|---|---|
| 1.0 | 2026-09-08 | BA (tadswan) | Initial FRD Pack (HTML-first · Recognize & Validate จาก welfare.html) — encode OQ-WEL-01 reversal + OQ-WEL-03 exposure display + governance guards จาก PM/BA fix round |

---

## §0.3 Scope

### In Scope
1. ทะเบียนประเภทสวัสดิการ (benefit type) — สร้าง/แก้เป็นเวอร์ชัน/ปิดใช้ (soft archive) · กลุ่มมีสิทธิ์ · โควตา/วงเงิน/ปี · effective dating
2. ผู้ติดตาม (คู่สมรส/บุตร/บิดา/มารดา) — เก็บใน Welfare (A-WEL-04)
3. คำขอใช้สิทธิ์ (self/dependent) — เลือกประเภทที่มีสิทธิ์ ณ วันยื่น · จำนวน/มูลค่า · แนบหลักฐาน
4. ส่งอนุมัติผ่าน **DOA** (slot picker เลือกคน 2 ขั้น · ไม่ hardcode สาย)
5. อนุมัติ (one-step advance ต่อการกด 1 ครั้ง) → ขั้นสุดท้ายตัดคงเหลือ + บันทึกมูลค่าเข้า 7C·EC + ส่งสถานะจ่าย (hook)
6. ไม่อนุมัติ / ยกเลิก (ก่อนอนุมัติ) / ระงับเพราะพ้นสภาพ (revoke)
7. **กลับรายการ (reversal)** ของคำขอที่อนุมัติแล้ว — append-only (OQ-WEL-01)
8. คงเหลือรายคนต่อ type (live จาก ledger) + exposure ของคำขอที่ยังค้าง (OQ-WEL-03 · display-only)
9. สิทธิ์เปิด/ปิดตาม joiner/leaver signal (hook On/Offboard)
10. รายงานการใช้สิทธิ์ตามแผน/กลุ่ม/ช่วง + filter
11. RESTRICTED masking · audit append-only

### Out of Scope — Scope Lock R11 (5 not-supported · ตัดโดยมติ ไม่ใช่ตกหล่น)
- **NS-1** จ่ายเงินจริง/เบิก/หักผ่านเงินเดือน — reason: จ่ายที่ Expense Claim/Payroll (F065/F101) · Welfare = hook display-only (LK-2 · A-WEL-02)
- **NS-2** จัดการผู้ให้บริการ (รพ./ประกัน) — reason: NICE ไม่อยู่ scope รอบนี้ (cap.19)
- **NS-3** สวัสดิการยืดหยุ่น/แต้ม (flex credits) — reason: NICE (cap.20)
- **NS-4** สร้าง/แก้ค่านโยบาย HR กลาง (ปฏิทิน/กลุ่มบริษัท/effective policy) — reason: อ่านจาก HR Configuration #107 เท่านั้น (LK-3)
- **NS-5** ออกเอกสารเลขรัน/PDF ทางการ — reason: ไม่มีเอกสารที่คนถือ (ไม่ doccfg/pdfdoc) · request_no = internal display id

> **reversal (กลับรายการ) = IN SCOPE** (authorized addition OQ-WEL-01) — append-only correction, **ไม่ใช่** real payout (ไม่มี pay action; clawback = flag แจ้งปลายทาง) ⇒ ไม่ขัด NS-1.

### Out of Scope (from Phase 2.5 conservative defaults — see §0.8 OQ)
- Atomic guarantee ของ re-check เพดาน ณ อนุมัติ (concurrent) — spec ให้ optimistic-lock + backend atomic แต่รอ BA/Dev ยืนยัน (OQ-04) `[AI-DEFAULT]`
- Attachment ชนิด/ขนาด/virus-scan policy — ปัจจุบัน mock; รอ policy (deferred to impl)

---

## §0.4 Roles & Responsibilities (COSO)

| Role | Person/Team | Responsibilities |
|---|---|---|
| **Maker** | พนักงาน (ESS ภายหลัง) / HR ยื่นแทน | สร้างคำขอ / ส่งอนุมัติ |
| **Checker + Approver** | หัวหน้าสายงาน (ขั้น 1) → HR สวัสดิการ (ขั้น 2) | อนุมัติตาม DOA · SoD: Maker ≠ Approver |
| **Owner (master)** | HR Welfare Admin | ทะเบียนประเภทสวัสดิการ · ผู้ติดตาม · reversal · รายงาน |
| **System** | — | resolve eligibility/DOA · ตัดคงเหลือ · CSQ EC · NTF · leaver revoke |

> รายละเอียดต่อ workflow → ดู `01_UI.md §1.3 Journey` + `05_RULES.md §5.3 Permission Matrix`

---

## §0.5 Dependencies

### Upstream (this feature depends on) — soft ref / hook (read-only)
| Dependency | Type | Source |
|---|---|---|
| Employee Master | Data (soft ref snapshot ชื่อ/ตำแหน่ง/แผนก/กลุ่ม · combobox #102) | F011 |
| On/Offboard | Signal (joiner/leaver · employment-window/resolve) | F127 / F128 |
| HR Configuration (#107) | Config resolve (company_scope · ปีสิทธิ์) — read-only, ไม่ CRUD | #107 |
| DOA engine (Delegation of Authority) | Approval chain resolve (GET /doa/resolve · slot picker) | F-DLG-001 |

### Downstream (features that depend on this) — Value Stream R12
| Consumer | What it uses | Trigger |
|---|---|---|
| CSQ engine (7C·EC) | มูลค่าสวัสดิการ = เงินได้พนักงาน (event `welfare.granted` EC) · reversal → EC reverse | approve / reverse |
| Payroll (F065) | สถานะจ่าย (display-only) · clawback flag | approve / reverse |
| Expense (F101) | สิทธิ์สวัสดิการกำกับวงเงินเบิก (revalidate) | approve |
| Notification (F-NOTIFY) | 4 business events + `welfare_request_reversed` | state transition |

### External
| Service | Purpose |
|---|---|
| Payroll/Expense pay-status hook | อ่านสถานะจ่าย display-only — **[ASSUMED contract A-WEL-02 · FRD Phase B]** |

---

## §0.6 Stack & Architecture

| Layer | Technology |
|---|---|
| Frontend | vanilla JS single-file SPA (prototype) → React/Next + Tailwind (prod) · hash routing `#/welfare/*` |
| API | Node.js / Strapi (HTTP layer) |
| Database | PostgreSQL (RLS multi-tenant) |
| Engine layer | CUBIC Registry (DOA · CSQ · NOTIFY existing; welfare eligibility/balance = new DRAFT) |
| Auth | JWT + role-based (admin/manager/employee) |

---

## §0.7 Multi-Tenant & Security Context

- [x] Multi-tenant feature: **YES** (RLS per tenant/company_scope)
- [x] PII data involved: **YES** (บุคคล/ผู้ติดตาม — ดู 04_DB §4.2 + §4.6)
- [x] Financial data: **YES** (มูลค่าสวัสดิการ → 7C·EC)
- [x] Audit log required: **YES** (append-only · ทุก transition + reversal — LK-5)

**Security Bible domains applied:** D2 (Auth) · D5 (Financial) · D7 (PII) · D9 (Audit) · D15 (Admin actions) · D17 (Multi-tenant) — see 05_RULES §5.7. Preset **P6 · HR / PII Sensitive**.

### §0.7.1 Data Classification Summary
Highest level ที่ feature แตะ = **Restricted**:
- [x] Has Restricted fields — `value` (มูลค่าสวัสดิการ), ข้อมูลบุคคล/ผู้ติดตาม (ดู 04_DB §4.2)
- [x] Has Confidential fields — employee snapshot, benefit usage
- Internal — status/timestamps/audit

**Linkage:** Restricted/Confidential fields → register ที่ Policy Center → Data Classification + Restricted Resources (04_DB §4.6.6). **Enforce ที่ backend ไม่ใช่แค่ UI** (OQ-05).

---

## §0.8 Open Questions

> Carry-over จาก BRD §15 + Decision Log + Phase 2.5 probes. OQ-WEL-01/02/03 + A-WEL-03 = **ตัดสินแล้ว** (encode เป็น rule) แต่ยังมีข้อ "ยืนยันปลายทาง/atomic/backend" ที่ค้าง.

| ID | Question | Blocking? | Owner |
|---|---|---|---|
| **OQ-WEL-01** | reversal scope ปลายทาง (Payroll clawback contract) หลังตัดสินใน HTML แล้ว | NO (encode แล้ว · รอยืนยันปลายทาง) | PM/BA → FRD Phase B |
| **OQ-WEL-02** | recurring benefit (PVD %) แบ่ง F102 enroll vs F065 deduct | NO (ยืนยันมติเดิม) | Strike |
| **OQ-WEL-03** | exposure คำขอค้าง = display-only (ไม่ soft-reserve) | NO (encode แล้ว) | PM/BA |
| **OQ A-WEL-03 / CL-0013** | สาย DOA exec path — รหัสสายจริงที่ DOA กลาง (CL-0013 ผู้บริหาร แขวน 31 ส.ค.) | NO (default 2-step · no-limit · no exec) | พี่เบิร์ด |
| OQ-01 | BR-01 eligibility rules → Rule Management (Phase 3) | NO | Strike |
| OQ-02 | BR-11 reversal policy (เงื่อนไข/สิทธิ์กลับรายการ) → Rule Management | NO | audit/finance |
| OQ-03 | Payroll/Expense hook contract (A-WEL-02) | **YES** (contract รอ Phase B) | Strike |
| OQ-04 | atomic re-check เพดาน ณ อนุมัติ (concurrent) `[AI-DEFAULT]` = optimistic-lock + backend atomic | **YES** (กระทบเงิน) | Dev/BA |
| OQ-05 | backend permission enforcement (ไม่ใช่แค่ UI masking) `[AI-DEFAULT]` = guard ทุก mutation ที่ backend | **YES** (กระทบข้อมูล) | Dev/BA |
| OQ-06 | plan chip: F102 dec=[doa,csq] แต่ feature ประกาศ +ntf | NO | PM |
| A-WEL-01 | benefit master เป็นของ Welfare (ไม่ใช่ HR Config group) | NO (default: effective_date เอง) | Strike |
| A-WEL-02 | จ่ายผ่าน Payroll/Expense = hook display-only | NO (= OQ-03) | Strike |
| A-WEL-04 | ผู้ติดตามเก็บใน Welfare | NO (default: เก็บใน Welfare) | Strike |
| A-WEL-05 | open enrolment / life-event change window | NO (default: reason ของคำขอ · window อ้าง HR Config) | Strike |

> Resolved → move to 07_LOCKED_DECISIONS §7.1 as LD-NN.

---

## §0.9 Glossary

| Term | Definition |
|---|---|
| Benefit type | ประเภทสวัสดิการ (master, versioned) — โควตา/วงเงิน/ปี ต่อกลุ่มพนักงาน |
| Balance / คงเหลือ | โควตา − ยอดใช้ (คำขอ approved สะสม) ต่อคน·ต่อ type·ต่อปีสิทธิ์ — computed live, ไม่เก็บซ้ำ |
| Exposure | คำขอ pending อื่นบนสิทธิ์เดียวกัน (N ใบ · รวมมูลค่า) — display-only (OQ-WEL-03) |
| Reversal (กลับรายการ) | การแก้คำขอที่อนุมัติแล้วแบบ append-only — คืนสิทธิ์ + EC reverse + clawback flag |
| One-step advance | อนุมัติ 1 ครั้ง = เลื่อน 1 ขั้น (ไม่ collapse ทั้งสาย) — FIX-03 |
| CSQ EC | Employee Cost / เงินได้พนักงาน (7C) — ท่อเดียวที่ Welfare ยิง (LK-6) |
| DOA | Delegation of Authority (F-DLG-001) — สายอนุมัติ resolve ตอนส่ง แล้ว freeze |
| soft ref | อ้างอิงแบบ snapshot (ชื่อ) ไม่มี FK cascade (LD-4C-02 · LK-4) |

---

## §0.10 Pack Navigation

| File | Audience | Purpose |
|---|---|---|
| 00_OVERVIEW.md | All | meta + scope + roles + coverage manifest |
| 01_UI.md | FE dev | Layout Decision Log + Pages + Journey (route จริงจาก HTML) |
| 02_API.md | BE dev (HTTP) | API contracts + Cross-Module Contract |
| 03_LOGIC.md | BE dev (logic) | Functions + Engines + Trace |
| 04_DB.md | DBA / BE | Tables + Fields + Classification |
| 05_RULES.md | BE + QA | Business Rules + State Machine + Edge Cases + Errors |
| 06_TESTS.md | QA | Acceptance + DoD + Cross-Module cases |
| 07_LOCKED_DECISIONS.md | All | Scope Lock §7.0 + LDs |
| INDEX.md | All | Cross-reference quick nav |

---

## §0.11 Scope Lock (pointer)
> FULL variant → Scope Lock อยู่ที่ **07_LOCKED_DECISIONS §7.0** (LK-1..6, immutable). Ref: HANDOFF.md §3 + PREBRIEF §0 OB-1..7.

---

## §0.12 Coverage Manifest ⭐ (กัน requirement หล่น BRD→FRD)

### 24 FN (FUNCTION_CHECKLIST) → ที่อยู่ใน Pack
| FN | สรุป | อยู่ที่ใน Pack |
|---|---|---|
| FN-01 | สร้างประเภท + กลุ่ม/โควตา/effective | 01_UI D-01 · 02_API-02 · 03 FN-01/FN-03 · 05 BR-03 · 06 AT-01 |
| FN-02 | แก้ = เวอร์ชันใหม่ ไม่ทับ [STD] | 01_UI D-01 · 02_API-04 · 03 FN-02 · 05 BR-03 · 06 AT-02 |
| FN-03 | ปิดใช้ (soft archive) | 01_UI M-06 · 02_API-05 · 03 FN-04 · 05 BR-07 · 06 AT-03 |
| FN-04 | quota≤0 / ช่วง effective ทับ → บล็อก | 02_API-02/04 · 03 FN-03 · 05 VR-01/VR-02 · 06 AT-04 |
| FN-05 | เพิ่มผู้ติดตาม (rel/dob/eligible) | 01_UI D-05 · 02_API-06 · 03 FN-05 · 05 VR-06/VR-07 · 06 AT-05 |
| FN-06 | ผู้ติดตามเกิน/บุตรอายุเกิน → เตือน/บล็อก | 02_API-06 · 03 FN-05 · 05 VR-06/VR-07 · 06 AT-06 |
| FN-07 | สร้างคำขอ type มีสิทธิ์ ณ วันยื่น + self/dep + แนบไฟล์ | 01_UI D-03 · 02_API-09 · 03 FN-07/FN-08/ENG-WEL-01 · 05 BR-01 · 06 AT-07 |
| FN-08 | ส่งอนุมัติ DOA slot picker (ไม่ hardcode) | 01_UI M-01 · 02_API-11 · 03 FN-10 · 05 BR-04 · 06 AT-08 |
| FN-09 | ใช้บางส่วน — คงเหลือถูกต้อง | 02_API-16 · 03 FN-15/ENG-WEL-02 · 05 BR-02/BR-05 · 06 AT-09 |
| FN-10 | ขอเกินคงเหลือ → บล็อก + ยอด | 02_API-09 · 03 FN-08/ENG-WEL-02 · 05 VR-04 · 06 AT-10 |
| FN-11 | ยื่น type ไม่มีสิทธิ์ → บล็อก+เหตุ | 02_API-09 · 03 FN-09/ENG-WEL-01 · 05 VR-05/BR-01/BR-06 · 06 AT-11 |
| FN-12 | ดูสถานะ + สาย DOA ปัจจุบัน (อ่าน) | 01_UI D-04 tab รายละเอียด · 02_API-10 · 06 AT-12 |
| FN-13 | อนุมัติ → ตัดคงเหลือ + 7C EC + hook จ่าย | 01_UI M-02 · 02_API-12 · 03 FN-11/ENG-WEL-02 · 05 BR-05/BR-09 · 06 AT-13 |
| FN-14 | ไม่อนุมัติ → ไม่ตัด + เหตุ + NTF | 01_UI M-03 · 02_API-13 · 03 FN-12 · 05 VR-08 · 06 AT-14 |
| FN-15 | ยกเลิกก่อนอนุมัติ ไม่กระทบคงเหลือ | 01_UI M-05 · 02_API-14 · 03 FN-13 · 05 VR-10/BR-05 · 06 AT-15 |
| FN-16 | leaver → คำขอค้าง revoked · null≠ทำงาน | 02_API (signal) · 03 FN-18 · 05 BR-06 · 06 AT-16 |
| FN-17 | สถานะจ่าย = อ่าน Payroll/Expense display-only | 01_UI D-04 tab รายละเอียด · 02_API §2.X hook · 05 BR-10 · 06 AT-17 |
| FN-18 | joiner → สิทธิ์เปิดอัตโนมัติ [STD] | 02_API (signal) · 03 FN-18 · 05 BR-06 · 06 AT-18 |
| FN-19 | รายงานใช้สิทธิ์ + filter จริง | 01_UI P-04 · 02_API-17 · 03 FN-17 · 05 BR-08 · 06 AT-19 |
| FN-90 | ค้นหา/filter + empty state | 01_UI P-01..P-04 · 03 FN-17 · 06 AT-20 |
| FN-91 | ปิดใช้/ยกเลิกผ่าน confirm + soft archive | 01_UI M-05/M-06 · 05 BR-07 · 06 AT-03/AT-15 |
| FN-92 | field validate + กัน double-submit | 03 FN-03/FN-08 · 05 §5.4 · 06 AT-21 |
| FN-93 | audit append-only ทุก transition | 04 T_welfare_audit_log · 05 BR-07 · 06 AT-22 |
| FN-94 | RESTRICTED masking ตาม role | 03 FN-19 · 04 §4.6 · 05 §5.7 D-CLASS · 06 AT-23 |

### Governance / authorized additions (Decision Log)
| Ref | Requirement | อยู่ที่ใน Pack |
|---|---|---|
| OQ-WEL-01 | reversal append-only | 01_UI M-04 · 02_API-15 · 03 FN-14 · 05 BR-11 · 06 AT-24/XT-03 |
| OQ-WEL-03 | exposure display-only | 01_UI D-04 tab คงเหลือ · 02_API-16 · 03 FN-16 · 05 BR-12 · 06 AT-25 |
| FIX-02 | re-check eligibility+เพดาน ณ final approval | 03 FN-11 · 05 BR-02/BR-DOA · 06 AT-13/AT-26 |
| FIX-03 | one-step advance ต่อ 1 การกด | 03 FN-11 · 05 §5.2 · 06 AT-27 |

### BRD Stories / Rules / Edges
- **Stories US-01..US-17** → mapped ผ่าน FN rows ข้างบน + 06_TESTS §6.1 (AT-01..AT-25).
- **Rules BR-01..BR-12** → 05_RULES §5.1 (all present).
- **Edges §10.1 (☑ confirmed 6)** → 05_RULES §5.5 EC-list; **§10.2 (☐ AI probes)** → OQ §0.8 + EC `[AI-DEFAULT]`.

**สรุป:** FN 24/24 ✅ · Stories 17/17 ✅ · Rules 12/12 ✅ · Edges confirmed 6/6 ✅ · ไม่มี requirement ไร้ที่ลง → OQ ที่ค้าง = OQ-03/04/05 (blocking, ยกไป §0.8).
