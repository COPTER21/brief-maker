# 02_API — F-HR-SALSTRUCT · Salary Structure (โครงเงินเดือน)

> **Audience:** BE dev (HTTP layer)
> **หลัก:** ชั้นนี้บาง — validate/serialize/authorize เท่านั้น · **business logic ทั้งหมดอยู่ที่ `03_LOGIC`** (R8) · **ไม่มี DELETE endpoint ทั้งแพ็ก** (P-4′) · **ไม่มี endpoint อนุมัติ** (BR-21)
> Base path: `/api/v1/salary-structure`

## §2.1 API Overview

| ID | Method | Path | ทำอะไร | Mutation | FN |
|---|---|---|---|:---:|---|
| API-01 | GET | `/grades` | รายการระดับ + กระบอก ณ วันที่ (as-of) | — | FN-01, FN-03, FN-10, FN-90 |
| API-02 | POST | `/grades` | สร้างระดับ + ร่างเวอร์ชันกระบอก | ✅ | FN-01, FN-04 |
| API-03 | PATCH | `/grades/{gradeId}/versions/{versionId}` | แก้ร่าง (**เฉพาะ `draft`**) | ✅ | FN-06 |
| API-04 | POST | `/grades/{gradeId}/versions/{versionId}/publish` | ประกาศ + ตั้งวันมีผล | ✅ | FN-02, FN-07, FN-29, FN-56 |
| API-05 | POST | `/grades/{gradeId}/versions/{versionId}/withdraw` | ถอนเวอร์ชันที่รอมีผล | ✅ | FN-08 |
| API-06 | POST | `/grades/{gradeId}/deactivate` | ปิดใช้ระดับ (soft archive) | ✅ | FN-09 |
| API-07 | POST | `/grades/{gradeId}/reactivate` | เปิดใช้กลับ = สร้างเวอร์ชันใหม่ | ✅ | FN-11 |
| API-08 | GET | `/grades/{gradeId}/versions` | ประวัติเวอร์ชัน | — | FN-12 |
| API-09 | GET | `/grades/diff` | ตารางเทียบ 2 เวอร์ชัน | — | FN-04 |
| API-10 | GET | `/components` | ทะเบียนองค์ประกอบ | — | FN-13, FN-40, FN-90 |
| API-11 | POST | `/components` | สร้าง/สร้างเวอร์ชันใหม่ขององค์ประกอบ | ✅ | FN-13…FN-16, FN-57 |
| API-12 | POST | `/components/{componentId}/deactivate` | ปิดใช้องค์ประกอบ | ✅ | FN-17 |
| API-13 | GET | `/rates` | รายการอัตราพนักงาน ณ วันที่ (**masked**) | — | FN-18…FN-25, FN-34, FN-35, FN-90 |
| API-14 | POST | `/rates` | ผูก/บันทึกอัตราใหม่ | ✅ | FN-19, FN-22, FN-23, FN-26, FN-29, FN-56, FN-58 |
| API-15 | POST | `/rates/{recordId}/withdraw` | ถอนอัตราที่รอมีผล | ✅ | FN-27 |
| API-16 | POST | `/rates/{recordId}/end` | ปิดช่วงอัตราเมื่อพ้นสภาพ | ✅ | FN-28 |
| API-17 | GET | `/rates/{employeeId}/history` | ประวัติอัตราของพนักงาน | — | FN-26, FN-42 |
| API-18 | GET | `/recurring` | รายการเงินได้/เงินหักประจำ | — | FN-30…FN-32, FN-90 |
| API-19 | POST | `/recurring` | เพิ่มรายการประจำ | ✅ | FN-30, FN-31, FN-33 |
| API-20 | POST | `/recurring/{itemId}/withdraw` | ถอนรายการประจำ | ✅ | FN-91 |
| API-21 | GET | `/usage` | ทะเบียนการใช้งาน + ค่าที่อ่านจาก HR Config | — | FN-38, FN-44, FN-45, FN-46 |
| API-22 | PATCH | `/usage/{consumerCode}` | ปรับสถานะ Module Linkage เอง | ✅ | FN-46 |
| API-23 | POST | `/usage/refresh-config` | ล้างค่าที่ดึงไว้ + ถามใหม่ | ✅ | FN-41 |
| **API-24** | GET | `/resolve` | **สัญญาการอ่านอัตราของ consumer** (§0.13.2) | — | FN-20, FN-44, FN-45 |
| **API-25** | GET | `/bands/resolve` | **สัญญาการอ่านกระบอกของ Manpower** (§0.13.3) | — | FN-45 |
| **API-26** | POST | `/rates/from-movement` | **ทางเข้าเดียวของ Employee Movement** (§0.13.5) | ✅ | FN-43 |
| API-27 | POST | `/usage` | consumer ลงทะเบียน where-used ของตัวเอง (SS-7) | ✅ | FN-46 |

