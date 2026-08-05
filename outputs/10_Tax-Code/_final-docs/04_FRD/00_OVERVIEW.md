# 00_OVERVIEW — F-TAX Tax Code (รหัสภาษี — VAT + Withholding Tax Master Data)

> **Audience:** All roles (PM, BA, FE, BE, QA, DBA)
> **Purpose:** Document Control + Scope + Roles + Dependencies + Coverage Manifest + Open Questions

---

## §0.1 Document Control

| Field | Value |
|---|---|
| **Feature ID** | F-TAX |
| **Feature Name** | Tax Code — รหัสภาษี (VAT ขาย/ซื้อ + Withholding Tax Master Data) |
| **Feature Code** | ACC-TAX (BRD-ACC-TAX-001) |
| **Module** | Accounting · ตั้งค่าบัญชี (Shared Foundation Master Data · Wave W1) |
| **Variant** | **FULL** (9 files + INDEX) — see §0.3.1 for decision |
| **Status** | DRAFT (generated) |
| **FRD Version** | 1.0 (2026-08-05) |
| **Generator** | frd-generator-v6 (HTML-first, Lane one-shot mode) |
| **Source Brief** | — (ไม่มี Brief; WF-01 HTML-first lane — Variant fallback จาก BRD) |
| **Source BRD** | BRD_F-TAX_TaxCode.md (status: APPROVED / AI Reviewed 28/28, 2026-08-05) |
| **Source HTML** | outputs/10_Tax-Code/01_HTML/TaxCode.html (SCREEN SOURCE OF TRUTH — ผ่าน ux gate R2 + coverage gate R2 28/28) |
| **Author** | BA (WF-01 · SOW3.3) |
| **Reviewers** | Tech Lead, Accounting/Finance Manager, QA Lead |

### §0.1.1 Design-Authority Sync (Sync Read log) ⭐

- **html-generator-v6 ไม่ได้ติดตั้ง** → ใช้เวอร์ชันสูงสุดที่มี = **html-generator-v7** (path: `WF-01_Pipeline_SkillSet/WF_Pipeline_SkillSet/html-generator-v7/`).
- Sync Read: `html-generator-v7/SKILL.md` + `knowledge/iron-rules.md` + `knowledge/ci-tokens.md` + `knowledge/microcopy.md`.
- **CI (อ่านสดจาก ci-tokens.md — ไม่ hardcode):** CUBE Design System **Warm Light** — Ivory ground `#FAF8F5` (`--c-bg-off`), White cards, Charcoal `#111111` (`--c-navy`/`--c-ink`), **Red `#FF3B30` (`--c-primary`) = action/priority**, **Orange `#FF9A1F` (`--c-teal`) = connection**; ฟอนต์ **Satoshi + Noto Sans Thai**.
- **Layout tokens (live):** Sidebar `232px` (`--sidebar-w`), Shell bar `52px` ขาว (`--shell-h`), Drawer `920px` / `.standard 680px`, Modal `440px`.
- **Iron Rules (live):** `knowledge/iron-rules.md` header ประกาศ **48 ข้อ base (v3.13)**; `SKILL.md` ต่อยอดชุดกฎอ้างถึง **#49 Minimal Scrollbar** และ **#94 Master Combobox** (field ที่อ้าง master = search-dropdown pattern เดียวเสมอ). FRD นี้ไม่ pin จำนวน/ค่าใด ๆ — ยึด Sync Read ปัจจุบัน.
- **HTML CI cross-check:** `TaxCode.html` L25–31 ใช้ `--c-primary:#FF3B30` / `--c-teal:#FF9A1F` / charcoal `#111111` → สอดคล้อง Warm Light v7 (แม้ `<title>` ยังเขียน "CUBE NATIVE" ซึ่งเป็น string ค้าง ไม่ใช่ theme จริง — ดู OQ-11).

---

## §0.2 Revision History

| Version | Date | Author | Changes |
|---|---|---|---|
| 1.0 | 2026-08-05 | BA (frd-generator-v6) | Initial FRD generation — FULL variant, HTML-first, one-shot; FLAG-1 resolved (WHT GL = WHT_PAYABLE only) |

