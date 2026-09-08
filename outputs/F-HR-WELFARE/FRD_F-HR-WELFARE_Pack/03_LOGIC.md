# 03_LOGIC — F-HR-WELFARE · Welfare (สวัสดิการ)

> **Audience:** BE dev (business logic layer)
> **Scope:** non-HTTP logic — functions, state transitions, calculations, integrations.
> **Iron Rule R8:** ทุก mutation API → ≥1 Function/Engine ใน §3.3.
> Naming: Function = camelCase · Engine = kebab-case.

---

## §3.1 Functions (Scope-Local)

### F-HR-WELFARE-FN-01: `createBenefitType`
- **Purpose:** สร้างประเภทสวัสดิการเวอร์ชันแรก (version 1, active).
- **Input:** `{ name, cat, unit, quota, covers_dep, groups[], eff_from }`
- **Output:** `BenefitType | ValidationError[]`
- **Invoked by:** API-02 · **Calls:** FN-03
- **Side effects:** INSERT T_welfare_benefit_type (code=WEL-<from name>, version=1, status=active, claimable=unit≠percent) · audit(create)
- **Error cases:** BR_QUOTA_INVALID, BR_GROUPS_REQUIRED
- **Iron rule:** ✅ no HTTP terms

### F-HR-WELFARE-FN-02: `publishOrVersionBenefitType`
- **Purpose:** แก้ประเภท — draft→publish (in-place active) หรือ active→**ออกเวอร์ชันใหม่** (BR-03).
- **Input:** `{ id, patch{...}, eff_from }`
- **Output:** `BenefitType | ValidationError[]`
- **Invoked by:** API-04 · **Calls:** FN-03
- **Side effects:**
  - ถ้าเดิม `draft`: UPDATE in-place → status=active (เผยแพร่).
  - ถ้าเดิม `active`: UPDATE เก่า→archived + `eff_to=dayBefore(eff_from)` + claimable=false; INSERT version+1 (active, eff_to=null). ช่วง [eff_from,eff_to] ไม่ทับ.
  - audit(publish|version)
- **Error cases:** BR_EFFECTIVE_OVERLAP, ERR_STALE_DATA
- **Iron rule:** ✅

### F-HR-WELFARE-FN-03: `validateBenefitType`
- **Purpose:** validate ทะเบียน — quota>0 (unless percent) · groups≥1 · effective no-overlap ต่อ code (เฉพาะ active/version).
- **Input:** `{ form, mode(create|edit), existingVersions[] }` · **Output:** `{ ok, errors{} }`
- **Invoked by:** FN-01, FN-02 · **Calls:** — · **Side effects:** — (pure validate)
- **Error cases:** BR_QUOTA_INVALID (VR-01), BR_EFFECTIVE_OVERLAP (VR-02), BR_GROUPS_REQUIRED (VR-03)
- **Iron rule:** ✅

### F-HR-WELFARE-FN-04: `archiveBenefitType`
- **Purpose:** soft archive (status='archived') · คำนวณจำนวนคำขอค้างที่อ้าง (สำหรับ UI เตือน · FIX-06).
- **Input:** `{ id }` · **Output:** `{ ok, pending_ref_count }`
- **Invoked by:** API-05 · **Side effects:** UPDATE status · audit(archive). **No hard delete** (LK-5).
- **Iron rule:** ✅

### F-HR-WELFARE-FN-05: `addDependent`
- **Purpose:** เพิ่มผู้ติดตาม · block บุตร>20 (FN-06) · warn count≥3.
- **Input:** `{ employee_id, name, rel, dob, eligible }` · **Output:** `Dependent | ValidationError[] | Warning`
- **Invoked by:** API-06 · **Side effects:** INSERT T_welfare_dependent · audit
- **Error cases:** BR_DEPENDENT_CHILD_AGE (VR-06); Warning BR_DEPENDENT_COUNT (VR-07 · non-block)
- **Iron rule:** ✅

### F-HR-WELFARE-FN-06: `removeDependent`
- **Purpose:** ลบผู้ติดตาม (confirm modal). **Input:** `{ employee_id, dep_id }` · **Output:** `{ ok }`
- **Invoked by:** API-07 · **Side effects:** DELETE/soft T_welfare_dependent · audit · **Iron rule:** ✅

