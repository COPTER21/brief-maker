# CTX — F-HR-WELFARE: Welfare (สวัสดิการ)

> **derived from:** FRD_F-HR-WELFARE v1.0 (2026-09-08) · **generated:** 2026-09-08
> **module:** HR (CUBE 4.0) · **feature code:** F102 · **status:** active (FRD DRAFT · พร้อม review)
> ⚠ Derived artifact — source of truth คือ FRD Pack · ถ้า FRD revise ต้อง regen CTX

---

## 1. Summary

ทะเบียนและคำขอใช้สิทธิ์ **สวัสดิการพนักงาน** (benefit type แบบ versioned + effective dating · โควตา/วงเงินต่อปีต่อกลุ่ม). พนักงาน/HR ยื่นคำขอใช้สิทธิ์ (self หรือ dependent) → ส่งอนุมัติผ่าน **DOA** (2 ขั้น · one-step advance) → ขั้นสุดท้าย re-check เพดาน แล้วตัดคงเหลือ (live ledger) + บันทึกมูลค่าเข้า **CSQ 7C·EC** + ส่งสถานะจ่าย (hook display-only ไป Payroll/Expense). รองรับไม่อนุมัติ / ยกเลิก (ก่อนอนุมัติ) / ระงับตาม leaver signal / และ **กลับรายการ (reversal)** ของคำขอที่อนุมัติแล้วแบบ append-only. คงเหลือ = computed live จาก ledger (approved only) · ผู้ให้บริการ/flex/จ่ายเงินจริง = out of scope.

## 2. Data Contract

> Source: FRD 04_DB. เอาเฉพาะ entities/fields ที่ feature อื่น join/อ่าน + keys/status/amount/refs. Field UI ล้วน (display_order ฯลฯ) ตัดออก. Owner ทุกตาราง = F-HR-WELFARE เว้นที่ระบุ soft ref.

### Entities
| Entity | PK | Key Fields | หมายเหตุ |
|---|---|---|---|
| T_welfare_benefit_type | id (uuid) | tenant_id, code (WEL-xxxx · versioned), name, cat, unit, quota, covers_dep, groups[] (jsonb ≥1), eff_from, eff_to, version, status, claimable, company_scope | master versioned; เวอร์ชันใช้ `code` ร่วม + version + effective dating (no-overlap). percent → claimable=false, quota=null |
| T_welfare_dependent | id (uuid) | tenant_id, employee_id (soft ref), name (Restricted), rel, dob, eligible | ผู้ติดตาม owned by Welfare (A-WEL-04); บุตร>20 บล็อก |
| T_welfare_request | id (uuid) | request_no (UNIQUE ต่อ tenant · internal display id ไม่ใช่เลขรันทางการ), employee_id (soft ref) + employee_snapshot (jsonb), use_for_type, use_for_dep_id, benefit_type_id (FK), amount, value (Restricted), use_date, status, pay, reject_reason/revoke_reason/reverse_reason, reversed_at, payroll_clawback, config_version_id, version_lock | transaction (state machine §5.2a). value → 7C·EC. snapshot ชื่อ/ตำแหน่ง + config_version ณ บันทึก (BR-10) |
| T_welfare_request_approval | id (uuid) | tenant_id, request_id (FK), step, role (role-id จาก DOA · ไม่ hardcode), person (jsonb {name,position}), status, acted_at | สาย DOA snapshot · append-only freeze หลัง submit · UNIQUE(request_id, step) |
| T_welfare_request_attachment | id (uuid) | tenant_id, request_id (FK), file_name, file_url, mime, size | หลักฐานแนบ; attachment policy deferred |
| T_welfare_audit_log | id (uuid) | tenant_id, entity, entity_id, action, actor, diff (jsonb), note, created_at | append-only · no update/delete (LK-5) |
| T_employee | (existing) | — | soft ref snapshot ชื่อ/ตำแหน่ง/แผนก/กลุ่ม (owner F011 · no FK cascade) |

> **ไม่มี** T_welfare_balance (คงเหลือ = computed) · **ไม่มี** running-number table (request_no = internal seq · NS-5).