---

## §0.3 Scope

### In Scope (จาก BRD §3.1)
- Master รหัสภาษี 2 ตระกูล: **VAT** (ทิศ ขาย/ซื้อ/ทั้งคู่; ประเภท STANDARD/ZERO_RATED/EXEMPT) และ **WHT** (ทิศจ่าย; บังคับประเภทเงินได้)
- สร้าง / แก้ไข / บันทึกร่าง / เปิดใช้งาน (activate) / ปิดใช้งาน (deactivate) / เก็บถาวร (archive)
- ผูกบัญชี GL (จาก CoA) ตามทิศทาง/ตระกูล — บังคับก่อน active (WHT filter `WHT_PAYABLE` เท่านั้น — LOCK-12)
- ช่วงวันมีผล (effStart/effEnd) คุมการโผล่ใน picker ตามวันที่เอกสาร
- Replacement flow (อัตราของรหัสที่ used>0 แก้ไม่ได้ → สร้างรหัสแทน + lineage)
- Preset ไทย 7 รหัสพร้อม GL ตั้งแต่วันแรก
- Picker ตามวันที่เอกสาร + immutable tax snapshot ลงเอกสาร consumer
- Append-only audit trail + soft archive (ไม่มี hard delete)
- current-company context; permissions `tax_code.view/create/update/activate/deactivate/view_audit`

### Out of Scope (จาก BRD §3.2 / AI_DEFAULTS §Out of Scope — ห้ามเผลอเติม)
- ❌ Default Tax Code รายชนิดเอกสาร (SO default VAT7) — อยู่ config module อื่น (OQ-1, resolved out)
- ❌ Incoming WHT / หนังสือรับรองภาษีฝั่งรับ (OQ-2, resolved out)
- ❌ การยื่นแบบ / เชื่อมต่อกรมสรรพากร (RD e-filing)
- ❌ การสร้างเอกสาร PDF (master/config — skip thai-doc-pdf-generator)
- ❌ ภาษีต่างประเทศ / multi-jurisdiction (THB/ไทยเท่านั้น)
- ❌ การสร้างหน้ารายงาน ภ.พ.30 / ภ.ง.ด.3/53 (downstream External Contract)

### Out of Scope (Phase 2.5 probe defaults tagged — resolve ที่ review, ดู §0.8)
- Draft auto-save/expiry policy — ใช้ conservative default "no auto-expiry" `[AI-DEFAULT]` (OQ-10)

### §0.3.1 Variant Decision (Fallback จาก BRD — one-shot, ไม่ถาม user) ⭐

ไม่มี Brief §3.4 → ใช้ Variant Fallback จาก BRD (skill Pack Variant Selection):

| Input | ค่าใน BRD | อ้างอิง |
|---|---|---|
| **pages** | 5 (P-01..P-05 render surfaces บน 1 route) | §14.6 Screen Inventory |
| **states** | 4 (draft / active / inactive / archived) | §8 State Diagram |
| **approval** | **YES** — activate/deactivate = Approver (Acct/Fin Manager); Maker≠Approver (SoD) | §4.2 / §5 COSO |
| **money** | **YES** — ผูก GL posting + อัตราภาษี + replacement (financial master) | §9 / §12.1 |

**Decision rule:** `states ≥ 4` (=4) → **FULL** · เสริมด้วย `approval AND money = YES` (ก็ FULL) · §9.5 Engine Management = ไม่มี (ไม่ใช่ trigger). → **Variant = FULL (9 files + INDEX).** Multi-engine (3 engines ใน 03_LOGIC §3.2) สอดคล้องกับ FULL.

---

## §0.4 Roles & Responsibilities (COSO) — จาก BRD §4

