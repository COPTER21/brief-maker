# 00_OVERVIEW — F-HR-ESS · ESS Portal (พนักงานทำเอง)

> **Audience:** All roles (PM, BA, FE, BE, QA, DBA)
> **Purpose:** Document Control + Scope + Roles + Dependencies + Open Questions + Coverage Manifest
> **Archetype:** `portal(aggregate)` — **display-only + deep-link** · ไม่มี CRUD/mutation/เอกสาร/เลขรัน/อนุมัติของตัวเอง (OQ-HR-04)

---

## §0.1 Document Control

| Field | Value |
|---|---|
| **Feature ID** | F-HR-ESS |
| **Feature Name** | ESS Portal — พนักงานทำเอง (Employee Self-Service) |
| **Feature Code** | F059 (Cube_Feature_List) |
| **Module** | HR (Human Resources) · platform CUBE 4.0 |
| **Variant** | **STANDARD** (7 files) |
| **Status** | DRAFT (พร้อม review) |
| **FRD Version** | 1.0 (2026-09-10) |
| **Generator** | frd-generator-v6 (v6.1 · HTML-first · Pack Mode · Recognize & Validate) |
| **Source Brief** | Pack Brief Feature/F-HR-ESS/0_DIRECTION (PREBRIEF · FUNCTION_CHECKLIST · STANDARD_BASELINE · HANDOFF) |
| **Source BRD** | outputs/F-HR-ESS/BRD_ess.md (status: **APPROVED**, 2026-09-10) |
| **Source HTML** | outputs/F-HR-ESS/ess.html (gate-passed: audit FAIL=0 · qc-ux BLOCK=0 · coverage FN 15/15 · PREFLIGHT v6.4 2026-09-10) |
| **Declarations (NOTE only)** | ntf = **need** (consume) · csq = **need** (SecC self-access) · doa = no · doccfg = no · pdfdoc = no |
| **Author** | tadswan@2bsimple.com (BA) |
| **Reviewers** | Strike · พี่เบิร์ด · Tech Lead · QA Lead |

### Variant decision (fallback from BRD)
`Variant = STANDARD` — pages = **7** (§14.7 Screen Inventory: 1 dashboard + 3 tab-list + action-picker + read drawers + 403 modal ⇒ > 2 ⇒ ไม่ LEAN) · states = **0** (ESS ไม่มี document lifecycle ของตัวเอง — §8 · < 4 ⇒ ไม่ FULL) · approval = **NO** (ESS ไม่มี approval step ในพอร์ทัล — COSO Approver = owner feature) · money-engine = **NO** (ไม่มีการคำนวณ/มูลค่า — read-only). ⇒ ไม่มี state machine / engine / mutation ⇒ **STANDARD**. Scope Lock → §0.11 (STANDARD convention; ไม่มีไฟล์ 07 แยก).

> **หมายเหตุความต่างจากพี่น้องในเลน:** F-HR-WELFARE = FULL เพราะมี state≥4 + approval + money. ESS ตรงข้าม — feature นี้นิยามด้วย "สิ่งที่ห้ามทำ" ไม่ใช่สิ่งที่ทำ → ไม่มี layer ที่ผลักขึ้น FULL. 03_LOGIC มี **read/aggregate/guard functions เท่านั้น · ไม่มี engine · ไม่มี mutation API** (R8 vacuously satisfied — ไม่มี mutation ให้ trace).

---

## §0.2 Revision History

| Version | Date | Author | Changes |
|---|---|---|---|
| 1.0 | 2026-09-10 | BA (tadswan) | Initial FRD Pack (HTML-first · Recognize & Validate จาก ess.html หลัง BA re-gate) — encode display-only/deep-link semantics, self-access SecC, RESTRICTED masking, consume-only NTF feed. Carry OQ-ESS-01 (CSQ event id) + OQ-ESS-02 (5 deep-link routes) เป็น [ASSUMED]/OQ ห้าม invent |

---

