# Implementation Handoff — F-WH-PACK Packing

## สถานะส่งมอบ

เอกสารสำหรับ AI Coding Agent พร้อมใช้งาน โดยยึด HTML ต้นทางตามสภาพภายใต้ UX waiver และใช้ Picking final เป็น contract ต้นน้ำเพียง feature เดียว ส่วน Delivery Note และ Transfer ถูกกั้นเป็น unresolved boundary ห้ามเดา

## ลำดับอ่านสำหรับ Coding Agent

1. `08_TLDR/FEATURE_TLDR_F-WH-PACK.html` — เข้าใจภาพรวมและขอบเขต
2. `03_BRD/BRD_F-WH-PACK_Packing.md` — เป้าหมายธุรกิจและ scope
3. `04_FRD/FRD_F-WH-PACK_Pack/INDEX.md` — จุดเริ่ม FRD และลำดับอ่านทุก layer
4. `f-wh-packing.html` + `05_UI_BRIEF/UI_BRIEF_F-WH-PACK.md` — หน้าจอที่ต้องทำให้พฤติกรรมตรงกัน
5. `09_DECLARATIONS/NTF_BRIEF_F-WH-PACK.md` — event แจ้งเตือนที่ feature นี้ประกาศ
6. `06_PRINT/` — ป้ายกล่องและใบแพ็คสินค้า
7. `testcase_qa/testcases-F-WH-PACK.md` — AI test cases ฉบับเต็ม
8. `UAT_F-WH-PACK_Packing.html` — UAT Lite สำหรับผู้ใช้
9. `02_QC/` และ `10_HANDOFF/PENDING_REGISTRY.md` — gate, waiver และเรื่องห้ามเดา

## Scope lock ที่ต้องรักษา

- งานแพ็คเกิดจาก Picking สถานะ `to_pack` และแยกหนึ่งงานต่อหนึ่ง source SO
- เปิดกล่องที่ยังไม่ปิดได้ครั้งละหนึ่งกล่อง
- ห้ามแพ็คเกินจำนวนที่หยิบมา และต้องรักษาล็อต/ตำแหน่ง/ใบขายต้นทาง
- ปิดงานได้เมื่อของครบและไม่มีกล่องเปิด
- การยกเลิกต้องมีเหตุผลและงานกลับคิว
- BOXLABEL เป็น 150×100 มม.; PACKSLIP เป็น A4 และไม่ใช่เอกสารภาษี
- Delivery Note ใน HTML เป็น mock; ห้ามเชื่อมจริงจน PACK-OQ-DN-01 ปิด
- Transfer ไม่อยู่ใน contract รอบนี้

## Quality status

- UX: `WAIVED-BLOCK` — ใช้ HTML ตามสภาพ; ไม่แก้ HTML
- Coverage round 1: `WARN — proceed with guarded boundaries`
- Coverage round 2: `PASS WITH GUARDED OQs`
- AI tests: 40 cases / 101 steps
- UAT Lite: 19 cases / 43 steps / 6 screenshot regions
- Feature TL;DR gate: PASS
- UI Brief shared verifier: not run because script is absent; recorded as PACK-TOOL-01
- Feature E2E suite: ไม่ได้รัน เพราะอยู่นอก workflow skills ที่ผู้ใช้อนุญาตในรอบนี้

## Declaration รอบนี้

`ntf-declaration` เท่านั้น: `pack_started`, `pack_box_closed`, `pack_done`, `pack_cancelled`

ไม่ใช้ `doa-declaration` และ `doccfg-declaration` ตามคำสั่งผู้ใช้

