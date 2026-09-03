# 07_LOCKED_DECISIONS — F-HR-TRAIN · Training (อบรม)

> **Audience:** All roles
> **Purpose:** Scope Lock (immutable) + Locked Decisions

---

## §7.0 Scope Lock (Imported from BRD §3.4) — IMMUTABLE

> ข้อยืนยันจากมติ 17 ส.ค. + STANDARD_BASELINE + HANDOFF §3 — ห้าม override ตลอด pack + chain ปลายน้ำ (HTML/Test/Dev)
> **Scope Lock Ref:** LANE_BRIEF + STANDARD_BASELINE (MUST 9) + HANDOFF §3 (LOCK 17 ส.ค. 2569)

| LOCK-ID | ข้อยืนยัน | อ้างเอกสาร | สถานะใน FRD |
|---|---|---|---|
| LOCK-01 | อนุมัติ (DOA) เมื่อหลักสูตร **has_cost** เท่านั้น (ฟรี = ข้าม) | มติ 17 ส.ค. · BRD §3.4 | ✅ สอดคล้อง (BR-04 · FN-08/09/10) |
| LOCK-02 | ค่าอบรม = **hook Expense Claim** (ไม่จ่าย/ไม่ post เอง) | มติ · BRD §3.4 | ✅ (BR-06 · FN-16 display-only) |
| LOCK-03 | gap = **hook Performance** (อ่านอย่างเดียว · ไม่สร้าง gap เอง) | มติ · BRD §3.4 | ✅ (BR-07 · FN-20 read-only) |
| LOCK-04 | CSQ = **EC เท่านั้น** (ไม่มี AC · Expense เป็นตัวลงบัญชี) | STANDARD_BASELINE cap.7 · CSQ_BRIEF | ✅ (BR-09 · FN-10 · §2.X ไม่ประกาศ AC) |
| LOCK-05 | audit **append-only** + masking ตาม role | current-state §3 · BRD §3.4 | ✅ (BR-08 · FN-21/FN-19 · 04_DB §4.6) |
| LOCK-06 | config หมวดหลักสูตร **อ่านจาก HR Config #107** (ไม่ CRUD) | มติ · BRD §3.4 | ✅ (Out-of-Scope #5 · API-26 read-only) |
| LOCK-07 | ใบรับรอง = **soft ref** (ไม่มีเลขรัน/PDF) | มติ · BRD §3.4 · NOT_NEEDED | ✅ (BR-07C · FN-15 · doccfg/pdfdoc = NOT-NEEDED) |

- **Drift พบระหว่างเขียน FRD (ชั้นที่ 3):** ไม่พบ In-Scope เกิน LOCK · **ยกเว้น** DOA role-id drift `role-hr-ld-head` (DOA_BRIEF) vs `role-hr-dev-head` (HTML) — ไม่ใช่ scope drift แต่เป็น config id ที่ต้องเคาะ → **OQ-04** (ห้าม hardcode · เดาผิดมีคนตั้งค่าจริง)

---

## §7.1 Locked Decisions (LD)

### LD-01: Optimistic locking (version) กัน concurrent approval
- **Date:** 2026-09-03 · **Context:** EC-01 (2 approver ชนกัน · BRD §10.2 [CA])
- **Options:** A) pessimistic lock · B) optimistic (`version`) · C) last-write-wins
- **Decision:** B — `version` column + 409 ERR_STALE_DATA
- **Rationale:** contention น้อย · pessimistic ลงโทษ 99% เคสปกติ
- **Implications:** 04_DB `version` ทุกตาราง mutation · 02_API If-Match/version · 06_TESTS TC-CC-01
- **Tag:** `[AI-DEFAULT]` (Lane Mode) → **confirm ที่ review** · **Reversibility:** MEDIUM

### LD-02: ENG-TRN-01/02 register CUBIC ที่ Phase 2 (scope-local ก่อน)
- **Context:** completion-metrics + hours-accumulator มี reuse potential (HR analytics)
- **Decision:** scope-local (DRAFT) ตอนนี้ · register ตอน feature ที่ 2 ยืนยัน reuse
- **Implications:** 03_LOGIC §3.2 status=DRAFT · **Reversibility:** EASY

