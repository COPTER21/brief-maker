# HANDOFF — F-ACC-CN ใบลดหนี้ลูกค้า (Credit Note · F096)

เปิดไฟล์ตามลำดับนี้เพื่อไม่ต้องไล่หาเอกสารจาก root

1. `01_prototype/F-ACC-CN_credit-note.html` — หน้าจอต้นแบบสำหรับทดลองใช้งาน
2. `testcase_qa/ใบลดหนี้ลูกค้า HTML Testcase.html` — คู่มือ Manual Test พร้อมภาพและช่องบันทึกผล
3. `08_tldr/FEATURE_TLDR_F-ACC-CN.html` — หน้าสรุปฟีเจอร์แบบอ่านง่าย (เริ่มที่นี่ถ้ายังไม่รู้จัก feature)
4. `README.md` — สารบัญชุดเอกสารที่จัดหมวดแล้ว
5. `10_handoff/PROPOSALS_outbound.md` — คำถามและข้อเสนอที่ต้องส่ง PM/BA

## หมวดเอกสาร

1. `00_context/` — PREBRIEF, Function Checklist, Context Card
2. `02_qc/` — รายงานตรวจหน้าจอ (qc-ux) และ Coverage รอบ 1/2
3. `03_brd/` — BRD Markdown และ Word
4. `04_frd/` — FRD Pack
5. `05_ui-brief/` — UI Brief สำหรับส่งต่อทีมพัฒนา
6. `06_print/` — Template และตัวอย่าง PDF (ม.86/10)
7. `08_tldr/` — หน้าสรุปฟีเจอร์แบบอ่านง่าย
8. `09_declarations/` — DOA, NTF, CSQ, DOCCFG declarations
9. `10_handoff/` — ข้อเสนอ ประเด็นค้าง และสถานะ Pending Registry
10. `testcase_qa/` — AI Test Cases และ UAT สำหรับผู้ใช้

## สถานะ gate (ตอนปิดงาน)

- audit FAIL=0 · qc-ux PASS · coverage R1 PASS (FN 22/22) · coverage R2 PASS (FN↔TC 22/22, ไม่มี DIVERGENCE) · e2e 33/33
- Declarations รอบนี้: DOA + NTF + CSQ + DOCCFG (+ pdfdoc = step 2 print)

ไฟล์เอกสารหลักบางไฟล์ยังอยู่ที่ root ของ `outputs/F-ACC-CN/` เพื่อเป็น canonical ตาม CUBE workflow (C3.6) และรักษาลิงก์จากรายงานเดิม
