# DOA_BRIEF — F-ACC-CN Credit Note
## 1. Identity
feature_id F-ACC-CN (F096) · Credit Note · Accounting/AR · platform CUBE 4.0 · scope company
## 2. Approval Actions
| Action | Trigger | Approve | Reject |
|---|---|---|---|
| ส่งอนุมัติใบลดหนี้ | draft → pending_approval | ครบสาย → approved · ออกเลข CN · cn_applied ใบเดิม · JE mock | กลับ draft (เหตุผลบังคับ · history append-only) |
## 3. Matrix (กรอกหน้า DOA กลาง) — **มีวงเงิน** · 1 สาย · sequential [DEFAULT — รอยืนยัน OQ-CN-04]
| set | amount_from (บาท) | amount_to (บาท) | departments | chainMode | steps[roles] |
|---|---|---|---|---|---|
| 1 | 0 | 50,000 | all | sequential | [role-mgr-sales] |
| 2 | 50,000.01 | 300,000 | all | sequential | [role-mgr-sales] → [role-mgr-acc] |
| 3 | 300,000.01 | null | all | sequential | [role-mgr-sales] → [role-mgr-acc] → [role-cfo] |
ฐานวงเงิน = ยอด CN รวม VAT (grand_total)
## 4. Field Contract
approval_required · approval_status (draft/pending_approval/approved/rejected/cancelled) · doa_entry_ref · approver_role · approved_by · approval_chain (jsonb snapshot) · approved_at · approval_history (append-only)
## 5. UI Contract
ปุ่มส่งอนุมัติ (draft) · slot picker เลือกคน (avatar+ตำแหน่ง+ชื่อ) · badge สถานะ · timeline ลายเซ็น · อนุมัติ/ไม่อนุมัติ เฉพาะผู้มีสิทธิ์ขั้นปัจจุบัน · My Approval hook · HTML: `resolveDoa()` mock ตาม matrix (3 tier) — ไม่มี chain hardcode
## 6. Wire Checklist
- [ ] ตั้ง DOA entry DOA-ACC-CN ตาม §3 · [ ] resolve ตอนส่ง + freeze · [ ] BR-DOA-01..05 · [ ] re-resolve ถ้าแก้ยอดหลังตีกลับ · wire_status: pending
## 7. Open Questions
OQ-CN-04 จุดตัดวงเงิน/บทบาท — Policy Center + Strike · OQ-AR-06 role-mgr-acc ยังไม่มีใน master
