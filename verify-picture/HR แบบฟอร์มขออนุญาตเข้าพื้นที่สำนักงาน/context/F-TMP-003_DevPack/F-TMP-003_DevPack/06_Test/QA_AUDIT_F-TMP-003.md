# QA_AUDIT — F-TMP-003 (qa-friendly-html-generator v3.1 · Lite)

- MD: 47 เคส / 82 step (testcases-F-TMP-003.md)
- เอกสารคน (Lite): 41 เคส / 75 step — TC id เดิมทุกเคส (R12)
- [NO-BROWSER] ไม่ได้ถ่ายภาพหน้าจอ (capture.py) — ทุก step regionKey = "" (ไม่มีปุ่มดูจอ) · ต้องรันรอบเต็มบนเครื่องที่มี browser

## Drop ledger (ไม่อยู่ในเอกสารคน — AI ครอบแล้วใน MD)
| TC | ตัด/ยุบ | เหตุผล |
|---|---|---|
| TC-L05 | ยุบ | ยุบเข้า TC-L02 (ส่วนท้ายตาราง) |
| TC-C05 | ยุบ | ยุบเข้า TC-C01 step 3 |
| TC-A04 | ยุบ | ยุบเข้า TC-S02 (ร่างที่ถูกไม่อนุมัติส่งใหม่) |
| TC-K02 | ยุบ | ยุบเข้า TC-K01 (ใช้ seed DOA 2 ขั้น) |
| TC-XT01 | ตัด | ตัด — prototype ไม่มีกล่องแจ้งเตือน ทดสอบตอน UAT ระบบจริง |
| TC-XT02 | ยุบ | ยุบเข้า TC-C02 (เลขเดิมตอนส่ง) |
