# 00_OVERVIEW — F-TAX ทะเบียนรหัสภาษี (Tax Code Master)

> **Audience:** All roles (PM, BA, FE, BE, QA, DBA)
> **Purpose:** Document Control + Scope + Roles + Dependencies + Coverage Manifest + Scope Lock + Open Questions
> **Mode:** HTML-first / Reverse Mode (frd-generator-v6 v6.1) — layout สกัด+ตรวจจากหน้าจอจริง `f-taxcode.html` (as-built · ผ่าน qc-ux + qc-coverage + E2E 42/42)

---

## §0.1 Document Control

| Field | Value |
|---|---|
| **Feature ID** | F-TAX |
| **Feature Name** | ทะเบียนรหัสภาษี (Tax Code Master) |
| **Feature Code** | F-TAX (Master Data — Accounting/System-wide) |
| **Module** | Master Data (per HTML sidebar) · เจ้าของเชิงบัญชี = Accounting (ดู OQ-TAX-05) |
| **Variant** | **STANDARD (7 files)** |
| **Status** | APPROVED (with documented residual OQs) |
| **FRD Version** | 1.0 (2026-08-10) |
| **Generator** | frd-generator-v6 (v6.1 HTML-first / Reverse Mode) |
| **Source Brief** | PREBRIEF_F-TAX_Tax-Code.md (v1, 2026-08-09) + FUNCTION_CHECKLIST_F-TAX (FN-01..24, FN-40/90/92/93) |
| **Source BRD** | BRD_F-TAX_Tax-Code.md (BRD-F-TAX-001, status: APPROVED, 2026-08-10) |
| **Source HTML (SoT)** | `f-taxcode.html` (as-built, html-generator-v8) |
| **Author** | Sales Lane BA |
| **Reviewers** | Accounting owner, PM/BA, Tech Lead, QA Lead |

**Variant Fallback rationale (from BRD — no Brief §3.4 Generator Hints):**
`pages = 6` (§19 Screen Inventory) · `states = 3` (draft/active/inactive, §8) · `approval = NO` (LOCK-DOA-NULL) · `money = simple` (rate 0–100, no complex calc engine at this feature — VAT/WHT calc happens downstream). → not LEAN (pages>2), not FULL (states<4, no approval, no Engine Management §13 Phase 4 = none) → **STANDARD**.

---

## §0.2 Revision History

| Version | Date | Author | Changes |
|---|---|---|---|
| 1.0 | 2026-08-10 | Sales Lane BA | Initial FRD generation (HTML-first Reverse Mode). Layout extracted+verified from `f-taxcode.html`. 5 residual OQs carried forward from BRD. |

---

## §0.3 Scope

### In Scope
- ทะเบียนรหัสภาษีกลาง: List + สร้าง / แก้ไข / ดูรายละเอียด (drawer view 3 tab: ภาพรวม / การใช้งาน / ประวัติ)
- ประเภทภาษี fix 3 ค่า: VAT / หัก ณ ที่จ่าย (WHT) / ยกเว้นภาษี
- อัตรา % 0–100 (ทศนิยม 2 ตำแหน่ง — ดู OQ-TAX-RATE-PREC) · auto-code เมื่อเว้นรหัสว่าง (VATxx/WHTxx/TAXxx)
- สถานะ 3 ค่าเปลี่ยนอิสระทุกทิศ (draft/active/inactive) — เดี่ยว + bulk · ไม่มี gate/อนุมัติ
- **IR-TAX-01:** `used > 0` → ล็อกรหัส/อัตรา/ประเภท (UI disabled + server logic guard) — แก้ได้เฉพาะชื่อ/สถานะ
- ประเภทยกเว้นภาษี → อัตราล็อก 0 อัตโนมัติ (create/edit/import)
- List: search / filter (ประเภท+สถานะ) / stat 4 ใบกดกรองเร็ว / sort (อัตรา+used เชิงตัวเลข) / pagination (pageSize 8)
- นำเข้า CSV (template + preview รายแถว + สถานะในไฟล์ + 6 error codes) · ส่งออก CSV (ตาม filter, BOM)
- ลบแบบ bulk เท่านั้น (ผ่าน confirm) — `used > 0` ถูกข้าม
- Audit ผู้สร้าง/ผู้แก้ + เวลา (tab ประวัติ)
- Lookup contract สำหรับ downstream (combobox เห็นเฉพาะ status=active)

