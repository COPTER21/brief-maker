# PIPELINE STATUS · Payment Term (F-PAY)

> WF-01 doc-gen pipeline · repo `brief-maker` · เริ่ม 2026-08-10
> Source of truth = HTML (`01_HTML/f-payterm.html`) · เอกสารทุกตัว derive จาก HTML
> **ใช้เฉพาะ 9 skills ที่กำหนด — ห้ามใช้ skill นอกลิสต์**

## Feature
- **F-PAY** · Payment Term / เงื่อนไขชำระเงิน · module Accounting · master (ไม่มีสายอนุมัติ)
- ใช้ร่วม P2P + S2C · 7 ประเภท · seed HTML ผ่าน E2E แล้ว (adopt เป็น SoT)

## Decisions (ยืนยันโดย user 2026-08-10)
- **D-01** Step 1 = **Adopt seed + v8 conformance pass** (ไม่ full re-gen)
- **D-02** **ข้าม Step 2** (thai-doc-pdf) — master ไม่มีเอกสาร PDF (OB-2)
- **D-03** FRD variant = **FULL** (step 6)

## Progress
| # | Skill | สถานะ | Output |
|---|-------|-------|--------|
| 0 | scaffold + 00_CONTEXT | ✅ DONE | `00_CONTEXT/`, `01_HTML/f-payterm.html` |
| 1 | html-generator-v8 (conformance) | ✅ DONE (audit FAIL=0) | `01_HTML/f-payterm.html` |
| 2 | thai-doc-pdf-generator | ⏭️ SKIP (D-02) | — |
| 3 | qc-ux-html-checker | ✅ PASS w/ documented residuals (retrofit done) | `02_QC/_UX_CHECK_REPORT.md` |
| 4 | qc-coverage-checker | ✅ WARN (FN 26/26 · BR 10/10 · edges 4/4 · no BLOCK) | `02_QC/_COVERAGE_REPORT.md` |
| — | 🛑 **GATE — user review (Phase A จบ)** | ✅ PASSED — G1 ถอด PR (PM/BA) · G2/G3 fixed · use_in=7 | — |
| — | **E2E test (2 รอบ)** | ✅ 23/23 · 0 JS err · เจอ+แก้ BUG-E2E-01 (scroll jump-to-top) | `02_QC/_E2E_REPORT.md` |
| 5 | brd-generator-full | ✅ DONE — QG 28/28 · .md+.docx · PR excluded (use_in 7) | `03_BRD/BRD_F-PAY.md` (+.docx) |
| 6 | frd-generator-v6 (FULL) | ✅ DONE — 9 ไฟล์ · PR excluded · ENG registered · Manifest 8/8·13/13 | `04_FRD/FRD_F-PAY_Pack/` |
| 7 | html-ui-brief | ✅ DONE — 13 sections · extraction-based · Drift Log 6 | `05_UI_BRIEF/UI_BRIEF_payment-term.md` |
| 8 | ai-testcase-md-generator | ✅ DONE — 89 cases · trace FRD ครบ · PR/used>0 tested | `06_TESTCASES/testcases-F-PAY.md` |
| 9 | qa-friendly-html-generator | ✅ DONE — 89=89 (1:1) · 2.9MB · 13 shots · self-contained | `07_UAT/UAT_payment-term.html` |
| — | _final-docs + README | ✅ DONE | `_final-docs/` (README index) |

## 🏁 PIPELINE COMPLETE (2026-08-10) — 8 steps (ข้าม step 2) · run-long mode Phase B
Dev handoff pack พร้อมที่ `_final-docs/` — เริ่มที่ `_final-docs/README.md`

## Gates
- 🛑 หลัง step 4 (Phase A) — user ตรวจ HTML + 2 QC reports ก่อนไป Phase B
- ผู้ใช้ขอให้หยุดทุก step ให้รีวิว (ไม่ใช่แค่ที่ gate หลัก)
