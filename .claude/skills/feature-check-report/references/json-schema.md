# report.json — schema

ทุก field optional ยกเว้นที่มี ★ · ตัวอย่างเต็ม: `assets/sample_report.json`

```jsonc
{
  "feature": { "code": "F-PO-001", "name": "ใบสั่งซื้อ", "module": "Purchase" },  // ★ code หรือ name อย่างน้อย 1
  "tester": "Gift (QA)",            // ★
  "date": "2026-09-30",             // ISO · ไม่ใส่ = วันนี้
  "round": 1,                       // รอบตรวจ · ไม่ใส่ = 1
  "env": "UAT", "build": "2026.09.28",
  "dev": "Bird", "reviewer": "Strike",
  "refs": "FRD v6.1 · TC 38 เคส",
  "summary_note": "",               // override เหตุผลในกล่องผล (ปกติไม่ต้องใส่)

  "scope": {
    "checked": ["สร้าง / แก้ไข / ยกเลิก PO"],
    "not_checked": [{ "item": "ส่งอีเมล PO", "reason": "UAT ไม่เปิด SMTP" }]   // หรือ string เฉย ๆ
  },

  "logic": [                        // ★ อย่างน้อย 1 แถว · 1 แถว = 1 กฎ/scenario
    { "item": "ส่วนลดท้ายบิล + VAT", "expected": "VAT หลังหักส่วนลด",
      "actual": "VAT ก่อนหักส่วนลด",   // pass ไม่ใส่ = "ตรงตามคาด"
      "status": "fail",               // pass | note | fail | na
      "bug": "BUG-01",                // บังคับเมื่อ fail/note
      "ref": "TC-07" }
  ],

  "ui_checked": true,               // true = ข้อมาตรฐานที่ไม่ได้ override → ผ่าน · false → ไม่ได้ตรวจ
  "ui": [                           // override เฉพาะข้อที่มีปัญหา
    { "id": "U-02", "status": "note", "note": "ช่องสูงไม่เท่ากัน", "evidence": "ui02.png" },
    { "item": "หัวข้อพิเศษนอก checklist", "status": "note", "note": "..." }      // ไม่มี id = เพิ่มแถวใหม่
  ],
  "ux_checked": true,
  "ux": [ { "id": "X-03", "status": "note", "note": "error ไม่บอกช่อง" } ],

  "bugs": [
    { "id": "BUG-01", "title": "VAT คิดก่อนหักส่วนลด", "severity": "high",   // critical | high | medium | low
      "steps": ["สร้าง PO รวม 10,000", "ส่วนลด 10%", "ดู VAT"],
      "expected": "VAT 630.00", "actual": "VAT 700.00",
      "evidence": ["bug01.png", "bug01.mp4"],       // string หรือ list · รูป = ฝังในไฟล์
      "status": "open" }                              // open | fixed (ตรวจซ้ำ)
  ],

  "suggestions": [ { "item": "เพิ่มปุ่มคัดลอก PO", "reason": "สั่งซ้ำทุกเดือน" } ]
}
```

## Checklist มาตรฐาน (script เติมให้ · override ด้วย id)

| id | UI | id | UX |
|---|---|---|---|
| U-01 | สี / ฟอนต์ ตรง CI | X-01 | ทำงานหลักจบได้เองโดยไม่ต้องเดา |
| U-02 | ระยะห่าง / การจัดแนว ฟอร์มและตาราง | X-02 | กดแล้วระบบบอกผลทุกครั้ง |
| U-03 | ตาราง 1 ช่อง = 1 บรรทัด | X-03 | error บอกว่าผิดที่ไหน แก้ยังไง |
| U-04 | ปุ่ม / ไอคอน สม่ำเสมอ | X-04 | ถามยืนยันก่อนลบ / ยกเลิก |
| U-05 | ข้อความไทยถูกต้อง | X-05 | หน้าว่าง / โหลด / ผิดพลาด มีทางไปต่อ |
| U-06 | Dropdown / popup ไม่จม ไม่ล้นจอ | X-06 | ความเร็วตอบสนองรับได้ |

แก้ checklist มาตรฐานได้ที่ `UI_STD` / `UX_STD` บนสุดของ `scripts/build_report.py` ที่เดียว
