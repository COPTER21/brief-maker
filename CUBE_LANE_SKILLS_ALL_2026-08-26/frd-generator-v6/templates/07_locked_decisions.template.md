# 07_LOCKED_DECISIONS — F-XX [Feature Name]

> **Audience:** All roles (PM, BA, FE, BE, QA, DBA, Architect)
> **Purpose:** Record decisions that were debated and resolved — ห้ามเปิดอภิปรายซ้ำ
> **Scope:** FULL variant standard; STANDARD/LEAN: LDs ใส่ใน 00_OVERVIEW §0.8 (Open Questions/LD) + Scope Lock ใน §0.11 แทน

---

## §7.0 Scope Lock (Imported from BRD §3.4) ⭐ v6 — IMMUTABLE

> ข้อยืนยันจากใบเซ็นลูกค้า — ห้าม override ตลอด pack และตลอด chain ปลายน้ำ (HTML/Test/Dev)
> ถ้า spec ใดใน pack ขัดกับ LOCK → LOCK ชนะเสมอ

| LOCK-ID | ข้อยืนยัน | อ้างเอกสาร | สถานะใน FRD |
|---|---|---|---|
| LOCK-01 | ... | ENH-SO-xxxx ข้อ 3 | ✅ สอดคล้อง |

- Scope Lock Ref: [เลขใบเซ็น + วันที่] / "N/A — standalone (งานไม่ผ่าน chain)"
- Drift พบระหว่างเขียน FRD (ชั้นที่ 3): [รายการ + OQ-XX] / ไม่มี



## §7.1 Locked Decisions (LD)

### LD-01: Use optimistic locking, not pessimistic
- **Date:** 2026-05-18
- **Context:** EC-01 concurrent approval scenario
- **Options considered:**
  - A) Pessimistic lock (SELECT FOR UPDATE)
  - B) Optimistic lock (`version` column + retry)
  - C) Last-write-wins (no protection)
- **Decision:** B — Optimistic lock with `version` column
- **Rationale:** Approval contention is rare; pessimistic lock penalizes 99% of cases for 1% conflict
- **Implications:**
  - 04_DB: add `version` column to T_payroll
  - 02_API: PUT/PATCH require `If-Match` header
  - 06_TESTS: TC-CC-01 verifies 409 on conflict
- **Reversibility:** MEDIUM — would require DB migration + API contract change

---

### LD-02: Engine ENG-005 register CUBIC at Phase 2 (not this sprint)
- **Date:** 2026-05-18
- **Context:** payroll-calculation-engine reuse potential
- **Options:**
  - A) Register now (this sprint) — slower delivery
  - B) Build scope-local first, register Phase 2 when 2nd feature confirms reuse
- **Decision:** B — scope-local now, register Phase 2
- **Rationale:** Avoid premature abstraction; confirm reuse pattern with F-XX (planned)
- **Implications:**
  - 03_LOGIC §3.2: status = DRAFT
  - 07_LD-XX (Phase 2): register decision LD
  - Migration plan: extract to CUBIC Registry, update F-04 to use registered ID
- **Owner:** Architect team
- **Reversibility:** EASY — just register later

---

### LD-03: Use ENG-006 (existing tax-rule-applier) instead of building new
- **Date:** 2026-05-18
- **Context:** Tax calculation logic
- **Options:**
  - A) Build new (custom for payroll)
  - B) Reuse ENG-006 from F-09 (Tax Reporting feature)
- **Decision:** B — Reuse ENG-006
- **Rationale:** Single source of truth for Thai tax rules; updates propagate automatically
- **Implications:**
  - 03_LOGIC §3.2 ENG-006 status = EXISTING
  - Add F-04 to ENG-006 "Used by features" list
- **Reversibility:** EASY

---

## §7.2 Convention Deviations

> ถ้า FRD นี้ deviate จาก `knowledge/conventions.md` → record ที่นี่พร้อมเหตุผล

### CD-01: [None — fully compliant]

ตัวอย่างถ้ามี deviation:

### CD-XX: Use POST /payrolls/:id/submit instead of PATCH
- **Convention default:** PATCH for partial state update
- **Deviation:** POST custom action
- **Reason:** Semantic clarity — "submit" is an action, not a property update
- **Approved by:** Tech Lead (2026-05-18)
- **Apply to:** F-XX-API-05 only (other endpoints follow convention)

---

## §7.3 Open Questions Promoted from 00_OVERVIEW

> เมื่อ OQ ใน 00_OVERVIEW ถูก resolved → move ที่นี่เป็น LD

[None pending]

---

## §7.4 Architecture Tradeoffs Acknowledged

### AT-01: PostgreSQL RLS over application-level filtering
- **Tradeoff:** Performance hit (~5%) vs. security guarantee
- **Accepted:** YES (CUBE ERP standard — Phase 2 lockup)
- **Mitigation:** Index optimization + connection pooling tuned

### AT-02: Synchronous engine calls vs. async queue
- **Tradeoff:** Latency (sync ~800ms) vs. complexity (async needs job tracking)
- **Accepted:** Sync for V1
- **Re-evaluate:** When latency > 2s sustained (load testing trigger)

---

## §7.5 Decisions Deferred to Implementation

> Items that don't block FRD signoff but need decision during dev

| Item | Owner | Deadline |
|---|---|---|
| Choose JSON field validation library (zod / yup / joi) | Tech Lead | Sprint planning |
| Cache strategy (Redis TTL value) | DevOps | Pre-deploy |
| Monitoring alert thresholds | DevOps + PM | Pre-deploy |

---

## §7.6 References

- **Convention source:** `knowledge/conventions.md`
- **CUBIC Registry policy:** `references/cubic-schema-templates.md`
- **Edge case origins:** `references/edge-case-probes.md`
- **Related FRDs:** F-09 Tax Reporting (shares ENG-006)
