# 05_RULES — F-AGM-011 Cane Receiving

## §5.1 Business Rules (→ invariants §3)
| BR | Rule |
|---|---|
| BR-CR-01 | Single Sync (dump v2): query checkin_datetime+weigh_coin+quota_id → caneType/times/weights (ไม่มี CCS) |
| BR-CR-02 | Auto สำเร็จ → lock read-only · fail → manual (net 2-dec + เหตุผล) |
| BR-CR-03 | net = gross − tare (หรือ manual) |
| BR-CR-04 | ออกใบ → CRN + Issued + CBM awaiting_payment + free coin + PDF A4+QR |
| BR-CR-05 | POST /cane-receivings idempotent (ไม่สร้างซ้ำ) |
| BR-CR-06 | Sync All bulk → dump+create ต่อ Draft · result modal (success/failed) |
| BR-CR-07 | Sync All บังคับเลือกวันที่ + ไม่รันซ้อน |
| BR-CR-08 | Receiving = SoT (ส่ง net_weight + cane_type ให้ Payment · CCS ที่ Payment) |
| BR-CR-09 | Void → status Void + rollback CBM awaiting_dump_result + block payment · reason≥5 |
| BR-CR-10 | Void ไม่ได้ถ้า paymentStatus=ชำระเงินแล้ว |
| BR-CR-11 | ดึงผลการเทใช้ได้เฉพาะรายการยังไม่ออกใบ (receiving_id NULL) |
| BR-CR-12 | cane type ไม่รู้จัก → คง code · Payment adjustment 0 + เตือน (ฝั่ง Payment) |

## §5.2 State Machine (→ invariants §4)
Receiving: `Draft(รอผลเท) → Issued(เทแล้ว) → Void(ยกเลิก)`
Dump: `- → auto(SUCCESS lock) / fail → manual`
CBM sync: issue → awaiting_payment · void → awaiting_dump_result

## §5.3 Permission (→ invariants §6)
Receiving Staff (dump+ออกใบ+Sync All) · Supervisor/Admin (manual override+void) · Viewer (read, ไม่เห็น Sync All/create)

## §5.4 Validation
| VR | Rule | Message |
|---|---|---|
| VR-01 | manual net required | "กรุณากรอกน้ำหนักสุทธิ" |
| VR-02 | net 2-dec non-neg | "กรุณากรอกน้ำหนักสุทธิเป็นจำนวนไม่ลบและ 2 ตำแหน่ง" |
| VR-03 | manual reason required | "กรุณากรอกเหตุผลการกรอกด้วยตนเอง" |
| VR-04 | void reason ≥5 | "เหตุผลต้องมีความยาวอย่างน้อย 5 ตัวอักษร" |
| VR-05 | Sync All date required | บังคับเลือกช่วงวันที่ก่อน |

## §5.5 Edge Cases
| EC | Case | Expected |
|---|---|---|
| EC-01 | ดึงผลการเท auto สำเร็จ | dump v2 card + lock read-only |
| EC-02 | ดึงผลการเท auto fail | "ไม่พบผลการเทจากโรงงาน — กรุณาเปลี่ยนเป็นโหมด Manual" |
| EC-03 | manual net ว่าง | VR-01 |
| EC-04 | manual net ผิดรูปแบบ | VR-02 |
| EC-05 | manual ไม่ใส่เหตุผล | VR-03 |
| EC-06 | ออกใบรับอ้อย | Issued + CRN + side effects + "ออกใบรับอ้อยสำเร็จ" |
| EC-07 | ออกใบซ้ำ (idempotent) | ไม่สร้างซ้ำ (409/no-op) |
| EC-08 | Sync All ไม่เลือกวันที่ | VR-05 block |
| EC-09 | Sync All สำเร็จบางส่วน | result modal (สำเร็จ X/ล้มเหลว Y) + failed table |
| EC-10 | Sync All fail item | keep Draft + error NOT_FOUND "ไม่พบข้อมูลผลการเทในระบบโรงงาน" |
| EC-11 | Void reason <5 | VR-04 |
| EC-12 | Void สำเร็จ | Void + rollback CBM + "Void ใบรับอ้อยสำเร็จ" |
| EC-13 | Void ที่จ่ายแล้ว | block (ชำระเงินแล้ว) |
| EC-14 | net cross-check (gross-tare≠net) | เก็บทั้งสามค่า debug |

## §5.6 Error Catalog
VALIDATION_FAILED · DUMP_NOT_FOUND "ไม่พบผลการเทจากโรงงาน — กรุณาเปลี่ยนเป็นโหมด Manual" / "ไม่พบข้อมูลผลการเทในระบบโรงงาน" · CONFLICT(409 dup) "รายการซ้ำ (idempotent)" · VOID_BLOCKED_PAID "ไม่สามารถยกเลิกรายการที่ชำระเงินแล้ว" · SYNC_ALL_DATE_REQUIRED