> **ไม่มี:** `DELETE` ใด ๆ · `/approve` · `/submit-for-approval` · `/tax-calc` · `/mass-revision` · `/import` · `/export-all` — ความไม่มีนี้เป็นข้อกำหนด (FN-47…FN-49 · FN-53 · FN-54 · FN-91)

## §2.2 Per-API Contract

### F-HR-SALSTRUCT-API-01 · `GET /grades`
- **Auth:** ทุก role ที่เข้าถึง feature · **Query:** `date` (default วันนี้) · `company_id` · `q` · `status` · `page` · `page_size`
- **Response 200:** `{ items: [{ grade_id, grade_code, grade_name, level_order, job_family, company_scope, companies[], band: { min, mid, max, currency, effective_date, effective_to, version_id } | null, version_status, headcount, status }], total }`
- **Logic:** `resolveBandAt` · `buildListQuery` · `filterActiveOptions`
- **Errors:** `400 ERR_INVALID_DATE`
- **DB:** อ่าน `T_ss_grade` · `T_ss_band_version`

### F-HR-SALSTRUCT-API-02 · `POST /grades`
- **Auth:** HR Comp Admin · **Header:** `Idempotency-Key`
- **Body:** `{ grade_code, grade_name, level_order, job_family?, company_scope, companies[]?, band: { min_amount, mid_amount, max_amount }, effective_date?, change_reason?, copy_from_version_id?, percent_adjust? }`
- **Response 201:** `{ grade_id, version_id, version_status: "draft" }`
- **Logic:** `createBandDraft` → `assertBandOrder` · `applyPercentAdjust` (เมื่อมี `copy_from_version_id`)
- **Errors:** `409 ERR_GRADE_CODE_DUPLICATE` · `422 ERR_BAND_ORDER_INVALID` (พร้อม `rows[]` ที่ผิด) · `409 ERR_IDEMPOTENCY_MISMATCH`
- **DB:** เขียน `T_ss_grade` · `T_ss_band_version` (`draft`)

### F-HR-SALSTRUCT-API-03 · `PATCH /grades/{gradeId}/versions/{versionId}`
- **Auth:** HR Comp Admin · **Body:** field ของกระบอก/ข้อมูลระดับ
- **Response 200:** เวอร์ชันที่แก้แล้ว
- **Logic:** `assertVersionEditable` (รับเฉพาะ `draft`) → `assertBandOrder`
- **Errors:** **`409 ERR_VERSION_NOT_EDITABLE`** (เมื่อสถานะ ≠ `draft` — บังคับ P-2′) · `422 ERR_BAND_ORDER_INVALID`

### F-HR-SALSTRUCT-API-04 · `POST /grades/{gradeId}/versions/{versionId}/publish`
- **Auth:** HR Comp Admin · **Body:** `{ effective_date, change_reason, below_legal_min_reason? }`
- **Response 200:** `{ version_id, version_status: "scheduled", effective_date, effective_to, warnings: [{ code, message, legal_min_version_id? }] }`
- **Logic:** `publishBandVersion` → `assertNoOverlap` · `assertNotInClosedPeriod` · `resolveLegalMinimum` · `evaluateBelowLegalMin` · `computeEffectiveWindow` · `emitCsq('salstruct.published')`
- **Errors:** `422 ERR_EFFECTIVE_OVERLAP` (`conflicting_version_id`) · `422 ERR_EFFECTIVE_IN_CLOSED_PERIOD` (`period_code`, `earliest_open_date`) · `422 ERR_REASON_REQUIRED` · `422 ERR_LEGAL_MIN_REASON_REQUIRED` · `503 ERR_HRCFG_UNAVAILABLE`
- **Side effects:** เขียน `T_ss_cfg_ref` (period + legal_min) · ยิง CSQ E1

