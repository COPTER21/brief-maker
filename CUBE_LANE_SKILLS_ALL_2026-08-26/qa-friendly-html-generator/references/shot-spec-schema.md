# shot-spec.json — schema

บอก `capture.py` ว่าจะถ่ายภาพหน้าจอจุดไหนบ้าง. Claude เขียนไฟล์นี้โดย **อ่าน HTML prototype**
เพื่อหาว่า (1) JS ตัวไหนเปิดหน้าจอไหน (2) element ที่กำลังทดสอบมี selector / ข้อความอะไร
(3) container ที่นับเป็น "หน้าจอ" คืออะไร.

```jsonc
{
  "html": "prototype.html",     // path ของ HTML เทียบกับโฟลเดอร์ --pack
  "route": "#/sow",             // (ออปชั่น) location.hash เริ่มต้น
  "vw": 1200, "vh": 1000,       // ขนาด viewport ตอนถ่าย
  "device_scale": 2,            // DPR — 2 = ภาพคม (retina)
  "shots": [
    {
      "key": "create_positions",                 // = regionKey ใน cases.json
      "setup": ["startSow('create')"],           // JS รันในหน้าเพื่อไปยังสถานะนั้น (เรียงตามลำดับ)
      "wait": 400,                                // (ออปชั่น) ms รอหลัง setup แต่ละบรรทัด
      "container": "#drawer",                     // element ที่ screenshot (กรอบ "หน้าจอ")
      "target": {                                 // element ที่จะถูกไฮไลต์ (spotlight)
        "selector": ".drawer-section",
        "has_text": "ตำแหน่งที่รับงานได้"          // (ออปชั่น) ระบุชิ้นที่ข้อความตรง — กันเลือกผิด
      }
    }
  ]
}
```

## หลักการเขียน
- **หนึ่ง shot = หนึ่งสถานะ + หนึ่งจุดไฮไลต์.** capture.py reload หน้าใหม่ทุก shot → สถานะสะอาดเสมอ
- `setup` คือ JS ที่ทำให้ถึงหน้าจอนั้น เช่น `startSow('create')`, `openDrawer('view','SOW-0001')`,
  `openModal('archive','SOW-0004')` — **อ่านจาก HTML จริง** ว่าฟังก์ชันชื่ออะไร พารามิเตอร์อะไร
- `container` ปกติคือกรอบหลักของหน้าจอนั้น: list = `#page-content`, drawer = `#drawer`, modal = `#modal`
  (ชื่อจริงแล้วแต่ prototype — อ่านจาก HTML)
- `target.has_text` ช่วยมากเวลามีหลาย `.drawer-section` — ใส่คำที่ unique ในส่วนนั้น
- ตั้ง `key` ให้สื่อความ + จับคู่กับ `regionKey` ใน cases.json ให้ตรงเป๊ะ

## การจับคู่ step → region (งานของ Claude, กึ่งอัตโนมัติ)
1. อ่าน `expect` + `do` ของแต่ละ step → รู้ว่าผู้ทดสอบควรเห็นส่วนไหน **ณ ตอนนั้น**
2. จับคู่กับ component/section ใน FRD/HTML → ตั้งเป็น `regionKey`
3. หลาย step ที่เห็น "จุดเดียวกันจริง ๆ" ใช้ `regionKey` เดียวกันได้ (build.py จะ dedup ให้)
4. step ที่ไม่มีหน้าจอเฉพาะ (เช่น "ปล่อยให้ตารางเรียงตามค่าเริ่มต้น") → `regionKey = ""`

> ไม่ต้องครอบคลุมทุก step ด้วยภาพ — ใส่ภาพเฉพาะจุดที่ "ดูแล้วเข้าใจขึ้น" พอ

## ★ ภาพต้องตรงสถานะ step (R18) — จุดที่พลาดบ่อย
- **`setup` ของ shot ต้องพาหน้าจอไปถึง "สถานะหลังทำ step นั้นเสร็จ" เป๊ะ.** step ที่ลึก (เปิด drawer,
  เปิด tab ที่ 2, กรอกฟอร์มไปครึ่งทาง, กดจนขึ้น modal ยืนยัน) → `setup` ต้องมีคำสั่งพาไปจนถึงจุดนั้นจริง
  ไม่ใช่ปล่อยภาพหน้ารายการตื้น ๆ ไว้. อ่าน HTML ว่าต้องเรียกฟังก์ชัน/คลิกอะไรต่อกันบ้างเพื่อให้ถึงสถานะ.
- **ห้าม reuse `key` ของสถานะตื้นกับ step ที่เข้าไปลึกกว่า** เพียงเพื่อประหยัด — จะได้ภาพผิดจุด.
  ถ้าไม่มีภาพที่ตรงจริง ตั้ง `regionKey=""` ที่ step นั้น (ปุ่ม 👁 จาง) ดีกว่าโชว์ภาพผิด.
- **Verify หลัง capture (บังคับ):** capture.py พิมพ์สถานะ `[ok]/[skip]/[FAIL]` ต่อ key + เขียนไฟล์
  `--report` (เล็ก ไม่มี base64). ต้องอ่านสรุปนี้ทุกครั้ง: key ที่ `skip`/`FAIL` = target หาไม่เจอ/ไม่ขึ้น
  → มัก setup ไม่พาไปถึงสถานะ หรือ selector/has_text ผิด → **แก้ shot-spec แล้ว capture ใหม่** จนผ่าน.
  key สำคัญยัง fail ห้าม build.