### F-HR-WELFARE-FN-07: `createRequest`
- **Purpose:** สร้างคำขอ (draft หรือ pending) · snapshot employee + config_version · gen request_no (internal seq).
- **Input:** `{ employee_id, use_for, benefit_type_id, amount?, value, use_date, reason?, files[], asDraft }`
- **Output:** `Request | ValidationError[]`
- **Invoked by:** API-09 · **Calls:** FN-08 (ถ้าไม่ draft)
- **Side effects:** INSERT T_welfare_request (+attachment) · snapshot (BR-10) · audit(create)
- **Iron rule:** ✅

### F-HR-WELFARE-FN-08: `validateRequest`
- **Purpose:** validate คำขอ — required fields + eligibility (BR-01) + remaining (BR-02) ก่อนส่ง.
- **Input:** `{ form, employee, benefit }` · **Output:** `{ ok, block? , errors{} }`
- **Invoked by:** API-09, FN-07 · **Calls:** FN-09 (eligibility), ENG-WEL-02 (remaining)
- **Error cases:** BR_NOT_ELIGIBLE (VR-05), BR_OVER_BALANCE (VR-04) · **Iron rule:** ✅

### F-HR-WELFARE-FN-09: `resolveEligibility`
- **Purpose:** wrapper อ่าน employment window (On/Offboard) + call ENG-WEL-01 ตัดสินสิทธิ์.
- **Input:** `{ employee, benefit, use_date }` · **Output:** `{ ok, reason }`
- **Invoked by:** FN-08, FN-11 (re-check) · **Calls:** ENG-WEL-01 · reads On/Offboard employment-window/resolve
- **Reasons:** พ้นสภาพ (leaver) · กลุ่มไม่มีสิทธิ์ · ก่อน/หลังช่วงมีผล (effFrom/effTo). **Iron rule:** ✅

### F-HR-WELFARE-FN-10: `submitRequestToDoa`
- **Purpose:** ส่งอนุมัติ — resolve DOA chain (ไม่ hardcode) · freeze snapshot คนที่เลือก · step1=current · status→pending_approval.
- **Input:** `{ request_id, picks{step:person} }` · **Output:** `Request(approvals[])`
- **Invoked by:** API-11 · **Calls:** ENG-DOA (GET /doa/resolve · external), ENG-NOTIFY
- **Side effects:** INSERT T_welfare_request_approval[] (append-only freeze) · UPDATE status · audit(submit) · NTF welfare_request_submitted
- **Error cases:** BR_DOA_SLOT_INCOMPLETE (VR-09) · **Iron rule:** ✅

### F-HR-WELFARE-FN-11: `approveRequestStep`
- **Purpose:** อนุมัติ — **one-step advance ต่อ 1 การกด** (FIX-03, no collapse); ขั้นสุดท้าย = re-check + finalize.
- **Input:** `{ request_id, actor }` · **Output:** `Request`
- **Invoked by:** API-12 · **Calls:** FN-19 (permission), FN-09/ENG-WEL-01 (re-check eligibility), ENG-WEL-02 (re-check remaining), ENG-CSQ, ENG-NOTIFY
- **Logic:**
  1. guard role (`canApprove` · FIX-04) + precondition status='pending_approval' (FIX-01).
  2. find `current` step. isLast = ไม่มี step > current.
  3. **isLast → FIX-02 re-check** eligibility + เพดาน (atomic · OQ-04) → fail = throw; ผ่าน → current=approved, status='approved', ตัดคงเหลือ (live), pay='pending', emit CSQ `welfare.granted` (EC), NTF welfare_request_result.
  4. **not last → advance:** current=approved, next=current, status คง pending_approval (ไม่ collapse).
- **Side effects:** UPDATE approval + request · audit("ตัดคงเหลือ + บันทึกมูลค่าเข้า 7C EC + ส่งสถานะจ่าย") · emit CSQ+NTF (finalize only)
- **Error cases:** ERR_INSUFFICIENT_ROLE, ERR_STALE_DATA, BR_NOT_ELIGIBLE_AT_APPROVAL, BR_OVER_BALANCE_AT_APPROVAL · **Iron rule:** ✅

