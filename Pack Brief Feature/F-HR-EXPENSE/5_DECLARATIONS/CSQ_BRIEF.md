# CSQ_BRIEF — F-HR-EXPENSE · เบิกค่าใช้จ่าย
> ประกาศ event→ท่อ · auto-register ตอน deploy · ไม่คำนวณมูลค่าเอง

## 1. Identity
feature_id: F-HR-EXPENSE · module: HR · engine: ENG-CSQ (F-CSQ-01)

## 2. Declared Events
| event_id | trigger point | ท่อ | เงื่อนไข | payload |
|---|---|---|---|---|
| expense.approved | pending→approved (S-09·BR-07) | **FC** | commit งบ/เงินสดเมื่ออนุมัติใบเบิก | ref:doc_no · cost_center(snapshot) · amount · currency=THB · basis: actual |
| expense.posted | approved→ส่ง GL (S-09·BR-07) | **AC** | ตั้งหนี้/ลงบัญชีเมื่อส่ง payload ไป Accounting | ref:doc_no · gl_payload · basis: actual |
| expense.recorded | approved (S-09) | **EC** | มูลค่าค่าใช้จ่ายที่อนุมัติ | ref:doc_no · amount · basis: actual |

## 3. ท่อที่ไม่ประกาศ (เหตุผล)
- **OC** — มาจาก Operation Process (Expense ไม่มี sow.*)
- **DC (เอกสาร) + doa_*** — DOA engine ยิงอัตโนมัติ (อนุมัติใบ = เซ็น ไม่ใช่ terminal decision)
- **SC** — สงวน (trigger=false · OQ-C3)

## 5. Register Checklist
- [ ] FC/AC/EC อยู่กลุ่มถูก · [ ] payload มี ref+amount+basis · [ ] ไม่ซ้ำ OC/DC/SC → กัน 422 · [ ] expense.posted ยิงเฉพาะเมื่อ Accounting มี (Module Linkage · ระหว่างนี้ payload "รอปลายทาง")
