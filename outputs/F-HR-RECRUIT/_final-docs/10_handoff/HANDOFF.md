# HANDOFF — F-HR-RECRUIT · F127 · สรรหา / Recruit

**วันที่ปิดงาน:** 2026-09-03 · **Workflow:** WF-01 (12 step ครบ) · **contract:** Cube_Feature_List (F127 · HR · Wave W9 · dep Manpower F124)

## สถานะ gate — ไม่มี BLOCK
| gate | ผล |
|---|---|
| qc-ux (ทำถูกมั้ย) | **PASS** (4 WARN) |
| qc-coverage รอบ 1 (HTML vs PREBRIEF) | **PASS** · FN 21/21 |
| qc-coverage รอบ 2 (FRD + TC) | **WARN** (non-blocking) · FN↔TC 21/21 · BR 10/10 · VR 5/5 · XT 4/4 · LOCK 7/7 |
| e2e (`_e2e/e2e-recruit.py`) | **24/24** · unsupported 5/5 absent · console 0 |
| UI Brief Verification | **PASS** (FAIL=0) |
| Feature TL;DR gate | ผ่าน |

## ชุดส่งมอบ (จัดใน `_final-docs/`)
1. `00_context/` — PREBRIEF + FUNCTION_CHECKLIST (21 FN)
2. `01_prototype/` — `สรรหา.html` (source of truth)
3. `02_qc/` — UX + Coverage รอบ 1/2
4. `03_brd/` — BRD (APPROVED 20/20)
5. `04_frd/FRD_Pack/` — FRD 9 ไฟล์ (FULL tier)
6. `05_ui-brief/` — UI Brief AS-BUILT
7. `08_tldr/` — หน้าปกสรุปภาษาคน
8. `09_declarations/` — DOA · NTF (ผ่าน skill) · CSQ (carried)
9. `10_handoff/` — HANDOFF · PROPOSALS_outbound · PENDING_REGISTRY
10. `testcase_qa/` — AI Test Case (62 TC) + UAT HTML (Lite 50 เคส · เปิดกดทดสอบได้)

> ไม่มี `06_print/` — feature นี้ไม่มีเอกสารพิมพ์ (ข้าม step 2 · offer letter = soft ref)

## เริ่มตรวจที่ไหน
- **เปิดต้นแบบ:** `01_prototype/สรรหา.html`
- **Manual test:** `testcase_qa/สรรหา HTML Testcase.html`
- **อ่านเร็ว 2 นาที:** `08_tldr/FEATURE_TLDR_สรรหา.html`

## 🔴 ของค้างก่อน wire ระบบจริง (ละเอียดใน `PROPOSALS_outbound.md`)
- **OQ-DOA** — role id ยืนยันไม่ได้ (DOA master หายจาก install) → role ติด `[DEFAULT—รอยืนยัน]` · **บล็อกเฉพาะ wire DOA จริง**
- **OQ-15** — On/Offboard inbound handoff ยังไม่ออกแบบ (ใครสร้าง employee ระหว่างกลาง)
- **OQ-16** PDPA retention → Policy Center · **OQ-17** req-cancel guard · **DR-04** terminate ไม่มี NTF event
- **SEC_BRIEF** ยังไม่ทำ (PII/PDPA เสี่ยงสูง — BA เคาะ) · **Manpower F124** warn-only (ยังไม่มีระบบ)

## declaration รอบนี้
`doa` + `ntf` (ผ่าน skill) · `csq` carried (ไม่มี csq skill ใน WF-01) · doccfg/pdf = not-needed
