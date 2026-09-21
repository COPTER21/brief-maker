# Final Docs — F-WH-STOCKTAKE

แพ็กเอกสารส่งมอบของ Stocktake รอบตรวจนับใหญ่ จัดหมวดตาม pattern ของ `outputs/17_Delivery-Note/_final-docs`

> ไฟล์ใน `_final-docs` เป็นสำเนาสำหรับส่งมอบ ส่วนไฟล์ต้นฉบับที่ feature root ยังคงไว้เพื่อไม่ให้ path ของ workflow/checker เดิมเสีย

| Folder | เนื้อหา |
|---|---|
| `00_context` | Function Checklist และ Context Card สำหรับอ้างอิงข้าม feature |
| `01_prototype` | HTML prototype ที่ผ่าน manual/E2E |
| `02_qc` | UX, Coverage, AI review และ E2E evidence report |
| `03_brd` | BRD Markdown และ Word |
| `04_frd` | FRD Pack ฉบับเต็ม |
| `05_ui-brief` | UI implementation brief |
| `08_tldr` | หน้าปกสรุปฟีเจอร์อ่านเร็ว |
| `09_declarations` | Declaration ที่ได้รับอนุมัติให้สร้างในรอบนี้ |
| `10_handoff` | ข้อเสนอ/Open Questions สำหรับส่งต่อ |
| `testcase_qa` | AI Test Cases, UAT HTML และ UAT drop ledger |

## เริ่มอ่าน

1. `08_tldr/F-WH-STOCKTAKE-TLDR.html` — เข้าใจฟีเจอร์แบบเร็ว
2. `01_prototype/F-WH-STOCKTAKE.html` — ทดลองหน้าจอ
3. `testcase_qa/testcase-F-WH-STOCKTAKE.html` — Manual UAT
4. `03_brd/BRD_F-WH-STOCKTAKE.docx` — ขอบเขตธุรกิจ
5. `04_frd/FRD_Pack/INDEX.md` — technical source of truth
6. `00_context/CTX_F-WH-STOCKTAKE.md` — context ย่อสำหรับแนบให้ feature อื่น/AI

## Verification snapshot

- E2E: 20/20 · FN 12/12 · console errors 0
- Coverage round 2: PASS
- UI Brief verifier: PASS
- UAT capture: 8/8 regions
- Feature TL;DR checker: PASS
- Declaration รอบนี้: `doa-declaration`