### F-HR-WELFARE-FN-12: `rejectRequest`
- **Purpose:** ไม่อนุมัติ · reason บังคับ · ไม่ตัดคงเหลือ (BR-05).
- **Input:** `{ request_id, reason, actor }` · **Output:** `Request`
- **Invoked by:** API-13 · **Calls:** FN-19, ENG-NOTIFY
- **Side effects:** UPDATE status='rejected' + reject_reason + current step=rejected · audit · NTF
- **Error cases:** BR_REASON_REQUIRED (VR-08), ERR_INSUFFICIENT_ROLE · **Iron rule:** ✅

### F-HR-WELFARE-FN-13: `cancelRequest`
- **Purpose:** ยกเลิกก่อนอนุมัติ · guard status ∈ {draft, pending_approval} (FIX-05) · owner/admin (`canCancelReq`).
- **Input:** `{ request_id, actor }` · **Output:** `Request` · **Invoked by:** API-14 · **Calls:** FN-19
- **Side effects:** UPDATE status='cancelled' · **ไม่กระทบคงเหลือ** · audit
- **Error cases:** BR_CANCEL_NOT_ALLOWED (VR-10) · **Iron rule:** ✅

### F-HR-WELFARE-FN-14: `reverseRequest` ⭐ (OQ-WEL-01)
- **Purpose:** กลับรายการคำขอที่อนุมัติแล้วแบบ **append-only** — admin/manager · reason บังคับ · คืนสิทธิ์ + EC reverse + clawback flag.
- **Input:** `{ request_id, reason, actor }` · **Output:** `Request`
- **Invoked by:** API-15 · **Calls:** FN-19, ENG-WEL-02, ENG-CSQ (reverse), ENG-NOTIFY
- **Logic:**
  1. guard `canApprove` (admin/manager · FIX-04) + **precondition status='approved' เท่านั้น** (แยกจาก cancel · FIX-05).
  2. reason required (mirror reject).
  3. **append-only:** set status='reversed', reverse_reason, reversed_at — **คงข้อมูลเดิมทั้งหมด**.
  4. **คืนคงเหลืออัตโนมัติ:** ENG-WEL-02 นับเฉพาะ approved ⇒ reversed = ลดยอดใช้เอง (ไม่ปรับซ้ำ · BR-05/BR-11).
  5. **CSQ EC reverse:** emit negative offsetting entry (คืนมูลค่าเข้าเงินได้ 7C·EC).
  6. ถ้า `pay='sent'` → `payroll_clawback=true` (display-only flag · **ไม่มี pay action**).
  7. NTF welfare_request_reversed.
- **Side effects:** UPDATE request (append fields) · audit("กลับรายการ · คืนมูลค่าเข้าเงินได้ (7C·EC)"[+"แจ้ง Payroll ตั้งเบิกคืน"]) · emit CSQ EC-reverse + NTF
- **Error cases:** BR_REVERSE_NOT_ALLOWED, BR_REASON_REQUIRED, ERR_INSUFFICIENT_ROLE, ERR_STALE_DATA · **Iron rule:** ✅

### F-HR-WELFARE-FN-15: `computeBalance`
- **Purpose:** คงเหลือรายคนต่อ type ต่อปีสิทธิ์ (live · approved only).
- **Input:** `{ employee_id, benefit_year }` · **Output:** `[{ benefit_type, quota, used, remaining }]`
- **Invoked by:** API-16, FN-08, FN-11 · **Calls:** ENG-WEL-02
- **Side effects:** — (read/compute). leaver → remaining หยุด. **Iron rule:** ✅

### F-HR-WELFARE-FN-16: `computeExposure` (OQ-WEL-03)
- **Purpose:** pending demand อื่นบนสิทธิ์เดียวกัน (N ใบ · รวมมูลค่า) — **display-only, ไม่ soft-reserve**.
- **Input:** `{ employee_id, benefit_type_id, exclude_request_id }` · **Output:** `{ pending_count, pending_sum }`
- **Invoked by:** API-16 (balance tab) · **Calls:** — · **Side effects:** — · **Iron rule:** ✅