### F-HR-SALSTRUCT-API-05 · `POST /grades/{gradeId}/versions/{versionId}/withdraw`
- **Body:** `{ cancel_reason }` (≥10) · **Logic:** `withdrawBandVersion` → `emitCsq('salstruct.cancelled')`
- **Errors:** `409 ERR_VERSION_NOT_WITHDRAWABLE` (ไม่ใช่ `scheduled` หรือถึงวันมีผลแล้ว) · `422 ERR_REASON_REQUIRED`

### F-HR-SALSTRUCT-API-06 · `POST /grades/{gradeId}/deactivate`
- **Auth:** HR Comp Admin หรือ HR Manager · **Body:** `{ deactivate_reason, acknowledged_where_used_count }`
- **Logic:** `countWhereUsed` → `deactivateGrade` → `emitCsq('salstruct.deactivated')`
- **Errors:** `409 ERR_WHERE_USED_NOT_ACKNOWLEDGED` (client ยังไม่ยืนยันจำนวนผู้ใช้) · `422 ERR_REASON_REQUIRED`
- **หมายเหตุ:** ไม่ลบแถว — ตั้ง `status='inactive'` เท่านั้น (FN-91)

### F-HR-SALSTRUCT-API-07 · `POST /grades/{gradeId}/reactivate`
- **Body:** `{ effective_date, change_reason }` · **Logic:** `reactivateGrade` (สร้าง **เวอร์ชันใหม่** `scheduled` — ไม่ย้อนสถานะ · P-2′)

### F-HR-SALSTRUCT-API-08 · `GET /grades/{gradeId}/versions` → ประวัติทุกเวอร์ชัน + ผู้แก้ + เหตุผล (`listVersionHistory`) · read-only

### F-HR-SALSTRUCT-API-09 · `GET /grades/diff?from={versionId}&to={versionId}`
- **Response:** `{ rows: [{ grade_code, field, old, new, delta, delta_pct }] }` · **Logic:** `buildVersionDiff` · ระดับที่ไม่เปลี่ยนคืน `delta: 0` (ไม่ซ่อน)

### F-HR-SALSTRUCT-API-10 · `GET /components` → ทะเบียนองค์ประกอบ (`status` filter · ค่า `inactive` แสดงได้แต่ `selectable: false` — C-5 · BR-18)

### F-HR-SALSTRUCT-API-11 · `POST /components`
- **Body:** `{ component_code, component_name, direction, calc_type, base_component_code?, frequency, include_in_band_base, payroll_code, is_ot_base?, is_ssf_base?, prorate_by_payment_days, effective_date }`
- **Logic:** `createPayComponent` → `detectComponentCycle`
- **Errors:** `409 ERR_COMPONENT_CODE_DUPLICATE` · **`422 ERR_COMPONENT_CYCLE`** (`cycle_path: ["X-PCT","Y-PCT","X-PCT"]`) · `422 ERR_PAYROLL_CODE_REQUIRED`
- **ห้ามรับ field:** สูตรภาษี/ปกส./ยอดสุทธิ/โบนัส — payload ที่มี key เหล่านี้ → `400 ERR_FIELD_NOT_SUPPORTED` (FN-49 · FN-59)

### F-HR-SALSTRUCT-API-12 · `POST /components/{componentId}/deactivate` → `deactivateComponent` + `countWhereUsed` → CSQ E4 · errors เหมือน API-06

### F-HR-SALSTRUCT-API-13 · `GET /rates` — **RESTRICTED**
- **Query:** `date` · `company_id` · `q` · `department_id` · `grade_code` · `status` · `out_of_range` · `unassigned` · `page`
- **Response 200:** `{ items: [{ record_id, employee_id, employee_name_snapshot, department_snapshot, grade_code, base_amount | null, masked, fte, band_position: {...} | null, effective_date, record_status }], total, unassigned_count, masked_policy: { role, reason } }`
- **Logic:** `buildListQuery` · `resolveCurrentRate` · ENG-SALBAND-01 · **`maskMoney` (ชั้น API — UI ไม่เคยได้ตัวเลขจริงถ้าไม่มีสิทธิ์ · OQ-FRD-04)** · `computeUnassignedCount`
- **Side effect:** เมื่อเรียกแบบ `detail=true` (เปิด drawer) → `logRestrictedView` + CSQ E10
- **Errors:** `403 ERR_FORBIDDEN` (ไม่มีสิทธิ์เข้าถึง feature เลย)

