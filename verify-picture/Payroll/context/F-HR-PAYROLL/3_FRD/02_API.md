# 02_API — F-HR-PAYROLL · Payroll (เงินเดือน)

> **Audience:** BE dev (HTTP layer)
> **R8:** ไฟล์นี้เป็น **ชั้น HTTP บาง ๆ เท่านั้น** — ตรวจ schema · ตรวจสิทธิ์ · เรียก Function ใน `03_LOGIC` · จัดรูป response · **ห้ามมี business logic อยู่ในไฟล์นี้** (Phase 3.5 §G)
> **Convention:** path `/api/v1/payroll/...` · `field_key` = `snake_case` · error code = `UPPER_SNAKE`
> **ทุก endpoint บังคับ `company_id`** (multi-tenant · `OQ-HR-05`)

---

## §2.0 กติกาข้ามทุก endpoint

| # | กติกา |
|---|---|
| **A-1** | ทุก **mutation** เรียก **`F-44 guardClosedRun` เป็นบรรทัดแรก** — รอบที่ `ปิดรอบแล้ว` ตอบ `409 ERR_RUN_CLOSED_IMMUTABLE` เสมอ |
| **A-2** | ทุก response ที่มี field เป็นเงิน ผ่าน **`F-59 maskAmountByPolicy`** ก่อนออก — **ค่าเริ่มต้นคือปิดบัง** |
| **A-3** ⭐ | **`amount: null` ต้องออกไปเป็น `null` ใน JSON** — ⛔ ไม่ใช่ `0` ไม่ใช่ `""` ไม่ใช่ `"0.00"` (`PI-2`) · ค่าที่ถูก **ปิดบัง** ใช้ค่าคนละแบบ (`"masked": true` + ไม่มี field ค่า) เพื่อให้แยกจาก `null` ของ "ยังคำนวณไม่ได้" ได้ |
| **A-4** | mutation ที่มีผลข้างเคียงหนัก (`API-23` ปิดรอบ · `API-27` ออกไฟล์) รับ **`Idempotency-Key`** |
| **A-5** | ทุก mutation เขียนไทม์ไลน์ผ่าน `F-57` — **append-only** |
| **A-6** | ⛔ **ไม่มี endpoint ใดที่เขียนกลับต้นทาง** — ทุกการเรียกต้นทางเป็น `GET` (§2.4) |
| **A-7** | ⛔ **ไม่มี endpoint ลบ (`DELETE`) ที่ใดในไฟล์นี้** — soft archive เท่านั้น |

---

## §2.1 Endpoint — รอบจ่าย

### API-01 · `GET /api/v1/payroll/runs`
- **query:** `company_id` (req) · `period_code?` · `run_type?` · `run_status?` · `q?` · `page` · `page_size`
- **response:** `{items:[{run_no, run_type, period_code, scope_type, run_status, employee_count, pay_date, totals:{net_total|null|masked}, has_material_variance, uncomputable_line_count, is_simulation, created_by, created_at}], page_info}`
- **logic:** query + `F-59` | **rules:** `BR-38`

### API-02 · `GET /api/v1/payroll/runs/{run_no}`
- **response:** หัวรอบทั้งก้อน + `readiness_flags` + `uncomputable_line_count`/`uncomputable_employee_count` + `missing_config_groups[]` + `relations[]` (จากดัชนี) + `source_changed_after_calc`
- **logic:** `F-27` · `F-49` (อ่านย้อน) · `F-59`

### API-03 · `POST /api/v1/payroll/runs` **(mutation)**
- **body:** `{company_id, period_code, run_type, scope_type, employee_ids[]?, references_run_no?, is_simulation}`
- **201:** `{run_no, run_status:"ร่าง"}` · **logic:** `F-02` → `F-01` (+ `F-46`/`F-48`/`F-49` เมื่อ `run_type ∈ {ปรับปรุง, กลับรายการ}`)
- **error:** `409 ERR_PERIOD_CLOSED` · `409 ERR_DUPLICATE_REGULAR_RUN` · `422 ERR_REFERENCE_RUN_REQUIRED` · `422 ERR_REFERENCE_RUN_NOT_CLOSED` · `422 ERR_SCOPE_EMPLOYEES_REQUIRED`

