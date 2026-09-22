# _COVERAGE_R1 — F-ACC-DN · **Verdict: PASS**
| Graph | hook | evidence | ผล |
|---|---|---|---|
| edge APINV→DN (in) | step 1 ตารางใบตั้งหนี้ค้างจ่าย (ap_open_item) · ref tab | `#src-rows` · tab ref | ✓ |
| ext RTV W3-LITE | step 2 select ใบคืนสินค้า (เหตุผลคืนของ) | `#f-rtv` | ✓ mock |
| ext PV / VAT ซื้อ / JE | ref tab: ภาษีซื้อติดลบ · รายการบัญชี (จำลอง) · DEMO จ่ายชำระ | tab ref | ✓ mock |
| scope creep | ไม่มีหน้า AP/RTV/PV/JE จริง | — | ✓ |
| FN | evidence (pw_dn 30/30) |
|---|---|
| FN-01/03 | เลือก API-0046 → ผู้ขาย/ใบกำกับเดิม/บรรทัดดึงมา · ตารางแสดง ยอดสุทธิ/จ่าย+ลดหนี้แล้ว/คงค้าง |
| FN-02 | tile "ลดหนี้ไม่อ้างใบ" → toast OQ-DN-01 |
| FN-04 | API-0038 (จ่ายครบ) ไม่อยู่ใน `#src-rows` |
| FN-05 | เหตุผลคืนสินค้า → `#f-rtv` บังคับ · pickRTV ตั้งจำนวน/เพดาน |
| FN-06 | OVERPRICE 5,000 > 4,100 → `.line-meta.bad` "ราคาลดเกินราคาเดิม" |
| FN-07 | ลบบรรทัด + ปุ่มคืน "บรรทัดจากใบเดิมที่ไม่ได้ลด" |
| FN-08 | meta "ลดจำนวนได้อีก 15" (60 − 10 รอ − 35 รอ) |
| FN-09 | 16 > 15 → qty-over + toast บล็อก · hard-warn เมื่อยอดเกินคงเหลือ |
| FN-10 | `#f-reasonText.is-error` < 10 |
| FN-11/12 | step5 การ์ด DOA · slot บังคับ · R4 2 ขั้น → DN-2026-0014 |
| FN-13/14 | R5 ไม่อนุมัติ → ร่าง + "รอบก่อนหน้า" · ผู้ส่งไม่มีปุ่ม |
| FN-15/16 | R6 ยกเลิก · DN-0014 ส่งให้ผู้ขาย → "ส่งผู้ขายแล้ว" |
| FN-17 | DEMO จ่าย 300,000 → CFO อนุมัติไม่ได้ |
| FN-18 | ref tab: คงค้างก่อน/หลัง · input_vat_line ติดลบ · JE (Dr เจ้าหนี้ · Cr สินค้า/ผลต่าง · Cr 1170 ภาษีซื้อ) |
| FN-90..92 | filter 3 + stat · audit · PDF อ้างเลขใบกำกับผู้ขาย + มูลค่าเดิม/ถูกต้อง/ผลต่าง/ภาษีของผลต่าง + เหตุผล |
Declarations: chip doa/ntf/csq/doccfg/pdfdoc = detect ✓ · DIVERGENCE 0
