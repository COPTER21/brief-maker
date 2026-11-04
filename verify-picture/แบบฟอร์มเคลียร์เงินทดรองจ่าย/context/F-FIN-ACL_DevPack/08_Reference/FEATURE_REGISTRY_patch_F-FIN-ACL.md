# แพตช์ FEATURE_REGISTRY — F-FIN-ACL (อัปที่หน้าโปรเจกต์)

## Core › Finance (ต่อจาก Petty Cash)
```
│  ├─ Petty Cash .................. (—)
│  └─ ใบเคลียร์เงินทดรองจ่าย ⟂ ...... (H·B·F·Q) = F-FIN-ACL · FM-FIN-02 (Credence) · doc_type ACL
```

## Cross-Module Data Contracts
| Contract | From → To | Payload / กลไก |
|---|---|---|
| ACL → DOA | F-FIN-ACL → F-DLG-001 | resolve?feature_id=F-FIN-ACL · 3 ขั้น ไม่มีวงเงิน · snapshot approval_chain |
| ACL → DOCCFG | F-FIN-ACL → F003 | ENG-DOC-NUM.next('ACL') ตอนบันทึกครั้งแรก · store approved_final |
| ACL → NOTIFY | F-FIN-ACL → ENG-NOTIFY | acl_cancelled · acl_overspent_approved · acl_refund_due |
| ACL → AP/GL | F-FIN-ACL → AP/GL | event acl.approved — ประกาศ ไม่ยิงรอบนี้ (DEC-02) |
| ACL ← Config | ExpensePolicy · Company.bank_accounts → F-FIN-ACL | advance_clear_due_day · purpose=advance_refund (อ่านอย่างเดียว) |
