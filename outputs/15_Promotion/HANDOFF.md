# Promotion — Handoff

โครงสร้างเอกสารนี้ใช้ pattern เดียวกับ `outputs/05_Sales_Territory` โดยแยกไฟล์ตามขั้นตอนการผลิต และมีชุดพร้อมส่งรวมอยู่ใน `_final-docs/`

| Folder | เนื้อหา |
|---|---|
| `01_HTML/` | HTML prototype ซึ่งเป็น UI source of truth และ generation log |
| `02_QC/` | UX, coverage, AI review และ UAT selection reports |
| `03_BRD/` | BRD Markdown และ DOCX |
| `04_FRD/` | FRD Pack |
| `05_UI_BRIEF/` | UI brief สำหรับ dev |
| `testcase_qa/` | AI test cases และ QA-friendly/UAT HTML สำหรับ tester |
| `08_TLDR/` | Feature TL;DR |
| `09_DECLARATIONS/` | DOA declaration สำหรับนำไปตั้งค่าที่ Policy Center |
| `10_HANDOFF/` | ข้อเสนอเชื่อมต่อ งานอนาคต และ open-question recap |
| `_final-docs/` | สำเนาเอกสารที่จำเป็นสำหรับส่งต่อ เรียงตามลำดับอ่าน |

## สถานะตรวจรับ

- PM/BA อนุมัติ HTML แล้ว
- Feature E2E ผ่าน 38/38 จำนวน 2 รอบ
- UX gate ผ่าน
- Coverage รอบ 1 และรอบ 2 ผ่าน
- UI Brief verification ผ่าน
- AI test cases 55 เคส / 173 ขั้น
- Manual UAT Lite 31 เคส / 67 ขั้น พร้อมภาพ 12 จุด
- UAT และ TL;DR เปิดแบบ offline ได้โดยไม่มี JavaScript error

## Declaration รอบนี้

- ใช้ `doa-declaration`: ไม่มีวงเงิน, อนุมัติตามลำดับ, อ่านจากการตั้งค่าส่วนกลาง
- ข้าม `doccfg-declaration` และ `ntf-declaration` ตามคำสั่งผู้ใช้

Raw results, screenshots, capture data, E2E scripts และ zip เก่าอยู่ที่ `test-artifacts/15_Promotion/` และไม่รวมใน deliverable pack
