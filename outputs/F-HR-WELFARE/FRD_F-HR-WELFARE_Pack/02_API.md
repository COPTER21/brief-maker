# 02_API — F-HR-WELFARE · Welfare (สวัสดิการ)

> **Audience:** Backend developer (HTTP layer)
> **🚨 Iron Rule:** ห้าม business logic >5 lines ที่นี่ — ย้ายไป 03_LOGIC §3.1.
> **🚨 R8:** ทุก mutation API ต้องระบุ "Calls (Logic)" → trace ใน 03_LOGIC §3.3.
> Prefix path: `/api/v1/welfare`. All endpoints: `X-Tenant-Id` required · JWT auth. Mutations accept `Idempotency-Key` (PR-7) + `If-Match` version (PR-2 · OQ-04).

---

## §2.1 API Overview

| ID | Method | Path | Summary | Auth (role) |
|---|---|---|---|---|
| API-01 | GET | /benefit-types | list ประเภท | any |
| API-02 | POST | /benefit-types | สร้างประเภท | admin |
| API-03 | GET | /benefit-types/:id | detail + versions | any |
| API-04 | PUT | /benefit-types/:id | แก้ (publish draft / ออกเวอร์ชันใหม่) | admin |
| API-05 | POST | /benefit-types/:id/archive | ปิดใช้ (soft) | admin |
| API-06 | POST | /employees/:empId/dependents | เพิ่มผู้ติดตาม | admin |
| API-07 | DELETE | /employees/:empId/dependents/:depId | ลบผู้ติดตาม | admin |
| API-08 | GET | /requests | list คำขอ + filter | any (own scope) |
| API-09 | POST | /requests | สร้างคำขอ (draft/pending) | any (ผู้ยื่น) |
| API-10 | GET | /requests/:id | detail (4 tabs) | any (own/มีสิทธิ์) |
| API-11 | POST | /requests/:id/submit | ส่งอนุมัติ (DOA resolve+freeze) | ผู้ยื่น/admin |
| API-12 | POST | /requests/:id/approve | อนุมัติ (one-step advance / finalize) | admin/manager (ตาม DOA) |
| API-13 | POST | /requests/:id/reject | ไม่อนุมัติ | admin/manager |
| API-14 | POST | /requests/:id/cancel | ยกเลิก (draft/pending) | owner/admin |
| API-15 | POST | /requests/:id/reverse | **กลับรายการ** (approved) | admin/manager |
| API-16 | GET | /balance | คงเหลือรายคน + exposure + ผู้ติดตาม | admin/manager |
| API-17 | GET | /report | usage report + filter | admin/manager |

