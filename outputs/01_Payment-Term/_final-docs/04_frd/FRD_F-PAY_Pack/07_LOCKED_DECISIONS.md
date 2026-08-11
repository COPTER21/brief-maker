# 07_LOCKED_DECISIONS — F-PAY Payment Term (เงื่อนไขการชำระเงิน)

> **Audience:** All roles
> **Purpose:** Scope Lock (imported) + Locked Decisions — ห้ามเปิดอภิปรายซ้ำ

---

## §7.0 Scope Lock (Imported from BRD §3.4 + SCOPE_LOCK.md) ⭐ IMMUTABLE

> ข้อยืนยันจากใบเซ็น/มติ — ห้าม override ตลอด pack และตลอด chain ปลายน้ำ (HTML/Test/Dev).
> **Conflict rule:** LOCK ชนะทุกกรณี. Ref: `00_CONTEXT/SCOPE_LOCK.md` + BRD §3.4.

| LOCK-ID | ข้อยืนยัน | อ้างเอกสาร | สถานะใน FRD |
|---|---|---|---|
| **LD-01** | payment term ที่ **PO/SO เท่านั้น** · **PR ไม่มี** · Quotation = ฝั่งขาย (proposal) | SCOPE_LOCK + D-08 | ✅ สอดคล้อง — use_in=7 (BR-06, 04_DB enum, 02_API validation) |
| **LD-02** | GRN/Ship trigger ตามประเภท: Prepay/Deposit รอชำระ · ที่เหลือ=ทันที | SCOPE_LOCK | ✅ ENG-PT-02 + BR-11 |
| **LD-05** | เปลี่ยน type หลัง approve เอกสารไม่ได้ (downstream) · Direct ไม่ผ่าน PR/PO/SO | SCOPE_LOCK | ✅ BR-12 + EC-03 (snapshot no retro) |
| **LD-08** | deposit % inherit + ปรับได้ที่ PO/SO | SCOPE_LOCK | ✅ 02_API cross-module (snapshot payload) |
| **LD-08b** | **Credit trigger = ทันที (locked)** — แก้ไม่ได้ | SCOPE_LOCK | ✅ BR-10 + FN-09 (lock badge, no dropdown) |
| **LD-09** | installment inherit + ปรับได้ · รวมต้อง 100% | SCOPE_LOCK | ✅ BR-04 + ENG-PT-01 |
| **LD-10** | Partial: GRN กำหนดยอดจ่ายต่อรอบ | SCOPE_LOCK | ✅ ENG-PT-02 (per-round unlock) |
| **LD-15** | Installment ≠ Partial (คนละประเภท) | SCOPE_LOCK | ✅ 2 type แยก (04_DB enum) |
| **VD-PDM** | สถานะ 3 ค่าอิสระ ไม่มีอนุมัติ · bulk ได้ · **ไม่มีลบเดี่ยว** · ตัด hint/field-help/panelInfo · **ไม่มี CSV** | เลน + มติ 2026-08-09 | ✅ §5.2 + BR-09 + 01_UI (no single-delete, no hint) |
| **Governance** | DOA null · NOTIF ไม่ emit · CI v8 Warm Light · Iron Rules #29/#94/#95/#96/#97 | SCOPE_LOCK | ✅ 00 §0.7 + 01_UI §1.0 + 04_DB (DOA null) |
| **Central Plan** | Soft-ref (snapshot, no FK cascade) · edges [config]→PO/AR Inv/AP Inv · append-only audit, soft archive, no hard delete | Central Plan v2 | ✅ 04_DB §4.3 + 02_API §2.X + BR-08 |

- **Scope Lock Ref:** `00_CONTEXT/SCOPE_LOCK.md` (สืบทอด PREBRIEF OB-1 + มติเลน + มติ 2026-08-09) + BRD §3.4 (2026-08-10).
- **Drift พบระหว่างเขียน FRD (ชั้นที่ 3):** **ไม่มี** — ทุก spec สอดคล้อง LOCK. จุด tension เดียว (PR ใน use_in) ถูกปิดโดย **D-08 (PR ถอด)** ก่อน FRD.