### Out of Scope
- ❌ แก้ รหัส/อัตรา/ประเภท ของตัวที่ถูกใช้แล้ว — reason: IR-TAX-01 (สร้างรหัสใหม่ + ปิดตัวเก่าแทน)
- ❌ ช่วงเวลาบังคับใช้อัตรา (effective date / validity period) — reason: คงเป็น **OQ-TAX-02** (open)
- ❌ ผูกเลขบัญชี GL ในหน้านี้ — reason: เป็นงาน GL Posting Setup (LOCK-NO-GL)
- ❌ เพิ่ม/แก้ประเภทภาษี — reason: fix 3 ค่า (LOCK-TYPE-3)
- ❌ ลบรายตัว / ลบตัวที่ถูกใช้ — reason: LOCK-BULK-DEL + BR-05
- ❌ ส่งอนุมัติ / สายอนุมัติ — reason: LOCK-DOA-NULL (DOA placeholder 4 fields = null)
- ❌ NOTIF emit event — reason: LOCK-NO-NOTIF (กระดิ่ง = placeholder) · icon/avatar หน้ารหัสใน list · ข้อความอธิบายคอลัมน์ในจอนำเข้า

### Out of Scope (mark from Phase 2.5 skipped/deferred probes)
- Real `used` counter sync จากสินค้า+เอกสาร → deferred เป็น **OQ-TAX-04** (bulk-delete guard พึ่งตัวเลขนี้)
- Role-gate จริง (RBAC ต่อ action) → deferred เป็น **OQ-TAX-06** (mock user เปิดหมด)

---

## §0.4 Roles & Responsibilities (COSO)

| Role | Person/Team | Responsibilities |
|---|---|---|
| **Maker** | ผู้ดูแลทะเบียนภาษี (ทีมบัญชี) | สร้าง/แก้ไข/เปลี่ยนสถานะ/นำเข้า/ส่งออก/ลบ bulk |
| **Checker** | — (N/A) | ไม่มีขั้นตรวจ — master maintenance เชิง config |
| **Approver** | — (N/A) | **LOCK-DOA-NULL** — ไม่มีสายอนุมัติทุก step |
| **Owner** | Accounting | เจ้าของ master + รับผิดชอบความถูกต้องเชิงบัญชี downstream |
| **Consumer (read-only)** | Sales / Item Master / เอกสารซื้อ-ขาย | เห็นเฉพาะ status=active ผ่าน lookup (BR-07) |

> COSO: Approver = N/A ทุก step (LOCK-DOA-NULL) · System enforce validation + IR-TAX-01 guard · ไม่มี approval → SoD ไม่ applicable [AI-DEFAULT ← BRD §5]
> รายละเอียดต่อ workflow → ดู `01_UI.md §1.3 Journey` + `05_RULES.md §5.2 State Machine`

---

## §0.5 Dependencies

### Upstream (this feature depends on)
| Dependency | Type | Source |
|---|---|---|
| — (master ต้นน้ำ) | — | ไม่มี upstream — ข้อมูลมาจากการ maintain โดยทีมบัญชี + seed อัตราภาษีไทยมาตรฐาน |

