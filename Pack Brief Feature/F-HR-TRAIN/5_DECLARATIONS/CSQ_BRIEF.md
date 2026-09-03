# CSQ_BRIEF — F-HR-TRAIN
## Declared Events
| event_id | trigger | ท่อ | เงื่อนไข | payload |
|---|---|---|---|---|
| train.enrolled_paid | อนุมัติลงทะเบียนที่มีค่าใช้จ่าย (S-04·BR-09) | **EC** | มูลค่าอบรม (ผลได้พนักงาน) | ref:enroll_id · course · value_declared · currency=THB · basis: declared |
## ไม่ประกาศ: **AC** — ไม่ประกาศ (การลงบัญชีค่าอบรม = Expense Claim เป็นผู้ประกาศ AC · เคส EC ไม่มี AC) · OC(OP) · DC-เอกสาร+doa_*(DOA) · SC(สงวน)
