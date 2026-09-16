# F-WH-STKADJ · Stock Adjustment (ใบปรับยอดสต๊อก · F082) — Final Docs

> ชุดเอกสารส่งมอบครบทุก step ของ WF-01 (12 step) จัดหมวดเป็นโฟลเดอร์ตามลำดับงาน
> pack นี้เป็น **สำเนาจัดระเบียบ** ของ deliverable ที่อยู่นอกสุดใน `outputs/F-WH-STKADJ/` (ไฟล์ทำงานเดิมยังอยู่ที่เดิม)
> สถานะ: **ครบ 12 step** · gate ล่าสุด qc-ux PASS · coverage R1+R2 PASS FN 55/55 · e2e 58/58 · วันที่ 2026-09-16

## แผนผังโฟลเดอร์

| โฟลเดอร์ | เนื้อหา | เปิดอ่านเมื่อ |
|---|---|---|
| `00_context/` | PREBRIEF · FUNCTION_CHECKLIST (55 FN, .md+.html) · BASELINE | อยากรู้ scope/ธุรกิจ/รายการ FN |
| `01_prototype/` | `F-WH-STKADJ.html` — ต้นแบบ (source of truth) | อยากลองจอจริง |
| `02_qc/` | รายงานตรวจ: UX check · coverage R1 · coverage R2 · WF ticks | เช็คว่าผ่าน gate จริง |
| `03_brd/` | BRD (.md + .docx) | เอกสารธุรกิจฉบับเต็ม |
| `04_frd/FRD_Pack/` | FRD 9 ไฟล์ (UI/API/LOGIC/DB/RULES/TESTS/LOCKED + OVERVIEW + INDEX) | dev อ่านสเปคจริง |
| `05_ui-brief/` | UI Brief (สกัดจาก HTML 1:1) | dev ทำ UI ให้ตรงจอ |
| `06_print/` | เอกสารพิมพ์ A4: print-spec · sample.pdf · template.html | ใบปรับยอดฉบับพิมพ์ |
| `07_context-card/` | CTX — technical contract ฉบับย่อ (entities/API/shared rules) | แนบเป็น cross-feature reference ตอนบรีฟ feature อื่น (แทน FRD เต็ม) |
| `08_tldr/` | Feature TL;DR (ELI5, เปิด browser) | อ่าน 2 นาทีเข้าใจฟีเจอร์ |
| `09_declarations/` | ใบประกาศ DOA · DOCCFG · NTF · CSQ | dev เอาไปตั้งค่าระบบกลาง |
| `10_handoff/` | HANDOFF · PROPOSALS_outbound · PENDING_REGISTRY extract | ปิดงาน + OQ ค้าง + BASE-KIT ที่รอแก้ |
| `testcase_qa/` | UAT (`ปรับยอดสต๊อก HTML Testcase.html`) · AI testcases (.md) | ทดสอบ/รัน AI test |

## ⚠️ ก่อนส่ง dev — เรื่องค้างที่ต้องเคาะ (ดูละเอียดใน `10_handoff/PROPOSALS_outbound.md`)
1. 🔴 **BA reference 2 ตัวเก่าค้าง ขัดมติ re-gate ของ BA เอง** — `5_DECLARATIONS/DOA_BRIEF`(reversal ไม่ผ่าน DOA) + `NTF_BRIEF`(cancel รวม approved) ยังเป็นก่อน FIX-02/03 → **pack นี้ยึดมติล่าสุดแล้ว** ขอ BA อัปเดตไฟล์ตัวเอง
2. coverage R2 3 WARN (doc cross-ref drift · non-blocking): TC-W204 stale cite · VR-16/17 cross-ref · subtable 117 vs 116
3. declaration Open Questions ส่ง owner (DOA cut-points/role-id · DOC-Q6 snapshot trigger · CSQ AC/W5 · NTF threshold)

## สิ่งที่ฟีเจอร์นี้ **ไม่** ทำ (scope)
ไม่ย้าย/โอนของข้าม bin/คลัง (=Stock Transfer F083) · ไม่นับสต๊อก/cycle count · ไม่มี VAT · ไม่ลงบัญชีจริง (mock `FWD-WIRE`) · ตั้งเลขรัน/วงเงิน/สายอนุมัติในหน้านี้ไม่ได้ · ไม่มี lot/serial/CSV import