### Enums / States (ครบทุกค่า — ห้าม compress)
| Field | Values | Transition owner |
|---|---|---|
| request.status | `draft` → `submitted` → `pending_approval` → `approved` → `closed`; branches: `rejected` · `cancelled` · `revoked` · `reversed` (9 states ตามตรรกะ; UI pill รวม submitted+pending_approval = "รออนุมัติ") | feature นี้ (reversed = FN-14 append-only; revoked = leaver signal; closed = system) |
| benefit_type.status | `draft` → `active` → `archived` (superseded เมื่อออกเวอร์ชันใหม่ · soft archive) | feature นี้ |
| request.pay | `none` · `pending` · `sent` | อ่านจาก Payroll/Expense (display-only hook · LK-2) |
| benefit_type.unit | `money` · `times` · `percent` (percent = ไม่ตัดยอด · claimable=false) | feature นี้ |
| request.use_for_type | `self` · `dependent` (dependent → use_for_dep_id required) | feature นี้ |
| dependent.rel | `คู่สมรส` · `บุตร` · `บิดา` · `มารดา` | feature นี้ |
| benefit_type.cat | `สุขภาพ` · `ครอบครัว` · `การเงิน` | feature นี้ |
| approval.status | `pending` · `current` · `approved` · `rejected` | feature นี้ (one-step advance) |
| audit_log.action | `create` · `update` · `publish` · `version` · `archive` · `submit` · `approve` · `reject` · `cancel` · `revoke` · `reverse` | feature นี้ |

### State transitions — request (ครบทุกเส้น)
| From | To | Action | Allowed roles | Condition / effect |
|---|---|---|---|---|
| draft | submitted → pending_approval | submit | ผู้ยื่น/admin | เลือก DOA ครบทุกขั้น (VR-09) · resolve+freeze chain |
| draft / pending_approval | cancelled | cancel | owner/admin | pre-approval เท่านั้น · ไม่กระทบคงเหลือ |
| pending_approval | pending_approval | approve (ขั้นกลาง) | approver (DOA) | one-step advance (current→approved, next→current) · ไม่ collapse ทั้งสาย |
| pending_approval | approved | approve (ขั้นสุดท้าย) | approver (HR · DOA) | re-check eligibility+เพดาน (FIX-02) → ตัดคงเหลือ + CSQ EC + pay hook |
| pending_approval | rejected | reject | approver | reason required · **ไม่ตัดคงเหลือ** |
| approved | reversed | reverse | admin/manager | reason required · append-only · คืนคงเหลือ + EC reverse + clawback flag |
| any (pre-closed) | revoked | leaver signal | system | คงเหลือหยุด · null≠ทำงาน (BR-06) |
| approved | closed | ปิดรอบ/หมดอายุ | system | — |

### Relationships
- T_welfare_benefit_type (1) —< (N) T_welfare_request [benefit_type_id — เวอร์ชันที่มีสิทธิ์ ณ วันยื่น snapshot]
- T_welfare_request (1) —< (N) T_welfare_request_approval / T_welfare_request_attachment
- (all entities) (1) —< (N) T_welfare_audit_log
- อ้าง master (soft ref · snapshot · **no FK cascade** · LK-4): Employee (F011) — อ่านอย่างเดียว; HR Configuration #107 (company_scope · ปีสิทธิ์) — resolve read-only, ไม่ CRUD
- BalanceLedger = `SUM(value|amount) FROM T_welfare_request WHERE status='approved' GROUP BY employee_id, benefit code, benefit_year` — **computed, no table**

## 3. API Surface

> Prefix: `/api/v1/welfare`. ทุก endpoint: `X-Tenant-Id` + JWT. Mutations รับ `Idempotency-Key` + `If-Match` (version_lock). Source: FRD 02_API.

| Method | Endpoint | ทำอะไร | Payload หลัก / Role |
|---|---|---|---|
| GET | /benefit-types · /benefit-types/:id | list / detail+versions | any |
| POST | /benefit-types | สร้างประเภท (v1 active) | `{ name, cat, unit, quota, covers_dep, groups[], eff_from }` · admin |
| PUT | /benefit-types/:id | publish draft หรือออกเวอร์ชันใหม่ (no-overlap) | If-Match · admin |
| POST | /benefit-types/:id/archive | ปิดใช้ (soft archive · เตือนคำขอค้าง) | admin |
| POST | /employees/:empId/dependents | เพิ่มผู้ติดตาม | `{ name, rel, dob, eligible }` · admin |
| DELETE | /employees/:empId/dependents/:depId | ลบผู้ติดตาม | admin |
| GET | /requests · /requests/:id | list+filter (`?status=`) / detail 4-tab | any (own scope) |
| POST | /requests | สร้างคำขอ (`?draft=true` = draft) | `{ employee_id, use_for_type, use_for_dep_id?, benefit_type_id, amount?, value, use_date, reason?, files[] }` |
| POST | /requests/:id/submit | ส่งอนุมัติ (DOA resolve+freeze) | `{ picks:{ step: person_key } }` · ผู้ยื่น/admin |
| POST | /requests/:id/approve | อนุมัติ one-step advance / finalize | If-Match · admin/manager (ตาม DOA) |
| POST | /requests/:id/reject | ไม่อนุมัติ | `{ reason }` · admin/manager |
| POST | /requests/:id/cancel | ยกเลิก (draft/pending เท่านั้น) | owner/admin |
| POST | /requests/:id/reverse | **กลับรายการ** (approved เท่านั้น) | `{ reason }` · If-Match · admin/manager |
| GET | /balance?employee_id= | คงเหลือ + exposure + ผู้ติดตาม | admin/manager (masking) |
| GET | /report?type=&group=&from=&to= | usage report + filter + stats | admin/manager |

