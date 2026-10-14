# 05_RULES — F-AGM-008 Debt Management

## §5.1 Business Rules (→ invariants §3)
| BR | Rule |
|---|---|
| BR-DEBT-01 | Debtor idempotent per quota (1:1) — create ซ้ำ → detail เดิม |
| BR-DEBT-02 | Payment allocation waterfall: priority↑ → ดอกเบี้ย → ค่าปรับ → ต้นเงิน |
| BR-DEBT-03 | Payment validate-then-save (ตรวจสอบการจัดสรรก่อนบันทึก) |
| BR-DEBT-04 | Write-off DOA > 100,000 → อนุมัติผู้จัดการ |
| BR-DEBT-05 | Write-off + reason + confirm บังคับ · irreversible warning |
| BR-DEBT-06 | Contract-sourced obligation = 🔒 locked (immutable ที่ Debt) |
| BR-DEBT-07 | Adjustment อ้างอิงรายการเดิม + adjustment_type · principal อาจติดลบ |
| BR-DEBT-08 | Ledger double-entry append-only (dr/cr + balance_after) |
| BR-DEBT-09 | Aging 0-30/31-60/61-90/90+ (สี เขียว/เหลือง/ส้ม/แดง) |
| BR-DEBT-10 | outstanding = ledger of record → CBM/Contract read |
| BR-DEBT-11 | Obligation source gating: contract→contract_id · adjustment→type+reference · other→desc |

## §5.2 State Machine (→ invariants §4)
Debtor: `active ⇄ suspended → closed(outstanding=0) → written_off`
Obligation: `active ⇄ suspended → closed(ชำระครบ) → written_off(WriteOff) → reversed(adjustment reverse)`
Ledger: append-only (immutable)

## §5.3 Permission (→ invariants §6)
Debt.Officer (CRUD + payment + write-off ≤DOA) · Debt.Manager (approve >DOA + adjustment/reverse) · Contract (write contract-obligation 🔒) · CBM/Contract (read outstanding)

## §5.4 Validation
| VR | Rule | Message |
|---|---|---|
| VR-01 | principal > 0 (manual/contract) | "จำนวนต้นทุนต้องมากกว่า 0" |
| VR-02 | other_type_desc (type=other) | "กรุณากรอกรายละเอียดประเภทอื่นๆ" |
| VR-03 | contract_id (source=contract) | "กรุณาระบุรหัสสัญญาเมื่อแหล่งที่มาเป็น \"จากสัญญา\"" |
| VR-04 | adjustment_type (source=adjustment) | "กรุณาเลือกชนิดการปรับปรุง" |
| VR-05 | reference (source=adjustment) | "การปรับปรุงต้องอ้างอิงรายการเดิม (ภาระหนี้หรือรายการสมุดบัญชี)" |
| VR-06 | disbursement ≤ start_interest | "วันที่เบิกต้องไม่เกินวันเริ่มคิดดอกเบี้ย" |
| VR-07 | start_interest ≤ maturity | "วันเริ่มคิดดอกเบี้ยต้องไม่เกินวันครบกำหนด" |
| VR-08 | payment amount > 0 | "กรุณากรอกจำนวนเงินที่ถูกต้อง" |
| VR-09 | validate allocation ก่อน save | "กรุณาตรวจสอบการจัดสรรก่อน" |
| VR-10 | payment reference_no | "กรุณากรอกเลขอ้างอิง" |
| VR-11 | write-off confirm | "กรุณายืนยันการตัดหนี้" |
| VR-12 | write-off reason | "กรุณากรอกเหตุผลการตัดหนี้" |
| VR-13 | write-off amount ≤ outstanding | inline "จำนวนเกินยอดคงเหลือ" |
| VR-14 | quota_id (create) | "กรุณากรอกรหัสโควตา" |
| VR-15 | farmer_name (create) | "กรุณากรอกชื่อเกษตรกร" |

## §5.5 Edge Cases
| EC | Case | Expected |
|---|---|---|
| EC-01 | create debtor ซ้ำโควตา | "มีลูกหนี้อยู่แล้ว" → navigate detail (BR-01) |
| EC-02 | payment > total outstanding | จัดสรรจนหมด obligation · "เหลือ: X ฿" (overpay) |
| EC-03 | payment allocation ไม่กด validate | block "กรุณาตรวจสอบการจัดสรรก่อน" |
| EC-04 | write-off > 100k | banner "จำนวนเกินขีดจำกัด - ต้องการอนุมัติจากผู้จัดการ" → PENDING_APPROVAL |
| EC-05 | write-off amount > outstanding | inline error "จำนวนเกินยอดคงเหลือ" · block |
| EC-06 | edit contract-sourced obligation | 423 LOCKED (🔒 · immutable) |
| EC-07 | adjustment ไม่อ้างอิง | VR-05 block |
| EC-08 | adjustment reduce_principal | principal ติดลบ (-5000) allowed · status→reversed ถ้า reverse |
| EC-09 | dates ผิดลำดับ | VR-06/07 block |
| EC-10 | ledger แก้/ลบ | ไม่ได้ (append-only) — ออก reverse entry |
| EC-11 | outstanding ติดลบ | แสดงสีแดง (credit balance) |
| EC-12 | optimistic stale | 409 CONFLICT_UPDATE_STALE |
| EC-13 | idempotent dup payment | 409/no-op |

## §5.6 Error Catalog
VALIDATION_FAILED · FORBIDDEN "ไม่มีสิทธิ์ดำเนินการ" · PENDING_APPROVAL(202) "ต้องการอนุมัติจากผู้จัดการ" · LOCKED(423) "รายการจากสัญญาแก้ไขไม่ได้" · CONFLICT_UPDATE_STALE(409) "ข้อมูลถูกแก้ไขโดยผู้อื่น กรุณารีเฟรช" · CONFLICT(409) "รายการซ้ำ (idempotent)"
