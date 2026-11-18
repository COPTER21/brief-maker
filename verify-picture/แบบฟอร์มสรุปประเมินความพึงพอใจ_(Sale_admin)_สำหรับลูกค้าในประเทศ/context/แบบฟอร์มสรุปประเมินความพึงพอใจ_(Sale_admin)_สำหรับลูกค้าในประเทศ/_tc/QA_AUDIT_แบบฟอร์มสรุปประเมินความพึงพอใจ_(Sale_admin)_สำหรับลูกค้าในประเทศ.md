# QA_AUDIT — F-TMP-005 ใบสรุปความพึงพอใจ Sale admin ลูกค้าในประเทศ

- ต้นทาง MD: **45 เคส** / 132 step (testcases-F-TMP-005.md)
- MD: 45 เคส → Lite: 38 เคส (โหมด Lite · id เดิม R12)
- [NO-BROWSER] ไม่ได้ capture ภาพ (capture.py ข้าม) → ทุก step regionKey = "" (ปุ่มดูจอจาง)

## Drop ledger (เคสที่ตัดจากเอกสารคน + เหตุผล)
| TC | เหตุผล |
|---|---|
| TC-S05 | ต้องใช้ console เพิ่มขั้น DOA (`__QA__.doa.push`) — ทดสอบที่ DOA กลาง/ระบบ |
| TC-S06 | ต้องใช้ console simulate (`__QA__.sim`) |
| TC-D03 | ต้องใช้ console เพิ่มขั้น DOA — ทดสอบที่ DOA กลาง |
| TC-E01 | ต้องใช้ console ปิดแบบเอกสาร (F-DOCCFG) |
| TC-E02 | ต้องใช้ console simulate (stale) |
| TC-L08 | permutation ของ pagination — e2e อัตโนมัติครอบแล้ว (U6) |
| TC-L02 | ตรวจโครงหน้าจอ (no-scorecard) — QA ภายในตรวจแล้ว |

## Merge note
- ไม่มีการรวมเคส · ยุบ step คำสั่ง agent เป็นภาษาคน (R13) · ค่าจำนวนแถวจาก prototype แปลงเป็น "เท่าที่มีสิทธิ์เห็น" (R16)