### F-HR-SALSTRUCT-API-14 · `POST /rates`
- **Auth:** HR Comp Admin · **Header:** `Idempotency-Key`
- **Body:** `{ employee_id, grade_code, base_amount, fte, effective_date, change_reason_code, change_reason, movement_doc_no?, out_of_range_reason?, below_legal_min_reason? }`
- **Response 201:** `{ record_id, record_status, effective_date, effective_to, superseded_record_id?, band_position, warnings[] }`
- **Logic:** `assertCompRecordComplete` → `assertChangeReasonCode` → `assertNotInClosedPeriod` → `assertNoOverlap` → `evaluateOutOfRange` → `resolveLegalMinimum` + `evaluateBelowLegalMin` → `closePreviousCompRecord` → `createCompRecord` → `emitCsq('salcomp.assigned')`
- **Errors:** `422 ERR_EFFECTIVE_IN_CLOSED_PERIOD` (`period_code`, `earliest_open_date`) · `422 ERR_OUT_OF_RANGE_REASON_REQUIRED` (`direction`, `min`, `max`) · `422 ERR_LEGAL_MIN_REASON_REQUIRED` · `422 ERR_CHANGE_REASON_CODE_REQUIRED` · `422 ERR_GRADE_INACTIVE` · `409 ERR_RATE_OVERLAP` · **`409 ERR_STALE_VERSION`** (optimistic lock · EC-16) · `503 ERR_HRCFG_UNAVAILABLE`

### F-HR-SALSTRUCT-API-15 · `POST /rates/{recordId}/withdraw`
- **Body:** `{ cancel_reason }` · **Logic:** `withdrawCompRecord` → CSQ E6 · **ไม่ใช่ reversal ของ E5** (E5 ยังไม่เคยยิง)
- **Errors:** `409 ERR_RECORD_NOT_WITHDRAWABLE` (ไม่ใช่ `scheduled`)

### F-HR-SALSTRUCT-API-16 · `POST /rates/{recordId}/end`
- **Body:** `{ effective_to, end_reason }` · **Logic:** `endCompRecord` → CSQ E7 (EC — ภาระค่าจ้างหยุด)
- **Errors:** `409 ERR_RECORD_NOT_CURRENT` · `422 ERR_END_DATE_BEFORE_EFFECTIVE`

### F-HR-SALSTRUCT-API-17 · `GET /rates/{employeeId}/history`
- **Response:** ทุกช่วงเรียงเวลา + ผู้บันทึก + เหตุผล + `movement_doc_no` (จำนวนเงิน masked ตามสิทธิ์) · **Logic:** `listRateHistory` · `renderPersonSnapshot` (ทำงานได้แม้ต้นทางปิดสถานะ — EC-13) · **Side effect:** `logRestrictedView`

### F-HR-SALSTRUCT-API-18 · `GET /recurring` → รายการประจำ (masked) · filter: `employee_id` · `component_code` · `direction` · `item_status` · ช่วงวัน

### F-HR-SALSTRUCT-API-19 · `POST /recurring`
- **Body:** `{ employee_id, component_code, amount? | percent?, effective_from, effective_to?, goal_amount? }`
- **Logic:** `assertNoOverlap` (พนักงาน × component) → `assertNotInClosedPeriod` → `createRecurringItem` → CSQ E8
- **Errors:** `409 ERR_RECURRING_OVERLAP` (`conflicting_item_id`, `range`) · `422 ERR_AMOUNT_OR_PERCENT_REQUIRED` · `422 ERR_GOAL_ONLY_FOR_DEDUCTION` · `422 ERR_COMPONENT_INACTIVE`

### F-HR-SALSTRUCT-API-20 · `POST /recurring/{itemId}/withdraw` → `{ cancel_reason }` · `withdrawRecurringItem` → CSQ E9 (`end_trigger: withdrawn`)

### F-HR-SALSTRUCT-API-21 · `GET /usage`
- **Response:** `{ config_refs: [{ config_group, asked_date, company_id, version_id | null, fetched_at, manage_url }], pay_periods: [{ period_code, range, period_status }], pending_from_movement: [...], consumers: [{ consumer_code, consumer_name, reads_what, link_status, manual_override, last_read_at }], audit_tail: [...] }`
- **Logic:** `listConfigRefs` · `listConsumers` — **ไม่มี field ให้แก้ค่าของ HR Configuration** (C-4)

