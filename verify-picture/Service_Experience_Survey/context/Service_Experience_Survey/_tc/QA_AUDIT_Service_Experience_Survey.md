# QA_AUDIT — F-TMP-006 Service Experience Survey (Sales Admin ต่างประเทศ)

- ต้นทาง MD: **30 เคส** / 89 step (testcases-F-TMP-006.md)
- MD: 30 เคส → Lite: 27 เคส (โหมด Lite · id เดิม R12)
- [NO-BROWSER] ไม่ได้ capture ภาพ (capture.py ข้าม) → ทุก step regionKey = "" (ปุ่มดูจอจาง)

## Drop ledger (เคสที่ตัดจากเอกสารคน + เหตุผล)
| TC | เหตุผล |
|---|---|
| TC-K02 | ENG-NOTIFY ไม่มีบน prototype — ทดสอบระดับระบบ |
| TC-E01 | ต้องใช้ console simulate |
| TC-E02 | ต้องใช้ console simulate |

## Merge note
- ไม่มีการรวมเคส · ยุบ step คำสั่ง agent เป็นภาษาคน (R13)
