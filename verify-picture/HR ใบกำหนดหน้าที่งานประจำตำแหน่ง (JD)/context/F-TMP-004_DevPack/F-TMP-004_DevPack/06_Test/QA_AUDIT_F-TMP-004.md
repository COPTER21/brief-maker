# QA_AUDIT — F-TMP-004 (qa-friendly-html-generator v3.1 · Lite)

- MD: 54 เคส / 94 step (testcases-F-TMP-004.md)
- เอกสารคน (Lite): 45 เคส / 84 step — TC id เดิมทุกเคส (R12)
- [NO-BROWSER] ไม่ได้ถ่ายภาพหน้าจอ (capture.py) — ทุก step regionKey = "" (ไม่มีปุ่มดูจอ) · ต้องรันรอบเต็มบนเครื่องที่มี browser

## Drop ledger (ไม่อยู่ในเอกสารคน — AI ครอบแล้วใน MD)
| TC | ตัด/ยุบ | เหตุผล |
|---|---|---|
| TC-L05 | ตัด | ตัด: pagination มาตรฐาน — ครอบโดย e2e/ตรวจ UI ทั่วไป |
| TC-V06 | ยุบ | ยุบเข้า TC-V05 (ตรวจแถวรูปแบบเดียวกัน) |
| TC-V09 | ตัด | ตัด: file policy กลาง (Document Center) — ครอบใน TC-V08 |
| TC-A04 | ตัด | ตัด: ค่าเริ่ม 1 ขั้น (DEC-03) — ครอบโดย TC-S02 + e2e S8 |
| TC-P06 | ยุบ | ยุบเข้า TC-L07 (ตรวจ CSV แบบเดียวกัน) |
| TC-D04 | ตัด | ตัด: ครอบโดยแบบพิมพ์ approved-doa6steps.data.json (parity) — ต้องดูภาพบนเครื่องที่มี browser |
| TC-E03 | ตัด | ตัด: ครอบโดย e2e/ตรวจ UI ทั่วไป |
| TC-XT01 | ตัด | ตัด: การแจ้งเตือนข้ามโมดูล = หลังบ้าน |
| TC-XT02 | ยุบ | ยุบเข้า TC-C04 (เลขเดิมตอนส่ง) |