### API-04 · `GET /api/v1/payroll/periods`
- **query:** `company_id` (req) · `date?`
- **response:** `{periods:[{period_code, period_from, period_to, pay_date, period_status, version_id}]}` · **logic:** `F-03`
- ⭐ **เป็น endpoint เดียวที่ให้รายการงวด — UI ไม่มีช่องพิมพ์งวด**

### API-05 · `POST /api/v1/payroll/runs/{run_no}/cancel` **(mutation)**
- **body:** `{cancel_reason}` (req) · **logic:** `F-44` → `F-04` · **error:** `422 ERR_REASON_REQUIRED` · `409 ERR_CANCEL_NOT_ALLOWED` · `409 ERR_RUN_CLOSED_IMMUTABLE`

## §2.2 Endpoint — ดึงข้อมูลและความพร้อม

### API-06 · `POST /api/v1/payroll/runs/{run_no}/pull` **(mutation · async)**
- **body:** `{sources[]?}` · **202:** `{job_id, sources_queued[]}` · **logic:** `F-44` → `F-05` → `F-06` → `F-07` → `F-10` (`ENG-PAY-03`)
- ⭐ **พารามิเตอร์ที่ส่งไปยังต้นทางทุกที่ต้องมี `pay_date` ของงวด** — ไม่ใช่ "วันนี้" (`PI-6`)
- **error:** `409 ERR_RUN_CLOSED_IMMUTABLE` · `409 ERR_PULL_NOT_ALLOWED_AFTER_SUBMIT` · `502 ERR_SOURCE_UNAVAILABLE` (ระบุ `failed_sources[]`)

### API-07 · `GET /api/v1/payroll/runs/{run_no}/snapshot`
- **response:** `{snapshots:[{source_feature, endpoint, params, called_at, row_count, period_status_at_read, version_block, hash, superseded_by}], source_version_ids, snapshot_hash}`
- ⭐ **`source_version_ids.hr_config.{sso,pit,pf,payroll_basis,payroll_deduction,payroll_review}` ต้องออกเป็น `null` ตรง ๆ** (`PI-5`)

### API-08 · `POST /api/v1/payroll/runs/{run_no}/pull/retry` **(mutation)** — `{sources[]}` · **logic:** `F-44` → `F-08`

### API-09 · `POST /api/v1/payroll/runs/{run_no}/repull` **(mutation)**
- **body:** `{reason?}` · **response:** `{cleared_line_count, superseded_snapshot_ids[]}` · **logic:** `F-44` → `F-09`
- ⭐ **ล้างผลคำนวณ · ไม่ลบ snapshot เดิม** · **error:** `409 ERR_REPULL_NOT_ALLOWED` (สถานะ ≥ `รออนุมัติ`)

### API-10 · `GET /api/v1/payroll/runs/{run_no}/readiness`
- **response:** `{rows:[{source_feature, state, flags[], affected_count, message, manage_link}], legal_config:{groups:[{group, available:false, missing_keys[]}]}, no_rate_employees[], incomplete_time_employees[], service_masked:bool}`
- **logic:** `F-11` · `F-12` · `F-13` · `F-14`

### API-11 · `GET /api/v1/payroll/runs/{run_no}/excluded` — `{excluded:[{employee_id, name, reason}]}` · **logic:** `F-10`

## §2.3 Endpoint — คำนวณ · ทบทวน · อนุมัติ · ปิดรอบ

### API-12 · `POST /api/v1/payroll/runs/{run_no}/calculate` **(mutation · async)**
- **202:** `{job_id}` → เสร็จแล้ว `{run_status:"คำนวณแล้ว", line_count, uncomputable_line_count, uncomputable_employee_count, missing_config_groups[]}`
- **logic:** `F-44` → `F-15` (`ENG-PAY-01` · `ENG-PAY-02` · `ENG-PAY-04`)
- **error:** `409 ERR_RUN_CLOSED_IMMUTABLE` · `409 ERR_SNAPSHOT_INCOMPLETE` · `403 ERR_RATE_MASKED_BLOCK_RUN`

