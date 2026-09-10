# 07_LOCKED_DECISIONS — F-HR-EXPENSE · Expense Claim (เบิกค่าใช้จ่าย)

> **Audience:** All roles
> **Purpose:** Scope Lock (immutable) + Locked Decisions

---

## §7.0 Scope Lock (Imported from BRD §3.4) — IMMUTABLE

> ข้อยืนยันจาก LANE_BRIEF + STANDARD_BASELINE + Central Plan row F101 + PM/BA 2026-09-10 (OQ-EXP-01/02/03) — ห้าม override ตลอด pack + chain ปลายน้ำ (HTML/Test/Dev)
> **Scope Lock Ref:** LANE_BRIEF + STANDARD_BASELINE (MUST 11 · lifecycle 8 state) + Central Plan row F101 (dec/dep · CL-0013 แขวน)

| LOCK-ID | ข้อยืนยัน | อ้างเอกสาร | สถานะใน FRD |
|---|---|---|---|
| LOCK-01 | อนุมัติ = **DOA threshold ตามวงเงิน** · ช่วงวงเงิน FREE ตั้งค่าอิสระ · **ไม่ hardcode สาย/ไม่ใช่ 3-tier ตายตัว** | BRD §3.4 · มติ 17 ส.ค. | ✅ สอดคล้อง (BR-04 · FN-05/06 · DOA_RANGES=mock) |
| LOCK-02 | เลข EXP-YYYY-NNNN + สำเนา = ENG-DOC-NUM/STORE (doccfg) · ออกตอนอนุมัติ (immutable) | BRD §3.4 | ✅ (BR-06 · FN-11/23 · ตัวนับ global) |
| LOCK-03 | จ่ายจริง/post = **hook display-only** (Payroll/โอน/PV/petty/Accounting) — F101 ไม่ทำเอง | BRD §3.4 | ✅ (BR-09 · FN-12 display-only · Out #1) |
| LOCK-04 | 7C = **FC + EC เท่านั้น (ไม่มี AC)** — Accounting ปลายทาง post | BRD §3.4 · CSQ_BRIEF · OQ-EXP-02 | ✅ (BR-07 · FN-22 · §2.X ไม่ประกาศ AC) |
| LOCK-05 | เพดานหมวด/นโยบาย = **อ่านจาก HR Config #107** (effective_date) — ไม่ CRUD | BRD §3.4 | ✅ (BR-02 · FN-13/14 read-only · Out #7 · A-EXP-04 mock) |
| LOCK-06 | ตำแหน่ง/ศูนย์ต้นทุน = **snapshot Movement ณ วันเบิก** (soft ref · null≠ไม่มี) | BRD §3.4 | ✅ (BR-08 · FN-15) |
| LOCK-07 | audit **append-only** + เงิน **RESTRICTED masking** + ไม่มี hard delete | BRD §3.4 | ✅ (BR-10 · FN-21/18 · 04_DB §4.6) |
| LOCK-08 | over-cap = **warn + บังคับเหตุผล (ไม่ hard block)** (A-EXP-05) | BRD §3.4 | ✅ (BR-02 · FN-13 · ยังส่งได้) |
| LOCK-09 | **[OQ-EXP-01]** cross-feature = touchpoint display-only (PV/petty F091 · หักลบทดรอง F103) — F101 ไม่ออก/ปรับ ledger ปลายทาง | BRD §3.4 · PM/BA 2026-09-10 | ✅ (FN-18 · FN-16/12 · Out #2) |
| LOCK-10 | **[OQ-EXP-03]** visibility scope: ผู้เบิก/ธุรการ=self · เจ้าหน้าที่ HR/Finance=all+unmask+ไม่อนุมัติ | BRD §3.4 · PM/BA 2026-09-10 | ✅ (FN-19/20 · §5.3 · BR-12) |

- **Drift พบระหว่างเขียน FRD (ชั้นที่ 3):** ไม่พบ In-Scope เกิน LOCK
  - **หมายเหตุ 1 (OQ-EXP-04):** hook เสริมใน HTML **F117 Budget** (edge F101→F117 ctl) + **F102 Welfare** (edge F102→F101 ctl) — มาจาก Central Plan edges · display-only mock มีป้ายกำกับชัด → บันทึก In-Scope §3.1(11)/BR-15 · ยืนยัน scope กับ BA (ไม่ตัด/ไม่รับรองเงียบ)
  - **หมายเหตุ 2 (OQ-01):** DOA role-id ปลายทาง + ช่วงวงเงินจริง + **CL-0013 (สายผู้บริหาร) แขวน 31 ส.ค.** — ไม่ใช่ scope drift แต่เป็น config ที่ต้องเคาะ → OQ-01 (ห้าม hardcode · เดาผิดมีคนตั้งค่าจริง)

---

## §7.1 Locked Decisions (LD)

### LD-01: Optimistic locking (version) กัน concurrent approval
- **Date:** 2026-09-10 · **Context:** EC-01 (2 approver ชนกันขั้นเดียว · BRD §10.2 [CA])
- **Options:** A) pessimistic lock · B) optimistic (`version`) · C) last-write-wins
- **Decision:** B — `version` column + 409 ERR_STALE_DATA
- **Rationale:** contention น้อย · pessimistic ลงโทษ 99% เคสปกติ
- **Implications:** 04_DB `version` ทุกตาราง mutation · 02_API If-Match/version · 06_TESTS TC-CC-01
- **Tag:** `[AI-DEFAULT]` (Lane Mode) → **confirm ที่ review** · **Reversibility:** MEDIUM

