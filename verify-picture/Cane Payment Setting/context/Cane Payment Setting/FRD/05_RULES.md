# 05_RULES — F-AGM-012 Cane Payment Setting

## §5.1 Business Rules (→ invariants §3)
| BR | Rule |
|---|---|
| BR-PS-01 | Payment Setting = SoT ต่อ season×product (Cane Payment อ่าน active) |
| BR-PS-02 | ราคาต่อตัน = Base@10CCS + (CCS − 10) × (Base@10CCS × K) |
| BR-PS-03 | งวด 1/2 = 50/50 |
| BR-PS-04 | VAT ก่อนแบ่งงวด (ถ้าเปิด) |
| BR-PS-05 | ดอกเบี้ยเฉพาะบิลขาว: daily_rate=roundUp(rate_year/base_days,7) · days_early=max(0,normal−actual) · interest=inst_after_debt×daily_rate×days_early |
| BR-PS-06 | บิลขาว WITH_CANE (พร้อมค่าอ้อย) = วันจ่ายบิลเขียว + ไม่คิดดอกเบี้ย |
| BR-PS-07 | Green = normal pay date · White FIXED_DATE = actual pay date |
| BR-PS-08 | Bank fee: โอน + จังหวัดบัญชี=จังหวัดหลัก→in-fee · ต่าง→out-fee · เช็ค/เงินสด→0 · หักหลังหักหนี้+ดอกเบี้ย |
| BR-PS-09 | Payment Setting ไม่ fix วิธีจ่าย |
| BR-PS-10 | Preview non-persistent |
| BR-PS-11 | unique Active per season×product · payout no-overlap |
| BR-PS-12 | audit + optimistic lock ทุก mutation |

## §5.2 State Machine (→ invariants §4)
Setting: `Active ⇄ Inactive` (unique Active per season×product) · Edit ห้ามเมื่อ Inactive
White schedule pay_type: `FIXED_DATE (มี pay_date)` / `WITH_CANE (pay_date=null)`

## §5.3 Permission (RBAC → invariants §5)
Finance Manager (CRUD+status) · Finance Officer (update config/charges/schedule + preview) · Operations (view+preview) · Auditor (read-only)

## §5.4 Validation
| VR | Rule | Message |
|---|---|---|
| VR-01 | interest_rate_year > 0 | "ดอกเบี้ยต่อปีต้องมากกว่า 0" |
| VR-02 | base_days > 0 | "วันฐานต้องมากกว่า 0" |
| VR-03 | main_province required (bank fee) | "กรุณาเลือกจังหวัดหลัก" |
| VR-04 | bank fee ≥ 0 | "ค่าธนาคารต้องไม่ติดลบ" |
| VR-05 | K 0–1 | "ค่า K ต้องอยู่ระหว่าง 0–1" |
| VR-06 | Green from≤to (1–31) + pay dates + no-overlap | "ช่วงวันที่ซ้อนทับกัน" / "กรุณากรอกวันจ่าย" |
| VR-07 | White FIXED_DATE ⇒ pay_date · WITH_CANE ⇒ null | "กรุณากรอกวันจ่ายเมื่อเลือกวันที่กำหนด" |
| VR-08 | unique Active | "มีการตั้งค่า Active สำหรับรอบหีบ+สินค้านี้อยู่แล้ว" |

## §5.5 Edge Cases
| EC | Case | Expected |
|---|---|---|
| EC-01 | กรอกดอกเบี้ยต่อปี+วันฐาน | daily_rate auto = roundUp(7) read-only |
| EC-02 | interest_rate_year ≤ 0 | VR-01 block |
| EC-03 | bank fee ไม่เลือกจังหวัดหลัก | VR-03 block |
| EC-04 | CCS preview | ราคาต่อตัน/กก. ตามสูตร |
| EC-05 | Green schedule overlap | VR-06 block |
| EC-06 | White FIXED_DATE ไม่กรอกวัน | VR-07 block |
| EC-07 | White WITH_CANE | วันจ่าย = "ตามตารางบิลเขียว (ไม่คิดดอกเบี้ย)" |
| EC-08 | Preview บิลขาวงวด n | days_early + interest แสดง |
| EC-09 | Preview บิลเขียว | ไม่มีดอกเบี้ย |
| EC-10 | Preview จังหวัด=หลัก | in-province fee |
| EC-11 | Preview จังหวัดต่าง | out-province fee |
| EC-12 | Save unique Active ซ้ำ | VR-08 (409) |
| EC-13 | Edit Inactive | guard (redirect+403) |
| EC-14 | Save stale ETag | 412 CONFLICT_UPDATE_STALE |

## §5.6 Error Catalog
VALIDATION_FAILED · SCHEDULE_OVERLAP "ช่วงวันที่ซ้อนทับกัน" · INVALID_PAY_TYPE · CONFLICT(409) "มีการตั้งค่า Active สำหรับรอบหีบ+สินค้านี้อยู่แล้ว" · CONFLICT_UPDATE_STALE(412) "ข้อมูลไม่ตรงปัจจุบัน กรุณารีเฟรช" · FORBIDDEN(403) "คุณไม่มีสิทธิ์ดำเนินการนี้"