### API-13 · `GET /api/v1/payroll/runs/{run_no}/lines`
- **query:** `employee_id?` · `line_kind?` · `line_state?` · `page` · `page_size`
- **response:** `{items:[{line_id, employee_id, employee_name_snapshot, cost_center, payroll_code, line_kind, direction, quantity, unit, rate_used, multiplier, amount, line_state, uncomputable_reason, source_ref, is_manual, version_ids_used}], totals:{gross_total, deduction_total, net_total, incomplete:bool}}`
- ⭐ **`amount` เป็น `null` เมื่อ `line_state = "ยังคำนวณไม่ได้"`** · ⭐ **`totals.incomplete = true` เมื่อรอบมีบรรทัดที่คำนวณไม่ได้ และ `net_total` เป็น `null`**

### API-14 · `GET /api/v1/payroll/runs/{run_no}/blockers`
- **response:** `{uncomputable_lines, uncomputable_employees, missing_config_groups:[{group, missing_keys[], oq_ref}], no_rate_employees[], service_masked, is_simulation}` · **logic:** `F-27` · `F-12` · `F-13`
- ⭐ เป็นแหล่งข้อมูลของ drawer **"รายการที่ต้องเคลียร์ก่อนส่งอนุมัติ"**

### API-15 · `POST /api/v1/payroll/runs/{run_no}/lines/manual` **(mutation)**
- **body:** `{employee_id, payroll_code, direction, amount, manual_reason (req), manual_doc_ref (req)}` · **logic:** `F-44` → `F-28`
- **error:** `422 ERR_MANUAL_REASON_REQUIRED` · `422 ERR_MANUAL_DOC_REQUIRED` · `409 ERR_RUN_CLOSED_IMMUTABLE`

### API-16 · `GET /api/v1/payroll/runs/{run_no}/variance`
- **response:** `{has_baseline:bool, baseline_run_no|null, by_employee[], by_payroll_code[], entrants[], leavers[], flagged[], has_material_variance: bool|null, threshold_available:bool, variance_threshold_version_id|null}`
- **logic:** `F-30` · `F-31` (`ENG-PAY-04`) · `F-59`

### API-17 · `POST /api/v1/payroll/runs/{run_no}/variance/{line_id}/review` **(mutation)** — `{note?}` · **logic:** `F-44` → `F-32`

### API-18 · `GET /api/v1/payroll/runs/{run_no}/cost-summary` — `{by_cost_center[], by_department[]}` · **logic:** `F-33` · `F-59`

### API-19 · `POST /api/v1/payroll/runs/{run_no}/submit` **(mutation)** ⭐⭐
- **body:** `{assignees:[{step, assignee_id}]}` (จาก slot picker)
- **200:** `{run_status:"รออนุมัติ", approval_action_id, approval_chain[]}`
- **409 พร้อม blockers เมื่อบล็อก:** `{code:"ERR_UNCOMPUTABLE_LINES_EXIST", uncomputable_lines, uncomputable_employees, missing_config_groups[]}`
- **logic:** `F-44` → **`F-36`** → `F-34` → `F-35` → `doa-resolve`
- **error อื่น:** `409 ERR_NO_RATE_EMPLOYEES` · `403 ERR_RATE_MASKED_BLOCK_RUN` · `409 ERR_SIMULATION_CANNOT_SUBMIT` · `422 ERR_ASSIGNEE_REQUIRED` · `409 ERR_SOD_VIOLATION`

### API-20 · `GET /api/v1/payroll/runs/{run_no}/approval`
- **response:** `{approval_action_id, action_reason, doa_resolve_payload, approval_chain:[{step, role_id, role_label, assignee_id, assignee_name, assignee_position, status, acted_at, comment}], approval_status}`
- ⭐ **`doa_resolve_payload` ถูกส่งกลับมาแสดงบนจอทั้งก้อน — ต้องไม่มี field ที่เป็นจำนวนเงิน** (`PI-9` · ตรวจได้ด้วยตาและด้วยเครื่องที่ `IA-12`)