### LD-03: มูลค่า EC / ต้นทุนต่อหัว = display-only จน Rate Card (F060) พร้อม
- **Context:** Rate Card ยังไม่ dev (R17 DYNAMIC) · **Decision:** render "อ้างอิง Rate Card · เชื่อมเมื่อพร้อม" — **ห้าม hardcode ตัวเลข**
- **Implications:** API-28 contract-pending · FE display-only · migrate Phase 2 · **OQ-03** · **Reversibility:** EASY (ต่อ endpoint เมื่อพร้อม)

### LD-04: cancel หลังส่ง EC = ไม่ auto-reverse (conservative)
- **Context:** EC-05 / BRD §10.2 [ST] (กระทบเงิน) · **Decision:** cancel ได้ (soft archive) แต่ **ไม่ถอน EC อัตโนมัติ** · flag Finance
- **Implications:** FN-12 · 06_TESTS XT-02 · **Tag:** `[AI-DEFAULT]` → **OQ-06 (BA/Finance เคาะ policy reverse)** · **Reversibility:** MEDIUM

### LD-05: DOA chain = ประกาศเท่านั้น (ไม่ hardcode สาย)
- **Context:** LOCK-01 · DOA_BRIEF · **Decision:** สายมาจาก DOA กลาง (F-DLG-001) · feature เก็บ slot_role/slot_name + approver_id ที่เลือก · **ไม่ hardcode คน/ลำดับในโค้ด**
- **Implications:** FN-09 · 04_DB T_training_approval_step · run doa-declaration **หลัง step 7 โดยผู้ใช้สั่ง** · **OQ-04** (role-id + drift) · **Reversibility:** N/A (config)

---

## §7.2 Convention Deviations

### CD-01: custom action endpoints (POST /:id/publish, /open, /approve, ...) แทน PATCH
- **Convention default:** PATCH สำหรับ partial state update
- **Deviation:** POST custom action (semantic clarity — publish/open/approve/close/cancel = action ไม่ใช่ property)
- **Reason:** สอดคล้อง lifecycle-action ของ archetype master · trace ชัดกับ FN
- **Apply to:** API-05/06/11/12/15/16/17/18/19/20/21/22

### CD-02: ใบรับรอง ไม่ใช้ doccfg (เลขรัน) / pdfdoc
- **Reason:** LOCK-07 soft ref · NOT_NEEDED.md ยืนยัน DOCCFG/PDFDOC = NOT-NEEDED

---

## §7.3 Open Questions Promoted from 00_OVERVIEW
> ยังไม่มี OQ ที่ resolved → ทั้งหมดยังเปิดที่ 00_OVERVIEW §0.8 (OQ-01..07) · เมื่อ BA/SEC เคาะ → ย้ายมาเป็น LD

---

## §7.4 Architecture Tradeoffs Acknowledged
### AT-01: PostgreSQL RLS over app-level filtering — YES (CUBE ERP standard)
### AT-02: Synchronous approval/notify (V1) — sync; re-evaluate เมื่อ latency > 2s
### AT-03: approval embedded (summary ใน enrollment) + child table (step) — สมดุล query + audit

---

## §7.5 Decisions Deferred to Implementation
| Item | Owner | Deadline |
|---|---|---|
| DOA role-id ปลายทาง (OQ-04) + CL-0013 แขวน | SEC/BA + DOA declaration | ก่อน wire DOA |
| RBAC หัวหน้า สร้าง/อนุมัติ (OQ-05) | SEC/BA | ก่อนตั้ง RBAC |
| นโยบาย reverse EC (OQ-06) | BA/Finance | ก่อน dev cancel path |
| Rate Card wire (OQ-03) | dev F060 | Phase 2 |
| Restricted Resources / PDPA scope wire | SEC + Policy Center | pre-deploy |

---

## §7.6 References
- Convention: `knowledge/conventions.md` · Edge origins: `references/edge-case-probes.md`
- Declarations (Sync Read): `5_DECLARATIONS/DOA_BRIEF.md · NTF_BRIEF.md · CSQ_BRIEF.md · NOT_NEEDED.md`
- Related: F-DLG-001 (DOA) · F-NOTIFY · F101 (Expense) · F131 (Performance) · F164 (HR Config) · F060 (Rate Card · pending)