**Soft-ref reads (external — consumed, ไม่ owned):**
| — | GET | /employees (Employee Master combobox #102) | soft ref | any |
| — | GET | /hr-config/resolve?date&company_id | HR Config #107 (company_scope · ปีสิทธิ์) | any |
| — | GET | /onboard/employment-window/resolve?employee_id&include=signal | joiner/leaver | system |
| — | GET | /doa/resolve?feature=F-HR-WELFARE | DOA chain (slot pools) | ผู้ยื่น |
| — | (hook) | pay-status Payroll F065 / Expense F101 | display-only | any |

---

## §2.2 Per-API Contract (mutation + key reads)

### API-02: POST /benefit-types (สร้างประเภท)
- **roles:** admin · **Headers:** X-Tenant-Id, Idempotency-Key
- **Body:** `{ name, cat, unit(money|times|percent), quota(>0; null if percent), covers_dep, groups[](≥1), eff_from }`
- **Validation (≤5 lines):** name required · groups ≥1 · quota>0 unless percent · **complex (overlap/effective) → FN-03**
- **Response 201:** `{ id, code, version:1, status:'active', ... }`
- **Errors:** 400 ERR_VALIDATION_FAILED · 403 ERR_INSUFFICIENT_ROLE · 422 BR_QUOTA_INVALID (VR-01) · 422 BR_EFFECTIVE_OVERLAP (VR-02) · 422 BR_GROUPS_REQUIRED (VR-03)
- **Side effects:** INSERT T_welfare_benefit_type · INSERT T_welfare_audit_log
- **Calls (Logic):** FN-01 createBenefitType, FN-03 validateBenefitType

### API-04: PUT /benefit-types/:id (แก้)
- **roles:** admin · **Headers:** If-Match (version_lock)
- **Behavior:** ถ้าเวอร์ชัน `status='draft'` → publish (draft→active + update). ถ้า `status='active'` → **ออกเวอร์ชันใหม่**: เก่า→archived + `eff_to=dayBefore(new eff_from)` + insert version+1 (BR-03 no-overlap).
- **Errors:** 409 ERR_STALE_DATA · 422 BR_EFFECTIVE_OVERLAP · 403
- **Side effects:** UPDATE (archive old) + INSERT (new version) หรือ UPDATE (publish draft) · audit
- **Calls (Logic):** FN-02 publishOrVersionBenefitType, FN-03 validateBenefitType

### API-05: POST /benefit-types/:id/archive (ปิดใช้)
- **roles:** admin · **Behavior:** soft archive (status='archived'). **เตือน**จำนวนคำขอค้างที่อ้างอยู่ (FIX-06) ที่ UI ก่อน confirm.
- **Errors:** 403 · 404
- **Side effects:** UPDATE status · audit. **No hard delete** (LK-5). คำขอเก่ายังอ่านได้.
- **Calls (Logic):** FN-04 archiveBenefitType

### API-06: POST /employees/:empId/dependents (เพิ่มผู้ติดตาม)
- **roles:** admin · **Body:** `{ name, rel, dob, eligible }`
- **Errors:** 422 BR_DEPENDENT_CHILD_AGE (บุตร>20 · VR-06) · Warning ≥3 คน (VR-07 · non-block)
- **Side effects:** INSERT T_welfare_dependent · audit
- **Calls (Logic):** FN-05 addDependent

### API-09: POST /requests (สร้างคำขอ)
- **roles:** any (ผู้ยื่น) · **Headers:** Idempotency-Key
- **Body:** `{ employee_id, use_for_type(self|dependent), use_for_dep_id?, benefit_type_id, amount?, value(>0), use_date, reason?, files[] }`
- **Query behavior:** `?draft=true` → status='draft' (partial ok); else pre-check eligibility+remaining → status='submitted'→'pending_approval' (HTML unshift pending แล้วเปิด DOA modal).
- **Validation:** required fields · **eligibility (BR-01) + remaining (BR-02) → FN-08/FN-09/ENG-WEL-01/ENG-WEL-02**
- **Response 201:** `{ id, request_no:'REQ-2569-nnn', status }`
- **Errors:** 400 · 422 BR_NOT_ELIGIBLE (VR-05) · 422 BR_OVER_BALANCE (VR-04) · 409 ERR_DUPLICATE_IDEMPOTENCY_KEY
- **Side effects:** INSERT T_welfare_request (+attachment) · snapshot employee/config_version · audit
- **Calls (Logic):** FN-07 createRequest, FN-08 validateRequest, ENG-WEL-01 (eligibility), ENG-WEL-02 (balance)

### API-11: POST /requests/:id/submit (ส่งอนุมัติ DOA)
- **roles:** ผู้ยื่น/admin · **Body:** `{ picks: { step: person_key } }` (จาก slot picker — เลือกคนในแต่ละขั้น)
- **Precondition:** status ∈ {draft, submitted} · เลือกครบทุกขั้น (VR-09)
- **Behavior:** GET /doa/resolve → pools ต่อขั้น · freeze chain snapshot (person {name,position}) · step 1 = current · status → pending_approval.
- **Errors:** 422 BR_DOA_SLOT_INCOMPLETE · 403
- **Side effects:** INSERT T_welfare_request_approval[] (append-only freeze) · UPDATE status · audit · NTF welfare_request_submitted
- **Calls (Logic):** FN-10 submitRequestToDoa

### API-12: POST /requests/:id/approve (อนุมัติ · one-step advance / finalize)
- **roles:** admin/manager (ตาม DOA · `canApprove`) · **Headers:** If-Match (version_lock — OQ-04 concurrency)
- **Precondition:** **status='pending_approval' เท่านั้น** (FIX-01) · role guard (FIX-04)
- **Behavior (FIX-03 one-step advance):**
  - หา approval ขั้น `current`. ถ้า **ไม่ใช่ขั้นสุดท้าย** → mark current=approved, next.step=current, `status` คง pending_approval (advance 1 ขั้น · **ไม่ collapse ทั้งสาย**).
  - ถ้า **ขั้นสุดท้าย (finalize)** → **FIX-02 re-check** eligibility (ENG-WEL-01) + เพดาน/remaining (ENG-WEL-02) **ก่อน** commit; ผ่าน → status='approved' · ตัดคงเหลือ (live) · CSQ EC `welfare.granted` · pay='pending' (hook) · NTF welfare_request_result.
- **Errors:** 403 ERR_INSUFFICIENT_ROLE · 409 ERR_STALE_DATA · 422 BR_NOT_ELIGIBLE_AT_APPROVAL · 422 BR_OVER_BALANCE_AT_APPROVAL (FIX-02)
- **Side effects:** UPDATE approval step · UPDATE request (final: status/pay) · audit ("ตัดคงเหลือ + บันทึกมูลค่าเข้า 7C EC + ส่งสถานะจ่าย") · emit CSQ + NTF
- **Calls (Logic):** FN-11 approveRequestStep, ENG-WEL-01, ENG-WEL-02

### API-13: POST /requests/:id/reject
- **roles:** admin/manager · **Body:** `{ reason (required · VR-08) }` · **Precondition:** status='pending_approval'
- **Behavior:** status='rejected' · current step=rejected · **ไม่ตัดคงเหลือ** (BR-05) · NTF welfare_request_result.
- **Errors:** 422 BR_REASON_REQUIRED · 403
- **Calls (Logic):** FN-12 rejectRequest

### API-14: POST /requests/:id/cancel
- **roles:** owner หรือ admin (`canCancelReq`) · **Precondition:** status ∈ {draft, pending_approval} (VR-10 · FIX-05)
- **Behavior:** status='cancelled' · **ไม่กระทบคงเหลือ**. approved → ปุ่มไม่ปรากฏ (ต้องใช้ reverse).
- **Errors:** 422 BR_CANCEL_NOT_ALLOWED · 403
- **Calls (Logic):** FN-13 cancelRequest

### API-15: POST /requests/:id/reverse (กลับรายการ · OQ-WEL-01)
- **roles:** admin/manager (`canApprove` · admin-only intent · VR-11) · **Body:** `{ reason (required · VR-08) }` · **Headers:** If-Match
- **Precondition:** **status='approved' เท่านั้น** (แยกจาก cancel — FIX-05)
- **Behavior (append-only):** status='reversed' · set reverse_reason + reversed_at · **คืนคงเหลืออัตโนมัติ** (usedByPerson นับเฉพาะ approved → reversed = ลดยอดใช้เอง ไม่ปรับซ้ำ · BR-05/BR-11) · **CSQ EC reverse** (negative offsetting entry คืนมูลค่าเข้าเงินได้ 7C·EC) · ถ้า pay='sent' → `payroll_clawback=true` (display-only flag แจ้ง Payroll ตั้งเบิกคืน · **ไม่มี pay action**) · NTF welfare_request_reversed.
- **Errors:** 422 BR_REVERSE_NOT_ALLOWED (ไม่ใช่ approved) · 422 BR_REASON_REQUIRED · 403 · 409 ERR_STALE_DATA
- **Side effects:** UPDATE request (append fields) · audit ("กลับรายการ · คืนมูลค่าเข้าเงินได้ (7C·EC)" [+ "แจ้ง Payroll ตั้งเบิกคืน"]) · emit CSQ EC-reverse + NTF. **ข้อมูลเดิมคงอยู่** (ไม่ลบ/ไม่แก้).
- **Calls (Logic):** FN-14 reverseRequest, ENG-WEL-02

### API-16: GET /balance?employee_id=
- **roles:** admin/manager (masking ต่าง role · FN-94) · **Response:** `{ employee(snapshot), benefit_lines:[{ benefit_type, quota, used, remaining }], exposure:[{ benefit_type, pending_count, pending_sum }], dependents:[], employment:{ joiner?, leaver? } }`
- **Note:** used/remaining = live compute (ENG-WEL-02, approved only). exposure = display-only (OQ-WEL-03). leaver → remaining หยุด.
- **Calls (Logic):** FN-15 computeBalance, FN-16 computeExposure

### API-17: GET /report?type=&group=&from=&to=
- **roles:** admin/manager · **Response:** `{ rows:[...], agg:{...}, stats:{ total, near_limit_count } }` · filter จริง + empty state.
- **Calls (Logic):** FN-17 buildUsageReport

### API-01 / API-03 / API-08 / API-10 (reads)
- GET list/detail — trivial reads (RLS + role scope). API-08 supports `?status=` filter. API-10 returns 4-tab payload (detail + attachments + balance-context + history + approvals + exposure). masking ตาม role.
- **Calls (Logic):** API-08/API-16-context → FN-15/FN-16; อื่น = read (—).

---

## §2.3 Common Concerns
- **Idempotency (PR-7):** mutation รับ `Idempotency-Key` — cache 24h · same key+body → cached · diff body → 409.
- **Optimistic Locking (PR-2 · OQ-04):** approve/reverse/edit ใช้ `If-Match` (version_lock). mismatch → 409 ERR_STALE_DATA. **re-check เพดาน ณ อนุมัติ = atomic ที่ backend** (`[AI-DEFAULT]` — OQ-04).
- **Multi-Tenant:** X-Tenant-Id → RLS. company_scope จาก HR Config resolve.
- **Backend permission enforcement (OQ-05):** guard ทุก mutation + masking read ที่ **backend** ไม่ใช่แค่ UI (`[AI-DEFAULT]`).
- **Audit:** mutation → T_welfare_audit_log (append-only · diff).
- **No hardcode:** DOA chain (GET /doa/resolve) · masking level (Policy Center) · เลขเอกสาร (ไม่มี · NS-5).

---

## §2.4 API → Logic Trace (Anchor for R8)
> Authoritative: 03_LOGIC §3.3.

| API | Calls Functions | Calls Engines |
|---|---|---|
| API-02 POST /benefit-types | FN-01, FN-03 | — |
| API-04 PUT /benefit-types/:id | FN-02, FN-03 | — |
| API-05 archive | FN-04 | — |
| API-06 POST dependents | FN-05 | — |
| API-07 DELETE dependents | FN-06 | — |
| API-09 POST /requests | FN-07, FN-08 | ENG-WEL-01, ENG-WEL-02 |
| API-11 submit | FN-10 | ENG-DOA (external) |
| API-12 approve | FN-11 | ENG-WEL-01, ENG-WEL-02, ENG-CSQ, ENG-NOTIFY (external) |
| API-13 reject | FN-12 | ENG-NOTIFY |
| API-14 cancel | FN-13 | — |
| API-15 reverse | FN-14 | ENG-WEL-02, ENG-CSQ, ENG-NOTIFY |
| API-16 GET /balance | FN-15, FN-16 | ENG-WEL-02 |
| API-17 GET /report | FN-17 | — |
| (signal) leaver/joiner | FN-18 | — |

> **R8 Check:** ทุก mutation row มี ≥1 Function/Engine ✅

---

## §2.X Cross-Module Contract ⭐ (จาก BRD §12.1 Downstream Impact)

| Downstream | รูปแบบ | Contract | Trigger | Payload หลัก | Compensating |
|---|---|---|---|---|---|
| **CSQ (7C·EC)** | Event | `welfare.granted` (ท่อ **EC เท่านั้น** · LK-6) | approve (finalize) | `{ ref:request_no, employee_id, benefit_type, value_declared, currency:THB, basis:declared }` | **EC reverse** (negative offset) on `reverse` |
| **CSQ reverse** | Event | `welfare.granted` reverse entry (EC negative offsetting) | reverse | `{ ref:request_no, value_declared:-x, reason }` | — |
| **Payroll (F065)** | hook + flag | สถานะจ่าย display-only (อ่าน); `payroll_clawback` flag on reverse (pay=sent) | approve (pay=pending) / reverse | `{ request_no, employee_id, value, clawback:bool }` | clawback = ตั้งเบิกคืนที่ปลายทาง (Welfare ไม่จ่ายเอง) |
| **Expense (F101)** | read | สิทธิ์สวัสดิการกำกับวงเงินเบิก (revalidate) | approve | `{ employee_id, benefit_type, remaining }` | — |
| **Notification (F-NOTIFY)** | Event (ENG-NOTIFY.emit) | 4 business + `welfare_request_reversed` | state transition | `{ event_id, ref, vars }` | — |

- **NTF events (5):** welfare_request_submitted · welfare_request_result · welfare_quota_near_limit (≥80%) · welfare_eligibility_ended (leaver) · **welfare_request_reversed** (OQ-WEL-01 · append step 7).
- DOA events (doa_pending/doa_result) = จาก DOA engine อัตโนมัติ **ห้ามประกาศซ้ำ**.
- ทุกแถวมี cross-module test → 06_TESTS §6.9 (XT-01..XT-05).