### API-21 · `POST /api/v1/payroll/runs/{run_no}/approve` **(mutation)** — `{comment?}` · **logic:** `F-44` → `F-37`
### API-22 · `POST /api/v1/payroll/runs/{run_no}/reject` **(mutation)** — `{reject_reason (req)}` · **logic:** `F-44` → `F-38` · **error:** `422 ERR_REASON_REQUIRED`

### API-23 · `POST /api/v1/payroll/runs/{run_no}/close` **(mutation · async · Idempotency-Key)** ⭐⭐
- **202:** `{job_id}` → เสร็จแล้ว `{run_status:"ปิดรอบแล้ว", payslip_count, snapshot_hash, closed_at}`
- **logic:** `F-44` → **`F-40`** → `F-41` → `F-42` → `F-43` → `F-53` → `F-55` → `F-56`
- ⭐ **ธุรกรรมเดียว — ถ้าส่วนใดล้ม rollback ทั้งหมดและไม่ยิง event ใด ๆ**
- **error:** `409 ERR_RUN_NOT_APPROVED` · `409 ERR_SIMULATION_CANNOT_CLOSE` · `500 ERR_PAYSLIP_RENDER_FAILED` (rollback)

## §2.4 Endpoint — สลิป · ไฟล์ · บัญชี · ร่องรอย

### API-24 · `GET /api/v1/payroll/runs/{run_no}/payslips` — `{items:[{payslip_no, employee_id, employee_name_snapshot, net_total, payslip_status}]}` · **logic:** `F-54` · `F-59`
### API-25 · `GET /api/v1/payroll/payslips/{payslip_no}` — สลิปทั้งก้อน (ดู `00_OVERVIEW §0.13.2`) · **logic:** `F-54` → `F-56` (SecC เมื่อไม่ใช่เจ้าของ)
- ⭐ **`403 ERR_PAYSLIP_FORBIDDEN` เมื่อไม่มีสิทธิ์ — ไม่มี response แบบ "เอกสารที่ตัวเลขถูกปิดบัง"** (`PI-10`)
### API-26 · `GET /api/v1/payroll/payslips/{payslip_no}/pdf` — คืน **สำเนาเดิมจากคลัง** (`pdf_ref`) · ⛔ **ไม่ render ใหม่** · `403` เหมือน API-25 · **logic:** `F-54` · `F-56`
### API-34 · `GET /api/v1/payroll/payslips` — ทะเบียนสลิปข้ามรอบ · **logic:** `F-54` · `F-59`

### API-27 · `POST /api/v1/payroll/runs/{run_no}/bank-file` **(mutation · Idempotency-Key)**
- **body:** `{bank_code}` · **response:** `{file_ref, record_count, excluded:[{employee_id, name, reason:"ไม่มีเลขบัญชีธนาคาร"}], format_source:"bank_specific"|"generic_fallback"}`
- **logic:** `F-44` → `F-50` (`ENG-PAY-06`) → `F-56` (SecC `payroll.bank_file_exported`)
- ⭐ `format_source = "generic_fallback"` เมื่อ `bank_file.format_by_bank` ยังไม่มี — **ต้องแสดงบนจอว่ายังไม่ใช่รูปแบบของธนาคารใด** `[AI-DEFAULT]`
- **error:** `409 ERR_RUN_NOT_CLOSED`

### API-28 · `POST /api/v1/payroll/runs/{run_no}/bank-file/mark-sent` **(mutation)** — ⭐ **คนกดเอง** · **logic:** `F-44` → `F-51`
### API-29 · `GET /api/v1/payroll/runs/{run_no}/gl-payload` — `{status:"รอปลายทาง"|"ส่งแล้ว", entries[], balanced:bool}` · **logic:** `F-52` (`ENG-PAY-07`) · ⛔ **ไม่มี endpoint post**
### API-30 · `GET /api/v1/payroll/runs/{run_no}/timeline` — `{events:[{at, actor, action, detail}]}` (append-only) · **logic:** `F-57`
### API-31 · `GET /api/v1/payroll/adjust-queue` — `{items:[{queue_id, run_no, source_feature, event_id, employee_id, detail, occurred_at, resolved_run_no|null}]}` · **logic:** `F-45`
### API-32 · `GET /api/v1/payroll/runs/{run_no}/relations` — `{as_source:[{new_run_no, relation_kind, created_at}], as_target:{references_run_no, relation_kind}|null}` · **logic:** `F-49`
- ⭐ **`as_source` มาจาก query ย้อนบน `payroll_run_relation` — ไม่ใช่ field บนแถวของรอบเดิม** (`PI-8`)
### API-33 · `GET /api/v1/payroll/employees/{employee_id}/ytd` — ดู `00_OVERVIEW §0.13.4` · **logic:** `F-53` · `F-59`

