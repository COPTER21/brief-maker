# ESS Portal (F059 · พนักงานทำเอง) — Final Documents

ชุดนี้จัดหมวดตาม pattern ของ `outputs/17_Delivery-Note` สำหรับส่ง PM/BA, Dev และ Tester
(สำเนาจัดระเบียบของไฟล์ working ที่อยู่ชั้นนอก `outputs/F-HR-ESS/`)

1. `00_context/` — PREBRIEF และ Function Checklist (contract ของ feature)
2. `01_prototype/` — HTML Prototype (จอจริง · design A launcher · display-only)
3. `02_qc/` — รายงาน UX และ Coverage (รอบ 1 + รอบ 2)
4. `03_brd/` — BRD Markdown และ Word
5. `04_frd/` — FRD Pack (7 ไฟล์ · UI/API/LOGIC/DB/Rules/Tests)
6. `05_ui-brief/` — HTML UI Brief (มี §DEMO-ONLY บอก dev ตัดอะไรใน production)
7. `08_tldr/` — หน้าสรุปฟีเจอร์แบบอ่านง่าย (ELI5)
8. `09_declarations/` — NTF (consume-only) และ CSQ (SecC) — feature นี้ใช้ `ntf + csq` · ไม่มี doa/doccfg/pdf
9. `10_handoff/` — Handoff, Proposals (OQ ค้าง) และ Pending excerpt
10. `testcase_qa/` — AI Test Cases และ UAT สำหรับ Manual Test
11. `11_context-card/` — Feature Context Card (technical contract ย่อ สำหรับ cross-feature reference)

> ไม่มี `06_print` — ESS เป็น portal **display-only** ไม่มีเอกสารพิมพ์ (สลิป/หนังสือรับรอง PDF มาจาก feature ต้นทาง)

เริ่มตรวจงานที่ `01_prototype/ess.html` และเริ่ม Manual Test ที่ `testcase_qa/ESS พนักงานทำเอง HTML Testcase.html`