### LD-02: ENG-EXP-01/02 register CUBIC ที่ Phase 2 (scope-local ก่อน)
- **Context:** expense-vat-calculator + advance-offset-calculator มี reuse potential (เอกสารธุรกรรมอื่น / F103 reconcile)
- **Decision:** scope-local (DRAFT) ตอนนี้ · register ตอน feature ที่ 2 ยืนยัน reuse
- **Implications:** 03_LOGIC §3.2 status=DRAFT · **Reversibility:** EASY

### LD-03: DOA chain = ประกาศเท่านั้น · ช่วงวงเงิน FREE (ไม่ hardcode 3-tier)
- **Context:** LOCK-01 · DOA_BRIEF · **Decision:** สายมาจาก DOA กลาง (F-DLG-001) · feature เก็บ slot_role + approver_id ที่เลือก · resolve ตามยอด · **DOA_RANGES ใน HTML = mock (ห้าม hardcode ในระบบจริง)**
- **Implications:** FN-05 · 04_DB T_expense_approval_step · run doa-declaration **หลัง step 7 โดยผู้ใช้สั่ง** · **OQ-01** (role-id + CL-0013 แขวน) · **Reversibility:** N/A (config)

### LD-04: จ่ายจริง/GL/ทดรอง/งบ/สวัสดิการ = hook display-only
- **Context:** LOCK-03/09 · BR-09/11/15 · **Decision:** F101 **ไม่จ่าย/ไม่ post/ไม่ปรับ ledger** — hook display-only (Payroll/Finance/F091/F109/F103/F117/F102)
- **Implications:** FN-12/16/17 · 06_TESTS XT-02/03/05 · **OQ-03** (pay/GL contract Phase B) · **OQ-EXP-04** (F117/F102 ยืนยัน) · **Reversibility:** EASY (ต่อ endpoint เมื่อพร้อม)

### LD-05: 7C = FC/EC เท่านั้น (ไม่มี AC)
- **Context:** LOCK-04 · CSQ_BRIEF · มติ PM/BA (OQ-EXP-02) · **Decision:** อนุมัติครบ → emit FC (commit งบ) + EC (มูลค่า) · **ไม่ประกาศ AC** (Accounting ปลายทาง post)
- **Implications:** FN-22 · 02_API §2.X · 06_TESTS XT-01 · **Reversibility:** LOW (มติล็อก)