| Role | Person/Team | Responsibilities | COSO |
|---|---|---|---|
| **Maker** | พนักงานบัญชี (Accountant) | สร้าง/แก้ไข/บันทึกร่าง, ผูก GL, ดูข้อมูล+audit | Maker |
| **Checker** | หัวหน้าบัญชี (Senior Accountant) | ทบทวนก่อนเปิดใช้ (optional layer, นอกจอ) | Checker |
| **Approver** | ผู้จัดการบัญชี/การเงิน | activate / deactivate / archive (governance master data) | Approver |
| **Owner (System)** | ระบบ | validate uniqueness/GL role, filter GL, snapshot ตามวันที่เอกสาร, audit append-only | System |
| **Consumer (External)** | SO/PO/Invoice/Payment/รายงานภาษี | อ่าน/เลือกผ่าน picker → ใช้ในเอกสาร; ไม่แก้ master | External Contract |

> **SoD บังคับ:** create/update (Maker) ≠ activate/deactivate (Approver). ดู 05_RULES §5.3 + §5.7 (S01-04).
> Journey เต็ม → 01_UI §1.3.

---

## §0.5 Dependencies

### Upstream (feature นี้พึ่งพา)
| Dependency | Type | Source | ถ้าไม่มี/ผิด |
|---|---|---|---|
| Chart of Accounts (CoA) — GL master | Data / API | Module Accounting (existing master) | ผูก GL ไม่ได้ → active ไม่ได้ (R04); ถ้า CoA ไม่มี GL ตระกูลภาษี ต้องสร้างใน CoA ก่อน |
| Permission / RBAC framework (`tax_code.*`) | Service | Platform (provisional — OQ-5) | ต้อง backfill 6 สิทธิ์ |
| Audit Log service (append-only) | Service | Platform (provisional — OQ-5) | ใช้ audit table ของ feature (T_tax_code_audit) เป็น fallback |
| Company / Session context | Data | Platform | ต้องมี current company ก่อนเข้าฟอร์ม (LOCK-02) |

### Downstream (features ที่พึ่งพา feature นี้) — **ทั้งหมด External Contract / ยังไม่ implement**
| Consumer | สิ่งที่ใช้ | รายละเอียด |
|---|---|---|
| SO / AR Invoice | VAT ขาย (rate, glSale, snapshot) | 02_API §2.X + 06_TESTS XT-01 |
| PO / AP Invoice | VAT ซื้อ + WHT (แนะนำ) | XT-02 |
| Payment Voucher | WHT จริง (จุดยืนยันหัก) | XT-03 (LOCK-06) |
| VAT Return (ภ.พ.30) — `#/accounting/reports/vat-return` | `vat_report_category` จาก snapshot | XT-04 |
| WHT report (ภ.ง.ด.3/53) — `#/accounting/reports/withholding-tax` | income category + WHT final จาก payment result | XT-05 |

### External Services
| Service | Purpose |
|---|---|
| — | ไม่มี 3rd-party integration ใน feature นี้ (RD e-filing = Out of Scope) |

---

## §0.6 Stack & Architecture

| Layer | Technology |
|---|---|
| Frontend | React / hash-routing (prototype = vanilla SPA, single route + drawers/modals) |
| API | Node.js / Strapi (HTTP layer) |
| Database | PostgreSQL (RLS multi-company) |
| Engine layer | CUBIC Registry (3 engines — ดู 03_LOGIC §3.2) |
| Auth | JWT + role-based (`tax_code.*`) |

---

## §0.7 Multi-Tenant & Security Context

- [x] Multi-tenant (per-company) feature: **YES** — company scope บังคับทุก query/uniqueness/GL (LOCK-02/R15/E18)
- [ ] PII data involved: **NO** — รหัสภาษีไม่มี personal data (BRD §16.1)
- [x] Financial data: **YES** — GL posting mapping + tax rates (Security Preset P3 Master Data)
- [x] Audit log required: **YES** — append-only ทุก mutation (R05/S06-03)

**Security Bible domains applied:** D2 (Auth/Session), D5-lite (Financial master — no payment), D9 (Audit), D15 (Admin actions/SoD), D17 (Multi-tenant isolation). **ไม่ trigger D7 PII** (ไม่มี PII). → ดู 05_RULES §5.7.

### §0.7.1 Data Classification Summary ⭐

