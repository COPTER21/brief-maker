# 05_RULES — F-PURCH-CFG-001 ตั้งค่าการจัดซื้อ (Purchase Configuration)

> **Audience:** BE + QA

---

## §5.1 Business Rules
| Rule | Rule | Tag |
|---|---|---|
| R01 | กติกาทั้งหมดอ่านจาก config — PR/PO/CP **ห้าม hardcode** | FIXED |
| R02 | enable_comparison=off → comparison_required/min/threshold/award ถูก disable | CONFIGURABLE |
| R03 | default_payment_type ต้อง ∈ pt_enabled (true) | FIXED |
| R04 | รายการ payment types ดึงจาก Payment Term (Finance); ที่นี่เลือกเปิดใช้ + ค่าเริ่มต้น inherit→PO | FIXED |
| R05 | ไม่มี cost_center/budget_account ใน PR mandatory — มากับใบปลดอายัด (UNLK); บังคับใบปลดอายัด อ่านจาก Budget Config | FIXED |
| R06 | approval ส่ง amount→DOA — ไม่ตั้ง tier ที่นี่ | FIXED |
| R07 | Direct Payment ไม่อยู่ที่นี่ (เปิดที่ AP Invoice — Finance) | FIXED |
| R08 | เลขที่เอกสารไม่ซ้ำ (atomic issue) + reset ตาม reset_cycle (last_reset_period กันซ้ำ) | FIXED |
| R09 | config มีผล forward-only (ไม่ย้อนเอกสารเดิม) | FIXED |
| R10 | ทุกการเปลี่ยน config/numbering เขียน audit log (diff old→new) | FIXED |
| R11 | comparison min/threshold/award · deposit%/installment/credit · numbering ปรับได้ | CONFIGURABLE |
| R12 | locked decisions D01–D15 = ไม่ทำเป็น toggle (read-only) | FIXED |

## §5.2 Validation
| VAL | เงื่อนไข | ผล |
|---|---|---|
| VAL-01 | enable_comparison=off & comparison_required=on | บังคับ required=off (disable ลูก) |
| VAL-02 | default_payment_type ∉ pt_enabled | block save / reset เป็นตัวแรกที่เปิด |
| VAL-03 | prefix ว่าง หรือ digits<1 | block + inline error |
| VAL-04 | next_no ≤ เลขที่ออกไปแล้ว | เตือนเสี่ยงเลขซ้ำ |
| VAL-05 | ปิดทุก payment type | block (≥1) |
| VAL-06 | ผู้ใช้ไม่มีสิทธิ์ edit | 403 ACCESS_DENIED |

## §5.3 State Machine
- config: working(dirty) → **active** (บันทึก) · ไม่มี lifecycle ซับซ้อน · มีผล forward-only
- numbering: next_no increment ต่อการ issue · รีเซ็ตเมื่อขึ้นรอบ (yearly/monthly) ครั้งเดียวต่อรอบ (last_reset_period)

## §5.5 Edge Cases
| EC | สถานการณ์ | คาดหวัง |
|---|---|---|
| EC-01 | เปลี่ยน config ขณะมี PR draft | PR ยังไม่ submit → ใช้ config ใหม่ตอน validate · submit แล้ว → คงเดิม (forward-only) |
| EC-02 | ปิด enable_comparison ขณะมี CP ค้าง | CP เดิมเดินต่อ · PR ใหม่ข้าม CP |
| EC-03 | ขึ้นปี/เดือนใหม่ + reset_cycle | next_no รีเซ็ต 1 ครั้งเดียว (last_reset_period กันซ้ำ) |
| EC-04 | ลด payment type ที่ default ใช้ | VAL-02 |
| EC-05 | 2 admin แก้พร้อมกัน | optimistic lock (updated_at) — เตือน reload |
| EC-06 | issue เลขพร้อมกัน (concurrent PR create) | atomic FOR UPDATE — ไม่ซ้ำ |

## §5.6 Error Catalog
| Error | HTTP | ข้อความ |
|---|---|---|
| ACCESS_DENIED | 403 | ไม่มีสิทธิ์แก้ตั้งค่าการจัดซื้อ |
| VALIDATION_FAILED | 400 | ตั้งค่าไม่ถูกต้อง (+รายการ field) |
| NUMBERING_INVALID | 400 | รูปแบบเลขที่ไม่ถูกต้อง |

## §5.7 D-CLASS Enforcement
- **Internal** ทั้งหมด · edit role-gated (FN-09) · audit ทุกการเปลี่ยน · ไม่มี Confidential/PII/Restricted
