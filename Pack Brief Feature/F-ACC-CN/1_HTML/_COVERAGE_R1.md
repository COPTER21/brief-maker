# _COVERAGE_R1 — F-ACC-CN · **Verdict: PASS**
| Graph | hook | evidence | ผล |
|---|---|---|---|
| edge ARINV→CN (in) | step 1 ตารางใบแจ้งหนี้คงค้าง (ar_open_item) · ref tab | `#src-rows` · tabBtn('ref') | ✓ |
| ext Sales Return W4-LITE | step 2 select ใบรับคืน (เหตุผลรับคืน) | `#f-sr` | ✓ mock |
| ext VAT Report / JE / RV | ref tab: ผลกระทบภาษีขาย · รายการบัญชี (จำลอง) · DEMO รับชำระ | ref tab | ✓ mock |
| scope creep | ไม่มีหน้า AR/SR/JE จริง | — | ✓ |
| FN | evidence (pw_cn 30/30) |
|---|---|
| FN-01/03 | เลือก INV-0140 → ลูกค้า/บรรทัดดึงมา · ตารางแสดง ยอดสุทธิ/ลดหนี้แล้ว/คงค้าง |
| FN-02 | tile "ลดหนี้ไม่อ้างใบ" → toast OQ-CN-01 |
| FN-04 | INV-0136 (ชำระครบ) · INV-0143 (void) ไม่อยู่ใน `#src-rows` |
| FN-05 | เหตุผลรับคืน → `#f-sr` บังคับ · pickSR ตั้งจำนวน/เพดานจากใบรับคืน |
| FN-06 | DISC ราคาลด 13,000 > 12,500 → `.line-meta.bad` "ราคาลดเกินราคาเดิม" |
| FN-07 | ลบบรรทัด + ปุ่มคืน "บรรทัดจากใบเดิมที่ไม่ได้ลด" (step3Block) |
| FN-08 | meta "ลดจำนวนได้อีก 7" (10 − CN-0021 1 − ร่าง 2) |
| FN-09 | qty 8 > 7 → qty-over + toast บล็อก · hard-warn เมื่อยอดรวมเกินคงเหลือ |
| FN-10 | `#f-reasonText.is-error` < 10 ตัว |
| FN-11 | step5 การ์ด DOA tier + submit modal slot บังคับเลือกคน |
| FN-12 | R4 อนุมัติ 2 ขั้น → CN-2026-0024 |
| FN-13 | ไม่อนุมัติ + เหตุผล → ฉบับร่าง + "รอบก่อนหน้า" ใน sign tab |
| FN-14 | ผู้ส่ง/คนที่ไม่ใช่ assignee ไม่เห็นปุ่มอนุมัติ |
| FN-15 | ยกเลิกร่าง R6 + เหตุผล |
| FN-16 | ส่งให้ลูกค้า → ส่งลูกค้าแล้ว |
| FN-17 | DEMO รับชำระ INV-0141 แล้วอนุมัติขั้นสุดท้าย → "อนุมัติไม่ได้" |
| FN-18 | ref tab คงค้างก่อน/หลัง · ภาษีขายที่ลด · JE จำลอง |
| FN-90..92 | filter/empty · audit append-only · PDF อ้างเลข+วันที่ใบเดิม/มูลค่าเดิม/ถูกต้อง/ผลต่าง/เหตุผล (pw) |
Declaration 0b: doa ✓ DOA_BRIEF · ntf ✓ · csq ✓ · doccfg ✓ (CN · ไม่ hardcode) — chip = detect (ไม่มี DIVERGENCE)