### F-HR-SALSTRUCT-API-22 · `PATCH /usage/{consumerCode}` → `{ link_status, manual_override: true }` · `setLinkStatus` (D15 admin action → audit)

### F-HR-SALSTRUCT-API-23 · `POST /usage/refresh-config`
- **Body:** `{ groups?: ["period_rule","ot_rate","legal_minimum"], reason?: "period_closed_event" }`
- **Logic:** `invalidateConfigCache` → `resolveHrConfig` ใหม่ทุก group → เขียน `T_ss_cfg_ref`
- **Response:** `{ refreshed: [{ config_group, version_id | null, fetched_at }] }` · เรียกได้ทั้งจากปุ่มบนจอ (FN-41) และจาก event handler ของ `hrconfig.period_closed` / `hrconfig.effective`

### F-HR-SALSTRUCT-API-24 · `GET /resolve` ⭐ **สัญญาการอ่านของ consumer**
- **Auth:** service token ของ consumer (สิทธิ์ผ่าน Policy Center) หรือผู้ใช้ที่มีสิทธิ์
- **Query:** `date` (**บังคับ**) · `company_id` · `employee_id` · `scope=employee|company` · `include` · `page` · `page_size`
- **Response 200:** rate snapshot ตาม **`00_OVERVIEW §0.13.2`** (มี `version_id` เสมอ · `masked` เมื่อไม่มีสิทธิ์ · `rate: null` + `reason: "NO_RATE_AT_DATE"` เมื่อไม่มีข้อมูล)
- **Logic:** `buildRateSnapshot` → `resolveCurrentRate` · `resolveBandAt` · ENG-SALBAND-01 · `maskMoney`
- **Errors:** **`400 ERR_RESOLVE_DATE_REQUIRED`** (ไม่ส่ง `date` — บังคับ P-5′) · `400 ERR_SCOPE_REQUIRES_COMPANY` · `403 ERR_FORBIDDEN`
- **Side effect:** อัปเดต `T_ss_consumer_usage.last_read_at`

### F-HR-SALSTRUCT-API-25 · `GET /bands/resolve` ⭐
- **Query:** `date` (บังคับ) · `company_id` · `grade_code?`
- **Response:** ตาม **§0.13.3** — ต่อระดับ: min/mid/max + `version_id` + `headcount` (ไม่ระบุตัวบุคคล → **ไม่ต้องมีสิทธิ์ RESTRICTED**)
- **Logic:** `buildBandSnapshot` · `resolveBandAt`

### F-HR-SALSTRUCT-API-26 · `POST /rates/from-movement` ⭐ **ทางเข้าเดียวของ Employee Movement**
- **Auth:** service token ของ `F-HR-MOVEMENT` เท่านั้น · **Header:** `Idempotency-Key: <movement_doc_no>` (บังคับ)
- **Body:** `{ employee_id, grade_code, base_amount, fte, effective_date, change_reason_code, change_reason, movement_doc_no, approved_by }`
- **Response 201:** `{ record_id, record_status: "scheduled" }` — **สร้างสถานะ `รอมีผล` เท่านั้น · ไม่มีการอนุมัติซ้ำ** (BR-21)
- **Logic:** `assertIdempotent` → `ingestMovementRate` → เส้นทางเดียวกับ API-14
- **Errors:** `422 ERR_EFFECTIVE_IN_CLOSED_PERIOD` (**ไม่สร้างเรคคอร์ดค้าง** · EC-29) · `409 ERR_IDEMPOTENCY_MISMATCH` · `200/201` ซ้ำด้วยผลเดิมเมื่อส่ง `movement_doc_no` เดิม (EC-30)

### F-HR-SALSTRUCT-API-27 · `POST /usage` (SS-7)
- **Body:** `{ consumer_code, consumer_name, reads_what }` · **Logic:** `registerWhereUsed` → เขียน `T_ss_consumer_usage` + เรียก `POST /hr-config/items/:id/usage` ต่อ (C-6)

## §2.3 Common Concerns

### Idempotency (PR-7)
ทุก `POST` ที่สร้างข้อมูลรับ `Idempotency-Key` (บังคับสำหรับ API-26) → เก็บใน `T_ss_idempotency` · key เดิม + payload เดิม = คืนผลเดิม · key เดิม + payload ต่าง = `409 ERR_IDEMPOTENCY_MISMATCH`

