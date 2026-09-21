# E2E Result — F-WH-STOCKTAKE

- วันที่: 2026-09-20
- Runner: `_e2e/e2e-stocktake.py`
- Browser: Chromium · 1440×900
- Result: **PASS 20/20**
- FN covered: **12/12**
- FN-40 rendered negative: **0/0** (checklist ไม่มี FN-40)
- Console errors: **0**
- PM/BA bypass cases: **B1/B2/B3 PASS**
- External CDN messages ignored by shared `uikit.py`: 63

| Case | Result | พิสูจน์ |
|---|:---:|---|
| FN-01 | PASS | ค้นหา/เลือกพื้นที่และสร้างรอบ |
| FN-02 | PASS | รายการสินค้า + ตำแหน่ง |
| FN-03 | PASS | block parent/child overlapping scope |
| FN-04 | PASS | snapshot immutable |
| FN-05 | PASS | assign person |
| FN-06 | PASS | counter blind / supervisor reveal |
| FN-07 | PASS | zero accepted; blank/negative blocked |
| FN-08 | PASS | equality vs greater-than threshold |
| FN-09 | PASS | independent recount assignee |
| FN-10 | PASS | DOA slot + reject reason + audit |
| FN-11 | PASS | adjustment draft + no on-hand mutation + unlock |
| FN-12 | PASS | no Cycle Count ABC surface |
| B1 | PASS | freeze ซ้ำบน counting ไม่เปลี่ยน status/freezeAt/snapshot |
| B2 | PASS | handoff ก่อน approved ถูก block และ lock ยังอยู่ |
| B3 | PASS | counter approve bypass ไม่ได้; approver จริงบน pending ทำได้ |
| FIX-04 | PASS | 25,000 บาท resolve 2 ขั้น; P3 → P4 ทีละขั้น |
| FIX-07/08 | PASS | F089 scan surface + ซ่อน demo-only แล้ว layout ไม่พัง |
| UI-01 | PASS | ปุ่ม “สแกน” กับ “ส่งผลนับ” เว้นช่องไฟอย่างน้อย 8px |
| UI-02 | PASS | สรุปส่งต่อใบปรับยอดเป็น section แบน ไม่มี card ซ้อน card |
| SEC-01 | PASS | เฉพาะผู้ได้รับมอบหมายเท่านั้นที่เห็น controls และส่งผลนับได้ |

Regression proof ก่อนแก้: UI-01 FAIL ที่ gap 0px · UI-02 FAIL เพราะพบ `.card section-pad` ซ้อนกัน 1 จุด

คำสั่ง rerun:

`.tools\python.cmd outputs\F-WH-STOCKTAKE\_e2e\e2e-stocktake.py outputs\F-WH-STOCKTAKE\F-WH-STOCKTAKE.html`