Highest classification level ที่ feature แตะ:
- [ ] Has Restricted fields — **ไม่มี** (ไม่มี salary/PII/board data)
- [x] Has Confidential fields — GL posting mapping (`gl_sale`/`gl_purchase`/`gl_wht`) = financial config จำกัด role
- [x] Internal (default) — ฟิลด์ส่วนใหญ่ (code/name/rate/status/effective dates/audit)
- [ ] Public-facing data — ไม่มี

**Highest level = Confidential.** ไม่มี Restricted → ไม่ต้อง wire Restricted Resources registry (แต่ยังลิงก์ Data Classification module ตาม 04_DB §4.6.6). สอดคล้อง BRD §16.3 S02-05 ("financial master — internal").

---

## §0.8 Open Questions

> Carried จาก BRD §15 (OQ-3/4/6/7 บังคับตามคำสั่ง lane — **ห้าม resolve โดยแต่ง spec**) + probe defaults ใหม่จาก Phase 2.5.

| ID | Question | Blocking? | Owner | Source |
|---|---|---|---|---|
| **OQ-3** | ต้องมี second-person approval (SoD) จริงสำหรับ activate/deactivate หรือ single-role accounting-admin เพียงพอ? (prototype demo user ถือครบ 6 สิทธิ์ L2067-2069) | NO (Phase 1 spec ใช้ SoD Maker≠Approver ไปก่อน) | Finance/บัญชี | BRD §15 / §4.2 |
| **OQ-4** | ระบบ consumer downstream (AR/AP/Payment/PP.30/WHT report) interface + timing? ยืนยัน snapshot contract + WHT-final-at-payment (LOCK-06) | NO (ทั้งหมด External Contract) | ทีม downstream | BRD §15 |
| **OQ-6** | ถ้า GL ที่ผูกไว้ถูก deactivate/ลบใน CoA ภายหลัง → รหัสภาษี active ควรทำอย่างไร (block posting / warn / require re-bind)? | **YES (กระทบ posting)** | Accounting + CoA owner | BRD §15 / E08 |
| **OQ-7** | อัตราแนะนำต่อประเภทเงินได้ WHT (R17) เก็บที่ config table หรือ hardcode reference? ใครอัปเดตตามกฎหมาย? | NO (low, CONFIGURABLE hint) | Accounting admin | BRD §15 |
| OQ-5 | System Module Registry (reuse vs สร้างใหม่ ของ audit/RBAC/CoA) — §12.3 provisional | NO | Platform/Arch | BRD §15 (carried — กระทบ §0.5) |
| **OQ-8** `[AI-DEFAULT]` | บังคับ `Idempotency-Key` header ทุก mutation (PR-7 default) — ยืนยันนโยบาย + TTL (default 24h) | NO | Tech Lead | Phase 2.5 PR-7 |
| **OQ-9** `[AI-DEFAULT]` | Optimistic locking ผ่าน `If-Match`/`version` → 409 บน edit/deactivate ที่ conflict (PR-1/PR-2 default; BRD E15 บอกให้มี lock แต่ไม่ระบุ contract) | NO | Tech Lead | Phase 2.5 PR-1/E15 |
| **OQ-10** `[AI-DEFAULT]` | Draft retention/expiry — default "ไม่มี auto-expiry" (master data ไม่ใช่ wizard, PR-6). ยืนยันว่าไม่ต้อง cleanup drafts | NO | BA/Accounting | Phase 2.5 PR-6 |
| OQ-11 | `<title>` ใน HTML เขียน "CUBE NATIVE" (legacy) ทั้งที่ CI tokens เป็น Warm Light v7 — cosmetic string mismatch (R14: raise, ไม่แก้ spec เอง) | NO | FE | HTML L6 vs L25-31 |

> **OQ-1 / OQ-2:** ✅ resolved = Out of Scope (BRD §15). ไม่นำเข้าเป็น OQ ค้าง.
> **Restricted fields:** ไม่มี → ไม่มี OQ wire Restricted Resources (R10 check).

---