### F-HR-WELFARE-FN-17: `buildUsageReport`
- **Purpose:** usage report — filter (type/group/from/to) จริง + agg + stats (total, near_limit ≥80%).
- **Input:** `{ filters }` · **Output:** `{ rows[], agg{}, stats{} }`
- **Invoked by:** API-17 · **Calls:** ENG-WEL-02 (near-limit) · **Side effects:** — · **Iron rule:** ✅

### F-HR-WELFARE-FN-18: `applyEmploymentSignal`
- **Purpose:** ประมวลผล joiner/leaver signal (On/Offboard) — joiner→สิทธิ์เปิด · leaver→revoke คำขอค้าง + คงเหลือหยุด · **null last-day ≠ ไม่มีวันจบ** (BR-06).
- **Input:** `{ employee_id, signal, effective_date }` · **Output:** `{ affected_requests[] }`
- **Invoked by:** signal webhook/job (system) · **Calls:** ENG-NOTIFY
- **Side effects:** UPDATE คำขอค้าง→revoked (+revoke_reason) · audit · NTF welfare_eligibility_ended
- **Error cases:** — · **Iron rule:** ✅

### F-HR-WELFARE-FN-19: `checkPermission` (masking + guard · FN-94)
- **Purpose:** resolve สิทธิ์ role — `canApprove` (admin|manager) · `canSeeValue`/`canSeePerson` (admin|manager) · `canSeeDependent` (admin) · `canCancelReq` (admin|owner). enforce ที่ **backend** (OQ-05).
- **Input:** `{ role, resource, owner_id, actor_id }` · **Output:** `{ allowed, mask{} }`
- **Invoked by:** FN-11/12/13/14 + read masking · **Calls:** — · **Side effects:** — · **Iron rule:** ✅

---

## §3.2 Engines (Reusable / CUBIC)

### ENG-WEL-01: `welfare-eligibility-resolver` [NEW · DRAFT]
| Field | Value |
|---|---|
| code | welfare-eligibility-resolver |
| name | Welfare Eligibility Resolver |
| category | validation |
| status | DRAFT (register CUBIC ตอน hand-off) |
| owner | F-HR-WELFARE (planned reuse: HR features ที่มี eligibility) |

**Input:** `{ employee:{group, ended, last_day}, benefit:{groups[], eff_from, eff_to}, use_date }`
**Output:** `{ ok:bool, reason?:string }`
**Logic Outline:**
1. leaver: `employee.ended` → ok=false ("พ้นสภาพ") · **null last_day ≠ พ้นสภาพ** (BR-06).
2. group: `benefit.groups.includes(employee.group)` มิฉะนั้น false ("กลุ่ม X ไม่มีสิทธิ์").
3. window: use_date ต้องอยู่ [eff_from, eff_to] (false ถ้าก่อน/เกิน).
**Used by:** F-HR-WELFARE (this) · HR eligibility features (planned).
**Iron rule:** ✅ pure · reusable · rule-driven (BR-01/BR-06 configurable → Rule Management Phase 3, OQ-01).

### ENG-WEL-02: `welfare-balance-calculator` [NEW · DRAFT]
| Field | Value |
|---|---|
| code | welfare-balance-calculator |
| name | Welfare Balance Calculator |
| category | financial-calculation |
| status | DRAFT |
| owner | F-HR-WELFARE |

**Input:** `{ approved_requests[], benefit:{quota, unit}, employee_id, benefit_year }`
**Output:** `{ used, remaining }`
**Logic Outline:**
1. `used` = SUM(value|amount) ของ requests status='approved' ตรง employee+benefit(code)+ปีสิทธิ์ (percent → not counted, claimable=false).
2. `remaining` = quota − used. **ไม่ negative-clamp ใน logic** (ติดลบ = สัญญาณ over-approval ต้องเห็น; UI display อาจแสดง 0).
3. reversed/rejected/cancelled/revoked = ไม่นับ (คืนยอดเอง).
**Used by:** F-HR-WELFARE (balance tab · pre-check · FIX-02 re-check · report near-limit).
**Iron rule:** ✅ pure · substantial · reusable.