## §0.3 Scope

### In Scope (read + navigate-out only)
1. **หน้ารวมของฉัน (home dashboard)** — 5 การ์ดสรุป read จากหลาย surface: สลิปล่าสุด · โควตาลาคงเหลือ · OT เดือนนี้ · ใบเบิกค้าง · แจ้งเตือน + launcher "ยื่นคำขอ" + ทางลัด (FN-01)
2. **สลิปเงินเดือน** — ดูสลิป + ประวัติ + YTD (อ่าน Payroll PS-1 · self · **all-or-nothing** · RESTRICTED) (FN-02)
3. **วันลา / โควตาคงเหลือ** (read) + ปุ่ม "ยื่นลา" = deep-link ออก (FN-03)
4. **OT / เวลา / การสแกน** (read) + **ตารางกะของฉัน (read-only)** (FN-04)
5. **ใบเบิกค่าใช้จ่ายของฉัน** (read) + ปุ่ม "ยื่นเบิก" = deep-link ออก (FN-05)
6. **หนังสือรับรอง / เอกสาร** (read) + ปุ่ม "ขอหนังสือ" = deep-link ออก (FN-06)
7. **สวัสดิการ/คงเหลือ · อบรม/ใบรับรอง** (read) (FN-07)
8. **โปรไฟล์/ข้อมูลส่วนตัว** (read · RESTRICTED masking) + ปุ่ม "ขอแก้ข้อมูล" = deep-link ออก (FN-08)
9. **แจ้งเตือนของฉัน** — consume feed จาก ENG-NOTIFY (ESS ไม่ยิง event เอง) + ค้นหา/กรอง + empty (FN-09 · FN-90)
10. **self-access guard** — เห็นเฉพาะข้อมูลตัวเอง · คนอื่น = 403 (SecC) (FN-10 · FN-94)
11. **[ASSUMED contract] soft ref** — surface ของ feature ที่ยัง ba-done แสดง display-only + chip (FN-11)
12. **responsive** (พนักงานใช้มือถือ) (FN-92) · **audit อ่าน (append-only)** ประวัติการเข้าถึงข้อมูลของฉัน (FN-93)
13. **5 deep-link (navigate-out)** = ลา · OT · เบิก · แก้ข้อมูลส่วนตัว · หนังสือรับรอง — ยื่นคำขอทั้งหมดทำที่หน้า owner feature

