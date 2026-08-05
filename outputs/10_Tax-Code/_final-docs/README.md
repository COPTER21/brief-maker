# Tax Code (F-TAX) — Final Handoff Pack

ชุดเอกสารส่งมอบสำหรับ **AI Coding Agent / dev** ไป implement feature "รหัสภาษีกลาง" (VAT + WHT master data)
สร้างผ่าน WF-01 pipeline (html-generator-v7 → QC gates → BRD → FRD → UI Brief → Test Cases → UAT)
รวบเมื่อ 2026-08-05 · Feature ID: **F-TAX** · route: `#/accounting/setup/tax-codes`

> ทุกไฟล์ในโฟลเดอร์นี้เป็น **สำเนา** ของ deliverable สุดท้าย — ต้นฉบับ + working files (screenshots, cases.json ฯลฯ) อยู่ที่ `outputs/10_Tax-Code/` ระดับบน

---

## 📦 มีอะไรบ้าง + ใครใช้

| โฟลเดอร์ | ไฟล์ | สำหรับใคร | คืออะไร |
|---|---|---|---|
| `00_CONTEXT/` | AI_DEFAULTS.md | ทุกคน | 11 ข้อสมมติที่ lock + Scope Lock + out-of-scope |
| | DECISION_LOG.md | ทุกคน | decision ที่ตกลง (สืบจาก session ก่อน) + cross-check กับ HTML |
| `01_PROTOTYPE/` | TaxCode.html | FE dev / QA | **source of truth ของ UI** — เปิดในเบราว์เซอร์ดูของจริงได้ทันที |
| `02_QC/` | TaxCode_UX_CHECK_REPORT.md | — | หลักฐาน gate: UX/CI/iron rules PASS |
| | TaxCode_COVERAGE_REPORT.md | — | หลักฐาน gate: business scope 28/28 PASS |
| `03_BRD/` | BRD_F-TAX_TaxCode.md/.docx | BA / PO / stakeholder | เอกสาร business (18 sections + COSO + Security + KPI) |
| | _AI_REVIEW_REPORT.md | BA | ผลตรวจ BRD (APPROVED 27/28) |
| `04_FRD/` | 00–07 + INDEX (9 ไฟล์) | dev ทุกสาย | **สเปกหลักสำหรับ implement** (ดูตารางล่าง) |
| `05_UI_BRIEF/` | UI_BRIEF_TaxCode.md | FE dev | design intent AS-BUILT — ทุกบรรทัด anchor กลับ HTML |
| `06_TESTCASES/` | testcases-tax-code.md | QA / AI test agent | 76 เคสละเอียด (สำหรับ browser-use/vision รันเอง) |
| `07_UAT/` | testcase-tax-code.html | ผู้ทดสอบ (คนทั่วไป) | แบบทดสอบเปิดในเบราว์เซอร์ ติ๊กผล + พิมพ์ PDF ได้ |

### FRD Pack (`04_FRD/`) — แบ่งงาน dev
| ไฟล์ | สำหรับ |
|---|---|
| 00_OVERVIEW.md | scope, dependencies, Coverage Manifest, Open Questions |
| 01_UI.md | FE dev — หน้า/route/pattern + Layout Decision Log |
| 02_API.md | BE dev — HTTP layer contracts |
| 03_LOGIC.md | BE dev — Functions + Engines + API↔Logic trace |
| 04_DB.md | DBA/BE — tables + Data Classification |
| 05_RULES.md | BE + QA — business rules + validation + errors + permission |
| 06_TESTS.md | QA — acceptance + DoD + cross-module |
| 07_LOCKED_DECISIONS.md | ทุกคน — LOCK-01..12 (immutable) |
| INDEX.md | นำทาง + function trace |

---

## ✅ สถานะคุณภาพ

- **qc-ux gate:** 🟢 PASS 0 warning (render จริง 12 ภาพ ยืนยัน CI/density ตรง)
- **qc-coverage gate:** 🟢 PASS 28/28
- **BRD:** 🟢 APPROVED (AI Review 27/28)
- **FRD:** 🟢 Phase 3.5 PASS ทุก section A–M · variant = FULL
- **traceability end-to-end:** Stories 10/10 · Rules 17/17 · Edges 19/19 (BRD Manifest ↔ FRD §0.12 ↔ 76 test cases ตรงกัน)
- **UI Brief:** 🟢 Verification Gate PASS
- **Test cases:** 76 เคส · Manifest cross-check ✅ · UAT HTML 1:1 (76 เคส, 19 ภาพจอ)

---

## ⚠️ Open Questions — ต้องเคาะก่อน/ระหว่าง dev

| id | เรื่อง | สถานะ |
|---|---|---|
| **OQ-6** | ถ้า GL ที่ผูกไว้ถูก deactivate ใน CoA ทีหลัง → posting กระทบยังไง | 🔴 **BLOCKING** ก่อน dev จริง |
| OQ-3 | master data ต้องมี SoD จริงไหม (prototype demo user ถือครบ 6 สิทธิ์) | ต้องยืนยัน |
| OQ-4 | downstream consumer 5 ตัว = External Contract (ยังไม่ implement) | ต้องยืนยัน contract |
| OQ-7 | ตาราง WHT recommended-rate เจ้าของ/ที่เก็บ | 🤖 inferred |
| OQ-8/9/10 | Idempotency-Key / optimistic lock 409 / draft ไม่ auto-expire | `[AI-DEFAULT]` — BA confirm |
| OQ-11 | HTML `<title>` เขียน "CUBE NATIVE" (cosmetic) | แก้เมื่อว่าง |

รายละเอียดเต็มอยู่ใน `04_FRD/00_OVERVIEW.md` (Open Questions) · เคสที่ผูกกับ OQ ติด `[AI-DEFAULT]` ใน `06_TESTCASES/`

---

## 🚀 เริ่มยังไง

1. เปิด `01_PROTOTYPE/TaxCode.html` ในเบราว์เซอร์ → เห็น UI จริง
2. อ่าน `04_FRD/00_OVERVIEW.md` + `INDEX.md` → เข้าใจ scope + นำทาง
3. implement ตาม FRD (01_UI/02_API/03_LOGIC/04_DB/05_RULES) โดยยึด HTML เป็นหน้าตาจริง + `05_UI_BRIEF/` เป็น design intent
4. เคลียร์ **OQ-6** ก่อนทำส่วน GL posting
5. ทดสอบด้วย `07_UAT/testcase-tax-code.html` (คน) หรือ `06_TESTCASES/testcases-tax-code.md` (AI agent)

**Out of scope (ห้ามทำ):** ค่าเริ่มต้น tax code รายเอกสาร · incoming WHT / หนังสือรับรองฝั่งรับ · ยื่นแบบ/เชื่อมกรมสรรพากร · gen PDF (ดู AI_DEFAULTS.md)