**Soft-ref reads (external · consumed, ไม่ owned):**
- GET /employees — Employee Master combobox (#102)
- GET /hr-config/resolve?date&company_id — HR Config #107 (company_scope · ปีสิทธิ์)
- GET /onboard/employment-window/resolve?employee_id&include=signal — joiner/leaver (F127/F128)
- GET /doa/resolve?feature=F-HR-WELFARE — DOA chain slot pools (F-DLG-001)
- (hook) pay-status Payroll F065 / Expense F101 — display-only [ASSUMED contract A-WEL-02 · FRD Phase B · **[not documented]** exact contract]

### Events emitted
| Event | ท่อ/Engine | Trigger point | Payload key |
|---|---|---|---|
| `welfare.granted` (forward) | CSQ · **EC เท่านั้น** (LK-6) | approve finalize (pending_approval→approved) | `{ ref:request_no, employee_id, benefit_type, value_declared, currency:THB, basis:declared }` |
| `welfare.granted` reverse | CSQ · EC negative offset | reverse (approved→reversed) | `{ ref:request_no, employee_id, benefit_type, value_declared:-x, currency:THB, basis:declared, reason }` |
| `welfare_request_submitted` | NTF (ENG-NOTIFY) | submit (draft→pending_approval) | `{ ref:request_no, employee }` |
| `welfare_request_result` | NTF | approve finalize / reject | `{ ref:request_no, result, reason? }` |
| `welfare_quota_near_limit` | NTF | ยอดใช้สะสม ≥80% โควตา | `{ ref, benefit_type, remaining }` |
| `welfare_eligibility_ended` | NTF | leaver signal → revoke | `{ ref:employee_id, last_day }` |
| `welfare_request_reversed` | NTF | reverse (approved→reversed) | `{ ref:request_no, reason, payroll_clawback? }` |

> DOA events (`doa_pending`/`doa_result`) = จาก DOA engine อัตโนมัติ — **feature ห้ามประกาศซ้ำ**.

## 4. Shared Rules (cross-boundary เท่านั้น)

> Source: FRD 05_RULES. เอาเฉพาะ rule ที่ module/feature อื่นต้อง conform หรือถูกกระทบ. Rule ภายใน (form validation VR-xx, UI behavior) ตัดออก.

| Rule ID | Rule | กระทบใคร |
|---|---|---|
| BR-09 / LK-6 | มูลค่าสวัสดิการ approved = เงินได้พนักงาน → ยิง CSQ **EC ท่อเดียวเท่านั้น** · Welfare ไม่คำนวณมูลค่าเอง (basis=declared) | CSQ (7C·EC) |
| BR-11 (reversal) | กลับรายการ approved = **append-only** (ไม่ลบ/แก้ของเดิม) · คืนคงเหลืออัตโนมัติ + **CSQ EC reverse (negative offset)** อ้าง request_no เดิม + `payroll_clawback` flag เมื่อ pay=sent | CSQ · Payroll (F065) · audit/finance |
| BR-05 / BR-BAL | ตัดคงเหลือ **เฉพาะ approved** · reject/cancel/revoke/reversed ไม่ตัด (reversed = คืนยอดเอง) · balance = live compute จาก ledger ไม่เก็บซ้ำ · never negative-clamp ใน logic | Payroll/Expense (revalidate วงเงิน), consumers ของ balance |
| BR-10 / LK-4 | snapshot ชื่อคน/บริษัท/config_version ณ บันทึก · **soft ref ไม่มี FK cascade** — feature ต้นทาง (Employee/HR Config) เปลี่ยน/ลบ ไม่ย้อนกระทบใบเดิม | Employee (F011), HR Config #107 |
| BR-04 / LK-1 | คำขอผ่าน DOA ก่อนตัดคงเหลือ · resolve ตอนส่ง (GET /doa/resolve) แล้ว freeze snapshot · **ห้าม hardcode chain** | DOA (F-DLG-001) |
| BR-06 | ช่วงสิทธิ์ผูก employment window (joiner เปิด · leaver ปิด) · **null last-day ≠ ไม่มีวันจบ/ยังทำงาน** | On/Offboard (F127/F128) |
| BR-07 / LK-5 | balance ledger + คำขอ + benefit type = append-only / soft archive · audit ทุก transition · **no hard delete** | audit/finance, DBA |
| BR-08 | ข้อมูลบุคคล/ผู้ติดตาม/มูลค่า = **RESTRICTED masking ตาม role** (Policy Center) · **enforce ที่ backend ไม่ใช่แค่ UI** (OQ-05) | Policy Center (Data Classification · Restricted Resources), all consumers |
| BR-BAL-2 | exposure (คำขอ pending อื่นบนสิทธิ์เดียวกัน) = **display-only · ไม่ soft-reserve** (จุดตัดสินจริง = re-check ณ final approval, FIX-02) | ผู้อนุมัติ, downstream ที่อ่าน balance |

**Permission capabilities (backend-enforced · BR-DOA-6 · OQ-05):** — anyone enforcing/consuming must honor
- `canApprove` = admin | manager (approve / reject / reverse)
- `canCancelReq` = admin | owner (cancel · pre-approval only)
- `canSeeValue` / `canSeePerson` = admin | manager (else masked `•••`)
- `canSeeDependent` = **admin เท่านั้น**
- ทะเบียน create/edit/archive = admin

## 5. Integration

- **Depends on (upstream · soft ref/hook read-only):**
  - Employee Master (F011) — ชื่อ/ตำแหน่ง/แผนก/กลุ่ม (soft ref snapshot · combobox #102)
  - On/Offboard (F127/F128) — joiner/leaver signal (employment-window/resolve)
  - HR Configuration (#107) — company_scope · ปีสิทธิ์ (resolve read-only, ไม่ CRUD)
  - DOA engine (F-DLG-001) — approval chain resolve (GET /doa/resolve · slot picker)
- **Depended by (downstream · Value Stream H2R):**
  - CSQ engine (7C·EC) — มูลค่าสวัสดิการ = เงินได้ (event welfare.granted EC · reverse → EC negative offset)
  - Payroll (F065) — สถานะจ่าย display-only + clawback flag (ตั้งเบิกคืนที่ปลายทาง · Welfare ไม่จ่ายเอง)
  - Expense (F101) — สิทธิ์สวัสดิการกำกับวงเงินเบิก (revalidate on approve)
  - Notification (F-NOTIFY) — 5 business events (incl. welfare_request_reversed)
- **Declarations (รอบนี้ 2026-09-08):**
  - **DOA** [yes] — scope `policy_approve` (อนุมัติคำขอใช้สิทธิ์ · ไม่ใช่ document_sign). Default sequential 2 ขั้น (หัวหน้าสายงาน → HR สวัสดิการ) · **no amount tier · no exec path**. reversal = HR admin/manager action, ไม่ใช่ DOA step. Exact role ids = **[not documented]** (OQ-DOA-01 · A-WEL-03/CL-0013 — placeholder `role-hr-line-manager`/`role-hr-welfare-admin` ยังไม่ verify กับ DOA master)
  - **NTF** [yes] — 5 events (submitted · result · quota_near_limit · eligibility_ended · request_reversed) · กลุ่มใหม่ "สวัสดิการ (welfare_*)" ใน F-NOTIFY. DOA events ไม่ประกาศซ้ำ
  - **CSQ** [yes] — EC forward (welfare.granted) + EC reverse (negative offset) · EC ท่อเดียว. ไม่ประกาศ OC/DC/SC/AC/FC
  - **DOCCFG** [no] — NOT-NEEDED (ไม่มีเอกสารเลขรัน/PDF · request_no = internal display id · NS-5)
- **Engine hooks:** ENG-DOA (F-DLG-001) · ENG-CSQ (F-CSQ-01 · EC) · ENG-NOTIFY (F-NOTIFY) — external, existing · ENG-WEL-01 welfare-eligibility-resolver [NEW·DRAFT] · ENG-WEL-02 welfare-balance-calculator [NEW·DRAFT] — register CUBIC ตอน hand-off (LD-04)
- **Open dependencies (blocking · [not documented] contract):**
  - Payroll/Expense pay-status hook contract (A-WEL-02 / OQ-03) — รอ FRD Phase B
  - atomic re-check เพดาน ณ อนุมัติ (concurrent · OQ-04) = optimistic-lock + backend atomic `[AI-DEFAULT]`
  - backend permission enforcement (OQ-05) `[AI-DEFAULT]`
  - DOA role ids จริง (OQ-DOA-01) · reversal ปลายทาง Payroll clawback contract (OQ-WEL-01 encode แล้ว รอยืนยันปลายทาง)

---
*trace: §1 ← FRD 00_OVERVIEW + BRD · §2 ← FRD 04_DB (+ 05_RULES §5.2 state machine) · §3 ← FRD 02_API/03_LOGIC · §4 ← FRD 05_RULES · §5 ← BRD §12.1 + DOA/NTF/CSQ briefs + 00_OVERVIEW §0.5/§0.8*