### Out of Scope — Scope Lock R11 (ตัดโดยมติ ไม่ใช่ตกหล่น · = FUNCTION_CHECKLIST unsupported[])
- **NS-1** สร้าง/แก้/ลบ ข้อมูลของ feature อื่น (ลา/เบิก/OT/เงินเดือน/โปรไฟล์) — reason: ESS อ่านอย่างเดียว · ยื่น = ไปหน้าเจ้าของ (**OQ-HR-04** · LK-1)
- **NS-2** ทำฟอร์มยื่นลา/OT/เบิก เองในพอร์ทัล — reason: deep-link ไป owner feature (**A-ESS-02** · LK-2)
- **NS-3** ออกสลิป/หนังสือรับรอง/PDF เอง — reason: มาจาก feature ต้นทาง (soft ref) · ไม่มี pdfdoc
- **NS-4** Manager self-service / ทีมของฉัน / อนุมัติในพอร์ทัล — reason: NICE ไม่รองรับรอบนี้ (ESS = พนักงาน)
- **NS-5** config เมนู/สิทธิ์เอง — reason: Roles/Permission กลาง (#107)
- **NS-6** ออกเอกสาร/เลขรันเอง (ไม่มี doccfg) · อนุมัติ/สายอนุมัติ (ไม่มี doa) — reason: portal อ่านอย่างเดียว

### Out of Scope (from Phase 2.5 conservative defaults — see §0.8 OQ)
- Deep-link fallback เมื่อ route ปลายทางเปลี่ยน/ยังไม่พร้อม — spec ให้ graceful message ไม่ค้าง แต่รอ route จริง (**OQ-ESS-02** · `[AI-DEFAULT]`)
- surface ต้นทาง down/timeout → per-card degrade — spec `[AI-DEFAULT]`, รอ contract owner feature

---

## §0.4 Roles & Responsibilities (COSO)

| Role | Person/Team | Responsibilities |
|---|---|---|
| **Viewer (self)** | พนักงาน (สมชาย ใจดี · EMP-00123 = persona ตัวอย่าง) | เปิดดูข้อมูลของตัวเอง (read) · กด deep-link เพื่อเริ่มยื่นคำขอ |
| **System (ESS)** | — | serve read จาก surface ต้นทาง (self-scope) · enforce self-access guard (403) · mask RESTRICTED · consume NTF feed · append access-audit · route ออกไป owner feature |
| **Maker / Checker / Approver** | **owner feature (นอก ESS)** | ทุก mutation/approval ของคำขอเกิดที่หน้า owner feature หลัง deep-link — **SoD N/A ภายใน ESS** (ESS ไม่มี approval step) |

> **COSO/SoD note:** ESS ไม่สร้างธุรกรรมของตัวเอง (display-only). ในพอร์ทัลมีแค่ System (serve read) + Employee (viewer). SoD จึง N/A ภายใน ESS และไม่ถูกละเมิด. รายละเอียด journey → `01_UI.md §1.3`.

---

## §0.5 Dependencies

### Upstream (this feature reads from) — soft ref / hook (read-only · self-scope ทั้งหมด)
| Dependency | Type | Source | หมายเหตุ |
|---|---|---|---|
| Payroll — Payslip PS-1 | Data read (สลิป + YTD) | F-HR-PAYROLL §0.13.2 | self · **all-or-nothing** · RESTRICTED · PDF จากต้นทาง (LK-3) |
| การลา (Leave) | Data read (โควตา + ประวัติ) | owner feature | [ASSUMED] soft ref |
| OT / Attendance | Data read (OT + การสแกน) | owner feature | [ASSUMED] soft ref |
| ระบบกะ/บันทึกเวลา (Time · W2) | Data read (ตารางกะสัปดาห์นี้) | owner feature | [ASSUMED] · ESS ไม่แก้กะ |
| เบิกค่าใช้จ่าย (Expense) | Data read (ใบเบิก + สถานะ) | F101 | [ASSUMED] soft ref |
| หนังสือรับรอง (Cert) | Data read (เอกสารที่ออก) | owner feature | [ASSUMED] soft ref |
| สวัสดิการ / อบรม (Welfare/Training) | Data read (คงเหลือ + ประวัติ) | F102 / owner | [ASSUMED] soft ref |
| Employee Master (profile) | Data read (ข้อมูลส่วนตัว) | owner feature | RESTRICTED masking · แก้ = deep-link |
| **ENG-NOTIFY** (Notification Center) | **Consume** feed (my notifications) | F-NOTIFY | อ่านอย่างเดียว · **ESS ไม่ประกาศ/ยิง event** |
| **ENG-CSQ** (SecC) | self-access enforcement | ENG-CSQ · CSQ_BRIEF_F059 | ทุก read ผ่าน guard (**OQ-ESS-01**) |

### Downstream (features ESS hands off to via navigate) — Value Stream R12
| Consumer | What flows | Trigger | Route ([ASSUMED] · OQ-ESS-02) |
|---|---|---|---|
| การลา (Leave) | navigate ผู้ใช้ไปหน้ายื่นลา | กด "ยื่นลา" / action-picker "ขอลา" | `#/leave/new` |
| ขอ OT | navigate ไปหน้ายื่น OT | action-picker "ขอทำงานล่วงเวลา (OT)" | `#/ot/new` |
| เบิกค่าใช้จ่าย (Expense) | navigate ไปหน้ายื่นเบิก | กด "ยื่นเบิก" / action-picker | `#/expense/new` |
| แก้ข้อมูลพนักงาน (Profile) | navigate ไปหน้าขออนุมัติแก้ข้อมูล | กด "ขอแก้ข้อมูล" / action-picker | `#/profile/edit-request` |
| หนังสือรับรอง (Cert) | navigate ไปหน้าขอหนังสือ | กด "ขอหนังสือ" / action-picker | `#/cert/new` |

> **ไม่มี downstream เชิงบัญชี/สต๊อก/งบ** (ESS ไม่ผลิตธุรกรรม) · ไม่มี DOA/DOCCFG/PDFDOC. ESS ส่งต่อ **การนำทางผู้ใช้ (navigation)** เท่านั้น ไม่ส่ง payload ข้อมูล — owner feature อ่าน context ผู้ใช้เอง.

### External
| Service | Purpose |
|---|---|
| Owner-feature read surfaces | อ่าน view display-only — **[ASSUMED contract A-ESS-03 · resolve เมื่อ owner ba-done]** |

---

## §0.6 Stack & Architecture

| Layer | Technology |
|---|---|
| Frontend | vanilla JS single-file SPA (prototype) → React/Next + Tailwind (prod) · tab state ภายในพอร์ทัล (home/pay/docs/notify) · deep-link OUT = hash route ของ owner feature |
| API | Node.js / Strapi (HTTP layer) — **GET only** (aggregate read) |
| Database | ไม่มี table ของตัวเอง (aggregator) — อ่าน read-model/view ของ owner feature + append `T_ess_access_audit` (audit อ่าน) |
| Engine layer | ใช้ ENG-CSQ (SecC) + ENG-NOTIFY (consume) ที่มีอยู่แล้ว — **ไม่สร้าง engine ใหม่** |
| Auth | JWT + role-based · **self-scope enforced ที่ backend** (id ผ่าน param → 403) |

---

## §0.7 Multi-Tenant & Security Context

- [x] Multi-tenant feature: **YES** (RLS per tenant/company)
- [x] PII data involved: **YES** (nationalId, bank account, profile — RESTRICTED)
- [ ] Financial write: **NO** (อ่านสลิป/มูลค่า display-only — ไม่ลงบัญชี/ไม่จ่าย)
- [x] Audit log required: **YES** (access-audit append-only · ทุกการเปิดข้อมูล — LK-6 · FN-93)

**Security Bible domains applied:** D2 (Auth) · D7 (PII) · D9 (Audit) · D17 (Multi-tenant) · D-SelfAccess (SecC) — see 05_RULES §5.7. Preset **P6 · HR / PII Sensitive (15 controls)**. **ESS ไม่มี write path → ลด attack surface (display-only by design)**.

### §0.7.1 Data Classification Summary
Highest level ที่ feature แตะ (อ่าน) = **Restricted**:
- [x] Has Restricted fields (read-through) — `national_id`, `bank_account_no`, `payslip.*` (มูลค่าเงินเดือน) — masking ตาม self · all-or-nothing (payslip)
- [x] Has Confidential fields — employee profile (email/phone/แผนก), leave/expense/training records
- Internal — notification feed, access-audit timestamps

**Linkage:** Restricted fields เป็น **read-through จาก owner feature** — ESS ไม่เก็บสำเนา. Register ที่ Policy Center → Data Classification / Restricted Resources ทำที่ owner feature (ESS อ้างอิง). **Enforce self-scope + masking ที่ backend ไม่ใช่แค่ UI** (VR-2/VR-3 · OQ ด้าน enforcement ใน §0.8).

---

## §0.8 Open Questions

> Carry-over จาก BRD §15 + HANDOFF §4 + Phase 2.5 probes. **OQ-ESS-01 / OQ-ESS-02 = BA-opened · ยังไม่ตัดสิน** → flag [ASSUMED]/OQ ทั้ง pack **ห้าม invent**.

| ID | Question | Blocking? | Owner |
|---|---|---|---|
| **OQ-ESS-01** ⚠️ | **CSQ event id จริง ที่ ESS ยิงเข้า SecC pipe** — CSQ_BRIEF_F059 ประกาศ `ess.self_access` แต่ HTML anchor เป็น `ess.restricted_view` (เปิดดู RESTRICTED) + `ess.access_denied` (403). **ต้อง reconcile 1↔2 ชื่อ + ยืนยัน event id ปลายทาง SecC** ก่อน dev wire · ห้าม ESS ประกาศ OC/DC ซ้ำ | **YES** (กระทบ security wire) | PM/BA → ENG-CSQ owner · ดู 05_RULES §5.7 [ASSUMED] |
| **OQ-ESS-02** ⚠️ | **5 deep-link routes** (`#/leave/new` · `#/ot/new` · `#/expense/new` · `#/profile/edit-request` · `#/cert/new`) ยัง **[ASSUMED contract]** — ยืนยัน route จริงกับ owner feature ก่อน dev; เดาผิด = navigate ค้าง | **YES** (กระทบ navigation) | PM/BA → owner features · ดู 02_API §2.4 + 01_UI §1.4 |
| OQ-ESS-03 | Deep-link fallback เมื่อ route ปลายทางยังไม่พร้อม → graceful message (ไม่ค้าง) `[AI-DEFAULT]` = แสดง toast/notice + คงหน้าเดิม | NO (default ปลอดภัย) | Dev/BA |
| OQ-ESS-04 | surface ต้นทาง down/timeout → per-card degrade "โหลดไม่ได้" ไม่ล้มทั้งหน้า `[AI-DEFAULT]` = try/catch ต่อ surface | NO (default ปลอดภัย) | Dev/BA |
| OQ-ESS-05 | self enforcement ที่ **backend** (employee_id ผ่าน URL/param) → 401/403 ไม่ leak field `[AI-DEFAULT]` = server-side guard ทุก read | **YES** (กระทบข้อมูล PII) | Dev/BA |
| OQ-ESS-06 | re-auth ก่อนเปิด RESTRICTED (session หมดอายุกลาง drawer) `[AI-DEFAULT]` = optional (P6 ○Optional) | NO | Dev/BA |
| OQ-ESS-A1 | A-ESS-01 อ่านทุก surface display-only (OQ-HR-04) | **RESOLVED** (LK-1) | — |
| OQ-ESS-A3 | A-ESS-03 surface ba-done = [ASSUMED contract] soft ref | **RESOLVED** (LK-5 · resolve เมื่อ owner done) | — |

> Resolved → move to §0.11 Scope Lock (ถ้า immutable) หรือ note ใน 05_RULES.

---

## §0.9 Glossary

| Term | Definition |
|---|---|
| portal(aggregate) | archetype รวมมุมมองหลายโดเมนไว้จุดเดียว · **read-only view layer** · ไม่มี entity/lifecycle ของตัวเอง |
| deep-link (navigate-out) | ปุ่ม "ยื่น/ขอ" = พาผู้ใช้ไปหน้า owner feature (ที่ฟอร์ม/submit อยู่จริง) — ESS ไม่รับ/บันทึกคำขอเอง |
| self-access (SecC) | พนักงานเห็นเฉพาะข้อมูลของตัวเอง · เข้าถึงคนอื่น = 403 · enforce ที่ backend |
| all-or-nothing (payslip) | เห็นสลิปทั้งใบ หรือไม่เห็นเลย — ไม่มีการโชว์บางส่วน (LK-3) |
| RESTRICTED masking | ปิดบัง nationalId/bank ตาม self · reveal ได้เฉพาะเจ้าของ (ปุ่ม "แสดง/ซ่อน") |
| soft ref / [ASSUMED contract] | surface/route ที่ owner ยัง ba-done → display-only + chip · ยืนยัน contract ทีหลัง (LK-5) |
| consume feed (NTF) | ESS อ่าน feed แจ้งเตือนจาก ENG-NOTIFY · **ไม่ยิง event เอง** (ต่างจาก feature ที่ประกาศ event) |
| access-audit | บันทึกการเข้าถึงข้อมูลตัวเอง (append-only · แก้/ลบไม่ได้) — FN-93 |

---

## §0.10 Pack Navigation (STANDARD · 7 files)

| File | Audience | Purpose |
|---|---|---|
| 00_OVERVIEW.md | All | meta + scope + roles + **Scope Lock §0.11** + **Coverage Manifest §0.12** |
| 01_UI.md | FE dev | Layout Decision Log + Pages + Journey (tab state + deep-link routes จริงจาก HTML) |
| 02_API.md | BE dev (HTTP) | **GET-only** aggregate read contracts + Cross-Module (navigate/consume) |
| 03_LOGIC.md | BE dev (logic) | read/aggregate/guard Functions (no engine · no mutation) + Trace |
| 04_DB.md | DBA / BE | read-model view refs + `T_ess_access_audit` + Classification |
| 05_RULES.md | BE + QA | Business Rules + Validation + Edge Cases + Errors + §5.7 D-CLASS/Security |
| 06_TESTS.md | QA | Acceptance per FN + DoD + Cross-Module (deep-link/consume) cases |

---

## §0.11 Scope Lock ⭐ (R11 · immutable — inherited จาก BRD §3.4 + HANDOFF §3)

> **STANDARD variant → Scope Lock อยู่ที่นี่** (ไม่มีไฟล์ 07 แยก). LK-XX ห้าม override ตลอด chain · spec ใดขัด LOCK → LOCK ชนะ + รายงาน. scope ใหม่ที่เกิน LOCK → Open Question (drift ชั้นที่ 3).

| LOCK | เนื้อหา | อ้าง |
|---|---|---|
| **LK-1** | display-only ทุก surface · **ห้าม CRUD feature อื่น** | OQ-HR-04 · BR-01 |
| **LK-2** | ยื่นคำขอ = **navigate (deep-link)** ไปหน้า owner feature · ไม่ทำ form เอง | A-ESS-02 · BR-03 |
| **LK-3** | สลิปอ่านจาก Payroll PS-1 · **self เท่านั้น · all-or-nothing** | F-HR-PAYROLL §0.13.2 · BR-02 |
| **LK-4** | **self-access เท่านั้น** · เข้าถึงคนอื่น = 403 (SecC) | current-state §3 · BR-06 |
| **LK-5** | surface ba-done = **[ASSUMED contract] soft ref** | BR-07 |
| **LK-6** | **CSQ = SecC เท่านั้น** + NTF = **อ่าน feed** (ไม่นับ doa_*) · **ไม่มี doa/doccfg/pdfdoc** · audit อ่าน (append-only) | §12 · HANDOFF §3 |

**Compliance check:** ไม่มี spec ใน pack นี้ขัด LK-1..6 (verify Phase 3.5 §L). ทุก API เป็น GET (LK-1) · ทุกปุ่มยื่น = navigate (LK-2) · ไม่มี table mutation ของตัวเอง (LK-1/LK-6).

---

## §0.12 Coverage Manifest ⭐ (R13 · กัน requirement หล่น BRD→FRD)

### 15 FN (FUNCTION_CHECKLIST · FN-01..11 + FN-90/92/93/94) → ที่อยู่ใน Pack
| FN | สรุป | อยู่ที่ใน Pack |
|---|---|---|
| FN-01 | หน้ารวมของฉัน (5 การ์ดสรุป read + launcher) | 01_UI P-01 · 02_API-01 · 03 FN-01(buildDashboardSummary) · 05 BR-04 · 06 AT-01 |
| FN-02 | สลิป + ประวัติ + YTD (PS-1 · self · all-or-nothing) | 01_UI D-01 · 02_API-02 · 03 FN-02(readPayslipSelf) · 05 BR-02 · 06 AT-02 |
| FN-03 | วันลา/โควตา (read) + "ยื่นลา" navigate-out | 01_UI P-02 · 02_API-03 · 03 FN-03 + FN-08(resolveDeepLink) · 05 BR-03 · 06 AT-03 |
| FN-04 | OT/เวลา/สแกน + ตารางกะ (read-only) | 01_UI P-02 · 02_API-03 · 03 FN-03 · 05 BR-01 · 06 AT-04 |
| FN-05 | ใบเบิกของฉัน (read) + "ยื่นเบิก" navigate-out | 01_UI P-03 · 02_API-03 · 03 FN-03 + FN-08 · 05 BR-03 · 06 AT-05 |
| FN-06 | หนังสือรับรอง (read) + "ขอหนังสือ" navigate-out | 01_UI P-03 · 02_API-03 · 03 FN-03 + FN-08 · 05 BR-01/BR-03 · 06 AT-06 |
| FN-07 | สวัสดิการ/อบรม/ใบรับรอง (read) | 01_UI P-03 · 02_API-03 · 03 FN-03 · 05 BR-01 · 06 AT-07 |
| FN-08 | โปรไฟล์ (read · masked) + "ขอแก้ข้อมูล" navigate-out | 01_UI P-03 + D-02 · 02_API-06 · 03 FN-05(maskRestricted) + FN-08 · 05 BR-03/VR-2 · 06 AT-08 |
| FN-09 | แจ้งเตือนของฉัน (consume ENG-NOTIFY feed) | 01_UI P-04 · 02_API-05 · 03 FN-06(consumeNotifyFeed) · 05 BR-08 · 06 AT-09 |
| FN-10 | เข้าถึงคนอื่น → ปิดบัง + 403 (self-access SecC) | 01_UI M-02 · 02_API-* guard · 03 FN-04(enforceSelfScope) · 05 BR-06/VR-3 · 06 AT-10 |
| FN-11 | surface ba-done → display-only + [ASSUMED contract] chip | 01_UI §1.0 note · 02_API §2.4 · 05 BR-07 · 06 AT-11 |
| FN-90 | ค้นหา/กรอง notif + empty state | 01_UI P-04 · 03 FN-06 · 05 §5.4 · 06 AT-12 |
| FN-92 | responsive (มือถือ) | 01_UI §1.5 · 05 BR-05 · 06 AT-13 |
| FN-93 | audit การเข้าถึงข้อมูลตัวเอง (append-only) | 01_UI D-02 · 02_API-07 · 03 FN-07(appendAccessAudit) · 04 T_ess_access_audit · 05 BR-08 · 06 AT-14 |
| FN-94 | ปิดบัง/ไม่แสดงข้อมูลนอกขอบเขตตัวเอง | 01_UI M-02 + banner · 03 FN-04/FN-05 · 05 BR-06/§5.7 · 06 AT-15 |

### BRD Stories / Rules / Edges
- **Scenarios S-01..S-11** (PREBRIEF/BRD §5) → mapped ผ่าน FN rows ข้างบน + 06_TESTS §6.1.
- **Rules BR-01..BR-08** → 05_RULES §5.1 (all present).
- **Edges §10.1 (☑ confirmed 6)** → 05_RULES §5.5 EC-list; **§10.2 (☐ AI probes 5)** → OQ §0.8 + EC `[AI-DEFAULT]`.
- **Declarations (NOTE only, ไม่ generate ใน pack นี้):** ntf=need (consume) · csq=need (SecC) — บันทึกไว้ที่ §0.1 + 05_RULES §5.7; doa/doccfg/pdf=no.

**สรุป:** FN 15/15 ✅ · Scenarios 11/11 ✅ · Rules 8/8 ✅ · Edges confirmed 6/6 ✅ · ไม่มี requirement ไร้ที่ลง → OQ ที่ค้าง (blocking) = **OQ-ESS-01, OQ-ESS-02, OQ-ESS-05** (ยกไป §0.8).
