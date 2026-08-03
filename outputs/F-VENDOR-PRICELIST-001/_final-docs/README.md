# Vendor Price List — Final Documentation Pack

ชุดเอกสารส่งมอบสำหรับ Feature ID `F-VENDOR-PRICELIST-001` เพื่อใช้เป็นข้อมูลอ้างอิงสำหรับ Project Manager, Business Analyst, Developer, AI Coding Agent และผู้ทดสอบระบบ

## เอกสารในชุดส่งมอบ

| ลำดับ | เอกสาร | วัตถุประสงค์ |
|---|---|---|
| 1 | [BRD_VendorPriceList_v2.4.md](BRD_VendorPriceList_v2.4.md) | ขอบเขตทางธุรกิจ เป้าหมาย และข้อกำหนดหลักของฟีเจอร์ |
| 2 | [vendor-price-list-v6.html](vendor-price-list-v6.html) | HTML Prototype ซึ่งเป็นแหล่งอ้างอิงหน้าจอและพฤติกรรม UI |
| 3 | [FRD_F-VENDOR-PRICELIST-001_Pack/INDEX.md](FRD_F-VENDOR-PRICELIST-001_Pack/INDEX.md) | จุดเริ่มต้นของ FRD Pack สำหรับ UI, API, Logic, Database, Rules และ Tests |
| 4 | [UI_BRIEF_F-VENDOR-PRICELIST-001.md](UI_BRIEF_F-VENDOR-PRICELIST-001.md) | รายละเอียด UI ที่สกัดจาก HTML Prototype สำหรับการพัฒนาหน้าจอให้ตรงต้นแบบ |
| 5 | [testcases-vendor-price-list.md](testcases-vendor-price-list.md) | Test Case แบบ Markdown สำหรับ AI Testing Agent จำนวน 62 เคส 303 ขั้นตอน |
| 6 | [testcase-vendor-price-list.html](testcase-vendor-price-list.html) | แบบทดสอบฉบับผู้ใช้ เปิดใช้งานได้ทันที บันทึกผลและดาวน์โหลดรายงาน PDF ได้ |
| 7 | [qa-friendly-work/](qa-friendly-work/) | Source data, screenshot bundle, template และสคริปต์สำหรับสร้างหรือตรวจ QA-friendly HTML ซ้ำ |

## ลำดับที่แนะนำสำหรับ AI Coding Agent

1. อ่าน BRD เพื่อทำความเข้าใจเป้าหมายและขอบเขตทางธุรกิจ
2. อ่าน `FRD_F-VENDOR-PRICELIST-001_Pack/INDEX.md` และไฟล์ใน FRD Pack ให้ครบ
3. ใช้ HTML Prototype เป็นแหล่งอ้างอิงหน้าจอและ interaction ที่ต้องพัฒนา
4. ใช้ HTML UI Brief เพื่อตรวจ selector, state, overlay, route และข้อความบนหน้าจอ
5. ใช้ AI Test Case ตรวจ traceability และ acceptance criteria ระหว่างพัฒนา
6. ใช้ QA-friendly HTML สำหรับการทดสอบโดยผู้ใช้หรือ UAT

## ไฟล์สำหรับสร้างและตรวจ QA-friendly HTML ซ้ำ

โฟลเดอร์ `qa-friendly-work` เป็น build/reproducibility bundle ประกอบด้วย:

- `cases.json` — ข้อมูล Test Case ที่แปลงจาก Markdown
- `shot-spec.json` — ข้อกำหนดตำแหน่งภาพประกอบ
- `shots_b64.json` — ภาพประกอบที่เข้ารหัสเพื่อฝังในเอกสาร HTML
- `template-offline.html` — Template ที่ทำงานแบบ offline
- `generate_cases.py` — สคริปต์แปลง Test Case เป็นข้อมูลสำหรับเอกสารผู้ใช้
- `smoke_qa.py` — สคริปต์ตรวจการทำงานของ QA-friendly HTML
- `smoke-main.png` — ภาพผลตรวจหน้าหลักล่าสุด

เมื่อรัน Python หรือ Playwright ใน workspace นี้ ให้ใช้ `.tools/python.cmd` และ `.tools/playwright.cmd` ตามลำดับ

## Integration ที่ฟีเจอร์อ้างอิง

- คู่ค้าอ้างอิงข้อมูลที่ใช้งานจริงจาก `F-VENDOR`
- สินค้าและ Purchase UOM อ้างอิงจาก Item/Product Master
- การอนุมัติอ้างอิง Approval Tier, Threshold Policy และ DOA Configuration ของระบบ
- เอกสารจาก PR/RFQ/PO ต้องเก็บข้อมูลราคาและวิธีคำนวณ ณ เวลาที่นำราคาไปใช้ เพื่อป้องกันผลย้อนหลังเปลี่ยนตาม Price Version ใหม่

## หมายเหตุขอบเขตเอกสาร

ฟีเจอร์นี้ไม่มีเอกสารธุรกรรม A4 ที่ต้องออกเป็นแบบฟอร์มทางการ จึงไม่มีชุดไฟล์จาก `thai-doc-pdf-generator` ส่วนไฟล์ QA-friendly HTML สามารถสร้างและดาวน์โหลดรายงานผลทดสอบเป็น PDF ได้ภายในตัวเอง

## สถานะการตรวจเอกสาร QA

- Test Case: 62 เคส
- ขั้นตอนทดสอบ: 303 ขั้นตอน
- กลุ่มการทดสอบ: 8 กลุ่ม
- ภาพประกอบการทดสอบ: 10 จุด
- ผ่านการตรวจการเปิดเอกสาร การแสดงข้อมูลตัวอย่าง การบันทึกผลในเครื่อง การสร้างหน้าสรุป และการดาวน์โหลด PDF
- Smoke test รอบสุดท้ายไม่พบ console error หรือ page error

---

Package: `F-VENDOR-PRICELIST-001`  
Prepared: 3 สิงหาคม 2569