## §0.9 Glossary

| Term | Definition |
|---|---|
| VAT | ภาษีมูลค่าเพิ่ม (STANDARD / ZERO_RATED / EXEMPT) |
| WHT | ภาษีหัก ณ ที่จ่าย (Withholding Tax) |
| ภ.พ.30 (PP.30) | รายงานภาษีมูลค่าเพิ่ม (downstream) |
| ภ.ง.ด.3/53 | รายงานภาษีหัก ณ ที่จ่าย บุคคล/นิติบุคคล (downstream) |
| GL | General Ledger account (จาก CoA) |
| Snapshot | ค่าภาษี immutable ที่บันทึกลงเอกสาร ณ วันที่เอกสาร |
| Replacement / lineage | การสร้างรหัสแทนเมื่ออัตราเปลี่ยน + เก็บความเชื่อมโยง (replaces/replacedBy) |
| SoD | Segregation of Duties (Maker ≠ Approver) |
| used | จำนวนเอกสารที่อ้างรหัสนี้ (badge) — read-only จาก consumer |
| pickable | active AND effStart ≤ วันที่เอกสาร ≤ effEnd |

---

## §0.10 Pack Navigation

| File | Audience | Purpose |
|---|---|---|
| 00_OVERVIEW.md | All | This file — meta + scope + coverage |
| 01_UI.md | FE dev | Layout Decision Log + Pages + Journey |
| 02_API.md | BE dev (HTTP) | API contracts + Cross-Module Contract |
| 03_LOGIC.md | BE dev (logic) | Functions + Engines + Trace |
| 04_DB.md | DBA / BE | Tables + Fields + Classification |
| 05_RULES.md | BE + QA | Rules + Validation + Edge Cases + Errors + Security |
| 06_TESTS.md | QA | Acceptance + DoD + Cross-Module cases |
| 07_LOCKED_DECISIONS.md | All | Scope Lock (§7.0) + LDs |
| INDEX.md | All | Cross-reference quick nav |

---

## §0.11 Scope Lock (pointer)

> FULL variant → Scope Lock อยู่ที่ **07_LOCKED_DECISIONS §7.0** (import ครบ LOCK-01..LOCK-12 จาก BRD §3.4, immutable).
> Scope Lock Ref: `AI_DEFAULTS.md` (F-TAX) — สถานะ LOCKED, 2026-08-05 (ไม่มีเลขใบเซ็น chain — งานเดินด้วย approved AI defaults).

---

## §0.12 Coverage Manifest ⭐ (กัน requirement หล่น BRD→FRD — R13)

### Stories (BRD §7)
| BRD Ref | Requirement (ย่อ) | อยู่ที่ใน Pack |
|---|---|---|
| §7 S-01 | ดูรายการรหัสภาษีแยก VAT/WHT + KPI | 01_UI P-01 · 02_API-01 · 03_FN-01 · 06 AC-01 |
| §7 S-02 | สร้างรหัสภาษีใหม่ (+activate) | 01_UI P-02 · 02_API-03/05 · 03_FN-02/05 · 06 AC-02/AC-03 |
| §7 S-03 | บันทึกร่างที่ยังผูก GL ไม่ครบ | 01_UI P-02 · 02_API-03 · 03_FN-02 · 05 BR-TAX-05 · 06 AC-04 |
| §7 S-04 | ผูก GL ตามทิศทาง/ตระกูล | 01_UI P-02 · 02_API-11 · 03_FN-11/ENG-03 · 05 BR-TAX-06/07 · 06 AC-05 |
| §7 S-05 | บังคับประเภทเงินได้ WHT | 01_UI P-02 · 02_API-05 · 03_FN-04/12 · 05 BR-TAX-03 · 06 AC-06 |
| §7 S-06 | ล็อกอัตราของรหัส used>0 | 01_UI P-02 · 02_API-04 · 03_FN-03 · 05 BR-TAX-02 · 06 AC-07 |
| §7 S-07 | สร้างรหัสแทนพร้อม lineage | 01_UI P-02 · 02_API-08 · 03_FN-08 · 05 BR-TAX-02 · 06 AC-08 |
| §7 S-08 | ปิดใช้งาน/เก็บถาวร ไม่ลบถาวร | 01_UI P-05 · 02_API-06/07 · 03_FN-06/07 · 05 BR-TAX-05 · 06 AC-09/AC-10 |
| §7 S-09 | ปรากฏใน picker ตามวันที่เอกสาร + snapshot | 01_UI P-04 · 02_API-09 · 03_FN-09/10 · ENG-01/02 · 06 AC-11 |
| §7 S-10 | ดูประวัติ (Audit) | 01_UI P-03 · 02_API-10 · 03_FN-13 · 05 §5.3 · 06 AC-12 |

