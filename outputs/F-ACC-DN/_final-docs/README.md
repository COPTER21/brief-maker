# Debit Note (ใบลดหนี้ผู้ขาย) — Final Documents

ชุดนี้จัดหมวดตาม pattern ของ `outputs/17_Delivery-Note/_final-docs` สำหรับส่ง PM/BA, Dev และ Tester
(F-ACC-DN · F097 · WF-01 ครบ 12 step · ทุก gate เขียว · AP/ฝั่งซื้อ mirror ของ F-ACC-CN)

1. `00_context/` — PREBRIEF, Function Checklist และ Context Card (CTX)
2. `01_prototype/` — HTML Prototype
3. `02_qc/` — รายงาน UX (qc-ux) และ Coverage รอบ 1/2
4. `03_brd/` — BRD Markdown และ Word
5. `04_frd/` — FRD Pack (9 ไฟล์)
6. `05_ui-brief/` — UI Brief สำหรับส่งต่อทีมพัฒนา
7. `06_print/` — Template, print-spec และตัวอย่างใบลดหนี้ PDF (ม.86/10)
8. `08_tldr/` — หน้าสรุปฟีเจอร์แบบอ่านง่าย
9. `09_declarations/` — DOA, NTF, CSQ และ DOCCFG declarations + index
10. `10_handoff/` — Handoff, Proposals และ Pending Registry
11. `testcase_qa/` — AI Test Cases (102) และ UAT HTML สำหรับ Manual Test

เริ่มตรวจงานที่ `01_prototype/F-ACC-DN_debit-note.html` และเริ่ม Manual Test ที่ `testcase_qa/ใบลดหนี้ผู้ขาย HTML Testcase.html`
