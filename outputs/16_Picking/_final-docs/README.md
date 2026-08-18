# Picking — Final Handoff Pack

ชุดเอกสารพร้อมส่งต่อของฟีเจอร์ F-WH-PICK จัดหมวดตามลำดับการอ่าน โดยไฟล์ในชุดนี้เป็นสำเนาจาก canonical artifacts ที่อยู่บริเวณ root ของ `outputs/16_Picking/`

1. `00_context/` — PREBRIEF และ Function Checklist ต้นทาง
2. `01_prototype/` — HTML prototype ที่ PM/BA ตรวจแล้ว
3. `02_qc/` — รายงาน UX, coverage และ UAT selection audit
4. `03_brd/` — BRD รูปแบบ Markdown และ DOCX
5. `04_frd/` — FRD Pack แบบ FULL
6. `05_ui-brief/` — UI handoff สำหรับทีมพัฒนา
7. `06_print/` — Template, ตัวอย่าง PDF และ print specification ของใบหยิบ
8. `testcase_qa/` — AI test cases ฉบับเต็มและ UAT HTML สำหรับผู้ทดสอบ
9. `08_tldr/` — หน้าสรุปฟีเจอร์แบบอ่านง่าย
10. `09_declarations/` — Notification declaration
11. `10_handoff/` — ข้อเสนอส่งต่อและ Open Questions

## สถานะตรวจรับ

- PM/BA ตรวจ HTML แล้ว
- Feature E2E ผ่าน 14/14 และครอบคลุม FN 29/29
- UX gate และ coverage สองรอบผ่าน
- UI Brief verification ผ่าน
- UAT Lite มี 16 เคส พร้อมภาพ 12 จุด
- UAT และ TL;DR เปิดอ่านแบบ offline ได้

## Declaration รอบนี้

ใช้ `ntf-declaration` และออก `NTF_BRIEF_F-WH-PICK.md` แล้ว

ไม่ได้ใช้ `doccfg-declaration` และ `doa-declaration`

Raw results, screenshots, capture data และ E2E scripts ยังคงอยู่ที่ `_e2e/` และ `_qa/` นอกชุดส่งมอบนี้
