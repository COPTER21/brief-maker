# AI Runner Guide — ให้ AI ทดสอบเองจาก testset .md

แนวทางสำหรับ "AI ผู้ทดสอบ" ที่ได้รับไฟล์ testset .md นี้.

## 0. เลือกโหมด
- มีคอลัมน์ **Setup/Locator** → ทำได้ทั้ง automated (Playwright/computer-use) และ vision
- ไม่มี → vision/manual เท่านั้น (เปิดแอปจริง ทำตาม Action + ดู Screenshot)

## 1. เตรียม
- อ่าน Meta → รู้ URL/แอป (`--app-url`) และ Feature ID
- อ่าน **Appendix Structured Suite (JSON)** เพื่อโหลดทุกเคสแบบ machine-readable (แนะนำให้ parse จากตรงนี้)

## 2. รันทีละเคส
สำหรับแต่ละ case:
1. จัด Preconditions ให้พร้อม
2. ทำทีละ step:
   - **automated:** รัน `setup` (JS) เพื่อไปยังหน้าจอ → หา element จาก `el` (selector / has_text) →
     ทำ action ตาม *Action* → ตรวจ DOM/ข้อความเทียบ *Expected*
   - **vision:** ทำตาม *Action* บน UI จริง → สังเกตผลเทียบ *Expected* (อ้าง Screenshot ประกอบ)
   - ขั้นตรง = PASS, ไม่ตรง = FAIL + เหตุผลสั้น
3. ตัดสินเคส: ทุกขั้น PASS และตรง *Pass criteria* → `pass`; มีขั้น FAIL → `fail`;
   ทำไม่ได้เพราะติดเงื่อนไข → `blocked`

## 3. กฎความปลอดภัยข้อมูล
- ห้ามแก้/ลบข้อมูลจริงเกินกว่าที่เคสกำหนด
- เคสที่ "สร้างของ" ให้ลบ/คืนสถานะหลังเทสถ้าทำได้ (กัน side-effect ข้ามเคส)
- เคส negative (เช่น "ไม่เลือกตำแหน่งแล้วต้องเตือน") → คาดหวัง "ระบบบล็อก/เตือน" ไม่ใช่ทำสำเร็จ

## 4. รายงานกลับ
กรอกบล็อก JSON เทมเพลตในไฟล์ (summary + results[]) ให้ครบ:
```json
{
  "feature_id": "F-91",
  "run_by": "AI",
  "summary": {"total": 18, "pass": 0, "fail": 0, "blocked": 0, "pass_rate": "0%"},
  "results": [
    {"id": "TC-01", "verdict": "pass", "failed_steps": [], "note": ""},
    {"id": "TC-03", "verdict": "fail", "failed_steps": [2], "note": "ขั้น 2 ระบบไม่ขึ้นคำเตือน"}
  ]
}
```
- `failed_steps` = เลขขั้นที่ FAIL
- คำนวณ `pass_rate = pass / total`
- สรุปจุดที่ FAIL เป็นภาษากระชับ ให้ทีม dev ตามต่อได้

## 5. ป้อนกลับเข้าเอกสารคน (ออปชั่น)
ผล verdict สามารถนำกลับไปกรอกในไฟล์ HTML ฉบับคน (ติ๊กผล/พิมพ์ Test Result) เพื่อให้ได้รายงาน
รูปแบบเดียวกับที่ผู้ทดสอบคนใช้.