### Downstream (features that depend on this — จาก BRD §12.1)
| Consumer | What it uses |
|---|---|
| Item Master (กลุ่มภาษี) | soft ref `code` + status (เฉพาะ active) — ดู 02_API §2.X Cross-Module + F-TAX-API-10 lookup |
| เอกสารขาย/ซื้อ (QT/SO/INV/PR/PO) | `rate` % → B2 line editor คำนวณ VAT/WHT ท้ายบิล (IR-TAX-01 คุ้มครองบิลเก่า) |
| GL Posting Setup (Accounting) | soft ref `code` → map เข้าบัญชี GL (ที่โมดูลบัญชี — ทะเบียนนี้ไม่ถือเลขบัญชี) |
| DOA / NOTIF | — (ไม่มีสาย + ไม่ emit — LOCK-DOA-NULL / LOCK-NO-NOTIF) |

### External
| Service | Purpose |
|---|---|
| Policy Center (future) | RBAC role-gate (OQ-TAX-06) + DOA placeholder wire |
| — | ไม่มี payment gateway / 3rd-party integration |

---

## §0.6 Stack & Architecture

| Layer | Technology |
|---|---|
| Frontend | SPA (vanilla per prototype; production = React/Next per platform) — single hash route `#/tax-codes`, overlay drawer/modal |
| API | Node.js / Strapi (REST `/api/v1/tax-codes`) |
| Database | PostgreSQL (RLS multi-tenant per platform standard) |
| Engine layer | ไม่มี CUBIC engine ใน feature นี้ (ดู 03_LOGIC §3.2) |
| Auth | JWT + role-based (role-gate deferred → OQ-TAX-06) |

---

## §0.7 Multi-Tenant & Security Context

- [x] Multi-tenant feature: YES (platform RLS standard) — 1 ERP = 1 company master
- [x] PII data involved: **NO** (ไม่มี PII field — ดู 04_DB §4.2/§4.6)
- [ ] Financial data: partial — เป็น "นิยามอัตรา" ที่ downstream ใช้คำนวณเงิน (ไม่ใช่ยอดเงินจริงในตารางนี้)
- [x] Audit log required: YES (created/updated by+at + mutation log)

**Security Bible domains applied:** Access Control (RBAC — deferred), Audit Trail, Data Integrity (unique + IR-TAX-01 guard), Input Validation — ดู `05_RULES.md §5.7`. Preset = **P3 Master Data** [AI-DEFAULT ← BRD §16.1].

### §0.7.1 Data Classification Summary
Highest classification level ที่ feature นี้แตะ:
- [ ] Has Restricted fields
- [ ] Has Confidential fields
- [x] **Internal only (default)** — code/name/rate/category/status/used/audit = Internal
- [ ] Public-facing data

**Linkage:** ไม่มี Restricted/Confidential field → ไม่ต้อง register Restricted Resources. (ถ้าต่อไปนับ `used` จริงจากเอกสารการเงิน — ทบทวน classification ตอน OQ-TAX-04 resolve.)

---

## §0.8 Open Questions

| ID | Question | Blocking? | Owner |
|---|---|---|---|
| OQ-TAX-02 | ไม่ทำ effective date/validity period — ใช้ "สร้างรหัสใหม่+ปิดตัวเก่า" พอมั้ยสำหรับ CUBE | NO (pin — คงเปิด) | Strike |
| OQ-TAX-03 | WHT scope — master กลางรวม WHT ตั้งแต่แรก (เลน Sales ใช้ VAT ก่อน) ยืนยัน scope | NO (pin) | Strike |
| OQ-TAX-04 | `used` เป็น mock — ของจริงต้องนับจากสินค้า+เอกสารทุกใบ · กระทบ bulk-delete guard (EC-A7 ข้อมูลสูญหาย) | **YES** (ก่อนเปิดพึ่งตัวเลข used จริง) | FRD/BE |
| OQ-TAX-05 | ตำแหน่งเมนู: HTML วางใต้ "Master Data"; Central Plan/PREBRIEF = Accounting — ยืนยัน navigation | NO | PM/BA |
| OQ-TAX-06 | Role-gate จริง (ใครสร้าง/แก้/นำเข้า) — mock เปิดหมด | NO (deferred) | FRD/Policy Center |
| OQ-TAX-RATE-PREC | rate precision — FRD ตั้ง `numeric(5,2)` (2 ทศนิยม) เป็น [AI-DEFAULT ← BRD §10 EC-A5] · ยืนยัน 2 ตำแหน่งพอมั้ย | NO | BA/BE |
| OQ-TAX-IMPORT-PARSE | CSV import จริง: validate header/encoding/คอลัมน์สลับ (mock ข้ามขั้นนี้) — parser จริงต้องทำ (EC-A1) | NO | BE |
| OQ-TAX-CONCURRENCY | 2 คนสร้างรหัสเดียวกันพร้อมกัน (EC-A3) — [AI-DEFAULT] server-side case-insensitive unique constraint → 409 · ยืนยัน | NO | BE |

