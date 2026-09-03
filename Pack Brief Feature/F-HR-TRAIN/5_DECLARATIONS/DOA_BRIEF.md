# DOA_BRIEF — F-HR-TRAIN · อบรม
## 1. Identity: F-HR-TRAIN · HR · อนุมัติ "การลงทะเบียนอบรมที่มีค่าใช้จ่าย" (ไม่มีค่าใช้จ่าย=ข้าม)
## 2. Actions: อนุมัติลงทะเบียน (เมื่อ has_cost) → ยืนยัน + ยิง EC · reject
## 3. Matrix **[ASSUMED · DEFAULT]** (ตามงบ · [ASSUMED ไม่มีวงเงินหลายชั้น รอบนี้])
| set | amount_from | amount_to | chainMode | steps[roles] |
|---|---|---|---|---|
| training_cost | 0 | null | sequential | [`role-line-manager`, `role-hr-ld-head`] |
## 4. Field: approver_role · approval_chain(snapshot) · cost (สำหรับ resolve ถ้าจะทำ threshold ภายหลัง)
## 5. UI: slot picker (17ส.ค.) · timeline · My Approval · เฉพาะเมื่อ has_cost
## 6. Wire: [ ] DOA entry training_cost · [ ] resolve เมื่อ has_cost · [ ] snapshot → wired
## 7. OQ: threshold ตามงบหรือไม่ (พี่เบิร์ด)
