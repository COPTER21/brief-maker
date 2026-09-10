# 00_OVERVIEW — F-HR-EXPENSE · Expense Claim (เบิกค่าใช้จ่าย)

> **Audience:** All roles (PM, BA, FE, BE, QA, DBA)
> **Purpose:** Document Control + Scope + Roles + Dependencies + Open Questions + Coverage Manifest

---

## §0.1 Document Control

| Field | Value |
|---|---|
| **Feature ID** | F-HR-EXPENSE |
| **Feature Name** | Expense Claim / เบิกค่าใช้จ่าย (ใบเบิกค่าใช้จ่ายพนักงาน) |
| **Feature Code** | F101 |
| **Module** | Human Capital → Expense & Reimbursement |
| **Archetype** | **Q-document** (เอกสารธุรกรรมมีเลขรัน EXP-YYYY-NNNN + PDF + line editor B2 v2 · Iron Rules #98–101) |
| **Variant** | **FULL** (9 files + INDEX) |
| **Status** | DRAFT (for BA/SEC review) |
| **FRD Version** | 1.0 (2026-09-10) |
| **Generator** | frd-generator-v6 (v6.1 HTML-first) |
| **Source Brief** | — (WF-01 lane · no CODE brief · variant fallback จาก BRD) |
| **Source BRD** | BRD_เบิกค่าใช้จ่าย.md (status: **APPROVED**, 2026-09-10) |
| **Source HTML** | expense.html (source of truth · 2512 บรรทัด · audit FAIL=0 · qc-ux BLOCK=0 · coverage FN 22/22 + FN-18/19/20 · S 15/15) |
| **Author** | BA — ทีม Human Capital (2BSimple) |
| **Reviewers** | Tech Lead · PM · SEC · QA Lead · Finance (มุม FC/EC + จ่าย) |

**Variant decision (fallback from BRD):** FULL — pages=7 (§14.6 · list + wizard 5 ขั้น + view drawer 4 tabs + 3 modal) · states: lifecycle **8** (≥4) · approval=**YES** (DOA ตามวงเงิน) · money=**YES** (ยอด/เพดาน/VAT/ทดรอง/7C) · §9.5 มี Rule-Engine (DOA R04, Budget/Welfare R15). เข้าเงื่อนไข `states ≥ 4 OR (approval AND money) OR Engine Management → FULL`.

---

## §0.2 Revision History

| Version | Date | Author | Changes |
|---|---|---|---|
| 1.0 | 2026-09-10 | BA Human Capital | Initial FRD (FULL) · HTML-first · สะท้อน scope BRD (FN-01..17 + FN-90..94) + **3 PM/BA additions 2026-09-10 (FN-18/19/20)** |

---

## §0.3 Scope

### In Scope
1. สร้างใบเบิกผ่าน **wizard 5 ขั้น** (เลือกแหล่งที่มา › ข้อมูลหลัก › รายการค่าใช้จ่าย › เอกสารแนบ › ตรวจสอบและยืนยัน) (FN-01)
2. หัวเอกสาร: ผู้เบิก (combobox #102) · วันที่ (พ.ศ.) · ช่องทางจ่าย · ตำแหน่ง/ศูนย์ต้นทุน snapshot ณ วันเบิก (FN-02, FN-06)
3. รายการค่าใช้จ่าย (line editor B2 v2): วันที่ · หมวด · รายละเอียด · จำนวนเงิน · VAT none/add/included + ยอดรวม/VAT/สุทธิ (FN-03)
4. เพดานหมวด (อ่านจาก HR Config #107) — เกิน = **เตือน + บังคับเหตุผล** (ไม่ hard block · A-EXP-05 · LOCK-08) (FN-04)
5. Validation ก่อนส่ง: ต้องมี ≥1 รายการ + ยอด>0 + แนบใบเสร็จตามนโยบายหมวด (FN-05, FN-12)
6. ส่งอนุมัติ → **DOA slot picker ตามวงเงิน** (ช่วงวงเงิน FREE ตั้งค่าอิสระที่ DOA กลาง · ไม่ hardcode สาย) (FN-07, FN-08)
7. แก้ยอดหลังส่ง → re-resolve สาย DOA ถ้าข้ามช่วงวงเงิน (FN-11)
8. ตีกลับ (ระบุเหตุผล) → แก้แล้วยื่นใหม่ · ยกเลิกก่อนอนุมัติ (soft archive · เฉพาะฉบับร่าง) (FN-13, FN-14)
9. อนุมัติครบสาย → ออกเลข EXP-YYYY-NNNN + เก็บสำเนา PDF + ยิง **7C (FC งบ / EC มูลค่า · ไม่มี AC)** (FN-09, FN-19)
10. มุมมองเอกสาร: tabs รายละเอียด › PDF Preview (a4) › ลายเซ็น/อนุมัติ (DOA timeline) › ประวัติ (audit) + เอกสารแนบใน tab รายละเอียด (FN-15, FN-17)
11. เลือกช่องทางจ่าย → ส่งจ่าย (**hook display-only**) + สถานะ "จ่ายแล้ว" อ่านจากปลายทาง (Payroll/Finance) (FN-10, FN-16)
12. **[FN-18 · PM/BA · OQ-EXP-01]** touchpoint ข้ามฟีเจอร์: (a) ช่องทางจ่ายเพิ่ม "ใบสำคัญจ่าย (PV)" + "เงินสดย่อย (F091)" hook display-only · (b) "เคลียร์เงินทดรอง หักลบอัตโนมัติ" soft-ref F103 · ยอดจ่ายสุทธิ = ยอดใบเบิก − ทดรองค้าง (display-only) — F101 **ไม่ออก/ไม่ปรับ ledger F103**
13. **[FN-19 · PM/BA · OQ-EXP-02]** 7C = **FC/EC เท่านั้น (ไม่มี AC)** — สะท้อนใน events/CSQ
14. **[FN-20 · PM/BA · OQ-EXP-03]** ขอบเขตการมองเห็น: ผู้เบิก/ธุรการ `scope:self` · **role ใหม่ "เจ้าหน้าที่ (HR/Finance)"** `scope:all` + unmask แต่ **ไม่ใช่ผู้อนุมัติ DOA**
15. กติกากลาง: list docPill + signprog + filter + empty (FN-90) · ตีกลับ/ยกเลิก confirm + soft archive (FN-91) · validate + กัน double-submit + wizard ล็อกลำดับ (FN-92) · audit append-only (FN-93) · masking ตัวเงิน RESTRICTED ตาม role (FN-94)

### Out of Scope (ตัดโดยมติ — unsupported 7)
- **จ่ายเงินจริง / โอน / ตัดจ่าย & GL posting** — hook display-only เท่านั้น (A-EXP-02 · LOCK-03 · ไปที่ Finance/Payroll/Accounting)
- **ระบบเงินสดย่อย / ออกเงินทดรองเต็มรูป** — อยู่ที่ F091 (Petty Cash) / F103 (Advance) · F101 ต่อ **แค่จุดเชื่อม** (OQ-EXP-01 · LOCK-09)
- **เบี้ยเลี้ยง / ค่าน้ำมันต่อกิโลเมตร (mileage)** — NICE ไม่รองรับรอบนี้
- **คำขออนุมัติเดินทางล่วงหน้า (travel request/authorization)** — NICE
- **หลายสกุลเงิน** — THB only รอบนี้
- **อ่านใบเสร็จอัตโนมัติ (OCR)** — ไม่รองรับ
- **สร้าง/แก้เพดานหมวด/นโยบายเอง** — อ่านจาก HR Configuration (#107) เท่านั้น (LOCK-05)

### Out of Scope (mark from Phase 2.5 skipped probes)
- ไม่มี probe ที่ skip — Lane Mode ตอบ probe ครบด้วย conservative default (`[AI-DEFAULT]` · ดู 05_RULES §5.5) · ทุก default carry เป็น OQ ให้ BA/SEC/Finance confirm

---

## §0.4 Roles & Responsibilities (COSO)

| Role | Person/Team | Responsibilities |
|---|---|---|
| **Maker** | ผู้เบิก / ธุรการ (พนักงาน) | สร้างใบเบิก · เพิ่มรายการ · แนบเอกสาร · ส่งอนุมัติ (DOA slot picker) · แก้/ยื่นใหม่เมื่อตีกลับ · ยกเลิกฉบับร่าง |
| **Approver** | หัวหน้าสายงาน / ผจก.แผนก / ผอ. (ตาม DOA วงเงิน) | อนุมัติ/ตีกลับตามลำดับขั้น (ตามวงเงิน) |
| **เจ้าหน้าที่ (HR/Finance)** | ทีม HR/Finance | ติดตามใบเบิกทั้งหมด (scope:all · unmask) · เลือก/ยืนยันช่องทางจ่าย (hook) · **ไม่มีสิทธิ์อนุมัติ DOA** (FN-20) |
| **Owner** | HR/Finance + ผู้บริหาร | ติดตาม DOA compliance · เกินเพดาน · ยอดหักลบทดรอง |

> **SoD:** Maker (ผู้เบิก · สร้าง/ยื่น) ≠ Approver (หัวหน้า/ผจก./ผอ. · อนุมัติ DOA) — ผ่าน · เจ้าหน้าที่ HR/Finance = ติดตาม (ไม่อนุมัติ · OQ-EXP-03)
> รายละเอียดต่อ workflow → ดู `01_UI.md §1.3 Journey` + `05_RULES §5.3 Permission Matrix`

---

## §0.5 Dependencies

### Upstream (this feature depends on)
| Dependency | Type | Source |
|---|---|---|
| Employee (ผู้เบิก/ผู้อนุมัติ) | Data / API (read) | F011 — `GET /employees?status=active&q=` (combobox #102) |
| Movement (ตำแหน่ง/ศูนย์ต้นทุน snapshot) | Data / API (read) | F-HR-MOVE — `resolve(as_of=วันเบิก)` · null≠ไม่มี (BR-08) |
| HR Configuration (หมวด/เพดาน #107) | Data / API (read) | F164 — read-only · **group เพดานยังไม่มี → mock** (A-EXP-04) |
| DOA engine (สายอนุมัติตามวงเงิน) | Engine (external) | F-DLG-001 Policy Center — feature ประกาศเท่านั้น (DOA_BRIEF · **CL-0013 แขวน**) |
| ENG-NOTIFY (แจ้งเตือน) | Engine (external) | F-NOTIFY — event ยื่น/ผล-ตีกลับ/จ่าย/เกินเพดาน (NTF_BRIEF) |
| ENG-DOC-NUM / ENG-DOC-STORE | Engine (external) | Document Config (DOCCFG_BRIEF) — เลข EXP + สำเนา PDF (ห้าม hardcode รูปแบบ) |
| F103 เงินทดรองค้าง | Data / hook (read · display-only) | F103 (Advance) — `GET /advances/outstanding?emp_id=` · **F101 ไม่ปรับ ledger** (FN-18) |

### Downstream (features/engines that consume from this feature)
| Consumer | What it uses |
|---|---|
| 7C / โครงสร้างต้นทุน (CSQ) | event ตอนอนุมัติครบ → **FC (commit งบ) + EC (มูลค่า)** เท่านั้น (**ไม่มี AC** · CSQ_BRIEF) |
| Payroll (HK-1) / Finance / F091 / F109 | สั่งจ่าย (hook display-only) — ไม่ auto-จ่าย · F101 อ่านสถานะ paid กลับ |
| F103 เงินทดรอง | ค่าหักลบ (offset) — display-only · F101 ส่งค่าให้ F103 ไม่ปรับ ledger เอง (FN-18) |
| F117 Budget Control | ยอดใบเบิกตรวจงบก่อนอนุมัติ (ctl · display-only mock · W7 ยังไม่ dev · OQ-EXP-04) |
| F102 Welfare | เพดานสิทธิ์สวัสดิการคงเหลือ (ctl · display-only mock · OQ-EXP-04) |

### External
| Service | Purpose |
|---|---|
| Policy Center (F-DLG-001) | DOA chain resolve **ตามวงเงิน (มีวงเงิน)** — FREE ranges (ไม่ hardcode 3-tier) |
| Policy Center (Data Classification / Restricted Resources) | wire field Restricted (ยอด/เพดาน/ทดรอง/มูลค่า EC · ดู 04_DB §4.6.6) |

---

## §0.6 Stack & Architecture

| Layer | Technology |
|---|---|
| Frontend | vanilla JS SPA (prototype) → React/Next.js (build) · single feature menu #104 (list + wizard drawer + view drawer + modals) |
| API | Node.js / Strapi (REST · `/api/v1/expense/...`) |
| Database | PostgreSQL (RLS multi-tenant) |
| Engine layer | CUBIC Registry (expense-vat-calculator, advance-offset-calculator) + external (DOA, ENG-NOTIFY, ENG-DOC-NUM/STORE) |
| Auth | JWT + role-based (RBAC กลาง · persona demo `.demo-strip` #105 = scaffolding) |

---

## §0.7 Multi-Tenant & Security Context

- [x] Multi-tenant feature: **YES** (RLS by tenant)
- [x] PII data involved: **YES** (ผู้เบิก/ผู้อนุมัติ snapshot: ชื่อ/ตำแหน่ง/แผนก — ดู 04_DB §4.2 + §4.6)
- [x] Financial data: **YES** (ยอดเบิก · เพดานหมวด · VAT · เงินทดรอง · มูลค่า FC/EC)
- [x] Audit log required: **YES** (append-only ทุก mutation · FN-93)

**Security Bible domains applied:** D2 (Auth) · D5 (Financial) · D7 (PII) · D9 (Audit) · D15 (Admin/approval · DOA) · D17 (Multi-tenant) — ดู 05_RULES §5.7 · Security Preset **P6 (HR/PII Sensitive · 15 controls)**

### §0.7.1 Data Classification Summary

Highest classification level ที่ feature นี้แตะ:
- [x] **Has Restricted fields** — `grand`/ยอดรวม · `unit_price`/จำนวนเงินต่อรายการ · เพดานหมวด · เงินทดรอง (advance_offset) · มูลค่า FC/EC → mask ตาม role (FN-94)
- [x] **Has Confidential fields** — employee snapshot (name/position/cost_center · PII) · approver identity · reject reason
- [x] Internal (default) — สถานะ · timestamps · audit
- [ ] Public-facing data — ไม่มี

**Linkage:** Restricted (ตัวเงินทั้งหมด) → register Policy Center → Restricted Resources · PII (ผู้เบิก/ผู้อนุมัติ snapshot) → PDPA consent scope (ดู 04_DB §4.6.6)

---

## §0.8 Open Questions

> Carry ครบจาก BRD §15 (ห้ามหายเงียบ) + Phase 2.5 `[AI-DEFAULT]` ที่ต้อง confirm

| ID | Question | Blocking? | Owner |
|---|---|---|---|
| OQ-01 (A-EXP-03) | **สาย DOA:** ช่วงวงเงินจริง (FREE ranges) + DOA role-id master · **CL-0013 (สายผู้บริหาร) แขวน 31 ส.ค.** — `DOA_RANGES` ใน HTML = mock (<5k/5k–50k/>50k) ห้าม hardcode ในระบบจริง · เดา role-id ผิดมีคนเอาไปตั้งค่าจริง | **YES** (dev ห้าม hardcode สาย · CL-0013 blocker) | SEC/BA + DOA declaration |
| OQ-02 (A-EXP-04) | **เพดานหมวด (R02):** ยังไม่มี group นี้ใน HR Config → mock · โครงอ้าง `resolve(date, company_id)` · ห้าม hardcode ตัวเลขเพดานในโค้ด | NO (ไม่บล็อก launch · dev อ่าน mock resolve จน group พร้อม) | HR Config / BA |
| OQ-03 (A-EXP-02) | **pay/GL hook contract (Phase B):** จ่ายจริง/GL = hook display-only — ยืนยัน contract ปลายทาง (Payroll HK-1 / Finance / Accounting / F109) | NO (ไม่บล็อก launch · ผูก Phase B) | dev Finance / BA |
| OQ-04 (RBAC) | mapping role→login จริง + สิทธิ์ "ธุรการสร้างแทนผู้เบิก" | YES (ก่อนตั้ง RBAC จริง) | SEC/BA |
| OQ-05 | **reverse-EC / release-FC on cancel-after-approval:** นโยบายถอน EC / ปลด FC commit เมื่อยกเลิก/แก้ **หลังออกเลข + ยิง FC/EC** — ⚠️ **หมายเหตุ:** HTML ปัจจุบัน `doCancel` อนุญาตยกเลิกเฉพาะ **draft** · `doReopen` เฉพาะ **rejected** เท่านั้น → **path "ยกเลิกหลังอนุมัติ" ยังไม่มีในระบบ** · flag ให้ BA ว่าควรมีหรือไม่ (ถ้ามี → ต้องนิยาม compensating FC/EC) | **YES** (กระทบเงิน) | BA/Finance |
| OQ-EXP-04 | hook เสริมใน HTML: **F117 Budget** (edge F101→F117 ctl) + **F102 Welfare** (edge F102→F101 ctl) — ยืนยันตั้งใจคงไว้ (display-only mock) หรือถอด · มาจาก Central Plan edges | NO (display-only · ไม่กระทบ verdict) | BA ยืนยัน |
| OQ-UX | ศัพท์ระบบบนจอ (hook / 7C / FC/EC / soft-ref) | NO | BA |
| OQ-06 | **Declarations (DOA/NTF/CSQ/DOCCFG/PDFDOC):** ผู้ใช้เลือก doccfg+doa+ntf (Central Plan dec chip ครบ 5) · รันสคริปต์ declaration **หลัง step 7 โดยผู้ใช้สั่ง** — FRD event/slot/doc_type/7C ⊆ brief แล้ว | NO | ผู้ใช้ (post-step-7) |

> Resolved → move to 07_LOCKED_DECISIONS §7.3

---

## §0.9 Glossary

| Term | Definition |
|---|---|
| DOA (มีวงเงิน) | Delegation of Authority — สายอนุมัติกลาง (F-DLG-001) resolve **ตามยอดรวม** · ช่วงวงเงิน FREE · feature ประกาศเท่านั้น |
| 7C | โครงสร้างต้นทุน 7 มิติ (CSQ) — feature นี้ยิง **FC (commit งบ) + EC (มูลค่าค่าใช้จ่าย)** ตอนอนุมัติครบ |
| FC | Fund/Budget Commit — จองงบตอนอนุมัติ (ยิงเข้า 7C) |
| EC | Expense Category — มูลค่าค่าใช้จ่าย (ยิงเข้า 7C) |
| AC | Accounting Cost — การลงบัญชี · **ไม่ประกาศในฟีเจอร์นี้** (Accounting ปลายทาง post เอง · LOCK-04) |
| hook display-only | จุดเชื่อมปลายทาง (จ่าย/งบ/ทดรอง/สวัสดิการ) — แสดงสถานะ/ค่า mock เท่านั้น · F101 ไม่จ่าย/ไม่ post/ไม่ปรับ ledger |
| touchpoint (F091/F103) | จุดเชื่อมข้ามฟีเจอร์ (PV/petty · หักลบทดรอง) — ไม่ใช่ระบบเต็มรูป (FN-18) |
| snapshot (ตำแหน่ง/cc) | ตำแหน่ง/ศูนย์ต้นทุน resolve จาก Movement ณ วันเบิก (soft ref · null≠ไม่มี · BR-08) |
| over-cap | รายการเกินเพดานหมวด → เตือน + บังคับเหตุผล (ยังส่งได้ · ไม่ hard block · LOCK-08) |
| scope self/all | ขอบเขตการมองเห็นใบเบิก: self (ผู้เบิก/ธุรการ เห็นเฉพาะใบตน) / all (ผู้อนุมัติ, เจ้าหน้าที่ HR/Finance) (FN-20) |

---

## §0.10 Pack Navigation

| File | Audience | Purpose |
|---|---|---|
| 00_OVERVIEW.md | All | meta + scope + coverage |
| 01_UI.md | FE dev | Layout Decision Log + Pages + Journey |
| 02_API.md | BE dev (HTTP) | API contracts |
| 03_LOGIC.md | BE dev (logic) | Functions + Engines + Trace |
| 04_DB.md | DBA / BE | Tables + Fields + Classification |
| 05_RULES.md | BE + QA | Rules + Edge Cases + Errors + Security |
| 06_TESTS.md | QA | AC + DoD + Cross-module |
| 07_LOCKED_DECISIONS.md | All | Scope Lock + LDs |
| INDEX.md | All | Cross-reference quick nav |

---

## §0.11 Scope Lock

> FULL variant → รายละเอียดอยู่ที่ **07_LOCKED §7.0** (immutable) · ที่นี่สรุป ref เท่านั้น
> **Scope Lock Ref:** LANE_BRIEF + STANDARD_BASELINE (MUST 11 · lifecycle 8 state) + Central Plan row F101 (dec/dep) · BRD §3.4 (LOCK-01..10 · รวม PM/BA 2026-09-10 OQ-EXP-01/02/03)

---

## §0.12 Coverage Manifest (กัน requirement หล่น BRD→FRD)

> ทุก FN (25) + Story (BRD §7) + Rule (§9) + Edge confirmed (§10) → ที่อยู่ใน pack · **คอลัมน์ FN-XX บังคับ (Lane Mode)**

| FN | BRD Ref | Requirement (ย่อ) | อยู่ที่ใน Pack |
|---|---|---|---|
| **FN-01** | §7 US-01 · §9 R14 | wizard 5 ขั้น | 01_UI P-02 · 02_API-02 · 03_FN-01 · 04_DB T_expense_claim · 05_RULES BR-14 · 06 AC-01 |
| **FN-02** | §7 US-01 | หัวเอกสาร: ผู้เบิก/วันที่/ช่องทางจ่าย | 01_UI P-02(step2) · 02_API-02/14/15 · 03_FN-01/FN-15 · 04_DB claim · 06 AC-01 |
| **FN-03** | §7 US-02 · §9 R01 | line editor + VAT none/add/included + totals | 01_UI P-02(step3) · 02_API-02 · 03_ENG-EXP-01 · 05_RULES BR-01 · 06 AC-02 |
| **FN-04** | §7 US-03 · §9 R02 | เกินเพดาน → เตือน + บังคับเหตุผล | 01_UI P-02(step3/5) · 02_API-02/05 · 03_FN-13 · 05_RULES BR-02 · 06 AC-03 |
| **FN-05** | §7 US-02 · §9 R03 | ไม่มีรายการ/ยอด=0 → ส่งไม่ได้ | 01_UI P-02(footer) · 02_API-05 · 03_FN-06 · 05_RULES BR-03 · 06 AC-04 |
| **FN-06** | §7 US-01 · §9 R08 | ตำแหน่ง/cc snapshot ณ วันเบิก | 01_UI P-02(step2) · 02_API-15 · 03_FN-15 · 05_RULES BR-08 · 06 AC-01 |
| **FN-07** | §7 US-04 · §9 R04 | ส่งอนุมัติจาก wizard/ใบเบิก | 01_UI P-04 · 02_API-05 · 03_FN-06 · 05_RULES BR-04 · 06 AC-05 |
| **FN-08** | §7 US-04 · §9 R04 | DOA slot picker ตามวงเงิน (ไม่ hardcode) | 01_UI P-04 · 02_API-05/12 · 03_FN-05/FN-06 + ENG (ext DOA) · 05_RULES BR-04 · 06 AC-05 |
| **FN-09** | §7 US-06 · §9 R06/R07 | อนุมัติ → เลข EXP + PDF + 7C (FC/EC) | 01_UI P-03(sign) · 02_API-06 · 03_FN-07/FN-11/FN-22/FN-23 · 05_RULES BR-06/BR-07 · 06 AC-06 · XT-01 |
| **FN-10** | §7 US-07 · §9 R09 | เลือกช่องทางจ่าย → ส่งจ่าย (hook) | 01_UI P-03(detail) · 02_API-10 · 03_FN-12 · 05_RULES BR-09 · 06 AC-07 · XT-02 |
| **FN-11** | §5 A6 · §9 R05 | แก้ยอดข้ามช่วง → re-resolve DOA | 01_UI P-02/P-04 · 02_API-04/05/12 · 03_FN-05 · 05_RULES BR-05 · 06 AC-05b |
| **FN-12** | §7 US-02 · §9 R03 | แนบใบเสร็จตามนโยบายหมวด | 01_UI P-02(step4) · 02_API-13 · 03_FN-14 · 05_RULES BR-03 · 06 AC-04 |
| **FN-13** | §5 A4 · §9 R04 | ตีกลับ → แก้แล้วยื่นใหม่ | 01_UI P-05 · 02_API-07/09 · 03_FN-08/FN-10 · 05_RULES BR-18 · 06 AC-08 |
| **FN-14** | §5 A5 · §9 R10 | ยกเลิกก่อนอนุมัติ (soft archive) | 01_UI P-06 · 02_API-08 · 03_FN-09 · 05_RULES BR-10 · 06 AC-09 |
| **FN-15** | §7 US-10 · §9 R06 | PDF tab (a4) + tab ลายเซ็น | 01_UI P-07 · 02_API-20 · 03_FN-23 · 06 AC-10 |
| **FN-16** | §7 US-07 · §9 R09 | "จ่ายแล้ว" อ่านจากปลายทาง display-only | 01_UI P-03(detail) · 02_API-11 · 03_FN-12 · 05_RULES BR-09 · 06 AC-07 |
| **FN-17** | §7 US-10 | view tabs รายละเอียด›PDF›ลายเซ็น›ประวัติ + แนบ | 01_UI P-03 · 02_API-03 · 03_FN (view build) · 06 AC-10 |
| **FN-18** | §3.1(12) · §9 R11 | touchpoint: PV/petty (F091) + หักลบทดรอง (F103 · display-only) | 01_UI P-03(detail) · 02_API-10/16 · 03_FN-16 + ENG-EXP-02 · 05_RULES BR-11 · 06 AC-11 · XT-03 |
| **FN-19** | §3.1(13) · §9 R07 | 7C = FC/EC เท่านั้น (ไม่มี AC) | 03_FN-22 · 02_API §2.X · 05_RULES BR-07 · 06 XT-01 |
| **FN-20** | §3.1(14) · §9 R12 | visibility scope self/all + role เจ้าหน้าที่ HR/Finance | 01_UI §1.2 · 02_API-01/03 · 03_FN-19/FN-20 · 04_DB §4.6 · 05_RULES BR-12/§5.3 · 06 AC-12 |
| **FN-90** | กติกากลาง | list docPill + signprog + filter + empty | 01_UI §1.6 P-01 · 02_API-01 · 03_FN (list/pill/signprog) · 06 AC-13 |
| **FN-91** | กติกากลาง | ตีกลับ/ยกเลิก confirm + soft archive | 01_UI P-05/P-06 · 02_API-07/08 · 03_FN-08/FN-09 · 05_RULES BR-10 · 06 AC-08/AC-09 |
| **FN-92** | กติกากลาง | validate + กัน double-submit + wizard ล็อก | 02_API §2.3 idempotency · 03_FN (state._busy) · 05_RULES EC-03 · 06 AC-14 |
| **FN-93** | กติกากลาง · §9 R10 | audit append-only | 03_FN-21 · 04_DB T_expense_audit_log · 05_RULES §5.7 D9 · 06 AC-15 |
| **FN-94** | §9 R10 · §4 note | masking ตัวเงิน RESTRICTED ตาม role | 01_UI §1.2 · 03_FN-18 · 04_DB §4.6 · 05_RULES §5.7 D-CLASS · 06 AC-12/AC-16 |

**สรุป:** FN **25/25** ครอบ (FN-01..17 + FN-90..94 + **FN-18/19/20**) · Stories 10/10 (US-01..10) · Rules R01–R15 → 05_RULES ครบ · Edges §10.1 (8 ☑) + §10.2 (6 probe) → 05_RULES §5.5 · **ไม่มี requirement ที่ไม่มีที่ลง** · ของที่ยังต้องเคาะ → OQ-01..06 + OQ-EXP-04 + OQ-UX
