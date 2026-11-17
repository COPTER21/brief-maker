# QA_AUDIT — F-TMP-003 ฟอร์มแจ้งงานขนส่งนอก

- ต้นทาง MD: **32 เคส** / 93 step (testcases-F-TMP-003.md)
- MD: 32 เคส → Lite: 29 เคส (โหมด Lite · id เดิม R12)
- [NO-BROWSER] ไม่ได้ capture ภาพ (capture.py ข้าม) → ทุก step regionKey = "" (ปุ่มดูจอจาง)

## Drop ledger (เคสที่ตัดจากเอกสารคน + เหตุผล)
| TC | เหตุผล |
|---|---|
| TC-K01 | ENG-NOTIFY ไม่มีบน prototype — ทดสอบระดับระบบ |
| TC-E01 | ต้องใช้ console simulate |
| TC-E02 | ต้องใช้ console simulate |

## Merge note
- ไม่มีการรวมเคส · ยุบ step คำสั่ง agent เป็นภาษาคน (R13)