> **[AI-DEFAULT] ที่ carry จาก BRD:** D-2.3 (KPI target), role-gate deferred, COSO Approver=N/A, Security preset P3.
> **[AI-DEFAULT] ที่ FRD เพิ่ม (Phase 2.5 Lane Mode — conservative):** rate=numeric(5,2), case-insensitive unique constraint + 409 on concurrent dup, Idempotency-Key ทุก mutation, optimistic lock (`version`/If-Match) บน PUT. ทุกข้อ tag `[AI-DEFAULT]` ที่ 05_RULES/02_API/04_DB.

---

## §0.9 Glossary

| Term | Definition |
|---|---|
| IR-TAX-01 | Immutability-on-use rule: `used > 0` → ล็อกรหัส/อัตรา/ประเภท (แก้ได้เฉพาะชื่อ/สถานะ) |
| `used` (used_count) | จำนวนสินค้า/เอกสารที่อ้างรหัสนี้ — **mock ปัจจุบัน**, ของจริงต้อง sync (OQ-TAX-04) |
| soft reference | ปลายทางเก็บแค่ `code` (string) ไม่มี FK cascade |
| exempt | ประเภท "ยกเว้นภาษี" — rate ล็อก 0 เสมอ |
| auto-code | สร้างรหัสอัตโนมัติเมื่อเว้นว่าง: VATxx / WHTxx / TAXxx ตามประเภท |
| 6 error codes (import) | REQUIRED / BAD_TYPE / RATE_INVALID / EXEMPT_RATE / BAD_STATUS / CODE_DUPLICATE |

---

## §0.10 Pack Navigation

| File | Audience | Purpose |
|---|---|---|
| 00_OVERVIEW.md | All | Meta + scope + coverage + scope lock |
| 01_UI.md | FE dev | Layout Decision Log + Pages + Components + Journey (route/pattern สกัดจาก HTML) |
| 02_API.md | BE dev (HTTP) | API contracts + Cross-Module Contract |
| 03_LOGIC.md | BE dev (logic) | Functions + Trace (no engines) |
| 04_DB.md | DBA / BE | T_tax_code + Fields + Classification |
| 05_RULES.md | BE + QA | Business Rules + State Machine + Edge Cases + Error Catalog + Security |
| 06_TESTS.md | QA | Acceptance + DoD + Cross-Module cases (expected text verbatim จาก HTML) |

> STANDARD variant: ไม่มี 07_LOCKED_DECISIONS/INDEX — Scope Lock อยู่ที่ §0.11 (ด้านล่าง)

---

## §0.11 Scope Lock (imported from BRD §3.4) ⭐ — IMMUTABLE

> Scope Lock Ref: **N/A — ไม่มีใบเซ็นทางการ (Reverse Mode)**; LOCK สกัดจาก "มติ + STD" ใน PREBRIEF และถือเป็น Locked Decisions ที่ห้าม override ตลอด chain (HTML/Test/Dev).
> ถ้า spec ใดใน pack ขัด LOCK → LOCK ชนะเสมอ.

