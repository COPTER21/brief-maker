# QA_AUDIT — F-TMP-008 (qa-friendly-html-generator · Lite)

- MD: 30 เคส (testcases-F-TMP-008.md)
- เอกสารคน (Lite): 26 เคส / 56 step — TC id เดิมทุกเคส (R12)
- Merge note: ตัด verb tag ออกเป็นภาษาคน · เกณฑ์ [AI-DEFAULT] เขียนเป็น "(เกณฑ์รอลูกค้ายืนยัน)" · ตัด step ที่ต้องใช้ console (1 step) · ไม่มีภาพหน้าจอ ([NO-BROWSER] ข้าม capture.py)

## Drop ledger (ไม่อยู่ในเอกสารคน — AI ครอบแล้วใน MD)
| TC | ตัด/ยุบ | เหตุผล |
|---|---|---|
| TC-XT01 | ตัด | ตรวจว่าไม่ส่งต่อระบบอื่น = หลังบ้าน |
| TC-C04 | ตัด | ตรวจหัวตาราง/ตัวเลือก 1:1 = งาน review ไม่ใช่ผู้ใช้ |
| TC-P02 | ยุบเข้า TC-L01 | ไม่เห็นร่างของคนอื่นตรวจใน step 3 |
| TC-L02 | ยุบเข้า TC-L03 | admin เห็นทุกใบตรวจตอนกรองใน TC-L03 |