---

## §2.5 Cross-Module Contract

### §2.5.1 ขาเข้า — อ่านอย่างเดียว (`X-API-01…X-API-07`)

| # | ปลายทาง | endpoint | พารามิเตอร์บังคับ | เรียกจาก |
|---|---|---|---|---|
| **X-API-01** | Salary Structure | `GET /api/v1/salary-structure/resolve` | `scope=company` · **`date=<pay_date>`** · `company_id` | `F-05` |
| **X-API-02** | Attendance | `GET /api/v1/attendance/periods/resolve` | **`period_code`** · `company_id` | `F-05` |
| **X-API-03** | Leave | `GET /api/v1/leave/periods/resolve` | **`period_code`** · `company_id` | `F-05` |
| **X-API-04** | OT / Shift | `GET /api/v1/ot/periods/resolve` | **`period_code`** · `company_id` | `F-05` |
| **X-API-05** | HR Configuration | `GET /api/v1/hr-config/resolve` | **`date=<pay_date>`** · `group` · `company_id` | `F-03` · `F-05` · `F-22`…`F-24` · `F-31` |
| **X-API-06** | On/Offboard | `GET /api/v1/onboard/employment-window/resolve` | **`as_of=<pay_date>`** · `scope=company` · `company_id` | `F-05` · `F-10` |
| **X-API-07** | DOA Engine | `GET /doa/resolve` | `action_id` + บริบท**ที่ไม่ใช่เงิน** | `F-35` |

⭐ **`X-API-05` ที่กลุ่ม `sso` · `pit` · `pf` · `payroll_basis` · `payroll_deduction` · `payroll_review` วันนี้คืนว่าไม่มีกลุ่มนั้น** → เข้ากติกา `03_LOGIC §3.0.1 G-1`
⛔ **ไม่มี `POST`/`PUT`/`PATCH`/`DELETE` ไปยังต้นทางใดทั้งสิ้น** — ยกเว้น `POST /<feature>/usage` ซึ่งเป็นการ **ลงทะเบียน where-used** ไม่ใช่การเขียนข้อมูล (`SS-7` · `AT-7` · `LV-7` · `OT-7` · `C-6` · `OB-6`)

### §2.5.2 ขาออก — surface ที่ปลายทางมาอ่าน

| # | ปลายทาง | อ่านอะไร | สัญญา |
|---|---|---|---|
| **X-OUT-01** | **ESS Portal** ⏳W6 | `API-34` · `API-25` · `API-26` · `API-33` | `00_OVERVIEW §0.13.2` · **all-or-nothing (403)** |
| **X-OUT-02** | **Accounting GL** ❌ | `API-29` | `00_OVERVIEW §0.13.5` · **Module Linkage ปิด · ไม่ post** |
| **X-OUT-03** | **Finance** | `API-27` (ไฟล์) · `API-28` (ยืนยันคนกดเอง) | ⛔ **ไม่มี endpoint สั่งโอน ไม่มี endpoint กระทบยอด** |
| **X-OUT-04** | **50 ทวิ / ภ.ง.ด.1ก → Accounting** | `API-33` (YTD) | เก็บให้ · **ไม่ออกแบบฟอร์ม** |
| **X-OUT-05** | **Expense Claim** ⏳ lane C | อ่านช่อง "รายการเบิกที่จ่ายผ่านเงินเดือน" ผ่าน `API-13` | Linkage ปิด → กลุ่มว่าง **ไม่บล็อก** |
| **X-OUT-06** | **ผู้ตรวจสอบ** | `GET /api/v1/payroll/runs/{run_no}/totals` (PS-2) | เฉพาะรอบที่ปิดแล้ว · `409` เมื่อยังไม่ปิด |