---

## §7.1 Locked Decisions (LD)

### LD-F-01: use_in = 7 เอกสาร — PR ถอด (D-08)
- **Date:** 2026-08-10 · **ผู้ตัดสิน:** PM/BA
- **Context:** source contradiction (OB-2/FN-10 มี PR vs LD-01/FN-40 ตัด PR) — OQ-PAY-08
- **Decision:** **ถอด PR** — payment term ไม่ผูกที่ PR (LD-01 + ERP standard) · use_in 8→7
- **Implications:** 04_DB enum (7 ค่า, ไม่มี pr) · 02_API validation ปฏิเสธ 'pr' · 05_RULES BR-06 · 06_TESTS AT-06 · UI ไม่แสดง PR checkbox · zero data impact (ไม่มี mock อ้าง PR)
- **Reversibility:** MEDIUM (ถ้ากลับมา = แก้ enum + UI + tests)

### LD-F-02: แก้ไขได้แม้ used>0 (ไม่ล็อกแบบ Tax Code)
- **Date:** 2026-08-10 · **ผู้ตัดสิน:** `[AI-DEFAULT AD-01]` — pending Strike (OQ-PAY-05)
- **Context:** ต่างจาก Tax Code ที่ล็อกเมื่อ used>0
- **Decision:** **แก้ได้ / ลบไม่ได้** เมื่อ used>0 — เพราะเอกสารปลายทาง snapshot ค่าแล้ว (ไม่ retro)
- **Options:** A) ล็อกแบบ Tax Code · **B) แก้ได้ (chosen)** — snapshot ป้องกันผลกระทบย้อนหลัง
- **Implications:** 03_LOGIC FN-02 (no edit lock) · BR-08 · 06 AT-09 · EC-03
- **Reversibility:** EASY (เพิ่ม guard ได้)

### LD-F-03: ENG-PT-01 / ENG-PT-02 = DRAFT → register CUBIC ที่ dev hand-off
- **Date:** 2026-08-10 · **Owner:** Architect (OQ-ENG-REG)
- **Context:** 2 engines reusable ข้าม feature (validate + downstream posting/trigger)
- **Decision:** build spec ที่ FRD (DRAFT), register CUBIC Registry ตอน hand-off — ห้ามเริ่ม Phase 4 ก่อน register
- **Implications:** 03_LOGIC §3.2 status=DRAFT · 06_TESTS DoD (register gate) · Global Engine IDs assigned at registration
- **Reversibility:** EASY

### LD-F-04: Optimistic lock + Idempotency (conservative default)
- **Date:** 2026-08-10 · **ผู้ตัดสิน:** `[AI-DEFAULT AD-04]` — Phase 2.5 probe (PR-1/PR-7) — pending OQ-PAY-CC-01
- **Context:** concurrency (2 admin ตั้ง default) + double-submit
- **Decision:** PUT/PATCH require If-Match (version) → 409 stale · POST require Idempotency-Key
- **Implications:** 02_API §2.3 · 04_DB `version` column · 05_RULES EC-01/EC-02 · TC-CC-01/TC-ID-01
- **Reversibility:** MEDIUM (API contract)

### LD-F-05: ส่วนลดจ่ายเร็ว = 1 ช่วง
- **Date:** 2026-08-10 · **ผู้ตัดสิน:** `[AI-DEFAULT AD-02]` — pending Strike (OQ-PAY-02)
- **Context:** SAP รองรับ 3 tiers
- **Decision:** 1 ช่วง (discount_pct + discount_days) — ตาม HTML as-built · ขยาย tier = เปลี่ยน logic (Phase 3, escalate ก่อน)
- **Reversibility:** MEDIUM