### Optimistic Locking (PR-1 / EC-16)
`POST /rates` รับ `If-Match: <etag ของอัตราปัจจุบันของพนักงานคนนั้น>` — ไม่ตรง → **`409 ERR_STALE_VERSION`** พร้อมข้อความให้โหลดใหม่ · `[AI-DEFAULT]` OQ-BRD-03

### Multi-Tenant
ทุก request ผูก `tenant_id` จาก token · ทุก query กรองด้วย `tenant_id` (D17) · `company_id` ใช้ตัดสินขอบเขตกระบอก ไม่ใช่ isolation

### Masking (D7 · BR-16)
`maskMoney` ทำงานที่ **ชั้น API ก่อน serialize** — ค่า Restricted ที่ผู้เรียกไม่มีสิทธิ์คืนเป็น `null` + `masked: true` (ไม่ใช่สตริงอำพราง เพื่อไม่ให้เดาจากความยาว) · ครอบ **ทุก** endpoint รวม `/resolve` และการ export

### Audit Log (D9)
ทุก mutation → `emitAuditEvent` (ใคร · อะไร · เมื่อไร · ที่ไหน · ผล) · ทุกการอ่าน **detail ของข้อมูล Restricted** → `logRestrictedView` + CSQ E10 · ปลายทางคือ Policy Center (ไม่เก็บ audit เอง)

### Config resolve (C-1…C-3)
ทุกจุดที่ต้องใช้ค่านโยบายเรียก `resolveHrConfig(date, companyId, group)` — **ส่ง `date` เสมอ** · เก็บ `version_id` ลง `T_ss_cfg_ref` + คอลัมน์ `*_version_id` ของเรคคอร์ด · cache ภายในวันเดียว · ล้างเมื่อได้ event
ถ้าเรียกไม่ได้ → **`503 ERR_HRCFG_UNAVAILABLE`** และ **ห้ามใช้ค่าที่จำไว้ข้ามวัน** (OQ-FRD-06 · EC-19)

### Error envelope
```json
{ "error": { "code": "ERR_EFFECTIVE_IN_CLOSED_PERIOD",
             "message": "งวด 2026-07 ปิดแล้ว ตั้งวันมีผลย้อนเข้างวดนี้ไม่ได้ · ตั้งได้ตั้งแต่ 01/08/2569",
             "details": { "period_code": "2026-07", "earliest_open_date": "2026-08-01" } } }
```
> ข้อความ `message` ต้องตรงกับข้อความบนจอ (`01_UI §1.6`) — QA ตรวจ verbatim

## §2.4 API → Logic Trace (Anchor for R8)

| API | Function / Engine ที่เรียก |
|---|---|
| API-01 | `buildListQuery` · `resolveBandAt` · `filterActiveOptions` |
| API-02 | `createBandDraft` · `assertBandOrder` · `applyPercentAdjust` |
| API-03 | `assertVersionEditable` · `assertBandOrder` |
| API-04 | `publishBandVersion` · `assertNoOverlap` · `assertNotInClosedPeriod` · `resolveLegalMinimum` · `evaluateBelowLegalMin` · `computeEffectiveWindow` · **ENG-EFFDATE-01** · **ENG-CSQ-01** |
| API-05 | `withdrawBandVersion` · **ENG-CSQ-01** |
| API-06 | `countWhereUsed` · `deactivateGrade` · **ENG-CSQ-01** |
| API-07 | `reactivateGrade` · `computeEffectiveWindow` |
| API-08 | `listVersionHistory` |
| API-09 | `buildVersionDiff` |
| API-10 | `buildListQuery` · `filterActiveOptions` |
| API-11 | `createPayComponent` · `detectComponentCycle` |
| API-12 | `deactivateComponent` · `countWhereUsed` · **ENG-CSQ-01** |
| API-13 | `buildListQuery` · `resolveCurrentRate` · `computeBandBase` · **ENG-SALBAND-01** · `maskMoney` (**ENG-MASK-01**) · `computeUnassignedCount` · `computeTotalFixedMonthly` · `logRestrictedView` |
| API-14 | `assertCompRecordComplete` · `assertChangeReasonCode` · `assertNotInClosedPeriod` · `assertNoOverlap` · `evaluateOutOfRange` · `resolveLegalMinimum` · `evaluateBelowLegalMin` · `closePreviousCompRecord` · `createCompRecord` · **ENG-SALBAND-01** · **ENG-CSQ-01** |
| API-15 | `withdrawCompRecord` · **ENG-CSQ-01** |
| API-16 | `endCompRecord` · **ENG-CSQ-01** |
| API-17 | `listRateHistory` · `renderPersonSnapshot` · `maskMoney` · `logRestrictedView` |
| API-18 | `buildListQuery` · `maskMoney` |
| API-19 | `assertNoOverlap` · `assertNotInClosedPeriod` · `createRecurringItem` · **ENG-CSQ-01** |
| API-20 | `withdrawRecurringItem` · **ENG-CSQ-01** |
| API-21 | `listConfigRefs` · `listConsumers` |
| API-22 | `setLinkStatus` · `emitAuditEvent` |
| API-23 | `invalidateConfigCache` · `resolveHrConfig` |
| API-24 | `buildRateSnapshot` · `resolveCurrentRate` · `resolveBandAt` · `computeBandBase` · `computeFteAdjustedBase` · **ENG-SALBAND-01** · `maskMoney` |
| API-25 | `buildBandSnapshot` · `resolveBandAt` |
| API-26 | `assertIdempotent` · `ingestMovementRate` (→ เส้นทาง API-14) |
| API-27 | `registerWhereUsed` |
| (scheduler) | `advanceEffectiveStates` · `evaluateRecurringEnd` — **ENG-EFFDATE-01** · **ENG-RECUR-01** |

