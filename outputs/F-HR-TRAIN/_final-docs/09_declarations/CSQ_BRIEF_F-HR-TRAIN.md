# CSQ_BRIEF — F-HR-TRAIN (อบรม · F133)

> **หมายเหตุการ carry:** WF-01 ไม่มี skill `csq-declaration` — carry verbatim จากแพ็กต้นทาง
> `Pack Brief Feature/F-HR-TRAIN/5_DECLARATIONS/CSQ_BRIEF.md` (2026-09-03) · เนื้อหาด้านล่างคือต้นฉบับ ไม่ได้แก้
> ผูก OQ: **OQ-06** (reverse EC เมื่อยกเลิกลงทะเบียนหลังส่ง Expense — default = ไม่ auto-reverse · รอ BA/Finance เคาะ) · **OQ-03** (Rate Card F060 ยังไม่ dev → `value_declared` เป็น display-only ไม่ผูกตัวเลขจนกว่าพร้อม)

---

## Declared Events
| event_id | trigger | ท่อ | เงื่อนไข | payload |
|---|---|---|---|---|
| train.enrolled_paid | อนุมัติลงทะเบียนที่มีค่าใช้จ่าย (S-04·BR-09) | **EC** | มูลค่าอบรม (ผลได้พนักงาน) | ref:enroll_id · course · value_declared · currency=THB · basis: declared |

## ไม่ประกาศ
**AC** — ไม่ประกาศ (การลงบัญชีค่าอบรม = Expense Claim เป็นผู้ประกาศ AC · เคส EC ไม่มี AC) · OC(OP) · DC-เอกสาร+doa_*(DOA) · SC(สงวน)
