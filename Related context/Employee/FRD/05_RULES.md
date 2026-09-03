# 05_RULES — F-EMP-001 Employee Master

> **Audience:** BE dev + QA
> **Purpose:** Business Rules + Validation + Edge Cases + Error Catalog + Security + State Machine + D-CLASS

---

## §5.1 Business Rules (จาก BRD §9)

| Rule ID | Rule | Tag | Enforced by |
|---|---|---|---|
| R01 | รหัส = `EMP-` + running 4 หลัก | FIXED (format), CONFIGURABLE (padding/prefix) | FN-04 generateEmployeeCode |
| R02 | 1 Employee : 1 User (employee_id UNIQUE) | FIXED | DB unique + F-IAM-01 |
| R03 | ห้ามลบ Employee ที่มี linked User (ON DELETE RESTRICT) | FIXED | FN-10/FN-11 |
| R04 | zip derive จากตำบล + locked | FIXED (lock), DYNAMIC (source) | ENG-02 |
| R05 | same_addr → copy cur→reg | FIXED | FN-05 |
| R06 | status ตาม state machine | FIXED | ENG-05 |
| R07 | ระยะทดลองงาน default 90 วัน | CONFIGURABLE (Admin Panel) | config key `probation_days` |
| R08 | DoA อนุมัติ lifecycle | CONFIGURABLE/WARNING | DOA Engine (Phase 3) |
| R09 | national_id 13 หลัก + checksum | CONFIGURABLE | ENG-01 |
| R10 | work_email domain | CONFIGURABLE | config key `work_email_domain` |
| R11 | Data Classification per field | FIXED | §5.7 D-CLASS + ENG-04 |
| R12 | supervisor ≠ self, no cycle | FIXED | FN-08/ENG-03 |
| R13 | snapshot org ณ บันทึก | FIXED | FN-09 org_snapshot |
| R14 | masking sensitive ตาม role (ABAC) | DYNAMIC | ENG-04 + Policy Center |

## §5.2 Validation Rules
| VR | Field/Action | เงื่อนไข | ประเภท | Error |
|---|---|---|---|---|
| VR01 | first_th,last_th | required | Error | ERR_VALIDATION (name) |
| VR02 | position_id,branch_id,hire_date,emp_type | required | Error | ERR_VALIDATION (employment) |
| VR03 | national_id | 13+checksum (ถ้ากรอก) | Error | ERR_INVALID_NATIONAL_ID |
| VR04 | national_id | unique | Error | ERR_DUPLICATE_NATIONAL_ID |
| VR05 | subdistrict | เลือก → zip auto | Trigger | — |
| VR06 | district/subdistrict | disabled ถ้าไม่เลือกระดับบน | Prevent | — |
| VR07 | supervisor_id | ≠self, no cycle | Error | ERR_INVALID_SUPERVISOR |
| VR08 | delete | linked user | Prevent | ERR_EMPLOYEE_HAS_LINKED_USER |
| VR09 | probation failed/extended | require reason/date | Error | ERR_REASON_REQUIRED |
| VR10 | CSV row | position/branch code มีจริง | Error | ERR_CSV_VALIDATION |
| VR11 | update | version match | Error | ERR_VERSION_CONFLICT |
| VR12 | sensitive change | ต้อง approval | Error | ERR_SENSITIVE_CHANGE_NEEDS_APPROVAL |

## §5.3 Edge Cases (จาก BRD §10 + Phase 2.5)
| EC | กรณี | Handling | Probe |
|---|---|---|---|
| E01 | ลบที่มี linked user | BLOCK + แจ้งถอนบัญชี | — |
| E02 | zip ไม่พบใน master | ปล่อยว่าง + เตือน | — |
| E03 | same_addr=true | copy ตอน save | — |
| E04 | เปลี่ยน position | เสนอ division/dept อัตโนมัติ | — |
| E05 | position/branch inactivate หลังผูก | ใช้ org_snapshot + เตือน | PR-3 |
| E06 | supervisor ถูกลบ | set ลูกน้อง supervisor_id=null | PR-3 |
| E07 | แก้พร้อมกัน 2 คน | optimistic lock (version) → ERR_VERSION_CONFLICT | PR-2 |
| E08 | national_id ซ้ำ | block (partial-unique index) | PR-1 |
| E09 | supervisor cycle | block (ENG-03) | PR-1 |
| E10 | รหัส EMP race | DB sequence/transaction + retry | PR-2 |
| E11 | ไฟล์ใหญ่เกิน limit | reject + แจ้งขนาด | PR-6 |
| E12 | ชนิดไฟล์ไม่อนุญาต | reject | PR-6 |
| E13 | ขยายทดลองงานเกิน N ครั้ง | require Dept Head approval | PR-9 |
| E14 | status ข้ามขั้น | block (ENG-05) | PR-9 |
| E15 | role ไม่มีสิทธิ์เห็น sensitive | mask (ENG-04) | PR-7 |
| E16 | export PII จำนวนมาก | Export Limit + audit | PR-7 |

