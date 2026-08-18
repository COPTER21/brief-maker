# UX Check Report — Promotion

- วันที่ตรวจ: 18 สิงหาคม 2569
- Artifact: `outputs/15_Promotion/Promotion.html`
- ต้นทางหลัก: `Pack Brief Feature/Promotion/f-promotion.html`
- Route: `#/promotions`
- Viewports: 1440×900 และ 1024×768

## Verdict: 🟡 FUNCTIONAL PASS / V8 CONFORMANCE WARN

ไฟล์ output สืบทอดโครง หน้าตา และ business behavior จาก HTML ต้นทาง แล้วแก้เฉพาะ defect ที่พบจาก manual test ใน output เท่านั้น ปัจจุบันขนาด 207,807 bytes, MD5 `c86bdc54e1d86816bfd96588a37c2eb7` และ flow ผ่าน E2E 38/38 สองรอบโดยไม่มี console error

อย่างไรก็ตาม self-audit ของ `html-generator-v8` ยังแจ้ง technical debt ที่ติดมากับ seed จึงไม่บันทึกเป็น V8 PASS เท็จ รายการเหล่านี้ไม่พบว่าเป็น functional bug จากรอบ E2E แต่ต้องตัดสินใจแยกหากต้องการ normalize seed ให้ผ่านกฎ V8 ทุกข้อ

## Automated Evidence

| Check | ผล | Evidence |
|---|---|---|
| Seed lineage | ✓ | ใช้ `f-promotion.html` เป็นฐาน; diff รอบนี้จำกัดที่ defect fixes และ regression hooks |
| Feature E2E รอบ 1 | ✓ | 38/38 FN, console error 0 |
| Feature E2E รอบ 2 | ✓ | 38/38 FN, console error 0 |
| Static UX scan | ✓ | hash route, hashchange, Escape, backdrop, drawer transform, disabled/confirm markers ถูกตรวจพบ |
| Desktop render | ✓ | `_render-fixed-1440.png`, `_timeline-fixed.png`, `_simulator-fixed.png`, `_bundle-fixed.png` |
| Adaptive render | ✓ | `_render-fixed-1024.png`; ตารางใช้ horizontal scroll ภายใน card |
| HTML v8 self-audit | ⚠ | seed ยังมี finding ด้าน token/layout/style ตามตารางด้านล่าง |

## Seed Findings ที่ยังเปิดอยู่

| Finding | จำนวน | หมายเหตุ |
|---|---:|---|
| spacing token นอกชุด | 89 | อยู่ใน CSS/inline layout เดิมของ seed และ style เฉพาะตาราง |
| font size/family เกินชุด | 12 / 19 sizes | ไม่พบข้อความหายในการ render |
| flex ไม่มี align / grid ไม่มี gap | 4 / 3 | ต้อง refactor CSS หากจะปิด audit |
| inline layout style | 87 | seed ใช้ template string จัด layout จำนวนมาก |
| ad-hoc z-index / off-palette hex | 9 / 7 | overlay ยังทำงานผ่าน E2E |
| naked hint / long banner | 5 / 12 | เป็นข้อความคำอธิบายธุรกิจใน seed และคำอธิบายผล simulator |
| missing dynamic id | 2 | `cbi-` และ `cbx-` เป็น prefix ของ ID ที่ประกอบ runtime; DOM จริงมี ID ครบ |
| full-width select / custom tabs / fat td | 1 / 6 / 1 | โครง UI เดิมของ seed |

## Visual/Behavior Review

- หน้า list ใช้แท็บสถานะ 7 รายการ ไม่มี KPI cards ซ้ำ
- ปุ่ม “ใกล้สิ้นสุด” เป็น conditional hook จาก seed และจะแสดงเมื่อมีรายการ active เหลือ 0–14 วัน; mock ปัจจุบันไม่มีรายการเข้าเงื่อนไขจึงไม่แสดง
- create drawer มี 3 ขั้นและ editor 4 ชนิด
- detail drawer มี 4 แท็บและ fact 6 ช่อง
- DOA เป็นลำดับตำแหน่ง 2 ขั้น ไม่มีวงเงิน
- basket simulator เพิ่ม/ลบบรรทัดและคำนวณ line discount, free goods, threshold, bundle, coupon, priority, TA net และ quota ได้

## Findings ที่ปิดจาก Manual Test

| Finding | ผลการแก้และหลักฐาน |
|---|---|
| ตัวกรองขอบเขตเลือกไม่ได้ | แยก `any` = ทุกขอบเขต ออกจาก `all` = ทุกลูกค้า; E2E เลือกทุกลูกค้า → กลุ่ม → ช่องทาง → ทุกขอบเขตได้จริง |
| เส้น DOA/audit timeline ผิดแนว | แยก `.audit-timeline` ออกจาก label `.tl` และวัดเส้นตรงกึ่งกลางจุดทุกจุด |
| Coupon พิมพ์ได้ทีละตัว | รักษา focus/caret หลังคำนวณใหม่; E2E พิมพ์ `WELCOME100` ต่อเนื่อง |
| ตารางตะกร้าสินค้าทับหน่วย | กำหนด colgroup 7 คอลัมน์และให้ชื่อสินค้าห่อบรรทัด; geometry check ไม่ overlap |
| Dropdown เพิ่มสินค้า scroll ไม่ได้ | ไม่ render portal ซ้ำเมื่อ scroll ภายใน menu; E2E ยืนยัน scrollTop เปลี่ยนได้ |
| ข้อความ simulator เป็นศัพท์เทคนิค | เปลี่ยน header/footer และคำอธิบายลำดับเป็นภาษาผู้ใช้ |
| Search icon ใน Bundle ทับข้อความ | คืน padding 34px ให้ input combobox ภายในตาราง; geometry/computed-style check ผ่าน |

## Scope Note

- รอบนี้แก้เฉพาะ output ตาม defect ที่ผู้ใช้พบ; ไฟล์ใน `Pack Brief Feature/Promotion` ไม่ถูกแก้
- Promotion ไม่มี printable A4 document จึงข้าม `thai-doc-pdf-generator`
