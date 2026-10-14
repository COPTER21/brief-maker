# BRD — F-AGM-008 Debt Management (จัดการหนี้ลูกหนี้เกษตรกร)

> Constraint mode (จาก invariants.md 🔒) · Module เกษตรกรรม (AGM) · WKN · สถานะ: APPROVED

## §1 Business Context
โมดูลบริหารหนี้ลูกหนี้เกษตรกรที่ผูกกับโควตา — เป็น **financial ledger of record** ที่รวมภาระหนี้ (obligation) ทุกประเภทของเกษตรกร คิดดอกเบี้ย/ค่าปรับ บันทึกการชำระ ตัดหนี้สูญ และปรับปรุงยอด. ยอดคงค้าง (outstanding) ที่โมดูลนี้ถือ เป็นข้อมูลที่ **Cane Booking (F-AGM-007)** อ่านตอนสร้างการจอง+หักตอน Payment และ **Contract (F-AGM-005)** ใช้ตั้งภาระหนี้.

## §2 Problem / Opportunity
ของเดิม (React prototype) มี logic ครบแต่ UI ไม่ standard (full-page + modal dialogs, ไม่มี stats, payment "กำหนดเอง" ยังไม่ทำงาน). Refactor → CUBE Warm Light + governance (ledger append-only, DOA gate, contract-lock) ให้ auditable และเชื่อม chain AGM.

## §3 Goals & Scope
### §3.4 Locked Decisions (LOCK — จาก invariants)
| LOCK | Decision |
|---|---|
| LOCK-01 | คงพฤติกรรม AS-BUILT 100% (3-entity ledger, enums, validation) |
| LOCK-02 | Debtor idempotent per quota (1:1) — create ซ้ำ → ไป detail เดิม (BR-01) |
| LOCK-03 | **Payment allocation waterfall**: เรียง obligation ตาม priority ↑ → ดอกเบี้ย → ค่าปรับ → ต้นเงิน (BR-02) |
| LOCK-04 | Payment validate-then-save (ต้องตรวจสอบการจัดสรรก่อนบันทึก) (BR-03) |
| LOCK-05 | **Write-off DOA**: ยอด > 100,000 → ต้องอนุมัติผู้จัดการ + reason + confirm บังคับ (BR-04/05) |
| LOCK-06 | Contract-sourced obligation = 🔒 locked (ตั้งจาก Contract, immutable ที่ Debt) (BR-06) |
| LOCK-07 | Adjustment ต้องอ้างอิงรายการเดิม (obligation/ledger) + adjustment_type · principal อาจติดลบ (BR-07) |
| LOCK-08 | **Ledger double-entry append-only** (dr/cr + balance_after) — แก้ = reverse/adjustment entry ใหม่ (BR-08) |
| LOCK-09 | Aging bucket 0-30/31-60/61-90/90+ (สี เขียว/เหลือง/ส้ม/แดง) (BR-09) |
| LOCK-10 | outstanding = ledger of record → อ่านโดย CBM (debtor_outstanding) + Contract (BR-10) |
| LOCK-11 | Obligation source gating: contract→contract_id, adjustment→type+reference, other→desc (validation §2) |

### Out of Scope
Payment-run engine จริง · accrual job รายวัน · เอกสารแนบจริง · manual allocation (OQ-02).

## §4 Entities & State
- **Debtor** (ลูกหนี้ `DEB-YYYY-####`): active/suspended/closed/written_off · aggregate ของ obligations
- **Obligation** (ภาระหนี้ `OBL-YYYY-####`): active/suspended/closed/written_off/reversed · มีดอก/ค่าปรับ/priority
- **LedgerEntry** (บัญชีสมุด `LED-YYYY-####`): append-only · kind charge/interest/penalty/payment/adjustment/write_off/reverse
State machine → invariants §4.

## §5 Key Business Rules
BR-01..11 (invariants §3). สำคัญ: allocation waterfall (BR-02), DOA 100k (BR-04), contract-lock (BR-06), ledger double-entry (BR-08), outstanding cross-module read (BR-10).

## §6 Functional Requirements (สรุป → FRD)
1. **US-01 Debtor List** — ค้นหา (โควตา/ชื่อ/เลขลูกหนี้) · กรอง status·aging · CSV · รายงาน Aging · bulk select · stats
2. **US-02 Debtor Create** — ค้นโควตา → idempotent (ถ้ามีแล้ว→detail) → preview → สร้าง
3. **US-03 Debtor Detail** — 5 แท็บ (ภาพรวม/ภาระหนี้/บัญชีสมุด/เอกสาร/การตั้งค่า) + quick stats
4. **US-04 Obligation Create** — source gating (สัญญา🔒/แมนนวล/ปรับปรุง) · 6 ประเภท · อัตรา/fee · repay+deduct · date order validation
5. **US-05 Manual Payment** — allocation waterfall (validate→preview→save) · methods cash/bank/offset · เลขอ้างอิงบังคับ
6. **US-06 Write-off** — amount≤คงเหลือ · reason+confirm · DOA >100k → ผู้จัดการ
7. **US-07 Ledger** — double-entry view + export statement
8. **US-08 Adjustment** — reduce/increase/reallocate/reverse principal อ้างอิงรายการเดิม
9. **US-09 Cross-module** — feed outstanding → CBM/Contract · read Quota/Contract

## §7 Non-Functional
list p95<3s · action<1s · ledger immutable+auditable · optimistic lock · เลขเอกสาร/statement ไทย · RBAC (Officer/Manager) · DOA governance.

## §18 Stats (list dashboard)
4 การ์ด: ลูกหนี้ทั้งหมด · ยอดคงค้างรวม (฿) · เกินกำหนด (aging 90+) · ตัดหนี้สูญ (เดือนนี้).

## §Cross-Module Map
```
Quota (F-AGM-002) ──read──▶ Debtor (quota_id, farmer snapshot)
Contract (F-AGM-005) ──write(🔒)──▶ Obligation (source=contract)
Debt (F-AGM-008) ──outstanding──▶ CBM (F-AGM-007 debtor_outstanding) + Contract (deduction)
```
