# F-BNK · Bank Master — Dev Handoff Pack

> ธนาคาร / บัญชีบริษัท (Finance · Shared-Foundation **master** · ไม่มี tier) · WF-01 pipeline ครบ 9 skills · 2026-08-06
> **HTML = source of truth** — BRD/FRD/UI-Brief/TC ทุกตัว derive มาจาก `BankMaster.html`

## 1. ในแพ็คมีอะไร · ใครใช้

| ไฟล์ | คืออะไร | ใครใช้ |
|---|---|---|
| `BankMaster.html` | Prototype ทำงานจริง (SPA เปิดใน browser) — ความจริงอ้างอิงของทุกอย่าง | ทุกคน · Dev เปิดดูพฤติกรรมจริง |
| `BRD_F-BNK_BankMaster.md` / `.docx` | Business Requirements (18 sections, Scope Lock, 12 BR, Value Stream) | BA · PM · ผู้อนุมัติ |
| `FRD_F-BNK_Pack/` (9 ไฟล์) | Functional spec แยก layer (00 Overview·01 UI·02 API·03 Logic·04 DB·05 Rules·06 Tests·07 Locked·INDEX) | **Dev** (สเปคหลักที่ implement ตาม) |
| `UI_BRIEF_bank-master.md` | บรีฟ UI สกัด 1:1 จาก HTML (tokens, z-index, anatomy, states, microcopy, traceability) | **Dev Frontend** (คู่กับ HTML) |
| `testcases-F-BNK-bank-master.md` | 76 test cases สำหรับ AI agent (browser-use) รันเอง | QA automation / AI runner |
| `UAT_F-BNK_bank-master.html` | เอกสารทดสอบฉบับคน (76 เคส 1:1, มีภาพ+data sample+ติ๊กผล+พิมพ์ PDF) | **ผู้ทดสอบ/ลูกค้า** (เปิดไฟล์เดียวจบ) |
| `QC/` | รายงาน 3 ตัว: `_UX_CHECK_REPORT` (form) · `_COVERAGE_REPORT` (scope) · `_E2E_TEST_REPORT` (functional) | Reviewer · QA |
| `DECISION_LOG.md` · `AI_DEFAULTS.md` | บันทึกการตัดสินใจ + ค่า [AI-DEFAULT] + bug journey | ทุกคน (บริบทว่าทำไมถึงเป็นแบบนี้) |

## 2. สถานะคุณภาพ

| ขั้น | ผล |
|---|---|
| skill 1 HTML | adopt ของเดิม (gate PASS) + แก้ bug จาก QC/E2E/manual test |
| skill 2 PDF | **ข้าม** (master ไม่มีเอกสารพิมพ์) |
| skill 3 qc-ux | 🟢 PASS |
| skill 4 qc-coverage | 🟡 WARN 24/25 · 0 block · no scope creep |
| **E2E (3 รอบ + re-test)** | 🟢 GREEN — เจอ+แก้ Bug A (drawer re-render), B (toast), C (modal z-index); regression ผ่าน |
| skill 5 BRD | ✅ APPROVED (gate 28/28) |
| skill 6 FRD | ✅ FULL 9 ไฟล์ · Phase 3.5 A–M ผ่าน · Coverage Manifest 9/9·12/12·15/15 |
| skill 7 UI Brief | ✅ PASS (extraction-based, 13 sections) |
| skill 8 AI Testcases | ✅ 76 TC (happy 20/neg 22/edge 13/error 6/permission 15) · trace ครบ |
| skill 9 UAT HTML | ✅ 76 TC 1:1 · 224 steps · 23 screenshots · self-contained |

**หัวใจความปลอดภัย:** เลขบัญชี = ข้อมูล Restricted → mask 4 ตัวท้าย · reveal เต็มต้องมีสิทธิ์ `canRevealFull` + audit ทุกครั้ง (audit-first) · ชุด permission test = P0

## 3. ⚠️ ต้องตัดสินก่อน/ระหว่าง dev

1. ✅ **EC-14 / OQ-BNK-05 — RESOLVED (2026-08-06): "เตือน + เคลียร์"** — ปิดใช้งาน/เก็บถาวรบัญชีที่เป็น default → เคลียร์ flag (กัน dangling default ที่ชี้บัญชีเลือกไม่ได้) + กล่องยืนยันแสดง**คำเตือน**ว่าบริษัทจะไม่มีค่าเริ่มต้น ให้ตั้งบัญชีใหม่ · sync ตรงกันครบ HTML + FRD (LD-06) + TC (E03/E06) + UI Brief (D-6) + UAT — ปิด divergence แล้ว
2. **OQ-1 [AI-DEFAULT]:** tier ไหนได้ `canRevealFull` — ตอนนี้ default = Finance-admin (mock) · **Policy ต้องยืนยัน tier จริง** ก่อน dev (ห้าม hardcode สายอนุมัติ)
3. **OQ-2 [AI-DEFAULT]:** multi-currency — ล็อก THB เฟสนี้ · field `currency` มีแล้ว → เปิดทีหลัง = toggle ไม่ใช่แก้ schema
4. **W1 (บันทึกแล้ว = R-08/BR-BNK-08):** ธนาคาร custom ลบถาวรได้เฉพาะ used=0 = **ข้อยกเว้นชัดเจนของ Global Contract #7** · preset ธปท. แก้/ลบไม่ได้
5. **Offline caveat:** icon (lucide) + ฟอนต์ Satoshi โหลดจาก CDN → เปิด offline จะ blank · ถ้าต้อง offline-safe 100% ให้ inline icon/font ตอน implement

**ไม่รองรับเฟสนี้ (Scope Lock):** เชื่อม bank API / statement อัตโนมัติ (S-06) · multi-currency · tier/Lite-Full

## 4. เริ่มยังไง

- **อยากเห็นของจริง:** เปิด `BankMaster.html` ใน browser (2 แท็บ: บัญชีบริษัท / ธนาคาร)
- **Dev:** อ่าน `FRD_F-BNK_Pack/INDEX.md` → ไล่ตาม layer · UI ยึด `UI_BRIEF_bank-master.md` + HTML คู่กัน
- **QA คน:** เปิด `UAT_F-BNK_bank-master.html` ทำตามทีละขั้น ติ๊กผล พิมพ์รายงาน
- **QA automation:** ป้อน `testcases-F-BNK-bank-master.md` ให้ AI runner (ผล cross-check กับ UAT ได้ เพราะ TC id ตรงกัน)

> ไฟล์ทำงานระหว่างทาง (screenshots, _bak, _e2e/_fix/_diag, results.json) อยู่ในโฟลเดอร์ staged `01_HTML`..`07_UAT` — ไม่รวมในแพ็คส่งมอบนี้
