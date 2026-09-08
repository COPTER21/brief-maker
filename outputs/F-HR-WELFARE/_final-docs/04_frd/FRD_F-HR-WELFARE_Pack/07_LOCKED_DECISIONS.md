# 07_LOCKED_DECISIONS — F-HR-WELFARE · Welfare (สวัสดิการ)

> **Audience:** All roles · **Purpose:** decisions ที่ debated + resolved — ห้ามเปิดซ้ำ.

---

## §7.0 Scope Lock (Imported from BRD §3.4) ⭐ IMMUTABLE

> ข้อยืนยันจาก HANDOFF §3 + PREBRIEF §0 (OB-1..7) — ห้าม override ตลอด pack + chain ปลายน้ำ. spec ใดขัด LOCK → LOCK ชนะ.

| LOCK-ID | ข้อยืนยัน | อ้างเอกสาร | สถานะใน FRD |
|---|---|---|---|
| **LK-1** | อนุมัติ = DOA `GET /doa/resolve` (slot picker · มติ 17 ส.ค.) — **ห้าม hardcode chain** | HANDOFF §3 · OB-4 | ✅ 02_API-11 · 03 FN-10/ENG-DOA · 05 BR-04/BR-DOA-2 |
| **LK-2** | **ไม่จ่ายเงินเอง** — Payroll/Expense จ่าย · Welfare = hook display-only | HANDOFF §3 · OB-3 | ✅ 00 NS-1 · 02_API §2.X · 04 request.pay · 05 BR (no pay action) |
| **LK-3** | policy/effective_date/company_scope = HR Configuration (#107) — **ไม่ทำหน้า config เอง** | HANDOFF §3 · OB-5 | ✅ 00 NS-4 · 02 (read /hr-config/resolve) · 04 company_scope |
| **LK-4** | soft reference LD-4C-02 (snapshot ชื่อ · **ไม่มี FK cascade**) | HANDOFF §3 · OB-1 | ✅ 04 employee_snapshot · 05 BR-10 |
| **LK-5** | audit **append-only** · RESTRICTED masking · no hard delete | HANDOFF §3 · OB-7 | ✅ 04 T_welfare_audit_log · 05 BR-07/BR-08 · §5.7 |
| **LK-6** | CSQ = **EC เท่านั้น** (ห้าม OC/DC-doc/SC) | HANDOFF §3 · OB-6 | ✅ 02 §2.X · 03 ENG-CSQ · 05 BR-09 |

- **Scope Lock Ref:** HANDOFF.md §3 (LK-1..6) + PREBRIEF §0 (OB-1..7) · Cube_Feature_List F102 (dep=OP✓ CL-0013 ผู้บริหาร แขวน 31 ส.ค.)
- **Drift พบระหว่างเขียน FRD (ชั้นที่ 3):** ไม่มี. reversal (OQ-WEL-01) + exposure display (OQ-WEL-03) = **authorized** (Decision Log · delegated PM/BA) — ไม่ใช่ drift.

---

## §7.1 Locked Decisions (LD)

### LD-01: reversal (กลับรายการ) = append-only correction (OQ-WEL-01)
- **Date:** 2026-09-08 · **Context:** แก้คำขอที่อนุมัติแล้ว (อาจส่งจ่ายแล้ว)
- **Options:** A) hard delete/edit · B) cancel เดิม + สร้างใหม่ · **C) reversal append-only** (D365/SAP reversal-document + negative offsetting entry)
- **Decision:** **C** — status='reversed', คงข้อมูลเดิม, คืนคงเหลือ, EC reverse, clawback flag (pay=sent), reason บังคับ, admin/manager เท่านั้น.
- **Rationale:** ไม่ทำลายรอยตรวจสอบ · ทุก financial reversal ต้องมี negative offset + reason (audit + payroll reconciliation).
- **Implications:** 04 request(+reverse fields) · 03 FN-14 · 05 BR-11/VR-11 · 02 API-15 · CSQ EC-reverse + NTF welfare_request_reversed. **ไม่ reintroduce real payout** (LK-2 คงอยู่).
- **Reversibility:** MEDIUM.

### LD-02: exposure = display-only, no soft-reserve (OQ-WEL-03)
- **Date:** 2026-09-08 · **Context:** คำขอ pending หลายใบบนสิทธิ์เดียวกัน
- **Options:** A) soft-reserve/lock โควตาระหว่างรออนุมัติ · **B) check-at-approval (FIX-02) + exposure display**
- **Decision:** **B** — จุดตัดสินจริง = ณ approval (hard re-check); ผู้อนุมัติเห็น pending demand ประกอบ (ไม่ล็อก).
- **Rationale:** soft-reserve สร้าง state กำกวม + เสี่ยง lock ค้าง · มาตรฐาน = ตัดสินที่จุด commit.
- **Implications:** 03 FN-16 · 05 BR-12/BR-DOA-5 · 02 API-16. **Reversibility:** EASY.

