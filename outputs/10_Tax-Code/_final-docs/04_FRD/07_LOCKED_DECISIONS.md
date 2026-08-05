# 07_LOCKED_DECISIONS — F-TAX Tax Code (รหัสภาษี)

> **Audience:** All roles
> **Purpose:** Scope Lock (immutable) + Locked Decisions + Convention deviations

---

## §7.0 Scope Lock (Imported from BRD §3.4) ⭐ — IMMUTABLE

> ข้อยืนยันจาก `AI_DEFAULTS.md` (LOCKED) — ห้าม override ตลอด pack และ chain ปลายน้ำ (HTML/Test/Dev). ถ้า spec ใดขัด LOCK → LOCK ชนะ.

| LOCK-ID | ข้อยืนยัน | อ้างอิง | สถานะใน FRD |
|---|---|---|---|
| LOCK-01 | Tax Code แยกตามบริษัท + รหัส unique case-insensitive ในบริษัทเดียว | AI-DEFAULT #1 / BR-01 | ✅ 04_DB UQ(company_id,lower(code)) · 05 BR-TAX-01 |
| LOCK-02 | UI ทำงานใน current-company context — เปลี่ยนบริษัทในฟอร์มไม่ได้ | AI-DEFAULT #2 | ✅ 01_UI company chip read-only · 04_DB RLS · 05 BR-TAX-15 |
| LOCK-03 | GL lookup รับเฉพาะบัญชีบริษัทปัจจุบัน `status=active` + `posting_allowed=true` | AI-DEFAULT #3 | ✅ 03_LOGIC ENG-03 · 05 BR-TAX-06 |
| LOCK-04 | VAT รองรับ STANDARD/ZERO_RATED/EXEMPT + ทิศ ขาย/ซื้อ/ทั้งคู่ + `vat_report_category` | AI-DEFAULT #4 | ✅ 03 FN-14 · 05 BR-TAX-10 |
| LOCK-05 | WHT เก็บ income category; แบบ ภ.ง.ด. resolve ที่ payment/reporting ไม่ hardcode ที่ Tax Code | AI-DEFAULT #5 | ✅ 04_DB report_mapping_rule · 05 BR-TAX-11 |
| LOCK-06 | AP เสนอ WHT ได้ แต่ Payment Voucher = จุดยืนยันหัก; WHT report อ่านจาก payment result | AI-DEFAULT #6 | ✅ 02 §2.X · 03 ENG-01 advisory · 05 BR-TAX-12 · 06 XT-03 |
| LOCK-07 | picker ใช้วันที่เอกสาร + บันทึก immutable tax snapshot ลงเอกสาร | AI-DEFAULT #7 | ✅ 03 ENG-01/ENG-02 · 05 BR-TAX-08 |
| LOCK-08 | ไม่มี hard delete — deactivate/archive + append-only audit | AI-DEFAULT #8 / BR-05 | ✅ 02 ไม่มี DELETE · 04_DB append-only · 05 BR-TAX-05 |
| LOCK-09 | อัตราของรหัสที่ถูกใช้แล้วแก้ไม่ได้ — เปลี่ยน = replacement code + lineage | AI-DEFAULT #9 / BR-02 | ✅ 03 FN-03 lock / FN-08 · 05 BR-TAX-02 |
| LOCK-10 | permissions ชุด `tax_code.*` 6 สิทธิ์ | AI-DEFAULT #10 | ✅ 02 auth · 05 §5.3 |
| LOCK-11 | route prod `/accounting/setup/tax-codes` | AI-DEFAULT #11 | ✅ 01_UI §1.0/§1.1 (prototype `#/accounting/setup/tax-codes`) |
| LOCK-12 | WHT GL picker filter เฉพาะ `WHT_PAYABLE` (FLAG-1 RESOLVED) | DECISION_LOG C2/F1 | ✅ 03 ENG-03 expectedRole · 04_DB gl_wht · 05 BR-TAX-07/VR09 · 06 AC-05b |

- **Scope Lock Ref:** `AI_DEFAULTS.md` (F-TAX) — LOCKED, 2026-08-05 (ไม่มีเลขใบเซ็น chain — approved AI defaults).
- **Drift พบระหว่างเขียน FRD (ชั้นที่ 3):** ไม่มี scope creep. ทุก API/หน้า/rule อยู่ในขอบเขต LOCK. Cosmetic mismatch (`<title>` legacy "CUBE NATIVE") = OQ-11 (raise, ไม่แก้ spec — R14).

---

## §7.1 Locked Decisions (LD)

### LD-01: Optimistic locking (version) ไม่ใช่ pessimistic
- **Date:** 2026-08-05
- **Context:** EC-15 concurrent edit/deactivate (BRD §14.3 E15 บอกให้มี lock)
- **Options:** A) pessimistic (SELECT FOR UPDATE) · B) optimistic (`version`/`If-Match` → 409)
- **Decision:** B — optimistic (`[AI-DEFAULT]`)
- **Rationale:** master data contention หายาก; pessimistic ลงโทษเคสปกติ
- **Implications:** 04_DB `version` column · 02_API `If-Match` + 409 ERR_STALE_DATA · 06 TC-CC-02
- **Reversibility:** MEDIUM · **Open:** OQ-9 (confirm contract)

### LD-02: Engines ENG-01/02/03 register CUBIC ตอน dev hand-off (status DRAFT)
- **Date:** 2026-08-05
- **Context:** tax-snapshot-builder / effective-date-resolver / gl-role-validator = reusable ข้าม consumer
- **Decision:** สร้าง scope-local (DRAFT) ก่อน → register CUBIC เมื่อ consumer doc แรก confirm reuse
- **Rationale:** avoid premature abstraction; consumers ยังเป็น External Contract (OQ-4)
- **Implications:** 03_LOGIC §3.2 status=DRAFT · CUBIC register ใน DoD (06 §6.4)
- **Reversibility:** EASY

