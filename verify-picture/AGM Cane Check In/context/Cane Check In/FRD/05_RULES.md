# 05_RULES — F-AGM-010 Cane Check-In

## §5.1 Business Rules (→ invariants §3)
| BR | Rule |
|---|---|
| BR-CI-01 | 3 วิธีเช็คอิน: CBM (รหัส/QR) · ไม่มีคิว-สมาชิก · ไม่มีคิว-โควต้ากลาง |
| BR-CI-02 | weighToken (เลขเหรียญชั่ง) บังคับทุกการเช็คอิน |
| BR-CI-03 | CBM check-in → event CHECK_IN → booking "รอผลการเท" (idempotent checkin_id) |
| BR-CI-04 | Sync fail → syncPending + badge ซิงก์ล้มเหลว + retry (idempotent) |
| BR-CI-05 | entry type → doc: จองคิว=CBM · ไม่จองคิว/กลาง=NBM |
| BR-CI-06 | Member/Central: payment bill งวด1+2 (บิลเขียว/บิลขาว) บังคับ |
| BR-CI-07 | Void + เหตุผล (ไม่บังคับ) |
| BR-CI-08 | 2-tab: ต้องส่ง → เช็คอินแล้ว |
| BR-CI-09 | สถานะ Booking column (checked-in, CBM only) · non-CBM = "-" |
| BR-CI-10 | QR scan / manual CBM entry |

## §5.2 State Machine (→ invariants §4)
CheckIn: `ต้องส่ง(จัดส่ง) → เช็คอินแล้ว(รอทำจ่าย) → เสร็จสิ้น` · void: เช็คอินแล้ว → ยกเลิก
Booking sync: `(no sync) → syncing → success(รอผลการเท)/fail(syncPending+retry)`

## §5.3 Permission (→ invariants §6)
เจ้าหน้าที่ชั่ง (เช็คอิน+retry+void) · หัวหน้ากะ (void) · Cane Booking (รับ event)

## §5.4 Validation
| VR | Rule | Message |
|---|---|---|
| VR-01 | weighToken required (CBM) | "กรุณาใส่เลขเหรียญชั่ง" |
| VR-02 | CBM code valid | "ไม่พบรหัส CBM นี้" |
| VR-03 | quota valid (member) | "ไม่พบโควต้านี้" |
| VR-04 | ข้อมูลครบ (Member/Central) | "กรุณากรอกข้อมูลให้ครบถ้วน" |
| VR-05 | payment bill งวด1+2 | "กรุณาเลือกประเภทการชำระเงินให้ครบถ้วน" |

## §5.5 Edge Cases
| EC | Case | Expected |
|---|---|---|
| EC-01 | CBM check-in สำเร็จ | check-in + sync → booking รอผลการเท |
| EC-02 | CBM code ไม่มี | VR-02 "ไม่พบรหัส CBM นี้" |
| EC-03 | weighToken ว่าง | VR-01 "กรุณาใส่เลขเหรียญชั่ง" |
| EC-04 | sync ล้ม (network) | syncPending=true + badge "ซิงก์ล้มเหลว" + retry |
| EC-05 | retry สำเร็จ | "ซิงก์สถานะ Booking สำเร็จ" (idempotent no dup) |
| EC-06 | retry ล้มอีก | "ซิงก์ล้มเหลว กรุณาลองใหม่" |
| EC-07 | member quota ไม่พบ | VR-03 "ไม่พบโควต้านี้" |
| EC-08 | member พบ | "พบข้อมูลสมาชิก" + auto-fill |
| EC-09 | ข้อมูลไม่ครบ | VR-04 |
| EC-10 | payment bill ไม่ครบ | VR-05 |
| EC-11 | central check-in สำเร็จ | "เช็คอินสำเร็จ" (NBM doc, no sync) |
| EC-12 | void | "ยกเลิกเช็คอินสำเร็จ" |
| EC-13 | QR scan/manual | เปิด CBM check-in flow |
| EC-14 | checked-in non-CBM สถานะ Booking | "-" |
| EC-15 | sync dup (same checkin_id) | 409/no-op |

## §5.6 Error Catalog
VALIDATION_FAILED · NOT_FOUND "ไม่พบรหัส CBM นี้"/"ไม่พบโควต้านี้" · SYNC_FAILED(retryable) "ซิงก์ล้มเหลว กรุณาลองใหม่" · CONFLICT(409 dup) "รายการซ้ำ (idempotent)"