## §5.4 Error Catalog
| Error Code | HTTP | ความหมาย |
|---|---|---|
| ERR_VALIDATION | 400 | field ไม่ผ่าน (พร้อม list) |
| ERR_INVALID_NATIONAL_ID | 400 | เลขบัตรไม่ถูก checksum |
| ERR_DUPLICATE_NATIONAL_ID | 409 | เลขบัตรซ้ำ |
| ERR_CODE_RACE | 409 | รหัสชนกัน (retry) |
| ERR_VERSION_CONFLICT | 409 | แก้พร้อมกัน |
| ERR_INVALID_SUPERVISOR | 400 | self/cycle |
| ERR_EMPLOYEE_HAS_LINKED_USER | 409 | ลบไม่ได้ มีบัญชีผูก |
| ERR_EMPLOYEE_NOT_FOUND | 404 | ไม่พบ |
| ERR_INVALID_STATE_TRANSITION | 422 | เปลี่ยนสถานะผิดลำดับ |
| ERR_REASON_REQUIRED | 400 | ขาดเหตุผล/วันที่ |
| ERR_SENSITIVE_CHANGE_NEEDS_APPROVAL | 422 | แก้ field อ่อนไหวต้องอนุมัติ |
| ERR_CSV_FORMAT / ERR_CSV_VALIDATION | 400/422 | CSV ผิดรูป/ข้อมูล |
| ERR_INSUFFICIENT_ROLE | 403 | สิทธิ์ไม่พอ |
| ERR_NOT_AUTHENTICATED | 401 | ไม่ได้ login |

## §5.5 COSO / SoD (จาก BRD §5)
- Maker (HR Officer) ≠ Approver (HR Manager/Dept Head) — บังคับในทุก approval action
- sensitive change (salary/bank): Maker→Checker(HR Manager)→Approver(HR Director)
- delete: Checker(HR Manager)+Approver(Dept Head+IT)

## §5.6 State Machine (employee-status-machine / ENG-05)
| Current | Action | Next | Guard |
|---|---|---|---|
| onboarding | start-probation | probation | set probation_start/end |
| probation | pass | active | result=passed |
| probation | fail | terminated | reason required |
| probation | extend | probation | new_end_date |
| active | leave | leave | — |
| leave | return | active | — |
| active | suspend | suspended | Dept Head+HR |
| suspended | reinstate | active | — |
| active/leave | resign | resigned | resign fields |
| active/leave | terminate | terminated | resign fields |
> ห้าม transition นอกตาราง → ERR_INVALID_STATE_TRANSITION (E14)

## §5.7 Security Bible Application (P6 — HR/PII, 15 controls)

> Domains: D2 (Auth), D7 (PII), Admin/SoD, D-CLASS · Preset P6 จาก BRD §16

### D2: Authentication & Session
- ทุก endpoint JWT + X-Tenant-Id · MFA สำหรับ HR role (S02-02; rollout = OQ)

### D7: PII Protection
- mask national_id/sso/tax/bank ใน response (ENG-04) · logs ใช้ ID ไม่ใส่ PII · column encryption (optional) สำหรับ Restricted

### SoD / Audit (S01-04, S01-07, S06-03)
- Maker≠Approver · immutable before/after audit ทุก mutation (sensitive เน้น who/what/when/where/result)

### D-CLASS: Data Classification ⭐ (รายละเอียด 04_DB §4.2 + §4.6)
| Layer | Confidential | Restricted |
|---|---|---|
| API response | mask if no permission | excluded ถ้าไม่ผ่าน ACL |
| UI display | `***` | hidden + audit access |
| Export/Print | excluded ถ้า role ไม่ผ่าน | require Restricted Resources approval (S02-06 Export Limit) |
- PDPA: Consent (S07-01), RTBF/Anonymization (S07-04) — Phase 2+ (OQ-03)