### §2.5.3 Event listener (ขาเข้าแบบ push)

| event ที่ฟัง | จากใคร | ทำอะไร |
|---|---|---|
| `attendance.day_adjusted` · `leave.withdrawn` · `ot.withdrawn` · `ot.hours_adjusted` · `salstruct.effective` · `ofb_case_cancelled` · `onb_start_date_changed` | ต้นทาง | **ก่อนปิดรอบ:** `F-58` ตั้งธง "ข้อมูลต้นทางเปลี่ยนหลังคำนวณ" (**ไม่แตะตัวเลข**) · **หลังปิดรอบ:** `F-45` เข้าคิวรอบปรับปรุง (**ไม่แตะตัวเลข**) |
| `hrconfig.effective` · `hrconfig.published` · `hrconfig.period_closed` | HR Configuration | ล้าง cache ของวันนั้น (`BR-03`) · ⭐ **เมื่อกลุ่ม `sso`/`pit`/`pf`/… ถูกเผยแพร่ครั้งแรก → ธง "มีค่าให้อ่านแล้ว" บนรอบที่ยังไม่ปิด** |

---

## §2.6 Error Catalog (สรุป — รายละเอียดที่ `05_RULES §5.4`)

| code | HTTP | เมื่อไร |
|---|:---:|---|
| `ERR_RUN_CLOSED_IMMUTABLE` ⭐ | 409 | คำสั่งเขียนใด ๆ บนรอบที่ปิดแล้ว (ทั้ง 6 คำสั่ง) |
| `ERR_UNCOMPUTABLE_LINES_EXIST` ⭐ | 409 | ส่งอนุมัติขณะที่ยังมีบรรทัดคำนวณไม่ได้ |
| `ERR_NO_RATE_EMPLOYEES` | 409 | ส่งอนุมัติขณะที่ยังมีคนไม่มีอัตรา ณ วันจ่าย |
| `ERR_RATE_MASKED_BLOCK_RUN` | 403 | Salary Structure คืน `masked = true` |
| `ERR_PERIOD_CLOSED` | 409 | สร้างรอบปกติบนงวดที่ปิด |
| `ERR_DUPLICATE_REGULAR_RUN` | 409 | มีรอบปกติของงวดนั้นอยู่แล้ว |
| `ERR_REFERENCE_RUN_REQUIRED` | 422 | `ปรับปรุง`/`กลับรายการ` ไม่อ้างรอบต้นฉบับ |
| `ERR_REFERENCE_RUN_NOT_CLOSED` | 422 | รอบที่อ้างยังไม่อยู่สถานะปิดรอบแล้ว |
| `ERR_SOD_VIOLATION` | 409 | ผู้จัดทำถูกเลือกเป็นผู้อนุมัติของรอบตัวเอง |
| `ERR_SIMULATION_CANNOT_SUBMIT` / `..._CLOSE` | 409 | รอบจำลอง |
| `ERR_PAYSLIP_FORBIDDEN` ⭐ | 403 | เปิดสลิปโดยไม่มีสิทธิ์ — **ไม่ส่งเอกสารมาให้** |
| `ERR_REASON_REQUIRED` | 422 | ยกเลิก/ไม่อนุมัติโดยไม่มีเหตุผล |
| `ERR_MANUAL_REASON_REQUIRED` / `..._DOC_REQUIRED` | 422 | รายการปรับด้วยมือไม่ครบ |
| `ERR_SOURCE_UNAVAILABLE` | 502 | ต้นทางเรียกไม่สำเร็จ (ระบุรายการที่ล้ม) |
| `ERR_SNAPSHOT_INCOMPLETE` | 409 | คำนวณขณะที่ snapshot ไม่ครบ 6 ต้นทาง |
| `ERR_REPULL_NOT_ALLOWED` | 409 | ดึงใหม่หลังส่งอนุมัติ |
| `ERR_RUN_NOT_CLOSED` | 409 | ขอไฟล์โอน/ยอดรวมของรอบที่ยังไม่ปิด |
| `ERR_PAYSLIP_RENDER_FAILED` | 500 | render PDF ล้มระหว่างปิดรอบ → **rollback ทั้งธุรกรรม** |
