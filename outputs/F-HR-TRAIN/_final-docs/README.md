# Training (อบรม · F133) — Final Documents

ชุดนี้จัดหมวดตาม pattern ของ `outputs/17_Delivery-Note/_final-docs` สำหรับส่ง PM/BA, Dev และ Tester
(เป็นสำเนารวมชุด — ต้นฉบับยังอยู่นอกสุดของ `outputs/F-HR-TRAIN/`)

1. `00_context/` — PREBRIEF และ Function Checklist (ต้นทางเนื้อธุรกิจ)
2. `01_prototype/` — HTML Prototype (`อบรม.html`)
3. `02_qc/` — รายงาน UX + Coverage (รอบ 1 + รอบ 2)
4. `03_brd/` — BRD (Markdown + Word)
5. `04_frd/` — FRD Pack (9 ไฟล์)
6. `05_ui-brief/` — HTML UI Brief
7. `08_tldr/` — หน้าสรุปฟีเจอร์แบบอ่านง่าย
8. `09_declarations/` — DOA / NTF / CSQ declarations
9. `10_handoff/` — Proposals (OQ ส่งออก) + Pending Registry
10. `testcase_qa/` — AI Test Cases + UAT สำหรับ Manual Test
11. `CTX_F-HR-TRAIN.md` — Context Pack (technical contract ฉบับย่อ · แนบเป็น cross-feature reference เวลาออกบรีฟ feature อื่นที่อ้าง Rate Card/Expense/Performance โดยไม่ต้องแนบ FRD เต็ม)

> **ไม่มี `06_print/`** — ฟีเจอร์นี้ไม่มีเอกสารพิมพ์ (ใบรับรอง = soft ref ไม่มีเลขรัน/PDF ทางการ · step 2 ข้ามตามกติกา)

เริ่มตรวจงานที่ `01_prototype/อบรม.html` และเริ่ม Manual Test ที่ `testcase_qa/อบรม HTML Testcase.html`

---

**สถานะ:** ครบ 12 step · ผ่านทุก gate (audit FAIL=0 · qc-ux/coverage PASS · e2e 36/36 FN 18/18 · UI-brief PASS)
แก้ตาม BA review 7 FIX + manual test 4 bug + re-gate 2 รอบเขียว · declaration = doa+ntf+csq