| LOCK-ID | ข้อยืนยัน | อ้าง | สถานะใน FRD |
|---|---|---|---|
| **LOCK-IR-TAX-01** | `used > 0` → ล็อกรหัส/อัตรา/ประเภท (UI + server guard) — แก้ได้เฉพาะชื่อ/สถานะ | BR-04 | ✅ สอดคล้อง (02_API-04 guard · 03_FN-03 · 05_RULES BR-04) |
| **LOCK-EXEMPT-0** | ยกเว้นภาษี → rate = 0 เสมอ (UI + logic + import validate) | BR-03 | ✅ (03_FN-04 · 04_DB CHECK · 05_RULES BR-03) |
| **LOCK-TYPE-3** | ประเภท fix 3 ค่า (VAT/WHT/exempt) — ห้ามเพิ่ม/แก้ | แผน | ✅ (enum constant กลาง · 04_DB CHECK) |
| **LOCK-NO-GL** | ไม่เก็บเลขบัญชี GL — mapping ที่ GL Posting Setup | BR-09 | ✅ (ไม่มี field/endpoint GL) |
| **LOCK-DOA-NULL** | ไม่มีสายอนุมัติ — DOA placeholder 4 fields = null | OB-4 | ✅ (04_DB approver_role/approved_by/approved_at/approval_chain = null) |
| **LOCK-NO-NOTIF** | ไม่ emit event เอง (กระดิ่ง placeholder) | OB-5 | ✅ (ไม่มี event emit ใน 03_LOGIC) |
| **LOCK-STATUS-FREE** | สถานะ 3 ค่าเปลี่ยนอิสระทุกทิศ ไม่มี gate/อนุมัติ | BR-06 | ✅ (05_RULES §5.2 free transitions) |
| **LOCK-SOFT-REF** | ปลายทางเก็บแค่ code (soft ref) · เลือกได้เฉพาะ active | BR-07 | ✅ (02_API-10 lookup filter active · no FK cascade) |
| **LOCK-BULK-DEL** | ไม่มีลบเดี่ยว — ลบ bulk ผ่าน confirm เท่านั้น · `used>0` ข้าม | BR-05 | ✅ (02_API-07 bulk-delete only · 03_FN-07 skip used>0) |

**Drift พบระหว่างเขียน FRD (ชั้นที่ 3):** ไม่มี scope เกิน LOCK. Module placement (Master Data vs Accounting) ยัง open = OQ-TAX-05 (ไม่ resolve เงียบ).

---

## §0.12 Coverage Manifest ⭐ (กัน requirement หล่น BRD→FRD)

### Stories (BRD §7)
| BRD Ref | Requirement (ย่อ) | อยู่ที่ใน Pack |
|---|---|---|
| §7 S-01 | สร้างรหัสภาษี (drawer เดียว, auto-code, ทศนิยม, เลือกสถานะ) | 01_UI P-02 · 02_API-02 · 03_FN-01/FN-02/FN-04 · 05 BR-01/02 · 06 AT-01/AT-02 |
| §7 S-02 | สร้างยกเว้นภาษี → rate ล็อก 0 | 01_UI P-02 · 03_FN-04 · 05 BR-03 · 06 AT-03 |
| §7 S-03 | แก้ตัว used=0 (แก้ได้ทุก field) | 01_UI P-03 · 02_API-04 · 03_FN-03 · 06 AT-04 |
| §7 S-04 | แก้ตัว used>0 (ล็อก 3 field + guard) | 01_UI P-03 · 02_API-04 · 03_FN-03 · 05 BR-04 · 06 AT-05/AT-06 |
| §7 S-05 | เปลี่ยนสถานะอิสระ (เดี่ยว/bulk) | 01_UI P-04 · 02_API-05/API-06 · 03_FN-06 · 05 BR-06/§5.2 · 06 AT-07/AT-08 |
| §7 S-06 | ลบ bulk (used>0 ข้าม + toast) | 01_UI P-06 · 02_API-07 · 03_FN-07 · 05 BR-05 · 06 AT-09/AT-10 |
| §7 S-07 | บล็อกเมื่อข้อมูลผิด (dup / rate invalid) | 02_API-02/04 · 03_FN-04 · 05 BR-01/02/VR-01..03 · 06 AT-11/AT-12 |
| §7 S-08 | นำเข้า CSV (preview + 6 codes + status ว่าง=ร่าง) | 01_UI P-05 · 02_API-08 · 03_FN-08/FN-09 · 05 §5.6 codes · 06 AT-13..AT-16 |
| §7 S-09 | ส่งออก CSV ตาม filter (BOM, 7 cols) | 01_UI P-01 · 02_API-09 · 03_FN-10 · 06 AT-17 |
| §7 S-11 | ดูการอ้างอิง + ประวัติ (tab) | 01_UI P-04 · 02_API-03 · 03_FN-11 · 05 BR-10 · 06 AT-18 |

