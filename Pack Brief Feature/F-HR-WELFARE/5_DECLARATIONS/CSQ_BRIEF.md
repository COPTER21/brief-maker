# CSQ_BRIEF — F-HR-WELFARE · สวัสดิการ
> ประกาศ event→ท่อ เท่านั้น · auto-register ตอน deploy · ไม่คำนวณมูลค่าเอง (ENG-CSQ-02 ทำ)

## 1. Identity
feature_id: F-HR-WELFARE · module: HR · engine: ENG-CSQ (F-CSQ-01)

## 2. Declared Events
| event_id | trigger point (อ้าง PREBRIEF) | ท่อที่ยิง | เงื่อนไข | payload fields |
|---|---|---|---|---|
| welfare.granted | คำขอ: pending_approval→approved/recorded (S-07 · BR-09) | **EC** | เมื่ออนุมัติคำขอใช้สิทธิ์ที่มีมูลค่า | ref: request_no · employee_id (snapshot) · benefit_type · value_declared · currency=THB · basis: **declared** (มูลค่าที่กรอก · ไม่คำนวณเอง) |

## 3. ท่อที่ไม่ประกาศ (และเหตุผล)
- **OC** — ไม่ประกาศ · มาจาก Operation Process (Welfare ไม่มี sow.*)
- **DC (เอกสาร) + doa_*** — ไม่ประกาศ · DOA engine ยิงให้อัตโนมัติ (การอนุมัติคำขอ = การเซ็น ไม่ใช่ terminal decision)
- **AC / FC** — ไม่ประกาศ · Welfare ไม่ลงบัญชี/ไม่กระทบเงินสด-งบเอง (จ่ายจริง = Payroll/Expense เป็นผู้ประกาศ AC/FC)
- **SC** — สงวน (trigger=false เสมอ · OQ-C3)

## 5. Register Checklist
- [ ] event welfare.granted อยู่ในกลุ่ม EC · [ ] payload มี ref + value_declared + basis=declared · [ ] ไม่ซ้ำท่อ OC/DC/SC → กัน reject 422