### LD-03: Idempotency-Key required บนทุก mutation
- **Date:** 2026-08-05
- **Context:** PR-7 (create/activate/deactivate/replacement retry safety); BRD ไม่ระบุ
- **Decision:** require `Idempotency-Key`, TTL 24h → 409 dup (`[AI-DEFAULT]`)
- **Rationale:** ป้องกัน double-submit / network retry (PR-4) — spec ปลอดภัยไว้ก่อน
- **Implications:** 02_API §2.3 · 05_RULES §5.5 · **Open:** OQ-8

### LD-04: WHT GL constrained = WHT_PAYABLE เท่านั้น (FLAG-1 RESOLVED)
- **Date:** 2026-08-05
- **Context:** DECISION_LOG C2/FLAG-1 — msg #1571 กำกวม ("เหมือนตอนนี้แสดงทุก GL") vs HTML filter WHT_PAYABLE
- **Decision:** WHT picker filter `WHT_PAYABLE` เท่านั้น (mirror VAT_SALE/VAT_PURCHASE) — user resolved 2026-08-05
- **Rationale:** สอดคล้อง AI-DEFAULT #3 + HTML L2581/2609; posting WHT ค้างจ่ายถูกต้อง
- **Implications:** 03 ENG-03 · 04_DB gl_wht · 05 BR-TAX-07/VR09 · 06 AC-05b — **= LOCK-12 immutable**
- **Reversibility:** LOCKED (ห้าม override)

### LD-05: Draft ไม่มี auto-expiry
- **Date:** 2026-08-05
- **Context:** PR-6 draft/resume — master data ไม่ใช่ wizard
- **Decision:** draft persist indefinitely; ไม่มี cleanup job (`[AI-DEFAULT]`)
- **Rationale:** งานค้างของ accountant ไม่ควรหาย; volume ต่ำ
- **Implications:** ไม่มี draft expiry logic · **Open:** OQ-10

---

## §7.2 Convention Deviations

### CD-01: ID prefix ใช้ `F-TAX-` (ไม่ใช่ `F-NN-`)
- **Convention default:** `F-XX` (2-digit)
- **Deviation:** Feature ID = `F-TAX` (ตาม BRD — master data ไม่มีเลข 2 หลัก)
- **Reason:** สืบทอดจาก BRD-ACC-TAX-001 / AI_DEFAULTS (Feature ID = F-TAX)
- **Apply to:** ทุก ID ใน pack (`F-TAX-API-NN`, `F-TAX-FN-NN`)

### CD-02: Multi-tenant key = `company_id` (ไม่ใช่ `tenant_id`)
- **Convention default:** template ใช้ `tenant_id` / `X-Tenant-Id`
- **Deviation:** ใช้ `company_id` / `X-Company-Id`
- **Reason:** domain = current-company context (LOCK-02); ERP multi-company semantic
- **Apply to:** 04_DB RLS, 02_API headers

### CD-03: Preset seed function (FN-15) ไม่ถูกเรียกจาก runtime API
- **Convention default:** ทุก Function trace ไป API (R8)
- **Deviation:** FN-15 seedThaiPresets = migration/seed job (04_DB §4.4), ไม่ใช่ orphan
- **Reason:** R16 seed one-time; ไม่ควร expose เป็น runtime endpoint
- **Approved:** BA (documented — ไม่นับ orphan ใน R8 เพราะมี invoked-by ชัด = seed job)

---

## §7.3 Open Questions Promoted from 00_OVERVIEW
> เมื่อ OQ resolved → move มาที่นี่เป็น LD. ปัจจุบันค้าง: OQ-3, OQ-4, OQ-5, OQ-6, OQ-7, OQ-8, OQ-9, OQ-10, OQ-11 (ดู 00_OVERVIEW §0.8). OQ-1/OQ-2 = resolved out-of-scope.

---

## §7.4 Architecture Tradeoffs Acknowledged

### AT-01: PostgreSQL RLS (company) over app-level filtering
- **Tradeoff:** perf ~5% vs security guarantee (cross-company E18)
- **Accepted:** YES (CUBE ERP standard)

### AT-02: Snapshot ที่ consumer เก็บ (denormalized immutable) over live master read
- **Tradeoff:** duplication vs ประวัติภาษีคงที่ (audit ผ่าน)
- **Accepted:** YES — statutory requirement (R08/LOCK-07); rebuild รายงานจาก snapshot ไม่ใช่ master

---

## §7.5 Decisions Deferred to Implementation

| Item | Owner | Deadline |
|---|---|---|
| GL-change-in-CoA behavior (E08 block/warn/re-bind) | Accounting + CoA owner | ก่อน dev validation (OQ-6, BLOCKING) |
| Audit/RBAC reuse vs สร้างใหม่ (System Module Registry) | Platform/Arch | Sprint planning (OQ-5) |
| Idempotency TTL exact value | Tech Lead | Pre-deploy (OQ-8) |
| SoD final model (second-person vs single accounting-admin) | Finance | ก่อน go-live (OQ-3) |

---

## §7.6 References
- **Scope Lock source:** `outputs/10_Tax-Code/00_CONTEXT/AI_DEFAULTS.md` + `DECISION_LOG.md` (FLAG-1)
- **Convention:** `knowledge/conventions.md`
- **CUBIC Registry:** `references/cubic-schema-templates.md`
- **Related (downstream, External Contract):** SO/AR, PO/AP, Payment Voucher, VAT Return (ภ.พ.30), WHT report (ภ.ง.ด.3/53)