### LD-F-06: ไม่รองรับ multi-currency (THB สมมติ)
- **Date:** 2026-08-10 · **ผู้ตัดสิน:** `[AI-DEFAULT AD-03]`
- **Decision:** THB assumed — ไม่มี currency field · **Reversibility:** MEDIUM

---

## §7.2 Convention Deviations

### CD-01: Route model = single-view SPA + overlay (ไม่มี hash router)
- **Convention default:** list/detail/create มี hash route แยก
- **Deviation:** HTML prototype = single view + overlay (openDrawer/openModal) — ไม่มี URL routing
- **Reason:** HTML SoT as-built (gate-passed). 01_UI §1.0 บันทึก route (observed) = trigger + route (production) เสนอสำหรับระบบจริง 1:1
- **Approved by:** HTML gate (UX/Coverage/E2E) · **Apply to:** ทุกหน้า P-01..05

### CD-02: DELETE ทำผ่าน POST /bulk-delete (ไม่มี DELETE /:id)
- **Convention default:** DELETE /resource/:id (single)
- **Deviation:** ไม่มี single-delete — bulk เท่านั้น (POST) + guard used>0
- **Reason:** pattern เลน VD-PDM ("ไม่มีลบเดี่ยว") + soft-guard + confirm modal
- **Approved by:** SCOPE_LOCK · **Apply to:** F-PAY-API-07

---

## §7.3 Open Questions Promoted to LD
> เมื่อ OQ ปิด → move ที่นี่. ปัจจุบัน pending (ดู 00_OVERVIEW §0.8):
- OQ-PAY-04 (deposit VAT), OQ-PAY-07 (used def), OQ-PAY-02 (discount tier), OQ-PAY-CC-01 (concurrency), OQ-ENG-REG — ยังเปิด, ยังไม่ promote.

---

## §7.4 Architecture Tradeoffs Acknowledged

### AT-01: Soft-reference snapshot over FK cascade
- **Tradeoff:** ข้อมูล snapshot ซ้ำในเอกสารปลายทาง vs. integrity guarantee (แก้ master ไม่พังเอกสารเก่า)
- **Accepted:** YES (Central Plan LD-4C-02 — reuse Tax Code pattern)

### AT-02: use_in = text[] (array) over child table
- **Tradeoff:** query flexibility (GIN) vs. relational normalization
- **Accepted:** array (small fixed 7-value set) · child table = acceptable alternative (DBA discretion, 04_DB note)

### AT-03: Server-side validation mirror ของ mock UI
- **Tradeoff:** duplicate logic (UI + server) vs. security (C4 — client validation ไม่พอ)
- **Accepted:** YES — F-PAY-FN-03 mirror `submitTerm()` 7 validations

---

## §7.5 Decisions Deferred to Implementation
| Item | Owner | Deadline |
|---|---|---|
| นิยาม `used` precise (นับ draft ปลายทาง?) — **blocking delete guard** | FRD/BA (OQ-PAY-07) | ก่อน dev delete |
| Deposit VAT flow (Hook-2, Tax Code) — **blocking deposit GL** | Strike/บัญชี (OQ-PAY-04) | ก่อน dev deposit posting |
| ENG-PT-01/02 CUBIC registration | Architect (OQ-ENG-REG) | ก่อน Phase 4 |
| Cache strategy สำหรับ /active picker (Redis TTL) | DevOps | pre-deploy |

---

## §7.6 References
- **Scope Lock source:** `00_CONTEXT/SCOPE_LOCK.md` + BRD §3.4 + `AI_DEFAULTS.md` + `DECISION_LOG.md`
- **Central Plan:** `Central Plan v2/CENTRAL_PLAN_CORE_ERP.md`
- **CUBIC Registry:** ENG-PT-01, ENG-PT-02 (DRAFT)
- **Related:** Tax Code master (feature #3 — Hook-2 deposit VAT)
