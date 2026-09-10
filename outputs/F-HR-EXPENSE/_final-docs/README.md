# เบิกค่าใช้จ่าย (Expense Claim · F101) — Final Documents

ชุดนี้จัดหมวดตาม pattern ของ `outputs/17_Delivery-Note/_final-docs` สำหรับส่ง PM/BA, Dev และ Tester
(สำเนาจัดหมวด — ต้นฉบับยังอยู่ที่ระดับนอกสุดของ `outputs/F-HR-EXPENSE/`)

1. `00_context/` — PREBRIEF + Function Checklist (บรีฟต้นทาง)
2. `01_prototype/` — HTML Prototype (`expense.html`)
3. `02_qc/` — รายงาน UX + Coverage รอบ 1 + รอบ 2
4. `03_brd/` — BRD Markdown + Word
5. `04_frd/` — FRD Pack (00–07 + INDEX) + `CTX_F-HR-EXPENSE.md` (context card ย่อ — technical contract สำหรับอ้างข้าม feature)
6. `05_ui-brief/` — HTML UI Brief
7. `06_print/` — Template + ตัวอย่างใบเบิก PDF + print-spec
8. `08_tldr/` — หน้าสรุปฟีเจอร์แบบอ่านง่าย (ELI5)
9. `09_declarations/` — DOA + DOCCFG + Notification declarations
10. `10_handoff/` — Handoff, Proposals/OQ + Pending Registry (BASE-KIT)
11. `testcase_qa/` — AI Test Cases + UAT สำหรับ Manual Test

เริ่มตรวจงานที่ `01_prototype/expense.html` · อ่านสรุปเร็วที่ `08_tldr/FEATURE_TLDR_เบิกค่าใช้จ่าย.html` · เริ่ม Manual Test ที่ `testcase_qa/เบิกค่าใช้จ่าย HTML Testcase.html`

> **หมายเหตุปิดงาน:** ผ่าน WF-01 ครบ 12 step (e2e 48/48 · qc-ux PASS · coverage R1+R2 PASS) · FN = **25** (เพิ่ม FN-18/19/20 = 3 จุดเชื่อมตาม PM/BA 2026-09-10) · declarations = doa + doccfg + ntf
> **ค้างให้ BA เคาะ** (ดู `10_handoff/PROPOSALS_outbound.md`): CL-0013 สายผู้บริหารแขวน + DOA role-id · เลขเอกสาร พ.ศ./ค.ศ. + global-vs-branch · reverse-EC เมื่อยกเลิกหลังอนุมัติ · CSQ config · **PREBRIEF/FUNCTION_CHECKLIST ต้นทางยังเป็น 22 FN — ต้องอัปเป็น 25**