### LD-03: DOA = 2-step, no-limit, no exec path (A-WEL-03 / CL-0013)
- **Date:** 2026-09-08 · **Context:** สายอนุมัติคำขอใช้สิทธิ์
- **Decision:** default **2 ขั้น** (หัวหน้าสายงาน → HR สวัสดิการ) · **ไม่มีวงเงิน (no amount tier)** · **ไม่มี exec/จ่ายจริง** (FIX-03 one-step advance) · เลือก "คน" ในตำแหน่งจาก DOA กลาง (ไม่ hardcode).
- **Rationale:** สวัสดิการไม่ผูกจุดตัดยอดเงิน (ต่างจาก Expense threshold) · chain มาจาก DOA engine.
- **Implications:** DOA_BRIEF §3 matrix · 03 ENG-DOA · 05 BR-04/BR-DOA-1..8. **Owner ยืนยันรหัสสายจริง:** พี่เบิร์ด (CL-0013 ผู้บริหาร แขวน 31 ส.ค. — ถ้าบางประเภทต้องผ่านคนอื่น ให้แยก set). **Reversibility:** EASY (ตั้งที่ DOA กลาง).

### LD-04: ENG-WEL-01/02 register CUBIC ตอน hand-off (ไม่ block sprint)
- **Date:** 2026-09-08 · **Decision:** eligibility-resolver + balance-calculator = scope-local DRAFT ก่อน · register CUBIC ตอน dev hand-off. **Reversibility:** EASY.

### LD-05: recurring (PVD %) = F102 enroll / F065 deduct (OQ-WEL-02)
- **Date:** 2026-09-08 · **Decision:** F102 enroll/ประกาศสัดส่วน (claimable=false, ไม่ตัดยอด); การหักจริง = F065 (FIX-07). **Reversibility:** MEDIUM.

---

## §7.2 Convention Deviations
### CD-01: request_no = internal display id (ไม่ผ่าน doccfg)
- **Convention default:** เอกสารธุรกรรมมีเลขรันจาก ENG-DOC-NUM (doccfg).
- **Deviation:** Welfare ไม่มีเอกสารทางการ (NS-5) → request_no = 'REQ-2569-'+seq (ภายใน) · **ไม่ register doc_type**.
- **Reason:** master + light transaction (ไม่ใช่ Pattern Q) · ไม่มีเอกสารที่คนถือ.
- **Approved:** PREBRIEF §12 chip DOCCFG=— · STANDARD_BASELINE §3.

### CD-02: z-index tokens ที่ feature :root
- BASE-KIT ไม่กำหนด `--z-*` → feature กำหนด (sticky/backdrop/drawer/modal). คงไว้ (HANDOFF §5) — ห้ามลบตอน vibe.

---

## §7.3 Open Questions Promoted from 00_OVERVIEW
> เมื่อ resolve → move ที่นี่. ปัจจุบันค้าง (ดู 00 §0.8): **OQ-03** (Payroll/Expense hook contract · Phase B) · **OQ-04** (atomic re-check · `[AI-DEFAULT]`) · **OQ-05** (backend permission enforce · `[AI-DEFAULT]`) · OQ-01/02/06 · A-WEL-01/02/04/05.

---

## §7.4 Architecture Tradeoffs
- **AT-01:** balance = computed live (ไม่เก็บ table) — trade compute cost เพื่อ single source of truth + reversal คืนยอดฟรี. Accepted.
- **AT-02:** optimistic lock (version_lock) สำหรับ approve/reverse concurrency (OQ-04) — trade retry เพื่อ throughput. Accepted (re-eval ถ้า contention สูง).
- **AT-03:** PostgreSQL RLS multi-tenant + company_scope. Accepted (CUBE standard).

---

## §7.5 Deferred to Implementation
| Item | Owner | Deadline |
|---|---|---|
| Attachment ชนิด/ขนาด/virus-scan policy (EC-14) | Tech Lead/Security | Sprint |
| Payroll/Expense hook contract (A-WEL-02 · OQ-03) | Strike/Dev | Phase B |
| Atomic isolation level ของ re-check (OQ-04) | Dev | Pre-deploy |

---

## §7.6 References
- Convention: `knowledge/conventions.md` · CUBIC: `references/cubic-schema-templates.md`
- Declaration briefs: 5_DECLARATIONS/{DOA,NTF,CSQ}_BRIEF.md (Sync Read) · Decision Log: outputs/F-HR-WELFARE/_DECISION_LOG_OQ.md
- Related: F-DLG-001 (DOA) · F-CSQ-01 (CSQ) · F-NOTIFY (NOTIFY) · F065 Payroll · F101 Expense · #107 HR Config
