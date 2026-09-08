# F-HR-WELFARE (F102 · สวัสดิการ / Welfare) — Dev Handoff Pack
> ชุดเอกสารส่งมอบครบทั้ง WF-01 (12 step) · ปิดงาน 2026-09-08 · archetype = master + light transaction (NOT Pattern Q)
> เปิดอ่านตามลำดับโฟลเดอร์ · เริ่มที่ `08_tldr` ถ้าอยากเข้าใจภาพรวมเร็ว

## ลำดับการอ่าน
| โฟลเดอร์ | มีอะไร | เปิดไฟล์ไหนก่อน |
|---|---|---|
| `00_context` | ที่มา: PREBRIEF · FUNCTION_CHECKLIST (24 FN) · STANDARD_BASELINE · HANDOFF · **_DECISION_LOG_OQ** (มติ 5 ข้อ research-based) | PREBRIEF.md |
| `01_prototype` | ต้นแบบจอเล่นจริง (single-file · e2e 49/49) | welfare.html |
| `02_qc` | รายงานตรวจ: UX (PASS) · Coverage R1 (HTML) · Coverage R2 (FRD+TC) | _UX_CHECK_REPORT.md |
| `03_brd` | BRD (APPROVED) | BRD_welfare.md |
| `04_frd` | FRD Pack FULL 8 ไฟล์ + INDEX (UI/API/LOGIC/DB/RULES/TESTS/LOCKED) | FRD_F-HR-WELFARE_Pack/INDEX.md |
| `05_ui-brief` | UI Brief (extraction-based · ui-brief-check PASS) | UI_BRIEF_welfare.md |
| `testcase_qa` | Test case สำหรับ AI/QA (60 เคส) + เอกสารทดสอบให้คนกด (53 เคส · ภาพจริง) | testcases-welfare.md · สวัสดิการ HTML Testcase.html |
| `08_tldr` | หน้าปกสรุปภาษาคน 2 นาที | FEATURE_TLDR_welfare.html |
| `09_declarations` | ใบประกาศให้ dev wire: DOA · NTF · CSQ | (3 ไฟล์) |
| `10_handoff` | OQ/ข้อเสนอส่งออก + สรุปให้ PM/BA | PROPOSALS_outbound.md |
| `CTX_F-HR-WELFARE.md` | 🔗 Context Card — technical contract ย่อ (entities/API/events/shared rules) สำหรับแนบตอนออกบรีฟ feature อื่น (derived from FRD) | (ไฟล์เดียว ที่ราก _final-docs) |

## สรุปฟีเจอร์
ทะเบียนสวัสดิการต่อกลุ่มพนักงาน (โควตา/วงเงินต่อปี) + ผู้ติดตาม + คำขอใช้สิทธิ์ → อนุมัติ (DOA 2 ขั้น) → ตัดคงเหลือ + บันทึกมูลค่าเข้าเงินได้ (7C·EC) · **กลับรายการได้ (admin)** · **ไม่จ่ายเงินเอง** (Payroll F065 / Expense F101 จ่าย · display-only hook)

## สถานะ Quality Gate (ทุกด่านเขียว)
- audit.sh **FAIL=0** · e2e **49/49** · FN **24/24** · qc-ux **PASS** · coverage R1/R2 **PASS** · ui-brief-check **PASS** · TL;DR check **PASS**
- ผ่าน PM/BA BLOCK fix รอบ (9 fixes: governance guards) + reversal (research-based)

## declaration รอบนี้
**doa + ntf + csq** (csq = EC เท่านั้น + reverse) · doccfg/pdfdoc = NOT-NEEDED

## 🔺 ต้องเคาะก่อน dev ตั้งค่าจริง (ดู 10_handoff/PROPOSALS_outbound.md)
- OQ-DOA-01: role id จริงของสาย DOA (ไม่มี master ให้ verify)
- A-WEL-02/OQ-03: สัญญา hook จ่าย Payroll/Expense
- OQ-05: permission enforce ฝั่ง backend
- PR-01: แผนกลาง F102 chip ควรเพิ่ม `ntf`

> หมายเหตุ: โฟลเดอร์นี้เป็น **สำเนา curated** สำหรับส่งมอบ · working files (พร้อม `_e2e/` · `_qa/`) อยู่ที่ root ของ `outputs/F-HR-WELFARE/`
