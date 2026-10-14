# 02_API — F-AGM-008 Debt Management

> REST `/api/debt/*` · headers: X-Idempotency-Key, If-Match(row_version), X-Trace-Id · R8: mutation → Function

## §2.1 Endpoints
| API | Method | Path | Purpose |
|---|---|---|---|
| API-01 | GET | /debt/debtors | list search/filter(status,aging)/sort/page + stats |
| API-02 | POST | /debt/debtors | สร้างลูกหนี้ (idempotent per quota) |
| API-03 | GET | /debt/debtors/:id | detail + obligations + ledger + stats |
| API-04 | GET | /debt/debtors/search?quota_id= | ค้นโควตา (preview / existing debtor) |
| API-05 | GET | /debt/debtors/export | export CSV |
| API-06 | GET | /debt/aging-report | รายงาน Aging |
| **API-OB1** | POST | /debt/debtors/:id/obligations | สร้างภาระหนี้ (source gating) |
| API-OB2 | GET | /debt/obligations/:oid | detail |
| API-OB3 | PUT | /debt/obligations/:oid | แก้ไข (ยกเว้น contract-sourced 🔒) |
| **API-PAY1** | POST | /debt/debtors/:id/payments/validate | คำนวณ allocation (waterfall) — preview |
| **API-PAY2** | POST | /debt/debtors/:id/payments | บันทึกการชำระ (idempotent, reference บังคับ) |
| **API-WO1** | POST | /debt/obligations/:oid/write-off | ตัดหนี้สูญ (reason+confirm · >DOA → 202 approval) |
| **API-ADJ1** | POST | /debt/debtors/:id/adjustments | ปรับปรุง (อ้างอิง obligation/ledger) |
| API-LED1 | GET | /debt/debtors/:id/ledger | บัญชีสมุด (double-entry) |
| API-LED2 | GET | /debt/debtors/:id/ledger/export | export Statement |
| **API-EXT** | GET | /debt/debtors/by-quota/:quota_id/outstanding | (อ่านโดย CBM/Contract) debtor_outstanding |
| API-12 | GET | /debt/debtors/:id/history | audit |

## §2.X Contracts ⭐
- **API-02 (create debtor):** idempotent per quota → ถ้ามีแล้ว 200 + existing debtor (ไม่สร้างซ้ำ · BR-01)
- **API-PAY1 (validate):** input {amount} → output allocation[] เรียง priority↑ → ต่อ obligation: interest→penalty→principal · remainder. **ต้องเรียก validate ก่อน PAY2** (BR-03)
- **API-PAY2 (payment):** idempotent (X-Idempotency-Key) · reference บังคับ · emit ledger entries (kind=payment) · method cash/bank/offset
- **API-WO1 (write-off):** reason+confirm บังคับ · amount ≤ outstanding · **ถ้า amount > DOA(100000) → 202 PENDING_APPROVAL** (ผู้จัดการ) · ledger kind=write_off (BR-04/05)
- **API-OB1 (obligation):** source=contract → contract_id required + 🔒 · source=adjustment → adjustment_type + reference(obligation/ledger) required · other → desc · dates: disb ≤ start_int ≤ maturity (validation §5.4)
- **API-ADJ1 (adjustment):** อ้างอิงรายการเดิม · principal อาจติดลบ · ledger kind=adjustment/reverse (BR-07)
- **API-EXT:** read-only outstanding — consumed by CBM create-booking + Payment deduction (BR-10)

## §2.2 ตัวอย่าง
```
POST /api/debt/debtors/DEB-2568-0001/payments/validate
{ "amount": 30000 }
→ 200 { "allocations":[{"obligation_id":"OBL-2568-0001","items":[
    {"kind":"interest","amount":2500},{"kind":"penalty","amount":0},{"kind":"principal","amount":27500}]}],
    "allocated":30000, "remaining":0 }
```
Events: `debt.debtor.created` · `debt.obligation.created` · `debt.payment.recorded` · `debt.writeoff.pending|approved` · `debt.adjustment.posted` · `debt.outstanding.changed` (→ CBM/Contract)

## §2.3 Errors → 05_RULES §5.6
VALIDATION_FAILED · FORBIDDEN · PENDING_APPROVAL(202 DOA) · CONFLICT_UPDATE_STALE(409) · CONFLICT(409 dup) · LOCKED(423 contract-sourced edit)