### Rules (BRD §9)
| BRD Ref | Rule | อยู่ที่ |
|---|---|---|
| §9 BR-01 | รหัสห้ามซ้ำ (case-insensitive) | 05 BR-01 · 04_DB UNIQUE lower(code) · 06 AT-11 |
| §9 BR-02 | อัตรา 0–100 ทศนิยม | 05 BR-02 · 04_DB CHECK · 06 AT-12 |
| §9 BR-03 | exempt → rate 0 | 05 BR-03 · 04_DB CHECK · 06 AT-03 |
| §9 BR-04 | IR-TAX-01 lock-on-use | 05 BR-04 · 03_FN-03 · 06 AT-05/06 |
| §9 BR-05 | used>0 ลบไม่ได้ (bulk skip) | 05 BR-05 · 03_FN-07 · 06 AT-10 |
| §9 BR-06 | สถานะเปลี่ยนอิสระ | 05 BR-06/§5.2 · 06 AT-07 |
| §9 BR-07 | ปลายทางเลือกเฉพาะ active | 05 BR-07 · 02_API-10 · 06 XT-01 |
| §9 BR-08 | import รายแถว/status ว่าง=ร่าง | 05 BR-08 · 03_FN-08/09 · 06 AT-14/15 |
| §9 BR-09 | ไม่เก็บ GL | 05 BR-09 · 04_DB (no field) · 06 AT-19 (absence) |
| §9 BR-10 | audit who/when | 05 BR-10 · 04_DB audit cols · 06 AT-18 |

### Edges confirmed (BRD §10.1 ☑)
| BRD Ref | Edge | อยู่ที่ |
|---|---|---|
| §10.1 EC-01 | รหัสซ้ำต่างตัวพิมพ์ | 05 EC-01 · 06 AT-11 |
| §10.1 EC-02 | rate=120 (import) | 05 EC-02 · 06 AT-16 |
| §10.1 EC-03 | exempt + rate≠0 (import) | 05 EC-03 · 06 AT-16 |
| §10.1 EC-04 | rate ทศนิยม 0.75 | 05 EC-04 · 06 AT-15 |
| §10.1 EC-05 | import status ว่าง=draft | 05 EC-05 · 06 AT-14 |
| §10.1 EC-06 | bulk ลบผสม used>0/used=0 | 05 EC-06 · 06 AT-10 |
| §10.1 EC-07 | ฝืน submit ตัว used>0 | 05 EC-07 · 03_FN-03 · 06 AT-06 |
| §10.1 EC-08 | นำเข้าไฟล์ที่ไม่ได้เลือก | 05 EC-08 · 06 AT-13 |

**สรุป:** Stories 10/10 ✅ · Rules 10/10 ✅ · Edges confirmed 8/8 ✅ · ไม่มีที่ลง → OQ: **ไม่มี** (AI-pattern edges §10.2 → carry เป็น OQ-TAX-04/RATE-PREC/IMPORT-PARSE/CONCURRENCY ใน §0.8)