### LD-06: cancel เฉพาะ draft · reopen เฉพาะ rejected — ยกเลิกหลังอนุมัติ = ไม่มี path
- **Context:** EC-05 · BRD §10.2 [ST] (กระทบเงิน) · **Decision (conservative):** cancel ได้เฉพาะ draft (soft archive) · reopen เฉพาะ rejected (กันเลขหาย) · **ไม่มี transition "approved/paid → cancelled"**
- **Implications:** FN-09/10 · 06_TESTS XT-04 · **Tag:** `[AI-DEFAULT]` → **OQ-05 (BA/Finance เคาะว่าควรเปิด path + นิยาม reverse EC/release FC หรือไม่)** · **Reversibility:** MEDIUM

---

## §7.2 Convention Deviations

### CD-01: custom action endpoints (POST /:id/submit, /approve, /reject, /cancel, /reopen, /pay-channel) แทน PATCH
- **Convention default:** PATCH สำหรับ partial state update
- **Deviation:** POST custom action (semantic clarity — submit/approve/reject/cancel/reopen = action ไม่ใช่ property)
- **Reason:** สอดคล้อง lifecycle-action ของ archetype Q-document · trace ชัดกับ FN
- **Apply to:** API-05/06/07/08/09/10

### CD-02: doc_no ออกตอนอนุมัติ (nullable ก่อนหน้า) แทน gen ตอนสร้าง
- **Reason:** LOCK-02 · เลข EXP immutable ออกตอนอนุมัติครบ (ก่อนหน้าแสดง "(ร่าง)/(รออนุมัติ)") · ENG-DOC-NUM ตัวนับ global

---

## §7.3 Open Questions Promoted from 00_OVERVIEW
> ยังไม่มี OQ ที่ resolved → ทั้งหมดยังเปิดที่ 00_OVERVIEW §0.8 (OQ-01..06 + OQ-EXP-04 + OQ-UX) · เมื่อ BA/SEC/Finance เคาะ → ย้ายมาเป็น LD

---

## §7.4 Architecture Tradeoffs Acknowledged
### AT-01: PostgreSQL RLS over app-level filtering — YES (CUBE ERP standard) + scope guard self/all (FN-20)
### AT-02: Synchronous approval/notify (V1) — sync; re-evaluate เมื่อ latency > 2s
### AT-03: approval embedded (summary current/done ใน claim) + child table (step) — สมดุล query + audit

---

## §7.5 Decisions Deferred to Implementation
| Item | Owner | Deadline |
|---|---|---|
| DOA role-id + ช่วงวงเงินจริง (OQ-01) + **CL-0013 แขวน** | SEC/BA + DOA declaration | ก่อน wire DOA |
| เพดานหมวด group ใน HR Config (OQ-02) | HR Config / BA | ก่อน dev over-cap จริง |
| pay/GL hook contract Phase B (OQ-03) | dev Finance / BA | Phase B |
| RBAC mapping + ธุรการสร้างแทนผู้เบิก (OQ-04) | SEC/BA | ก่อนตั้ง RBAC |
| นโยบาย reverse EC/release FC on cancel-after-approval (OQ-05) | BA/Finance | ก่อนเปิด path ยกเลิกหลังอนุมัติ |
| F117 Budget / F102 Welfare ยืนยัน display-only (OQ-EXP-04) | BA | pre-dev |
| Restricted Resources / PDPA scope wire | SEC + Policy Center | pre-deploy |

---

## §7.6 References
- Convention: `knowledge/conventions.md` · Edge origins: `references/edge-case-probes.md`
- Declarations (Sync Read · run post-step-7 โดยผู้ใช้สั่ง): DOA_BRIEF · NTF_BRIEF · CSQ_BRIEF (FC/EC) · DOCCFG_BRIEF · PDFDOC (print-spec)
- Related: F-DLG-001 (DOA · CL-0013 แขวน) · F-NOTIFY · F164 (HR Config) · F-HR-MOVE (Movement) · F103 (Advance) · F117 (Budget · W7) · F102 (Welfare) · F091 (Petty Cash) · F109 (Payment) · F011 (Employee)
