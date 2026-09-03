# 06_TESTS — F-EMP-001 Employee Master

> **Audience:** QA
> **Purpose:** Acceptance Criteria per FR + Definition of Done

---

## §6.1 Acceptance Criteria (Given-When-Then)

### AC-01 สร้างพนักงาน (S-01 / API-03)
- Given HR เปิด P-03, When กรอก required ครบ + บันทึก, Then ออกรหัส EMP-NNNN + บันทึก + ไป P-02
- Given required ไม่ครบ, When บันทึก, Then คงหน้า + ระบุ field ที่ขาด (ไม่สูญข้อมูล)

### AC-02 Address cascade (S-02 / API-10)
- Given ยังไม่เลือกจังหวัด, When เปิดอำเภอ, Then อำเภอ disabled
- Given เลือกตำบล, When derive, Then zip เติมอัตโนมัติ + disabled

### AC-03 Profile tabbed (S-03 / API-02)
- Given เปิด P-02, When โหลด, Then เห็น 7 แท็บ + quick-facts
- Given role ไม่มีสิทธิ์เห็น salary, When เปิดแท็บงาน, Then salary/bank แสดง masked

### AC-04 Delete guard (S-04 / API-05)
- Given พนักงานมี linked user, When ลบ, Then BLOCK + แจ้งถอนบัญชี (ERR_EMPLOYEE_HAS_LINKED_USER)
- Given ไม่มี user, When ยืนยันลบ, Then soft-delete + audit

### AC-05 Probation (S-05 / API-06)
- Given status=probation, When result=passed + อนุมัติ, Then status=active
- Given result=failed, When บันทึกไม่ใส่เหตุผล, Then ERR_REASON_REQUIRED

### AC-06 CSV import (S-06 / API-08)
- Given upload CSV, When validate, Then preview ผ่าน/ไม่ผ่าน รายแถว ก่อน apply
- Given mode=replace, When apply, Then คงพนักงานที่มี linked user

### AC-07 Optimistic lock (E07 / API-04)
- Given 2 HR แก้คนเดียวกัน, When คนที่ 2 บันทึกด้วย version เก่า, Then ERR_VERSION_CONFLICT

### AC-08 Sensitive change (VR12 / API-04)
- Given HR Officer แก้ salary/bank, When บันทึก, Then เข้าสู่ approval flow (HR Manager→HR Director)

### AC-09 State machine (E14 / ENG-05)
- Given status=onboarding, When สั่ง resign, Then ERR_INVALID_STATE_TRANSITION

### AC-10 national_id (VR03/VR04)
- Given national_id ผิด checksum, Then ERR_INVALID_NATIONAL_ID
- Given national_id ซ้ำ, Then ERR_DUPLICATE_NATIONAL_ID

### AC-11 Supervisor cycle (VR07/ENG-03)
- Given เลือก supervisor ที่ทำให้เกิด cycle, Then ERR_INVALID_SUPERVISOR

### AC-12 Export limit/audit (E16/API-09)
- Given export CSV ที่มี PII, When ดำเนินการ, Then enforce Export Limit + บันทึก audit; Restricted columns excluded ถ้าไม่ผ่าน ACL

## §6.2 Test Coverage Map
| API | AC | Edge |
|---|---|---|
| API-01 | list/filter | — |
| API-02 | AC-03 | E15 masking |
| API-03 | AC-01, AC-10 | E08,E10 |
| API-04 | AC-07, AC-08, AC-11 | E07,E09 |
| API-05 | AC-04 | E01 |
| API-06/07 | AC-05, AC-09 | E13,E14 |
| API-08 | AC-06 | E11,E12,VR10 |
| API-09 | AC-12 | E16 |
| API-10 | AC-02 | E02 |
| API-11 | AC-04 | — |

## §6.3 Definition of Done
- [ ] ทุก AC ผ่าน (12 AC)
- [ ] RLS multi-tenant verified (ไม่เห็นข้าม tenant)
- [ ] Classification enforced: Confidential masked, Restricted excluded/audited
- [ ] 2 Governance checkpoints: User Access (F-IAM-02) map สิทธิ์ + DOA Pre-fields พร้อม wire (F-PC-DOA-01)
- [ ] Audit log immutable (before/after) ทุก mutation
- [ ] Prototype parity: list/profile/full-page form/cascade/CSV ตรง employee-management.html
- [ ] No orphan logic (R8) · conventions pass (camelCase fn / kebab engine / snake field)