### External engines (EXISTING — feature ประกาศ/เรียกเท่านั้น)
- **ENG-DOA** (F-DLG-001) — GET /doa/resolve · slot picker · ไม่ hardcode chain (LK-1). Default 2-step หัวหน้าสายงาน→HR สวัสดิการ · no amount tier · no exec path (A-WEL-03/CL-0013).
- **ENG-CSQ** (F-CSQ-01) — event `welfare.granted` (ท่อ **EC เท่านั้น** · LK-6) + EC reverse (negative offset) on reversal. Welfare ไม่คำนวณมูลค่าเอง (basis=declared).
- **ENG-NOTIFY** (F-NOTIFY) — 5 business events (§02_API §2.X). DOA events อัตโนมัติ ไม่ประกาศซ้ำ.

---

## §3.3 API ↔ Logic Trace Table (R8 Anchor)

| API ID | Method | Path | Calls Functions | Calls Engines |
|---|---|---|---|---|
| API-01 | GET | /benefit-types | — (read) | — |
| API-02 | POST | /benefit-types | FN-01, FN-03 | — |
| API-03 | GET | /benefit-types/:id | — | — |
| API-04 | PUT | /benefit-types/:id | FN-02, FN-03 | — |
| API-05 | POST | /benefit-types/:id/archive | FN-04 | — |
| API-06 | POST | /dependents | FN-05 | — |
| API-07 | DELETE | /dependents/:id | FN-06 | — |
| API-08 | GET | /requests | — | — |
| API-09 | POST | /requests | FN-07, FN-08 | ENG-WEL-01, ENG-WEL-02 |
| API-10 | GET | /requests/:id | FN-15, FN-16 (context) | ENG-WEL-02 |
| API-11 | POST | /requests/:id/submit | FN-10 | ENG-DOA, ENG-NOTIFY |
| API-12 | POST | /requests/:id/approve | FN-11, FN-19, FN-09 | ENG-WEL-01, ENG-WEL-02, ENG-CSQ, ENG-NOTIFY |
| API-13 | POST | /requests/:id/reject | FN-12, FN-19 | ENG-NOTIFY |
| API-14 | POST | /requests/:id/cancel | FN-13, FN-19 | — |
| API-15 | POST | /requests/:id/reverse | FN-14, FN-19 | ENG-WEL-02, ENG-CSQ, ENG-NOTIFY |
| API-16 | GET | /balance | FN-15, FN-16 | ENG-WEL-02 |
| API-17 | GET | /report | FN-17 | ENG-WEL-02 |
| (job) | signal | leaver/joiner | FN-18 | ENG-NOTIFY |

### Trace Verification (Self-Check)
- [x] ทุก mutation API มี ≥1 Function/Engine.
- [x] ไม่มี orphan Function — FN-01..19 ทุกตัวถูก trace (FN-19 masking = ทุก mutation + read; FN-09 = FN-08/FN-11).
- [x] ไม่มี orphan Engine — ENG-WEL-01/02 traced; external DOA/CSQ/NOTIFY traced.
- [x] ไม่มี hidden logic ใน 02_API.

---

## §3.4 Dependencies
**External called:** `GET /doa/resolve` (ENG-DOA) · `GET /hr-config/resolve` (#107) · `GET /onboard/employment-window/resolve` (F127/128) · Payroll/Expense pay-status hook (A-WEL-02 [ASSUMED]).
**Into this feature:** — (feature เป็น producer ของ CSQ EC events; consumers = CSQ/Payroll/Expense/NOTIFY engines).

---

## §3.5 Open Questions / LD referenced
- **LD-04** (07_LOCKED): ENG-WEL-01/02 register CUBIC ตอน dev hand-off (ไม่ block sprint).
- **OQ-01** (00 §0.8): BR-01 eligibility → Rule Management Phase 3 (ENG-WEL-01 rule-driven).
- **OQ-04:** re-check เพดาน ณ อนุมัติ = **atomic ที่ backend** (`[AI-DEFAULT]` · optimistic lock + serializable) — FN-11.
- **OQ-05:** permission/masking enforce backend (FN-19) `[AI-DEFAULT]`.
