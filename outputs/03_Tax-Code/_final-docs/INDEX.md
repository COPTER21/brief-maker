# F-TAX · Tax Code (ทะเบียนรหัสภาษี) — Final Docs Pack

ชุดเอกสารส่งมอบสำหรับ dev / AI Coding Agent — module: Accounting (รอเคาะ OQ-TAX-05), CUBE 4.0 Core ERP, Wave 1 (ฐานราก).
Generated ผ่าน WF-01 fixed 9-skill pipeline · โหมด **HTML-first / Reverse Mode** (HTML = source of truth).

> อ่านตามลำดับ: **HTML → BRD → FRD Pack → UI Brief → Test Cases → UAT**. ทุก layer trace ถึงกัน ไม่มี drop เงียบ.

## เอกสารในโฟลเดอร์นี้

| ไฟล์ | มาจาก skill | คืออะไร |
|---|---|---|
| `f-taxcode.html` | html-generator-v8 | Prototype SPA (source of truth) — เปิดใน browser ได้เลย |
| `BRD_F-TAX_Tax-Code.md` / `.docx` | brd-generator-full | BRD FULL tier — business scope, rules, data entity, value stream (APPROVED) |
| `FRD_F-TAX_Pack/` | frd-generator-v6 | FRD STANDARD 7 ไฟล์ (UI/API/LOGIC/DB/RULES/TESTS + OVERVIEW) — สเปคให้ dev |
| `UI_BRIEF_F-TAX_Tax-Code.md` | html-ui-brief | บรีฟ UI สกัดจาก HTML 1:1 (tokens, z-index, overlay, microcopy verbatim) |
| `testcases-F-TAX_Tax-Code.md` | ai-testcase-md-generator | 72 test cases สำหรับ AI agent (browser-use) รันเอง |
| `UAT_F-TAX_Tax-Code.html` | qa-friendly-html-generator | เอกสารทดสอบฉบับผู้ใช้ (self-contained, ติ๊กผล + print PDF) — 72/72 1:1 |
| `_qc-evidence/` | qc-ux · qc-coverage · E2E | รายงาน QC/test (หลักฐาน gate) |

## สถานะ Quality Gate
- qc-ux **PASS** · qc-coverage **PASS** · E2E jsdom **42/42** (×2 รอบ, 0 JS error)
- BRD **APPROVED** · FRD **PASS** (Coverage: Stories 10/10 · Rules 10/10 · Edges 8/8 · Screens 6/6) · UI Brief untraceable **0**
- Test: 72 cases (Rules 10/10 · Scope Lock 9/9 · XT 4/4 · 6 import error codes verbatim)

## Open Questions — ต้องให้ BA เคาะก่อน dev จริง (surface ไว้ ยังไม่ตัดสิน)
- **OQ-TAX-04** — `used` ใน prototype เป็น mock → **ห้ามเปิด hard-delete ตัวจริง** จนกว่า sync ยอดใช้งานจริง (เสี่ยง data-loss, EC-A7)
- **OQ-TAX-05** — วาง module ที่ Accounting หรือ Master Data (HTML sidebar = Master Data, plan = Accounting)
- **OQ-TAX-06** — mock-user drift (พิมพ์ใจ vs วิภา) + RBAC/role-gate ยัง defer ไป Policy Center
- **OQ-TAX-02** — effective date / validity period = out of scope (ใช้แนวสร้างรหัสใหม่ + ปิดตัวเก่า)
- **OQ-TAX-03** — WHT scope ใน master กลาง (เลน Sales ใช้ VAT ก่อน)
- FRD เพิ่ม: rate precision (numeric 5,2), CSV parser header/encoding, concurrency 409 — ติด `[AI-DEFAULT]` รอ confirm

## ข้อจำกัดที่รู้อยู่ (documented, ไม่ซ่อน)
- **Import เป็น mock** — `bulkPick()` ใช้ `BULK_SAMPLE` hardcoded (ไม่อ่านไฟล์จริง) → 12 test cases tag `(ต้อง simulate)` = **blocked-not-fail** (ไม่ใช่ fail; ต้อง sim ตอนมี backend)
- **IR-TAX-01 ต้องบังคับฝั่ง server** — F-TAX-FN-03 guard code/rate/category แม้ client ฝืน (TC-E04 = P0)
- **Visual render gate** (pixel/layout ใน browser จริง) = ยัง NOT-CHECKED รอบนี้

---
*Sync note: `f-taxcode.html` ในโฟลเดอร์นี้ = สำเนา identical กับ source pack `Pack Brief Feature/3. Tax Code/f-taxcode.html` (source ต้องคงครบ). ถ้าแก้ HTML ต้อง sync ทั้งสองที่.*
