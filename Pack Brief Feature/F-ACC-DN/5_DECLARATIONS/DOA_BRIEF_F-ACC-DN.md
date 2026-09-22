# DOA_BRIEF — F-ACC-DN Debit Note
## 1. Identity: F-ACC-DN · Debit Note · Accounting/AP · CUBE 4.0 · company
## 2. Approval Actions
| Action | Trigger | Approve | Reject |
|---|---|---|---|
| ส่งอนุมัติใบลดหนี้ผู้ขาย | draft → pending_approval | ครบสาย → approved · เลข DN · dn_applied ใบตั้งหนี้ · input_vat_line ติดลบ · JE mock | กลับ draft (เหตุผล · history append-only) |
## 3. Matrix — **มีวงเงิน** · sequential [DEFAULT — รอยืนยัน OQ-DN-02]
| set | amount_from | amount_to | steps[roles] |
|---|---|---|---|
| 1 | 0 | 50,000 | [role-mgr-pur] |
| 2 | 50,000.01 | 300,000 | [role-mgr-pur] → [role-mgr-acc] |
| 3 | 300,000.01 | null | [role-mgr-pur] → [role-mgr-acc] → [role-cfo] |
ฐาน = grand_total รวม VAT
## 4. Field Contract: approval_required · approval_status · doa_entry_ref · approver_role · approved_by · approval_chain (jsonb) · approved_at · approval_history
## 5. UI Contract: ส่งอนุมัติ (draft) · slot picker เลือกคน · timeline · อนุมัติ/ไม่อนุมัติเฉพาะขั้นปัจจุบัน · `resolveDoa()` mock ตาม matrix
## 6. Wire Checklist: [ ] DOA-ACC-DN · [ ] resolve+freeze · [ ] BR-DOA-01..05 · wire_status: pending
## 7. OQ: OQ-DN-02 · OQ-AP-06