**ทุก mutation API มี ≥1 Function/Engine · ไม่มี Function/Engine ที่ไม่ถูกเรียก** → ดู `03_LOGIC §3.3`

## §2.X Cross-Module Contract ⭐ (จาก BRD §12.1 Downstream Impact Map)

| ปลายทาง | อ่าน/เขียนอะไร | endpoint / event | ข้อผูกพันของปลายทาง |
|---|---|---|---|
| **Payroll (W4)** | อ่าน rate snapshot ณ วันงวด (`scope=company` ได้) | `GET /resolve` · ฟัง `salcomp.*` · `salrecur.*` | SS-1 ส่ง `date` · SS-2 เก็บ `version_id` ลงงวด · SS-3 ล้าง cache · **SS-6 ห้ามคำนวณ compa-ratio เอง** · หยุดหักเมื่อได้ `salrecur.ended` |
| **หนังสือรับรอง (W3)** | อ่านเงินเดือนปัจจุบัน ณ วันออกหนังสือ | `GET /resolve?scope=employee` | เก็บ `version_id` + ค่าที่พิมพ์เป็น snapshot ในเอกสาร — เอกสารเก่าต้องไม่เปลี่ยนค่า |
| **Manpower Planning (W6)** | อ่าน mid-point + headcount ต่อระดับ | `GET /bands/resolve` · ฟัง `salstruct.effective` | ห้ามใช้ค่าเฉลี่ยอัตราจริงแทน mid-point (RESTRICTED) · คำนวณงบใหม่ตั้งแต่วันมีผล ไม่ย้อนของเดิม |
| **Employee Movement (W3)** | อ่านอัตราปัจจุบัน · **เขียนอัตราใหม่** | `GET /resolve` · **`POST /rates/from-movement`** | ส่ง `Idempotency-Key = movement_doc_no` · ยกเลิกคำสั่ง → เรียก `POST /rates/{id}/withdraw` · **ห้ามคาดหวังการอนุมัติที่ฝั่งนี้** |
| **ESS Portal (W6)** | มุมมองพนักงานเอง | ผ่าน feature ต้นทาง | ไม่เรียก endpoint นี้ตรง (OQ-HR-04) |
| **HR Configuration** (ขาเข้า) | `resolve` + ลงทะเบียน where-used | `GET /hr-config/resolve` · `POST /hr-config/items/:id/usage` | ฝั่งเราทำตาม C-1…C-6 |
| **ENG-CSQ 7C** | 10 event (EC · SecC) | ตาม `CSQ_BRIEF.md §2` | ห้ามยิงท่อ OC / DC-เอกสาร / SC |
| **Policy Center** | masking · ABAC · audit | runtime | ต้องลงทะเบียน Restricted resource ก่อน go-live (OQ-FRD-05) |
