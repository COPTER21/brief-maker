# DOA_BRIEF — F-HR-RECRUIT · สรรหา
## 1. Identity: F-HR-RECRUIT · HR · อนุมัติ 2 action: เปิดอัตรา · ข้อเสนอจ้าง (ไม่ผูก threshold ยอดเงิน — ตามระดับตำแหน่ง)
## 2. Approval Actions
| action | trigger | approve | reject |
|---|---|---|---|
| อนุมัติเปิดอัตรา | req: ร่าง→pending | ประกาศได้ | ตีกลับ |
| อนุมัติข้อเสนอจ้าง | offer: pending | เสนอผู้สมัคร | ไม่อนุมัติ |
## 3. Matrix **[ASSUMED A-REC-02 · DEFAULT]** (ไม่มีวงเงิน · ตามตำแหน่ง)
| set | amount_from | amount_to | chainMode | steps[roles] |
|---|---|---|---|---|
| requisition | 0 | null | sequential | [`role-hiring-manager`, `role-hr-recruit-head`] |
| offer | 0 | null | sequential | [`role-hiring-manager`, `role-hr-recruit-head`] |
> ระดับสูง (ผู้บริหาร) อาจเพิ่มชั้น — ตั้งที่ DOA กลาง
## 4. Field: approver_role · approval_chain(snapshot append-only) · **ไม่มี field ยอดเงินใน doa_resolve_payload** (offer ไม่ผูก threshold)
## 5. UI: slot picker (avatar+ตำแหน่ง+ชื่อ · 17ส.ค.) · timeline · My Approval
## 6. Wire: [ ] DOA entry req+offer · [ ] resolve ตอนส่ง · [ ] snapshot chain → wired
## 7. OQ: A-REC-02 (พี่เบิร์ด) ยืนยันสายเปิดอัตรา/ข้อเสนอ
