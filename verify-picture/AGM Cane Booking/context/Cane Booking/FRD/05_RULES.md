# 05_RULES — F-AGM-007 Cane Booking Management

## §5.1 Business Rules (→ invariants §6)
| BR | Rule |
|---|---|
| BR-CBM-01 | no-skip pipeline A→B→C · Gate: B เมื่อ A=verified · C เมื่อ B closed |
| BR-CBM-02 | system-controlled (รอผลการเท/รอทำจ่าย/เสร็จสิ้น) manual ไม่ได้ · event เท่านั้น |
| BR-CBM-03 | idempotent + optimistic (row_version) ทุก action/event |
| BR-CBM-04 | reverse/reject/cancel/void ต้องมี reason + audit · ห้ามย้อนข้ามแกน |
| BR-CBM-05 | debt % 0-100 · offset จริงที่ Payment |
| BR-CBM-06 | completed → read-only |
| BR-CBM-07 | print CUT ≥ awaiting_cutting · DLV ≥ awaiting_dispatch |
| BR-CBM-08 | ไม่มี dispatched · ปิดแกน B ด้วย closed_at |
| BR-CBM-09 | verified label "อนุมัติรอบจองแล้ว" |
| BR-CBM-10 | derived display + phase "-" + filter "ยังไม่เริ่ม" |

## §5.2 State Machine (LOCK-01..05) — combined 10-step
`รออนุมัติ → อนุมัติรอบจองแล้ว → รอส่งอนุมัติตัด → รออนุมัติตัด → รอตัด → รอจัดส่ง → อยู่ระหว่างจัดส่ง → รอผลการเท → รอทำจ่าย → เสร็จสิ้น`
Transition matrix ดู invariants §4 · ทางออกพิเศษ: rejected/cancelled/deleted (แกน A)

## §5.3 Permission (→ invariants §4)
CBM.Approver/Admin · Cut.Manager · Dispatch.Manager · Finance.Manager (events) · SoD flag (OQ-CB4)

## §5.4 Validation
| VR | Rule | Message |
|---|---|---|
| VR-01 | quota/season/รถ/เลน/เวลา required | "กรุณากรอกข้อมูลให้ครบถ้วน" |
| VR-02 | debt % 0-100 | "หักหนี้ต้องอยู่ระหว่าง 0-100" |
| VR-03 | reason บังคับ (reject/cancel/void/reverse) | "กรุณาระบุเหตุผล" |
| VR-04 | no-skip guard | "ไม่สามารถข้ามขั้นตอนได้" |
| VR-05 | system-controlled manual | "สถานะนี้ระบบจะอัปเดตให้อัตโนมัติ เมื่อข้อมูลจากระบบอื่นเสร็จสิ้น" |
| VR-06 | print gate | "ต้องอนุมัติตัดก่อน จึงจะพิมพ์ใบสั่งตัดได้" / "ต้องอยู่สถานะรอจัดส่งขึ้นไป จึงจะพิมพ์ใบนำส่งได้" |

## §5.5 Edge Cases
| EC | Case | Expected |
|---|---|---|
| EC-01 | approve booking | verified · Gate B เปิด |
| EC-02 | ขออนุมัติตัด ก่อน verified | block (Gate) |
| EC-03 | ข้ามขั้น (เช่น อนุมัติตัด ก่อนขออนุมัติตัด) | VR-04 "ไม่สามารถข้ามขั้นตอนได้" |
| EC-04 | manual set รอทำจ่าย/เสร็จสิ้น | VR-05 block ILLEGAL_STATE_TRANSITION |
| EC-05 | check-in event | derived "รอผลการเท" |
| EC-06 | receiving-completed สำเร็จ | ปิดแกน B (closed_at) + payment=awaiting_payment ("รอทำจ่าย") |
| EC-07 | receiving-completed แต่สร้างคำขอจ่ายล้ม | คง dispatching + banner "สร้างคำขอจ่ายไม่สำเร็จ — ระบบจะพยายามใหม่อัตโนมัติ" + retry |
| EC-08 | payment-completed | completed (lock) |
| EC-09 | event ซ้ำ (event_id เดิม) | 409/no-op ไม่ซ้ำผล |
| EC-10 | print CUT ก่อน awaiting_cutting | VR-06 block |
| EC-11 | print DLV ก่อน awaiting_dispatch | VR-06 block |
| EC-12 | void ที่ อยู่ระหว่างจัดส่ง | revert → รอจัดส่ง + clear dispatch_started_* |
| EC-13 | edit หลัง completed | read-only (BR-06) |
| EC-14 | phase display | approval≠verified → B/C "-" · verified&cut=null → "รอส่งอนุมัติตัด" |
| EC-15 | filter "ยังไม่เริ่ม" B | คืนเฉพาะ cut=null (& approval=verified แสดง รอส่งอนุมัติตัด) |
| EC-16 | optimistic stale | 409 CONFLICT_UPDATE_STALE |

## §5.6 Error Catalog
VALIDATION_FAILED "กรุณากรอกข้อมูลให้ครบถ้วน" · FORBIDDEN "ไม่มีสิทธิ์ดำเนินการ" · ILLEGAL_STATE_TRANSITION "ไม่สามารถข้ามขั้นตอนได้" / "สถานะนี้ระบบจะอัปเดตให้อัตโนมัติ…" · CONFLICT_UPDATE_STALE(409) "ข้อมูลถูกแก้ไขโดยผู้อื่น กรุณารีเฟรช" · CONFLICT(409) "รายการซ้ำ (idempotent)"
