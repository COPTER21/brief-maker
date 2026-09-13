# ความยินยอม PDPA — Final Documents

ชุดนี้จัดหมวดตาม pattern ของ `outputs/17_Delivery-Note/_final-docs` สำหรับส่ง PM/BA, Dev และ Tester
feature **ความยินยอม PDPA** (F-MKT-CONSENT · F058) · standalone · module การตลาด · wave W1 · declaration = csq

1. `00_context/` — Brief (PREBRIEF) และ Function Checklist
2. `01_prototype/` — HTML Prototype (ต้นแบบจริง)
3. `02_qc/` — รายงาน UX และ Coverage (รอบ 1 + รอบ 2)
4. `03_brd/` — BRD Markdown และ Word
5. `04_frd/` — FRD Pack (10 ไฟล์)
6. `05_ui-brief/` — HTML UI Brief
7. `08_tldr/` — หน้าสรุปฟีเจอร์แบบอ่านง่าย
8. `09_declarations/` — CSQ declaration (declare-only, 7 events)
9. `10_handoff/` — Handoff, Proposals และ Pending Registry
10. `testcase_qa/` — AI Test Cases และ UAT สำหรับ Manual Test
11. `11_context-card/` — Feature Context Card (technical contract ย่อ สำหรับ cross-feature reference)

> ไม่มี `06_print/` เพราะฟีเจอร์นี้ไม่มีเอกสารพิมพ์ (WF-01 step 2 ข้ามได้ตัวเดียว)

เริ่มตรวจงานที่ `01_prototype/consent-pdpa.html` และเริ่ม Manual Test ที่ `testcase_qa/ความยินยอม PDPA HTML Testcase.html`
อ่านสรุป handoff + สิ่งที่ต้องเคาะก่อน dev/launch ที่ `10_handoff/HANDOFF.md`
