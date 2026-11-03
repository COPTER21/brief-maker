# QA_AUDIT — F-TMP-005 (qa-friendly-html-generator v3.1 · Lite)

- MD: 41 เคส / 75 step (testcases-F-TMP-005.md)
- เอกสารคน (Lite): 37 เคส / 70 step — TC id เดิมทุกเคส (R12)
- [NO-BROWSER] ไม่ได้ถ่ายภาพหน้าจอ (capture.py) — ทุก step regionKey = "" (ไม่มีปุ่มดูจอ) · ต้องรันรอบเต็มบนเครื่องที่มี browser

## Drop ledger (ไม่อยู่ในเอกสารคน — AI ครอบแล้วใน MD)
| TC | ตัด/ยุบ | เหตุผล |
|---|---|---|
| TC-L05 | ตัด | ตัด: pagination มาตรฐาน — ครอบโดย e2e/ตรวจ UI ทั่วไป |
| TC-V07 | ตัด | ตัด: file policy กลาง (Document Center) — ครอบโดย e2e/ตรวจ UI ทั่วไป |
| TC-D03 | ตัด | ตัด: ครอบโดยแบบพิมพ์ long-31rows/approved-doa6steps.data.json (parity) — ต้องดูภาพบนเครื่องที่มี browser |
| TC-XT02 | ยุบ | ยุบ: ครอบโดย TC-C04 (เลขเดิมตอนส่ง) + TC-C01 |
