# Performance (ประเมินผลงาน · F131) — Final Documents

ชุดนี้จัดหมวดตาม pattern เดียวกับ `outputs/17_Delivery-Note` สำหรับส่ง PM/BA, Dev และ Tester

1. `00_context/` — PREBRIEF และ Function Checklist
2. `01_prototype/` — HTML Prototype (จอจริง)
3. `02_qc/` — รายงาน UX และ Coverage (รอบ 1 + รอบ 2)
4. `03_brd/` — BRD Markdown และ Word
5. `04_frd/` — FRD Pack (9 ไฟล์ + INDEX)
6. `05_ui-brief/` — HTML UI Brief
7. `08_tldr/` — หน้าสรุปฟีเจอร์แบบอ่านง่าย (TL;DR)
8. `09_declarations/` — DOA / NTF / CSQ declarations
9. `10_handoff/` — HANDOFF, Proposals และ Pending Registry
10. `testcase_qa/` — AI Test Cases (md) และ UAT (HTML) สำหรับ Manual Test

- `CTX_F-HR-Performance.md` — Feature Context Card (technical contract ย่อ สำหรับอ้างอิงข้าม feature)

> ℹ️ ไม่มี `06_print/` — feature นี้ไม่มีเอกสารพิมพ์ A4 (master+cycle ไม่ใช่ Pattern Q)

**เริ่มตรวจงานที่** `01_prototype/performance.html`
**เริ่ม Manual Test ที่** `testcase_qa/ประเมินผลงาน HTML Testcase.html`

---
- Feature: F131 Performance · mod HR · wave W2 · archetype master+cycle
- Declarations: **doa + ntf + csq**
- Gate: qc-ux PASS · coverage PASS (R1+R2) · e2e 36/36 · audit FAIL=0
- 18 FN · 4 หน้าจอ · scope: staff=SELF / mgr=DEPT / HR=ALL