### Rules (BRD §9.1 R01–R17)
| BRD Ref | อยู่ที่ | BRD Ref | อยู่ที่ |
|---|---|---|---|
| R01 uniqueness | 05 BR-TAX-01 · 06 AC-02b | R10 VAT enum | 05 BR-TAX-10 |
| R02 immutable used-rate | 05 BR-TAX-02 · 06 AC-07 | R11 WHT resolve contract | 05 BR-TAX-11 |
| R03 WHT income required | 05 BR-TAX-03 · 06 AC-06 | R12 AP advisory / Payment final | 05 BR-TAX-12 · 06 XT-03 |
| R04 GL before active | 05 BR-TAX-04 · 06 AC-05b | R13 rate 0–100 | 05 §5.4 VR05 |
| R05 no hard delete | 05 BR-TAX-05 · 06 AC-10 | R14 effEnd ≥ effStart | 05 §5.4 VR11 |
| R06 GL company/active/posting | 05 BR-TAX-06 · ENG-03 | R15 current-company | 05 BR-TAX-15 · 05 §5.7 D17 |
| R07 GL role (WHT=WHT_PAYABLE) | 05 BR-TAX-07 · 06 AC-05 | R16 preset seed 7 | 05 BR-TAX-16 · 03 FN-15 |
| R08 picker date + immutable snapshot | 05 BR-TAX-08 · ENG-01 | R17 WHT recommended rates | 05 BR-TAX-17 · OQ-7 |
| R09 pickable window | 05 BR-TAX-09 · ENG-02 | | |

### Edge Cases (BRD §10 — confirmed ☑ + probed ☐)
| BRD Ref | อยู่ที่ | BRD Ref | อยู่ที่ |
|---|---|---|---|
| E01 deactivate→picker/snapshot | 05 EC-01 · 06 XT-01 | E11 future effStart | 05 EC-11 |
| E02 edit rate used>0 | 05 EC-02 · 06 AC-07 | E12 replacement overlap | 05 EC-12 |
| E03 delete used | 05 EC-03 | E13 reactivate effEnd past | 05 EC-13 |
| E04 draft no GL | 05 EC-04 · 06 AC-04 | E14 concurrent create (uniq DB) | 05 EC-14 |
| E05 WHT-in-purchase advisory | 05 EC-05 · 06 XT-03 | E15 concurrent edit/deactivate | 05 EC-15 (OQ-9) |
| E06 duplicate code | 05 EC-06 · 06 AC-02b | E16 Maker submit guard | 05 EC-16 |
| E07 foreign tax | 05 EC-07 | E17 view_audit direct | 05 EC-17 |
| E08 GL deactivated in CoA | 05 EC-08 · **OQ-6** | E18 cross-company access | 05 EC-18 |
| E09 GL taxRole moved | 05 EC-09 | E19 multi-rate per doc | 05 EC-19 · 06 XT-04 |
| E10 income type removed | 05 EC-10 | | |

**สรุป:** Stories 10/10 ✅ · Rules 17/17 ✅ · Edges 19/19 ✅ · ไม่มีแถวที่ "อยู่ที่" ว่าง. รายการที่ยกเป็น Open Question (ไม่ resolve เงียบ): E08→OQ-6, E15→OQ-9, R17→OQ-7. Downstream contract (5) → 02_API §2.X + 06 XT-01..05.
