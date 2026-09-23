# HANDOFF — F-ACC-DN ใบลดหนี้ผู้ขาย (Debit Note · F097)

เปิดไฟล์ตามลำดับนี้เพื่อไม่ต้องไล่หาเอกสารจาก root

1. `01_prototype/F-ACC-DN_debit-note.html` — หน้าจอต้นแบบสำหรับทดลองใช้งาน
2. `testcase_qa/ใบลดหนี้ผู้ขาย HTML Testcase.html` — คู่มือ Manual Test พร้อมภาพและช่องบันทึกผล
3. `08_tldr/FEATURE_TLDR_F-ACC-DN.html` — หน้าสรุปฟีเจอร์แบบอ่านง่าย (เริ่มที่นี่ถ้ายังไม่รู้จัก feature)
4. `README.md` — สารบัญชุดเอกสารที่จัดหมวดแล้ว
5. `10_handoff/PROPOSALS_outbound.md` — คำถามและข้อเสนอที่ต้องส่ง PM/BA

## หมวดเอกสาร

1. `00_context/` — PREBRIEF, Function Checklist, Context Card (CTX)
2. `02_qc/` — รายงานตรวจหน้าจอ (qc-ux) และ Coverage รอบ 1/2
3. `03_brd/` — BRD Markdown และ Word
4. `04_frd/` — FRD Pack (9 ไฟล์)
5. `05_ui-brief/` — UI Brief สำหรับส่งต่อทีมพัฒนา
6. `06_print/` — Template และตัวอย่าง PDF ใบลดหนี้ (ม.86/10)
7. `08_tldr/` — หน้าสรุปฟีเจอร์แบบอ่านง่าย
8. `09_declarations/` — DOA, NTF, CSQ, DOCCFG declarations + index
9. `10_handoff/` — ข้อเสนอ ประเด็นค้าง และสถานะ Pending Registry
10. `testcase_qa/` — AI Test Cases (102) และ UAT สำหรับผู้ใช้

## จุดต่างสำคัญจากฝั่งลูกค้า (F-ACC-CN Credit Note)

- ฝั่ง **ผู้ขาย/AP** · **ภาษีซื้อ (input VAT) ค่าลบ** · prefix **DN-YYYY-NNNN**
- **ใบตั้งหนี้ที่จ่ายครบแล้วยังออก DN ได้** → ส่วนเกินหนี้ค้าง = **เครดิตคงเหลือกับผู้ขาย** (เพดาน = มูลค่าที่ลดได้ `dnRoom` ไม่หัก paid) — FN-20
- **ภาษีซื้อกลับเมื่อได้รับใบลดหนี้จากผู้ขาย** (กรอกเลขที่+วันที่ vendorCn → เดือนภาษี = วันที่ได้รับ · ม.82/10) — FN-21
- ส่วนลดท้ายบิล + ปรับ VAT ม.86/10 — FN-19

## สถานะ gate (ตอนปิดงาน)

- audit FAIL=0 · qc-ux PASS · coverage R1 PASS (FN 24/24) · coverage R2 PASS (FN↔TC 24/24, ไม่มี DIVERGENCE) · e2e 36/36 · console 0
- Declarations รอบนี้: DOA + NTF + CSQ + DOCCFG (+ pdfdoc = step 2 print)

ไฟล์เอกสารหลักบางไฟล์ยังอยู่ที่ root ของ `outputs/F-ACC-DN/` เพื่อเป็น canonical ตาม CUBE workflow (C3.6) และรักษาลิงก์จากรายงานเดิม — `_final-docs/` คือชุดสำเนาที่จัดหมวดสำหรับส่งมอบ
